# coding: utf-8
"""Unit tests for mtbsccli.output formatting helpers."""

from __future__ import annotations

import io
import json
import sys
import unittest
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

import metaPyScape
from mtbsccli import output as out
from mtbsccli.cli import cli


def _make_project():
    """Build a simple Project with one experiment and one feature table."""
    project = metaPyScape.Project()
    project.id = "87d912bb-4153-4443-bf2a-1036548a0961"
    project.name = "TestProject"

    exp = metaPyScape.Experiment()
    exp.id = "6f281a94-40d5-425b-be62-e283a964796e"
    exp.name = "TestExperiment"

    ft = metaPyScape.FeatureTable()
    ft.id = "2c32680e-debc-4f77-8970-78cf547d9875"
    ft.name = "TestTable-pos"
    ft.polarity = "POSITIVE"
    exp.feature_tables = [ft]

    project.experiments = [exp]
    return project


class TestFormatOutputJson(unittest.TestCase):
    """format_output with output_format='json' must emit valid JSON on stdout."""

    def _capture_json(self, data):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            out.format_output(data, "json")
        finally:
            sys.stdout = old_stdout
        return buf.getvalue()

    def test_project_json_is_valid(self):
        project = _make_project()
        raw = self._capture_json(project)
        parsed = json.loads(raw)  # must not raise
        self.assertEqual(parsed["id"], "87d912bb-4153-4443-bf2a-1036548a0961")

    def test_project_json_no_extra_lines(self):
        """The JSON output must start with '{' — no extra lines before it."""
        project = _make_project()
        raw = self._capture_json(project)
        self.assertTrue(raw.lstrip().startswith("{"), f"JSON output starts with: {raw[:40]!r}")

    def test_list_json_is_valid(self):
        project = _make_project()
        raw = self._capture_json([project, project])
        parsed = json.loads(raw)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 2)

    def test_none_json(self):
        raw = self._capture_json(None)
        self.assertEqual(json.loads(raw), None)

    def test_nested_experiments_in_json(self):
        """Nested experiments and feature_tables must appear in JSON output."""
        project = _make_project()
        raw = self._capture_json(project)
        parsed = json.loads(raw)
        self.assertIn("experiments", parsed)
        self.assertEqual(len(parsed["experiments"]), 1)
        ft_list = parsed["experiments"][0]["feature_tables"]
        self.assertEqual(ft_list[0]["polarity"], "POSITIVE")


class TestFormatOutputTable(unittest.TestCase):
    """format_output with output_format='table' must not emit Python dict repr."""

    def _capture_table(self, data):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            out.format_output(data, "table")
        finally:
            sys.stdout = old_stdout
        return buf.getvalue()

    def test_no_python_dict_repr_for_single_object(self):
        """Nested dicts must NOT appear as Python {'key': 'value'} strings."""
        project = _make_project()
        output = self._capture_table(project)
        self.assertNotIn("{'id':", output)
        self.assertNotIn("{'name':", output)

    def test_nested_experiment_fields_visible(self):
        """Experiment id and name must appear in the table output."""
        project = _make_project()
        output = self._capture_table(project)
        self.assertIn("6f281a94-40d5-425b-be62-e283a964796e", output)
        self.assertIn("TestExperiment", output)

    def test_nested_feature_table_fields_visible(self):
        """Feature table id and polarity must appear in the table output."""
        project = _make_project()
        output = self._capture_table(project)
        self.assertIn("2c32680e-debc-4f77-8970-78cf547d9875", output)
        self.assertIn("POSITIVE", output)

    def test_list_of_projects_as_table(self):
        """A list of projects should render with column headers."""
        project = _make_project()
        output = self._capture_table([project])
        # Headers should be uppercased column names
        self.assertIn("ID", output)
        self.assertIn("NAME", output)

    def test_empty_list(self):
        output = self._capture_table([])
        self.assertIn("No items found", output)

    def test_none_data(self):
        output = self._capture_table(None)
        self.assertIn("No data", output)

    def test_empty_list_field_renders_not_as_python(self):
        """An empty list value must not render as '[]' Python repr in nested context."""
        project = metaPyScape.Project()
        project.id = "aaa"
        project.name = "empty"
        project.experiments = []
        output = self._capture_table(project)
        # experiments: [] is acceptable (empty list notation), but must not
        # contain raw Python dict repr
        self.assertNotIn("{'id':", output)


class TestGetCommandOutputFlag(unittest.TestCase):
    """The get subgroup must honour -o both at root level and at get-group level."""

    def _invoke(self, args):
        project = _make_project()
        with patch("mtbsccli.cli._make_client") as mc, patch(
            "metaPyScape.ProjectsApi"
        ) as MP:
            mc.return_value = MagicMock()
            mp_inst = MagicMock()
            mp_inst.retrieve_project.return_value = project
            MP.return_value = mp_inst

            runner = CliRunner()
            return runner.invoke(cli, args, catch_exceptions=False)

    def test_root_flag_json(self):
        r = self._invoke(["-o", "json", "get", "project", "87d912bb"])
        self.assertEqual(r.exit_code, 0)
        parsed = json.loads(r.output)
        self.assertEqual(parsed["id"], "87d912bb-4153-4443-bf2a-1036548a0961")

    def test_get_group_flag_json(self):
        """mtbsccli get -o json project <id> must output valid JSON."""
        r = self._invoke(["get", "-o", "json", "project", "87d912bb"])
        self.assertEqual(r.exit_code, 0)
        parsed = json.loads(r.output)
        self.assertEqual(parsed["id"], "87d912bb-4153-4443-bf2a-1036548a0961")

    def test_get_group_flag_table_no_python_repr(self):
        """mtbsccli get -o table project <id> must not emit Python dict repr."""
        r = self._invoke(["get", "-o", "table", "project", "87d912bb"])
        self.assertEqual(r.exit_code, 0)
        self.assertNotIn("{'id':", r.output)
        self.assertIn("6f281a94-40d5-425b-be62-e283a964796e", r.output)

    def test_root_flag_overridden_by_get_group_flag(self):
        """get-group -o json overrides root-level -o table."""
        r = self._invoke(["-o", "table", "get", "-o", "json", "project", "87d912bb"])
        self.assertEqual(r.exit_code, 0)
        parsed = json.loads(r.output)
        self.assertIsInstance(parsed, dict)

    def test_json_output_starts_with_brace(self):
        """JSON output must start with '{', no extra lines before it."""
        r = self._invoke(["-o", "json", "get", "project", "87d912bb"])
        self.assertTrue(r.output.lstrip().startswith("{"), repr(r.output[:60]))


if __name__ == "__main__":
    unittest.main()
