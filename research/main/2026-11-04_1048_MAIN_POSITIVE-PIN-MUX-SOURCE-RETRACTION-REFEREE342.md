# POSITIVE-PIN-MUX-SOURCE-RETRACTION-REFEREE342

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 10:48 PST**

**Status:** **PROVED/RESTRICTED.** In the unchanged fixed `R_mix341`, source bits of one declared explicit fan-in-two indexed evaluator can be replaced by distinct *positive* fresh variables, fixed to either truth value by paid DEF/RES derivations. A 2:1 mux then exposes its selected input by an eight-node DEF/RES macro beyond the shared false-pin setup. Consequently a transparent evaluator made from explicit masks, acyclic muxes and private OR/AND aggregation has a polynomial authenticated source retraction: after deriving its root from the authentic CNF, an arbitrary downstream mixed proof is copied unchanged. This yields an explicit D4-style reduction from one universal reflection family `H_(A,N)` to authentic sources, without substituting inside the mixed proof. **FALSIFIED:** the initial `O(N)` overhead prediction and literal equality with REFEREE341's `T(F)`. **PROVED COUNTEREXAMPLE:** full specialized-evaluator length is not representation- or algorithm-independent, even if every padded gate is syntactically root-reachable. **OPEN:** short `R_mix341` reflection from `SAT in P`, B1/B2/B3, a superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP.

No task, schedule, enabled state, ownership, rule, weight, or role changed.

## Outcome

The run removes one real but representation-specific transfer obstacle. A source compiler need not constant-fold an indexed evaluator to the clause-private `T(F)`. It may retain the evaluator topology, materialize every source bit as a paid positive variable, derive local mux aliases, derive the evaluator root from the authentic clauses, and splice any downstream `R_mix341` refutation without translating its RES, AND3, GF(2), LOCAL-CONVERT, or DEF nodes.

This is not representation-independent hardness. It works for one deliberately transparent architecture. Arbitrary semantically correct evaluators remain excluded by REFEREE340's poison counterexample, and `SAT in P` still does not imply polynomial reflection proofs for the same fixed calculus.

## IDEA -> SEARCH -> ITERATE

### IDEA, stated before search

Fix a uniform indexed evaluator with source-bit units, signed literal muxes, private clause OR trees, and a global AND tree. Try to specialize it to the exact private evaluator `T(F)` with `O(N)` paid nodes.

Assumptions: full two-input Tseitin facets; fresh outputs; canonical padding; no semantic merging, free constants, weakening, SAT oracle, or per-input rule; one uniform compiler; valid sources authenticated separately.

Falsifiable predictions:

1. fixed source bits and mux aliases have constant-size local proofs;
2. raw specialization is literally `T(F)`;
3. the total compiler is linear in the binary source length.

### SEARCH

Primary sources actually read:

- Jan Krajicek, *A Note on SAT Algorithms and Proof Complexity*, IPL 112 (2012), 490--493, DOI `10.1016/j.ipl.2012.03.009`. Its D4 source-recovery condition is separate from evaluator correctness.
- Stephen Cook and Robert Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36--50. Polynomial simulation is an explicit encoded proof translation.
- Christian Bessiere, George Katsirelos, Nina Narodytska and Toby Walsh, *Circuit Complexity and Decompositions of Global Constraints*, IJCAI 2009. Complete input assignments propagate through standard circuit encodings; this does not itself prove source retraction.
- Jan Krajicek's D1--D4 formulation and the ordinary-Resolution restriction literature were used only within their stated proof models; no full-mixed restriction theorem was inferred.

Actual web queries included `indexed evaluator mux constant alias source replay`, `primary paper Tseitin encoding propagation complete multiplexer circuit CNF unit propagation`, `Extended Resolution closed under restrictions substitution extension variables`, `Pippenger Fischer circuit simulation`, and `Krajicek D4 source proof evaluator`. A separately branded direct Google UI was unavailable, so the available general web search was used without claiming a direct Google session.

Project files actually read include:

