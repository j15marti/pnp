# LSPV-3/613: Native /341 terminal-object identifiers and a sound terminal-key quotient

**2026-11-13 05:30 PST | Hypergraph & Proof Certificates | Route B | PROVED/RESTRICTED source theorem plus COMPUTATIONAL original-body replay. P versus NP remains OPEN.**

## Candidate and four falsifiers, fixed before the focused original-body tests

**Candidate [P2-L3-613]:** For the original archived SOURCE/AND3/XOR checker, the terminal paid node may have any valid JSON object or array as its `id`; nonterminal paid nodes and SOURCE records cannot use separately parsed object/array identifiers because each must be referenced from another JSON position. Consequently, object/array terminal identifiers admit an exact semantics- and cost-preserving canonicalization to a fresh terminal atom in this **restricted checker**.

- F1: An object-valued or array-valued terminal ID rejects because of native Map freshness or root ancestry.
- F2: A SOURCE object/array ID is successfully re-referenced by a structurally identical JSON parent object/array.
- F3: A nonterminal object/array ID is successfully re-referenced by a structurally identical JSON parent object/array.
- F4: Canonicalizing a fresh terminal object/array ID changes the native acceptance, number of paid nodes, or terminal contradiction.

## Source authority and precedence

Original unmodified verifier: `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Native accepted K4 fixture: the `minimal.packetBytes` member of `results/raw/arc/2026-11-10_1112_LSPV2_537_NATIVE_BYTE_CORPUS_RAW.json`, blob `d5e2d22674b0af365e9b82e4f1b2af8307182ba6`.

Both root trackers `proof1.txt` (blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`) and `proof2.txt` (blob `930c5eeddafce656717f28055a7a9a755f44737c` via immutable blob), issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, canonical `main.tex`, current handoffs, LSPV-3/539, /544, /549, /598, /611, /612, LSPV-1/616, LSPV-4/583-584, LSPV-5/524, actual Grok notes and Claude ledger were consulted. The previous LSPV-3/612 established that only the terminal ID property may be absent. **New here:** object/array terminals are genuinely accepted while structurally identical nonterminal JSON references fail, and a precisely scoped terminal-key exact quotient follows. Earlier LSPV-3/611 authenticated parsed primitive-key distinctions; neither /611 nor /612 made this object-terminal theorem.

Primary language authority: ECMAScript 2025, `JSON.parse` and `Map.prototype.get/set`, https://tc39.es/ecma262/2025/multipage/structured-data.html and https://tc39.es/ecma262/2025/multipage/keyed-collections.html. Proof-system boundary: Cook and Reckhow (1979), *Journal of Symbolic Logic* 44:36-50, https://doi.org/10.2307/2273702. These authorities do **not** authenticate historical R_mix341 grammar.

## Theorem 613.1: Terminal complex-key closure, restricted /341

Let `P` be any genuinely accepted original-/341 packet and consider any one fixture with `N=4V` signed SOURCE records, exactly `N-1` distinct paid binary inference records, all SOURCE records required in the terminal ancestor closure, and terminal record `t`. Let `J` be any syntactically valid JSON object or array value. Replace only the `id` property of `t` by `J`, serializing a new packet. **The unchanged checker accepts the new packet with exactly the same signed sources, parent DAG, paid record count and original assertions.** Conversely, in any accepted such packet, a SOURCE or nonterminal paid `id` cannot be object/array valued.

**Proof.** By LSPV-3/612's rooted binary ancestor-edge argument, every SOURCE and every nonterminal paid node is referenced from at least one distinct parent position. `JSON.parse` creates separate JavaScript object identities at distinct positions: even two structurally identical literals do not have referential identity. The checker's `Map` lookup by reference cannot retrieve such an object/array ID from a separately parsed parent object/array. Thus accepted SOURCE and nonterminal IDs must be JSON primitives. Any object/array used as terminal ID is a fresh `Map` key, distinct from all earlier accepted primitive keys. The checker stores the terminal under `p.id` and recursively looks up `last.id` from the *same parsed terminal record*, so the same object identity is used. Terminal `id` is not read as a parent anywhere later. All checks and logical conclusions are unchanged. QED.

