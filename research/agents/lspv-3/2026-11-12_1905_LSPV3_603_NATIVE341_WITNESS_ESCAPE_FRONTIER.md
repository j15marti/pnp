% LSPV-3 REPORT::603::2026-11-12T19:05:00-08:00
# LSPV-3/603: Exact native /341 witness JSON-escape acceptance frontier

**November 12, 2026, 19:05 PST | Hypergraph & Proof Certificates | Historical Route B | PROVED/RESTRICTED original-source parser theorem plus COMPUTATIONAL unchanged-body hosted V8. P versus NP OPEN.**

## Target candidate and four registered falsifiers

**Candidate [P2-L3-603]:** The pinned historical /341 SOURCE/AND3/XOR checker decodes raw JSON, then requires each non-null deletion assignment and the even-charge witness to pass an exact length check and ECMAScript anchored binary-string regex. The raw JSON Unicode escape \u0030 for the final ASCII zero is accepted as the same parsed digit; replacing that digit by JSON-escaped LF, CR, U+2028, U+2029, TAB, SPACE, or x is rejected. A Python reimplementation using re.match with a dollar anchor may spuriously allow the final newline. This authenticates one exact P2-D1 evidence-field grammar, not the complete historical R_mix341 calculus.

F1: the unchanged checker accepts any replaced terminal line separator. F2: it rejects a JSON escape that decodes to unchanged ASCII zero. F3: the accepted escaped witness changes signed SOURCE clauses, parent DAG, paid identities or final sink. F4: corrupted SOURCE literal, parent pointer or terminal affine RHS nonetheless passes. F1-F4 are excluded in the reported controls; the parser result follows from source code.

## Pinned source and precedence

The original checker is https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_341_independent_verify.js , Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**. The original K4 specimen is https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json , Git blob **393d13265192b4e43073c6f6559bc22b6a71ece5**; it contains 16 signed SOURCE occurrences, 15 paid inference records, six edge variables and a final 0=1 affine contradiction, accepted with 1,401 checker assertion groups.

The executable source checks the *decoded parsed values*, in the mathematical checker:

    assert(d.assignment.length===E&&/^[01]+$/.test(d.assignment),"bad deletion witness bits");
    assert(f.evenWitness.length===E&&/^[01]+$/.test(f.evenWitness),"even witness");

The JSON parser maps raw \u0030 escape spelling to the ASCII digit zero, whereas raw \n escape spelling produces a line feed. Both fields require exact checked witness bits, so parity and deletion constraints remain independently enforced. In Python, re.match(r'^[01]+$', '00000\n') succeeds because its dollar anchor matches just before the final newline, whereas original JavaScript /^[01]+$/.test on that decoded string is false. Python re.fullmatch is closer for this particular decoded-string check, but a Python rewritten checker has no historical source authority.

Prior LSPV-3/591, /594, /596, /599 and /600 authenticated different byte-domain/parser fibers. LSPV-2/586 authenticated unbounded duplicate-member finality for the different /386 checker; LSPV-2/549 established that a dual-checker polyglot does NOT constitute one mixed proof. LSPV-3/551 and /554 already showed that the recovered /341 checker can accept SAT sources and cannot support an unqualified semantic-UNSAT goal. LSPV-2/539 is a DISTINCT reference checker, not native historical authority. This result is not a rediscovery of any of those findings.

## Theorem 603.1: accepted exact lexical witness class, original /341 only

Fix the pinned original /341 checker and an otherwise accepted parsed K4 packet with a string-valued evenWitness or non-null deletion assignment of length E=6. In raw JSON, replace the final literal zero digit inside that witness with its Unicode escape spelling \u0030. The complete decoded data object remains identical and the original checker accepts, preserving all source clause identities, parent edges, paid identities, semantic goal, and W=15. Replacing that digit instead with the JSON escape for LF, CR, U+2028, U+2029, TAB, SPACE or x causes rejection by the original checker. In particular, any approximate checker accepting the resulting newline-ended string is an *overapproximate but not acceptance-exact* implementation of this witness constraint.

**Proof:** ECMAScript JSON.parse decodes Unicode escapes to code points before the witness checks. A decoded 0 is unchanged, so every checked property and mathematical assertion is unchanged. A decoded non-binary character fails the anchored ECMAScript binary regex or the exact bit-length condition. SOURCE, proof DAG and tariff records have not changed; tests of the malicious mutations are independent. This is a theorem about the archived parser's witness fields, not about missing mixed transitions, source-byte authentication, or arbitrary SAT lower bounds. QED.

