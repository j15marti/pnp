# Six-role handoff: clocked one-sided totalization, full row coverage and exponent firewall

**Role:** independent time-space auditor. **Run:** 2026-11-19 America/Los_Angeles. **Status:** PROVED logical resource lemmas; FALSIFIED incomplete-row UNSAT inference; COMPUTATIONAL strict-C controls; CONDITIONAL unrestricted SAT transfer; OPEN critical-C and P versus NP.

## Clocked one-sided totalization (PROVED)
For a uniform deterministic globally sound specialist for L=SAT or L=UNSAT, if **every input in that target polarity** yields a verified accepted output within effectively constructible T(n),S(n), simulate with **both** time and workspace hard caps, including certificates, input access, index tapes and output. Accept its valid polarity output; on timeout/space overflow return its complement. Soundness prevents a wrong answer, while promised-polarity inputs finish before the caps. This produces a total deterministic decider in T(n) polylog overhead and S(n)+O(log T(n)) workspace, even if raw wrong-polarity runs have unbounded resources. Not applicable to oracle advice, uncharged verification, nonuniform clock, or restricted promises.

Buss-Williams (2015, Fig. 8.2/8.3) verify an alternation-trading SAT lower bound at deterministic random-access (c,epsilon)=(1.34070,0.5), with a 44-round numerical refutation; therefore a uniform unrestricted (1.33+o(1),0.5+o(1)) sound one-sided algorithm in the *same* model contradicts this known result. This does **not** rule out the restricted strict-C critical family.

## Row coverage firewall (PROVED; shortcut FALSIFIED)
For F(z,x1,...,xB)=AND_j F_j(z,x_j), with disjoint private xj,
SAT iff EXISTS z FORALL j EXISTS xj F_j(z,xj).
UNSAT iff FORALL z EXISTS j FORALL xj NOT F_j(z,xj).
FORALL **listed** z does not replace FORALL z. Explicit exhaustive T5 rows require R>=5^q, hence if R<=N^0.195, q<=0.195 log_5 N. Strict C counterexample: F=C(h,u,v), supplied row (u,v)=(0,0) is refutable for all h, but omitted row (0,1) has complete SAT witness h=2. Checked with the original strict-C predicate. This is a counterexample to the row-coverage inference, not to source-uniform symbolic search.

## Charged sequential scan (CONDITIONAL, exact exponents)
Given a total correct local decision solver time m^a, space m^s; R=N^0.195 rows, B=N^0.65 blocks, m=N^0.35 private length; fixed-width source/row access and O(m) materialization:
T=N^(max{1,1.195,0.845+0.35a}+o(1)) + extra verification/output costs.
Time <=N^1.33 requires a<=97/70 (1.385714...); local space <=N^0.5 requires s<=10/7 and every other writable cache controlled. Keeping B explicit word-offsets requires N^0.65 logN writable bits, **too large** for N^0.5; repeat source scans instead, charging N^1.195 materialization. Recompute and stream a final SAT witness on a second pass, rather than retaining Theta(N) output bits. Negative child decisions require actual complete decision/certification, not a block index alone. Arbitrary polynomial SAT seed does not guarantee a<=97/70.

## Advice, alternation and published polarities
One supplied correct polarity bit is answer advice, not a uniform decision method. A sound polytime verifier with polynomial k-bit existential paths for BOTH SAT and UNSAT on every unrestricted CNF would place coSAT in NP and imply NP=coNP; wrong-path soundness is indispensable. Naive deterministic replay can cost 2^k complete verifications. A single existential path cannot certify universal branches of an alternating strategy. A read-only, freely rereadable k-bit advice tape is not the standard work-space-limited nondeterministic guess model (Diehl et al., Section 2.1).

FLMV, JACM 2005, Theorems 1.1/1.2: random-access Turing machine SAT deterministic c<golden ratio and **co-nondeterministic SAT** c<sqrt(2), each excluding n^c time with n^{d(c)} space for *some* positive d(c); not an explicit .5 lower bound. Diehl-van Melkebeek-Williams (2011) nondeterministic TAUT: d<cube_root(4) implies an exclusion at *some* positive space exponent e, not necessarily .5. Neither applies to SAT-witness nondeterminism without correct quantifier/model translation. Resolution lower bounds do not transfer to unrestricted execution.

## Reproducible strict C controls (COMPUTATIONAL)
Executed local standard-library audit.py and separate independent_replay.py, deterministic lexicographic enumeration with no PRNG. C=30/125; private-head existential projection 25/25 endpoint pairs; strict C private-head K6 gives all 5^6=15,625 shared rows blocked with 70,785 first-hit edge comparisons. All 15 original clause deletion complete SAT witnesses were generated and 210/210 remaining original C clauses checked; deleted clauses were not extendable. Independent quadratic evaluation replayed all witnesses. Exact scripts, full JSON deletion witness ledger, and SHA-256 manifest in local package T5C_Resource_Clocked_Specialist_Audit_20261119.zip. Script audit.py SHA256 510eefe1ec5967a9781e39aae7b96bb90a03ef0d22a05a331c4c4aca2d365f79. These are finite controls, not time-space lower bounds.

## Next blocker
Prove exhaustive or sound symbolic coverage of z, then demonstrate an actual resource-preserving reduction from unrestricted SAT to the stipulated row/block+critical-C promise, including the original source encoding and local access. Else the published deterministic SAT exclusion cannot transfer. P versus NP remains OPEN.

References: Buss-Williams, Computational Complexity 24 (2015), https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf ; Fortnow-Lipton-van Melkebeek-Viglas, JACM 52(6), 2005, https://lance.fortnow.com/papers/files/tst.pdf ; Diehl-van Melkebeek-Williams, J Comb Optimization 22, 2011, https://pages.cs.wisc.edu/~dieter/Papers/taut-ts-cocoon.pdf . Reviewed existing lead handoff blob 61926bd41b207cd6d0f6184d27331ed144febc30.
Additional older baseline: Fortnow and van Melkebeek, DIMACS TR 2000-06, exclude deterministic SAT at time exponent a and space b<((a+2)/a^2-a)/2. For a=1.33 this is b<0.2762629317655, so that older bound alone does not exclude b=.5. The newer Buss-Williams (1.34070,.5) refutation does.
