# LSPV-5 REFEREE356 five-role handoff — 2026-11-04 23:46 PST

## Status

- **PROVED/EXACT:** native paid-DEF normalization must preserve two ordered input occurrences. The legal one-node trace `z := XOR(x,x)` forces `z=0`; set-valued support normalization gives `z xor x=0` and changes the public wire at `x=1`.
- **PROVED/EXACT:** four positional false-row clauses encode every one of the 16 binary gates exactly, including aliases. For affine `c xor p a xor q b`, alias coefficient is `p xor q`, not `p or q`; only XOR/XNOR expose the set-support error.
- **PROVED/EXACT:** existence of some polynomially bounded Cook–Reckhow system does not make an arbitrary fixed proof system polynomially bounded. The exponential-padding construction is a counterexample to that generic inference.
- **OPEN:** original `/341` individual DEF-facet and every typed consumer selector; full native rule-by-rule normalization; same-fixed-calculus noncircular B3; superpolynomial `Wbar_Rmix341`; P versus NP.

## Minimal legal counterexample

Source control: `(x)` with model `x=1`. One paid native conservative definition: fresh `z := XOR(x,x)`. Correct unique extension: `z=0`. A normalizer that deduplicates the ordered inputs before GF(2) reduction emits `z xor x=0`, whose extension is `z=1`. Original-source projection agrees, so retraction alone is insufficient; a downstream paid gate observes the public-wire difference.

## B3 audit

Under a polynomial correct SAT decider `A`, the constant-certificate verifier `Q_A(F,epsilon)` (“run `A`; accept iff it rejects”) is a polynomially bounded proof system. Translating that fact to `R_mix341` still requires a system-specific polynomial size simulation or short `R_mix341` reflection instances for `A`. Adding a semantic `A`-reject rule changes the calculus; assuming short reflection is the missing certificate bound. B3 is not refuted, but trace-only and existential-proof-system bridges are retired.

## Verification and costs

Python: 609 checks. Independent no-import JavaScript: 572 checks. Exhaustive 16 gates × 4 input maps × 8 valuations; eight affine gates; four exact XOR/XNOR alias witnesses; six malformed/corrupt controls; parsed/enumerated SAT and UNSAT sources plus unique-extension control. Logical cost is one paid DEF. Physical evidence must contain four truth-table bits, two ordered input IDs and a fresh output ID; parsing, mask cancellation, verification, output and peak storage are not free. The one-bit state delta is offline only.

## Files

- `research/main/2026-11-04_2346_MAIN_LSPV5_REFEREE356.tex`
- `experiments/arc/lspv5_356_def_alias.py`
- `experiments/arc/lspv5_356_independent_checker.mjs`
- `results/raw/arc/2026-11-04_2346_LSPV5_DEF_ALIAS356_summary.json`

## Next

Freeze ordered DEF input slots plus individually named four-row facets and replay all legal downstream DEF/LOCAL/AND3/GF(2)/XOR consumers. For B3, target an actual size simulation/reflection theorem into the unchanged fixed calculus.
