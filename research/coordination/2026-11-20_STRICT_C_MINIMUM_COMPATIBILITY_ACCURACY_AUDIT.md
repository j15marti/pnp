# Strict T5 minimum-compatibility / accuracy audit
Date: 2026-11-20. Status: PROVED (restricted hidden-record information theorem and strict-C K4 equality certificate); COMPUTATIONALLY VERIFIED (finite audits); FALSIFIED (rarity-only computational hardness criterion); OPEN (unrestricted source-visible time-space-error lower bound).

Original strict C: R(a,b) iff (b-a) mod 5 is 1 or 3; C(a,b,c) is a directed 3-cycle. All 125 value triples independently checked; exactly 30 satisfy.

## Source-visible matched experiment
For each k=2,3,4,6,8,12, 24 matched balanced SAT/UNSAT pairs were constructed, separately relabeled and clause shuffled (288 original-C sources total). Sources have 19k+2 variables and 14k+1 physical C clauses; the two pair members differ in exactly one physical clause. The closed chain is clause-critical UNSAT; the open chain is SAT. All 144 SAT witnesses were independently checked against the original C predicate; all 144 UNSAT sources received independently replayed source-grounded K4-equality certificates. A first-pass degree-4 signature distinguishes the matched family perfectly, so the family is deliberately an easy source-aware control. The exact SAT shared-assignment density is (24/3125)^k.

Random shared-assignment witness sampling: k=2 had 8 successful shared assignments across 120000 trials, detecting 6/24 SAT sources, for 62.5% balanced classifier accuracy; k=3,4,6,8,12 had no hits at the preselected sample budgets, giving 50% on the balanced labels. Failure to sample a SAT witness is not a valid UNSAT certificate.

Criticality: 496 complete single-physical-C-clause deletion witnesses verified on k=2,3,4,6,8,12 closed chains; 54494 retained/deleted original-C checks passed. Native critical controls: 8- and 25-clause sources have 33 archived deletion witnesses independently replayed; the original native 25-clause 1046-node/600-leaf static UNSAT proof was replayed; 11 native matched pairs were solved afresh both polarities by complete CSP search. Total corpus classifications: 310, split 155 SAT and 155 UNSAT.

## Exact restricted near-perfect-accuracy theorem
Hidden-record erasure oracle: balanced label Y, one uniformly hidden differing record J among M, query reveals Y only if J hit. With q distinct probes, maximum accuracy is p=1/2+q/(2M), so error epsilon forces q>=(1-2epsilon)M. There is **no superpolynomial cliff** when p increases from 99% to 100%; q increases linearly to M. A 100000-trial seeded simulation over four physical source lengths supports the exact calculation. This bound does not apply directly to unrestricted source-visible T5 computation.

Changing stage parameters can reuse or waste earlier probes. With eight stages each covering one-eighth of records, disjoint acquisition reaches 100% in the restricted model; independent repeated acquisition reaches only 82.82% expected correctness.

## Scope and next theorem
The matched chains have fixed incidence girth six and recognizable K4 structure; strong source-aware shortcuts and full source access are permitted. Python tracemalloc and selected candidate counters are empirical only, not machine-independent bit time/peak writable-space proofs. The necessary next lower-bound lemma must survive every source-aware algorithm, GF(5) and graph shortcuts, alternate variable orders, learned constraints, recomputation, both child polarities, verification, output, and input access; it must hold for a balanced physical strict-C distribution with a proved model-matched reduction to arbitrary SAT. The existing deterministic SAT time-space lower bound does not exclude randomized algorithms solely from high accuracy.

All 16 artifact files, scripts, raw JSON, 310 serialized source cases, 496 critical witnesses, archived static proof, and independent verification are distributed in the conversation file **T5C_Minimum_Compatibility_Accuracy_Audit_20261120.zip**, SHA-256 708eaf78150dba060e83baa897011e5f69cf2ec1a87de6857d4b5ed398dfbe60. Seed 20261120. This GitHub handoff does not claim the ZIP was uploaded to the repository.

P versus NP remains open.
