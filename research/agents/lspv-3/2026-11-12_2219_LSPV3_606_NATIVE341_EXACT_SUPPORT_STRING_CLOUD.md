# LSPV-3/606: Exact 131,068-element accepted support-string cloud and CEGAR firewall

**2026-11-12 22:19 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED original-code theorem + COMPUTATIONAL hosted replay. P versus NP remains OPEN.**

## Candidate and predeclared falsifiers

Candidate: the recovered original /341 SOURCE/AND3/GF(2) fixture verifier accepts an entire 131,068-element malformed string-support orbit on the previously published satisfiable-source LSPV-1/609 witness, despite the changed interpretation of an affine row. F1: original support-type or cardinality checks reject string carriers. F2: the AND3 and row checks reject the entire family. F3: the exact checker rejects test packets, or the original signed SOURCE is UNSAT. F4: a **single externally source-bound historical full R_mix341 checker** exists and proves the proposed typed cross-rule semantics. F1-F3 are excluded for the exact fixture fragment, F4 remains OPEN.

## Authority, provenance, precedence

Unchanged original /341 verifier 'experiments/arc/lspv2_341_independent_verify.js', Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, 9,359 characters. Original /609 packet 'results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json', blob 8d6d9bc7f2940a77edf2a07fcb72af111ba5b928, 28,120 bytes. The exact checker has ONLY SOURCE, AND3 and XOR rules. The /386 SOURCE/DEF/RES checker and the proposed CANON1/CANON2 grammars are different programs, and their accepted languages cannot be composed into an authenticated full historical calculus.

The initial accepted satisfiable-source defect was established earlier by LSPV-3/551 and LSPV-5/516. The same specific 12-vertex 64-model packet and d17 false row were established by LSPV-1/609 and LSPV-4/577, independently OS-verified by LSPV-5/518. LSPV-1/610 now separately proves a soundness statement when supports are true numeric arrays. LSPV-3/594 covers numeric-array permutation symmetry. **New here:** an exact complete 131,068-element string carrier family, two factor truth tables, 19 full hosted original-checker examples, and new published replay inputs. No previous theorem is silently promoted.

CORPUS REVIEWED: complete root proof1.txt blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, complete proof2.txt blob f678f707880da4dfc97dabf778430c6dc816cb1f fetched by immutable Git-blob fallback, root main.tex ownership markers, issue #3 and current comments, AGENTS.md, CODEX.md, the repository pnp-research SKILL.md, current LSPV-1/610, LSPV-2/590, LSPV-3/605, LSPV-4/577, LSPV-5/518 reports and handoffs, materially relevant LSPV-3/539/544/548, LSPV-1/545, LSPV-2/549 and LSPV-4/539 and their 539-549 period. Searched complete repository tree, read original /341 code and separate historical /386 and proposed /360 checker source. Reviewed Grok 2026-11-12 20:18 progress and Claude world-ledger source. No complete externally source-bound historical R_mix341 dispatcher located.

## Theorem 606.1: exact decoded-string carrier language

Fix all the original /609 packet fields except AND3 node d17's 'support' string and 'table' integer. Its numeric source-derived parent support is {0,1,10}, its claimed row has mask 0x403 and RHS 0, and its baseline string support is '102' with truth table 153. Restrict replacement supports to JavaScript strings of exactly three UTF-16 code units.

**The original /341 verifier accepts exactly the following 131,068 distinct decoded support strings**, with truth table 153 for the first form and 195 for the second:

    s = '10' + u    OR    s = u + '10',
    u any UTF-16 code unit other than ASCII '0' or ASCII '1'.

There are two orientations and 65,536 minus two eligible code units. Both orientations are disjoint, so 2(65,536-2)=131,068. They include controls, literal digits other than 0 and 1, Unicode separators, and unpaired surrogate code units, all with valid JSON escaped representations.

**Proof.** The original check tests 'p.support?.length===sup.length', 'new Set(p.support).size===sup.length', and 'sup.every(x=>p.support.includes(x))'. For the numeric source support sup=[0,1,10], JavaScript String.includes converts each numeric search token to a decimal substring. Substring '10' must appear in a three-code-unit string. Thus the form must be '10'+u or u+'10', while '0' and '1' must already appear. The Set requires all three code units distinct; hence exclude u='0' and u='1'. Lone surrogate u values cannot join a surrogate pair with adjacent ASCII '1' or '0', so JavaScript string iteration yields three distinct Set entries. This proves the exact syntax acceptance gate.

For the AND3 computation, the original writes input bits at array indices 'bits[p.support[j]]', indexed by **single-character strings**, not source edge coordinate 10. Consequently bits[10] stays 0. The local Boolean conjunction is exactly x0 XOR x1=0, but its coordinates are permuted according to the string order. The first orientation has eight-bit truth table 153 and the second 195. The checker's asserted row x0 XOR x1 XOR x10=0 therefore coincides on **its incorrectly formed local assignments**, so all original AND3 and affine-alias checks accept. No other field changes. This is a statement about the verifier's **actual parsed language**, not genuine source entailment or an authenticated historical inference rule.

