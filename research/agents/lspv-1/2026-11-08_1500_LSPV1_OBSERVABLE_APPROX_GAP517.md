# LSPV-1/517: a positive-optimum inapproximability gap for observable-affine guard rank

**2026-11-08 15:00 PST | Route B lead | PROVED/RESTRICTED mathematical reduction plus COMPUTATIONAL finite controls | P versus NP OPEN.**

Affected new node [P2-L1-517]. Strengthens [P2-L1-516] (coNP-complete zero-affinity test) and [P2-L1-506] (observable common-direction affine rank), credits [P2-L1-384] (prior semantic factorization hardness), and refines the scope of [P2-C3]. [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P2-A2], [P2-A5] and [P1-01]/[P1-03]/[P1-04] remain OPEN.

## IDEA: prediction and four precise falsifiers

Hypothesis: /516's zero-versus-positive recognition barrier can be quantitatively amplified to **rank 1 versus rank at least k+1**, using a polynomial-size shared circuit compiled from an arbitrary ORIGINAL signed proper 3-CNF, without a zero-optimum approximation loophole.

F1: For SAT F, a common-direction subspace of codimension less than k+1 makes all outputs affine by using the shared F evaluator. F2: For UNSAT F, the independent baseline product does not have exact rank one. F3: Construction requires a satisfying assignment or expands F exponentially. F4: The claim silently changes the historical R_mix341 rule grammar or assumes free online semantic optimization.

## SEARCH and exact continuity

Read both complete live trackers on main before work: proof1.txt Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 UTF-8 characters) and proof2.txt blob d6a381b4c8d40e3a9ffd56ae5ed6865671ab04d7 (528,935 characters), current issue #3 and its 1,389 then-visible comments, historical five-role handoff at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Read predecessor LSPV-1/515 and /516, peer research/agents/lspv-3/2026-11-08_1457_LSPV3_THREE_LOCAL_SOURCE_EXCESS_RIGIDITY513.md (blob 6f1e40f7), red-team LSPV-5/445 through issue #3 and proof2, Grok GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f), Claude research/agents/claude/world-ledger/README.md (blob de75a371). The nearest existing project predecessor /516 already proves the coNP-complete zero case; the only new result here is a **positive-optimum approximation gap**. Do not claim originality from unsuccessful searches.

Actual GitHub change-aware reads: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 and proofs/complexity/README.md blob 7ee9a11e (finite-machine scope, not B3); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea and REVIEW_ADDENDUM.md blob 6a7cc2f8 (relaxations, not P versus NP resolution); meelgroup/frat-xor format.md blob 986a21aa (external XOR record language); peitl/short-proof README.md blob 93d2090d (Resolution-specific minima); tanyongkiam/cake_lpr README.md blob e94f45e9 (Nov 1 2026 checker note); openai/math README.md blob cc5b0a03 (raw research, not historical R_mix341 authority). Project search queries included "observable guard rank approximation coNP hard", "affine guard approximate rank multiplicative", "second derivative symplectic amplification", and "nonlinear output rank gap SAT". Web searches checked Pang, arXiv:2610.00837v2 (24 October 2026) and the Chvátal-Szemerédi published ordinary-Resolution theorem, with Pang's exact Theorem 7.2(a) read from arxiv HTML. No separately branded Google browsing was executed.

## ITERATE: exact theorem and proof

Let F(x) be ANY valid original proper signed 3-CNF on n variables and m clauses, with original clause/literal IDs and n>=3. For k>=1 add independent original circuit-input pairs (t_i,u_i), i=1,...,k, and a,b. Build one shared bounded-fanin Boolean evaluator F(x) (not a SAT solver) and expose k+1 outputs:

$$
H_{F,k}(x,t,u,a,b)=(ab,\ F(x)t_1u_1,\ldots,F(x)t_ku_k).
$$

The circuit has D=n+2k+2 input bits and O(n+m+k) gates, with polynomially many source-indexed serialization bits. No satisfiability label or semantic simplification is used in construction.

For any vector Boolean function H over the D-dimensional cube define the common-direction observable-affine guard rank:

$$
\rho_{\rm obs}(H)=D-\max\left\{\dim U:U\le\mathbb F_2^D,\
\Delta_s\Delta_t H_j(z)=0\text{ for all }s,t\in U,z,j\right\}.
$$

This is the MINIMUM number of independent global affine guard equations needed for a common-direction coset partition on which EVERY observable output is affine. It is an offline SEMANTIC optimum, not a historical R_mix341 inference rule.

**Theorem 517.1 (PROVED/RESTRICTED, rank gap).**

$$
F\text{ UNSAT}\implies \rho_{\rm obs}(H_{F,k})=1,\qquad
F\text{ SAT}\implies \rho_{\rm obs}(H_{F,k})\ge k+1.
$$

**Proof.** If F is unsatisfiable, all products F(x)t_i u_i vanish; only ab remains. A quadratic product ab is nonaffine over the full cube, forcing rank at least 1, while fixing a=0 makes ab affine on every resulting coset, giving rank exactly 1.

If F is satisfiable, choose a satisfying x* only for this mathematical proof. Let U be any admissible common-direction affine subspace, and put V=U intersect ker(projection onto the n original x coordinates). Rank-nullity gives dim(V)>=dim(U)-n. On the slice x=x*, the observable functions are precisely the k+1 independent products ab,t_1u_1,...,t_ku_k. Each has polar form

$$
B_i(s,t)=s_{p_i}t_{q_i}+s_{q_i}t_{p_i}.
$$

The restriction of every B_i to V times V vanishes: the original output is affine on U-cosets, and x does not change along V. Since B_i is nondegenerate on its two-bit coordinate pair, the projection of V onto each such pair has dimension at most 1. These disjoint projections jointly determine each v in V, so dim V<=k+1. It follows that dim U<=n+k+1, whence rho>=D-(n+k+1)=k+1. This holds for arbitrary output cancellations and all direction subspaces, without charging sharing twice. QED.

