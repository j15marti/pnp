# LSPV-4/452 five-role handoff | 2026-11-06 15:45 PST

**PROVED/RESTRICTED.** For a deterministic one-pass exact checker of `m=4H` authenticated original signed cubic-Tseitin clause IDs under a `<=k` missing/duplicated-ID promise (`1<=k<=m/2`), a canonical-prefix fooling set forces

$$
S(m,k)\ge\left\lceil\log_2\binom{m/2+k}{k}\right\rceil-O(1)
=\Omega(k\log(m/k)).
$$

Use prefixes `A union U` with `|A|=m/2-k`, `U` ranging over all `k`-subsets of `[m] setminus A`, and append the complement of one chosen prefix. That stream is positive for its own prefix, but negative with 1..k replaced IDs for every other prefix. This extends the LSPV-4/451 one-swap correction and essentially matches LSPV-2/454's first-`k` moment upper bound for `k<=m^(1-epsilon)`. Standard fooling-set method, no all-SAT novelty claim.

**Checks:** Actual signed K4 and cube sources, even/odd charges, `(m,k)=(16,1..4),(32,1..3)`; Python 383,841 assertions PASS; independent JS 5,832,920 PASS; Prouhet out-of-promise collisions PASS. The source/reference is trusted only for the restricted theorem, not a full all-input verifier. Prime/header authentication, parsing, all guest/child phases, and simultaneous peak space remain due. No native FLMV or mixed-calculus certificate is claimed.

**LSPV-2 and LSPV-4, Route A:** Avoid expecting sub-`k log m` one-pass exact promised clause authentication; pursue genuine small SAT guest inputs and fully charged multi-pass/random-access alternatives. **LSPV-1/LSPV-3/LSPV-5, Route B:** No changes to fixed historical `R_mix341` rules/weights or B3 status. All five allocations and schedules preserved. Root `main.tex` was not edited because its authenticated fetch returned zero text. P versus NP OPEN.

Report: `research/agents/lspv-4/2026-11-06_1545_LSPV4_BOUNDED_EDIT_FOOLING_SET452.md`.
