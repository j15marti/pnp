# LSPV-2/407: A Six-Node Export-Port Disambiguator for the Original R_mix341 Grammar

**November 4, 2026, 20:12 PST | IDEA -> SEARCH -> ITERATE.** Role: PNP SAT-Circuit Reduction Builder (LSPV-2). Original fixed calculus and all weights, tasks, schedules, ownership and enabled states unchanged.

**Status:** **PROVED/EXACT** for two explicitly specified, source-sound *completions of an unresolved serialization convention*; **COMPUTATIONAL** independent truth-table and GF(2) checks; **OPEN** which completion is the legal unchanged native R_mix341, full original-source normalized polynomial compiler, B1/B2/B3, superpolynomial mixed minimum and P versus NP. **This report does not exhibit a certified legal native-R counterexample.** The distinction is a formal syntax/well-formedness ambiguity, not a theorem about the native minimum W_R.

## IDEA before SEARCH: exact hypothesis, prediction, four falsifiers

**Hypothesis:** The original paid-DEF rule's promise that all defining relations are "attributed to that same charged node" and that subsequent uses "reference its charged node" does **not determine** whether a binary XOR gate automatically exposes an individually addressable GF(2) equation as an operand of the already specified binary XOR rule. Predict two compatible source-sound type completions accepting and rejecting the *same* six-node nested AND3 + DEF + GF(2) + LOCAL-CONVERT certificate, differing at the first exported-row read.

Falsifiers: (F1) input is not SAT or the claimed row is not an original-source consequence under conservative definitions; (F2) a false or improperly typed gate row is accidentally accepted; (F3) original /341 explicitly settles the DEF-to-GF(2) selector, making one completion incompatible; (F4) the alleged difference is a shortest-proof or B3 difference rather than mere acceptance of one serialized trace. Include a signed-source mutation, XNOR mutation, forged defining row, forged row sum, malformed DIMACS, and mistaken LOCAL target.

## SEARCH: actual sources, searches, prior art and limitations

Read first the governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (current blob c3889a3e; original published blob 033b54b8). Read current coordination issue #3 through latest LSPV-1/408 and LSPV-3/409, AGENTS.md (blob 19656af1), CODEX.md (754999f5), .codex/skills/pnp-research/SKILL.md (b8df83a7), authoritative source research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11), original-LSPV1/384 grammar addendum (bbcdad9a), LSPV-2/406 (58300e7d), LSPV-3/409 (2b5a58bf), LSPV-4/400 (e01464b9) and contemporaneous REFEREE352 via issue #3. LSPV-3/409 already gives a **conditional** two-DEF-six-RES XOR alias and unbounded chaining, so those results are prior art, not reclaimed here. LSPV-4/400 already gives a **genuinely native** AND3-LOCAL-RES consumer rewrite counterexample. The increment here is an explicit *AND3 + 2 DEF + 2 GF(2) + LOCAL* input, a rule-by-rule port-type disambiguator, and matched positive/negative semantic fixtures.

**Actual independent project files:** GROKPROOF/2026-11-05_0315_PROGRESS.md (blob 2c21a1eb; universal all-input FLMV contraction still OPEN); research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727; restricted alternation trading); research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6; sequential-access crossing-sequence model). These do not specify the native export port or establish B3.

**General-web queries:** "Haken Intractability of Resolution 1985 pigeonhole principle exponential resolution"; "Cook Reckhow relative efficiency of propositional proof systems 1979"; "Raz Tzameret Resolution over Linear Equations multilinear proofs GF2"; "Pich Santhanam Towards P not equal NP from Extended Frege Lower Bounds ECCC TR23-199"; "Cook A short proof pigeon hole principle using extended resolution 1976"; "Buss Krajicek circuit rewrite proof systems 2026." Read Haken's original journal abstract/metadata (full 1985 paper **not** obtained), Cook–Reckhow's author-posted 1979 PDF text, Raz–Tzameret's 2008 institute abstract and ECCC abstract for Pich–Santhanam; no result was treated as a same-R compiler. Primary URLs: https://doi.org/10.1016/0304-3975(85)90144-6 ; https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf ; https://weizmann.elsevierpure.com/en/publications/resolution-over-linear-equations-and-multilinear-proofs/ ; https://eccc.weizmann.ac.il/report/2023/199/ . **Direct Google-branded search unavailable; general web search was used without claiming Google site access.**

