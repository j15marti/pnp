# LSPV-1/595: BigInt coercion quotient of the recovered /341 checker

**November 12, 2026, 09:00 PST | LSPV-1 General SAT Lower-Bound Lead | Historical Route B | PROVED/RESTRICTED + COMPUTATIONAL hosted original-checker replay | P versus NP OPEN.**

## Candidate, exact scope and advance falsifiers

**Candidate theorem:** In the pinned, unchanged archived /341 SOURCE/AND3/XOR checker, holding the parsed signed-source packet, its proof DAG, paid record identities and every other field fixed, a `row.mask` field may be replaced by *any* JSON value whose JavaScript `BigInt` conversion exists and equals the original mask's converted integer. The verifier's acceptance and entire logical-work ledger are invariant. For the original signed odd-K4 fixture, replacing exactly one of its seven annotated masks, while holding the other six and every nonmask field fixed, is accepted **if and only if** that BigInt equality holds.

The exact authority is the original checker `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, and the original seven-fixture packet `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`. Its local SOURCE/AND3/XOR program is **not** an authenticated full historical `R_mix341` dispatcher. All fixed native logical inference weights and rule scopes are unchanged.

Four falsifiers registered before the original-checker differential:
- **F1:** Any well-converted same-BigInt JSON alias is rejected with the other packet fields unchanged.
- **F2:** A single changed K4 mask whose converted BigInt differs nonetheless passes the complete unchanged checker.
- **F3:** Simultaneously substituting all 157 annotated masks in all seven fixtures with equal-BigInt nested JSON arrays alters a signed SOURCE, paid identity, charge, or acceptance.
- **F4:** Source forgery or a false AND3, parent, XOR sink, typed RHS or noncoercible mask is admitted.

None occurred in the executed restricted controls. A **different**, deliberate countercontrol succeeds: two simultaneous changed AND3 masks with matching high ghost-bit toggles pass even though their individual BigInt values differ. Therefore the iff is deliberately limited to a **single** changed mask, not simultaneous arbitrary substitutions.

## Theorem 595.1: exact equal-BigInt substitution preservation

Let `V341` be the exact JavaScript verification function in the pinned checker. Fix any parsed packet `P` for which `V341(P)` accepts, and let `r` be any annotated `row.mask` occurrence. Let `v` be a JSON value satisfying `BigInt(v) = BigInt(P[r].row.mask)`, where both conversions terminate normally. Form `P[r := v]` without changing any other field. Then

```
V341(P[r := v]) = ACCEPT
W341(P[r := v]) = W341(P)
```

The same conclusion holds under **any finite collection of independent, simultaneously equal-BigInt** substitutions. In particular, this preserves each SOURCE occurrence, original formula, derived DAG edge, charged node, inference identity and complete terminal sink.

**Proof.** Inspect the pinned verifier source. The only semantic observations of an annotated mask are `BigInt(p.row.mask)` in the optional AND3 affine-alias test, `BigInt(a.row.mask)`, `BigInt(b.row.mask)` and `BigInt(p.row.mask)` in XOR equality, and `BigInt(last.row.mask)` in the terminal sink condition. All these occurrences factor through the same partial conversion `B(v)=BigInt(v)`. Every other verifier predicate reads the unchanged graph, charges, original signed clauses, parent IDs, truth tables, row RHS values, deletion witnesses and proof length. Substitution preserving B leaves every assertion, its control-flow order and its Boolean result unchanged. The original logical payment counts derived proof records, not mask serialization bytes. The same reasoning applies componentwise to any finite simultaneous family of substitutions. QED.

For every positive integer k, replacing a zero mask by a string of k decimal zeros is an accepted finite encoding whenever the execution can parse that finite JSON payload. Thus the accepted-byte syntax has infinitely many distinct serialized witnesses for one fixed proof at constant logical W. This is **not** a zero physical parsing-time claim: input length, evidence bits and machine resource usage change.

## Theorem 595.2: exact seven-position single-field iff on odd K4

Fix the original first K4 fixture and its original other six row masks. Its seven annotated nodes are:

| Record | Native rule | Original mask |
| --- | --- | --- |
| d2 | AND3 | 0x7 |
| d5 | AND3 | 0x19 |
| d8 | AND3 | 0x2a |
| d11 | AND3 | 0x34 |
| d12 | XOR | 0x1e |
| d13 | XOR | 0x34 |
| d14 | final XOR | 0x0 |

The fixed XOR edges are `d12=(d2 XOR d5)`, `d13=(d12 XOR d8)` and `d14=(d13 XOR d11)`, each with exactly checked entire-mask BigInt equality and fixed RHS. Each AND3 mask participates as an immediate input of one of those XORs, and each earlier XOR mask participates in a later checked XOR. The terminal XOR mask is required to be zero.

Suppose exactly one row.mask is replaced by a JSON value v, with no other change. If B(v) is undefined, the checker throws; if B(v) differs, either the next fixed XOR equality or the fixed final zero-mask equality fails. Equal B(v) is accepted by Theorem 595.1. Therefore:

```
V341(K4 with exactly one mask changed to v) = ACCEPT
iff BigInt(v) is defined and equals that row's original BigInt mask.
```

This iff concerns one specific pinned fixture and one changed mask, not all formulas, all mixed proofs or all joint perturbations. QED.

## Executed original-code differential and hostile controls

Both exact source files were fetched by repository content SHA. The checker function was executed without replacing its mathematical body in the **hosted V8 runtime**, supplying only `fs.readFileSync`, `process.argv` and `console.log` adapters. The original full seven-fixture packet passed **30,714 original assertions**; the isolated first K4 fixture passed **1,401 assertions**.

For each of seven K4 masks, test 45 concrete JSON values, including `null`, Boolean values, integers, `[]`, singleton and nested arrays, numeric strings, whitespace strings, binary/octal/hexadecimal strings, `[null]`, objects and malformed numeric strings. Across **315 one-field tests**, **40 accepted** and **275 rejected**; all **315/315** matched independently calculated BigInt-coercion equality. Example accepted substitutions include `[[7]]` for 0x7 and `false`, `[]`, `[[0]]`, empty string and whitespace string for final 0x0. `null` is rejected because JavaScript `BigInt(null)` throws.

All **157 annotated masks in all seven original fixtures** were then changed simultaneously to nested arrays `[[decimal_string]]`; the complete original checker still passed **30,714 assertions**, with the same signed sources, 4h-1 derived nodes per fixture and fixed paid counts. A 128-leading-zero decimal-string terminal mask also passed. Two simultaneous high ghost-bit toggles passed, emphasizing that same-BigInt preservation is sufficient, not generally necessary for joint modifications. Six independent hostile mutations were rejected: corrupted signed SOURCE, false AND3 conjunction table, nonexistent parent, false sink RHS, invalid typed row RHS, and noncoercible terminal mask.

**Reproducible published code:** `experiments/arc/lspv1_595_native341_bigint_parser_quotient.cjs`. It verifies the exact pinned Git blobs and replays the unmodified original checker in Node's V8 `vm` with I/O adapters, producing a detailed raw result when given an output path.

**Immutable original-body hosted evidence:** `results/raw/arc/2026-11-12_0900_LSPV1_595_BIGINT_QUOTIENT_HOSTED_RAW.json`. The published independent OS Node replayer is **not yet independently executed as an operating-system subprocess**. The reported pass counts belong to the actual hosted-V8 replays, not an unverified Node OS run.

## Corpus, novelty and dependencies

Read both root `proof1.txt` and `proof2.txt`, issue #3 with current role reports, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, actual pinned checkers and source packet; reconciled LSPV-1/539, /543, /544, /549, /594, LSPV-2/550, /576, /577, LSPV-3/573, /578, /587, /591, relevant LSPV-4 resource results and LSPV-5/505; reviewed associated recent five-role handoffs. Search of the source repo and archived checker commit history found no authenticated single original RES-to-AND3 or DEF-to-LOCAL-CONVERT dispatcher.

**Previously known:** LSPV-3/591 already showed 128 accepted single-level array substitutions across the K4 masks. LSPV-5/414 already found high-ghost-bit acceptance for coordinated changes. This run does not rebrand either as novel. **New here:** the exact source-code factorization theorem for arbitrary equal-BigInt JSON aliases, its stated single-field iff for all seven original K4 row positions, 315 differential controls and the simultaneous all-157-row nested-value test. Accept the prior parser warning, reject any claim that abstract raw-mask syntax can be freely identified when measuring **bytes, parser time, or independent source authenticity**.

**Methodological references:**
1. S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702. An accepted-byte verifier for one restricted grammar is not the historical full calculus.
2. P. Cousot and R. Cousot, *Abstract Interpretation*, POPL 1977, DOI 10.1145/512950.512973. A quotient requires a simulation of all legally observed transitions and costs.
3. E. Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000, DOI 10.1007/10722167_15. Parser-refined CEGAR must replay concrete, source-bound evidence rather than discard genuine acceptances.
4. Original project historical checker and first-party LSPV-3/591 report, as pinned above.

**Abstract-interpretation consequence:** When modeling *logical-work-only* acceptance for the restricted /341 source, the mask value may be abstracted by its exact BigInt coercion while preserving row RHS, signed support, all source/proof identities and paid history. This quotient is **not** a sound abstraction for raw evidence bits, byte-aware runtime, or all historical operations without a separate proof. A `BigInt` coercion failure is an actual rejected branch, and synchronized ghost-bit changes show equality of abstract mask values is not necessary for common end acceptance.

**P2-D1 OPEN:** This is a newly formalized accepted-byte subgrammar fiber of the recovered /341 restricted fixture verifier. SOURCE, Resolution, AND3, GF(2), LOCAL-CONVERT, paid DEF, fresh/private/exported wires, branch/discharge, weakening, joins, deletions and fixed rule charges in a *single complete historical checker* are **not** authenticated by this result.

**P2-C3 OPEN:** No all-rule concrete transition system, cost-sound alpha/gamma or admissible CEGAR minimum-work potential is furnished. For a proper whole shared proof DAG, distinct paid occurrence IDs are charged once and all AND/context obligations must be discharged. Incomplete historical rules remain MAY rather than silently omitted.

**P2-B1 OPEN:** Source families, tree-only Resolution potentials and fixture-size equalities do not give a superpolynomial optimum over unrestricted shared-DAG mixed proofs. An arbitrary legitimate GF(2), extension, learning, preprocessing, branch or algebraic shortcut remains in scope. **P2-B2/B3 remain separately OPEN:** no transfer from SAT in P or an unrelated checker into polynomial Wbar is established. P versus NP OPEN.

**Resource ledger:** first K4 proof has 16 genuine SOURCE clauses and 15 paid AND3/XOR records; original fixed-W does not count raw alternate JSON bytes, discovery, V8 verifier time, proof span, or peak working space. The all-fixture 157-row encoding rewrites evidence syntax only, not a claimed optimal proof.

**Barrier audit:** This is a local parser-equivalence theorem. No circuit lower bound, relativization-resistant theorem, algebraization transfer, Natural Proof, unrestricted RAM-time statement or universal SAT decision result follows.

**Trackers reviewed; no material change.** Full historical calculus, full CEGAR abstraction, all-rule lower bound and same-calculus transfer remain OPEN. Root `main.tex` must be reconciled solely inside LSPV-1's marked region if complete current blob and SHA are available. All other ownership regions, prior peer reports and five role assignments stay unchanged.

**Next decisive target:** have LSPV-5 independently replay /595 in original operating-system Node and challenge the single-field iff with exotic JSON values. In parallel, require LSPV-3 to obtain one authoritative, externally source-bound historical single-dispatcher accepted RES-to-AND3 or DEF-to-LOCAL-CONVERT record, with hostile rule-port controls; that is the load-bearing P2-D1 requirement.
