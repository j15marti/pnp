# TMR-3/052: Source-indexed adaptive headwalks, exponential graph diversity, and a charged selector

**2026-11-15 13:40 PST | TMR-3 / PNP Time-Space Tradeoffs | Track B | SOURCEGRAPH052**

**Status:** PROVED/EXACT for the precisely qualified enumeration and source-access lemmas, independent mathematics review OPEN; finite replay COMPUTATIONAL. P versus NP OPEN. No general Tree Evaluation improvement or unrestricted SAT lower bound.

## 1. Candidate and four falsifiers

**Candidate:** Exhibit for **one fixed physical deterministic machine** a family with 2^B different *authentic* computation-graph motion records but a source-authenticated O(log N)-space selector. For input-independent fixed-order protocols that individually test graph guesses until the true graph, prove that a worst-case source forces 2^B genuine trials and hence Omega(B) peak workspace by deterministic configuration counting. This supplies a true-input witness for the conditional TMR-3/051 enumerative bound, and an explicit legal shortcut invalidating any unrestricted graph-diversity-to-space argument.

**F1:** An input-dependent order, bulk prefix pruning, or direct source selector escapes this theorem. **F2:** A count of syntactically possible guesses does not establish 2^B genuine graph traces; injectivity of one machine's source-to-trace map is essential. **F3:** Read-only source must have N=poly(B); count all writable space, buffers and output. **F4:** Physical local-head source rereads and source validation are not free indexed memory accesses.

## 2. Authentic fixed-machine construction

For each B>=1 and **odd** b>=1, choose z in {0,1}^B and the read-only source

    X_b(z)=z_1^b z_2^b ... z_B^b,    N=Bb,

where v^b denotes b copies of the literal bit v. B and b are public parameters of the declared block service, or may be included in a charged logarithmic-size source header. A one-pass source scanner with counters checks the promised constant-run syntax in O(N) sequential work and O(log N) writable memory. Malformed inputs are not silently treated as authenticated.

Fix a single finite-control program M independent of B,b,z. At each input symbol it moves the immutable source head one cell right, moves a distinct blank-work-tape head right by one cell iff that symbol is 1, and XORs one parity bit in its finite control. It halts with that parity on the endmarker. M is deterministic and total on *all* binary inputs. Its physical runtime on X_b(z) is N+O(1). For this family, the work-head location after j complete b-step blocks is exactly

    H_j=b sum_{i=1}^j z_i,

and its authentic block-movement label is

    m_j=(H_j-H_{j-1})/b=z_j in {0,1}.

The source head's movement record is fixed. Williams's computation-graph encoding explicitly records the other head's m_j at every time block [1, Section 3.2]. Therefore the source-to-full-graph-record map is injective: there are **2^B genuine different graph signatures for the same fixed M and fixed B,b,N**. This is not merely a synthetic count of all possible ternary records.

For odd b, M's parity on X_b(z) equals parity(z), so both final output labels occur. A different source-dependent deterministic decision procedure can still compute the result in **O(N) time and O(1) writable workspace**, by reading the source once and updating one parity control bit. This is an intentionally easy hostile control.

## 3. Fixed-order enumeration theorem (proved)

**Theorem 052-A.** Fix M and (B,b). Let E be a fixed uniform deterministic exact candidate protocol satisfying:

1. Its complete candidate-record order depends on M,B,b,N but **not** on the actual bits of source z.
2. It pays at least one real machine transition for every individually tested candidate.
3. It returns a non-FAIL accept/reject answer **only after** testing the unique true graph record for that source, and halts on every promised source.
4. It has a fixed number of locally moving source/work heads, finite control/alphabet, charges every visited writable cell including query/address/output buffers, and has original immutable input length N<=B^c for some constant c.

Then for **every such E and every B**, there exists z* depending on E and B such that E on X_b(z*) performs at least 2^B candidate trials and has peak writable space S_E=Omega(B).

**Proof:** The construction gives 2^B distinct authentic graph records R. In any z-independent candidate order covering all R, one R member has rank at least 2^B. Choose its corresponding z*. Every earlier record is false for that particular source; exact per-candidate checking cannot terminate before the target. Hence the actual machine performs at least 2^B genuine paid transitions.

If Q is the simulator's finite control set, H its constant number of source heads, w its constant number of writable tapes and Gamma its fixed writable alphabet, the complete configuration count with source length N and S visited writable cells obeys the generous bound

    C(N,S) <= |Q| (N+2)^H (S+2)^(2w) |Gamma|^(S+w).

