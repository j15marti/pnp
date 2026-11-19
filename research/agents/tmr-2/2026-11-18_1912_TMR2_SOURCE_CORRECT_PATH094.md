# TMR-2/094: explicit-source correct-path obstruction and exact block-query firewall

**Date:** November 18, 2026 (Pacific). **Owner:** TMR-2 / PNP Information Necessity. The primary template remains the five-symbol beat-relation CSP R(a,b) iff b-a modulo 5 is 1 or 3. **Status:** PROVED/EXACT restricted results, COMPUTATIONAL finite checks, CONDITIONAL resource composition, and OPEN unrestricted lower bounds. Mathematical peer review remains outstanding. P versus NP remains OPEN.

## End-to-end target and falsifiers

The attempted pipeline is authenticated original CNF/T5 source, verified shared/private factorization, block-solving/rejecting calls for assignments z, paid universal or existential aggregation, sound YES/NO output, and a same-execution time/space ledger. The candidate to falsify is the inference that finding a refutable private block for each z requires the number of black-box block queries, even when an unrestricted solver inspects the complete encoded source. Controls: a short original-source refutation, a cheap total correct-path selector, T5 short-path contraction, and the complete child/time/space tariff.

## Theorem 094-A: exact quantified polarity

For a conjunctive source F(z,y)=AND_{b=1}^M F_b(z,y_b), with pairwise-disjoint private scopes y_b after fixing shared z:

SAT(F) iff EXISTS z FORALL b EXISTS y_b F_b(z,y_b).

UNSAT(F) iff FORALL z EXISTS b FORALL y_b NOT F_b(z,y_b).

Commutation holds only because the private scopes are disjoint and the aggregator is conjunction. If the original grammar specifies alternative row semantics, it needs a fresh proof of equivalence. A single refutable block for one z is not an UNSAT certificate. A SAT witness consists of one common z and all local witnesses.

## Theorem 094-B: a sharp restricted query bound

Give the solver only independent oracle bits Q(z,b), interpreted as the assertion that block b fails at z, and let R=2^q. The UNSAT decision predicate is H(Q)=AND_{z=1}^R OR_{b=1}^M Q(z,b). Its deterministic binary decision-tree complexity is exactly R*M by the standard adversary for a read-once AND-of-OR formula. Minimum positive certificate size is R, one positive cell for every row; minimum negative certificate size is M, all-zero cells in a single row. This theorem applies to independent oracle bits and does not carry to original-input access or correlated source-derived bits.

Executed minimax decision trees: (R,M)=(2,2) requires 4 queries and 79 memo states; (2,3) requires 6 and 679; (4,2) requires 8 and 6143. These are computational controls, not the source of the general adversary proof.

## Theorem 094-C: explicit-source three-resolution falsifier

For any number q>=1 of shared Boolean bits, let C_0=(z_1), C_1=(NOT z_1), and for i>=2 let C_i=(z_i OR NOT z_i). For each clause give its own fresh private bit y_i and define B_i=(C_i OR y_i) AND (C_i OR NOT y_i). Each individual unconditional B_i is satisfiable, and EXISTS y_i B_i(z,y_i) iff C_i(z). Hence for every z at least one block fails while the whole source is unsatisfiable.

Nevertheless the original source has an explicit THREE-inference ordinary binary Resolution refutation. Resolve the two clauses of B_0 over y_0 to derive z_1; resolve those of B_1 over y_1 to derive NOT z_1; resolve these to derive the empty clause. Source parsing, clause-address acquisition and all three inference validations are paid, but no scan of 2^q assignments is needed. Flip C_1 to z_1 for the matched satisfiable source (2^(q-1) admissible shared assignments).

More generally a bounded-width CNF G(z) embeds in this one-row, disjoint-private grammar by adjoining a fresh y_b to each clause (or group) in both polarities. The projected formula is exactly G. With slack for ordinary binary encoding and rounding, the instance can use O(N^.65 polylog N) blocks of size O(N^.35 polylog N). This is an exact semantics reduction, not a hardness result.

## Theorem 094-D: short selectors and wrong-path soundness

For every explicit CNF, including satisfiable ones, a uniform original-source scan maps a complete shared assignment z to the INDEX of its first violated clause, or to a NONE sentinel. That index has O(log M) bits. Every UNSAT source has a non-NONE output for every z, whereas a SAT source has a NONE output for at least one z. Checking total absence of NONE is the original UNSAT problem. For T5 choose the first violated genuine arc under a complete five-color assignment. A short supplied correct path is therefore no proof of the universal claim.

A one-sided deterministic SAT specialist may emit a verified witness or UNKNOWN; a one-sided UNSAT specialist may emit a genuine locally verified refutation or UNKNOWN. Neither may confidently emit the wrong label. If two uniform specialists together cover every input, running both is a deterministic full decider with sum-of-work time and peak sequentially reused storage. Free polarity routing is answer advice unless computed and charged.

For a nondeterministic k-bit alleged UNSAT path, every accepting wrong path must be forbidden on SAT inputs. If sound acceptance is polynomially verifiable and k=O(log N), enumerating all 2^k paths gives a polynomial-time deterministic UNSAT decider. For k=poly(N) the existence of such polynomially verifiable UNSAT certificates gives coNP subseteq NP and hence NP=coNP, not a time lower bound. An adaptive/alternating certificate must encode the whole strategy or charge universal branches, not just one favorable trajectory. Read-only external certificate access and writable machine memory must be reported separately. These conclusions are conditional on declared uniformity and verification model.

