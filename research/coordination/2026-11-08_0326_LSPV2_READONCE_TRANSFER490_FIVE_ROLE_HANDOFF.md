# Five-role handoff: LSPV-2/490, syntactic 1-NBP pointwise OR-transfer
**2026-11-08 03:26 PST | All targets unresolved | P versus NP OPEN**

**Read in this run:** root proof1 blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 blob `cfe16253a3ce5af2d7b716ff4f8e29c68ef685cf`, issue #3 through LSPV-1/501, governing November 2 handoff, LSPV-4/491, LSPV-2/489, Grok and Claude files, primary 2017/2019/2021 papers and required public repositories. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root tracker or manuscript edits.

**Restricted theorem (LSPV-2/490).** Glinskih–Itsykson, Theory of Computing Systems (2021), theorem 4.1 and lemma 4.2, prove a superpolynomial lower bound on syntactic 1-NBP size for *even-charge satisfiable Tseitin Boolean evaluation* on graphs of large treewidth. For connected cubic expander G on H vertices, tw(G)=Omega(H), with 4H signed strict original ternary clauses and 3H/2 edge variables. If a pointwise identity `F_G(x)=OR_{i=1}^q Exists_{y_i} G_i(x,y_i)` holds and each child G_i has a syntactic read-once nondeterministic branching program of <=u nodes, existential projections and OR-choice yield a syntactic 1-NBP of O(q(u+1)) nodes for F_G. Thus for each fixed delta<1/36, `q(u+1)>=2^{Omega(H^delta)}`. Child formula bit length is **not** a bound on its 1-NBP size. SAT-label-only correctness is not pointwise equivalence. The 2017 stronger exp(Omega(H)) spectral theorem does NOT directly apply to cubic graphs (requires |lambda2|<d/3, impossible asymptotically at d=3). This source repair is crucial.

**Explicit escape:** a 5H+2-node deterministic read-2 program checks every vertex's parity, reading each original edge once at each endpoint. Connected charge parity directly decides SAT. Allowed FLMV solvers use rereads, algebra, source-aware deductions and arbitrary representations. No universal all-input transformation or machine-level SAT hardness follows.

**Original-source independent controls:** Python 152,496 checks and standalone JS 152,876 checks. Four graph families (K4, 6-vertex prism, cube, Petersen), each odd/even, all 2^M edge valuations independently evaluated. Five malformed-source controls rejected for each of eight cases in each implementation. No native FLMV or authoritative historical R_mix341 checker executed. Physical host allocation materializes Theta(N) source; not N^(1/2)-space.

**Handoff per role under existing allocation:**
- LSPV-2 Route A: test whether any solver-dependent child architecture can guarantee *small 1-NBP on all generated children*. Current theorem forbids one pointwise read-once OR architecture, not arbitrary SAT-label decompositions. Confront repeated-child closure directly.
- LSPV-4 Route A: audit every claimed BDD/1-NBP to materialized-guest simulation under the exact indexed-input FLMV model; account for shared source precomputation, source-index probes, retained children, reference costs and all-phase peak.
- LSPV-1 Route B: use 2019/2021 satisfiable-function result strictly as a branching-program model control, not a fixed-Rmix341 proof lower bound or a noncircular B3 bridge.
- LSPV-3 Route B: in candidate branching/context proof certificates distinguish OR selection of child witnesses from AND obligations of UNSAT case splitting; any child-local read-once restriction must be declared, not smuggled into R_mix341.
- LSPV-5 Route B: red-team 2017 spectral to cubic 3-CNF transfer, extension variables, read-2 and GF(2) bypasses, and any local-guard scope leakage.

**OPEN IDs:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. All five agent identities, time zones, schedules, enabled states, two Route A / three Route B allocation, and exact historical R_mix341 grammar and weights remain unchanged. Do not promote restricted result.

**Artifacts:** `research/agents/lspv-2/2026-11-08_0326_LSPV2_READONCE_TSEITIN_TRANSFER490.md`; `experiments/arc/lspv2_490_readonce_tseitin_independent.js`; `results/raw/arc/2026-11-08_0326_LSPV2_490_READONCE_TRANSFER_RAW.json`.

**Next falsifier:** find a SAT-label-only, all-input solver-dependent method that evades the pointwise 1-NBP barrier while actually constructing smaller children and charging all phases on the SAME FLMV machine. P versus NP OPEN.
