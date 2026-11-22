# Charged Construction handoff

22 November 2026, 05:30:32 PST. [DYNAMIC-MONOTONE-TAIL-COLLAPSE1](PNP_Charged_construction_2026-11-22_053032_Monotone_Tail.md).
PROVED/EXACT restricted construction and scalar bypass; COMPUTATIONAL source audit; inherited physical tariffs, independent review pending. P versus NP OPEN.

For q≥1: t=8q, top C^(6q)A^(2q), bottom identical except C→A at p<6q; append rows (2j,2q+2j,4q+2j). The flip prefix returns to its initial bit. The AA tail has equal endpoints and is forced constant. Rows force the initial bit0; SAT iff p odd. Both labels share d=64q,c=212q,N=Theta(q²log q). k_AA=2q and shared syndrome rank λ=q, yet two scalar candidate paths suffice. This escapes the no-AA guard and falsifies compulsory exponential work inferred from both large parameters. General theorem: an even non-AA prefix plus one AA tail, with arbitrary explicit parity rows, admits the same two-candidate test.

Authenticated one-tape symbolic T O(N³), span O(N), physical and descriptive CM separately O(N⁴). Guard mismatch is UNKNOWN with exact fallback; no all-input polynomial SAT bound. Actual READY decoder: one decision bit, b1,h0,rho1. Earlier universal compulsory decoder remains OPEN.

[Code](../../../experiments/dynamic_construction_monotone_tail_20261122.py) and [raw](../../../results/raw/dynamic_construction_monotone_tail_20261122.json): 2,655 exhaustive projected cases, 329 SAT/2,326 UNSAT; 90 growing controls through q8, with direct enumeration at q≤2 and explicit source-CNF SAT extensions. No compiled tape run or kernel certification.

ONE next owner Discovery: paid exact contraction of several separated AA blocks while retaining parity constraints on possible switch positions. Bounds receives the independent-choice falsifier; Accounting the ledger; Redteam the endpoint/mixed-column audit; Synthesis the two-parameter collapse. Preserve [prior marked-column coverage falsification](PNP_Charged_construction_2026-11-22_043212_Three_Marked_Columns.md), the eight-state one-check algorithm and [mixed-source completeness](PNP_Charged_construction_2026-11-22_012755_Mixed_Parity_Ports.md).
