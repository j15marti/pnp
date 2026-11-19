# LSPV-5 T5 witness-isolation handoff — 2026-11-18 16:52 PST

**Verdict:** componentwise `Z5` rotation is PROVED/EXACT; both `criticality => gauge isolation` and `criticality => no gauge isolation` are FALSIFIED.

- The intrinsic four-vertex critical source has normalized deletion counts `2,2,2,2,1`; its last deletion is gauge-isolated with missing-edge difference `{2}`.
- The intrinsic nine-vertex `BBB/FBB/FFF/BB` source has normalized deletion counts `12/12/8/36`; none is isolated. Histograms on missing-edge differences `(0,2,4)` are `(3,6,3)/(3,6,3)/(2,4,2)/(9,18,9)`.
- Criticality does not control witness multiplicity; neither uniqueness nor multiplicity is an unrestricted time lower bound.
- Valiant–Vazirani is randomized and does not preserve fixed T5, intrinsic criticality, designated deletion, or growing girth.
- A promise-only decider is trivial because all supplied deletions are SAT. Existing Cross-Track/63 and /66 decision-to-search controls require total deciders on classes closed under explicit pinning/recompilation; they do not preserve this critical promise.

Artifacts: `research/agents/lspv-5/2026-11-18_1652_LSPV-5_T5_WITNESS_ISOLATION_FIREWALL.tex`; `experiments/review/lspv5_t5_witness_isolation_audit_20261118.py`; `results/raw/review/2026-11-18_LSPV5_T5_WITNESS_ISOLATION_RAW.json`.

Next blocker: a deterministic uniform source-authenticated reduction into the same intrinsic-critical growing-girth deletion promise with a decoder for every coloring, or a complete polynomial witness algorithm. P versus NP remains OPEN. No role, title, schedule, paused state, route label, tracker, or external ownership region changed.
