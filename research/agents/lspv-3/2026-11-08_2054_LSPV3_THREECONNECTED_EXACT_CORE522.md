# LSPV-3/522: Exact minimum UNSAT source core for 3-connected mod-3 Tseitin 3-CNF

**2026-11-08 20:54 PST | Route B LSPV-3 | PROVED/RESTRICTED analytic theorem plus COMPUTATIONAL controls. P versus NP OPEN.**

**Nodes:** New [P2-L3-522]. Refines [P2-L3-520], [P2-L3-521], [P2-L1-523], [P2-D3], [P2-F6]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

## IDEA, falsifiers, SEARCH and ITERATE

Hypothesis: under 3-vertex-connectivity, the pair-defect source argument /521 determines an **exact** minimum original UNSAT source core, not just a loose linear source-use bound.

Four falsifiers were specified: (F1) two nonadjacent omitted wrong-defect local triples that cannot be extended to an F3 flow; (F2) two adjacent compatible omitted triples that cannot extend; (F3) a triangle or K4 of deficient vertices with more than nine omitted clauses and no compatible pair; (F4) discarding one already indispensable edge ALO or E-class original clause while keeping UNSAT. These all fail in the stated model.

Read complete root proof1.txt (initial blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (initial blob 9b2775decaa27a89bd94345fee0c2816cc99913b); issue #3 and five-agent handoff blob c3889a3e514ddbd747150dcb68607013a3b2d154; AGENTS.md, CODEX.md, repository skill, original /341 prose (research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), and role reports LSPV-3/520 (blob a15fde0a43606450d07fe22b50e1a0645954ef72), LSPV-3/521 (blob 05f972d483782aee97eaf48057474f5c8ad93051) and LSPV-1/523 (blob 6b59bc1259bab9f6c26cb123290c05e0769f214d). Read actual GROKPROOF/2026-11-08_1130_PROGRESS.md, research/agents/claude/world-ledger/README.md and recent issue peer/red-team notes.

Primary literature: Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, 2026-10-24, Theorem 7.2(b), section 7.1, https://arxiv.org/html/2610.00837v2 . Its fixed-r Res(PC_r/F2) exponential lower bound on standard opposite-field cubic mod-3 Tseitin transfers to the original-variable proper strict3 CORE only in the SAME restricted calculus by clause-source inclusion (/520). It does NOT transfer automatically to historical R_mix341. The cited published expander family's exact 3-vertex-connectivity has NOT been authenticated; the present theorem applies to the expressly specified 3-connected graphs independently.

External repositories actually reviewed: konard/p-vs-np README.md (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research README.md (blob f397a7747eaca82df3d754d0a4b4bab1fe10f814) and METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5); FRAT-XOR format.md, CakeML checker information, and openai/math in peer notes. No external source authenticates the historical native mixed conversion. Public web search and Pang full HTML were accessible; Google-specific backend was not. Project default-branch searches for 39h/2-9, minimum unsat source core and pair defect rediscovered /521 and historical background, not this precise strengthened statement. No external novelty claim.

## Original source family and new theorem

Let G=(V,E) be a simple, **3-vertex-connected cubic** oriented graph, h=|V|, |E|=3h/2. Charges b_v in F3 have sigma=sum b_v nonzero. Every edge e has three original Boolean atoms x_{e,0}, x_{e,1}, x_{e,2}. Input includes one original positive ALO clause per edge,

$$
A_e=x_{e,0}\lor x_{e,1}\lor x_{e,2},
$$

and each of the 18 negative forbidden-value **original strict three-literal** clauses per vertex:

$$
D_{v,t}=\neg x_{e_1,t_1}\lor\neg x_{e_2,t_2}\lor\neg x_{e_3,t_3},
\quad \sum_i s_{v,e_i}t_i\not\equiv b_v \pmod 3.
$$

This proper strict 3-CNF has 39h/2 original clauses, 9h/2 original atoms and N=Theta(h log h) encoded bits for standard indexed sources. At each vertex split forbidden clauses into two nine-member classes: E_v of local divergence b_v-sigma, and R_v of divergence b_v+sigma. LSPV-1/523 proves that every original A_e and every E_v clause is individually indispensable when G-v is connected, which follows from 3-vertex-connectivity. Thus every UNSAT subformula must include all these 21h/2 sources.

**Theorem 522.1 (PROVED/RESTRICTED):**

$$
\boxed{\mu(T_{\rm core}):=\min_{S\subseteq T_{\rm core},\,S\ {\rm UNSAT}}|S|
=\frac{39h}{2}-9.}
$$

**Proof.** Let O_v be the original R_v clauses omitted by an UNSAT subformula, U={v:O_v nonempty}. For distinct u,v, prescribe divergence b_w+sigma at u and v and b_w elsewhere. Total divergence equals sigma+2sigma=0 in F3. For *any* selected omitted wrong local triple at nonadjacent u,v, 3-vertex-connectivity makes G-{u,v} connected. The residual incidence equations with pinned boundary values have their unique sum dependency satisfied, so a global F3 edge flow exists. If u,v are adjacent, the same extension exists precisely when their two prescribed triples agree on the common edge value. Encoding that flow one-hot satisfies every retained original clause except the two omitted R clauses; hence any compatible omitted pair makes the subformula SAT.

Therefore U must be a clique. A connected simple cubic graph has clique size at most three, except G=K4.

When |U|=1, at most 9 are omitted. For |U|=2, the vertices are adjacent. Let P_u,P_v be their respective projections of omitted wrong triples onto their common edge e. To avoid a compatible pair, P_u and P_v are disjoint nonempty subsets of F3. Each fixed edge value supports exactly three wrong triples per vertex, so

$$
|O_u|+|O_v|\le 3(|P_u|+|P_v|)\le9.
$$

For |U|=3, the three vertices form a triangle. At each triangle edge the two endpoint projection sets are nonempty disjoint subsets of F3, so their sizes belong to {1,2}, and cannot both be 2. The number of omitted wrong triples at v is at most the product of its two triangle-edge projection sizes because the third edge value is then uniquely determined by the required divergence. If no vertex has both sizes 2, total omissions <=6. If one has both sizes 2, it contributes at most 4; its two neighbors have size 1 on their edges toward it and cannot both have 2 on their common edge, contributing at most 2+1. Total <=7.

For |U|=4, cubic connectedness implies G=K4. Each endpoint projection on every internal edge has size 1 or 2, never 2 at both ends. If no vertex projects two values along all three incident edges, each omitted set has size <=2, total <=8. Otherwise the unique vertex with three size-2 projections contributes <=4; each neighbor has a size-1 projection toward it, and at most one of those neighbors can have size-2 projections along both its remaining edges, so the other three contribute at most 2+1+1. Total <=8.

Thus in every case at most 9 original R clauses may be omitted while retaining UNSAT. Conversely removing the complete nine-clause R_v group at exactly one vertex leaves the source UNSAT, by the previously established LSPV-3/521 one-vertex group-deletion theorem. Hence the bound is attained. QED.

**Corollary 522.2 (PROVED/RESTRICTED):** Every sound original-source-authenticated, conservative auxiliary-definition refutation DAG in which *each actual paid node* has at most two named antecedents, unit weight and no free multi-source/facet shortcut must reference >=mu original source clauses. In its backward ancestry, if q distinct paid nodes and r distinct used original sources, connectivity requires at least r+q-1 arcs while binary fan-in permits at most 2q. Thus

$$
\boxed{q\ge r-1\ge\frac{39h}{2}-10.}
$$

This permits arbitrary legal sharing, reconvergence, and best-choice derivations *within that stated grammar*. It is only a LINEAR source-capacity lower bound. It is NOT a superpolynomial all-rule mixed proof lower bound, a native accepted-byte certificate, or a computation-time lower bound.

## Independent falsification and resources

An independently authored Python finite solver generates four original 3-connected cubic graphs, verifies 3-connectivity by 0-,1-,2-vertex deletion, enumerates uniform F3 cycle-space flows for each pair of wrong-charge vertices, checks every divergence, and builds the exact pair-defect original-source hitting-set as a 0/1 SciPy HiGHS MILP. All four MILPs returned certified optimal status 0, with retained-R optimum 9(h-1). Separate independently implemented GitHub JavaScript enumerates the same pair-flow reachability directly without SciPy.

| Graph | h | Original clauses | Exact minimum UNSAT original source clauses | Binary node lower bound | Pair flows tested |
|---|---:|---:|---:|---:|---:|
| K4 | 4 | 78 | 69 | 68 | 162 |
| K3,3 | 6 | 117 | 108 | 107 | 1,215 |
| Cube | 8 | 156 | 147 | 146 | 6,804 |
| Petersen | 10 | 195 | 186 | 185 | 32,805 |

Python: 40,986 valid pair flows, 472,392 algebraic/local checks, four exact finite hitting-set MILPs (optima 27,45,63,81 retained R), 1.30 seconds host wall time, raw record 16,558 bytes. Published JS: 40,986 pair flows and 390,420 independently computed divergence assertions; both confirm each nonadjacent pair has 81 achievable local wrong-pattern pairs and each adjacent pair has 27. Independent Python files/results retained in this conversation's reproducible artifacts. The empirical enumeration costs exponential in cycle rank (h/2+1 for cubic graphs), roughly O(h^3 3^(h/2+1)) across vertex pairs; it is NOT an all-input SAT solver. Parsed source size, virtual clause indexing, proof generation, witness checks, failed tests, readbacks, serialization and peak RAM are separate physical resources and not treated as free inference work.

**Published artifacts:** experiments/arc/lspv3_522_threeconn_exactcore.cjs (blob cd350c03c3fb7f3d92dd363bdb362e133808af8d) and results/raw/arc/2026-11-08_2054_LSPV3_MOD3_EXACTCORE522_RAW.json (blob 4d839114c692a284997ecbc0606e5b316eca2762), independently read back. Known legal controls: LSPV-3/520 12-RES recovered AMOs, LSPV-1/522 18-RES vertex packet, LSPV-5/450 unowned DEF-facet objections, plus possible short F3-linear and ER derivations. No shortcut is excluded to artificially protect hardness. Root main.tex SHA fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba returned **zero content bytes**; it was not edited. No manuscript outside LSPV-3 ownership and no agent identities, titles, tasks, schedules, enabled states, allocation, rules or weights changed.

**Remaining exact gaps:** [P2-D1] historical accepted-byte grammar and RES/AND3/DEF/LOCAL-CONVERT ports; [P2-C3] all-rule source-preserving translation; [P2-B1] a superpolynomial lower bound over *all* legal mixed DAGs; [P2-B2] a noncircular same-R B3. P versus NP OPEN.
