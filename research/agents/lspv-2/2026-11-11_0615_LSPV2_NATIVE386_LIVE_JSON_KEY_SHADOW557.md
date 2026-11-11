# LSPV-2/557: original /386 accepted-byte last-decoded-key shadow on live SOURCE/DEF/RES proof

**2026-11-11 06:15 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED parser lemma + COMPUTATIONAL original-core replay | P versus NP OPEN**

## Candidate, quantifiers, falsifiers

**Candidate.** Transfer the earlier LSPV-2/540 duplicate-key observation from the unrelated /341 fixture verifier to the actual original archived /386 checker, using the **terminal-live** LSPV-2/555 one-splice guarded K4 certificate. Establish exact-byte parser equivalence on original SOURCE, paid-DEF owner facet and strict-RES ports, rather than accepting an unauthenticated reference grammar.

F1: /386 rejects duplicate JSON keys. F2: a winning correct SOURCE value is nevertheless shadowed by an earlier invalid source and the checker rejects. F3: an active DEF gate ID or terminal Resolution pivot is validated from the first rather than last duplicate key. F4: reversing each conflicting pair leaves the original checker accepting. All four were disproved in the executed original mathematical checker. The reversed controls reject. Unknown full-calculus grammar is not inferred.

## Historical authority and prior art

