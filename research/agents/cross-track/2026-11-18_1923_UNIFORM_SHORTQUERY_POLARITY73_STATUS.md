# CROSS-TRACK 73 | Uniform short-query self-simulation and polarity firewall
2026-11-18 19:23 PST. **P versus NP OPEN**. Full local report, executed audit and manifest in this run's reproducibility bundle. No other agent files were modified.

## Frozen before retrieval
Four candidates recorded beforehand: (1) SAT/UNSAT correct-path and strategy ledger; (2) seed-dependent versus source-only contraction; (3) exact CNF/T5 wrong-path falsifiers; (4) nonrelativizing WRAPPER and Resolution transport guards.

## Latest specialist and literature review
Resource Contraction: TMR-1/096, parsimonious four-layer T5 compiler, with polynomial but non-fine-grained source costs. TMR-3's signed-cycle DP and source recognition are cheap-source controls.
Nonrelativizing Simulation: LSPV-5 row-block correct-path reproduction (18:48 PST), verifies separate polarities, no necessary WRAPPER hinge.
Universal Obstruction: TMR-2/093, exact mod-five syndrome DP; similar dynamic support profiles can have differing SAT status.
Proof Transport: TMR-4/093 mixed-locality example, large SAT-side OBDDs and cheap source recognition, no arbitrary-decider transport.
Also read Clock Gate 46, SHIELD1, current GitHub handoffs, project Library SAT_Contraction_Proof_Attempt.pdf (18 Nov 2026, notably its section 5's self-simulation barrier), Drive's older proof-tracker matches, and primary sources [1]-[4]. This self-simulation principle appears in the Library note; the present cross-track contribution is its uniform all-input and polarity-sensitive integration, not an assertion of wholly independent discovery.

## Main formal result: answer-only controller no-go
Let M be a fixed uniform total exact controller for EVERY ordinary encoded CNF, whose only external SAT primitive is an *exact yes/no answer* on a strictly shorter explicit CNF. The local charged time/space are n^(lambda+o(1)), n^(sigma+o(1)), maximum child call count n^(q+o(1)), and maximum child encoding length n^(beta+o(1)), beta<1. Include BOTH answer polarities, rejected trials, generation, parsing, materialization, repeated access, replay, output, child work, stack and peak live space. It may inspect finite source code of an initial seed, but must be correct extensionally given exact child answers. If
lambda<c=1.34070, sigma<=.5, q+beta*c<c,
then M cannot exist on the Buss-Williams random-access model [1]. Replace each oracle answer by recursively running M on the child. Induct on length for exact correctness. For every d>c close enough, T(n)<=n^lambda+n^q T(n^beta)=O(n^(d+o(1))) since lambda<d and q+beta*d<d. Reuse a single child and a geometric stack, S(n)<=n^(.5+o(1)). This yields SAT in DTISP(n^(c+o(1)),n^(.5+o(1))), contradicting [1]. Non-extensional solver trace/identity/timing dependence is NOT covered and must be fully charged before use.

Counterfactual application of supplied layout R=n^.195, B=n^.65, child length=n^.35: lambda=1.195, q=.845, beta=.35, sigma=.35. q+beta*c=1.314245<c, so an all-input answer-only hereditary controller with these guarantees is prohibited, even if it mentions a seed. The *actual authenticated supplied-layout* algorithm remains sound; no reduction of arbitrary CNF to this class is established. At beta=.5 the analogous call cap is q<c/2=.67035; the present .845 call exponent does not satisfy it.

## Correct-path and polarity result
For authentic F(z,y)=AND_i F_i(z,y_i) with disjoint private variables:
SAT iff EXISTS z FOR ALL i EXISTS y_i F_i(z,y_i).
UNSAT iff FOR ALL z EXISTS i FOR ALL y_i NOT F_i(z,y_i).
The bad block may vary with z. A verifier accepting an UNSAT cover must check one *source-bound genuine local negative proof* for every z. Malformed indices, missing rows, counterfeit proofs and incomplete covers produce UNKNOWN, not SAT or UNSAT. A genuine 2-CNF implication contradiction supplies an unconditional one-sided specialist; arbitrary-CNF cases may be UNKNOWN. A SAT path requires a common z plus all compatible private witnesses.

Uniform sound and complete monolithic correct-path verifier of time n^(1.33+o(1)), space n^(.5+o(1)), k<=alpha log2(n) advice bits yields deterministic exhaustive replay n^(1.33+alpha+o(1)) time, n^(.5+o(1)) space, and is excluded by [1] for alpha<.01070. A *separably verifiable* block certificate of additional alpha log n bits AFTER explicit enumeration of n^.65 blocks and n^.195 rows, with O(n^.35) verification per attempt, costs n^(1.195+alpha+o(1)); a uniform all-input complete implementation would conflict with [1] for alpha<.14570. This is an all-input conditional no-go, not a lower bound against the supplied class. A supplied free correct path or polarity bit is advice, not a uniform strategy. Alternating quantifiers cannot be collapsed to one existential path; universal branches or an independently validated full strategy must be charged. Read-only certificate access and writable certificate storage use different machine models.

## Distinct sourced time-space exclusions
[1] Deterministic SAT: NOT in DTISP(n^1.34070,n^.5), random-access RAM as defined in the paper, Fig. 8.2. Both bounds are simultaneous; space n^(o(1)) gives the 2cos(pi/7)~1.80194 threshold.
[2] Nondeterministic SAT: standard YES witnesses are existential; Fortnow 1997 rules out a different *near-linear time*, n^(1-epsilon)-space regime, NOT (n^1.33,n^.5).
[3] Nondeterministic UNSAT / TAUT (equivalently co-nondeterministic SAT): Diehl-van Melkebeek-Williams establish the 4^(1/3)~1.5874 exponent only at n^(o(1)) space in the cited result, NOT n^.5 space at time 1.33. Separate dual-algorithm tradeoffs do not directly fill this gap.
Resolution lower bounds require an actual proof-system transport theorem and cannot be promoted to unrestricted algorithms.

## Executed independent controls
Standard-library Python audit (seed 202611181915): **1,848 assertions, 0 failures**. 600 random authenticated small block-CNFs checked against independent finite exhaustive search: SAT=85, UNSAT=515, sound 2-CNF certificates on 401 UNSAT cases, UNKNOWN=199, false UNSAT=0. Explicit switching UNSAT source F1=(z OR a)(z OR NOT a), F2=(NOT z OR b)(NOT z OR NOT b): z=0 needs block 1, z=1 needs block 2, and no one block works across both rows. Forged and incomplete covers rejected. Four native T5 paths BBB/FBB/FFF/BB have offset supports {0,1,2,3},{0,1,2,4},{0,2,3,4},{1,3,4}; all four intersect to empty, every proper subset remains SAT. Every 25-terminal assignment has some bad path, but this is not one global favorable path. T5 arc SAT, opposed digon UNSAT, directed triangle SAT controls passed. The finite exhaustive oracle is a checker, NOT the hypothesized polynomial seed.

## Proof DAG
ESTABLISHED: published model-specific alternation-trading exclusions and 2-SAT implication criterion.
PROVED under stated interface: all-input uniform answer-only self-simulation exclusion, correct same-input SAT/UNSAT quantifiers, wrong-path soundness and charged enumeration.
PROVED finite: 1,848 exact assertions and T5 control cases.
CONDITIONAL: supplied block scan with exact seed; n^1.33 time and sqrt space only at specified seed exponents; any all-input non-extensional seed-dependent compiler.
OPEN: unrestricted NO-block discovery, universal same-input UWI, indispensable nonrelativizing WRAPPER operation, arbitrary-decider-to-Resolution transport, n^1.33 matched SAT witness procedure, P versus NP.

## Assignments
Resource Contraction: test non-extensional genuinely seed-dependent hereditary compressor and fully price code access, calls, failed branches, replay and live stack.
Nonrelativizing Simulation: isolate indispensable WRAPPER operation surviving ordinary exact-answer self-reduction; no assumed hinge.
Universal Obstruction: common original F, ALL shared z with possibly different bad blocks, SAT witness comparator, source-aware T5 shortcuts, one uniform clock.
Proof Transport: check all local NO proof objects and full alternating strategy size; distinguish Resolution and arbitrary computational refutations.

## Sources
[1] Buss & Williams, Computational Complexity 24 (2015), Fig. 8.2, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf
[2] Fortnow, CCC 1997, https://doi.org/10.1109/CCC.1997.612300
[3] Diehl, van Melkebeek & Williams, https://research.cs.wisc.edu/techreports/viewreport.php?report=1601
[4] van Melkebeek, SAT lower-bound survey, https://pages.cs.wisc.edu/~dieter/Papers/sat-lb-survey-fttcs.pdf
