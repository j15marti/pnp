# LSPV-1/523: Global-charge classification of indispensable strict-3 Tseitin clauses
**2026-11-08 19:56 PST | Route B lead | PROVED/RESTRICTED original-source semantic necessity and binary-premise counting; COMPUTATIONAL finite controls. P versus NP OPEN.**

**New tracker node:** [P2-L1-523]. Refines [P2-L3-520], [P2-L1-522], [P2-F6], [P2-C3] and [P2-B1]. Historical byte grammar [P2-D1], complete mixed transfer [P2-C3], superpolynomial mixed minimum [P2-B1], and noncircular same-calculus B3 [P2-B2] remain OPEN. Cross-chain [P1-X1] unchanged.

## IDEA before SEARCH: precise falsifiers
Hypothesis: for LSPV-3/520's original-variable strict-proper-3CNF modulo-3 Tseitin CORE, the global nonzero charge forces exactly one of the two incorrect local charge classes on any possible one-clause deletion witness. Thus only half the forbidden-triple clauses can be semantically indispensable, while each edge ALO is indispensable. On 2-vertex-connected cubic graphs, EVERY clause in that predicted half is indispensable. This yields a precise, explicitly qualified linear source-ancestry lower bound for any sound conservative calculus whose paid inferences have at most two premises.

Registered falsifiers: (F1) a multi-hot model of the formula with just one forbidden clause deleted; (F2) a single-clause-deletion assignment violating a forbidden tuple of the *wrong* charge defect; (F3) a critical forbidden tuple on a 2-vertex-connected graph that fails to extend to a satisfying assignment of all other sources; (F4) an edge ALO whose deletion still leaves the formula UNSAT. Exhaustive K4 and constructive finite witness checks did not trigger any falsifier. A higher-premise or semantic-oracle rule would invalidate the claimed **unit-arity bound**, but not the semantic source-deletion classification.

## SEARCH / continuity and actual corpus
Read BOTH complete live trackers: proof1.txt blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** (18,553 characters) and proof2.txt blob **979d99acc6afd9b2363fea238f3737c74052a5fe** (598,750 characters), and current coordination issue #3 including peer LSPV-3/520, LSPV-5/449 and LSPV-4/509. Historical governing five-role refocus at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e514ddbd747150dcb68607013a3b2d154; AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561; CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef; .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f; historical Rmix341 declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Actual Grok GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70 and actual Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4e7e0e3edff3aba8610852c45534bdde128 were reviewed.

Immediate role peers: research/agents/lspv-3/2026-11-08_1925_LSPV3_MOD3_21CLAUSE_STRICT3_PORT520.md blob a15fde0a43606450d07fe22b50e1a0645954ef72; research/agents/lspv-1/2026-11-08_1900_LSPV1_MOD3_VERTEX_LOCAL_SOURCE_RES522.md blob ab0cd2db22f67ed57486d5048fc804813a39d5b0; research/main/2026-11-08_1851_MAIN_ONEHOT_MOD3_RESOLUTION_PACKET_REFEREE449.md blob 687128b76215b443b9a0cf8989418bbe3505d59a. Prior LSPV-2/341 already gives analogous essential-source binary counting for mod-2 Tseitin; present mod-3 *global defect selection* is more specific and should not be characterized as a new general graph-counting theorem.

