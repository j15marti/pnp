# LSPV-4/562 | Exact paid-recomputation retention frontier in a native-/386 shared DAG

November 12, 2026, 06:32 PST. PNP Time-Space Resource Auditor. Historical Route A retained.
Status: **PROVED/EXACT in the declared finite resource transition system, independently replicated COMPUTATIONAL verification; external peer review pending. P versus NP OPEN.**

## Candidate cost theorem and four falsifiers

**Candidate.** The previously proved 82 retained slot-steps and 883 retained clause-byte steps for **no-recomputation** schedules of the fixed LSPV-4/560 proof are **not** sound lower bounds on all four-register schedules if legally paid recomputation is permitted.

F1: no legal recomputation schedule improves the two minima. F2: an apparent improvement requires forbidden expanding overwrites. F3: a candidate recomputation certificate changes original signed SOURCE, DEF, pivot, parent or terminal semantics and fails the unchanged checker. F4: shared gate owners or a recomputed Resolution deduction are under- or overcharged.

## Authenticated source and declared concrete resource semantics

The identical original signed odd-K4 packet is results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json, Git blob 6b72c961c2db19be87a0936361c467ef3445f4e2. It contains 17 original SOURCE, six defining facets, 35 strict paid Resolution deductions and three globally paid AND2 owners. Its declared archived-/386 logical work is W = 35 + 3 = 38. The unchanged authoritative restricted checker is experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986. It does **not** authenticate the complete historical R_mix341 grammar.

Number its 35 paid RES identities 0 through 34. A post-inference state S is a subset of their resident output clauses, with at most four simultaneous derived-result registers. SOURCE and DEF facets remain read-only. An operation j requires every paid predecessor in S. The output may use an empty register, or overwrite a required paid parent after it has been read. Under the nonexpanding policy the overwritten parent's canonical JSON clause-array length must be at least that of the result. Free deletions can occur before or after the inference. Any recomputation of a previously produced RES identity is **another paid RES execution**; global gate definitions are paid once each.

For a sequence of post-execution resident states S(t), define:

$$
A_{slot}=\sum_t |S(t)|,\qquad
A_{byte}=\sum_t\sum_{j\in S(t)} |\mathrm{JSON}(C_j)|.
$$

These are precisely defined abstract output-retention measures, not physical RAM measurements. Temporary parsing, premise retrieval, source authentication, reference handling, verification and discovery are separate.

**Exact transition-coverage lemma.** Every legal schedule maps to a path in the resident-subset state graph with equal paid execution count and retention area; every enumerated edge is implementable. Free deletion-only transitions can be absorbed into the next inference because deletion never makes a missing parent available. The next resident state is the new result plus a subset of prior residents. The union of retained old outputs and required parents must fit the capacity, or an eligible already-read parent must be overwritten when full. These are exactly the predicates in the executable auditor. Hence no concrete schedule of this stipulated machine is omitted.

## New exact finite-graph theorem

For four derived-result registers, **allowing any number of separately paid recomputations** gives the following global minima over all legal schedules of this fixed dependency graph:

| Objective and overwrite policy | Exact area minimum | Paid RES executions | Settled states | Discovered states | Admitted transitions |
|---|---:|---:|---:|---:|---:|
| Slot-steps, nonexpanding | **71** | 36 | 44,872 | 45,024 | 5,239,163 |
| Canonical clause-byte steps, nonexpanding | **748** | 36 | 44,616 | 44,882 | 5,207,331 |
| Canonical clause-byte steps, expanding | **746** | 36 | 45,646 | 46,042 | 5,372,194 |

Both nonexpanding minima have a 36-step witness containing all 35 original paid deductions and exactly one repeated computation of RES 0. The total fixed-grammar native logical work becomes **W = 36 + 3 = 39**.

Independent operating-system Python and independently implemented hosted V8/BigInt Dijkstra searches agree on the 71/748 values, state counts and transition counts. For the expanding overwrite case Python computes 746. The original no-recomputation result (/560) was 82 slot-steps and 883 byte-steps. One extra charged inference therefore saves **11 slot-steps (13.4%)** and **135 clause-byte steps (15.3%)**. The slot-objective witness returned by Python has byte-area 750, while the byte-optimal witness achieves both 748 byte-steps and 71 slot-steps.

**Proof of finite optimality.** For each state, enumerate every ready paid RES and every old-result retention subset. Apply the capacity/parent-overwrite test. The edge weight is the positive post-execution area. Dijkstra extracts paths in nondecreasing total area and therefore the first terminal output-34 state has the global minimum, despite arbitrary cycles from recomputation. Exhaustive finite enumeration supplies the lower bound; the independently validated, explicitly published 36-step resident-state trace supplies a matching upper bound. This is an exact conditional finite-state result, with independent external review pending, not an unrestricted mathematical hardness result.

