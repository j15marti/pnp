# REDTEAM26 independent verification (peer slot :36)
Status: COMPUTATIONAL + short proof check of a restricted lemma. P versus NP remains OPEN. No root main.tex edit.

Re-implemented the REDTEAM26 family from scratch (own generator, pairing of addresses 2k,2k+1 by parity(k)); script was scratchpad-local, raw output at results/raw/separation/2026-10-20_REDTEAM26_INDEPENDENT_VERIFY_raw.json.
- Brute force n=1..4 (up to 17 variables): a=1 gives exactly 2 satisfying assignments, a=0 gives 0. Agrees with REDTEAM26.
- n=1..12: clause count = 3N/2; both claimed assignments (planted b=0,y_i=parity(i); shared b=1,y_i=0) satisfy every clause. The j/3 random-access indexing is consistent (one unit clause + two binary clauses per address pair).
- Dependency argument re-checked: parity on n address bits depends on all n inputs, so a connected fan-in-2 DAG needs >= n-1 binary gates. Exhaustive small search: XOR2 needs 4 gates over AND/OR/NOT counting NOT (3 binary + NOT), consistent with the bound.
No falsification found. Scope reminder: the lemma only shows "hard planted witness does not imply hard shared witness"; it says nothing about SAT lower bounds. The load-bearing open arrows (CHMY small-beta transport, MMW SAT->MKTP R_k, ARC joint resource contraction) are unchanged.
END_REDTEAM26_INDEPENDENT_VERIFY_P_VS_NP_OPEN
