# LSPV-4/537: Dense numeric namespaces for the original archived /386 calculus

**2026-11-11 00:36 PST | PNP Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED code theorem + COMPUTATIONAL checker replay | P versus NP OPEN**

## Candidate theorem and falsifiers

Candidate: Every packet accepted by the unchanged original **archived /386** SOURCE/DEF/strict-RES mathematical checker has an accepted, logically isomorphic dense-numeric-identifier normal form, with identical paid owner count, RES count, source identity, complete shared deduction graph and terminal contradiction. This is a representation/resource firewall for [P2-D1]/[P2-C3], **not** recovery of the historical five-rule R_mix341 checker.

F1: renaming guard or gate output wire changes SOURCE or DEF facets and invalidates original grounding. F2: a nonmonotone gate-wire renaming changes strict signed pivots or introduces a duplicate or tautological resolvent. F3: renaming owner IDs aliases two paid owners or an input used before its declared owner. F4: raw token substitution that neglects canonical clause sorting is incorrectly admitted by the historical checker. Also audit the known /535 core-vs-CLI mismatch; no blanket CLI theorem is claimed.

## Pinned authentic scope

- Original archived /386 checker: \`experiments/arc/lspv2_386_independent_verify.js\`, blob \`338305c0ce101704205e57543756b8127074a986\`.
- Original checker-accepted two-owner source-bound signed K4 packet: \`results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json\`, blob \`08aa169b5db49b2ddd1cb5a9b6890fcc3b790916\`.
- Original /341 **semantic declaration**, blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`, specifies free SOURCE and unit-priced RES, AND3, XOR, LOCAL-CONVERT and conservative paid DEF; it is not an authoritative accepted-byte dispatcher. The surviving /341 fixture checker is disjoint, blob \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\`. The /549 polyglot cannot establish native cross-rule composition.

## Theorem 537.1: accepted core numeric-namespace normal form (PROVED/RESTRICTED)

Let P be a packet accepted by the original archived /386 \`checkProof(P,{control:true})\`. Let E be its number of source edge variables and g the number of declared gate owners in **gate_defs order**. All record indices, graph edges, vertex source identities and source charges are held fixed. Define the injective signed-literal map on the source's auxiliary namespace:

\[
\pi(\mathrm{guard})=E+1,\qquad
\pi(z_i)=E+2+i\ (0\le i<g),\qquad
\pi(\pm x_e)=\pm x_e\ (1\le e\le E).
\]

Map each signed gate input, every clause literal and signed RES pivot by sign-equivariant \(\pi\); map old owner ID \(id_i\) to integer \(i\); map every DEF record's owner reference accordingly. **Re-sort every mapped clause by the checker's exact \`key\` comparator**, not lexical order. Preserve record and gate-definition order, all positional parents, metadata and summary. Then

\[
\mathrm{Accept}_{386}(P)\Longrightarrow\mathrm{Accept}_{386}(\mathrm{Dense}(P)),
\qquad
W(\mathrm{Dense}(P))=W(P)=N_{\mathrm{RES}}+g.
\]

Also, applying Dense twice has the same result as once: Dense is idempotent on accepted JSON parse trees. Each source occurrence, defining facet, paid gate owner and RES deduction corresponds one-to-one, and all shared references remain shared.

**Proof.** In an accepted packet, original edge wires lie in 1..E; the positive guard exceeds E and is distinct from each fresh positive gate output; each gate output is distinct and exceeds E, and has a unique nonnegative integer owner ID. Input gate wires refer only to source edges or earlier declared output wires (possibly negated). The proposed renaming preserves these relations because output order is unchanged and all mapped wires are distinct with positive integer magnitudes. The original four source clauses per signed cubic vertex are reconstructed from the unchanged source graph/charge and the mapped guard; since they are canonically re-sorted, SOURCE membership and unique-source checks hold exactly. Each DEF facet is \((\neg z\lor a)\), \((\neg z\lor b)\), or \((z\lor\neg a\lor\neg b)\); signed injective renaming commutes with these constructions, tautology exclusion and canonical sorting. For each RES record, mapped parents retain complementary signed pivot occurrences, and strict canonical resolvents commute with injective renaming after re-sorting. Induction along unchanged positional parent indices proves every derived clause corresponds exactly, including the empty terminal clause. Summary counts and the gate-payment set cardinality remain unchanged. The graph's odd/even model-count control does not consult auxiliary labels. Reapplying the deterministic ordinal assignment makes no further change. QED.

This is a **one-way compiler of accepted parse trees into accepted \`JSON.stringify\` serializations**, not preservation of every possible raw JSON lexical spelling, ignored field, duplicate key or inaccessible checker extension. The theorem does not establish equality of physical verification costs or online CEGAR step completeness.

## Numeric representation bound and cost-soundness

Every recognized auxiliary **wire magnitude** after normalization is at most \(E+g+1\), and every recognized gate-owner identifier at most \(g-1\). The recognized literal and owner identifier tokens thus require \(O(\log_{10}(E+g+2))\) decimal digits, independent of arbitrarily large safe-integer original labels. Positional parent indices remain at most \(L-1\) for L records. This is an **upper bound on recognized identifier token lengths**, not all JSON evidence bytes: arrays, source clauses, extra fields and duplicate/ignored properties may dominate.

For the completed-trace abstraction \(\alpha(P)=\mathrm{Dense}(P)\), choose \(\gamma(Q)\) to include accepted inverse auxiliary/owner renamings preserving the same signed source, full owner-aware DAG and contexts (this /386 checker has no branch contexts). The original P is represented by \(\gamma(\alpha(P))\), terminal refutation and source identity are preserved, and abstract *logical* cost equals concrete cost, hence \(W^\#(\alpha(P))\le W(P)\). This is **not** a full native concrete-step transformer. No cost reduction is inferred for output/parsing/retrieval or peak writable memory.

## Executed original-checker evidence

The unchanged /386 checker function and its complete CLI body (including **all eleven bundled hostile controls**) were executed with only virtual file-input, output and SHA-report adapters in hosted V8. No semantic verifier edit was made. Four accepted packets:

| Namespace | Encoded JSON bytes | Dense JSON bytes | Paid RES+DEF | Original CLI assertions |
| --- | ---: | ---: | ---: | ---: |
| Original (guard 7; gates 8,9; owners 0,1) | 4,421 | 4,421 | 51+2=53 | 4,663 |
| Guard 9,876,543,210,123; reversed large gate wire order | 5,146 | 4,421 | 53 | 4,663 |
| Guard 13; gate wires near safe-integer boundary | 4,744 | 4,421 | 53 | 4,663 |
| Guard 9,007,199,254,740,800; sparse near-safe IDs/wires | 5,366 | 4,421 | 53 | 4,663 |

All four accepted, with 74 records, 17 SOURCE, 51 strict RES, 2 paid gate owners and eleven original bundled negative tests per accepted packet. **18,652** original CLI checker assertions across the four successful full-wrapper invocations. Each sparse packet normalized back to the original seed *byte-for-byte after \`JSON.stringify\`*. Seven independent hostile mutations were rejected: unsorted relabel, duplicate owner, duplicate output, dangling DEF owner, wrong signed RES pivot, underpayment and unsafe owner integer. The unsorted near miss was rejected specifically at canonical clause checking, confirming that literal substitution without re-sorting is unsound.

Runnable original-checker audit: \`experiments/arc/lspv4_537_archived_386_numeric_relabel.cjs\`. Machine-readable V8 summary: \`results/raw/arc/2026-11-11_0036_LSPV4_537_NATIVE_DENSE_NAMESPACE_RAW.json\`. **The published standalone OS Node command was not executed in this tool environment; V8 results are not a physical indexed-machine resource measurement.** The script pins both Git blobs and can reproduce the core/CLI checks in a full checkout.

## Resource ledger and outstanding falsifiers

SOURCE: zero paid, exact original signed source plus source-index and guard evidence. DEF: once-paid per distinct owner declaration, even if facets referenced many times; each DEF facet view adds zero paid inference but its clause, ID and lookup require real bytes/time. RES: exactly unit paid per distinct strict RES record; two positional parent references, signed pivot and canonical clause processing require physical verification; shared RES/owner deductions are charged once, not per reference. Sequential verification performs nonzero scanning, sorting, lookup and model-count control work; neither assertion counts nor JSON bytes are native Turing steps. Ideal dependency span is preserved by graph isomorphism. Live retention, retrieval, recomputation and peak writable bits are NOT measured, and the original \`known\` array materializes all previous clauses. Offline normalization itself needs parsing, lookup maps, canonical sorting and output storage, which cannot be treated as zero-cost.

GF(2) cheap shortcut, compact affine row, XOR, AND3, LOCAL-CONVERT, branch/assumption/discharge/joins, learned lemma and cross-context reuse remain **unauthenticated** by the /386 checker. A low-cost extension proof in the other checker must still be retained in the MAY search; do not transfer this normalization to a missing mixed parser. Recomputed intermediate results and streaming bit representations can change space independently of this name equivalence. Big integer raw lexemes beyond the ECMAScript safe-integer domain cannot be legitimized by this theorem.

## Literature, project reconciliation and status

Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44:36-50, DOI 10.2307/2273702, formalizes proof systems and proof length but provides no historical /386 byte contract. Nordström and Håstad (2013), *Towards an Optimal Separation of Space and Length in Resolution*, Theory of Computing 9:471-557, DOI 10.4086/toc.2013.v009a014, concerns length/space in other formal models. Exact namespace isomorphism here is proved by inspection of the pinned /386 code, not imported as a result of those papers. Related /527 alphanumeric-string ID compression concerns the disjoint /341 checker; /535-536 owner/facet and nested-gate accounting, /549 checker noncomposition, /551 semantic MAY ceiling and /564/566 orientation/topological quotients were checked for overlap. None proves this numerical wire-and-guard dense normalization in the pinned signed /386 calculus.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root \`proof1.txt\` (blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`) and root \`proof2.txt\` (startup blob \`8927e4ba0c54ba701ceac55e918203fcdf675e1a\`) remain unchanged because no load-bearing P2 dependency is closed. [P2-D1] historical grammar OPEN; [P2-C3] all-rule cost-sound alpha/gamma OPEN; [P2-B1] superpolynomial minimum-work lower bound OPEN; separate [P2-B2/B3] OPEN; P versus NP OPEN. main.tex may be updated only within **LSPV-4 OWNED** delimiters with current SHA and complete readback.

**Next:** recover one genuine RES-to-AND3 or paid DEF-to-LOCAL-CONVERT same-checker accepted transition, and test whether the proven signed namespace quotient survives actual gate export, assumption scope and context joins. Exactly five existing research roles, titles, PST schedules, historical rule weights and two Route A/three Route B labels are preserved; no automations changed.
