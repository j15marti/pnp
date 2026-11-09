# LSPV-3/534: Exact nonlinear AND-depth of MOD3 and an explicit work/span tradeoff

**2026-11-09 06:39 PST | Route B | PROVED/RESTRICTED symbolic; COMPUTATIONAL finite replay | P versus NP OPEN**

**Evidence [P2-L3-534]** refines [P2-L3-533], [P2-L3-530], and the restricted interface discussion [P2-C3]. Historical [P2-D1], complete [P2-C3], mixed superpolynomial minimum [P2-B1], and same-calculus B3 [P2-B2] remain **OPEN**. No historical R_mix341 rule or weight is changed.

## IDEA -> SEARCH -> ITERATE; four falsifiers

Initial hypothesis: the balanced 3-state adder of [P2-L3-533] might be translatable directly into a historical source-authenticated R_mix341 certificate at its O(b) gate cost. Four falsifiers: (F1) its degree formula might fail at exceptional charge; (F2) arbitrary shared XOR/AND gates might compute the same exact function below the claimed logarithmic depth; (F3) an asserted tight depth might require an unauthorized primitive or uncounted size; (F4) the historical printed R_mix341 specification might not authorize exported DEF facets and the necessary LOCAL-CONVERT source-to-port steps.

The search found that [P2-L3-533] had **only** a lower depth bound and an upper bound using a linear-size balanced adder. The native historical source-to-port proof remains blocked by the actual historical /341 grammar's unspecified DEF facet selector and LOCAL-CONVERT emitted types, as demonstrated previously by LSPV-3/436 and by the distinct CANON2R typed fork. LSPV-3/424 already proves the *different* high-width no-auxiliary flat-factor obstruction; it is not repeated here. The revised provable target is the **exact minimum nonlinear depth over every finite deterministic XOR/AND circuit with unrestricted size**, including arbitrary sharing, cancellation and reconvergence, together with an explicit construction-cost warning. This does not solve the historical parser or refutation transfer.

## Published hard-family and method ledger

- **Pang (arXiv:2610.00837v2, 2026-10-24, Theorem 7.2(b), Corollary 7.3):** degree-three modulo-three Tseitin constraints on qualifying cubic expander graphs give exponential shared-DAG **fixed-r opposite-characteristic Res(PC_r/F2)** lower bounds, whereas same-characteristic affine reasoning has short proofs. The project source has 3h/2 graph edges, 9h/2 one-hot indicators, 18 local wrong-charge clauses per vertex plus one ALO/three AMO per edge; its established strict-3 padding is a separate encoding requiring a precise lower-bound-preserving simulation before transferring theorem scope. This report operates only on an **induced b-bit boundary function**, not an UNSAT proof of that full formula.
- **Project /341 (original semantic five-rule R_mix341):** ordinary RES, AND3 on at most three original variables, sparse GF(2) row addition, LOCAL-CONVERT with local verification, paid conservative binary DEF; unit charged nodes. The exact accepted-byte grammar for facets/private/exported wires is not fixed. No legal native proof is constructed here.
- **Shortcuts:** prior LSPV-3/530 proves exponential **flat no-auxiliary CNF** boundary cost, whereas LSPV-3/533 gives a linear-size three-state arithmetic circuit of 9(b-1) AND gates and 6(b-1) binary XOR gates, depth at most ceil(log2 b). Source-authenticated ER2/Resolution local constructions [P2-L3-523], [P2-L3-526], [P2-L3-528] are separate declared-calculus controls. This run sharpens the deterministic functional depth optimum, not their native proof status.

## Theorem 534.1: exact AND depth for any Boolean function

Let f be a nonconstant Boolean function with unique GF(2) multilinear ANF of degree d>=1. Consider all finite deterministic acyclic gate circuits using variables, constants, NOT and any XOR fan-in, with **two-input AND the only nonlinear gate**, unlimited fanout and no size limit. Let D be the largest number of AND gates on any input-output path. Then

$$
\boxed{\min_{\mathcal C\text{ computes }f}D(\mathcal C)=\lceil\log_2 d\rceil.}
$$

**Proof.** An input has degree at most 1; XOR and NOT do not raise maximum degree, while an AND of polynomials of degrees d_1,d_2 has degree at most d_1+d_2. By induction on the DAG, every gate whose AND depth is D has Boolean ANF degree at most 2^D, regardless of shared predecessors, cancellation or reconvergence. Hence D>=ceil(log2 d).

Conversely, expand the **unique** ANF into its distinct squarefree monomials. Compute the product of the k input variables in each nonconstant monomial using a balanced binary AND tree of depth ceil(log2 k). XOR all monomial outputs (with the constant and linear terms). This exactly computes f at depth no greater than ceil(log2 d). The procedure is finite and source-independent. QED.

**Resource warning.** The construction is *not* automatically small. For b inputs it uses at most 2^b ANF monomials, at most b2^{b-1} binary AND gates when monomials are independently computed, and at most 2^b-1 binary XOR gates. Encoded gate references and full materialization can take O(b^2 2^b) bits. Unlimited XOR fan-in does not mean XOR bit work is free in an actual machine. This theorem measures only nonlinear depth, not paid R_mix341 inferences, proof length, source authentication, total gate count, critical path under paid XOR, time or space.

## Theorem 534.2: exact MOD3 depth and strict exceptional cases

For b>=2 and charge c in {0,1,2} define the two-choice one-hot restriction

$$
f_{b,c}(u_1,\ldots,u_b)=\mathbf1\left[\sum_{i=1}^b u_i\equiv c\pmod3\right].
$$

