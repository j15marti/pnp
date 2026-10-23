# SHARED-INTERFACE-TABLE92 handoff

**Status:** P versus NP remains **OPEN**. The new theorem is **PROVED/EXACT only in the declared explicit-table/word-query model**; the finite audit is **COMPUTATIONAL**.

## New exact result

For a `J x K` Boolean compatibility table with `K=2^h`, define

`f(R) = OR_a AND_j R[j,a]`.

The exact deterministic orientation-field decision-tree complexity is `J*K`: the unique multilinear polynomial has the full monomial with nonzero coefficient. A fixed-metadata CNF uses `h` selector variables, one forced cell variable per table entry, and a clause saying “if the selector is `a`, then this cell is 1.” Standard fresh-variable gadgets give ordinary proper 3CNF with `Theta(J*K*h)` clauses/variables and exact satisfiability preservation.

This does **not** amplify the chain bound. The explicit table already has `J*K` fields, so the lower bound is only input acquisition. A paid reduction costs `Theta(J*K*h)` and makes the positive transport remainder nonpositive; direct inclusion preserves only `Omega(N/(h log N))` word probes under the stated record encoding.

## Ladder reconciliation

- Fixed-width 2-CNF chain: exact `q`-field bound; linear SCC upper bound.
- 2-CNF plus `k` ternaries: `2^k poly(N)` upper bound; `k=O(log N)` polynomial; exponential necessity OPEN.
- CRITICAL65 and PERMUTATION-HOLONOMY50: large cores/backdoors/coupling coexist with charged linear/polynomial recognition.
- AGGREGATION-CEILING91: independent composition stays at input order.
- SHARED-INTERFACE-TABLE92: explicit shared compatibility also stays at input order.
- Succinct shared compatibility and unrestricted proper-3CNF time lower bounds: OPEN.

## Resource ledger

- Source: `M=J2^h` aligned orientation records, `N_src=Theta(Mw)` bits.
- Exact source decision: `M` field/record/word probes, `O(M)` word time, `O(1)` auxiliary words.
- Proper-3CNF map: `Theta(Mh)` source/output work; `O(h)` streaming workspace or `Theta(Mh)` retained-output peak.
- Packed encoding: only `Omega(M/w)` word probes.
- No inference to SAT-solving circuits, proof systems, or unrestricted superlinear time.

## Audit

- Seed: `20261023`
- 356 exhaustive tables; 400 seeded controls
- 756 proper-3CNF SAT checks
- 1,605 assertions; 0 failures
- Hostile controls: all-zero, all-one, single-good-column, one-zero-per-column, hidden shared interface

## Artifacts

- Report: `research/main/2026-10-23_1448_MAIN_SHARED_INTERFACE_TABLE92.tex`
- Code: `experiments/review/shared_interface_table92_audit.py`
- Raw: `results/raw/review/SHARED_INTERFACE_TABLE92_raw.json`

## Sources reviewed

Root governance and pnp-research protocols; SMALL-INTERFACE-EXACT-JOIN64; ROOT-LABEL-QUOTIENT85; AGGREGATION-CEILING91; CRITICAL65; PERMUTATION-HOLONOMY50; Aspvall--Plass--Tarjan (1979); Schaefer (1978); Cook (1971).

## Highest-value next lemma

Prove an all-algorithm **succinct-compatibility dichotomy**: on a fixed succinct proper-3CNF family with independently defined `h=omega(log N)`, every exact uniform decider must either acquire/validate a context-complete source-closed summary at `2^Omega(h)` charged cost or pay `2^Omega(h)` in direct continuation. The statement must survive decide-first normalization and every easy control listed in the report.
