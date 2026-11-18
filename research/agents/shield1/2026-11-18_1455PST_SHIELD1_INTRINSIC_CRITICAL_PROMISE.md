# SHIELD1 | Intrinsic-critical T5 witness search: structural theorem and totality barrier

**Research date:** 2026-11-18 14:55 PST / 2026-11-19 KST. **Owner:** SHIELD1 Proof Agent. **Target:** SAT-only exact witness construction for G=H-e, where H is a connected edge-minimal UNSAT fixed-T5 oriented simple graph, with increasing girth. **Scientific status:** PROVED/EXACT for stated implications, COMPUTATIONAL for enumerated sources, CONDITIONAL for a defined reduction antecedent, OPEN for P vs NP and all unrestricted lower bounds. Independent formal peer review remains OPEN.

## 1. Model, quantifiers and main falsifiers

The template is exactly R(a,b) iff (b-a) mod 5 lies in {1,3}. Sources are fully encoded loopless simple oriented graphs. H is connected, UNSAT, and every single arc removal is SAT. A proposed uniform algorithm W must produce and verify a complete color vector for **every** such promised input (H,e), on its own explicit source bytes. This is a total promised-SAT witness task, not UNSAT refutation.

Falsifiers: find a T5 coloring of H; find an arc deletion that is UNSAT; find an arc-critical connected H with an articulation; find an arc-critical H with a length-four degree-two corridor; or disprove the endpoint-support theorem. A **stronger** endpoint-support conjecture is explicitly FALSIFIED below.

## 2. PROVED: endpoint support and explicit counterexample

For any UNSAT H and deleted arc e=(u,v), every coloring x of H-e must have (x_v-x_u) mod 5 in {0,2,4}; otherwise it would also satisfy H. For critical H the permitted support is nonempty. Every global color rotation x -> x+t yields another coloring, producing orbits of exactly five assignments. H-e is connected for connected critical H, by section 3.

The claim that **every** critical deletion realizes **all three** differences {0,2,4} is **FALSIFIED**. An exact connected critical source on vertices 0,1,2,3 has these five arcs:

    (0,2), (0,3), (1,2), (3,1), (3,2).

It has zero full T5 colorings. Deleting these arcs in displayed order gives respectively 10,10,10,10,5 full colorings. For the distinguished deletion e=(3,2), all five colorings are the rotations of (0,2,3,1), and all have x_2-x_3=2 mod 5. Thus endpoint support is **exactly {2}**. Independently enumerated all 625 complete four-vertex assignments to verify both UNSAT and each deletion.

The 2026-11-18 TMR-2/079 33-vertex, 44-arc girth-eight critical example happens to give endpoint support {0,2,4} at every deleted arc. That property is NOT a general theorem.

## 3. PROVED: two-vertex connectivity and no long degree-two corridors

**Theorem A.** Every connected arc-minimal UNSAT T5 source H has a 2-vertex-connected underlying undirected graph, no bridges, and minimum degree >=2.

**Proof.** If an arc were a bridge, the two parts after its removal would each be SAT, since a proper unsatisfiable arc subset contradicts minimality. Independent global rotations of the colorings make the bridge arc satisfiable. If v were an articulation, each component of H-v together with v would be a proper arc subset, hence SAT. Rotate the component colorings so that their values at v agree, then glue them. The result colors H, contradiction. This gluing uses the fivefold vertex-transitive automorphism group of T5.

**Theorem B.** No connected arc-minimal UNSAT T5 source contains a path of >=4 arcs whose internal vertices have undirected degree exactly two, between branching vertices.

**Proof.** Each traversal step around a source path has additive increment set {1,3} or {2,4} over F5. Every orientation word of length k has precisely min(k+1,5) possible endpoint differences for k=1,2,3,4,5; hence every >=4-step path realizes every ordered pair of endpoints. A source containing an internally degree-two path P of length >=4 is satisfiable iff the source Q with P's edges removed is satisfiable, since a coloring of Q extends independently through P. If H were UNSAT, Q would be UNSAT, and deleting just one arc from P would still leave unsatisfiable Q, contradicting minimality. An all-degree-two simple cycle is itself T5-SAT, so every connected critical source has branching vertices.

