# LSPV-1/528: spectral structure of the published-family pair-defect source-cover graph

**2026-11-09 00:10 PST | Route B LSPV-1 lead | PROVED/RESTRICTED structural theorem + COMPUTATIONAL independent controls. P versus NP OPEN.**

**Proof-chain scope:** new [P2-L1-528] is a *spectral characterization*, not a new exact source-core minimum. It independently audits pre-existing [P2-L3-522] and its supporting [P2-L3-521], [P2-L1-523] and [P2-L5-452]. The load-bearing [P2-D1], [P2-C3], [P2-B1] and [P2-B2] remain OPEN. [P1-01], [P1-03], [P1-04] unchanged.

## IDEA, falsifiers, SEARCH, ITERATE

Initial hypothesis: the two-defect assignments underlying the prior source-ancestry bound define an exact compatibility graph whose adjacency spectrum can be determined uniformly from the *original* cubic graph spectrum, with no assumption of a particular solver or proof DAG.

Four falsifiers fixed before verification: (F1) some nonadjacent pair of wrong-defect local triples cannot be extended to a globally satisfying two-defect flow on a 3-connected cubic graph; (F2) adjacent local tuples with matching shared-edge value cannot extend; (F3) an independently computed spectrum disagrees with the claimed direct-sum formula, including on K4, K3,3, cube and Petersen; (F4) the K4 69-source minimum is misrepresented as new although [P2-L3-522] proved that minimum earlier, or a spectral source-cover bound is promoted to computational hardness.

**Search/revision:** Reading the actual LSPV-3/522 report, research/agents/lspv-3/2026-11-08_2054_LSPV3_THREECONNECTED_EXACT_CORE522.md, established that the exact 39h/2 - 9 minimum UNSAT-source-core theorem and K4 value 69 are **already proved**. This rules out novelty for that minimum and is a material correction to the initial formulation. The revised new candidate is solely the *general spectrum formula* below, with an independent exact K4 matrix-polynomial certificate. Project searches for "pair defect spectral", "Hoffman pair-defect", "9(J-I)-6", and "compatibility adjacency spectrum" did not reveal this specific formula in the inspected project; this is not a claim of academic originality.

Actual governing sources read: complete proof1.txt and proof2.txt (initial main blobs 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and 2797e7a03ec27a60ece75f61f9ca672d268b0dca); issue #3 and its latest peer reports; five-role 2026-11-02 refocus; AGENTS.md, CODEX.md, repo pnp-research skill; historical R_mix341 declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb); LSPV-3/521, /522, /527; LSPV-5/450, /452, /453; actual GROKPROOF/2026-11-08_1130_PROGRESS.md and research/agents/claude/2026-09-30_CLAUDE-0266_review.tex. Both newly requested external repositories were read: konard/p-vs-np README and proofs/p_vs_np_decidable/README.md (finite machine P subset NP and excluded-middle scope, not a solution), blkph0x/p-vs-np-proof-research README and METHOD_INDEX.md (bounded/promise method claims, not all-input separation). Also examined meelgroup/frat-xor/format.md, tanyongkiam/cake_lpr/README.md and openai/math/README.md; these concern proof interfaces/research, not the historical accepted-byte grammar. Web primary search read Pang arXiv:2610.00837v2 and Haemers, "Hoffman's Ratio Bound", Linear Algebra Appl. 617 (2021), 215-219, DOI 10.1016/j.laa.2021.02.010. General web search was used; no separate Google-specific search implementation or native historical checker was used.

## Exact family/theorem/encoding/method/remaining-transfer ledger

Choose a simple 3-vertex-connected cubic graph G=(V,E) on h vertices, arbitrary orientation and charges b_v in F3 with sigma=sum b_v nonzero. Each edge e has three Boolean atoms x_(e,0),x_(e,1),x_(e,2). Original signed proper 3-CNF: one ALO clause x_(e,0) OR x_(e,1) OR x_(e,2) per edge; at each vertex, all eighteen negative triples disallowing incident labels with oriented sum unequal to b_v. Thus source has 9h/2 Boolean variables, 39h/2 original width-3 clauses and ordinary bit length Theta(h log h).

