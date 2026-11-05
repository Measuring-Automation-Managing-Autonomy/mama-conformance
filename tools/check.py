#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""MAMA conformance checker: run shared fixtures against the schemas of the
repos they belong to, at pinned commits.

Design: this repo owns FIXTURES only (synthetic data; never real pilot data).
The schemas live in their source repos; CI (or a developer) clones the repos
at the commits recorded in pins.json and passes --repos-dir. Each suite lists
valid fixtures (must validate) and invalid fixtures (must be rejected).
Any mismatch is a conformance failure — the release gate for Phase 3.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema
import yaml

SUITES = [
    {
        "name": "metric-cards",
        "repo": "mama-metrics",
        "schema_path": "schema/metric-card.schema.json",
        "root": "metric-cards",
    },
    {
        "name": "assessment-import",
        "repo": "mama-integrations",
        "schema_path": "contracts/assessment-import.schema.json",
        "root": "assessment-import",
    },
    {
        "name": "ledger-import",
        "repo": "mama-integrations",
        "schema_path": "contracts/ledger-import.schema.json",
        "root": "ledger-import",
    },
    {
        "name": "usecase-mapping",
        "repo": "mama-integrations",
        "schema_path": "contracts/usecase-mapping.schema.json",
        "root": "usecase-mapping",
    },
    {
        "name": "usecase-record",
        "repo": "mama-tools",
        "schema_path": "schemas/usecase-record.schema.json",
        "root": "usecase-record",
    },
    {
        "name": "series-record",
        "repo": "mama-tools",
        "schema_path": "schemas/series-record.schema.json",
        "root": "series-record",
    },
    {
        "name": "tracker-record",
        "repo": "mama-tools",
        "schema_path": "schemas/tracker-record.schema.json",
        "root": "tracker-record",
    },
]


def _coerce_dates(node):
    import datetime as dt
    if isinstance(node, dt.date) and not isinstance(node, dt.datetime):
        return node.isoformat()
    if isinstance(node, dict):
        return {k: _coerce_dates(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_coerce_dates(v) for v in node]
    return node


def load(path: Path):
    if path.suffix in (".yaml", ".yml"):
        return _coerce_dates(yaml.safe_load(path.read_text(encoding="utf-8")))
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Run MAMA conformance fixtures.")
    ap.add_argument("--repos-dir", required=True,
                    help="directory containing the cloned source repos at pinned commits")
    ap.add_argument("--fixtures", default=str(Path(__file__).resolve().parent.parent / "fixtures"))
    args = ap.parse_args()

    pins = json.loads((Path(__file__).resolve().parent.parent / "pins.json").read_text(encoding="utf-8"))
    failures = []
    checked = 0
    for suite in SUITES:
        repo_dir = Path(args.repos_dir) / suite["repo"]
        if not repo_dir.exists():
            failures.append(f"{suite['name']}: repo {suite['repo']} not cloned under --repos-dir")
            continue
        schema = load(repo_dir / suite["schema_path"])
        if suite.get("schema_patch"):
            for k, v in suite["schema_patch"].items():
                schema[k] = v
        validator = jsonschema.Draft202012Validator(schema)
        root = Path(args.fixtures) / suite["root"]
        for kind, expect_valid in (("valid", True), ("invalid", False)):
            for f in sorted((root / kind).glob("*.*")):
                checked += 1
                doc = load(f)
                errors = list(validator.iter_errors(doc))
                if expect_valid and errors:
                    failures.append(f"{suite['name']}/valid/{f.name}: rejected — {errors[0].message[:120]}")
                if not expect_valid and not errors:
                    failures.append(f"{suite['name']}/invalid/{f.name}: accepted but must be rejected")

    if failures:
        for f in failures:
            print(f"FAIL - {f}", file=sys.stderr)
        print(f"conformance: {len(failures)} failure(s) across {checked} fixtures", file=sys.stderr)
        return 1
    print(f"conformance: {checked} fixtures pass ({len(SUITES)} suites)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
