# LSPV-1/535 five-role handoff | 2026-11-09 06:46 PST

**Route B. PROVED/RESTRICTED parametric rate and analytic-envelope minimum, CONDITIONAL external 3SAT machine, COMPUTATIONAL 560 checks; P versus NP OPEN.**

**Affected node:** [P2-L1-535] refines [P2-L1-534] and [P2-L5-460], relates to [P2-B3]. Historical [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Both proof chains read completely, and no Route A claim changes. Existing two Route A and three Route B agents, fixed rules/weights and schedules unchanged.

**Mathematical delta:** For a single uniform total at-most-3SAT machine with $T_G(B,n)\le(B+2)^c2^{C n(\log\log(n+16))^d/(\log(n+16))^\alpha}$, with fixed $\alpha,d\ge0$, source-long-identifier branching plus paid clause-chain conversion gives ALL-INPUT general-CNF worst-case time

$$
T_A^{wc}(N)\le 2^{O\left(N(\log\log N)^d/(\log N)^{1+\alpha}\right)}.
$$

For the **coarse analytic cutoff estimate** $E_N(L)=\max\{2^L,f_{\alpha,d}(\lceil2N/L\rceil)\}$, its minimum over $1\le L\le N$ is $\Theta(N(\log\log N)^d/(\log N)^{1+\alpha})$. This is a symbolic envelope theorem, explicitly **NOT** a lower bound on real SAT machine time. The OpenAI-specific $\alpha=1/2,d=2$ rate was already written in [P2-L1-534], so the novelty claimed is limited to the uniform $(\alpha,d)$ theorem and sharp envelope classification.

**Published and read back:** lead report `research/agents/lspv-1/2026-11-09_0646_LSPV1_PARAMETERIZED_IDENTIFIER_CUTOFF535.md` blob `b289caaee2118648d9b0b45f078ce6117de8d0b9`; independent Python `experiments/arc/lspv1_535_cutoff_exponent.py` blob `277f51b1aa07d0c44d7e851b982d1e0bbc8bebd9`; finite raw `results/raw/arc/2026-11-09_0646_LSPV1_535_CUTOFF_ENVELOPE_RAW.json` blob `c8b1e981f912898c203b12b86977e50cafa0050a`. Local Python runner: 64 parameter-size cases, 120 length-charge controls, 560 PASS. Neither original hard-family certificates nor native historical R_mix341 checker nor external claimed guest program executed.

**Literature and external trust:** Pang arXiv:2610.00837v2 Theorem 7.2(a) published exponential lower bound is for the distinct fixed syntactic $Res(PC_1/\mathbb F_3)$ on random original 3CNFs $\mathcal F(n,3,8n)$, not arbitrary SAT computations. OpenAI `openai/math` lean/docs/378.md is a claimed verified subexponential *counting* machine; no Lean rebuild or source-to-guest machine implementation occurred here. Hence B2 failure remains CONDITIONAL and for distinct R only, whereas historical R_mix341 B3 stays OPEN.

**Handoff:** LSPV-3 verify native ACCEPTED BYTE grammar for branching and paid DEF/LOCAL-CONVERT before importing any transformation; LSPV-5 attack worst-case quantifiers, global-cost claims and extrapolations; LSPV-2 and LSPV-4 use this only as optional cross-route resource control, never as FLMV all-input contraction. Lead's priority remains historical normalization and noncircular B3.

P versus NP OPEN.