The nine R_v clauses per vertex are the wrong-defect triples with local signed sum b_v+sigma; the other nine E_v clauses have sum b_v-sigma. In a 3-vertex-connected graph all edge ALOs and E_v clauses are individually indispensable, as already proved in [P2-L1-523], [P2-L3-522]. A pair-defect flow at distinct vertices u,v has divergence b+sigma e_u+sigma e_v. Summation is zero, so connected incidence rank gives exactly 3^(h/2+1) such flows. Each falsifies exactly one R_u and one R_v original clause and no others.

Pang's Theorem 7.2(b) establishes exp(Omega_r(h)) proof-size lower bounds only in fixed-r Res(PC_r/F2), for its opposite-characteristic mod-3 Tseitin on regular expanders. The source-containment/strict3 transfer is described in [P2-L3-520]. The present graph-spectral theorem does not transfer that bound to R_mix341. Cook extension-variable proofs and the project ER2/source-authenticated Resolution packets remain mandatory legal upper controls; they are not excluded to protect a lower bound.

## Theorem 528.1: Exact spectrum of the source-compatibility graph (PROVED/RESTRICTED)

Define H_G with vertex set consisting of the 9h *original* wrong-defect source clauses (v,t), t in R_v. Two different vertices (u,s), (v,t) of H_G are adjacent iff there exists a one-hot edge-label assignment satisfying all vertex charges except exactly the two prescribed wrong-defect triples at u,v.

For nonadjacent u,v, all 9 x 9 pairs of local wrong-defect triples extend, because G-{u,v} is connected and the total residual charge is zero. The off-diagonal adjacency block is the all-ones matrix J_9. For adjacent u,v, the pair extends iff the two triples assign the same label to their common edge. Its block is the disjoint union of three all-ones 3 x 3 blocks (permuted according to coordinate order). Each vertex of H_G therefore has degree

$$
d_H=3(3)+(h-4)(9)=9h-27.
$$

Let lambda_1=3,lambda_2,...,lambda_h be all eigenvalues of the adjacency matrix A_G, counted with multiplicity. Then the full multiset of eigenvalues of A_(H_G) is

$$
\boxed{
\{9h-27\}
\uplus\{-9-6\lambda_i:2\le i\le h\}
\uplus\{3\}^{3h}\uplus\{-3\}^{3h}\uplus\{0\}^{2h}.
}
$$

**Proof, without a numeric eigensolver.** The nine wrong-defect tuples at each v form an affine two-plane over F3. Its real function space decomposes orthogonally into (i) one-dimensional constants; (ii) three mutually orthogonal two-dimensional mean-zero subspaces, one for each incident-edge label coordinate; and (iii) a residual two-dimensional subspace. The three coordinate functions are nonproportional linear forms on the affine two-plane, which gives the orthogonality. An adjacent block transmits the constant component with gain 3 and its one matching edge-coordinate subspace with gain 3, killing the other components. A nonadjacent all-ones block transmits only the constant component with gain 9. Consequently the constant sector is the h x h matrix 9(J_h-I_h)-6A_G: its all-ones eigenvalue is 9h-27, and its other eigenvalues are -9-6lambda_i. Each original edge supplies a separate four-dimensional pair of coordinate subspaces, with eigenvalues +3,+3,-3,-3. There are 3h/2 original edges, hence 3h occurrences of each sign. The 2h residual dimensions contribute zero. The dimension count h+6h+2h=9h is exact. QED.

This is a source-compatibility spectrum, **not** a spectral lower bound on arbitrary algorithms, mixed proof work, or proof-search time. Even a strong eigenvalue bound on alpha(H_G) is only a source-cover statement, and [P2-L3-522] already proves a stronger general *exact* source-cover result.

## K4 exact spectral and source-core audit (known value independently reproduced)

For K4, adjacency spectrum of G is {3,-1,-1,-1}. The formula gives H_K4 on 36 wrong-defect source clauses, degree 9, with eigenvalues 9 (1), +3 (12), 0 (8), -3 (15). Hoffman's ratio bound gives

$$
\alpha(H_{K4})\le\frac{36\cdot3}{9+3}=9.
$$

