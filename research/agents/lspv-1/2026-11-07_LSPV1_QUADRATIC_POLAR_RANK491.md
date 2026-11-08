# LSPV-1/491 | Quadratic polar-rank spectrum for affine-template covers with sharing
**November 7, 2026 PST | Route B | PROVED/RESTRICTED (standard Walsh/rank theorem derived in this model) + COMPUTATIONAL | P versus NP OPEN.**

**Nodes:** material refinement [P2-F13]; dependencies remain OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]; cross-chain context [P1-X1], [P1-01]. This result does not change any rule or weight in historical R_mix341, nor the five-agent two Route A / three Route B allocation.

## IDEA and precommitted falsifiers

**Hypothesis:** LSPV-1/490's independent-AND affine agreement ceiling extends to arbitrarily shared *quadratic* Boolean output maps when the individual term `3^g` is replaced by the polar-rank spectrum of every output linear combination. The quantity must acknowledge algebraic cancellations from shared gates and be invariant under invertible coordinate changes.

**Falsifiers:** (F1) an affine predictor whose agreement count exceeds the spectrum upper bound; (F2) a quadratic Walsh coefficient with amplitude different from zero or the rank-predicted amplitude; (F3) the proposed bound incorrectly equals `3^g` for duplicated/shared gates; (F4) a loss of polar rank under an invertible input affine change or output invertible linear recombination. All are excluded by the symbolic argument; F1–F3 also faced finite controls. No claim of mixed-proof complexity is implicit.

## SEARCH: provenance and existing work

Read both complete root proof chains (`proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` startup blob `22b1ef4dc3d9e6d81b911130966072ccc1cca801`), issue #3 and newest comments, historical governing five-role handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, `AGENTS.md`, `CODEX.md`, and `.codex/skills/pnp-research/SKILL.md`. Exact current peer reports reviewed: LSPV-1/490 `research/agents/lspv-1/2026-11-07_1614_LSPV1_CROSS_GATE_AFFINE_PENALTY490.md`, LSPV-3/485 `research/agents/lspv-3/2026-11-07_1632_LSPV3_AFFINE_ANCHOR_RANK485.md`, LSPV-5/420 `research/main/2026-11-07_1648_MAIN_REACHABILITY_UNIT_DISCHARGE_REFEREE420.md`. Actual Grok `GROKPROOF/2026-11-07_1920_PROGRESS.md` and Claude `research/agents/claude/world-ledger/README.md` read. The latter are critiques/context, not authorities.

Required external sources were read on the current default branch: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` (scoped finite-machine theorem index); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (scoped rank/relaxation methods); `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (a distinct CNF/XOR elaboration proof format); and `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` (research/manuscript status). None supplies historical R_mix341 authorization.

Primary references for the *existing* mathematics, not novelty claims: Claude Carlet, **Boolean Functions for Cryptography and Coding Theory**, section 5.2.1, quadratic Walsh/polar-radical formula; see also DOI `10.1007/s10623-022-01024-4` for the standard quadratic Walsh amplitude statement. Pang, **A Degree--Size Relation for Resolution over Polynomials**, arXiv:2610.00837v2 (2026-10-24), Thm. 7.2, supplies a separate Res(PC_r/F_p) hard-family benchmark. Cook--Reckhow (JSL 1979) supplies proof-system quantifier context. Public indexed research search was used, not a Google-branded interface.

## Theorem 491.1: polar-rank spectrum bound (PROVED/RESTRICTED)

Fix `n,m>=1`. Let `Q: GF(2)^n -> GF(2)^m` be any vector map whose coordinate functions have GF(2) algebraic degree **at most two**, with arbitrary shared input variables and cancellations. Put `q_s(x)=s·Q(x)`. Its polar bilinear form is
$$
B_s(x,y)=q_s(x+y)+q_s(x)+q_s(y)+q_s(0)
$$
and `r_s=rank_GF(2)(B_s)` (necessarily even). For any globally affine vector prediction `A(x)=Lx+b`, let
$$
M_Q(A)=|\{x:Q(x)=A(x)\}|.
$$
Then
$$
\boxed{M_Q(A)\le U(Q):=2^{n-m}\sum_{s\in GF(2)^m}2^{-r_s/2}.}
$$
The ceiling holds for **every** L and b, including all cross-output/cross-input dependencies. Consequently, if K globally affine predictions have agreement regions covering all `2^n` assignments, then
$$
\boxed{K\ge \left\lceil 2^n/U(Q)\right\rceil.}
$$
An output rank-spectrum is invariant as a multiset under any invertible affine change in original input coordinates and any invertible linear recombination of the output coordinates (also under affine output shifts). It is not invariant under arbitrary noninvertible projections or nonlinear substitutions.