- `research/main/2026-11-04_0948_MAIN_CLAUSE-PRIVATE-EVALUATOR-COST-REFLECTION-REFEREE341.md`, blob `9010e7474166f2d6f558315186f1621586810044`;
- `research/main/2026-11-04_0848_MAIN_SEMANTIC-EVALUATOR-SOURCE-RETRACTION-FIREWALL-REFEREE340.md`;
- fixed calculus `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`;
- `research/agents/lspv-1/2026-11-02_2200_LSPV-1_PIN_AND_REPLAY_RESTRICTION_FREE_BRIDGE354.tex`;
- `research/agents/lspv-2/2026-11-03_0016_LSPV-2_TWO_RAIL_GATE_SLOT_RT354.tex`;
- `research/agents/lspv-1/2026-11-03_0004_LSPV-1_MASKED_OR_REFLECTION_REPLAY356.tex`, blob `63dc7545ad7aad2f4b4cd53154f711bb85773c39`;
- `research/agents/lspv-1/2026-11-03_0356_LSPV-1_UNIVERSAL_MASK_REFLECTION_ER361.tex`, blob `f1132a5fae81148de380bcd43289e87d34b65008`;
- issue #3 through the current LSPV-1/393, LSPV-2/395, LSPV-3/399 and LSPV-4/392 updates.

OpenAI GitHub queries included `Tseitin multiplexer CNF proof checker`, `extended resolution substitution SAT proof`, `SAT proof checker mux CNF`, and `CookLevin formulaBits evaluator`. No applicable `R_mix341` compiler was found. One AIG compiler in `openai/math` was an implementation clue only, not a theorem.

### ITERATE

Search falsified the proposed obstruction and two predictions. LSPV-1/354 and LSPV-2/RT354 already show that paid two-rail pins repair constants and aliases in restricted ER2 banks. Raw mux restriction is not syntactically `T(F)`, but it has a constant-size authenticated alias proof. The revised target therefore became a positive-variable pin bank that permits literal alpha-renaming, followed by a retained-topology mux compiler. This avoids needing signed substitution through arbitrary downstream mixed nodes.

The linear prediction also failed: an explicit `n`-to-1 mux uses `n-1` 2:1 muxes, hence three DEF gates per internal mux. With `L` literal slots and `N=Theta(L log n)` input bits, `L=Theta(n)` gives `G=Theta(Ln)=Theta(N^2/log^2 N)`. The compiler is polynomial in the declared evaluator size, not linear in source bytes.

## Lemma 1: paid positive source-bit bank

Assume the valid source has two occurring variables `x,y`; the finitely many smaller-variable UNSAT cases have direct constant-size refutations. Introduce

`u <-> x AND y`, `v <-> not x AND not y`, and `z <-> u AND v`.

Three DEF and three RES nodes derive `(not z)`:

1. `(not u OR x)` and `(not v OR not x)` derive `(not u OR not v)`;
2. resolve with `(not z OR u)`;
3. resolve with `(not z OR v)`.

Create four distinct false wires `f_i <-> z AND l_i`, for `l_i` in `x,not x,y,not y`. Each costs one DEF and one RES to derive `(not f_i)`. Define two true wires

`t_1 <-> not f_1 AND not f_2`, `t_2 <-> not f_3 AND not f_4`.

Each costs one DEF and two RES to derive its positive unit. The shared base therefore costs exactly 20 nodes.

For every source bit create a fresh positive variable `q_i`:

- bit 0: `q_i <-> z AND t_1`, costing one DEF and one RES to derive `(not q_i)`;
- bit 1: `q_i <-> t_1 AND t_2`, costing one DEF and two RES to derive `(q_i)`.

For `B_0` zero bits and `B_1` one bits the exact displayed cost is

`20 + 2 B_0 + 3 B_1 <= 20 + 3B`.

This is less economical than the earlier signed two-rail bank, but it has the useful property that every evaluator source variable is replaced by an ordinary fresh variable `X_i -> q_i`, not by a negated variable. Hence every downstream typed formula retains exactly the same syntax up to alpha-renaming.

## Lemma 2: exact mux alias

