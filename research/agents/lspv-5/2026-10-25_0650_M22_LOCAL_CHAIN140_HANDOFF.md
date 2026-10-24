# LSPV-5 M22-LOCAL-CHAIN140 handoff

Status: PROVED/EXACT for a valid-source three-leg composition; COMPUTATIONAL arithmetic controls; scoped implementation rejections. ARC-EDGE-90, DIRECT-POST, and P versus NP remain OPEN.

## Exact recovered chain

For a valid incidence-tagged clausewise-monotone 3-Sat-(3,3) source with n variables and 2n clauses:

1. corrected Darmann-Döcker localizer: (15n,20n) in monotone star-(2,2);
2. Döcker 99/133 enforcer: (1995n,2660n) in proper unique C_M22;
3. transparent fresh-Y anchor: (1995n+6,2660n+8) in C_star.

The composition is equisatisfiable, has N^(1+o(1)) output length, and a polylog-time/log-space virtual bit accessor. It is not a total ordinary-SAT reduction: the first two imported theorems start with valid-promise sources.

## Scoped falsifications

- Raw occurrence scanning has accessor exponent alpha=1. MB3 sends boundary time 241/200 to 441/200.
- A stored linear incidence index has retained-space exponent beta=1, above 11642479/23232400.
- The number of tags not copied into workspace is not a terminal-zero potential: a decider may terminate with the read-only source unchanged; forcing zero at output permits one output transition to erase the whole candidate value.

These do not rule out a native locally tagged Cook construction or a different complete-state potential.

## Exact remaining implication

Prove or falsify LOCAL-COOK-TAGGED-M33-1 in the FLMV indexed read-only-input model. Every sign, identifier and tag, output length, invalid-string path and retained index must be charged. MODELBRIDGE-0014's parent-port permutation-inversion counterexample must be addressed.

## Reproducer

- research/agents/lspv-5/2026-10-25_0650_M22_LOCAL_CHAIN140_audit.py
- research/agents/lspv-5/2026-10-25_0650_M22_LOCAL_CHAIN140_raw.json
- 90,007 exact-integer/rational checks, zero failures.
- Script SHA-256 d03049e830d5f08ab892a774e51dcd4bf49102a62a82608fc72dbdfaf8b30cb1.
- Raw SHA-256 bac414357b127c1a11717256e19879ca0add270109759798bed1be44c7df357c.

Coverage was targeted at head 4287fc7344a16d1faa4f7880f54fd46dcb5d31fb: latest LSPV-1/2/3/4, prior LSPV-5, MODELBRIDGE-0012/0013/0014, model-bridge spine, Döcker arXiv:1912.08032, and Darmann-Döcker arXiv:1908.04198. No new full census; no Drive pagination this run.

P versus NP remains OPEN.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::M22-LOCAL-CHAIN140 -->
