# LSPV-2/581: An unbounded terminal-live structural congruence gap

**2026-11-12 12:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED symbolic theorem + COMPUTATIONAL original-OS replay | P versus NP OPEN**

## One candidate and four falsifiers

**Candidate [P2-D1/P2-C3]:** For each integer k >= 1, construct a valid, externally source-authenticated, archived /386 proof with 4k newly inserted PAID Resolution records, all terminal-live, for which saturation of structural DEF/RES congruence leaves an extra 2k cost even though original-checker-valid same-signed-clause reuse can eliminate all 4k. This is a falsifier of incomplete structural abstractions, not a hard-formula lower bound.

**F1:** native signed pivot, conservative paid gate or exact resolvent fails. **F2:** any inserted paid inference is not a genuine terminal ancestor. **F3:** iterated ordered-parent/pivot/conclusion structural congruence eliminates all excess work. **F4:** semantic reuse, source preservation, or native full-CLI corruption subtests reject the claimed W29 reconstruction. Six separate hostile packets test wrong signed DEF facet, payment, forward parent, pivot, forged SOURCE and unsupported AND3 opcode.

## Authority and novelty

Unchanged original archived restricted checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986; local exact SHA-256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113. It accepts SOURCE/DEF/strict RES JSON, paid AND2 owners and zero-additional-cost defining facets. It does NOT implement the full historical mixed R_mix341 calculus. The separate archived /341 checker, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, has SOURCE/AND3/XOR fixture semantics instead.

External 17-clause guarded K4 original SOURCE is results/raw/arc/574_k01_SIGNED_SOURCE.cnf, SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c, 215 bytes. Original accepted W29 seed: results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, SHA-256 0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0. It has 17 SOURCE, 28 RES, and one original paid AND2 owner.

**Prior art:** LSPV-4/539 proved general same-clause-value reuse for the restricted /386 core; LSPV-2/562 established ordinary-JSON full-CLI preservation with owner and final pivot retained; LSPV-2/579 established duplicate live DEF facet quotient; LSPV-2/580 established finite order-sensitive DEF/RES normalization. This report does not claim those results as new. **New:** a parametric **unbounded** separation with every redundant paid record terminal-live, a structural fixed point, and independently replayed original-OS accepted-byte witnesses.

## Native source-bound construction

The seed's genuine SOURCE record 7 has signed clause

$$
C=[-1,-4,-5,-7].
$$

Retain the original paid owner tuple [0,8,1,4] declaring auxiliary 8 as the AND of signed variables 1 and 4. Its two legal zero-extra-charge defining facets are

$$
A=[1,-8], \qquad B=[-1,-4,8].
$$

The exact original signed Resolution rules verify

$$
T=\operatorname{Res}_{-1}(C,A)=[-4,-5,-7,-8]
$$

and

$$
\operatorname{Res}_{-8}(T,B)=[-1,-4,-5,-7]=C.
$$

At each of k levels build TWO distinct two-step chains, taking the two previous-level outputs as their inputs. The first level reads SOURCE 7 twice. Redirect the original seed's two downstream SOURCE-7 parent uses to the two last-level outputs; retain every other original record and all source identities unchanged. The two branches on the last level are used by different original downstream paid steps. Induction backward through levels shows that all 4k inserted RES nodes, together with the two DEF views, are genuine ancestors of the final empty clause.

## Theorem 581.1 (PROVED/RESTRICTED)

Let P_k denote the native accepted constructed proof. Let S be chronological structural duplicate elimination, with DEF key (owner ID, exact signed facet) and RES key (already-remapped ordered parent identities, signed pivot, exact signed conclusion), iterated to a fixed point. Let Q be the established earlier-identical-signed-clause quotient of /539-/562 followed by a terminal-ancestor prune that RETAINS every original SOURCE occurrence, the original complete paid owner bank, and the terminal RES. For every k >= 1,

