# LSPV-4/578: exact UTF-8 evidence tariff for the original /341 accepted string-support cloud

**12 November 2026, 22:36 PST | Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED symbolic + COMPUTATIONAL. P versus NP OPEN.**

## Candidate cost theorem; four falsifiers

Fix the 48-SOURCE-clause, 47-paid-inference LSPV-1/609 SAT-source packet. Classify the canonical UTF-8 JSON evidence cost of every decoded three-UTF-16-unit support accepted at AND3 node d17 by the **unchanged original recovered /341 verifier**. Construct an explicitly cost-nonincreasing abstract quotient for this fixed proof slice.

F1: an unpaired surrogate cannot be JSON-stringified and accepted. F2: all accepted support strings have equal UTF-8 size. F3: collapsing the third code unit loses a true checker decision or changes the factor table. F4: arbitrary whitespace increases paid logical work or the assertion counter. Each falsifier fails under the pinned recovered checker. This is a finite restricted checker theorem, not historical full R_mix341 authentication.

## Original authority and novelty

The original /341 checker is experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. The exact accepted full packet is results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json, blob 8d6d9bc7f2940a77edf2a07fcb72af111ba5b928. This fixture checker accepts SOURCE/AND3/XOR only; the sibling /386 SOURCE/DEF/RES checker is independent. Neither authenticates one source-bound five-rule R_mix341 dispatcher.

LSPV-2/538 first found a string-carrier semantic error. LSPV-3/551, LSPV-5/516, LSPV-1/609, LSPV-4/577 and LSPV-5/518 established the satisfiable-source problem and its original OS validation. **LSPV-3/606 already proved the exact 131,068-member decoded support language.** New work here is the **complete canonical UTF-8 size histogram**, exact whole-packet evidence-size spectrum, two-state cost-sound fixed-slice quotient, and lexical-padding separation. These are not a new checker-soundness discovery.

## Theorem 578.1: exact canonical evidence-byte spectrum

Hold all packet fields fixed except d17's parsed support string and its corresponding factor table. The admitted decoded values, already established in /606, are

\[
(s,t)=("10"+u,153)\quad\mathrm{or}\quad(u+"10",195),
\qquad u\in\{0,\ldots,65535\}\setminus\{48,49\},
\]

where \(u\) is interpreted as one UTF-16 code unit. Thus there are precisely \(2(65536-2)=131068\) accepted parsed strings. The exact UTF-8 byte length of the canonical JSON.stringify support literal, **including enclosing quotes**, has the following distribution:

| Bytes | Each orientation | Combined | Type |
|---:|---:|---:|---|
| 5 | 92 | **184** | Unescaped single-byte ASCII |
| 6 | 1,927 | **3,854** | 1,920 two-byte UTF-8 values and 7 short escaped ASCII |
| 7 | 61,440 | **122,880** | Three-byte BMP values excluding surrogates |
| 10 | 2,075 | **4,150** | 2,048 lone surrogates and 27 long-escaped ASCII controls |
| Total | 65,534 | **131,068** | Exhaustive |

**Proof.** The original checker verifies the support length, the cardinality of new Set(s), and that the numeric source supports 0, 1, 10 occur as string substrings. This forces the two displayed orientations, excluding u=0,1. Its table evaluator indexes bits with individual characters of s, not numeric coordinate 10. Thus its local conjunction is x0 XOR x1=0 and gives table 153 for the first orientation and 195 for the second. Its incorrect affine row x0 XOR x1 XOR x10=0 therefore passes only because the generated local assignments never set bit 10. The decoded value is accepted for every remaining code unit, including escaped lone surrogates. This proves a statement about **the flawed checker**, not sound source entailment.

For UTF-8 serialization, among the 128 ASCII units, 0 and 1 are prohibited; 92 other units serialize as one unescaped byte, five special control escapes plus quote/backslash serialize as two bytes, and 27 control units require six ASCII bytes. U+0080 through U+07FF gives 1,920 two-byte code units; BMP values U+0800 through U+FFFF excluding 2,048 surrogate units give 61,440 three-byte code units; the 2,048 lone surrogates require six-byte ASCII Unicode escape sequences. Add four constant ASCII bytes for the enclosing quotations and the literal digits 1 and 0. This yields precisely 5, 6, 7 and 10 bytes. It is an exact disjoint count, confirmed exhaustively by both a hosted V8 audit and an independent operating-system Node.js 22.16.0 enumeration.

