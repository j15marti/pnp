# LSPV-5/453 five-role handoff: explicit contexts and AND discharge

**Node:** `[P2-L5-453]`  
**Classification:** **PROVED/RESTRICTED** plus **COMPUTATIONAL** controls.  
**P versus NP:** **OPEN**.

## Reusable result

For any sound, acyclic, source-explicit branching proof DAG with an empty-context false root, the original-source ancestors form an UNSAT subset. Therefore the semantic source cover `[P2-L5-452]` survives arbitrary legal branching, reconvergence and shared lemmas. If paid nodes have maximum indegree $a>1$, then $q\ge\lceil(r-1)/(a-1)\rceil$. A node shared between complementary branches must be valid under a context contained in their intersection; a branch-local conclusion cannot cross that boundary.

This uses a distinct proposed `BRANCH_CTX` control with explicit `SPLIT_AND`; it does not modify or authenticate historical `R_mix341`. The exact packet has 3 sources, 7 paid nodes, span 3 and one source shared twice/count-once. An independent verifier passed 65 checks and rejected seven hostile mutations.

## Role actions

* **LSPV-1:** any claimed native branching certificate must identify the historical rule bytes, record both AND premises and preserve context provenance. Do not import `SPLIT_AND` from this control.
* **LSPV-3:** mutate future packets for omitted sibling cases, cross-branch false reuse, root assumption leaks and duplicate charging; compare exact accepted bytes if a historical checker appears.
* **LSPV-2/LSPV-4:** Route A may use the theorem only as a proof-DAG control. It supplies no same-machine all-input contraction.
* **LSPV-5:** next test the first authenticated historical candidate for implicit ambient-source access; otherwise strengthen the established-family transfer, not the toy packet.

## Still open

`[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, and `[P1-X1]`. The restricted theorem does not establish a full mixed-calculus lower bound, noncircular B3, or P versus NP.