**Proof.** Orthogonality of all `m` characters gives, for any fixed affine A,
$$
M_Q(A)=2^{-m}\sum_{s\in GF(2)^m}(-1)^{s\cdot b}\sum_{x\in GF(2)^n}(-1)^{q_s(x)+(L^Ts)\cdot x}.
$$
For a scalar quadratic f and linear mask a, write `S=\sum_x(-1)^{f(x)+a·x}`. Re-index the square by `h=x+y`:
$$
S^2=2^n\sum_{h\in\mathrm{rad}(B_f)}(-1)^{f(h)+f(0)+a\cdot h}.
$$
On the radical, the exponent is affine-linear with zero constant, so its sum is either zero or `2^{n-r_f}`. Thus every Walsh coefficient is zero or has absolute value `2^{n-r_f/2}`. Bound each Fourier term by its amplitude and sum to get U(Q). The K-cover bound is union counting. Invertible input changes conjugate each polar matrix by `T^T B_s T`, preserving rank, while invertible output recombinations permute all s, proving the stated invariances. QED.

This proof is an application of the standard quadratic Walsh theorem to the *vector-agreement/covering* setting. It does not establish a novel SAT proof-system lower bound.

## Explicit controls, sharing and falsification

1. **Independent AND:** `Q_i=u_i v_i`, `n=2g,m=g`. Each `q_s` has polar rank `2|s|`; hence `U(Q)=3^g`, exactly recovering LSPV-1/487/490, with the all-zero affine prediction meeting the bound. The covering lower bound recovers `K>=ceil((4/3)^g)`.
2. **Overlapping AND:** `Q=(uv,uw)` on 3 bits. All three nonzero scalar combinations have rank 2; `U=2(1+3/2)=5`. The zero prediction agrees on exactly five of eight inputs. Global templates `A_0=(0,0)` and `A_1=(v,w)` cover all eight inputs (the latter is exact whenever u=1), so K=2 is an exact cover optimum. This is a deliberate source-sharing control, not a SAT lower bound.
3. **Duplicate AND:** `Q=(uv,uv)`. One nonzero output character cancels to zero rank; `U=3`, attained by zero. Adding arbitrarily many duplicate outputs leaves the best zero-template agreement at 3/4, irrespective of the number of syntactically repeated AND gates. This falsifies any attempt to promote raw nonlinear-gate count into a representation-independent hardness invariant.
4. **Affine-only and duplicate-plus-zero controls:** `Q=(0,0)` on 4 original bits gives `U=16`; `Q=(uv,uv,0)` on 3 gives `U=6`.

The exact independently executed Python script `rank_spectrum_verify.py` checked 1,125 pseudorandom quadratic maps, 11,250 randomly selected affine predictions, 45,160 quadratic Walsh coefficients, the named controls and 1,344 exhaustive affine predictors for independent, shared and duplicate maps. The separately authored published V8/Node.js script executed 1,125 deterministic random maps, 11,250 affine checks, 44,400 Walsh coefficient checks, 1,344 exact candidate predictions and a zero-character corruption control. It found maxima 9, 5 and 3 respectively. **All passed.** Neither independent finite implementation is the native historical accepted-byte checker. Numerical verification is not the proof of the all-size result.

**Published executable:** `experiments/arc/lspv1_491_quadratic_rank_spectrum.cjs`.
**Published raw:** `results/raw/arc/2026-11-07_LSPV1_491_QUADRATIC_RANK_SPECTRUM_RAW.json`.

## Established hard-family and known-shortcut ledger

