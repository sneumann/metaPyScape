# coding: utf-8
"""Unit tests for mtbsccli.convert (build_mztabm, build_mgf, build_mat).

These tests use synthetic MetaboScape model objects built from the JSON
fixture files in test/fixtures/.  No live MetaboScape server is required.

Strategy
--------
1. Each fixture file (projects.json, featuretable.json, …) contains a
   minimal but realistic API response captured from a real server (or crafted
   by hand following the OpenAPI schema).

2. Tests construct the corresponding metaPyScape model objects directly,
   mirroring what the Swagger-generated ApiClient would return.

3. ``build_mztabm()`` is called with the mock objects and the resulting
   MzTabM is inspected for correctness.

4. For CLI integration tests the Click test runner (``CliRunner``) is used
   together with ``unittest.mock.patch`` to replace the API calls with
   values built from the same fixture data.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load(filename: str):
    with open(FIXTURES_DIR / filename) as fh:
        return json.load(fh)


def _make_project():
    """Build a metaPyScape.Project from fixtures."""
    import metaPyScape

    data = _load("project.json")
    project = metaPyScape.Project()
    project.id = data["id"]
    project.name = data["name"]
    project.experiments = []
    return project


def _make_project_info():
    """Build a metaPyScape.ProjectInfo from fixtures."""
    import metaPyScape

    data = _load("project_info.json")
    info = metaPyScape.ProjectInfo()
    info.project_id = data["project_id"]
    info.name = data["name"]
    info.description = data["description"]
    return info


def _make_annotation(ann_data: dict):
    """Build a metaPyScape.Annotation from a dict (may be None)."""
    import metaPyScape

    if ann_data is None:
        return None
    ann = metaPyScape.Annotation()
    ann.id = ann_data.get("id")
    ann.name = ann_data.get("name")
    ann.formula = ann_data.get("formula")
    ann.structure_smiles = ann_data.get("structure_smiles")
    ann.structure_inchi = ann_data.get("structure_inchi")
    ann.database_identifiers = ann_data.get("database_identifiers") or []
    return ann


def _make_feature_ion(ion_data: dict):
    """Build a metaPyScape.FeatureIon from a dict."""
    import metaPyScape

    ion = metaPyScape.FeatureIon()
    ion.id = ion_data.get("id")
    ion.ion_notation = ion_data.get("ion_notation")
    ion.mz = ion_data.get("mz")
    ion.ccs = ion_data.get("ccs")
    ion.main_ion = ion_data.get("main_ion", False)
    return ion


def _make_feature_table():
    """Build a list of metaPyScape.Feature objects from fixtures."""
    import metaPyScape

    rows = _load("featuretable.json")
    features = []
    for row in rows:
        feat = metaPyScape.Feature()
        feat.id = row["id"]
        feat.rt_in_seconds = row.get("rt_in_seconds")
        feat.mass = row.get("mass")
        feat.feature_ions = [_make_feature_ion(i) for i in (row.get("feature_ions") or [])]
        feat.primary_annotation = _make_annotation(row.get("primary_annotation"))
        feat.all_annotations = []
        feat.user_flags = []
        features.append(feat)
    return features


def _make_samples():
    """Build a list of metaPyScape.Sample objects from fixtures."""
    import metaPyScape

    rows = _load("samples.json")
    samples = []
    for row in rows:
        sample = metaPyScape.Sample()
        sample.id = row["id"]
        sample.name = row.get("name")
        sample.type = row.get("type")
        sample.analysis = []
        sample.attributes = []
        for a in row.get("analysis", []):
            analysis = metaPyScape.Analysis()
            analysis.id = a["id"]
            analysis.name = a.get("name")
            analysis.include = a.get("include", True)
            sample.analysis.append(analysis)
        for attr_data in row.get("attributes", []):
            attr = metaPyScape.SampleAttribute()
            attr.name = attr_data.get("name")
            attr.value = attr_data.get("value")
            sample.attributes.append(attr)
        samples.append(sample)
    return samples


def _make_intensity_matrix():
    """Build a metaPyScape.FeatureMatrix from fixtures."""
    import metaPyScape

    data = _load("intensity_matrix.json")
    matrix = metaPyScape.FeatureMatrix()
    matrix.intensities = data["intensities"]
    matrix.feature_ids = data["feature_ids"]
    matrix.analysis_ids = data["analysis_ids"]
    return matrix


# ---------------------------------------------------------------------------
# Tests for build_mztabm
# ---------------------------------------------------------------------------


class TestBuildMztabm(unittest.TestCase):
    """Tests for mtbsccli.convert.build_mztabm()."""

    def setUp(self):
        self.project = _make_project()
        self.project_info = _make_project_info()
        self.feature_table = _make_feature_table()
        self.samples = _make_samples()
        self.intensity_matrix = _make_intensity_matrix()
        self.featuretable_id = "ft-0001-0000-0000-000000000001"

    def _build(self):
        from mtbsccli.convert import build_mztabm

        return build_mztabm(
            project=self.project,
            project_info=self.project_info,
            feature_table=self.feature_table,
            samples=self.samples,
            intensity_matrix=self.intensity_matrix,
            featuretable_id=self.featuretable_id,
        )

    def test_returns_mztabm_instance(self):
        from mztab_m_io.model.mztabm import MzTabM

        result = self._build()
        self.assertIsInstance(result, MzTabM)

    def test_metadata_fields(self):
        result = self._build()
        mtd = result.metadata
        self.assertEqual(mtd.mztab_version, "2.0.0-M")
        self.assertEqual(mtd.mztab_id, self.featuretable_id)
        self.assertEqual(mtd.title, self.project.name)
        self.assertEqual(mtd.description, self.project_info.description)

    def test_software_version_in_parameter(self):
        """Software[1] parameter value must be the MetaboScape version string."""
        from mtbsccli.convert import _METABOSCAPE_VERSION

        result = self._build()
        sw = result.metadata.software[0]
        self.assertEqual(sw.parameter.value, _METABOSCAPE_VERSION)

    def test_msrun_location_is_valid_uri(self):
        """Every ms_run location must start with a valid scheme (file://)."""
        result = self._build()
        for ms_run in result.metadata.ms_run:
            self.assertTrue(
                ms_run.location.startswith("file:///"),
                f"location {ms_run.location!r} is not a valid file URI",
            )

    def test_msrun_scan_polarity_set_when_polarity_provided(self):
        """When polarity='POSITIVE', every ms_run must have a scan_polarity param."""
        from mtbsccli.convert import build_mztabm

        result = build_mztabm(
            project=self.project,
            project_info=self.project_info,
            feature_table=self.feature_table,
            samples=self.samples,
            intensity_matrix=self.intensity_matrix,
            featuretable_id=self.featuretable_id,
            polarity="POSITIVE",
        )
        for ms_run in result.metadata.ms_run:
            self.assertIsNotNone(ms_run.scan_polarity)
            self.assertEqual(len(ms_run.scan_polarity), 1)
            self.assertEqual(ms_run.scan_polarity[0].cv_accession, "MS:1000130")

    def test_msrun_scan_polarity_negative(self):
        """When polarity='NEGATIVE', every ms_run must have the negative scan CV term."""
        from mtbsccli.convert import build_mztabm

        result = build_mztabm(
            project=self.project,
            project_info=self.project_info,
            feature_table=self.feature_table,
            samples=self.samples,
            intensity_matrix=self.intensity_matrix,
            featuretable_id=self.featuretable_id,
            polarity="NEGATIVE",
        )
        for ms_run in result.metadata.ms_run:
            self.assertIsNotNone(ms_run.scan_polarity)
            self.assertEqual(ms_run.scan_polarity[0].cv_accession, "MS:1000129")

    def test_database_prefix_mtbsc(self):
        """database[1]-prefix must be 'mtbsc'."""
        result = self._build()
        self.assertEqual(result.metadata.database[0].prefix, "mtbsc")

    def test_database_uri_not_null(self):
        """database[1]-uri must be a non-null, non-empty string."""
        result = self._build()
        uri = result.metadata.database[0].uri
        self.assertIsNotNone(uri)
        self.assertNotEqual(uri, "null")
        self.assertTrue(uri.startswith("http"))

    def test_database_software_version(self):
        """database[1] version and param value must match the software version."""
        from mtbsccli.convert import _METABOSCAPE_VERSION

        result = self._build()
        db = result.metadata.database[0]
        self.assertEqual(db.version, _METABOSCAPE_VERSION)
        self.assertEqual(db.param.value, _METABOSCAPE_VERSION)

    def test_metadata_assays_match_analyses(self):
        """One assay per analysis_id in the intensity matrix."""
        result = self._build()
        n_analyses = len(self.intensity_matrix.analysis_ids)
        self.assertEqual(len(result.metadata.assay), n_analyses)
        self.assertEqual(len(result.metadata.ms_run), n_analyses)

    def test_study_variable_covers_all_assays(self):
        result = self._build()
        # All assay refs across all study variables must cover every assay.
        all_assay_refs = set()
        for sv in result.metadata.study_variable:
            all_assay_refs.update(sv.assay_refs)
        n_assays = len(result.metadata.assay)
        self.assertEqual(all_assay_refs, set(range(1, n_assays + 1)))

    def test_study_variable_names_from_attribute_values(self):
        """study_variable names must be derived from sample attribute values."""
        result = self._build()
        sv_names = [sv.name for sv in result.metadata.study_variable]
        # Fixture has two samples with attribute values "OS" and "NS".
        self.assertIn("OS", sv_names)
        self.assertIn("NS", sv_names)

    def test_study_variable_description_matches_name(self):
        """Each study_variable must have a description equal to its name."""
        result = self._build()
        for sv in result.metadata.study_variable:
            self.assertEqual(
                sv.description,
                sv.name,
                f"study_variable {sv.id!r} description does not match name",
            )

    def test_study_variable_assay_refs_match_attribute_values(self):
        """Each study_variable's assay_refs must include only assays from samples
        that carry the matching attribute value."""
        result = self._build()
        n_assays = len(result.metadata.assay)
        # Fixture splits 18 analyses evenly (9 OS, 9 NS).
        self.assertEqual(n_assays, 18)
        sv_by_name = {sv.name: sv for sv in result.metadata.study_variable}
        self.assertEqual(len(sv_by_name["OS"].assay_refs), 9)
        self.assertEqual(len(sv_by_name["NS"].assay_refs), 9)
        # The two groups must be disjoint and together cover all assays.
        os_refs = set(sv_by_name["OS"].assay_refs)
        ns_refs = set(sv_by_name["NS"].assay_refs)
        self.assertEqual(os_refs & ns_refs, set())
        self.assertEqual(os_refs | ns_refs, set(range(1, n_assays + 1)))

    def test_sample_entries_in_metadata(self):
        """MTD must not contain any mzTab Sample entries."""
        result = self._build()
        self.assertIsNone(result.metadata.sample)

    def test_assay_has_no_sample_ref(self):
        """Assays must not carry a sample_ref."""
        result = self._build()
        for assay in result.metadata.assay:
            self.assertIsNone(
                assay.sample_ref,
                f"assay {assay.id!r} ({assay.name!r}) has unexpected sample_ref",
            )

    def test_missing_attributes_create_undefined_study_variable(self):
        """When no sample attributes are present a single 'undefined' study
        variable covering all assays must be produced."""
        from mtbsccli.convert import build_mztabm

        # Strip all attributes from the samples.
        for sample in self.samples:
            sample.attributes = []

        result = build_mztabm(
            project=self.project,
            project_info=self.project_info,
            feature_table=self.feature_table,
            samples=self.samples,
            intensity_matrix=self.intensity_matrix,
            featuretable_id=self.featuretable_id,
        )
        self.assertEqual(len(result.metadata.study_variable), 1)
        self.assertEqual(result.metadata.study_variable[0].name, "undefined")
        n_assays = len(result.metadata.assay)
        self.assertEqual(
            result.metadata.study_variable[0].assay_refs,
            list(range(1, n_assays + 1)),
        )

    def test_sml_count_matches_features(self):
        result = self._build()
        self.assertEqual(
            len(result.small_molecule_summary), len(self.feature_table)
        )

    def test_smf_count_matches_features(self):
        result = self._build()
        self.assertEqual(
            len(result.small_molecule_feature), len(self.feature_table)
        )

    def test_sml_annotated_feature_fields(self):
        """Feature at index 42 (Kinetin) has a primary annotation; check chemical fields."""
        result = self._build()
        sml = result.small_molecule_summary[42]
        self.assertEqual(sml.sml_id, 43)
        self.assertIsNotNone(sml.chemical_name)
        self.assertIn("Kinetin", sml.chemical_name)
        self.assertIsNotNone(sml.chemical_formula)
        self.assertIn("C10H9N5O", sml.chemical_formula)
        # Kinetin in the fixture has no SMILES/InChI/database_identifiers
        self.assertIsNone(sml.smiles)
        self.assertIsNone(sml.inchi)
        # No real db ID → dummy mtbsc placeholder assigned
        self.assertIsNotNone(sml.database_identifier)
        self.assertIn("mtbsc:unknown_43", sml.database_identifier)

    def test_sml_unannotated_feature_fields(self):
        """First feature has no primary annotation; chemical fields must be None."""
        result = self._build()
        sml = result.small_molecule_summary[0]
        self.assertIsNone(sml.chemical_name)
        self.assertIsNone(sml.chemical_formula)

    def test_sml_theoretical_neutral_mass_null_when_no_formula(self):
        """theoretical_neutral_mass must be None when chemical_formula is None."""
        result = self._build()
        sml = result.small_molecule_summary[0]
        # Unannotated feature: no formula, so mass must also be None.
        self.assertIsNone(sml.chemical_formula)
        self.assertIsNone(sml.theoretical_neutral_mass)

    def test_sml_theoretical_neutral_mass_set_when_formula(self):
        """theoretical_neutral_mass must be set when chemical_formula is provided."""
        result = self._build()
        sml = result.small_molecule_summary[42]
        # Kinetin: formula is known, so mass must be non-None.
        self.assertIsNotNone(sml.chemical_formula)
        self.assertIsNotNone(sml.theoretical_neutral_mass)

    def test_sml_db_id_real_when_available(self):
        """When a real database_identifier is available it should be used as-is."""
        rows = _load("featuretable.json")
        # Find first feature with a non-null database_identifier.
        real_id_idx = None
        expected_id = None
        for i, row in enumerate(rows):
            ann = row.get("primary_annotation") or {}
            ids = ann.get("database_identifiers") or []
            if ids:
                real_id_idx = i
                expected_id = ids[0].get("identifier")
                break
        if real_id_idx is None:
            self.skipTest("No feature with real database_identifier in fixture.")
        result = self._build()
        sml = result.small_molecule_summary[real_id_idx]
        self.assertIn(expected_id, sml.database_identifier)

    def test_sml_abundance_study_variable_columns(self):
        """Each SML must have abundance_study_variable and abundance_variation columns."""
        result = self._build()
        n_sv = len(result.metadata.study_variable)
        for sml in result.small_molecule_summary:
            self.assertIsNotNone(sml.abundance_study_variable)
            self.assertEqual(len(sml.abundance_study_variable), n_sv)
            self.assertIsNotNone(sml.abundance_variation_study_variable)
            self.assertEqual(len(sml.abundance_variation_study_variable), n_sv)

    def test_sml_abundance_assay_length(self):
        """Each SML row must have one abundance value per assay."""
        result = self._build()
        n_assays = len(result.metadata.assay)
        for sml in result.small_molecule_summary:
            self.assertEqual(len(sml.abundance_assay), n_assays)

    def test_sml_reliability_annotated(self):
        """Annotated feature (formula known) must have reliability '3' (putatively characterized)."""
        result = self._build()
        sml = result.small_molecule_summary[42]
        self.assertIsNotNone(sml.chemical_formula)
        self.assertEqual(sml.reliability, "3")

    def test_sml_reliability_unannotated(self):
        """Unannotated feature (no formula) must have reliability '4' (unknown)."""
        result = self._build()
        sml = result.small_molecule_summary[0]
        self.assertIsNone(sml.chemical_formula)
        self.assertEqual(sml.reliability, "4")

    def test_sml_reliability_never_none(self):
        """Every SML row must have a non-None reliability value."""
        result = self._build()
        for sml in result.small_molecule_summary:
            self.assertIsNotNone(sml.reliability)
            self.assertIn(sml.reliability, ("3", "4"))

    def test_smf_retention_time(self):
        result = self._build()
        smf = result.small_molecule_feature[0]
        self.assertAlmostEqual(smf.retention_time_in_seconds, 31.070858001708984, places=3)

    def test_smf_mz(self):
        result = self._build()
        smf = result.small_molecule_feature[0]
        self.assertAlmostEqual(smf.exp_mass_to_charge, 104.10685559415053, places=3)

    def test_no_feature_ions(self):
        """Feature with empty feature_ions list must not raise."""
        self.feature_table[0].feature_ions = []
        result = self._build()
        smf = result.small_molecule_feature[0]
        self.assertIsNone(smf.exp_mass_to_charge)
        self.assertIsNone(smf.adduct_ion)

    def test_missing_intensity_row(self):
        """Feature whose id is absent from the matrix gets None abundances."""
        self.feature_table[0].id = "nonexistent-id"
        result = self._build()
        sml = result.small_molecule_summary[0]
        n_assays = len(result.metadata.assay)
        self.assertEqual(len(sml.abundance_assay), n_assays)
        self.assertTrue(all(v is None for v in sml.abundance_assay))

    def test_empty_samples(self):
        """No samples should still produce a single default assay."""
        self.samples = []
        self.intensity_matrix.analysis_ids = []
        self.intensity_matrix.intensities = []
        result = self._build()
        # metadata is still valid (no assays)
        self.assertIsNotNone(result.metadata)

    def test_write_tsv(self):
        """build_mztabm output can be written to TSV without errors."""
        import mztab_m_io as mztabm

        result = self._build()
        with tempfile.NamedTemporaryFile(suffix=".mztab", delete=False) as fh:
            path = fh.name
        try:
            _ = mztabm.write(result, path, format="tsv")
            self.assertTrue(os.path.exists(path))
        finally:
            os.unlink(path)

    def test_write_json(self):
        """build_mztabm output can be written to JSON without errors."""
        import mztab_m_io as mztabm

        result = self._build()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            path = fh.name
        try:
            _ = mztabm.write(result, path, format="json")
            self.assertTrue(os.path.exists(path))
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# CLI integration tests (no server required)
# ---------------------------------------------------------------------------


class TestConvert2MztabmCli(unittest.TestCase):
    """Test the convert2mztabm Click command with mocked API calls."""

    def _run_cli(self, args, featuretable_id="ft-0001-0000-0000-000000000001"):
        from click.testing import CliRunner
        from mtbsccli.cli import cli

        project = _make_project()
        project_info = _make_project_info()
        feature_table = _make_feature_table()
        samples = _make_samples()
        intensity_matrix = _make_intensity_matrix()

        with patch("metaPyScape.ProjectsApi") as MockProj, patch(
            "metaPyScape.FeaturetableApi"
        ) as MockFt, patch("metaPyScape.SamplesApi") as MockSamp, patch(
            "mtbsccli.cli._make_client"
        ) as MockClient:
            MockClient.return_value = MagicMock()
            mock_proj_instance = MagicMock()
            mock_proj_instance.retrieve_project.return_value = project
            mock_proj_instance.retrieve_project_info.return_value = project_info
            MockProj.return_value = mock_proj_instance

            mock_ft_instance = MagicMock()
            mock_ft_instance.retrieve_feature_table.return_value = feature_table
            mock_ft_instance.retrieve_intensity_matrix.return_value = intensity_matrix
            MockFt.return_value = mock_ft_instance

            mock_samp_instance = MagicMock()
            mock_samp_instance.list_all_samples.return_value = samples
            MockSamp.return_value = mock_samp_instance

            runner = CliRunner()
            result = runner.invoke(cli, args, catch_exceptions=False)
            return result

    def test_convert_tsv(self):
        with tempfile.NamedTemporaryFile(suffix=".mztab", delete=False) as fh:
            path = fh.name
        os.unlink(path)
        try:
            result = self._run_cli(
                [
                    "convert2mztabm",
                    "proj-0001-0000-0000-000000000001",
                    "ft-0001-0000-0000-000000000001",
                    "-f", path,
                ]
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_convert_json(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            path = fh.name
        os.unlink(path)
        try:
            result = self._run_cli(
                [
                    "-o", "json",
                    "convert2mztabm",
                    "proj-0001-0000-0000-000000000001",
                    "ft-0001-0000-0000-000000000001",
                    "-f", path,
                ]
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.unlink(path)


# ---------------------------------------------------------------------------
# Helpers for build_mgf / build_mat tests
# ---------------------------------------------------------------------------


def _make_signal(mz: float, intensity: float):
    """Build a metaPyScape.Signal."""
    import metaPyScape

    s = metaPyScape.Signal()
    s.mz = mz
    s.intensity = intensity
    s.width = 0.0
    return s


def _make_msms_spectrum(signals):
    """Build a metaPyScape.MsMsSpectrum with the given Signal list."""
    import metaPyScape

    sp = metaPyScape.MsMsSpectrum()
    sp.signals = signals
    return sp


def _make_ms_spectrum(signals, analysis_id=None, mean_measured_mz=None,
                      rt_in_seconds=None, ccs=None):
    """Build a metaPyScape.MsSpectrum."""
    import metaPyScape

    sp = metaPyScape.MsSpectrum()
    sp.signals = signals
    sp.analysis_id = analysis_id
    sp.mean_measured_mz = mean_measured_mz
    sp.rt_in_seconds = rt_in_seconds
    sp.ccs = ccs
    return sp


def _make_msms_info(feature_id, feature_ion, spectra):
    """Build a metaPyScape.FeatureIonMsMsSpectrumInfo."""
    import metaPyScape

    info = metaPyScape.FeatureIonMsMsSpectrumInfo()
    info.feature_id = feature_id
    info.feature_ion = feature_ion
    info.spectra = spectra
    return info


def _make_ms1_info(feature_id, feature_ion, spectra):
    """Build a metaPyScape.FeatureIonMsSpectrumInfo."""
    import metaPyScape

    info = metaPyScape.FeatureIonMsSpectrumInfo()
    info.feature_id = feature_id
    info.feature_ion = feature_ion
    info.spectra = spectra
    return info


# ---------------------------------------------------------------------------
# Tests for build_mgf
# ---------------------------------------------------------------------------


class TestBuildMgf(unittest.TestCase):
    """Tests for mtbsccli.convert.build_mgf()."""

    def setUp(self):
        self.feature_table = _make_feature_table()

        # Build a minimal msms_map: every feature gets one MS/MS spectrum
        # with two peaks.
        self.msms_map = {}
        for feat in self.feature_table:
            ion = feat.feature_ions[0] if feat.feature_ions else None
            signals = [_make_signal(100.0, 500.0), _make_signal(150.0, 1000.0)]
            sp = _make_msms_spectrum(signals)
            info = _make_msms_info(feat.id, ion, [sp])
            self.msms_map[feat.id] = [info]

    def _build(self, polarity=None):
        from mtbsccli.convert import build_mgf

        return build_mgf(self.feature_table, self.msms_map, polarity=polarity)

    def test_returns_string(self):
        result = self._build()
        self.assertIsInstance(result, str)

    def test_contains_begin_end_ions(self):
        result = self._build()
        self.assertIn("BEGIN IONS", result)
        self.assertIn("END IONS", result)

    def test_block_count_matches_features_with_msms(self):
        """One BEGIN IONS block per feature that has MS/MS data."""
        result = self._build()
        self.assertEqual(result.count("BEGIN IONS"), len(self.feature_table))

    def test_peaks_present(self):
        result = self._build()
        self.assertIn("100.0\t500.0", result)
        self.assertIn("150.0\t1000.0", result)

    def test_pepmass_is_ion_mz(self):
        result = self._build()
        # First feature ion mz: 104.10685559415053
        self.assertIn("PEPMASS=104.10685559415053", result)

    def test_rtinseconds_present(self):
        result = self._build()
        # First feature rt: 31.070858001708984
        self.assertIn("RTINSECONDS=31.070858001708984", result)

    def test_charge_parsed_from_m_plus_h(self):
        """'[M+H]+' ion notation must produce CHARGE=1+."""
        result = self._build()
        self.assertIn("CHARGE=1+", result)

    def test_ionmode_from_polarity_positive(self):
        result = self._build(polarity="POSITIVE")
        self.assertIn("IONMODE=Positive", result)

    def test_ionmode_from_polarity_negative(self):
        # Override every ion notation to negative so IONMODE is inferred
        for feat in self.feature_table:
            if feat.feature_ions:
                feat.feature_ions[0]._ion_notation = "[M-H]-"
        result = self._build(polarity="NEGATIVE")
        self.assertIn("IONMODE=Negative", result)

    def test_ionmode_inferred_without_polarity_arg(self):
        """IONMODE must be inferred from '[M+H]+' even when polarity=None."""
        result = self._build(polarity=None)
        self.assertIn("IONMODE=Positive", result)

    def test_adduct_present(self):
        result = self._build()
        self.assertIn("ADDUCT=[M+H]+", result)

    def test_ccs_present_when_available(self):
        result = self._build()
        # First feature ion ccs: 161.7107391357422
        self.assertIn("CCS=161.7107391357422", result)

    def test_annotation_name_in_block(self):
        """Annotated feature (Kinetin, index 42) must include NAME field."""
        result = self._build()
        self.assertIn("NAME=Kinetin", result)

    def test_annotation_formula_in_block(self):
        result = self._build()
        self.assertIn("FORMULA=C10H9N5O", result)

    def test_feature_id_field(self):
        result = self._build()
        feat0_id = self.feature_table[0].id
        self.assertIn(f"FEATURE_ID={feat0_id}", result)

    def test_feature_without_msms_is_skipped(self):
        """A feature with an empty spectra list must not appear in the output."""
        first_id = self.feature_table[0].id
        self.msms_map[first_id] = []
        result = self._build()
        # One fewer block expected.
        self.assertEqual(result.count("BEGIN IONS"), len(self.feature_table) - 1)

    def test_empty_feature_table(self):
        from mtbsccli.convert import build_mgf

        result = build_mgf([], {})
        self.assertEqual(result.strip(), "")

    def test_no_msms_map_entries_produces_empty_output(self):
        from mtbsccli.convert import build_mgf

        result = build_mgf(self.feature_table, {})
        self.assertEqual(result.strip(), "")


# ---------------------------------------------------------------------------
# Tests for build_mat
# ---------------------------------------------------------------------------


class TestBuildMat(unittest.TestCase):
    """Tests for mtbsccli.convert.build_mat()."""

    def setUp(self):
        self.feature_table = _make_feature_table()

        self.msms_map = {}
        self.ms1_map = {}
        for feat in self.feature_table:
            ion = feat.feature_ions[0] if feat.feature_ions else None

            ms2_signals = [_make_signal(100.0, 500.0), _make_signal(150.0, 1000.0)]
            ms2_sp = _make_msms_spectrum(ms2_signals)
            msms_info = _make_msms_info(feat.id, ion, [ms2_sp])
            self.msms_map[feat.id] = [msms_info]

            ms1_signals = [
                _make_signal(104.1, 10000.0),
                _make_signal(105.1, 1000.0),
            ]
            ms1_sp = _make_ms_spectrum(ms1_signals)
            ms1_info = _make_ms1_info(feat.id, ion, [ms1_sp])
            self.ms1_map[feat.id] = [ms1_info]

    def _build(self, polarity=None):
        from mtbsccli.convert import build_mat

        return build_mat(
            self.feature_table, self.msms_map, self.ms1_map, polarity=polarity
        )

    def test_returns_string(self):
        result = self._build()
        self.assertIsInstance(result, str)

    def test_compound_block_count(self):
        result = self._build()
        self.assertEqual(result.count(">compound "), len(self.feature_table))

    def test_parentmass_present(self):
        result = self._build()
        # First feature mass: 103.09957914192053
        self.assertIn(">parentmass 103.09957914192053", result)

    def test_charge_from_positive_ion_notation(self):
        result = self._build()
        self.assertIn(">charge 1", result)

    def test_charge_from_negative_ion_notation(self):
        for feat in self.feature_table:
            if feat.feature_ions:
                feat.feature_ions[0]._ion_notation = "[M-H]-"
        result = self._build()
        self.assertIn(">charge -1", result)

    def test_charge_fallback_to_polarity(self):
        """When ion_notation has no charge, polarity argument must be used."""
        for feat in self.feature_table:
            if feat.feature_ions:
                feat.feature_ions[0]._ion_notation = None
        result = self._build(polarity="NEGATIVE")
        self.assertIn(">charge -1", result)

    def test_rt_present(self):
        result = self._build()
        self.assertIn(">rt 31.070858001708984", result)

    def test_ionization_present(self):
        result = self._build()
        self.assertIn(">ionization [M+H]+", result)

    def test_ccs_present(self):
        result = self._build()
        self.assertIn(">ccs 161.7107391357422", result)

    def test_annotation_formula_in_block(self):
        result = self._build()
        self.assertIn(">formula C10H9N5O", result)

    def test_ms1_section_present(self):
        result = self._build()
        self.assertIn(">ms1", result)

    def test_ms1_peaks_present(self):
        result = self._build()
        self.assertIn("104.1 10000.0", result)
        self.assertIn("105.1 1000.0", result)

    def test_ms2_section_present(self):
        result = self._build()
        self.assertIn(">ms2", result)

    def test_ms2_peaks_present(self):
        result = self._build()
        self.assertIn("100.0 500.0", result)
        self.assertIn("150.0 1000.0", result)

    def test_annotated_compound_name_used(self):
        """Annotated feature (Kinetin) must use compound name, not UUID."""
        result = self._build()
        self.assertIn(">compound Kinetin", result)

    def test_unannotated_feature_uses_id(self):
        """Unannotated feature must use the feature UUID as compound name."""
        first_feat = self.feature_table[0]
        self.assertIsNone(first_feat.primary_annotation)
        result = self._build()
        self.assertIn(f">compound {first_feat.id}", result)

    def test_feature_without_msms_is_skipped(self):
        first_id = self.feature_table[0].id
        self.msms_map[first_id] = []
        result = self._build()
        self.assertEqual(result.count(">compound "), len(self.feature_table) - 1)

    def test_no_ms1_still_writes_ms2(self):
        from mtbsccli.convert import build_mat

        result = build_mat(self.feature_table, self.msms_map, {})
        self.assertIn(">ms2", result)
        self.assertNotIn(">ms1", result)

    def test_empty_feature_table(self):
        from mtbsccli.convert import build_mat

        result = build_mat([], {}, {})
        self.assertEqual(result.strip(), "")


# ---------------------------------------------------------------------------
# CLI integration tests for convert2mgf
# ---------------------------------------------------------------------------


class TestConvert2MgfCli(unittest.TestCase):
    """Test the convert2mgf Click command with mocked API calls."""

    def _run_cli(self, args):
        from click.testing import CliRunner
        from mtbsccli.cli import cli

        feature_table = _make_feature_table()

        def _mock_msms(feature_id):
            feat = next((f for f in feature_table if f.id == feature_id), None)
            if feat is None:
                return []
            ion = feat.feature_ions[0] if feat.feature_ions else None
            signals = [_make_signal(100.0, 500.0), _make_signal(150.0, 1000.0)]
            sp = _make_msms_spectrum(signals)
            return [_make_msms_info(feature_id, ion, [sp])]

        with patch("metaPyScape.FeaturetableApi") as MockFt, patch(
            "mtbsccli.cli._make_client"
        ) as MockClient:
            MockClient.return_value = MagicMock()
            mock_ft_instance = MagicMock()
            mock_ft_instance.retrieve_feature_table.return_value = feature_table
            mock_ft_instance.retrieve_feature_ms_ms_spectra.side_effect = _mock_msms
            MockFt.return_value = mock_ft_instance

            runner = CliRunner()
            result = runner.invoke(cli, args, catch_exceptions=False)
            return result

    def test_creates_mgf_file(self):
        with tempfile.NamedTemporaryFile(suffix=".mgf", delete=False) as fh:
            path = fh.name
        os.unlink(path)
        try:
            result = self._run_cli(
                ["convert2mgf", "ft-0001-0000-0000-000000000001", "-f", path]
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertTrue(os.path.exists(path))
            content = open(path).read()
            self.assertIn("BEGIN IONS", content)
            self.assertIn("END IONS", content)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_mgf_with_polarity_flag(self):
        with tempfile.NamedTemporaryFile(suffix=".mgf", delete=False) as fh:
            path = fh.name
        os.unlink(path)
        try:
            result = self._run_cli(
                [
                    "convert2mgf",
                    "ft-0001-0000-0000-000000000001",
                    "-f", path,
                    "-p", "POSITIVE",
                ]
            )
            self.assertEqual(result.exit_code, 0, result.output)
            content = open(path).read()
            self.assertIn("IONMODE=Positive", content)
        finally:
            if os.path.exists(path):
                os.unlink(path)


# ---------------------------------------------------------------------------
# CLI integration tests for convert2mat
# ---------------------------------------------------------------------------


class TestConvert2MatCli(unittest.TestCase):
    """Test the convert2mat Click command with mocked API calls."""

    def _run_cli(self, args):
        from click.testing import CliRunner
        from mtbsccli.cli import cli

        feature_table = _make_feature_table()

        def _mock_msms(feature_id):
            feat = next((f for f in feature_table if f.id == feature_id), None)
            if feat is None:
                return []
            ion = feat.feature_ions[0] if feat.feature_ions else None
            signals = [_make_signal(100.0, 500.0), _make_signal(150.0, 1000.0)]
            sp = _make_msms_spectrum(signals)
            return [_make_msms_info(feature_id, ion, [sp])]

        def _mock_ms1(feature_id):
            feat = next((f for f in feature_table if f.id == feature_id), None)
            if feat is None:
                return []
            ion = feat.feature_ions[0] if feat.feature_ions else None
            signals = [_make_signal(104.1, 10000.0), _make_signal(105.1, 500.0)]
            sp = _make_ms_spectrum(signals)
            return [_make_ms1_info(feature_id, ion, [sp])]

        with patch("metaPyScape.FeaturetableApi") as MockFt, patch(
            "mtbsccli.cli._make_client"
        ) as MockClient:
            MockClient.return_value = MagicMock()
            mock_ft_instance = MagicMock()
            mock_ft_instance.retrieve_feature_table.return_value = feature_table
            mock_ft_instance.retrieve_feature_ms_ms_spectra.side_effect = _mock_msms
            mock_ft_instance.retrieve_feature_ion_ms_spectra.side_effect = _mock_ms1
            MockFt.return_value = mock_ft_instance

            runner = CliRunner()
            result = runner.invoke(cli, args, catch_exceptions=False)
            return result

    def test_creates_mat_file(self):
        with tempfile.NamedTemporaryFile(suffix=".ms", delete=False) as fh:
            path = fh.name
        os.unlink(path)
        try:
            result = self._run_cli(
                ["convert2mat", "ft-0001-0000-0000-000000000001", "-f", path]
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertTrue(os.path.exists(path))
            content = open(path).read()
            self.assertIn(">compound ", content)
            self.assertIn(">ms1", content)
            self.assertIn(">ms2", content)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_mat_with_polarity_flag(self):
        with tempfile.NamedTemporaryFile(suffix=".ms", delete=False) as fh:
            path = fh.name
        os.unlink(path)
        try:
            result = self._run_cli(
                [
                    "convert2mat",
                    "ft-0001-0000-0000-000000000001",
                    "-f", path,
                    "-p", "NEGATIVE",
                ]
            )
            self.assertEqual(result.exit_code, 0, result.output)
        finally:
            if os.path.exists(path):
                os.unlink(path)


if __name__ == "__main__":
    unittest.main()
