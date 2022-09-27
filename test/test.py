"""Unit tests.

TODO's
 1. CLI tests
 2. Python API tests
 3. CompLoincTest: Anything redundant to remove?
 4. later: Need to run sequentially? Prob not, but have SequentialTests from pma-api I could re-use
 5. later: Run from __main__? if so, pma-api has a python api to run tests
 6. How to test outputs? file size? existence? arbitrary content? md5 match?
"""
import os
import shutil
import subprocess
import unittest
from pathlib import Path

try:
    from test.config import PROJECT_DIR, TEST_STATIC_DIR
except ModuleNotFoundError:
    from config import PROJECT_DIR, TEST_STATIC_DIR


class StaticFileTests(unittest.TestCase):
    """super class for common test functions"""

    # todo: May not need to use, since using static files at project root.
    # @staticmethod
    # def get_input_name_path_map(test_method_dir: str) -> Dict[str, Path]:
    #     """Get list of files in a directory."""
    #     dir_glob_path = os.path.join(TEST_STATIC_DIR, test_method_dir, 'input', '*')
    #     paths: List[str] = glob(dir_glob_path)
    #     return {
    #         os.path.basename(path): path
    #         for path in paths if not os.path.isdir(path)
    #     }

    @staticmethod
    def outdir(test_method_dir: str) -> str:
        """Get list of files in a directory."""
        return os.path.join(TEST_STATIC_DIR, test_method_dir, 'output')


class CompLoincTests(StaticFileTests):
    """CompLOINC tests"""

    cli_command_base = 'python comp_loinc/build.py'

    def run_command(self, test_name: str, outfile: str, command_str: str) -> float:
        """Run command for test"""
        outdir = self.outdir(test_name)
        Path(outdir).mkdir(parents=True, exist_ok=True)
        outpath = os.path.join(outdir, outfile)
        command_str = command_str.format(self.cli_command_base, outpath)
        command_list = command_str.split(' ')
        if os.path.exists(outpath):
            os.remove(outpath)
        subprocess.run(command_list, cwd=PROJECT_DIR)
        size_kb = os.path.getsize(outpath) / 1000
        return size_kb

    def all(self):
        """Wrapper for running all at once."""
        self.test_cli_parts()
        self.test_cli_codes()
        self.test_cli_composed()
        self.test_cli_merge()
        self.test_cli_reason()

    # def test_cli_parts(self):
    #     """Test CLI: parts"""
    #     test_name = 'test_cli_parts'
    #     outfile = 'part_ontology.owl'
    #     filesize_threshold_kb = 500  # semi-arbitrary for now
    #     command_str = \
    #         '{} parts ' \
    #         '--schema-file ./model/schema/part_schema.yaml ' \
    #         '--part-directory ./data/part_files ' \
    #         '--output {}'
    #
    #     size_kb = self.run_command(test_name, outfile, command_str)
    #     self.assertGreaterEqual(size_kb, filesize_threshold_kb)

    def test_cli_codes(self):
        """Test CLI: codes"""
        test_name = 'test_cli_codes'
        outfile = 'code_classes.owl'
        filesize_threshold_kb = 500  # semi-arbitrary for now
        command_str = \
            '{} codes ' \
            '--schema-file ./model/schema/code_schema.yaml ' \
            '--part-directory ./data/part_files ' \
            '--output {}'

        size_kb = self.run_command(test_name, outfile, command_str)
        self.assertGreaterEqual(size_kb, filesize_threshold_kb)

    def test_cli_composed(self):
        """Test CLI: composed"""
        test_name = 'test_cli_composed'
        outfile = 'composed_component_classes.owl'
        filesize_threshold_kb = 500  # semi-arbitrary for now
        command_str = \
            '{} composed ' \
            '--schema-file ./model/schema/grouping_classes_schema.yaml ' \
            '--composed-classes-data-file ./data/composed_classes_data.yaml ' \
            '--output {}'

        size_kb = self.run_command(test_name, outfile, command_str)
        self.assertGreaterEqual(size_kb, filesize_threshold_kb)

    def test_cli_merge(self):
        """Test CLI: merge"""
        test_name = 'test_cli_merge'
        outfile = 'merged_loinc.owl'
        filesize_threshold_kb = 500  # semi-arbitrary for now
        command_str = \
            '{} merge ' \
            '--owl-directory ./test/test_cli_merge/input/ ' \
            '--output {}'

        # Setup
        input_dir = './test/test_cli_merge/input/'
        inputs = [os.path.join(*[TEST_STATIC_DIR] + x) for x in [
            ['test_cli_parts', 'output', 'part_ontology.owl'],
            ['test_cli_codes', 'output', 'code_classes.owl'],
            ['test_cli_composed', 'output', 'composed_component_classes.owl']
        ]]
        if os.path.exists(input_dir):
            os.remove(input_dir)  # just in case last test failed and something goes wrong in this test
        Path(input_dir).mkdir(parents=True, exist_ok=False)
        for x in inputs:
            shutil.copy(x, input_dir)

        # Run test
        size_kb = self.run_command(test_name, outfile, command_str)
        self.assertGreaterEqual(size_kb, filesize_threshold_kb)

        # Tearown
        os.remove(input_dir)

    def test_cli_reason(self):
        """Test CLI: reason"""
        test_name = 'test_cli_reason'
        outfile = 'merged_reasoned_loinc.owl'
        filesize_threshold_kb = 500  # semi-arbitrary for now
        command_str = \
            '{} reason ' \
            '--merged-owl ./test/static/test_cli_merge/output/merged_loinc.owl ' \
            '--owl_reasoner elk ' \
            '--output {}'

        size_kb = self.run_command(test_name, outfile, command_str)
        self.assertGreaterEqual(size_kb, filesize_threshold_kb)


# Debugging / development
DEBUG = False
if DEBUG:
    CompLoincTests().all()
