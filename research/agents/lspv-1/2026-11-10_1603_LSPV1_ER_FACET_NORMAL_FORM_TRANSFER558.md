# LSPV-1/558: All-input ER-normal-form to paid DEF/RES transfer, with an exact owner-facet probe

**November 10, 2026, 16:03 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED conditional calculus theorem + COMPUTATIONAL | P versus NP OPEN**

## IDEA and falsifiers registered before search

**Candidate.** An exact, *normal-form* Extended Resolution (ER) proof can be compiled **one paid node per extension plus one per Resolution inference** into the previously declared \`R_fac\` completion, provided that all three clauses defining one paid OR gate are available as owner-qualified Resolution premises at **zero additional paid-node cost**. This gives an all-input simulation statement and a precise accepted-byte interface test for [P2-D1], not a native result and not a superpolynomial lower bound.

Four falsifiers: (F1) historical native \`R_mix341\` does not expose owner-qualified DEF facets as RES clause parents; (F2) native costs charge one or more independent nodes per facet rather than a single DEF owner; (F3) a compiler uses a new original-source clause, an unowned facet, cyclic auxiliary, invalid pivot, or duplicated paid ID; (F4) a terminal empty clause is not derivable under the declared DEF/RES semantics. **F1 and F2 remain OPEN for the native byte language.** F3 and F4 are excluded for the 16-paid-node fixture by the independent verifier and eight hostile controls; the general theorem follows by syntactic induction under its explicit interface hypotheses.

## SEARCH: original source, nonduplication and primary literature

Read both full living trackers (root \`proof1.txt\`, \`proof2.txt\`), issue #3 with contemporary specialist reports, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, November 9 research handoffs, the original [LSPV-2/341 declaration](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex) (blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`) and recovered partial checker (blob \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\`). Also reviewed prior [LSPV-1/548](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-09_1600_LSPV1_BITPHP_UNARY_ER_SHORTCUT548.md), LSPV-3/436, /554, /555, LSPV-2/541, LSPV-4/527, LSPV-5/453, original Grok 2026-11-10 14:35 UTC and Claude WORLD-LEDGER-0001. The **facet accessibility gap and extension-proof idea are already identified in LSPV-1/548 and LSPV-3/436**. The contribution here is a precise universal normal-form quantifier, exact tariff-preserving proof compiler, and new independently executed fully owned-facet end-to-end example, not a claim of first discovering ER or the facet ambiguity.

Primary literature: Cook (1976), *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, DOI 10.1145/1008335.1008338; Cook–Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, DOI 10.2307/2273702; Cousot–Cousot (1977), *Abstract Interpretation*, DOI 10.1145/512950.512973; Krajíček (2025), *The Case of ER*, DOI 10.1017/9781009611664.009; Braun (2026), arXiv:2609.23015v2, for **Res(XOR) only**. Change-aware original external corpus files were read: \`konard/p-vs-np/scripts/proof_status.json\` blob \`93b77ed3d8fe456f81c690035f45f07910a247f2\` and \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` blob \`18d693ea71dfa433370eb7afbebc3106e32f03e5\`. Neither authenticates the historical \`R_mix341\` mixed-rule byte checker.

## Theorem 558.1: universal normal-form simulation (PROVED/RESTRICTED, conditional interface)

Fix original CNF $F$ in **one independently authenticated input encoding**. Let $\mathrm{ER}^{\lor}_2$ be the source-indexed, acyclic, shared-DAG refutation language whose only derived instructions are (i) introducing one globally fresh extension variable $z$ with $z\leftrightarrow(a\lor b)$, where $a,b$ are signed literals on distinct *previously existing* Boolean variables, and (ii) ordinary oriented binary Resolution. Each extension is represented by the three exact signed defining clauses

$$
(\neg z\lor a\lor b),\qquad(z\lor\neg a),\qquad(z\lor\neg b).
$$

Let $R_{\mathrm{fac}}$ be the **separate explicit semantic completion** with the exact same authenticated original SOURCE records, one unit-paid two-input DEF owner for each such gate, all three facets referenced only as owner-qualified views at no *additional* paid inference-node cost, and one unit-paid RES for each binary Resolution. Proof DAGs are arbitrary, with reused paid nodes counted once; neither calculus grants free CASE, semantic oracle, uncharged non-source axiom, source substitution, or disjoint-branch summation.

**Theorem.** For every original CNF $F$ and every finite valid topologically ordered $\mathrm{ER}^{\lor}_2$ refutation $\pi$ of $F$ having $e$ distinct extension introductions and $r$ distinct derived Resolution nodes, there is a uniform effective compiler $C$ such that

$$
C(F,\pi)\text{ is a valid }R_{\mathrm{fac}}\text{ refutation of the SAME }F,\qquad
W_{R_{\mathrm{fac}}}(C(F,\pi))=e+r.
$$

The compiler's explicit certificate is polynomial in the encoded original source and $\pi$ (with owner-qualified facet references and appropriately bounded canonical identifier encoding). Consequently,

$$
W_{R_{\mathrm{fac}}}(F)\le
\min_{\pi\text{ ER}^{\lor}_2\text{ refutation of }F}(e(\pi)+r(\pi)).
$$

**Proof.** Traverse $\pi$ topologically. Map every original SOURCE to its original unique source ID. At an extension instruction, introduce the same fresh $z$ with its already-defined signed inputs, allocate exactly one new globally unique charged DEF owner ID, and expose only its three indexed facets. Their conjunction is exactly $z\leftrightarrow(a\lor b)$, so every prior-variable model has a unique extension. At each RES instruction, translate both parent references (original source, earlier RES, or earlier DEF facet) and the same complementary pivot, recording one exact signed resolvent with a globally new paid node ID. By induction on the trace, every translated clause is justified and all shared predecessor references remain shared. The original ER empty clause becomes an empty-clause RES conclusion of the same source under the same conservative extensions. The map from paid ER instructions to paid target owners/nodes is bijective, hence $e+r$ and never the total number of facet references or proof paths. Parsing, emission and verification are distinct *actual computation* costs, not the logical paid tariff. QED.

**Conditional native implication.** If and only if further authoritative evidence demonstrates the necessary \`R_mix341\` source+DEF-owner-facet+RES accepted-byte interface with no extra inference charges, this *particular* compiler becomes a native upper-bound transfer. Then any proposed superpolynomial [P2-B1] mixed minimum on a family would imply a superpolynomial lower bound for its normal-form ER refutations. That is a strong additional proof-complexity obligation, **not a proof of impossibility** and not a statement about unrestricted algorithms. The recovered /341 fixture checker dispatches only AND3/XOR and currently cannot accept this certificate.

## ITERATE: exact fully owned-facet control

Use the genuine strict proper width-three UNSAT source $F_8$ containing all eight signed 3-clauses over $a,b,c$. All $2^3$ assignments were checked; zero satisfy $F_8$. Introduce ONE owner $z=a\lor b$, expose three owner facets, and produce the following for each $\sigma\in\{+c,-c\}$, using only exact binary RES:

1. From $(a\lor b\lor\sigma)$ and two DEF facets derive $(z\lor\sigma)$ in 2 RES nodes.
2. From $(a\lor\neg b\lor\sigma)$ and $(\neg a\lor\neg b\lor\sigma)$ derive $(\neg b\lor\sigma)$; from $(\neg a\lor b\lor\sigma)$ and $(\neg a\lor\neg b\lor\sigma)$ derive $(\neg a\lor\sigma)$; use these two clauses and the third owner facet to derive $(\neg z\lor\sigma)$. These are 4 RES nodes.
3. Resolve $(z\lor\sigma)$ and $(\neg z\lor\sigma)$ to derive unit $\sigma$ (1 RES).

Thus $2\cdot7+1=15$ Resolution nodes plus one paid DEF owner. Final RES of $(c)$ and $(\neg c)$ derives the empty clause. All three owner facets are actually referenced, not independent SOURCE axioms. Total **16 distinct paid nodes**, **three owner-qualified free facet views**. This is *not* an optimality claim: the eight-clause source has much shorter pure Resolution proofs.

Original, freshly published executable \`experiments/arc/lspv1_558_er_facet_replay.cjs\` (blob \`44c15ed4b0b88c811db2dfd6dfd90caf6549157f\`) was evaluated in V8, and its exact returned JSON was published. It independently reconstructs and checks original clause IDs, all owner truth-table rows, global identity/freshness, every signed pivot and resolvent, final empty clause and source equality. **Eight of eight hostile controls rejected**: original source alteration, unknown facet owner, incorrect pivot, forged RES conclusion, reused paid ID, cyclic DEF, unknown opcode, and missing intermediate RES. The source is an independently supplied canonical in-memory signed-clause array; the code **does not implement a production DIMACS byte parser or authenticate the missing historical grammar**. Published Node OS process execution, full historical checker execution and independent LSPV-5 review were **not** performed.

## Dependency ledger and proposed cross-role interface

**[P2-D1] OPEN.** Demand an authoritative original-byte acceptance test for (a) externally fixed SOURCE $F_8$, (b) paid \`DEF z=a OR b\`, (c) exact owner-qualified facets, and (d) one RES using a facet parent and another using a previously derived RES parent. Do not substitute proposed \`R_fac\`, CANON1, CANON2, CANON2R or FRAT-XOR for historical authority. Original /341 prose lists five charged rule families (RES, AND3, XOR, LOCAL-CONVERT, DEF) and no independently declared native free case/discharge opcode.

**[P2-C3] OPEN.** A complete alpha/gamma proof must simulate ALL *authenticated* native operations, including source-byte identities, owner facets, contexts and any actual branching/joins; one cost-preserving ER fragment is not an all-rule abstraction. Unknown rules are conservatively MAY-overapproximated, not silently excluded.

**[P2-B1] OPEN.** The theorem supplies a **conditional full-input upper-bound transfer** from normal-form ER to facet-enabled mixed calculus, restricting candidate hard families. It gives NO superpolynomial lower bound. Known Res(XOR), ordinary Resolution, and tree-like lower bounds do not automatically transfer upward.

**[P2-B2]/B3 OPEN.** SAT in P and a checker do not imply polynomial minimum proof work in this preselected calculus. No arbitrary-decider bridge obtained. [P1-01], [P1-03], [P1-04] remain OPEN.

**Role interfaces:** LSPV-3 should try to authenticate the native owner/facet-to-RES parent precisely or produce a byte-level refusal. LSPV-2 should independently source-bind and compile a small honest ER trace. LSPV-4 should charge evidence bits and all-phase checker time/space separately from 16 paid logical nodes. LSPV-5 should independently falsify source/facet freshness, owner reuse and the all-input compiler quantifiers. No role, identity, schedule, native weight, main.tex ownership or historical 2 Route A / 3 Route B allocation was changed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No load-bearing status is promoted: this explicit general compilation is within the previously declared R_fac interface and sharpens LSPV-1/548, not evidence of historical parser acceptance. Root trackers and main.tex preserved. No conflict-risky 0.94MB tracker overwrite attempted.

## Publication and limitations

Report and handoff published on GitHub main; code and raw computational evidence published and full-content readback verified separately. Mathematical argument is a **conditional theorem** for a distinct semantic completion, not an accepted native refutation or new proof-complexity lower bound. Next decisive test is a genuine historical \`DEF->FACET->RES\` accepted-byte certificate or authenticated refusal. P versus NP remains OPEN.
