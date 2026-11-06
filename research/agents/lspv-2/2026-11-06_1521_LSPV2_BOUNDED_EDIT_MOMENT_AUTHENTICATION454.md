# LSPV-2/454 | Bounded-edit moment source authentication and Prouhet collision firewall

**2026-11-06 15:21 PST. Route A primary. PROVED/RESTRICTED + COMPUTATIONAL; universal FLMV contraction OPEN; P versus NP OPEN.** LSPV-2/LSPV-4 Route A and LSPV-1/LSPV-3/LSPV-5 Route B unchanged. No task schedules, native R_mix341 rules, inference weights or root manuscript changed.

## IDEA -> SEARCH -> ITERATE and falsifiers

Hypothesis: generalize the corrected LSPV-4/451 single-replacement modular checksum to at most k missing/duplicated facets using first k power sums. Falsifiers: (F1) false accept with <=k replacements, (F2) repeated extra facets evade the Newton argument, (F3) an >k-edit source passes although malformed, (F4) an unauthenticated source-header or full-array lookup silently spends parent-scale workspace. F1/F2 are ruled out only on the stated promise. F3 has explicit Prouhet counterexamples for every k. F4 is not waived; the resource claim needs an indexed authenticated header or fixed family facet generator.

Reviewed actual issue #3, LSPV-2/453 and LSPV-4/451 reports/handoffs, AGENTS.md, CODEX.md and repo skill, CLAUDE_ONETAPE-0001, GROK_REWIRE 2026-10-23, konard/p-vs-np/ISSUE_27_ANALYSIS.md (blob a58e3a10), blkph0x/p-vs-np-proof-research/AFFINE_CANCELLATION_LITERATURE_SCOPE.md (c4b47e6a), FRAT-XOR README (38a137bc), openai/math README (cc5b0a03). Read the primary FLMV 2005 source and Fortnow-Santhanam compression scope plus Newton/Prouhet literature. No claim of independent Google browser access. LSPV-4/451 already gave one k=2 collision; new local application is the general promise/collision pair with executable controls, not novelty of Newton or Prouhet.

## Established 3-CNF hard-family control

For a connected cubic graph G=(V,E), H=|V|, |E|=3H/2, charges chi_v in GF(2), and incident edge IDs a<b<c, original signed strict-3CNF contains for p,q in {0,1}:

$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),\quad \ell_0(x)=x,\quad\ell_1(x)=\neg x.
$$

There are m=4H distinct original clauses, 12H signed literals and N=Theta(H log H) encoded bits. Odd total charge is certified UNSAT; even charge SAT. Published exponential *ordinary DAG Resolution* proof-size lower bounds apply to suitable growing expander Tseitin families (Urquhart JACM 1987; Ben-Sasson/Wigderson JACM 2001). Finite prism test instances are correctness controls, NOT certified asymptotic hard sequences. GF(2) parity is a permitted very short semantic computation and blocks all-machine hardness inference. There is no 3-CNF reduction needed: these are the original source clauses.

## Theorem 454.1: exact bounded-edit promised stream

Let each of m unordered records be locally verified as one specific authenticated original signed facet ID in [m]. The input is promised to be either a permutation of these m facets, or a multiset with at most k missing original records and the same number of extra locally legitimate duplicates. Fix prime p>max(m,k). Keep count and moments P_j=sum_i ID_i^j mod p for j=1,...,k and compare them with the canonical moments.

**PROVED/RESTRICTED:** Every good permutation is accepted and every permitted nonpermutation is rejected. After cancelling equal records, let A be omitted and B be surplus root multisets, |A|=|B|=r<=k. Equal moment sums through r imply equal elementary symmetric coefficients by Newton identities, using characteristic p>r. Thus products of (X-a) and (X-b) are the same monic polynomial over GF(p). Equality of root multisets forces A=B; the chosen disjoint omission/surplus multisets then imply r=0. Repeated surplus IDs are covered.

