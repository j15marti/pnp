# RP AFFINE-BASIS25 | 2026-10-22 08:36 Asia/Seoul

**STATUS:** P=RP OPEN; P!=RP OPEN; P vs NP OPEN. **ESTABLISHED restricted** uniform derandomization theorem, not universal derandomization.

## Pre-source hypotheses and bounded coverage
Recorded H1 full-rank affine-coordinate basis-invariant small-bias hitting, H2 dense invertible XOR source network with nonlinear local factors, H3 rank-deficient local-rejection-sum falsification **before** consulting original sources. Directly read exactly three repository originals this run: COMPONENT-BIAS23 handoff (blob `18a145f277807167b2401b235464c1d1ce6370e3`), `experiments/wrapped_dag/wrapper_as_sat_prime_lineage_toy.py` (blob `95abeb9447a71b4ef6cb523e58adace6da6c808f`), and AFFINE-LUMPABILITY-RANK-GATE55 handoff (blob `943a6c94222b29414da40cacdfd2f890175f00de`). User-provided :12 SOURCE-CHANNEL21/DIGEST-LUMP19/CLAUSE-COHERENCE20 were audited as handoffs, not falsely counted as direct reads.

## AFFINE-BASIS25 theorem, established restricted
For uniform RP verifier `R(x,r)` on m genuine independent original random bits, assume the **complete** acceptance function is
`R(x,r)=AND_{j=1}^s f_j(Y,Z_j)`, where `Y=A_0 r+b_0` has c bits, `Z_j=A_j r+b_j` has <=k bits, and **all concatenated affine row vectors** are linearly independent over GF(2). Here c,k=O(log n), s,m=poly(n); syntax of XOR preprocessing, factor DAG dependencies and row rank must have polynomial-time uniform source certificates.

Choose power-of-two `q >= 16*m*(s+1)*2^(c+ceil(k/2))`. Enumerate a,z in GF(q) and the **original** m-bit tapes `r_i=Tr(a*z^i)`, i=0,...,m-1. Every YES instance has a tape in this multiset that the **unchanged verifier** accepts. All NO tapes reject. Size `q^2=O(m^2(s+1)^2 4^c 2^k)=poly(n)`; seed enumeration, irreducible-polynomial search, field arithmetic, input access, original verifier evaluations and peak workspace are all polynomial. No advice or independent gate traces.

**Proof:** Uniform original r makes Y,Z_1,...,Z_s mutually independent from row rank. Some Y=alpha gives conditional YES acceptance >=1/2, hence local conditional rejection probabilities delta_j obey sum delta_j <= ln2. The trace tape distribution has every nonzero parity bias <=eps=(m-1)/q by polynomial root counting. Parity bias is invariant under full-row-rank affine coordinate maps. E=[Y=alpha] has normalized Fourier spectral L1=1. B_j=[f_j(alpha,Z_j)=0] has spectral L1<=2^(k/2). Thus P_H(E)>=2^(-c)-eps, P_H(E B_j)<=2^(-c)delta_j+eps*2^(k/2). Therefore P_H(R=0 | E) <= (ln2+s*2^c*eps*2^(k/2))/(1-2^c eps) <= (ln2+1/16)/(15/16) <1. A valid original accepting tape is hit.

The hitting list does not use the hidden basis, factor partition or accepting seed, but **membership in this restricted subclass is a source-certification promise**; no general Boolean-circuit semantic factor compiler is claimed.

## Real gate/source audit
For 16 original bits, define p=XOR_i r_i, y_i=p XOR r_i. Matrix I+J has rank 16 and squares to identity in GF(2), and each y_i depends on 15 primary source bits. Acceptance is four disjoint OR3 blocks AND (y15 OR the fifth OR3 block). Its source-visible shared DAG contains 31 XOR, 11 OR and 4 AND gates, 46 total. Exact original YES acceptance =36015/65536=0.5495452880859375 and ANF degree 16. The per-primary-tape functional Tseitin extension is unique. Sampling gate auxiliaries independently would yield an incorrect probability. GF(256) empirical test has 65,536 seed pairs, 7,701 distinct tapes and 35,312 YES accepting pairs; q256 is *below* the conservative theorem threshold for m16.

Separate theorem-sized control m=3,c=1,k=1,s=2, q=1024: 1,048,576 seed pairs, 523,264 YES-accepting, zero NO-accepting; max of seven nonzero parity biases exactly 2/1024 (the root-count bound). Exact original YES density 1/2. Independent proper forced-3CNF source scanner: 128 YES witness recoveries and 128 augmented UNSAT NO controls, with 16,384 original random tapes checked. Total standalone Python auditor: **95,764 assertion-accounted checks, zero failures**.

Rank is essential: f1=f2=[r0=0] yields density 1/2 and local rejection sum 1 > ln2; duplicate affine coordinates invalidate the independence step.

## :12 P!=RP red team
SOURCE-CHANNEL21 capacity h*2^(q+b*t-n) is correct only under its stated transcript and equality-probe interface. Explicit formula-clause reads must be charged, and forced-3CNF sources reveal the missing excluded assignment. The inspected WRAPPER toy directly calls DPLL on `cnf.clauses`, has t1=s, b1=t1, L1_T=b1, t2=L1_T, hence t2=s; hardcoded stage SAT results mean it is not the generalized SHA/timer solver. Toy hashes 8 and 1 are different, not a collision. Complete generalized WRAPPER source-read q,b,t,h is **OPEN**. AFFINE-LUMPABILITY-RANK-GATE55's affine-transition congruence check is a separate rank criterion and does not make an arbitrary nonlinear digest complete.

Primary methods: Naor-Naor 1993 small-bias; Gopalan-Meka-Reingold-Trevisan-Vadhan FOCS 2012 combinatorial rectangles; Bazzi-Nahas 2017 cautions on low-density small-bias hitting. This construction assumes YES probability at least 1/2.

**Next test:** instrument ONE generalized WRAPPER source gate netlist, propagate affine GF(2) masks until genuinely nonlinear gates, check rank and apex+factor cones, count complete source/gate reads, and give either a certified restricted hitting-set application or a concrete violating gate/rank witness. Never promote a verifier-presentation obstruction to a language lower bound.

**Proof status:** affine-basis hitting ESTABLISHED restricted; explicit 46-gate and source scanner ESTABLISHED finite; generalized WRAPPER factorization CONDITIONAL/OPEN; universal derandomization and P vs RP/NP OPEN.
