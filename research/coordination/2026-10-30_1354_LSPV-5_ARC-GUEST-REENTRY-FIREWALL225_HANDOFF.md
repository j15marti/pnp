# LSPV-5 handoff: ARC-GUEST-REENTRY-FIREWALL225

30 October 2026, 13:54 America/Los_Angeles. P versus NP remains **OPEN**. No task identity, enabled/paused state, schedule, role ownership, or team count changed.

## One exact restricted falsifier

**PROVED/EXACT, restricted arbitrary-guest simulation theorem.** Let `B` be any total exact SAT decider. A fixed correct wrapper finds input length `m`, jumps its read-only input head to `m+1`, moves left twice and records the symbol at `m-1`, then jumps directly to `m-1` and records it again. It returns `B` when the symbols agree and the complement otherwise. On every physical nonempty input the symbols agree, so the wrapper is correct on both SAT and UNSAT.

A simulator that handles the far jump by a sticky out-of-bounds state and returns blank after later ordinary moves until another indexed jump is incorrect: it loses the two left moves, compares blank with the actual last bit, and reverses `B` when that bit is 1. Therefore exact child length and a far-address guard are necessary but not sufficient; the complete simulator must reproduce ordinary input-head motion and boundary re-entry, index erasure, all guest tapes and blank semantics inside the charged access tariff. This is not a lower bound on SAT algorithms and does not contradict FLMV's complete on-demand Cook encoding.

## Finite controls

One fixed identity emitter/wrapper was checked on a proper-3CNF SAT source and the proper-3CNF UNSAT source containing all eight sign patterns. Physical/exact re-entry returned both exhaustive labels; sticky OOB and a valid-domain-only wraparound accessor reversed both. The audit passed 7,990 address-shadow membership checks and 7,990 erasure resets. These are logical controls, not native FLMV timing.

## Corpus reconciliation

Actual FLMV Sections 2.1 and 3.1/Theorem 3.4 were read. LSPV-4 ARC-MATERIALIZE-GUARD253 already proved the far indexed-jump/work-tape firewall and explicitly left ordinary moves open; this run does not duplicate that result. Current peer synthesis retained: LSPV-1 ONEHOT-CHILD-SELECT253 is a restricted probe floor with full-scan/cache escape; LSPV-2 VIRTUAL-SORT-ACCESS254 has direct intermediate indexed access but expands physically; LSPV-3 ADDITIVE-MULTIPLICATIVE-GATE257 separates scan and per-step access tariffs; LSPV-4 ARC-JOINT-SLOPE-FRONTIER255 gives conditional strict margins, not a constructor. AFFINE-SMALLBIAS-DESCENT-GATE2 remains restricted input-independent affine MCSP semantics.

Primary sources: Fortnow--Lipton--van Melkebeek--Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, <https://lance.fortnow.com/papers/files/tst.pdf>; Seiferas--Vitányi, *Counting Is Easy*, JACM 1988, DOI 10.1145/48014.63141. The latter is a candidate component for head-distance tracking, not a completed model transfer.

## Verified publication provenance

- Report: `research/main/2026-10-30_1354_MAIN_ARC-GUEST-REENTRY-FIREWALL225.tex`, create commit `001553fb217dc1751a7eacb6bad44be4f8e537f9`, blob `43083e34610a3b6529604bb5be652ea064067dd5`, sentinel readback verified.
- Code: `experiments/arc/2026-10-30_1348_guarded_virtual_input_audit.py`, create commit `86b10fe70ef5f8072d3603537df63cae80719c78`, blob `f119b694035b6585567833dd716686e740290a08`, SHA-256 `2753bde3e80be75990aef499e97ad4348ccf8c7c2fa74f534dc657f69cf556a0`, readback verified.
- Raw results: `results/raw/arc/2026-10-30_1348_guarded_virtual_input_audit.json`, create commit `d3d4c47aebfca0ac80b42a407197f780f9b9ac97`, blob `ae68f8fe0f8631b5522bafd184018623c118783c`, SHA-256 `d87ccda2c538516032bfefe8d948da3737e6d5b0dca4ba84d28771bc5d88dbdb`, readback verified.
- Root reconciliation: commit `b24d3cff46e5182d8e1d8b6171529267c452ce20`, blob `2ad4d7d5eb9a2ec3a2b0e816dfeaf3375209a53b`; current header/sentinel, explicit OPEN status, and one balanced marker pair for every LSPV role read back and verified.

## Next single target

Construct or falsify an exponent-oblivious complete input-head transducer in the FLMV indexed model: arbitrary binary indexed jumps, index erasure, ordinary moves, exact blank/re-entry semantics and all guest tapes must cost only polylogarithmic time per guest step plus logarithmic or already charged guest space. Only then compose it with a separately proved both-label physical power-short hereditary ordinary-SAT child emitter.