All nine R clauses belonging to one original vertex form an independent set, so alpha=9 exactly. Any unsatisfiable original-source subset must hit every compatible pair, so it must retain at least 36-9=27 R clauses. Additionally all 6 edge ALO and all 36 E clauses are indispensable; thus every UNSAT core has at least 6+36+27=69 sources. Conversely omitting exactly one full nine-clause R_v group leaves UNSAT (existing [P2-L3-521]). Therefore the known exact minimum 69 of [P2-L3-522] follows by a **second independent spectral proof**.

Under a sound source-explicit unit-cost at-most-binary-premise DAG, this gives W>=68 paid nodes for the K4 source (known implication of [P2-L3-522]). It allows shared DAGs, optimal offline selection and authorized shortcuts. It does not produce the true K4 mixed minimum; peer [P2-L3-527] supplies a legal ordinary Resolution **upper** witness of 174 nodes under declared RES semantics, not historical accepted-byte verification.

## Independent checks, controls, resources

Independent numpy/scipy Python enumerated the original K4 78 signed strict-3 clauses, all 162 two-defect assignments (27 for each vertex pair), and all 36 compatibility vertices. It obtained exactly 162 distinct edges and degree 9, and spectrum (-3:15,0:8,+3:12,+9:1). An independent 36-variable 162-edge integer MILP returned optimum 27 and matching dual bound 27 (this independently confirms, but does not replace, the analytic Hoffman proof). The independently authored Node.js verifier generated the signed source and graph separately, tested the integer matrix identity A(A-9I)(A-3I)(A+3I)=0, checked 262,144 complete Boolean assignments and verified that the 69-clause retained core is UNSAT and each of its 69 single-clause deletions is SAT, with explicit witnesses. A corrupted repeated-atom clause is flagged as malformed.

A further independent Python script constructed four 3-vertex-connected original graphs, checked vertex connectivity through two deletions, and compared all 9h numeric eigenvalues with the *symbolic formula* for K4 (h=4), K3,3 (h=6), cube (h=8), and Petersen (h=10). All four passed. Least eigenvalues respectively -3, -9, -15, -15. These are small controls, not certificates of an unbounded expander family.

Resource ledger: 69 original clauses retained, 0 new inference nodes constructed in this investigation, 36 compatibility vertices/162 edges for the K4 control, 262,144 Boolean assignments in the Node verification; 162 one-hot pair-defect flows; 69 deletion witnesses. Independent local Python K4 enumeration and MILP took 0.22 host seconds and the general spectral check uses 90 x 90 matrices at largest. These measurements exclude web/GitHub reads/writes, source indexing, standalone Node process RSS, proof discovery, persistent cache, verification of historical rules, and peak-machine accounting; **no FLMV exponent is inferred**. The ideal minimum may choose derivations freely, whereas any implemented optimizer must charge all searches, references, storage, verification, failed policies and output. No original-source SAT oracle, branch-discharge rule, altered weight, or uncharged algebraic inference is introduced.

## Status and next gap

**Actual advance:** full analytic pair-defect compatibility spectrum from the original cubic graph spectrum; exact independent spectral proof and hostile finite checks of a source-core value already established in [P2-L3-522]. It is a source-cover invariant, not a new minimum or a hardness theorem. No new historical inference grammar is authenticated.

**Remaining:** [P2-D1] historical accepted-byte grammar including DEF ownership and LOCAL-CONVERT; [P2-C3] full mixed-rule transfer; [P2-B1] superpolynomial all-rule work invariant; [P2-B2] noncircular fixed-calculus B3. In particular, the spectrum alone does not improve the already exact linear source bound and cannot establish any of these arrows.

**Publication safeguard:** root main.tex was queried at blob fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba but returned empty content bytes. It was deliberately not modified. Historical roles, R_mix341 grammar, weights and five-agent allocation unchanged. P versus NP OPEN.

## References

[1] Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 October 2026), Theorem 7.2(b). https://arxiv.org/html/2610.00837v2
[2] Willem H. Haemers, *Hoffman's Ratio Bound*, Linear Algebra and Its Applications 617 (2021), 215-219. DOI: 10.1016/j.laa.2021.02.010.
[3] LSPV-3/522, research/agents/lspv-3/2026-11-08_2054_LSPV3_THREECONNECTED_EXACT_CORE522.md (prior exact minimum).
[4] LSPV-5/452 and /453, source fan-in and context/AND-discharge scope.
[5] LSPV-2/341, frozen declared historical mixed calculus and proof-qualification limits.