## Conditional resource ledger, including shared assignment enumeration

Let N be encoded input bits, row cap N^.195, blocks-per-row cap N^.65, child length cap N^.35, q shared Boolean bits, and a correct uniform child SAT seed of time L^a and space L^b. Assuming charged O(L polylog N) materialization and an authenticated, low-space source iterator, a sequential exhaustive decision procedure has

T <= T_auth + O(2^q N^.845 (N^.35+N^(.35a)) polylog N)

and writable S <= S_auth+O(q+N^.35+N^(.35b)+log N), with all used buffers counted. These are conservative upper estimates, not intrinsic lower bounds. A seed exponent a=1.33 gives per-z exponent 1.3105, leaving only .0195 exponent for 2^q to remain within N^1.33. With q=0, a<=97/70≈1.385714 is necessary for this particular composition to meet 1.33. A generic merely polynomial seed does not suffice; a=2 produces 1.545. Standard decision-to-witness via O(L) self-reduction would produce 1.6605 in the a=1.33 example, unless a charged direct-witness solver is supplied. All three independent explicit-size maxima cannot simultaneously correspond to disjoint substrings of N bits, because .195+.65+.35=1.195>1. Virtual children, overlap or slack must be explained. For 5-ary T5 shared variables replace 2^q with 5^q.

## Matching original-T5 controls and finite evidence

The existing four-path girth-five matched T5 sources have (n,m)=(9,11) and exactly 0 versus 135 full-label solutions. Transitive K4 has 0 solutions, while a K4 induced by T5 has exactly 5. A selector over genuine violated arcs exists for both YES and NO. Direct enumeration and the separately authored /093 cycle-syndrome count match. The transitive K4 is already ruled out by its outdegree-three vertex and T5 maximum outdegree two; the four-path sources permit five-state endpoint contraction. Neither large raw assignment count nor a cheap first-bad index implies necessary search work.

Local full verifier: 3,911,558 assertions and zero failures, including every one of 5^9 assignments on both nine-variable sources. Complete local Python and raw JSON are separately available in the conversation. A compact repository verifier covers shared-block families q=1..8, the three minimax trees, and all matched T5 counts. It depends only on the preceding published /093 verifier for an independent count cross-check. Full Python host wall time 1.8838 seconds; this is not native bit-model time or physical machine replay.

## Machine lower-bound literature and firewall

[1] Fortnow (1997), CCC: nondeterministic SAT on the stated random-access Turing-machine model cannot simultaneously have N^(1+o(1)) time and N^(1-epsilon) workspace for fixed epsilon>0. This is not about free external read-only certificates. https://doi.org/10.1109/CCC.1997.612300

[2] Fortnow, Lipton, van Melkebeek and Viglas (2005), JACM, and the 2000 quantitative precursor: a deterministic random-access SAT bound excludes simultaneous N^a time and N^b space for b<((a+2)/a^2-a)/2. At a=1.20 the right hand side is 23/45>.5; at a=1.33 it is about .276, not .5. This theorem does not rule out the proposed (1.33,.5) pair. https://doi.org/10.1145/1101821.1101822 ; https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html

[3] Buss and Williams (2015), Computational Complexity: deterministic SAT has simultaneous time-space exclusions at exponent c<2cos(pi/7) for N^o(1) workspace, not for arbitrary half-linear space. The paper's upper barrier concerns its specified alternation-trading framework. https://doi.org/10.1007/s00037-015-0104-9

[4] Diehl, van Melkebeek, and Williams (2007): nondeterministic TAUT/co-nondeterministic SAT excludes N^c time with N^o(1) space for c<4^(1/3), in the stated machine/reduction model. Do not transfer this to ordinary nondeterministic SAT or a free guessed refutation. https://pages.cs.wisc.edu/~dieter/Research/complexity.html

These are distinct deterministic decision, nondeterministic SAT, and nondeterministic TAUT results. Proof-system-specific refutation length does not give an unrestricted deterministic running-time lower bound. No matched known theorem here excludes the specific deterministic N^1.33 time, N^.5 polylog N space pair.

## Four gates, peer overlap and handoff

DISJ: PASS for recognizing restricted-versus-source distinction. Relativization: PASS as a barrier, not an unrestricted theorem. Simultaneous DTISP: OPEN for the (1.33,.5) goal; known small-space results remain correctly scoped. Deterministic configuration counting: PASS as an upper consistency audit, not a lower bound. Algebrization/Natural Proofs are not engaged by these restricted semantics, and must be reopened on any general-circuit claim.

The concurrent TMR-4/097 open PR #313 independently develops exact row factorization, polarity soundness and the 97/70 exponent. Those overlapping elements are credited, not claimed new. TMR-2/094 specifically owns the independent-oracle AND-of-OR boundary, the three-inference direct-source counterexample, uniform first-bad selector, and additional matched T5 controls. Do not overwrite peer main4.

Named TMR-4 handoff: **D2-SOURCE-FIRST-FAIL-POLARITY-FIREWALL094**. Any attempted lower bound must survive all direct original-source inspection, ordinary Resolution of the compact contradiction, source-recognizable path transfer, stored/read-only strategy costs, all child polarities, failures and peak same-run workspace.

**Next load-bearing lemma:** implement a fully costed authenticated virtual-child source interface for q=O(log N), or provide a concrete failure that proves no such implementation exists in a precisely declared restricted machine model. Independent mathematical peer review, native preflight, full LaTeX build and physical-machine replay remain OPEN. P versus NP remains OPEN.