# LSPV-5/454: independent audit of the K4 174-RES packet and 69-source minimum

**2026-11-09 00:29 PST | Route B, LSPV-5 independent red team | COMPUTATIONAL finite replay plus PROVED/RESTRICTED source-cover reasoning | P versus NP OPEN**

**Tracker result:** `TRACKERS REVIEWED; NO MATERIAL CHANGE`. The audit independently confirms existing [P2-L3-527], [P2-L1-528], [P2-L3-522] and the scoped binary-source implication [P2-L5-452]. It does not change [P2-D1], [P2-C3], [P2-B1] or [P2-B2], all of which remain OPEN. Route A [P1-01], [P1-03], [P1-04] and cross-chain [P1-X1] remain OPEN.

## IDEA: hypothesis and precommitted falsifiers

**Initial hypothesis.** The complete JSON packet behind [P2-L3-527] is a genuine source-authenticated signed binary-Resolution refutation of the exact 78-clause K4 modulo-three strict 3-CNF, and its 70 live source leaves form a self-contained UNSAT source subset. Independently, the compatibility/spectral argument reported in [P2-L1-528] certifies the already-known 69-clause minimum source core of [P2-L3-522], rather than merely exhibiting one small core.

The four falsifiers fixed before implementation were:

1. a SOURCE record outside, duplicated within, or missing from the exact 78-clause source;
2. a forward/cyclic parent, false signed pivot, mutated resolvent or nonempty root;
3. a mismatch in root ancestry, live-source count, reference count or critical depth;
4. a Boolean model of the claimed 69-clause core, a missing deletion witness, a compatibility pair without a deletion witness, or a spectral/vertex-cover calculation that fails to prove the lower bound for every UNSAT source subset.

No falsifier fired. The revised conclusion is deliberately narrow: the result is an independent finite audit and source-cover certificate, not historical accepted-byte R_mix341 authentication, not an all-rule proof lower bound, and not B3.

## SEARCH: exact project and primary sources

Both live trackers were read completely. The run began from `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `2797e7a03ec27a60ece75f61f9ca672d268b0dca`. Before any tracker decision, main was refetched: proof1 remained at the same blob while proof2 had advanced to blob `98d1e6df14f43fe359f649ac79506731526a3e32`, containing concurrent [P2-L1-528]. That conflict-safe reread is why no duplicate tracker entry was written.

Actual governing/project material read included:

- `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, current blob `c3889a3e514ddbd747150dcb68607013a3b2d154` (historical requested commit remains `4e29ed7646f484707767acb6e63ec5f38afd98a8`);
- current issue #3, `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, and `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f` plus its mode/protocol references;
- actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md`, blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`, and actual Claude `research/agents/claude/world-ledger/README.md`, blob `de75a371ce3143a4495e6892df7fb04794a6b708`;
- [P2-L3-527] report `research/agents/lspv-3/2026-11-08_2352_LSPV3_K4_RES_UPPER_IMPROVEMENT527.md`, blob `af89fb597abe341772e8804b3aeafc414dd72090`; generator `experiments/arc/lspv3_527_k4_res_better_upper.cjs`, blob `ff0d0f1251363dfd1537f2dcaff4ecc664de36f7`; complete packet `results/raw/arc/2026-11-08_2341_LSPV3_527_K4_RES_IMPROVED_RAW.json`, blob `3f3df06ec0338b065910d468fd006d9fa414014e`; and handoff blob `65fc05f5f4d7da1c8747e09d667a920dc5d41577`;
- [P2-L1-528] report `research/agents/lspv-1/2026-11-09_0010_LSPV1_PAIR_DEFECT_SPECTRAL_SOURCE_COVER528.md`, blob `bd28f451704486a42bc8d2e88cb2867a9d41ceb8`; V8 checker blob `ffb7f2ba782890791cfd937349998a6f5aef3584`; raw blob `5973f96275b727ef026613053a03bdff768fb0aa`; and handoff blob `0c83a20b66bc14a5de46a07e047e94e3ddbeff5d`.

Primary-source queries were `Hoffman ratio bound independence number regular graph least eigenvalue original paper`, `Shuo Pang A Degree-Size Relation for Resolution over Polynomials Theorem 7.2 Tseitin`, `Haken intractability of resolution pigeonhole principle 1985`, and `Cook feasible constructive proofs extended resolution 1976`. Haemers, *Hoffman's ratio bound*, Linear Algebra Appl. 617 (2021), 215-219, DOI `10.1016/j.laa.2021.02.010`, explicitly records that Hoffman did not publish the ratio bound and supplies its history. The bound used here is $\alpha\le n(-\tau)/(d-\tau)$ for a $d$-regular graph with least adjacency eigenvalue $\tau$. Pang, arXiv:2610.00837v2, Theorem 7.2(b), gives $\exp(\Omega(N))$ size only for fixed-$r$ $\operatorname{Res}(\mathrm{PC}_r/\mathbb F_p)$ refutations of fixed-prime-$q\ne p$ Tseitin formulas on fixed-degree regular expanders; its lines are DAG nodes in that stated syntactic system. Haken's 1985 result is ordinary Resolution on pigeonhole formulas; Cook's short ER controls show extension rules can change proof size. Publisher page opens for Haemers, Haken and Cook failed with 403/redirect restrictions; indexed metadata and the accessible arXiv HTML were used. A separate Google-branded interface was unavailable and was not claimed.

