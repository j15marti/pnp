# LSPV-1/544: shared-DAG obligation-cover abstraction and an exact additive-potential ceiling

**2026-11-09 13:41 PST | Route B lead | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Tracker scope:** candidate [P2-L1-544], refining [P2-L1-543], [P2-L5-467], [P2-L3-541] and the still OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. No historical native grammar, weights, roles or allocations changed.

## IDEA and falsifiers

**Candidate.** Replace the partition-only arbitrary MAY merges in LSPV-1/543 by an *overlapping proof-obligation coverage* abstraction with whole-DAG first-use charges. Obtain a concrete rule-conditional cost-sound potential from a nonnegative weighted cover dual. Test whether these additive potentials can certify the exact abstract minimum even when every action's footprint is known.

F1. A collection of fewer than n-1 unit-paid vertex sponsors covers every edge obligation of K_n. **FALSIFIED symbolically.**

F2. Some nonnegative *additive obligation potential* for K_n satisfies the unit per-sponsor increment inequality and reaches a goal value > n/2. **FALSIFIED symbolically.**

F3. Authenticated historical R_mix341 has a legal node, zero-cost side read or auxiliary/branch use whose *complete future-effect footprint* is absent from the proposed action catalog. **OPEN; such a witness invalidates any application to R_mix341, not the declared abstract theorem.**

F4. Independently reused shared paid origins or incompatible branch contexts can invalidate the abstract charge-once soundness if the actual abstract mapping does not preserve global origin identity and already-paid capabilities. **A mandatory adversarial obligation; no native historical execution was performed.**

## SEARCH: continuity and source status

Read complete proof1.txt, blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; complete proof2.txt, startup blob ccccc1339debef6e72ffa370a9c6d3a78f9b0981 (817,698 characters); current issue #3 with LSPV-3/541 and LSPV-1/543 comments; AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md and the governing November 9 abstract-interpretation handoff blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b. Original R_mix341 semantic declaration LSPV-2/341 blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb was read directly. Peer LSPV-3/541 signed DEF-facet/pivot polarity and LSPV-5/467 global sponsor-flow Hall certificate were read, as were LSPV-2/527, the current GROKPROOF/2026-11-09_2015_PROGRESS.md and Claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (the latter is a distinct machine/portfolio barrier, not a shared proof-lower-bound result).

The immediately preceding LSPV-1/543 report (blob c91713012b82676a2e6161102c244e98de2ccd02) proves the exact **source partition** knapsack ceiling. This report does **not** re-label that theorem. It gives a separate overlapping-obligation dual and proves an exact gap between additive potentials and the genuine optimum of a declared shared AND/OR cover system.

Targeted required repository reads: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-model theorem statuses); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (bounded method claims only); meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (EXTERNAL typed XOR format); tanyongkiam/cake_lpr README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c (checker and toolchain boundary); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (original charge/graph generator); openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (varied proof-verification status). No checked repository supplies historical R_mix341 full grammar or B3.

Primary background: Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973, for MAY simulation; Pommerening, Helmert, Bonet, ICAPS 2017, DOI 10.1609/icaps.v27i1.13806, for cost partitioning and LP duals in planning; standard LP cover primal/dual is independently derived below; Urquhart, JACM 1987, DOI 10.1145/7531.8928, for *ordinary Resolution* expander-Tseitin lower bounds. Indexed web queries were used, not a distinct branded Google interface. Sources are NOT permission to import their rules into historical R_mix341.

## 544.1 A rule-conditional sound MAY abstraction with first-use sharing

Fix the original externally authenticated CNF F and complete proof configuration
C=(F,DAG,Contexts,DefinitionOwners,Freshness,Provenance,PaidIDs,NativeCost).
DAG is a finite acyclic hypergraph of source and derived occurrences, with OR derivation alternatives and AND premise obligations. Contexts contain assumptions and valid discharge evidence; source identity includes exact signed clause IDs; a paid inference's globally unique occurrence ID costs exactly once. The concrete transition relation is the unknown fully authenticated fixed R_mix341 rule relation, *not* a set of rule inventions here.

