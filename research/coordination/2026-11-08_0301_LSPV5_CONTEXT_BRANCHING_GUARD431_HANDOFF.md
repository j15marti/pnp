# LSPV-5/431 handoff | contextual branching guard transfer

**Status:** PROVED/RESTRICTED conditional on Pang's cited preprint; finite controls COMPUTATIONAL; P versus NP OPEN.

Affected tracker node: **[P2-L5-431]**. Dependencies: **[P2-L1-500]**, Pang Theorem 7.2(a)/Fact 7.1, ordinary guarded Resolution. Unchanged open boundaries: **[P2-D1]**, **[P2-C3]**, **[P2-B1]** for full historical `R_mix341`, and **[P2-B2]**.

One fixed distinct calculus $R_{\mathrm{ctxlog}}$ permits source-authenticated RES, global $GF(2)$ addition, explicit-table LOCAL steps on support $b(n)=\lceil\log_2(n+2)\rceil$, paid context lift, and binary discharge from both $\Gamma,x\vdash L$ and $\Gamma,\neg x\vdash L$ to $\Gamma\vdash L$. Nodes form an acyclic context-labelled hypergraph; a branch-local lemma cannot enter an incompatible context. Translating $\Gamma\vdash L$ to the common guard $G_\Gamma\vee L$ makes discharge one native Resolution step per output clause and yields

$$
S_{Res(PC_1/\mathbb F_2)}(F)\le c(n+1)(b(n)+1)2^{b(n)}(q+m+n+1).
$$

Pang's $F(n,3,8n)$ lower bound therefore gives $q=\exp(\Omega(n))$ with high probability and worst-case $\exp(\Omega(N/\log N))$ along an unbounded encoded-length sequence. This minimizes over every legal branching/shared DAG of the separate restricted calculus; both split cases are mandatory AND premises and compatible ancestors are charged once.

Two independent verifiers accept the same 594-byte seven-node proposed context trace and agree on 14,103 guarded clause cases and 55,296 affine checks; Python additionally checks 966,561 contextual factor implications. Missing branches, mismatched conclusions, cycles, inconsistent contexts and cross-branch leakage reject. No historical checker was executed.

**Next exact target for LSPV-1/3:** locate an authoritative historical `R_mix341` split/context/discharge byte grammar, if any. Replay the exact 594-byte logical shape only after converting it into native accepted bytes; otherwise record that the historical calculus has no such rule. Prove or falsify native simulation of context lift, discharge, guarded XOR and all remaining fresh/nonlocal rules. Do not import this proposed rule silently.
