# LSPV-4/573: Exact byte-weighted retention under two-register scheduling for the original /341 proof trees

**November 12, 2026, 17:36 PST (America/Los_Angeles) | LSPV-4 Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED finite fixed-DAG optimum, independently executed Python and hosted-JS semantic replay | P versus NP OPEN.**

## Candidate theorem, precise model, four attempted falsifiers

**Candidate.** The previously proven minimal *unweighted* two-register DFS schedule in LSPV-4/572 need not minimize *byte-weighted* cumulative retention when the live derived value is represented by its complete compact JSON paid-node record. Determine the exact minimum of this representation-specific byte-step area for each of the seven unchanged original /341 SOURCE/AND3/XOR proof DAGs. This is a **retained-record serialization proxy**, not live JavaScript heap bytes, a lower bound on encoded semantic information, or the historical full mixed-calculus cost.

F1: The earlier /572 DFS schedule minimizes both atomic-slot area and record-byte area. **FALSIFIED** by three exact original DAGs: Petersen (6760 to 6751), Prism6 (8220 to 8211), Prism16 (23869 to 23836).

F2: A reordered source-backed schedule breaks a signed original AND3 or XOR deduction. **Not found:** independent direct truth-table/affine-row replay passed all 321 reordered paid nodes over seven unchanged signed source fixtures. The unmodified original OS checker for *these newly reordered* full packets has not yet run; a standalone reproducer is published.

F3: A two-live-atomic-register model implies at most two records are allocated during a fresh output. **FALSIFIED as a transfer:** if the new result is allocated before parent release, transient bytes are the pre-step retained record bytes plus new-result bytes, potentially including **three records**, even though only two results remain after the step. The exact fresh-output transient record peaks of the optimum schedules are 338, 338, 338, 344, 344, 360 and 339 bytes in fixture order. These are not measurements of physical RAM.

F4: This static schedule excludes recomputation, extensions, algebraic row compaction, shared lemmas, contexts and legal mixed rules, so it proves a general machine-space or paid-work lower bound. **Rejected as a scope error:** all such alternate routes remain admissible in P2-D1/C3/B1. Known affine GF(2) shortcuts are present in the original 75 XOR steps, but the unknown historical cross-rule GF(2) transitions are not authenticated.

## Corpus, primary authority and novelty discipline

Preflight corpus: both root trackers (root proof1 Git blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, root proof2 Git blob `f678f707880da4dfc97dabf778430c6dc816cb1f` recovered via Git blob after an empty contents fetch); issue #3 and current specialist comments; root AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; root main.tex ownership; current LSPV-4/572 and /539, /548, /549, /571; LSPV-2/585 and LSPV-5/513 current handoffs; original /341 source, checker and result packet, distinct /386 sibling and historical mixed-rule counterexamples. The 539-549-era resource work already treats slot/byte nonexpansion as separate coordinates. This report does not relabel that prior work as new.

