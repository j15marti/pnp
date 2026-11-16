# TMR-4/058 v2 | 2026-11-15 18:41 PST | All-input arity guard correction

**Status:** PROVED/EXACT RESTRICTED symbolic source-to-OBDD theorem unchanged, COMPUTATIONAL verification strengthened, independent math review OPEN. This is a model-matched, genuinely necessary implementation correction in the authenticated source parsing arrow. The original /058 v1 source/raw remain byte-exact and unchanged. P versus NP OPEN.

## Precise failed all-input implementation premise

The v1 finite parser checked that every declared original input ID has at least one authentic gate use, but allocated an array of size declared n before enforcing this. An adversarial canonical source may declare n=1,000,000,000,000 (a valid safe JSON integer) with only one gate referencing x0 twice. The source is OUT-OF-CLASS because it has 999,999,999,999 unused input identities. Nevertheless v1 attempts a massive allocation and cannot claim its complete invalid-word rejection lies within its stated polynomial source-size budget. This is a real source-acquisition defect, not a theorem counterexample on the valid wavefront class. The actual source word is short.

## Exact repair, quantifiers and cost

Each binary gate record carries exactly two operand references, so a source with g gates can reference at most 2g DISTINCT original input IDs. For EVERY valid source where ALL n original variables occur, necessarily n<=2g. The v2 parser checks this simple necessary condition immediately after reading the parsed n and gate-list length, BEFORE constructing any n-indexed input tables. It rejects n>2g as OUT-OF-CLASS. When n<=2g, the n-element input use table has O(g) cells and O(L)-polynomial construction cost. This is a symbolic, exact, strict arithmetic guard. The actual gate-array length is physically obtained by full source parsing; both the comparison and rejected return are paid. Gate-only level discovery, rank inequalities, complete stage path semantics and the source's n distinct variables are otherwise unchanged.

The implication is one-way: n<=2g is necessary but not sufficient. The rest of the authenticator still rejects missing input uses, duplicate IDs, cycles, dead gates, nonadjacent gate edges and cross-level repeated input uses. This retains the genuine all-input parse and source promise, rather than silently assuming short declarations.

## Execution and exact evidence

Authored executable revision tmr4-wavefront-dag058.v2 includes the one-line preallocation n>2g guard and a new canonical source with n=1000000000000, one gate g0=AND(x0,x0), output g0. Actually executed through native hosted V8 Function and independently rerun after GitHub branch readback. 137 valid canonical cases (125 shared internal gate), 8 malformed/out-of-class controls, 82,168 exact assertions, 4,440 assignments, 35,534 gate replays, 1,526 GF(2)/GF(101) ranks and ZERO failures. The additional rejected case takes the early guard and never allocates n slots. Original seed 20261115 and all 137 exact v1 source fixtures are preserved. Structured raw results were reproduced exactly after fetching the published source and raw branch blobs.

- executable experiments/tmr/tmr4_wavefront_dag_e2e058_v2.js; exact Git blob 94393d83acad96a029632bc366f844d3689beb9e
- raw results/raw/tmr/2026-11-15_1841_TMR4_WAVEFRONT_DAG058_V2_V8_RAW.json; exact Git blob d76e7248c2635a4e197b8f832afacf33225ff3a6
- original report research/agents/tmr-4/2026-11-15_1841_TMR4_WAVEFRONT_DAG_NO_ADVICE_END_TO_END058.md and original v1 evidence remain unchanged

## Four mandatory gates and one next dependency

DISJ PASS restricted, general circuit hardness transfer OPEN; relativization PASS intermediate but nonrelativizing NP step OPEN; simultaneous DTISP PASS conservative SAME_REALIZATION upper bound, forbidden pair OPEN; deterministic configuration counting PASS as an upper-bound consistency guard ONLY, no necessary-work or quantum inference. Canonical source size, reference count, sharing, and invalid input are now more explicitly charged. Horn, 2SAT, affine, unique-solution rank one and compact representations remain legitimate. /341 full UNSAT authority FAIL; /386 RESTRICTED.

**ONE next D4-LONG-EDGE-SPILL:** charge live intervals for nonadjacent gate edges and repeated original-input use across levels. All unrestricted circuit/SAT-machine transfers and P versus NP OPEN. Independent mathematical peer review OPEN.
