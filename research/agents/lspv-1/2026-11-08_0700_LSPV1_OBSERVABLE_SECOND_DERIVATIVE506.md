# LSPV-1/506: Observable second-difference guards and source-exact Resolution cancellation

2026-11-08 07:00 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.

**Exact IDs:** NEW [P2-L1-506]; related [P2-L1-505], [P2-F13], [P2-L1-491]; OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Cross-chain [P1-01], [P1-03], [P1-04] unchanged.

## IDEA: hypothesis and 4 falsifiers

The /505 one-layer, named-gate common-isotropic theorem should extend to arbitrary-degree *observable outputs* of nested shared Boolean DAGs by using the second finite-difference test. Algebraic cancellations among internal nonlinear gates may lower the number of necessary affine guards, provided we can legally derive the reduced output facets from the **original source**, not claim a free semantic conversion.

F1: basis-pair derivative vanishing does not characterize affine coset restrictions in degree >=3. F2: a claimed named/observable rank gap vanishes when all named gate semantics are retained. F3: the output identity cannot be derived by original-source-indexed, oriented standard Resolution without a new opcode. F4: this result silently authenticates the incomplete historical R_mix341 RES/DEF/LOCAL-CONVERT/branch grammar. F1–F3 are disproved by the theorem and independent checks. F4 remains an explicit boundary; historical native checker was NOT executed.

## SEARCH: primary sources, existing project work and repositories

Read complete live proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; 18,553 chars) and proof2.txt (startup blob e4ba2233300074e36827d511d814135ccfd004f9; 428,781 chars), current issue #3 and recent comments, the governing five-role handoff, AGENTS.md, CODEX.md and research SKILL. Read LSPV-1/491 (quadratic output rank-spectrum for affine-template agreement, an adjacent but different result), LSPV-1/505 (named one-layer common-isotropy), /502; LSPV-3/502 (native reduced checker), LSPV-5/435 (ignored-schema firewall), LSPV-4/495 and LSPV-2/493. Read actual Grok 2026-11-08_0320_PROGRESS.md and Claude world-ledger README; neither licenses missing native rules.

Required external repositories and exact inspected blobs: konard/p-vs-np README.md 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93; meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math/README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae. Also searched project code for common isotropy / output cancellation, finding preceding /491 and /505 rather than the present all-degree observable partition and strict-source gadget certificate. Public indexed research search was used, not a separate Google-branded client. Primary Pang arXiv:2610.00837v2 (24 Oct 2026) Section 7 and Cook–Reckhow (1979) were inspected; the latter's PDF page 2 was visually checked. Both concern distinct proof-system theorems and do not authorize R_mix341.

## Theorem 506.1: exact observable affine-fiber criterion for arbitrary shared nested Boolean circuits (PROVED/RESTRICTED)

Let $H=(H_1,\ldots,H_k):\mathbb F_2^n\to\mathbb F_2^k$ be any selected outputs from a finite acyclic Boolean gate circuit, with arbitrary sharing, reconvergence, nesting, and polynomial algebraic degree. Write $\Delta_u H(x)=H(x+u)+H(x)$. Define

$$
\rho_{\mathrm{obs}}(H)=n-\max\{\dim U:\ \Delta_u\Delta_v H_j(x)=0\ \text{for all }x\in\mathbb F_2^n,\ u,v\in U,\ j\}.
$$

The exact minimum number of independent **global linear guard equations** for a **common-direction coset partition** on which every observable output is affine on every cell is $\rho_{\mathrm{obs}}(H)$. Such a partition has exactly $2^{\rho_{\mathrm{obs}}}$ disjoint cosets. It suffices to verify second differences for *distinct pairs of basis directions* of candidate $U$ for every starting point $x$.

**Proof:** Restrict each $H_j$ to the affine space $a+U$ in basis coordinates. Its unique Boolean algebraic normal form has degree at most one iff all mixed second coordinate finite differences vanish identically; every nonzero monomial of degree at least two survives some such derivative. This is independent of circuit depth/degree. All cosets satisfy this iff the displayed identity holds at every source $x$. A codimension-$r$ subspace is exactly the common solution direction of $r$ independent GF(2) linear guards, and has $2^r$ cosets. Minimize codimension. This characterizes **common-direction** partitions, not optimal adaptive branching DAGs or minimal proof work. Finding an optimal $U$ may itself take $2^{\Theta(n^2)}$ exhaustive subspace enumeration: the ideal minimum grants that choice free for a lower-bound relaxation but a real producer must pay it.

## Theorem 506.2: unbounded named-versus-observable guard gap (PROVED/RESTRICTED)

For each $g\ge1$ use original $x_i,y_i$ ($1\le i\le g$), shared $t$, and conservative gate wires

$$
a_i=x_iy_i,\quad p_i=y_i\oplus t,\quad b_i=x_ip_i,\quad h_i=a_i\oplus b_i=x_it.
$$

There are $2g+1$ original variables and $4g$ auxiliary wires. For every **named nonlinear gate**, the global /505 guard codimension is exactly $g$: the sum of the polar forms of the $a_i=x_iy_i$ has symplectic rank $2g$ and radical dimension 1, giving maximum isotropic dimension at most $g+1$; setting all $x_i=0$ attains it and simultaneously linearizes every named gate. But for the selected **observable outputs** $h_i$, one guard $t=0/1$ suffices:

$$
t=0:\ h_i=0,\qquad t=1:\ h_i=x_i.
$$

At least one is necessary since each $x_it$ is nonaffine. Hence

$$
\boxed{\rho_{\mathrm{named}}=g,\qquad \rho_{\mathrm{obs}}=1.}
$$

