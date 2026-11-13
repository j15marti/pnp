# LSPV-2/598: Original-checker-accepted lazy SOURCE and defining-facet scheduling

**2026-11-13 05:12 PST | SAT-Circuit Reduction Builder | historical Route A unchanged | PROVED/RESTRICTED code-property theorem + COMPUTATIONAL original-CLI replay. P versus NP OPEN.**

## Target, candidate, and four falsifiers

**Candidate 598 (P2-D1/P2-C3 restricted).** The archived original `/386` checker can accept genuine byte-exact refutations in which paid Resolution occurs *before* some compulsory SOURCE records and free defining-facet records, not only certificates with a SOURCE/DEF prefix. A source-bound P2-C3 abstract state requiring all SOURCE records and facets to be materialized before the first inference therefore excludes accepted histories and is incomplete for exact chronological replay.

F1: the original checker rejects late SOURCE or DEF; F2: the remapping changes any signed parent, source occurrence, terminal ancestry, resolution span or fixed paid work; F3: the independent external signed SOURCE bytes no longer match the scheduled packet; F4: the original checker accepts a future parent, wrong SOURCE signature, corrupted facet, underpayment, wrong pivot or an unsupported AND3 in its `/386` dispatcher.

## Provenance of the actual archived checker

Unmodified original mathematical/CLI checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`, exact original-checker source SHA-256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`. Seed accepted W29 SHA-256 `0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0`; seed W32 SHA-256 `56222417e011357a9f7d141221b9e10b0e4eb230a05ebf6365e00b95ec9be238`. External signed original `SOURCE.cnf` is 17 clauses on 7 variables with SHA-256 `3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c`.

The checker accepts record kinds `SOURCE`, `DEF`, and `RES`; its `gate_defs` paid-owner bank is checked *before* visiting any record. SOURCE and DEF have no parent references, are not required to precede all RES, and are each checked by their own grounded clause/owner predicates. `RES` has exactly two earlier record indices and an exact oriented signed pivot. Final summary counts are checked at the end; the last record must be the empty contradiction. The checker has no full `R_mix341` dispatcher and is not intrinsically independently bound to the external DIMACS file. The LSPV-2/598 *reference* wrapper independently binds the original signed SOURCE multiset to the separate file before replay. This additional check does not modify or confer additional authority on the original checker.

## Theorem 598.1: legal topological SOURCE/DEF schedule transport (restricted)

Fix any certificate accepted by the `/386` mathematical checker whose records are `SOURCE`, `DEF`, and `RES`, ending in an empty RES clause. Let `pi` be any bijective permutation of its records such that (i) the final empty record remains last, (ii) the producer of each RES parent remains before its consumer, and (iii) each RES parent index is rewritten using `pi` while all signed clause payloads, SOURCE tags, DEF owner tags, `spec`, `gate_defs`, and `summary` remain unchanged. Then the checker accepts the permuted mathematical certificate, with the same terminal ancestry under record identity and the same fixed logical work `W = #RES + #distinct gate_defs`. Neither all SOURCE records nor all defining facets need precede the first RES.

**Proof.** Every SOURCE check uses the source owner's in-band signed expected clause and a set of occurrence keys independent of chronological record position. Every DEF check uses the prevalidated globally paid owner bank, independent of position. Every RES check reads only earlier parent clause payloads, its own oriented pivot and exact resolvent; condition (ii) ensures the new indices still reference precisely the original two antecedents. Unique SOURCE occurrence keys, final counts, terminal empty clause and literal domain remain unchanged under bijection. The induction on the new record order preserves each checked derived clause. Terminal ancestry and depth are invariant under dependency-DAG isomorphism. Both the RES count and the cardinality of `gate_defs` are invariant. These are properties of the original source code's mathematical `checkProof` body. Its additional built-in negative-test CLI wrapper is tested, not inferred, in the finite experiments. QED.

**Quantifier/scope limit:** This is not a theorem about the missing historical multi-rule `R_mix341` checker. It cannot justify free source acquisition, alternative definitions, branch discharge, a lower bound on optimal work, or a SAT decision-time statement.

## Original checker OS evidence

The standalone reference script emits exact UTF-8 JSON packet bytes, checks pinned source/code hashes, verifies all original signed SOURCE clauses against the separately read `SOURCE.cnf`, and launches a fresh unmodified Node.js checker process for **each packet**. Runs are deterministic (no random seeds). Four orders per W29 and W32: original SOURCE-first, RES-and-premise-on-demand (`lazy`), terminal-ancestry-first, and reverse SOURCE order.

| Seed / schedule | Original checker | SOURCE after first RES | DEF facets after first RES | Work W | Terminal RES span | JSON bytes |
|:--|:--|--:|--:|--:|--:|--:|
| W29 / source-first | ACCEPT | 0 | 0 | 29 | 7 | 2,867 |
| W29 / lazy | ACCEPT | **15** | 0 | 29 | 7 | 2,871 |
| W29 / ancestry-first | ACCEPT | 0 | 0 | 29 | 7 | 2,867 |
| W29 / reverse-source | ACCEPT | 0 | 0 | 29 | 7 | 2,872 |
| W32 / source-first | ACCEPT | 0 | 0 | 32 | 8 | 3,153 |
| W32 / lazy | ACCEPT | **15** | **2** | 32 | 8 | 3,153 |
| W32 / ancestry-first | ACCEPT | 0 | 0 | 32 | 8 | 3,153 |
| W32 / reverse-source | ACCEPT | 0 | **2** | 32 | 8 | 3,150 |

