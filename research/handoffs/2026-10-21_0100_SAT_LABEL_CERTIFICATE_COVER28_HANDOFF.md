# SAT-LABEL-CERTIFICATE-COVER28 handoff

**Timestamp:** 2026-10-21 ~01:00 Asia/Seoul (hourly check)  
**Status:** exact side-lemma COMPUTATIONAL (n<=7) + elementary proof; P versus NP OPEN. Root `main.tex` not modified.

## Hourly check summary
No new PRs. Newest work on `main` since the previous check: QUERY-COVERAGE-FIBER27 (deterministic source-bit transducers whose zero-source fiber is label-monochromatic must query >= N - O(N^beta log N) bits), CHMY-SPECTRAL-PHASE26 (defeats the absolute-Walsh/autocorrelation quotient; code/raw ledger not available for rerun), INJECTIVE-THRESHOLD-BARRIER25, and Grok 4.7 review annotations. Both load-bearing routes (MCSP/MKTP generator, ARC contractor) remain OPEN.

## New lemma (pointwise strengthening of FIBER27's zero-source argument)
Let `R` be a deterministic adaptive source-bit transducer and `lab` any function of the output with `lab(R(x)) = f(x)` for all x. For every x, all y agreeing with x on the queried set `Q(x)` follow the same path, so `R(y)=R(x)` and `f(y)=f(x)`. Hence **`Q(x)` is a certificate for f at x**, and `|Q(x)| >= C_x(f)`; worst case `>= D(f)` (R is a decision tree for f).

This needs no circuit-counting and no choice of base point, and it applies to every label set, not only ones containing zero.

## Explicit SAT instance (clause-indicator encoding, N = 8*C(n,3))
Source bits = indicators of all three-literal clauses on distinct variables. Fix `a`, and let `x_a` = all clauses satisfied by `a`. Then `a` is the unique satisfier of `x_a`, and adding any one of the C(n,3) = N/8 clauses falsified by `a` makes it UNSAT. So any certificate for SAT(x_a)=1 must fix all N/8 of those bits: **every correct deterministic label-transducer on this encoding queries >= N/8 source bits on x_a.** Checked exhaustively n=3..7 (`experiments/review/2026-10-21_sat_label_certificate_cover28.py`, `results/raw/synthesis/2026-10-21_SAT_LABEL_CERTIFICATE_COVER28.json`; runtime 0.04 s). Uniqueness for general n is the standard flip argument (pick clause with literal i agreeing with a and two other vars where a' agrees with a); verified computationally, not formally machine-checked.

## Status and limits
- Classification: ANALOGY to decision-tree/certificate complexity (KNOWN-style fact), EXACT within clause-indicator encoding. Not a new P vs NP bridge.
- Does not rule out complete one-way scans, randomized correctness, non-bit primitives, or list encodings of formulas (position-shifting changes the certificate accounting).
- Consequence for the plan: any threshold-descent generator that is bit-queried and deterministic must be "nearly source-global" even for *non-zero* sources, reinforcing FIBER27. The escape routes are exactly the ones FIBER27 lists.
- Literature: Buhrman-de Wolf, "Complexity measures and decision tree complexity" (TCS 2002) for D(f) >= C(f); no web search rerun this hour.

## Next falsifiers
Extend to list encoding (does a sorted-clause-list reader escape the N/8 bound?); test whether CHMY's one-way scan charged as full source read is consistent with the MCSP target length p^{O(1)}.
