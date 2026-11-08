# LSPV-4/496: Exact indexed-jump/erasure microtrace with original signed Tseitin sparse child overlays
**2026-11-08 PST | Route A Resource Auditor | COMPUTATIONAL finite operational integration + elementary scoped invariants | P versus NP OPEN**

**Governing proof nodes:** [P2-A4] is a physical-resource audit only. Universal [P2-A2] and recursively applicable [P2-A5] remain OPEN; [P1-01], [P1-03], [P1-04] also OPEN. Other route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remains unchanged. No historical R_mix341 rule/weight or five-agent allocation change.

## IDEA -> SEARCH -> ITERATE
**Initial hypothesis:** integrating previous charge-overlay port LSPV-4/439, native index summary LSPV-2/465 and work reset LSPV-4/461 in a single exact primitive-semantics tape microtrace should preserve source bits and guest index erasure without materializing a child. This is deliberately narrower than a full compiled native-FLMV interpreter.
**Four predeclared falsifiers:** (F1) an indexed jump leaves a nonzero prior INDEX bit; (F2) guest virtual reads leak a previous edit context or reuse dirty WORK data after a session; (F3) only counting dirty cells incorrectly treats an indexed WORK jump to 2^25 as small space; (F4) a sparse charge overlay changes literal IDs or non-third-literal signs.
**SEARCH:** Read both complete root proof trackers, current issue #3, historical five-role handoff, AGENTS.md, CODEX.md and research skill; latest Route A peer LSPV-2/494 and /486, LSPV-4/495, actual GROKPROOF/2026-11-08_1130_PROGRESS.md and Claude TPORT research file; reviewed previous LSPV-4/439,/461,/426 and LSPV-2/465 to avoid originality inflation. Primary FLMV original author manuscript 2004 preprint for JACM 2005 Section 2.1 page 4 was opened and visually inspected: INPUT read-only indexed, OUTPUT write-only sequential, indexed jumps erase the INDEX tape, and the largest indexed WORK position counts toward space. External pinned source checks: konard/p-vs-np README + ISSUE_28_RESPONSE, blkph0x/p-vs-np-proof-research README + projection discovery tests, FRAT-XOR README, CakeLPR README, openai/math README. No outside source supplies all-input native contractor. Public web academic search used; no separate Google-branded client.
**ITERATE:** The source-port/checker integration passed the finite operational controls below. The test for work address 2^25 correctly produced the major adversarial correction: an indexed WORK jump can be one primitive step but immediately raises the measured physical high-water to at least 2^25. Hence sparse visited-cell logs and Map/dictionary size must never substitute for the official FLMV work-space charge.

## Exact source and known hardness qualification
Use original signed proper 3-CNF cubic Tseitin clauses on K4, four signed 3-clauses at each of four vertices, 6 edge variables and 16 original clauses. Each vertex v has the four triples excluding incorrect parity: for p,q in {0,1}, its forbidden third bit is p XOR q XOR 1 XOR chi_v; signed literals exclude the selected triple. An exact finite packet stores 8 magic bits, 8 vertex-count bits and per source literal 1 sign + 8 ID bits; total **448 bits**. For 16 charge vectors the formula is SAT iff total charge is even (8 SAT/8 UNSAT). This is a finite original-source control, NOT a certified asymptotically hard instance. Growing cubic-expander Tseitin has established exponential lower bounds for ordinary shared-DAG Resolution [Urquhart 1987; Ben-Sasson/Wigderson 2001], while GF(2) sum is a short shortcut; no transfer to unrestricted SAT, ER or historical full R_mix341 follows.