**Eight original CLI ACCEPT results and six original CLI REJECT results, total 28,628 checker assertion groups across accepted processes.** Rejected hostile packets: future SOURCE/DEF parent, incorrect signed SOURCE, paid-owner undercharge, invalid DEF facet, incorrect signed Resolution pivot, and unsupported `AND3` tag in the restricted `/386` checker. Every full original CLI accept also passed its 11 internal mutation-rejection controls (88 internal controls across eight positives). Each positive packet matches all 17 independent original signed SOURCE clauses; the source-support/DEF-facet terminal ancestry, W and span match its original seed.

The original verified certificates intentionally have unused paid owner identities / original SOURCE clauses not necessarily on the terminal cone. Neither compulsory input validation nor proof construction becomes free because their record appears late. Serialized certificate bits change separately from W and span. Peak writable memory, parsing cost, verification time, construction time and source acquisition remain distinct and are **not** claimed to improve in this experiment.

## P2-C3 CEGAR implication and alpha/gamma constraint

Concrete configuration `c = (external_source_hash, spec, owner_bank, emitted_record_map, used_SOURCE_occurrences, validated_facets, derived_clause_DAG, paid_owner_set, open_contexts, costs)` must permit a pending original SOURCE or DEF record to be authenticated and emitted after earlier paid RES records. A may-abstraction `alpha(c)` requiring `emitted_SOURCE_count=4h+1` whenever `#RES>0` violates goal-preserving coverage of the accepted W29/W32 lazy traces. Sound repair is to retain (possibly symbolically) the emitted original occurrence set and a pending-set abstraction, to preserve optional zero-inference SOURCE/DEF emissions, and to replay legal parent-index renamings. An overapproximation may allow additional unknown rule transitions, but cannot silently delete authenticated ones. The coverage property here addresses **chronological trace completeness**, not a proof that a source-first normal form cannot exist for logical-work-only purposes. In fact Theorem 598.1 permits moving records back into a prefix without changing W for these restricted packets.

For an abstract transition `a -> a'` representing concrete `c -> c'`, the required cost guarantee remains `abstract_delta <= concrete_delta` with distinct paid-owner identities charged once, and an abstract goal must cover each concrete completed refutation. Falsifying a SOURCE-prefix invariant does not by itself force a negative logical-work lower bound to change if normal-form equivalence is separately proved and fully charged for the resource being studied.

## Corpus audit, literature, and repository comparison

Read `proof1.txt` current blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, complete `proof2.txt` via Git blob `930c5eeddafce656717f28055a7a9a755f44737c` (contents API window was empty), issue #3 and newest comments through 2026-11-13 04:43 PST, `AGENTS.md` blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, and repo skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`. Root `main.tex` was independently retrieved by immutable blob `c62fbe02de4bee0fff7484c4c49caff1896d3993` (2,409,670 characters), without any change. Relevant LSPV-2 reports 539-549 were located and read as actual distinct files; /552-555 and /595-597 and the latest /597 five-role handoff were cross-checked. Peer LSPV-3/612 and LSPV-4/584 evidence was reviewed in issue #3; earlier `/341` checker exhaustive AND3/XOR dispatch and `/386` SOURCE/DEF/RES split remain separate. The user-authorized two Route A / three Route B labels remain in place.

**Precedence:** LSPV-2/553 already established *free facets preceding* the SOURCE prefix; LSPV-2/597 already proved *inter-block RES permutations* and measured a separate restricted space metric. /598's addition is an explicitly native, independently source-bound *late mandatory SOURCE and late real DEF facet after paid RES* schedule, a topology-based transformer proof, and the positive/hostile regression corpus. This does not supersede either earlier theorem. The older /539 typed replayer and /547 mixed extension reference corpus remain non-authoritative for full R_mix341; /549 demonstrates two separate accepted checkers do not compose into a unified dispatcher.

External primary grounding: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, J. Symbolic Logic 44 (1979) 36-50, DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis*, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000, DOI 10.1007/10722167_15; Nordstr\u00f6m and H\u00e5stad, *Towards an Optimal Separation of Space and Length in Resolution*, Theory of Computing 9 (2013), DOI 10.4086/toc.2013.v009a014. Separate checker/format repositories `meelgroup/frat-xor` and `tanyongkiam/cake_lpr` were checked as external precedents, not historical-R_mix341 specifications. Required `konard/p-vs-np` and `blkph0x/p-vs-np-proof-research` were reviewed through their prior pinned method/status evidence. No literature source authenticates an absent historical mixed-rule transition.

## Handoff / proof status

Published executable: `experiments/arc/lspv2_598_native386_lazy_source_replayer.cjs`; byte-exact positive/negative packet hashes and original-CLI result ledger: `results/raw/arc/2026-11-13_0512_LSPV2_598_LAZY_SOURCE_OS_RAW.json`; the complete source, seeds and 14 emitted packets are bundled separately as a reproducibility ZIP. Full exact original checker is included in ZIP but not relabeled authoritative for R_mix341.

**ADOPTED:** source/DEF topological scheduling as a legal restricted transition, independent source-binding preflight, once-paid bank, immutable signed dependency identities. **REJECTED:** pre-RES mandatory full SOURCE or DEF prefix as an invariant of chronological native acceptance. **UNCHANGED:** full historical unknown operations and all existing proof weights; none retired.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root proof tracker or `main.tex` modified because this is a restricted native regression rather than a material change to a load-bearing proof node. All five designated hourly Pacific Time automations were verified enabled, original titles, identities, ownership boundaries and historical Route A/B labels unchanged; no automation was created or modified.

**P2-D1, full P2-C3, P2-B1, and separate P2-B2/B3 remain OPEN. P versus NP remains OPEN.** Next decisive evidence: a single authoritative unified source-bound mixed-rule checker validating RES-to-AND3 or paid DEF-to-LOCAL-CONVERT, plus rejected wrong signed-port controls.