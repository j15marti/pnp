# LSPV-3/529: Exact source-authenticated shared-Resolution projection over an arbitrary cubic-vertex path

**2026-11-09 01:42 PST | Route B | PROVED/RESTRICTED symbolic construction + COMPUTATIONAL independent replay | P versus NP OPEN.**

**Node:** newly supported [P2-L3-529] extends peer [P2-L1-529] (two adjacent vertices) to every path length k. Refines evidence and limitations for [P2-C3] and [P2-D1], without resolving [P2-B1] (all mixed-rule superpolynomial minimum), [P2-B2] (noncircular same-calculus B3), or P1-01.

## IDEA, falsifiers, peer duplication and revision

Initial proposed two-vertex original-source cancellation was **already independently published** by LSPV-1/529 at `research/agents/lspv-1/2026-11-09_0109_LSPV1_TWO_VERTEX_BOUNDARY_ELIMINATION529.md` (blob `d683e37fae244cac2d56ccd5d633b00d5a302976`). Rather than duplicate it, test the substantive next implication: can its exact 72-node shared binary-Resolution interface be composed repeatedly for an arbitrary growing **tree path** of cubic vertex constraints, with one common original clause per physical edge and no free auxiliary axioms? Prediction: an explicit recurrence and legal shared-DAG certificates for k=3,4,5, with polynomial dependence on the number of **materialized boundary clauses**, although exponential in path boundary width.

Predeclared falsifiers: (F1) some intermediate projected clause requires a non-original or differently signed source; (F2) a proposed Resolution pivot, shared premise, inference ordering, or source provenance is illegal; (F3) some projected forbidden tuple is missing or excludes a genuine original-source model, including non-one-hot Boolean assignments; (F4) calling full negative-clause boundary materialization an **unrestricted** minimum-work lower bound silently excludes legal XOR, extension or compact-DAG shortcuts.

## Exact input, fixed model and existing hard-family ledger

Use a cubic tree-path fragment with k vertices v0,...,v(k-1), each incident to three **distinct edge groups**, and k-1 shared edges oriented +1 at the left vertex and -1 at the right. There are 2k+1 different edge groups and 3(2k+1) Boolean indicators. For each group E, the **original** positive ALO source is E0∨E1∨E2. At each vertex with signs s1,s2,s3∈{±1} and charge c∈F3, include exactly 18 original proper signed three-literal clauses

$$
\neg E_{1,a}\lor\neg E_{2,b}\lor\neg E_{3,d},\qquad
s_1a+s_2b+s_3d\not\equiv c\pmod3.
$$

There are exactly **20k+1 distinct original strict 3-CNF source clauses**: 18k wrong-charge forbidders and (2k+1) ALO clauses. The graph fragment has k+2 exposed boundary edge groups; all interior shared edge groups occur with opposite signs. All sources are SAT, with exactly 3^(k+1) Boolean models; this is a source-preserving **local interface** construction, not an UNSAT family.

**Original-source Boolean-model lemma.** Every original ALO makes each edge group nonempty. If two indicators of one group E were simultaneously true, select any one true indicator from each of the other two groups at an incident vertex (ALO guarantees their existence). One of these two E values fails that vertex's signed mod-3 equation, so its corresponding original negative forbidden ternary is false. This contradicts source satisfaction. Thus each group is EXACTLY one-hot, despite having no imported AMO source clauses. Over F3 the k vertex equations on a tree path of 2k+1 edge groups are independent: an end-vertex row has two exterior edges absent from all other rows, so recursive end-row removal shows rank k. Accordingly exactly 3^((2k+1)-k)=3^(k+1) original Boolean models exist. For fixed exterior boundary values, the interior k-1 shared-edge values are uniquely determined by successively solving end-vertex equations; an extension exists iff the one remaining global boundary-balance equation holds. This proves the asserted existential projection without an uncharged oracle or auxiliary-source assumption.

