# Agent Rules

These rules apply to every future human-assisted or AI-assisted change in this Paper 1 repository.

## Mandatory operating rules

1. Read `PROGRESS.md`, `GATES.md`, `DECISION_LOG.md`, `CLAIMS.md`, `HANDOFF.md`, and `CONVENTIONS.md` before making changes.
2. Never reopen a closed gate unless a concrete inconsistency is documented.
3. Never silently change conventions. Record and approve any change before recalculation.
4. Commit the derivation note before production code.
5. Tests and regression anchors are mandatory.
6. Never edit raw outputs manually.
7. Processed results must identify the exact script and raw input used.
8. Do not update any `.tex` paper file before reviewer acceptance.
9. Preserve failed results and their provenance.
10. Explicitly distinguish the original model, a model extension, a phenomenological EFT, and a numerical proxy.
11. Every result must identify its regulator, cutoff, normalization, seeds, and operating point.
12. One branch corresponds to one scientific gate or one paper-edit task.

## Role separation

### ChatGPT

ChatGPT is responsible for conceptual discussion, physical interpretation, analytic derivation planning, gate design, preparation of calculation specifications, and identification of assumptions and competing interpretations. ChatGPT does not certify numerical results.

### Codex

Codex is responsible for repository maintenance, symbolic and numerical implementation, tests, regression anchors, reproducibility, result files, and branch and commit discipline. Codex must not promote a result into a paper claim without review.

### Claude

Claude is the independent reviewer and discriminator. Claude reviews derivations and results, records a verdict on whether a gate passes, identifies overclaims, and updates the paper only after results are accepted.

### User / Principal Investigator

The User / Principal Investigator owns the physical programme, approves assumptions, gates and scope changes, accepts or rejects final verdicts, and decides when paper text may be updated.

## Scope boundary

This is the one-paper repository for Paper 1. Never merge substantive material from another paper repository into this one. Cross-paper inputs must be explicitly identified and governed.