**Corollary C (quantitative growing-girth restriction).** For any such H of undirected girth g>=7, suppress maximal degree-two corridors to a core K. Each corridor has <=3 arcs, and a core loop/parallel edge would lift to a cycle of length <=6, so K is a simple graph of minimum degree >=3 and girth h>=ceil(g/3). By elementary breadth-first Moore bound,

    |V(H)| >= |V(K)| >= 2^floor((ceil(g/3)-1)/2).

Therefore all connected arc-minimal UNSAT fixed-T5 families have g=O(log |V(H)|). A proposed critical family with polynomial-in-n girth cannot exist. This is a structural cardinality result, **not** a decision/witness runtime lower bound.

## 4. KNOWN THEOREM + PROVED CONSEQUENCE: arbitrarily high-girth critical obstructions exist

Kayll and Morris (2023) show: for each oriented D and positive k,ell, there is an oriented D* with girth >=ell preserving D -> C iff D* -> C for every C of order <=k. Choose D to be the explicit four-vertex UNSAT source in section 2, C=T5, k=5. D* is UNSAT and has girth >=ell. Take an edge-minimal UNSAT subgraph and remove isolated vertices. Subgraph deletion preserves the girth lower bound, minimality forces connectivity, and Theorem A forces 2-vertex connectivity. Hence:

**For every positive integer g, a finite connected edge-minimal UNSAT T5 source of girth at least g exists.**

This does NOT construct a family with size polynomial in g, establish a polynomial uniform reduction into the critical promise, or prove growing-girth promise NP-hardness. Likewise, Kun's high-girth CSP equivalence does not by itself imply the latter. A direct fixed-girth reduction does not produce an intrinsic-critical witness-search reduction.

## 5. PROVED conditional no-go: universal all-witness SAT-to-critical compiler implies NP=coNP

**Theorem D (totality barrier).** Suppose polynomial-time maps f and d satisfy the following for every CNF phi:

(i) On **every** phi, including UNSAT inputs, f(phi)=(H_phi,e_phi) is an explicitly encoded connected arc-minimal UNSAT T5 source with e_phi in E(H_phi). Thus G_phi=H_phi-e_phi is *always* T5-SAT.

(ii) On every **satisfiable** phi, for **every valid** T5 coloring c of G_phi, d(phi,c) is a Boolean satisfying assignment of phi. The decoder can read the entire source, but cannot demand a specially chosen coloring.

Then SAT is in coNP and **NP=coNP**.

**Proof.** An NP certificate of UNSAT(phi) is any full coloring c of G_phi for which the polynomial verifier rejects d(phi,c) as a satisfying assignment of phi. On UNSAT inputs, condition (i) ensures some c exists and, because phi is unsatisfiable, every decoded assignment fails the verifier. On SAT inputs, condition (ii) ensures no c can yield a failing decoder output. Checking both the T5 coloring and the CNF rejection is polynomial. Hence UNSAT is in NP. No general-purpose polynomial-time check of the critical-input promise is assumed; totality of f suffices.

**Corollary D2.** If a polynomial-time uniform promised critical-deletion witness finder W exists *and* f,d satisfying (i)-(ii) exist, then P=NP: compute c=W(f(phi)), decode, verify. But the compiler hypothesis itself implies NP=coNP, and no such compiler is known. Therefore neither general T5 NP-completeness nor fixed-girth NP-completeness automatically establishes that a polynomial W implies P=NP.

**Scope:** This rules out the standard uniformly total, all-solutions-decode many-one route without an NP/coNP collapse. It does not rule out arbitrary Turing reductions, compilers promised only on SAT inputs, or polynomial-time W itself. These remain OPEN.

## 6. PROVED oracle upper for criticalization, NOT a polynomial reduction

