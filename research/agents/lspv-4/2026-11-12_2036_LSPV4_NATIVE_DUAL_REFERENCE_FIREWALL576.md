% LSPV-4 REPORT::576::2026-11-12T20:36:00-08:00
# LSPV-4/576: Exact per-reference decoding and once-paid work on two distinct native checker fragments

**2026-11-12 20:36 PST | LSPV-4 Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED combinatorial lemma; COMPUTATIONAL source-pinned accepted-certificate audit | P versus NP OPEN**

## Candidate resource invariant, and falsifiers

**Candidate.** For a fixed, accepted, chronologically typed proof DAG, *paid derivation identities* and *parent-reference occurrences* are different resource sets. Charge each paid RES/AND3/XOR identity and each once-paid owner exactly once, while charging each textual parent application at its actual width **each time it is read**. Topological reordering cannot change the multiset of original parent references, but tree-unfolding a genuinely shared paid result can overcharge logical work. This theorem concerns the separate actual archived /341 and /386 checker fragments, **not** a fabricated combined checker.

F1: every authenticated /341 fixture shares a paid node. **False.** All seven original accepted proof fixtures have maximum fanout one, consistent with LSPV-3/598's stronger accepted-language tree theorem.

F2: the actual /386 W38 DAG contains no shared paid Resolution. **False.** Its original RES record index 23 is applied twice.

F3: unrolling /386's shared RES costs the same as its actual signed shared DAG. **False.** The accepted DAG charges 35 distinct RES plus three once-paid gate owners, W=38; its tree expansion contains 36 RES occurrences and costs 39 under a no-sharing policy.

F4: a count of parent applications determines serialized reference cost. **False.** Actual ASCII ID lengths in /341 and decimal record-index lengths in /386 must be retained; legal ID relabeling and support representation changes can alter those sizes. The exact figures below are not universal encoding minima.

## Original authority, provenance, literature and precedence

Independently fetched both root proof trackers (proof1 blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 Git blob f678f707880da4dfc97dabf778430c6dc816cb1f), issue #3, AGENTS.md, CODEX.md and the repository skill; reviewed the current /575 role report and handoff, /574, /539 and /544, original /341 checker and sibling /386 reports, peer LSPV-3/598 and LSPV-2/588, plus relevant /527 and /539-549 search results. Original /341 source fixture packet: Git blob fe27fe1011d0021e721ccaeb747ed58da65d7464, checked by original archived checker fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Original /386 W38 accepted shared-DAG packet: Git blob 28fc9f41ec151a741e70274637c06629fb9a224f, checked by separate archived checker 338305c0ce101704205e57543756b8127074a986.

**Precedence:** LSPV-3/598 already established /341 accepted-packet tree rigidity. LSPV-4/539 already normalized redundant /386 clauses. LSPV-4/566-570 investigated particular W38 storage schedules; /527 established native /341 identifier-optimal relabelings. The incremental result here is the **source-pinned, side-by-side, exact application-lexeme ledger and 38-versus-39 shared-work falsifier**, computed independently on actual two sibling packets. This is deliberately not a new general pebbling or abstract-interpretation theorem.

Primary literature: Hong and Kung, *I/O Complexity: The Red-Blue Pebble Game*, STOC 1981, DOI 10.1145/800076.802486; Sethi and Ullman, *The Generation of Optimal Code for Arithmetic Expressions*, JACM 1970, DOI 10.1145/321607.321620; Nordström, *Pebble Games, Proof Complexity, and Time-Space Trade-offs*, LMCS 2013, DOI 10.2168/LMCS-9(3:15)2013. These distinguish work, I/O and storage in their respective machines, **not** the historical R_mix341 dispatcher.

## Exact theorem and count-once proof

Fix an original byte packet with a finite acyclic chronological proof DAG G. For a node v, let c(v) be the authenticated fixed paid tariff if v is a *new paid inference*, excluding references to v. Let O be the set of once-paid gate-definition owners. Let E be the **multiset** of ordered inference-parent occurrences, whose encoded reference lexeme lengths are len(e).

Define the *separate* exact coordinates

$$
W(G)=\sum_{v\in V_{\rm paid}(G)}c(v)+\sum_{o\in O}c(o),\qquad
L_{\rm ref}(G)=\sum_{e\in E}\operatorname{len}(e).
$$

These are equal to the actual respective counts of distinct paid identities and recorded parent-lexeme characters, by definition of the original accepted packet; the two sums range over different **resource events**. Every topology-preserving execution reordering that keeps the same IDs, edges, original source and paid owners leaves both quantities invariant. By contrast, replacing the shared DAG by its recursively unfolded tree changes paid event multiplicities. For any node v, its tree multiplicity is defined by m(root)=1 and propagation m(u)+=m(v) for each parent occurrence v->u in reverse chronology. The tree-only tariff is therefore the sum of m(v)c(v), plus once-paid gate owners if they remain globally owned. This is at least W for the same fixed packet, with strict inequality whenever a paid node has m(v)>1. This is an exact **representation-specific reference ledger**; a different syntactic encoding may alter L_ref.

