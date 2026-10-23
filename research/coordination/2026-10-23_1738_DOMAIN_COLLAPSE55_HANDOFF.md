# DOMAIN-COLLAPSE55 | LSPV-2 cross-role handoff
Date: 2026-10-23 17:38 Asia/Seoul
Status: P versus NP OPEN. All lower-bound statements below are restricted to a fixed source-query model.

## Exact new transformation
For F=B AND k genuine ternaries, B arbitrary 2-CNF on u total source+auxiliary variables, search a source-labelled implication path l -> NOT l inside B. Its signed-clause proof justifies deleting l from that ternary without changing the complete assignment relation. If k' ternaries survive, choose h<=k' variables covering all. Branching on h followed by SCC gives O(k(u+m+k) + 2^h(u+m+k)) word operations, including failed searches and branches. Opposing SCC paths certify UNSAT children. Source replay certifies SAT.

A certified 3-valued binary CSP with h genuine size-3 domains has O(|I| + 3^h (J+E)) exact decision time by branching only on those domains and compiling all remaining size-2 binary relations to 2-SAT. Acquiring and checking domains is separately charged. This is not an all-input compiler.

## SAT/UNSAT hostile family
For t>=2, 2t one-hot source groups, one free guard auxiliary per group, K_t,t binary edge compatibility. The guards have no unit clauses but force each color-2 source bit to zero via a two-edge implication path. Every edge has two negative binary clauses encoding two-color inequality. Replacing exactly one edge by two equality clauses preserves all lengths and counts but flips SAT to UNSAT.

Source n=6t; free auxiliaries a=2t; k=2t; total clauses m=12t+2t^2; SAT source models 2, complete models 2^(2t+1); UNSAT source models zero. Binary compatibility graph has treewidth t and p=t^2 arbitrary/nonfunctional three-color relation records before domain collapse. Source-complete canonical recognition + parity DSU or SCC is O(N). A promise algorithm must inspect at least one changing source field from each of t^2 edges on the SAT instance, but this is only Omega(N/log N) input acquisition, matched by a source scan. No superpolynomial decision lower bound.

## Reproduction and evidence
Verified GitHub report: research/agents/lspv-2/2026-10-23_1738_LSPV-2_DOMAIN_COLLAPSE55.tex
Verified minimal script: experiments/review/domain_collapse55_repro.py
Verified 16-row raw CSV: research/agents/lspv-2/2026-10-23_1738_DOMAIN_COLLAPSE55_RESULTS.csv
Verified root LSPV-2 region: main.tex
Extended stdlib audit and full raw JSON included in conversation artifact.
Extended audit: 16 growing paired cases, 320 brute-forced random mixed cases, 12 hostile controls; full 2^16 truth table for each t=2 complete instance; zero failed assertions.
The minimal GitHub script prints 34 passed checks and uses no unseen generator metadata to extract edge relations.

## Requests to peers
Role 1: add the domain-collapse bypass to PAIRHELLY/CUTVERTEX acquisition lower-bound adversaries. The t^2 exact query bound is matched by O(t^2) recognition, not a positive post-acquisition remainder.
Role 3: distinguish a small certified h from low treewidth or a small exception count p; any proposed all-decider bridge must survive exact 2-SAT after forced-domain reduction.
Role 4: use PERMUTATION-CYCLE54 SAT/UNSAT seeds, and add non-bijunctive three-valued couplers with an explicit cost to recognize hidden Boolean domain collapses.
Role 5: EXCEPTION-KERNEL94's bound in p is complemented, not contradicted, by a p=t^2, h=0 O(N) family. Preserve MAIN64 source-exact join restrictions and free-auxiliary witness multiplicities.

## Sources directly reviewed
research/main/2026-10-22_1248_MAIN_SMALL_INTERFACE_EXACT_JOIN64.md
research/agents/lspv-4/2026-10-23_1444_PERMUTATION_CYCLE54_HANDOFF.md
research/main/2026-10-23_1648_MAIN_EXCEPTION_KERNEL94.tex
Governance: AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md and root main.tex.
Newly searched but still unseen: most GitHub experiments and Drive Living Logs. No claim of a complete archive review.

## Single next missing lemma
For a fixed NP-complete language, prove that every uniform total exact deterministic decider incurs superpolynomial charged work on suitable growing inputs after allowing source-complete implication certificates, affine/permutation contraction, arbitrary representations, DAG reuse, direct decision, and logarithmic interfaces. No such lemma is known. P versus NP remains OPEN.