A halting deterministic run cannot repeat a complete configuration. Therefore 2^B <= T_E+1 <= C(N,S_E), giving

    B <= O(S_E+log(N+2)+log(S_E+2)).

For N polynomial in B, S_E=o(B) contradicts this inequality. The same E, one actual source z*, actual elapsed time and actual peak space are used throughout. QED.

The input-dependent selector is **outside** hypothesis 1, not disallowed as a cheap algorithm. A machine which bulk-eliminates candidates is outside hypothesis 2. A precomputed oracle or external output tape must be separately charged. The theorem is not a common hard input for all simulators or a SAT lower bound.

**Finite integer example:** In an illustrative q=8-state, one-read-only-head, one-binary-work-tape model, 2^B paid trials require

    q (N+2) (S+2) 2^S >= 2^B.

For B=256, odd b=17, N=4352, integer arithmetic gives **S>=234** binary work cells for that declared model and enumerative execution. The general Omega(B) theorem does not depend on q=8.

## 4. Matching source-dependent shortcut, and its actual resource ledger

On a validated promised source the true movement label at stage i is the physical source bit at address (i-1)b+1:

    m_i=X_b(z)[(i-1)b+1].

An indexed-bit model uses O(log N) address bits and one charged indexed source access. On a physically locally headed immutable source tape, from any earlier source-head location, seeking the requested symbol takes at most N+O(1) local moves, with O(log N) writable counter/index bits. A full scan authenticating run constancy requires O(N) work and O(log N) space. The source identity and validation status must be retained or reverified before subsequent uses, with costs.

Before stage j, the work head's block index is p_j=sum_{i<j} z_i, computable by a source scan in O(N) sequential time and O(log N) writable space. This block index is monotone. Consequently its most recent earlier work-tape block use is stage j-1 **if z_(j-1)=0**, and no earlier stage otherwise; the associated source/last-use edge predicate is generated within the same logarithmic workspace. Source-tape graph edges follow its fixed sequential scan. Thus this particular **adaptive, source-dependent** computation graph is genuinely locally regenerable without holding a B-bit candidate.

For an otherwise separately proved implicit-tree evaluator making Q graph/leaf queries, with work W_tree and live writable space S_tree excluding these services, a conservative possible charged interface composition on this family would have

    W_total <= W_tree + O(N Q) + O(N) + W_other,
    S_total <= S_tree + O(log N) + S_other.

Here W_other,S_other explicitly include all retained simulator information, leaf evaluation, data representations, conversions, output, arithmetic, failed attempts and sharing. Reusable service scratch cannot be double-counted, but unerasable retained data must be added. **No polynomial bound on Q or W_tree is asserted.** In particular, Cook-Mertz/Williams gives a space simulation, not a free polynomial-time Tree Evaluation evaluation.

## 5. Track B consequence and model firewall

Choose b=Theta(sqrt B), odd. Then T=N=Bb=Theta(B^(3/2)), B=Theta(T^(2/3)), b=Theta(T^(1/3)). The input-independent fixed-order enumerator on some source requires Omega(T^(2/3)) workspace, while authentic graph lookup for the SAME family uses only O(log T) extra workspace, O(T) worst per physical source query. This is a sharp **architectural contrast**, not a work lower bound for the source-aware algorithm.

If a new constant-arity evaluator were *independently proved* to use soft-O(b+sqrt B) space with all graph, node, arithmetic and address costs included, this source-aware family would not introduce a hidden Omega(B) graph-guess barrier. The conditional balance would be soft-O(T^(1/3)) space. Such an evaluator is not built here. Repeating the unchanged square-root Williams simulation or its potentially exponential-time evaluation is not an improved algorithm. The unrestricted case of head positions depending on **revisited, previously written work symbols** remains OPEN.

The result strengthens TMR-3/051's architecture-specific lower-bound antecedent by producing genuine worst-case source records; it simultaneously gives the cheap input-aware escape anticipated by TMR-3/050. It does not contradict Williams's 2025 O(sqrt(T log T)) general space simulation [1] or Cook-Mertz [2].

## 6. Same-machine accounting and mandatory gates

