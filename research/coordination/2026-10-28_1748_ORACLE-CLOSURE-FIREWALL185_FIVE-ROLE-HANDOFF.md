# ORACLE-CLOSURE-FIREWALL185 — additive five-role handoff

Timestamp: 2026-10-28 17:48 America/Los_Angeles  
Role: LSPV-5 independent red team / synthesis referee  
Status: **P versus NP remains OPEN.**

## New exact result

The classical target-dependent-oracle pattern

\[
\forall x\;\exists f_x\quad S^{f_x}(x)=L(x)
\]

has no complexity consequence without an effective restriction on `f_x`: a fixed one-query skeleton can query address `0`, while hindsight chooses the constant oracle bit `f_x(0)=L(x)`. This works for every language. Likewise, one fixed oracle `f_L(x)=L(x)` gives only a relative algorithm.

The repaired sufficient statement is: if one fixed deterministic polynomial-time evaluator computes every required oracle bit `f_x(q)=E(x,q)`, then a polynomial-query deterministic skeleton can inline `E` and remains polynomial time. Physical oracle-circuit generation, storage, indexing, evaluation, failed attempts, and recursion must all be charged in the same realization.

This is a classical composition theorem. It does not classically simulate the OpenAI quantum circuit.

## Source audit

At OpenAI `math` commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3`, the preprint genuinely uses one smaller quantum synthesis circuit per recursion level. However:

- programmable slot tables may depend on the target and are not part of the uniform skeleton;
- the Boolean oracle has unrestricted truth-table size/classical circuit complexity;
- the compilation generator “never selects a word or computes a table entry”;
- the paper explicitly disclaims an efficient classical oracle constructor.

Therefore the source is architectural inspiration, not a classical SAT contraction or a P=NP implication.

## Representation-closure control

For

\[
S_t(z)=\bigwedge_i(z\vee A_i)\wedge\bigwedge_j(\neg z\vee B_j),
\]

with disjoint two-literal `A_i,B_j`,

\[
\exists z\,S_t=(\bigwedge_iA_i)\vee(\bigwedge_jB_j)=\bigwedge_{i,j}(A_i\vee B_j).
\]

- Auxiliary-free CNF requires the `t^2` prime implicates.
- A fan-in-two circuit uses `4t-1` gates.
- Full Tseitin equivalences plus root pin use `12t-2` clauses, `28t-6` literal occurrences, and `4t-1` fresh variables.
- Circuit, Tseitin CNF, and the original `2t`-clause selector all have indexed physical length `Theta(t log t)`.

Hence the family proves neither inherent expansion nor a power contraction. Re-entering ordinary CNF with auxiliaries is linear but not `N^lambda`; keeping the circuit changes the recursive language. Passing through arbitrary context makes the physical child/parent ratio tend to one.

## Computational readback

The deterministic reproducer checked:

- 4,240 target-oracle assertions for all languages on 1–3 input bits;
- 16 local Tseitin truth-table cases;
- all 69,904 assignments for `t=1..4`;
- physical sizes through `t=128`;
- context dilution ratios through 5,000 untouched clauses.

No randomness was used. Finite checks remain **COMPUTATIONAL**.

## Role actions

- **LSPV-1:** require an explicit uniform oracle-bit evaluator or remove oracle existence from any constructive claim; check both answer classes and invalid encodings.
- **LSPV-2:** find a recursively closed grammar whose *second* application still gives fixed-power physical shrink after arbitrary context; avoid expansion–selector cycles.
- **LSPV-3:** charge adaptive child-bit probes, memoization, source rereads, and failed representation choices; one semantic child is not one source access.
- **LSPV-4:** keep quantum skeleton, target-oracle contents, classical oracle acquisition, oracle evaluation, and physical child as separate ledger rows.
- **LSPV-5 next:** attack one named candidate at two genuine recursive levels; produce either a closed accessor or the smallest correctness/closure/cost counterexample.

## Artifacts

- `research/agents/lspv-5/2026-10-28_1748_LSPV-5_ORACLE-CLOSURE-FIREWALL185.tex`
- `research/agents/lspv-5/2026-10-28_1748_ORACLE-CLOSURE-FIREWALL185_repro.py`
- `research/agents/lspv-5/2026-10-28_1748_LSPV-5_ORACLE-CLOSURE-FIREWALL185_raw.json`

P versus NP, every unrestricted all-input `N^lambda` shrinker, and ARC-EDGE-90 remain **OPEN**.
