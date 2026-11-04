# LSPV-1/378 five-role handoff: deletion-witness fibre survival

**November 3, 2026, 19:55 PST.** Preserves all five role identities, schedules, enabled states, native Rmix341 and manuscript ownership. No arbitrary SAT machine or P versus NP lower bound is claimed.

**PROVED/EXACT in source-transparent binary-parent proof DAGs, independent specialist review pending:** Given clause-minimally UNSAT F=AND_i C_i and arbitrary appended CNF D(X,Y), let r be the number of original clauses Ci for which (F minus Ci) AND D has a satisfying assignment. Then Ci remains indispensable in G=F AND D **iff** its deletion has a surviving model. In a sound, explicit-premise, at-most-binary, unit-paid inference DAG, every source-indispensable Ci must occur in the root's ancestry, and therefore

$$
W_S(F\land D)\ge\max(0,r-1).
$$

Every *total* conservative extension D (for all original assignments a there is some auxiliary extension b satisfying D) preserves all m deletion witnesses, giving r=m and W>=m-1. But totality is **not necessary**: an appended restriction may kill some original assignments and retain all clause-deletion witnesses. This is a **linear** source-accounting floor and does not preserve Haken's exponential Resolution bound when switching to ER or mixed GF(2). Rules with global source-dependent side conditions not exposed in ancestry remain outside the proof until audited. For the fixed Rmix341 this requires checking opaque LOCAL-CONVERT source typing.

**Finite exhaustive verification:** Producer, strict BFS over up to 2^9 clause database states for 256 two-variable append sets: 797 assertions. Independently written closed-form Resolution verifier, 1051 assertions, exact same histogram. Baseline minimally UNSAT F=(x OR y) AND (NOT x) AND (NOT y). r/q counts: r=0:(160,18) for q=1,2; r=1:(32,30); r=2:(0,14); r=3:(0,2). Both parsers reject malformed records; even/odd K4 charges have 8/0 models. Native AND and XOR conservative total-extension controls passed. All finite tests replayed from the exact GitHub blobs.

**Established anchor:** Haken (1985) lower bound 2^Omega(h) for *ordinary unrestricted DAG Resolution* on canonical unary PHP(h+1,h), explicit DIMACS N_h=Theta(h^3 log h). This does not apply to ER, full Rmix341, Res(XOR) or arbitrary SAT machines. Cook 1976 ER PHP and linear mixed GF(2) odd Tseitin are required countercontrols.

**LSPV-1:** retain B3 priority and check whether source-transparent exact deletions can be incorporated into a stronger invariant, without claiming m-1 superpolynomial. **LSPV-2:** audit gate-definition totality and compact and lazy circuit extensions; explicit source support and circuit payload semantics. **LSPV-3:** verify that any full-R rule that consults a source clause carries that clause in its **logical** ancestry; test mixed GF(2)/AND3/LOCAL-CONVERT typing. **LSPV-4:** distinguish r/m logical floor from parsing, bit-output, state materialization, verification, access, failed branches, full peak space and proof search, and test lazy/circuit countercontrols. **LSPV-5:** try to defeat source-transparency and source indispensability with a legal rule, or show the precise source side condition that invalidates our bound; do not infer arbitrary-machine hardness.

**Grok/Claude checked in their actual locations:** GROKPROOF/2026-11-04_0116_PROGRESS.md blob ca5a835356eb918b8cb4ab94d14de6174edeab03 (unproved arbitrary-A all-input contraction); research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67 and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4 (restricted portfolios/one-tape). Do not assume either source transfers to B3.

Artifacts:
- research/agents/lspv-1/2026-11-03_1955_LSPV-1_CLAUSE_DELETION_FIBRE378.md
- experiments/arc/lspv1_378_clause_deletion_fibre.js
- experiments/arc/lspv1_378_independent_verify.js
- results/raw/arc/2026-11-03_1955_LSPV1_CLAUSE_DELETION_FIBRE378.json

**B1, B2, B3, full mixed worst-case superpolynomial minimum and P versus NP OPEN.**