Let a shared false wire `c` have unit `(not c)`. For a left-selected mux introduce

`a <-> not c AND x`, `b <-> c AND y`, `q <-> a OR b`.

The three DEF nodes expose all full facets. Two RES nodes with `(not c)` derive `(a OR not x)` and `(not b)`. Three further RES nodes derive

`(q OR not x)` and `(not q OR x)`.

Thus `q <-> x` is authenticated with exactly three DEF plus five RES nodes beyond the shared false unit. Right selection is symmetric. Raw restriction is **not** literally a direct selected leaf: it retains alias and dead-branch clauses. Therefore literal equality with `T(F)` is false, while polynomial source replay survives.

## Restricted indexed-evaluator source retraction

Fix once and for all a transparent evaluator family `E_N` with:

1. `B(N)` explicit source-bit positions;
2. `G(N)=poly(N)` explicit two-input Tseitin gates;
3. acyclic 2:1 mux networks for signed literal lookup and masks;
4. private binary OR trees for clauses and a private binary AND tree for the formula;
5. no semantic gate merging after specialization.

For valid `F`, retain the full evaluator definition bank and add the appropriate source-bit units and positive root unit; call this `U_F`. Materialize source bits using Lemma 1, introduce all evaluator gates topologically by paid DEF, use Lemma 2 along each selected mux path, compose adjacent aliases by two RES steps per level, resolve the resulting literal-to-slot implications against each authentic source clause, and use REFEREE341's OR/AND replay to derive the evaluator root.

Now let `pi` be any `R_mix341` refutation of `U_F`. Map every bit unit to the corresponding derived `q_i` unit, every evaluator clause to its charged DEF facet, and the root unit to the source-derived root. Alpha-rename proof-owned variables and copy every later node unchanged. Since the formulas and antecedents are identical, RES, AND3, GF(2), LOCAL-CONVERT and DEF nodes need no rule translation.

Therefore, for this declared architecture,

`W_Rmix341(F) <= W_Rmix341(U_F) + poly(N)`, 

with a direct bound `O(B+G+P+L)`, where `P` is the total selected mux-path length and `L` the literal-occurrence count. This is the D4-like source retraction that REFEREE341 lacked, but only for `E_N`. It is not a theorem about arbitrary semantically correct, merged, implicit, shared, or time-multiplexed evaluators.

Malformed inputs still require a paid validity/parser circuit in the total decider. The retraction theorem applies to valid source formulas and does not treat an inactive mask as proof of syntactic validity.

## Universal reflection source-retraction corollary

The preceding compiler can be made into one explicit family-wide D4 reduction. Fix a canonical padded source encoding. For cutoff `N` let

`P = 2^ceil(log_2 max(2,N))`, `d=log_2 P`, and `B=(d+2)P^2+P`

be the padding, mux depth, and pin count of the declared transparent evaluator. Fix one total correct decider `A` with an explicit uniform bounded-fanin clocked circuit family. Let `H_(A,B)` be the authentic two-input gate CNF, with positive root, for

`Valid(s) AND Reject_A(s) AND Eval(s,y)`.

For every valid UNSAT `F` of length at most `N`, every supplied `R_mix341` refutation `pi` of `H_(A,B)` compiles uniformly into a refutation of the exact private `T(F)` without modifying any downstream node of `pi`:

1. the positive root of `T(F)` recovers all clauses of `F` in exactly `L+m-2` RES nodes (`L` occurrences, `m` clauses);
2. Lemma 1 derives the `B` pinned source units as positive variables;
3. every `H` gate is introduced by DEF and Valid/Reject are evaluated on the pinned record;
4. a depth-`d` mux derives equivalence with its pinned leaf in `5d+2(d-1)=7d-2` RES steps; sign, mask, clause OR and formula AND replay derive the Eval and conjunction roots;
5. the complete original `pi` is alpha-renamed and copied byte-for-byte at the logical-node level.

Writing `G_H` for all `H` gates and `G_VR` for Valid/Reject gates, the displayed construction has the explicit polynomial upper bound

