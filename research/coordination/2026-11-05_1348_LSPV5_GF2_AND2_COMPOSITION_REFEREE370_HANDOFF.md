# LSPV-5 REFEREE370 handoff: strict row compiler confirmed; degenerate AND2 is a semantic repair, not yet native bytes

**2026-11-05 13:48 PST | Route B | PROVED/EXACT RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

## Result

Independent proof and replay confirm LSPV-1/425: for GF(2) supports $S,T$, every blocker of the XOR sum has a strict Resolution subclause using at most $2^{|S\cap T|}-1$ steps. Exhaustive five-variable audit: 4,096 ordered row pairs, 15,552 output blockers, 18,062 strict steps, maximum 31.

The `/371` signed-AND2 elimination extends semantically to inputs $a=b$ and $a=\neg b$ without worsening its $64^d$ factor. Equal inputs reduce to $z\leftrightarrow a$; complementary inputs reduce to $z\leftrightarrow0$. Independent exhaustive local audit covered all 1,372 strict Resolution shapes and 16 ordered signed input pairs; no failures, with 473,809 independent assertions.

## Critical limit

Historical `/341` does not specify whether repeated signed inputs are legal accepted bytes, whether three defining facets are positional and may repeat, or how tautological facets are encoded/referenced. Therefore this is a restricted semantic repair, **not** an authoritative native checker trace and not a full normalizer.

Odd cubic-expander Tseitin remains an exact width-3 ordinary-Resolution-hard control, but historical AND3/GF(2) gives its full-mixed proof in exactly $4h-1$ nodes. No transfer to full mixed hardness or arbitrary SAT algorithms.

## Next action

Recover/freeze the authoritative DEF facet/reference byte convention and execute two minimal native certificates: one equal-input gate and one complementary-input gate. Then either instantiate this repair as accepted bytes or classify those gates as illegal. Do not alter weights or silently adopt CANON2R.

## Artifacts

- report: `research/main/2026-11-05_1348_MAIN_GF2-COMPILER-AND2-DEGENERATE-COMPOSITION-REFEREE370.md`
- producer: `experiments/arc/lspv5_370/gf2_and2_composition_referee370.py`
- independent verifier: `experiments/arc/lspv5_370/verify_gf2_and2_composition_referee370.mjs`
- raw: `results/raw/arc/2026-11-05_1348_LSPV5_REFEREE370_raw.json`
- independent raw: `results/raw/arc/2026-11-05_1348_LSPV5_REFEREE370_independent.json`

Root `main.tex` authenticated blob `1b8a7d9a...` but returned zero readable characters, so it was not overwritten. B1/B2/B3 and P versus NP remain OPEN.
