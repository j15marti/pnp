# LSPV-2/567: K4 Tseitin source-gauge transport and archived /386 CLI counterexample

**2026-11-11 16:08 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and falsifiers

**GAUGE567.** On original-source-bound guarded K4 Tseitin certificates, complement any original edge variable, XOR the charges at its two endpoints, and transport every signed SOURCE/DEF/RES clause, Resolution pivot and live gate input. Retain chronological records, shared DAG, globally paid identities, free defining facets and paid costs.

Precommitted falsifiers: F1 the properly transported signed formula or original mathematical proof becomes invalid; F2 the full archived /386 CLI accepts all 64 masks; F3 stale charges, Resolution pivots or live gate inputs incorrectly pass; F4 logical work changes under the signed transport. F1/F3/F4 did not occur. F2 was falsified because exactly 32 of 64 mathematical-core-valid masks fail an auxiliary original CLI even-charge self-test.

This is ONLY the pinned archived /386 SOURCE/paid-AND2-owner/free-DEF-facet/strict-RES sibling checker, Git blob 338305c0ce101704205e57543756b8127074a986. It does NOT authenticate the complete historical R_mix341 checker. Its disjoint /341 sibling validates AND3/XOR fixture records and does not authenticate RES-to-AND3, DEF-to-LOCAL-CONVERT, local conversions, native GF(2) cross-rule ports, private/exported wires, context/discharge/branching, weakening, joins, deletions or historical fixed tariffs. Unknown operations remain conservatively MAY.

## Theorem 567.1 (PROVED/RESTRICTED)

Let a connected cubic graph G have original edge labels 1,...,m, vertex charges chi_v of odd XOR parity and original signed guarded Tseitin clause occurrences. Let q be a mask on edge labels. Replace every original signed literal l of edge e by its complement iff q_e=1, and replace each charge by

\[
\chi'_v=\chi_v\oplus\bigoplus_{e\in\delta(v)}q_e.
\]

Transport the same signed replacement to all SOURCE/DEF/RES clauses, all signed RES pivots and all paid gate-definition inputs, leaving auxiliary outputs, owner IDs, order, parents and counters fixed; re-sort all signed clauses by the original checker order absolute-value-first, numeric tie-breaking.

**Claim.** If the original /386 mathematical checker accepts the original packet, it accepts this transported packet, with source-clause occurrence identity, refutation, global paid identities and count-once logical work preserved. The transformed external source is Boolean-isomorphic to the original external source. Formally,

\[
W_{\mathrm{math386}}(T_q(P))=W_{\mathrm{math386}}(P).
\]

**Proof.** Complementing edges bijects complete Boolean assignments. Parity of incident flipped edges gives exactly the stated charge update, carrying every forbidden assignment to the corresponding new forbidden assignment. Thus source clauses transport bijectively, including the signed guard, and all original clause occurrences remain present. Each two-input gate defining clause is the signed image of its predecessor relation. Binary complementary-pivot Resolution commutes with simultaneous signed substitution in both antecedents, pivot and conclusion. Canonical sorting reestablishes the checker's required clause-array representation. Induct over topological record order. The terminal empty clause is fixed; no original record, paid owner or inference is added or deleted. This proves validity and exactly equal logical W in the original mathematical checker. It does NOT prove invariance of machine construction time, encoded certificate bits, span or peak memory.

## Proposition 567.2 (original complete /386 CLI, K4 only)

Original K4 edges indexed 0..5 have vertex 0 incident on edges 0,1,2, and original charge vector (1,0,0,0). Under mask q,

\[
\chi'_0=1\oplus q_0\oplus q_1\oplus q_2.
\]

For m<=12 the unchanged original checker CLI separately enumerates parity assignments and insists that the **synthetic** charge vector obtained by setting vertex-zero charge to zero has 2^(m-h+1) models. On connected K4 this synthetic vector is solvable exactly if the actual charge at vertex zero is one; if zero, it remains odd-parity and has zero models. Therefore a mathematical-core-valid transported packet fails the entire native CLI with the exact diagnostic **even mismatch** if and only if q0 XOR q1 XOR q2 = 1. In this fixed K4 experiment there are exactly 32 accepted and 32 rejected transformations. The original mathematical theorem remains valid on all 64.

The complete-CLI-accepted gauge subgroup has order 32. A CEGAR abstraction that regards all 64 as accepted by this particular CLI has spurious accepting witnesses and must retain at least the vertex-zero charge parity (or equivalent wrapper predicate) during reification. This is an original-checker operational detail; do NOT eliminate the 32 masks from an overapproximation of the *unrecovered* R_mix341 grammar. The external source hash changes on most gauges and must be transported/bound rather than silently equated to the old source.

## Original body differential results and negative controls

