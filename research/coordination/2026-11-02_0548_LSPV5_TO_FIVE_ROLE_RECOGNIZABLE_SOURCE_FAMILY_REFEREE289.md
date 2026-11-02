# LSPV-5 handoff: RECOGNIZABLE-SOURCE-FAMILY-BYPASS-REFEREE289

2 November 2026, 05:48 PST. **P versus NP remains OPEN.** No task identity,
title, enabled state, Pacific schedule, role ownership, or prior verified lemma
changed.

## Exact red-team result

**PROVED/EXACT recognizable-family bypass; independently COMPUTATIONAL.** Let
`U198` be the authenticated canonical UNSAT original, `V198` its authenticated
canonical SAT occurrence-swap source, and `Z6` the canonical six-variable SAT
block. In the declared block serialization,

- `R_t^- = U198 AND Z6^t` is UNSAT;
- `R_t^+ = V198 AND Z6^t` is SAT;
- both are valid duplicate-free proper monotone 3-SAT-(2,2) originals with
  `n=198+6t`, `m=264+8t`.

A strict streaming source-template recognizer decides this unbounded both-label
family in linear source comparisons and logarithmic counters before compiling
`C_F`, PG/Tseitin, OBDD, Shannon/cofactor DAG, semantic cache, continuation
equivalence, or assignment-recovery keys. Composed with any exact fallback it
is a correct all-input decider. Thus none of those representations is
**necessary work on every canonical input**. This does **not** refute a
worst-case lower bound on other inputs and does not prove polynomial SAT.

## Independent controls

- Replayed all 64 U198 boundary rows and 152 module calls.
- Checked the 198-bit V198 witness against all 264 source clauses.
- Built and recognized both labels for `t=0..4`; ten canonical sources.
- Reproduced F9: 70 models; all 512 source/circuit rows; 35 gates, depth 6;
  best/natural/worst OBDD 52/66/80; same-original pins SAT2/UNSAT0 with eight
  complete original-clause falsification leaves.
- No-producer-import verifier passed 36,201 counted checks. Malformed controls
  reject; valid nonfamily inputs fall through without a guessed label.

The restricted private forward circuit on the recognized family would contain
`3m-1 = 791+24t` gates, but the recognizer constructs zero. The after-answer
constant 0/1 circuit is not used.

## Charged recurrence and limits

`T_D = T_parse + T_recognize + (recognized ? T_output : T_fallback + all guest/access/output work)`.
Every source/index/head read, failed comparison, parser record, output bit and
simultaneous peak is charged. No guest launches on members. A materializing
Python parser pays `O(N)` host memory; the abstract streaming recognizer's
`O(log n)` counter bound is separately stated. Constructive witness/proof
emission is charged if requested; decision-only output needs neither.

The exact remaining gap is unchanged: no polynomial-total-work all-input
solver, no representation-independent superpolynomial lower bound, no
arbitrary-`A` power-short `Phi(A)`, and no strict same-machine numerical FLMV
transfer. The prior d=4 exact source fallback remains exponential. The recent
OpenAI counting preprint remains conditional and is not used.

Artifacts: [formal report](../main/2026-11-02_0548_MAIN_RECOGNIZABLE-SOURCE-FAMILY-BYPASS-REFEREE289.tex),
[producer](../../experiments/arc/lspv5_289/recognizable_source_family_referee289.py),
[independent verifier](../../experiments/arc/lspv5_289/verify_recognizable_source_family_referee289.py),
[raw](../../results/raw/arc/2026-11-02_0548_LSPV5_RECOGNIZABLE_SOURCE_FAMILY_REFEREE289_raw.json),
[verification](../../results/raw/arc/2026-11-02_0548_LSPV5_RECOGNIZABLE_SOURCE_FAMILY_REFEREE289_verify.json).
