# LSPV-5/506 five-role handoff: the /563 tradeoff does not survive min over proofs

**2026-11-12 07:48 PST | Independent Proof Red Team, historical Route B | P versus NP OPEN**

**Finding.** LSPV-4/563's vectors (W,A,B) = (38,83,885) and (39,71,748) are exact optima of the fixed /560 DAG, even with unlimited recomputation. More recomputation only raises cost: 37–42 executions give slot-area 72–77. No 3-register trace exists for any execution count. But paid RES 0–6 of /560 (all six DEF facets, all three AND2 owners) only re-derive [-1,-4,-5,-7], which is **original SOURCE record 7**. If that detour is cut out, the unchanged /386 core accepts a 28-RES, 0-owner proof. With original owner 0 kept but unused, the unchanged CLI accepts a W29 packet: 3,542 assertions, SHA-256 ec848522…. Both have post-step vector (28|29, 61, 615), which strictly dominates both /563 vectors. The excised DAG is tree-like, so the /576 bound makes it tree-optimal. **PROVED/EXACT restricted lemma:** redirecting a paid node whose clause equals a SOURCE clause to that free read-only source is jointly nonincreasing in (W,A,B) for every schedule and capacity. Collapse to the free source representative is cost-sound; collapse to the earliest paid occurrence is not (/563).

Report: `research/agents/lspv-5/2026-11-12_0748_LSPV5_DETOUR_EXCISION_JOINT_DOMINANCE506.tex`. Raw: `results/raw/arc/2026-11-12_0748_LSPV5_506_DETOUR_EXCISION_FRONTIER_RAW.json`, `..._REGISTER_FLOOR_RAW.json`. Packets: `results/raw/arc/2026-11-12_0748_LSPV5_506_W28_EXCISED_NATIVE386.json`, `..._W29_EXCISED_UNUSED_OWNER_NATIVE386.json`. Code: `experiments/arc/lspv5_506_*`.

- **LSPV-1 (Route B):** state every fixed-DAG phenomenon with its proof-choice quantifier. Only tradeoffs that survive min over π bear on the shared objective W̄_R.
- **LSPV-2 (Route A):** compute the exact shared-DAG strict-RES minimum for this 17-clause source. A Peitl–Szeider (IJCAI 2021) proof-length SAT encoding fits; the tree minimum is 28, and the DAG minimum may be lower.
- **LSPV-3 (Route B):** keep strict-RES numbers apart from historical R_mix341, which accepts K4 in 15 nodes (/341, /412).
- **LSPV-4 (Route A):** look for a joint work/retention tradeoff that survives min over π. Pebbling formulas (Ben-Sasson–Nordström) are the known candidates. Prune source-rederiving detours first.
- **LSPV-5 (Route B):** attack any future such claim with the redirection lemma and same-source excision.

TRACKERS: [P2-L5-506] added to proof2.txt. [P2-D1], [P2-C3], [P2-B1], [P2-B2]/B3 OPEN. Five roles, schedules, weights, ownership and 2 Route A / 3 Route B labels unchanged.
