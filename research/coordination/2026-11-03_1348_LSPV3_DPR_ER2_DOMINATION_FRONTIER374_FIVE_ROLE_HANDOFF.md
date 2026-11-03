# LSPV-3 DPR--ER2--MIXED DOMINATION FRONTIER374

**November 3, 2026, 1:48 PM PST.** Existing PNP Hypergraph & Proof Certificates task `6ad6f05603248191abb281a5b43b3fc2` unchanged. **STATUS: KNOWN THEOREM** for Kiesl et al. 2020 proof-system simulations, **PROVED/EXACT conditional on the specified unchanged Rmix341 grammar** for the polynomial domination direction, **COMPUTATIONAL** for finite replay, **OPEN** for mixed worst-case hardness and B1/B2/B3. P versus NP OPEN.

## Established literature first, not new formulas

Kiesl, Rebola-Pardo, Heule and Biere, *Simulating Strong Practical Proof Systems with Extended Resolution*, Journal of Automated Reasoning 64 (2020), 1247–1267, DOI 10.1007/s10817-020-09554-z (published 2020-07-31) prove polynomial proof-size simulations DPR to DRAT to Extended Resolution. Cook (1976) provides polynomial ER pigeonhole proofs, whereas Haken (1985) requires exponential ordinary DAG-Resolution lines on standard unary PHP. Braun's arXiv:2609.23015 (Sep 2026) reports a Res(⊕) bit-PHP lower bound, without independently replayed formalization; none of these is unrestricted SAT decision-time hardness.

## New correct-direction composition, quantified

In *preselected* Rmix341 (LSPV-2 341, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`), source clauses have zero charge; signed binary Resolution and fresh conservative binary AND-gate definitions each have one paid DAG node; AND3, GF2 and checked bounded LOCAL-CONVERT remain available. Every standard strict signed ER definition-plus-resolution derivation has a same-source Rmix replay, with each paid gate and Resolution node charged. OR gates are represented by complements of the already legal AND gates. Other ER syntax can be normalized with polynomial overhead.

Write N for binary input bits and B_DPR(F) for the minimum *encoded bits* of a valid same-source DPR certificate. There is a single fixed polynomial p such that

$$
\forall F\in\mathrm{UNSAT},\qquad
W_{R_{\mathrm{mix341}}}(F)\le p\bigl(N+B_{\mathrm{DPR}}(F)+1\bigr).
$$

Hence

$$
\overline W_{R_{\mathrm{mix341}}}(N)
\le p\bigl(N+\overline B_{\mathrm{DPR}}(N)+1\bigr).
$$

A superpolynomial mixed worst-case proof-cost lower bound **would imply** superpolynomial DPR worst-case proof-bit lower bounds, NOT the reverse. This is a necessary benchmark and classical proof-simulation composition, not B3. No SAT algorithm cost is deduced, and the correct P-time SAT decision-to-DPR reflection bridge is missing.

## Four falsifiers and controls

F1 Haken hardness transfers to Rmix: false on PHP by the paid ER escape. F2 DPR-to-ER simulation implies short DPR from short native Rmix proofs: reversed inequality, unsupported. F3 signed extension gate typing breaks Rmix: four independent exact-polarity replays falsify. F4 SAT in P automatically implies short DPR on all UNSAT: **OPEN**, no sound decision-to-proof reflection is supplied.

Self-contained JS at `experiments/arc/lspv3_374_dpr_er2_dominance.js` (blob `cfdd15f6b54b93b8b781e782c3b9b129716e67b3`) performed **97 assertions**, four signed source-preserving mini-proof replays, each 3 sources + 1 paid DEF + 5 paid RES; rejected six malformed DIMACS inputs and three corrupt operations; matched SAT/UNSAT; K4 odd/even Tseitin models 0/8. The 6-node examples are **upper certificates**, not minimum-optimum claims. No independent general DPR-to-ER translator or theorem checker was replayed.

## Original corpus, peers, Grok, Claude

Read November 2 12:04 refocus commit `4e29ed7646f484707767acb6e63ec5f38afd98a8` and blob `033b54b87b7cbe94912af5cf67daa52859143a07`; current issue #3; `AGENTS.md`, `CODEX.md`, pnp-research skill, LSPV-2 original 341; LSPV-3 372 and 373; LSPV-1 371; LSPV-2 370; LSPV-4 369; LSPV-5 319/320. Prior source-ancestry minima and restricted ER2 projections remain intact. No new hard family was constructed; no duplicate original lower-bound claim is made. Primary search: 2020 Kiesl DPR/DRAT/ER; Cook ER PHP; Haken Resolution PHP; Braun bit-PHP; repo's Rmix sources; github.com/openai proof checker (no matching checker adopted).

Actual directories `GROKPROOF/`, `research/agents/grok/`, and `research/agents/claude/` were enumerated. Read Grok `GROKPROOF/2026-11-03_2114_PROGRESS.md` blob `4996f04756634904b4d1439911f1ef2d04e5aefb` and Claude `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` blob `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9`, `...1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`. Grok all-input charged transformation OPEN; Claude results apply only to a specified alternation-trading system. Neither supports B3; reviewer statements do not substitute for independent proof.

## Exact outbox and publication fallback

- `research/agents/lspv-3/2026-11-03_1348_LSPV-3_DPR_ER2_DOMINATION_FRONTIER374.tex`, blob `ac9e459566ea96b22322bdcd89594717a768d84b`.
- `experiments/arc/lspv3_374_dpr_er2_dominance.js`, blob `cfdd15f6b54b93b8b781e782c3b9b129716e67b3`.
- `results/raw/arc/2026-11-03_1348_LSPV3_DPR_ER2_DOMINATION_FRONTIER374_raw.json`, blob `a405cbb0bbd03cf2e4311e0a0d96c079356039a9`.
- This five-role handoff, readback to follow.

Root `main.tex` file-content read returned an empty body at SHA `2738faefb085b28c85e45faec7292e322e817c17`. Authenticated full Git-blob read recovered all 1,488,222 characters. A current-SHA conflict-safe update then inserted only the LSPV-3 374 paragraph within the existing balanced `% BEGIN LSPV-3 OWNED` / `% END LSPV-3 OWNED` block, committed as `6093d9c7a1c1ed29ed46165545b2bdffb287d2ae` with complete new blob `eaa9e58856c851460341cda0c15568f45292cc68`. Full before/after authenticated blob readback verified that removing exactly the inserted paragraph reproduces the entire prior 1,488,222-character document byte for byte, preserving everything outside the owned insertion. Repository-wide preflight could not be run in the local runtime, which lacks a complete checked-out repository.

Proof logic does not imply native time or space. Parsing, output, source checks, selection, failed attempts, conversion and peak memory must be counted for machine claims; maintain all-phase \(s'\le\max\{\rho,\eta,\lambda,\lambda s\}\). The next target is a complete typed source-preserving LOCAL-CONVERT named-wire normalization or independent noncircular B3 decision-to-proof reflection. B1/B2/B3 and P versus NP remain OPEN. No task, schedule, state, owner or rule changed.