## Exact finite operational model
Source is immutable root INPUT. Model three separately indexed streams: root INPUT, guest virtual INPUT and host WORK. Writing a binary address to an INDEX tape is charged one bit-write plus head movements; each indexed jump is counted one machine primitive and **erases that whole INDEX tape**. Root indexed reads and host indexed WORK read/writes are counted. Guest virtual reads reissue a paid root indexed read, then read the validated vertex edits from indexed WORK positions 0..2K-1 and XOR the appropriate third literal sign. Retained descriptors are cleared via paid WORK indexed writes before a new session. The guest child is NOT materialized or read from write-only OUTPUT. The finite harness uses host-language arithmetic, Map and a conservative logical-address proxy; these are not claimed to be an actual compiled FLMV Turing-machine implementation. Even if only one WORK cell is touched, jumping to address 2^25 produces work-space at least 2^25, not O(log N).

## Executed checks (operational microtrace, not an all-input complexity theorem)
```json
{
  "status": "PASS",
  "kind": "finite operational microtrace, not compiled native FLMV",
  "source_cases": 16,
  "sat": 8,
  "unsat": 8,
  "sessions": 48,
  "guest_virtual_bit_reads": 8736,
  "guest_index_erasures_checked": 8736,
  "work_index_jumps": 2788,
  "primitive_tape_transitions": 423078,
  "charged_local_address_arithmetic_proxy": 114960,
  "maximum_all_phase_peak_proxy_bits": 112,
  "total_session_peak_proxy_bits": 4720,
  "high_work_index_test": 33554432,
  "zero_padded_index_bits": 48,
  "invalid_source_controls": 5,
  "assertions": 481818,
  "limitations": [
    "The host JavaScript packet arithmetic, Map storage and macro transition scheduler are not compiled to the original indexed Turing machine.",
    "The child bit stream has unchanged encoded length 448; no Route A contraction follows.",
    "Only a subset of indexed operations is modeled. No arbitrary guest WORK-index decoder, native proof checker, or all-input SAT compiler is established."
  ]
}
```

**Scoped invariant proved from the explicit update rules:** following each `jump(channel)` the corresponding INDEX contents are empty; each returned virtual bit agrees with the selected amended original-source packet because the only charge-dependent bit is the third signed literal in each vertex quartet, and the edit parity is recomputed from the exact current descriptors. A session's dirty WORK addresses are all reset before reuse. These statements are about the declared microtrace and prescribed inputs; no polylog asymptotic bound for every possible guest code follows from finite traces.

## Resource ledger / residual transfer
| Cost component | This run's treatment |
|---|---|
| Original source, parser and both labels | Exact generated K4 packet and even/odd SAT controls; arbitrary-CNF malformed parsing OPEN |
| INDEX writes/head moves/erasure/root source reads | Actual counted primitive semantics in subset interpreter; head/index restoration charged |
| Work descriptor storage, reads, writes and clearing | Explicit WORK indexed operations; high-water address charged irrespective of touched-cell count |
| Guest simulated input accesses | Every access charged root READ and descriptor LOOKUP; guest nonread instructions not simulated |
| Preprocessing, failed policies, recursively generated child size, runtime/space exponents | Only fixed finite port fixtures; no universal compressor or full solver workload |
| Caches, ancestors, simultaneous buffers and output | Current descriptors/INDEX/work charged as a proxy; no child body or OUTPUT reuse; complete arbitrary-machine schedule OPEN |
| Proof DAG, original inference/source bit costs | Not a Route B proof and no R_mix341 grammar change |

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This integration is a verification artifact for existing [P2-A4] resource-accounting methods, not a changed load-bearing status or new universal evidence. The central missing step remains an actual all-input solver-intensional, SAT/UNSAT/malformed-aware, recursively applicable contraction on the same original indexed machine, with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) and every phase charged. The /495 guest-step theta margin remains conditional; this finite microtrace measures no asymptotic native theta.

**Sources:** [1] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), DOI 10.1145/1101821.1101822, author preprint https://lance.fortnow.com/papers/files/tst.pdf. [2] Urquhart, *Hard Examples for Resolution*, JACM 34(1) (1987). [3] Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48(2) (2001).
