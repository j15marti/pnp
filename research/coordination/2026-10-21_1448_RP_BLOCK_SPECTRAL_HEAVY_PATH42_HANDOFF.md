# RP-BLOCK-SPECTRAL-HEAVY-PATH42 handoff

**Status:** restricted theorem ESTABLISHED; P=RP, P!=RP and P!=NP OPEN.

The new BLOCK-SPECTRAL7 handoff is valid in its explicit promise model once
the missing density step is supplied. With `ell` independent blocks and at
most `w` boundary states, edges of conditional probability at most
`delta=1/(4*ell*w)` are traversed with total probability at most `1/4`.
Since an RP YES input accepts with probability at least `1/2`, an accepting
path exists whose every edge has density greater than `delta`. If every edge
indicator has known Fourier L1 at most `B`, an explicit epsilon-biased set
with `epsilon<delta/(2B)` hits every edge of that path. Layered reachability is
therefore a uniform deterministic polynomial-time decider and can reconstruct
an accepting tape.

Firewall: singleton indicators have Fourier L1 exactly one but exponentially
small density, so small L1 alone does not hit arbitrary nonempty transitions.
The RP mass plus polynomial block/state count is load-bearing. No arbitrary RP
normal form was proved. No PNP arrow was changed.

Reproduction: `rp_block_spectral_heavy_path42_audit.py` and
`RP_BLOCK_SPECTRAL_HEAVY_PATH42_raw.json`; 104,891 exact assertions, zero
failures.

Next :36 falsifier: block-size tradeoff for the quadratic-phase verifier,
tracking boundary-state count times local Fourier L1. Next :12 obligation:
name a language and quantify against all deterministic polynomial machines.

