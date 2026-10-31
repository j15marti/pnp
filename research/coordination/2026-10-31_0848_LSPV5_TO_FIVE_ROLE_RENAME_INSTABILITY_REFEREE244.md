# Five-role handoff: RENAME-INSTABILITY-REFEREE244

Timestamp: 2026-10-31 08:48 America/Los_Angeles  
Status: PROVED/EXACT restricted theorem; COMPUTATIONAL finite controls; ARC/FLMV and P versus NP OPEN.

## Exact red-team result

GATE277's ordered-promise projection theorem is correct, but its contiguous variable-bin recognizer is not invariant under a pure variable permutation. For infinitely many `n=s^2-1`, both the SAT family

`(x1 or x2) and units x3,...,xn`

and the UNSAT mate obtained by adding `(x1)`, `(not x1)`, and two balancing `(xn)` copies are recognized in canonical order. Swapping `1<->n` and `2<->floor(n/2)` produces a semantically identical, exactly same-length DIMACS mate whose coupling clause crosses private bins for every tested logarithmic boundary. Recognition success is therefore a representation property, not yet a semantic all-input residual parameter.

This is not a lower bound on every permutation-invariant finder. Luks's bounded-valence result is a hostile control showing that restricted orbit problems can be polynomial. The required next arrow is a fully charged, permutation-invariant interface finder or an exact fallback.

## Reproducibility

- Producer: `experiments/arc/lspv5_244/rename_instability_referee244.py`
- Independent checker: `experiments/arc/lspv5_244/verify_rename_instability_referee244.py`
- Raw: `results/raw/arc/2026-10-31_0848_LSPV5_RENAME_INSTABILITY_REFEREE244_raw.json`
- Summary and verification: matching files under `results/summaries/arc/`
- 16 principal rows: 8 canonical recognized, 8 renamed rejected.
- 512 fixed-seed random renamings: 0 recognized (COMPUTATIONAL only).
- Independent checker: PASS, 134,588 units, 4 injected corruptions rejected.
- Raw SHA-256: `3983ccc26828038fabb2f38cdad68baba36c6147d6a87128ed849e1bbcb98bbb`.

## Integration rule

Preserve GATE277 as a promise-class theorem. Do not count favorable source order, best-policy advice, normalization, switching, failed trials, source access, retained candidates, or output as free. Preserve AFFINE-SMALLBIAS-DESCENT-GATE2 only as a restricted affine MCSP semantic no-go; it does not yield universal SAT runtime. All five roles should test candidate residual parameters under adversarial variable renaming before crediting all-input ARC coverage.
