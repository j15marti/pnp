# LSPV-1/596: JSON Number rounding accepted by the recovered /341 BigInt-mask parser

**2026-11-12 10:00 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED source-inspection corollary of /595 + COMPUTATIONAL original-body hosted-V8 replay | P versus NP OPEN.**

## Candidate theorem and falsifiers, fixed before testing

**Candidate [P2-D1].** In the *unchanged recovered /341 fixture checker* (and not an authenticated historical full `R_mix341`), a JSON `row.mask` **numeric token** need not denote an exact integer in decimal notation. The JSON parser first maps the token to an IEEE-754 Number; if that Number rounds to an integer with the required BigInt mask, the checker can accept. By contrast a **string** containing a nonintegral decimal is not rounded in the same way by `BigInt`. The observation refines the accepted-byte domain of LSPV-1/595, and is **not a new all-rule theorem**.

Four precommitted falsifiers: **F1**, rejection of numeric `7.0000000000000001` while identical parsed-integer mask `7.0` accepts; **F2**, acceptance of its quoted nonintegral decimal string despite `BigInt` requiring an integer string; **F3**, rejection of a zero-mask numerical token `1e-400` whose JSON Number underflows to zero; **F4**, changed original signed source, paid work, ancestry or mathematical SAT label rather than a parsing-only variant.

## Exact accepted-byte result

Pin the original verifier `experiments/arc/lspv2_341_independent_verify.js` (Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`) and original seven-fixture packet `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json` (Git blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`). Extract the K4 fixture unchanged except for **one literal JSON token** in its `row.mask` field, and supply the correct one-fixture summary. It retains 16 original signed ternary clauses on six edge variables, 12 AND3 plus three XOR paid records, and the same terminal contradiction; exhaustive direct assignment enumeration independently confirms **zero** SAT assignments among 64.

**Theorem 596.1 (exact parser-interface subfiber, conditional on original program).** Let `P` be the pinned checker-accepted K4 packet with original mask `"0x7"`. Replace only that mask's JSON lexical token by any standards-compliant JSON *numeric* token `t` for which `Number(JSON.parse(t))` is an integral finite IEEE-754 Number `z` and `BigInt(z)=7n`. Then the unmodified checker accepts the entire packet with the same paid work and same assertion count. In particular, decimal tokens `7.0000000000000001` and `6.9999999999999999` satisfy the condition because JSON Number parsing rounds each to 7. A quoted string `"7.0000000000000001"` instead makes `BigInt` throw; it is not in this equivalence fiber. Similarly, replacing terminal `"0x0"` by numeric tokens `1e-400` or `-1e-400` preserves acceptance because these parse respectively to +0 and -0, both mapped by `BigInt` to zero.

**Proof and precedence.** The original code parses the packet with `JSON.parse` before checking every `row.mask` via `BigInt(...)`. LSPV-1/595 previously proved from the source that all semantic observations of annotated masks factor through that converted BigInt value. Exact equal-BigInt substitution therefore preserves every original checker predicate and the fixed paid DAG. The present result identifies a **lexical-number fiber within that existing theorem**, including nonintegral decimal spellings and underflow. This is an independently verified accepted-byte witness and an implementation-boundary detail, not an independently new mathematical lower-bound result. Under the stricter hypothetical grammar requiring decimal mask lexemes to themselves represent integers, these accepted bytes would be excluded, but adopting that grammar changes the historical acceptance language and requires an explicit proof of cost-preserving normalization.

## Direct unchanged-original-body replay

The original verifier's mathematical source was evaluated in hosted V8 using only filesystem, process-argument and console adapters. It was **not reimplemented**. Thirteen differential JSON packets were executed; **8 accepted, 5 rejected**, matching all fixed expectations. Every acceptance performed **1,401 original checker assertion groups**, 11,208 in aggregate.

| Replacement mask JSON token | Parsed mask type/value | Original checker |
|---|---|---|
| `"0x7"` (baseline) | string / 0x7 | ACCEPT |
| `7.0`; `7e0` | Number / 7 | ACCEPT |
| `7.0000000000000001` | Number / 7 | ACCEPT |
| `6.9999999999999999` | Number / 7 | ACCEPT |
| `7.000000000000001`; `7.5` | noninteger Number | REJECT |
| `"7.0000000000000001"` | nonintegral string | REJECT |
| `"7"` | integer string | ACCEPT |
| `1e-400`; `-1e-400` (terminal zero mask) | Number / +0 or -0 | ACCEPT |
| `1e-8` (terminal mask) | noninteger Number | REJECT |
| `"1e-400"` (terminal mask) | nonintegral string | REJECT |

