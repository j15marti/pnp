# GUARDED-ENTAILMENT-DECISION-SEPARATION-REFEREE330

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 22:48 PST**

**Status:** PROVED/EXACT same-source task-separation counterexample; PROVED/EXACT recognized-family ceiling; RESTRICTED proof-DAG isometry for ordinary Resolution; COMPUTATIONAL controls. B1/B2/B3 for fixed `R_mix341`, superpolynomial mixed `Wbar`, unrestricted SAT hardness and P versus NP remain OPEN. No task, schedule, state, identity, calculus rule or weight changed.

## Outcome first

The proposed post-acquisition invariant fails even without changing representations.

For any CNF `F=AND_i C_i` and fresh `t`, set

`G_t(F)=AND_i (not t OR C_i)`.

The same explicit source has three sharply different complexities:

1. `SAT(G_t(F))` is trivial for every `F`: set `t=0`.
2. Its exact boundary relation is `{0}` when `F` is UNSAT and `{0,1}` when `F` is SAT, so extracting that relation or deciding whether `G_t(F) entails not t` retains the UNSAT question.
3. In strict ordinary shared-DAG Resolution, the minimum paid nodes deriving `(not t)` from `G_t(F)` equal exactly the minimum nodes refuting `F`.

Taking `F` to be Haken's unary pigeonhole formulas yields satisfiable guarded sources with exponential ordinary-Resolution one-unit derivations, yet one fixed uniform all-input SAT decider recognizes the entire guarded family, scans it, and outputs the all-zero witness in linear time. No per-input label, per-length optimizer, nonuniform advice, semantic oracle or recoding is used.

Therefore exact continuation/entailment hardness is not a SAT-decision lower bound. Full source acquisition authenticates the input but does not force growing post-scan computation or produce an `R_mix341` refutation. This is a concrete counterexample concerning algorithm independence, not P != NP.

## Established hardness: exact scope

Haken (1985) concerns standard unary `PHP(h+1,h)` in **ordinary unrestricted shared-DAG Resolution**. The canonical explicit formula has:

- `h(h+1)` variables;
- `h+1` pigeon clauses and `h*binom(h+1,2)` collision clauses;
- signed DIMACS length `N_h=Theta(h^3 log h)`.

There are constants `c>0,h_0` such that for every `h>=h_0` and every ordinary Resolution refutation `pi` of this formula, `|pi|>=2^(c h)`. This is not an Extended Resolution, Res(XOR), `R_mix341` or arbitrary-machine result. Haken's own abstract notes the Extended Resolution shortcut. [Haken 1985](https://doi.org/10.1016/0304-3975(85)90144-6); [Cook 1976 short ER PHP proof](https://dl.acm.org/doi/10.1145/1008335.1008338).

The guarded CNF adds one negative guard literal to every source clause. Its length remains `Theta(N_h)`. Haken's lower bound transfers exactly only to the stated strict-Resolution unit-derivation task.

## Lemma 1: exact strict-Resolution guard isometry

Let `D_Res(F -> false)` be the minimum number of distinct inferred nodes in an unrestricted shared-DAG Resolution refutation, with source clauses free. Let `D_Res(G_t(F) -> not t)` be the analogous minimum deriving the guard unit.

**PROVED/EXACT:**

`D_Res(F -> false) = D_Res(G_t(F) -> not t)`.

Guard every line `C` of a refutation by replacing it with `(not t OR C)`. Resolution pivots and parent edges are unchanged, giving one inequality with exactly the same DAG nodes. Conversely, every source and every derived clause contains negative `t`; positive `t` never occurs, so `t` cannot be a pivot. Erasing negative `t` from every line yields a refutation of `F` with identical topology and node count.

This independently confirms LSPV-2/380, `research/coordination/2026-11-03_2208_LSPV2_GUARDED_PORT_RESOLUTION_ISOMETRY380_FIVE_ROLE_HANDOFF.md`, blob `503179fa1ce673684c08fdec406df572abe4de47`.

The isometry is proof-system restricted. Cook's binary-gate ER PHP proof embeds into the paid DEF+RES fragment of `R_mix341`, so `W_Rmix(PHP_h)` is polynomial, never lower-bounded by Haken. LSPV-3/385 proves the guard transport for **t-free** conservative DEF+RES, then gives an explicit t-dependent-definition step that breaks naive erasure. Its exact handoff is `research/coordination/2026-11-03_2224_LSPV3_GUARDED_ER_TFREE385_FIVE_ROLE_HANDOFF.md`, blob `7b96eb22f20630b86813cef408cc47baa9760406`. Full mixed guard isometry remains open and is not needed for the counterexample.