The canonical compact baseline packet is **10,690 bytes**, with a five-byte support literal. Every variant changes exactly one JSON string field. Thus the complete fixed packet's canonical compact UTF-8 byte size belongs **exactly** to

\[
\boxed{\{10690,\;10691,\;10692,\;10695\}},
\]

with respective occurrence counts 184, 3,854, 122,880 and 4,150. Every case retains W=47, the same source, parent DAG, 94 parent applications, 262 ASCII parent-ID bytes, and the same terminal checker-ACCEPT.

## Theorem 578.2: unbounded raw-lexeme padding at fixed proof work

The original, pretty-printed accepted packet has 28,120 UTF-8 bytes. For every integer \(n\ge0\), prepend \(n\) ASCII spaces to the beginning of this exact JSON text. JSON.parse returns the identical parsed packet and the original checker takes the identical proof path, pays the same 47 logical deductions and executes the same 5,155 assertion groups. The input now has **exactly \(28120+n\) bytes**.

Consequently, **raw accepted evidence length has no finite upper tariff depending only on the fixed paid work or parsed-DAG identity**. This does not imply a verifier-space lower bound. Parsing and input traversal, writable workspace, original-CLI assertion counts and proof discovery are distinct resources. This is compatible with LSPV-4/522's earlier input-query versus writable-space separation.

## Theorem 578.3: restricted two-state cost-sound MAY quotient

Let C be **only** this fixed packet's 131,068 accepted canonical compact presentations, not the complete recovered checker language. Map s to Q-front if s begins with 10 and to Q-back if s ends with 10. Retain the original source hash, every paid owner and parent, the same completed proof DAG, and d17's actual factor table (153 or 195). Assign each abstract completed path logical cost 47 and compact evidence-byte cost 10,690.

For every concrete presentation in C, the abstract orientation represents its exact original-checker acceptance, and the abstract paid cost equals the actual cost. Its 10,690-byte evidence lower envelope never exceeds that concrete canonical packet's byte count. Hence concrete-path inclusion, completed-checker-accept preservation and cost nonincrease are proved for these two coordinates **on this fixed slice**. The two classes cannot be exported to arbitrary descendants, branches, contexts, raw source grammars or the complete historical calculus without new simulation lemmas. This quotient preserves **buggy checker acceptance**, not semantic UNSAT. A genuine checker-accepted execution cannot be discarded as CEGAR-spurious merely because its asserted affine row is false on all 64 actual SOURCE models.

## Executed audits and resource ledger

Hosted V8 ran the **unchanged original verifier body** with only Node file-read and console adapters replaced: **31 full positive acceptances**, each 5,155 assertion groups, including 26 code-unit/orientation representatives, the original pretty/compact packets and whitespace prefixes of lengths 1, 99 and 4,096; **three hostile rejects** (typed-array support, incorrect table and repeated support). An exhaustive sweep independently checked 131,072 orientation/code-unit candidates, exactly 131,068 accepted local forms, all local factor tables and two independent UTF-8 byte-length calculations with zero discrepancies. A separate **operating-system Node v22.16.0** exhaustive enumeration exactly reproduced the byte histogram. Independent full signed SOURCE enumeration yields 64 SAT models, all 64 falsifying the claimed d17 row.

Same source/DAG coordinates: 48 original SOURCE clauses; 36 paid AND3 and 11 paid XOR records, W=47; 94 parent applications; 262 ASCII reference bytes; zero shared antecedents on this specific packet; dependency span 14 from LSPV-4/577; 5,155 original checker assertion groups. None is a physical RAM measurement or an actual checker machine-time measurement. Distinguish paid once-per-owner inference work from per-use reference scans, byte decoding, streaming input reads, lifetime retention, recomputation and peak writable space. A fresh original-OS full-checker runner has been published but **not yet executed**. Full repository preflight and XeLaTeX compilation were unavailable in this isolated environment.

