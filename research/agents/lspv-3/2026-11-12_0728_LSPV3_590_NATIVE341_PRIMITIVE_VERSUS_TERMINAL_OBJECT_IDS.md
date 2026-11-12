# LSPV-3/590: Parsed JSON identifier kinds are position-sensitive in the archived /341 checker

**November 12, 2026, 07:28 PST | LSPV-3 Hypergraph & Proof Certificates | Historical Route B | PROVED/RESTRICTED source-code theorem + COMPUTATIONAL original-checker hosted V8. P versus NP OPEN.**

**Affected IDs:** P2-D1 restricted accepted-byte authentication; P2-C3 concrete/abstract parser identity; P2-B1 and P2-B2/B3 OPEN. No historical rule or weight modification.

## Candidate and four advance falsifiers

Candidate: the unchanged archived /341 checker accepts parsed JSON primitive values of any kind as SOURCE and intermediate paid inference IDs when all independent parent/deletion references have the same primitive value. An object or array ID at a referenced node fails because the separately encoded references become distinct objects after JSON.parse. However an object or array ID at the *unreferenced terminal record* is accepted because the checker accesses that exact in-memory object in `ancestor(last.id)`.

F1: any primitive SOURCE/paid ID replacement fails. F2: independently referenced array/object succeeds after genuine JSON serialization and reparse. F3: unreferenced terminal object/array fails. F4: duplicate source IDs, wrong deletion types, and type-changed parent references pass. All four falsifiers were tested and did not occur as counterexamples to the candidate.

## Authenticated historical boundary

Unmodified checker: `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Original seven-fixture packet: `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, Git blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`. The input to each experiment was serialized and parsed anew before the checker body executed; this matters because pre-serialization in-memory aliases would be nonrepresentable in ordinary JSON. Only the original fs/argv input and console output were replaced by hosted V8 adapters; checking semantics and built-in five hostile controls were unchanged. This is original-code replay, not an independently rewritten verifier, and **not** an operating-system Node subprocess. The published self-contained Node reproducer invokes the unchanged original checker using actual subprocesses but has not been independently OS-executed during this run.

Direct code analysis: `src.has(c.id)`, `byId.get(parentId)`, `d.sourceId===c.id`, and `used.has(id)` use parsed value equality/identity. The terminal `last.id` is passed through the same object reference to the ancestor walk, whereas any reference encoded in a different JSON location is independently allocated. The type of an ID is not validated at ingress.

## Theorem 590.1, restricted executable/type theorem

Fix an original accepted packet P of the unchanged /341 checker, a SOURCE or paid proof node u having at least one independent later reference, and a fresh replacement token t used identically at u and all its reference fields. Among JSON type *classes*, null, Boolean, number and string tokens permit acceptance where no collision occurs and all downstream native checks remain unchanged. Replacing t by an array or object cannot preserve that reference equality after a genuine JSON parse, as independently parsed compound values have distinct object identity. This is an identifier-type statement, not a claim that every numerical value or arbitrary token substitution avoids collisions.

In contrast, if u is an unreferenced terminal inference, an array or object ID is allowed by the current checker: its local map insertion is fresh and the ancestor walk reuses `last.id` as the very same object. Thus identifier admissibility depends on the *reference topology* as well as type. There is no valid normalization of all ID tokens by their printed string without changing this accepted predicate.

**Proof:** JSON.parse creates an independent compound value for each separate textual occurrence. JavaScript Map keys compare object references by identity, whereas primitive keys compare by value (subject to the language's numeric equality). The original checker performs no ID-type test, but calls `byId.get` for independently encoded parents and strict `===` for deletion source IDs. Hence referenced compound IDs miss their antecedents; matching primitive values can succeed. A terminal ID is not encoded as a later parent, and `ancestor(last.id)` uses the existing terminal object. All remaining validations are unchanged in the exact demonstrated substitutions. QED.

## Original checker differential results

The experiment exercised **28 serialized/reparsed K4 cases**, **20 ACCEPT and 8 REJECT**, including the baseline and combined source-null / terminal-object packet. All positives retained 16 original signed SOURCE clauses and 15 paid AND3/XOR inferences; all positive replays passed 1,401 unchanged original-checker assertions, total 28020. Tested referenced primitive IDs: null, false, true, numeric zero, numeric -7 and the empty string. Referenced [] and {} were rejected as missing antecedents. Terminal null, true, numeric zero, [], {}, and nested object IDs were accepted. Hostiles tested duplicate source identity, a deletion-source type mismatch, a parent type mismatch, and an independently replaced terminal parent.

The exact, separately parsable combined witness is `results/raw/arc/2026-11-12_0728_LSPV3_590_NULL_SOURCE_OBJECT_TERMINAL_NATIVE341.json`; raw original-checker outcomes are `results/raw/arc/2026-11-12_0728_LSPV3_590_NATIVE341_JSON_ID_HOSTED_V8_RAW.json`. An in-memory object graph with a shared array reference can pass where the same graph serializes to *rejected JSON*: such a test cannot be reported as an accepted-byte certificate. This explicit roundtrip guard is the substantive repair to the experimental method.

## CEGAR and typed hypergraph consequence

A MAY abstraction that collapses numeric 0, string "0", null, false and empty string into a common printed or falsy ID can merge distinct native ancestors and fabricate a cheap path. Conversely a blanket ban on compound IDs excludes genuine accepted terminal records. The required parser-state refinement is `(JSON type, primitive value or compound allocation identity, reference topology, SOURCE provenance, paid node identity)`, with native replay before exclusion. The tested malformed object parent is spurious; the terminal object is a genuine legal archived-checker encoding. Neither adds a paid logical step; certificate byte count, checker time, span and peak space are distinct.

This is **not** a source-independent soundness proof: the /341 packet still supplies its own original source. LSPV-3/589's separately trusted source-bound gate is distinct. Earlier ID alias audits LSPV-5/415/416/477/479 and LSPV-3/549 cover numerical or canonical identifier issues; the present distinction isolates primitive versus compound JSON values at referenced and terminal records, with original-checker reparse replay. LSPV-3/559 proves /341's dispatch remains only AND3/XOR. No RES-to-AND3, DEF/LOCAL-CONVERT, exported/private wire or branch/discharge accepted byte was authenticated.

## Corpus, references, status

Read root proof1.txt blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and proof2.txt blob ba4d1c0faf9acbce836ffc5e16740b197e4c7bbe; issue #3; AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; original /341 and /386 code; LSPV-3/539-546, /548-549, /559, /582-589; current LSPV-1/592, LSPV-5/505, LSPV-2/547 and LSPV-4/562; current Grok 2026-11-12_0917 and Claude context. Primary references: Cook & Reckhow (1979), *J. Symbolic Logic* 44, 36-50 (DOI 10.2307/2273702); Clarke et al. (2000), *CAV*, 154-169 (DOI 10.1007/10722167_15); ECMAScript JSON.parse and Map key semantics (ECMA-262; MDN JavaScript JSON.parse). External FRAT-XOR/XLRUP syntax is another proof language, not native authority.

No new lower bound, no arbitrary-SAT transfer and no historical full R_mix341 checker located. P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN. P versus NP OPEN. The next decisive target is an original-source-bound full mixed-rule checker with one accepted cross-rule inference.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt or proof2.txt. Preserve the existing five roles and schedules, fixed weights, boundaries and two Route A / three Route B labels.
