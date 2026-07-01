import hashlib
from pathlib import Path


def test_no_legacy_frozen_package_files_changed():
    root = Path(__file__).parents[1]
    sums_path = root / "outputs" / "coder_packages" / "TRIM_retest_v0_2_1_coder_package.SHA256SUMS.txt"

    assert sums_path.exists()
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        if relative == "TRIM_retest_v0_2_1_coder_package.zip":
            path = sums_path.parent / relative
        elif relative.startswith("TRIM_retest_v0_2_1_semantic_steering_audit"):
            path = sums_path.parent / relative
        else:
            path = root / relative
        assert path.exists(), relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected

