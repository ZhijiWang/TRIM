import hashlib
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_legacy_archive_reference_is_documented_and_legacy_outputs_removed():
    root = Path(__file__).parents[1]
    legacy_doc = (root / "docs" / "legacy_history.md").read_text(encoding="utf-8")

    assert "legacy-trim-v0.2.1" in legacy_doc
    assert "252f4b1c867751bd996885ec674f5f546ddbc110" in legacy_doc
    assert not (root / "trim").exists()
    assert not (root / "outputs" / "coder_packages").exists()


def test_frozen_trim_haa_source_hashes_are_preserved():
    root = Path(__file__).parents[1]
    walk = root / "examples" / "in_a_grove_walkthrough"

    assert _sha256(walk / "author_analytic_record.csv") == "8155a280880f9fda1035f1b3790f7dbd2932db0b07de940bf9c023cb3ab86871"
    assert _sha256(walk / "ai_raw_output.txt") == "343b9858e3fc9c89840be68542e2ad1aa8b389f8841a86db9c9ceaec48a149a2"
    assert _sha256(walk / "prompts" / "in_a_grove_trim_haa_v0_1.txt") == "74af647ec15697e99bd87ee4c4fdbfecfd402ff09cc76dc8acf55e3bf856e8f5"
