# CLOCKASYMTRANSFER24 | Asymmetric YES-section transfer

**Date:** 2026-11-17 America/Los_Angeles. **Status:** PROVED/EXACT conditional implication; no actual quotient constructed. Independent review OPEN. P versus NP OPEN. CLOCK-INDEPENDENT-GATE1 is outside the five TMR manuscript owners.

## Proposed mechanisms and falsifiers

(A) Seek *YES-only* short circuit representatives, not cheap representatives for every target. Falsifier: NO source shares an image with a short-circuit source.
(B) Use the existential bounded-circuit image predicate, not unrestricted existential image membership. Falsifier: CLOCKMASKEDINVERSE22 has easy general image membership but PSPACE-complete supplied-circuit equality.
(C) Cofinal contraction of both target and short-witness length absorbs a *fixed joint* PH verifier exponent. Falsifier: stage-specific exponents grow as lambda^(-j), or source compilers grow too costly with stage j.
(D) Mere target length contraction without compressed YES sections is inadequate. Falsifier: identity quotient preserves labels but requires long YES witnesses.

Read November 15 end-to-end directive, AGENTS.md, CODEX.md, pnp-research skill, LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, K_ELIMINATION_TRANSFER4, SOURCEQUERY_SYNTHESIS10, CLOCKMASKEDINVERSE22 and CLOCKWITNESSPH23; surveyed current other-agent issue #3 updates and duplicates. The quantified stage and reduction-composition ideas are classical; no priority claim.

## ASYMMETRIC-YES-TRANSFER24: exact conditional theorem

Let N=2^n and let s(n)=floor(N^mu2), where mu2 is **the particular constant** appearing in Cheraghchi-Hirahara-Myrisiotis-Yoshida's randomized one-way-input/one-work-tape MCSP N^1.99 lower bound, STACS 2021. Let Y={f:CC(f)<=s}, NO={f:CC(f)>s}. Fix 0<lambda<1, a>0 and 0<=delta<0.90.

Suppose an **unconditionally specified** family H_(j,n), for every fixed nonnegative integer stage j, has all four properties:

1. A headerless one-way read-only input, single writable work-tape compiler consumes the **authentic N source bits** and computes a fully serialized target H_(j,n)(f) of length m_j<=N^(lambda^j+o(1)). Its **same-run total time** is N^(1+delta+o(1)), with a single delta independent of j and all source parsing, workspace and output costs counted. Fixed-j multiplicative constants are allowed.
2. An effectively computable gate budget w_j<=N^(a lambda^j+o(1)) has **YES-image coverage**: for every f in Y, some legal n-input circuit C of at most w_j gates satisfies H_(j,n)(TT(C))=H_(j,n)(f).
3. **NO exclusion**: for every f in NO, no such circuit C of at most w_j gates has the same image. Once w_j<=s, this follows from full exact purity H_(j,n)(Y) intersect H_(j,n)(NO)=empty, but full purity is not needed as a separate assumption.
4. The **joint succinct equality predicate** E(n,j,y,C)=[C is legal AND H_(j,n)(TT(C))=y] is uniformly in ONE fixed PH level, with j, n, target and candidate circuit all actual inputs. This is much stronger than P-time existential-image recognition or fast explicit-source streaming.

**Conclusion: these four premises imply P != NP.** The theorem is a *sufficient target for a future construction*, not such a construction.

**Proof.** Assume P=NP, so PH=P. Target predicate T(n,j,y)=[there exists a legal circuit C with <=w_j gates such that E(n,j,y,C)] is in a single fixed PH level and therefore in deterministic P with some unknown but FIXED exponent kappa. Circuits of w_j gates admit descriptions of L_j=O(w_j log(n+w_j))=N^(a lambda^j+o(1)) bits. Constructing the unary pad 1^L_j is an ACTUAL charged step on the same work tape, costing at most O(q_j^2) time, where the padded target input length q_j=N^(A lambda^j+o(1)) for A=max(1,a).

