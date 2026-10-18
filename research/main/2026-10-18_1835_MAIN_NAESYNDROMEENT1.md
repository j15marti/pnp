# NAESYNDROMEENT1: Gauge-quotient entropy and the fixed-support barrier

**Date:** 18 October 2026  
**Status:** PROVED/EXACT for the stated quotient/entropy and fixed-support circuit statements, pending independent review. COMPUTATIONAL for the finite Fano audit. No unrestricted monotone-circuit lower bound and no P vs NP proof.

## IDEAS PROPOSED BEFORE LITERATURE

**CANDIDATE A: support-revealed entropy collapse.** Test whether one SAT/UNSAT pair of gauge cosets remains hard after the scaffold and reference signing are known.

**CANDIDATE B: many-syndrome quotient.** Quotient the four-ary NAE sign-label space by vertex gauges. Test whether arbitrary SAT- and UNSAT-syndrome mixtures retain exact forest-local equality.

**CANDIDATE C: coset-avoidance formulation.** Characterize satisfiability of a syndrome by existence of a representative with no zero NAE edge.

**CANDIDATE D: direct code lower bound.** Try the 2025 code-based monotone lower-bound theorem. Falsifier: exact density forces a low-weight gauge codeword.

## LITERATURE CHECK AND REVISIONS

INFOFLOWCHAIN1 already proves that Shannon or directed information is not computational work: COPY and invertible prefix-parity transport can carry the entire source entropy cheaply. Entropy is therefore used here only to describe the quotient distribution.

Cavalar--Fabris--Mukhopadhyay--Srinivasan--Yehudayoff, ECCC TR25-219, Theorem 4.3, require a binary code with both large primal distance and large dual distance. In their notation a (d,t)-well-behaved code must satisfy d(C)>d and d*(C)>t, with 2n<d for an n-dimensional generator. The gauge code below fails the primal-distance requirement for every exact-density support.

de Rezende--Vinyals, CCC 2025, prove a DAG-like query-to-communication lifting theorem over nonbinary alphabets using colourful sunflowers. This directly targets monotone circuit size. After the code route fails, this is the strongest literature match: the NAE sign alphabet has four values, and the remaining target is a relation-level embedding into the exact-slice monotone KW game.

Classical nowhere-zero tension literature confirms that affine potential spaces, cycle constraints, and nowhere-zero representatives are standard combinatorial objects. The exact block condition below is proved directly and is not claimed to coincide with every standard tension convention.

## CONSTRUCTION OR PROOF ATTEMPT

Let H=(V,E) be a connected 3-uniform support with q=|V| and m=|E|. Each signed NAE class on edge e is an element of Q_e = F_2^3 / <111> ~= F_2^2. Put Q = direct_sum_e Q_e.

The vertex-gauge map is delta:F_2^V -> Q, with (delta x)_e = x restricted to e modulo <111>. Let C=im(delta) and let S=Q/C be the syndrome space.

### Theorem 1: Gauge-quotient entropy

For connected H:

- rank(delta)=q-1.
- dim(S)=xi=2m-q+1.
- If syndrome S is sampled arbitrarily and L is uniform in the chosen affine coset, then H(L|S)=q-1 and I(S;L)=H(S).

For J subset E, let v_J be the number of used vertices and c_J the number of connected components after isolated vertices are deleted. Then

H(L_J | S) = v_J-c_J = 2|J|-xi(J),

where xi(J)=2|J|-v_J+c_J is the incidence-cycle defect.

**Proof.** The kernel of delta consists exactly of gauges constant on each connected component. For connected H its dimension is one. The same argument on J gives kernel dimension c_J. Uniform gauge gives a uniform point in the projected affine image.

### Corollary 1: Arbitrary-coset-mixture forest independence

If J is a Berge hyperforest, then v_J=2|J|+c_J, hence xi(J)=0 and

I(S;L_J)=0.

This holds for **every distribution on syndromes**. Therefore any mixture of SAT cosets and any mixture of UNSAT cosets have exactly identical sign-label marginals on every forest.

This strictly strengthens the earlier two-companion construction.

### Theorem 2: SAT is a block-nowhere-zero coset property

Let 0_e be the NAE sign class falsified by the all-zero assignment. For signing sigma and assignment x, gauge-transforming by x gives sigma+delta x. Therefore

syndrome s=sigma+C is SAT iff
(sigma+C) intersects product_e (Q_e minus {0_e}).

So satisfiability is a well-defined Boolean predicate on syndrome space.

### Theorem 3: Fixed-support dual-rail syndrome extraction

