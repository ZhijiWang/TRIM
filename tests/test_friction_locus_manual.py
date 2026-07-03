import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_friction_locus_manual_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_friction_locus_manual.py"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "friction_locus_manual_validation: ok" in result.stdout

