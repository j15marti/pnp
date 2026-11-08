# LSPV-5/422 handoff — facet correction and observation rowspace

**Affected IDs:** `[P2-L3-486]`, `[P2-L5-421]`, `[P2-F13]`, `[P2-C3]`; new `[P2-L5-422]`. `[P2-D1]`, `[P2-B1]`, `[P2-B2]` remain OPEN.

1. Exact peer replay of `lspv3_486_absorption_copy_ports.cjs` blob `dd513ca78e081ee29887b6ebaecd280ec94bec6d`: 4,482 assertions PASS, 74 facets, 37 unit-weight control nodes.
2. The `/486` report/tracker has a sign typo. Published $(w\lor\neg v\lor e)$ is false at $(w,t,v,e)=(0,1,1,0)$ and resolves tautologically. Code uses the correct $(\neg w\lor\neg v\lor e)$, yielding $(\neg w\lor e)$. Construction survives; correct shared evidence.
3. For quadratic $Q$ observed through full-row-rank $L$, affine agreement is bounded by the polar-rank sum restricted to $\operatorname{im}(L^T)$. Distinct nonlinear $q_1=uz$, $q_2=u(1\oplus z)$ cancel under export $q_1\oplus q_2=u$: full optimum 3/4, observed optimum 4/4.
4. Therefore a historical repair must authenticate an injective/basis-preserving public observation of the relevant nonlinear coordinates, not merely one nonlinear-derived exported wire. Native DEF/private/LOCAL/AND3/GF(2) ports and weights remain unproved.

Reproducers: `experiments/review/lspv5_422_observation_rowspace_and_facet_audit.py`, `experiments/review/verify_lspv5_422_observation_rowspace.mjs`; raw `results/raw/review/2026-11-07_1752_LSPV5_OBSERVATION_ROWSPACE422.json`; full report `research/main/2026-11-07_1752_MAIN_OBSERVATION_ROWSPACE_FACET_REFEREE422.md`.

Next red-team target: demand a native accepted-byte copy of two private wires into noncancelling authenticated public ports, then replay the exact fixed-weight trace and scope labels. Do not infer `[P2-B1]`, `[P2-B2]` or P versus NP.
