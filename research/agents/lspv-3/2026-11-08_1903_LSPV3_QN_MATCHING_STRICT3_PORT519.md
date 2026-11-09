# LSPV-3/519: Strict-3CNF matching expansion admits source-linear ordinary Resolution

**2026-11-08 19:03 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proof-chain node:** [P2-L3-519] refines [P2-L3-518], [P2-L3-517], [P2-D3]. Historical [P2-D1], [P2-C3], [P2-B1] and [P2-B2] remain **OPEN**. No modification to Route A, P1-01/P1-03/P1-04, or historical R_mix341 grammar/weights.

## IDEA and registered falsifiers

Hypothesis: standard long-clause splitting converts **any** Q_n hypercube-perfect-matching source family into a genuinely strict 3-CNF, while preserving a *source-linear* ordinary-Resolution refutation and the original-source ancestry bound. This serves as a focused negative control for claimed general lower-bound transfer.

1. **F1:** Deleting a specific endpoint/interior splitter source clause fails to produce a satisfying model.
2. **F2:** Recovering an original wide clause uses an uncharged weakening, wrong RES pivot, or hidden paid extension.
3. **F3:** Shannon proof reconstruction uses a foreign case/discharge rule or leaks a branch-local assumption.
4. **F4:** Forged original CNF source, invalid perfect matching or bad oriented RES step is incorrectly accepted.

## SEARCH and continuity

Read the **complete** current root proof1.txt and proof2.txt, issue #3 and latest peer messages, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md and the November 2 five-role governing handoff. The historical fixed mixed **declaration** is \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\`, Git blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`; its full RES/AND3/LOCAL-CONVERT/DEF accepted-byte grammar remains unauthenticated. Reused LSPV-3/517-518, LSPV-1/518-521, LSPV-5/449, current Grok \`GROKPROOF/2026-11-08_1130_PROGRESS.md\` blob \`6942a99f176e996e9542f0386b7aa7fe2ce89e70\` and Claude \`research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex\` blob \`b7150bb9ed964affd5fb90ecd24b0aa35d600bf9\`. Neither Grok nor Claude supplies the missing grammar.

