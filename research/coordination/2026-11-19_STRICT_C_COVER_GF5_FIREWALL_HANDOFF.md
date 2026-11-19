# Strict-C obstruction cover handoff | 2026-11-19

**Role:** fresh independent global source-verifiable obstruction covers.

**PROVED:** Exact global block cover is W(z)=product_j E_j(z)=0 for every shared assignment, where E_j(z) is the *existential* private-block support. An exact GF5 support projector uses Boolean OR as 1-product_x(1-T_j), not sum_x T_j.

**FALSIFIED (connected strict-C local block):** C(z,a,b) AND C(z,a,c) has ten satisfying private extensions for every fixed z, but sum of extension indicators in F5 is zero for every z. Free D5 action implies all nonempty strict-C full witness counts divisible by ten; even D5 orbit counts can vanish mod 5 on SAT.

**PROVED source-indexed global UNSAT templates:** primal K6 yields six variables/15 source clauses/pigeonhole; four-clause type1 C(a,b,e),C(a,c,e),C(a,d,e),C(b,c,d) yields at most two possible completions versus three required distinct follower values. Second control has a 5-colorable K5 primal but is strict-C UNSAT. Both return source-verifiable UNSAT or UNKNOWN without polarity advice. Wrong-path UNKNOWN. Neither is complete on arbitrary C.

**REPLAY:** K6 private-head encoding: 15,625 exhaustive rows, 234,375 pair tests, 120 unique-bad rows per each of 15 blocks, 15 complete strict-C deletion witnesses. Type1: all 3,125 color assignments UNSAT, four deletion witnesses, unique-bad rows 20/20/20/90. Independent explicit-tournament replay: 25 random input relabelings, 15 missing-edge negative controls, 19 strict C full witness vectors, 222 retained C checks. Myc3(C5) 283-variable 236-C source returned UNKNOWN. Python heap readings not machine bounds.

**RESOURCE CAUTION:** Naive sequential R B m^alpha is N^{.845+.35alpha}, requiring alpha<=97/70 for N^{1.33} after all charged preprocessing, output and verification. Source proof does not cover all arbitrary CNFs; no unrestricted machine lower bound. P vs NP OPEN.

**REPORT:** research/agents/strict-c-cover/2026-11-19_GF5_MARGINAL_FALSE_ZERO_GLOBAL_COVER.md
**LOCAL REPLAY PACKAGE:** T5C_Global_Cover_GF5_Cancellation_20261119.zip, SHA256 c5f532a142d9b1be6d32b676d09c14a64e9ba6cbef1b9ae39943f9ef97546f20 (main script, independent replay, sources, raw results, deletion witnesses, full report, hashes).

**NEXT:** certified exact separator-join projection with both positive and negative child evidence and fully charged extraction. Independently test growing-girth critical strict-C families without finite clique/capacity obstructions. No schedule/enabled-state or manuscript ownership changes.