`P_A(F) <= G_H + 2G_VR + 2B + L(8d+8) + L + m + 3P + O(1)`

using the more economical signed pin bank; using the positive-variable bank above changes only the polynomial pin term and makes unchanged mixed-node replay immediate. Therefore

`W_Rmix341(T(F)) <= W_Rmix341(H_(A,B)) + poly_A(N)`,

and REFEREE341 yields

`W_Rmix341(F) <= W_Rmix341(H_(A,B)) + poly_A(N) + 3(L-1)`.

The quantifiers are family-wide: one fixed `A`, one fixed evaluator/compiler, every valid UNSAT `F` at the cutoff, and every supplied proof `pi`; minimization occurs only after the transformation. Exponentially large `pi` is allowed and copied at its full encoded cost.

This is not B1: `H_(A,B)` uses a worst-case clock and is not bounded by pointwise `T_A(F)`. It is not B2 until `W(H_(A,B))` itself is bounded. It gives only the conditional implication

`SAT in P via A` **and** `W_Rmix341(H_(A,B_N))=poly(N)` `=> Wbar_Rmix341(N)=poly(N)`.

The second conjunct—short reflection proofs in the same fixed calculus—is still open and is not supplied by `SAT in P`.

## Counterexample: full materialized evaluator length is not intrinsic

Let any correct uniform evaluator `E_N` have output `c`. Append a uniform `h(N)`-gate circuit with output `p`, then set

`t = p AND not p`, `y = c OR t`.

Every added gate can be made a syntactic ancestor of `y`, yet `y=c` on every valid, SAT, UNSAT and malformed input. With `h(N)=2^N`, a compiler required to emit every specialized gate writes `Omega(h(N) log h(N))` bits and spends at least that output time; retaining them costs the same-order peak space. A fixed uniform lazy solver recognizes the final local identity and evaluates only `E_N`, never addressing the padded subcircuit. If the padding is explicit input, its bytes are honestly charged to input length; if it is an implicit family, the compact alternative bypasses it.

Hence full specialized-evaluator length, even with root reachability, is not representation- or algorithm-independent. This falsifies any B1/B2/B3 argument based solely on compulsory full materialization. It does not refute a future minimum-over-representations or proof-reachable invariant.

## Exact published lower-bound anchor

For `h` holes and `h+1` pigeons, unary `PHP(h+1,h)` has `h(h+1)` variables, `h+1` positive pigeon clauses, and `h binom(h+1,2)` binary collision clauses. With ordered signed binary variable indices its explicit encoding length is `N_h=Theta(h^3 log(h+2))`.

Haken's theorem states: there exist constants `c>0,h_0` such that for every `h>=h_0`, **every ordinary unrestricted shared-DAG Resolution refutation** of this explicit CNF has at least `2^(c h)` lines. The system has authentic source clauses and binary Resolution only. It has no extension variables, GF(2), circuit definitions, semantic rule, SAT oracle, or arbitrary algorithm. The encoded-length strength is therefore `2^Omega((N_h/log N_h)^(1/3))` for this family in ordinary Resolution.

It is not an Extended Resolution, `Res(oplus)`, `R_mix341`, or machine lower bound. Polynomial Extended-Resolution PHP proofs are the mandatory escape. Odd expander Tseitin formulas likewise have exponential ordinary-Resolution lower bounds but compact authenticated GF(2) proofs; the established fixed-calculus result is linear mixed cost, not unrestricted computation.

## Finite verification

The Python producer/checker generated all 511 source-bit patterns of widths zero through eight. It verified the exact formula `20+2B_0+3B_1`, both truth values, fresh outputs, every DEF facet, and every Resolution step. It also generated both selector values and all signed choices of two mux inputs, eight mux records total, and checked the exact eight-node macro.

Both-label controls were the two-variable four-blocker UNSAT formula and a SAT sibling. Five malformed bit lists were rejected. An independently written JavaScript verifier reconstructed all eight mux records and passed 204 checks.

Artifacts:

