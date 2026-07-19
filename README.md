# 1-dark-matter-structure

Paper 1 — **Dark Matter Structure and Galaxy Phenomenology**

Core scientific responsibility: halo structure, SPARC, RAR, BTFR, and dark-matter candidate phenomenology.

This repository contains one paper only. Material belonging to the other four papers must remain in their own repositories.

## Current status

`SCIENTIFIC RECORD IMPORTED — GOVERNANCE ACTIVE`

The scientific record was imported from `zetacheng/yukawa-sparc-fits`
(commit `fd3b2b6…`, byte-for-byte) on 2026-07-16 and registered against paper
v16.3: SPARC data under `data/`, analysis scripts under `scripts/`, raw result
CSVs under `results/<gate>/raw/`, a populated claim ledger (`CLAIMS.md`), gate
registry (`GATES.md`), and a regression suite (`tests/`). Claims are recorded
`SUPPORTED` (independently reproduced), **not** `VERIFIED` — no independent
reviewer record exists in this repository yet. Migration provenance and the
known artifact gaps are in `MIGRATION.md`.

## Role separation

### ChatGPT

ChatGPT supports conceptual discussion, physical interpretation, analytic derivation planning, gate design, preparation of calculation specifications, and identification of assumptions and competing interpretations. ChatGPT does not certify numerical results.

### Codex

Codex maintains the repository; implements symbolic and numerical work; creates tests, regression anchors, reproducible artifacts, and result files; and maintains branch and commit discipline. Codex must not promote a result into a paper claim without review.

### Claude

Claude acts as the independent reviewer and discriminator: reviewing derivations and results, deciding whether a gate passes, identifying overclaims, and updating the paper only after results are accepted.

### User / Principal Investigator

The User / Principal Investigator owns the physical programme, approves assumptions, gates, and scope changes, accepts or rejects final verdicts, and decides when paper text may be updated.

## Directory guide

- `paper/`: imported paper source and paper figures.
- `derivations/`: analytic specifications committed before production code.
- `scripts/`: symbolic, numerical, processing, and reproducibility scripts.
- `tests/`: structure, unit, and regression tests.
- `results/`: immutable raw outputs and provenance-tracked processed artifacts.
- `reviews/`: independent ChatGPT and Claude review records.
- `archive/`: preserved retired routes and historical material.
- `docs/`: workflow, result schema, and branching policy.

## Standard gate workflow

1. The Principal Investigator approves the question, scope, assumptions, conventions, anchors, and kill criterion.
2. A derivation note and calculation specification are committed on one `gate/<gate-name>` branch.
3. Codex implements the calculation, tests, regression anchors, and reproducible result artifacts.
4. Claude independently reviews the evidence and records a gate verdict.
5. The Principal Investigator accepts or rejects the verdict and authorizes any claim or paper update.
6. Only accepted closed gates may enter `main`.

## Reproducibility commands

```text
make structure
make lint
make test
make check
```

## Evidence warning

No result is accepted merely because code runs. Acceptance requires analytic and regression anchors, tests, stored outputs with provenance, and independent review.
