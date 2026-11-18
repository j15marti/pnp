# SCHAEFERGUARD-SIGMA3-1: supplementary adversarial controls
2026-11-18 01:04 PST. Parent report: [SCHAEFERGUARD-SIGMA3-1](https://github.com/j15marti/pnp/blob/main/research/agents/sigma-primary/2026-11-18_0057PST_SCHAEFERGUARD_SIGMA3_1.md).

**COMPUTATIONAL:** A second, independent dependency-free Python script completed **1,455 additional assertions**, zero failures. Combined with the 26,683 primary checks, that is **28,138 assertions**, zero failures. The local reproducibility ZIP SIGMA_SCHAEFERGUARD_20261118_0057PST_bundle.zip now includes the full mathematical REPORT.md, HANDOFF.md, audit.py, results.json, adversarial.py, adversarial_results.json and a verified SHA256SUMS.txt; ZIP integrity tested.

Adversarial breakdown:
- 1,024 source-backed truth-table feasibility replay tests with trailing input padding; 33,813 source characters visited. Demonstrates cheap inspection in explicit easy sources, not a forced entropy lower bound.
- 32 restricted subset-oracle observation comparisons between a complete four-challenge status map and one with an unqueried challenge removed. This models only the stated oracle observation, **not** unrestricted Circuit-SAT or source-readable access.
- Global-vs-adaptive equality check: exists x forall y exists z [z=x XOR y] TRUE but exists x,z forall y [z=x XOR y] FALSE.
- 256 explicit parity-Skolem challenges and 4 compact challenge-dependent x(v)=v XOR 1 witnesses. Local adaptivity can be trivial even when global x is impossible.
- 4 affine-hash image checks: dropping one of two universal bits hides one missing challenge. Does not exclude source-aware methods.
- 100 rational calculations: an actually reached parent-sized delay-padded guest A_D violates the target K'<=max(11/10,3/5+D/2) for integer D=2..101. A compiler that bypasses A_D is not excluded.

**Scope:** This strengthens falsification coverage of padding, source replay, restricted oracle simulation, affine shortcuts, equality/witness reorderings and easy compact strategies. Primary physical-DAG tests already covered reconvergence. No all-input hereditary A→Phi(A), no same-machine FLMV implementation, no proof of P≠NP. Next target remains genuine source-backed small-child conversion with all acquisition, memory and recursive costs charged.

ADVERSARIAL_VERIFICATION_SENTINEL_SCHAEFERGUARD_SIGMA3_1_20261118_0104PST_1455