External required source checks: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5. These are scoped investigations, not P-vs-NP proofs or Rmix341 checkers. FRAT-XOR README.md blob 38a137bca4d4ab6443703d4c31fba5783021c581 specifies a DIFFERENT certificate format. openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae has diverse formalization status, not this inference grammar. The full current primary arXiv HTML was inspected: Shuo Pang, arXiv:2610.00837v2 revised 2026-10-24, Theorem 1.1 and Section 7.2 (https://arxiv.org/html/2610.00837v2). Public search queried modular Tseitin essentiality, established proof lower bounds and random cubic expanders; Google-branded backend not separately available. No novelty inference is made from an unsuccessful search.

## Theorem 523.1: exact global one-deletion classification
Let G=(V,E) be a **simple connected cubic graph**, h=|V|, m=3h/2. Orient edges arbitrarily. Each edge has three ORIGINAL Boolean indicators x_(e,t), t∈F3. At vertex v with signed incidences s_(v,e)∈{±1}, require sum_e s_(v,e)t_e = b_v in F3. Let the global charge sigma=sum_v b_v∈{1,2}.

The LSPV-3/520 CORE contains one **proper signed ternary ALO** A_e=x_(e,0)∨x_(e,1)∨x_(e,2) per edge, and for each vertex the 18 **proper signed ternary forbidden triples**
D_(v,a,b,c)=NOT x_(e1,s1 a)∨NOT x_(e2,s2 b)∨NOT x_(e3,s3 c)
for a+b+c≠b_v (signed values a,b,c). There are 39h/2 original source clauses and 9h/2 original Boolean atoms; no AMO facets, padding, private wires or new axioms.

**(i)** Every A_e is individually indispensable: F\{A_e} has a satisfying assignment.

**(ii)** If D_(v,a,b,c) is individually indispensable, then
$$
a+b+c\equiv b_v-\sigma\pmod3.
$$
Consequently all 9h forbidden triples with the OTHER nonzero defect are individually redundant: deleting any one leaves the formula UNSAT.

**(iii)** If G-v is connected for every v (2-vertex-connectivity), the converse holds. Exactly 9 of the 18 forbidden triples at each vertex, those satisfying the displayed identity, are indispensable. The complete exact count of semantically indispensable original clauses is
$$
m_{\rm ess}=|E|+9h=\frac{21h}{2},
$$
and the other 9h clauses are individually redundant. This is a classification of **one-source deletion**, not a claim that all individually redundant clauses can be removed simultaneously while preserving UNSAT.

**Proof of (ii).** All ALOs still hold after removing one D. Every edge has an endpoint w≠v because G is loop-free. At w all 18 forbidden clauses are intact. Since its other two incident edges have at least one true indicator, two distinct true values on any one incident edge would activate a forbidden triple (at most one value can satisfy the charge). Thus *every* edge is still one-hot. All w≠v satisfy their vertex equations. Summing these equations cancels all internal edge contributions and gives the forced signed sum at v:
$$
S_v=-\sum_{w\ne v}b_w=b_v-\sigma\pmod3.
$$
If F\{D} has a model, it must activate exactly the removed D at v; the triple's signed sum must be b_v-σ. This proves (ii) without assuming G-v connected.

**Proof of (iii).** Choose any forbidden triple with signed sum b_v-σ, fix the three incident edge values accordingly, and solve the vertex equations at all w≠v. Their coefficient matrix on the edges of connected G-v has rank h-2 over F3; its sole row dependency is the sum. The fixed boundary values make the sum consistent by the displayed equality. Hence a solution exists. Set every original indicator to the resulting one-hot assignment. Exactly the removed D is false; every other source clause is true.

**Proof of (i).** Remove A_e with e={u,v}, set ALL three bits of edge e to zero, making the forbidden clauses at u and v automatically true. The equations at every w outside {u,v} involve all other edges and have full row rank h-2: each component of G-{u,v} has a boundary edge to {u,v}, and the signed incidence rows have no nonzero dependence. Thus the remaining equations are solvable for arbitrary charges. Encode their edge values one-hot. Every other original clause is satisfied and A_e is false. This construction uses no semantic oracle in a claimed solver; Gaussian elimination is an OFFLINE source-deletion witness generator.

**Important graph hypothesis.** The exact 9h forbidden indispensability in (iii) needs G-v connected. It is NOT established here for an arbitrary expander with a cut vertex. Pang's hardness theorem must not silently be specialized to a 2-vertex-connected expander subfamily without separately sourcing that graph-family property.

## Corollary 523.2: binary-premise minimum work, qualified
Consider ANY sound source-authenticated derivation of false from this CORE, conservative in auxiliaries, with its FREE input premises explicitly referenced, and with every paid inference of fan-in ≤2 and weight ≥1. Every individually indispensable original source appears in the ancestry of the contradiction. The undirected underlying one-root proof DAG is connected. If q paid nodes and m≥21h/2 indispensable source leaves occur, there are at most 2q premise arcs and at least m+q-1 arcs to connect all vertices. Therefore
$$
q\ge m-1\ge\frac{21h}{2}-1.
$$
This permits ALL legal binary-premise sharing and reconvergence, and counts each distinct node once. The result is a **linear** minimum lower bound under the stated calculus assumptions, NOT a superpolynomial lower bound. In the explicit indexed source encoding N=Θ(h log h), its order is Ω(N/log N), not Ω(2^h). It does NOT automatically apply to the unauthenticated historical native grammar or to higher-arity/semantic-oracle rules. It does not establish a lower bound on SAT algorithms.

## ITERATE: independent finite falsification and resource ledger
Self-contained Python: experiments/arc/lspv1_523_global_charge_source_essentiality.py (conversation fallback /mnt/data/lspv1_523_global_charge_source_essentiality.py). It independently constructs the literal 3-CNF, verifies every predicted indispensable clause by actual source-deletion satisfaction checks on GF3-solved assignments for K4, K3,3, cube Q3 and Petersen, both σ=1,2. Results: (h,m,clauses,essential)=(4,6,78,42),(6,9,117,63),(8,12,156,84),(10,15,195,105). All eight cases pass; 588 individual clause witnesses verified (two charge settings: 2*(42+63+84+105)=588). Every full-source nonzero-charge case is UNSAT by the symbolic total-charge invariant.

Independent Node.js program experiments/arc/lspv1_523_k4_independent.js reconstructs K4 sources *from scratch* and exhaustively scans all 2^18=262,144 Boolean indicator assignments at each σ=1,2, and zero-charge baseline σ=0. For σ=1 and σ=2 each: precisely 42 distinct clauses admit singleton source-violation assignments, 36 other D clauses do not, and no satisfying assignment exists. In each nonzero-charge run there are 270 assignments violating exactly one clause. At σ=0 there are 27 satisfying assignments (and no UNSAT or essentiality conclusion). A deliberately flipped clause literal is detected as corruption. JS host run 0.27 seconds, 33,128 KiB reported maximum RSS; Python host run 4.69 seconds. These finite timings are NOT machine asymptotic bounds.

Distinct logical proof work is lower bounded as above; NO upper proof in historical Rmix341 is claimed. Offline Gaussian witness search costs polynomial time (naive dense O(h^3) per witness, O(h^4) for all O(h) witnesses), O(h²) simultaneously held dense-matrix bits and O(h²) total witness bits before object/serialization overhead; the provided Python raw fixture is 192,974 UTF-8 bytes for the tested cases. K4 exhaustive host work is 3*2^18 input masks with pruning and no use as an oracle in an actual SAT algorithm. Build/parser/source/authentication, all code setup, traversals, failed assignments, memory retention, output/readback and host runtime are separate charges, not hidden in W_R. No same-machine FLMV inference is made.

**Historical Rmix341 status:** Its /341 prose declares RES, AND3, GF(2), LOCAL-CONVERT all at most binary-premise and positive unit weights; the **complete authoritative native byte grammar and accepted checker** remain unverified, so application to that exact system is conditional. No new rules or weights introduced. No branched inference/discharge is silently added.

**TRACKER CHANGE:** New [P2-L1-523] is material source-essentiality classification and restricted linear mixed-arity control. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. proof1 unchanged. Do not promote this result or LSPV-3/520's existing restricted Pang-hard strict3 family to a P-versus-NP solution. Precise remaining mathematical task is an invariant surviving all legal mixed shortcuts plus an INDEPENDENT noncircular same-R B3.

## Publication and protected manuscript
Publish this role-owned report, executable JS, small raw summary, five-role handoff and SHA-guarded proof2 update. Root main.tex fetch returned zero content bytes despite blob 87081775f78ee61032a55abc8ffce806bedff245; leave it unchanged rather than overwrite unreadable material. Never edit other owners' regions, identities, schedules, tasks or native weights. Report all actual write/readback failures rather than claiming success.

## References
1. Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 Oct 2026), Theorems 1.1, 7.2(b): https://arxiv.org/html/2610.00837v2 .
2. Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979): proof-system qualification.
3. LSPV-3/520, source-core construction and restricted lower-bound monotonicity: research/agents/lspv-3/2026-11-08_1925_LSPV3_MOD3_21CLAUSE_STRICT3_PORT520.md .
4. LSPV-1/522, local 18-node exact Resolution packet: research/agents/lspv-1/2026-11-08_1900_LSPV1_MOD3_VERTEX_LOCAL_SOURCE_RES522.md .
