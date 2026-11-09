# LSPV-1/519: A polynomial conservative ER2 refutation upper bound for the strict modulo-three Tseitin family

**2026-11-08 17:00 PST | Route B | PROVED/RESTRICTED for the explicit RES + paid binary DEF gate/facet calculus, not yet accepted by the historical byte checker | COMPUTATIONAL finite controls | P versus NP OPEN.**

**Affected evidence:** [P2-L1-519], [P2-L1-518], [P2-L5-447], [P2-F6], [P2-C3]. Outstanding [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Route A and P1-01/P1-03/P1-04 unchanged.

## IDEA: hypothesis and falsifiers

Hypothesis: the exact strict proper 3-CNF opposite-characteristic modulo-three Tseitin family from LSPV-1/518 has a polynomial-size proof if the calculus permits paid conservative Boolean two-input gate definitions plus ordinary Resolution. Such a proof would obstruct transferring the externally established syntactic Res(PC_r/F2) lower bound into the full mixed calculus.

Four falsifiers: (1) source clauses cannot yield fixed-size local mod-three flow implications after paid definitions; (2) global sum cancellation requires an unbounded-support inference that cannot be broken into polynomially many small Boolean RES macros; (3) the construction silently uses free extensions, a semantic oracle, omitted source clauses, incompatible branch assumptions or superpolynomial cost; (4) the declared ER2 semantic grammar is incorrectly equated to the historical accepted byte grammar.

The constructive argument below resolves (1)-(3) within the **specified ER2 rule model**. Item (4) remains OPEN and bars a historical native-checker acceptance claim.

## SEARCH: sources, continuity, duplication controls

Complete current root tracker reads: proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt startup SHA 27b7c71e460d04d5245ec4b87e43a6462597883b. Read issue #3 including the newest LSPV-5/447 referee; the governing 2026-11-02 12:04 five-role handoff at 4e29ed7646f484707767acb6e63ec5f38afd98a8; AGENTS.md 19656af102604d5f0a721d548cf2e4e72a063561; CODEX.md 754999f50de93cdb693ed37bc8110d31e9e698ef; research skill b8df83a7b0b1428f349b0e02ce1387d979e8db7f.

Historical fixed-rule source: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb); source-facet ER2 model: research/coordination/2026-11-03_0100_LSPV1_ER2_SOURCE_PADDING_TYPE_FIREWALL358_FIVE_ROLE_HANDOFF.md (52747b023adae98151890daf20b62cbc8f0c2e97). Prior LSPV-1/464 and /476 already establish ordinary Resolution restriction simulation. Prior LSPV-1/482 already shows B1-vs-B2 separation in a *different* fixed F3 proof system; no novelty from that result is claimed. Reused LSPV-1/518 primary family (407ca3822d21387a4710d8ec41aebc831cda7856), LSPV-5/447 independent strict-padding referee (dee761f03de1e9749bf4b0373d6582cfe3133768), LSPV-3/515 typed external XLRUP control (f9aed3b802319f83fb26e2719592319cb55b93d4). No conflicting peer result was silently overwritten.

Actually read Grok GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70 and Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4e7e0e3edff3aba8610852c45534bdde128. External required repositories read: konard/p-vs-np README.md 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research README.md f397a7747eaca82df3d754d0a4b4bab1fe10f814, METHOD_INDEX.md known blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor format.md 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae. These are sources, not authority for the historical inference grammar. Web primary research read Pang arXiv:2610.00837v2 (2026-10-24), Theorems 1.1, 7.2(b), Corollary 7.3 and source definition; Raz and Tzameret 2008 abstract checked. Repository searches for historical mod-3 ER2 macros found related /358, /434, /464, /476 but not this complete strict-source upper template. Not a claim of independent academic novelty. No separate Google-branded portal or PDF was used.

## Exact source/encoding and published theorem ledger

Take a connected simple oriented cubic graph G=(V,E), h=|V| even, |E|=3h/2; charges b_v in F3 sum to a nonzero element. For each edge e introduce the original Boolean atoms x[e,0],x[e,1],x[e,2]. The edge source clauses are (x[e,0] OR x[e,1] OR x[e,2]) and the three distinct negative binary uniqueness pairs. For each vertex, forbid the 18 incident edge-label triples whose signed F3 sum disagrees with its charge, using one signed negative ternary source clause per forbidden triple. Deduplicate binary uniqueness pairs as required by LSPV-5/447. Old CNF: 9h/2 original atoms, 24h canonical clauses, 9h/2 of them binary.

