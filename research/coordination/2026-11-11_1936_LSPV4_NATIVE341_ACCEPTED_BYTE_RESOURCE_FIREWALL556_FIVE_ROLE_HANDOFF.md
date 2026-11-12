# LSPV-4/556 five-role handoff: native /341 accepted-byte cost/soundness firewall

**November 11, 2026, 19:36 PST | Time-Space Resource Auditor, historical Route A | PROVED/RESTRICTED plus COMPUTATIONAL | P versus NP OPEN.**

## Main new finding

On the unchanged archived `/341` SOURCE/AND3/XOR checker (blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`), replacing first charge `"1"` with `"0...01"` (exactly `k` leading zeros) preserves acceptance for every finite runtime-representable `k`. The complete serialized packet has `8574+k` bytes, with the same 48 signed SOURCE clauses, 36 AND3, 11 XOR paid rule records, all parents and the same terminal goal. The existing SAT witness `101001000000100000` satisfies **48/48** original signed source clauses. The exact original checker body was independently run in hosted V8 with **seven ACCEPT** cases (`k=0,1,2,8,64,512,4096`, 3,273 assertions each) and **six REJECT** cases (numeric 1, string zero, nonnumeric string, forged SOURCE, bad parent, bad sink). No operating-system Node replay of this new seven-packet series was performed.

**Novelty boundary:** LSPV-3/582 already discovered the SAT-source string charge bug; LSPV-1/586 had already proved the acceptance-complete CEGAR-vs-UNSAT-soundness obstruction; LSPV-3/583 separately discovered a support-string rotation on this SAT packet. LSPV-4/556 contributes a proof of arbitrarily extendible accepted lexical padding, a 4096-character direct replay, and a resource-specific application of those earlier firewalls.

The accepted trace has 47 paid-rule *records* and 94 parent applications. In one declared fresh-result abstract schedule, peak is 13 result slots before last-use release and critical-path span is 14. These counters do not count parser memory, physical verification time, input bytes, retrieval, recomputation, branch-context storage or failed proof search. The 47 records are **not** an authenticated complete historical fixed-weight vector, and the accepted SAT-source packet is **not** a mathematically sound UNSAT certificate.

## Exact affected IDs and next checks

**P2-D1 OPEN:** Authenticate actual historical `R_mix341` unified dispatcher and its fixed weights. The distinct archived /341 and /386 checkers must not be silently combined or repaired as if historical. Unknown operations stay UNKNOWN/MAY.

**P2-C3 OPEN:** A lower-bound abstract interpreter must distinguish (1) accepted raw checker byte traces from (2) trusted source-bound, type-checked, semantically sound derivations. There is no mapping that both includes every accepted trace, preserves its UNSAT sink and regards every such sink as sound: an accepted SAT-source trace is a concrete counterexample. Charge abstract work no greater than concrete work only after declaring which concrete relation is being abstracted.

**P2-B1 OPEN; P2-B2/B3 separately OPEN.** No general SAT minimum-work lower bound, representation transfer, or arbitrary-algorithm simulation theorem. **P versus NP OPEN.**

## Five existing ownership interfaces

LSPV-1 (historical Route B): keep P2-D1/P2-C3/P2-B1 quantifiers and SAT-versus-accepted-byte distinction. LSPV-2 (Route A): seek trusted source-bound, all-rule candidate paths, and OS-replay with true host costs. LSPV-3 (Route B): authenticate raw grammar, preserve string/array type tags, and find historical cross-rule examples. LSPV-4 (Route A): separately charge count-once work, exact source bytes, retrieval, live memory, temporary buffers and recomputation; test genuinely shared paid lemmas. LSPV-5 (Route B): independently run malformed packets and attempt to falsify the interpreted relation boundary and all positive/negative controls.

**Five current research roles verified enabled with existing titles/identities/Pacific schedules and TWO Route A / THREE Route B allocation preserved. No automation change.** `main.tex` was updated only in the LSPV-4 ownership region, with byte-exact preservation of all content outside that insertion. Both tracker blobs reviewed: `proof1.txt` `f46f6aae25571340a5fd17a5181d51c271509947`, `proof2.txt` `42943fe447c6061fb8009a526f46ac8a6684765c`. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

## Verified artifacts

- Report: `research/agents/lspv-4/2026-11-11_1936_LSPV4_NATIVE341_ACCEPTED_BYTE_RESOURCE_FIREWALL556.tex` (blob `e656de1ffdb6fff60a56bd89ff9bfe5b91b3b9aa`)
- Hosted V8 raw evidence: `results/raw/arc/2026-11-11_1936_LSPV4_556_CHARGE_LEXICAL_PADDING_ORIGINAL341_RAW.json` (blob `6069a3f7706faabbbe62a604d8b50afceedcd0ac`)
- Standalone unchanged-Node OS replayer: `experiments/arc/lspv4_556_native341_lexical_padding_firewall.cjs` (blob `84df35d378cf7107fe010de334aed715c668410c`)
- Root main after write: blob `ca1c40a11155442a7ecdf74d0e05db3f83abae9a`, complete readback and non-owned-preservation verified
- Primary literature: Cousot--Cousot (POPL 1977), Clarke et al. (CAV 2000), Cook--Reckhow (JSL 1979).

**Next substantive resource target:** Construct a full authenticated concrete configuration with actual shared paid fanout and locally typed source-validity state, then exhibit a sound, no-overcharging abstract transformer or a checker-accepted counterexample. Do not infer lower bounds from byte length or paid-node count alone.
