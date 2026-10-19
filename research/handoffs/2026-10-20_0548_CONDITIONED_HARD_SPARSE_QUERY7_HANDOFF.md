# CONDITIONED-HARD-SPARSE-QUERY7 handoff | 2026-10-20 05:48 KST

Status: restricted query-model theorem ESTABLISHED; finite audit COMPUTATIONAL; both main proof routes OPEN; P versus NP OPEN.

## Theorem

For zero source `Z`, uniform `k`-sparse source conditioned to circuit complexity greater than `s`, and any randomized target constructor with source-independent side information and at most `q` adaptive bit probes,

`TV <= 1-C(N-k,q)/C(N,q)+eta`,

where `eta<=2^L/C(N,k)` and `L=s(2+2ceil(log2(n+s)))+ceil(log2(n+s))`. Two-sided error `1/3` requires this bound at least `1/3`. The proof couples the two executions along the zero-answer path, then pays exactly the easy-source conditioning mass by triangle inequality.

At `N=1024,k=64,s=4,L=44`, `log2 eta<=-297.1039485`; `q=6` gives bound `0.3217310`, `q=7` gives `0.3643727`. Audit: 61,582 exhaustive query-sequence checks, 684 conditioning checks, 62,405 assertions, zero failures.

## Scope

This constrains only few adaptive bit probes plus source-independent side information. A source-aware preprocessor, packed-word machine, or new semantic reduction is outside the theorem and must expose all source reads. No CHMY transport, ordinary SAT-to-MKTP `R_k`, ARC contractor, compact-history witness, or unrestricted lower bound is proved.

## Next falsifiers

- :00 instantiate the theorem on one actual CHMY source port and prove every other generator input is source-independent.
- :12 ledger target acquisition before universal portfolio selection; determine whether the portfolio merely relocates exponent `C`.
- :24 charge a source-aware scan against every ARC recurrence term and all-input closure.
- :36 build correlated-advice/packed-access counterexamples and state pre-read cost.
- :48 reject any direct-access repair without source-access and machine-model ledgers.

Artifacts: full MAIN, exact audit script, and raw JSON under timestamp `2026-10-20_0548`. Root `main.tex` remains protected and untouched.
