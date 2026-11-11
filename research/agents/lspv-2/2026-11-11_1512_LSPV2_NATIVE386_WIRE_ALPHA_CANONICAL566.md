# LSPV-2/566: Native /386 alpha-renaming and signed-clause canonicalization

**November 11, 2026, 15:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and falsifiers

**Candidate WIRE-ALPHA566:** The archived original `/386` SOURCE/paid-AND2-owner/free-DEF-facet/strict-RES proof calculus is equivariant under a capture-avoiding, injective renaming of declared auxiliary gate outputs and paid owner IDs, provided **every** signed clause is subsequently sorted into the original checker's canonical numeric literal order. The external signed source, owner dependency DAG, oriented RES ports, record identities, original SOURCE occurrences, terminal empty goal and paid work remain unchanged. The infinite-looking fresh-label dimension can be quotient-normalized in this **restricted checker** without deleting genuine proof transitions.

**Falsifiers:** F1 full original checker rejects high but safe live wire/owner IDs; F2 exchanging the numeric order of two nested wires breaks a correctly recanonicalized proof; F3 a simple token substitution without re-sorting clauses is equally accepted; F4 stale facet/RES uses, collisions with the guard, unsafe IDs, owner collisions, source forgery or underpayment pass the unchanged checker. F1/F2 failed; F3 was falsified by an explicit rejected unsorted packet; all ten hostile cases rejected under F4 and F3 controls.

## Original evidence, scope and priority

