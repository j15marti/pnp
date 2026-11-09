# LSPV-3/543: Exact minimal signed-CNF facets for every two-input conservative DEF gate

**2026-11-09 15:24 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Tracker:** proposed [P2-L3-543], refining [P2-L3-542], [P2-L3-541] and the OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. No historical inference weights, roles, calendars, or automation configurations changed.

## IDEA: candidate and falsifiers

Candidate: extend the earlier parity-only owner/facet audit to *every* arbitrary two-input total Boolean function permitted semantically by the original /341 DEF declaration. Construct an exact, locally checker-readable, conservative owner-to-signed-facets representation with the smallest number of direct CNF clauses and no additional logical charges for multiple facets. Historical accepted-byte legality is NOT presumed.

Registered falsifiers:

1. Some binary total Boolean gate needs more than four direct signed clauses, or has a different minimum than 1, 2, 3 or 4.
2. Minimal facet sets lack the exact total functional extension property when gates are nested, reconvergent and shared.
3. A forgotten facet can be omitted without admitting an incorrect (input,output) row.
4. A selector referring to another owner, a reused output, incompatible assumption contexts, an incorrect signed pivot, or a malformed original source passes the DECLARED typed audit. The audit is not the historical checker.

## SEARCH: authenticated materials and method adjustment

Read both root trackers, proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2 preflight blob 14bb30384bb88ab4d26dc0c1bb2f8a1d155786e0; the governing 2026-11-09 abstract-negative handoff blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b; issue #3 and its peer updates including LSPV-1/546, LSPV-5/469 and LSPV-2/528; AGENTS.md blob 4ae902888754d0b06ba4ce1aaeca0657a92b46a9, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef and .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f. Prior LSPV-3/537/539/540/541/542 and LSPV-5/450 were reviewed for duplicates.

The historical original semantic declaration is research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb). Its RES, AND3, XOR, LOCAL-CONVERT and DEF rules include total fresh two-input gates and unit logical cost; **the accepted byte productions and owner-to-facet references remain missing**. The recovered experiments/arc/lspv2_341_independent_verify.js (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0) dispatches only AND3/XOR. No missing native rule was invented.

Read actual GROKPROOF/2026-11-09_2015_PROGRESS.md (blob 5610d47e2a78ded4e4e57bc24fca3266e03f42ac) and Claude research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (blob b7150bb9ed964affd5fb90ecd24b0aa35d600bf9); neither authenticates DEF/LOCAL-CONVERT. New repository change-aware pins: konard/p-vs-np scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5). Proof-format control: meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), which explicitly disclaims native RAT support and records independent XOR checking; tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c), a distinct formally derived checker; openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae), which explicitly warns manuscripts have different verification status. None authenticates /341.

