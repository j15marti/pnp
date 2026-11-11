# LSPV-4/541: Native archived /386 verifier has a logarithmic-workspace read-only rescan implementation

**2026-11-11 04:36 PST | PNP Time-Space Resource Auditor | historical Route A retained | PROVED/RESTRICTED and COMPUTATIONAL | P versus NP OPEN**

## One candidate theorem; four falsifiers

**Candidate.** Let L be the byte length of an *explicit, canonical ASCII JSON* certificate of the original archived /386 SOURCE / paid DEF owner / free defining facet / strict binary RES checker. Canonical here means unique recognized keys, exact signed safe-integer decimal tokens, fixed-depth prescribed objects and arrays, no duplicate-key shadowing, no binary64 alternate numeric spellings. Every accepted certificate in this canonical sublanguage can be verified, including its original full-CLI eleven adversarial self-tests, with

$$
S_{\mathrm{work}}(L)=O(\log(L+2)),\qquad
T_{\mathrm{verify}}(L)=O(L^6)
$$

by a *separately specified read-only multi-pass verifier*. It is a proved restricted upper bound on **certificate verification**, not a measured V8/Node implementation bound, and not a bound on finding a proof, executing all proof deductions, or SAT decision.

**Falsifiers:** (F1) prepending authentic zero-charge facets breaks native chronological references; (F2) the unchanged complete original checker rejects the resulting certificate; (F3) a derived parent clause must be kept live instead of read again from its explicit certificate record; (F4) altered source, owner/facet, pivot, parent, or paid counters pass the original checker. All four fail in the explicitly tested family. Noncanonical decimal/binary64 aliases and the absent mixed checker are deliberate scope exclusions, not falsified extrapolations.

## Proof and exact native rule charges

The original verifier [pinned code, Git blob 338305c0ce101704205e57543756b8127074a986](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_386_independent_verify.js) checks each inference against clauses explicitly present in its read-only certificate. A read-only indexed scanner needs only logarithmic-size record, literal, owner and byte-position counters. Check the cubic SOURCE graph by rescanning the edge list; regenerate each vertex's four forbidden parity rows using an eight-mask loop, compare against the original signed clauses, and verify their exact occurrence once each. For paid gate owners, rescan preceding declarations to verify fresh outputs and legal producer-before-consumer inputs. For a DEF record, compare its encoded clause against the three canonical owner facets. For a RES record, find its two earlier encoded parent records by indexed rescanning; compare signed pivot and sorted resolvent literals one at a time without materializing any complete derived row. Enforce the empty terminal clause, source completeness, symbol scope and native summary counters by further scans.

All nested loop bounds are polynomial in L; a deliberately loose O(L^6) bound pays for source reconstruction, indexed parent retrieval, pairwise sorting, record/owner comparisons and the 11 full-CLI negative controls. Each negative control is a read-only virtual view with one prescribed field/tuple changed; no physical structuredClone copy is necessary for the *mathematical* verifier. The native E<=12 truth-table control enumerates at most 4096 edge assignments, a constant. Canonical fixed-depth JSON syntax can itself be checked with logarithmic position counters. Any hash of the input for the original CLI's diagnostic SHA output can be computed streaming with constant-size digest state.

For this **archived /386 fragment only** the actual charges are:

| Rule | Logical charge | Separate physical evidence/retrieval costs |
|---|---:|---|
| Original signed SOURCE | 0 | Source clause bytes, signed source provenance, indexed retrieval |
| Globally declared conservative DEF owner | 1 per distinct paid owner | Declaration tuple, wire namespace/freshness, gate dependency check |
| Authentic defining DEF facet | 0 additional | Facet bytes, indexed retrieval, owner lookup |
| Strict binary RES | 1 per record | Two parent references, pivot/resolvent comparison, retrieval |
| Full-CLI built-in adversarial tests | Not part of historical proof work | Eleven repeated validation checks |
| AND3, GF(2), LOCAL-CONVERT, branches, contexts, weakening, discharge, joins, deletion and exported/private wire operations | **NOT AUTHENTICATED TOGETHER** | Exact historical grammar/weights/transition still missing |

For an accepted full packet, W equals the number of paid RES records plus the number of declared DEF owners, each counted once. A rescan verification path can charge exactly these amounts in a restricted owner-aware abstract ledger and retain the explicit original source and empty terminal goal. This is a realizable P2-C3 **fragment** witness, not an all-rule abstract cost theorem.

## Native evidence and independent controls