**Scope qualification:** no claim that every accepted JSON value in all other fields is canonically typed. Further JSON coercion and prototype behavior remain for full accepted-language enumeration.

## Native original-code replay and hostile controls

The *unchanged full original mathematical checker body* executed 25 times in hosted V8 with only fs/process/console adapters. This is authoritative source-body execution but NOT an operating-system Node subprocess replay of the published standalone program.

| Case class | ACCEPT | REJECT |
|---|---:|---:|
| Original K4 baseline | 1 | 0 |
| Escaped ASCII zero separately in each witness and together | 3 | 0 |
| Two unchanged literal last-zero controls | 2 | 0 |
| Seven malformed-character escapes in each witness field | 0 | 14 |
| Last binary zero replaced by one, two witnesses | 0 | 2 |
| Forged original signed source, parent ID or GF(2) sink | 0 | 3 |
| **TOTAL** | **6** | **19** |

All 25 predictions held; six accepted native-body checks totaled **8,406 original assertion groups**. Every accepted packet retains 16 signed SOURCE records and 15 paid inference records. Positive/negative tests include all seven non-binary escapes, not just the LF special case. The accepted both-escaped original packet is the exact raw JSON specimen, not a generated mathematical proof of a new rule.

**Published evidence:**
- Positive exact JSON: https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_1905_LSPV3_603_K4_ESCAPED_WITNESSES_ACCEPTED.json
- Raw 25-case hosted ledger: https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_1905_LSPV3_603_NATIVE341_WITNESS_BYTE_GRAMMAR_RAW.json
- Pinned OS subprocess reproducer (published, not executed in this run): https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_603_native341_witness_escape_grammar.cjs , final source Git blob **a18ae9760ffc20f51e08fb8537a4e25f8d88e2ad**. Source syntax-checked in JS and readback verified.

## Hypergraph, alpha/gamma and proof-chain implications

For the archived restricted checker, JSON raw-byte alternatives representing the SAME decoded witness string form a cost-preserving lexical fiber. An alpha projection can canonicalize the spelling while preserving external original-source identity *as a separate object*, signed SOURCE occurrences, paid-node event identities, every parent edge and the terminal goal; its gamma must include every genuine raw accepted alternative. The positive escaped source is a legal concrete step and cannot be excluded to strengthen a bound. The false Python-newline acceptance is a spurious abstract candidate and may be eliminated with the source-proved exact ECMAScript regex predicate. Cost remains W=15 only for logical paid nodes; raw evidence bytes, actual parsing/verification machine time, span and peak space remain distinct.

This single-field quotient is not a complete rule-by-rule abstract transformer system. The recovered checker has a known accepted-SAT-source defect, and its accepted terminal is NOT equivalent to a semantically sound UNSAT proof. No sound universal lower bound can follow by counting these lexical distinctions. Free choice of shortest whole-DAG proof, valid global paid-node sharing, reconvergence and all originally legal unknown transitions must remain available in the target historical calculus.

## Literature and scientific blockers

Primary: [ECMAScript specification, regular expressions and character assertions](https://tc39.es/ecma262/multipage/text-processing.html); [ECMAScript JSON.parse semantics](https://tc39.es/ecma262/multipage/structured-data.html); Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 1979, [DOI 10.2307/2273702](https://doi.org/10.2307/2273702). These give language/parser and proof-verification context, not the missing historical mixed-rule dispatcher. No model-transfer, all-input time-space lower bound or complexity-theoretic breakthrough follows.

Both root proof trackers (proof1 blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 blob f678f707880da4dfc97dabf778430c6dc816cb1f), issue #3 and current comments, AGENTS.md, CODEX.md, project skill, prior current handoffs, both pinned archived checkers, and materially relevant LSPV/peer/Grok/Claude 539–549 and subsequent material were surveyed. TRACKERS REVIEWED; NO MATERIAL CHANGE. Five current research automations verified enabled with original Pacific :00/:12/:24/:36/:48 timing and two Route A / three Route B labels; none changed.

**Affected proof IDs:** [P2-D1] OPEN (one new native evidence-field syntax authenticated); [P2-C3] OPEN; [P2-B1] OPEN; [P2-B2]/[P2-B3] separately OPEN; P versus NP OPEN.

**Unfinished:** full historical externally source-bound R_mix341 dispatcher, real RES-to-AND3 or DEF-facet-to-LOCAL-CONVERT parent link, global payment and assumption/context/branch interfaces. The standalone published Node OS reproduction, full preflight, and LaTeX compilation were NOT run. A complete accepted historical mixed-rule certificate with corrupt signed-source and parent controls remains the next decisive falsifier.

% END LSPV-3 REPORT::603