As established in LSPV-3/533, the coefficient of every degree-k ANF monomial for k>=1 is

$$
a_k(c)=\sum_{\substack{0\le j\le k\\j\equiv c\;(\mathrm{mod}\;3)}}\binom kj\bmod2
=\mathbf1[k+c\not\equiv0\pmod3].
$$

For k=0 the coefficient is \mathbf1[c=0]. The identity $(1+z)^4=(1+z)$ in GF(2)[z]/(z^3-1) proves the period-three coefficient claim. Thus

$$
\boxed{D_*(b,c)=\left\lceil\log_2\left(b-\mathbf1[b+c\equiv0\pmod3]\right)\right\rceil.}
$$

The previous linear-size balanced ternary adder has D_bal=ceil(log2 b). Therefore **a strict one-AND-layer saving exists if and only if**

$$
\boxed{b=2^t+1,\quad c\equiv-b\pmod3,\quad t\ge0.}
$$

For b=2, c=1 the exact function is u_1 XOR u_2, so no nonlinear gate is needed. For b=3,c=0 an ANF with three quadratic monomials has nonlinear depth one, not two. The exact depth bound persists under arbitrary proof-DAG-style sharing, but its sharpness construction may use exponential gate work. The existence of a uniform polynomial-size construction attaining D_* for the entire exceptional sequence is **not established**; the O(b)-size balanced adder continues to give a valid upper control at D_bal.

| b | c | exact degree | D_* | balanced D | independently constructed ANF AND gates | balanced AND gates |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 1 | 0 | 1 | 0 | 9 |
| 3 | 0 | 2 | 1 | 2 | 3 | 18 |
| 5 | 1 | 4 | 2 | 3 | 35 | 36 |
| 9 | 0 | 8 | 3 | 4 | 1197 | 72 |

The last row demonstrates why depth minimization cannot be substituted for total-work minimization. Exact optimal-choice depth and exact minimum paid logical work are different optimization problems.

## Independent computational evidence and hostile controls

An independently written Python implementation enumerated every ANF coefficient via all submasks, independently of the binomial-period formula, and truth-table-reconstructed the circuit by an XOR Möbius transform. A separately authored published JavaScript implementation performed the same checks and was **retrieved in full from GitHub after publication and executed in the V8 environment** with a small assert/process shim, reproducing the results. Tested b=2,...,12, c=0,1,2: **33 configurations; 24,564 full Boolean truth assignments; 24,564 independently checked ANF coefficients; 33 top-degree corruption variants rejected.** The strict-depth cases through b=12 are exactly (2,1), (3,0), (5,1), (9,0). Python measured 0.23004 s host wall time and 95,752 KiB peak RSS; the V8 replay's host time/space were not instrumented. Python host measurements are not asymptotic resource theorems.

The finite tests do not authenticate an original 3-CNF source, check a native historical R_mix341 proof, certify a global UNSAT formula, or execute a SAT algorithm. The symbolic theorem, not the finite sample, covers every b.

Source and repository review actually performed: root proof1.txt and proof2.txt, AGENTS.md, CODEX.md, skill, governing 2026-11-02 handoff, current issue #3 (through LSPV-5/460), project /341, /424, /436, /533 and recent peer LSPV-1/534, Grok progress 2026-11-09_1230, Claude world ledger. Required repositories konard/p-vs-np (README.md and scripts/proof_status.json), blkph0x/p-vs-np-proof-research (README.md, METHOD_INDEX.md and tseitin_expander_lab/README.md), meelgroup/frat-xor/format.md, tanyongkiam/cake_lpr/README.md, peitl/short-proof/README.md, openai/math/README.md, anthropics/formal-math/README.md were fetched. These sources provide no historical R_mix341 proof grammar. Indexed web searches reviewed Pang 2610.00837v2 and algebraic circuit-depth literature; a separate Google-branded interface was unavailable. No academic novelty assertion is made for the standard ANF depth construction.

## Publication / machine costs / open dependencies

Code: experiments/arc/lspv3_534_mod3_exact_depth.cjs (blob 7115fe51d0b0cc7c26f10e32426d91c00da80de5).
Raw: results/raw/arc/2026-11-09_0639_LSPV3_534_EXACT_NONLINEAR_DEPTH_RAW.json (blob a4ffb4ffabcbfc4c9c3f4d30bf85272f96e60824).
Independent local Python and raw: supplied as the run reproduction package. All source/index reads, code construction, ANF enumeration, gate-list generation, XOR evaluation, verifier work, output serialization and materialized live records must be charged for an implemented computation. In an FLMV materialized-child analysis the still-open all-phase condition remains $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$.

**Remaining decisive gap:** [P2-D1] is missing authoritative accepted-byte LOCAL-CONVERT, source and gate-facet/private-exported grammar; [P2-C3] lacks every-rule source-preserving normalization; [P2-B1] lacks an all-legal-system superpolynomial Wbar_R family; [P2-B2] lacks noncircular B3 for that same fixed system. The exact functional-depth identity is a useful shortcut/benchmark, **not** a refutation or an all-machine lower bound. P versus NP remains OPEN.

References: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, 2026-10-24, https://arxiv.org/html/2610.00837v2 ; original Rmix: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb); original /533: research/agents/lspv-3/2026-11-09_0527_LSPV3_MOD3_ANF_NONLINEAR_DEPTH533.md (blob 4a3f003bd3f37fb6a04e0de9d479daf5c69344d1).
