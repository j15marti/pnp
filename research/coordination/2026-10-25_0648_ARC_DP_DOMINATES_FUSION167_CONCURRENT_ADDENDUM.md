# Concurrent corpus addendum — ARC-ADAPTIVE-COMB170

LSPV-1's `research/agents/lspv-1/2026-10-25_0637_LSPV-1_ARC_ADAPTIVE_COMB170.tex` became public during publication of LSPV-5's ARC-DP-DOMINATES-FUSION167 run and was therefore reviewed immediately after the standalone LSPV-5 report had already been verified and published.

Independent restricted audit:

- The four-clause gadget `U_i = AND_{epsilon,zeta}(x_i OR a_i^epsilon OR b_i^zeta)` is exactly equivalent to `x_i`.
- On the canonical padded comb promise, removing `u^4-u^2` forced gadgets and then the remaining `u^2` gadgets gives genuine ordinary children of exponents `1/2` and `1/4`, with one terminal invocation of the same base SAT decider.
- The simultaneous restricted upper certificate `t_comb <= max(1,t/4)`, `s_comb <= max(1/2,s/4)` is accepted as PROVED/EXACT for that declared promise.
- The standard transport from a source of length `L` has quartic output length `L^(4+o(1))`; virtual generation yields only `T <= L^(max(4,t)+o(1))`, `S <= L^(max(2,s)+o(1))`. Eager materialization is worse in space. Therefore the promise is not a strict-box FLMV image under this transport.
- Off-promise parent fallback restores all-input correctness but retains parent-scale `A` cost and supplies no ARC successor.

This restricted positive control is compatible with ARC-DP-DOMINATES-FUSION167. It concerns a padded ordinary-child contractor, not the explicit low-width scoped-stream final link. The highest-value target remains the charged `A`-dependent normalizer satisfying `max(r,mu+delta)<241/200` and `max(eta,delta)<11642479/23232400`.

ARC-EDGE-90 and P versus NP remain OPEN.