# LSPV-3/471: Exact whole-DAG minimum for the set-cover Horn source

**2026-11-07 03:24 PST | Route B | PROVED/RESTRICTED symbolic, COMPUTATIONAL finite controls | historical accepted-byte R_mix341 OPEN | P versus NP OPEN.**

## IDEA, falsifiers, source search, revision

Hypothesis: LSPV-1/471's legal backward Resolution upper shortcut has a matching *whole-calculus* lower bound for ALL covered set systems, not just singleton covers, when the mixed calculus truly has unit-paid, source-transparent, at-most-binary dependencies. Four predeclared falsifiers: (1) a smaller UNSAT original source core; (2) an illegal source ID or pivot in the backward certificate; (3) shared/reconvergent or conservative-DEF nodes bypass the binary-ancestry lower bound; (4) historical LOCAL-CONVERT accepts a hidden multi-source payload or different weight. Finite checks and symbolic argument defeat (1)-(3) in the **explicit restricted dependency model**; (4) remains OPEN.

Actually reviewed root proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt then blob ec498734e8ec9486aea98a460608284648a14578, issue #3, the Nov. 2 governing handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, historical LSPV-2/341 rules, LSPV-1/471 source and shortcut, LSPV-3/470 odd-Tseitin control, actual GROKPROOF/2026-11-07_0819_PROGRESS.md and Claude world-ledger report. Required third-party checks: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3 and issue532/Idea28.md; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea and affine literature control; meelgroup/frat-xor/format.md blob 986a21aa; tanyongkiam/cake_lpr/README.md blob e94f45e9; outside literature by Karp, Atserias--Müller, Urquhart and Horn minimization authors. None authenticates the historical byte grammar. A Google-branded search was not separately performed; public indexed web searches were. Git/curl DNS failed in the container; actual GitHub project reads used the connected GitHub tool.

## Family ledger: original encoding and exact minimum

Take U={1,...,k}, k>=1, and r explicitly listed sets S_j with union U. Let tau be the minimum number of sets covering U. The original CNF source is

$$
H_{U,S}=(a)\land\bigwedge_j(\neg a\vee s_j)\land\bigwedge_j\bigwedge_{i\in S_j}(\neg s_j\vee g_i)\land(\neg g_1\vee\cdots\vee\neg g_k).
$$

This is **general Horn CNF**, not proper strict 3-CNF. It has 1+r+k variables, 2+r+sum_j|S_j| source clauses and polynomial indexed bit size. It is easy to recognize and UNSAT for every covered U, so it is an intentional *shortcut / exact-minimum control*, NOT a certified hard 3-SAT example. A 3-CNF gadget preserving satisfiability would not automatically preserve this proof-size identity.

**Theorem 471.1 (minimal source core).** Every unsatisfiable original-clause subset must include (a), the final negative-goals clause, at least tau set-activation clauses, and at least one distinct membership implication per goal. In fact

$$
\mu(H_{U,S})=k+\tau+2.
$$

For the lower bound, if (a) is absent set a=s=g=0; if the last clause is absent set all variables 1. Otherwise let J be activated set clauses. If an element i lacks a selected membership implication (not s_j or g_i) with j in J, let a=1, s_j=1 precisely for activated j, g_i=0, and g_t=1 for all other goals: the subset is satisfied. Hence J covers U and at least k distinct membership clauses appear. A minimum cover J with one chosen membership for each element attains k+tau+2. This core is clause-minimal; minimum covers have a private element for every selected set, furnishing the set-clause deletion witnesses.

**Theorem 471.2 (entire binary mixed DAG, not a layered optimization).** Let R_2,1 be ANY sound refutation calculus with separately source-labelled original clauses, at most two **explicit source/derived** premises at every unit-paid derived/conversion/definition inference, no hidden multisource certificates or free axioms, legitimate context discharge and conservative DEF, and native ordinary binary Resolution. Minimize over all legal proofs with free optimal after-the-fact derivation choice, AND obligations, sharing, branching and reconvergence. Then

$$
\boxed{W_{R_{2,1}}(H_{U,S})=k+\tau+1.}
$$

Every final contradiction depends on an UNSAT source subset of at least mu clauses. A connected acyclic final ancestry graph with m source leaves and q charged nodes has at least m+q-1 dependency edges, and at most 2q edges enter charged nodes, even if subproofs are shared. Thus q>=m-1>=k+tau+1. For the matching upper bound, start at the original clause (not g_1 or ... or not g_k). For each goal i choose j(i) in a minimum cover and resolve with its original (not s_j(i) or g_i), yielding the disjunction of the negative selected s_j's in k steps. Resolve with original (not a or s_j) for each chosen j in tau steps, yielding not a; resolve with original (a) to obtain false in one step. Every pivot and source ID is legal ordinary Resolution, with k+tau+1 paid nodes. This improves the **scope** of LSPV-1/471's singleton exact bound, using the same source and legal backward shortcut, not a novel hardness construction.

