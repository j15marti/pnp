# LEAD-0030 — Code-specialized macro-DAG wrapper audit

Timestamp: 2026-10-07 08:53 PT  
Agent: LEAD  
Global status: **P versus NP remains OPEN.**

## Target

Attack the surviving PRE-A-MACRO-SHRINK1 route after LEAD-0028: use the fixed code of an arbitrary hypothetical polynomial-time exact SAT decider A non-black-boxly, but avoid executing A on a current-scale SAT instance or materializing its N^K computation. The desired Williams landing remains, e.g.,
[
q\le N^{1/3+o(1)},\qquad |G_i|\le N^{2/3+o(1)},
]
with near-linear local work.

## Literature control

Williams (STOC 2024), *Self-Improvement for Circuit-Analysis Problems*, explicitly asks whether self-improvement can reach the P=NP regime and says the current construction encounters bottlenecks before the polynomial regime. Fortnow--Santhanam, Dell--van Melkebeek, and Drucker show that generic exact SAT compression/sparsification is already a powerful object; their PH-collapse consequences are absorbed under the contradiction assumption P=NP and therefore are not a terminal contradiction here.

## CONFIG-MERGE-WRAPPER-GUARD1 — PROVED/EXACT

Any proposed K-neutralization theorem based on counting or merging **identical full machine configurations** is not wrapper invariant.

Given any exact decider A, construct DELAY_d[A] that simulates A but inserts N^d semantically inert delay steps carrying a monotonically changing counter before returning the same output. Every full delay configuration is distinct because the counter differs. Thus the number of distinct configurations and the time-unrolled DAG size can be inflated to N^d for arbitrary fixed d without changing the computed SAT function.

Therefore no lower or upper bound based on raw configuration count, repeated-state count, time-unrolled DAG node count, or exact configuration hashing can provide a K-independent canonical representation of the SAT computation for arbitrary implementations.

COPY and RECOMP give analogous representation inflation. This is a representation guard, not a SAT lower bound.

## Finite wrapper sanity check — COMPUTATIONAL

For n in {16,32,64,128,256} and delay exponent d in {1,2,3,4}, the synthetic DELAY wrapper has n^d distinct full configurations while preserving the same two-valued semantic output. At n=256,d=4 this is 4,294,967,296 distinct configurations. This finite calculation merely illustrates the exact symbolic guard.

## INPUT-DEPENDENT-SLICE1 — CANDIDATE, not established

A possible repair is to quotient away state that cannot influence the final output, retaining only the input-dependent semantic slice. This defeats the trivial counter-only DELAY wrapper.

However, a generic syntactic dependency slice is still not wrapper invariant: an implementation may mix a delay/copy/recompute variable into intermediate values and cancel it later. Determining that the dependence is semantically irrelevant requires function equivalence rather than graph reachability.

Under P=NP, ordinary polynomial-size circuit equivalence/minimization decision problems collapse with PH, but this does not solve the present problem: the specialized computation itself has N^{K+o(1)} materialized size by PARTIAL-EVAL-K-CARRY1. Running a polynomial-time canonicalization algorithm in the materialized computation size still costs N^{Omega(K)} and retains K. A succinct representation of that computation moves the task to succinct/meta computation rather than ordinary SAT.

Thus INPUT-DEPENDENT-SLICE1 remains only a candidate interface.

## SEMANTIC-CANON-GATE1 — PROVED/EXACT classification

To survive DEAD/COPY/DELAY/INTERP/RECOMP, a generic code-specialized compactor must depend on the **semantic function realized by the specialized code**, or on another wrapper-covariant invariant proved equivalent for the purpose at hand, rather than raw implementation size/history/configuration identity.

But obtaining such a semantic canonical form cheaply from an arbitrary N^K-time implementation is itself the self-improvement problem. Merely naming semantic quotienting does not provide the Williams compiler.

## BLACKBOX / source-only cross-check

A source-only Williams-landing shrinker is already excluded by BLACKBOX-MACRO-NOGO1: recursively closing it would directly violate Williams. Therefore the surviving object has a narrow specification:

1. depend non-black-boxly on A's fixed code;
2. be invariant/covariant under semantics-preserving wrappers;
3. avoid materializing N^K execution;
4. avoid a current-scale call to A;
5. output ordinary smaller SAT instances, not a succinct or quantified stronger problem;
6. satisfy the Williams time-space landing parameters.

No construction satisfying all six conditions is known here.

## New red arrow: K-NEUTRAL-CANON1 — OPEN

Construct from fixed code(A) and source F, in fixed-exponent time/space independent of A's polynomial exponent K, a wrapper-covariant semantic summary Q(A,F) sufficient to produce an exact fractional SAT self-reduction, while never materializing or executing the N^K computation.

This is strictly stronger than repeated-state DAG merging and is the current code-specialized form of PRE-A-MACRO-SHRINK1.

## Result

The attempted repeated-state/hash macro-DAG compactor is **FALSIFIED/RETIRED as a generic hinge** by DELAY/COPY/RECOMP wrapper inflation.

The broader non-black-box self-improvement route survives, but its next theorem must be semantic and K-neutral:
[
\boxed{\text{K-NEUTRAL-CANON1 (OPEN).}}
]

P versus NP remains OPEN.
