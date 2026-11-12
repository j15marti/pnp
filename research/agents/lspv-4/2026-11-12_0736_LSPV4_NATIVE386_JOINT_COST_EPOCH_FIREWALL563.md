# LSPV-4/563: Same-realization work/retention firewall for an actual native-/386 recomputation proof

**November 12, 2026, 07:36 PST. PNP Time-Space Resource Auditor; historical Route A.**

**Status: PROVED/RESTRICTED finite fixed-DAG resource theorem, independently reproduced COMPUTATIONAL checks; external review pending. P versus NP OPEN.**

## One candidate theorem and four falsifiers

**Candidate.** Logical-work-safe elimination of repeated paid Resolution conclusions need not be simultaneously cost-nonincreasing for *retention area* on the very same fixed native proof DAG. Moreover, LSPV-4/560 reports pre-execution live-set area while LSPV-4/562 reports post-execution resident-set area: their earlier quoted 82-to-71 and 883-to-748 comparisons were not in precisely the same resource convention.

- **F1:** No-recomputation area under the exact /562 post-execution metric is still (82,883). **Falsified:** it is (83,885); the unique terminal empty-clause result contributes (1,2).
- **F2:** The 36-execution packet changes original signed SOURCE, gate owners or some paid proof identity other than recomputing one deduction. **Rejected:** all 23 original SOURCE/DEF records, spec and three owner declarations are identical, and the 35 signed paid deductions are preserved; original paid RES 0 appears twice.
- **F3:** Its 71/748 resident-state trace omits a live premise, uses an expanding overwrite or creates an unearned result. **Rejected:** an independent 36-transition parent/retention/nonexpansion audit validates every step.
- **F4:** An alternative valid proof, GF(2) conversion, extension, branch learning, or representation could defeat an *all-proof* lower bound. **Admitted:** this theorem is intentionally only about the pinned archived /386 proof dependency graph, not the full historical mixed calculus or all SAT algorithms.

## Authenticated object, precedent and evidence provenance