$$
\boxed{W(P_k)=29+4k,\qquad W(S(P_k))=29+2k,\qquad W(Q(P_k))=29.}
$$

Therefore

$$
\boxed{W(S(P_k))-W(Q(P_k))=2k\to\infty.}
$$

**Proof.** Each two-step gadget is exactly checked above. Both original parent consumers receive the original signed clause C, thus remain valid. The original 28 RES rows and original paid owner contribute 29; every gadget level contributes four distinct paid RES rows, proving the first identity. Within each level the two first-stage T nodes become structurally congruent after their inputs are canonicalized, as do the two resulting C nodes, removing precisely two paid RES occurrences per level. Across levels, the surviving T_j and C_j nodes have distinct chronological parent identities, even though their signed clause *values* repeat. No further structural keys coincide, and a second complete pass is idempotent. The seed has no previously derived auxiliary-8 clauses. Therefore exactly two RES rows survive per level, proving the second identity. In Q, each C_j equals SOURCE 7's original signed clause; all uses can be redirected chronologically to that original SOURCE. The repeated T_j is equal to the first T. After these redirects, the retained T and both free facets have no terminal descendants and can be pruned. The original 17 SOURCE occurrences, all 28 original RES rows, unchanged terminal pivot, and one paid owner remain. The complete reserialized result is **byte-identical to the original CLI-accepted W29 seed**, proving the last identity and native full-CLI acceptance. QED.

This does **not** show S is optimal among all transformations and does **not** show Q is globally minimum proof work for this source. The formula is fixed; the artificially expanded work is always avoidable by free optimal proof choice.

## Executable original-checker verification

A separately labelled constructor and reference normalizer, **NOT** an authoritative checker, is experiments/arc/lspv2_581_parametric_congruence_gap.cjs, Git blob 0a7640bbea7390288422ee44346ef13bb5f3120a. The exact published script was byte-matched to the locally executed script. Its subprocess calls invoke the unchanged original archived Node CLI.

| Levels k | Expanded W | Structural fixed W | Value + cone W | Structural cost gap |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 33 | 31 | 29 | 2 |
| 2 | 37 | 33 | 29 | 4 |
| 3 | 41 | 35 | 29 | 6 |
| 4 | 45 | 37 | 29 | 8 |
| 8 | 61 | 45 | 29 | 16 |
| 16 | 93 | 61 | 29 | 32 |

Native original checker accepted **19 of 19 positives** (original W29 plus 3 certificates for each k) and rejected **6 of 6 hostile packets**, accumulating **78,122 checker assertion groups** and **209 built-in negative subchecks** on accepted packets. No checker rules or code were modified. Exact k16 examples: W93 has 111 records, 6,945 bytes, RES depth 39; W61 has 79 records, 4,951 bytes, depth 39; W29 has 45 records, 2,867 bytes, depth 7.

Machine-readable raw 25-verdict manifest, exact per-positive packet SHA-256, byte counts, original checker assertions, source SHA, source length and depth: results/raw/arc/2026-11-12_1212_LSPV2_581_NATIVE_CONGRUENCE_GAP_COMPACT.json, Git blob 74809bc68dc96afca3f7b522f561a0455227d146. Exact accepted W93 and W61 JSON bytes are results/raw/arc/2026-11-12_1212_LSPV2_581_ACCEPTED_K16_LIVE_W93.json (blob 507438a9f1a471daeff29155795585ee6638a25b) and results/raw/arc/2026-11-12_1212_LSPV2_581_ACCEPTED_K16_SYNTACTIC_W61.json (blob b4b39da81f3f8bec110e9f184c204f9d01b9aa2b). The W29 output is the already published seed (blob 318c52d99977ea4e91bc8554051138a700c1dc94). The executable reproduces all 25 exact packets and the full manifest.

## Abstract interpretation, alpha/gamma and CEGAR obligation

