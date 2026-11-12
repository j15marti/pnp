# LSPV-3/583: Two accepted raw support-string lexemes induce the same false affine attribution

**2026-11-11 19:24 PST (America/Los_Angeles) | LSPV-3 Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED original-code theorem + COMPUTATIONAL unchanged original-body V8 replay | P versus NP OPEN**

## Candidate and four falsifiers, fixed before differential execution

**Candidate (P2-D1):** In the unmodified historical archived \`/341\` fixture checker, the *previously accepted SAT-source* packet from LSPV-3/582 contains a malformed AND3 \`support:"012"\` at paid node 50, whose intended numeric source-coordinate union is \`[0,1,12]\`. A different three-character string \`"120"\` with its checker-computed truth table 90 (rather than 102) is also accepted by the same unchanged verifier and makes the same false GF(2) assertion. This is a raw accepted-byte *parser distinction*, not an independently sound refutation, a new historical rule, or a completion of the mixed calculus.

- **F1:** The unmodified checker rejects the rotated string when its truth table is correctly transported.
- **F2:** The same checker accepts correctly typed numeric support \`[0,1,12]\` with the false claimed affine row, or accepts all other permutations of three digits, so the predicted lexical two-element class is wrong.
- **F3:** The original signed 48-clause source has no concrete satisfying assignment, or the advertised affine row evaluates true under the witness.
- **F4:** Hostile unadjusted table, forged SOURCE, bad parent, unsupported opcode or bad sink is also accepted, invalidating the differential.

All four were excluded by exact original-source inspection, independent source evaluation, and unmodified-body replay. A correctly typed support array is **REJECTED** for a concrete reason: it does not permit the false conjunction/table to match, whereas the string silently changes the enumerated coordinates.

## Historical source and scope

Pinned original verifier: \`experiments/arc/lspv2_341_independent_verify.js\`, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**. Pinned original SAT-source packet: \`results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json\`, Git blob **6cf9b0fe1e5a9419e8967d836c707c385418b810**. Recovered archived \`/386\` is a **different** SOURCE/DEF/strict-RES checker, Git blob **338305c0ce101704205e57543756b8127074a986**, and is not part of this accepted-byte proof.

The original archived semantic declaration \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\`, blob **c87acd11d32ccfc3b7acd3667ef11daeb60079cb**, lists RES, AND3, XOR, LOCAL-CONVERT, paid DEF but lacks an executable unified accepted-byte grammar for all rules. The pinned executable explicitly recognizes **only AND3 and XOR** as derived rules, and uses an independent in-band graph/SOURCE fixture rather than an externally caller-bound original DIMACS root.

Reviewed current root \`proof1.txt\` and \`proof2.txt\`, issue #3, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, and current handoffs. Reconciled peer work LSPV-4/539 (archived /386 free-facet and RES quotient), LSPV-3/542-543 (distinct semantic DEF-facet systems), LSPV-2/549 (two-checker polyglot noncomposition), LSPV-3/568, /578, /582, LSPV-1/586 (CEGAR accepted-SAT impossibility), and LSPV-5/499 (different /386 raw SOURCE-coordinate lexical alias); also the Nov. 11 GROKPROOF status and Claude TPORT-0001. This packet **depends** on the previously known SAT-source and malformed support defect. The new, nonduplicated result is the **exact two-element rotation class** and an independently replayed second accepted-byte certificate.

Primary references: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36-50, DOI [10.2307/2273702](https://doi.org/10.2307/2273702) (a proof checker that certifies UNSAT must be sound); Clarke, Grumberg, Jha, Lu, Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000, DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15) (real concrete paths cannot be removed as spurious); Cousot and Cousot, *Abstract Interpretation*, POPL 1977, DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973). The external [FRAT-XOR format](https://github.com/meelgroup/frat-xor/blob/main/format.md) is a **distinct** source-indexed mixed-rule interface, not historical /341 syntax.

## Theorem 583.1: exact two-string support parser ambiguity (restricted original-code theorem)

The original verifier computes the numeric union \`sup=[0,1,12]\` from its two authentic parents. It then applies:

\`\`\`js
p.support?.length===sup.length
new Set(p.support).size===sup.length
sup.every(x=>p.support.includes(x))
\`\`\`

**But it never requires \`Array.isArray(p.support)\`.** With a JavaScript string \`s\`, \`includes(x)\` stringifies the *number* \`x\` and performs **substring** rather than numeric-set membership. Iteration and indexed access, however, enumerate the **individual characters** \`s[0],s[1],s[2]\` as coordinate keys in the eight-row truth-table checker.

Consider all six permutations of the three distinct characters \`0,1,2\`. Exactly the two strings \`"012"\` and \`"120"\` include each of the strings \`"0"\`, \`"1"\` and \`"12"\`. All six have length three and three distinct characters, so the two are exactly the possibilities satisfying the three original membership predicates. This is an exhaustive string-combinatorial claim **only for the declared six-candidate class**, not a characterization of arbitrary UTF-8 input strings or other source supports.

For \`s="012"\`, the checker-computed table is decimal **102**; for \`s="120"\`, it is decimal **90**. In both cases, the truth table is computed over original variables 0,1,2, with bit 12 **never varied**. The original support union is 0,1,12, and the false row metadata stays \`{"mask":"0x1003","rhs":1}\`. The corrupted string consequently bypasses the intended exact original-coordinate test.

**Proof of acceptance distinction:** The original checker performs the above predicates, computes the conjunction table by enumerating \`p.support[j]\`, compares the exact transported table, and checks the advertised row on the same enumerated character indices. The parent clauses, all source rows, chronological IDs and later XOR masks are unchanged. Both accepted records pass every original checker predicate, while the other four strings fail \`AND3 support names\`. This is a theorem about the actual quoted JavaScript statements and was corroborated by running the original full checker body in hosted V8.

## Real SAT-source / false-row countermodel

The packet's original source is a cubic 12-vertex, 18-edge graph with **48 signed original SOURCE clauses**, and a 47-node AND3/XOR paid derivation. Independently evaluate each literal under the assignment

\`\`\`
101001000000100000
\`\`\`

All **48/48 original SOURCE clauses are true**. The first \`charges\` item is JSON string \`"1"\`, retained from LSPV-3/582, so the checker's \`charges.reduce((x,y)=>x^y,0)\` coercion passes while its strict local \`!==\` comparison does not establish correct source parity.

At paid node **50** the original parents are \`[49,3]\`. The advertised affine row is

$$
x_0\oplus x_1\oplus x_{12}=1.
$$

The witness has $(x_0,x_1,x_{12})=(1,0,1)$, hence the left-hand side is **0**, contradicting the claimed RHS **1**. The checker instead evaluates \`table[model_index]\` as true:

| Support string | Table | Assignment's table index | Table says | Real affine RHS satisfied? |
| --- | ---: | ---: | ---: | --- |
| \`"012"\` | 102 | 5 | 1 | **No** |
| \`"120"\` | 90 | 6 | 1 | **No** |

Thus the second accepted certificate is a **real accepted-by-checker path that is not a mathematically sound refutation of its original SAT source**. The same source binding and row defect were previously found by peers; the new exact variant tests the parser's two-lexeme ambiguity, not a new independent source-unsoundness mechanism.

## Original full checker execution and hostile controls

The **unchanged original verifier body** ran in hosted V8 via \`new Function\` with adapters ONLY for \`require('fs')\`, \`process.argv\`, and \`console.log\`. The inference, source, support, affine, provenance, sink, and built-in hostile-check logic was not rewritten. Original-body count **3,273 assertions** per accepted packet, including its seven malformed-CNF and five fixture-corruption controls.

- Accepted: original \`"012", table=102\`, rotated \`"120", table=90\` (**2/2** positive).
- Rejected: the other four three-character digit permutations (**4/4**), unadjusted rotated table, correct numeric support with false table, array of string support keys, four-character string, numeric first charge, forged source literal, unsupported LOCAL-CONVERT, nonexistent parent, and incorrect terminal row (**9/9** additional hostile cases).

Total **15** tests, **2 ACCEPT** and **13 REJECT**. Both accepted source-labelled packets retain all 48 original signed clauses, 47 paid inference records, all antecedent IDs, 18 original variables, and source assignment. The new exact compact JSON plus LF is **8,573 bytes**, one byte shorter than the original due to replacing decimal table \`102\` by \`90\`. The source clauses and all node IDs are unchanged. Byte length is not paid logical work.

**Execution qualification:** Hosted V8 executed the original body. The separately published Node.js \`vm.runInNewContext\` OS process reproducer is complete and pinned to original Git blobs, but **that published Node subprocess has not been executed in this run**. No independent reimplementation is represented as authoritative.

## P2-D1/P2-C3 canonical semantics and CEGAR firewall

The actual original \`/341\` accepted-byte state needs a distinction between the numeric intended set \`{0,1,12}\`, raw \`support\` JSON *type and lexeme*, its string-substring membership behavior, its character-wise table enumeration, true original-coordinate semantics, signed SOURCE ancestry, and independently verified externally pinned SAT meaning. Identifying these two strings with a sound numeric support set while treating accepted rows as genuine logical consequences **falsifies semantic adequacy**.

An acceptance-complete abstract transformer must include the **genuine checker ACCEPT** path. A mathematical soundness abstraction must simultaneously reject it as an UNSAT proof based on its actual SAT source and false row. These are different transition goals and must not be conflated (LSPV-1/586). Sound CEGAR cannot classify a real checker-accepted trace as spurious merely because its parser bug is inconvenient.

The historical full \`R_{\mathrm{mix341}}\` remains **unknown**. For full-calculus abstract semantics, unlocated Resolution-to-AND3, DEF facet-to-GF(2), LOCAL-CONVERT, exported/private wires, branching, weakening, discharge, joins, deletion, global freshness and all their fixed historical weights remain **UNKNOWN/MAY**, and are **not** inferred from the recovered /341 acceptance grammar. Free ideal proof selection, shared proof DAG, original-source provenance, count-once paid ownership and contexts remain separate.

## Reproducibility / publication receipts

1. **New immutable exact accepted certificate:** \`results/raw/arc/2026-11-11_1924_LSPV3_583_ROTATED_SUPPORT_SAT_ACCEPTED_PACKET.json\`, Git blob **5d78d8f6eb5934bf805ee90736b1f88d4acd2729**.
2. **15-case original-body raw ledger:** \`results/raw/arc/2026-11-11_1924_LSPV3_583_SUPPORT_STRING_ROTATION_V8_RAW.json\`, Git blob **2227183f393442a7bd3d242f93618a4f2ddd8426**.
3. **Complete runnable pinned standalone Node replay (OS execution pending):** \`experiments/arc/lspv3_583_support_string_rotation_native_replay.cjs\`, Git blob **07cfb86f32607e6a6d25a2d20f06e45d8e54fafa**. Run from repository root: \`node experiments/arc/lspv3_583_support_string_rotation_native_replay.cjs\`.
4. Dated role-owned five-role handoff in \`research/coordination/\`, also requiring full GitHub readback.

All three listed artifacts were individually published to the repository default branch, fetched back, and compared with the exact authored content. Published node identities are canonical and are not inferred from semantic clause equality.

## Status, materiality and next handoff

**[P2-D1] OPEN:** additional exact historical fixture parser distinction; not recovered unified calculus. **[P2-C3] OPEN:** acceptance and sound source-root mathematical refutation must remain separate; no full cost-sound rule-by-rule transformer. **[P2-B1] OPEN**, with **[P2-B2]/[P2-B3] independently OPEN**; no general lower bound or SAT-decision transfer. **P1-01/P1-03/P1-04 OPEN**. **P versus NP remains OPEN**.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** New evidence refines the existing restricted parser-lexeme subclaim but does not change the status of any root proof-chain node. No historical fixed weight, role, ownership boundary, title, identity, or two Route A / three Route B assignment was changed; no automation mutation was requested or performed.

**Next decisive experiment:** recover a *single* original-source-external-input-bound historical checker with one dispatcher accepting a genuine RES-to-AND3 or paid DEF-facet-to-LOCAL-CONVERT/GF(2) edge. Until then, preserve raw parser acceptance separately from source/root soundness and record any missing native transitions as MAY rather than silently substituting CANON1/2/2R.
