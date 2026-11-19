# TMR-3/100: strict C orbit routing and charged same-machine accounting
Date: 2026-11-19, America/Los_Angeles
Owner: TMR-3 / PNP Time-Space Tradeoffs
Status: PROVED (structural), COMPUTATIONAL (finite operations), CONDITIONAL (model transfer), OPEN (unrestricted lower bound).

## Canonical relation and revalidation

Use strict C(x,y,z) iff R(x,y)R(y,z)R(z,x) or R(x,z)R(z,y)R(y,x), where R(a,b) iff (b-a) mod 5 belongs to {1,3}. C has 30/125 valid triples, strict headed S has 40/125, historical exact-one Q has 60/125, old P/O has 20/125. The original library package `t5_strict_research_package.zip` and PDF were inspected; both local S/C gadget identities were independently verified on every terminal assignment (including 25 auxiliary choices).

**Previous TMR-3/099 Q findings require revalidation, not relabeling:** q=(0,4,2,2,4), p=(2,0,1,1,0), 1,584 Q deletion certificates, Q's projected S5 symmetry, and Q/P counts are not strict-C results.

## Theorem A: exact unpinned strict-C shared-assignment quotient (PROVED)

The automorphisms of C are precisely the ten color transformations a -> ±a+t modulo 5, as verified independently by enumerating all 120 color permutations. For s>=1 shared variables, rotate the first value to zero; reflection sends the remaining tail to its additive inverse. The sole reflection-fixed tail is the all-zero tail. Thus the exact number of global orbits is

K_C(s) = (5^(s-1)+1)/2 = (5^s+5)/10.

The sequence for s=1..6 is 1,3,13,63,313,1563. Every child under a common pure-C conjunctive block decomposition is equivariant, so testing one representative of each orbit is sound. The algorithm may enumerate tails lazily using O(s) color slots, charging O(s*5^(s-1)) time. This saves only a constant factor, not an exponential base. It is invalid when external color pins or noninvariant predicates break the symmetry.

## Theorem B: exact private-head C kernel (PROVED)

For fresh h used only in C(h,u,v), let w(d)=number of h values completing C(h,0,d). The exact kernel is

w=(0,2,1,1,2).

Hence projection of C(h,u,v) is exactly u!=v. For a source graph G, the full number of assignments (including every head) is the weighted sum over base 5-colorings of product of w(color difference) on the edges. This is not an unweighted counting reduction.

For the private-head encoding of K6, all 15 C clauses together are UNSAT. After deletion of *any* physical C clause, 120 base 5-colorings remain; each gives a multiplicity 2^7=128 over the 14 retained heads, while the deleted head is freely colored in five ways. The exact full-witness count is 120*128*5=76,800 for each of all 15 deletions. Two deletions were separately counted using direct C-predicate loops rather than reading the projected weight array. All 15 deletion instances have explicitly constructed, fully verified 21-variable witnesses. This is an easy intrinsically clause-critical example, not a hardness result.

## Theorem C: charged deterministic block recurrence (PROVED conditional on authentication)

Given M explicit blocks B_i(z,y_i) of the pure-C language with pairwise private-disjoint y_i after s shared variables z, an exact deterministic algorithm can scan K_C(s) representatives. For each representative, check blocks until the first truly negative child. All positive children before that index are failed attempts to discover a blocker and must be charged, along with materialization, positive witness checking, complete negative child decisions, prefilters, source access, output, and replay. A SAT output must contain and verify every original C variable and clause.

Writing tau(z) for the first refuted block, or M for a SAT row, a conservative exact charged upper recurrence is

T <= T_auth+T_pre+O(s*5^(s-1))+sum_(z in orbits)[T_route(z)+sum_(i<=tau(z))(T_mat+T_child+T_verify)_(z,i)]+T_replay+T_output+T_source_verify.

Sequential space: S_peak <= S_auth+S_pre+O(s+log K+log M)+max_i S_child(i)+S_live_reconstruction+S_replay_check, all in bits (3 bits per color plus address bits), including simultaneously live objects only. A write-only output tape does not make witness acquisition or repeated computation free.