**Authenticated github.com/openai searches:** "ExecCNF", "CookLevin", "resolution proof checker", "LRAT". Read the full openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f44ad49370d1b812e862c03c3a91d7f836). That code explicitly tracks one concrete program run's trace and cost and is useful as resource-accounting discipline, but neither it nor other results supplies original-source mixed proof normalization or B3. "LRAT" search had unrelated substring matches; no theorem was inferred from them.

## ITERATE: the precise six-node diverging certificate

Original *satisfiable* source, ASCII DIMACS exactly 20 bytes:

~~~dimacs
p cnf 2 2
1 0
1 2 0
~~~

Write its original variables as x,y. It has exactly two models: x=1 and y arbitrary. It entails x=1. All inference/definition nodes have weight one and at most two antecedent node IDs; sources are free.

| Node | Native rule name | Parents | Proposed output | Consequence / typing |
|---|---|---|---|---|
| 1 | AND3 | source (x), source (x or y) | factor x=1, annotated GF(2) row x=1 | support {x,y}; exact truth table |
| 2 | DEF | no earlier derived node required for gate introduction | fresh a := x XOR y | charged binary conservative gate; possible row a+x+y=0 |
| 3 | DEF | prior named a allowed | fresh b := a XOR y | charged binary conservative gate; possible row b+a+y=0 |
| 4 | XOR | defining rows of nodes 2 and 3 | b+x=0 | first disputed DEF-row selector |
| 5 | XOR | rows from nodes 4 and 1 | b=1 | exact GF(2) sum |
| 6 | LOCAL-CONVERT | row from node 5 | clause (b) | on both source models, b=x=1 |

All plus signs in equation rows denote GF(2) sum, **not** assertion of standalone true gate outputs. Each fresh definition uniquely extends each original assignment. The original support of a is {x,y}; that of b is at most {x,y} and in fact its Boolean function simplifies to x. The emitted clause (b) is **not** inferred from x without accounting for the two definitions.

Define two precise completions of the **unresolved DEF port syntax**, while retaining all original rule names, unit weights, source axioms and explicit RES completeness:

* **Splus (public-row interpretation):** when a separately paid two-input DEF gate is XOR2, its defining relation may be selected from that existing paid record as a typed GF(2) equation operand, with no additional **inference node**; the selector and exact row bits are still supplied and physically checked. No new free Boolean fact or hidden SAT oracle.
* **Sminus (private-row interpretation):** the paid DEF relation is retained as a conservative Boolean gate constraint for subsequent typed gate/possibly clause-level use, but it is **not already an addressable GF(2) row**. A separately justified, typed conversion would be necessary to make it a GF(2) XOR operand. The original /341 text does not give the conversion's byte grammar or cost.

**Proposition 407.1, PROVED/EXACT for the two completions:** The displayed six-node certificate is accepted by Splus but is rejected by Sminus **at node 4**, because Sminus has no GF(2)-row operand selector for nodes 2 and 3. Both completions preserve source SAT under their respective legal inferences and are refutationally complete via original RES. Proof: each source model has a uniquely determined a=x XOR y and b=a XOR y=x; the two exported Splus equations XOR to b+x=0, then with row x=1 to b=1, whose LOCAL clause is valid. In Sminus the node-4 parent references have Boolean DEF-gate type, not GF(2)-equation type, so the XOR rule's precondition fails. Neither completion permits a false conclusion on a SAT source. QED.

This proves that the *present prose does not uniquely certify this trace*. It **does not prove** that the authentic preselected R_mix341 accepts it, that an alternative proof cannot exist in Sminus, or that W_R changes between interpretations. This grammar ambiguity was already known from LSPV-2/406; the new contribution is an executable six-node distinguishing certificate with AND3, two charged XOR-gate definitions, two GF(2) additions and consumer LOCAL-CONVERT, and exact source/row negatives.

**Additional negative controls:** Replacing the second gate by b:=a XNOR y gives row b+a+y=1, hence b+x=1; x=1 implies b=0, so the proposed LOCAL clause (b) is rejected. Replacing the source unit (x) by (not x), keeping (x or y), gives SAT with x=0,y=1 and also rejects (b). Forging either gate row or the first GF(2) sum is detected. Forging the target clause is detected.

## Computational controls and physical costs

The local Python producer ran 17 assertions plus **7 malformed DIMACS rejects**, independently verified all four valuations of x,y and the complete 6-node positive/negative typing. A separately implemented JavaScript checker ran **38 independent assertions** from the machine-readable record. It validated all XOR identities and type distinctions, the two original SAT models, source-sign and XNOR countercontrols and five corrupted/false conclusions. No random seed, no heuristic optimization, no SAT oracle and no numeric shortest-proof claim.

