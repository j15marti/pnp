# LSPV-1/557: Independent alternative prism family falsifies recovered /341 checker source soundness

**2026-11-10 15:03 PST | General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED (alternate construction) + COMPUTATIONAL | P versus NP OPEN**

## IDEA, four falsifiers, and duplication audit

**Candidate:** The previously established LSPV-3/551-553 phenomenon, wherein the recovered incomplete /341 SOURCE/AND3/XOR checker accepts a purported refutation of an actually SAT source, persists on an independently constructed infinite family of connected cubic graphs: a subdivided K4 connected by a bridge to a subdivided k-prism for k>=3. This is **an independent replication/alternate family**, not a first discovery of parameterized SAT-source forgery.

Falsifiers registered: (F1) graph cubicity, source incidence or bridge fails for some k; (F2) the fixed four-edge cycle assignment falsifies a source clause; (F3) the pinned original checker rejects the generated purported refutation; (F4) a one-field repair of charge typing or support typing, or an AND3/sink corruption, still passes. No falsifier occurred in the five sizes tested; F1 and F2 have uniform combinatorial arguments, while F3 and F4 were tested using original verifier functions.

**Prior work credited:** LSPV-3/551 found the first SAT-source accepted packet; LSPV-3/552 proved a parametric checker-accepted family via repeated triangle expansion and a sharp E>=18 threshold; LSPV-3/553 proved exact bridge/cycle source model counts; LSPV-3/554 proved accepted-goal/semantic-UNSAT incompatibility. The present work gives a distinct k-prism family and an independent replay of the original executable bodies, rather than claiming any of those results anew. Earlier LSPV-1/553-556, LSPV-2/539-541, LSPV-4/525-526, and LSPV-5/477 were compared for grammar/provenance scope.

## Construction and exact mathematical scope

Start with K4 and subdivide its edge (0,1) at vertex 4. Start with a k-prism (2k vertices) and subdivide one top edge at vertex 5+2k. Join the two new subdivision vertices by a bridge. Reorder edges so vertex 0 meets edge indices 0,1,12, where edges 0=(0,2), 1=(0,3), 12=(0,4). This yields a simple connected cubic graph with

$$
V_k=2k+6,\qquad E_k=3k+9.
$$

For each other vertex use the usual four proper signed width-three clauses imposing even incident parity. For vertex zero use the four proper clauses

$$
(x_0\lor x_1\lor x_{12})\land
(x_0\lor x_1\lor\neg x_{12})\land
(\neg x_0\lor\neg x_1\lor x_{12})\land
(\neg x_0\lor\neg x_1\lor\neg x_{12}),
$$

which impose x_0 XOR x_1=1 independently of x_12. Exactly edges 0,2,5,12 form the cycle 0-2-1-4-0. Assigning those four edge bits to one and all others to zero satisfies every source clause, so the actual source F_k is **SAT**, with m_k=4V_k=8k+24 clauses.

The omitted edge 12 belongs to a cycle, not the bridge. The already proved LSPV-3/553 graph-cycle theorem therefore yields

$$
\#\operatorname{SAT}(F_k)=2^{E_k-V_k}=2^{k+3}.
$$

This count is a direct corollary of the earlier theorem, not a new model-count theorem. It shows why a forged checker-accepted contradiction here is semantically invalid.

## The recovered fixture verifier, not the declared fixed calculus

The pinned original producer builds odd-charge Tseitin AND3/XOR deductions. For each new graph, preserve the original producer proof skeleton except the four special vertex-zero source clauses, set charge[0] to the JSON **string** "1", and set the first three paid factor tables to 238, 230, 102. On the third, set support to the **string** "012" instead of the array [0,1,12], retaining its purported row mask 0x1003 with RHS 1. Set deletion witnesses null and essential count zero, since the graph has a bridge. Include a genuine K4 fixture first to satisfy the original executable self-tests. The proof still contains q_k=4V_k-1=8k+23 purported paid nodes.

The checker coerces string charge "1" to numeric 1 for XOR, but the strict source pattern comparison does not authenticate the source clauses. String support "012" admits substring 12 in a membership check, while a separate character-wise iteration indexes 0,1,2 rather than 0,1,12. This causes a false third AND3 factor/affine alias to pass the checker. At the actual SAT witness, x_0 XOR x_1 XOR x_12=0, so the purported row asserting value 1 is false. This packet is **not a legal mathematical refutation** of F_k.

The graph's bridge bypasses the checker's bridgeless all-essential condition; E_k>=18 bypasses its small-instance brute-force UNSAT test. All other original producer XOR steps continue to pass. This is a precise explanation of why the original incomplete executable accepts the counterfeit and does NOT authenticate any historical RES, LOCAL-CONVERT, DEF, branching, context, discharge, join, weakening or deletion grammar.

