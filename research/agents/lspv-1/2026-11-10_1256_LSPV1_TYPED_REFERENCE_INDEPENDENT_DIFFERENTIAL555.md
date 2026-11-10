# LSPV-1/555: independent differential audit of the strict source-bound /341 fragment

**2026-11-10 12:56 PST | General SAT Lower-Bound Lead | Route B | INDEPENDENT REPRODUCTION, PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA and falsifiers registered before search

**NATIVE-555 candidate:** An independently written, externally source-bound, typed SOURCE/AND3/XOR replay kernel preserves all seven genuine recovered /341 proofs, rejects the previously discovered checker-accepted SAT-source forgery, accepts a sound unused extra paid inference, and agrees with independent LSPV-2/539 on these core probes. This is **replication of an earlier result**, not a newly discovered historical grammar or lower bound.

**Falsifiers:** F1, any honest original fixture fails; F2, the forged satisfiable source receives a sound typed refutation; F3, a correct unused fresh paid node is excluded as logically illegal; F4, the new independent implementation contradicts the prior /539 reference on honest, forged or padding probes. None occurred in the tested scope. They are precise finite tests and not full-calculus closure.

## Original evidence and literature search

Read complete current root proof1.txt and proof2.txt, issue #3 and recent specialist comments, AGENTS.md, CODEX.md, the repository research skill, the November 9 abstract-negative/FLMV handoffs and the latest November 10 native-calculus focus. Directly inspected relevant original reports LSPV-1/553-554, LSPV-2/538-539, LSPV-3/550-551, LSPV-4/524 and LSPV-5/477. Read actual GROKPROOF 2026-11-10_1212 review and 2026-11-10_1523 progress, and the Claude ONETAPE-0001 original as a separate machine-model control. Earlier 539-549 mathematical results are retained at their known scope, not blanket reverified.

Pinned originals: producer Git blob 4081022e8a3841d79f751a3d3a7a10decbb026da; recovered limited checker blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; independent LSPV-2/539 reference blob fc91a6f33d0d010d6225365a3d9ce72a090af21f; LSPV-3/551 SAT-forged packet blob 706947c767361e7c979b8208677eb983d33838f4.

Required external primary files were read: konard/p-vs-np scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c). The latter formats define **different proof languages**, not a historical /341 parser. Relevant primary paper controls are Cook and Reckhow (1979) on proof checkers and Cousot and Cousot (1977) on semantic simulation [1,2].

## Independently verified restricted soundness invariant

Let F be any separately supplied strict signed proper 3-CNF source in the new reference input syntax, and let pi be a finite topologically ordered proof using **only** the new typed SOURCE, AND3, and XOR grammar. Then

$$
\forall F\,\forall\pi:\quad
\operatorname{StrictKernel}(F,\pi)=\mathrm{ACCEPT}
\Longrightarrow F\in\mathrm{UNSAT}.
$$

Proof by induction over the shared DAG: every original SOURCE factor is the exact Boolean function of its signed clause in the independently supplied source. Every AND3 node is checked, for every local assignment on the actual union of at most three original variables, to be exactly the conjunction of two already established factors. Any attached affine alias must equal that factor on every such assignment. Every XOR record combines two earlier validated GF(2) consequences by exact symmetric-difference mask and RHS xor. Reuse of an existing paid node does not change its proposition. The only accepted terminal is the impossible equation 0=1, so no model of F exists. Distinct paid IDs are charged once, at unit weight in this declared restricted calculus. Source references are free.

The independent implementation checks original signed source clause vectors against a **separate external DIMACS argument**, paid string-ID freshness, typed original-variable supports and exact factor/GF(2) semantics. Graph and charge annotations are inert metadata, not premises. This is a conditional theorem about the NEW typed fragment. The source parser does not authenticate the complete historical accepted-byte grammar, canonical raw-byte identity, branch contexts, DEF ownership, LOCAL-CONVERT or the missing historical operations. Unknown native transitions are not silently excluded from the true historical calculus.

For this typed subset only, an exact semantic projection can store source vectors, the complete shared prior-node DAG, typed factors and rows, original-variable supports and globally first-created paid identities. Each declared paid creation has abstract cost one, and references cost zero. Concrete step inclusion and completed-goal preservation follow directly from the checked rule semantics. This restricted statement is already conceptually established in LSPV-2/539; our independent implementation provides additional reproducibility, **not a new all-rule P2-C3 theorem**.

## Actual differential replay

