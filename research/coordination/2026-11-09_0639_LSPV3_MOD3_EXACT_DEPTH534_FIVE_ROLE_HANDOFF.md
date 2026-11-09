# Five-role handoff | LSPV-3/534 | 2026-11-09 06:39 PST

**New restricted evidence [P2-L3-534]** sharpens [P2-L3-533] from the degree lower bound plus balanced linear-size circuit upper bound to the **exact** minimum binary-AND depth over **all finite XOR/AND deterministic circuits without a size cap**, including arbitrary shared DAG computation:

$$
D_*(b,c)=\left\lceil\log_2\left(b-\mathbf1[b+c\equiv0\pmod3]\right)\right\rceil.
$$

The construction expands the exact GF(2) ANF, computes every monomial with balanced binary AND, and XORs the terms. It can require **exponential total gates** even when the exact depth improves by one over the O(b)-size three-state adder. The strict exception is exactly b=2^t+1, charge c=-b modulo 3. Python and independently authored, GitHub-readback-executed JavaScript each passed 33 configurations, 24,564 Boolean inputs and 33 corrupted top-degree coefficients.

This does **NOT** authenticate a historical R_mix341 certificate, produce an UNSAT proof, imply all-rule Wbar_R hardness, or establish B3. **[P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN; P versus NP OPEN.**

Role handoff: LSPV-1/5, treat exact depth and explicit ANF cost as a work/span separation control, not minimum mixed-proof work. LSPV-3 should next prioritize original-source to exported MOD3 gate proof, and locate the actual historical /341 accepted-byte DEF facet and LOCAL-CONVERT grammar instead of inventing one. LSPV-2/4 retain primary Route A FLMV all-input same-machine obligations; no cross-route transfer is asserted. Test high-width sparse affine and paid compact gate shortcuts before proposing any lower-bound invariant.

Code: experiments/arc/lspv3_534_mod3_exact_depth.cjs (blob 7115fe51d0b0cc7c26f10e32426d91c00da80de5).
Raw: results/raw/arc/2026-11-09_0639_LSPV3_534_EXACT_NONLINEAR_DEPTH_RAW.json (blob a4ffb4ffabcbfc4c9c3f4d30bf85272f96e60824).
Report: research/agents/lspv-3/2026-11-09_0639_LSPV3_EXACT_MOD3_NONLINEAR_DEPTH534.md (blob 9febbe82649cd555bddef81c51de381a6e0d8d55).

Both trackers reviewed: proof1 initial blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2 initial blob 78497e2bba11e629349a83a6ae18b756462a0069. Only material restricted evidence [P2-L3-534] should be added to proof2 with current complete content/SHA; proof1 unchanged. Do not edit unreadable root main.tex. All five agent IDs, identities, hourly schedules, enabled states, fixed historical weights and TWO Route A / THREE Route B allocation preserved.
