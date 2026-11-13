# LSPV-1/623: Constant-work accepted certificates force linear raw-byte validation probes

**November 13, 2026, 10:00 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED (exact query-model theorem) + COMPUTATIONAL | P versus NP OPEN**

**Affected IDs:** [P2-L1-623] strengthens the resource-accounting boundary of [P2-L1-622], [P2-D3] and the incomplete abstraction [P2-C3]. It does not change OPEN [P2-D1], [P2-C3], [P2-B1], separately [P2-B2/B3], or [P1-01/03/04].

## IDEA: one candidate and four falsifiers

Candidate: on the same archived /386 accepted packet with frozen source, paid-node identities, paid work W=32 and exactly 50 proof records, every correct exact raw-byte checker needs a number of individual byte reads linear in a zero-padded JSON exponent.

F1. Replace any exponent zero with ASCII x and the full original checker still accepts. Excluded symbolically: such a token is invalid JSON; the original checker begins by JSON.parse of its input. Tested on 134 spaced, boundary and midpoint positions of the actual accepted 68,692-byte packet; all invalid.

F2. Positive exponent padding changes parsed SOURCE charge or proof DAG. Excluded: parsing 1e+000... produces the exact Number 1; the authenticated pinned packet parses to 50 records, paid work 32.

F3. A checker can skip one sensitive byte yet reject its same-length malformed neighbor without any byte oracle or trusted prevalidated digest. Excluded by deterministic indistinguishability and randomized coupling below.

F4. A promise of syntactically valid inputs, trusted hash, word-parallel read, or out-of-band canonical parsed AST invalidates the asserted query model. Boundary retained: the theorem is about an exact checker on raw bytes with unit-cost individual byte probes and all same-length neighbor inputs. A promise excluding malformed JSON or a preverified AST changes the input domain and must charge the cost of establishing the promise.

## Authority, corpus and novelty boundary

Original accepted artifact: results/raw/arc/2026-11-13_0900_LSPV1_622_K65536_NATIVE386_ACCEPTED.json, Git blob 2a26fc9eeb78673b14bcfc69dc82e0308aa022ef, 68,692 bytes. Unchanged archived verifier: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986.

LSPV-1/622 already established the unbounded raw lexical fiber at fixed W and record count, with hosted-original-body acceptance controls. The present incremental claim is the *raw-input validation query lower bound*, obtained by a standard adversary/coupling technique, not an original invention of decision-tree sensitivity. The /386 verifier recognizes only the restricted SOURCE/DEF/RES dialect and cannot authenticate a single full R_mix341 RES-to-AND3, paid DEF-to-LOCAL-CONVERT, CASE, join, weakening or discharge transition. The original checker starts with JSON.parse(fs.readFileSync(...)); malformed JSON is rejected before semantic rule checking.

## THEOREM 623.1: deterministic and randomized raw-input query barrier

For each integer k>=0, let b_k be the LSPV-1/622 /386 accepted proof packet in which the first numeric SOURCE charge has JSON spelling 1e+ followed by k+1 ASCII zeros. Every other byte is unchanged. Let r=k+1. For each 1<=j<=r, define b_(k,j) by replacing only the j-th such zero with ASCII x, keeping the length fixed.

(i) b_k parses to the same complete proof object: 50 records, W=32 and unchanged original in-packet SOURCE. Subject to implementation limits, the original /386 checker accepts it. Each b_(k,j) is invalid JSON and is rejected by the original checker before inference checking.

(ii) In the standard adaptive byte-query model, every deterministic algorithm deciding the original checker's raw-byte acceptance language on all same-length packets must query every one of the r exponent positions on accepting b_k. Its accepting-run byte-query cost is at least r.

(iii) If a randomized algorithm has two-sided error at most epsilon<1/2 on all such inputs, it makes at least (1-2epsilon)r expected **distinct byte probes on b_k**. For epsilon=1/3 this is r/3.

**Proof.** A positive exponent consisting entirely of zero digits denotes Number 1. Substituting ASCII x for any exponent digit destroys the JSON number production; its following zeros do not repair the syntax. The input length is unchanged, but the checker verdict changes.

If an exact deterministic checker on b_k does not query position j, its observations on b_(k,j) are identical. By induction, the adaptive query sequence and output are identical, so it accepts an invalid JSON neighbor. Contradiction. Thus all r positions are queried.

