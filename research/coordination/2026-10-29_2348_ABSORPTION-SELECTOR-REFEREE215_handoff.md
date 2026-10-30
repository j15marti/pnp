# LSPV-5 handoff: ABSORPTION-SELECTOR-REFEREE215

Status: **PROVED/EXACT** parent-pair theorem; **COMPUTATIONAL** hostile controls; P versus NP **OPEN**.

For proper 3-clauses with exactly one opposite-polarity shared pivot and `s` same-polarity shared tail variables, the direct resolvent is absorbed by the two-parent formula iff `s=0`. Therefore `s>=1` is an exact local selector for parent-level non-absorption. It is not an exact selector for non-absorption by the full formula: on the dense XOR K6 control, it retains 60 candidates while full-formula absorption retains none.

The charged fixed-order UP-DPLL control shows why construction cannot be treated as free. The local selector reduces total work on W1 UNSAT (15,371 to 12,575) and padded-units UNSAT (589 to 521), but increases it on S15 SAT (729 to 2,904) and most easy controls. Exact full-formula absorption costs 903,797 work units on dense XOR K6 versus baseline 911. One uniform beneficial policy is not established.

Next lemma: find a cheap sufficient full-formula non-absorption test, or an amortized selector/controller whose charged total work improves on matched infinite SAT and UNSAT families without receiving the answer class and without per-candidate UP-probe explosion.

Artifacts: report, reproducer, compact summary, raw manifest/chunks. Coordination remains issue #3.
