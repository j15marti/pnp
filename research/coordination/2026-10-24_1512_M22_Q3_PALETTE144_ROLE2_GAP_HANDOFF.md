# LSPV-2 -> all five roles: M22-Q3-PALETTE-FIREWALL144 (2026-10-24)

**Research status:** PROVED/EXACT within the displayed canonical M22 q=3 source and infinite padded family; independent review pending. Six-variable census COMPUTATIONAL. **ARC-EDGE-90 OPEN, DIRECT-POST OPEN, P versus NP OPEN.** User's five existing schedules and agent task counts are unchanged; no third-party communications.

## What changed

The predecessor Q2-FOURCOLOR140 proved ANY positive-primal proper four-coloring can be paired into a NAE witness when q=2. **That property is false for q=3**, even within valid non-fully-paired canonical sources.

Exact signed supports on original variables 1..6:
- P positive = {123,124,356,456}.
- Q negative = {123,145,256,346}; one partial complement support 123, q=3, each variable degree (2,2), k=6, m=8.
- Proper positive-primal four-colors c=(0,1,2,2,0,1) are lex-first, yet pairing 01|23 makes negative clause 256 all one bit, 02|13 makes 145 all one bit, and 03|12 makes 346 all one bit.
- Original source SAT witness 001100, NAE witness 001110. Alternate source-aware coloring (0,1,2,2,0,3) with 03|12 does succeed, NAE witness 011100.

For every h>=0, append h DISJOINT fully complementary-paired copies with P=Q={123,124,356,456} on fresh names; **C_star includes partial pairs**. All F_h stay in-target with k=6(h+1), m=8(h+1), q=3, repeated NAE witness 001110; lex-first coloring repeats the defective 6-color sequence and still has all three pair failures. This is an UNBOUNDED *easy* family. No connectedness, hardness, minimal UNSAT or pair-free assumptions.

**Finite exhaustive reproduction:** 75 possible simple degree-two positive support sets of size 4 on six variables; 75^2=5,625 ordered (P,Q), independent 64-assignment search. q histogram 0:75,2:1260,3:1680,4:2610; **600 / 1680 q3 pairs defeat the first-coloring three-pair test**, 1080 pass, and all 1680 are NAE-satisfiable. All 5625 six-var supports have NAE witnesses. h=0..5 lift checks pass; bit lengths 107,254,449,593,737,1028 in the declared fixed-width code. No arbitrary-N inference from the census.

## Verified peer-accessible artifacts and persistent proofs

- LaTeX body: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1512_LSPV-2_M22_Q3_PALETTE_FIREWALL144.tex (Git blob 6b13f437950bd9de2703937b69dabeaf96059237).
- Python: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1512_M22_Q3_PALETTE144_repro.py (blob 328406acde54fd00d6b8435d0b7841237243c8dc, SHA256 e8e37dc3be53daab506a23069f5096e85f1dcd98d1b54f8202731d1802b5896d).
- Raw JSON: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1512_M22_Q3_PALETTE144_results.json (blob 26f7e96bb7b6ce9f61a26bbe16b3eff7aac08ce4).
- Cumulative role ledger: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1512_M22_Q3_PALETTE144_COVERAGE_HANDOFF.md (blob 974b1e4b00eb764b67d90eb66c345abb5b2aabb9).

Raw and Python bytes match independently executed local evidence by exact Git blob readback. No physically instrumented FLMV machine traces, temporal complete-state flip totals or cumulative bit-time measurements are claimed.

## Gap compatibility and resource accounting

At one adaptive checkpoint use T_A(F)=C_A(F,R)+T_finish,A(F,R) with actual paid prior work and actual future work. A uniform solver must charge graph construction, all three failed partitions, recomputation or recoloring, source validation, source traffic, addressing, memory writes even unchanged, result checking, caches and exact fallback. One single decision bit is not free. The new color technique emits no SAT children, and **does not prove either recursive level of ARC**. If exhaustive independent 2^k fallback is elected, Psi=2^k and R_search=0, an OPTIONAL accounting upper bound only, not a lower bound or a necessary algorithm. Peak writable bit space must cooccur with charged time in the same machine, not in independently optimized implementations. SAT/UNSAT measures can change with state without label oracle.

E remains jointly achievable simultaneous resource pairs of one exact total all-ordinary-input uniform SAT machine in FLMV read-only-input indexed random-access model. OPEN sufficient route: cofinally many achievable integer diagonals -> finite charged all-input route -> **strict** t<241/200 and s<11642479/23232400. Historical t+s<2cos(pi/7) universal landing RETIRED. A C_star-only shortcut cannot be directly inserted into ordinary-SAT E. DIRECT-POST still needs a post-scan, independently large complete-state potential with bounded decrease for EVERY legal adaptive transition. Source-only hitting tau<=N is not sufficient. Worst-case P!=NP remains OPEN.

## Source recovery and handoff requests

This run read full main13, current governance and original Q2-FOURCOLOR140; latest peer Roles 1/3/4/5: CONNECTED-CYCLIC-LIFT139, MAXDEFECT-FACTOR101, NEUTRAL-PORT100, LOCAL-CHAIN140. Recovered original CROSS-TRACK SORTCONSISTENCY31 and MODELBRIDGE-0013: structured source bit/local occurrence arithmetic known, raw rank barrier only raw stream, and FLMV ordinary-SAT -> tagged monotone-(3,3) first leg still OPEN. Drive FRONTIER21 and HUB-JOIN1 contain restricted exact interfaces, ARC-UNANNOTATED-JOIN22 doc returns ZERO characters. HEREDITARY-SCOPED10 original source is still a transient unpublished local artifact in the continuity log, not reusable peer source. GitHub searches bounded; earlier 3532 SHA keyword survey not full math review. Drive LOG/PROVED_EXACT pagination not exhausted; folder BOOL/SIL/Manuscript and main2-main12 mathematical bodies largely unread. See role ledger for paths, statuses and next unread queue.

Roles 1 and 3: test q3 source-aware recoloring with both labels and compare connected easy max-q controls, do not assume any chosen fourcolor works. Role 4: neutral-port and enforcer do not imply target-valid strict child shrink or exact parent decision; test two levels. Role 5: independently audit exact small witness and 600-case census, preserve ARC OPEN. Role 2: search genuine all-input hierarchical contraction or explicit existential edge, with ordinary serialized children, paid gluing, SAT/UNSAT and same-machine storage; inspect inaccessible hereditary executable or construct a genuinely different candidate.

**No schedules or task allocations changed.**
