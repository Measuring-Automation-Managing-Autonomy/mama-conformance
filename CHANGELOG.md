# Changelog — mama-conformance

Versions are semver; `draft`-status artifacts may change without notice.

## [0.1.0] — 2026-11-05

### Added (initial release, CR MAMA-ORG-CR-001 Phase 3 gate)

- 17 fixtures across 5 suites (metric-cards, assessment-import, ledger-import,
  usecase-mapping, usecase-record), each suite with valid and invalid cases
  naming the rejection reason
- `tools/check.py` — runs fixtures against the source repos' schemas at the
  commits pinned in `pins.json`
- CI: clones the four source repos at pins and runs the checker