- `experiments/arc/lspv5_342/source_bit_materialization_referee342.py`;
- `experiments/arc/lspv5_342/verify_source_bit_materialization_referee342.js`;
- `results/raw/arc/lspv5_342/source_bit_materialization_referee342.json`, SHA-256 `e4d0fd190ccb480af48f2fe71822ca25f7cbb9edaffd35f636ff3b3c1da1a717`.

These finite controls validate the displayed local derivations, not global minima, short reflection, or Haken's theorem.

## Fully charged physical ledger

| phase | explicit retained evaluator/proof | compact or lazy alternative |
|---|---:|---:|
| source validation | at least all adversarial source bits; malformed/count/index checks | streaming saves space, not source reads |
| positive pin bank | `Theta(B log(V+G+B))` encoded bits | generate per use; repeated generation/access charged |
| gate definitions | `Theta(G log(V+G+B))` encoded bits | query only referenced gates; generator and address work charged |
| mux/root replay | bounded-width records plus source-clause payload; `O(B+G+P+L)` ideal nodes | lazy clauses shift work to reconstruction/checking |
| proof splice | reads/writes the old proof plus new IDs | streaming may recompute and can lose DAG sharing |
| verification | reads every emitted proof bit and validates every rule/payload | no free virtual clause, GF(2) row, or LOCAL-CONVERT payload |
| peak space | full source, definition bank, replay and ID map if retained | source cache plus active records; rereads/recomputation charged |
| exponential intermediate | exponential honest construction/output/access/space | allowed, but compact alternatives must be checked |

The ideal logical node bound is not physical runtime. Conversely, no peak-space lower bound follows merely from the index width of an implicit exponential evaluator if the algorithm never addresses it.

## B1/B2/B3 classification

| obligation | result |
|---|---|
| positive-variable source-bit materialization | **PROVED/RESTRICTED**, exact `20+2B_0+3B_1` macro |
| 2:1 mux selected alias | **PROVED/RESTRICTED**, exact 8 nodes beyond shared false unit |
| source retraction for declared transparent `E_N` | **PROVED/RESTRICTED**, polynomial overhead |
| universal `H_(A,N)` to authentic source retraction | **PROVED/RESTRICTED**, polynomial D4-style compiler |
| literal specialization to exact `T(F)` | **FALSIFIED** |
| `O(N)` full-mux normalization | **FALSIFIED**; explicit architecture can be `Theta(N^2/log^2 N)` |
| full materialized evaluator length as intrinsic work | **FALSIFIED** by root-reachable padding |
| arbitrary sound representations/evaluators | **OPEN/false under semantics alone** |
| SAT in P -> short fixed-`R_mix341` reflection | **OPEN** |
| B1 / B2 / B3 | **OPEN** |
| superpolynomial `Wbar_Rmix341`, unrestricted SAT lower bound, P versus NP | **OPEN** |

The next proof obligation is now narrower: prove polynomially short `R_mix341` refutations for the one fixed universal reflection family of a uniform correct polynomial SAT decider, or give a new invariant that survives compact/implicit representations without charging syntactic padding. The present run supplies neither.

## Five-role, Grok and Claude review

All five specialists followed IDEA -> SEARCH -> ITERATE. LSPV-1 audited quantifiers and the B1/B2/B3 ceiling; LSPV-2 gave the direct mux compiler and quadratic explicit-size counterexample; LSPV-3 checked raw residual semantics and the exact alias; LSPV-4 supplied the materialization counterexample and full physical ledger; LSPV-5 isolated nonprime residual clauses, malformed-index behavior, and mixed-rule caveats.

The latest Grok file actually reviewed was `GROKPROOF/2026-11-04_1518_PROGRESS.md`, blob `4e2bb9d941295f620a64e078117d29244caf4fba`; it leaves the arbitrary-decider, fully charged all-input transform open and supplies no source retraction or B3 theorem.

Claude files actually checked were:

- `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`;
- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

They concern restricted direct-product, transport/alternation and one-tape ledgers. None proves indexed-evaluator retraction, reflection shortness, B3, or unrestricted SAT hardness.
