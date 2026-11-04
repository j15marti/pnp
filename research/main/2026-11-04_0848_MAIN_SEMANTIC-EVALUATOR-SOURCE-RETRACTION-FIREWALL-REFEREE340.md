# SEMANTIC-EVALUATOR-SOURCE-RETRACTION-FIREWALL-REFEREE340

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 08:48 PST**

**Status:** **PROVED/EXACT COUNTEREXAMPLE** to any reflection/specialization lemma whose evaluator premise is only extensional semantic correctness. A uniformly generated, polynomial-size satisfaction evaluator can be exact on every input yet specialize on a uniformly recognizable hard source to an auxiliary one-step contradiction instead of the source clauses. **PROVED/RESTRICTED COROLLARY:** for canonical unary pigeonhole formulas, no polynomial ordinary-Resolution backtranslation from these poisoned residual proofs to authentic source proofs exists. **PROVED/FINITE:** two independent implementations pass 73 assertions each. **OPEN:** full `R_mix341` restriction/source-retraction, B1, B2, B3, a superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP. No task, schedule, enabled state, ownership, calculus rule, or weight was changed.

## Outcome

The initial idea was to reduce B3 to short fixed-decider reflection formulas. Search showed that this is already present in LSPV-1/353, LSPV-1/361, LSPV-1/367 and REFEREE318, and that Krajíček's published transfer theorem explicitly requires an evaluator-to-source recovery property separate from semantic correctness.

The revised result isolates that premise by counterexample:

> Semantic equivalence of two satisfaction evaluators, uniform polynomial construction, honest traces, and proof restriction closure do not imply source-rooted proof transport. A separate polynomial **source retraction** is necessary.

This is a negative transfer theorem, not a lower bound on `R_mix341` or machine time. It explains exactly why a compact semantic evaluator cannot simply replace a witness-transparent source encoding in the B3 bridge.

## IDEA -> SEARCH -> ITERATE

### IDEA, stated before search

Fix a deterministic, total, correct polynomial-time SAT decider `A`. At length `n`, form the bounded false-rejection CNF

`H_A,n(X,U,V,Z) = Valid(X) AND SatEval(X,U,V) AND RejectTrace_A,n(X,Z)`.

**Proposed lemma:** if the fixed `R_mix341` has polynomial refutations of this one uniform family and proofs specialize with polynomial overhead, then B3 follows.

**Assumptions:** honest stuttering clock; explicit canonical validity circuit; uniform circuit/tableau generator; malformed inputs separated from SAT/UNSAT; authenticated restriction; source clauses recovered after specialization; full rule-by-rule `R_mix341` closure; proof bytes and all machine phases charged.

**Falsifiable prediction:** evaluator semantics plus an honest rejecting trace might be enough to make the specialized proof source-rooted.

### SEARCH and evidence that changed the idea

Primary literature actually read:

- Jan Krajíček, *A Note on SAT Algorithms and Proof Complexity*, Information Processing Letters 112 (2012), 490–493, DOI `10.1016/j.ipl.2012.03.009`. Its reflection formula is `Sat(a,phi) -> not Reject_M(w,phi)`. The paper warns that the SAT encoding must be chosen carefully and isolates four “decent proof system” properties. D1 is specialization, while D4 recovers a proof of the source formula from a proof of the evaluator statement. The proof uses both; neither follows from extensional correctness.
- Pavel Pudlák, *Reflection Principles, Propositional Proof Systems, and Theories*, arXiv:2007.14835. Reflection shortness is proof-complexity content, not a consequence of the represented machine's semantic correctness.
- Michal Garlík, *Resolution Lower Bounds for Refutation Statements*, MFCS 2019, LIPIcs 138:37, DOI `10.4230/LIPIcs.MFCS.2019.37`. Reflection/refutation statements themselves can be exponentially hard for ordinary Resolution.
- Stephen Cook and Robert Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50. Polynomial proof simulation is a property of encoded proof systems and translators, not of arbitrary correct decision traces.
- Armin Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308, DOI `10.1016/0304-3975(85)90144-6`.

Actual web queries:

- `reflection principles propositional proof systems p-optimal proof system bounded arithmetic primary paper PDF`;
- `Cook Reckhow reflection principle propositional proof systems soundness tautologies polynomial proofs`;
- `Krajicek Pudlak reflection principles p-optimal proof systems PDF`;
- `SAT solver computation trace soundness reflection principle proof complexity`;
- `resolution proofs closed under restrictions partial assignments proof complexity lemma`;
- `extended resolution closed under restrictions proof size substitution lemma`;
- `propositional proof systems closure under substitutions restrictions reflection principles`.