If M<=N^.65 total blocks of size N^.35 and T_child(B)=B^(alpha+o(1)), a *fully visited* representative has child work N^(.65+.35*alpha+o(1)). Distinct N^.195 rows containing M independent blocks would exceed an N-symbol explicit source length, absent charged reuse/implicit generation. When s=N^.195, exhaustive orbit enumeration remains exp(Theta(N^.195)), so no n^1.33 uniform specialist follows.

## Correct polarity and machine model

Free correct-route indices are oracle information. A k-bit route must be correctly checked on wrong strings, without accepting a false SAT/UNSAT certificate. A literal negative-index table for K representatives needs K*ceil(log2 M) bits, or a succinct program whose evaluation and universal coverage must be charged. A single promised-SAT witness solver does not decide UNSAT. However, if sound bounded-resource one-sided SAT *and* UNSAT programs both exist uniformly, cap and dovetail them; the result is an all-input deterministic decider with comparable simultaneous time and space.

Buss and Williams (2015), as accurately tabulated in Buss's MFCS survey, exclude SAT in DTISP(N^1.34070,N^.5) on deterministic multitape **indexed random-access Turing machines** (with n^o(1) exponent slack). Thus a uniform unrestricted Boolean SAT decider at N^1.33, N^.5 polylog in that model is ruled out. This does not itself give a strict-C/RAM exclusion. C<->S gadgets permit constant-size fixed-width-record rewrites and virtual input indexing using O(logN) scratch and polylog work per access, but importing SAT's fine-grained exclusion to C still needs a valid near-linear reduction and a fully costed simulation. Nondeterministic TAUTOLOGIES bounds (Diehl, van Melkebeek, Williams) establish small e(d)>0, not the explicit e=.5 exclusion at 1.33. Named resolution lower bounds remain proof-system specific.

## Exact original strict-C operation counters (COMPUTATIONAL)

K6 all-C UNSAT, with six shared base vertices and fifteen private heads:
- All 5^6 labels: 15,625 shared assignments, 70,785 child calls, 55,160 failed negative-index attempts, 15,625 negative children, 210,509 direct C tests.
- D5 quotient: 1,563 representatives, 7,079 child calls, 5,516 failed attempts, 1,563 negative children, 22,424 direct C tests.

K6 minus edge (0,1), SAT:
- All labels: witness after 195 shared assignments, 516 child calls, 1,868 C tests.
- D5 quotient: witness after 133 shared assignments, 454 child calls, 1,558 C tests.
Both independently verified all fourteen clauses and emitted values for all twenty-one source variables, assigning the unused deleted head arbitrarily. The logical peak live color slots are 7 on UNSAT and 21 on SAT; source/counters/program/instrumentation are *not* included in that proxy. No source-independent time/space lower bound follows from these traces.

The standard-library script and full raw JSON are in `TMR3_STRICT_C_100_Reproducible.zip` (local generated attachment). Its deterministic SHA256 audit digest, excluding timing and tracer memory, is:
`a40d3e403fb2127b57eb3a0400107da92aa2e31931db35f21b0e919fd75121f6`.
Two repeated audits matched. Independent human mathematical review, native machine execution and full combined LaTeX compilation remain outstanding.

## Verification gates and open dependency

Disjointness/physical criticality: PASS for the K6 source. Relativization/alternate algorithms: OPEN; graph coloring, treewidth, GF(5), algebra and machine-specific shortcuts remain permitted. Simultaneous DTISP: only constructive charged upper accounting, no necessary-work lower bound. Configuration/advice: exact orbit upper bound, not an unrestricted information lower bound.

NEXT: C3-STRICT-C-SEMANTIC-BLOCK-ROUTING101. Find a uniform nontrivial strict-C source family with authenticated private-disjoint blocks and growing shared interface; establish whether a sound succinct refutable-block strategy can bypass the exponential representative scan with full acquisition and verification costs. P versus NP OPEN.

References: [1] Buss & Williams (2015), https://doi.org/10.1007/s00037-015-0104-9 . [2] Buss (2013), https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimitsMFCS/MFCS2013_Buss_revised.pdf . [3] Fortnow et al. (2005), https://doi.org/10.1145/1101821.1101822 . [4] Diehl et al. (2011), https://doi.org/10.1007/s10878-009-9286-x .
