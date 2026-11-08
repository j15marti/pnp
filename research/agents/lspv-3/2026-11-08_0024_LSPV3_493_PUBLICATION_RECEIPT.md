# LSPV-3/493 publication verification | 2026-11-08 00:24 PST

**PROVED/RESTRICTED; P versus NP OPEN.** Complete GitHub readback of report, executable, raw results, handoff, full prewrite outbox and both trackers succeeded. Evidence new [P2-L3-493] refines [P2-D1] and [P2-C3], leaving [P2-B1] and [P2-B2] OPEN.

| Artifact | Path | Verified Git blob |
| --- | --- | --- |
| Report | `research/agents/lspv-3/2026-11-08_0024_LSPV3_ONEHOT_NATIVE_CORE_CLOSURE493.md` | `38a0b97484252096f4931770ba61cb9185a0fa04` |
| Exact published executable | `experiments/arc/lspv3_493_onehot_source_and3_xor_closure.js` | `09ca3e0aa1e9f3ba18ed84b5e586df789a6a3cd4` |
| Raw results | `results/raw/arc/2026-11-08_0024_LSPV3_493_ONEHOT_LOCAL_CORE_RAW.json` | `5a0d7dd9a9b426c949bb60ef8e82bbb702ed9eee` |
| Five-role handoff | `research/coordination/2026-11-08_0024_LSPV3_ONEHOT_NATIVE_CORE493_FIVE_ROLE_HANDOFF.md` | `ba8bdd3d2fd3ec85c5679506b02af3752fd0cbcd` |
| Exact complete prewrite proof2 backup | `research/agents/lspv-3/outbox/2026-11-08_0024_LSPV3_493_PROOF2_PREWRITE_EXACT.txt` | `20008a8678f5f043e93a3260c9984a1a6f0b4cf9` |
| Updated proof2 tracker | `proof2.txt` | `f88a11267e194fb63cef14a0b55929d95d530cbe` |
| Reviewed unchanged proof1 tracker | `proof1.txt` | `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` |

**Tracker write:** commit `89315c5c79621c12f6c055ebef269e88bfdf2c30`. The updater refetched current complete proof2 content, passed current blob SHA to the replacement action, verified complete readback equality, and established exact unchanged previous-content prefix. No other nodes or historical weights modified.

**Coordination:** issue #3 comment 6719426308, `https://github.com/j15marti/pnp/issues/3#issuecomment-6719426308`, complete body-equality readback succeeded.

**Reproduction:** independent Python 7,392 checks/4 rejects, independent Node 4,691 checks/4 rejects, separately published V8 source 37,510 checks/4 rejects. The recovered historical /341 checker was not executed against the one-hot source; it lacks RES and a general one-hot source binding interface. This is a restricted relative-incompleteness finding, not a lower bound on complete historical R_mix341. The five existing agents, two Route A/three Route B allocation, schedules, enabled states and historical weights remain unchanged. Root main.tex untouched. P versus NP OPEN.
