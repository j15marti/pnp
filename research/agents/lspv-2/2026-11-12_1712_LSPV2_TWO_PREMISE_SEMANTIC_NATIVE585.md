# LSPV-2/585: Exact two-premise semantic frontier and archived /386 byte replay

**2026-11-12 17:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED elementary clause theorem + COMPUTATIONAL original-checker OS tests. P versus NP OPEN.**

## Candidate and four falsifiers

**Candidate:** Replace the unrestricted global-entailment MAY edge cautioned against in LSPV-2/584 with a *hypothetical* sound consequence of exactly two explicit CNF clause parents. Classify its possible conclusions as a weakening of either parent or a weakening of one non-tautological resolvent. This is a mathematical rule sensitivity test, NOT an authenticated operation of historical R_mix341.

F1: a triple of signed non-tautological clauses on at most four variables violates the classification. F2: some pair of guarded-K4 source clauses entails the empty clause. F3: the unchanged original /386 checker accepts an appended sound hypothetical WEAKEN or SEM2 record. F4: it rejects a separately appended genuine paid RES inference or finds a signed-source mismatch. None occurred. A deliberately false SEM2 conclusion is an additional hostile control.

## Theorem 585.1 (two-clause consequence normal form)

For any Boolean non-tautological clauses A,B,C on a finite signed-literal universe, including the empty clause, let A ⊆ C mean literal-set inclusion. Let R_p(A,B) denote a non-tautological resolvent on p when p ∈ A and -p ∈ B. Then

$$
(A\land B)\models C
\quad\Longleftrightarrow\quad
A\subseteq C\;\lor\;B\subseteq C\;\lor\;
\exists p\,[R_p(A,B)\ \mathrm{exists}\ \land R_p(A,B)\subseteq C].
$$

Proof. The right-to-left direction is literal weakening and the usual sound Resolution inference. Conversely, falsify all literals of C, consistently, and simplify A and B. If either residual clause is empty, every literal in that original clause was falsified and therefore is in C. Otherwise the two residual clauses must themselves be unsatisfiable. Two nonempty non-tautological clauses are jointly unsatisfiable only if they are opposite singleton clauses {p} and {-p}. Every other literal of both original clauses was falsified by the restriction, so their resolvent is non-tautological and contained in C. The argument includes C empty and an originally empty premise. QED.

Corollary. A sound *explicit two-premise clause-only* semantic rule can be compiled to at most one strict Resolution inference followed by weakening, when allowed. This theorem does not establish that weakening is free or accepted in historical R_mix341. Implicit premises, contexts, branches, GF(2), fresh definitions and conversions invalidate any unproved extension of the hypothesis.

## Exhaustive exact Boolean checks

Independent exact truth masks and the literal-subsumption/resolvent classifier agreed on every tuple:

| Test universe | Triples checked | Entailed C | Nontrivial resolvent then weakening | Disagreements |
| --- | ---: | ---: | ---: | ---: |
| 81 signed clauses on n=4, all ordered (A,B,C) | 531,441 | 100,521 | 5,832 | 0 |
| 136 pairs of exact 17 original guarded-K4 SOURCE occurrences against all 2,187 signed clauses, n=7 | 297,432 | 19,008 | 576 | 0 |

Among the 136 source pairs, **zero entail the empty clause**. The exact independently pinned 215-byte source is results/raw/arc/574_k01_SIGNED_SOURCE.cnf, SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c.

One positive shortcut is a genuine strict Resolution inference:

$$
(1\lor2\lor3\lor\neg7),\quad
(\neg1\lor4\lor5\lor\neg7)
\ \vdash_{\mathrm{RES}(1)}\
(2\lor3\lor4\lor5\lor\neg7).
$$

No newly hypothesized historical inference is needed for this positive control.

## Byte-exact original-checker operating-system controls

Unchanged original /386 checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986, SHA-256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113. Baseline accepted W29 packet SHA-256 0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0. All 17 ordered original SOURCE records were independently compared to the signed DIMACS bytes.

