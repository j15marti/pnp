# REFEREE351 — typed-interface normalization repair and B3 reflection firewall

**PNP Independent Proof Red Team | November 4, 2026, 18:49 PST**  
**Status:** PROVED/EXACT compositional typed-interface lemma; PROVED/EXACT minimal legal native counterexample to implication-only, edge-preserving normalization (independently reproducing LSPV-4/400); PROVED/EXACT trace-only reflection impossibility and a conditional proof-system characterization of B3; COMPUTATIONAL finite controls. The exact native `LOCAL-CONVERT` payload/export grammar is still under-specified in `/341`, so no unconditional full native normalization theorem is claimed. B1/B2/B3, superpolynomial mixed lower bounds, unrestricted SAT hardness, and P versus NP remain OPEN.

## IDEA before search

Attack the remaining logical core of both requested deliverables.

**Hypothesis A (normalization repair).** For the strict root-only completion audited in REFEREE350, polynomial normalization remains valid only if every public typed conclusion is preserved exactly (up to a globally consistent alpha-renaming) and every consumer is recompiled and rechecked. Mere implication, equisatisfiability, or strengthening of each node is insufficient.

**Falsifiable prediction:** there is a smallest legal native `AND3 -> LOCAL-CONVERT -> RES` fragment for which a stronger entailed replacement deletes a named Resolution pivot. If exact public interfaces are preserved, local verifier legality composes by topological induction.

**Hypothesis B (B3 firewall).** Assuming a fixed polynomial SAT decider `A`, one gets a polynomially bounded Cook–Reckhow-style UNSAT verifier `Q_A`, but a same-`R_mix341` B3 transfer additionally requires `R_mix341` to p-simulate `Q_A` (equivalently, short same-system reflection/correctness evidence). A rejecting computation trace alone cannot supply this uniformly.

**Falsifiable prediction:** primary literature will impose short proof-system soundness/reflection as a separate hypothesis. A source showing that bare `SAT in P` already makes Extended Frege/ER p-bounded would falsify the firewall.

Four adversarial checks were fixed before search: (1) a legal pivot-loss witness; (2) a weakening whose exact resolvent changes; (3) a satisfiable input and an unsound always-reject machine sharing a local rejecting trace; (4) malformed rule records and both-label controls.

## SEARCH

### Governing project, issue, peers, Grok, and Claude

Read the governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, current issue #3 through LSPV-4/400, and the authoritative unchanged rule declaration

`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`

(blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`). Its exact words authorize: ordinary RES; exact support-at-most-three AND3 truth-table factors; binary GF(2) row addition; a unary LOCAL conversion to a clause or bounded-support circuit condition after an explicit constant-support implication check; and one paid fresh conservative two-input DEF. It still gives no byte grammar for LOCAL circuit payloads, public internal gate IDs, or pay/no-pay export boundaries.

Current peer findings used, not rebranded as novel:

- `research/agents/lspv-1/2026-11-04_1758_LSPV-1_POLY_DENSE_REFLECTION_CHECKPOINT405.md` (blob `130eb0e0`): dyadic sampling is exact, but it assumes the missing compiler and short reflection proofs.
- `research/coordination/2026-11-04_1812_LSPV2_ALL_VALID_ROOT405_FIVE_ROLE_HANDOFF.md`: under conditional explicit payload syntax `U`, exact supplied-root extraction can require reading every payload bit even though a constant equivalent root exists; `U` is not certified native.
- `research/coordination/2026-11-04_1824_LSPV3_PAID_DEF_ALIAS407_FIVE_ROLE_HANDOFF.md`: structural DEF canonicalization is sound but semantic wire equality is coNP-hard in a conditional setting; downstream consumers still require validation.
- `research/agents/lspv-4/2026-11-04_1836_LSPV-4_LOCAL_CONSUMER_REWRITE400.md` (blob `e01464b9`): the legal native pivot-loss witness independently reproduced below. This run credits LSPV-4/400 and adds the exact typed congruence repair and B3 proof-system characterization.
- REFEREE350: the strict completed root grammar is conditionally p-equivalent to fan-in-two ER, but the original prose does not force that grammar.

Actual independent assessments read:

- `GROKPROOF/2026-11-04_2315_PROGRESS.md` (blob `f5b8ef62`): black-box child writing is restrictedly lower-bounded; universal white-box residual extraction remains OPEN.
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727`): a restricted portfolio/alternation-trading theorem, not B3.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6`): sequential-access crossing-sequence bounds, explicitly not the indexed random-access or proof-reflection target.

Neither Grok nor Claude supplies a native proof compiler or a same-calculus reflection theorem.

### Primary research literature and general web

Actual queries:

1. `P equals NP Extended Frege polynomially bounded proof system open problem reflection primary`;
2. `NP coNP does not imply Extended Frege polynomially bounded proof complexity p optimal primary`;
3. `feasible reflection Extended Frege p bounded SAT algorithm Krajicek primary paper`;
4. `propositional proof systems P NP p-optimal Extended Frege soundness self-provability primary`;
5. `A note on SAT algorithms and proof complexity Krajicek PDF`;
6. `Cook Reckhow relative efficiency propositional proof systems polynomially bounded iff NP coNP PDF`.

Read rather than relying on snippets:

- Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979): a polynomially bounded proof system exists iff `NP=coNP`; this is an existential theorem about some system, not a p-simulation into a preselected one. <https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf>
- Krajíček, *A note on SAT algorithms and proof complexity* (IPL 2012): `Alg(P)` contains algorithms whose soundness tautologies have polynomial `P`-proofs. Bare algorithmic correctness is not substituted for this proof hypothesis. <https://www2.karlin.mff.cuni.cz/~krajicek/sat.pdf>
- Buss, *Propositional Consistency Proofs*: polynomial partial consistency/reflection and p-simulation are linked; in particular, Frege proves partial consistency of EF iff Frege p-simulates EF. <https://mathweb.ucsd.edu/~sbuss/ResearchWeb/prop_consis/paper.pdf>
- Pich and Santhanam, *Towards P != NP from Extended Frege Lower Bounds*, ECCC TR23-199: the transfer explicitly introduces self-provability of upper bounds as additional structure. <https://eccc.weizmann.ac.il/report/2023/199/>
- Krajíček, *Implicit proofs*, ECCC TR03-055: circuits may describe exponentially long proofs; this strengthens rather than erases the need to state the proof representation and checker. <https://eccc.weizmann.ac.il/eccc-reports/2003/TR03-055/index.html>

The available browser exposed general web search, not a direct Google-branded search UI. This limitation is explicit; no direct Google session is claimed. The ScienceDirect and one Buss index-page fetch failed (403/timeout), so the accessible author PDF and indexed primary metadata were used.

### GitHub, including OpenAI

Authenticated OpenAI queries:

- `proof system reflection certificate verifier SAT`;
- `Extended Frege resolution proof checker`;
- `ExecCNF`.

The first two returned no relevant OpenAI files. The third located and the run read the complete `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean` at commit `4eaee875`: it formalizes executable CNF list operations, semantic preservation, comparison counts, and explicitly refuses to treat arbitrary equality comparisons as unit bit cost. It is useful implementation discipline but not a native `R_mix341` compiler, ER reflection proof, or B3 theorem.

Project queries included `R_mix341 LOCAL-CONVERT exported wire AND3 GF(2)`, `GROKPROOF R_mix341 B3`, `Claude R_mix341 B3`, and `LSPV-1 dyadic checkpoint 405`. A guessed LSPV-1 filename and a guessed Claude ONETAPE filename returned 404; repository search located the exact paths above. No absence was treated as mathematical evidence.

## ITERATE I — exact typed-interface repair

### Typed public objects

For a machine-readable completion, a derived node's public conclusion must have one of these exact types:

1. **CLAUSE:** exact signed literal set, with a consumer RES record naming its complementary pivot and exact resolvent;
2. **FACTOR:** ordered original-variable support plus complete truth table;
3. **AFFINE:** exact named-variable coefficient mask and RHS bit;
4. **DEF:** globally fresh output ID, exact four-bit two-input gate table, and exact signed predecessor IDs;
5. **ROOT/LOCAL:** exact bounded-support root relation or exact clause; private checking gates are not public unless separately paid DEF nodes.

Source records keep their original identities. Alpha-renaming must be a single injective map respecting negation, freshness, supports, and every downstream reference.

### Theorem 351.1 — exact-interface congruence (PROVED/EXACT meta-lemma)

Fix a finite typed proof grammar whose verifier for a record is a deterministic predicate of its rule tag, exact public parent objects, exact public conclusion, source references, and local justification bytes. Suppose a translation processes records in topological order and, for every record, constructs a target record that the target verifier accepts and whose public object is the globally alpha-renamed exact source public object. Then every consumer remains well-typed and the translated DAG is legal. If each record translation, output length, and verifier run is polynomial in the supplied encoded proof length `M=N+E`, the whole translation is polynomial in `M` and its output length.

**Proof.** Induct over the topological order. Source identities are fixed at the base. At record `i`, all translated parents already expose the exact renamed objects assumed by the local translator. The target verifier therefore accepts record `i`, and its exact conclusion becomes available to all later records. The induction reaches the contradiction node. Summing polynomially many polynomial local construction/checking/output bounds is polynomial in the explicit input/output lengths. This proves syntactic composition, not semantic discovery of an equivalent interface. QED.

Applied to REFEREE350's explicitly completed root grammar, the theorem repairs its translation statement: each mixed record is recompiled to an ER macro from the exact public relation, and every later consumer is recompiled from those exact interfaces. It is not an in-place edge-preserving substitution. The GF(2) coefficient mask, clause pivots, factor tables, and paid DEF ports are preserved exactly up to alpha-renaming.

This does **not** settle the original native grammar. `/341` still omits the serialized LOCAL payload/export contract. The theorem is a sufficient compiler discipline once that grammar and all per-rule macros are supplied.

### Theorem 351.2 — implication-only normalization fails on a legal native fragment

Independently reproducing and crediting LSPV-4/400, take the satisfiable original source

`F = (x) AND (x OR z) AND (NOT y)`.

It has exactly two models (`x=1,y=0,z` arbitrary). Three paid native nodes are legal:

1. AND3 of `(x)` and `(x OR z)` yields the exact factor `x`;
2. LOCAL-CONVERT yields the implied clause `(x OR y)`;
3. RES with original `(NOT y)` on named pivot `y` yields `(x)`.

Replacing the LOCAL conclusion by the stronger entailed `(x)` while retaining its consumer makes the RES record illegal because pivot `y` vanished. Replacing it by the valid weakening `(x OR y OR z)` changes the exact resolvent to `(x OR z)`; retaining `(x)` is again illegal. Thus source entailment, implication, and satisfiability preservation are not congruences for proof syntax. Exact typed interfaces or consumer-aware recompilation are necessary.

This is a minimal original-rule legal counterexample to the overstrong **independent edge-preserving normalizer**, not a counterexample to every polynomial global compiler and not a refutation of `R_mix341`.

## ITERATE II — B3 and reflection

### Theorem 351.3 — canonical decider proof system characterization

Assume `SAT in P` via one fixed total correct uniform polynomial-time decider `A`, including malformed-input behavior. Define a verifier-style UNSAT proof system `Q_A` by

`Q_A(F, epsilon)=accept` iff `F` is a valid CNF and `A(F)=UNSAT`.

The only proof is the empty string. Correctness of `A` makes `Q_A` sound and complete, and its verifier is polynomial time. Hence `Q_A` is polynomially bounded.

For any fixed sound complete proof calculus `R`, the implication

`SAT in P => Wbar_R(N) is polynomial`

is exactly the additional assertion that, under this assumption, `R` has polynomial-size proofs for every `Q_A`-accepted input—that is, `R` p-simulates the canonical decider proof system in proof length. If an effective compiler is required, its construction/checking/output cost must also be polynomial.

This is a characterization, not a proof of the simulation. Cook–Reckhow gives existence of a p-bounded system such as `Q_A`; it does not force the preselected `R_mix341` to simulate it. Krajíček's `Alg(P)` makes the missing premise explicit as polynomial `P`-proofs of the algorithm's soundness formulas. Buss and Pich–Santhanam likewise identify feasible consistency/self-provability as additional structure. Assuming short `R_mix341` proofs of those formulas would presuppose the certificate phenomenon B3 is meant to derive.

### Theorem 351.4 — rejecting traces alone cannot be a uniform sound compiler

No compiler that sees only a machine code, one input, and a syntactically valid rejecting trace can both (i) emit a sound refutation for every such trace and (ii) omit any independently checked correctness/reflection premise. The correct decider and an unsound always-reject machine can have the same local trace on an UNSAT input, while the latter has the same kind of trace on a satisfiable input. Emitting a refutation there contradicts soundness. Therefore a general trace compiler must either reject some traces using semantic/correctness evidence or restrict to machines whose soundness is separately established.

For one fixed mathematically correct `A`, this theorem does not deny that another noncircular construction might exist. It only refutes the trace-only route and identifies the exact missing uniform premise. B3 remains OPEN.

## Established hard-family controls

Haken's theorem starts from the standard explicitly encoded unary pigeonhole CNF `PHP_(h+1)^h`. For all sufficiently large `h`, every ordinary shared-DAG Resolution refutation has `2^{Omega(h)}` lines. With binary variable indices the signed source length is `Theta(h^3 log h)`. The proof system allows arbitrary Resolution width, pivots, and DAG reuse, but no extension definitions, GF(2), AND3, LOCAL conversion, or arbitrary decider. Cook's Extended Resolution has polynomial PHP proofs, so Haken does not lower-bound the ER-equivalent strict root completion.

Odd Tseitin is the mandatory opposite control: ordinary Resolution may be hard, while `/341` extracts local parity factors and derives the contradiction by linear GF(2) addition. Res(oplus) lower bounds retain their exact proof-language restrictions. None transfers to all algorithms or B3 without the missing simulation.

## Computational verification

Artifacts:

- `experiments/arc/lspv5_351/typed_interface_referee351.py`;
- `experiments/arc/lspv5_351/verify_typed_interface_referee351.js`;
- `results/raw/arc/2026-11-04_1849_LSPV5_351_TYPED_INTERFACE.json`.

The producer passed **180,264 assertions**: the legal native witness, all 5,832 named-pivot Resolution instances on non-tautological clauses over four variables with 93,992 global alpha-renaming checks, 73,728 renamed GF(2) additions on five variables, every support-at-most-three factor truth table under support permutations (12,426 row checks), all 16 two-input DEF gates, both-label/trace controls, and malformed records. The independently authored Node verifier passed **34,606 checks**, including 23,328 clause-renaming and 11,264 affine-renaming cases. Producer semantic SHA-256: `0686df7c40e3bd55394aad9e1303041b335fc8b998495c0a778c8c2ca11bea45`.

Finite tests corroborate local semantics and parser controls only. They do not prove the asymptotic compiler, p-simulation, lower bound, or B3.

## Physical cost ledger

Let `N` be original CNF bits, `E` supplied proof/payload bits, `M=N+E`, and `L` output bits. A faithful translator must read and parse `M`, validate source identities, build a consumer index or rescan references, compile every exact public object, serialize `L`, and verify the target proof. A buffered implementation uses `O(M+L)` bits plus object overhead and polynomial time. A read-only-input implementation may rescan to save writable space but still pays all head/index/read operations and can use `O(M^2)` time before compilation. Neither schedule proves the FLMV target exponents.

Logical paid-node count does not charge these physical costs automatically. Exponential supplied intermediates remain legal only with their actual `E`-bit acquisition, checking, and output costs; compact equivalent roots are alternatives only when their exact interface can be certified and every consumer recompiled. Peak space includes all preprocessing and allocate-then-free phases.

## Precise proof status and next unresolved step

- **PROVED:** exact typed-interface preservation is a compositional grammar congruence.
- **PROVED, legal native counterexample:** implication-only, edge-preserving LOCAL normalization fails at three paid nodes.
- **PROVED, conditional strict grammar:** REFEREE350's root-to-ER translation survives after exact-interface consumer recompilation.
- **PROVED:** bare reject traces do not furnish a uniform sound proof compiler.
- **CHARACTERIZED, NOT PROVED:** under `SAT in P`, B3 for the fixed calculus requires its p-simulation of the canonical decider proof system / feasible reflection.
- **OPEN:** authoritative full native LOCAL payload/export grammar; unconditional all-rule polynomial translation; noncircular same-`R_mix341` B3; superpolynomial `Wbar_Rmix341`; P versus NP.

The next decisive step is not another hard family. It is either (i) an authoritative byte grammar proving all LOCAL internal gates private and every reusable wire separately paid, followed by a checked exact-interface compiler; or (ii) a legal native record whose exact public interface cannot be polynomially compiled. For B3, one must construct short `R_mix341` soundness/reflection proofs from the decider without assuming them, or find a genuinely different non-reflection argument.
