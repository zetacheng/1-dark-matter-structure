# Result Schema

## Principles

- Raw outputs are immutable. Never edit them manually or replace them without recording a new run.
- Processed results must contain provenance linking them to the exact script, configuration, and raw inputs used.
- Failed, inconclusive, and retired results must remain available for audit.
- A passing program or test suite is not a scientific verdict.

## Required contents

Every result directory must include:

- `README.md` describing the scientific question, gate, operating point, and artifact inventory;
- a machine-readable configuration, normally `config.json`;
- raw output;
- a processed table;
- `verdict.md` containing the result and reviewer verdict;
- the exact commit hash;
- the branch name;
- the run date;
- environment information, normally `environment.txt`.

The metadata must also identify the regulator, cutoff, normalization, random seeds, operating point, generating script, and every raw input. If a field is not applicable, record that explicitly rather than omitting it.

## Recommended layout

```text
results/<gate-id>/
  README.md
  config.json
  raw/
  processed/
  figures/
  verdict.md
  environment.txt
```

Processed tables and figures are derived artifacts. Their documentation must make regeneration from immutable raw output possible with one recorded command.
