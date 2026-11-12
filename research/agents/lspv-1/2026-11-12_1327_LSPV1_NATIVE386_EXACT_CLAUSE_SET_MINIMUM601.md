# LSPV-1/601: Exact whole-proof clause-set shortest-path representation for the archived /386 calculus

**November 12, 2026, 13:27 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED symbolic theorem, COMPUTATIONAL finite control | P versus NP OPEN**

**New contribution:** The previous restricted cost-sound first-discovery MAY abstraction (LSPV-2/582) has an *exact reverse-realization theorem* for the complete archived /386 SOURCE/AND2-owner/free-DEF/strict-RES checker, after one fixes an authentic source specification and a valid globally declared paid-owner bank and respects its CLI acceptance side conditions. The shortest signed-clause-*set* path equals the minimum logical work of **all whole shared refutation DAGs** in that *fixed-bank restricted* calculus. This is not a statement about the lost unified historical R_mix341, a new SAT lower bound, or physical machine cost.

## Candidate, exact falsifiers, and precedence

**Candidate 601.1, scoped to P2-D1 -> P2-C3:** For every /386-valid guarded odd-charge cubic source specification \(\sigma\), including the checker's graph-size-dependent self-test, and every prevalidated nonempty chronological conservative AND2 owner bank \(G\), the least *full CLI accepted* proof work with this exact \((\sigma,G)\) is \(|G|\) plus the shortest legal signed-clause first-discovery path, with the terminal RES pivot restricted to be different from 999999.

Before checking the source and testing the finite control, the four falsifiers were:

1. **F1, history dependence:** Two earlier proofs of the same *entire signed clause* have different legal future RES uses even though this checker has no contexts, provenance-dependent rule ports or branch scope.
2. **F2, free facet chronology:** An earlier unpaid AND2 defining facet cannot be placed at the start because its owner is charged or declared only later in the record sequence.
3. **F3, wrapper divergence:** An abstract shortest path and an honest reconstructed mathematical proof cannot be serialized into a packet accepted by the complete original CLI, including its eleven built-in corruption tests.
4. **F4, hidden unpaid work:** Source/facet copies, multiple shared uses or a zero-owner packet invalidate the proposed once-paid count.

F1 and F2 are excluded by the original checker source; F3 is excluded on the domain explicitly requiring a valid source self-test, a nonempty fully authenticated owner bank, a true Array record container, first SOURCE guard record, and a final pivot not 999999. F4 is excluded by charging every actual distinct owner once and each newly discovered RES clause once. No claim is made about accepted serializations outside this normal-form image.

**Precedence audit.** LSPV-4/539 established exact signed SOURCE caching, LSPV-2/561 exact repeated RES congruence, LSPV-1/590 complete-CLI owner sentinel, LSPV-2/579-581 facet/paid quotient controls, LSPV-1/599 canonical SOURCE-dominant cone pruning, LSPV-1/600 paid-owner closure and complete OS replay, LSPV-2/582 the one-way signed-clause first-discovery MAY simulation, and LSPV-5/505 the Array-container correction. None was a same-CLI *global, all-DAG shortest-path equality* over a prevalidated fixed owner bank. The new direction is the reverse (abstract-path to concrete-CLI) construction, not a rediscovery of these forward lemmas.

## Exact model, all-DAG minimum and theorem