Required change-aware repository review found no head changes relative to the pinned prior inventory:

| Repository | Current head | Exact material reviewed | Relevance |
| --- | --- | --- | --- |
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | `README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`; `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` | finite-machine P-subset-NP formalization; NP-subset-P open; no R_mix341 source authentication |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | `README.md` blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` | bounded/promise exact results and scoped barriers; no general SAT separation |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` | provisional FRAT-XOR/XLRUP interface; not native historical mixed grammar |
| `peitl/short-proof` | `2c524cfceecf68b56f51d23f6b63255b502856d3` | `README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab` | bounded SAT encodings for shortest Resolution proofs; no global optimum was inferred |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | `README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` | verified checker toolchain and trust boundary, not historical R_mix341 |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | `README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` | raw research artifacts with mixed verification status |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | `eth/README.md` blob `0b3dcf4a858ff802b3275fc5999ffb134c74de60` | separate claimed subexponential #3-SAT formalization; no imported theorem or automatic authority |
| `MassimoLauria/cnfgen` | `24e633bdbed0d0998493bee99c42faf480c7dc96` | repository inventory and `README.org` blob `9fba4e26f2a4cd10444a7226a7a3a7caa1762721` | established benchmark-generator control; no use as proof of hardness |

## Family/theorem/encoding/known-method/remaining-transfer ledger

| Item | Exact scope |
| --- | --- |
| Family instance | K4, vertices 0,1,2,3; six lexicographically ordered edges; charge vector $(1,0,0,0)$ over $\mathbb F_3$ |
| Exact 3-CNF | 18 Boolean atoms $x_{e,a}$; six positive ALO clauses $(x_{e,0}\vee x_{e,1}\vee x_{e,2})$; for each cubic vertex, 18 negative three-literal clauses excluding incident label triples with signed sum unequal to its charge; total 78 proper width-three clauses |
| Certified status | UNSAT by complete source-authenticated Resolution packet and by exhaustive Boolean check; finite instance only |
| Established family lower bound | Pang Theorem 7.2(b): exponential DAG-node size in fixed-$r$ $\operatorname{Res}(\mathrm{PC}_r/\mathbb F_p)$ for fixed $q\ne p$ on fixed-degree regular expander Tseitin families, under the theorem's encoding/simulation assumptions |
| Known shortcuts actively allowed | ordinary shared-DAG Resolution, paid ER/extension definitions, GF(2)/affine rules, learned lemmas, reconvergence and any other legal historical rule; the 174-node packet uses only original SOURCE plus binary RES |
| Remaining transfer | authenticate exact historical byte grammar and source identity [P2-D1]; prove a polynomial normalization covering every legal mixed rule [P2-C3]; prove a superpolynomial minimum across all mixed rules [P2-B1]; or prove noncircular same-calculus B3 [P2-B2] |

Certified UNSAT, minimum source-subset size, ordinary-Resolution upper size, restricted-system asymptotic hardness, and empirical solver work are separate facts throughout.

## ITERATE: independent trace replay

The new Python audit reconstructs all 78 clauses without importing either peer generator. For every one of the 252 packet records it canonicalizes signed literals, verifies unique original source membership, requires two earlier parents for each RES line, checks the opposite signed pivot and recomputes the exact resolvent. It then traverses the dependency DAG backward from record 251.

The independently reproduced metrics are:

| Metric | Result |
| --- | ---: |
| SOURCE records | 78, exactly the source once each |
| RES records | 174 |
| Root | record 251, empty clause |
| Live root ancestry | 244 records |
| Live original-source leaves | 70 |
| Live paid RES nodes | 174 |
| Premise references in live ancestry | 348 |
| Unit-inference critical path | 16 |
| Maximum clause width | 6 |
| Literal occurrences in all records | 949 |
| Omitted source indices | 7, 10, 18, 21, 22, 31, 32, 34 |

Five hostile mutations were independently rejected: forged source, future parent, false pivot, mutated resolvent and nonempty root. This is replay of the published JSON semantics, **not** execution of an authoritative historical R_mix341 byte parser. There are no branch assumptions, case-split discharge rules or weakening rules in this packet. Sharing is charged exactly once by counting the union of distinct live RES nodes; references are counted separately. The packet therefore witnesses only

$$W_{\mathrm{RES}}(F_{K_4,3})\le174.$$

It neither proves that 174 is minimum nor excludes a shorter ER, affine or other mixed proof.

## Independent source-minimum argument

The audit enumerated all $2^{18}=262{,}144$ Boolean assignments and indexed each exact set of violated source clauses.

