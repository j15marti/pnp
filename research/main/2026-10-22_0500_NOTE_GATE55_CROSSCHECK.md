# GATE55 cross-check (hourly watch)

**Global status: P versus NP OPEN. P versus RP OPEN.** No new claim beyond the corpus.

- **COMPUTATIONAL:** brute-force over all same-hash pairs agrees with `rank([H;HA]) == rank(H)` in 900/900 random GF(2) instances (s<=6, k<=4), supporting Lemma 55A. Script: `research/main/2026-10-22_affine_lumpability_gate55_crosscheck.py` (<5 s).
- **Observation (COMPUTATIONAL, not a theorem):** lumpable fraction among uniform random (A,H) falls fast: s=3,k=1: 48/150; s=4,k=2: 16/150; s=5,k=3: 1/150; s=6,k=3: 0/150. Corollary 55B therefore applies only to *engineered* affine verifiers; generic affine machines with short hashes are not lumpable. Heuristic: roughly 2^{-k(s-k)} (CANDIDATE, unproved).
- Transfer classification: Lemma 55A is an exact linear-algebra transfer (Myhill-Nerode / lumpable Markov chain, Kemeny-Snell); the step to general circuits is blocked by Lemma 55C (coNP-complete quotient validation). Unrestricted bridge remains OPEN.
- Next angle: test whether lumpability of the *minimal* H (smallest invariant subspace containing the acceptance functional, Krylov/observability subspace) has small dimension k for affine verifiers arising from XOR-SAT-style RP checks. This is the control-theory observability transfer (observable quotient), EXACT for affine, ANALOGY for nonlinear.
