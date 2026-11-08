# LSPV-4/500 publication receipt | 2026-11-08 11:36 PST
**Result:** Restricted proof + finite computational controls, P versus NP OPEN.

| Artifact | Path | Exact Git blob | Commit |
| --- | --- | --- | --- |
| Independent Node source | `experiments/arc/lspv4_500_fullscan_trace_antichain.mjs` | `fd7e20bf7974393d9a089f95266f6b4486fb7c1d` | `18c32c676060322a4913f00097178e32ff9c858f` |
| Raw result ledger | `results/raw/arc/2026-11-08_LSPV4_500_FULLSCAN_ANTICHAIN_RAW.json` | `4fdd59d00103ca84a4eb86e65ab56d6ff399b019` | `8eb6619a88719be73d5a7c5149a694c5be8a9fd7` |
| Role-owned report | `research/agents/lspv-4/2026-11-08_LSPV4_FULLSCAN_TRACE_ANTICHAIN500.md` | `98397dc8dc3277b8440be9467b511c6082ec53e8` | `e29a09123b52a16644a2f8f8cf6f94f3c8cf35d0` |
| Five-role handoff | `research/coordination/2026-11-08_LSPV4_FULLSCAN_TRACE_ANTICHAIN_FIVE_ROLE_HANDOFF500.md` | `5edaa59dd5107031bdaefa3c24683343fef5ee45` | `548504efc72012c6af750d94cdbf9b33d5b8b036` |
| Root tracker append | `proof2.txt` | `668e68fc4121622efd712e91ae9165dc429c79ce` | `d9ff1455ded09e11c2fa71fb2dbb48266306d832` |

All four new files individually re-fetched with exact UTF-8 string equality. For `proof2.txt`, fetched prior blob `6f2103674963296f3710a6d3533adf329995d640`, used that current SHA in a conditional write, and fetched the complete resulting `proof2.txt` (490,077 characters); the first 486,870 characters match the entire previous file exactly, with new node `[P2-L4-500]` appended. `proof1.txt` reviewed without change at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.

Coordination issue #3: https://github.com/j15marti/pnp/issues/3#issuecomment-6726299545, comment ID 6726299545, independently fetched and exact-body readback verified.

Locally executed two independent implementations (Python and Node/V8) on 128 distinct K4 odd-only and 128 distinct odd/even sources. Cross-language comparison: all 32 portfolio/anchor configurations and two source SHA256 strings match. All full-read portfolios show 128 actual guest calls, 0 cache hits. Short-prefix positive control with two anchors shows 2 calls, 126 hits. Four malformed controls rejected in Python. No raw hosted execution is a native FLMV finite-state machine or the historical Rmix341 accepted-byte checker.

**Publication limitations:** Local git network DNS unavailable; used authenticated GitHub connector for publishing. Repository root `main.tex` fetched at blob `68188a24badda635a5983fda1c381cdb694fd497` but yielded empty text and was NOT edited. Repo preflight / CI report checks not run locally because a repository clone was not available. The symbolic full-scan decider theorem is conditional on any hypothetical correct polynomial SAT decider; the finite test fallback is not that decider. No other agent's manuscript region or research task was modified.

**Open nodes:** [P2-A2], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Historical R_mix341 grammar/weights, existing five agents, identities, schedule/timezone/enabled states and two-A/three-B allocation preserved. P versus NP OPEN.
