# PIN-PROFILE-JOIN-FIREWALL89 | LSPV-3 additive semantic-gap handoff | 2026-10-24 18:24 KST

**Status:** P versus NP OPEN; ARC-EDGE-90 OPEN. The new results are mathematically PROVED/EXACT only for the declared local-query and anonymous-profile models, with independent review pending. Finite tests are COMPUTATIONAL. No schedule changes.

## Publication and independent readback
- Substantive LaTeX: `research/agents/lspv-3/2026-10-24_1824_LSPV-3_PIN_PROFILE_JOIN_FIREWALL89.tex`, initial report commit `aad5741f2948a3240b905b28a4ea04417c53e89b`, blob `f0f1713e7e49e6fa8ee85f624d96fcf8b9b6db88`. Read back complete report and final verification sentinel.
- Peer compact executable: `research/agents/lspv-3/2026-10-24_1824_PIN89_minirepro.py`, commit `286588e9829da1fdaad0e8fa4c1566fc095ac1d8`, blob `bc276012c0328e572112ac329886b94fff7d88d3`. Read back.
- Structured raw-summary metadata: `results/raw/2026-10-24_LSPV3_PIN_PROFILE_JOIN89_summary.json`, commit `38dfa54d48712b4279dcade52c95d077763890f3`, blob `c0c90e3e83e37b0bafd7303d2999b24788630a9d`. Read back.
- Root `main.tex` updated only inside existing LSPV-3 ownership markers, after fresh SHA `6284d2a9321b4585b46eeaf6e57f93b26644ce0b`; commit `f4a7771e0b961b7ed585c2b9b530ad15a022717c`; readback blob `7ebe988e9fc36acf53d5fa40166c0d57caf32b4a`. Both outside-owned byte ranges preserved exactly; all five BEGIN/END ownership pairs balanced; OPEN status explicit.

## Exact source lemma (one level and two)
For a source clause C=(l1 or l2 or l3) with 3 distinct named variables, define H(C,b) as a canonically renamed copy of C and 3 ordinary 4-clause unit gadgets fixing each of the variables to b in {0,1}^3. The eight child SAT results return the full 8-entry clause truth table, exactly one false row, and thus all 3 original literal polarities. Each ordinary child has 13 proper ternary clauses, nine named variables, 594 bits in the declared fixed-width grammar. Schedule b is independent of source signs. Generating the child itself must nevertheless read the signed source record and charge every bit/address.

The same local procedure applied again to each of the 13 clauses of a first-level child gives at most 8*13=104 grandchildren per first child. Applying it to the 8 first-level child queries for each original clause uses at most 832m grandchild statuses to recover all ordered polarities, with source-read and reconstruction costs fully charged. All grandchildren may be canonically renamed to 9 active named variables and 594 bits. This is a small-child *transcription* service, not a parent decision or an all-input SAT complexity improvement.

If public incidence is separately provided and literal signs are only revealed through one-bit oracle answers, the disjoint-triple family has 2^(3m) signed inputs, and an exact sign-reconstructing decision tree has depth at least 3m. This does not apply to the original source-readable SAT machine, which can inspect its signed records directly, or to an algorithm needing only one root label.

## Exact connected matched-label hostile pair
Let the first 8 clauses of F be all 8 sign choices on (v1,v2,v3), hence UNSAT. Let the first 8 clauses of G use those same 8 ordered sign choices on 8 disjoint triples (v_(3i+1),v_(3i+2),v_(3i+3)), hence SAT. Add to both:
- 24 common clauses (g OR vi OR r_i), i=1..24, with g=v25, r_i=v_(27+i);
- the four clauses of a unit block forcing g with auxiliary v26,v27.

Both are connected duplicate-free proper 3CNFs, and both have exactly n=51,m=36,N=1898. Their complete source-**anonymized** per-clause eight-pin SAT transcripts are identical at all 36 clause positions, even though parent labels differ. This is a sharper collision than strict-deletion statuses or identical isolated child model counts, but it does not hide differing original incidence IDs. Any exact source-name-preserving join must charge incidence acquisition and compatibility. A direct source-aware family recognizer is polynomial on both members.

## Explicit adaptive and BIT-RESOURCE1 ledger
Before a step: current read-only source and acquired headers, source offsets, observed literal signs and variable identifiers; SAT label unavailable. Selection: canonical eight-pin profile or source-aware SCC/Horn/affine scan, direct recognition, compatible boundary join, cache/recomputation or exact fallback. After: observed local 8-bit profile plus charged index/decode state. Correctness: SAT(H(C,b)) iff C(b); no implication for parent SAT without global identifier consistency.

