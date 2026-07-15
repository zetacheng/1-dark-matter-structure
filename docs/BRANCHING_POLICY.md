# Branching Policy

## Branch names

```text
gate/<gate-name>
paper/<paper-version>
review/<review-topic>
fix/<issue>
archive/<retired-route>
```

## Rules

- `main` contains accepted infrastructure and accepted closed gates only.
- Active calculations stay on a `gate/` branch.
- Failed gate branches are preserved.
- Do not squash the history of scientific derivations.
- Prefer conventional commits.
- Tags mark accepted scientific milestones.
- A branch corresponds to one scientific gate or one paper-edit task.
- Paper branches may update paper source only after reviewer acceptance and Principal Investigator authorization.
