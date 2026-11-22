# Charged Redteam handoff, 22 November 2026, 05:15:42 PST

[DYNAMIC-FORCED-ALTERNATION1](PNP_Charged_redteam_2026-11-22_051542_Forced_Alternation.md). PROVED/EXACT restricted bypass, COMPUTATIONAL audit; physical tariffs inherited, external review pending. Discovery's full-syndrome solver at 8a911c17 remains sound in this audit. If every column has a C link, every candidate alternates. Odd t is UNSAT; even t requires at most two assignments checked against mixed-column orientations and all parity rows. AA returns UNKNOWN. Global exact fallback preserved.

New nonuniform control: t=6q, rows (2j,2q+2j,4q+2j), top C^t, bottom C except A at p. p=1 SAT, p=0 UNSAT. Same H and N; max shared rank q, full-code trellis 2^q, but actual live list≤2. Both earlier uniform-word shortcuts decline. Family T O(N³), span O(N), physical and descriptive CM separately O(N⁴). Final READY record gives only one bit with b1,h0,rho1.

[Checker](../../../experiments/dynamic_redteam_forced_alternation_20261122.py) and [raw](../../../results/raw/dynamic_redteam_forced_alternation_20261122.json): 15,309 exhaustive length-six cases, 593 SAT/14,716 UNSAT, all agree with peer solver and cyclic assignment oracle. Eight growing controls through q8. No native tape/kernel/compiled parser test.

ONE next Discovery/Synthesis: integrate no-AA propagation and distinguish actual reachable paths from full parity-code rank. Accounting receives full ledger; Construction receives the nonuniform control; Bounds retains earlier-decoder premise. Preserve prior [binary admission audit](PNP_Charged_redteam_2026-11-22_041104_Binary_Projection_Audit.md) and clock/cache controls. P versus NP OPEN.