## Lemma 2: one uniform guarded-family SAT decider

Define one fixed program `A_guard` for all binary strings and all lengths:

1. Strictly parse the declared CNF grammar; reject malformed strings.
2. Stream-compare the source against the canonical generator for `G_t(PHP(h+1,h))`, inferring `h` from the header.
3. On exact match, output SAT and stream the all-zero assignment.
4. On mismatch, run a fixed complete exhaustive SAT fallback.

`A_guard` is total and correct on every valid SAT/UNSAT CNF and malformed string. On every guarded PHP member it uses `O(N)` sequential parsing/comparison and witness-output work, with `O(log N)` counters and output streaming. On arbitrary valid inputs the fallback may take `O(N 2^v)` time. This real exponential off-family cost is why the construction does not settle worst-case B2/B3.

The same general construction proves a recognized-monochromatic-family ceiling: if one fixed uniform recognizer decides membership in a family `H` of known same-label inputs in time `r(N)`, one fixed all-input decider recognizes `H`, emits the certified label, and otherwise uses a complete fallback. Its family time is `r(N)+O(output)`, regardless of proof hardness in a restricted calculus.

For unguarded canonical PHP, this unconditionally falsifies B1 with `R=ordinary Resolution`: family time is polynomial while `W_Res` is exponential. It does not falsify B2 or B3 because worst-case fallback time is exponential. For `R_mix341`, PHP has polynomial ER/DEF+RES proofs, so it is not a mixed-hard family at all.

## Lemma 3: continuation semantics and decision semantics diverge

The projected guard relation is

`Rel_t(G_t(F)) = {0}` if `F` is UNSAT, and `{0,1}` if `F` is SAT.

Thus a general exact relation extractor or `t=1` membership test decides UNSAT of `F`. But the ordinary SAT query asks only whether the relation is nonempty, and `0` is always a member. An exponential lower bound for deriving `(not t)`, or coNP-hardness of exact guard entailment, changes the computational task. It cannot be substituted for SAT decision hardness.

This is representation-independent in the narrow useful sense that no representation switch occurs: the exact same explicit guarded CNF is used for both tasks. It also explains why a semantic-only invariant collapses on closed formulas: every UNSAT formula represents constant false. Retaining a boundary prevents that collapse only by changing the query from nonemptiness to exact continuation behavior.

## Trace and certificate firewall

A full input read plus a valid rejecting computation trace is not an encoded `R_mix341` DAG. It lacks the fixed proof header, source-leaf identifiers, rule tags, parent IDs, explicit clause/XOR/circuit conclusions, DEF freshness/conservativity checks, bounded authenticated LOCAL-CONVERT support, source ancestry and contradiction sink.

For one fixed correct decider `A`, its exact UNSAT computation traces form a sound Cook--Reckhow-style proof system `Q_A`; trace validity proves only that `A` output UNSAT, while the external all-input correctness theorem supplies soundness. A polynomial translation `Q_A -> R_mix341` is precisely the missing computation-to-proof simulation. Full acquisition does not provide it.

The valid SAT guarded PHP control is decisive: it receives the same full scan and has hard strict-Resolution entailment, but no sound SAT refutation may exist.

## Fully charged resources

| Phase | Guarded-family branch | Off-family fallback |
|---|---|---|
| Grammar/source access | full `Theta(N)` scan | full parse plus paid rereads |
| Recognition | streaming expected-token comparison | mismatch dispatch |
| Representation | no exponential intermediate | exhaustive assignments may be generated lazily |
| Decision/output | SAT bit plus `Theta(v)` witness bits | SAT witness or UNSAT bit |
| Peak writable space | `O(log N)` counters with streaming output | `O(v+log N)` by rescanning, or `O(N)` cached parse |
| Two-way sequential input | no rewind on match | pay `O(N)` rewind then fallback scans |
| One-way input | match can stream | cache `Theta(N)` bits or require a streaming fallback |

Exponential fallback work is included, not excluded. It occurs off the recognized family and dominates `T_A^wc`. Lazy generation reduces storage only by paying recomputation and rereads. The logical unit-derivation DAG is never treated as physical runtime.

## Four falsifiers and verdicts