The available web-search service was used. A separately branded direct Google endpoint was not available in this environment, so this report does not claim a direct Google session.

Project/GitHub queries actually run:

- `reflection repo:j15marti/pnp`;
- `correctness tautology repo:j15marti/pnp`;
- `proof verifier org:openai`;
- `SAT certificate org:openai`;
- `DRAT org:openai`;
- `"reflection principle" org:openai`;
- `"Cook-Reckhow" org:openai`;
- `"proof system" "SAT" org:openai`.

The project search found the prior reflection equivalence and strict-Resolution guarded construction. The OpenAI search found general Lean/Cook–Levin machinery, including `openai/math/lean/OAI/Computability/DirectedFeedback/CookLevin/NPTableau.lean`, but no ER/LRAT/reflection compiler or source-retraction theorem applicable to `R_mix341`. No-result searches are not novelty evidence.

### ITERATE

The initial reflection lemma was not new. The search changed the target from “short reflection implies B3” to the missing D4/source-retraction premise. The revised idea was then attacked with a uniform semantic poison, proved below, and replayed independently on all two-variable CNFs generated by four assignment-blocking clauses.

The falsifiable prediction failed: two extensionally identical evaluators can have radically different specialized source semantics. The corrected conditional reflection theorem therefore needs all of:

1. honest clock coverage;
2. short `R_mix341` reflection proofs;
3. full typed proof specialization;
4. a polynomial authenticated source retraction from the specialized evaluator to the original CNF.

SAT in P supplies a decider and traces, not items 2–4.

## Exact published lower-bound anchor

For `h` holes and `h+1` pigeons, canonical unary `PHP(h+1,h)` uses variables `x_(i,j)`. It contains one width-`h` positive pigeon clause per pigeon and, for every hole and pair of pigeons, the binary collision clause `(not x_(i,j) OR not x_(k,j))`. There are `h(h+1)` variables and `Theta(h^3)` explicit clauses. With ordered signed binary variable indices, the canonical encoding has `N_h=Theta(h^3 log(h+2))` bits.

Haken's theorem has the quantifiers:

`there exist c>0,h0 such that for every h>=h0, every ordinary Resolution refutation of PHP(h+1,h) has at least 2^(c h) lines.`

The model is ordinary unrestricted shared-DAG Resolution: authentic source clauses and binary resolution on a complementary pivot, with arbitrary derived-clause width, pivot choice and DAG reuse. It has no extension variables, GF(2) rows, circuit axioms, semantic inference, SAT oracle or arbitrary machine step. Thus the strength is `2^Omega((N_h/log N_h)^(1/3))` line lower bounds for this explicit family in ordinary Resolution.

It is not an Extended Resolution, `Res(oplus)`, `R_mix341`, or all-algorithm SAT lower bound. Cook's polynomial Extended-Resolution PHP proofs are a mandatory escape control. Odd-Tseitin formulas likewise have exponential ordinary-Resolution hardness but exact linear authenticated GF(2) proofs in fixed `R_mix341`.

## The semantic-poison theorem

Let `K_h` be any uniformly generated, polynomial-time recognizable UNSAT CNF family; canonical unary `PHP(h+1,h)` is the established anchor. Let

`Sat_h(X,U,V)`

be any uniform exact satisfaction relation at the relevant source length: for a valid source `X` and assignment `U`, an auxiliary witness `V` exists exactly when `U` satisfies `X`. Let `Eq_h(X)` be the uniform bitwise equality test `X=K_h`. Define

`Sat*_h(X,U,V) = (not Eq_h(X)) AND Sat_h(X,U,V)`.

### Theorem 1: exact semantic equality

For every valid `X,U`,

`exists V Sat*_h(X,U,V) iff exists V Sat_h(X,U,V)`.

**Proof.** If `X != K_h`, the added factor is true, so the relations are identical. If `X=K_h`, no assignment satisfies `K_h` because `K_h` is UNSAT; both existential relations are false. The equality circuit has linear size and a uniform generator, so the modified evaluator remains uniform and polynomial size. QED.

This construction is not a per-input answer table or a nonuniform per-length optimizer. One fixed algorithm generates `K_h`, its equality comparator and the evaluator for every `h`; the relation remains exact on every source string of the declared length.

### Theorem 2: specialization need not retract to the source