Introduce one globally fresh ORIGINAL padding bit z and replace each binary clause B by the two strict clauses (B OR z) and (B OR NOT z). The resulting exact proper signed 3-CNF has 9h/2+1 atoms, 57h/2 canonical clauses, encoded size O(h log h). Either Boolean restriction of z recovers the old formula. Pang Theorem 7.2(b) plus the syntactic polynomial-calculus degree preservation proved by LSPV-1/518 give exp(Omega_r(h)) proof-size hardness for the **different, fixed-r syntactic Res(PC_r/F2)** on a published cubic-expander subfamily, conditional on the cited 2026 preprint. This is neither all-algorithm hardness nor an ER2 lower bound.

## Theorem 519.1: polynomial ER2 upper proof schema

Fix the separately declared **ER2** calculus: original clauses are free; each globally fresh two-input signed-AND Boolean definition has unit paid cost and emits its three conservative defining facets, which may be used as already paid antecedent conditions in **ordinary binary Resolution**; each RES inference costs one; all other semantic shortcuts are forbidden. Negated wire ports are literal signs, and OR gates are represented using De Morgan signed AND gates. The proof is a single source-authenticated acyclic shared DAG with no case-split/discharge rules.

For every G,b as above there is a uniform construction of a valid ER2 refutation with

$$
\boxed{W_{\mathrm{ER2}}(F^z_{G,b})\le C h^3}
$$

and encoded proof length O(h^3 log h), where C is a fixed constant determined by the finite Boolean-gate basis and a constant-support Resolution macro compiler. This is an **upper bound**, not an assertion of optimality or historical checker acceptance.

**Constructive proof.**

1. Resolve the original padded pair (B OR z),(B OR NOT z) on z to derive the EXACT old B. Each old binary clause costs **one** paid RES inference, 9h/2 in total. The old ternary clauses remain original sources. Share each recovered B wherever referenced.

2. Treat each edge label as a one-hot F3 number. A modulo-three adder for two one-hot triples is a constant-size Boolean circuit: output bit r is the OR of the three conjunctions x_i AND y_j with i+j=r mod 3. Compile all Boolean gates into paid conservative signed two-input AND definitions and exact defining facets. Negative edge incidences use the permutation exchanging the one-hot labels 1 and 2. Under source-proved one-hot constraints, output triples are one-hot and compute F3 addition. No F3 rule is imported.

3. **Finite-support Resolution lemma.** If a satisfiable CNF H over at most K Boolean atoms implies a clause C, saturating ordinary Resolution derives a subclause of C with at most 3^K distinct non-tautological derived clauses, since a clause has three states per atom and Resolution is implicate-complete up to subsumption. Every inference is emitted with two earlier parent IDs and an exact signed pivot. Stronger subclauses are reusable by standard subclause-preserving Resolution replay; no free weakening is introduced. Whenever H is a constant-size circuit gadget, fixed one-hot input axioms and its defining facets, K is an ABSOLUTE constant. Hence each required bounded-gadget identity and local vertex consequence has a uniformly bounded, source-indexed paid RES derivation. Source triples are at most three edges (nine original bits); gate gadgets are fixed size.

4. Form a left-fold Boolean F3-adder circuit on the 3h **signed incidence terms in vertex order**. Using each vertex's original 18 forbidden clauses, edge one-hot constraints, paid gate facets and the constant-support RES lemma, prove by induction that the accumulator after vertex v has the cumulative charge of the first v vertices. Every induction step depends on the prior three-bit accumulator plus the next three local edge values only. It uses O(1) paid gates and RES macros. The final vertex-order accumulator is the nonzero total charge B.

5. Transform the incidence list into an edge-paired order (+e,-e) by at most (3h)(3h-1)/2 adjacent transpositions. For an adjacent swap, construct the corresponding new left fold. At the changed position use the constant-size identity

$$
(P+a)+c=(P+c)+a\pmod 3.
$$

Propagate three-bit output equivalence through the identical suffix using constant-size congruence RES macros, each with original or paid-def provenance. At most O(h) gate/proof work per swap gives O(h^3) total. Reuse valid shared prefixes; charge each unique gate and derived clause node only once.

