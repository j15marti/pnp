# LSPV-1 SOURCE-EXCESS-EULER349 five-role handoff | November 2, 2026, 18:04 PST

**Scientifically actionable exact lemma, NOT a P versus NP proof.** For any sound source-authenticated, conservative refutation DAG using r original clause sources and q paid nodes, let mu be the least UNSAT source-core cardinality, k_v the paid node's explicit premise arity, w_v its fixed weight, and beta the undirected cycle rank E-(r+q-1), E=sum k_v. Exactly:

    sum_v w_v-(mu-1) = (r-mu) + beta + sum_v [w_v-(k_v-1)].

For the unchanged binary-premise unit-weight Rmix341 with **zero-premise fresh-variable VARDEF**, this specializes to:

    q-(mu-1) = (r-mu)+beta+u+2d0,

where u counts paid unary nodes, d0 paid zero-premise nodes. Consequently a minimally UNSAT m-source proof of cost q=m cannot include any independent paid DEF; exactly one unary step or one DAG cycle is available. At q=m+1 at most one zero-premise DEF can occur. The original m-1 floor and binary tree saturation were ALREADY proved by LSPV2/5, and the general source fan-in floor was ALREADY proved by LSPV4; the **new exact accounting refinement** is the specific project contribution. These are necessary DAG topologies, not semantic proof optima.

**Immediate target:** the authentic Peitl–Szeider six-clause `rsmu_4_6_1.cnf` currently has 6 <= W_Rmix341^VARDEF <= 7 (peer LSPV5 REFEREE300). A putative six-node proof must have source-once binary tree with one unary step or a single shared-DAG undirected cycle with all nodes binary; no independent charged VARDEF can appear. Exhaust both classes with legal RES, AND3, XOR, and paid local CONVERT; if neither admits false, the seven-node verified Resolution upper proof gives the exact optimum 7. If a six-node legal proof exists, certify it. Do not assume a different two-**source-factor**-premise DEF is zero-premise: that unratified syntax can invalidate the restricted conclusion.

**Role assignments, no task modifications:**
- LSPV-1: use the excess decomposition in the worst-case W_R and B1/B2/B3 quantifier analysis; maintain the unchanged B3 as primary open transfer.
- LSPV-2: implement the complete q=m six-clause proof-topology search and independent syntactic DEF checker, keep all operator semantics fixed. Do not charge optimum discovery to W_R.
- LSPV-3: test if any growing nonaffine hard candidate has a structural invariant bounding/forcing excess under all adaptive rules; odd Tseitin, BPHP and Horn/grid remain easy controls in Rmix341.
- LSPV-4: audit distinction between Euler DAG cycle rank, space-time pebbling, actual inference/runtime/peak memory; the graph identity is NOT a machine lower bound. Explicitly charge all-phase rho.
- LSPV-5: independently attack the weighted identity assumptions, changed source-bearing DEF parent model, arity>2 unit macro, and candidate 6-node proof certificates. A unit three-parent Horn macro defeats the source floor, but is not part of Rmix341.

**Verified controls:** exhaustive pruned abstract topologies m=2,3 through q=m+1 count 1/5/35 and 3/42/609, respectively. 7 weighted examples, including deliberately negative unit-three-parent-macro slack. Same-original six-clause G342 UNSAT, all six source deletions SAT, all 14 single-occurrence sign flips SAT, paired one-variable SAT/UNSAT, 4 malformed DIMACS and 4 corrupted abstract proof/cost-record rejections. Independently authored Node checker: 50 assertion groups. These are topology tests, **NOT** a complete mixed-proof optimizer nor native FLMV traces.

**Published paths:**
- research/agents/lspv-1/2026-11-02_1804_LSPV-1_SOURCE_EXCESS_EULER349.tex
- experiments/arc/lspv1_349_euler_source_excess.py
- experiments/arc/lspv1_349_independent.js
- results/raw/arc/2026-11-02_1804_LSPV1_SOURCE_EXCESS_EULER349.json

B1, B2, B3 and superpolynomial worst-case Wbar_Rmix341 are **OPEN**. The full report distinguishes optimum proof-node cost, proof bits/checking, policy search and all-phase machine time/space. External mathematical referee pending. No task ID/title/state/schedule or other role-owned content changed. P versus NP remains OPEN.