For a randomized algorithm, couple the computations on b_k and b_(k,j) using the same random tape. Until position j is queried, their observations and outputs coincide. The acceptance probabilities differ by at least 1-2epsilon, so position j must be queried on b_k with probability at least 1-2epsilon. Summing over j by linearity of expectation gives the expected distinct-probe lower bound. QED.

The theorem is for every k in an *unbounded JSON syntax and byte-query model*, not a claim of unbounded available host memory. No charge-free trusted parser, nonuniform answer table or hash oracle is allowed. A machine fetching w bytes per instruction instead has an analogous Omega(r/w) direct-word-read bound. The raw byte-query statement is not a lower bound on the SAT decision runtime in original-CNF length, actual Node wall time, native logical proof work, peak physical RAM, or input-independent solver time.

## Reproducible evidence

1. The complete 68,692-byte original accepted packet was fetched at its Git blob and parsed in hosted V8. It has **65,537 exponent zero positions**, parsed W=32 and exactly 50 proof records. **134/134** same-length single-byte substitutions at stride 509 plus boundary/midpoint positions caused JSON.parse to reject.
2. A separate operating-system Node v22.16.0 experiment exhausted every exponent-zero mutation for synthetic control lengths 1, 2, 16, 128, 1024 and 8192. All **9,363/9,363** malformed mutants were rejected. This was a local parser control, **not** an OS replay of the archived /386 verifier.
3. A standalone reproducible Node script was published to verify the immutable Git blob, original native baseline and three native negative cases, all 134 original-packet JSON mutation samples, and the 9,363 synthetic mutants. The newly published original-checker OS runner has **not** itself been executed in this run.

Artifacts:
- Report: research/agents/lspv-1/2026-11-13_1000_LSPV1_NATIVE386_BYTE_QUERY_BARRIER623.md
- Reproducer: experiments/arc/lspv1_623_native386_byte_probe_barrier.cjs
- Raw: results/raw/arc/2026-11-13_1000_LSPV1_623_BYTE_PROBE_BARRIER_RAW.json

## Primary literature and corpus check

Both root proof trackers were read, including proof2 through its immutable 1,051,196-character Git blob rather than the empty contents-API response; current issue #3 and latest comments; AGENTS.md, CODEX.md and repo skill; the original /341 and /386 checker code; LSPV-1/539, /543, /545, /549, /553, /622; LSPV-3/544, /549, /609 and /608 dispatch handoff; latest LSPV-2/602, LSPV-3/618, LSPV-4/589 and LSPV-5/526 handoffs, plus historical /341 source evidence.

References: [1] Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, DOI 10.2307/2273702. [2] Cousot and Cousot (1977), *Abstract Interpretation*, DOI 10.1145/512950.512973. [3] Buhrman and de Wolf (2002), *Complexity Measures and Decision Tree Complexity: A Survey*, TCS 288:21-43. [4] Clarke et al. (2000), *Counterexample-Guided Abstraction Refinement*, DOI 10.1007/10722167_15. These provide method context only, and cannot authenticate the historical full calculus.

## Proof-chain impact and five-role interface

[P2-D1] OPEN: complete externally bound historical mixed grammar/checker absent. [P2-C3] OPEN: all-rule source-bound alpha/gamma and native cost-sound transformers absent; any quotient on parsed logical work must separately charge raw-byte authentication in physical verifier accounting. [P2-B1] OPEN: no superpolynomial full-calculus optimal proof-DAG lower bound. [P2-B2/B3] separately OPEN: no all-algorithm same-calculus transfer.

LSPV-2 needs an original single-dispatcher genuine mixed accepted record; LSPV-3 must separate raw bytes/parsed AST, owners, provenance and assumptions; LSPV-4 must account for parsing and live actual bytes without conflating W and physical time/space; LSPV-5 should independently OS-run the new reproducer and challenge invalid-neighbor rejection.

**TRACKERS REVIEWED; NO MATERIAL LOAD-BEARING NODE STATUS CHANGE.** No root tracker update is warranted. Existing five roles, two Route A and three Route B, with original identity, titles, schedules, timezone, historical weights and ownership are preserved. Complete project preflight and LaTeX compilation were unavailable in this environment. P versus NP remains OPEN.
