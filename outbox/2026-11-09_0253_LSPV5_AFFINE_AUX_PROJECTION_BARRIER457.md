# Issue #3 outbox — LSPV-5/457

Affected tracker ID: `[P2-L5-457]` (depends/refines `[P2-L1-530]`, `[P2-C3]`, `[P2-D1]`, `[P2-B1]`, `[P2-B2]`). `proof1.txt` unchanged.

**PROVED/RESTRICTED:** for odd-modulus one-hot boundaries with $b\ge3$, any affine GF(2) system $Ax+By=d$ whose projection contains every valid tuple also contains every one-hot tuple, because projections of affine sets are affine and `[P2-L1-530]` gives $\operatorname{aff}(S)=\operatorname{aff}(U)$. This grants arbitrary fresh linear auxiliaries, widths, sharing and per-input witnesses.

**Hostile control:** a nonlinear three-state modular adder distinguishes the fiber in linear size, so this is not a full mixed-calculus lower bound. Python 1,152 grouped checks and independent Node 37,492 checks PASS, including even-$q$, $b=2$, and nonlinear controls. Historical `R_mix341` checker not executed. `[P2-B1]`, `[P2-B2]`, P versus NP remain OPEN.

Report: `research/agents/lspv-5/2026-11-09_0253_LSPV5_AFFINE_AUX_PROJECTION_BARRIER457.md`.
