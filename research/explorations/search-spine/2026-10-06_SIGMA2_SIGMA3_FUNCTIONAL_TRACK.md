# Sigma_2 / Sigma_3 and Functional-Hierarchy Comparison Track

Timestamp: 2026-10-06 11:46 PT  
Status: exploratory / OPEN.

## Definitions used

Sigma_2^P has the standard form

x in L iff exists y forall z R(x,y,z)

for a polynomial-time predicate R.

Sigma_3^P has the form

x in L iff exists y forall z exists w R(x,y,z,w).

A deterministic functional polynomial hierarchy also exists. A clean standard notation is

FDelta_{k+1}^P := FP^{Sigma_k^P}.

Thus:
- FDelta_1^P = FP;
- FDelta_2^P = FP^NP;
- FDelta_3^P = FP^{Sigma_2^P}.

Notation "FSigma_2^P" is not universal. In this project, if used, it must be explicitly typed.

Two distinct meanings must not be conflated:

1. deterministic oracle functions: FP^{Sigma_2^P} = FDelta_3^P;
2. an outer-witness search relation of the form:
   given x, output y such that forall z R(x,y,z),
   if such y exists.

The second is a natural search analogue of Sigma_2 but has a coNP-verifiable witness relation rather than an ordinary P-time FNP verifier.

For total search, TF Sigma_2 is an established object in recent literature on the total function polynomial hierarchy, but black-box separations there are not unrestricted Turing-time separations.

## Track A: P versus Sigma_2^P

A separation

P != Sigma_2^P

would imply P != NP, because P=NP collapses the polynomial hierarchy to P.

### What becomes easier

The current FSC exactness predicate naturally has a form resembling

exists G,pi forall r V(G,pi;r)=1,

which is Sigma_2-like.

Therefore under a contradiction assumption

P = Sigma_2^P,

this predicate is polynomial-time decidable.

This removes one *quantifier-class mismatch* in an exploratory Sigma_2 track.

### What does NOT disappear

It does not automatically produce the endpoint-sized co-nondeterministic circuit required by the current vMS/RMV interface.

A polynomial-time Sigma_2-decider under the collapse may:
- have unknown exponent K;
- operate at current source scale;
- compile to a circuit too large for the required size-m interface.

Thus FSC-EXTEND1 is not simply solved. The problem changes from:

"how do we express exact local-to-global acceptance with an existential certificate?"

to:

"can the now-polynomial exact predicate be realized within the required source-normalized size/resource endpoint without a current-scale hidden call?"

### Decision-output problem remains

P versus Sigma_2 is still a language separation. The algorithm outputs one bit.

Therefore the general one-bit-to-rich-resource issue remains unless a wrapper/search formulation is used.

A QBF_2 self-reduction can recover the outer existential witness on YES instances using polynomially many Sigma_2 decision calls, but these are current-scale calls and relativize.

### Barriers remain

Still required:
- ordinary-source acquisition/use lower bound;
- exact endpoint/model matching;
- nonrelativization;
- separate nonalgebrization;
- Natural-Proofs audit if applicable.

### Potential endpoint advantage

Known results give strong fixed-degree circuit lower bounds inside low levels of PH (e.g. Kannan-type results). These are useful hostile/endpoint controls but do not by themselves separate P from Sigma_2, because the hard language may depend on the fixed degree.

A usable route would need uniform control over the degree/reduction overhead.

## Track B: P versus Sigma_3^P

P != Sigma_3^P would also imply P != NP.

However the current architecture has no obvious missing predicate that intrinsically needs the extra existential block beyond Sigma_2.

The natural semantics

exists y forall z exists w R(x,y,z,w)

introduce an inner response function w(z).

An explicit full strategy z -> w(z) may be exponentially large, so the one-bit decision problem does not automatically expose it.

Therefore Sigma_3 currently appears to add semantic complexity without removing a central requirement.

Status: lower priority than Sigma_2 unless a future source predicate naturally lands at Sigma_3.

## Track C: deterministic functional analogue

A clean functional counterpart of P versus Sigma_2 is

FP versus FP^{Sigma_2^P} = FDelta_3^P.

This equivalence is exact at the collapse level:

FP = FP^{Sigma_2^P}
iff
P = Sigma_2^P,

because characteristic functions of Sigma_2 languages are computable with a Sigma_2 oracle, while a collapse P=Sigma_2 makes such oracle computation ordinary polynomial time.

This track is logically clean but does not force explicit witnesses; the oracle function may still be used only to compute a decision bit.

Thus it does not automatically solve the consumer/output-resource issue.

## Track D: Search-Sigma_2 (project name)

Define a polynomially balanced relation

R_2(x,y) := forall z P(x,y,z),

where P is polynomial-time.

The associated search task is:
- on x with some valid y, output such a y.

This is the natural outer-witness search analogue of Sigma_2.

Potential advantage:
- explicit y is part of the computational output;
- the quantifier structure aligns with FSC's current exists/forall gate;
- path exposure disappears just as in FP/FNP.

New difficulty:
- checking a proposed y is coNP, not P;
- correctness of y contains an implicit universal obligation;
- an algorithm need not materialize all universal challenges;
- ordinary output length still gives only polynomial information;
- a source/acquisition lower bound is still required.

Therefore Search-Sigma_2 trades:
- FNP's all-witness robustness / P-verification
for
- stronger witness semantics / harder verification.

## Track E: "F Sigma_2" terminology

"F Sigma_2^P" is not a single universally standardized object.

Use one of these explicit labels in project documents:

- FDelta_3^P = FP^{Sigma_2^P} for deterministic polynomial-time functions with a Sigma_2 oracle;
- Search-Sigma_2 for outer existential witness search with a Pi_1/coNP predicate;
- TF Sigma_2 for total search at the second level of the total function polynomial hierarchy.

Do not interchange them.

## Requirement-removal matrix

| Requirement | FP vs FNP | P vs Sigma_2 | Search-Sigma_2 | P vs Sigma_3 |
|---|---|---|---|---|
| one-bit path exposure | removed | remains unless wrapped | removed | remains unless wrapped |
| raw-to-consumer K mismatch | replaced by witness/output theorem | remains | partly replaced by output theorem | remains |
| all-witness choice | yes | no | yes | no |
| FSC exists/forall quantifier mismatch | not removed | partially absorbed | naturally aligned | absorbed but overpowered |
| current-scale/unknown exponent | remains | remains | remains | remains |
| ordinary-source acquisition LB | remains | remains | remains | remains |
| endpoint/model match | remains | remains | remains | remains |
| nonrelativization | remains | remains | remains | remains |
| nonalgebrization | remains | remains | remains | remains |

## Current recommendation

Maintain three parallel tracks:

1. FP-FNP search track:
   best for eliminating one-bit output/path exposure.

2. P-vs-Sigma_2 track:
   best for testing whether FSC-EXTEND1 and exact accepted-source consistency become structurally simpler when exists-forall is native.

3. Search-Sigma_2 exploratory track:
   best hybrid if an explicit outer witness can be tied to source-dependent obligations.

Do not prioritize Sigma_3 unless a concrete source predicate genuinely needs the third quantifier block.

## Central warning

Moving upward in PH does not remove the unrestricted lower-bound requirement.

At best it changes the interface:

decision one-bit problem
-> explicit witness problem
or
NP-style certificate mismatch
-> native Sigma_2 predicate.

The final proof still needs an unconditional ordinary computational lower bound plus a barrier-safe endpoint.

P vs NP and all stated higher-level separations remain OPEN.
