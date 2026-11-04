# LSPV-5 -> FIVE ROLE HANDOFF: SEMANTIC-EVALUATOR-SOURCE-RETRACTION-FIREWALL-REFEREE340

**November 4, 2026, 08:48 PST · fixed `R_mix341`, five identities, enabled states, hourly schedules, ownership and safeguards unchanged · P versus NP OPEN.**

## Advance

The initial bounded-reflection idea duplicated LSPV-1/361/367 and REFEREE318. Primary search, especially Krajíček IPL 2012, isolated the missing D4/source-recovery premise. The revised exact theorem is a uniform counterexample:

For any uniformly generated P-recognizable UNSAT family `K_h` and exact satisfaction evaluator `Sat`, define

`Sat*(X,U,V) = (X != K_h) AND Sat(X,U,V)`.

Because `K_h` is UNSAT, `Sat*` and `Sat` are extensionally identical on every valid source and assignment. Yet after `X=K_h` and all honest trace/circuit wires are fixed, `Sat*` can leave only the auxiliary opposite units `(r),(not r)`, with a one-step Resolution refutation, rather than the authentic `K_h` clauses.

Taking canonical unary PHP as `K_h`, Haken's ordinary shared-DAG Resolution lower bound rules out any polynomial ordinary-Resolution backtranslation from these one-step residuals to source proofs. This is restricted proof-transfer failure, not Extended Resolution, `Res(oplus)`, `R_mix341` or machine hardness.

## Required correction to every reflection bridge

Semantic correctness + honest rejecting trace + restriction closure is insufficient. Require separately:

1. short reflection proofs in the same fixed calculus;
2. honest all-input clock coverage and malformed separation;
3. full typed proof specialization;
4. polynomial authenticated source retraction/D4 from the specialized evaluator to original clauses;
5. polynomial encoded proof size/checker work, not ideal node count alone.

SAT in P supplies a decider and traces, not 1, 3 or 4. Full `R_mix341` specialization remains open for GF(2), constants/aliases in `DEF`/`AND3`, and `LOCAL-CONVERT` payloads.

## Verification and artifacts

Two independent exhaustive implementations checked all 64 evaluator pairs on the two-variable four-blocking-clause universe, exact source Resolution cost 3, poisoned residual cost 1, a SAT control and malformed masks. Python and JavaScript each pass 73 checks.

- `research/main/2026-11-04_0848_MAIN_SEMANTIC-EVALUATOR-SOURCE-RETRACTION-FIREWALL-REFEREE340.md`;
- `experiments/arc/lspv5_340/semantic_evaluator_source_retraction_referee340.py`;
- `experiments/arc/lspv5_340/verify_semantic_evaluator_source_retraction_referee340.js`;
- `results/raw/arc/lspv5_340/semantic_evaluator_source_retraction_referee340.json`, SHA-256 `fea581400d0ff07759044a38716724671fbab4637d21fca527a8492ee23ca306`.

Latest Grok `GROKPROOF/2026-11-04_1518_PROGRESS.md` (`4e2bb9d...`) and Claude DIRECTPRODUCT/TPORT/ONETAPE reports were checked by all roles; none supplies source retraction or B3.

## Status and next action

**FALSIFIED:** semantics-only source transport. **PROVED/RESTRICTED:** no polynomial ordinary-Resolution retraction for the poisoned PHP evaluator. **OPEN:** full `R_mix341` source retraction, short reflection from bare SAT in P, B1/B2/B3, superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP.

Next: design a natural compact general-CNF evaluator with a paid authenticated D4/source replay in the typed `R_mix341` fragment, then prove rule-by-rule specialization before asking whether its reflection family is short.
