# LSPV-3/460 five-role handoff | 2026-11-06 PST

**Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.** A focused theorem on the established Chvatal--Szemeredi random 3-CNF (m=8n independent source clauses) rules out only immediate AND3 original-source merges, not unrestricted R_mix341 proofs.

## Analytic theorem and exact scope

For uniformly independent original variable triples, M=binom(n,3),

$$
\mathbb E Z_n = \frac{\binom{8n}{2}}{M}
= \frac{24(8n-1)}{(n-1)(n-2)}
=\frac{192}{n}+O(n^{-2}).
$$

Hence with probability 1-O(1/n) every original 3-clause uses a different *set of original variable names*. A proper three-literal clause has no nontrivial <=3-original-coordinate semantic consequence other than itself; therefore a restricted source-only derivation using support-3 AND3 and direct LOCAL-CONVERT cannot combine different sources or extract parity, even with shared DAGs. This does NOT restrict later local deductions after arbitrary RES, paid DEF, private/exported gates or cross-branch reconvergence. In fact LSPV-3/459 exhibits Theta(n) immediate legal width-4 source RES opportunities. Cubic odd-Tseitin has four clauses per triple and a 4h-1 paid mixed AND3/XOR shortcut (LSPV-2/341), so no claimed transfer from its ordinary Resolution hardness.

## Falsifier, experimental reproducibility and source integrity

Initial xorshift32 low-bit sampling produced suspect collisions at n=8192: 0,2,2,2 vs IID expected 0.023 per fixture. **Rejected this generator** rather than relying on its output. The replacement deterministic SHA256-counter procedure, independently implemented in Python and Node and NOT mathematically IID, yielded collision counts at seeds 11,23,47,89:
- n256: 0,0,2,1 (expected .7585 per fixture)
- n512: 0,0,0,1 (expected .3771)
- n2048: 0,0,0,0 (expected .0939)
- n8192: 0,0,0,0 (expected .02345).

Independent JS replay checked 1,421,493 assertion groups, original signed DIMACS SHA hashes, exact clause/pair counts, eight-row GF(2) source-parity control, and rejected four intentional mutations. None of the deterministic random fixtures were independently UNSAT-certified; this is not execution of the authoritative historical R_mix341 byte checker.

## Role-by-role next falsifier

**LSPV-1 / LSPV-5 (Route B):** Audit whether arbitrary wide RES and paid DEF can create inexpensive cross-source local factors, check owner-qualified facets, sharing and original-source provenance. B3 stays OPEN. **LSPV-3 (Route B):** Prioritize authenticating the historical DEF/LOCAL/private-export-port byte grammar or constructing a legal all-rule normalizer/counterexample. **LSPV-2 / LSPV-4 (Route A):** This restricted original-local scarcity is *not* a physical time/space lower bound and gives no same-machine FLMV contraction. All agents must preserve prior valid work, two Route A/three Route B allocation, no schedule/weight changes.

Relevant repo reports: LSPV-3/438 established Tseitin cut-parity projection, LSPV-1/423 established Tseitin minimum mixed span, LSPV-3/459 unrestricted-RES width4/5 escape, LSPV-1/457 separately declared bidirectional ER 3-CNF transport. Full report: research/agents/lspv-3/2026-11-06_LSPV3_RANDOM3_AND3_SOURCE_LOCALITY460.md. Code in experiments/arc/lspv3_460_source_triples.py and experiments/arc/lspv3_460_independent_verify.mjs; compact raw results in results/raw/arc/2026-11-06_LSPV3_460_RANDOM3_SOURCE_COLLISIONS.json; rejected PRNG raw and complete proofs in user-facing reproducibility archive. Historical R_mix341 /341 blob c87acd11.

**OPEN:** Historical accepted-byte LOCAL-CONVERT / DEF semantics, arbitrary full mixed DAG proof normalization, superpolynomial Wbar_R, noncircular B3. Root main.tex unchanged due current GitHub SHA but empty content readback. P versus NP OPEN.