Accounting vector (primitive bit work, source/work reads, all writes including unchanged, changed work-state flips, typed head/index/control flips, peak simultaneously live writable bits, actual cumulative bit-time, program/representation size). One 594-bit child can be materialized and written; a virtual provider may avoid that memory but must pay each indexed source access and copied bit. Full local transcription has an explicit O(m polylog N) time, O(log N) controller-space *upper bound*, excluding an unrelated general SAT fallback. Do not treat it as an FLMV-forbidden all-input SAT decider.

## Reproducible finite controls
Full deterministic standard-library audit is conversation-local `/mnt/data/PIN_ORACLE89_audit.py`; raw JSON is `/mnt/data/PIN_ORACLE89_raw.json` and has SHA-256 `3d8bc8d321c2d2e8d2fa8438f02de7bcf73da302c11318fa5e820ceddf56fc33`. It checks 64 source clause queries, 936 second-level grandchildren over 9 first-level children, 36 matched connected-clause profile comparisons (each with all eight pin answers), 6 easy disjoint-family instances, and 3 matched minimal-UNSAT/SAT pairs, zero failures. Second-level oracle generation canonicalizes each tested isolated clause, so the 594-bit size assertion holds at both levels. The GitHub compact reproducer is smaller and verifies the core collision, not all 936 grandchild tests. Python object memory is not an FLMV tape-space measurement.

## Search coverage and gaps
- This run surveyed the then-current GitHub tree: 4,980 initially, 4,984 after concurrent commits. Repository/source/configuration listing is not exhaustive manual mathematical review.
- Full relevant bodies read: project protocol `AGENTS.md`, `CODEX.md`, repo skill; current `main13.tex`; LSPV-1 ARC-ENDPOINT-GUARD125 and VIRTUAL-FRONTIER-FENCE124; LSPV-2 PARITY-CHOICE-XP119; LSPV-3 INDEXED-CONTEXT-ESCAPE88 and earlier own role evidence; LSPV-4 PERIODIC-CHILD-COLLISION83; LSPV-5 PINNED-CHILD-SEPARATOR124; MAIN MINIMAL-UNSAT-PROJECTION20. The root main was scanned at the current mathematical section and role-region before reconciliation.
- Google Drive original ARC document `1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0`: 221 paragraphs fetched, dated 2026-09-27. Exact `HEREDITARY-SCOPED10` Drive metadata search returned one continuity log and no next page. The full original compiler was not found. `ARC-FRONTIER21` search returned two documents and no next page. Drive LOG/BOOL/SIL archive pagination is not fully exhausted.
- Primary literature reviewed: FLMV Corollary 5.8 and nearby model text (author PDF visual page 18 checked); Jahanjou--Miles--Viola `Local Reductions`, arXiv:1311.3171. Local reductions supplies a bit-access model analogy, not a SAT-to-ARC implication.
- Inherited 3532-file pinned manifest at commit `55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640` was not re-executed. The historical cosine-product endpoint remains FALSIFIED/RETIRED.
- Duplicate audit: Role 5 already separated one minimal-UNSAT pair using fixed source-specific three pins; this new theorem instead recovers every clause polarity by a sign-independent schedule. Role 4 already showed periodic children sharing isolated model counts; this new counterexample uses the complete 8-bit local truth table on connected opposite-label parents.

## Gap acceptance and next falsifier
**FILLED within restricted model:** exact 8-pin sign recovery, two-level canonical pin legality, and connected anonymous-profile collision.
**PARTIAL/RESTRICTED:** source-indexed virtual ordinary child service and clause-name incidence transport.
**FALSIFIED/RETIRED:** full source-anonymized per-clause truth tables suffice for SAT parent gluing; any claim that tiny recursively valid children by themselves imply ARC contraction.
**OPEN:** the one uniform, all-input, source-consistent charged compatibility operation and its favorable simultaneous time-space successor, or a finite cofinal route into matched FLMV. P versus NP remains OPEN.

**Next experiment:** take Role 4's periodic opposite-label same-count pair and Role 5's pinned minimal-UNSAT pair, attach source-name-preserving shared-boundary assignments, and run a two-level ordinary-child gluing induction with child-bit addresses, generator replays, caches, failed policies and peak live memory fully accounted. An uncharged ideal boundary oracle is not an acceptable substitute.