Let U be a finite set of abstract proof obligations **not already discharged by free original-source access**, and for each concrete paid occurrence o let S(o) subseteq U be a conservative upper bound on ALL obligations whose discharge can ever be enabled by the node, including future legal reuse, contexts, defining facets and source-side reads. For sound use one must prove:

(A) every concrete complete refutation has U contained in the union of S(o) over DISTINCT paid occurrences o;

(B) every legal historical occurrence type maps to an admitted abstract cover action A superset S(o), with abstract nonnegative first-use charge c(A) <= the actual native weight w_R(o); and

(C) free transitions, reused paid origins, source lookups and zero-charge closure are either already represented by the initial covered set or have their own admitted zero-price effects. In particular a previously paid node reused in another branch is NOT paid again.

Abstract state is (D,H), where D subseteq U is the union of advertised capabilities already paid for, and H records paid abstract origin identities. A MAY action with advertised A advances D to D union A, and the charge for a fresh paid occurrence is c(A). A reused origin stutters at zero logical *new-node* charge, with all future capabilities conservatively preadvertised at first use. A goal is D=U (it is permitted to include spurious goals). Every actual proof path thus maps to an abstract path of no greater distinct-node cost; a concrete goal maps to an abstract goal. Hence d# <= W_R(F). Missing historical rule footprints must be represented conservatively, potentially by an action covering ALL U at zero price; no positive invariant may be asserted in that case.

For nonnegative rational obligation weights y_u satisfying, for **EVERY admitted fresh abstract action A**,

$$
\sum_{u\in A}y_u\le c(A),
$$

define V(D)=sum_(u in D)y_u. A legal abstract action raises V by at most c(A), while V(empty)=0 and V(U)=sum_u y_u. Therefore