Under a separately justified O(log N)-workspace facet generator/indexed verified header, sequential scan uses O(k log N) bits of transient/work state and O(N k polylog N) bit operations with schoolbook modular arithmetic. It is compatible as *one promised phase* with the target time N^(11/10+o(1)) for k=N^delta, delta<1/10, and with N^(1/2+o(1)) space for delta<1/2. It is NOT a complete all-input SAT compiler or a correct arbitrary-corruption validator. Actual host implementation retains arrays and cannot be cited as native-TM resource measurement.

## Theorem 454.2: Prouhet collisions disprove any general-input promotion

For any k and m>=2^(k+1), partition IDs 1,...,2^(k+1) using parity of the binary digit sum of ID-1. Let A be even parity and B odd parity. Both have 2^k members and identical power sums of degrees 0 through k **as integers**. Proof: generating polynomial sum_i (-1)^s2(i) z^i = product_{r=0}^k(1-z^(2^r)) has a zero of multiplicity k+1 at z=1; differentiation and conversion from falling factorials to power polynomials gives the equal sums. Replace each missing A facet with a duplicate B facet; all records remain locally valid, the multiset is NOT a permutation, but all k modular moment checks pass. The k=2 explicit collision is {1,4,6,7} versus {2,3,5,8}: both sum to 18, squares to 102. Such collisions already appeared as a finite example in LSPV-4/451. No moment-only accept rule covers all malformed inputs.

This does not defeat the corrected unrestricted one-pass Omega(m) deterministic permutation-checking state lower bound from LSPV-4/451. A multi-pass or otherwise exact fallback is necessary and must charge its own time and simultaneous peak space.

## Finite source-authenticated controls, independent implementations

Executed Python producer (seed 202611061519, prime 65537): original proper signed 3-CNF from six cubic prisms of H=6,8,10,16,32,64 vertices with odd and even charges. 208 genuine permutations accepted; 3,124 corrupted multisets with <=k replacements rejected; 52 Prouhet beyond-promise collisions accepted by the intentionally promise-only checker; 52 signed-clause corruptions and 104 wrong-length controls rejected; 7,082 Python assertions PASS. Independent Node.js rebuild of graph, literal signs, moments and K4 brute-force SAT labels passed 558 assertions, including 52 collisions. Host checks are not historical R_mix341 accepted-byte proofs or FLMV machine time/space measurements.

**Resource ledger:** zero mixed-calculus inference nodes and certificate inference bits; one input scan and m local indexed-facet reads; k modular registers and a record buffer; no paid child output, guests, discovery or joining because NONE is constructed. A real full-input Phi(A) must add authentication, local policies, failed branches, cache retention/recomputation, references, indices, guest simulation, output bits and simultaneous peak. No free splitter, oracle, proof-system transfer or omitted malformed source allowed.

## Remaining transfer and handoff

Route A: keep correct stronger all-corruption floor, allow Newton moment sketch only under explicitly proved <=k-change promise and a fully charged fallback. Try genuine solver-dependent *derived* short SAT children with authenticated joins; pure source-clause subsets and parity-family-only algorithms do not satisfy the all-input condition. Route B: neither native R_mix341 nor B3 altered.

The exact missing universal same-machine recursively iterable all-input transformation for every total polynomial SAT decider A remains:

$$
t'\le\max\left(\frac{11}{10},\frac35+\frac t2\right),\qquad s'\le\max\left(\frac12,\frac s2\right).
$$

Full locally executed producer, independent verifier, raw JSON and SHA-256 manifest are in the downloadable reproducibility archive. Root main.tex unchanged. **P versus NP OPEN.**

References: Fortnow/Lipton/van Melkebeek/Viglas (JACM 2005, doi:10.1145/1101821.1101822); Urquhart (JACM 1987); Ben-Sasson/Wigderson (JACM 2001); de Vries arXiv:2305.19850 (characteristic issue); classical Prouhet-Thue-Morse identity; Fortnow/Santhanam STOC 2008/JCSS 2011 (compression barrier has distinct premise).
