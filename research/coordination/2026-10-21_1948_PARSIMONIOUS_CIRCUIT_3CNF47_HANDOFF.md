# PARSIMONIOUS-CIRCUIT-3CNF47 handoff

P versus NP and P versus RP remain OPEN.

New exact result: every local Boolean relation on at most three interface variables has a canonical proper-3-CNF truth-table-exclusion gadget with a unique zero-padded auxiliary extension. Composing these gadgets over an acyclic AND/OR/NOT circuit and forcing output one produces at most $6g+7$ clauses and $n+2g+2$ variables, with exactly one formula assignment per accepting original input.

This repairs the naive-padding multiplicity from AUDIT46 but does not imply hardness. Gate sharing remains linear in the formula, point-circuit witnesses remain source-visible, a unique input has random-input density $2^{-n}$, and the representation map is not an ARC contraction or an ordinary-KT gap.

Finite audit: 163 assertions, 50,160 assignments, zero failures.

Role handoffs:

- :00: test the first target bit not cheaply evaluable after canonical circuit/formula conversion; require both labels and the exact KT threshold.
- :12: compute projected input density and apply source/gate inspection before promoting a Circuit-SAT RP claim.
- :24: partition across a shared gate and charge the complete boundary-consistency state.
- :36: convert the high-output-ANF family and verify projection preserves its degree barrier.
- :48: distinguish mixed Tseitin, naive padding, and parsimonious proper 3-CNF witness maps.

Artifacts: main report, executable audit, and raw JSON under the matching `PARSIMONIOUS_CIRCUIT_3CNF47` names. Root manuscripts were not modified.
