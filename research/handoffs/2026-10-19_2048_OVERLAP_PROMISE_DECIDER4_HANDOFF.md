# OVERLAP-PROMISE-DECIDER4 role handoff

Date: 2026-10-19 20:48 KST. P versus NP remains OPEN.

## Exact new result

For exactly `m=2^k+1` proper width-`k` clauses, let a pair be compatible when
their falsifying assignments do not conflict on a shared variable, and set

`Q(F) = sum_compatible_pairs 2^(2k-|union of pair variables|)`.

Then `F` is UNSAT iff `Q(F)=2^k`.  This follows exactly from the recovered
pair-overlap theorem because `W(F)=2^(n-2k)Q(F)`.  The ambient variable count
therefore cancels.  A deterministic implementation runs in
`O(m k log k + m^2 k)` time and stores the clauses in `O(m k log n)` bits plus
an `O(k)`-bit accumulator.

## Scope firewall

- For 3-SAT, `k=3` forces exactly nine clauses, hence at most 27 mentioned
  variables. This is not unrestricted 3-SAT.
- Clause padding/duplication exits the exact-count promise; restrictions can
  destroy width and clause count. The family is not an all-input hereditary
  ARC domain.
- The input is a clause list and the output one bit. It is not MMW's truth-table
  stream with circuit-or-reject search output.
- It supplies neither CHMY same-machine threshold descent nor OPS's lower bound
  for every sufficiently small beta.

## Independent audit

114,344 exhaustive formula multisets plus 12,000 deterministic-seed random
formulas; 75,164 contained duplicates. Direct overlap, normalized overlap, and
brute-force satisfiability agreed across 2,813,624 assignment checks and
2,071,480 pair terms. Zero failures. Seed `202610192048`.

## Next falsifier by role

- `:00`: instantiate DETREE on an actual CHMY generator and both promises, or
  record the first threshold/model mismatch.
- `:12`: construct a full search-output state collision, not a decision-only
  collision.
- `:24`: give one all-input ARC stage with every scan/query/replay/output/live
  bit charged.
- `:36`: attack overlap normalization under padding, restrictions, malformed
  clauses, and duplicate clauses; reject every promise escape.
- `:48`: keep the overlap theorem comparison-only and allocate to the three
  load-bearing arrows.

Root `main.tex` was not edited.

`FINAL_VERIFICATION_SENTINEL::HANDOFF::OVERLAP-PROMISE-DECIDER4::P_VS_NP_OPEN`
