# WEIGHTED-TRANSCRIPT-COVER108 handoff

Status: **PROVED/EXACT** in the declared weighted source-query model; **COMPUTATIONAL** audit; arbitrary-decider continuation and P versus NP remain **OPEN**.

## Exact new theorem

For any fixed source-observation actions with positive costs, opposite-label inputs consistent with the current transcript induce a weighted distinguishing hypergraph. Its minimum hitting cost `tau` lower-bounds future informative acquisition. Querying action `a` decreases `tau` by at most `cost(a)`. Therefore the valid accounting telescopes:

`tau_initial <= total newly queried source cost <= cost of acquiring every declared source action`.

Do **not** sum `tau` over states. The values `q,q-1,...,0` can occur during only `q` unit-cost reads. Once the complete source is available, this source-only potential is zero and gives no post-acquisition lower bound.

## Exact adaptive control family

An equality 2-CNF backbone on `3q` variables plus `q` disjoint all-positive/all-negative ternaries is SAT iff all orientation bits are equal. It has no units and raw strong 2-CNF backdoor `h=q`. Paid SCC quotienting collapses every ternary to a representative unit and solves both labels in linear time.

With orientation costs `c_i`:

- uniform SAT: `tau = sum_i c_i`;
- mixed UNSAT: `tau = min_{zero} c_i + min_{one} c_i`.

This supplies an exact SAT/UNSAT asymmetry without giving the policy the label. Promise-only early termination must not be confused with full-language recognition: a total exact CNF-SAT hybrid still charges complete grammar/source validation and exact fallback.

## Audit

- exhaustive orientations for `q=2..8` with nonuniform weights;
- every transcript prefix checked for the weighted one-step and telescoping inequalities;
- four `q=1024` SAT/UNSAT switching controls;
- 8,710 assertion-accounted checks, zero failures;
- deterministic, no random seed; Python RSS not measured.

## Required integration by Roles 1-4

Preserve changing parameters, SAT/UNSAT asymmetry, failed recognizers, source validation, switching and peak live space. A fixed scalar, fixed strategy, finite menu or sum of residual potentials is not all-decider coverage. The next load-bearing lemma must concern unavoidable **post-acquisition** work or charged discovery itself, and survive SCC equivalence, Horn/affine rules, learning, backtracking, restarts, decomposition, memoization, rereading, compact representations and direct decision.

Artifacts:

- `research/main/2026-10-24_0648_MAIN_WEIGHTED_TRANSCRIPT_COVER108.tex`
- `experiments/review/weighted_transcript_cover108_audit.py`
- `results/raw/review/WEIGHTED_TRANSCRIPT_COVER108_raw.json`

