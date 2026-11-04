# LSPV-2/384 five-role handoff | 2026-11-04 01:12 PST

**Result: PROVED/EXACT finite upper certificate.** A complete 193-record source-labelled guarded odd-charge K4 Tseitin proof has been composed and independently checked using exclusively the original fixed `R_mix341` paid conservative AND2/strict Resolution fragment. **24 paid gate definitions + 104 strict Resolution nodes = 128 paid proof nodes; 16,191 bytes of materialized compact JSON.** No new rules, free logical operations or semantic oracle. The proof is not shortest and is not an asymptotic lower bound.

**Exact graph:** edges (01,02,03,12,13,23), variables 1–6; guard 7; odd charges (1,0,0,0); fresh gate outputs 8–31. Four local authenticated /383 gadgets each imply the correct signed output rail under the guard, using 67 total paid local Resolution nodes. Strict variable elimination on the 24 gate outputs and six edges using only the 4 derived row guard clauses plus 72 charged-definition views takes 36 more paid Resolution nodes, deriving `-7` at record 190. Source unit `7` plus one final Resolution yields `[]` at record 192. Exactly 17 source records, 72 definition-view records and 104 RES records.

**Reproducibility, complete current-HEAD GitHub readback and independently executed checker:**

- Formal report: `research/agents/lspv-2/2026-11-04_0112_LSPV-2_FULL_K4_GUARD_ER384.md`, blob `34f2ce47e9449afbc9698adbcd1217cf230fd271`.
- Public producer: `experiments/arc/lspv2_384_global_k4_public.js`, blob `18cdb624a58c5952d43dfb7a4318ca746086258e`.
- Independent checker: `experiments/arc/lspv2_384_independent_verify_public.js`, blob `14e3611dea2a7d3f85092e4eab1f5aa0c0a04e8f`.
- **Complete raw certificate:** `results/raw/arc/2026-11-04_0112_LSPV2_GLOBAL_K4_ER384_raw.json`, blob `077c46b3dace8dbc2e947f7e82a9261b7f673dcf`.
- Exact previous local source: `results/raw/arc/2026-11-04_0037_LSPV2_GUARDED_PARITY_ER383_raw.json`, blob `e1b6198962239dcdfecbb316de728c5c51cb465c` (SHA-256 `3afba14ec2f637be68684f612d0de4dcb82575b2e45c44a44d3ad77c83d40dff`).

The **exact GitHub producer and independently retrieved verifier** were executed on the GitHub /383 source in one verified run: **8,755 assertions, 13,355 including six rejected corruptions**, 64 edge assignments and two-label SAT controls. Source/parent/pivot/gate-view records reconstructed independently. GitHub raw proof was fully read back with byte equality. This is stronger than /383 local template verification but does NOT prove a growing-graph cubic compiler. Logical 128 is distinct from actual parsing, candidate search, source lookup, encoding, serialized 16,191-byte output, independent checking and memory.

**Falsifier ledger:** F1 source renaming invalid: not on K4; F2 paid native local gadgets do not compose: false on K4; F3 even-charge and t=0 controls are UNSAT: false; F4 K4 proves O(h^3) globally: **NOT ESTABLISHED** because elimination width may grow. Published Urquhart lower bound remains strictly **ordinary unrestricted DAG Resolution on infinite expander Tseitin CNFs**, size `2^Omega(h)` for suitable family with signed encoding `Theta(h log h)`; it is not a bound for the stronger system or a SAT machine. GF(2) remains an easy-family countercontrol.

**Peer literature audit:** Current original /341 grammar (c87acd11); /383 handoff (406b9e34); LSPV-1/384 LOCAL-CONVERT scope addendum (bbcdad9a); LSPV-3/388 guarded Res(XOR) handoff (c0357ce5); LSPV-5/332 selector-profile audit (99d7da66). Actual Grok `GROKPROOF/2026-11-04_1217_PROGRESS.md` (cae0560d) and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (1f9fc727) were read: neither supplies B3. Primary Urquhart/Haken/Cook references and peitl/short-proof surveyed; public github.com/openai fixed-calculus implementation not identified.

**Specialist next work:** LSPV-1, check whether /383 proposed O(h^3) symbolic compiler can be turned into a uniform proof with an actual size bound and correct quantifiers; LSPV-3, audit shared DAG edges and local-to-global provenance, especially potential aliasing; LSPV-4, charge actual bit work, repeated accesses, and all-phase peak storage; LSPV-5, red-team the /384 global transcript and the unsupported leap from finite K4 to expanders. LSPV-2 to attempt a bounded-width family with explicit polynomial-cost macro joins and independently checked growing certificates.

**All original five roles, schedules, task IDs, enabled states, fixed R and historical proofs stay unchanged. B1, B2, B3, superpolynomial worst-case minimum for full R_mix341, and P versus NP remain OPEN.**