By YES coverage and NO exclusion, T(n,j,H_(j,n)(f)) decides *exact ordinary MCSP[s]* on all N-bit inputs. A standard fixed multitape P algorithm for T can be sequentially simulated using the single **same writable work tape** after H has finished its genuine input scan, for time q_j^K with one finite K independent of j (absorbing quadratic and fixed overhead). Thus the complete physical machine has time at most N^(1+delta+o(1)) + N^(K A lambda^j+o(1)). Choose a SINGLE fixed stage j, after the hypothetical K is known, satisfying a lambda^j<mu2 and K A lambda^j<1.90. This stage is selected among previously defined H_j, without changing any source bit map based on K. The total time is O(N^1.95) for sufficiently large N, contradicting CHMY's unconditional randomized one-tape N^1.99 bound at mu2. Hence P!=NP conditional on the displayed construction. QED.

**Important:** General target existential-image recognition is NOT required, nor is uniform reconstruction of a source preimage. Only jointly PH-low supplied-circuit equality and existential **bounded-YES-circuit** classification are required. Conversely, an arbitrary H that gives short circuits for *all* its images would make H(Y)=im(H) and automatically fail NO exclusion. The search target is deliberately asymmetric.

## Falsification and reproducibility

The standard-library Python audit exhaustively enumerates all 256 n=3 source truth tables. It uses **minimum binary AND/OR/XOR formula-gate count with free complemented edges**, not ordinary MCSP circuit complexity. Exactly 8,30,114,80,24 tables have formula costs 0,1,2,3,4. For s/w pairs (1,0), (2,1), (3,2), six image maps are evaluated: parity, weight histogram, first/last bits, adjacent-pair histogram, identity, and a deliberately circular one-bit formula-complexity oracle. There are 18 configurations x 256 inputs = **4,608 exhaustive source-image evaluations** with zero assertion failures.

At s=2,w=1, parity/first-last have short-witness NO collisions; histogram and k-gram counters fail YES coverage and NO exclusion; identity has NO exclusion but no compressed YES section; the artificial decision oracle passes both but merely embeds the original decision and has no verified cheap uniform compiler. These controls show that the properties must be checked separately; finite formula complexity is not evidence about real MCSP.

Numerical cofinal tests for lambda=1/2,a=2 and fixed K in {1,2,4,10,25,100,1000} found stages j={2,3,4,5,6,8,12} with 2 K a lambda^j<1.80. A hostile *stage-dependent* K_j=2^j instead has K_j lambda^j=1 for every j, so it does NOT support uniform exponent absorption. No P=NP hypothesis, PH oracle or one-work-tape complexity bound was experimentally tested.

## SAME_REALIZATION ledger / gates

**Resource ledger:** authentic N-bit read-once headerless input; fully charged H computation and serialization N^(1+delta+o(1)); short circuit description L_j; polynomial verifier under hypothetical P=NP; sequential one-tape simulation overhead within finite K; all on one physical work tape. Peak workspace belongs to this same run; no random oracle, free preimage circuit or uncharged output. Source and target threshold must both match the exact mu2 used by CHMY; the smaller magnification mu1 is not interchangeable.

**DISJ:** NOT APPLICABLE, no rank invariant. **Relativization:** OPEN for any future unconditional lower bound. **Simultaneous DTISP:** OPEN until an actual compiler exists. **Deterministic configuration counting:** PASS only as ordinary upper-bound consistency, not a lower bound. Natural Proofs/algebrization and Horn, affine, parity, hash, source-as-seed, mixed-fiber, wrapper controls remain open for an actual quotient.

**Primary sources:** CHMY, STACS 2021, DOI https://doi.org/10.4230/LIPIcs.STACS.2021.23. Fortnow and Santhanam, STOC 2008, DOI https://doi.org/10.1145/1374376.1374398 (OR compression distinct from this MCSP target). **Do not** assert the latter's no-compression theorem directly applies to this quotient.

**NEXT:** ASYMMETRIC-YES-QUOTIENT25. Build or falsify an actual fixed clock-independent source-authentic H_j with both short YES-image witnesses and universal NO short-witness exclusion, a single PH supplied-circuit equality verifier and near-linear headerless one-work-tape compiler. Test all legal alternate circuits/decoders and true MCSP thresholds. P versus NP remains OPEN.
