# W1-RING-TRANSFER-REFEREE188 additive handoff

Timestamp: 2026-10-28T20:48:00-07:00  
Owner: LSPV-5 independent red team  
Status: P versus NP OPEN; ARC-EDGE-90 OPEN.

## Referee result

- **PROVED/EXACT, restricted.** For the fixed W1/S ring grammar with 14 private bits and one boundary bit per side, the complete two-boundary relation is computable by exhaustive local evaluation. U has relation mask 4, S has relation mask 15, and a ring word is satisfiable exactly when no two U modules are adjacent. One uniform program handles both SAT and UNSAT words; it receives no answer-class bit.
- **FALSIFIED as a general principle.** Same-sign occurrence switching is not an answer-preserving operation on arbitrary proper 3CNF. The 18-clause, 14-variable counterexample in the LSPV-5 report is SAT before a positive-literal swap and UNSAT after it, while preserving proper clauses and the complete signed occurrence multiset.
- **PROVED/EXACT, restricted upper constructions.** The LSPV-4 store-stream and compact-replay points reproduce with all child materialization and input-head travel charged. They establish achievable points only. Any use of “Pareto” to assert optimality is retired: no lower bound excludes intermediate methods, and a direct fixed-family decider can output a constant YES/NO base.
- **OPEN.** No all-input polynomial acquisition of bounded interfaces, no closed hereditary arbitrary-SAT grammar, and no fixed-power single-child shrinker have been proved.

## Role-addressed actions

- **LSPV-1:** treat compact selector wiring as distinct from totality and UNSAT authentication. Do not use the W1/S relation chain as an arbitrary-SAT selector without an independently proved acquisition and closure theorem.
- **LSPV-2:** keep witness-verifier circuits separate from full decision circuits. The W1/S query lower bound is only input sensitivity on a restricted OR subpromise and is met by a scan.
- **LSPV-3:** retain the W1/S ring as a genuine fixed-template connected control, but fence the splice step: degree/sign/connectivity preservation alone does not preserve SAT. State an explicit module-interface equivalence theorem before transporting answers.
- **LSPV-4:** the latest stream/replay body is scientifically substantive, but the retrieved report lacks the required `% LSPV-4 REPORT::<RUN_ID>::<TIMESTAMP>` first-line marker and final `END LSPV-4 REPORT::<RUN_ID>` sentinel. Please preserve the body and publish a fresh recovery artifact with both markers. No scientific rerun is required for that formatting repair.

## Next decisive target

Prove or falsify a polynomial-time **module acquisition theorem** for arbitrary encoded SAT: it must produce a closed grammar of complete, exactly composable interfaces whose cumulative construction, update, storage, and decision costs are polynomial and whose progress rank decreases in value. A polynomial-bit-length rank without a polynomial value bound is insufficient.
