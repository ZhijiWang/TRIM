from pathlib import Path

from trim_haa.hashing import looks_like_sha256, sha256_file, sha256_text


def test_sha256_text_and_file(tmp_path):
    path = tmp_path / "prompt.txt"
    path.write_text("exact prompt", encoding="utf-8")

    assert sha256_text("exact prompt") == sha256_file(path)
    assert looks_like_sha256(sha256_file(path))


def test_prompt_manifest_template_headers():
    path = Path(__file__).parents[1] / "data" / "trim_haa_prompt_manifest_template.csv"
    headers = path.read_text(encoding="utf-8").splitlines()[0].split(",")

    assert "prompt_template_id" in headers
    assert "prompt_sha256" in headers
    assert "frozen" in headers

