# coding: utf-8
"""Tests for mtbsccli version flags, -h alias, and mzTab-M second software entry."""

from __future__ import annotations

import importlib
import unittest

from click.testing import CliRunner

import metaPyScape
from mtbsccli import __version__
from mtbsccli.cli import cli

_MZTABM_AVAILABLE = importlib.util.find_spec("mztab_m_io") is not None


class TestVersionFlag(unittest.TestCase):
    """--version / -v must display mtbsccli version and pymzTabM version."""

    def _invoke(self, flag):
        return CliRunner().invoke(cli, [flag])

    def test_version_long(self):
        r = self._invoke("--version")
        self.assertEqual(r.exit_code, 0)
        self.assertIn("mtbsccli", r.output)
        self.assertIn(__version__, r.output)

    def test_version_short(self):
        r = self._invoke("-v")
        self.assertEqual(r.exit_code, 0)
        self.assertIn("mtbsccli", r.output)
        self.assertIn(__version__, r.output)

    def test_version_mentions_pymztabm(self):
        r = self._invoke("--version")
        self.assertIn("pymzTabM", r.output)

    def test_version_string_is_0_1(self):
        self.assertEqual(__version__, "0.1")
        r = self._invoke("--version")
        self.assertIn("0.1", r.output)


class TestHelpAlias(unittest.TestCase):
    """-h must be a valid alias for --help at root and sub-group level."""

    def test_root_help_long(self):
        r = CliRunner().invoke(cli, ["--help"])
        self.assertEqual(r.exit_code, 0)
        self.assertIn("Usage", r.output)

    def test_root_help_short(self):
        r = CliRunner().invoke(cli, ["-h"])
        self.assertEqual(r.exit_code, 0)
        self.assertIn("Usage", r.output)
        # Both outputs should be identical
        r_long = CliRunner().invoke(cli, ["--help"])
        self.assertEqual(r.output, r_long.output)

    def test_get_group_help_long(self):
        r = CliRunner().invoke(cli, ["get", "--help"])
        self.assertEqual(r.exit_code, 0)
        self.assertIn("Usage", r.output)

    def test_get_group_help_short(self):
        r = CliRunner().invoke(cli, ["get", "-h"])
        self.assertEqual(r.exit_code, 0)
        self.assertIn("Usage", r.output)
        r_long = CliRunner().invoke(cli, ["get", "--help"])
        self.assertEqual(r.output, r_long.output)

    def test_config_group_help_short(self):
        r = CliRunner().invoke(cli, ["config", "-h"])
        self.assertEqual(r.exit_code, 0)
        self.assertIn("Usage", r.output)


@unittest.skipUnless(_MZTABM_AVAILABLE, "mztab_m_io not installed")
class TestBuildMztabmSecondSoftware(unittest.TestCase):
    """build_mztabm must include mtbsccli as software[2] when converter_version is set."""

    def _build(self, converter_version=None):
        from unittest.mock import MagicMock

        from mtbsccli.convert import build_mztabm

        project = metaPyScape.Project()
        project.id = "proj-1"
        project.name = "TestProject"

        project_info = MagicMock()
        project_info.description = None
        project_info.name = "TestProject"

        intensity_matrix = MagicMock()
        intensity_matrix.analysis_ids = []
        intensity_matrix.feature_ids = []
        intensity_matrix.intensities = []

        return build_mztabm(
            project=project,
            project_info=project_info,
            feature_table=[],
            samples=[],
            intensity_matrix=intensity_matrix,
            featuretable_id="ft-1",
            converter_version=converter_version,
        )

    def test_no_converter_version_yields_one_software(self):
        mztab = self._build(converter_version=None)
        self.assertEqual(len(mztab.metadata.software), 1)
        self.assertEqual(mztab.metadata.software[0].id, 1)
        self.assertEqual(mztab.metadata.software[0].parameter.name, "MetaboScape")

    def test_with_converter_version_yields_two_software(self):
        mztab = self._build(converter_version="0.1")
        self.assertEqual(len(mztab.metadata.software), 2)

    def test_second_software_is_mtbsccli(self):
        mztab = self._build(converter_version="0.1")
        sw2 = mztab.metadata.software[1]
        self.assertEqual(sw2.id, 2)
        self.assertEqual(sw2.parameter.name, "mtbsccli")
        self.assertEqual(sw2.parameter.value, "0.1")

    def test_second_software_version_matches_input(self):
        mztab = self._build(converter_version="1.2.3")
        self.assertEqual(mztab.metadata.software[1].parameter.value, "1.2.3")

    def test_first_software_unchanged(self):
        mztab = self._build(converter_version="0.1")
        sw1 = mztab.metadata.software[0]
        self.assertEqual(sw1.id, 1)
        self.assertEqual(sw1.parameter.name, "MetaboScape")


if __name__ == "__main__":
    unittest.main()