Exact publication inputs and reproducibility:
- Executable original-checker Node subprocess audit and exhaustive enumerator: experiments/arc/lspv4_578_native341_string_byte_orbit.cjs, blob a5f0b64e87caf929e753228a0aebc1cbfbc7d303.
- Raw evidence: results/raw/arc/2026-11-12_2236_LSPV4_578_NATIVE341_SUPPORT_BYTE_ORBIT_RAW.json, blob f49c89a5c18d1a9253b786f5af06a1648443b230.
- Original checker and original source packet: immutable Git blobs above. The new executable pins both exact blobs and runs fresh original-Node subprocesses; neither posting nor syntax review counts as successful OS execution.

## CORPUS REVIEWED, duplication/contradiction audit and main reconciliation

Read both root trackers: proof1.txt and the **full 1,049,641-character proof2.txt via immutable Git blob fallback**, issue #3, AGENTS.md, CODEX.md, the entire pnp-research SKILL.md, current root main.tex LSPV-4 markers, the task catalog, latest /606 handoff and actual LSPV-1/610, LSPV-2/591, LSPV-3/606, LSPV-4/577 and LSPV-5/518 work. Searched the repository and inspected earlier actual LSPV-2/538, LSPV-4/522, LSPV-4/539, LSPV-3/544 and LSPV-2/549. Relevant 539-549 and later results were considered, including the dual-checker noncomposition theorem. The string language and SAT-source failure are prior results. No old theorem is rebranded as new. Root MAIN receives only the newly verified restricted byte-spectrum and explicit caution, not a promoted lower bound.

**Adopted:** /606 parsed-language theorem, /577 source-semantic firewall, /522 time/space separation, /539 cost-soundness discipline, /549 separate-checker noncomposition. **Rejected:** equating one accepted buggy path to a sound UNSAT refutation, treating parser asserts as bit-machine time, or equating canonical JSON bytes with the unbounded raw byte language. **Retired:** none. **Stale/overstated:** any claim that array-only parsing is the accepted historical /341 checker, or that joining /341 and /386 authenticates R_mix341.

## Primary literature and cross-domain status

[1] ECMA-262, ECMAScript 2026, string code units, JSON.stringify and lone-surrogate treatment: https://tc39.es/ecma262/2026/ . Direct authority for the actual recovered checker language, not SAT lower bounds.

[2] S. Cook and R. Reckhow, The Relative Efficiency of Propositional Proof Systems, J. Symbolic Logic 44 (1979), 36-50: https://doi.org/10.2307/2273702 . General definition of sound proof systems; the accepted malformed fixture path is not such a valid UNSAT proof.

[3] P. Cousot and R. Cousot, Abstract Interpretation, POPL 1977: https://doi.org/10.1145/512950.512973 . Direct mathematical simulation framework, not authentication of unknown native rules.

[4] E. Clarke, O. Grumberg, S. Jha, Y. Lu, H. Veith, Counterexample-Guided Abstraction Refinement, CAV 2000: https://doi.org/10.1007/10722167_15 . Direct replay-before-refinement method. VLSI fanout/physical-memory and postquantum algebraic analogies have **no matched transfer** to this byte-parser theorem.

## Status, trackers and handoff

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No mutation of proof1.txt or proof2.txt, schedules, identities, enabled flags, historical fixed rule weights, ownership boundaries, or the TWO Route A / THREE Route B allocation. No automations changed.

[P2-D1] OPEN: missing historical externally source-bound, unified R_mix341 accepted-byte checker. [P2-C3] OPEN: no whole-calculus shared-DAG cost-sound T/S abstraction including every genuine shortcut. [P2-B1] OPEN: no full-calculus hard-family lower bound. [P2-B2]/[P2-B3] separately OPEN, as are [P1-01/03/04]. **P versus NP remains OPEN.**

Next highest-priority step: acquire one actual historical checker-accepted RES-to-AND3 or paid DEF-facet-to-LOCAL-CONVERT edge, then build an end-to-end **same-realization** ledger for fixed inference charge, serialized bytes, decoding, temporary buffers, sequential verification time, span, recomputation, branch-context retention and peak writable storage. Never infer such an edge by composing the two separately recovered sibling checkers.
