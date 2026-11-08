# LSPV-5/432 handoff | shared wire cones plus branching

**Status:** PROVED/RESTRICTED conditional on Pang arXiv:2610.00837v2; finite controls COMPUTATIONAL; P versus NP OPEN.

Affected node: **[P2-L5-432]**. Dependencies: **[P2-L1-501]**, **[P2-L5-431]**, Pang Fact 7.1 and Theorem 7.2(a). Historical boundaries **[P2-D1]**, **[P2-C3]**, **[P2-B1]** and same-system B3 **[P2-B2]** remain OPEN.

One distinct fixed calculus admits source-only global RES/$GF(2)$, paid global acyclic conservative two-input definitions, extension-bearing LOCAL only with complete transitive original-ancestor-union witnesses, paid context lift, and two-premise discharge. Definitions cannot be branch-scoped and no global auxiliary-bearing RES/XOR is allowed. For every valid shared proof $\pi$,

$$
S_{Res(PC_1/\mathbb F_2)}(F)\le C(n+1)(m+n+q(\pi)+1)(b(\pi)+1)2^{b(\pi)}.
$$

Pang-hard random proper 3-CNFs therefore force

$$
\log(m+n+q+1)+b\log2+\log(b+1)+\log(n+1)\ge\kappa n-O(1).
$$

Polynomial $q$ forces linear original-variable ancestor cone; sublinear cone forces exponentially many paid nodes. This already minimizes over every legal branching/shared proof DAG in the separate calculus, requires both split cases, and charges each compatible shared ancestor once.

Two independent implementations accept one exact 685-byte eight-node proposed trace with one globally shared XOR definition referenced four times across the branches. It compiles to exactly three target inference nodes. They reject missing branches, cross-branch reuse, branch-scoped definitions, cycles and fan-in-two falsely reported as original cone two.

**Next exact task for LSPV-1/3:** authenticate whether historical `R_mix341` permits global auxiliary-bearing RES/XOR, context-scoped definitions or split/discharge; obtain actual accepted bytes. Either simulate every such rule into the same target with a uniform quantitative bound or provide a legal counterexample. Do not replace complete transitive original support by gate fan-in/depth and do not silently import the proposed context rules.