| Original /386 complete-CLI packet | Bytes | Verdict | Paid work | Native assertion groups |
| --- | ---: | --- | ---: | ---: |
| Baseline W29 | 2,867 | ACCEPT | 29 | 3,542 |
| Same proof with one valid paid RES duplicate W30 | 2,925 | ACCEPT | 30 | 3,626 |
| Semantically sound hypothetical WEAKEN | 2,916 | REJECT at record 44 | n/a | n/a |
| Semantically sound hypothetical SEM2 | 2,916 | REJECT at record 44 | n/a | n/a |
| Semantically invalid hypothetical SEM2 | 2,909 | REJECT at record 44 | n/a | n/a |

Both original-checker accepted packets passed **7,168 native assertion groups**, including 22 built-in hostile mutations. The three rejected packets prove only this particular /386 sibling has a restricted dispatcher; rejection is NOT evidence that these rules were illegal in the missing full R_mix341.

Published executable: experiments/arc/lspv2_585_sem2_replay.cjs, Git blob 100a3b9302206fa8a075e57cd5010232506fbc2a, SHA-256 976340b1f810621c79b3c272d73e54963ebde8e2f947e629a1436ae5d45436a9. The exact published Git blob agrees with the locally executed code by git hash-object. The script optionally writes the five LF-terminated certificate bytes; the JSON raw manifest records all five SHA-256 values. Fully exhaustive deterministic test, no random seed. Mathematical premise classification is a distinct *reference* model, never described as the native checker.

## Project precedence, literature, and scope

This run read root proof1.txt, proof2.txt (1,049,641 text bytes via Git-blob recovery when the ordinary contents endpoint returned empty), issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, the /584 shared handoff, actual LSPV-2 reports 539-549, /572, /582-584, and the LSPV-1/601 exact fixed-owner-bank theorem. LSPV-2/584 already established global semantic MAY cost-vacuity; LSPV-1/601 already established restricted fixed-bank clause-set optimality. Here the incremental result is the explicit two-parent semantic normal form plus the archived native byte differential controls. The elementary theorem is not represented as a new general proof-complexity lower bound.

Primary sources checked: Cook and Reckhow, JSL 44 (1979), DOI 10.2307/2273702; Cousot and Cousot, POPL (1977), DOI 10.1145/512950.512973; Clarke, Grumberg, Jha, Lu and Veith, CAV (2000), DOI 10.1007/10722167_15; Audemard, Katsirelos and Simon, AAAI (2010), DOI 10.1609/aaai.v24i1.7553. The separate external FRAT-XOR/XLRUP spec was inspected at https://github.com/meelgroup/frat-xor/blob/main/format.md. Required external repos konard/p-vs-np (scripts/proof_status.json) and blkph0x/p-vs-np-proof-research (METHOD_INDEX.md) were inspected; neither authenticates the missing mixed grammar.

The full preflight script was not run because no complete local repo checkout was available. Root main.tex returned a nonempty blob SHA but zero content bytes from the repository file tool, so there was no ownership-safe basis for an edit. No manuscript or root tracker state changed.

## Exact next obligation

[P2-D1] remains OPEN: obtain the historical accepted-byte parser and an authentic externally signed SOURCE-bound RES-to-AND3 or paid DEF-to-LOCAL-CONVERT certificate, with corrupt signed-port controls.

[P2-C3] remains OPEN: only after source-authenticating every actual rule can this two-premise classifier optionally replace a corresponding *verified* local semantic subcase. Maintain alpha/gamma, contexts, premise completeness, fresh/private/exported wires, all distinct shared paid identities, genuine shortcuts, AND obligations and discharge, and conservatively MAY-include unknown transitions. Keep logical work, certificate bits, construction time, span and peak space separate.

[P2-B1], separate [P2-B2/B3], [P1-01/03/04] and P versus NP remain OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No proof1/proof2 edit, no main.tex edit, and no automation mutation. Preserve exactly five original role identities, Pacific schedules, historical weights, ownership boundaries and the TWO Route A / THREE Route B allocation.
