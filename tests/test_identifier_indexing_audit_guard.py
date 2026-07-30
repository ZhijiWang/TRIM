import ast
from pathlib import Path


ROOT = Path(__file__).parents[1]
PRODUCTION_ROOTS = (ROOT / "src" / "trim_haa", ROOT / "scripts")
FROZEN_LEGACY_CALL_ALLOWLIST = {
    ("src/trim_haa/provenance.py", "export_lineage_rows"),
    ("src/trim_haa/provenance.py", "lineage_for"),
}
AUDITED_ANNOTATION_INDEX_FILES = (
    ROOT / "src" / "trim_haa" / "reporting.py",
    ROOT / "src" / "trim_haa" / "validator.py",
    ROOT / "scripts" / "run_trim_haa_synthetic_dry_run.py",
)


def _scope_name(tree: ast.AST) -> dict[ast.AST, str]:
    scopes: dict[ast.AST, str] = {}

    def visit(node: ast.AST, scope: str) -> None:
        scopes[node] = scope
        child_scope = node.name if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else scope
        for child in ast.iter_child_nodes(node):
            visit(child, child_scope)

    visit(tree, "<module>")
    return scopes


def _legacy_usage(source: str, relative_path: str) -> tuple[set[tuple[str, str]], list[str]]:
    tree = ast.parse(source, filename=relative_path)
    scopes = _scope_name(tree)
    allowed_calls: set[tuple[str, str]] = set()
    violations: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            is_provenance_module = node.module == "trim_haa.provenance" or (
                node.level > 0 and node.module == "provenance"
            )
            if is_provenance_module and any(
                alias.name == "annotation_index" for alias in node.names
            ):
                violations.append(f"{relative_path}:{scopes[node]}:legacy import")
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        is_legacy_call = (
            isinstance(function, ast.Name) and function.id == "annotation_index"
        ) or (
            isinstance(function, ast.Attribute)
            and function.attr == "annotation_index"
        )
        if not is_legacy_call:
            continue
        location = (relative_path, scopes[node])
        if location in FROZEN_LEGACY_CALL_ALLOWLIST:
            allowed_calls.add(location)
        else:
            violations.append(f"{relative_path}:{scopes[node]}:legacy call")
    return allowed_calls, violations


def _production_python_files():
    for root in PRODUCTION_ROOTS:
        yield from sorted(root.rglob("*.py"))


def test_legacy_annotation_index_allowlist_is_exact_and_line_independent():
    allowed_calls: set[tuple[str, str]] = set()
    violations: list[str] = []
    for path in _production_python_files():
        relative_path = path.relative_to(ROOT).as_posix()
        allowed, found = _legacy_usage(
            path.read_text(encoding="utf-8"),
            relative_path,
        )
        allowed_calls.update(allowed)
        violations.extend(found)

    assert violations == []
    assert allowed_calls == FROZEN_LEGACY_CALL_ALLOWLIST


def test_guard_rejects_a_new_production_legacy_import():
    source = (
        "from trim_haa.provenance import annotation_index\n"
        "def active(records):\n"
        "    return annotation_index(records)\n"
    )

    _, violations = _legacy_usage(source, "src/trim_haa/new_active_module.py")

    assert violations == [
        "src/trim_haa/new_active_module.py:<module>:legacy import",
        "src/trim_haa/new_active_module.py:active:legacy call",
    ]


def test_guard_rejects_a_new_relative_production_legacy_import():
    source = (
        "from .provenance import annotation_index\n"
        "def active(records):\n"
        "    return annotation_index(records)\n"
    )

    _, violations = _legacy_usage(source, "src/trim_haa/new_active_module.py")

    assert violations == [
        "src/trim_haa/new_active_module.py:<module>:legacy import",
        "src/trim_haa/new_active_module.py:active:legacy call",
    ]


def test_guard_allows_the_versioned_strict_api():
    source = (
        "from trim_haa.indexing import strict_annotation_index\n"
        "def active(records):\n"
        "    return strict_annotation_index(records)\n"
    )

    allowed, violations = _legacy_usage(source, "src/trim_haa/new_active_module.py")

    assert allowed == set()
    assert violations == []


def test_audited_annotation_callers_have_no_known_last_wins_comprehension():
    violations = []
    for path in AUDITED_ANNOTATION_INDEX_FILES:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.DictComp):
                continue
            key = node.key
            if not (
                isinstance(key, ast.Attribute)
                and key.attr == "annotation_id"
            ):
                continue
            iter_names = {
                child.id
                for generator in node.generators
                for child in ast.walk(generator.iter)
                if isinstance(child, ast.Name)
            }
            if iter_names & {"annotations", "core"}:
                violations.append(
                    f"{path.relative_to(ROOT)}:{node.lineno}:annotation_id dict comprehension"
                )

    assert violations == []