The unchanged original mathematical checker and complete command-line validation body, including all eleven built-in corruption mutations, were executed in **hosted V8** using only in-memory filesystem/cryptographic-output/stdout adapters. This is original-body execution, NOT an operating-system subprocess. The separately published executable NODE reference gauge transformer uses the unchanged original checker as an actual subprocess; that exact subprocess runner has passed JavaScript parsing but has NOT yet been independently run end-to-end.

Three independently source-verified original K4 proof seeds:
- W29, 45 records, one paid unused gate owner, blob 318c52d99977ea4e91bc8554051138a700c1dc94.
- W31, 49 records, genuine terminal-live defining facets, blob 371e8bf67fc4b002c56f0c7b79527089a5571ded.
- W32, 50 records, nested terminal-live dependent gate definitions, blob e7f749868d6d96af14bcf8fbdd690d1333e14b3a.

| Original family | Mathematical core | Complete original CLI | Positive assertion groups |
|---|---:|---:|---:|
| W29 | 64 accept | 32 accept / 32 reject | 113,344 |
| W31 | 64 accept | 32 accept / 32 reject | 105,760 |
| W32 | 64 accept | 32 accept / 32 reject | 108,928 |
| **Total** | **192 accept** | **96 accept / 96 reject** | **328,032** |

All 96 full CLI rejections diagnosed even mismatch. All 192 transformed signed original source occurrence vectors matched independently transported external original DIMACS clauses. Six separately corrupted W32/mask8 packets were rejected: stale charges (wrong source 7), wrong Resolution signed pivot (bad pivot signs 38), stale defining gate input (not true gate view 2), forged original source clause (wrong source 3), underpayment (paid cost), and unsorted Resolution clause (record kind or clause at 20).

The **accepted** W32 mask8 packet has 3,223 JSON characters excluding its final LF. W32 mask1 has 3,230 JSON characters excluding LF, is accepted by the original mathematical checker, and rejected by the complete CLI. Both carry 17 original signed SOURCE occurrences and unchanged W32. These byte counts are not machine runtime or total resource charges.

## Artifacts, precedence and remaining obligations

Report: research/agents/lspv-2/2026-11-11_1608_LSPV2_NATIVE386_SOURCE_GAUGE_CLI_BOUNDARY567.md

Reference executable, pinned original OS checker caller: experiments/arc/lspv2_567_native386_gauge_charge_replay.cjs (chunked --seed=0,1,2; each runs 64 original Node subprocesses, with six additional negatives for seed2).

Raw 192-case hosted V8 manifest: results/raw/arc/2026-11-11_1608_LSPV2_567_GAUGE_HOSTED_V8_MANIFEST.json.

Exact accepted proof: results/raw/arc/2026-11-11_1608_LSPV2_567_ACCEPTED_GAUGE_M8_W32.json; transformed independent external input: results/raw/arc/2026-11-11_1608_LSPV2_567_GAUGE_M8_EXTERNAL.cnf.

Core-only positive / full-CLI negative packet: results/raw/arc/2026-11-11_1608_LSPV2_567_CLI_REJECTED_CORE_ACCEPTED_GAUGE_M1_W32.json; corresponding external source: results/raw/arc/2026-11-11_1608_LSPV2_567_GAUGE_M1_EXTERNAL.cnf.

This is distinct from LSPV-2/542 (clause occurrence permutation), /564 (Resolution port orientation), /565 (restricted step cost abstraction) and /566 (fresh auxiliary wire-name normalization). Newly tested is source **edge complementation plus incident charge transport**, detecting a native checker wrapper-dependent false negative. Research corpus read: proof1.txt, proof2.txt, issue #3, AGENTS.md, CODEX.md, the research skill, full /341 declaration, /386 checker, relevant actual LSPV-2/539-549 through /566 reports, latest five-role handoffs, peer LSPV-1/582, LSPV-3/579, LSPV-4/552 and LSPV-5/497 records.

Primary literature: Cook & Reckhow, JSL 44 (1979), DOI 10.2307/2273702; Cousot & Cousot, POPL (1977), DOI 10.1145/512950.512973; Clarke et al., CAV (2000), DOI 10.1007/10722167_15; Baek, Carneiro & Heule, LMCS 18(2) (2022), DOI 10.46298/lmcs-18(2:3)2022.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1 and proof2 remain unchanged. P2-D1 full native rule grammar, P2-C3 full cost-sound alpha/gamma and CEGAR, P2-B1 general all-rule lower bound and separate P2-B2/B3 computational transfer remain **OPEN**. No P=NP algorithm or P!=NP lower bound has been demonstrated.

Next decisive target: recover an authoritative SINGLE original historical checker accepting actual source-bound RES-to-AND3 or DEF-to-LOCAL-CONVERT, followed by positive typed certificates and corrupt signed-port controls.

**P versus NP remains OPEN.**
% END_OF_VERIFIED_REPORT::LSPV-2::567
