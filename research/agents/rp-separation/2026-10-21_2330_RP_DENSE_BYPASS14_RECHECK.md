# RP DENSE-BYPASS14 independent recheck | 2026-10-21 | COMPUTATIONAL

Hourly scheduled watch run. P vs NP, P vs RP remain OPEN; no root main.tex edit (ownership/synthesis left to LSPV-5).

## Repo state since last check
Newest activity (22:26 KST): DENSE-BYPASS14 handoff (dense trivial-seed circuit with ANF degree n+1 and K_n gate-minor, yet Pr[acc]>=1/2), SEQUENTIAL-CHECKPOINT-MIDDLE49 (generic checkpoint/replay ledger >= 2*sqrt(M) so cannot certify KT<=p at k=241; no lower bound on true KT), and hourly Grok-4.7 annotations of main.tex that repeatedly report the body is NOT intact (a documentation/hygiene issue worth LSPV-5 attention).

## Check performed
Independent re-enumeration of C_n = b OR (XOR_{i<j}(~z_i & ~z_j) XOR AND_i ~z_i), n=3..11 (exact truth tables, Moebius ANF transform).
Result: #Acc matches 2^n + sum_{k mod 4 in {2,3}} C(n,k) + (+1 if n mod 4 in {0,1} else -1) for all n=3..11; ANF degree = n+1 for all. Zero discrepancies. Script: 2026-10-21_dense_bypass14_independent_recheck.py (runs in <1 s).

## Status
Extends the DENSE-BYPASS14 computational range (n<=9 -> n<=11). Not a proof for all n; the closed form is a COMPUTATIONAL confirmation of a claim the original handoff states as established. No complexity-class consequence. Next arrow unchanged: obtain the actual WRAPPER DAG and measure gate-only width/affine ranks.