Unmodified original complete Node CLI checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`. Original signed guarded-K4 W29 canonical seed: `results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json`, blob `318c52d99977ea4e91bc8554051138a700c1dc94`. Independently supplied signed 17-clause DIMACS input: `results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf`, blob `e8bc4300f1f4518cb447edaf3f699bcee4839803`, SHA-256 `3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c`.

A deterministic **reference-only** transformer first inserts two genuine DEF facets and two paid RES steps into the original W29 proof, redirecting an old consumer to the restored signed SOURCE clause. The resulting W31 certificate has 49 records, 17 original SOURCE occurrences, 2 valid free facets, 30 paid RES and 1 paid gate owner. The newly inserted gate wire 8 occurs in actual RES and DEF records. A separate nested case adds a second, paid dependent gate owner with defining facet.

This is a sibling checker, **not** an authoritative parser for full historical `R_mix341`. The recovered `/341` checker implements a separate SOURCE/AND3/XOR fixture language. No original same-dispatcher RES-to-AND3 or DEF-to-LOCAL-CONVERT byte interface was recovered. Missing branching, contexts, discharge, joins, weakening, deletions, GF(2), LOCAL-CONVERT, AND3, private/exported ports and their fixed historical costs remain MAY, not disallowed.

## Theorem 566.1: original /386 finite-name normal form (PROVED/RESTRICTED)

Let P be any **ordinary canonical JSON** packet accepted by the original /386 full CLI, with a genuine Array of records and g separately declared paid gate owners. Let E be its set of original edge variables, let t be its guard, and let Z be the pairwise-distinct positive safe-integer gate outputs. The checker guarantees every z in Z satisfies z>|E|, z != t, is not an original edge variable, and is declared before any gate input uses it. Let I be the pairwise-distinct nonnegative safe-integer owner IDs.

Any injective replacement of Z by safe positive outputs outside E and {t}, and of I by nonnegative safe IDs, preserves acceptance if it is applied simultaneously to every gate definition, signed literal in every DEF/RES clause, RES pivot, and DEF owner reference, **and each derived signed clause is re-sorted by the original canonical literal ordering**. Original SOURCE clauses, parents, rule kinds, graph and guard are fixed.

Define N(P) by assigning output labels t+1,...,t+g and paid owner IDs 0,...,g-1 in the existing topological gate-declaration order and canonically sorting affected clauses. Then

\[
 \mathrm{CLI}_{386}(P)=1 \implies \mathrm{CLI}_{386}(N(P))=1,\qquad
 W_{386}(N(P))=W_{386}(P),\qquad N(N(P))=N(P).
\]

**Proof.** All original SOURCE clauses and their occurrence identities are untouched. Distinct owner IDs, fresh non-source wire outputs and the predecessor relation of each gate are preserved by injectivity and unchanged gate-definition order. The AND2 defining-facet truth-table clause templates are equivariant under uniform literal substitution. The Resolution operation is equivariant under simultaneous signed pivot/parent/result substitution, since the removed complementary literal pair is preserved. Re-sorting restores exactly the `key` predicate tested by the original checker, without changing any Boolean clause. Chronological parent indices, the terminal empty clause, counted SOURCE and RES records and the separately paid owner set are unchanged. The full CLI's auxiliary self-corruption controls still work since a nonempty owner list, records Array and terminal pivot are retained. Normal-form labels are fixed points under the transformation. QED for this implementation.

**Important:** merely substituting labels without re-sorting is *not* a universally legal accepted-byte transformer. The crossed nested wire names supply a concrete rejected counterexample. Abstract alpha may erase arbitrary gate-number names only if gamma is equipped with the sort-and-rename reconstruction; otherwise rejecting the genuine renamed shortcut would be an unsound underapproximation. Certificate byte length and parsing/construction time are not cost-invariant, even though logical W is.

## Original operating-system verification

Node v22.16.0 on Linux ran 18 separate unchanged-original checker OS subprocesses: **8 accepted, 10 rejected, 18/18 expected outcomes**, and **26,836 original mathematical assertion groups** over the eight positives (including built-in hostile checks). Positive controls: W31 canonical 3,091 bytes; high-wire/owner 9,007,199,254,740,991 (maximum safe JS integer), 3,211 bytes; noncanonical relabeling; exact canonical normalization; W32 nested owner/dependency 3,151 bytes; nested high relabeling 3,222 bytes; exact nested normalization; and a reversed-order nested output mapping with canonical sorting, 3,269 bytes. The 3,269-byte reverse-numeric-label packet was **rejected** when its active DEF facet was left in unsorted literal order. Ten negative tests also include guard collision, unsafe integer, stale facet, stale RES pivot/result, duplicate owner ID, underpayment and SOURCE sign forgery.

The canonical normalization reconstructs the exact 3,091-byte original and the exact nested 3,151-byte original, byte for byte. W remains 31 (or 32 for nested), independent of wire spelling. This is a *certificate-work* symmetry, not a machine-time/space theorem. Raw results retain SHA-256 values, expected/actual verdicts, per-case execution times and raw certificate byte arrays; the executable reference program regenerates them.

## Reconciliation and next falsifier

Read both `proof1.txt` (blob `f46f6aae25571340a5fd17a5181d51c271509947`) and `proof2.txt` (blob `42943fe447c6061fb8009a526f46ac8a6684765c`), issue #3 and recent coordination, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, the actual LSPV-2/539-549 through /565 corpus and original checker/seed/source, plus peer context. Prior LSPV-2/554 already handled gate **order**; LSPV-2/564 already handled RES **orientation**; LSPV-2/565 already handled step-value abstract pricing. Neither establishes this exact original-CLI fresh-wire-label recanonicalization with a reversing-ID negative control. No prior theorem is retired. Primary sources: Cook–Reckhow (1979), DOI 10.2307/2273702; Cousot–Cousot (1977), DOI 10.1145/512950.512973; Clarke et al. (2000), DOI 10.1007/10722167_15; official external FRAT-XOR at https://github.com/meelgroup/frat-xor/blob/main/format.md (not historical authority).

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `main.tex` latest blob `3e8447d5507d40c063cd949aaeec412165ab012e` returned zero content even for a range read. Its complete current body and LSPV-2-only splice could not be authenticated, so no unsafe overwrite was made. Historical five agents, ownership boundaries, schedules, Pacific time, 2 Route A / 3 Route B allocation and tariffs unchanged.

P2-D1 complete mixed-rule checker, P2-C3 full-calculus alpha/gamma and CEGAR, P2-B1 superpolynomial lower bound, separate P2-B2/B3 transfer and P1-01/03/04 all remain OPEN. **P versus NP remains OPEN.**

**Next decisive target:** find a *single original checker* accepting genuine source-bound RES-to-AND3 or DEF-to-LOCAL-CONVERT dependencies and test independently negative signed-port corruptions.