Primary methods: Cousot & Cousot, POPL 1977 (https://cs.nyu.edu/~pcousot/COUSOTpapers/POPL77.shtml); D'Silva/Haller/Kroening, Abstract Satisfaction, POPL 2014 (DOI 10.1145/2535838.2535868); Clarke et al., CEGAR, JACM 2003; Giacobazzi/Ranzato/Scozzari JACM 2000; Pommerening/Helmert/Bonet ICAPS 2017 (DOI 10.1609/icaps.v27i1.13806); Urquhart, Hard Examples for Resolution, JACM 1987 (DOI 10.1145/7531.8928). Their stated scope is abstract semantics, planning cost partitioning or restricted Resolution, not mixed proof hardness. An external Google-branded search interface was not available; web search and direct GitHub source inspection were used.

## ITERATE: theorem 543.1, precise facet minimum

Fix distinct Boolean inputs x,y and fresh output z. For each of the 16 functions f:{0,1}^2->{0,1}, let G_f be the four-element graph {(x,y,z): z=f(x,y)}. Define m(f) as the fewest non-tautological clauses using **only x,y,z** whose conjunction is exactly G_f (no extra auxiliaries).

**Theorem 543.1 (PROVED/RESTRICTED; standard local CNF combinatorics).**

$$
m(f)=\begin{cases}
1 & \text{if f is one of the 2 constants},\\
2 & \text{if f is one of 4 signed input projections},\\
3 & \text{if f is one of 8 signed-AND/OR gates},\\
4 & \text{if f is XOR or XNOR}.
\end{cases}
$$

**Proof.** Let B_f be the four wrong-output vertices of the Boolean 3-cube. Each clause sound under G_f excludes a Boolean subcube contained in B_f; conversely, every such subcube corresponds to an allowed implicate. Constants: B_f is a two-dimensional face, so one literal covers it. Signed projections: B_f is two disjoint cube edges, so two binary clauses suffice and one cannot cover its disconnected set. Signed-AND/OR gates: B_f consists of two edges with a common vertex plus one isolated vertex; every allowed non-singleton clause covers an edge, and its two possible edges overlap. Two clauses cannot cover four vertices, whereas the standard signed three-clause gate definition does. XOR/XNOR: all pairs of B_f vertices have Hamming distance two, so no allowed implicate covers more than one wrong vertex; four complete 3-literal clauses are necessary and sufficient. These four classes exhaust 2+4+8+2=16 functions. QED.

The four full-width tuple-exclusion clauses are a universal *non-minimal* normal form of every gate. Optimizing direct CNF can shorten physical facet lists to the stated m(f). Both representations denote the same deterministic conservative gate, but converting one into the other is NOT automatically an uncharged historical inference.

## Theorem 543.2: source retraction for nested shared DEF circuits

For any original CNF F(X) and any finite acyclic circuit of d fresh output wires z_1,...,z_d, where gate z_i=f_i(u_i,v_i) uses prior original or already-defined wires and any of 16 total binary gate tables, let D be the conjunction of each gate's exact minimal signed-CNF facets.

Then

$$
\forall a\in\{0,1\}^X,\quad
\#\{b:(a,b)\models D\}=1;
\qquad
\exists Z\,[F(X)\land D(X,Z)]\ \equiv\ F(X).
$$

**Proof.** Fix a primary input assignment a. Gate 1's exact clauses fix z_1 uniquely to its table f_1; inductively, gate i is fixed by its already-valued parents. Sharing and reconvergence merely reuse previous values; acyclicity ensures no circular dependency. Therefore exactly one extension exists. Since F does not mention fresh Z, existential elimination returns precisely F. QED.

This supplies a *source-retracting semantic transformer* for the declared binary-gate DEF fragment. A typed audit can record (original source ID, wire scope, immutable fresh output, table, owning paid DEF node, facet selector, signed clause, branch context). One DEF owner is charged once, even if several facets are consumed. This remains a **proposed typed audit**; no historical accepted-byte DEF record has been authenticated. Full rule-by-rule cost-sound overapproximation, including LOCAL-CONVERT and branching/discharge, is still OPEN.

For any original-variable clause C derived soundly under F and these definitions with **fully discharged** assumptions, the theorem implies F entails C. Without discharge, only the scoped claim F and Gamma entail C is justified. The global shared proof DAG and paid origin union cannot be replaced by independent marginal counts; see LSPV-5/469.

## Concrete replay and CEGAR controls

Published independent JavaScript implementation: experiments/arc/lspv3_543_all_binary_gate_facet_minimality.cjs (blob c80081724c56554f31e8933c7f31af060453e456). It enumerates all 26 nonempty three-variable signed clause patterns, filters those entailed by each gate, computes the exact minimum covering the four wrong tuples by dynamic programming, checks semantic equivalence and indispensability, and separately checks four nested shared gates and two original strict3 K4 Tseitin controls. Its raw result is results/raw/arc/2026-11-09_1524_LSPV3_543_BINARY_GATE_FACETS_RAW.json (blob 5457b1457bfe2d6095ee7461ea1558adbb7395f1), 218 assertions, 7 explicitly rejected wrong typed packet controls. Those packet checks are **not** the historical checker.

An independently implemented Python model in the current-run fallback tested all sixteen gates through a different signed-clause implementation: 264 assertions, 8 nested original-input assignments with exactly one extension each; K4 odd charge had 16 proper strict3 source clauses, 0 models and 0 expanded models; even charge had 8 models and 8 expanded models. Python elapsed about 0.0036 seconds and observed process max RSS 96,264 KiB; host initialization dominates this RSS. No random seeds. Python also rejected three malformed proper-source clause encodings. A typed RES example for original unit sources x,y and paid z=x AND y has one paid DEF and two paid RES (three distinct paid nodes) and cannot borrow facet syntax from a different owner.

No original K4 lower bound is claimed: K4 is a finite XOR shortcut control. For published asymptotic expander-based Resolution hardness, see Urquhart 1987. The declared mixed AND3/GF(2) proof uses the known 4h-1 paid-node Tseitin construction; this cheap upper bound is mandatory, not excluded.

## Cost ledger and limitations

For a circuit with d gates the explicit direct CNF has sum_i m(f_i) clauses, between d and 4d, each at most three signed literals. A proposed owner-indexed format has d paid DEF nodes, not sum_i m(f_i) paid nodes; facets are views of their owner *only when the interface authenticates them*. Bit size depends on the entire canonical variable/owner identifier lengths, at most O(d L) under maximum identifier bit length L and constant-size gate symbols, not O(d) for arbitrary-precision identifiers. The exhibited unit-source typed RES example has three distinct paid nodes; logical critical path is three under unit-depth sequential dependency. The 16-gate finite DP is an *offline test*, not a zero-cost native inference.

Actual production and checking require source parsing, owner/facet indexing, ID validation, gate table evaluation, memory allocation, JSON serialization, evidence output, retrieval and failed-attempt work. No benchmark here measures all these phases or certifies a same-machine FLMV exponent; GitHub reads and write operations and independent JS V8 execution are separate from Python timing/RSS. Logical node count, explicit evidence bits, real work, parallel span and simultaneous peak space are not identified.

An abstraction that drops even one necessary gate clause is a MAY overapproximation: it retains every valid extension and adds wrong extensions. This is sound for reachability overapproximation but cannot justify a new exact Resolution premise. CEGAR must restore the owner-bound facet and context before treating the path as concrete. A known cheap affine Tseitin shortcut invalidates any lower-bound relaxation that discards GF(2) or treats DEF facets as separately paid.

## Remaining gaps and publication boundaries

[P2-D1] OPEN: historical accepted-byte DEF owner/facet selectors, RES/AND3 parent views, LOCAL-CONVERT/private/exported ports, branching/discharge and correct weights.

[P2-C3] OPEN: full same-R all-rule source-authenticated, nonexpanding-cost abstract transformer and proof-to-proof normalization. This run proves only the **semantic typed DEF interface** and an exact local CNF facet optimizer.

[P2-B1] OPEN: representation-invariant superpolynomial Wbar_R across every mixed proof rule.

[P2-B2] OPEN: noncircular B3 and same-R computational transfer.

**Next falsifier:** locate one authenticated native DEF-owner/facet->RES accepted-byte trace, or exhibit two historical-prose-consistent grammars that disagree on its legality; replay concrete source scope with a truly native checker. Do not replace the missing grammar by the typed checker from this run.

P versus NP remains OPEN.