| Item | Actual accounting |
|:--|:--|
| Original physical M | T=N+O(1), one immutable source head, one moving blank work head, one parity control bit; up to N+1 work cells **visited** even if not written |
| Source X_b(z) | N=Bb; B,b headers, source authentication, indices and rereads counted |
| Enumerative E | One hard source z* forces 2^B sequential paid candidate trials and Omega(B) writable cells for that SAME E |
| Direct D | A different but genuine all-source parity decider uses O(N) time, O(1) writable space; not mixed with E to prove a lower bound |
| Source selector G | O(log N) writable scratch, O(N) worst physical local seek/query, reusable only with a charged source-validation method |
| Tree evaluator | Q and W_tree unknown; no uncharged leaf calls, external oracle, output memory, sharing or address-generation operations |
| Parallel execution | Not substituted for sequential work; aggregate workspace/messages needed for network variants |

| Gate | Status and scope |
|:--|:--|
| DISJ sanity | **PASS.** No static-rank-to-circuit theorem; DISJ, Horn, affine and low-treewidth controls remain easy, as does this parity family |
| Relativization | **NOT APPLICABLE WITH REASON** to a P-vs-NP separation (none claimed). Ordinary fixed-machine configuration bound is model-specific; no nonrelativizing step, algebrization or Natural Proofs inference |
| Simultaneous DTISP | **PASS** for the restricted same-E time/space claim and independently charged easy D; **OPEN** for simultaneous arbitrary-SAT/FLMV transfer |
| Configuration counting | **PASS.** The upper bound on halting-run length is used *only after* separately proving 2^B actual enumerative transitions; not interpreted as an independent work lower bound |

The following are legal falsifying shortcuts, not excluded inputs: source-aware candidate ordering, bulk source-based pruning, cached source bit accesses, streaming reconstruction, compact algebra, and independent cheap parity decision. A malformed source such as 1000 at b=4 falsifies an unvalidated first-bit graph selector; promise checking is compulsory. Historical /341 is FAIL as a full UNSAT authority; /386 is RESTRICTED. All general SAT-machine arrows remain OPEN.

## 7. Computational audit, corpus and publication

**Executed twice, byte-identical CPython 3.13.5 raw JSON, 6,686,711 exact assertions, zero failures.** Checked all 196,602 promised sources at B=1,...,15, b in {1,3,5}, with stepwise physical head positions, prefix block indices, recovered true movement labels, distinct true graph signatures, last-use predecessor identities, parity labels, and indexed access. Malformed-run, physical seek, q=8 capacity, and 2^B trial-order controls tested separately. Seed NONE. No low-level native simulator, Lean proof, or end-to-end SAT machine executed. Finite evidence COMPUTATIONAL; the restricted theorem has a separate symbolic proof.

- Report: research/agents/tmr-3/2026-11-15_1340_TMR3_SOURCE_INDEXED_GRAPH_SELECTOR052.md
- Executed source: experiments/tmr/tmr3_source_indexed_graph052.py
- Raw: results/raw/tmr/2026-11-15_1340_TMR3_SOURCE_GRAPH052_PY_RAW.json
- Compact history-preserving handoff: research/agents/tmr-3/runs/2026-11-15_1340/handoff.md

Current directive read FIRST: SAT compression/circuits main blob 7b8804dc7587abc5134055b5b0d16a143055ca5a. Also reviewed proof1 current content, proof2 and main.tex blob SHAs (oversized bodies returned empty), all current five TMR handoffs, AGENTS.md, CODEX.md, repo research skill/mode/protocol, issue #3, original TMR-3/050 and 051 on their still-open draft branches, relevant Track A/C peer findings, and Williams's paper including its PDF p.8 screenshot. No full checkout/preflight was possible because git DNS was unavailable. This is a new explicit graph-trace family, not priority claimed for the underlying counting or streaming facts.

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** No schedule, task, root tracker, main.tex, historical proof, or other agent-owned file changed. P versus NP OPEN.

**Next precise research objective:** Determine whether a *fixed source machine whose head reversals depend on revisited, formerly written symbols* admits an authentic graph-indexing service with space o(B), while bounding Q and all physical query work. Distinguish a truly new evaluator from a freely supplied correct transcript.

## Sources

[1] R. Ryan Williams, *Simulating Time With Square-Root Space*, STOC 2025, arXiv:2502.17779v1, Section 3.2, Claims 3.4-3.5, Section 3.3. https://arxiv.org/pdf/2502.17779

[2] Cook and Mertz, *Tree Evaluation Is in Space O(log n log log n)*, STOC 2024, Theorem 7; restated in [1], Theorem 2.2. https://doi.org/10.1145/3618260.3649664

[3] Internal TMR-3/050 (draft PR #142), /051 (draft PR #147). The latter's lower bound assumes actual 2^(Omega(B)) trials, which are explicitly witnessed under the new fixed-order protocol here.
