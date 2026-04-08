# coding: utf-8
"""Conversion of MetaboScape data to mzTab-M format."""

from __future__ import annotations

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


def build_mztabm(
    project: metaPyScape.Project,
    project_info: metaPyScape.ProjectInfo,
    feature_table: list,
    samples: list,
    intensity_matrix: metaPyScape.FeatureMatrix,
    featuretable_id: str,
    polarity: Optional[str] = None,
    software_version: str = _METABOSCAPE_VERSION,
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

    Returns
    -------
    MzTabM
        Populated mzTab-M object ready to be written with
        ``mztab_m_io.write()``.
    """
    analysis_ids: List[str] = intensity_matrix.analysis_ids or []

    # Build analysis-id → display name lookup from sample metadata.
    analysis_name: Dict[str, str] = {}
    for sample in (samples or []):
        for analysis in (sample.analysis or []):
            if analysis.id:
                analysis_name[analysis.id] = analysis.name or analysis.id

    # Scan polarity parameter (may be None when polarity is unknown).
    polarity_param = _POLARITY_PARAM.get((polarity or "").upper())
    scan_polarity = [polarity_param] if polarity_param is not None else None

    # One ms_run / assay per analysis.
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

    study_variables = [
        StudyVariable(
            id=1,
            name="undefined",
            assay_refs=list(range(1, num_assays + 1)),
            factors=[
                Parameter(cv_label="MS", cv_accession="MS:1001808", name="undefined")
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
        software=[
            Software(
                id=1,
                parameter=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1000799",
                    name="MetaboScape",
                    value=software_version,
                ),
            )
        ],
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
