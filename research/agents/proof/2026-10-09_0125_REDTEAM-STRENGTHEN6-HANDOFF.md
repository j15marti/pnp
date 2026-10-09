# REDTEAM-STRENGTHEN6 handoff

## Result

- **Accepted with repairs:** ARC6's nested-guard semantics, isolation, exact strip, and PIVOT cap for the explicitly scoped policy `old ARC5 prefix; GUARD-STRIP; {PIVOT,pure}`.
- **Repaired:** global fixed-width renaming now covers both old and fresh identifiers before isolation; empty proper input is a direct TRUE base and malformed input is parser-NO.
- **Repaired:** the least-covered-domain theorem now fixes a finite type set, one common `rho(N) -> 0`, one strict shrink threshold/base, promise runtime notation, multiplicity, transient workspace, retained state, and ancestor frames.
- **Downgraded:** `(6/5,1/2)` is proved only for `SAT|D*`, not for all SAT.
- **Corrected:** 3,010 pivots produced 115,943 raw pairs; ARC6 omitted 12,874 isolated pairs from its combined count.
- **OPEN:** an all-input PRE-A source-level compiler and hereditary successor coverage. Therefore P versus NP remains OPEN.

## Smallest falsification found

If types are countable and each type receives its own `o(1)`, let type `tau_k` binary-expand to two length-`N-1` children for `N < 2k` and shrink thereafter. Every fixed type has only finitely many bad lengths, but roots of type `tau_N` generate an exponential tree. Finite types plus one common convergence modulus repair this defect.

## Validation

- Bounded byte/grammar/pivot runner: PASS_WITH_ACCOUNTING_CORRECTION; 0.15 seconds on rerun, all invariant values and digest unchanged.
- Digest: `31d03a667d3d520d44bdca23b7684ccf5c8b629c82fbb36767bda37664eb751a`.
- Standalone report: two successful `pdflatex -halt-on-error` passes, 4 pages.
- `scripts/check_research_reports.py`: pass.
- repository research preflight `--check`: pass.
- Root `main4.tex`/`main5.tex` compilation remains blocked by pre-existing absent archived snapshots `main4_before_b7f40aa12692.tex` and `main5_before_406de99b1e12.tex`; the new additions themselves are included after ARC6.

## Next target

Construct or refute one fixed all-input phase derived from the assumed clocked polynomial SAT decider whose parent answer depends on essential, source-derived, strictly smaller ordinary-SAT children before any parent-scale semantic call, and prove every emitted successor re-enters the same finitely typed covered domain under one common charged ledger.