The exact derivative identity also holds for every original assignment:

$$
\Delta_{t_i}\Delta_{u_i} H_{i}(x,\mathbf0,0,0)=F(x),\quad
\Delta_a\Delta_b H_0=1.
$$

**Corollary 517.2 (PROVED/RESTRICTED, approximation reduction).** For every fixed epsilon>0, a deterministic uniform polynomial-time algorithm that, for EVERY explicitly serialized bounded-fanin multi-output circuit H, outputs a one-sided numerical approximation A(H) satisfying

$$
\rho(H)\le A(H)\le D^{1-\varepsilon}\rho(H)
$$

would imply SAT in P and hence P=NP. Given encoded source bit length L, choose k=L^2, so D=O(L^2), and for sufficiently large L, k+1>D^(1-epsilon). The exact rank-1 versus rank-(k+1) gap makes the output distinguish UNSAT from SAT. All finitely many smaller lengths can be handled uniformly by fixed exhaustive search. A two-sided estimate rho/D^c<=A<=D^c rho with fixed c<1/2 also distinguishes the disjoint ranges since k+1>D^(2c) eventually. The theorem is a **conditional complexity-hardness statement**, not a resolution of P versus NP.

A sound construction of a rank upper bound, its guards and required output-affinity certificates would itself have to be charged by a real SAT algorithm. The after-the-fact lower-bound optimization [P2-D2] intentionally does not charge discovery, but it does NOT authorize a polynomial-time rank oracle.

## Reproducible finite controls and resource ledger

Published executable JS constructs actual shared fan-in-two gate records for ALL 256 subsets of the eight original proper signed 3-variable clauses (255 SAT, 1 UNSAT). It verifies 3,072 independent mixed-derivative equalities, 2,048 baseline polar tests, 2,065 further checks, four malformed-source rejections and one deliberately corrupted output-gate detection. Independently written Python enumerated all RREF subspaces for D=7 on five valid strict-3CNF sources and computed exact rank: UNSAT/all8=1, UNSAT/repeated all8=1, SAT/single=5, SAT/three=5, SAT/empty=2. It separately reconstructed original signed proper 3-CNF cubic K4 odd-charge (n=6,m=16,0 models) and even-charge (n=6,m=16,8 models), checked 36 exact derivatives, and rejected four malformed sources. The K4 graph is a finite both-label control, NOT a certified asymptotic hard expander. Neither implementation executed the historical native R_mix341 checker.

Shared source compilation takes O(m+n+k) abstract 2-input gates plus O((m+n+k)log(m+n+k)) serialization bits in straightforward indexed format. A supplied circuit can be evaluated in linear gate time and polynomial working memory. Exhaustive small-instance rank search over direction subspaces is exponential and is OFFLINE; no universal efficient rank construction, proof search, native machine peak-space profile or FLMV recurrence is asserted. An implemented solver must pay source reading, parsing, gate compilation, guard selection, branch joins, certificate writing, verification, storage, caching/retrieval, recomputation, failed searches and total simultaneous peak space.

## Published hard-family ledger, shortcuts and precise missing transfer

| Existing family, exact original encoding | Published theorem and model | Strongest known shortcut / missing direction |
| --- | --- | --- |
| Proper random signed 3-CNF: n variables, m=8n independent uniform width-three clauses with three distinct variable names and independent uniform signs, clauses may repeat, binary input Theta(n log n) bits. | Pang 2026-10-24 arXiv:2610.00837v2 Thm 7.2(a): a.a.s. exp(Omega(n)) shared DAG lower bound in Res(PC_r/F_p) for each fixed p,r; preprint, no conservative extension variables. | The new H construction may have offline rho=1 when UNSAT even for this proof-hard original F; semantic rank is not an original-source authenticated refutation. Transferring any hard-family bound through ALL historical mixed legal rules remains [P2-C3] OPEN. |
| Odd-charge cubic-expander Tseitin: one variable per edge, four original strict signed width-three clauses per vertex, h vertices, m=4h, N=Theta(h log h). | Urquhart 1987; Ben-Sasson-Wigderson 2001: exponential ordinary DAG Resolution for suitable expander families. | Historical-declared AND3 and GF(2) yield linear-node parity refutations /341, so pure Resolution lower bounds do NOT transfer to unrestricted mixed calculus. Finite K4 source check here does not certify a hard expander. |
| Haken pigeonhole PHP: h+1 pigeons into h holes, standard non-3CNF encoding. | Haken 1985: exponential ordinary Resolution. | Cook Extended Resolution polynomial proof control. Equisatisfiable conversion to strict 3CNF alone does not preserve the lower-bound direction. |

**Actual advance:** Quantitative rank-1 versus rank-k SAT reduction and a positive-optimum sublinear-factor approximation barrier for /506's semantic observable guard rank. It does **not** prove any historical R_mix341 superpolynomial minimum, all-rule translator or same-calculus B3. P versus NP OPEN.

## References

[1] S. Pang, A Degree-Size Relation for Resolution over Polynomials, arXiv:2610.00837v2, 24 October 2026, Theorem 7.2(a), https://arxiv.org/html/2610.00837v2.
[2] V. Chvatal and E. Szemeredi, Many hard examples for resolution, JACM 35(4) (1988) 759-768, DOI 10.1145/48014.48016.
[3] A. Urquhart, Hard Examples for Resolution, JACM 34 (1987), 209-219.
[4] E. Ben-Sasson and A. Wigderson, Short Proofs Are Narrow, JACM 48 (2001), 149-169.
[5] S. Cook and R. Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979), 36-50.
