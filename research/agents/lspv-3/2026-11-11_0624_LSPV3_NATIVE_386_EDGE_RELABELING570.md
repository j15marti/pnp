# LSPV-3/570: Original /386 native source-edge relabeling equivariance

**2026-11-11 06:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Candidate and falsifiers registered before the source experiment

**Candidate:** Every permutation of the original edge-variable identifiers, transported simultaneously through the labeled source graph, source literals, true nested DEF facets, gate inputs, and signed RES inferences, preserves acceptance by the recovered archived /386 mathematical core and exactly preserves the whole shared-DAG paid cost. It acts on relabeled in-band formulas, not on one fixed externally hashed CNF.

F1: SOURCE parity or completeness fails. F2: nesting, facet type or signed RES pivot fails. F3: the unchanged original checker rejects or mischarges the transformation. F4: an inconsistent edges-only or proof-only partial transport is accepted. Source-code proof below addresses F1-F3 universally for the mathematical core. The full native-code K4 differential rejects F4 and six other corruptions.

## Exact authority and comparison

Both proof1.txt and proof2.txt, issue #3, AGENTS.md, CODEX.md, pnp-research SKILL.md, original /341 declaration and /341 vs /386 parsers, current handoffs, LSPV-2/539 and /549 plus subsequent peer work, LSPV-3/561-569, LSPV-1/566, /570-572, LSPV-4/541-542, LSPV-5/485-487, relevant Grok and Claude reports were reviewed. Native original checker: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. Original nested owner K4 packet: results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json, blob **08aa169b5db49b2ddd1cb5a9b6890fcc3b790916**.

This relabeling is different from /565 edge **sign complementations**, /569 disconnected-component charge orbits, LSPV-1/566 **proof-record reorderings**, and LSPV-2/554 **paid gate-owner declaration reorderings**. Native FRAT-XOR/XLRUP and its certified checker are separate external formats, not historical R_mix341 (https://github.com/meelgroup/frat-xor). Primary context: Cook and Reckhow 1979 (https://doi.org/10.2307/2273702), Cousot and Cousot 1977 (https://doi.org/10.1145/512950.512973).

## Theorem 570.1: exact original /386 core source-relabeling symmetry

Let P be a parsed packet accepted by the exact archived /386 mathematical core with E original graph edges and pi any permutation of the E edge numbers. Form T_pi(P) by moving graph edge at index i to index pi(i) and replacing each signed original edge variable +/- (i+1) by +/- (pi(i)+1) in **every** SOURCE, DEF and RES clause, gate input and signed RES pivot. Re-sort clauses in the original checker's canonical signed order. Preserve original vertex labels, charge, guard, globally paid auxiliary outputs and owner IDs, all record parent indices, chronological order and summaries.

Then

$$
\mathrm{Core}_{386}(P)\Longrightarrow\mathrm{Core}_{386}(T_\pi(P)),
\qquad
W_{386}(T_\pi(P))=W_{386}(P)=N_{\rm RES}+N_{\rm owner}.
$$

The map is inverted by pi inverse, and every SOURCE/DEF/RES native core transition commutes with this map. Therefore alpha mapping each concrete prefix to its S_E orbit and gamma returning the orbit is a goal-preserving, exact-cost abstraction on this **three-kind archived fragment**, not on the full historical mixed calculus.

**Proof.** Each vertex's four forbidden signed SOURCE clauses are computed from its three incident **edge-array positions** and binary charge. Permuting those positions and every corresponding signed literal bijectively carries the exact original local source set to the new local set, retaining the positive guard unit, source count and completeness. Original gate-owner checks validate signed old-edge or already declared conservative gate inputs; the map moves only old-edge coordinates, leaving fresh outputs and dependent owner DAG untouched, and its computed three defining facets transform identically. For every RES parent pair with pivot p and -p, the mapped pair contains mapped p and -mapped p. Canonical resolution commutes with atom bijection and resorting. Induction on unchanged chronological parent IDs proves every derived clause including the empty sink. Counts and globally paid owner IDs are unchanged; its E<=12 parity model count is a bijection on assignments. Applying pi inverse restores every parsed clause, so the map is invertible. QED.

**Full-CLI condition is nontrivial:** LSPV-1/571 proves the original eleven-test CLI further requires at least one paid owner and the terminal numeric RES pivot **not equal to +999999**. Hence full-CLI acceptance transfers only if the transformed final pivot also differs from +999999. For E<999999 this follows automatically when P was full-CLI accepted; with E>=999999 a raw edge renaming could hit that sentinel. Do not assert unqualified full-CLI equivalence on arbitrary huge inputs.

## Original checker experiment

Pinned unchanged checker body was executed directly in hosted V8 with filesystem/console and **output-only** digest adapters, including the complete original eleven built-in negative tests. The separately published OS Node subprocess runner was not executed as an OS process in this run.

Fixture: signed guarded K4, E=6, 17 SOURCE, 2 globally paid nested AND2 owners, 6 zero-extra-paid DEF facets, 51 strict signed Resolution nodes, 74 chronological records. **W=53.**

**32/32** deterministic full transports were accepted by original checker, **31 distinct** permutations, **32/32** exact inverse parsed-packet roundtrips, each positive **4663 original checker assertions**, combined **149216 assertion groups**. Reverse edge permutation native certificate is **4421 compact JSON bytes**, W=53. Eight extra corrupted original packets were all rejected: graph-only permutation, proof/owner-only permutation, charge change, source literal sign, DEF facet, pivot, paid summary and unsupported LOCAL-CONVERT opcode. The latter excludes the opcode only from this distinct /386 checker.

## Soundness limits and publication

A relabeled source is a **different raw labeled external source**. Source-retracting abstraction must retain any independently verified original-source hash **plus explicit renaming**; the archived /386 code only verifies its own in-band spec. Never conflate external-source hash with an isomorphic signed source. It has no recovered native AND3, GF(2), LOCAL-CONVERT, branch/weakening/discharge, private/exported wire, join or deletion rules. No new mixed-rule lower bound or P-versus-NP implication follows. P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 all remain **OPEN**.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Original main.tex blob 18e38478fc623aaf970a50b4dfe432e204098964 returned zero content via the GitHub contents connector. Since no complete body was available for safe owned-region merge, main.tex was not modified. Preserve all five current agent identities, schedules, weights and TWO Route A / THREE Route B allocation. P versus NP OPEN.
