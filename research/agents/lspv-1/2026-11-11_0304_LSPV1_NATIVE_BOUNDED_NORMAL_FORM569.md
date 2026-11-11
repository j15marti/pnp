# LSPV-1 Result 569: bounded native certificate normal form and actual OS-Node verification

**2026-11-11 03:04 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Candidate theorem and falsifiers stated before the literature and corpus search

**Candidate 569.1.** Every accepted parsed certificate of the original archived /386 SOURCE/DEF/RES mathematical checker with fixed source spec, h vertices and total logical cost W has a same-source, same-cost accepted canonical certificate with at most 4h+1+4W records, dense paid-owner labels and dense fresh output-wire labels (skipping the fixed guard). Thus, for any fixed source and K, existence of a /386 mathematical-core refutation of logical cost at most K reduces to a FINITE enumeration. This is NOT a theorem for full historical R_mix341.

**Falsifiers:** (F1) a genuine SOURCE occurrence is lost or its signed clause/source vertex changes; (F2) changing owner or output-wire labels breaks an accepted gate facet or RES pivot; (F3) removing repeated zero-priced DEF views invalidates a chronological parent; (F4) a claim of complete-CLI acceptance is inferred from mathematical-core acceptance even though original negative self-tests reject the packet. F1–F3 were ruled out for the actual /386 mathematical grammar by the constructive proof below, and tested on a two-owner chain. F4 is REAL and deliberately excluded from the theorem: the native 28-RES, zero-owner proof is accepted by the mathematical core but rejected by the full CLI.

## Preflight and primary-source scope

Read current root proof1.txt (Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), proof2.txt (Git blob 20fd65cf8842d32a851a14a1496c7ea6156cb160), issue #3 and recent comments, AGENTS.md (4ae902888754d0b06ba4ce1aaeca0657a92b46a9), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), and .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f). Reconciled five handoffs LSPV-1/568, LSPV-2/553, LSPV-3/566, LSPV-4/539 and LSPV-5/483, along with relevant earlier 539–549 reports/corpus. The complete historical mixed checker still was not located; two archived sibling checkers are not a unified system.

Primary literature checked: Cook–Reckhow (1979), Journal of Symbolic Logic 44:36–50, DOI 10.2307/2273702; Cousot–Cousot (1977), POPL:238–252, DOI 10.1145/512950.512973; Ben-Sasson–Wigderson (2001), JACM 48:149–169, DOI 10.1145/375827.375835; FRAT-XOR/XLRUP author format https://github.com/meelgroup/frat-xor/blob/main/format.md; Efremenko, Garlik and Itsykson, Lower Bounds for Regular Resolution over Parities, DOI 10.1137/24M1696640. None establishes full R_mix341 semantics or a lower bound for unrestricted DAG resolution over parities.

## Theorem 569.1 (PROVED/RESTRICTED): cost-bounded finite core normal form

Fix a source specification s=(h,edges,charge,guard) for which the *exact* original /386 mathematical checker accepts some parsed refutation P. Let g be the number of globally declared, distinct paid gate owners, r the number of RES records, and W=g+r. The original checker already forces exactly 4h+1 distinct signed SOURCE occurrences, one per original guarded parity clause and one positive guard unit. Let Q be the following explicit transformation:

1. Preserve each SOURCE occurrence, its signed clause, source-vertex tag, and the entire s object, moving all SOURCE records to the front while maintaining a complete old-to-new positional-reference map.
2. Preserve all g original gate-definition semantics and their declaration order. Canonically rename gate IDs to 0,...,g-1 and map their output wires, in declaration order, to the first g integers strictly greater than the original edge count, excluding the source guard. Apply this signed, injective coordinate renaming to every gate input, DEF facet, RES clause and RES pivot. It fixes every original edge variable and source guard.
3. Preserve at most one DEF record for each (gate owner, canonical facet clause) pair, and redirect all references to a removed later duplicate to the earlier retained facet. Every owner has at most three possible defining facets because this checker implements AND2 views [[-z,a],[-z,b],[z,-a,-b]]. These views are zero-priced. All gate owners are declared globally before records are scanned and DEF views have no record parents.
4. Preserve each RES record in its original relative order, update its parents using the old-to-new reference map, and re-sort its clause and pivot under the wire renaming. Every RES parent remains before its child. Preserve the final empty-clause sink. No paid RES occurrence or owner is erased or duplicated.
5. Recompute the exact summary counters from the retained record list and owner list.

Every SOURCE, DEF and oriented strict RES check is invariant under this transformation. Original-source completeness is unchanged. The checker's graphical parity and model-count controls depend only on s, which is unchanged. Every old parent denotes a newly earlier record with the same renamed canonical clause. The checker therefore accepts Q with precisely

$$
W_{\mathrm{386,core}}(Q)=r+g=W_{\mathrm{386,core}}(P).
$$