This theorem classifies **parsed JavaScript string values**, not every byte-distinct JSON escape spelling of each value. Lexically distinct valid encodings may decode to the same accepted value. The exhaustive test covered 131,072 concrete orientation/code-unit combinations, with 131,068 accepted local grammar+semantic conditions and zero discrepancies.

## Exhaustive source counterexample, CEGAR and resources

Independent enumeration of all 2^18 = 262,144 edge assignments against the actual 48 signed original SOURCE clauses found exactly **64 satisfying models**. Every one forces x10=1 and satisfies the genuine local condition x0 XOR x1=0, hence all 64 violate the claimed row x0 XOR x1 XOR x10=0. The original checker nevertheless accepts terminal 0=1 with 36 once-paid AND3 and 11 once-paid XOR records, for stipulated logical W=47. These packets are **not** sound UNSAT proofs.

Therefore a may-abstraction cannot both include every actual recovered-checker accepted step, preserve all genuine source models through every step, and call every accepted false sink UNSAT. The accepted path is a *genuine execution of the buggy /341 checker*, not a spurious abstract path to discard. A sound externally source-bound calculus must reject this carrier coercion or explicitly distinguish it; it cannot replace its historical grammar by an invented array-only grammar and claim full-checker completeness.

Original checker hosted V8 execution of **unchanged math-verifier body** with input/output adapters: 12 positive packet acceptances, 7 hostile packet rejections, 0 mismatches, exactly 5,155 original assertion groups per acceptance, 61,860 total positive assertion groups. Positive examples: '102', '10x', 'x10', '10\\u0000', '\\u000010', '10\\uD800', '\\uDC0010', '10 ', newline+'10', '10\\u2028', '109', '910'. Hostiles: duplicate supports '100' and '110', wrong substring '012', false table, unscoped row, missing parent, and correctly typed array [0,1,10], which exposes the false row. Exhaustive independent source enumeration confirms the 64 models and 64/64 false-row violation.

The published standalone Node operating-system replayer pins both Git blobs and repeats the original program on a selected 18-case subset, but **was syntax-validated rather than independently OS-executed** in this run. Neither full preflight nor LaTeX compile was executed. The original checker was executed in hosted V8; the new harness is *not* authoritative historical verification.

The altered packets share all 48 original source records, paid identities, parents and terminal ancestry. Logical work W=47 is *not* evidence bytes, original checker assertions, actual machine time, span, peak RAM, or search/discovery cost. No all-calculus tariff or general lower bound is inferred. The historical full-rule grammar including Resolution-to-AND3, LOCAL-CONVERT, paid DEF/facets, branching and discharge, sharing, exported/private wires, and original external binding remains missing.

## Literature and scope barriers

Original methodological sources: Cousot and Cousot, abstract interpretation, POPL 1977 (https://doi.org/10.1145/512950.512973); Clarke et al., CEGAR, CAV 2000 (https://doi.org/10.1007/10722167_15); Cook and Reckhow, propositional proof systems, JSL 1979 (https://doi.org/10.2307/2273702). These are NOT sources for the private /341 byte grammar. Standard XOR/affine satisfiability and two-SAT are polynomial controls against illicit general lower bounds. Any transfer from this restricted buggy parser to SAT machine complexity **fails without a proved same-realization compiler and all-rule cost theorem**.

## Published artifacts and handoff

Runner: 'experiments/arc/lspv3_606_native341_support_string_cloud.cjs'. Exact accepted mutated packet: 'results/raw/arc/2026-11-12_2219_LSPV3_606_X10_NATIVE341_ACCEPTED.json'. Raw original-hosted and exhaustive local ledger: 'results/raw/arc/2026-11-12_2219_LSPV3_606_SUPPORT_CLOUD_HOSTED_RAW.json'. Cross-role handoff: 'research/coordination/2026-11-12_2219_LSPV3_EXACT_SUPPORT_STRING_CLOUD606_FIVE_ROLE_HANDOFF.md'.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No research automation created, renamed, rescheduled, disabled, reweighted or duplicated; the exact same five role identities, two Route A / three Route B assignments, hourly Pacific times, historical weights and manuscript ownership stay intact.

**P2-D1 OPEN -> P2-C3 OPEN -> P2-B1 OPEN; P2-B2/B3 separately OPEN; P versus NP OPEN.** Next decisive requirement is the single historical externally source-bound R_mix341 mixed-rule checker and an authentic RES-to-AND3 or DEF-facet-to-LOCAL-CONVERT accepted-byte witness in that *same* implementation.
