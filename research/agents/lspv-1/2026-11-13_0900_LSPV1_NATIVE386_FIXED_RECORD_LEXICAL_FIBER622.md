# LSPV-1/622: Constant-record original /386 acceptance has arbitrarily long JSON numeric lexemes

**13 November 2026 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED source-level theorem + COMPUTATIONAL original-body replay | P versus NP OPEN**

**Affected IDs:** [P2-L1-622] supplies restricted accepted-byte evidence for [P2-D1] and a cost/resource firewall for [P2-C3]. These remain OPEN, as do [P2-B1], separate [P2-B2/B3] and [P1-01/03/04].

## Candidate theorem and four prespecified falsifiers

Candidate: even fixing the whole parsed original-source shared DAG, all paid identities, logical work and the number of records, the unbounded ECMAScript JSON numeric grammar permits arbitrarily long distinct representations of a single accepted /386 proof. This requires no new free facets or paid nodes. A particular V8 process nevertheless has finite string and RAM limits.

F1: positive-exponent zero padding is invalid JSON or parses differently. F2: original checker acceptance depends on raw bytes or a raw SHA gate. F3: a numeric alias changes source, parents, paid owner or terminal, or the original checker rejects it or fails its internal corruption checks. F4: this works only in a replacement/canonical checker, not the original source body. Source inspection and full hosted original-body replay address the four falsifiers within the scoped fragment.

## Exact authority and prior work

Archived checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986, SHA-256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113.

Accepted K4 seed: results/raw/arc/2026-11-13_0812_LSPV2_601_W32_NATIVE386_SEED.json, Git blob 3a2f40d09b03089e8c86ce2ff2619ad83fbb8e5e. Its 3153 bytes contain 17 signed SOURCE records, one globally paid conservative gate owner, two genuine free DEF facet records, 31 paid Resolution records, 50 records total and a terminal empty clause. Its exact W=32.

This original source first reads file content and JSON.parse(content), then validates the parsed object through checkProof. It computes SHA-256(content) for diagnostic output only, not as an acceptance predicate. All built-in hostile mutations act on clones of the parsed object.

Novelty boundary: LSPV-3/616 already proved finite /386 numeric lexeme equivalences. LSPV-5/526 gives separate /341 numeric aliases, LSPV-5/525 duplicate JSON members. LSPV-1/621 establishes unbounded raw-record action languages via *additional zero-cost facets*. The new result establishes an unbounded byte-string fiber **without any additional proof record or semantic change**, at fixed W and fixed original parsed DAG.

## Theorem 622.1: constant-W, constant-record lexical fiber

Let b be the canonical 3153-byte K4 packet. Let b_k for integer k >= 0 be the byte string formed by replacing the single JSON substring

    "charge":[1,0,0,0]

with

    "charge":[1e+00...0,0,0,0]

where the exponent consists of exactly k+1 zero digits. Then:

* In the ideal ECMAScript JSON grammar allowing arbitrary finite input strings, JSON.parse(b_k) equals JSON.parse(b) as a complete JavaScript object for every finite k.
* Whenever an operational checker can allocate and parse b_k, its entire original checkProof run and marginal logical work are identical. Every b_k ACCEPTs with W=32, 50 proof records, one paid gate owner and 31 Resolution nodes.
* The raw packets are pairwise distinct, with exact byte lengths **|b_k|=3156+k**.

Therefore, in the unbounded syntax model, there is no finite function f(W, number_of_records) upper-bounding accepted-byte length even when the whole parsed graph and cost are frozen. This is *not* a claim that a finite real V8 engine accepts every k beyond its implementation limits.

**Proof.** JSON numeric syntax permits a plus-signed exponent with arbitrarily many leading zeros. The Number denoted by 1e+00...0 is exactly 1. Every other byte of b_k equals b, hence the complete parsed object equals the original. Inspection of the complete archived verifier proves its source/rule/paid/goal decisions depend only on that parsed object; the original raw SHA is printed afterward and does not determine acceptance. Consequently the paid ledger and all rule checks agree. Changing one byte "1" to the four bytes "1e+0" plus k further zeros increases length by exactly k+3, giving 3156+k. QED in the declared syntax/operation model.

**P2-C3 implication:** A quotient by the full parsed proof state is exact for this lexical fiber's native legal rules, accepting terminal and W, but not exact for raw bytes, SHA, parsing time, bandwidth or memory. Raw caller-source digest authentication must retain and check the original bytes or explicitly install a separately proved canonicalization layer. Requiring canonical numeric syntax would be a **new frontend**, not an authenticated restriction of the historical checker.

## Verified computational certificate

The unchanged original pinned /386 checker body was executed in hosted V8 with file-read/crypto-output/console/structuredClone adapters. Only its diagnostic SHA output was stubbed. All original checkProof rule checks and all eleven original hostile mutations per accepted packet executed unmodified.

