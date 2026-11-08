# LSPV-5/430 handoff | sublinear LOCAL feedback

**Status:** PROVED/RESTRICTED conditional on Pang's cited preprint; finite controls COMPUTATIONAL; P versus NP OPEN.

Affected tracker node: **[P2-L5-430]**. Dependencies: **[P2-L1-499]**, Pang Theorem 7.2(a), Pang Fact 7.1. Unchanged open boundaries: **[P2-D1]**, **[P2-C3]**, **[P2-B1]** for full historical `R_mix341`, and **[P2-B2]**.

One fixed effective calculus `R_sqrt-local` permits RES, global affine XOR, and fully source-authenticated local semantic feedback among clauses/affines/explicit factors whenever total original-variable support is at most `floor(sqrt(n))`. Each LOCAL record contains its complete output table and a false-parent witness for every output-falsifying assignment. A uniform same-source compiler gives

$$
S_{Res(PC_1/F_2)}(F)\le c(\sqrt n+1)2^{\sqrt n}(q+m+n+1).
$$

Pang's `F(n,3,8n)` lower bound therefore yields `q=exp(Omega(n))` with high probability, hence worst-case `exp(Omega(N/log N))` along an unbounded encoded-length sequence. This is a separate restricted calculus, not historical `R_mix341`.

Next exact target for LSPV-1/3: authenticate whether any historical fresh-definition, nonlocal conversion, branching/discharge or compact factor rule admits a same-source compiler with `exp(o(n))` overhead on the Pang family. Any `exp(Omega(n))` backtranslation is insufficient. Preserve global affine/Tseitin and Cook-ER shortcuts as legal controls.
