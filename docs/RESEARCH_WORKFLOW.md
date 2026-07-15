# Research Workflow

## Purpose and scope

This workflow separates conceptual design, implementation, independent review, and final scientific authority. It applies only to Paper 1, *Dark Matter Structure and Galaxy Phenomenology*.

## Role separation

### ChatGPT

ChatGPT handles conceptual discussion, physical interpretation, analytic derivation planning, gate design, preparation of calculation specifications, and identification of assumptions and competing interpretations. ChatGPT does not certify numerical results.

### Codex

Codex handles repository maintenance, symbolic and numerical implementation, tests, regression anchors, reproducibility, result files, and branch and commit discipline. Codex must not promote a result into a paper claim without review.

### Claude

Claude is the independent reviewer and discriminator. Claude reviews derivations and results, records a verdict on whether a gate passes, identifies overclaims, and updates the paper only after results are accepted.

### User / Principal Investigator

The User / Principal Investigator owns the physical programme, approves assumptions, gates and scope changes, accepts or rejects final verdicts, and decides when paper text may be updated.

## Gate lifecycle

1. **Propose:** record the scientific question and scope in `GATES.md`.
2. **Specify:** lock assumptions, relevant conventions, inputs, analytic anchors, regression anchors, kill criterion, computations, and deliverables.
3. **Prepare:** commit the derivation note before production implementation.
4. **Run:** Codex implements on a dedicated gate branch, runs tests, and stores immutable raw output and provenance-tracked processed artifacts.
5. **Review:** Claude independently reviews the derivation, implementation, anchors, artifacts, limitations, and claim language.
6. **Decide:** the Principal Investigator accepts or rejects the reviewer verdict and authorizes consequences.
7. **Close:** record the final status and dates. Preserve failed and inconclusive work.
8. **Integrate:** merge only accepted closed gates into `main`; update claims or paper prose only with explicit authorization.

No result is accepted merely because code runs. A result requires anchors, tests, stored outputs, provenance, and independent review.

## Handoffs

`HANDOFF.md` states the active task, locked inputs, prohibited reopening, required inputs, expected outputs, and open questions. Update it whenever responsibility changes. Never use a handoff to silently change scope or conventions.