Encode `Sat*_h` by a bounded-fanin circuit with equality-output wire `r` and output wire forced true. Fix `X=K_h`, fix all equality/evaluator wires to their actual values, and fix an honest rejecting trace. The equality circuit authenticates `r=1`, while the forced true value of `Sat*_h` requires `r=0`. After ordinary restriction and local simplification, the surviving contradiction can be exactly the opposite units

`(r)` and `(not r)`.

They have a one-inference Resolution refutation. The actual clauses of `K_h` need not occur in the residual at all. Therefore extensional evaluator correctness, trace honesty and restriction closure do not yield a proof from the authentic source clauses.

The conclusion is intensional: the evaluator representation has lost source provenance even though its Boolean relation is exact.

### Corollary: no polynomial ordinary-Resolution source backtranslation

Take `K_h=PHP(h+1,h)`. Suppose a uniform polynomial-overhead translator converted every specialized poisoned-evaluator Resolution refutation into an ordinary Resolution refutation from the authentic `K_h` clauses. Applying it to the one-step opposite-unit proof would give `poly(N_h)`-line PHP refutations, contradicting Haken's `2^Omega(h)` lower bound. Hence no such ordinary-Resolution translator exists.

This corollary is deliberately restricted. It says nothing about Extended Resolution or full `R_mix341`, both of which contain relevant escapes. It is also not machine hardness: it proves that one proposed proof backtranslation cannot have polynomial overhead.

## Four proposed falsifiers and dispositions

1. **Extensional equality of evaluators guarantees source-rooted specialization. — FALSE.** The poison theorem is an explicit uniform counterexample.
2. **An honest rejecting trace repairs the evaluator. — FALSE.** The trace only fixes `A(K_h)=UNSAT`; the opposite-unit contradiction still lives in the equality/evaluator wires.
3. **Restriction closure alone supplies D4. — FALSE.** Restriction faithfully preserves the poisoned auxiliary contradiction; it does not turn auxiliary leaves into authentic PHP clauses.
4. **An exponential backtranslation is evidence of SAT runtime hardness. — FALSE.** It establishes only failure of that proof-transfer route. The physical decider may use a compact recognizer, GF(2), circuits, definitions or another algorithm.

Additional controls: a too-short clock can leave a clock contradiction; malformed strings require a paid `Valid` circuit and a distinct MALFORMED output; a per-source constant answer circuit is forbidden; a uniform equality comparator for a fixed family is allowed and fully charged.

## Fixed `R_mix341` consequence

The unchanged target is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. It includes strict Resolution, bounded-support `AND3`, GF(2), explicit constant-support `LOCAL-CONVERT`, and fresh conservative two-input `DEF` gates, with unit paid inference nodes and shared-DAG reuse.

The present theorem does not show `R_mix341` hardness. It shows that a candidate B3 proof cannot use only semantic evaluator correctness. A valid positive theorem must prove a typed source retraction for every evaluator/representation used and a polynomial specialization/compiler for every mixed rule. Current unresolved cases include GF(2) zero-row normalization, fixed constants and aliases in `DEF`/`AND3`, and the exact public payload semantics of `LOCAL-CONVERT`.

## Fully charged physical ledger

Let the compact machine/evaluator/equality circuit have `G=poly(N)` gates. A constant-clause Tseitin encoding has `Theta(G)` records and `Theta(G log(G+2))` explicit indexed bits.

| phase | explicit materialization | compact/lazy alternative |
|---|---:|---:|
| generate equality/evaluator/trace circuit | at least all `Theta(G log G)` output bits | generator state plus paid record generation per query |
| parse and validate source | `Omega(N)` adversarial bit reads | no free promise; queried bits and eventual exact validation charged |
| specialize wires | `Theta(G)` assignment bits and a full proof pass | recompute wire values per use; repeated work charged |
| proof output | every encoded proof bit, not only logical nodes | DAG IDs/cache or recomputation charged |
| verification | `Omega(formula bits + proof bits)` reads plus rule checks | streaming schedule, index map and random access explicitly charged |
| peak writable space | materialized circuit, trace, proof and maps | smaller state is allowed, but rereads/recomputation count as work |

An exponential truth table or intermediate representation is allowed, but its construction, bit access, output and peak space are exponential and it is dominated here by the compact comparator/circuit. Conversely, a one-node ideal residual is not one unit of physical runtime. This report uses the one-node residual only to refute source transport.

## Finite independent verification

The finite control uses two variables and the four full clauses, one falsified by each assignment. Their conjunction `K` is clause-minimally UNSAT. Exhaustive checks cover all 16 clause subsets and all four assignments:

