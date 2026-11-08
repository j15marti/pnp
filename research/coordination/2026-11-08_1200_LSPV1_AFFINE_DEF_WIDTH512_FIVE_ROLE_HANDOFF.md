# LSPV-1/512 five-role handoff: affine conservative definitions preserve expanded XOR cut width

**2026-11-08 12:00 PST | Route B lead | PROVED/RESTRICTED; COMPUTATIONAL independent checks | P versus NP OPEN.**

**Material node:** [P2-L1-512] refines [P2-L3-375] using paid acyclic affine fresh-wire definition equations with unrestricted shared binary XOR inference DAGs. For odd-charge connected cubic Tseitin graph $G$ with $h$ vertices, EVERY such refutation contains a row $Q$ for which fully substituted original-edge width satisfies

$$
\mathrm{ew}(Q)\ge \beta(G)h/3,\qquad
\beta(G)=\min_{\varnothing\ne S\subsetneq V}\frac{|\delta(S)|}{\min(|S|,h-|S|)}.
$$

**Proof:** Augmented vertex incidence rows $[B\mid\chi]$ are independent since charges sum to 1; thus every projected XOR row has a unique coefficient vector over original vertex equations. Every conservative affine definition projects to $0=0$. The root $0=1$ has coefficient all-ones. Its ancestry has a first node crossing $h/3$ vertex coefficients. Two binary parents cap its weight by $2h/3$, so its expanded edge mask is a balanced vertex cut. Shared subproofs and cancellation are permitted.

**Scope:** A DISTINCT affine-DEF+XOR calculus, not the historical accepted-byte R_mix341. The parity-view extraction from original proper signed 3-CNF was semantically checked but not output as a native R_mix341 certificate. RES, AND3, nonlinear DEF, LOCAL-CONVERT, branching and assumption discharge are outside this theorem. Expanded semantic width is not record width, logical work, real machine time, or space, and cannot establish P != NP.

**Finite controls:** Independently implemented Python and V8 JavaScript check K4/K3,3/cube3 (16/24/32 proper original 3-clauses; odd SAT counts 0/0/0, even counts 8/16/32); unique row coefficients, source-input truth tables, explicit shared-definition detours and directed XOR replay. Crossing widths 4,9,5 exceed bounds 8/3,10/3,8/3. Malformed defining equations, forged root and even-charge contradiction controls reject. Python runtime 0.65 sec, 96,140 KiB Linux peak RSS, including finite exhaustive tests; no FLMV timing.

**Assignments within unchanged five-role allocation:** LSPV-1 Route B continue full mixed-rule and noncircular B3 transfer. LSPV-3 Route B authenticate historical byte grammar, parity extraction and paid DEF/LOCAL ports. LSPV-5 Route B falsify nonlinear or branch-scope projection and logical-to-bit-cost leaps. LSPV-2/4 Route A review only pertinent resource effects; continue all-input same-machine FLMV requirement.

Read proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2 initial blob 9e27a9b6cdd533813a8efa556b3001c8c717bed6. New [P2-L1-512] is restricted evidence only. Historical [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

Report: research/agents/lspv-1/2026-11-08_1200_LSPV1_AFFINE_DEF_SEMANTIC_WIDTH512.md.
Code: experiments/arc/lspv1_512_affine_def_projection.cjs.
Raw: results/raw/arc/2026-11-08_1200_LSPV1_512_AFFINE_DEF_XOR_PROJECTION.json.

No changes to historical inference grammar/weights, agent/task identities, schedules, enabled states, or 2A/3B allocation. **P versus NP remains OPEN.**
