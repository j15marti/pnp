WIRE-LEDGER1 (2026-10-19): source-checked exact logical connection census, P vs NP OPEN.

Original basis: research/agents/lspv-1/2026-10-19_0616_LSPV-1_REVFIXGATEAUDIT1.tex; research/agents/lspv-1/2026-10-19_0512_LSPV-1_NAEPC2D1.tex; research/agents/proof/2026-10-07_162204_PROOF_COMBINED_REPLAY1.tex; research/agents/proof/2026-10-08_2253_RECOVERY-STRENGTHEN6.tex.

For m>=2 anchored REVFIX has 3m-1 AND, 2m-1 XOR, m equality functional gates, 12m-4 functional input-terminal incidences, and a declared NAND2 realization of 19m-6 gates (38m-12 NAND input pins). The source's proper 3CNF compilation has 27m-9 clauses and therefore 81m-27 literal incidences. Additional variables: 14m-4.

For m>=2 two-shear REVFIX has 3m AND, 2m XOR, m equality gates, 12m input-terminal incidences, a declared 19m NAND2 realization (38m input pins), 27m proper clauses and 81m literal incidences. Additional variables: 14m. The known m=1 semantic defect is excluded.

Proof: two input terminals per AND/XOR/equality; source gate counts and 5/4/4 proper-CNF clauses per AND/XOR/equality; declared NAND2 library AND=2, XOR=4, XNOR=5. This is an upper-bound implementation census, NOT a minimum transistor/net/wire-area bound. CNF literal incidences are syntactic, not physical net counts. Fanout, routing, source-literal wires, buffers, and physical delay are not yet charged.

Finite arithmetic audit: 499 sizes m=2..500, all exact formula checks passed. Local reproducible files: /mnt/data/pnp_wire/WIRE_LEDGER1.md, wire_audit.py, wire_audit_results.json; local paths are not assumed persistent across scheduled runs. This report does not claim that the code or raw results were uploaded to GitHub.

Next: instrument COMBINED-REPLAY1 per source bit read and maximum simultaneous live bits, and synthesize physical fanout/routing for matched NAE and REVFIX circuits. Distinguish input-circuit evaluation cost from arbitrary Circuit-SAT decision. The latter unrestricted bridge is OPEN.