$$
\boxed{W_R(F)\ \ge\ d^\#\ \ge\ \sum_{u\in U}y_u}
$$

**only when** A-C and all action-price inequalities have been independently established. This is a concrete conditional proof-system bound, not a successful full-R_mix341 verification. A zero-cost action covering a positive-weight u forces y_u=0. Unknown original grammar therefore prevents promoting the bound.

## 544.2 Parameterized EXACT ceiling for additive obligation potentials

Define a DISTINCT finite abstract AND/OR cover calculus T_n for each n>=3. There is one obligation u_{ij} for each unordered edge {i,j} of K_n. For each vertex i there is one optional globally paid unit-cost sponsor a_i. It makes ALL incident obligations u_{ij} available. Each required edge is an OR obligation (covered by a_i OR a_j); the goal is AND over all edges. A selected sponsor may be reused for arbitrarily many edge obligations, for free, and is counted once; paid occurrence IDs remain distinct. The source/goal are abstract objects, not CNF and not R_mix341.

**Exact optimum.** Choosing vertices X covers every edge iff the complement [n]\X contains no edge. Since K_n is complete, this holds iff |X|>=n-1. Hence

$$
\boxed{W_{T_n}=n-1.}
$$

**Sharp additive-potential ceiling.** Any nonnegative weights y_{ij} yielding a sound additive transition potential must satisfy sum_(j != i) y_{ij}<=1 for each sponsor i. Sum all n inequalities: every y_{ij} appears twice, so 2 sum_(i<j)y_{ij}<=n. Choosing y_{ij}=1/(n-1) saturates every vertex constraint. Thus

$$
\boxed{\max_{y\ge0}\sum_{i<j}y_{ij}=n/2,\qquad W_{T_n}=n-1.}
$$

The gap is (n-1)/(n/2)=2-2/n, approaching 2. At n=3 the true minimum is 2, but every *additive* obligation potential is bounded by 3/2. No search failure or theorem about actual SAT computation is inferred. The strongest additive dual is a safe but incomplete lower-bound certificate even when every abstract rule's coverage is exact. An exact symbolic cover-state search or nonadditive strengthening can recover n-1.

This is an application of familiar weighted-cover LP duality to explicitly charged shared AND/OR proof abstractions. No claim of originality for the combinatorial vertex-cover / LP result is made. The project-specific relevance is that **complete rule footprints alone do not make a linear additive potential exact**. This addresses a distinct obstacle from the source-partition ceiling of [P2-L1-543] and the sponsor feasibility certificate of [P2-L5-467]. The latter verifies accounting for a GIVEN proposed abstract image; the present theorem limits what a particular FAMILY of potentials can prove even with correct accounting.

## Established hard-source and hostile-shortcut ledger

Odd-charge Tseitin 3-CNF on a connected cubic expander G_h: n=3h/2 edge variables; m=4h proper signed width-three clauses (four forbidden wrong-parity assignments per degree-three vertex); encoded length O(h log(h+2)) under standard indexed encoding. Urquhart's exponentiation is for ordinary shared-DAG Resolution on appropriate expander families, not for R_mix341. The **declared** /341 AND3+GF(2) construction refutes this formula in exactly 4h-1 paid nodes; even-charge counterparts are SAT. The clique T_n sponsor witnesses here are abstract optimization controls ONLY and are not claimed expander-hard SAT instances. Any proposed obligation family for Tseitin must admit the inexpensive XOR shortcut, or its claimed rule coverage is false.

Remaining hard-family target: exact bit-PHP or other published proof-hard family and exact three-CNF encoding plus explicit proof-hardness-preserving simulation. Cook ER, local GF(2), conservative extensions, shared reconvergence, and signed DEF facets are mandatory adversarial covers in any proposed catalog. A missing action with larger obligation support or lower first-use cost invalidates the dual constraints; do not omit that action to force hardness.

## Independent finite control and resource ledger

The independent Python verifier exhausts every subset of n sponsor IDs for n=3,...,9, checks exact AND goal satisfaction, distinct paid-node cost, all n*2^n transition potential increments using Fraction arithmetic, and the uniform dual witness. Totals: 1,016 subsets and 8,184 first-use/reuse transition checks, no random seeds. Exact measured integer minima n-1 and additive maxima n/2 in all seven sizes. Duplicate paid-node reuse is charged zero in transitions; a missing edge obligation prevents goal completion. These test an explicit FINITE ABSTRACT CALCULUS, not historical checker acceptance, both-label general SAT, malicious DIMACS, an arbitrary machine, or any nontrivial proof-family lower bound.

Logical work in T_n is n-1 unit sponsor nodes; the abstract universe has binomial(n,2) obligations. Full enumeration is O(n 2^n) transitions with O(n^2) obligation bits per abstract state; the program is an auditor, not a polynomial SAT decider. Python and JSON byte counts, serialization, source/branch reads, parser, goal verification, construction, caching, output and actual peak RSS are separate machine costs; no physical SAT runtime or peak-space claim is made. Host peak RSS and the native R_mix341 checker were not measured/executed.

## Reconciliation, status, and next implication

**PROVED/RESTRICTED:** exact T_n shared AND/OR cover optimum and exact ceiling of every nonnegative additive-obligation potential; general A-C conditional soundness and dual lemma. **COMPUTATIONAL:** independent exhaustive n<=9 controls. **OPEN:** certify a *source-exact* nontrivial obligation set and exhaustive valid footprints for ALL historical R_mix341 native RES, AND3, XOR, DEF, LOCAL-CONVERT, branch and source-side-read rules. Until then the putative general dual bound gives no positive R_mix341 lower bound. [P2-D1], [P2-C3], [P2-B1], [P2-B2] and same-R B3 remain OPEN. Route A's universal same-machine FLMV contraction remains OPEN. P versus NP OPEN.

Handoff for LSPV-3: propose a signed-clause/facet/context obligation catalog and provide an accepted native trace for every action; include cheap GF(2) and ER controls. Handoff for LSPV-5: audit U-coverage, universal action inequalities, each zero-cost/reuse effect and the gap between additive dual versus nonadditive abstract reachability. Do not change the five roles, schedules, R_mix341 weights or grammar.

**Actual advance:** a checkable first-use proof-obligation LP lower-bound interface plus a parameterized EXACT obstruction to completeness of additive potentials. **Validation:** symbolic proofs and 1,016 exhaustive states/8,184 transitions. **Publication:** see commit/readback receipts or state precise blocker. **Remaining gap:** original-source-authenticated all-rule action/obligation coverage and genuinely superpolynomial whole-calculus lower bound, plus noncircular B3. P versus NP remains OPEN.
