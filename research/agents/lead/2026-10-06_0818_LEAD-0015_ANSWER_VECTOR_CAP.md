# LEAD-0015 — Answer-vector cap and RMV data-structure triage
Timestamp: 2026-10-06 08:18 PT
Agent: LEAD

GLOBAL STATUS: P versus NP remains OPEN.

## Immediate publication repair
The full LEAD-0014 body was successfully written to GitHub, replacing the prior one-line publication marker. Commit: 8a1c036ac66876cded31beb98a5605227bd77b44.

## Older corpus clue recovered
FULLPAIR6 already defines the exact finite legal-slice incidence matrix M_{s,a} and complete co-occurrence graph E_full for a source-typed declared realization. PAIR2COVER1 proves rho(H) >= 1+r+|E| and the spanning-clique full-rank criterion. ORBITBATCH1 proves strong query-address deduplication: for each orbit position the union over vector seeds is exactly the child domain B, and over all orbit positions it remains B.

Thus LEAD-0014's proposed generic "derive the RMV query matrix" was partly duplicative. The correct next question is whether the existing legal-query family can support any storage/query lower bound stronger than its trivial answer-table upper bound.

## PROVED/EXACT: ANSWER-VECTOR-CAP1
Let Q_x be any finite legal query family for fixed data/source x, and let f_x:Q_x->{0,1}. There is always a static representation
    S_x = (f_x(q))_{q in Q_x}
of |Q_x| bits, with O(1) random-access query probes once a query index is supplied.

Therefore no unrestricted static representation lower bound for this fixed query family can exceed the information needed to store its complete answer vector, up to addressing/encoding overhead. In particular, large algebraic/product-span rank of an internal realization does not by itself force storage larger than the answer-vector table.

Proof: enumerate Q_x canonically and store one answer bit per query. Query q reads its indexed bit. This is independent of how expensive S_x is to construct.

## PROVED/EXACT: PREPROCESSING-OR-QUERY-DICHOTOMY1
For the RMV static-data-structure route to contribute to an arbitrary-SAT contradiction, at least one of the following must be separately proved:
(A) the legal query family is so large, in the original SAT normalization, that storing the complete answer vector violates the target space budget; or
(B) construction/acquisition of the answer vector is itself charged and lower-bounded in the target machine model.

A pure query-probe lower bound cannot establish (B). If |Q_x| is polynomial in the relevant original input size, the trivial answer vector is polynomial space and this route cannot contradict P merely from representation size.

This is a model consequence, not a SAT lower bound.

## Interaction with ORBITBATCH1
ORBITBATCH1 makes the warning stronger. Seed-by-orbit multiplicity cannot be counted as distinct information demand because invertibility collapses the union of field-query addresses to B. It also shows that source normalization N=p^r is not the original SAT length. Therefore neither apparent orbit multiplicity nor a large N-normalized query family can be used in the final contradiction without the complete n_SAT -> |y| -> (h,r,Delta,p) -> p^r map.

## Interaction with FULLPAIR6 / product span
FULLPAIR6 remains useful as a fixed-realization structural theorem. Dense E_full can prove quadratic feature rank for the declared Hadamard realization. ANSWER-VECTOR-CAP1 shows why that fact cannot automatically become a static-storage lower bound for semantic SAT answers: the evaluator may store answers directly instead of preserving the algebraic feature representation.

This is another form of Generic Avoid, now stated at the static-data-structure layer.

## Literature check
Gál-Miltersen's succinct-data-structure theorem concerns representations close to an information-theoretic baseline and gives redundancy/query tradeoffs for explicit problems with a coding-theoretic property. It does not charge preprocessing computation.
Fredman-Saks cell probe intentionally allows free computation between probes and arbitrary representations.
Recent complexity-preserving data-structure reductions can preserve preprocessing time/space, but that is a property of an explicit reduction; it does not supply an RMV/SAT preprocessing lower bound.

## Candidate revision
RMV-DATASTRUCTURE1 is downgraded from a possible direct bridge to a diagnostic subroute.

CANDIDATE/OPEN revised target:
RMV-DATASTRUCTURE2 = prove a source-matched lower bound only after explicitly specifying:
1. original SAT-normalized number of legal semantic queries |Q_x|;
2. information-theoretic number of distinct answer vectors over the allowed source family;
3. representation budget S in the endpoint machine;
4. preprocessing/acquisition budget P if construction cost is needed;
5. query budget t;
6. a reduction preserving the relevant P,S,t quantities.

Without all six, no cell-probe result is load-bearing for P vs NP.

## Barrier audit
Relativization: unchanged OPEN. A SAT oracle can generate semantic answer vectors unless an intensional source restriction blocks it.
Algebrization: unchanged OPEN. FULLPAIR6/product-span and current cell-probe formulations are algebraic/extensional.
Wrappers: answer-vector storage is wrapper invariant and therefore a strong hostile control against trace/provenance storage claims.
Arbitrary-algorithm extraction/CSE: OPEN.
Acquisition: OPEN.
Model matching: OPEN.

## Main-file decision
No main2/main3 edit yet. This materially downgrades RMV-DATASTRUCTURE1, but that candidate was introduced only in LEAD-0014 and is not yet a root theorem dependency. Keep main files stable until WRITE performs the pending synchronized update.

## Next target
Shift from generic cell-probe richness to the source-normalized semantic answer family:
1. use ORBITBATCH1 and SOURCETRACE1 to enumerate the actual legal semantic query types, deduplicated extensionally;
2. derive |Q_x| in original SAT length n, not N=p^r;
3. determine whether answer vectors across source-valid X have entropy exceeding polynomial storage;
4. if not, RETIRE static representation size as a route and return entirely to acquisition/CSE;
5. if yes, identify an explicit data-structure theorem whose hypotheses match that exact answer matrix.

No Python experiment is justified until the exact semantic query indexing and SAT-length normalization are fixed; finite rank experiments cannot resolve this asymptotic/model question.

## Handoffs
PROOF: formalize ANSWER-VECTOR-CAP1 and check whether any current sufficient-state lemma accidentally assumes the representation must preserve source/algebraic coordinates rather than semantic answers.
RED: use direct answer-vector storage as the default hostile implementation against every sufficient-state/storage lower-bound claim.
RESEARCH: look specifically for static data-structure lower bounds that charge preprocessing time, or lower bounds on preprocessing+query jointly, under arbitrary representations; distinguish word-RAM from cell probe.
WRITE: do not promote RMV-DATASTRUCTURE1 as a bridge. If mentioned, include ANSWER-VECTOR-CAP1 and PREPROCESSING-OR-QUERY-DICHOTOMY1 immediately.

## Strict status
ANSWER-VECTOR-CAP1: PROVED/EXACT.
PREPROCESSING-OR-QUERY-DICHOTOMY1: PROVED/EXACT model consequence.
STATIC-DS-TYPING1: PROVED/EXACT.
PREPROCESSING-GAP1: PROVED/EXACT.
RMV-DATASTRUCTURE1 direct-bridge interpretation: RETIRED.
RMV-DATASTRUCTURE2 fully normalized diagnostic: CANDIDATE/OPEN.
FULLPAIR6 structural rank: PROVED/EXACT at its declared fixed-realization scope.
Arbitrary-algorithm CSE: OPEN.
Ordinary-source acquisition lower bound: OPEN.
Nonrelativizing hinge: OPEN.
Nonalgebrizing hinge: OPEN.
P versus NP: OPEN.
