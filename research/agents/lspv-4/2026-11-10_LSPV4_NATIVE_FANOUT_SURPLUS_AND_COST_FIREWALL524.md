# LSPV-4/524: exact native source-DAG fanout surplus and zero-cost firewall

**2026-11-10 PST | LSPV-4 Time-Space Resource Auditor | Route A label preserved.** PROVED/RESTRICTED mathematical accounting; COMPUTATIONAL original-fixture replay. P versus NP OPEN.

**Dependencies:** [P2-D1] -> [P2-C3] -> [P2-B1], with separate [P2-B2]/B3. Evidence [P2-L4-524] refines [P2-L4-522], [P2-L4-523], [P2-L1-553], [P2-L1-554], [P2-L2-538] and [P2-L3-550]. No full historical native grammar or P-versus-NP lower bound has been proved.

## IDEA and falsifiers

Hypothesis: Exact source/arity/fanout accounting yields a stronger saturation invariant and exposes the failure of converting derived-node count directly to native paid work when a zero-priced multi-premise step exists.

F1. A rooted source-complete binary DAG with m sources and q=m-1 derived nodes admits a genuine paid lemma with two consumers. Refuted by the exact identity.
F2. A unit-paid unary LOCAL-CONVERT or nullary DEF can be inserted into a saturated q=m-1 graph while retaining all source ancestors. Refuted by the exact arity penalty.
F3. Source essentiality alone gives paid cost >=m-1 even if an *additional hypothetical* zero-paid binary inference is allowed. Refuted by a 3-source 2-inference graph with one free inference and one paid inference. This is not an authenticated historical R_mix341 rule.
F4. A shared paid lemma may be independently charged in both consumer views without exceeding its true creation cost. Refuted by a 3-paid-node shared DAG, whose naive doubled charge is 4 rather than 3.

## SEARCH: original project and external sources

Read complete root proof1.txt and proof2.txt (startup blobs 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and 2d49fa56208014f64c0be0639c45fc8502fdcbc3), issue #3 and current comments, AGENTS.md, CODEX.md, the pnp-research skill, November 9 abstract-interpretation handoff, November 10 LSPV-4/523 handoff and reports 522/523, LSPV-1/553/554, LSPV-2/538, LSPV-3/549/550, plus current GROKPROOF review/progress and original Claude TPORT report. LSPV-3/549 is a distinct test-only CASE/WEAKEN grammar. Relevant 539-549 results were checked for conflicts and do not authenticate the full historical mixed checker.

**Immutable native sources:** original producer 'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js' blob 4081022e8a3841d79f751a3d3a7a10decbb026da; original verifier 'experiments/arc/lspv2_341_independent_verify.js' blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; declared semantics 'research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex' blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb.

**Change-aware required repository checks:** 'konard/p-vs-np/scripts/proof_status.json' blob 93b77ed3d8fe456f81c690035f45f07910a247f2; 'blkph0x/p-vs-np-proof-research/METHOD_INDEX.md' blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; 'meelgroup/frat-xor/format.md' blob 986a21aa92b62f844ef1fce852193142c41b2b1f; 'tanyongkiam/cake_lpr/README.md' blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; 'peitl/short-proof/README.md' blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab; 'openai/math/README.md' blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. These are distinct proof/calculus projects, not missing native R_mix341 specifications. The CakeML LPR checker noted a November 1, 2026 final release; no checker substitution is made.

Primary controls: Cook and Reckhow, Journal of Symbolic Logic 44 (1979), 36-50, DOI 10.2307/2273702; Ben-Sasson and Nordstrom, arXiv:1008.1789 (2010), on proof length versus space; Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973, on abstraction soundness.

## Theorem 524.1, PROVED/RESTRICTED: exact surplus identity

Let P be a finite, acyclic, single-sink proof-dependency DAG with m distinct indegree-zero source/axiom roots, q derived nodes, and every node an ancestor of the sink. For each derived node v let a(v) be its number of premise occurrences. Let d+(u) be the number of times u appears as a premise of later derived nodes. Multiplicities count as separate dependency incidences, although the recovered /341 checker rejects duplicate parent IDs.

