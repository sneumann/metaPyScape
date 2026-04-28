# coding: utf-8
"""Conversion of MetaboScape data to mzTab-M and MGF formats."""

from __future__ import annotations

import re
import urllib.parse
from typing import Dict, List, Optional

import metaPyScape
from mztab_m_io.model.common import (
    CV,
    Assay,
    Database,
    MsRun,
    Parameter,
    Software,
    StudyVariable,
)
from mztab_m_io.model.mztabm import MzTabM
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.section.smf import SmallMoleculeFeature
from mztab_m_io.model.section.sml import SmallMoleculeSummary

# Default MetaboScape software version (matches the OpenAPI spec version).
_METABOSCAPE_VERSION = "2025b"

# URI for the MetaboScape database entry (used as a required placeholder).
_METABOSCAPE_DB_URI = "https://www.bruker.com/en/products-and-solutions/mass-spectrometry/data-analysis/metaboscape.html"

# MS CV polarity term map.
_POLARITY_PARAM: Dict[str, Parameter] = {
    "POSITIVE": Parameter(
        cv_label="MS", cv_accession="MS:1000130", name="positive scan"
    ),
    "NEGATIVE": Parameter(
        cv_label="MS", cv_accession="MS:1000129", name="negative scan"
    ),
}

_MS_CV = CV(
    label="MS",
    full_name="Mass Spectrometry Ontology",
    version="4.1.38",
    uri="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo",
)


def _wrap(value) -> Optional[List]:
    """Return [value] if value is not None, else None."""
    return [value] if value is not None else None


def _primary_ion(feature):
    """Return the main FeatureIon for a feature, or None."""
    if not feature.feature_ions:
        return None
    for ion in feature.feature_ions:
        if ion.main_ion:
            return ion
    return feature.feature_ions[0]


def _db_identifier(annotation) -> Optional[str]:
    """Extract the first database identifier string from an Annotation."""
    if annotation is None or not annotation.database_identifiers:
        return None
    first = annotation.database_identifiers[0]
    if isinstance(first, dict):
        return first.get("identifier")
    return getattr(first, "identifier", None)


def _msrun_location(name: str) -> str:
    """Return a valid file URI for an analysis run name."""
    return "file:///" + urllib.parse.quote(name, safe="-._~")


def _parse_charge(ion_notation: Optional[str]) -> Optional[int]:
    """Parse the integer charge from an ion notation string.

    Examples: ``'[M+H]+'`` → ``1``, ``'[M-H]-'`` → ``-1``,
    ``'[M+2H]2+'`` → ``2``.  Returns ``None`` when the notation cannot be
    parsed.
    """
    if not ion_notation:
        return None
    notation = ion_notation.strip()
    m = re.search(r"(\d*)[+-]$", notation)
    if m:
        n = int(m.group(1)) if m.group(1) else 1
        sign = 1 if notation.endswith("+") else -1
        return sign * n
    return None


def _ionmode_string(polarity: Optional[str]) -> Optional[str]:
    """Return ``'Positive'`` or ``'Negative'`` for the MGF IONMODE field."""
    if not polarity:
        return None
    p = polarity.upper()
    if p in ("POSITIVE", "POS"):
        return "Positive"
    if p in ("NEGATIVE", "NEG"):
        return "Negative"
    return None


def _find_msms_info_for_ion(msms_info_list: list, ion) -> Optional[object]:
    """Return the FeatureIonMsMsSpectrumInfo entry that matches *ion*.

    Matching is first tried by ion ID, then falls back to the first entry that
    contains at least one spectrum with signals.
    """
    if not msms_info_list:
        return None
    ion_id = getattr(ion, "id", None) if ion is not None else None
    if ion_id:
        for info in msms_info_list:
            if getattr(getattr(info, "feature_ion", None), "id", None) == ion_id:
                if info.spectra:
                    return info
    for info in msms_info_list:
        if info.spectra:
            return info
    return None


