# mama-conformance

**MAMA** (Measuring Automation, Managing Autonomy) shared conformance
fixtures: synthetic test data that every MAMA implementation must handle the
same way, checked against the schemas of the source repos **at pinned
commits** (`pins.json`).

> **First reference:** MAMA (Measuring Automation, Managing Autonomy) uses
> the `mama` (measuring and managing autonomy) method for its
> autonomy-governance component; its canonical home is
> [`emmanuel-a-otchere/measuring-and-managing-autonomy`](https://github.com/emmanuel-a-otchere/measuring-and-managing-autonomy).

**Status:** `draft` (v0.1.0) · **License:** Apache-2.0 · **Maintainer:** see [MAINTAINERS.md](MAINTAINERS.md)

## Suites

| Suite | Schema source (repo / path) | Fixtures |
|---|---|---|
| metric-cards | mama-metrics / `schema/metric-card.schema.json` | valid 2 · invalid 2 |
| assessment-import | mama-integrations / `contracts/assessment-import.schema.json` | valid 1 · invalid 2 |
| ledger-import | mama-integrations / `contracts/ledger-import.schema.json` | valid 1 · invalid 3 |
| usecase-mapping | mama-integrations / `contracts/usecase-mapping.schema.json` | valid 1 · invalid 2 |
| usecase-record | mama-tools / `schemas/usecase-record.schema.json` | valid 1 · invalid 2 |

Rules: `valid/*` must validate; `invalid/*` must be rejected. Any mismatch
fails CI — this is the Phase 3 release gate ("conformance fixtures pass").

## Rules for fixtures

1. **Synthetic data only** — never real customer, pilot, or sensitive
   organizational data ([org GOVERNANCE](https://github.com/Measuring-Automation-Managing-Autonomy/.github/blob/main/GOVERNANCE.md)).
2. **Pins move with fixtures.** A fixture change that depends on a schema
   change updates `pins.json` in the same PR.
3. **Each invalid fixture names its rejection reason in the filename.**
4. New suites cover new schemas; every MAMA-published schema should have a
   suite here before tools ship against it.

## Run locally

```bash
python3 -m pip install jsonschema pyyaml
# clone the four source repos (any location), then:
python3 tools/check.py --repos-dir /path/to/clones-parent
```
