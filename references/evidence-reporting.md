# Evidence and Reporting

## Initial report template

```markdown
# Reverse Engineering Initial Report

## Summary
- Artifact:
- Scope:
- Current phase:
- Overall risk:

## Artifact inventory
| Name | Path | Size | SHA-256 | Type | Notes |
|---|---|---:|---|---|---|

## Verified facts
| ID | Evidence | Source/offset/tool | Interpretation | Confidence |
|---|---|---|---|---|

## Key findings
### Finding 1: <title>
- Evidence:
- Impact:
- Confidence:
- Validation status:

## Unknowns
- 

## Recommended next steps
1. 
2. 
3. 
```

## Deep reverse report template

```markdown
# Deep Reverse Engineering Report

## Executive summary
## Scope and artifacts
## Methodology
## Architecture and behavior model
## Function/module map
## Data-flow and trust boundaries
## Dynamic observations
## Vulnerability candidates
## Evidence appendix
## Reproducibility notes
## Recommended next steps
```

## Vulnerability advisory template

```markdown
# Vulnerability Report: <title>

## Summary
## Affected product/version/component
## Severity and rationale
## Preconditions
## Root cause
## Technical details
## Safe reproduction evidence
## Impact
## Remediation guidance
## Detection/mitigation
## Evidence appendix
## Timeline/status
```

## Confidence vocabulary
- **High**: directly observed in code or runtime and reproducible.
- **Medium**: supported by multiple static indicators but not fully executed.
- **Low**: plausible hypothesis with limited evidence.

## Evidence table rules
Use stable identifiers. Include offsets, function names, command outputs, hashes, log excerpts, screenshots, or traces. Keep raw logs in the case directory and summarize only the relevant lines in reports.

### Identifier scheme (pick one per report, never mix silently)

| Backend state | ID format | Required fields per row |
|---|---|---|
| Rea MCP available | `ev_<64 hex>` returned by the backend, cited verbatim | backend ID + procedure/address + observation |
| Rea absent (scripts/CLI only) | `E1`, `E2`, ... sequential | SHA-256 of the artifact + exact command + offset/function/string |
| Mixed (partially available) | prefix by source: `rea:ev_...` / `local:E3` | as above, plus a one-line note at the top of the report explaining which section came from which backend |

Rules:

- Never renumber, shorten, or invent a backend `ev_` identifier; it is a hash, not a label.
- An `E#` row without SHA-256 + command is not evidence — move it to "Unknowns".
- Report degraded mode explicitly: `Backend: local scripts only (Rea unavailable)` in the Summary block, and cap confidence at Medium.
- `verify_reconstruction` passing covers declared claims only. State the claim list in the report; undeclared behavior remains `unknown`.

See `rea-backend.md` for the probe/routing/degradation workflow.
