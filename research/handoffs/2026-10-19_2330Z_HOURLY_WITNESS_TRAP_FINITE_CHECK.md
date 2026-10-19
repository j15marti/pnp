# HOURLY check 2026-10-19 23:30Z — finite verification of CANONICAL-WITNESS-TRAP9
**P versus NP remains OPEN.** Scope: partial corpus survey (latest MAIN, REDTEAM27 handoff, recent commits); not a full corpus-wide LSPV reconciliation; root `main.tex` untouched.

Status of check: COMPUTATIONAL (finite instances only; does not strengthen the PROVED/EXACT theorem).
Script: `research/experiments/witness_trap_min_circuit_check.py` (single run, a few seconds; exhaustive min-circuit search over all 16 binary gate types).

| n | #SAT assignments of trap CNF | min gates canonical W0 | min gates alternate W1 | proved bound n-1 |
|---|---|---|---|---|
| 1 | 2 | 1 | 0 | 0 |
| 2 | 2 | 2 | 0 | 1 |
| 3 | 2 | 3 | 0 | 2 |

Consistent with the n-1 lower bound (observed n; upper bound n via XOR chain + one AND). Confirms exactly two satisfying assignments. Says nothing about hardness of every witness for the actual diagonal family; that arrow (uniqueness + hardness of the unique witness, or all-witness hardness) stays OPEN.