## ITERATE: original-source V8 verification

| k | V | E | m | Claimed paid q | Accepted original checker assertions | Hostile controls |
|---:|---:|---:|---:|---:|---:|---|
| 3 | 12 | 18 | 48 | 47 | 2272 | 4/4 rejected |
| 4 | 14 | 21 | 56 | 55 | 2416 | 4/4 rejected |
| 5 | 16 | 24 | 64 | 63 | 2560 | 4/4 rejected |
| 8 | 22 | 33 | 88 | 87 | 2992 | 4/4 rejected |
| 12 | 30 | 45 | 120 | 119 | 3568 | 4/4 rejected |

Each of the five forged original sources has an independently checked satisfying assignment with one-bits at edges 0,2,5,12; all five counterfeit packets were **ACCEPTED** by original checker function bodies in Code Mode V8. All 20 hostile controls (numeric charge repair, integer-array support repair, incorrect third AND3 table, false terminal RHS) were **REJECTED**. Separately enumerated all 2^18 assignments of the k=3 true source and found exactly 64 satisfying assignments. Larger cases rely on the established cycle-space theorem, not pretended exhaustive search.

The standalone published Node reproducer was syntax parsed and passed complete GitHub readback; it was **not** independently executed by an operating-system Node process in this run. Source code pins: original producer Git blob 4081022e8a3841d79f751a3d3a7a10decbb026da; unchanged checker fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; prior genuine-K4/SAT-source packet 706947c767361e7c979b8208677eb983d33838f4.

Executable: experiments/arc/lspv1_557_prism_independent_replay.cjs (verified blob 39189ef40eaadadd30f4e9a10a462ed606de134b).
Raw: results/raw/arc/2026-11-10_1503_LSPV1_557_PRISM_INDEPENDENT_RAW.json (verified blob 7a4fc22888481832dda2e6c505fbdf78da094903).

## Corpus / literature, cross-role interface and proof-chain ledger

Read both complete root trackers, issue #3 and its latest specialist evidence, AGENTS.md, CODEX.md, the project skill and topic handoffs, the original checker and producer, actual relevant LSPV-1/2/3/4/5 original reports, Grok 2026-11-10 14:35 UTC progress and Claude ONETAPE-0001 (a distinct machine control). Change-aware exact reads of konard/p-vs-np scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2) and blkph0x/p-vs-np-proof-research METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5) found no authenticated full /341 parser. Primary scope controls: Cook-Reckhow 1979 DOI 10.2307/2273702 (sound proof systems), Cousot-Cousot POPL 1977 DOI 10.1145/512950.512973 (sound abstract semantics), Urquhart 1987 DOI 10.1145/7531.8928 (Resolution-hard Tseitin families, not full mixed-calculus hardness).

For a fixed, genuine source-authenticated calculus R, the still-OPEN global minimum is

$$
W_R(F)=\min_{\pi\in \mathrm{LegalRefutations}_R(F)}
\sum_{v\in\mathrm{DistinctPaidNodes}(\pi)}w_R(v).
$$

The minimization grants the best complete branching/shared proof DAG, counts each globally shared paid node once, enforces assumption discharge and exact native contexts, and includes any authentic auxiliary/definition/extension shortcuts. This counterfeit is **not** in the legal proof set and does not provide a W_R upper bound. Cost-sound abstractions require simulation of every genuine native step, faithful goals and native cost no less than abstract cost; a checker-ACCEPT goal is not equivalent to a semantic UNSAT goal.

**[P2-D1] OPEN:** full historical accepted-byte grammar/source binding missing. **[P2-C3] OPEN:** full legal-rule cost-sound alpha/gamma simulation missing. **[P2-B1] OPEN:** no superpolynomial full-calculus bound. **[P2-B2]/B3 OPEN:** no same-R noncircular all-decider bridge. All P1 algorithm nodes remain OPEN. Source and certificate bits, logical work, discovery, actual runtime, span and peak space remain distinct.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt full blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters) and proof2.txt full blob 6338814517505963386646c288a4ecb47c68bb77 (935,119 characters) were read. Because this independently confirms preexisting material [P2-L3-551-554], no duplicate root evidence node or tracker edit was made. Root main.tex fetch returned empty content with blob SHA df94dfa745e2578095e6e7aa6df86d351598de28, so no safe ownership-region write was possible. Repository-wide preflight, complete native checker and independent specialist review were not executed. The five identities, titles, schedules, timezone, enabled states, historical weights, ownership and two Route A / three Route B allocation were not modified.

**P versus NP remains OPEN.**
