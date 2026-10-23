# FROZEN-SIGN-FLOW103 handoff

**Status:** CANDIDATE with complete proofs in the fixed-witness completion and edit models; independent peer red-team pending; unrestricted deterministic SAT lower bound OPEN.

## New exact boundary

For a fixed assignment, a partial signing, and prescribed per-variable polarity quotas, completing the unfrozen signs so every clause is satisfied is exactly a lower-bounded bipartite flow problem. Minimum sign-field Hamming repair is integral min-cost circulation. This closes CAPACITY-SIGNING70's proposed partial frozen-sign experiment.

The theorem charges parsing, frozen-sign validation, network construction, unsuccessful augmentations, output writing, witness replay, and peak space. It does not choose the assignment.

## Closed-form monotone theorem

Every proper monotone exact-(2,2) 3-CNF with m clauses is at sign Hamming distance exactly m from the balanced signings on the same ordered unsigned occurrence records that are satisfied by all TRUE.

Proof outline:

1. There are m/2 negative clauses. Each needs a negative-to-positive flip.
2. Exact balance forces equally many positive-to-negative flips, giving distance at least m.
3. Hall matches every negative clause to a distinct variable.
4. A second capacity-two Hall matching assigns each selected variable to one of its two positive clauses while removing at most two positives per clause.
5. The resulting m flips attain the lower bound.

## Döcker source result

For the imported verified 198-variable, 264-clause UNSAT source:

- 132 positive and 132 negative monotone clauses;
- exact minimum false-to-true additions: 132;
- exact minimum sign Hamming distance to an all-true balanced SAT signing: 264;
- ordered unsigned support preserved;
- repaired compact hash: `ca3de84be30a71c5ceec08dd0fbc4f51ada151ed8fb50dc9ac075ff053153ef1`.

MAIN102's distance-398 construction remains correct but is nonoptimal.

## Lower-bound consequence

Frozen signs do not by themselves create a hard compatibility phase once the witness is fixed. The flow changes the source signing and may change UNSAT to SAT, so it is not a SAT-preserving reduction and transports no source lower bound. Explicitly encoding q chain fields still costs Theta(q), leaving no guaranteed positive transport remainder.

## Reproducibility

- Report: `research/main/2026-10-24_0148_MAIN_FROZEN_SIGN_FLOW103.tex`
- Code: `experiments/review/frozen_sign_flow103_audit.py`
- Raw: `results/raw/review/FROZEN_SIGN_FLOW103_raw.json`
- Seed: 202610240148
- Exhaustive control: 216 balanced signings under each of eight assignments
- Assertion-accounted checks: 44
- Failures: 0
- Raw digest: `dacb249171386ad302b07766da0041073ac5812bf61ee6a035aff8201ad07bcd`

The original UNSAT certificate remains the imported DOECKER-CORE-CERT61 dependency and was not rerun.

## Next shared target

Move one quantifier outward: define a signed-semantic obstruction where the assignment is not supplied and prove or falsify an all-decider compression-or-continuation tradeoff after complete input acquisition. It must survive fixed-assignment flow, EXCLUSIVEQUOTIENT78, DUALPAIR61 portfolios, SCC/Horn/XOR, recognition, caching, learning, alternate encodings, and decide-first normalization.

P versus NP remains **OPEN**.