The 20-byte source input is **N**, while evidence length **E** includes six paid records, gate types, input IDs, output IDs, signed RHSs, two GF(2) operand references, the conclusion and any serialized gate facets. The logical cost is **q=6** under Splus (1 AND3 + 2 DEF + 2 XOR + 1 LOCAL). It is not the physical bit-cost. Parsing, all truth-table/gate row checks, proof DAG pointers, source lookups, row mask XORs, LOCAL validation and output bits must be charged. For the displayed 2-original-variable trace they are finite constant-work verifications. For an arbitrary M=N+E evidence length with explicit bounded-arity gate truth tables and row masks, a straightforward fully materialized checker uses at most polynomial bit time and polynomial peak memory in M, **not necessarily polynomial in N+q** if uncharged payloads can be arbitrarily long. Host RSS was not measured, and no FLMV-compatible simultaneous (T,S) claim is made. One compact alternative representation is simply the *shared two-gate network* with 2 paid DEF records, computing b=x without unfolding the circuit into a large CNF; extracting a consequence still requires an authenticated consumer proof.

## The two decisive missing arrows

**Deliverable 1 remains OPEN:** settle the authentic /341 grammar with a byte-level choice for DEF-to-GF(2), public/private auxiliary ports, named defining CNF facets, LOCAL circuit payloads, and exact support typing; then establish consumer-aware polynomial normalization/translation **in supplied evidence bits**, and only claim an N+q bound after independently proving E polynomial in N+q. This report supplies the minimum *discriminating* type check, not a legal full-native counterexample.

**Deliverable 2 remains OPEN, B3 for the same fixed R:**
$$
\mathrm{SAT}\in\mathrm{P}\ \Longrightarrow\
\exists C,k\;\forall N\quad
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$
A hypothetical correct uniform polynomial-time decider can certify its own **rejection as a machine event**; its *global correctness as UNSAT reasoning* is a separate semantic fact. Cook–Reckhow gives a potentially different polynomial proof system with an A-based verifier under SAT in P, not a source-authenticated polynomial derivation in the unchanged R. Neither typed trace acceptance nor proof-bit normalization implies B3. Distinguish B1 pointwise, B2 worst-case, B3 minimal conditional. No per-input advice, relabelled source, or uncharged machine correctness axiom.

**Hard-family control:** Haken 1985 concerns every ordinary shared-DAG Resolution proof of standard explicit unary PHP_(h+1,h) CNF, with h(h+1) Boolean variables, m=(h+1)+h*binom(h+1,2) clauses, N=Theta(h^3 log(h+2)) signed-index bits, and 2^{Omega(h)} Resolution lines. It is NOT an all-algorithm, GF(2), DEF, ER or mixed calculus lower bound. Cook 1976 gives polynomial Extended Resolution PHP proofs, and the established odd bridgeless cubic Tseitin fixed mixed calculus optimum is 4h-1, despite restricted Resolution hardness. Raz–Tzameret Res(lin) is a different proof grammar.

**Status:** P versus NP OPEN. No tasks, schedules, enabled states, native rules/weights or other roles' manuscript regions changed. Root main.tex readback returned SHA 020e9fc2 with **zero content bytes** in the connector response. Therefore root was **not written**: a partial/empty response cannot safely preserve other authors' text. Local preflight/check scripts could not operate on the repository, which is inaccessible to the container's DNS; report and code were tested separately.

## Exact outbox and next step

Report: research/agents/lspv-2/2026-11-04_2012_LSPV-2_DEF_ROW_EXPORT_DISAMBIGUATION407.md
Producer: experiments/arc/lspv2_407_port_divergence.js
Independent checker: experiments/arc/lspv2_407_independent.js
Raw: results/raw/arc/2026-11-04_2012_LSPV2_PORT_DIVERGENCE407_raw.json
Handoff: research/coordination/2026-11-04_2012_LSPV2_PORT_DIVERGENCE407_FIVE_ROLE_HANDOFF.md

**Next needed authoritative input:** a serialized native row-selector rule, positive or negative, for paid DEF nodes plus a complete LOCAL exported-wire grammar. In the absence of that source, do not promote Splus acceptance to native legality. Independently, prove a same-R simulation from a hypothetical correct polynomial-time decider, not merely its rejecting trace or an alternative proof system.
