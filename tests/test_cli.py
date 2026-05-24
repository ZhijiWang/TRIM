from pathlib import Path

import json
import pandas as pd

from trim.cli import main


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO_CSV = PROJECT_ROOT / "data" / "demo_annotations.csv"


def test_cli_validate_writes_report(tmp_path):
    output_path = tmp_path / "validation_report.csv"

    result = main(["validate", str(DEMO_CSV), "--out", str(output_path)])

    report = pd.read_csv(output_path)
    assert result == 0
    assert output_path.exists()
    assert list(report.columns) == ["case_id", "field", "severity", "message"]
    assert report.empty


def test_cli_validate_alias_writes_report(tmp_path):
    output_path = tmp_path / "validation_report.csv"

    result = main(["trim-validate", str(DEMO_CSV), "--out", str(output_path)])

    assert result == 0
    assert output_path.exists()


def test_cli_executable_alias_writes_report(tmp_path, monkeypatch):
    output_path = tmp_path / "validation_report.csv"
    monkeypatch.setattr(
        "sys.argv",
        ["trim-validate", str(DEMO_CSV), "--out", str(output_path)],
    )

    result = main()

    assert result == 0
    assert output_path.exists()


def test_cli_report_writes_markdown(tmp_path):
    output_path = tmp_path / "report.md"

    result = main(["report", str(DEMO_CSV), "--out", str(output_path)])
    text = output_path.read_text(encoding="utf-8")

    assert result == 0
    assert "# TRIM Demo Comparison Report" in text
    assert "### Primary same-cue test: prophecy" in text
    assert "### Additional detected same-cue groups" in text


def test_cli_graph_writes_graph_outputs(tmp_path):
    graphml_path = tmp_path / "demo.graphml"
    json_path = tmp_path / "demo.json"

    result = main(
        [
            "graph",
            str(DEMO_CSV),
            "--graphml",
            str(graphml_path),
            "--json",
            str(json_path),
        ]
    )

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert result == 0
    assert graphml_path.exists()
    assert payload["directed"] is True
    assert len(payload["nodes"]) == 76


def test_cli_compare_writes_tables(tmp_path):
    output_dir = tmp_path / "tables"

    result = main(["compare", str(DEMO_CSV), "--outdir", str(output_dir)])

    assert result == 0
    assert (output_dir / "same_function_different_signature.csv").exists()
    assert (output_dir / "same_cue_different_function.csv").exists()
    assert (output_dir / "broad_family_different_signature.csv").exists()
    assert (output_dir / "contested_cases.csv").exists()
