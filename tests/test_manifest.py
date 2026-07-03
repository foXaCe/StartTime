"""Structural validation of the integration manifest and metadata.

These tests intentionally avoid importing Home Assistant so they run fast on any
supported Python version. Behavioural tests can be layered on top later.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTEGRATION = ROOT / "custom_components" / "start_time"
MANIFEST = INTEGRATION / "manifest.json"

REQUIRED_MANIFEST_KEYS = {
    "domain",
    "name",
    "codeowners",
    "config_flow",
    "documentation",
    "integration_type",
    "iot_class",
    "issue_tracker",
    "version",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_exists() -> None:
    assert MANIFEST.is_file()


def test_manifest_has_required_keys() -> None:
    manifest = _load(MANIFEST)
    missing = REQUIRED_MANIFEST_KEYS - manifest.keys()
    assert not missing, f"Missing manifest keys: {sorted(missing)}"


def test_domain_matches_folder() -> None:
    manifest = _load(MANIFEST)
    assert manifest["domain"] == INTEGRATION.name == "start_time"


def test_codeowner_is_fork_owner() -> None:
    manifest = _load(MANIFEST)
    assert manifest["codeowners"] == ["@foXaCe"]


def test_documentation_points_to_fork() -> None:
    manifest = _load(MANIFEST)
    assert "foXaCe/StartTime" in manifest["documentation"]
    assert "foXaCe/StartTime" in manifest["issue_tracker"]


def test_translations_present() -> None:
    for name in ("strings.json", "translations/en.json", "translations/fr.json"):
        path = INTEGRATION / name
        assert path.is_file(), f"Missing {name}"
        _load(path)  # must be valid JSON


def test_icon_translations_present() -> None:
    icons = _load(INTEGRATION / "icons.json")
    assert icons["entity"]["sensor"]["start_time"]["default"].startswith("mdi:")


def test_hacs_json_valid() -> None:
    hacs = _load(ROOT / "hacs.json")
    assert hacs["name"] == "Start Time"
    assert hacs["render_readme"] is True