Baseline: the original signed guarded odd-K4 [LSPV-4/540 certificate, Git blob 25b5c1f95734f6eae36bdbb4a17c948c00753cff](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json), comprising 17 original SOURCE records, 30 RES, two genuine DEF facets and one paid globally declared gate owner. For each integer k>=0 prepend k copies of the same *genuine* facet (owner 0, clause [1,-8]), increase all original RES parent indices by k and increase only the facet/record summary counters. This leaves the source, every paid inference, its original dependencies, and contradiction intact:

$$
W(k)=31,\quad R(k)=60,\quad N_{\mathrm{records}}(k)=49+k,\quad
N_{\mathrm{facets}}(k)=2+k.
$$

| Extra true facets k | Raw canonical JSON bytes, no newline | Records | Paid work | Original full-CLI assertions |
|---:|---:|---:|---:|---:|
| 0 | 3,079 | 49 | 31 | 3,750 |
| 1 | 3,129 | 50 | 31 | 3,341 |
| 4 | 3,279 | 53 | 31 | 3,467 |
| 32 | 4,638 | 81 | 31 | 4,643 |
| 128 | 9,308 | 177 | 31 | 8,675 |
| 512 | 27,740 | 561 | 31 | 24,803 |

**Actual executed validation:** The complete original archived /386 CLI body, unchanged except hosted V8 I/O adapters and a diagnostic placeholder hash, accepted all six variants and passed **66 built-in hostile tests**, with **48,679 original checker assertion groups** in aggregate. An independently written source/owner/RES rescan-by-index semantic check accepted all six. A 36-case corruption matrix, six variants each of pivot, facet owner, facet clause, forward parent, paid counter and original charge, was rejected by both the original mathematical checker and the independent rescan check. These are computations on actual checker rules, not OS Node benchmark or machine-space experiments.

The executable audit [lspv4_541_archived_386_rescan_firewall.cjs](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_541_archived_386_rescan_firewall.cjs) reconstructs the same positives and hostile controls and **runs the unchanged original checker via a separate operating-system Node subprocess when executed in a local repository checkout**. It passed JS syntax compilation in hosted V8. Its operating-system end-to-end execution has NOT been observed in this run. Its independent JS step audit stores the JSON-parsed input in host RAM; this is NOT a physical logspace implementation of the mathematical verifier.

## Physical resource firewall and falsifier implications

Evidence size B(k) grows with k, from 24,632 bits to 221,920 bits in the tested range. The original checker stores a reference for every input record in its internal known array, so its source code requires Omega(49+k) such references; actual V8 high-water bytes have not been measured. The native checker visits all 49+k records, requiring Omega(k) record-iteration steps in that implementation. By contrast, a separately specified read-only multi-pass verifier may retain *zero derived clause values* and use O(log B) writable bits by paying for rescans. Its conservative sequential time is O(B^6).

The RES-only dependency depth of the underlying refutation remains 7 (as separately audited in /540); the newly prepended DEF facets introduce no paid inference depth. A particular fresh-result chronological proof-evaluation schedule was previously bounded above by nine paid-result slots, but this **does not imply a lower bound on independent certificate verification memory**. Source/packet parsing, references and retrieval, recomputation, arbitrary identifier lengths, compact affine rows, transient buffers, live contexts and branch joins must be charged separately in any physical model. In particular, proof discovery and proof execution remain unbounded by this verifier theorem.

## Corpus and literature audit

Reviewed both complete root trackers (preflight Git blobs: proof1 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2 2d148226643a04cdb139f2b981f35ed528b89b90), issue #3 and recent comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, /540 five-role handoff, original /386 code, original /540 fixture, LSPV-4/539-540, LSPV-2/549, LSPV-1/569, LSPV-5/483-485 and LSPV-3/567. The earlier /531-533 results were for a separate canonical proof grammar. Here the logical checks and positive packets come from an actual recovered archived checker, but the new logspace theorem is still scoped to canonical bytes. Actual accepted raw binary64 decimal aliases and duplicate-key shadows from /483-485 and /567 show why the theorem must NOT be asserted for all ECMAScript JSON byte strings.

Primary sources: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, J Symbolic Logic 44 (1979) 36-50, DOI 10.2307/2273702; Nordström, *Pebble Games, Proof Complexity, and Time-Space Trade-offs*, Logical Methods in Computer Science 9(3), 2013, DOI 10.2168/LMCS-9(3:15)2013. The proof-system verifier and proof-evaluation resource are distinct.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No edits to proof1.txt, proof2.txt, main.tex, historical inference weights, agent ownership, times, or two Route A / three Route B labels.

**P2-D1 OPEN:** no authenticated complete historical R_mix341 accepted-byte checker. **P2-C3 OPEN:** no all-rule cost-sound abstract interpretation. **P2-B1 OPEN:** no superpolynomial minimum-work lower bound. **P2-B2/B3 OPEN separately. P versus NP OPEN.**