The argument does **not** show L_ref as a lower bound on arbitrary machine time. It is the number of original parent-lexeme payload bytes under a declared one-scan-per-reference textual decoder. Full original parser time, UTF-8 decoding, hashing, context lookups, actual writable memory, proof discovery and SAT decision complexity are separate coordinates.

## Concrete replay and exact resource results

| Actual original packet | Paid logical work | Parent applications | Reference-lexeme payload | Shared parent records | Naive expanded paid work |
|---|---:|---:|---:|---:|---:|
| /341 K4 | 15 | 30 | 70 ASCII ID bytes | 0 | 15 |
| /341 K3,3 | 23 | 46 | 118 bytes | 0 | 23 |
| /341 Cube | 31 | 62 | 166 bytes | 0 | 31 |
| /341 Petersen | 39 | 78 | 214 bytes | 0 | 39 |
| /341 Prism6 | 47 | 94 | 262 bytes | 0 | 47 |
| /341 Prism16 | 127 | 254 | 796 bytes | 0 | 127 |
| /341 Bridged K4x2 | 39 | 78 | 214 bytes | 0 | 39 |
| /386 W38 original shared DAG | **38** | **70** | **121 decimal-index digits** | **13** | **39** |

Seven /341 fixtures are SEPARATE independent proof claims, **not** a single 321-node deduction. Summing their per-packet audit rows gives **321 paid deductions, 642 parent applications, 328 SOURCE applications, 314 derived applications, 942 ASCII SOURCE-reference bytes and 898 ASCII derived-reference bytes (total 1,840)**. Across the seven fixed fixtures all owners have fanout one.

The /386 accepted 58-record packet contains 17 original SOURCE, six zero-extra-paid defining-facet records, 35 paid Resolution inferences and three globally once-paid gate owners: W=35+3=38. There are 70 RES-parent applications but just 57 distinct referenced records, with 13 of those applied twice: 11 SOURCE, one DEF facet at index 22, and one paid RES at index 23. Terminal rooted tree expansion contains 29 SOURCE occurrences, eight DEF-facet occurrences, and 36 RES occurrences. A tree-only expense for paid Resolution would be 36 rather than 35, overcharging by exactly one. The parent's decimal-digit lexeme sizes total **121 bytes**, not the 790-byte *parent-clause scan payload* of /566: those are different accounting metrics.

**Evidence status.** Independent hosted V8 parsing and arithmetic computed all coordinates from pinned GitHub source blobs and asserted the central identities and quantities. The new runnable reproducer includes optional original **OS Node CLI** calls for both pinned separate checkers; those optional OS calls have not been executed during this hosted run. Earlier /575 and /566 original-checker acceptance evidence is inherited as provenance, not retested or strengthened here.

## Resource firewall and full-path limits

The exact /341 /575 packed-value area and peak are *separate* post-step semantic retention coordinates. The source IDs and parent lexemes above are *read-only evidence traffic*, not extra derived registers. It would be erroneous to add L_ref measured in bytes to retained area measured in byte-steps without an explicit per-read tariff or conversion. It would also be erroneous to combine /341 packed-value minima with /386 shared-Resolution work as one realizable mixed proof: the two original checkers have different languages and do not authenticate RES-to-AND3 edges.

Full historical operations SOURCE, Resolution, AND3, GF(2), LOCAL-CONVERT, paid DEF, wire export/private scopes, contexts, weakening, branching, discharge, joins and deletion remain unproven as a single original accepted-byte calculus. Alternate proof DAGs, GF(2) shortcuts, extension-variable proofs, learned-lemma sharing across compatible branches, arbitrary recomputation, large identifiers and compact affine encodings remain MAY in the all-rule abstraction. The correct full-calculus lower-bound quantity W_R still minimizes over **all** legal proofs; proof discovery and certificate verification are different costs.

**Proof-chain IDs [P2-D1] OPEN -> [P2-C3] OPEN -> [P2-B1] OPEN, with [P2-B2] and [P2-B3] separately OPEN. [P1-01], [P1-03], [P1-04] OPEN. TRACKERS REVIEWED; NO MATERIAL CHANGE. P versus NP OPEN.**

## Reproduction

- Executable: experiments/arc/lspv4_576_dual_native_reference_accounting.cjs
- Hosted V8 raw data: results/raw/arc/2026-11-12_2036_LSPV4_576_DUAL_NATIVE_REFERENCE_LEDGER_RAW.json
- Five-role handoff: research/coordination/2026-11-12_2036_LSPV4_NATIVE_REFERENCE_ACCOUNTING_FIVE_ROLE_HANDOFF576.md
- Optional original OS checker replays: node experiments/arc/lspv4_576_dual_native_reference_accounting.cjs --native
% END_OF_VERIFIED_REPORT::LSPV-4::576
