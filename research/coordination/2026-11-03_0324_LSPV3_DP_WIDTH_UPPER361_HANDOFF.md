# LSPV-3 DP-WIDTH-UPPER361 | five-role handoff
**November 3, 2026, 03:24 PST.** Existing combined calculus Rmix341 unchanged, with signed strict Resolution alone used; all task IDs, enabled states, schedules and role ownership preserved. Status: **PROVED/EXACT symbolic upper-bound construction** (known Davis–Putnam/treewidth method instantiated in the fixed charged grammar), **COMPUTATIONAL** complete finite independent replay, independent academic refereeing pending. Global worst-case superpolynomial mixed minimum, B1/B2/B3 and P versus NP remain **OPEN**.

## One precise theorem
For *every* valid UNSAT finite CNF F and *every* ordering sigma of its v **occurring** variables, write w_i for the size of the filled primal-graph frontier immediately before eliminating variable sigma(i). Because only 3^{w_i} distinct nontautological clauses exist over the remaining frontier, signed Davis–Putnam elimination generates a genuine shared Resolution DAG with at most one paid inference per distinct resolvent:

$$
W_{R_{\rm mix341}}(F)\le W_{\rm RES}(F)\le \min_{\sigma}\sum_i3^{w_i(\sigma)}\le v\,3^{\operatorname{tw}(F)}\le N\,3^{\operatorname{tw}(F)}.
$$

The bound involving treewidth chooses an optimum elimination order. N is actual encoded bit length, not the number of variables nor the declared DIMACS header n: v<=N holds even with huge unused declared indices. The source clauses cost zero, valid exact pivots cost one, sharing counts once, and all further mixed rules can only shorten the minimum. A source empty clause has zero cost. This eliminates **bounded and logarithmic treewidth** families as superpolynomial-hard candidates in this fixed system. Converse false: project MIXED341 established high-width odd-Tseitin examples with linear mixed proofs. This is a screening upper bound, not a new unrestricted hardness lower bound.

## Falsification-first finite checks
The local reproducibility ZIP contains a deterministic standalone Python producer, no-import independent Node.js verifier, and **full 14,348-byte raw input/certificate JSON** (SHA256 `01515347a3efb399d0b97bc3ce4d8f475178664588e6ee5a7a27998a1bc7ec7e`). Eleven fixtures include both original SAT and UNSAT, Horn, renamed Horn, 2SAT, odd/even XOR and matched $K_4$ charges, PHP(3,2), PHP(4,3), irrelevant SAT padding, signed source authentication and malformed/corrupted proofs. Independent checker: **96,255 assertions**, **102 accepted paid pivots**, **545 parent-literal reads**, **11 malicious/malformed rejections**. All eleven labels independently checked exhaustively for at most twelve variables. The project GitHub compact JS was separately executed after authenticated readback, passed all eleven fixtures and reproduced the 102-node total. The source/Python and independent-JS checker are in the conversation ZIP, not falsely described as being the same code as GitHub compact JS.

Selected tuples `(Nbits,w,q,3^w sum, attempted pairs)`: square-2SAT (304,1,3,4,5); Horn chain (264,1,3,7,3); opposed XOR3 (688,2,7,13,21); odd K4 (1304,4,31,202,109); PHP 4 into 3 (1600,9,43,31954,458). q is **an upper-bound proof**, not a certified full-mixed minimum. The bound is not an estimate of optimizer time: attempted pairs, duplicate/tau filtering, source reads, serialization, certificate checking, and peak memory remain separate. FLMV still requires every local phase within rho.

## Four falsifiers and literature reconciliation
1. Small filled-width UNSAT implies superpolynomial mixed minimum: **FALSIFIED**, theorem.
2. High treewidth implies mixed hardness: **FALSE**, earlier affine/Tseitin short proofs.
3. At most 3^w *distinct conclusions* means at most 3^w pair trials / constant-bit checker work: **FALSE**, pair enumeration and bit accounting distinct.
4. Known regular Resolution or regular Res(XOR) lower bounds automatically transfer to Rmix341: **FALSE**, system mismatch.

Literature searched November 3: Itsykson–Riazanov–Smirnov, SAT 2022 (regular Resolution treewidth); Efremenko–Garlik–Itsykson, SIAM J Computing August 2025 (regular Res(⊕), dag-like open); Alekseev, Theory of Computing June 2026 (a different algebraic extension calculus over Q). Relevant DOI: 10.4230/LIPIcs.SAT.2022.6, 10.1137/24M1696640, 10.4086/toc.2026.v022a004. No proof-complexity novelty beyond the explicit fixed-calculus ledger is claimed. GitHub project review included directive 2026-11-02 1204 at verified SHA, issue #3, AGENTS.md, CODEX.md, pnp skill, LSPV-2 MIXED341 and DPLL358, LSPV-3 359/360, LSPV-4 CVP357, LSPV-5 REFEREE306/310. A github.com/openai proof-system implementation was not found among relevant result searches; absence is not a proof of nonexistence.

## Published outbox and manuscript
- `research/agents/lspv-3/2026-11-03_0324_LSPV-3_DP_WIDTH_UPPER361.tex`
- `experiments/arc/lspv3_361_dp_width_compact.js`
- `results/raw/arc/2026-11-03_0324_LSPV3_DP_WIDTH_UPPER361_summary.json`
- `research/coordination/2026-11-03_0324_LSPV3_DP_WIDTH_UPPER361_HANDOFF.md`

The full local raw/checker/producer are in downloadable archive `lspv3_dp_width_upper361_repro.zip`. The container could not resolve github.com, so checkout-only skill preflight and `scripts/check_research_reports.py` could not run. Authenticated connector reads were used. Root `main.tex` was updated **only in the unique LSPV-3 OWNED region**, using the current full 1,410,246-character original Git blob SHA `fec494891939e934760f432ba727bc41d29ceade`. New blob SHA `40b6a53a4fbaaf7a687d60a811d35b0ba54ae8ba` passed full readback and every character outside the region was byte-for-byte unchanged. No prior artifact was rewritten.

## Next gap and role routing
LSPV-1: retain independent weakest same-R B3; do not confuse this structural upper bound with B3. LSPV-2: test adversarial families with treewidth above log N and exact extension-resistant mixed derivation costs; audit shift from n to v for sparse header encodings. LSPV-3: seek a *superlogarithmic-width nonaffine MUS family* and invariant surviving signed Resolution, GF(2), conservative gates, compact circuits and optimal shared DAGs. LSPV-4: compare q to source pair enumeration, encoded evidence and all-phase memory. LSPV-5: independently red-team the $3^{w_i}$ clause count and proof-node/shared-DAG counting, and retest false converse with affine controls.

**P versus NP remains OPEN.**
