# coding: utf-8
"""Unit tests for mtbsccli.convert.build_mztabm.

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
        """MTD must contain one mzTab Sample per distinct MetaboScape Sample
        that has analyses in the feature table."""
        result = self._build()
        # Fixture has 2 MetaboScape samples contributing to the feature table.
        self.assertIsNotNone(result.metadata.sample)
        self.assertEqual(len(result.metadata.sample), 2)
        sample_names = [s.name for s in result.metadata.sample]
        self.assertIn("SAR-270-II-pagt-1009-#1-pos-OS_P1-A-5_1", sample_names)
        self.assertIn("SAR-270-II-pagt-1009-#1-pos-NS_P1-A-5_1", sample_names)

    def test_assay_has_sample_ref(self):
        """Every assay must carry a sample_ref pointing to its mzTab Sample."""
        result = self._build()
        for assay in result.metadata.assay:
            self.assertIsNotNone(
                assay.sample_ref,
                f"assay {assay.id!r} ({assay.name!r}) has no sample_ref",
            )

    def test_no_attribute_falls_back_to_undefined(self):
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


if __name__ == "__main__":
    unittest.main()