Moreover,

$$
N_{\mathrm{records}}(Q)\le (4h+1)+3g+r \le 4h+1+4W.
$$

There are finitely many canonical wire labels, owners, clauses, record positions, parent pairs, pivots and possible gate tuples for every fixed source and K. Enumerating these finitely many canonical packets and running the pinned checker decides *whether there exists* an accepted parsed /386 mathematical-core proof of cost W<=K. If an accepted proof exists, its exact minimum can be computed by searching increasing K; no claim is made about polynomial discovery time or about termination of unbounded minimization on a source with no accepted proof. For a fixed source and K the normalized search space is finite, even though raw accepted packets admit repeated zero-cost facets and unbounded numeric spelling choices.

**Important distinctions.** This is a cost-preserving existence result over complete shared proof DAGs, not an assertion that the original full CLI self-tests accept every normalized packet. It preserves charged owners once and free views without charging each occurrence. It does not provide abstract transformers for AND3, GF(2), LOCAL-CONVERT, weakening, branching, contexts, discharge or joins. It does not equate logical node work with evidence bits, parsing, search, CPU runtime, span or peak writable space. The theorem is independent of proposed CANON1/2/2R systems.

## Independent actual operating-system Node.js verification (COMPUTATIONAL)

For the first time in the LSPV-1/568 chain, ran the original archived /386 verifier as an actual Node.js 22.16.0 OS subprocess. Recreated its 6,345-byte source **byte-for-byte** and confirmed Git blob 338305c0ce101704205e57543756b8127074a986. Independently regenerated both complete 568 witness packets with byte-exact Git hashes, including the 7,674-byte core-only packet c68eeaf67015416dae49a34ad5ce25432b839bee and the 7,724-byte full-CLI witness e3eb2a46857776089ab83f4ad50159ef622d2869. Source-independent brute-force evaluation found 0 satisfying assignments among all 64 original edge assignments.

The mathematical core accepted the 28-paid witness; the unchanged complete CLI rejected it as its owner-deletion corruption is a no-op. The unchanged complete CLI accepted the 29-paid witness, including all **11** original built-in hostile checks, with **3,542** check assertions.

A separate source-exact specimen used two paid, nested fresh AND2 owners (raw owner IDs 900/901 and wires 135/136), 10 legitimate repeated free DEF facets, 28 original RES nodes and all 17 original SOURCE occurrences. The original complete CLI accepted at W=30, 55 records and 3,560 check assertions. Its canonicalized version used IDs 0/1, wires 8/9, two free facets and 47 records; the original complete CLI accepted at the identical W=30, 3,223 assertions. Independent normalizer idempotence passed. Four hostile source, future-parent, paid-tariff and undeclared gate-input packets were rejected both by the original mathematical core and by the actual OS CLI.

All positive files, hashes and counters are in the machine-readable raw artifact. The reproducer uses only Node standard libraries; it imports the unchanged verifier source and original 568 packet by exact Git blob hashes. The core function text is unmodified; a VM only exposes it for direct mathematical acceptance testing. The full CLI runs separately as a real operating-system subprocess. The original verifier's own output hash is now independently measured; unlike earlier hosted V8 results, this is not a substituted filesystem/hash interface. Neither physical allocator-level peak memory nor generic machine-model time is measured.

## Dependencies, governance and disposition

[P2-D1] remains OPEN: only the distinct archived /386 SOURCE/DEF/RES system was authenticated, not a single original R_mix341 checker implementing all legal rules. [P2-C3] remains OPEN: this is a valid original-core restricted normal form and finite-K enumeration, not a complete cost-sound alpha/gamma simulation. [P2-B1] remains OPEN: no superpolynomial minimum-work lower bound is proved for the full mixed calculus. [P2-B2]/[P2-B3] remain separate and OPEN: no all-input same-calculus SAT-algorithm transfer is proved. P1-01/P1-03/P1-04 remain OPEN. P versus NP remains OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither root tracker was modified: the new theorem does not close or falsify a load-bearing node. Root main.tex was read via the connected GitHub file interface, but it returned empty content for this approximately 2-MB file, so a conflict-safe full-content ownership-region update could not be authenticated; main.tex was **not modified** to avoid corrupting other roles. The report and coordination handoff serve as the role-owned publication until an intact manuscript read is available. No automation, role title, schedule, identity, Pacific timezone, fixed historical rule/weight, ownership region or two Route A/three Route B allocation was altered.

**LSPV-5 falsification request:** independently rerun actual OS Node; attack the canonical renaming and duplicate-facet deletion on packets with actively used nested wire pivots, final-pivot CLI sentinels and branch-context counterexamples; classify core and CLI acceptance separately. **Next P2-D1 target:** independently source-bound accepted-byte mixed RES+AND3/GF(2)/LOCAL-CONVERT transition from one authoritative original checker.