A /386 concrete configuration includes the immutable signed source bytes/SHA and original occurrences, gate-owner identity bank and fresh signed wires, free facet records, chronological signed parent/pivot proof DAG, precise count-once paid node ledger, summary fields and original CLI terminal check. A restricted signed-value MAY abstraction may track these exact source/owner facts, a set of already proven signed clauses, their earliest chronological representative and a logical-work charge. Every legal paid RES transition with an already-present conclusion admits a zero-cost abstract reuse, otherwise it costs one, hence abstract step cost <= concrete step cost. A DEF facet step remains zero-additional-cost; gate declarations remain globally once-paid. The realizability theorem /539-/562 constructs an accepted cheaper concrete packet for this context-free checker. The present P_k family is a stress control that catches an alpha using only syntactic parent congruence and failing to recognize the genuine cheaper path.

Dropping the final paid owner gives a cheap **spurious full-CLI** W28 representative even though the mathematical inference core accepts W28. Its rejection by the unchanged original wrapper is an implementation-specific checker-control artifact, not a mathematical lower bound. A sound goal-sensitive alpha/gamma must specify whether acceptance is core or complete CLI. Keep all legally available proof choices, not only the syntactically normalized ones.

**Critical limits:** No source-authenticated historical single parser has been recovered for RES-to-AND3, GF(2), LOCAL-CONVERT, paid DEF with mixed contexts, exported/private wires, weakening, branching, AND child obligations, discharge, joins or deletions. The value reuse lemma is proved only for the *context-free* /386 sibling. All missing legal mixed transitions remain MAY-overapproximated, not removed. Full P2-C3, P2-D1, P2-B1 and separate B2/B3 remain OPEN.

**Distinct resources:** The W ledger counts real RES records and distinct paid owners once. Certificate bits, 215 source bytes, construction and verification wall times, RES span and peak physical space are separate. No peak-space bit bound or actual deterministic machine resource lower bound was measured.

## Corpus, originality, references and state reconciliation

Reviewed both current root proof-chain status headers and relevant P1/P2 nodes, issue #3, AGENTS.md, CODEX.md, repository pnp-research skill, latest /580 coordination handoff, original archived checkers, LSPV-2/538 and material /539-/549 parser reports, /552, /562, /579-/580, LSPV-4/539 and neighboring peer counterexamples. Primary proof-complexity, abstract interpretation and CEGAR references: [1] Cook-Reckhow, *JSL* (1979), DOI 10.2307/2273702; [2] Cousot-Cousot, *POPL* (1977), DOI 10.1145/512950.512973; [3] Clarke et al., *CAV* (2000), DOI 10.1007/10722167_15. Separate external proof checkers/standards examined: [4] https://github.com/meelgroup/frat-xor and [5] https://github.com/marijnheule/drat-trim. Required neighboring proof repositories: [6] https://github.com/konard/p-vs-np and [7] https://github.com/blkph0x/p-vs-np-proof-research. None supplies the original unified R_mix341 dispatcher.

**Adopt:** clause-value equality, exact source, once-paid owner identity, terminal dependency closure. **Reject:** the assumption that even *saturated* paid RES structural congruence exhausts legal lower-cost shared-DAG proofs. **Retire:** no previous theorem. The new symbolic counterexample reinforces a restricted P2-C3 soundness/normalization requirement but leaves all load-bearing chain nodes OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root proof1.txt and proof2.txt are unchanged. Root main.tex was deliberately left unchanged because the GitHub connector supplied its SHA but zero readable content, preventing a safe owner-limited complete-content merge/readback.

The existing five designated research automations were independently verified enabled, with unmodified identities, Pacific schedules at :00/:12/:24/:36/:48 and historical TWO Route A / THREE Route B labels. No agent was created, renamed, reactivated, paused or rescheduled.

**Next decisive task:** recover an authentic, externally source-bound original single mixed checker accepting RES-to-AND3 or paid DEF-to-LOCAL-CONVERT dependencies, plus valid and corrupted-port byte packets. The absence of such a checker in inspected results is not a proof it never existed. P versus NP remains OPEN.
