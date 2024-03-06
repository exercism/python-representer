"""
Run tests on the test runner itself, using golden files.
"""

import json
import subprocess
import os
import tempfile
from pathlib import Path


import pytest

ROOT = Path(__file__).parent
REPRESENTER = ROOT.joinpath("..", "bin", "run.sh").resolve(strict=True)
TESTS = sorted(ROOT.glob("example*/example_*.py"))
CONCEPT_EXERCISES = sorted(ROOT.glob("concept*/*.py"))
PRACTICE_EXERCISES = sorted(ROOT.glob("practice*/*.py"))

def run_in_subprocess(test_path, golden_path, args=None):
    """
    Run given tests against the given golden file.
    """
    exercise_dir = test_path.parent
    exercise_name = exercise_dir.name
    with tempfile.TemporaryDirectory(prefix="test-representer-tests", dir=ROOT) as tmp_dir:
        rc = subprocess.run([REPRESENTER, exercise_name, exercise_dir, tmp_dir]).returncode

        mapping = Path(tmp_dir).joinpath("mapping.json").resolve(strict=True)
        representation_json = Path(tmp_dir).joinpath("representation.json").resolve(strict=True)
        representation_out = Path(tmp_dir).joinpath("representation.out").resolve(strict=True)
        representation_txt = Path(tmp_dir).joinpath("representation.txt").resolve(strict=True)

        golden_mapping, golden_representation_json, golden_representation_out, golden_representation_txt = golden_path

        results = mapping, representation_json, representation_out, representation_txt

        return ((json.loads(mapping.read_text()), json.loads(golden_mapping.read_text())),
                (json.loads(representation_json.read_text()), json.loads(golden_representation_json.read_text())),
                (representation_out.read_text(), golden_representation_out.read_text()),
                (representation_txt.read_text(), golden_representation_txt.read_text())), rc


@pytest.fixture(params=TESTS, ids=(os.path.split(path)[0].split("/")[-1] for path in TESTS))
def test_with_golden(request):
    """
    Path to a test and its golden files.
    """
    path = request.param

    golden_mapping = path.parent.joinpath("mapping.json").resolve(strict=True)
    golden_representation_json = path.parent.joinpath("representation.json").resolve(strict=True)
    golden_representation_out = path.parent.joinpath("representation.out").resolve(strict=True)
    golden_representation_txt = path.parent.joinpath("representation.txt").resolve(strict=True)

    golden = (golden_mapping, golden_representation_json, golden_representation_out, golden_representation_txt)


    return path, golden

@pytest.fixture(params=CONCEPT_EXERCISES, ids=(os.path.split(path)[0].split("/")[-1][8:] for path in CONCEPT_EXERCISES))
def test_concept_exercises_with_golden(request):
    """
    Path to a test and its golden files.
    """
    path = request.param

    golden_mapping = path.parent.joinpath("mapping.json").resolve(strict=True)
    golden_representation_json = path.parent.joinpath("representation.json").resolve(strict=True)
    golden_representation_out = path.parent.joinpath("representation.out").resolve(strict=True)
    golden_representation_txt = path.parent.joinpath("representation.txt").resolve(strict=True)

    golden = (golden_mapping, golden_representation_json, golden_representation_out, golden_representation_txt)


    return path, golden

@pytest.fixture(params=PRACTICE_EXERCISES, ids=(os.path.split(path)[0].split("/")[-1][9:] for path in PRACTICE_EXERCISES))
def test_practice_exercises_with_golden(request):
    """
    Path to a test and its golden files.
    """
    path = request.param

    golden_mapping = path.parent.joinpath("mapping.json").resolve(strict=True)
    golden_representation_json = path.parent.joinpath("representation.json").resolve(strict=True)
    golden_representation_out = path.parent.joinpath("representation.out").resolve(strict=True)
    golden_representation_txt = path.parent.joinpath("representation.txt").resolve(strict=True)

    golden = (golden_mapping, golden_representation_json, golden_representation_out, golden_representation_txt)


    return path, golden

def test_results_matches_golden_file(test_with_golden):
    """
    Test that the results of a run matches the golden file.
    """

    results, rc = run_in_subprocess(*test_with_golden)

    for result, golden in results:
        assert result == golden, "results must match the golden file"

    assert rc == 0, f"return code must be 0 even when errors occur: got {rc}"

def test_concept_exercises_match_golden_file(test_concept_exercises_with_golden):
    """
    Test that the results of a run matches the golden file.
    """

    results, rc = run_in_subprocess(*test_concept_exercises_with_golden)

    for result, golden in results:
        assert result == golden, "results must match the golden file"

    assert rc == 0, f"return code must be 0 even when errors occur: got {rc}"

def test_practice_exercises_match_golden_file(test_practice_exercises_with_golden):
    """
    Test that the results of a run matches the golden file.
    """

    results, rc = run_in_subprocess(*test_practice_exercises_with_golden)

    for result, golden in results:
        assert result == golden, "results must match the golden file"

    assert rc == 0, f"return code must be 0 even when errors occur: got {rc}"