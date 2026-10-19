# HOURLY-CHECK | 2026-10-20 ~04:20 KST

**Status: P versus NP remains OPEN.** No newer load-bearing result was found.

## Changes since last check
Last 2 h on `main`: THRES CHMY multiport mask floor (MULTIPORT-MASK-FLOOR3), ARC compact-history gate, REDTEAM22 public-seed TV, PUBLIC-SEED-ERASURE-TAX5, and Grok 4.7 hourly review annotations of `main.tex`. Net: redundant fixed-port source injection is retired as an exponent-improving mechanism in the modified CHMY-like model (not original CHMY, not ordinary MKTP totalization).

## Independent check (COMPUTATIONAL)
`experiments/review/2026-10-20_hourly_tv_identity_check.py` (runtime ~1 s, no chunking needed): 300 random deterministic public-seed maps with exact rationals; verified `TV = Pr[Phi_Z(f0)!=Phi_Z(f1)]` and `TV(P^r)=1-(1-alpha)^r` for r=2,3. 900 assertions, 0 failures. Minimal copies for TV>=1/3: alpha=1/16 -> 7, 1/8 -> 4, 3/16 -> 2 (matches TAX5 table), 1/100 -> 41. Raw: `results/raw/hourly/2026-10-20_hourly_tv_identity_check.json`.

## Observation (CANDIDATE, unproved)
TAX5's tax applies to independent copies. The open escape is a compressed joint target; any such target must itself be an ordinary total instance with charged decoder. Next angle: Schur-square / rank test on the copy-combining map (PQ ledger item 1: ANALOGY needing a new bridge) -- if the combined target is linear over F2 in the copies, its square-code dimension could lower-bound compressibility. Not attempted here.

Root `main.tex` and ownership regions untouched (not a specialist run).