def build_mztabm(
    project: metaPyScape.Project,
    project_info: metaPyScape.ProjectInfo,
    feature_table: list,
    samples: list,
    intensity_matrix: metaPyScape.FeatureMatrix,
    featuretable_id: str,
    polarity: Optional[str] = None,
    software_version: str = _METABOSCAPE_VERSION,
    converter_version: Optional[str] = None,
) -> MzTabM:
    """Build an :class:`MzTabM` object from MetaboScape API responses.

    Parameters
    ----------
    project:
        Project object from ``ProjectsApi.retrieve_project()``.
    project_info:
        ProjectInfo object from ``ProjectsApi.retrieve_project_info()``.
    feature_table:
        List of Feature objects from ``FeaturetableApi.retrieve_feature_table()``.
    samples:
        List of Sample objects from ``SamplesApi.list_all_samples()``.
    intensity_matrix:
        FeatureMatrix from ``FeaturetableApi.retrieve_intensity_matrix()``.
    featuretable_id:
        UUID of the feature table (used as ``mztab_id``).
    polarity:
        Scan polarity of the feature table: ``"POSITIVE"``, ``"NEGATIVE"``,
        or ``None``.  When provided, each ms_run gains a ``scan_polarity``
        entry using the appropriate MS CV term.
    software_version:
        Version string of the MetaboScape software, defaults to the value
        from the OpenAPI specification (``_METABOSCAPE_VERSION``).
    converter_version:
        Version string of the mtbsccli converter.  When provided, a second
        ``Software`` entry (``software[2]``) is added to the mzTab-M metadata
        to record the tool that performed the conversion.

    Returns
    -------
    MzTabM
        Populated mzTab-M object ready to be written with
        ``mztab_m_io.write()``.
    """
    analysis_ids: List[str] = intensity_matrix.analysis_ids or []
    ft_analysis_id_set = set(analysis_ids)

    # Build analysis-id → MetaboScape Sample lookup and collect samples that
    # have at least one analysis present in the feature table.
    analysis_to_sample: Dict[str, metaPyScape.Sample] = {}
    ft_samples_ordered: Dict[str, metaPyScape.Sample] = {}  # preserves insertion order (py3.7+)
    for sample in (samples or []):
        for analysis in (sample.analysis or []):
            if analysis.id and analysis.id in ft_analysis_id_set:
                analysis_to_sample[analysis.id] = sample
                if sample.id and sample.id not in ft_samples_ordered:
                    ft_samples_ordered[sample.id] = sample

    # Build analysis-id → display name lookup from sample metadata.
    analysis_name: Dict[str, str] = {}
    for sample in (samples or []):
        for analysis in (sample.analysis or []):
            if analysis.id:
                analysis_name[analysis.id] = analysis.name or analysis.id

    # Scan polarity parameter (may be None when polarity is unknown).
    polarity_param = _POLARITY_PARAM.get((polarity or "").upper())
    scan_polarity = [polarity_param] if polarity_param is not None else None

    # One ms_run / assay per analysis present in the feature table.
    ms_runs: List[MsRun] = []
    assays: List[Assay] = []
    for idx, aid in enumerate(analysis_ids, start=1):
        name = analysis_name.get(aid, aid)
        ms_runs.append(
            MsRun(
                id=idx,
                location=_msrun_location(name),
                scan_polarity=scan_polarity,
            )
        )
        assays.append(Assay(id=idx, name=name, ms_run_ref=[idx]))

    num_assays = len(assays) or 1

    # Build study_variable list grouped by unique attribute value.
    # Each distinct SampleAttribute.value becomes one StudyVariable whose
    # assay_refs contains every assay whose parent sample carries that value.
    # When no attributes are present a single "undefined" fallback is used.
    value_to_assay_ids: Dict[str, List[int]] = {}
    for assay_idx, aid in enumerate(analysis_ids, start=1):
        parent_sample = analysis_to_sample.get(aid)
        attrs = (parent_sample.attributes or []) if parent_sample else []
        for attr in attrs:
            if attr.value:
                value_to_assay_ids.setdefault(attr.value, []).append(assay_idx)

    if value_to_assay_ids:
        study_variables = [
            StudyVariable(
                id=sv_idx,
                name=sv_value,
                description=sv_value,
                assay_refs=sv_assay_ids,
            )
            for sv_idx, (sv_value, sv_assay_ids) in enumerate(
                value_to_assay_ids.items(), start=1
            )
        ]
    else:
        study_variables = [
            StudyVariable(
                id=1,
                name="undefined",
                description="undefined",
                assay_refs=list(range(1, num_assays + 1)),
                factors=[
                    Parameter(
                        cv_label="MS", cv_accession="MS:1001808", name="undefined"
                    )
                ],
            )
        ]
    num_study_variables = len(study_variables)

    title = getattr(project, "name", None) or featuretable_id
    description = (
        getattr(project_info, "description", None)
        or getattr(project_info, "name", None)
        or title
    )

    # Build the software list: MetaboScape as [1], mtbsccli as [2] when available.
    software_list = [
        Software(
            id=1,
            parameter=Parameter(
                cv_label="MS",
                cv_accession="MS:1000799",
                name="MetaboScape",
                value=software_version,
            ),
        )
    ]
    if converter_version is not None:
        software_list.append(
            Software(
                id=2,
                parameter=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1000799",
                    name="mtbsccli",
                    value=converter_version,
                ),
            )
        )

    MTD = Metadata(
        mztab_version="2.0.0-M",
        mztab_id=featuretable_id,
        title=title,
        description=description,
        quantification_method=Parameter(
            cv_label="MS",
            cv_accession="MS:1001834",
            name="LC-MS label-free quantitation analysis",
        ),
        software=software_list,
        ms_run=ms_runs,
        assay=assays,
        study_variable=study_variables,
        cv=[_MS_CV],
        small_molecule_quantification_unit=Parameter(
            cv_label="MS",
            cv_accession="MS:1002887",
            name="Progenesis QI normalised abundance",
        ),
        small_molecule_feature_quantification_unit=Parameter(
            cv_label="MS",
            cv_accession="MS:1002887",
            name="Progenesis QI normalised abundance",
        ),
        small_molecule_identification_reliability=Parameter(
            cv_label="MS",
            cv_accession="MS:1002896",
            name="compound identification confidence level",
        ),
        database=[
            Database(
                param=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1000799",
                    name="MetaboScape",
                    value=software_version,
                ),
                prefix="mtbsc",
                version=software_version,
                uri=_METABOSCAPE_DB_URI,
            )
        ],
        id_confidence_measure=[
            Parameter(
                cv_label="MS",
                cv_accession="MS:1002890",
                name="fragmentation score",
            )
        ],
    )

    # Build feature-id → intensity-row-index lookup.
    matrix_feature_ids: List[str] = intensity_matrix.feature_ids or []
    intensities = intensity_matrix.intensities or []
    feature_id_to_row: Dict[str, int] = {
        fid: idx for idx, fid in enumerate(matrix_feature_ids)
    }

    sml_list: List[SmallMoleculeSummary] = []
    smf_list: List[SmallMoleculeFeature] = []

    for sml_idx, feature in enumerate(feature_table or [], start=1):
        ann = feature.primary_annotation
        ion = _primary_ion(feature)

        # Intensity row for this feature (None-padded if missing).
        row_idx = feature_id_to_row.get(feature.id)
        if row_idx is not None and row_idx < len(intensities):
            abundance: Optional[List] = list(intensities[row_idx])
        else:
            abundance = [None] * num_assays

        # Chemical annotation fields.
        chemical_formula = ann.formula if ann else None
        chemical_name = ann.name if ann else None
        smiles = ann.structure_smiles if ann else None
        inchi = ann.structure_inchi if ann else None

        # Ensure theoretical_neutral_mass is null when chemical_formula is null.
        theoretical_neutral_mass = feature.mass if chemical_formula else None

        # database_identifier: use real ID if available; fall back to a dummy
        # mtbsc-prefixed placeholder when formula is known but no DB ID.
        raw_db_id = _db_identifier(ann)
        if chemical_formula and raw_db_id is None:
            db_identifier: Optional[str] = f"mtbsc:unknown_{sml_idx}"
        else:
            db_identifier = raw_db_id

        # reliability: "3" (putatively characterized) when the exact mass is
        # known (i.e. a chemical formula is available), "4" (unknown) otherwise.
        reliability = "3" if chemical_formula else "4"

        sml = SmallMoleculeSummary(
            sml_id=sml_idx,
            smf_id_refs=[sml_idx],
            database_identifier=_wrap(db_identifier),
            chemical_formula=_wrap(chemical_formula),
            smiles=_wrap(smiles),
            inchi=_wrap(inchi),
            chemical_name=_wrap(chemical_name),
            theoretical_neutral_mass=_wrap(theoretical_neutral_mass),
            adduct_ions=_wrap(ion.ion_notation if ion else None),
            reliability=reliability,
            abundance_assay=abundance,
            abundance_study_variable=[None] * num_study_variables,
            abundance_variation_study_variable=[None] * num_study_variables,
        )
        sml_list.append(sml)

        smf = SmallMoleculeFeature(
            smf_id=sml_idx,
            sml_id_refs=[sml_idx],
            adduct_ion=ion.ion_notation if ion else None,
            exp_mass_to_charge=ion.mz if ion else None,
            charge=1,
            retention_time_in_seconds=feature.rt_in_seconds,
            abundance_assay=abundance,
        )
        smf_list.append(smf)

    return MzTabM(
        metadata=MTD,
        small_molecule_summary=sml_list,
        small_molecule_feature=smf_list,
    )


