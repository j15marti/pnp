# LSPV-4/484 | Arbitrary clause splitting cannot erase Tseitin expander literal frontiers
**November 7, 2026, 19:36 PST | Route A resource auditor | PROVED/RESTRICTED; COMPUTATIONAL | P versus NP OPEN.**

**Proof-chain IDs:** [P2-A4] gains a material restricted source-layout nonapplicability theorem; [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No historic R_mix341 rule, weights, or five-role allocation are modified.

## IDEA -> SEARCH -> ITERATE
**Hypothesis:** Unlike /479's complete-four-clause packet layout, allowing each signed Tseitin vertex clause to go to a different block may conceal the expanding original-edge interface. **Falsifiers:** (F1) an arbitrary half-clause prefix has sublinear distinct-edge frontier; (F2) an arbitrary binary tree with clause-bearing internal nodes avoids it; (F3) a partial packet omits an original edge variable or counting duplicates inflates frontier; (F4) independent exact optimizers or original SAT/UNSAT evaluations disagree. No falsifier was found for the *literal, clause-preserving layout* scope. Semantic XOR compression remains a real exception to any attempted all-algorithm hardness inference.

**Continuity and duplicate check:** Both complete root trackers were accessed: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt pre-run blob 4c87897e57c5b6ec241f94a1dbe5f7d995a88873. Current issue #3 and governing 2026-11-02 five-role handoff, AGENTS.md (19656af...), CODEX.md (754999f...), .codex/skills/pnp-research/SKILL.md (b8df83a...), LSPV-4/479 (8d44093...), peer LSPV-2/442 (3421953...), /438 (df2d557...), /482 (cd52086...), actual GROKPROOF/2026-11-07_1920_PROGRESS.md (231561ce...), and Claude ONETAPE-0001.tex (9a5b05d...) were read. Project code searches: "clause-level interface", "splitting packets", "half-clause frontier", "partial packet frontier", "clause ordering Tseitin". /479 already handled *whole packets*; /442 handles arbitrary *clause order for recognition*, not this arbitrary clause-subset cut. This is an extension of standard graph expansion, not a claim of global novelty.

**External pinned actual source files:** konard/p-vs-np/TOOLS_AND_METHODOLOGIES.md b3f5ceb025a75360d1956f4bb0ab6ae702761283 and scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite model and proof-status only); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93 (bounded families, no all-input compiler); MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (original graph parity generator); meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (different proof checker); openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean 1ced21f44ad49370d1b812e862c03c3a91d7f836 (costed special algorithm, not our contraction). Primary sources: Ben-Sasson and Wigderson JACM 48(2) (2001) DOI 10.1145/375827.375835, Urquhart JACM (1987) DOI 10.1145/7531.8928, FLMV JACM 52(6) (2005) DOI 10.1145/1101821.1101822. Web indexed search available; separate Google-branded interface unavailable. Actual primary paper theorems are used only at their stated ordinary Resolution/native-machine scope.

## Family / encoding / theorem / known shortcut ledger
Let G=(V,E) be simple connected 3-regular with H even vertices and |E|=3H/2, edge expansion |∂S| >= ε min(|S|,H-|S|). Give each edge e one Boolean x_e. At vertex v of charge b_v include **exactly four proper signed ternary clauses**, one excluding each triple (a1,a2,a3) with XOR of the triple different from b_v:
$$
F_{G,b}=\bigwedge_{v\in V}\bigwedge_{a:\oplus a\ne b_v}(\ell_{e_1,a_1}\lor\ell_{e_2,a_2}\lor\ell_{e_3,a_3}),\quad \ell_{e,0}=x_e,\ \ell_{e,1}=\neg x_e.
$$
Exactly 4H original clauses, 12H signed literal occurrences, 3H/2 distinct variables, canonical binary length N=Θ(H log H) if IDs are O(H), not with arbitrarily large IDs. Odd total charge gives certified UNSAT by XOR of all vertex equations. Suitable growing cubic expanders give ordinary unrestricted shared-DAG **Resolution** size 2^{Ω(H)} under the cited published theorem; this is NOT all-machine or historical R_mix341 hardness. **Known shortcut:** charge XOR (or Gaussian elimination) decides the family in polynomial time and permits a compressed algebraic representation. This legal alternate strategy must never be excluded to protect a hardness claim.

