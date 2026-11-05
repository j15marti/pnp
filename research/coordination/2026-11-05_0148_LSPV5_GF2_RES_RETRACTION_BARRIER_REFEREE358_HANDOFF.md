# LSPV-5 REFEREE358 handoff: no polynomial GF(2)-erasing source-only Resolution retraction

**Time:** 2026-11-05 01:48 PST. **Fixed calculus/weights/tasks/schedules:** unchanged. **P versus NP:** OPEN.

## New exact result

There is no polynomial-overhead translator taking every valid `R_mix341` refutation to an ordinary Resolution refutation of the same original clauses. Choose cubic expander odd-Tseitin sources. Authoritative `/341` gives valid mixed proofs of cost `4h-1`; source bits are `Theta(h log h)`. Urquhart requires `2^{Omega(h)}` lines for every ordinary Resolution refutation. Any bound `poly(source_bits + mixed_nodes)` contradicts that theorem.

This falsifies only a normalization that erases GF(2)/strong rules and leaves source clauses plus RES. It does not falsify a strong-rule-preserving same-mixed-system compiler; native DEF-facet, LOCAL exported-wire and GF(2) selectors remain unsettled.

## B3 consequence

Combined with LSPV-1/413:

1. answer bits/raw traces are not sound native certificates;
2. polynomial all-input RUP/DRUP/Resolution logging is impossible on PHP;
3. strong mixed certificates escape those lower bounds, but require the still-open same-system p-simulation/reflection theorem.

Thus B3 for fixed `R_mix341` remains OPEN. Exponential backtranslation is not SAT-machine hardness.

## IDEA → SEARCH → ITERATE

The initial bounded-port byte lemma was found substantially duplicated by LSPV-1/386 and LSPV-3/416. LSPV-2/412 supplied the shared-correlation falsifier. The revised established-family attack produced the theorem above. Read latest issue peers, original `/341`, Grok `GROKPROOF/2026-11-05_1218_PROGRESS.md`, Claude TPORT/ONETAPE, primary Urquhart/Ben-Sasson–Wigderson/Haken/Cook ER/Res(XOR) sources, and full relevant OpenAI GitHub Lean cost/verifier files. Direct Google UI was unavailable; general web search was used.

## Verification

- Python: K4, K3,3, cube, Petersen; 448 local parity-table checks; odd/even model counts; five malformed rejects.
- Independent Node: 533 assertions, identical labels and `4h-1` node counts.
- These are finite mixed-proof controls, not a proof of the literature lower bound.

## Artifacts

- `research/main/2026-11-05_0148_MAIN_GF2-TO-RESOLUTION-RETRACTION-BARRIER-REFEREE358.tex`
- `experiments/arc/lspv5_358/tseitin_retraction_barrier_referee358.py`
- `experiments/arc/lspv5_358/verify_tseitin_retraction_barrier_referee358.mjs`
- `results/raw/arc/2026-11-05_0148_LSPV5_REFEREE358_raw.json`

## Next exact obligation

Freeze all remaining typed selectors, then prove a sparse-ID, joint-correlation, strong-rule-preserving same-source compiler—or produce an accepted native trace whose normalized replay fails. Separately prove conditional p-optimality of that same checker without assuming short proofs or decider reflection.