**14/14 accepted variants** for k=0,1,2,4,8,16,32,64,128,256,1024,4096,16384,65536. Every variant has W=32, 50 records, exactly 3460 original assertion groups and 11/11 internally rejected corruptions. Largest packet: **68,692 bytes**, Git blob 2a26fc9eeb78673b14bcfc69dc82e0308aa022ef, completely reread and parsed identically to the 3153-byte seed.

**7/7 hostile variants rejected:** "1e+" (incomplete exponent); "01" (invalid JSON leading zero); quoted string charge; "1e+309" (Infinity); "-1e+000" (wrong charge); "0e+000" (even parity); and "1e+000a" (invalid suffix). Invalid syntax and semantic charge failures were distinguished.

Published complete raw hosted-V8 ledger:
results/raw/arc/2026-11-13_0900_LSPV1_622_NATIVE386_EXPONENT_FIBER_HOSTED_RAW.json (Git blob d3ca39f9b4637240cf445dc04c77d4897de5affa).

Complete deterministic k=65536 accepted byte packet:
results/raw/arc/2026-11-13_0900_LSPV1_622_K65536_NATIVE386_ACCEPTED.json.

Pinned original-checker operating-system Node.js reproducer:
experiments/arc/lspv1_622_native386_numeric_exponent_fiber.cjs (Git blob 68c29a4c891b153707315ec42f51076b18561d19).
The published standalone OS runner was **not** independently executed in this run; operational evidence consists of original-body hosted-V8 execution. The report does not claim that the SHA adapter reproduced the real checksum.

## Dependency, status, and barrier audit

[P2-D1] **OPEN**: this is only the actual SOURCE/DEF/RES /386 byte language, not an authenticated single-dispatcher full R_mix341; the /341 SOURCE/AND3/GF(2) checker is distinct and may accept semantically false refutations. No original source-bound RES-to-AND3, paid DEF-to-LOCAL-CONVERT, branching, context discharge, joins, deletion, exported/private wires or exact cross-rule tariff is proved by this result.

[P2-C3] **OPEN**: a full cost-sound MAY transformer remains unconstructed. A lexical quotient for *logical cost* is allowed, but unbounded evidence length and parsing cannot be inferred from W. [P2-B1] **OPEN**: no superpolynomial lower bound. [P2-B2/B3] **OPEN** and separate: no noncircular same-calculus SAT-decision-to-proof-size transfer. P versus NP OPEN.

The theorem neither uses nor claims a relativizing oracle, algebrization, a Natural Proofs property or a hard-instance machine lower bound. Ideal grammar versus finite V8 resource limits are explicitly separated. Logical W, number of records, evidence bits, verification, discovery, actual time, span and peak memory remain separate quantities. LSPV-5 independent OS red-team remains pending.

## Corpus, original literature and handoff

Read root proof1.txt blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and proof2.txt blob 930c5eeddafce656717f28055a7a9a755f44737c (second through Git blob API because >1 MB Contents endpoint was blank), issue #3 and newest comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, November 9 abstraction handoff, original historical LSPV-2/341 and LSPV-5/413 scope report, actual LSPV-1/539, /549, /586, /621; LSPV-2/549, /601; LSPV-3/549, /616; LSPV-4/549; LSPV-5/525 handoff and /526 issue evidence. Checked current main.tex via Git blob, including exact LSPV-1 ownership markers, and searched duplicate lexeme and mixed checker work. All earlier scope limitations retained.

Primary references queried: Cook & Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1):36-50 (1979), https://doi.org/10.2307/2273702; Cousot & Cousot, *Abstract Interpretation*, POPL (1977), https://doi.org/10.1145/512950.512973; Giacobazzi, Ranzato & Scozzari, *Making Abstract Interpretations Complete*, JACM 47(2):361-416 (2000), https://doi.org/10.1145/333979.333989. These provide methodological scope only; no outside paper authenticates historical source bytes.

**Adopted:** authenticated original /386 seed/checker, earlier /616 lexical equivalence, /621 work-only-versus-raw-action distinction. **New:** exact constant-node lexical-length relation, original-body 21-case regression and complete large accepted packet. **Rejected:** W plus node count as an automatic upper bound on evidence bytes. Both root trackers unchanged because no load-bearing proof-chain status changed: **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

LSPV-2 Route A: seek one actual single-dispatcher mixed cross-rule acceptance and test native lexeme behavior. LSPV-3 Route B: keep byte identity, parsed identity, source, provenance, full shared DAG, original assumptions and paid identity distinct in alpha/gamma. LSPV-4 Route A: charge raw parsing/verification time and peak space independently. LSPV-5 Route B: independently OS replay large k and attack the ideal-grammar/real-memory distinction. LSPV-1 Route B: maintain P2-D1 -> P2-C3 -> P2-B1 quantifiers; P2-B2/B3 remain separate.

All five designated PNP automations were independently found enabled on the original Pacific hourly schedules with exactly two Route A and three Route B. None was created, renamed, updated or rescheduled. Local repo preflight, report checker, LaTeX compilation and independent OS Node replay were unavailable without a complete local checkout. **P versus NP remains OPEN.**
