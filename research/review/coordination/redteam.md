# REDTEAM audit, current run 2026-10-11

## RT-0014 — child-only fanout detection (2026-10-11T16:36:00Z)

**Status:** VERIFIED and published. **P versus NP remains OPEN.**

`FORWARD-FANOUT-DETECTION1` is **PROVED/EXACT** in the declared acyclic child-oracle model. With one target and `n` possible later parents, deciding zero fanout, outputting the complete parent set, or certifying fanout at most fixed Delta requires exactly `n` deterministic child queries. The proof is an indistinguishable-completion adversary.

This retires `CHILD-LOCALITY-IMPLIES-FANOUT-CERT1` only as an unqualified interface implication. TESTS-0009's parent-owned clause construction remains valid and avoids reverse enumeration. `JMV-FORWARD-FANOUT1` remains source-specific and OPEN.

The audit executed 376,370 exact vector/order cases through `n=12`, falsified all 2,664 capped shortcuts, and retained Horn, 2SAT, affine/Tseitin, bounded-treewidth, independent-product, padding, redundant-clause, alternate-encoding, and wrapper controls.

No arbitrary-SAT transfer follows. The result is polynomial, relativizing, and compatible with SAT in P. The next exact task is to unfold the JMV labels and separate forward child locality from target-owned reverse normalization.

Report: `research/review/reports/redteam/2026-10-11_1636_RT-0014.tex`.
