# WCD-0001: audit of the bridge SAT in P => W_R(N) <= poly(N)

Status: red-team audit. Nothing here is a lower-bound proof. P vs NP OPEN.

## Setup
R a propositional proof system (Cook-Reckhow: poly-time verifier V_R, F in UNSAT iff some pi with V_R(F,pi)=1). cost_R = |pi| (or time/space variants).

## Claim A (PROVED/EXACT): bridge fails for fixed weak R
Take R = Resolution. Haken: PHP_{n}^{n+1} needs 2^{Omega(n)} size. So W_R(N) is superpolynomial. Whether SAT is in P is untouched. Hence "SAT in P => W_R poly" is not a theorem for Resolution (it is false if SAT in P and the Haken bound holds; the hypothesis is not known false, so the implication is only "known false" given SAT in P, which is itself unknown; the implication is refuted in any world where SAT in P). Conclusion: the bridge cannot hold for any R with a known superpolynomial lower bound unless SAT not in P.
Caveat: since SAT in P is unproven, strictly the statement is: bridge for Resolution implies SAT not in P. A bridge proof would therefore itself prove P != NP. Same for every R with known lower bounds (CP, PC, bounded-depth Frege).

## Claim B (KNOWN): bridge for strong R
If R is p-optimal (p-simulates every proof system), then SAT in P => NP=coNP => some system is poly-bounded => R is. So the bridge holds, but then W_R superpoly <=> NP != coNP. Existence of optimal systems is open (Krajicek-Pudlak 1989; oracles: Egidy-Glasser STOC 2025).

## Claim C: "free optimal sequence" is not a relaxation that helps
min over pi is the NP-certificate quantifier already in Cook-Reckhow. Lower bound on min cost = lower bound on shortest proof. The only relaxation relative to algorithms: proofs can be nondeterministic. A deterministic SAT algorithm's trace is one such proof only in a system able to verify the algorithm's correctness (needs provable soundness, cf. bounded arithmetic PV/EF: if PV proves A correct, EF polynomially simulates A's refutations). Soundness proofs of A are not assumed.

## Weakest sufficient bridge, restated (CANDIDATE)
Replace "fixed R" by a *family* indexed by algorithm: R_A = derivations that are traces of deterministic algorithm A with resource budget. Then W_{R_A} is bounded by A's runtime by definition, and the question becomes the repo's existing time-space charged-trace spine (ARC/FLMV). No new content from the minimum-over-sequences relaxation.

## Hard-instance plan
Test multisign DAG hypergraph encodings of Tseitin(expander), PHP, random 3-CNF; compute exact minimal derivation sizes for tiny n by exhaustive search (future run; each Python call <30s, chunked by n).

## Literature
- Cook-Reckhow 1979; Krajicek-Pudlak 1989 (optimal systems / fast consistency provers); Haken 1985.
- Egidy, Glasser, arXiv 2408.07408 (STOC 2025); Egidy, arXiv 2602.02294.
- MFCS 2023 paper on p-optimal systems for SAT/TAUT and the Boolean hierarchy over NP.
Transfer classification: Cook-Reckhow and Krajicek-Pudlak = directly transferable theorems; oracle results = barrier (relativization); "algorithm-trace" system = analogy needing a new transfer theorem.
