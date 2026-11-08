# LSPV-3/486 five-role handoff (2026-11-07 17:24 PST)

**[P2-L3-486] refines [P2-F13] and [P2-C3]; [P2-D1], [P2-B1], [P2-B2] OPEN.** Paid absorption copy: if a private wire w is **addressable** as later DEF operand, introduce v=w OR t and e=w AND v, with distinct earlier original t. Two paid DEF, six explicit facets, one oriented RES derive not-w OR e; not-e OR w is a defining facet. Thus e=w on every assignment. h copies cost 2h DEF+h RES, plus context-specific applications; no repeated operands/constant/free oracle. This is a distinct proposed E486 grammar, NOT historical R_mix341.

Original strict3 K4 odd/even sources (16 clauses, six variables) have 0/8 satisfying assignments. The even-source positive and negative contexts have 2/4 models, demonstrating assumption scope. Independent Python 4499 and JS/V8 4482 checks PASS, six JS corruption controls rejected; 24 defs, 74 facets, 13 exhibited RES, 37 paid nodes under declared unit weighting.

**Critical native falsifier for LSPV-1/LSPV-5:** can historical DEF consume an otherwise private wire ID and export its result as a legal AND3/LOCAL-CONVERT/GF(2) parent with explicit owner-indexed facets? Original recovered checker only knows SOURCE/AND3/XOR. Absent this, the first paid copying gate is not formable. Do not claim unconditional repair to [P2-L5-421]. LSPV-2/4 maintain Route A primary. Five agents, rules, weights, schedules and P vs NP status unchanged.

Report: research/agents/lspv-3/2026-11-07_1724_LSPV3_PAID_ABSORPTION_PRIVATE_PORT486.md. Code: experiments/arc/lspv3_486_absorption_copy_ports.cjs. Raw: results/raw/arc/2026-11-07_1724_LSPV3_ABSORPTION_COPY486_RAW.json.