Original pinned accepted-source fixture packet: `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`.
Original unchanged recovered /341 checker: `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. It recognizes SOURCE, AND3 and XOR for seven fixture graphs, **not** Resolution/LOCAL-CONVERT/DEF/branch joins in a historical unified R_mix341 checker. The distinct /386 checker cannot be merged by inference.

Classical Sethi-Ullman register ordering is acknowledged prior art [1]. Proof length versus space and pebbling tradeoffs are established topics [2,3]. The new contribution is **the finite, original-record-weighted optimum and its nontrivial disagreement with the existing slot-optimal DFS ordering**, not a new pebbling complexity theorem.

## Exact normalized-state theorem

Fix one original paid-DAG \(G=(V,E)\) with \(n=4H-1\) paid vertices and its original signed SOURCE leaves available read-only. Every nonsink paid result has exactly one consumer in these seven fixed templates. Every paid inference executes once. Immediately after its last application, a paid result can be deleted at zero logical charge. No extra inference nodes or modified semantics are allowed. The two-register constraint limits *post-step* live paid results to at most two, with last-use parent overwrite as in LSPV-4/572.

For each original paid node \(u\), fix the **representation** to its exact compact, ASCII JSON paid-node record, and let

$$
w(u)=\bigl|\operatorname{UTF8}(\operatorname{JSON.stringify}(u))\bigr|.
$$

For an executed order ideal \(S\subseteq V\), define its minimal live frontier, including the terminal sink,

$$
L(S)=\{u\in S:\operatorname{Succ}(u)\not\subseteq S\}\cup\{z:z\in S\text{ is terminal}\}.
$$

The precise retained-record byte-step objective is

$$
A_w(\pi)=\sum_{t=1}^{n}\sum_{u\in L(S_t)}w(u).
$$

**Theorem 573.1 (general recurrence and finite exact seven-fixture conclusion).** For every fixed acyclic paid DAG in this no-recomputation, immediate-freeing, fixed-record-byte model, the optimal two-live-result retained area satisfies the exact order-ideal recurrence

$$
D(\emptyset)=0,\qquad
D(S\cup\{v\})=
\min_{\substack{v\ \mathrm{ready\ after}\ S\\|L(S\cup\{v\})|\le2}}
\left[D(S)+\sum_{u\in L(S\cup\{v\})}w(u)\right],
$$

where each subset state is updated from **all** feasible predecessors. For the seven original /341 packets, evaluating this recurrence gives exactly the seven optimum byte areas in the table below.

**Proof.** Every legal no-recompute concrete schedule has a unique monotone sequence of topologically closed completed-node sets. Any paid result with a future consumer must remain available; retaining a last-used node adds nonnegative area and never helps, so canonical immediate deletion weakly improves cost. Thus the live frontier above is necessary and sufficient at each state. Every ready-node extension with no more than two live results is realizable by the declared atomic overwrite model (read the parents before last-use overwrite). Its cost increment is exactly the weighted live frontier after this inference. Dynamic programming over these acyclic order-ideal edges therefore optimizes over *all* legal topological orders, without counting an inference twice. This proves the recurrence and exactness of exhaustive enumeration. The finite numerical claims additionally use the two independently implemented full-state audits described below. \(\square\)

**Cost-soundness boundary.** For every concrete execution within precisely the declared model, the identity-of-completed-paid-vertices abstraction maps it to a legal abstract path of **equal**, hence no greater, retained-record area. It preserves the identical terminal goal and paid-node count. Dropping node identities or representation widths could overestimate the concrete cost; treating this specialized recurrence as an all-rule historical proof lower bound would instead underrepresent legal proof alternatives. The transient fresh-object peak is measured separately as \(\max_t(\sum_{u\in L(S_{t-1})}w(u)+w(v_t))\), **not** the physical verifier heap.

## Exhaustive findings

| Separate original fixture | Paid deductions | Reachable 2-slot ideals | Legal state edges | Producer byte-steps | /572 DFS byte-steps | New exact optimum | Fresh-output peak at optimum |
|---|---:|---:|---:|---:|---:|---:|---:|
| K4 | 15 | 79 | 132 | 4109 | 2452 | **2452** | 338 |
| K3,3 | 23 | 189 | 323 | 9184 | 3862 | **3862** | 338 |
| Cube | 31 | 347 | 598 | 16322 | 5272 | **5272** | 338 |
| Petersen | 39 | 553 | 957 | 25775 | 6760 | **6751** | 344 |
| Prism6 | 47 | 807 | 1400 | 37221 | 8220 | **8211** | 344 |
| Prism16 | 127 | 5987 | 10450 | 273783 | 23869 | **23836** | 360 |
| Bridged K4x2 | 39 | 553 | 957 | 25655 | 6724 | **6724** | 339 |

Both independently written algorithms agreed on every reachable-state count, legal-edge count and optimum. The native-record encoder was used as the authoritative weight source for hosted JS; the Python 3 independent program used separately extracted identical original weights and the fixed original tree dependency pattern. The Python program ran as an OS process and passed assertions on the seven numerical optima; the Node source-aware program was evaluated in hosted V8 and its independent arithmetic/signed semantic replay agreed. **The published original-CLI OS runner is not yet executed for these reordered packets.** No claim is made of its new original-OS acceptance.

For Petersen and Prism6, the first complete factor from vertex 1 occupies a three-byte-shorter original JSON record than the first complete factor from vertex 0, and Prism16's is eleven bytes shorter. Computing the second vertex's three-step chain first therefore saves exactly

$$
3\bigl(w(\mathrm{factor}_{0})-w(\mathrm{factor}_{1})\bigr)\in\{9,33\}
$$

over the DFS ordering, with unchanged \(7H-4\) minimum **atomic slot-steps**. The other original fixtures already achieve their exact byte area under /572's DFS ordering. A serial mathematical table/row byte cost and an atomic derived-value byte cost can give different rankings; even the complete-record proxy is not automatically equivalent to either.

The seven SOURCE fixtures comprise **321 paid distinct original inference occurrences**, namely 246 AND3 and 75 XOR, with **642 binary parent applications**. These are seven *separate* accepted tree proofs, not one joint 321-step refutation. Source, individual inference records, their parent IDs, paid work, critical-path dependency, and compact 77,714-byte JSON fixture-packet serialization are unchanged by the permitted record-array permutation. No globally paid owner or shared-node duplication is introduced.

## Remaining firewall obligations and exact P2 status

P2-D1 must still authenticate the real historical **single mixed** R_mix341 accepted-byte grammar and its original immutable weights. The original /341 and /386 sibling programs do not certify RES-to-AND3, paid DEF facets, LOCAL-CONVERT, private/exported wires, branching, weakening, discharge, joins, contexts or deletion opcodes in that unified system. P2-C3 requires a configuration/abstract-step theorem for all legal **shared** DAGs, all valid representational shortcuts, source checking, parent references and variable identifiers, all stages of writable memory, recomputation, direct GF(2), extensions and learned branch-compatible lemmas. P2-B1 requires a growing-instance lower bound against the **entire** authenticated rule system; P2-B2/B3 remain separate. The ideal \(W_R\) is not the complexity of finding a proof, the time of checking its certificate or a SAT decision algorithm.

The exact status is therefore **P2-D1 OPEN, P2-C3 OPEN, P2-B1 OPEN, P2-B2/B3 OPEN, P1-01/P1-03/P1-04 OPEN, P versus NP OPEN**. Neither root tracker contains a material new closure. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

## Executable, raw data, and replay provenance

- Exact original-packet Node checker and weighted DP OS runner: `experiments/arc/lspv4_573_native341_weighted_record_area.cjs`. The script pins the original checker/packet Git blob hashes, checks exact 77,714-byte compact packet length, executes original and reordered packets against the *unchanged* original Node CLI, and requires three forged packets to be rejected. **Its OS replay is an outstanding external test, not an already completed verification.**
- Machine-readable fixture weights, all 7 optimal orderings, state/edge counts, retention, peak proxies and independent-Python reconciliation: `results/raw/arc/2026-11-12_1736_LSPV4_573_NATIVE341_WEIGHTED_RECORD_AREA_RAW.json`.
- Five-role handoff: `research/coordination/2026-11-12_1736_LSPV4_WEIGHTED_RECORD_FIREWALL_FIVE_ROLE_HANDOFF573.md`.
- Corpus-wide Python preflight, the unchanged original-checker Node OS replay against new packets and independent physical-heap profiling remain **outstanding** because a full checkout was not available in the isolated execution environment. No checker code was altered.

## Primary literature

[1] R. Sethi and J. D. Ullman, "The Generation of Optimal Code for Arithmetic Expressions," *J. ACM* **17** (1970), 715–728. DOI: https://doi.org/10.1145/321607.321620.

[2] E. Ben-Sasson and J. Nordström, "Understanding Space in Proof Complexity: Separations and Trade-offs via Substitutions," ECCC TR10-125 (2010), https://eccc.weizmann.ac.il/report/2010/125/.

[3] E. Ben-Sasson and J. Nordström, "Short Proofs May Be Spacious: An Optimal Separation of Space and Length in Resolution," ECCC TR09-002 (2009), https://eccc.weizmann.ac.il/report/2009/002/.