6. For the paired list, at each edge use another fixed macro for (P+a)+(-a)=P. The final edge-paired accumulator is zero. The derived output-equivalence clauses transport the nonzero unit from the original fold to the paired fold; one contradictory output bit and its negation resolve to the empty clause. All case obligations are discharged in the single unconditional proof, with no branch-local leakage.

This is a constructive **polynomial-cost Boolean extended-resolution proof template**. The use of generic constant-support implicate completeness is explicit; its astronomically large but fixed worst-case constant is not treated as a free unit-cost oracle. Every gate and each RES inference is charged. Certificate generation can mechanically enumerate those fixed local proof spaces rather than solving arbitrary SAT.

## ITERATE: consequence and the historical-type limitation

The q=3 opposite-characteristic strict3 Tseitin family **cannot be a superpolynomial minimum-work witness in any preselected calculus that actually polynomially simulates the declared ER2 gate/facet/RES fragment**. This is an explicit upper-bound shortcut that must be admitted rather than suppressed to protect Pang's restricted lower-bound statement. The same family is still exponentially hard for the published syntactic fixed-degree F2 proof system; the proof models differ.

This does NOT authenticate every native historical R_mix341 production, especially definition facets, exported/private gate ports and source-vs-derived premise admissibility. The actual historical mixed checker has not accepted a complete compiled packet; the theorem is **PROVED/RESTRICTED for ER2, CONDITIONAL as an R_mix341 family-failure inference**. No B1/B2/B3 implication is established or negated for historical R_mix341. Haken ordinary Resolution and odd-charge GF2 Tseitin remain separate controls.

## Independent finite checking, resource ledger, and handoff

Independent Python on six K4/K3,3/Q3 signed source controls (three even/SAT, three nonzero-total/UNSAT) completed **4,116 checks**: exact original and strict canonical clause counts, signed pair de-padding, 96 sampled one-hot edge flows at BOTH padding values per case, source-based mod3 rank, 27 ternary adjacent-swap identities, nine pair cancellations and sorted incidence order. It preserved full strict DIMACS SHA256 per case and detected corrupt signed pairs. A separately authored JavaScript verifier published at experiments/arc/lspv1_519_er2_mod3_controls.cjs completed **1,959 checks**, was executed in V8, and passed exact full readback at blob 02eb011c85d9754d7e6704d59eec13b75cd36a3d. These are finite controls, **not** acceptance of a complete historical native proof certificate, and the test graphs are not asymptotic expanders.

Distinct-node theoretical upper bound O(h^3), bit evidence O(h^3 log h), uniform local-proof construction and total machine-time O(h^3 polylog h) with a very large constant from exhaustive finite K-variable clause closure, peak source+gates+evidence+verification O(h^3 log h) bits for a fully materialized implementation, and O(h^2) adjacent-swap planning. All source/index/ref reads, gate construction, local RES searches, verification and output are included in this polynomial upper estimate; no measurement of actual historical native-TM tape high-water is asserted. Free ideal proof choice remains distinct from implemented optimizer cost. The Route A inequality s'<=max(rho,eta,lambda,lambda*s) is preserved and not invoked.

**Next tests:** LSPV-3 should emit and check a full typed local adder and K4 native packet with original source and paid facets. LSPV-5 should independently red-team the constant-support implicate compiler, subclause replay, source/auxiliary typing and total sharing. LSPV-1 should seek a genuinely established family surviving these legal Boolean ER2 shortcuts, and independently continue [P2-B2] noncircular same-system B3. Historical grammar and weights, all agent identities, schedules, enabled states and two Route A/three Route B allocation were untouched. Root main.tex was not modified because safe full-content ownership preservation has not been established.

**P versus NP remains OPEN.**

## Primary references

[1] Pang, S., A Degree–Size Relation for Resolution over Polynomials, arXiv:2610.00837v2, 24 October 2026, Theorem 7.2(b), Corollary 7.3: https://arxiv.org/html/2610.00837v2

[2] Raz, R., Tzameret, I., Resolution over Linear Equations and Multilinear Proofs, Annals of Pure and Applied Logic 155 (2008), 194–224: https://arxiv.org/abs/0708.1529