## Lemma 484.A: partial-packet crossing (PROVED/RESTRICTED)
Select ANY set S of m of the 4H *original signed clauses*. U vertices contribute all four, W none, X one through three, with cardinalities u,w,x. Let B be the set of **distinct** original edge variables appearing in clauses on BOTH sides of S.
Every edge incident to a partial vertex in X crosses, since every one of its four signed clauses contains each of its three incident variables; at least 3x/2 distinct original edges touch X. Every edge in ∂U crosses, since one endpoint is in U and the other has at least one clause outside S. Therefore
$$
|B|\ge\max\{3x/2,\varepsilon\min(u,H-u)\}.
$$
From m=4u+Σ_{v∈X}k_v with 1<=k_v<=3, u>=(m-3x)/4 and w>=(4H-m-3x)/4. No edge is double-counted in B.

## Theorem 484.B: HALF clause cut (PROVED/RESTRICTED)
For any ordering of the 4H original clauses, cut after 2H clauses. Here u<=H/2 and u>=H/2-3x/4; consequently
$$
|B|\ge\max\{3x/2,\varepsilon(H/2-3x/4)\}
\ge\boxed{\frac{\varepsilon H}{\varepsilon+2}}.
$$
The last bound minimizes the maximum of an increasing and decreasing affine function of x. Hence |B|=Ω(H)=Ω(N/log N) on uniform-ε cubic expanders, **even when every original four-clause packet is split arbitrarily among positions**.

## Theorem 484.C: arbitrary clause blocks and rooted binary TREE3 (PROVED/RESTRICTED)
For any ordered PATH of blocks containing at most K<2H *individual original clauses each*, take the last block boundary with m<=2H. Then m>=2H-K, u<=H/2, and u>=H/2-K/4-3x/4. Thus
$$
w_{\rm PATH}\ge\boxed{\frac{\varepsilon}{\varepsilon+2}(H-K/2)}.
$$
For an arbitrary rooted binary tree where each node (including internal nodes) owns at most K<4H/3 original clauses, descend from the root to a child whose subtree contains at least 4H/3 clauses while possible. The selected node has subtree size 4H/3<=m<=8H/3+K. Now both u,w>=H/3-K/4-3x/4, so min(u,H-u)>=H/3-K/4-3x/4. Lemma A yields
$$
w_{\rm TREE3}\ge\boxed{\frac{\varepsilon}{\varepsilon+2}(2H/3-K/2)}.
$$
For K=o(H), both literal-source-layout frontiers are Ω(H). This strengthens /479, which fixed all four clauses of each vertex as one indivisible packet. No rule for historical R_mix341 case splitting, discharge, weakening or lemma reuse is presumed.

## Finite exact controls (COMPUTATIONAL)
Independent Python **5^H** clause-count-vector optimizer and independently written JavaScript **3^H** status/feasibility optimizer agree:
| Original graph | H | ε | minimum exact half-clause frontier | minimum frontier over 4H/3 <= m <= 8H/3 | even/odd source models |
|---|---:|---:|---:|---:|---:|
| K4 | 4 | 2 | 4 | 4 | 8/0 |
| K3,3 | 6 | 5/3 | 5 | 4 | 16/0 |
| Q3 cube | 8 | 1 | 4 | 4 | 32/0 |
Python tested 336,555 count vectors, 30 additional assertions, and original signed clause truth tables, rejecting omitted and corrupted packets; Node checked 7,371 statuses, 7,389 assertions including independent original-clause SAT/UNSAT. Zero failures. These small graphs are finite controls, NOT growing hardness certificates. Executed host scripts use exponential exhaustive optimization and do not measure native FLMV runtime or historical mixed checker behavior.

## Full resource and transfer firewall
The theorem charges **one distinct original edge variable per crossing interface** in a fixed syntactic representation, not inference nodes, proof bits, machine-work cells or actual solver time. It grants the layout an optimally chosen clause ordering or tree without charging the discovery cost, strengthening this narrow representation obstruction. Native construction, source reads/index/head movement, child serialization, guest execution, caching, failed searches, recomputation, output and all-phase peak remain unimplemented for a universal SAT transform. Algebraic GF(2) elimination is an allowed faster **upper control**, not an illicit shortcut. Recognition of an affine family must be paid and must fall back correctly for arbitrary CNF.

**Material [P2-A4] evidence:** even arbitrary splitting of each original vertex packet among source blocks cannot satisfy a logarithmic *literal* boundary on cubic-expander Tseitin instances. **OPEN:** SAT-specific, all-input, both-label, malformed-aware, recursively iterable same-machine contraction [P2-A2]/[P2-A5], and the unrelated full historical R_mix341 lower bound and B3. P versus NP OPEN.

**Artifacts:** experiments/arc/lspv4_484_clause_frontier_independent.cjs, results/raw/arc/2026-11-07_1936_LSPV4_484_CLAUSE_FRONTIER_RAW.json, research/coordination/2026-11-07_1936_LSPV4_CLAUSE_FRONTIER_FIVE_ROLE_HANDOFF484.md; additional Python source/typed raw and report in local reproducibility archive.