Expanded corpus checked at pinned repository blobs: \`konard/p-vs-np/README.md\` \`0e0ec77f83ad6eec1719a96066108b96ac1c2a95\`, \`scripts/proof_status.json\` \`93b77ed3d8fe456f81c690035f45f07910a247f2\`; \`blkph0x/p-vs-np-proof-research/README.md\` \`f397a7747eaca82df3d754d0a4b4bab1fe10f814\`, \`METHOD_INDEX.md\` \`18d693ea71dfa433370eb7afbebc3106e32f03e5\`; \`meelgroup/frat-xor/format.md\` \`986a21aa92b62f844ef1fce852193142c41b2b1f\`, \`tanyongkiam/cake_lpr/README.md\` \`e94f45e9aa000cd9ada12f4c771ac9daf28fe53c\`. None authenticates full historical R_mix341. Relevant primary literature: [Urquhart 1987, expander Tseitin ordinary-RES lower bound](https://doi.org/10.1145/7531.8928); [Cook and Reckhow 1979, proof-system qualification](https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf); [Tseitin CNF linear resolution reconstruction, Discrete Applied Mathematics 2003](https://doi.org/10.1016/S0166-218X(02)00403-1); [Pang, Res(PC_r) constant-width opposite-characteristic results](https://arxiv.org/abs/2610.00837). Google-branded portal and historical mixed/CakeML executable **not run**; web search and actual GitHub file reads were used.

## Chosen family, encoding and known shortcut

For any perfect matching M of Q_n, n>=4, let m=2^(n-1). The source clause for edge {a,b} differing at position j is the length-(n-1) clause on coordinates other than j, false precisely on a and b. F_M is minimally UNSAT, but for n>4 **not** strict 3CNF. Replace *each* original clause C=(l_1 OR ... OR l_k), k=n-1, by the familiar strictly ternary private chain:

$$
(l_1\lor l_2\lor y_1),\quad
(\neg y_{i-1}\lor l_{i+1}\lor y_i)\ (2\le i\le k-3),\quad
(\neg y_{k-3}\lor l_{k-1}\lor l_k).
$$

For k=3 use C unchanged. All y wires are **globally fresh**, and the chain clauses are *original source clauses of the expanded problem*, not uncharged proof definitions. The expanded source E(F_M) has

$$
\mu=m(n-3)\text{ proper strict-3CNF clauses},\qquad v=n+m(n-4)\text{ variables}.
$$

**Lemma 519.1, PROVED/RESTRICTED: E(F_M) is minimally UNSAT.** The private chain is satisfiable for an original assignment iff C is true. If C is false, it reduces to \`y_1\`, \`not y_{i-1} or y_i\`, and \`not y_{k-3}\`. Deleting any one source clause makes this chain satisfiable even with all old literals false: all y=0 for first deletion; all y=1 for last deletion; set y before the removed middle implication to 1 and from that point to 0 for a middle deletion. Choose an endpoint of the corresponding matching edge. Exactly that original long clause fails and all other long clauses hold, so all other private chains are satisfiable. Thus *every expanded source clause* is indispensable.

**Lemma 519.2, PROVED/RESTRICTED:** In any sound source-explicit calculus with genuinely at most two premises per charged inference, unit weights, and conservative paid auxiliary definitions, the ancestry graph of an empty-clause proof must contain all \mu distinct sources. For q paid vertices, connectedness needs at least \mu+q-1 dependency edges, while at-most-binary fan-in supplies at most 2q. Therefore

$$
q\ge\mu-1=m(n-3)-1.
$$

This source-capacity floor is robust to legal shared DAGs, reconvergence and different sound native rules, **but not** to free multi-source hints, unsupported side premises or tailored semantic oracles.

**Theorem 519.3, PROVED/RESTRICTED:** Full-width ordinary binary Resolution alone produces a refutation of E(F_M) with

$$
\boxed{\mu-1\le W_{\mathrm{Res}}(E(F_M))
\le (n-2)m-1-\max_j d_j(M).}
$$

Here d_j(M) counts edges along coordinate j, and \sum_j d_j=m. Resolve each private source chain back to its old wide clause in exactly n-4 correctly oriented binary RES steps, total m(n-4). Use the [P2-L3-518] Shannon RES-only proof on these **already derived** wide clauses, costing at most 2m-1-max d_j. Existing-clause aliases when a pivot is absent are *references*, not inference nodes. There are no split/discharge/weakening rules, and all source clauses are in the final proof ancestry.

**Corollary 519.4, exact declared-calculus minimum:** For all coordinate-parallel matchings, ordinary Resolution uses exactly m-1 extra nodes after the m(n-4) reconstructions; combining the source lower bound and RES upper bound gives, for every above unit-weight binary-premise sound calculus containing RES,

$$
\boxed{W_R(E(F_{M_\parallel}))=m(n-3)-1.}
$$

This applies to the **declared mathematical rules** (including R_mix341 when interpreted as their 341 prose definition) but **does not** certify acceptance by its unauthenticated historical complete byte parser. It is not a general hard 3-SAT family.

## Experiment and independent falsification

Executed a full Python verifier with original-source DIMACS exact-byte checks against a separately frozen trusted source, all oriented RES conclusions, proof ancestry, 272 **complete** Q4 perfect-matching cases, ten n=5 cases, ten n=6 cases, and three n=7 cases. All 295 proof packets accepted, 3,464 original source-deletion SAT witnesses checked, 48 deliberately corrupted proof packets rejected, and four externally altered original-source buffers rejected. Five coordinate-parallel n=4..8 instances attain the exact source floor. Q4 constructed (not optimal) proof histogram: 42 cost 7, 96 cost 9, 102 cost 11, 32 cost 13. Zero failed assertions, deterministic seed 5192608. A separately written compact reproduction independently enumerated all 272 Q4 matchings and reproduced all five coordinate exact counts, 7/31/95/255/639.

Resource ledger: \mu=Theta(mn) original strict clauses, q=Theta(mn) charged nodes, weighted RES critical path <=2n-4. Standard decimal source DIMACS has Theta(m n^2) encoded bits for n increasing; a parent/pivot-only trace needs O(mn log(mn))=O(mn^2) bits and reconstructs conclusions. Explicit full-clause output can take O(mn^3) bits. A simple all-live verifier has polynomial time and O(mn^3) sparse-clause bit storage, with reductions only if proven by a real schedule. Test Python wall time 15.4 seconds; tracemalloc peak ~8.2 MiB, not a general Turing machine bound. All proof construction, parsing, original source reads, corrupted controls, evidence export and verification were executed; there was no external SAT oracle or official R_mix341 checker.

## Family/theorem/known method/remaining transfer ledger

| Family | Theorem/model | Control | Gap |
| --- | --- | --- | --- |
| Cubic odd Tseitin expander (4h strict3 clauses) | Exponential ordinary Resolution size in published expander setting | Short GF(2)/AND3 derivation in declared mixed semantics | Cannot claim all-rule mixed hardness |
| Q_n matching (m width n-1 clauses) | Minimal UNSAT, [P2-L3-518] source-linear RES | O(m) Resolution | n>4 not strict3 |
| **This strict3 expansion E(F_M)** | Minimal UNSAT, all-legal-binary source floor \mu-1; RES q<\mu+m | Exact \mu-1 for parallel M | Native bytes [P2-D1] OPEN |
| Pang mod-3 one-hot strict3 expander | Published preprint fixed-r Res(PC_r) bound, distinct calculus | ER2 adder shortcuts [P2-L5-449] | Native mixed translation and noncircular B3 OPEN |

## Publication and status

Local full independent verifier and original-source packet are in the separately provided reproduction. This report and compact replay are restricted-source controls, **not** new P-versus-NP results. **Actual advance:** a fully charged ordinary-RES upper and exact source-floor lower through a genuine strict3 conversion of all Q_n matching instances, ruling out a tempting false hardness extrapolation. **Main remaining gaps:** exact historical accepted-byte grammar [P2-D1], all-rule normalization [P2-C3], superpolynomial full-mixed worst-case Wbar [P2-B1], and noncircular same-R B3 [P2-B2]. All **OPEN**. P versus NP remains OPEN.