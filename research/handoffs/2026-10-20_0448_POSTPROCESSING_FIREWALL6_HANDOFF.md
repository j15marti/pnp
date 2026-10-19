# POSTPROCESSING-FIREWALL6 handoff | 2026-10-20 04:48 Asia/Seoul

## New theorem

Any deterministic or randomized compact target computed only from the repeated public-seed masked transcripts is a source-independent Markov postprocessor. Total variation cannot increase, so the prior requirement

`1-(1-alpha)^r >= 1/3`

still holds. Hashing, majority encoding, and transcript compression cannot reduce the `Omega(1/alpha)` evidence-sample requirement.

This does not prove `Omega(r)` construction time for a fused implementation. A target with increased distinguishability must use additional source-dependent access or a different random experiment; treat it as a new charged `R_k`, not as postprocessing.

Exact audit: every Boolean compressor for the canonical `alpha=1/2` model at `r=1,2,3`; 32,904 compressors, 32,910 exact assertions, zero failures.

## Next falsifiers

- **MCSP:** classify every proposed combiner as transcript-only or direct-source; prove both promises under the actual CHMY randomness.
- **Universal Solver:** expose direct source calls, encoder exponent, output length and peak live state.
- **ARC:** determine whether fused construction—not just serialization—meets the contractor inequalities.
- **Red team:** attack shared-seed correlations, hidden source reads and promise leakage.
- **Synthesis:** reject a compact-target claim without a Markov/access ledger and ordinary-total witness semantics.

Root `main.tex` remains unsafe and untouched. Compact History is diagnostic only. **P versus NP OPEN.**

END_OF_VERIFIED_HANDOFF::POSTPROCESSING_FIREWALL6
