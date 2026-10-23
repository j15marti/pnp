# ADAPTIVE-TERNARY-COLLAPSE69: independent Role 5 and Roles 1–3 handoff

**Status:** PROVED/EXACT in the declared source/backdoor/word-RAM model; COMPUTATIONAL finite corroboration. The universal P-versus-NP implication remains OPEN. No task schedules were changed.

## Construction (replay verbatim)

For q >= 1 and b in {0,1}^q, take z_0..z_q, y_0..y_q, p_0..p_q, and u,v. Emit these binary clauses:

- (z_0 OR u), (z_0 OR NOT u);
- (y_q OR v), (y_q OR NOT v);
- (NOT z_0 OR p_0);
- (NOT p_{i-1} OR p_i) for each 1 <= i <= q;
- (NOT z_{i-1} OR z_i) when b_i=1, or (NOT z_{i-1} OR NOT z_i) when b_i=0.

For each i=0..q emit exactly four ternary clauses:
```
(z_i OR y_i OR NOT p_i)
(z_i OR NOT y_i OR p_i)
(NOT z_i OR y_i OR p_i)
(NOT z_i OR NOT y_i OR NOT p_i)
```
These represent z_i XOR y_i XOR p_i = 0.

Exact ledger: n=3q+5; binary m_2=2q+5; genuine ternary k=4q+4; total M=6q+9. With four fixed-width words per clause and two header words, w=ceil(log2(64(9q+15))), N=(24q+38)w bits. Original variables z,u,v number q+3; p,y are 2(q+1) functional auxiliaries, no new free auxiliaries. Each complete original satisfying assignment extends uniquely by p_i=1 and y_i=NOT z_i. No initial unit or pure literal. Each ternary support {z_i,y_i,p_i} is disjoint, so raw strong syntactic 2-SAT backdoor h=q+1.

## Precise identities and switching requirement

The two clauses (z_0 OR +/-u) resolve to z_0. Binary implication closure gives all p_i=1. Then each four-clause XOR quartet reduces to two binaries (z_i OR y_i), (NOT z_i OR NOT y_i), enforcing y_i=NOT z_i. The endpoint (y_q OR +/-v) forces y_q=1 and hence z_q=0. The old implication chain remains, so SAT iff at least one b_i=0; UNSAT iff all b_i=1; #SAT is exactly the original F_b model count. The binary-only skeleton is SAT for all b, **including UNSAT full formulas**.

The analytic minimum seed trigger g_B=1 counts one source-justified pair-resolvent unit sufficient by binary propagation to touch every ternary. No solver is handed g_B or the optimum h. A total solver scans source, searches binary complementary pairs, propagates with an implication adjacency graph, simplifies all clauses, then chooses immediate UNSAT on an empty clause, SCC on a 2CNF residual, or complete DPLL fallback otherwise. It charges source reads, pair lookups, graph operations, propagation, simplification, policy evaluation, SCC/DPLL, reconstruction and peak live space. It does not use a preknown SAT label or fixed exponential formula.

An arbitrary total deterministic exact decider must read all q independent consequent-sign fields on H_{q,1^q}, since flipping any one makes a same-size SAT input. This gives only Omega(N/log N) addressed-word acquisition, tight by both direct source scanning and the adaptive solver. No universal superpolynomial lower bound follows.

## Independent Role 5 verification requests

1. Check the four ternary clauses encode *even* XOR; test all eight triples including p=0 and p=1.
2. Prove the parsimony and h=q+1 identities under raw syntactic restriction; distinguish semantic/propagation-aware backdoors.
3. Verify the binary-only skeleton is SAT for all b and that the forced pivot chain really collapses all ternaries with a certified one-seed implication chain.
4. Audit all counts n,m_2,k,M,N, plus q=1024 ledger, and ensure no uncharged shortcut discoverer.
5. Check the generic solver on arbitrary signed permutations, SAT and UNSAT, and the DPLL fallback. The independent review is not yet claimed.

## Role 1–3 hostile controls and first amplification attempt

Use matched H_{q,1^q} (UNSAT) and H_{q,0 1^{q-1}} (SAT). At q=1024, both have n=3077, M=6153, k=4100, h=1025, N=492280 bits. Raw binary SCC says SAT for both. The adaptive policy uses 43084 abstract events (UNSAT) or 68705 (SAT), while a declared non-pruning complete-backdoor enumerator at q=8 makes 512 leaf calls on both. This is a **restricted-policy** comparison, not all-decider coverage.

Propose then falsify a stronger mechanism: replace the XOR quartet with a source-uniform **non-affine, interacting** gadget for which no O(N)-discoverable local pivot closure exists. Track a vector state (raw k, raw h, certificate trigger g, detected units, remaining ternaries, available representations, peak live memory) at every phase. Try SCC, Horn, affine, cached joins, clause learning, decomposition, direct source recognition and generic exact fallback. A candidate lower bound must survive every adaptive combination, not merely this finite menu. SAT needs a witness or bit; UNSAT need not enumerate all assignments or emit a chosen refutation.

## Project and provenance

Published report: `research/agents/lspv-4/2026-10-24_0536_LSPV-4_ADAPTIVE_TERNARY_COLLAPSE69.tex`.
Standalone GitHub mini: `research/agents/lspv-4/2026-10-24_0536_ADAPTIVE69_MINI.py`.
Results summary: `research/agents/lspv-4/2026-10-24_0536_ADAPTIVE69_RESULTS.json`.
Full stdlib auditor SHA256: `107bebd6db2145ddca1aa95f048feead479aa772a80899fba2017e439327f648`.

The complete local five-suite audit recorded 1,315 assertions across 480 result records with zero failures. The five suites are small exhaustive, restricted backdoor enumeration, q<=1024 scaling, arbitrary fallback controls, and 400 adversarial/general randomized controls. Independent prior work includes original F_b chain, PRIORITY-HORN67, FUNCTIONAL-OCCURRENCE68, MAIN106 and Role 3 ADAPTIVE-SPLIT74. The finite tests are not asymptotic hardness evidence.

**Next missing lemma:** a model-matched structural measure, universal charged-work inequality, and coverage of every total uniform deterministic exact decider, all separately proved. P versus NP remains OPEN.
