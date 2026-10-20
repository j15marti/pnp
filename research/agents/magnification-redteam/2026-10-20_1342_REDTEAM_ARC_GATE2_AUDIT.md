# REDTEAM-ARC-GATE2-AUDIT
Date: 2026-10-20 13:42 Asia/Seoul. Role :36 red team, target ARC_HISTORY_INPUT_GATE2. P != NP OPEN.

## Falsifiers proposed before checking
(1) the Shannon floor Omega(N/log N) was stated asymptotically; check an explicit-constant crossover vs sqrt(N); (2) the ARC recurrence t'<=max(1.1,e,0.6+g+t/2) may hide fragility to per-level leakage g; (3) depth to constant size is log log N, so per-level overhead could compound; (4) FLMV compatibility of (1.2,0.5) was asserted, not checked.

## Results (code: experiments/review/2026-10-20_1336_redteam_gate2_audit.py; raw: results/summaries/2026-10-20_1336_redteam_gate2_audit.json; runtime <1s)
- COMPUTATIONAL: GATE2's counting step survives. With explicit 16-gate fan-in-2 basis, one designated output, inputs from earlier gates, ceil(log2 N) index bits and constants, the description count reaches 2^N only at s >= 159 (N=159 first exceeds sqrt N); s/sqrt N = 1.19 at N=256, 7729 at N=2^38. s*log2(N)/N stays near 0.56, so the Omega(N/log N) shape holds with constant about 0.56 under this bound. Nonuniform existence only, no explicit x. Matches GATE2 PROVED claim; no repair needed.
- COMPUTATIONAL (new, sensitivity): the recurrence limit is exactly max(1.1, e, 2(0.6+g)). Leakage g=0.01 -> 1.22, 0.05 -> 1.30, 0.10 -> 1.40, 0.30 -> 1.80. Every +g in the per-level exponent costs +2g in the limit, so the fixed point 1.2 has no slack: the "numerically compatible with FLMV" claim holds only if g (source reads, replay, parent frames, child multiplicity) is charged at essentially 0 exponent at EVERY level.
- COMPUTATIONAL: with g=0 the recursion tree's total exponent at depth j is 1.2 - 2^-j (1.1, 1.15, 1.175, ...), i.e. the deep levels dominate and the bound is approached from below, never beaten. From t0=3, 8 levels reach 1.21. Reaching constant-size children needs depth ceil(log2 log2 N) (4 for N=2^10, 10 for N=2^1000). A per-level constant factor c compounds only to (log N)^{log2 c}, acceptable; a per-level factor N^eps measured against the ORIGINAL N is not (N^{eps log log N}). Overhead must be measured against the current child length, a requirement not stated in GATE2.
- FLMV check: NOT verified. FLMV/Williams forbidden-region statements I can cite with confidence are for space n^{o(1)} (exponent 2cos(pi/7)~1.8019); the (t,s)=(1.2,0.5) point needs the full alternation-trading LP for polynomial space, which was not run here. Status of "compatible with a calibrated forbidden region": CONDITIONAL / UNVERIFIED.

## Precise repairs requested
1. GATE2 ledger should state that hereditary overhead is relative to current child length, and that the limit is max(1.1,e,2(0.6+g)), not 1.2 robustly.
2. The next ARC run must exhibit g=0 at all levels for an actual A->Phi(A), or retire the 1.2 target; any g>=0.3 already reaches 1.8.

## Status
PROVED/EXACT: none new. COMPUTATIONAL: items above. CONDITIONAL: ARC ledger. OPEN: all-input arbitrary-decider contractor, FLMV region check at s=0.5, P != NP. No claim of a lower bound.
Not run this cycle: full repo audit, root main.tex edit (main.tex has a known truncation marker per SOURCE-REFERENCE-FLOOR15; left untouched).
% END_OF_VERIFIED_REPORT::REDTEAM-ARC-GATE2-AUDIT