1. All six ALO clauses and all 36 `E`-type forbidden clauses have a witness satisfying the other 77 sources. Hence every UNSAT source subset must retain these 42 clauses.
2. On the 36 `R` clauses, join two clauses when one Boolean assignment violates exactly that pair and no other source. The audit found 162 edges and stored an explicit assignment witness for every edge. Therefore the retained R clauses of any UNSAT subset form a vertex cover of this compatibility graph.
3. The 36-by-36 symmetric integral adjacency matrix is 9-regular and satisfies exactly

   $$A(A-9I)(A-3I)(A+3I)=0.$$

   Exact rational row reduction gives multiplicities $-3:15$, $0:8$, $3:12$, $9:1$. Hoffman's ratio bound gives $\alpha\le36\cdot3/(9+3)=9$, while the nine R clauses at one K4 vertex are an explicit independent set. Thus $\alpha=9$ and every vertex cover has at least 27 vertices.
4. Every UNSAT source subset therefore has at least $42+27=69$ clauses. Omitting all nine R clauses at vertex 3 gives a 69-clause UNSAT core; exhaustive checking found no model and explicit witnesses for deletion of each of its 69 clauses.

This independently validates the pre-existing [P2-L3-522] minimum and [P2-L1-528]'s K4 spectral control. It does not add a new exact minimum. For any sound **source-explicit, at-most-binary-premise** refutation DAG whose root depends on an UNSAT source subset, a connected dependency graph with $r$ source leaves needs at least $r-1$ paid binary joins. Thus the scoped finite lower bound is 68. This is [P2-L5-452]'s model-specific source-capacity argument, not an unconditional lower bound for every rule or byte interpretation in historical R_mix341.

The general [P2-L1-528] block proof was also challenged. For a simple 3-vertex-connected cubic graph, deleting two vertices leaves the remainder connected, so the incidence map over $\mathbb F_3$ extends any compatible two-defect boundary data. Nonadjacent blocks are $J_9$; adjacent blocks are three $K_{3,3}$ blocks. The reported real-function decomposition into constants, incident-coordinate subspaces and the residual space is dimensionally exact. No counterexample was found, but this run's executable certificate is the finite K4 instance; it does not substitute finite sampling for the general proof.

## Resource and trust ledger

- Logical evidence: 174 live RES nodes, 70 live source leaves, 348 live premise references, span 16.
- Explicit local evidence: audit source 12,332 bytes, SHA-256 `4fb7de8101cfeb7eea1f57744b4b1c85ab27536250541bc6f9cdc5eccfe51f74`; JSON result 9,914 bytes, SHA-256 `5141c79562d30bd5884763123826fd597c0860121ffa0b493dde808142025a75`.
- Implemented checking: source construction, JSON parsing, clause canonicalization, 174 exact resolution checks, root traversal, five corruption replays, 262,144 Boolean assignments, exact compatibility construction, 36-by-36 integral products and rational ranks. Host wall time recorded inside the run was 20.3301 seconds; maximum resident set was 56,720 KiB. These hosted measurements are not a native-machine asymptotic bound.
- Discovery/search: project and web reads, failed publisher opens, report drafting, remote transport and publication are not included in that wall/RSS figure. The ideal $W_R$ minimum intentionally excludes discovery cost; an implemented solver would have to charge it.
- The LSPV-3 optimizer's published 5,169-order search cost (21.12 seconds, 68,340 KiB) was inspected but not rerun; it is an upper-bound construction cost, not proof of optimality.
- Local preflight could not treat the scratch directory as a complete repository checkout: root `main.tex`, `AGENTS.md`, `CODEX.md` and the repo skill were absent locally. Authoritative GitHub blobs were read instead. The GitHub connector continued to return root `main.tex` as an empty readable body with blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba`; it was not edited. This report is the durable role-owned fallback.

## Status, publication, and precise remaining gap

**Actual advance:** a new independently authored replay validates every line of the best published 174-node finite K4 Resolution upper packet, rejects five adversarial corruptions, and emits all deletion/compatibility witnesses plus exact rational spectral multiplicities for the 69-source minimum argument. The evidence strengthens confidence in existing finite controls but does not materially change either tracker.

**Publication artifacts:** `experiments/lspv5_454_k4_independent_audit.py`; `results/raw/arc/2026-11-09_0020_LSPV5_454_K4_INDEPENDENT_AUDIT.json`; this report; and the accompanying five-role handoff. Full GitHub blob/commit/readback receipts are recorded after publication.

**Precise remaining gap:** no authenticated complete historical R_mix341 accepted-byte checker or exhaustive native-rule grammar has been recovered; no normalization covers all extension, GF(2), LOCAL-CONVERT, exported/private-wire and Resolution combinations; no published established family has a superpolynomial lower bound transferred through every such rule; and no noncircular argument proves SAT in P implies polynomial $\overline W_R$ for this same fixed calculus. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. P versus NP remains OPEN.
