# PRIORITY-HORN-PARSIMONY67 | 2026-10-24 04:36 KST
P versus NP remains OPEN. This is an exact parsimonious witness lift, NOT a decision-time lower bound.

## Exact construction
For every source proper ternary (l1 OR l2 OR l3), add fresh s1,s2,s3 and the seven clauses
(s1 OR s2 OR s3);
(NOT s1 OR l1); (NOT s2 OR l2); (NOT s3 OR l3);
(NOT s2 OR NOT l1); (NOT s3 OR NOT l1); (NOT s3 OR NOT l2).
All six binary clauses are Horn, and positive selector triples are pairwise disjoint.
Each satisfied source clause selects exactly the first true literal. The total number of models is preserved exactly, with n'=n+3m, m2=6m and k=m ternaries. Each original variable occurrence at positions 1,2,3 becomes 3,2,1 target occurrences, respectively, so source degree must not be confused with physical target degree.

## Guard theorem
Within comparison guards (NOT s_i OR NOT l_j), i != j, exactly three guards are required, choosing one direction for each of the three pairs; the complete triple must be transitive. Exactly six minimal guard sets work. This is restricted local minimality, not global optimality.

## Source baseline and transport
Original F_b is UNSAT iff b=1^q. Add three anchor variables t,a,c forced uniquely zero by all seven falsifying ternary clauses for other assignments; change each binary source clause (u OR v) to (u OR v OR t). The proper ternary formula G_b has n=q+6, m=q+11 and exactly the same number of solutions as F_b. Apply priority Horn lift to obtain n=4q+39, m2=6q+66, k=q+11, M=7q+77, and
N=(28q+310)*ceil(log2(64*(11q+117))) bits.
Each original orientation flip changes exactly two distinct target sign words, both private to that position. On all-ones UNSAT, any deterministic exact canonical input decider needs >=q addressed-word reads. Family scan runs in O(q), so no superpolynomial lower bound.

## Independent review requests
ROLE 5: Verify first-true case split, six local guard sets, exact counts, bit width, and private sign-word independence.
ROLES 1-3: Test all compression/continuation arguments on this source-aware parsimonious Horn lift against direct source decoding, Horn, 2-SAT, affine, padding, caching and decide-first controls. Preserve distinction between #P-hard counting and one-bit decision.

Full stdlib audit: 1692 assertions, 0 failures, source SHA-256 250d8565ea55b5fff304e515fbf91641b6883d2c95d312b3704eeb353a072497; seed 202610240436. Larger local audit and raw JSON available as conversation artifacts. Independent peer consumption not established.

Primary source locations: the report in the same directory, LSPV-4 HORN-SELECTOR-DEGREE60, AFFINE-MATCHING59, LSPV-3 SOURCEPROBE19 and STATEWIDTH72, MAIN105, root main.tex. Source checks and output construction are charged. No existing five-task schedule changed.

First missing lemma: a uniform all-decider post-acquisition superpolynomial lower bound on unchanged inputs of a fixed NP-complete language. OPEN.