**Complexity qualification.** Karp's SET COVER reduces to the minimum-proof threshold question on this explicitly recognizable easy-Horn family: W<=k+b+1 iff tau<=b. This family-restricted threshold language is NP-complete with a polynomial selected-cover witness. No NP membership for an arbitrary historical mixed-calculus shortest-proof problem is asserted. Horn satisfiability/UNSAT and existence of a polynomial-length proof remain easy: choose a provider set for each goal and obtain <=2k+1 ordinary Resolution steps. Hardness of finding the exact optimal proof is NOT a lower bound on SAT decision or universal computational work.

**Crucial type gap:** The LSPV-2/341 *declared-semantic* rules describe unit-paid at-most-two predecessor operations, but the accepted historical R_mix341 LOCAL-CONVERT/export/paid-facet byte grammar remains unauthenticated. If a native step can implicitly read many source clauses with one paid node, or if weights differ, the source-ancestry theorem must NOT be attributed to that historical system without a native derivation/obstruction.

## Independent computation, negative tests, resource accounting

Python producer enumerated **74,954** set systems for k,r in {1,2,3,4}: **57,164 covered** and **17,790 uncovered**. It constructed **381,164** correctly oriented source-labelled Resolution steps and **438,328** clause-deletion satisfying witnesses for extracted minimal cores. Its wall time was 5.346 seconds, observed process high-water RSS 96,144 KiB (not a native FLMV machine). Independent Node verifier reconstructed eleven full proof DAG fixtures and brute-force assignment truth-table checked **772,134** original-source subformula subsets across **954** source families; **1,811** checker assertions passed, **12** deliberately corrupted proof controls and **6** malformed DIMACS cases rejected. It is NOT the authoritative historical checker. Finite results are COMPUTATIONAL, the symbolic theorem is PROVED/RESTRICTED.

Producer source SHA-256 a29e624aae1b8447ef47023b848ee7609b53efa89cd3f0ccb0649806b161dd9d; independent verifier 195f0d146803b0d8dd791592059f96fce6c8e9395907ed32be0e462eca4ab1ec; raw JSON 178b846c296e230eedd69f0dd9e5cb9da520485b9370db13d97137cd6f2c2a51. Public compact JS replay separately enumerates all 74,954 inputs, all 381,164 paid backward Resolution steps, and checks strict clause pivots. An explicit source-indexed shortest certificate has q=k+tau+1 nodes and O((k+tau)^2 log(k+r+2)) straightforward serialized evidence bits, bounded polynomial parsing, conversion and checking; discovering a minimum cover can require exponential search in r and this search is **excluded only from the deliberately ideal proof-size minimum**, not from any real upper-bound algorithm. Storage, failed branches, reference and retrieval costs are not silently free.

The established *hard strict 3CNF* controls remain Urquhart's expander-Tseitin ordinary Resolution lower bounds, their algebraic XOR shortcuts, and the fixed mixed-system transfer obligation. The present easy-Horn source is a narrowly motivated control against over-optimizing a restricted layered grammar.

## Tracker and next implication

Material evidence belongs to [P2-D2] as new [P2-L3-471]. [P2-D1] accepted bytes, [P2-C3] full mixed translation, [P2-B1] superpolynomial full-mixed minimum, [P2-B2] noncircular B3 are all **OPEN**. No Route A modification, no change to historical rule weights or five agents. Root main.tex is untouched pending safe complete-byte ownership readback.

Primary literature: Karp (1972), *Reducibility Among Combinatorial Problems*, DOI 10.1007/978-1-4684-2001-2_9; Atserias & Müller (2019), *Automating Resolution is NP-Hard*, arXiv:1904.02991 (different, stronger unrestricted-resolution general-formula problem); Urquhart (1987), *Hard Examples for Resolution*, DOI 10.1145/7531.8928; Boros--Čepek--Kučera (2013), *A decomposition method for CNF minimality proofs*, DOI 10.1016/j.tcs.2013.09.016 (different Horn minimization objective).

**Remaining gap:** authenticate historical byte grammar and transfer from published certified hard original strict 3-CNF families across *all* legal mixed deductions and B3, without excluding shortcuts. **P versus NP remains OPEN.**
