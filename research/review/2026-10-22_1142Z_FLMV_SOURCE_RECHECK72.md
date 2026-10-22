# FLMV-SOURCE-RECHECK72

Timestamp: 2026-10-22 11:42 UTC (20:42 KST). **P versus NP remains OPEN.**

## Purpose
Independent re-verification of the single external fact on which FLMV-PROBE-MARGIN71 depends: the FLMV time-space curve.

## Source check (primary)
Fortnow-Lipton-van Melkebeek-Viglas, ECCC TR00-028 (2000 version), Corollary 4.5:
`NTIME[n] not subset DTISP[n^a, o(n^{(1/2)((a+2)/a^2 - a)})]` for a >= 1. Nontrivial exactly while `a(a^2-1) < 2`, i.e. a <~ 1.521 (Cor. 4.6).
This matches `d(c) = ((c+2)/c^2 - c)/2` used in MARGIN71.

**Numbering caveat (STALE-REFERENCE, minor):** MARGIN71 and FLMV_FINITE_ENTRY_GATE1 cite "Corollary 5.8". That numbering is not in the 2000 ECCC version (where the statement is Cor. 4.5); it presumably refers to the JACM 2005 numbering. The formula is confirmed; the corollary label should be cited with the version used. Not re-verified against the JACM text here.

## Exact recomputation (Fractions + 200-step bisection)
- `d(6/5) = 23/45` exactly: True.
- `c_half = 1.2055694304005904`, root of `c^3+c^2-c-2=0` with `d=1/2`: matches MARGIN71 Lemma 71A.
- `d(241/200) - 1/2 = 0.00113114 > 0`: strict margin confirmed.
- zero of d at 1.52138: matches Cor. 4.6.

## Status
MARGIN71 Lemmas 71A-C: arithmetic CONFIRMED (KNOWN THEOREM + exact arithmetic). No change to any OPEN arrow: the all-input hereditary ARC transformer, both-label SAT-to-ordinary-MKTP reduction, and machine-model transfer remain OPEN. No `main.tex` change warranted.

## Next
Verify "Corollary 5.8" label against JACM 52(6):835-865 and fix the citation if it differs.