The exact recovered /341 producer and mathematical verifier functions were run inside V8, modifying only file/console I/O wrappers. The new independent kernel was executed from its newly committed GitHub contents, and LSPV-2/539 reference source was separately evaluated in V8. LSPV-2/539 produced an explicitly **stubbed digest only** in this isolated adapter; no stub value is an actual SHA or is used in the reasoning.

| Control | Recovered historical limited checker | LSPV-2/539 independent reference | New LSPV-1/555 |
| --- | --- | --- | --- |
| Seven original correct fixtures | ACCEPT, 30,714 checks | 7/7 ACCEPT | 7/7 ACCEPT |
| Forged SAT source, 48 clauses on 18 variables | **ACCEPT**, 2,273 checks in two-fixture packet | REJECT | REJECT |
| Sound unused additional K4 paid AND3 (16 rather than 15) | REJECT, previously established /553 | ACCEPT | ACCEPT |

Honest paid counts are 15, 23, 31, 39, 47, 127 and 39, total 321. Independent clause evaluation confirmed that the 18-bit witness **101001000000100000** satisfies **48/48** of the original signed clauses in the forged source. The strict kernel rejects its malformed support in the false AND3 step; replacing string-valued charge metadata with an integer still rejects it. Eight further hostile controls were rejected by the new kernel: original literal string, AND3 support string, numeric paid ID, false affine sink, incorrect factor truth table, dangling antecedent, an unsupported RES opcode **in this subset only**, and independent external-source substitution. All tests were on exactly identified originals with no random seed.

A sound extra unused paid node passes both independently written reference checkers but fails the original limited checker because its fixed proof-length test is not a general mathematical rule. This difference is expected. The new typed auditor must **not** be passed off as the original accepted-byte semantics or imported as an all-native restriction. The SAT-source acceptance is a true bug in the recovered fixture checker, **not** a legal cheap mathematical refutation or a cost-sound abstract proof for a SAT instance.

The V8 work is not a full local Node CLI run, complete checkout preflight, formal verification, memory measurement, or all-native proof checker execution. A Node CLI script was published and GitHub-readback verified; its OS execution remains untested here. Actual runtime, proof-discovery effort, proof evidence bits, logical work, span and physical space remain distinct quantities.

## Dependency ledger and publication

| Node | Status and effect |
| --- | --- |
| P2-D1 | **OPEN**. Original /341 checker is incomplete and accepts a SAT-source forgery. Separate typed replayers do not restore its missing historical native productions. |
| P2-C3 | **OPEN**. No authenticated complete full-calculus simulation, rule cost map, auxiliary wire/facet scope, branching/discharge or join proof. |
| P2-B1 | **OPEN**. No full mixed-calculus superpolynomial minimum. |
| P2-B2/B3 | **OPEN**. No noncircular same-calculus bridge from all deterministic SAT solvers. |

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full root proof1.txt Git blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** (18,553 characters) and proof2.txt blob **32d8be19dd5ee29ed1c629db645b08c55231bede** (913,110 characters) were retrieved. Earlier peer evidence IDs **P2-L2-539** and **P2-L3-551** already capture the substantive facts. No new status, dependency or previously unrecorded counterexample justifies another root tracker entry. Root main.tex was recovered in full through immutable blob **41b6556cbaed92e65f366bfee424f452e404c9f1** after the contents API returned an empty body; it remains unchanged to avoid duplicate nonmaterial content and preserve all ownership regions.

Code: experiments/arc/lspv1_555_typed_subset_kernel.cjs (Git blob **3e887f2c8f581f6784895be819dcfc534f505d68**).

Raw V8 results: results/raw/arc/2026-11-10_1256_LSPV1_555_TYPED_KERNEL_INDEPENDENT_DIFF_RAW.json (blob **d6fa3a8b24f3840fa14ad46ff71052b740a29529**).

**Required next load-bearing step:** LSPV-3 must obtain an actual accepted-byte full-rule native checker (or identify the missing authoritative source), with independently bound original input and genuine accepted RES, GF(2), DEF/facet ownership, LOCAL-CONVERT and properly discharged branch records. LSPV-5 independently falsifies its scope/identity and cost assumptions. LSPV-2 and LSPV-4 retain their Route A obligations. All five titles, identities, schedules, time zones, historical weights and Route A/B labels were left untouched.

**P versus NP remains OPEN.**

## References

[1] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic 44 (1979), 36–50. DOI 10.2307/2273702.

[2] Cousot P, Cousot R. Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints. POPL (1977). DOI 10.1145/512950.512973.

[3] meelgroup/frat-xor/format.md, external mixed CNF/XOR record format. Distinct from the historical R_mix341 accepted grammar.
