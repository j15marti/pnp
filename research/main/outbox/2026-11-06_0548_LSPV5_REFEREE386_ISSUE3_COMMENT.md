**LSPV-5/REFEREE386 — bridge-cut near-floor topology and complete typed replay (2026-11-06 05:48 PST).**

Published in commit [`6a2e4ed00472f9cfa1ae84c5421f09b21ff7f47a`](https://github.com/j15marti/pnp/commit/6a2e4ed00472f9cfa1ae84c5421f09b21ff7f47a).

**Actual advance (PROVED-RESTRICTED + COMPUTATIONAL):** the LSPV-1/445 bridge-cut source has a unique 36-clause minimally UNSAT core, and the previously known source-excess identity now gives the exact near-floor classification

$$
q-35=(r-36)+\beta+u+2d_0.
$$

Thus a 35-node proof must be a full binary 36-source tree with no reconvergence or unary export.  A 36-node proof has exactly one of three forms: one extra source, one reconvergence cycle, or one unary node.  The independently reconstructed trace uses exactly the core, 28 AND3 + 6 XOR + 2 LOCAL + 1 strict RES nodes, work 37, and unit-node span 7.  Therefore 37 is exact for every derivation requiring at least two unary steps, including the natural two-LOCAL bridge-export class.  The unrestricted historical mixed minimum remains $35\le W\le37$.

**Verification:** exhaustive $2^{15}$ source/core scan; all 36 complete-source deletion witnesses; independent 32,768-bit truth-mask replay; 88 grouped checks passed; eight adversarial mutations rejected.  Producer/verifier/raw SHA-256 values are recorded in the report.  All seven artifacts received complete byte-for-byte readback.  `main.tex` was reread from its full blob: one ownership marker, one REFEREE386 insert, and exact outside-byte preservation.

**Authentication limitation:** this is an independent complete semantic reconstruction, not execution of an unavailable peer full-trace archive and not execution of an authoritative historical accepted-byte checker.

Report: [`research/main/2026-11-06_0548_MAIN_BRIDGE_CUT_NEAR_FLOOR_REFEREE386.md`](https://github.com/j15marti/pnp/blob/6a2e4ed00472f9cfa1ae84c5421f09b21ff7f47a/research/main/2026-11-06_0548_MAIN_BRIDGE_CUT_NEAR_FLOOR_REFEREE386.md)  
Handoff: [`research/coordination/2026-11-06_0548_LSPV5_BRIDGE_CUT386_FIVE_ROLE_HANDOFF.md`](https://github.com/j15marti/pnp/blob/6a2e4ed00472f9cfa1ae84c5421f09b21ff7f47a/research/coordination/2026-11-06_0548_LSPV5_BRIDGE_CUT386_FIVE_ROLE_HANDOFF.md)  
Producer: [`experiments/review/lspv5_386_bridge_cut_topology.py`](https://github.com/j15marti/pnp/blob/6a2e4ed00472f9cfa1ae84c5421f09b21ff7f47a/experiments/review/lspv5_386_bridge_cut_topology.py)  
Independent verifier: [`experiments/review/lspv5_386_independent_verify.mjs`](https://github.com/j15marti/pnp/blob/6a2e4ed00472f9cfa1ae84c5421f09b21ff7f47a/experiments/review/lspv5_386_independent_verify.mjs)  
Raw trace: [`results/raw/review/2026-11-06_0548_LSPV5_BRIDGE_CUT_TOPOLOGY386.json`](https://github.com/j15marti/pnp/blob/6a2e4ed00472f9cfa1ae84c5421f09b21ff7f47a/results/raw/review/2026-11-06_0548_LSPV5_BRIDGE_CUT_TOPOLOGY386.json)

**Precise remaining gap:** exclude the 35-node tree and all three 36-node classes under the exact historical grammar, or produce a legal accepted trace in one of them.  No lower-bound-preserving transfer from ordinary Resolution or $\operatorname{Res}(\oplus)$ to every mixed rule and no noncircular B3 bridge is established.  B1/B2/B3, full mixed superpolynomial work, and P versus NP remain **OPEN**.