The original *unchanged* restricted checker is \`experiments/arc/lspv2_386_independent_verify.js\`, blob \`338305c0ce101704205e57543756b8127074a986\`. Its rule source was inspected. Let \(\sigma=(h,E,b,g)\) be an in-band graph/source specification for which all of that original checker's graph, odd-charge, edge-uniqueness, guard-range and small-graph parity self-check conditions hold. Let \(S_\sigma\) be the mandatory **entire exact signed 4h+1 SOURCE clause-occurrence list**, including the positive guard unit. This requirement is not relaxed merely because the clause-set state will ignore duplicates.

Let \(G=[(id_i,z_i,a_i,b_i)]_{i=1}^k\) be any **nonempty** owner bank satisfying the checker's original safe-integer IDs, fresh output wire, signed inputs, exclusion of guard variables, and earlier-owner dependency tests. Each such owner is paid exactly once. Let \(D(G)\) be every individually legal \`views(z,a,b)\` conservative AND2 defining clause, excluding tautological facets exactly as the original checker does. A free facet may be emitted as a zero-parent DEF row because the whole G bank is validated before any records. Set
\[
K_0(\sigma,G)=\{\text{clause value of each SOURCE occurrence in }S_\sigma\}\ \cup\ D(G).
\]
Here a clause value is its exact sorted, non-tautological, signed literal tuple, not a clause hash lacking polarity, a source ID, or a paid occurrence identity. Original source occurrence IDs, owner IDs and their dependency order remain in the *reconstructed concrete state* even though this restricted optimum needs only signed clause values for future RES selection.

A **legal discovery edge** \(K\to K\cup\{C\}\), charge one, chooses two (not necessarily distinct-occurrence) known signed clauses \(A,B\in K\) and an oriented nonzero pivot \(p\) with \(p\in A\), \(-p\in B\), and
\[
 C=\operatorname{sort}\big((A\setminus\{p\})\cup(B\setminus\{-p\})\big)
\]
which passes the original \`clean(C)\` predicate (no complementary literals and canonical safe signed integers), with \(C\notin K\). The terminal edge must first introduce the empty clause and must have \(p\ne999999\) to avoid the complete CLI's pivot-corruption no-op. There are finitely many possible clause values on the original edge and declared owner wires, at most \(3^m\) non-tautological signed clauses for \(m\) wires. Let \(d_{\sigma,G}\) be the shortest number of discovery edges ending in that terminal condition, or \(+\infty\) if none exists.

Let \(\mathcal P_{\sigma,G}^{CLI}\) be **all** original complete-CLI-accepted ordinary Array-record packets with the same \(\sigma\), exactly the same paid owner bank \(G\), all mandated SOURCE occurrences, arbitrary legal DEF facet occurrences, and arbitrary legal chronological strict RES steps. It permits free after-the-fact selection and sharing across any whole DAG, not merely normalization of one selected proof.

**Theorem 601.1 (exact restricted global minimum).** For every such \((\sigma,G)\),
\[
\boxed{\quad
\min_{P\in\mathcal P_{\sigma,G}^{CLI}}W_{386}(P)
=|G|+d_{\sigma,G},\qquad W_{386}(P)=|G|+\#RES(P).
\quad}
\]
Both sides are \(+\infty\) if no accepted proof exists. If optimizing the archived /386 system over **all** eligible paid owner banks rather than fixing G, the exact characterization is
\[
\boxed{\quad
W^{CLI}_{386}(\sigma)
=\min_{\substack{G\ \text{original-checker-valid}\\ |G|\ge1}}
\big(|G|+d_{\sigma,G}\big).
\quad}
\]
This second equality is a minimization over owners **and all complete proof DAGs**. It asserts no efficient method for choosing G or finding the shortest path.

**Proof of the lower inequality.** Take any accepted complete packet P. Every original SOURCE can be retained and moved to a prefix, preserving all mandatory signed source occurrences. Insert once at the prefix each distinct allowable free facet from the fixed globally validated G bank. This changes no paid work. Traverse the original RES steps chronologically; whenever a paid RES creates a clause already present, substitute an earlier representative with *exactly the same signed tuple* in all later RES parent ports. This is valid because the checker inspects only the two parent clause values, oriented pivot and exact non-tautological resolvent, not parent kinds, contexts, provenance or discharge state. Delete every unused paid RES, keeping the original terminal RES and its signed pivot. This is the original-source-dominant normal-form argument of /599, applied after full facet preloading. Any earlier empty-clause step is dead, since an empty clause cannot supply the nonzero pivot required by a later RES; remove it. The remaining strictly new RES clauses in their chronological order form a discovery path of length at most \(\#RES(P)\), and its terminal pivot is not 999999: otherwise the complete CLI pivot-corruption test would be a no-op and reject P. Hence \(d_{\sigma,G}\le\#RES(P)\), giving \(|G|+d_{\sigma,G}\le W(P)\).

**Proof of the upper inequality and terminal preservation.** Given any finite path realizing d, emit the mandatory SOURCE records *once each* with correct original IDs, placing the positive-guard SOURCE first. Emit all distinct non-tautological DEF facets needed by the path, each with its genuinely declared G owner ID and zero parents (emitting every available facet also works). For each discovery edge, select actual already-emitted parent record indices representing A and B, and append the checked signed RES record with its oriented pivot and exact new C. This is chronological, source-authenticated, respects valid owner outputs and charges each distinct new paid RES occurrence once. Append the empty-producing step as the last record, with its required pivot not 999999, and recompute the six original summary counts. All ordinary core checks pass. The original complete CLI's eleven hostile mutations also fail: the first record is the positive guard unit and therefore its altered negation is a forged SOURCE; G is nonempty so deleting its first owner changes the paid summary; the last pivot change is now nontrivial and invalid; and the other nine original mutations force an invalid terminal clause, forward parent, payment, charge parity, false SOURCE type, duplicate edge, invalid literal zero or invalid guard. Thus this *specific canonical packet* is complete-CLI-accepted, with work exactly \(|G|+d\). If no path exists, the lower direction implies no accepted packet exists. Taking the minimum over eligible G proves the second equality.

This is exact **only because** the original /386 checker is context-free, all owners are prevalidated globally, and every legal DEFINE facet may be frontloaded without changing its meaning. Its state quotient is *not* a faithful quotient of arbitrary serialized proof histories; it is sufficient for **optimal logical work** in this particular original sibling grammar. Arbitrary \`R_mix341\` may have historical RES-to-AND3 ports, GF(2), LOCAL-CONVERT, contexts, exported/private wires, branch AND obligations, discharge, weakening and joins, invalidating the reduction. Those transitions remain possible MAY edges until authenticated.

## Independent exhaustive control and precise limitation

The standalone Python program, \`experiments/arc/lspv1_601_clause_set_exact_control.py\`, was executed locally as an operating-system process with no dependencies or random seed. Its Git content is exactly the executed bytes: Git blob \`f4d6072e402229e556378d900ba5c74fdeae52ad\`; SHA-256 \`5b1ad3a8c3339f1e9aeec107dce698598ff2eecf94b2a6f569f68e24f3b0bb9f\`. The exact resulting raw JSON is \`results/raw/arc/2026-11-12_1327_LSPV1_601_CLAUSE_SET_EXACT_CONTROL_RAW.json\`, Git blob \`6a6c138a62e84ac3a9f3f2070d4b467c15d07291\`, SHA-256 \`f64d9be5d9ccceba920f8d3ac615ee3d1e6875713015e23080a792595b7d0b29\`.

The experiment enumerated all \(2^8=256\) subsets of the eight nonempty non-tautological clauses over two Boolean variables. For each source it independently compared (a) a four-assignment truth-table SAT oracle; (b) shortest set-state Resolution closure by BFS; and (c) **ordered proof-sequence** DFS without state memoization at all shorter depths and at the discovered minimum. All exact comparisons passed.

| Source status or minimum paid RES count | Number |
|---|---:|
| SAT sources, no RES contradiction path | 95 |
| UNSAT, minimum 1 | 112 |
| UNSAT, minimum 2 | 48 |
| UNSAT, minimum 3 | 1 |
| Total original source subsets checked | 256 |

The unique minimum-3 source comprises the four signed binary clauses \((x\lor y),(x\lor\neg y),(\neg x\lor y),(\neg x\lor\neg y)\): derive units \(x,\neg x\), then empty. Every output source, cost and witness is in the raw JSON. **Crucial scope:** This is a declared two-variable Resolution control, not an original /386 guarded-cubic SOURCE packet; no newly constructed original /386 packet or original OS CLI replay is claimed for this particular run. The symbolic full-CLI theorem instead follows from the inspected immutable checker source plus the previously accepted /386 whole-DAG normalization evidence. LSPV-5 should independently falsify the universal converse with native original bytes.

## All-rule and barrier audit

1. **P2-D1 remains OPEN.** The pinned /386 sibling and the separate /341 SOURCE/AND3/GF(2) fixture checker are not one unified historical R_mix341 grammar. No evidence permits removal of unknown rule types from the actual transition relation. The full original accepted-byte semantics, especially mixed parent ports, local conversion, contexts and discharge, remain absent.
2. **P2-C3 remains OPEN.** The exact quotient is a genuine realization theorem on one fixed ROOT-context source/DEF/RES sublanguage. For the historical full calculus, one must retain all paid-node identities, assumptions, owner and wire scopes, all authorized transitions, and concrete-step inclusion; a cheap MAY path is not automatically real. CEGAR must replay against the *correct original checker* before rejecting shortcuts.
3. **P2-B1 remains OPEN.** No asymptotic \(\bar W_R\) lower bound follows, even for the archived sibling. A shortest-path characterization is not a high lower bound or an efficient shortest-path discovery algorithm. An algebraic or extension shortcut may make published Resolution-hard sources easy in the full grammar.
4. **P2-B2 and P2-B3 separately OPEN.** There is no noncircular same-calculus transfer from a polynomial SAT algorithm or from another proof system's short certificates. Keep \(\text{paid logical work}\), evidence-bit length, construction/discovery time, actual machine time, proof span, and peak storage distinct; no one is set equal to another.
5. **Barrier controls.** Horn/2-SAT and the two-variable truth-table sources are deliberate easy controls. Signed-clause aliases are safe only under exact context-free RES semantics. Padding, dead owners, semantically identical but syntactically distinct clauses, altered source families, and unknown algebraic rules defeat unqualified extrapolation. This is not a proof-system-independent complexity lower bound.

Primary literature: [1] S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI https://doi.org/10.2307/2273702, emphasizes fixed proof-system interpretation; [2] P. Cousot and R. Cousot, *Abstract Interpretation*, POPL (1977), https://doi.org/10.1145/512950.512973, on representation and sound simulation; [3] Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV (2000), https://doi.org/10.1007/10722167_15, on concrete replay; [4] Atserias and Müller, *Automating Resolution Is NP-Hard*, JACM 2020 / arXiv 1904.02991, https://arxiv.org/abs/1904.02991, on distinguishing minimum proof existence from searching for one. None supplies missing R_mix341 authority.

## Corpus reconciliation, ownership, and next falsifier

**CORPUS REVIEWED.** Both current root proof trackers, issue #3 and latest peer comments, AGENTS.md, CODEX.md and the repository skill, root main.tex ownership markers, latest five-role handoffs and native source/bank code, LSPV-1/590/599/600 and earlier relevant 539-549, LSPV-2/561/579-582, LSPV-3/549/595, LSPV-4/539/549/568, LSPV-5/503-510, and the required prior /341 fixture/source-authentication limits. The immutable original /386 source was read rather than reconstructed from prose.

**DUPLICATION/CONTRADICTION.** Adopted /539, /599, /600 and /582 as forward directions. Extended them only by the all-path converse for fixed G; no earlier missing historical rule has been authenticated. Rejected universal transfer of this equality to a mixed native grammar. No previous valid theorem is retired or promoted. Root MAIN needs only a new restricted LSPV-1 evidence paragraph, without touching peers' owned regions.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Current \`proof1.txt\` blob \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`, \`proof2.txt\` blob \`d9de384bed127661242adbb840e7940bd3f6e3d8\`; the statuses and quantified dependency arrows are unchanged. No change to weights, agent identities, five original schedules or 2 Route A / 3 Route B labels. Full repository report-checker/preflight and a new native-CLI OS replay were not executed because no authenticated complete repository checkout was available to this run.

**Exact next task for LSPV-5:** take a source-valid /386 bank with nested dependent owner IDs, DEF facets and repeated RES clauses, construct a shortest clause-set path, serialize the canonical packet, and execute the unchanged original CLI with its eleven corruption controls. Try to produce one counterexample to the converse, especially through noncanonical parsed IDs or a hidden wrapper mutation. For LSPV-3: compare every proposed R_mix341 mixed-rule port against this deliberately narrow history-independent criterion, without replacing the missing historical authority.