- 64 evaluator pairs satisfy `Sat*(X,U)=Sat(X,U)`;
- a SAT control has models;
- the four-clause `K` has exact minimum ordinary shared-DAG Resolution cost 3;
- the specialized auxiliary residual `(r),(not r)` has exact cost 1;
- five malformed masks are rejected;
- Python: 73 assertions PASS;
- independent JavaScript: 73 checks PASS.

Artifacts:

- `experiments/arc/lspv5_340/semantic_evaluator_source_retraction_referee340.py`;
- `experiments/arc/lspv5_340/verify_semantic_evaluator_source_retraction_referee340.js`;
- `results/raw/arc/lspv5_340/semantic_evaluator_source_retraction_referee340.json`, SHA-256 `fea581400d0ff07759044a38716724671fbab4637d21fca527a8492ee23ca306`.

These controls validate the elementary construction and exact finite optima. They do not reprove Haken, prove a mixed-calculus lower bound, or certify machine hardness.

## B1/B2/B3 classification

| obligation | result after this run |
|---|---|
| semantics-only specialization/source transport | **FALSIFIED** |
| conditional short reflection + honest specialization + source retraction -> B3 | **PROVED/CONDITIONAL**, already localized by prior work |
| SAT in P -> short reflection proofs for fixed `R_mix341` | **OPEN** |
| full `R_mix341` restriction and source retraction | **OPEN** |
| B1 for fixed `R_mix341` | **OPEN** |
| B2 for fixed `R_mix341` | **OPEN** |
| B3 for fixed `R_mix341` | **OPEN** |
| superpolynomial `Wbar_Rmix341`; unrestricted SAT lower bound; P versus NP | **OPEN** |

The quantifier correction is important: without first assuming or fixing an externally correct polynomial-time `A`, “B3 iff short reflection for a P-time A” can be vacuous when SAT is not in P. The proved positive statement is conditional on one fixed correct `A` and all source-transport premises. No `A_N`, advice, or per-input hardcoded answer is used.

## Project, five-role, Grok and Claude review

Issue #3 was read through the current peer updates. Relevant exact project paths include:

- `research/main/2026-11-03_1048_MAIN_REFLECTION-FAMILY-EQUIVALENCE-REFEREE318.md`;
- `research/agents/lspv-1/2026-11-03_0956_LSPV-1_RESTRICTION_STABLE_REFLECTION367.tex`, blob `64f4e87a...`;
- `research/agents/lspv-1/2026-11-03_0356_LSPV-1_UNIVERSAL_MASK_REFLECTION_ER361.tex`;
- `research/coordination/2026-11-03_0032_LSPV1_GODEL_REFLECTION_B3_FIREWALL357_FIVE_ROLE_HANDOFF.md`;
- `research/main/2026-11-02_1148_MAIN_TRACE-CORRECTNESS-FIREWALL-REFEREE294.md`.

All five current role agents checked the candidate and the current external review folders. LSPV-1 confirmed the duplicate reflection theorem and quantifier requirements. LSPV-2 audited the compact evaluator, affine escapes and source replay. LSPV-3 identified the poison construction and Krajíček D4. LSPV-4 supplied the complete explicit/lazy time-space ledger and clock controls. LSPV-5 attacked reject-all, appended contradictions, underclocking, nonuniform `A_N`, and malformed gaps. Their agreement is evidence; the proof above is assessed independently.

The latest Grok file actually reviewed was `GROKPROOF/2026-11-04_1518_PROGRESS.md`, blob `4e2bb9d941295f620a64e078117d29244caf4fba`. It leaves the arbitrary-`A`, fully charged all-input transfer open and supplies no source-retraction theorem.

Claude has no post-October-28 applicable bridge. Files actually checked were:

- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

They concern restricted direct-product, portfolio/alternation-trading and one-tape models. They do not prove reflection shortness, source retraction, B3, or unrestricted SAT hardness.

## Precise next gap

Construct one natural, uniform, compact satisfaction evaluator for general CNF together with a polynomial authenticated `R_mix341` source retraction satisfying the analogue of Krajíček's D4, and prove typed specialization for every rule actually used. The evaluator must survive malformed inputs, compact/lazy circuits, GF(2), definitions, shared DAGs and full encoded-cost accounting. Only after that source theorem is available does it make sense to attack short reflection proofs. An exponential backtranslation is a failed transfer, not evidence for P != NP.

