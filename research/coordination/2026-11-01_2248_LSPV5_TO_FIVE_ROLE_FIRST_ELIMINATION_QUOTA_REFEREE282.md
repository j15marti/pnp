# LSPV-5 to five roles: FIRST-ELIMINATION-QUOTA-REFEREE282

**2026-11-01 22:48 PST. PROVED/EXACT first-step theorem; independently COMPUTATIONAL iteration countercontrol. P versus NP OPEN.**

## Exact theorem

For every valid canonical original F with m clauses and every original variable x, Davis--Putnam elimination considers exactly four positive-negative source-clause pairs and computes a CNF exactly equivalent to exists x F with:

- at most m clauses;
- at most 3m+4 literal records; and
- width at most four.

Proof: remove the two positive and two negative x-clauses and add at most four non-tautological width-four resolvents. Standard resolution elimination gives exact existential equivalence. Tautology, duplicate and subsumption removal can only decrease size.

## Independent falsification of iteration

The original 2-positive/2-negative quota is not hereditary. On F9, eliminating x9 then x6 already gives six candidate pairs at the second step. Exact DP over all F9 orders gives:

| class | total candidate pairs | largest step | projected peak literals | order |
|---|---:|---:|---:|---|
| best | 9 | 4 | 28 | 3,2,1,5,9,4,6,7,8 |
| worst | 35 | 12 | 36 | 8,5,7,4,2,9,6,3,1 |

All pairs are charged even if later tautological or subsumed; normalization and policy acquisition are additional costs. Thus neither quota persistence nor order equivalence survives.

The no-import verifier checked all first projections of Y6/F9/F15 on 248,256 residual assignments and 248,340 assertion groups. It independently reproduced forward evaluator truth tables and counts: Y6 23 gates/depth 5/20 models, F9 35/depth 6/70, F15 59/depth 7/1,032. F9 OBDD 52/66/80, 264 S/U modes and six malformed rejects remain checked.

Same-original F9 pins (x3,x5,x6,x7,x8)=(0,1,0,0,0) give an x1=0 SAT residual {x2},{x9} with two models and zero elimination pairs, versus an x1=1 UNSAT residual {x2},{x9},{not x2 or not x9} with zero models and two pairs to derive contradiction.

## Charged gap

W_D = grammar + source/index/head + discovery + elimination/resolvent + failed/select/switch + semantic/proof/GE + cache/replay + child/output/bit + guest DELAY/COPY/RECOMP + sum over every evaluated successor.

Peak includes all co-live source and occurrence lists, candidate-resolvent buffer, normalized projected CNF/circuit, proof/cache, ancestors, children, index/head and guest state. The projected CNF is ordinary noncanonical mixed 4-CNF. No polynomial aggregate bound, free favorable-order oracle, hereditary canonical child, arbitrary-A contraction, or strict same-machine FLMV numerical transfer is proved.

Literature and implementation audit found established bounded variable elimination and explicit occurrence/growth caps in SATCH and OR-Tools. Targeted project and OpenAI searches found no exact source-local first-step statement; absence is not novelty evidence.

Artifacts: [report](../main/2026-11-01_2248_MAIN_FIRST-ELIMINATION-QUOTA-REFEREE282.tex), [producer](../../experiments/arc/lspv5_282/first_elimination_quota_referee282.py), [independent verifier](../../experiments/arc/lspv5_282/verify_first_elimination_quota_referee282.py), [raw](../../results/raw/arc/2026-11-01_2248_LSPV5_FIRST_ELIMINATION_QUOTA_REFEREE282_raw.json).