For fixed labeled support H, all xi syndrome bits and their complements are computable from the four one-hot sign indicators per edge by a polynomial-size monotone Boolean circuit.

**Proof.** Fix a binary parity-check basis h_1,...,h_xi for C-perp. Each binary coordinate of a Q_e label, and its complement, is the OR of two of the four one-hot sign indicators. Thus every input bit to each parity check is available in dual-rail form. XOR on dual rails is monotone:

p XOR r = (p AND not-r) OR (not-p AND r),
not(p XOR r) = (p AND r) OR (not-p AND not-r).

A balanced tree computes each parity bit and complement. All xi checks cost O(xi*m) gates.

### Corollary 2: Fixed-support monotone simulation

Let f be gauge-invariant on fixed-support signings and let fbar be its syndrome quotient. If fbar has a general Boolean circuit of size s, then f has a monotone circuit on the one-hot sign-label promise of size poly(q+m)+O(s).

Hence fixed-support syndrome entropy cannot itself yield a monotone lower bound. A superpolynomial monotone lower bound there would require a corresponding general-circuit lower bound for the quotient predicate.

**CANDIDATE A is retired as a direct lower-bound route.**

### Theorem 4: Exact-density gauge codes have small primal distance

Let d_H(v) be the support degree of vertex v. Flipping only v yields a nonzero gauge word supported only on incident hyperedges. In the two-bit binary encoding each changed edge contributes at most two nonzero bits. Therefore

d(C) <= 2 min_v d_H(v) <= 6m/q.

For exact density m=Theta(q),

d(C)=O(1).

At the NAE density m=4q/3 this gives d(C)<=8; the transparent-leaf scaffold is even worse because it contains degree-one private vertices.

### Corollary 3: Direct well-behaved-code import fails

The Cavalar et al. code theorem requires primal distance exceeding twice the generator dimension. Here dim(C)=Theta(q) but d(C)=O(1), so no exact-density gauge code of this form can satisfy that theorem's hypothesis, regardless of its logarithmic dual distance/high girth.

**CANDIDATE D is retired for this code family.**

## WHAT ENTROPY LEAVES ALIVE

Random support permutation does not literally hide the support: the formula input reveals whether a support triple is present by OR-ing its four sign coordinates. What is not monotone-trivially available is a canonical alignment/parity-check basis for a support that varies with the input.

The surviving target is therefore relational rather than scalar-entropic:

support-varying exact-slice mKW -> large DAG-like protocol.

The four-valued edge alphabet and exact forest independence fit the colourful-sunflower lifting framework. The concrete next construction is to start with a hard high-width 4-ary CSP search relation, compose it with the nonbinary indexing gadget, and embed that relation into the monotone KW game of the exact-density NAE slice while preserving the output coordinate and critical Hamming layer.

## TESTS AND OUTCOME

A complete Fano-plane audit used support triples

012, 034, 056, 135, 146, 236, 245.

The gauge code has rank 6, orbit size 64, syndrome dimension xi=8, and block-support minimum distance 3.

All 4^7=16384 signings partition into exactly 256 gauge cosets of 64 signings. Exhaustive NAE evaluation gives:

- SAT cosets: 255
- UNSAT cosets: 1

Let mu_SAT be uniform over all SAT cosets and mu_UNSAT uniform over the unique UNSAT coset. Across every single-edge sign pattern and every pair-edge sign pattern, the maximum probability difference is exactly 0. At order three, a Berge cycle becomes visible. The maximum observed difference is 0.01568627450980392; one pattern has probabilities 0.015563725490196079 and 0.03125.

This exactly matches the symbolic forest/cycle theorem.

## OUTCOME

- Candidate A: FALSIFIED/RETIRED as a direct entropy lower bound.
- Candidate B: PROVED/EXACT. Every syndrome mixture has identical forest marginals.
- Candidate C: PROVED/EXACT. SAT is a block-nowhere-zero affine-coset property.
- Candidate D: FALSIFIED/RETIRED for exact-density gauge codes because primal distance is necessarily O(1).

The main positive change is that the entropy picture is now exact: the local views erase **all syndrome information**, not merely the SAT/UNSAT bit. The main negative change is equally exact: on fixed support the syndrome itself is polynomially recoverable in the monotone dual-rail model.

## NEXT TARGET

Build a colourful-sunflower lifting interface into the exact-slice KW relation. The gauge theorem should serve as the local full-range certificate, not as a claimed gate-cost measure. The load-bearing missing lemma is an output-preserving embedding from a lifted high-width 4-ary CSP search relation into NAE-UNSAT-vs-SAT on the critical slice.

P vs NP remains OPEN.