**Exact terminal-key quotient.** On the domain of accepted fixture-prefixes with valid parent references and a genuinely fresh terminal key, define `alpha_terminal` to replace any object/array terminal key by a single distinguished fresh abstract terminal atom, and `gamma_terminal` to admit all JSON object/array terminal-key serializations. For each such accepted execution, its alpha-image and every gamma-instance have the same native acceptance and charged work; hence this single-terminal-key abstraction has exact cost (and is a safe subcomponent for P2-C3). No claim of precise abstraction of *invalid* packets, older object-key references, branch joins, or the missing mixed dispatcher is made. Absent, `null`, and primitive-collision cases remain separately typed and subject to prior freshness constraints. For the original K4 fixture, `W=15` and source ancestry is unchanged.

## Direct original-code experiment

Executed the **unchanged** original 9,359-character checker body in hosted V8 by substituting only its file-input and stdout adapters. Re-parsed JSON for each test. The 18 focused packets yielded **11/11 expected acceptances** and **7/7 expected hostile rejections**, zero unexpected outcomes and **15,411 original-checker positive assertion groups** (each accepted K4 gives 1,401). Accepted cases include empty/nested object terminal IDs, empty/nested array IDs, object IDs that visually resemble prior source names, null, Boolean, number and absent IDs. Hostiles included object/array SOURCE and nonterminal keys with structurally equal references, forged terminal parent, and a primitive-ID collision. All positives have 16 unchanged signed SOURCEs, 15 paid nodes, W=15 and identical source/parent structure.

The accepted nested-object certificate, full raw ledger, and a separately published standalone Node.js operating-system subprocess replayer are listed below. **The standalone subprocess script is published but not executed in this run**; this result is authoritative-body hosted execution, not independent OS-process replay.

## Scope, limitations and next work

This is a newly authenticated subgrammar distinction and a cost-exact quotient for a terminal key, **not** an authentication of the complete historical, externally source-bound `R_mix341` grammar. Its original checker is a specialized, independently written /341 program handling SOURCE/AND3/XOR with a fixed 4V-1 proof length; it does not execute Resolution-to-AND3, DEF-facet-to-LOCAL-CONVERT, branches/discharges, deletion as an inference, interfaces or globally paid mixed owners. Further, other previously accepted E>=16 packets demonstrate checker-acceptance and genuine UNSAT are distinct goals.

**P2-D1, P2-C3, P2-B1 OPEN; P2-B2/B3 separately OPEN. P versus NP remains OPEN.** No full mixed-calculus theorem, SAT algorithm-time lower bound, physical runtime/space bound, or altered original historical weight is claimed. No outside verification of standalone Node, full preflight, or LaTeX compilation in this hosted run. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

## Artifacts

- Report: `research/agents/lspv-3/2026-11-13_0530_LSPV3_613_NATIVE_TERMINAL_OBJECT_KEY_QUOTIENT.md`
- Code: `experiments/arc/lspv3_613_terminal_object_id_native.cjs`
- Raw hosted original-checker ledger: `results/raw/arc/2026-11-13_0530_LSPV3_613_TERMINAL_OBJECT_NATIVE_HOSTED_RAW.json`
- Native accepted object-terminal JSON packet: `results/raw/arc/2026-11-13_0530_LSPV3_613_TERMINAL_OBJECT_ACCEPTED.json`
- Handoff: `research/coordination/2026-11-13_0530_LSPV3_TERMINAL_OBJECT_QUOTIENT613_FIVE_ROLE_HANDOFF.md`

Decisive next dependency: recover or obtain the complete historical single-checker mixed-rule R_mix341 with native RES-to-AND3 and DEF-facet-to-LOCAL-CONVERT transitions and external original-source authentication. Do not extend the restricted terminal quotient to unknown mixed-calculus parent/reconvergence rules without new source or a legal accepted-byte replay.