The pre-existing established-hard family remains opposite-characteristic modulo-3 Tseitin on qualifying fixed-degree expander graphs: Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), Theorem 7.2(b), exponential for fixed r in Res(PC_r/F_p) when p≠3 under the stated expansion/degree assumptions, with matching-field affine shortcuts. Pang's theorem is NOT a lower bound for historical R_mix341, extended Resolution, or the particular SAT tree fragment used here. The present original one-hot strict-three encoding is from project LSPV-3/520; no general theorem-preserving conversion from Pang's exact encoding to R_mix341 is claimed. Ben-Sasson and Wigderson (JACM 48, 2001) characterize Resolution width/size controls in a different proof model.

## THEOREM 529.1 (PROVED/RESTRICTED, ordinary binary Resolution)

For every k≥1 and every charge/sign choice on such a cubic path, the original sources have a **single original-source-authenticated shared-DAG ordinary Resolution** derivation of *all* boundary forbidding clauses for the wrong modulo-three boundary sums. Precisely, the k+2 exposed edge groups have

$$
M_k=2\cdot3^{k+1}
$$

forbidden one-hot boundary tuples, each exported as one all-negative width-(k+2) clause. The explicit derivation uses exactly

$$
\boxed{W_k=4\cdot3^{k+1}-36=2M_k-36}
$$

distinct unit-paid binary Resolution steps, with 2W_k premise references, exactly 19k-1 distinct original-source ancestors, maximum intermediate clause width k+2, and ideal unit-weight dependency span 3(k-1). Each original clause is supplied at most once as a SOURCE node, all derived nodes use two prior premises, and shared intermediate clauses are charged once.

**Proof.** For k=1 the 18 original wrong-charge ternaries are exactly the 18 forbidden boundary tuples: M1=18 and W1=0. Suppose the k-vertex fragment has a source-authenticated derivation of all M_k negative clauses on boundary B∪{E}, with |B|=k+1 and E the outgoing shared edge. For each of the 3^(k+1) assignments a on B, precisely one value t(a)∈F3 of E makes the contracted charge equation true. The other two values t' and t'' each have an already derived forbidden clause (¬B_a∨¬E_t'). From the ORIGINAL E-ALO source and these two negative clauses, make two oriented binary-RES inferences to derive the guarded port (¬B_a∨E_t(a)). These 2·3^(k+1) nodes are shared by all later uses of that port.

Attach a new cubic vertex with incident groups E,C,D, sign of E opposite to its sign in the old cluster, and its 18 ORIGINAL wrong-charge source ternaries. For every assignment (a,c,d) that violates the new (k+1)-vertex boundary balance, its unique old permissible shared t(a) is forbidden by the new vertex source (¬E_t(a)∨¬C_c∨¬D_d). One binary Resolution on E eliminates the internal edge and exports exactly (¬B_a∨¬C_c∨¬D_d). There are 2·3^(k+2) such final joins. Therefore

$$
W_{k+1}=W_k+2\cdot3^{k+1}+2\cdot3^{k+2}
       =W_k+8\cdot3^{k+1},
$$

and induction from W1=0 yields Wk=4·3^(k+1)-36. Every source is a genuine original ALO or wrong-charge clause, each RES is oriented, and assumptions are globally empty. New joins have depth at most three beyond the previous stage. Every vertex's 18 forbidden sources and every internal edge's ALO are ancestors, yielding 18k+(k-1)=19k-1; the k+2 unused original ALO boundary clauses remain legitimate original source records but are not ancestors. The exact existential projection on one-hot boundary assignments follows by uniquely reconstructing the internal edge values from the end along the tree. QED.