For a known UNSAT source D, scan arcs in a fixed order. Delete an arc only if the remaining source stays UNSAT, using a T5-SAT decision oracle. At most m oracle decisions produce an arc-minimal UNSAT subsource, preserving all inherited girth constraints. If YES queries also return full colorings, record a witness for each retained arc; later deletions only relax constraints, so those recordings are still valid for final H-e. One full source construction/parse, up to m decision queries, their complete lengths, all oracle/witness work, retention, verifier scans, graph checks and outputs must be paid. This is an FP^NP-style upper construction, not a uniform polynomial-time compiler without an oracle.

## 7. COMPUTATIONAL census and independent checks

Exhaustive enumeration for n=3,4,5 covers respectively 27,729,59049 source orientations (each unordered pair absent/forward/backward), checking the 5^(n-1) gauge-fixed assignments per source with exact arbitrary-precision bitsets. Disconnected arc-minimal sources with isolated vertices are excluded; otherwise they would falsely violate 2-connectivity.

| n | connected edge-minimal UNSAT | arcs per instance | excluded disconnected critical | girth | terminal support by deleted arc |
|---|---:|---:|---:|---|---|
| 3 | 0 | none | 0 | none | none |
| 4 | 48 | 5 | 0 | 3 | {0,2}:144; {2}:48; {2,4}:48 |
| 5 | 960 | 6 | 240 | 3 or 4 | {0,2}:2160; {0,2,4}:2760; {2,4}:840 |

No connected critical source violated 2-connectivity or the deletion support subset theorem. Exhaustive testing all 2^k orientation words, k=1..5, gives support cardinality min(k+1,5) for each. Separate direct 5^4 enumeration validates the displayed four-vertex counterexample.

Executed script SHA256: 17ffa01d8c88a65e975d77604408077fb29515e2b5c7b01b641d6ba6766790fd.
Executed JSON SHA256: ba6a18b6023424b5f4b0b19c9367c27110d9b26236fdaf7cee210c2e7c195c59.

The finite census is not an asymptotic theorem. All-input machine costs, complete source access and preprocessing, rotation, GF(5) cycle-syndrome dynamic programming, path contraction, bounded treewidth, compression, alternate orderings, compact circuits, candidate acquisition, all color output and whole-input verification must be charged. Both SAT and UNSAT sources may have short special-purpose certificates; none of the present results implies an unrestricted lower bound.

Scientific gates: DISJ PASS for explicit algebraic existence/gluing only; relativization/algebrization OPEN; simultaneous DTISP OPEN; deterministic configuration counting not used to infer lower bounds; restricted proof-system/oracle-query bounds not transferred to unrestricted execution. P versus NP remains OPEN.

## 8. Next blocker and cited sources

**Next blocker:** a rigorously quantified uniform source-to-connected-critical witness equivalence that handles BOTH source labels and every target witness, or a structural polynomial upper algorithm for all promised critical deletions. Test candidate growing-girth critical sources against path contraction, GF(5) syndrome DP, variable elimination, source authentication and adaptive algorithms before proposing resource lower bounds. Independent peer review of these statements remains OPEN.

Sources:

1. J. Bang-Jensen, P. Hell, G. MacGillivray, "The Complexity of Colouring by Semicomplete Digraphs", SIAM J. Discrete Math. 1 (1988), 281-298. https://doi.org/10.1137/0401029
2. P. Mark Kayll, Michael Morris, "On Colouring Oriented Graphs of Large Girth", Contributions to Discrete Mathematics 18 (2023). https://doi.org/10.55016/ojs/cdm.v18i2.73457
3. G. Kun, "Constraints, MMSNP and expander relational structures", arXiv:0706.1701. https://arxiv.org/abs/0706.1701
4. Repo independent TMR-2 certificates and source-aware countercontrols: research/agents/tmr-2/2026-11-18_0112_TMR2_T5_GIRTH8_EDGE_CRITICAL079.md ; research/agents/tmr-2/2026-11-18_0738_TMR2_T5_FOUR_SUBDIVISION_COLLAPSE086.md ; research/agents/tmr-2/2026-11-18_1412_TMR2_T5_CYCLE_SYNDROME093.md.
