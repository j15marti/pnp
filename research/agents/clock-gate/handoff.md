# Clock Gate scoped research handoff, 2026-11-18 05:11 Asia/Seoul
Owner: CLOCK-INDEPENDENT-GATE1 legacy research stream. Scientific status: P versus NP OPEN, no fully promise-pure quotient or machine-lower-bound transfer.

**Latest:** [CLOCKKGRAM19 exact report](2026-11-18_0511_CLOCKKGRAM19.md) (commit e0d70150e4516c32dc667fdaff99d06d93c02f98); audit [Python](../../../experiments/meta_lift/2026-11-18_clock_kgram_section19_audit.py) (commit 5db3fc22d00ff4c1c4516e575e8ce50cf379d72a), [raw digest](../../../results/raw/meta_lift/2026-11-18_CLOCKKGRAM19_raw.json) (commit a19945726268a4a5667d4cfaf6dc3d2f42329222), all independently read back.

**PROVED/EXACT restricted, independent review pending:** An N=2^n-bit word's full binary k-gram count vector and (k-1)-bit endpoints have a representative word g with identical statistics and Boolean circuit complexity at most C[2^k(n+1)^2+4^k(n+1)]. Explicit feasible labels admit a uniform polynomial-in-(2^k+n) compact witness constructor using de Bruijn cycle decomposition; binary adjacent-pair count has a direct O(n)-circuit two-run/alternating-tail form. Therefore, if original source MCSP YES includes circuits above this bound, every statistic-derived output label has a source YES representative and genuine NO labels cannot be separated.

**COMPUTATIONAL:** 5,078 source/k cases; 94,071 assertions; zero failures; exact compressed controls for 2^17,2^18,2^19-bit inputs. Seed 202611180511. Full local LaTeX, PDF, source, raw and BibTeX are retained outside the GitHub report. Local code SHA-256 a82dd0dd29101eab86c0cab62c7ea23590d0ad3edfa8f6bec290d01e1578e7a7.

**Charge:** One-way read-only input plus one writable tape can compute the k-gram output using O(N*2^k*(n+1)) sequential worst-case work, O(2^k*(n+1)+k) work bits, and O(2^k*n+k) output bits. The proposed reduction's failure is semantic NO purity, not uncharged cost.

**Scope guards:** This does not apply to address-indexed nonlinear changes, provenance not factoring through the k-gram statistics, source-bound decoder eligibility, or arbitrarily growing windows. It cannot establish a fixed NP/PH verifier for arbitrary postprocessing, a CHMY lower bound transfer, or P != NP.

**Peer precedence:** Current root AGENTS.md/CODEX.md and 2026-11-15 end-to-end coordination supersede historical tracker workflow. This handoff changes no TMR identity, schedule, or owner's manuscript. Existing THRES-STREAMSATURATION12/AUTOMATICSECTION15 already cover stationary automata; LSPV-5 REFEREE271 covers failure of fixed-window histograms as SAT labels. No generic novelty claim for Euler decomposition.

**ONE next dependency:** ORDER-SENSITIVE-SOURCE-BIND20. Construct or falsify a fully sourced, succinctly address-dependent one-pass nonlinear rolling summary with correctly charged provenance and mixed-fiber controls, then seek one jointly NP/PH-low verifier and fixed stage-independent exponent. Avoid rank-only and clock-circular claims.
