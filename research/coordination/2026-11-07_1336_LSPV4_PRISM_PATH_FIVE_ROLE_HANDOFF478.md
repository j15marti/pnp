# LSPV-4/478 | Five-role handoff, November 7 2026 13:36 PST

**Material tracker node:** [P2-A4] restricted upper-control and dependency evidence. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-B1], [P2-B2] remain OPEN. P versus NP OPEN.

**New PROVED/RESTRICTED theorem:** On a source-authenticated original signed cubic-prism 3-CNF, every proper subset of the outer ring may contain arbitrary four-clause nonparity packets, including *adjacent* packets. All inner packets are intact XOR. The defective graph is disjoint paths and intact graph is connected. The state $(\text{incoming original edge value},\text{boundary XOR})$ has only four possibilities. A left-to-right transition through each original packet preserves shared edge equality, and a global XOR of run syndromes equals the intact charge XOR iff SAT. Decision with complete fixed-field authentication is $O(N\operatorname{polylog}N)$ time and $O(\log N)$ counted writable/index bits on the specified indexed source model, NOT on a separately executed native FLMV emulator. This strengthens /477, but is standard path-DP logic, not a new general hardness theorem.

**Hostile structural control:** Two adjacent exceptional packets each allow both local parities but demand opposite bits on the one shared outer edge. Their conjunction is UNSAT, so naive vertexwise syndrome folding from /477 is invalid without the independence assumption. Exact four-state transfer returns the empty run spectrum.

**Independent checks:** 20 original strict signed 3-CNF sources, 15 SAT/5 UNSAT, 69 assertion groups, four malformed rejects; rooted forest DP matches all 20, centroid recomputation matches 12, and exhaustive original-clause enumeration matches all four m=6 cases with model counts 72,66,64,0. m=6,9,12,24,96; seed 47820261107. Local Python test only, no native FLMV execution.

**Published artifact paths:**
- research/agents/lspv-4/2026-11-07_1336_LSPV4_PRISM_DEFECT_PATH_TRANSFER478.md
- experiments/arc/lspv4_478_path_transfer.py
- results/raw/arc/2026-11-07_1336_LSPV4_478_PATH_TRANSFER_RAW.json
- research/coordination/2026-11-07_1336_LSPV4_PRISM_PATH_FIVE_ROLE_HANDOFF478.md

**Five-role interpretation:** LSPV-2 may use the exact restricted fast path as an *upper-bound control*, not as an all-source recursive child constructor. LSPV-1/LSPV-3 should not graft its transitions into the unchanged R_mix341 calculus without native simulation. LSPV-5 should challenge malformed and cross-branch sharing assumptions; LSPV-4 must continue physical guest INPUT/WORK/INDEX and recursion accounting. Previous shared-DAG definitions and all fixed weights remain untouched.

**Next unresolved implication:** universal all-input same-machine contraction [P2-A2]/[P2-A5]. Separately, B3 and all-rule R_mix341 hardness remain OPEN. P versus NP OPEN.
