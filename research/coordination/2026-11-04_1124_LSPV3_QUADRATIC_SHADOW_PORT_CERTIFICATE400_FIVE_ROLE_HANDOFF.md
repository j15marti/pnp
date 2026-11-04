# LSPV-3/400 | Quadratic-shadow port certificate

November 4, 2026, 11:24 PST. **PROVED/EXACT in a restricted XOR/AND/NOT shared-DAG circuit model** with independent specialist review pending; **COMPUTATIONAL** controls independently passed. The unchanged full `R_mix341`, B1, B2, B3 and P versus NP remain **OPEN**. No modifications to any task, schedule, enabled state, role or proof rule.

## IDEA -> SEARCH -> ITERATE

Initial falsifiable conjecture: the nonaffine inner-product port `I_m = XOR_i(u_i AND v_i)` from LSPV-3/398-399 requires at least m binary nonlinear gates under every shared XAG representation, even with nonlinear intermediates and conservative auxiliary wires. Four falsifiers: (F1) fewer than m ANDs, (F2) affine recoding makes the bound disappear, (F3) original AND3/LOCAL-CONVERT automatically counts as an XAG gate, (F4) gate cost implies SAT-time hardness. F1 and F2 fail in the declared circuit model; F3 and F4 are invalid transfer steps.

Search covered exact original Rmix341 [`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob c87acd11], LSPV-3/399 blob f8a54ca5, LSPV-4/391 blob a4b146f5, LSPV-5/315 blob 66a18447, the November 2 refocus blob 033b54b8, active issue #3, AGENTS.md, CODEX.md and the pnp skill. Literature queries: multiplicative complexity inner product Boolean rank; Mirwald Schnorr quadratic forms; unrestricted nonlinear XOR AND circuits; Cook/Haken proof systems. Primary Mirwald--Schnorr (TCS 102:307-328, 1992) already proves quadratic-form multiplicative complexity, so academic novelty is **not asserted**. NIST Calik/Turan/Peralta (2020) and Boyar/Peralta/Pochuev (2000) provide related MC bounds. Direct Google-branded search unavailable; general web and authenticated GitHub connector search used. In `github.com/openai`, `openai/math/lean/ComparatorChallenges/SATVariance.lean` blob 5ecf51d9 is an unrelated variance problem with an admitted proof gap, not a SAT proof translator.

Actual independent assessments: `GROKPROOF/2026-11-04_1518_PROGRESS.md` blob 4e2bb9d9 maintains its universal charged ARC transfer as OPEN; `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob 1f9fc727 treats a restricted alternation-trading proof framework, not B3. Neither validates a general computational-to-proof bridge.

An attempted gate-by-gate quadratic-rank proof was revised because Boolean idempotence `x^2=x` allows high-degree nonlinear intermediate products to collapse degree. The successful repair is a **topological affine-freezing lemma**: a circuit with k AND gates has an affine flat of codimension at most k where every AND output is constant, hence the output affine. Any affine restriction of the output function that is quadratic with polarization rank 2r therefore requires at least r AND gates, even when the original circuit uses nonlinear intermediates and shared wires.

## Result and exact scope

For every m>=1, the nondegenerate polarization of `I_m` has rank 2m. Hence its exact unrestricted *XAG multiplicative complexity* is **m**; the m product gates attain it. For the earlier port `T_m=(a OR I_m) AND (b OR NOT I_m)`, restriction to a=0,b=1 recovers `I_m`; so every XAG for `T_m` requires >=m AND gates. Its mux identity `T_m=a XOR ((a XOR b) AND I_m)` gives m+1 AND and m+1 XOR gates, 2m+2 total. Exact MC of T_m is not claimed. Forced auxiliary-free CNF erasure remains exponential by LSPV-3/399, but the compact circuit avoids that overhead.

The theorem is **representation invariant only inside the declared XOR/AND/NOT circuit grammar**, including arbitrary affine recodings, conservative named wires and nonlinear shared intermediates. It does not assert that every legal RES, AND3, XOR-equation or LOCAL-CONVERT proof node corresponds to an XAG gate, nor that the semantic port must be computed by every refutation. It is a linear gate-budget lower bound, not superpolynomial mixed proof cost, uniform SAT time or peak space.

## Tests and explicit artifacts

Deterministic Python producer seed 4001124: **23,263 assertions**, including 30 invertible-affine recodings at each m=1..6, canonical truth tables, mux truth tables m=1..5, 360 arbitrary shared-XAG DAGs and three malformed-reference rejects. Separately authored Node verifier: **1,343 assertions**; full enumeration of affine (m+1)-flats for m=1,2,3 with 1/15/651 linear subspaces and 1/30/2604 affine cosets, all hostile checks passed. Results do not substitute for all-size proof.

Committed, conflict-safe and verified by complete readback:

- Formal report `research/agents/lspv-3/2026-11-04_1124_LSPV-3_QUADRATIC_SHADOW_PORT_CERTIFICATE400.tex` (blob 078ce6de1b356481bfe7c943d5dfb481a6c3a1a6).
- Independent checker `experiments/arc/lspv3_400_affine_flat_checker.js` (blob e58136fc0d27d353ba4b8c7550e4e3196b6fc946).
- Raw ledger `results/raw/arc/2026-11-04_1124_LSPV3_QUADRATIC_SHADOW400_summary.json` (blob 333a275d58fd4b6145b27a3923aa9097084cb9d3).
- This five-role handoff.

The full Python producer, independent Node implementation and complete raw outputs are in the conversation reproducibility archive, with source/output SHA-256 recorded in the raw ledger. Root `main.tex` at blob 2189f027324f72dec260fddd8999aa8cffbdd047 returned **zero bytes** through ranged fetch, so ownership-safe reconciliation is blocked; no unsafe overwrite was attempted. Local full repository preflight and LaTeX compilation unavailable because no checkout was accessible.

## Role-specific implications and next test

**LSPV-1:** This does not establish B1/B2/B3. Retain universal uniform total-decider quantifiers. **LSPV-2:** Test whether any legal mixed conversion can force, rather than merely optionally compute, the quadratic-shadow port, with explicit syntactic provenance. **LSPV-3:** Next, freeze exact LOCAL-CONVERT payload/exported-wire grammar and test the contradiction-producing port obligation against RES, AND3, XOR and paid DEF alternatives. **LSPV-4:** Charge all actual construction, bit access, code length, validation, failed attempts, output and peak live space, keeping the full `s'<=max{rho,eta,lambda,lambda*s}` envelope. **LSPV-5:** Audit the difference between a semantic circuit output lower bound and a refutation DAG lower bound; seek a legal shortcut in Rmix341.

The known Haken and Urquhart lower bounds concern ordinary shared-DAG Resolution, not the complete mixed calculus or arbitrary uniform SAT machines. Odd Tseitin has a polynomial XOR shortcut. No superpolynomial `Wbar_Rmix341(N)` bound has been proved; P versus NP is OPEN.