## Original checker and hostile falsifiers

A new complete certificate was generated by preserving **all 23 original SOURCE/DEF records and all three original owner declarations exactly**, emitting the 36 paid RES occurrences in the optimized order, and rebasing parent references to the most recently emitted corresponding paid RES record.

The new original-checker-accepted certificate is results/raw/arc/2026-11-12_0632_LSPV4_562_W39_RECOMPUTED_NATIVE386_ACCEPTED.json (Git blob 389fbbf94599ce26c6875f657d5a945e46008182). It is **3,701 bytes, 59 records, 17 SOURCE, six DEF facets, 36 strict RES, three gate owners, W39**. The unchanged archived /386 original checking body was executed in hosted V8 and accepted it, including the terminal contradiction, zero odd-source models and eight even-control models. All eleven original hostile mutation controls were applied and rejected, across 3,970 checker assertions. **Separate Node operating-system execution of these new bytes was not completed.**

All four falsifiers are thereby addressed within their declared scope. A blanket abstraction assigning an 82-step minimum area to **every** concrete four-register schedule accidentally overcharges this genuine recomputation path, violating the requirement that abstract path cost not exceed concrete cost. Conversely treating the repeated RES 0 as a free use undercharges actual logical work; the correct certificate is W39, not W38. The globally paid definition owners remain paid exactly once, independently of facet reuse and fan-out.

## Physical resources, literature, and boundaries

The original certificate has 3,639 bytes, 58 records and 70 parent applications. The new certificate has 3,701 bytes, 59 records and 72 parent applications. This tradeoff reduces abstract retention area while **increasing proof logical work and certificate size**. Exact verification must acquire and check those certificate bytes; the old Node checker retains objects beyond any hypothetical four paid-output registers. Peak writable physical bits, sequential check time, parallel check span, retrieval/recomputation, scratch-buffer growth, large identifiers and compact representations are not bounded by the four-register number. The ideal minimum proof work W_R is also distinct from proof discovery and verifier execution. Summing lower-bound components requires a disjoint cost partition.

Pebbling and fixed-DAG scheduling are directly relevant model-matched methods, as in Nordström and Håstad (2013) and Nordström (2013). Their arbitrary-resolution proof lower bounds do not transfer automatically from one pinned proof DAG, and analogies to VLSI area-time or memory hierarchy need explicit simulations.

Prior original /386 controls /539-549 and /558-561, plus peer updates LSPV-1/590-591, LSPV-2/574-575, LSPV-3/588 and LSPV-5/503-504 were reviewed. The current source already has a legal W29 alternative proof, so the W39 construction cannot imply any minimum over all proof structures. The complete historical R_mix341 accepted-byte grammar and its fixed mixed-rule weights, including AND3, GF(2), LOCAL-CONVERT, paid DEF, fresh/exported/private wires, branch contexts, weakening, discharge, joins and compact rows, remain unauthenticated. Legitimate shortcuts cannot be excluded by this restricted model.

The main path **P2-D1 -> P2-C3 -> P2-B1** remains OPEN; P2-B2 and P2-B3 separately OPEN. P versus NP remains OPEN.

## Reproducibility and repository governance

- Reproducer: experiments/arc/lspv4_562_recompute_area.py, Git blob c2ee17e12af2454a49cf35f3b3fa94e7b7d3f770. With original certificate path argument it authenticates the exact paid parents and canonical clause lengths, emits the W39 certificate and returns the three optimal resource traces.
- Raw experimental evidence: results/raw/arc/2026-11-12_0632_LSPV4_562_RECOMPUTE_AREA_FRONTIER_RAW.json, Git blob d379176330a712b3355cc6e9b8894fdf52ebf21d.
- Root proof1.txt and proof2.txt and issue #3 reviewed: **TRACKERS REVIEWED; NO MATERIAL CHANGE**. No general proof obligation changed status. The canonical root main.tex could not be retrieved as nonempty complete content using the connected GitHub file interface, even with ranged reads (blob f3caa8adb89b720b780f30d29c85635dab42b4ee). No overwrite was attempted without a conflict-safe ownership-preserving merge.
- Exactly the original five roles, titles, Pacific hourly schedules, historic weights, ownership boundaries and TWO Route A / THREE Route B labels have been preserved. No automations were created or changed.

**References:** [1] Nordström J, Håstad J. Towards an Optimal Separation of Space and Length in Resolution. *Theory of Computing*. 2013;9:471-557. https://doi.org/10.4086/toc.2013.v009a014 . [2] Nordström J. Pebble Games, Proof Complexity, and Time-Space Trade-offs. *Logical Methods in Computer Science*. 2013;9(3). https://doi.org/10.2168/LMCS-9(3:15)2013 .

<!-- END_OF_VERIFIED_REPORT::LSPV-4::562 -->