This makes the common-direction affine partition shrink from $2^g$ to 2 cells, with an arbitrary multiplicative gap. This is a **legal-output upper-control candidate**, not a lower-bound invariant.

## Theorem 506.3: source-indexed syntactic standard-Resolution interface projection (PROVED/RESTRICTED)

Encode each of the four gates in one gadget by **all four** clauses excluding its falsifying assignments. All 16 original clauses are proper signed width-three clauses using three distinct variables. They impose a=x AND y; p=y XOR t; b=x AND p; h=a XOR b. A source-indexed shared DAG of **21 ordinary oriented Resolution inferences**, critical-path depth 4, derives the three CNF facets

$$
(\neg x\vee\neg t\vee h),\qquad(x\vee\neg h),\qquad(t\vee\neg h).
$$

A local Davis–Putnam producer generated 33 candidate inferences; after retaining the ancestors of the three facets, exactly 21 distinct paid Resolution nodes and 16 source records remain. Each inference has two earlier parent clauses, an explicitly oriented pivot, and the exact resolvent, checked independently in Python and JavaScript. During iteration, one canonical facet did **not** follow directly from eliminating only internal wire variables; a final genuine and explicitly paid Resolution on original pivot x completed the three facets. No weakening, free new rule, semantic oracle or branch-local assumption is used.

Let $F_g$ be the disjoint-per-gadget conjunction of these 16g original clauses (sharing only t) and $Q_g$ the 3g source-derived exposed output facets $h_i=x_i\land t$. For **any** additional CNF $G$ over exposed variables (not the hidden wires), concatenating these source-authenticated deductions with any standard Resolution refutation of $Q_g\land G$ yields

$$
\boxed{S_{\mathrm{Res}}(F_g\land G)\le21g+S_{\mathrm{Res}}(Q_g\land G).}
$$

This is a general **ordinary Resolution upper bound**, not hardness and not an assertion that 21g is the minimum. Shared deductions are counted once. The source $F_g$ itself is satisfiable, with one wire completion for each original assignment. No formula is being sold as a hard UNSAT family.

**Resources:** 16g original signed three-clauses, 21g paid unit-Resolution inferences, local critical path 4, and $O(g\log(g+2))$ source and explicit proof bits using positional source IDs and binary variable indices; a straightforward fully materialized producer/checker needs $O(g\,\operatorname{polylog}(g+2))$ bit operations and $O(g\log(g+2))$ peak bits including writing, reads, parsing, source authentication, proof references and verification. A true historical R_mix341 cost can be asserted only after authenticating its RES grammar and exact weights. The proof is independent of any inference system's purported zero-cost transformations. A downstream algorithm must additionally charge all search, false branches, proof acquisition, storage/recomputation and machine-time/space phases. This does not establish FLMV transformation or B3.

## ITERATE: independent execution and adversarial controls

Python /mnt/data/lspv1_506_observable_guard.py: **4,196 assertions**, all pass. It independently enumerated all 128 assignments on the signed seven-variable source (8 SAT source models), explicitly checked two SAT completions with x=t=h=1 and no completions for x=t=1,h=0; rejected malformed source grammar, source mutation and corrupted inference. It generated and checked all 33 candidate inferences and selected exactly 21 in the three-facet ancestry; checked all subspaces/cosets for g=1,2 and all $2^7$ cancellations for g=3; plus 24 random nested Boolean circuit controls comparing basis second derivatives to the full coset criterion. Raw: /mnt/data/lspv1_506_observable_guard_raw.json (SHA-256 c0fbd46bc92e8dfed98d42f9989ae5ae8fdf64a18d36e82c4f3e8de3fe0d7358). Measured local Python wall ~0.835s, tracemalloc peak 232005 bytes (not an all-machine cost proof).

Independent V8/Node project verifier experiments/arc/lspv1_506_observable_derivative.cjs (blob 9e4ac3cc7b6306e8e3eb338aadd4e83e16c8b988) actually executed, **654 assertions**, same original signed source and 21-node source-oriented checker, proper SAT/UNSAT, corrupted and malformed controls, subspace enumeration for g=1,2, cancellation for g=3, and nested cubic-AND guard codimension 2. Raw results: results/raw/arc/2026-11-08_0700_LSPV1_506_OBSERVABLE_GUARD_RAW.json (blob 9fc26eef4c283329d645b2c57ed36ff36aeb16aa).

**Boundary:** Historical /341 checker NOT executed. Its restricted accepted SOURCE/AND3/XOR packet does not authenticate purported additional RES, definition facet, branch or weight metadata (LSPV-5/435). Neither this source witness nor Pang's separate Res(PC) random-3CNF lower bound proves mixed R_mix341 hardness. Mandatory controls remain Haken ordinary PHP lower bound, Cook ER shortcut, odd-charge cubic Tseitin cheap GF(2), and all available legal shared DAG shortcuts. B3 remains wholly OPEN.

**Actual advance:** all-degree observable affine partition theorem; exact unbounded distinction from gate-by-gate guard rank; 21-node *original-source* standard-Resolution certificate giving a legal interface reduction. **Next:** LSPV-3 test native accepted historical RES wire facets and any context-discharge step; LSPV-5 attack output-interface assumptions/try a shorter proof; Route A charge native machine T/S. Remain OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. P versus NP OPEN.

### Sources

[1] Shuo Pang (2026), A Degree–Size Relation for Resolution over Polynomials, arXiv:2610.00837v2, https://arxiv.org/html/2610.00837v2 .
[2] Cook & Reckhow, The Relative Efficiency of Propositional Proof Systems, J. Symbolic Logic 44 (1979), https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf .
[3] Claude Carlet, Boolean Functions for Cryptography and Coding Theory, Boolean ANF/derivative methods. Older project /491 and /505 are cited as predecessors, not claimed as external novelty.
