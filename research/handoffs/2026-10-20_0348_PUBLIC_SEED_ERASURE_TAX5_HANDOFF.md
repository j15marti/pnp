# PUBLIC-SEED-ERASURE-TAX5 handoff | 2026-10-20 03:48 Asia/Seoul

## New exact result

For a deterministic public-seed map, joint-output TV for two sources equals the probability their outputs differ. With independent repetition it is exactly `1-(1-alpha)^r`. Two-sided error at most `1/3` on both sources requires TV at least `1/3`, hence `r=Omega(1/alpha)`.

Combined with MULTIPORT-MASK-FLOOR3, `alpha<=|S|p^t`. For unbiased masks, constant-density support and `t=(1+kappa)log_2 N` imply `alpha<=delta N^-kappa` and therefore `r=Omega(N^kappa)`. Explicit repeated target instances carry a polynomial output/time tax. A compact joint target could evade this only with a new proved ordinary-target encoding and charged decoder.

Exact audit: five REDTEAM22 values need `7,4,7,2,2` copies to reach TV `1/3`; polynomial-erasure controls through `N=64,kappa=2`; 39 exact assertions, zero failures.

## Next falsifiers

- **MCSP:** original private CHMY generator only; test actual two-coordinate dependence and both promises in the critical band.
- **Universal Solver:** price construction and verification of one compact target combining `r` copies; preserve the unknown solver exponent.
- **ARC:** charge repetition/combination in `a,g,r,eta,lambda` and all output bits.
- **Red team:** attack independence, adaptive ports, nonlinear embeddings, and alleged compressed joint targets.
- **Synthesis:** keep the result scoped to modified public fixed-port maps.

Root `main.tex` remains placeholder-bearing and untouched. Compact History is diagnostic only. **P versus NP OPEN.**

END_OF_VERIFIED_HANDOFF::PUBLIC_SEED_ERASURE_TAX5
