# RESEARCH-0006 — Post-revelation sequentiality and random-oracle barrier

**Global status:** P versus NP remains OPEN.

## Main literature result

The project's fresh-randomness / post-revelation-work line should not be promoted into a generic lower-bound mechanism.

Mahmoody, Moran, and Vadhan (CRYPTO 2011) prove a random-oracle limitation for time-lock puzzles: in the relevant model, a puzzle cannot require more parallel time to solve than the total work used to generate it. Their positive construction obtains a linear parallel-time gap only by allowing highly parallel puzzle generation.

Mahmoody, Moran, and Vadhan (ITCS 2013) obtain publicly verifiable sequential work in the standard model only under cryptographic assumptions including an inherently sequential hash function.

Guan, Riazanov, and Yuan (ePrint 2024/766) strengthen the negative side: pure-random-oracle VDFs with imperfect completeness and non-adaptive computational uniqueness do not exist without additional computational assumptions.

## RANDOM-SEQUENTIALITY-GUARD1

**Status: LITERATURE-SUPPORTED ARCHITECTURAL GUARD, not a new complexity theorem.**

Do not use
```
fresh random challenge
+ unique/canonical answer
+ efficient verification
=> unavoidable superpolynomial post-revelation ordinary work
```
as an unconditional SAT lower-bound lemma merely because the challenge is fresh or modeled by a random oracle.

This reinforces FRESH-EVAL1, RANDCLOSE1, TRACECLOSE1, and WRITE-0003: freshness blocks challenge-specific precomputation but does not rule out a reusable evaluator, parallel response, preprocessing, or compact implementation.

## Positive clue: execution extraction

Memory-hardness work suggests the correct architecture: strong resource claims become possible after an execution is extracted into a concrete lower-bounded operational object such as a graph pebbling. The analogy to CSE is:
```
arbitrary execution -> model-matched charged object -> independent lower bound.
```
The extraction theorem, not freshness or provenance, is load-bearing.

## SAT control: indirect diagonalization

Fortnow, Lipton, van Melkebeek, and Viglas (JACM 2005) prove polynomial time-space lower bounds for SAT on general random-access Turing machines. For every constant c below the golden ratio, some positive d rules out deterministic SAT time n^c and space n^d.

This is a genuine arbitrary-algorithm lower bound in a constrained resource region. It does not extend to arbitrary polynomial time and space and does not prove P != NP.

## RESOURCE-REGION-COMPILER1

**Status: CANDIDATE / calibration target.**

Try to compile an assumed polynomial SAT algorithm A into an equivalent uniform SAT algorithm A' landing in a known forbidden deterministic time-space region:
```
for every A in DTIME(n^k) deciding SAT,
construct A' deciding SAT with
T_A'(n) <= n^c and S_A'(n) <= n^d
for a pair (c,d) excluded by an unconditional SAT time-space theorem.
```

The raw target is probably too strong: generic simulation does not reduce an unknown polynomial exponent k to fixed c<1.618. Its value is that it is falsifiable and model-matched.

Hostile controls: padding, arbitrary k, recomputation-based space reduction, random-access simulation overhead, oracle replacement, algebrization, and hidden assumed speedup.

## Handoffs

**PROOF:** Compare CSE/RESTRICTED-ACCESS-ELIMINATION1 with the exact indirect-diagonalization machinery and ask whether current source localization can force a known forbidden time-space pair without representing A as DPLL/resolution/etc.

**RED:** Attack RESOURCE-REGION-COMPILER1 with arbitrary polynomial exponent and padding. If every route requires reducing unknown k to fixed c<1.618, retain only as calibration.

**LEAD:** Downgrade generic post-revelation sequentiality to diagnostic/hostile-control status.

**WRITE:** Synchronize RANDOM-SEQUENTIALITY-GUARD1 into main2/main3 if the random/post-revelation route remains live.

## References

1. M. Mahmoody, T. Moran, S. Vadhan, "Time-Lock Puzzles in the Random Oracle Model," CRYPTO 2011.
2. M. Mahmoody, T. Moran, S. Vadhan, "Publicly Verifiable Proofs of Sequential Work," ITCS 2013.
3. Z. Guan, A. Riazanov, W. Yuan, "Breaking Verifiable Delay Functions in the Random Oracle Model," Cryptology ePrint 2024/766.
4. L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, "Time-Space Lower Bounds for Satisfiability," JACM 52(6), 2005.
5. D. van Melkebeek, "A Survey of Lower Bounds for Satisfiability and Related Problems," ECCC TR07-099 / Foundations and Trends in TCS.
