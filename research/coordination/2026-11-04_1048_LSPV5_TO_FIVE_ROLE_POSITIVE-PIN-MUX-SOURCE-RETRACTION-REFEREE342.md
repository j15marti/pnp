# REFEREE342 FIVE-ROLE HANDOFF

The complete report is `research/main/2026-11-04_1048_MAIN_POSITIVE-PIN-MUX-SOURCE-RETRACTION-REFEREE342.md`.

## New restricted results

1. **Positive pin bank:** for `B_0` zero and `B_1` one source bits, a paid DEF/RES construction materializes distinct positive variables with exact cost `20+2B_0+3B_1`. This avoids signed substitution through downstream mixed nodes.
2. **Mux alias:** one fixed 2:1 mux exposes its selected input in exactly three DEF plus five RES nodes beyond the shared false unit.
3. **Declared transparent evaluator:** retain its full gate topology, derive its root from authentic source clauses, and copy any downstream `R_mix341` proof unchanged. This gives polynomial source retraction for explicit masks, acyclic muxes and private OR/AND aggregation.
4. **Universal reflection D4:** for the declared `H_(A,N)=Valid AND Reject_A AND Eval`, every supplied mixed refutation compiles to an authentic source refutation with polynomial overhead while all downstream nodes remain unchanged. This is not short reflection.
5. **Failures:** raw specialization is not literally REF341's `T(F)`; explicit full mux reconstruction need not be `O(N)`; full materialized evaluator length is not intrinsic because root-reachable `p AND not p` padding can be exponential yet uniformly bypassed.

## Status

These are architecture-specific source-compilation results and a representation-independence counterexample. They do not prove short reflection, B1, B2, B3, a superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, or P versus NP.

## Next split

- LSPV-1: combine the positive-variable alpha-renaming with the exact reflection quantifiers; determine the weakest remaining reflection theorem.
- LSPV-2: minimize the transparent evaluator size without semantic merging and audit binary-index versus one-hot encodings.
- LSPV-3: formalize the source-leaf map and certificate semantics for masks, mux paths and padding.
- LSPV-4: schedule the emitted proof with explicit construction/access/checking/output and peak-space bounds.
- LSPV-5: attack short reflection and any claim that minimum-over-representations is automatically machine work.

Artifacts are in `experiments/arc/lspv5_342/` and `results/raw/arc/lspv5_342/`; raw SHA-256 is `e4d0fd190ccb480af48f2fe71822ca25f7cbb9edaffd35f636ff3b3c1da1a717`.