Define total consumer reuse surplus
$$
S(P)=\sum_{u\neq\mathrm{sink}}(d^+(u)-1)\ge 0.
$$
Every nonsink node has a consumer by goal-ancestry. Double count E, the number of premise incidences:
$$
E=\sum_{\mathrm{derived}\ v}a(v)=\sum_{u\neq\mathrm{sink}}d^+(u).
$$
There are m+q-1 nonsink nodes, so
$$
\boxed{q-(m-1)=S(P)+\sum_{\mathrm{derived}\ v}(2-a(v)).}\tag{524.1}
$$
For only binary, unary, and nullary steps, this becomes
$$
\boxed{q-(m-1)=S(P)+u+2z,}\tag{524.2}
$$
where u and z count unary and nullary steps. Thus for *all binary* steps, q=m-1+S; equality q=m-1 forces every source and paid nonsink to have exactly one consumer. Any genuinely shared paid lemma forces q>=m, unless other premises/sources or rule arities are changed. In a source-saturated proof whose all-derived records are paid one unit, no unary or nullary step can occur. This is an exact graph-accounting corollary of the earlier source-capacity inequality, not an unrestricted proof-size lower bound.

**Applicability firewall:** m means actual source roots in the sink ancestry. Replacing it by every clause of F requires separate original-input binding, soundness and source indispensability. If a DEF node introduces several zero-priced facets, they must retain their paid sponsor dependencies. If any legal closure has zero weight, the total number q of *all* derived records differs from weighted paid work W. The synthetic counterexample has roots s0,s1,s2; z0=(s0,s1) at *hypothetical* zero price; d0=(z0,s2) at price one. q=2=m-1 and S=0, but W=1<m-1. It falsifies any lower-bound argument that silently ignores free multi-premise steps. Historical /341 prose declares derived nodes unit priced; full accepted byte semantics remain missing.

## Theorem 524.2, CONDITIONAL: count-once abstraction cost polarity

For each *native* first-creation event v with fixed charge w(v)>=0 and for each historically authenticated reference/application event e with separate tariff r(e)>=0, choose component charges c_i(v), d_i(e)>=0 satisfying
$$
\sum_i c_i(v)\le w(v),\qquad \sum_i d_i(e)\le r(e).
$$
If every concrete step has an abstract successor that contains its concrete successor, abstract goals preserve the target, and every abstract path charges at most its allocated actual events, then every concrete refutation projects to abstract refutations with combined charges no more than actual W(P). Taking the infimum over legal concrete refutations gives
$$
\sum_i h_i\le \inf_P W(P).
$$
This is a **sufficient conditional schema**, not a completed cost-sound abstraction of the historical mixed calculus. Shared nodes are charged once globally at creation. Context-scoped lemmas may be reused only under compatible or legally discharged assumptions. The synthetic 3-paid-node DAG d0(s0,s1), d1(d0,s2), d2(d0,d1) has one shared *paid* d0, S=1 and W=3. Independently charging d0 in two consumer views gives 4>3; allocating its one native unit across views fixes the inequality. Such allocations are accounting fractions, **not revised fixed native weights or accepted historical branch rules**.

## COMPUTATIONAL native original-checker replay and independent controls

Executed the **unmodified original producer and original independent verifier function bodies inside V8**, replacing only Node file/console I/O adapters. They accepted the original seven-fixture set with **30,714 original assertion groups**, 7 malformed-input controls, and 5 corrupt-certificate controls. Every paid node in these packets has one consumer, as independently implied by the exact saturation identity.

| Original signed 3-CNF fixture | SOURCE m | Paid q | S | Reused paid | JSON bytes | Deletion witness bits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| K4 | 16 | 15 | 0 | 0 | 3,364 | 96 |
| K33 | 24 | 23 | 0 | 0 | 5,081 | 216 |
| Cube | 32 | 31 | 0 | 0 | 6,880 | 384 |
| Petersen | 40 | 39 | 0 | 0 | 8,757 | 600 |
| Prism6 | 48 | 47 | 0 | 0 | 10,682 | 864 |
| Prism16 | 128 | 127 | 0 | 0 | 33,003 | 6,144 |
| Bridged K4x2 | 40 | 39 | 0 | 0 | 8,701 | 540 |

All seven had q=m-1 and were trees, not examples of genuine *paid* reconvergence. The bridge fixture has only 36 individually essential original clauses despite 40 used roots; q=39 is an upper bound, not an independently certified mixed-calculus optimum. For the six bridgeless source families, the original /341 theorem certifies source indispensability in the declared unit-priced binary system. A cheap valid GF(2) refutation is retained, not excluded.

