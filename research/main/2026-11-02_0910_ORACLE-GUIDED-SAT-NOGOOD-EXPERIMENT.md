# Oracle-guided SAT with sound nogood exclusion: F15 experiment
**2026-11-02 PST. USER-DIRECTED EXPERIMENT. FINITE COMPUTATIONAL RESULT; P vs NP OPEN.**

## Authenticated source and oracle contract
Original F15 from `experiments/arc/lspv2_323/compact323.py` is valid proper duplicate-free Döcker monotone 3-SAT-(2,2), n=15, m=20, 1032 full models. Independent source enumeration verified counts. On this SAME original, pins `x1=1,x2=1,x3=0,x4=1,x5=1,x9=0` give **2** completions among 512, differing in one remaining bit. Flipping **only x3=1** gives **0** completions. No original clause is already falsified by either six-bit partial assignment. Pinned residuals are NOT canonical originals.

An OFFLINE known satisfying witness w supplies each still-unset bit with probability p, and otherwise the bit is uniform random; independent effective correct-bit probability is q=(1+p)/2. The witness was obtained by exhaustive enumeration and its acquisition is **NOT** included in solver runtime. This is hypothetical noisy advice, not an implementable SAT oracle. For the pinned SAT pair the exact first-draw success probability is **q^8**.

The simulator generates complete assignments, never reevaluates duplicates, and records all violated **original** clauses as sound falsifying cubes. Candidates matching recorded cubes are rejected before full evaluation. Duplicate proposals, rejected proposals and clause-cube membership tests still incur work. Those cubes are present in the source from the beginning, so they add no new semantic information.

## Results: 2500 runs/level, deterministic seed 20261102
| p advice invocation | q true-bit accuracy | pinned exact first draw success | pinned mean generated | pinned mean full evaluations | full F15 mean generated |
|---:|---:|---:|---:|---:|---:|
| 0% | 50% | 0.3906% | 248.269 | 5.364 | 31.303 |
| 66% | 83% | 22.523% | 4.513 | 3.046 | 5.418 |
| 75% | 87.5% | 34.361% | 2.956 | 2.398 | 3.444 |
| 90% | 95% | 66.342% | 1.487 | 1.453 | 1.648 |
| 95% | 97.5% | 81.665% | 1.232 | 1.225 | 1.279 |
| 99% | 99.5% | 96.069% | 1.038 | 1.038 | 1.046 |

Full original F15 exact first-draw success probabilities are respectively 3.1494%, 18.5892%, 28.6820%, 60.5572%, 77.8399%, 95.1206%. Actual raw generated-candidate expectation is 1/P(first draw) for an iid proposal stream even when duplicate/nogood proposals are rejected, since no true model can be excluded. Recorded source-clause nogoods reduce **full evaluations**, not the number of hypothetical proposal draws.

A **complete** chronological DPLL solver with charged original-clause unit propagation solves the pinned SAT residual in exactly **2 nodes** and the one-bit UNSAT sibling in exactly **1 node**, regardless of advice. On the unpinned F15, DPLL averages ~10 nodes across all advice settings. Thus the oracle yields a striking speedup for blind sampling but essentially no branch-node gain over this source-aware solver in these finite controls.

## Strong no-repeat implementation and its acquisition expense
A second simulation (1000 runs/level) explicitly preenumerated **all 512 possible complete residual assignments**, then sampled only from the live, unexcluded population with weights q^(9-d)(1-q)^d. It never generated duplicates or logically excluded assignments. Its mean full evaluations for p=0/66/75/90/95/99% were 5.387/3.060/2.402/1.437/1.236/1.042. But this required **512 complete candidate strings before the first query**, followed by 835.6/927.7/857.8/652.2/596.9/527.6 mean per-run weight computations, respectively, and paid exclusion scans. Generalizing such explicit conditioning incurs Omega(r*2^r) storage bits; treating it as free would be an invalid oracle for survivors.

## Referee and asymptotic implications
Independent no-producer-import verifier independently regenerated 32,768 F15 source values, the F15 same-original 2/0 pair, F9 70 original models, F9 same-original 2/0 controls, source-clause nogood soundness, and exact OBDD min/natural/max **52/66/80** via subset dynamic programming.

For exactly one witness, independently guessed bit correctness q gives success q^r, hence iid expected proposals q^(-r). For two witnesses differing in one variable the exact rate is q^(r-1), still exponential in r for each fixed p<1. Advice quality approaching 1-O(log r/r) could make this particular sampling bound polynomial, **if a correct-witness-correlated oracle can be obtained in polynomial TOTAL work**, which is precisely not proved. No canonical infinite sparse-model family or arbitrary-decider lower bound is inferred from this example.

Full paid ledger: grammar/source reads, indexing, witness advice acquisition, r random/advised bit draws per generated proposal, duplicate-key storage/checks, clause-cube checks, original-clause evaluations, source-provenance, output checking, rejections, cache, failed policies, and simultaneous peak memory. A true UNSAT instance has no correct witness bits, and random failed trials cannot establish UNSAT. The central polynomial all-input controller, arbitrary-A power-short mapping, and strict numerical SAME-MACHINE FLMV transfer remain **OPEN**.

**Source and literature:** `experiments/arc/lspv2_323/compact323.py`; Schöning, *A Probabilistic Algorithm for k-SAT and Constraint Satisfaction Problems* (FOCS 1999); SAT clause-learning/restart literature, e.g. *A Verified SAT Solver Framework with Learn, Forget, Restart, and Incrementality* (2018). Full local runnable Python study, conditional-sampler variant, independent verifier, and raw JSON were produced as conversation downloadable artifacts, not asserted to be in this GitHub commit.

No tasks, titles, enabled states, schedules or root manuscript were modified.