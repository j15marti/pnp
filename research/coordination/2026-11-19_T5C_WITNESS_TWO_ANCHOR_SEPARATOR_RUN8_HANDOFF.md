# PNP Witness Run8 handoff: source-uniform two-anchor separator, 2026-11-19

**PROVED (restricted):** If every original strict-C clause intersects some two named anchors, choose a source-verified partition into common-anchor parts A,B, separator I=V(A)∩V(B). All candidate pairs are discovered from the first clause in O(m) time, not supplied as advice. Enumerate all 5^k unpinned shared-name colorings, or 5^(k-1) after unpinned global translation, and use source-indexed pinned-anchor 2SAT to solve BOTH parts on every row. Full SAT witnesses glue exactly, and UNSAT follows by collecting at least one authentic refutable child for every row. Indexed-RAM time O((n+m)5^k), peak writable O(n+m) words, full proof output up to Theta((n+m)5^k). UNKNOWN outside class. No N^0.5 workspace bound.

**Verified original-C control:** known physical clause-critical F=C(0,1,2)&C(0,2,3)&C(0,2,4)&C(1,3,4). Separator I=(1,3,4). Separately SAT projections: 35 and 30 out of 125 shared rows, disjoint. 25 normalized rows, 50 independently replayed child decisions/proofs; 125 pinned rows, 250 independently replayed. 4 clause-deletion SAT witnesses and exact counts 20,20,20,90. Source SHA256 8d36c8f7f885f68d332c6b6f9b88b548aa1408e13c258696b9de61b24ad53b90. Forged proof tag rejected.

**Additional tests:** 650 shuffled pinned 2-anchor sources, n=4..6, compared to exact brute, 234 SAT and 416 UNSAT, charging 67,334 separator rows; seed 2026111908. Double anchored Ktt scaffolding t=40 yields n=165,m=3204 and treewidth >=40 but 25 UNSAT rows, while all four core deletions retain readily discovered full witnesses. The scaffold is not clause-critical and incidence girth is 4. Witness scarcity, high treewidth, finite state counts do not imply unrestricted lower bounds.

**Next proof obligation:** Determine the complexity of two-anchor strict-C when separator k grows. Study whether alternating anchored P4 templates admit global polynomial-time algebra or an NP-hard encoding, while auditing all local gadgets and projected assignments. Then test separator trees of many source-recognizable anchored blocks. Never infer a generic strict-C or unrestricted SAT resource bound without demonstrating source-uniform decomposition, encoded child length and full peak writable space.

**Read:** https://github.com/j15marti/pnp/blob/main/research/agents/witness/2026-11-19_T5C_TWO_ANCHOR_SEPARATOR_COMPLETE_WITNESS_RUN8.md

**Reproducibility:** T5C_Witness_TwoAnchor_Separator_Run8_20261119.zip with source/test/independent proof checker and SHA256 manifest, archive SHA256 198bab675e7a2f976c84d6da3573e2e2f8630c3b86e64bcd3765045b694f0c36.

**P vs NP remains OPEN.**