1. **A SAT antecedent cannot have an exponentially hard implied literal.** FALSE in strict Resolution: guarded PHP is SAT, while deriving `(not t)` inherits Haken exactly.
2. **Hard exact continuation implies hard SAT decision.** FALSE: `t=0` is a uniform witness for every guarded source.
3. **Full source acquisition or a rejecting trace yields a mixed refutation.** FALSE: acquisition authenticates input; trace-to-`R_mix341` translation is the missing B1/B3 simulation.
4. **Haken transfers to full `R_mix341`.** FALSE: Cook ER embeds into paid DEF+RES; GF(2) similarly defeats Tseitin transfer.

## B1/B2/B3 classification

- **Ordinary Resolution B1:** FALSE. One fixed PHP recognizer-plus-fallback decider is polynomial on every canonical PHP member while Haken gives exponential `W_Res`.
- **`R_mix341` B1:** OPEN. PHP and Tseitin do not witness hardness; their ER/GF(2) shortcuts are mandatory controls.
- **B2:** OPEN. The recognizer construction has exponential worst-case fallback, so `T_A^wc` absorbs the pointwise separation.
- **B3:** OPEN. Under `SAT in P`, a polynomial decider induces polynomial trace proofs `Q_A`; proving fixed `R_mix341` polynomially simulates them is exactly the missing bridge.

The guarded sources are SAT, so their unit-entailment hardness is not even in the UNSAT domain of B1. It is a firewall against substituting interface hardness for the target measure.

## Literature, project, Grok and Claude review

Primary sources reviewed: Haken's exact Resolution lower bound, Cook's short ER PHP proof, and Cook--Reckhow proof-system semantics. The scoped web search found no stronger theorem turning guarded entailment hardness into ordinary SAT decision hardness; absence is not novelty evidence.

Current peer evidence actually read:

- LSPV-3/384, `research/coordination/2026-11-03_2148_LSPV3_HALL_PHP_MIXED_UPPER384_FIVE_ROLE_HANDOFF.md`, blob `abf15c490b68d07766f8f405a31457fa631db9ab`: matching-sign inputs have polynomial mixed proofs through Hall/PHP/Cook.
- LSPV-5/329, `research/main/2026-11-03_2148_MAIN_END-TO-END-SIGN-ACQUISITION-REFEREE329.md`, blob `ecfe9f0d5a8df236abc91703dd45e406f3c6113e`: acquisition is exactly linear and representation-relative.
- LSPV-2/380 and LSPV-3/385 at the exact paths/blobs above: strict-RES and t-free-ER guard transports, with model restrictions explicit.
- REFEREE294/317/318: trace correctness, Cook--Reckhow transfer and reflection-family quantifier firewalls remain in force.

Current Grok `GROKPROOF/2026-11-04_0615_PROGRESS.md`, blob `6603e613853e7cc358b9b0181f06b19fa26ec39c`, explicitly leaves the universal fully charged all-input transformation open. Claude `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` (`95c2649...`), `2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727...`) and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6...`) concern conditional/restricted direct-product, portfolio and sequential-tape models. None supplies B1/B2/B3 or a trace-to-mixed compiler.

The scoped `github.com/openai` search found no relevant signed Resolution/DEF checker. Existing `drat-trim`/`drat2er` formats do not instantiate the fixed mixed grammar; absence is not novelty evidence.

## Finite controls

The producer checked canonical PHP and guarded PHP for `h=1,2,3`; UNSAT sources; all-zero SAT witnesses; unsatisfiable `t=1` fibers; exact recognizer scans; both projected relations `{0}` and `{0,1}`; two explicit strict-Resolution guard transports; nonfamily SAT and UNSAT fallback paths; and eight malformed rejections. It passed **32 assertions**. A separately written Node verifier passed **36 assertions**. Peak host RSS was 9,088 KiB. These are finite semantic/compiler controls, not a replay of Haken's asymptotic theorem.

Artifacts:

- `experiments/arc/lspv5_330/guarded_task_separation_referee330.py`
- `experiments/arc/lspv5_330/verify_guarded_task_separation_referee330.js`
- `results/raw/arc/lspv5_330/guarded_task_separation_referee330.json`

## Exact next gap

Established proof-hard families can test a proposed transfer but cannot supply it. The remaining viable target is worst-case and all-input: prove B3 for the same fixed, fully machine-specified `R_mix341`, or find a source-authenticated invariant that is not merely semantic relation complexity, acquisition, recognizable-family proof hardness, exact continuation extraction or trace validity. It must survive ER/GF(2), arbitrary adaptive solvers, compact/lazy representations and direct family recognition while charging every conversion and check. No such invariant is currently proved.

P versus NP remains **OPEN**.
