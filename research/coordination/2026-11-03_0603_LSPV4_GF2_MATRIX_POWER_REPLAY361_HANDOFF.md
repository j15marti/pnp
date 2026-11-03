# PNP Time-Space Resource Auditor, GF(2) path-power replay 361

**Date:** November 3, 2026, 06:03 PST (America/Los_Angeles). **Status:** PROVED/EXACT in an authenticated ROW/XOR fragment of the existing fixed `Rmix341`; COMPUTATIONAL independently checked finite controls. B1, B2, B3, superpolynomial worst-case minimum and P versus NP remain OPEN. Additive to the original November 2, 12:04 five-role scientific handoff. No task identity, title, enabled state or schedule changes.

## Exact theorem

A ROW record naming four source clauses on three variables must be justified by all eight truth assignments and expands into **three charged binary AND3 inference nodes**. A later XOR record costs one node and names two previous rows. With `r` ROW records, `t` XORs, `K=r+t` macro records, the logical cost is **q=3r+t**, not `K`. Let `M=N+P` be the complete binary source plus supplied proof evidence.

Let the strictly upper-triangular GF(2) adjacency matrix `A` count parent-slot occurrences **modulo two**, including duplicate parent cancellation. For final record `f`, the contribution from ROW `i` is the parity of all directed paths to `f`, `c_i=(sum_(j=0)^(K-1) A^j)[i,f]`. Set `B=[[A,I],[0,I]]`; then **`c_i=(B^K)[i,K+f]`**. Recursively compute matrix-power coordinates by midpoint summation, querying individual bits of the proof/source from read-only input rather than materializing `B`. Recursion depth `O(log M)`, each frame `O(log M)` scratch: **all-phase peak writable O(log²(M+2)) bits and total native time M^O(log(M+2))**. Check each actual source-variable coordinate of the final equation as zero and constant coordinate as one. This verifies exactly authenticated `0=1` in the **ROW/XOR fragment**, not the full mixed calculus. It requires the certificate as an input. Free optimizer selection in `W_R` remains separate from machine construction of that certificate.

## Falsifiers

1. **Restricted FALSIFIED:** every supplied parity proof intrinsically requires `K` writable coefficient bits. The new slower checker needs only logarithmic-squared scratch, without free source/random-access operations.
2. **FALSIFIED:** treating duplicate XOR parents as a single ordinary graph edge is sound. In GF(2), the two edges cancel; tested coefficients `[0,1]`.
3. **FALSIFIED:** even-charge SAT sources or signed clause-flip SAT neighbors can yield authenticated contradictory ROW/XOR proofs. The local truth-table authentication and final coordinate tests reject them.
4. **OPEN:** this verifier gives a polynomial-time universal SAT solver, strict FLMV resource contraction, or B3. It is quasipolynomial time in supplied certificate size and does not handle RES/DEF/LOCAL-CONVERT.

## Independently reproduced controls and resources

Independent Python recursive-power producer and JavaScript no-import referee verified odd/even cubic `K4` and `Prism3` sources. The labels/model counts are K4 even 8, odd 0; prism3 even 16, odd 0. Exact charged node counts: K4 q=15, K=7; prism3 q=23, K=11. Source+JSON certificate lengths: 468 and 691 bytes; recursive call counts 5,811 and 120,626; actual maximum recursion depths 4 and 5. Python counted 37 controls with 16 odd-source sign-flip SAT neighbors, 11 malformed encodings and forged-reference tests; independently written JavaScript checked 276 assertions including 40 additional DAGs with repeated parent operands, 80 source sign-flip SAT checks and malformed controls. Python host peak RSS 96,396 KiB, Node host RSS 31,728 KiB, **not native writable-space bounds**. The host Python materializes the input and does not itself instantiate the theorem's low-space TM.

## Corpus, literature and duplication

Read original five-role handoff first, current issue #3 and materially relevant LSPV-2 calculus341, LSPV-4 affine coordinate360, LSPV-5 source alias313, AGENTS/CODEX and pnp-research skill. Queried project GitHub for `matrix powering`, `GF(2) path` and `Savitch`; queried github.com/openai. No relevant previous exact ROW/XOR source-coordinate time/space theorem surfaced, but matrix powering and Savitch recursion are established methodology and no novelty claim is made. Reference: Walter Savitch (JCSS 1970), Cook/Reckhow (JSL 1979); small-space matrix approximation in STOC 2023 is a different result and is not transferred.

## Repository artifacts and next gap

- [Role-owned formal report](../agents/lspv-4/2026-11-03_0603_LSPV-4_GF2_MATRIX_POWER_REPLAY361.tex)
- [Standalone public compact reproducer](../../experiments/arc/lspv4_361_gf2_matrix_power_compact.js)
- [Machine-readable summary](../../results/raw/arc/2026-11-03_0603_LSPV4_GF2_MATRIX_POWER_REPLAY361_summary.json)

The full two-language independent implementations, LaTeX source and raw JSON run evidence are in the conversation reproducibility archive. Root `main.tex` is very large; no unsafe contents overwrite is authorized. If full authenticated readback and ownership-only change are not possible, leave root unchanged and report fallback.

**Next:** typed polynomial-size downstream-preserving normalization of the `RES`, `LOCAL-CONVERT` and conservative `DEF` records, including source/pointer costs and full proof DAG storage/recomputation. Preserve `s'<=max(rho,eta,lambda,lambda*s)` with `rho` covering all local phases. Neither this theorem nor a small proof on a family implies B2 or B3. **P versus NP remains OPEN.**

## Verified root manuscript reconciliation (post-publication)

The root `main.tex` was recovered as the complete authenticated blob `0fe0b805dc14b3e784b2ded95bbe246ea50fc03f`, not its incomplete ordinary contents response. A new LSPV-4-only marked block `GF2-MATRIX-POWER-REPLAY361` was inserted immediately after the existing LSPV-4 result 360, using the exact current content SHA. New blob: `1ea3987bcece826cf12910bd18df8c6eee5e0b06`, commit `26d7d0baf0154c5623c7d21c057fd623ce5f44bf`. Both immutable Git blobs were read back, and removing precisely the newly marked 2,468-character block from the new blob restored the old 1,434,184-character blob **character for character**. The original root bytes outside the authorized insertion remain unchanged. This succeeds the earlier anticipated retrieval fallback.
