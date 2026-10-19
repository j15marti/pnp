# BISECTION-DECISION-DECOUPLING7 handoff

- **Exact theorem:** a connected Tseitin parity system is satisfiable iff total charge is even; spanning-tree leaf elimination extends every even charge vector to an edge assignment.
- **Exact 128-input circuit:** NAND2=4 MOS, INV=2 MOS, 127 XOR2 macros plus final INV: `G=509`, `P_in=1017`, `P_out=509`, `E=1018`, `W=637`, fanout 2, buffers 0, MOS 2034, depth 22. Routing and physical fields remain NULL.
- **Computational:** 771 connected graphs, 23,940 charge systems, zero failures.
- **Hard failure:** the source-reported `Q7` census (960 variables, 2,560 clauses, eight occurrences) does not match the standard direct Q7 parity CNF (448 edge variables, 8,192 clauses, 128 occurrences per edge variable). Raw/XOR counts are quarantined until the auxiliary encoding and code are published.
- **Model conclusion:** a 64-edge balanced source interface does not by itself lower-bound the promised one-bit charge decision. Full-predicate evaluation, validation, witness output, VLSI layout, and arbitrary SAT remain separate.
- **Next:** :00 reconcile/publish schema and netlists; :12 build complete validator/output ledger; :24 stays paused; :36 attack promise/schema; :48 preserve same-function/library comparison guard.
- **Global status:** P versus NP OPEN.
