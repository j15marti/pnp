# Polynomial-SAT assumption audit and next proof obligation

2026-11-11 12:03 PST. **P versus NP remains OPEN.**

## Result

The audit assumes one total correct uniform SAT decider with an arbitrary fixed polynomial exponent. It establishes accounting and representation controls, and refines the conditional growth comparison already in LSPV-1/540. It obtains no contradiction to P = NP.

Report: `research/agents/codex/2026-11-11_1203_SAT_POLYNOMIAL_ASSUMPTION_AUDIT.tex`.
Bibliography: `research/agents/codex/2026-11-11_1203_SAT_POLYNOMIAL_ASSUMPTION_AUDIT_refs.bib`.

## Material findings

1. A SAT-oracle reduction with construction exponent h, query-count exponent b, and query-length exponent a yields exponent max(h,b+ac) under an assumed SAT exponent c. An independent lower exponent lambda contradicts this only when lambda exceeds both terms. Ruling out every c requires unbounded reduction-normalized lower exponents, or a different transfer.
2. The fixed-r bridge comparison from /540 sharpens to the sufficient condition limsup log W_R(N)/(log N)^r = infinity. A factor log log N beyond that envelope would already yield a mildly superpolynomial SAT lower bound. Neither premise is proved.
3. An all-decider quasipolynomial runtime bridge plus superquasipolynomial proof growth excludes quasipolynomial SAT algorithms too. The weaker hypothesis-only target SAT in P implies W_R in QP avoids that excess obligation. Given W_R outside QP, proving that target is still logically equivalent to the desired separation; it is not an established shortcut.
4. The November 2026 Strassle–Subercaseaux generalized Cook–Levin decomposition has explicit branching and construction costs. Substitution of polynomial SAT yields the expected polynomial simulation at b=t, without the strict power contraction needed for a hierarchy contradiction.
5. Arbitrary 3-SAT admits an arity-three circuit-CSP representation with variable factor-degree at most two. Equality expansion uses up to four literal occurrences, so degree-two factors do not mean occurrence-two CNF.
6. A SAT and UNSAT source pair produces identical eight-factor, ten-variable unsigned incidence matrices of GF(2) rank seven. Relation polarity remains essential.
7. Polynomial total actual query volume stays polynomial under P = NP, even at polynomial same-candidate sequential depth. A clocked self-reference construction needs a sufficiently small explicit encoding, not merely semantic self-reference.

## Reproducible evidence

Complete script: `experiments/review/sat_contradiction_degree2_audit_20261111.py`.
Raw JSON: `results/raw/review/2026-11-11_SAT_CONTRADICTION_DEGREE2_AUDIT.json`.

The deterministic finite audit passed 676 formulas, 2,694 source-assignment lifts, and 56,937 complete CSP assignments, with zero failures. It checked occurrence counts one through seven, both labels, repeated literals, tautologies, empty clauses, expanded CNF equivalence, and the same-incidence pair. The general representation theorem is proved symbolically in the report. These checks are not unrestricted time lower bounds.

Code SHA-256: `901465d00a001e0887250f7224b9e8b96553cdeb2da7c62bec092ba897554676`.

## Reconciliation

Adopt /540 as prior work; retain /478 and /479 limitations. Preserve REFEREE295's distinction between pointwise and global bridges. The latest finite source-cost intervals and fixed-DAG scheduling results retain their restricted status. The root manuscript was recovered by blob SHA 82c36196547752a4d83e21b40bec006cb94ceddb and relevant sections inspected. This is an ordinary Codex report for LSPV-5 reconciliation, not an edit to any role-owned manuscript region.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to open proof-chain nodes.

## Validation

Independent mathematical review found three small issues, all corrected: the global time hypothesis now quantifies every formula explicitly, query accounting retains length + 1, and the proof-system simulation states the required proof-length-to-native-cost condition. Repository preflight and report-hygiene checks passed on the fresh partial snapshot. The LaTeX source was not compiled to PDF because this runtime lacks pdflatex.fmt. No PDF verification is claimed.

## Single next target

For one authenticated fixed proof calculus R, specify a quasipolynomial simulation of the solver-induced UNSAT proof system S_A for every hypothetical polynomial-time SAT decider A. Prove it using the polynomial-time hypothesis, with all encoding and native proof costs charged. Pair it only with an independently proved sufficiently strong lower bound for the same R. Do not substitute an arbitrary existential Cook–Reckhow proof system for the preselected calculus.