Standalone local Node synthetic audit: **167 assertions**, six graph controls (binary saturation, one paid shared node, free binary closure, unary and nullary steps, and 252-character identifiers), four hostile graph rejections. **Independent Python exhaustive audit** on 3-root ordered binary DAGs with q=2,3,4,5 found **3, 24, 219, 2,508 reachable graphs** respectively; all satisfy (524.1). The Python zero-price control independently reproduced W=1<m-1. The separately published new Node wrapper was NOT executed as an OS process; the immutable original checker/producer and local synthetic programs WERE executed. No full historical R_mix341 checker has been executed or located.

**Raw evidence:** 'results/raw/arc/2026-11-10_LSPV4_524_FANOUT_SURPLUS_NATIVE_RAW.json', blob 7541617f031354f6afab7b17d322e56089c68745. **Published Node wrapper:** 'experiments/arc/lspv4_524_fanout_surplus_audit.cjs', blob b8c5132f53e94ab754b4410758877637f2661486.

## Native resource and rule ledger

| Operation | Fixed logical charge in /341 prose and known executable | Real bit/time/space obligations |
| --- | --- | --- |
| Original SOURCE (recovered fixture) | 0 derived-unit charge | Signed literal JSON tokens and ID strings have nonzero serialized bytes; original checker parses all JSON, authenticates graph source and deletion witnesses inside packet, but **does not bind an independently supplied DIMACS source**. SOURCE retention in its byId map is physical memory, not free. |
| AND3 (recovered) | 1 per distinct derived node | Two parent references; support/table/optional row; at most eight semantic rows if *typed* width<=3. Original checker accepts a semantically invalid string support (LSPV-2/538); accepted-byte abstraction must cover that behavior or mark repaired typing as new calculus. Byte parsing, indexed retrieval, copies and caching paid separately. |
| XOR/GF(2) (recovered) | 1 per distinct derived node | Two parent IDs; serial mask/RHS bytes; BigInt XOR and sparse-versus-dense representation costs are NOT free native-machine work. Paid-node dependency span is one plus maximum premise span under ideal parallel unit-cost model; actual indexed-machine span/time depends on bit widths. |
| RES, LOCAL-CONVERT, DEF/facets/wires (prose only) | Unit per declared derived step, but historically authoritative checker not recovered | Native rule bytes, owner/facet tariffs, definitions and external-source binding UNKNOWN. The recovered dispatcher handles AND3/XOR only and hard-checks q=4V-1; it is NOT full proof-language complete (LSPV-1/553). |
| CASE, weakening, contexts, discharge, joins, deletion | Historical grammar and reference tariffs UNKNOWN | Synthetic branch controls and separately developed CASE grammar do not authenticate native operations. Every assumption scope, join/reference, retention/recomputation, failure/restart and all-phase simultaneous peak must be verified before summing abstract lower bounds. |

The 127 paid-node Prism16 fixture has **6,144 original deletion-witness bits** even before JSON/ID and checker overhead. LSPV-4/523 separately proved a 3-semantic-slot DFS schedule on the *same fixed proof DAG* under fresh non-overwriting outputs. Such logical retention is neither the original Node verifier's high-water writable memory nor a native FLMV machine bound. Long IDs, compact affine rows, materialized output, sources and caches make these resources noninterchangeable. Distinguish ideal W(P) (free proof discovery) from actual proof search, failed policies, source parsing, certificate construction/verification and readback.

## ITERATE and remaining gap

The exact graph budget sharpens the earlier source-capacity lower bound by proving that **at saturation no shared paid lemma, unary transformation or nullary construction can occur** under its stated constraints. The zero-price adversarial control demonstrates why a full accepted-rule and weight inventory is essential before using this structural inequality in a universal native-calculus abstraction. The recovery gap remains: source-bound historical accepted-byte semantics for RES, LOCAL-CONVERT, paid DEF and facets, exported/private wires, branching/weakening/discharge/joins/deletions; then a goal-preserving, concrete-inclusive, cost-sound all-rule abstraction; then unrestricted Wbar lower bounds and a separate noncircular B3 bridge.

**Actual advance:** PROVED/RESTRICTED exact fanout/arity surplus formula and free-rule countercontrol. **Verification:** original checker V8 replay plus two independent finite audit implementations. **Publication:** role-owned report, code/raw and coordination handoff; tracker status requires current full-SHA reconciliation. **P versus NP remains OPEN.**