| Family, exact encoding and size | Published model and hardness | Known applicable upper-bound controls | Remaining transfer |
|---|---|---|---|
| Odd-charge cubic-expander Tseitin, one variable per edge, four forbidden-parity signed 3-clauses per vertex, h vertices, 3h/2 vars, 4h proper 3-CNF clauses, O(h log h) encoded bits | Ordinary shared-DAG Resolution exp(Omega(h)) for appropriate expander families (Urquhart; Ben-Sasson--Wigderson) | Characteristic-two GF(2) gives linear semantic contradiction; exact historical native rules still to authenticate; branching, definitions and sharing allowed | No mixed R_mix341 superpoly lower bound |
| Random proper signed 3-CNF `F(n,3,8n)`, sampled from `8*binom(n,3)` signed proper width-three clauses, O(n log n) bits | Pang 2026 Thm 7.2(a): exp(Omega(n)) shared-DAG Res(PC_r/F_p) for fixed r,p, asymptotically almost surely (preprint theorem) | Res, CDCL, algebra, extension variables, full source-authenticated mixed DAG and any permitted shortcut | Bound not transferred to all historical rules |
| Bit PHP, n+1 pigeons and `n=2^ell` holes with ell original index bits per pigeon; collision constraints, with separately justified 3-CNF faceting if required | Pang 2026 Thm 7.2(e) Res(XOR) exp(Omega(n)) (preprint theorem) | Cook Extended Resolution and shared circuit facets; source-changing translation overhead matters | Equisatisfiability alone insufficient; mixed-rule transfer OPEN |

This rank-spectrum work itself generates **no original SAT source or refutation**, so no native SAT/UNSAT or corrupted-certificate claim is made. Prior K4 odd/even checks remain external controls, not evidence for this theorem.

## Resource, simulation and barrier audit

The symbolic rank-spectrum is an **offline analytical bound**. To compute it from explicit quadratic monomials, one may enumerate all `2^m` output masks and do GF(2) rank elimination, requiring at most `2^m poly(n,m,input-bits)` arithmetic operations and corresponding matrix workspace. Enumeration of candidate globally affine maps has up to `2^{m(n+1)}` alternatives. Neither cost is hidden as unit work. A full machine-T/S ledger must charge construction, input parsing, matrix ranks, storage, all source/index reads, searching, reference retrieval, serialization, and checking. The published Node script and Python implementation test small dimensions only; no FLMV same-machine bounds are asserted. Distinct proof-DAG work, critical-path span and physical runtime/peak space remain separate.

No normalization of RES/LOCAL-CONVERT/AND3/GF(2)/DEF or any assumption-discharge port into historical R_mix341 follows. Restriction to quadratic maps is substantial: nested AND can produce cubic/higher ANF, while polynomial auxiliary wires and semantic equivalence can yield nonquadratic representations. In fact the duplicate/overlap controls show why a lower bound based on syntactic gate count would overstate true semantic complexity. The rank sum is a potential **restricted analytical upper-control/lower-cover metric**, not a lower bound on fully shared-DAG refutation cost, nor a B3 mechanism.

Cross-domain transfer classification: the vectorial Boolean Walsh/polar-rank theorem is a **DIRECT theorem transfer** to affine agreement; analogy from coding theory's quadratic rank spectra to all mixed SAT proof work is **FAILED WITHOUT a new rule-by-rule simulation**. This does not bypass relativization, algebrization or Natural-Proofs barriers.

Root `main.tex` fetched at blob `68188a24badda635a5983fda1c381cdb694fd497` but returned zero content bytes. No safe ownership-region edit is possible; it was left untouched. A full local repository checkout and local pnp-research preflight were unavailable. The remote artifact publication, independent verification and exact full-file readback status must be reported separately.

## ITERATE and status

Compared with LSPV-1/490, the revised statement is a **model-general analytic bound** on arbitrary shared quadratic maps, with explicit cancellation controls and affine-equivalence invariance. [P2-F13] gains a reusable restricted test for proposed nonlinear-gate shortcuts. It does **not** improve [P2-B1] or prove [P2-C3] or B3. Next: LSPV-3 can test whether any historically accepted mixed certificate even exposes a fixed quadratic output map; LSPV-5 should test nonlinear coordinates and cancellation controls. The minimal remaining implication is an original-source-authenticated proof-complexity invariant across ALL historical legal rules, plus separately noncircular [P2-B2].

**P versus NP OPEN.**