The same original signed 16-clause source, all paid node IDs and parent dependencies, all fixed weights and the terminal GF(2) contradiction were retained. Original source is UNSAT independent of checker acceptance. The experiment does **not** test or authenticate RES, RES->AND3, LOCAL-CONVERT, paid DEF, defining facets, exported/private wires, branching, contexts, assumption discharge, joins, weakening or deletions.

**Reproducer:** `experiments/arc/lspv1_596_native341_numeric_token_rounding.cjs`; the complete independent OS Node executable pins the checker and fixture Git blob SHAs, calls the unchanged original checker under the Node VM, and checks the 13 outcomes and all six-variable source assignments. Its OS execution is **pending**. **Actually executed raw ledger:** `results/raw/arc/2026-11-12_1000_LSPV1_596_NUMERIC_MASK_ROUNDING_HOSTED_RAW.json`. The raw evidence records individual lexical tokens, parsed values, acceptance, exact original assertion count, errors and byte lengths; input lengths ranged about 3,400 to 3,417 bytes. The code/data were committed and individually read back via GitHub.

## Proof dependency, abstraction and resource ledger

The exact intended global objective, **not computable from these fixtures**, remains

$$
W_R(F)=\min_{\pi\in\operatorname{Ref}_R(F)}
\sum_{v\in\operatorname{PaidIDs}(\pi)} w_R(\operatorname{rule}(v)),
$$

where `Ref_R(F)` includes **every** source-authenticated whole shared proof DAG in one *fully fixed* native calculus, with free optimal proof selection. Count each globally distinct paid node once, preserve paid-owner state, contexts and branch AND-obligations, and discharge assumptions before sharing globally. The observed K4 fixture has W=15 in its restricted checker; this is an **upper witness**, not an optimum for the full calculus. Evidence bits, discovery/selection, verification time, actual machine running time, peak space and span are separate and unmeasured here.

**[P2-D1] OPEN:** an actual original mixed-rule dispatcher covering all historical legal rules and accepted bytes is still missing. Numeric mask lexical alias acceptance is a restricted authenticated checker fact; canonicalizing these bytes may be cost-neutral for restricted logical work but not for evidence-byte/time accounting. **[P2-C3] OPEN:** the full alpha/gamma and every legal native abstract transformer are unauthenticated. A MAY overapproximation must include genuine checker-accepted paths and all unknown legal transitions; it may not silently replace the original calculus with CANON1/2/2R. The earlier checker-accepted SAT-source counterfeit demonstrates why complete checker acceptance and independent mathematical UNSAT validity must be kept separate. **[P2-B1] OPEN:** no superpolynomial optimal work lower bound for the whole calculus. **[P2-B2/B3] separately OPEN:** no noncircular same-calculus transfer from arbitrary SAT algorithms. All P1-01/03/04 OPEN; P versus NP OPEN.

## Literature and corpus reconciliation

Reviewed both root proof trackers, issue #3, root AGENTS.md/CODEX.md, the pnp-research skill, latest five-role handoffs, actual LSPV-1/595, LSPV-5/506, LSPV-3/550 and /568, relevant LSPV-1/539-549, LSPV-1/559, LSPV-2/549 and /578, LSPV-3/592, LSPV-4/565 and LSPV-5/506 issue reports and original checkers. Searched the repository for genuine RES->AND3, DEF->LOCAL-CONVERT and full-dispatch authority; none was recovered. Some peer report filenames were unavailable by guessed paths and were not treated as read. **Precedence:** /595 already proves equal-BigInt substitution; /550 reports JavaScript source-literal coercion; /568 reports malformed numeric charge acceptance. This record is a new *direct decimal-token fixture validation* under /595, not a new full-calculus rule or P2 material closure.

Primary references: ECMA-262 `BigInt` conversion, `JSON.parse`, Number numeric representation (https://tc39.es/ecma262/); P. Cousot and R. Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973; E. Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV (2000), DOI 10.1007/10722167_15; S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702. These sources describe the parser/model/methodological constraints; none authenticates a missing R_mix341 native operation.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither root proof1.txt nor proof2.txt is rewritten for a corollary of existing P2-D1 evidence. No automation, title, ownership region, schedule, rule, historical weight, timezone or two Route A / three Route B allocation was changed. **Independent LSPV-5 falsification requested:** actual OS Node replay of the 13-case archive plus hostile invalid-mask and SAT-source controls.

**Next load-bearing target:** recover an authoritative *single* mixed-rule checker and one accepted externally source-bound RES-to-AND3 or paid DEF-to-LOCAL-CONVERT trace with a corrupt-port rejection. Until then the full native calculus remains open.
