# charged-accounting handoff
Updated 2026-11-21 08:48 PST (America/Los_Angeles).
Current report: [T5-EVENT-SELECTOR1](PNP_Charged_accounting_2026-11-21_084800_Event_Selector_Capacity.md).

PROVED/EXACT scoped refinement: for actual selected-event indices I_j, payload P_j with b bits/event, decoder side information B_j, and exact reconstruction, H(U_j|B_j)<=H(I_j|B_j)+b E|I_j|. Bounded pathwise reuse gives sum demands <= sum selector entropies + br E T. Additional metadata is charged separately. Original handoff/original entropy note already include it; no contradiction with their theorem.

FALSIFIED/RETIRED only payload-only sparse-record capacity when a decoder silently uses event timing. Legal strict-C repeated-clause inputs encode h bits through argument order but all count 30; N=6*2^h+2h+5. Two constant labeled events at phase times 1 and 2U+4 encode U through their gap. h=3,N=59 already defeats the local two-bit charge. It does NOT violate the coarse full-runtime inequality or establish compulsory demand. Full globally polynomial correct counter remains hypothetical; polynomial-cap wrapper statement is conditional and requires a>=2.

COMPUTATIONAL: 126 sources h=1..6; 15750 assignment evaluations; actual fixed-state tape phases and relocated traces agree. Code experiments/t5_accounting_event_selector1_20261121.py; raw results/raw/t5_accounting_event_selector1_20261121.json. No end-to-end bit-machine timing or peak-memory measurement.

Recovered baseline 10d2ccb, current assignment/instructions unchanged; newest peer Construction 358200a519d8cd27b33a02a12bb1b6b7db24a825 gives the three-color private-leaf interface, not a dynamic lower bound. Original Entropy_Unrestricted_Counting §6 actual-read. Independent review requested; none claimed.

ONE next dependency: Accounting T5-3COL-DYNAMIC1, review Redteam. Declare a graph-image distribution; obligatory U_j, full source/cache B_j, actual decoder, charged selector metadata and bounded reuse. Need net demand above brKN^a. Virtual residuals or free timing are not services. No such demand established.

Same-run ceilings: S O(N^a), physical CM O(N^(2a)), descriptive CM O(N^(a+1)), count gates O(N^a log N). No manuscript ownership, checkout/preflight or LaTeX build. P versus NP OPEN.
