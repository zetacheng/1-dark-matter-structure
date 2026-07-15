# Results

Raw outputs are immutable and must never be edited manually. Processed results must record complete provenance, including the generating script and raw input used.

Every result directory must include:

- `README.md`;
- configuration;
- raw output;
- a processed table;
- a verdict;
- the commit hash;
- the branch;
- the date;
- environment information.

Recommended layout:

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

See `docs/RESULT_SCHEMA.md` for the required provenance standard.