**Scope.** This is an explicit simultaneous **UPPER certificate** in ordinary RES, not an optimality theorem, not a complete global UNSAT refutation, and not an accepted-byte R_mix341 certificate. The historical LSPV-2/341 prose (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`) semantically lists arbitrary-width RES, but the authoritative historical checker grammar and full DEF/AND3/GF(2)/LOCAL-CONVERT interface [P2-D1] are unauthenticated. No silent rule addition or historical weight change was made.

## ITERATE: independent finite proof and source checks

The complete Python producer and independently implemented signed-RES checker were executed locally, followed by a **separately written Node.js verifier** rebuilding the authentic original clauses and checking every pivot, source owner, parent ordering, final tuple and one-hot model. For k=2 and k=3, independent Node.js checked **all 2^15=32768 and 2^21=2,097,152 original Boolean assignments**, confirming respectively 27 and 81 original-source models, including exclusion of every non-one-hot assignment. It rejected eight corruption variants at each of k=2,3,4 (24 total). No official historical mixed or CakeML checker was run. Exact source/model controls:

| k | Original strict 3-CNF clauses | Paid RES | Total records | Boundary arity | Export clauses | Live source ancestors | Ideal span | Python JSON proof bytes |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 21 | 0 | 21 | 3 | 18 | 18 | 0 | 2,166 |
| 2 | 41 | 72 | 113 | 4 | 54 | 37 | 3 | 9,920 |
| 3 | 61 | 288 | 349 | 5 | 162 | 56 | 6 | 31,406 |
| 4 | 81 | 936 | 1,017 | 6 | 486 | 75 | 9 | 95,318 |
| 5 | 101 | 2,880 | 2,981 | 7 | 1,458 | 94 | 12 | 298,193 |

The Python source generator/checker, independent JS checker, compact JS generator and actual certificates for k=2,3,4 plus machine-readable raw summary are supplied as run artifacts. GitHub-reproducible compact JS is `experiments/arc/lspv3_529_compact_tree.js`; machine-readable project summary is `results/raw/arc/2026-11-09_0142_LSPV3_TREE_PROJECTION529_RAW.json`.

Finite proof construction/verification across k≤5 took 1.064 s Python host wall time, with process max-RSS 125,324 KiB including Python interpreter and checking. Independent Node.js k≤4 replay took 93, 531 and 70 ms respectively for the three certificates; these figures are implementation measurements, **not** minimum-work or native-Turing-machine runtime bounds. The ideal W excludes discovery; actual programs additionally charge source parsing, graph and certificate generation, output bytes, source and commit/index/head reads, independent verification, failed attempts and live memory. For a tree fragment of size k, the explicit record count is Θ(3^k), with O(k log k) bits per large record and O(k·3^k log k) total serial bits. Peak host RSS is not a theorem about the FLMV same-machine model.

## SEARCH provenance and model controls

Read full root proof1.txt SHA `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2.txt initially SHA `a44ee2f4a7aceedd9587f721c0dc52ae8f7ee308`, current issue #3 including LSPV-1/529, historical five-role handoff blob `c3889a3e514ddbd747150dcb68607013a3b2d154`, AGENTS.md, CODEX.md, project pnp-research skill, historical /341 calculus prose, LSPV-3/526 and /528, LSPV-5/455 critique, actual GROKPROOF/2026-11-06_2316_PROGRESS.md, and Claude world-ledger README. Search scope: 'two vertex boundary modulo-three resolution elimination', 'Tseitin expander Resolution width size', Pang arXiv:2610.00837v2, GitHub repo `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` (conditional/finite formalization), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (bounded claims), `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (distinct high-arity XLRUP format), and `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. `tanyongkiam/cake_lpr` README lookup on assumed main returned 404; no claim of inspecting that current branch. No Google-branded search or official proof checker was executed. Literature search was focused, not exhaustive.

**Interpretation:** This precisely exhibits *cross-vertex, multi-stage shared proof-DAG reasoning* at a calculable cost, but does not prove that all legal proofs must materialize the exponentially many boundary clauses. Compact affine, ER circuit, extension, non-frontier, algebraic and shared-circuit shortcuts remain available and are mandatory upper controls. Thus the result supplies no full mixed-system lower bound, no conversion B3, and no universal SAT decision bound. [P2-D1], [P2-C3], [P2-B1], [P2-B2] all remain OPEN. P versus NP OPEN.

**Reference sources:** [1] Pang (2026), arXiv:2610.00837v2 (opposite characteristic, fixed-degree calculus); [2] Ben-Sasson & Wigderson, JACM 48:149-169 (2001), DOI:10.1145/375827.375835 (Resolution width/size); [3] LSPV-1/529 (existing two-vertex base case); [4] LSPV-2/341 (fixed mixed prose, not authenticated bytes).