def build_mgf(
    feature_table: list,
    msms_map: Dict[str, list],
    ms1_map: Dict[str, list],
    polarity: Optional[str] = None,
) -> str:
    """Build an MGF string suitable for GNPS submission.

    One ``BEGIN IONS``/``END IONS`` block is written per feature that has at
    least one MS/MS spectrum with peaks.  Features without MS/MS data are
    silently skipped.

    Parameters
    ----------
    feature_table:
        List of Feature objects from ``FeaturetableApi.retrieve_feature_table()``.
    msms_map:
        Mapping from feature ID to the list of
        ``FeatureIonMsMsSpectrumInfo`` objects returned by
        ``FeaturetableApi.retrieve_feature_ms_ms_spectra()``.
    ms1_map:
        Mapping from feature ID to the list of
        ``FeatureIonMsSpectrumInfo`` objects returned by
        ``FeaturetableApi.retrieve_feature_ion_ms_spectra()``.
        Used to look up the precursor intensity for the ``PEPMASS`` line.
    polarity:
        Scan polarity from the ``FeatureTable`` metadata attribute:
        ``"POSITIVE"``, ``"NEGATIVE"``, or ``None``.  When provided, the
        ``IONMODE`` field is included in each spectrum block.

    Returns
    -------
    str
        MGF-formatted text ready to be written to a ``.mgf`` file.

    Notes
    -----
    The following fields in the produced MGF are non-standard extensions and
    may not be recognised by all tools, but carry useful MetaboScape metadata:

    ``ADDUCT``
        Ion notation (e.g. ``[M+H]+``).
    ``CCS``
        Ion mobility collision cross-section in Å².
    ``FEATURE_ID``
        MetaboScape internal feature UUID.
    ``FORMULA``
        Molecular formula from the primary annotation.
    ``IONMODE``
        Scan polarity (``Positive`` or ``Negative``).
    ``MSLEVEL``
        Fixed value ``2``.
    """
    ion_mode = _ionmode_string(polarity)
    lines: List[str] = []

    # Counter for unannotated features only, so Feature_N numbering is
    # consistent regardless of which features happen to have annotations.
    unannotated_counter = 0

    for feat_idx, feature in enumerate(feature_table or [], start=1):
        ann = feature.primary_annotation
        has_annotation = ann is not None and (
            getattr(ann, "name", None) or getattr(ann, "formula", None)
        )

        if not has_annotation:
            unannotated_counter += 1

        msms_info_list = msms_map.get(feature.id) or []
        ion = _primary_ion(feature)
        msms_info = _find_msms_info_for_ion(msms_info_list, ion)

        if not msms_info or not msms_info.spectra:
            continue

        spectrum = msms_info.spectra[0]
        if not spectrum.signals:
            continue

        # Prefer the ion stored inside FeatureIonMsMsSpectrumInfo as it may
        # carry more complete information than the feature's own ion list.
        active_ion = getattr(msms_info, "feature_ion", None) or ion

        lines.append("BEGIN IONS")

        # TITLE: use compound name when available, otherwise Feature_N where N
        # counts only unannotated features so the numbering stays stable.
        compound_name = getattr(ann, "name", None) if ann else None
        title = compound_name if compound_name else f"Feature_{unannotated_counter}"
        lines.append(f"TITLE={title}")

        lines.append(f"SCANS={feat_idx}")
        lines.append("MSLEVEL=2")

        if ion_mode:
            lines.append(f"IONMODE={ion_mode}")

        precursor_mz = getattr(active_ion, "mz", None) if active_ion else None
        if precursor_mz is None:
            precursor_mz = feature.mass

        # Look up precursor intensity from the MS1 isotope cluster.
        precursor_intensity: Optional[float] = None
        active_ion_id = getattr(active_ion, "id", None) if active_ion else None
        for ms1_info in (ms1_map.get(feature.id) or []):
            ms1_ion = getattr(ms1_info, "feature_ion", None)
            ms1_ion_id = getattr(ms1_ion, "id", None) if ms1_ion else None
            if active_ion_id and ms1_ion_id and ms1_ion_id != active_ion_id:
                continue
            for ms1_sp in ms1_info.spectra or []:
                signals = ms1_sp.signals or []
                if signals:
                    precursor_intensity = max(
                        (s.intensity for s in signals if s.intensity is not None),
                        default=None,
                    )
                    break
            if precursor_intensity is not None:
                break

        charge = (
            _parse_charge(getattr(active_ion, "ion_notation", None))
            if active_ion
            else None
        )

        if precursor_mz is not None:
            pepmass_parts = [str(precursor_mz)]
            if precursor_intensity is not None:
                pepmass_parts.append(str(precursor_intensity))
                if charge is not None:
                    pepmass_parts.append(str(charge))
            lines.append(f"PEPMASS={' '.join(pepmass_parts)}")

        if charge is not None:
            sign = "+" if charge >= 0 else "-"
            lines.append(f"CHARGE={abs(charge)}{sign}")

        if feature.rt_in_seconds is not None:
            lines.append(f"RTINSECONDS={feature.rt_in_seconds}")

        ion_notation = getattr(active_ion, "ion_notation", None) if active_ion else None
        if ion_notation:
            lines.append(f"ADDUCT={ion_notation}")

        ccs = getattr(active_ion, "ccs", None) if active_ion else None
        if ccs is not None:
            lines.append(f"CCS={ccs}")

        if ann and getattr(ann, "formula", None):
            lines.append(f"FORMULA={ann.formula}")

        if feature.id:
            lines.append(f"FEATURE_ID={feature.id}")

        for signal in spectrum.signals:
            lines.append(f"{signal.mz}\t{signal.intensity}")

        lines.append("END IONS")
        lines.append("")

    return "\n".join(lines)
