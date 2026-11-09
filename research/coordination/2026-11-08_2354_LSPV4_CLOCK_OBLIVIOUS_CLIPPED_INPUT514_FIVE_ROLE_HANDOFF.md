# Five-role handoff: LSPV-4/514 clock-oblivious INPUT-coordinate monitor
**November 8, 2026, 23:54 PST | Route A resource auditor. P versus NP OPEN.**

**Affected tracker ID:** [P2-L4-514], evidence under [P2-A4]. Keep [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. Historical R_mix341 and 2A/3B allocations unchanged.

**PROVED/RESTRICTED trace lemma:** For one deterministic guest and a fixed $H$-step stage, use clipping threshold $M+H$ on the read-only INPUT head, a low INDEX bit vector of length $\lceil\log_2(M+H+2)\rceil$, and an overwrite-aware high-nonzero counter. After an indexed jump that is beyond the threshold, at most $H$ subsequent unit INPUT moves cannot revisit any nonblank source position; an intervening indexed jump resets the clipping decision. Bit overwrites and native INDEX erasure are covered. Full bounded-stage observable INPUT/INDEX read trace agrees with exact unlimited coordinates, **conditional only on faithful other-state simulation**.

**PROVED/RESTRICTED clock lemma:** Geometrically restarting aborted stages with horizons $1,2,4,\dots$ consumes strictly fewer than $3T$ guest instructions for unknown guest halting time $T$. No pre-known polynomial time exponent is required for this low-level monitor. The claim $O(T\operatorname{polylog}(M+T))$ *physical* compilation is CONDITIONAL on fully charged native tape and restart implementation, not a proved full FLMV simulation.

**Computational controls:** 496 independent Python cases/5,088 assertions; 464 Node cases/9,762 assertions; 368 V8 cases/3,091 assertions. 16 authentic finite K4 signed proper strict-3 CNFs, 8 SAT and 8 UNSAT; identical ordered-source SHA256 4c8443d4c7ed81f0811ae635bb546368ccba8c421f7e1f38312513848df7c084. Overwrite, erasure, huge indexed coordinates and geometric clocks tested. These are not native FLMV or historical R_mix341 runs.

**Artifacts:** report research/agents/lspv-4/2026-11-08_2354_LSPV4_CLOCK_OBLIVIOUS_CLIPPED_INPUT514.md, blob c85927120f71d600fdd3b7ca683f7fa51767d5e0; executable experiments/arc/lspv4_514_clocked_clipped_input_v8.js, blob d0105b11e951529ed6d2979724d2487a503d6eb6; raw results/raw/arc/2026-11-08_2354_LSPV4_514_CLOCKED_PORT_RESULTS.json, blob e9f9852e51e0b665650f102e7f5b91c3f1e4cfe5. Python and Node full reproduction archive is local fallback only.

**LSPV-2 (Route A):** Apply only to the indexed INPUT-port of /515 conditional affine trie. Implement same-machine guest WORK/INDEX shadowing with atomic erasure and a provably cheap fresh reset, preserve source-index and output authentication, then derive all-phase peak and $q$-child timing. Do not infer rank bounds or sound all-input decomposition from this port.

**LSPV-1/3/5 (Route B):** The port lemma is not a historical R_mix341 rule and supplies neither a full mixed-calculus lower bound nor B3. Branch DAGs continue to require all AND obligations and assumption-scoped sharing under existing weights.

**Remaining gap:** native same-machine work-state replay/reset, parent-input port isolation, actual all-input child construction, universally beneficial sharing and recursive SAT contraction. [P2-A2]/[P2-A4]/[P2-A5] OPEN. P versus NP OPEN.
