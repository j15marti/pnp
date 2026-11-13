# LSPV-1/604 five-role handoff: finite MAY-state lower-bound ceiling

**2026-11-12 15:56 PST | Historical Route B | PROVED/RESTRICTED mathematical corollary + COMPUTATIONAL. P versus NP OPEN.**

**Exact finding:** For a finite reachable MAY abstraction with \(M\) states, goal reachability, nonnegative edge costs at most \(\kappa\), complete native-step cost-sound simulation, and completed-refutation preservation, every admissible Bellman potential at the initial state is bounded by \(\kappa(M-1)\). The bound is sharp on a unit-paid chain. Thus any finite-state sound-MAY certificate of superpolynomial paid work, with fixed rule maximum charge, needs superpolynomially many *distinct abstract states*. This does **not** imply superpolynomial actual W, memory or solver time. A compact \(b\)-bit symbolic state can denote one of \(2^b\) states. This is an incremental corollary of LSPV-1/589's sound potential theorem, not a new proof-complexity lower bound.

**Reproducible evidence:** 4,096 independently enumerated 3-state directed weighted graphs, 24,576 ordered distinct source/goal pairs, 21,888 reachable, 2,688 unreachable; Dijkstra and explicit simple-path enumeration agree on all 24,576. Zero bound violations, exact distance maximum 4 with costs in 0..2; unit-chain sharpness for 2..10 states; a speculative free MAY edge collapses a cost-4 chain lower bound to zero.

**Files committed and read back:**
- [LSPV-1/604 report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-12_1556_LSPV1_MAY_STATE_CARDINALITY_CEILING604.tex)
- [Executable Python](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_604_abstract_state_cardinality.py)
- [Raw exhaustive evidence](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_1556_LSPV1_604_ABSTRACT_STATE_CARDINALITY_RAW.json)

**Role interfaces:** LSPV-1 maintains exact P2-D1 -> P2-C3 -> P2-B1 quantifiers and preserves B2/B3 separately. LSPV-2 and LSPV-3 must continue seeking one genuine original-source-bound complete historical \(R_{\mathrm{mix341}}\) mixed-rule checker; two archived sibling grammars, or their raw-byte product, are insufficient. LSPV-4 should distinguish the number of possible abstract states from peak physical space. LSPV-5 should independently falsify the cardinality ceiling hypotheses and test cost- or goal-unsound abstract shortcuts. No use of this general graph theorem as a proxy for full native calculus authentication.

**Dependencies/status:** P2-D1 OPEN, P2-C3 OPEN, P2-B1 OPEN; P2-B2 and P2-B3 separately OPEN. Complete source and proof accepted-byte grammar missing. TRACKERS REVIEWED; NO MATERIAL CHANGE. Exactly five existing roles, titles, schedules, weights, ownership regions and TWO Route A/THREE Route B allocation unchanged. No automations modified. P versus NP OPEN.