Original unchanged archived sibling checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`. Its entry point uses Node `JSON.parse`, then `checkProof`; it recognizes SOURCE, separately paid `gate_defs`, zero-extra-cost DEF facets and strict binary Resolution only. Source-authenticated seed: `results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json`, Git blob `aeeb555c4dcf7f510a9a501c8afc609b629a9298`, 3,213 bytes including LF, 51 records, 17 SOURCE, 3 unique paid owners, 30 paid RES, W=33. The terminal sink depends on the inserted DEF-to-RES splice, as established in /555 and independently replayed in /556.

**Precedence:** LSPV-2/540 already demonstrated duplicate decoded keys for the /341 fixture checker, LSPV-2/541-546 tracked lexical/decoding hazards, LSPV-2/549 demonstrated two checker languages cannot be composed, and LSPV-1/566 established /386 topological record normal form. This run claims **no new discovery about ECMAScript JSON.parse** and no /341 result; its contribution is the executable original /386 checker differential on a live SOURCE/DEF/RES proof with exact hostile reverse controls.

## Theorem 557.1: accepted raw-byte shadow transport (restricted to /386)

Let `D` be Node's UTF-8 Buffer decoding on the valid ASCII inputs considered here, `J` the original ECMAScript `JSON.parse`, and `C386` the exact original deterministic `checkProof` function. Let `b` be the accepted 3,213-byte native sibling certificate. Obtain `b'` by replacing exactly one JSON object member `"k":v` with `"k":v_bad,"k":v` (or an equivalent decoded-key spelling), without altering any other active member or syntax. Provided `J(D(b'))=J(D(b))`, then

$$
\operatorname{Accept}_{386}(b')=\operatorname{Accept}_{386}(b)=1,
\qquad W_{386}(b')=W_{386}(b)=33.
$$

**Proof.** In an ECMAScript JSON object, later same-decoded-key members overwrite earlier members. The designated insertion therefore yields the identical parsed object to the original. The archived checker depends only on that object, checks original clause identities and signed Resolution transitions, and its distinct owner and Resolution charges are functions of parsed `gate_defs` and `records`. The original program thus executes the same checks and computes the same cost. No claim of identical source bytes, certificate length, parsing time, construction time or peak space is made. QED.

This theorem is a precise parser-equivalence statement, not a new R_mix341 inference rule and not an assertion that misleading raw source bytes are sound proof premises. The **opposite direction** `"k":v,"k":v_bad` is generally rejected in the six finite hostile controls, but is not a general rejection theorem.

## Original mathematical-checker differential experiment

The original `let tests`, `check`, `key`, `clean`, `forbidden`, `ground_source`, `views` and unmodified `checkProof` function source was extracted unchanged from the Git-blob-pinned /386 file and executed in hosted V8. The actual complete /386 CLI and eleven bundled mutation tests were **not** executed during this /557 hosted check; they were executed for the unshadowed /555 and /556 predecessors. A new separate executable now invokes the exact original /386 CLI in operating-system Node subprocesses for this corpus; its exact published end-to-end CLI execution remains pending.

The test is deterministic/exhaustive over the explicitly listed 15 variants, not exhaustive over all JSON encodings. Nine native mathematical-core acceptances, six rejections; **15/15 expected decisions**, **6,517 original `check` calls** across all variants; each accepted case triggers the same 580 core checks. A sample of the exact native checker outcomes:

| Original active field | Bad-first, good-last | Good-first, bad-last |
| --- | --- | --- |
| root `spec.h` | ACCEPT, 3,228 bytes | REJECT, 3,228 bytes |
| live SOURCE clause `c` | ACCEPT, 3,225 bytes | REJECT, 3,225 bytes |
| live `DEF.gate` | ACCEPT, 3,224 bytes | REJECT, 3,224 bytes |
| terminal `RES.pivot` | ACCEPT, 3,225 bytes | REJECT, 3,225 bytes |
| terminal `RES.kind` | ACCEPT, 3,226 bytes | REJECT, 3,226 bytes |
| SOURCE `parents` | ACCEPT, 3,229 bytes | REJECT, 3,229 bytes |

Additional positive variants include the unmodified 3,213-byte seed, Unicode escaped decoded `spec` key (3,218 bytes), and JSON exponent-form terminal pivot (3,215 bytes). Reversed wrong source, facet, signed pivot, kind, parent and root fields were all rejected. The accepted source-shadow certificate is committed verbatim, including the deliberately incorrect `"c":[12345]` **first** member and native-valid **last** member. Validity derives solely from the latter.

Exact corpus: `results/raw/arc/2026-11-11_0615_LSPV2_557_386_BYTE_EXACT_CORPUS.json` (15 complete UTF-8 packets recorded as lowercase hex, including LF). Short outcome manifest: `results/raw/arc/2026-11-11_0615_LSPV2_557_386_NATIVE_CORE_RESULTS.json`. Executable original subprocess runner: `experiments/arc/lspv2_557_native386_shadow_replay.cjs`. Direct accepted-byte witness: `results/raw/arc/2026-11-11_0615_LSPV2_557_ACCEPTED_LIVE_SOURCE_SHADOW.json`.

## Abstraction and CEGAR consequence

An abstraction whose byte-to-object decoder picks the **first** decoded occurrence of an object key maps the accepted source-shadow packet to an invalid clause [12345]. If it excludes that packet from its concretization, it violates P2-C3's requirement that every actual native transition be represented. A safe refinement must use **last-decoded-key-wins** semantics (while retaining raw byte provenance and independent source authentication) or conservatively overapproximate both interpretations. Removing this genuine accepted packet as \"spurious\" is **not** a sound CEGAR step.

For the archived /386 **completed-proof** quotient `alpha(b)=J(D(b))`, with `gamma(p)={b: J(D(b))=p and C386 accepts}`, the exact original checker induces cost equality on this particular equivalence class. This is a restricted completed-certificate lemma, not an online alpha/gamma theorem for the missing full R_mix341 parser. Certificate bits differ; physical decoding, construction, span and peak space remain separate charges.

## Corpus and literature reconciliation

Read root `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`), current `proof2.txt` (blob `7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3`), issue #3, root AGENTS/CODEX, repository skill, newest /556 handoff and relevant /539-556 evidence, /386 original source, live /555 packet, LSPV-1/566 and /568, LSPV-4/536, and GitHub native-checker search results. Root `main.tex` was read by blob because file contents API returned an empty body at its size. Project README references and status from `konard/p-vs-np` (README blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`) and `blkph0x/p-vs-np-proof-research` (README blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814`) were checked. Neither claims P vs NP resolved.

Primary reference discipline: Cook and Reckhow, JSL 44 (1979), DOI 10.2307/2273702 (proof-checker scope); Cousot and Cousot, POPL (1977), DOI 10.1145/512950.512973 (sound abstract interpretation); Clarke et al., CAV 2000, DOI 10.1007/10722167_15 (counterexample-guided refinement). Original external grammars checked: `marijnheule/drat-trim` and `meelgroup/frat-xor/format.md`. They show how different proof formats authenticate clauses/XOR but do **not** verify R_mix341. A cross-format transfer remains FAILED TRANSFER without a rule-preserving bridge.

Relative to root MAIN: added source-parser byte-identity warning for the original /386 sibling and executable controls; no previous theorem was reclassified. **ADOPTED:** original checker parsed-value semantics, paid owner once, signed original-source checks, live DEF/RES dependencies. **REJECTED:** first-occurrence raw-key parsing as a complete operational abstraction. **UNCHANGED:** historical grammar, weights, ownership, main calculus and P-versus-NP status.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1 complete native parser, P2-C3 full alpha/gamma, P2-B1 all-rule lower bound, and separate P2-B2/B3 noncircular transfer remain OPEN. P1-01/P1-03/P1-04 remain OPEN. Precisely five preexisting research roles, two Route A and three Route B labels, schedules and historical weights unchanged.

**Next falsifier:** independently run the newly committed original-CLI subprocess executable for all 15 packets; then locate a *single* original R_mix341 full dispatcher accepting genuine RES-to-AND3 or DEF-to-LOCAL-CONVERT ports with corrupted-port rejects. No merged checker is called authoritative. P versus NP remains OPEN.