The original source-authenticated odd-\(K_4\) proof is [LSPV-4/560's W38 packet](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json), Git blob `6b72c961c2db19be87a0936361c467ef3445f4e2`. It contains all 17 original signed SOURCE records, six genuine free DEF facets, 35 strict signed Resolution deductions and three once-paid conservative AND2 gate owners. It was checked against the unchanged archived /386 checker, [blob `338305c0ce101704205e57543756b8127074a986`](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_386_independent_verify.js).

The second object is [LSPV-4/562's W39 accepted packet](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0632_LSPV4_562_W39_RECOMPUTED_NATIVE386_ACCEPTED.json), blob `389fbbf94599ce26c6875f657d5a945e46008182`: it pays for 36 RES **executions**, of which two are the same fixed RES identity 0, plus the same three globally charged owners. Its identical signed source and owner objects are not reconstructed or guessed. The fixed 35-node paid parent DAG and canonical clause-array lengths are those authenticated in [LSPV-4/560](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-11-12_0436_LSPV4_NATIVE386_NONSOURCE_SHARED_LEMMA560.tex) and [LSPV-4/562](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-11-12_0632_LSPV4_NATIVE386_RECOMPUTATION_AREA_FRONTIER562.md).

Corpus reconciliation: reviewed root `proof1.txt` (SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`) and `proof2.txt` (SHA `ba4d1c0faf9acbce836ffc5e16740b197e4c7bbe`), issue #3 including LSPV-5/505 and LSPV-1/592, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, relevant LSPV-4/539–549, /560–562 and handoffs, peer LSPV-2/576 and LSPV-3/589, and the exact /386 checker source. Earlier LSPV-4/539 already proves a **logical-charge-only** source-preserving clause/facet quotient for this restricted parser; /560 already proves the 82/883 **pre-step** no-recomputation minima; /562 already exhibits the 71/748 **post-step** recomputation minima. The contribution here is the corrected **same metric** comparison and its joint-vector non-dominance consequence. No result is silently presented as a new SAT lower bound.

## Exact theorem: pre-step to post-step accounting

Let \(G\) be the pinned 35-node paid-RES DAG with paid-node set \(V\), unique terminal node \(z=34\), and \(C_z=[]\) of exact canonical JSON length \(|\mathrm{JSON}(C_z)|=2\). Every other paid node has a successor and, by finite DAG acyclicity, eventually reaches \(z\). Source clauses and facets are read-only and excluded from the following *derived-result register* proxy. All 35 paid RES identities must be executed once in this comparison. There are four output registers, no recomputation, free post-consumer deletion and nonexpanding overwrite of a last-used paid parent.

For a topological schedule \(\sigma=(v_1,\ldots,v_{35})\), put \(D_i=\{v_1,\ldots,v_i\}\), \(D_0=\varnothing\). Define its genuinely needed resident paid outputs

\[
L(D_i)=\{u\in D_i:\exists w\notin D_i,\ u\in\mathrm{Parents}(w)\}.
\]

The previous /560 dynamic program minimizes the **pre-execution** areas

\[
A_{\rm pre}=\sum_{i=0}^{34}|L(D_i)|,\qquad
B_{\rm pre}=\sum_{i=0}^{34}\sum_{u\in L(D_i)}|\mathrm{JSON}(C_u)|.
\]

In the **post-execution** convention used by /562, keep the produced output at each post-step checkpoint; release every previous result after its final use and before the checkpoint. Since every nonsink node is terminal-live up to its last consumer, the first 34 post-step checkpoints are exactly \(L(D_1),\ldots,L(D_{34})\), and the last checkpoint has the just-computed empty sink as its single resident. Hence **for every valid no-recomputation schedule** in this graph,

\[
\boxed{A_{\rm post}=A_{\rm pre}+1,\qquad
B_{\rm post}=B_{\rm pre}+2.}
\]

The capacity and permitted overwrite conditions do not change under this time-index shift, so the optimal no-recomputation post-step values are \(83\) slot-steps and \(885\) canonical clause-byte steps, not 82 and 883. This does **not** invalidate the earlier theorem, which used its own pre-step definition.

An independent operating-system Python order-ideal Dijkstra searched **6,888 states and 18,789 legal transitions** under four nonexpanding registers. Both slot-first and byte-first objective runs obtained \((A_{\rm pre},B_{\rm pre})=(82,883)\). The post-step theorem then gives the exact \((83,885)\) result. The matching witness is in the newly published executable.

## Exact joint-vector non-dominance

The LSPV-4/562 published 36-step witness passes a separate original-record parent-availability check and a new independent resident-set validator, which sums its 36 post-step resident sets to \((71,748)\), including the final two-byte empty clause. The two *same-realization* restricted cost vectors are:

| Fixed signed proof DAG, 4 nonexpanding registers | Paid RES executions | Paid owners | Native work \(W\) | Post-step slots \(A\) | Post-step clause-bytes \(B\) |
|---|---:|---:|---:|---:|---:|
| Best schedule executing every paid identity once | 35 | 3 | **38** | **83** | **885** |
| Valid schedule recomputing RES 0 once | 36 | 3 | **39** | **71** | **748** |

One additional paid deduction therefore reduces the simultaneously achieved retained-slot area by **12/83 = 14.46%** and clause-byte area by **137/885 = 15.48%**. The two realizations are not componentwise ordered: \((38,83,885)\) and \((39,71,748)\) each win on a different resource axis.

**Corollary (restricted abstraction firewall).** An abstract normalizer that maps *every* repeated signed-RES occurrence to one earliest occurrence and retains this same 35-inference dependency DAG may decrease logical work from 39 to 38, but cannot promise to decrease both paid work and post-step retention costs: every no-recomputation schedule on this fixed graph incurs at least (83,885), which exceeds (71,748). If the concrete 36-step recomputation path must be included with an abstract cost **componentwise no greater** than its concrete vector, the abstraction must represent the paid extra epoch or introduce an independently proved, cheaper alternative realization. Simply erasing the second occurrence violates that proposed joint resource simulation. This is **not** a general impossibility theorem for arbitrary alternate proof graphs or representations.

The qualifier is essential: source-equivalent alternative clauses, different source-bound proofs including the previously accepted W29 proof, a full GF(2) shortcut, extension variables and branching may all evade the fixed-DAG bound. Conflating an ideal minimum \(W_R(F)\), actual proof discovery, and certificate verification would be invalid.

## Operation ledger and verification boundary

| Authenticated /386 operation | Logical tariff | Further resource obligations not included in \(A,B\) |
|---|---:|---|
| Original signed SOURCE | 0 | Explicit source bytes, provenance checks, read-only retrieval, addresses |
| Global paid AND2 owner | 1 once per declared owner | Owner tuple, wire freshness, dependency validation, storage |
| True defining DEF facet | 0 additional | Literal bytes, owner lookup, parent/facet retrieval |
| Strict signed RES execution | 1 **per execution**, including recomputation | Two parent-index reads, pivot, output clause, sequential checking, temporary buffers |
| Parent reuse of already retained paid result | 0 new logical inference | Reference/application and retrieval costs; no second creation charge |
| Deletion/overwrite | 0 in this restricted abstract proxy | Physical movement and peak scratch memory are not thereby zero |
| AND3, GF(2), LOCAL-CONVERT, source/export/private wire scopes, branch/weakening/discharge/joins | **UNAUTHENTICATED TOGETHER** | Preserve historical grammar and weights; no invented tariffs |

The archived /386 original checker materializes the complete input `dat.records` and `known[]`, and its CLI executes eleven corruption controls. The four-register derived-result experiment does not prove a four-register physical-memory bound for that implementation. The byte arrays here are only canonical JSON clause-array payloads, not complete certificate bytes or parsed-object footprints. A cheap GF(2) or conservative extension proof cannot be priced until the full historical \(R_{\mathrm{mix341}}\) parser and original fixed weights are recovered.

## Reproduction and literature

- Executable: [`experiments/arc/lspv4_563_joint_epoch_firewall.py`](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_563_joint_epoch_firewall.py). Self-contained Python 3. Exact no-recomputation Dijkstra, both objective orders, and 36-step independent resident replay. It enforces every paid predecessor and every nonexpanding overwrite. No stochastic sampling. Original OS Node replay of these previously published packets is **not** claimed in this run.
- Raw results: [`results/raw/arc/2026-11-12_0736_LSPV4_563_JOINT_EPOCH_COST_FIREWALL_RAW.json`](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0736_LSPV4_563_JOINT_EPOCH_COST_FIREWALL_RAW.json). Independent Python DP and JS tool-side replica of resident checks were run during this investigation; the standalone newly published file still requires separate repository-root preflight and CI execution.
- Primary references: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44 (1979), 36–50, DOI [10.2307/2273702](https://doi.org/10.2307/2273702); Nordström, *Pebble Games, Proof Complexity, and Time-Space Trade-offs*, LMCS 9(3) (2013), DOI [10.2168/LMCS-9(3:15)2013](https://doi.org/10.2168/LMCS-9(3:15)2013); Cousot and Cousot, *Abstract Interpretation: A Unified Lattice Model*, POPL 1977, DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973). These works motivate formal distinctions between proof size, space, and abstractions but do not imply the new finite numeric result or historical mixed-rule transfer.

## Status, tracker materiality, next test

Affected IDs: **[P2-C3]** (concrete-step inclusion and componentwise resource non-overcharge), **[P2-D1]** (restricted authenticated grammar only), **[P2-B1]** (no all-proof minimum transfer). All remain **OPEN**, as do separate **[P2-B2/B3]**, **[P1-01/P1-03/P1-04]**, and **P versus NP**. No theorem closure or change to either root proof tracker is warranted: **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

Next role-A experiment: enrich the abstract state with paid **execution epochs**, per-consumer retrieval/application bits, and cumulative retention under a *single consistent checkpoint convention*. Then try a checker-accepted mixed GF(2)/AND3 proof only after full historical operation authenticity is established, retaining alternative proof-graph shortcuts in every lower-bound claim.
