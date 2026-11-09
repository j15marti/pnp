# LSPV-2/509 five-role handoff | 2026-11-08 18:13 PST

**Route A (LSPV-2 builder): PROVED/RESTRICTED contextual replay repair, COMPUTATIONAL finite checks; P versus NP OPEN.**

Report: [research/agents/lspv-2/2026-11-08_1813_LSPV2_FRAME_PRESERVING_EFFECT_REPLAY509.md](../agents/lspv-2/2026-11-08_1813_LSPV2_FRAME_PRESERVING_EFFECT_REPLAY509.md) blob \`fd870979e615e73adc4a7d69fd88394c14b70c79\`.

Published exact executable: \`experiments/arc/lspv2_509_frame_effect_replay.cjs\` blob \`3f350ed83e1150154ce40f446fc18ac680b78e9b\` (matches local \`git hash-object\`; independently executed Node.js). Raw: \`results/raw/arc/2026-11-08_1813_LSPV2_509_FRAME_EFFECT_RAW.json\` blob \`c5bb52a8da9d07e238a4d93b31433ddc7b126155\`. Independent Python implementation, full Node.js source, and results accompany the conversation archive.

Theorem: With equal deterministic guest entry control/head state, equal immutable-input length and bit values at all read positions, and equal initial WORK cells read before first write, a trusted anchor trace determines the SAME guest continuation. Its write log may be **applied only to cells actually written**, preserving target caller's other memory. The whole-run FLMV WORK high-water must join the caller's historic peak and the guest's paid accesses. This avoids the LSPV-2/508 incorrect whole-poststate merge. It is an application of established imperative self-adjusting computation principles, not a new general SAT speedup.

Finite results: JavaScript 882 assertions, 192 exactly matched framed replays, 64 rejections (16 each changed source, live memory, entry metadata, forged source record); independent Python 834 assertions, same 192 accepted plus 48 mutation rejections. Sixteen original signed K4 strict 3-CNF sources classified by exhaustion (8 SAT, 8 UNSAT), two malformed controls. Python and Node have the same K4 source SHA-256. Neither run used the native FLMV machine or historical R_mix341 checker.

- **LSPV-4, Route A:** Audit paid source read, log construction, lookup, update, retained state, peak WORK high-water, indexed-address representation and recomputation versus retention; no uncharged sparse dictionary or exponential high-address alias.
- **LSPV-2, Route A:** Need solver-dependent, exponent-oblivious all-input 3-CNF constructor and recursive applicability. This frame lemma only permits some guest reuse; \`q=N^{3/5+o(1)}\` and child bound \`N^{1/2+o(1)}\` remain unproved for all source inputs.
- **LSPV-1/LSPV-3/LSPV-5, Route B:** No implications for fixed historical R_mix341 grammar/weights, B1/B2/B3, or shared proof DAG legality. Do not import an external write-log trace as an UNSAT certificate. Test assumption-scope leaks if a cached branch effect is transplanted into a proof context.

**Exact OPEN nodes:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No task, identity, schedule, enablement, route allocation, inference rule or weight changed. Root \`main.tex\` fetched by GitHub twice (utf-8 and base64) with blob \`63b54c9988cc83533472a05c25bda2ab48b5e4ca\` but zero readable bytes; left untouched rather than overwriting an unreadable root file.

**Next decisive deliverable:** prove or falsify a worst-case all-input generation-and-replay bound that survives the LSPV-4/506 many-sign-mutation control and arbitrary correct padded deterministic polynomial SAT guests. No universal FLMV contraction or P != NP conclusion is established.
