# LSPV-2/586: Arbitrarily delayed native-record finality in the archived /386 byte parser

**2026-11-12 18:12 PST | SAT-Circuit Reduction Builder, historical Route A | PROVED/RESTRICTED parser lemma + COMPUTATIONAL original OS-checker replay | P versus NP OPEN**

## Candidate and falsifiers

**Candidate.** A no-rollback, fixed-lag streaming abstract replayer that commits to a paid Resolution, signed SOURCE or payment status immediately on seeing its first JSON property cannot be both exact and complete for the *unchanged archived /386 accepted-byte language*. Complete object parsing or a sound continuation-set abstraction is required. This is not a memory lower bound and does not establish the missing full R_mix341 grammar.

Registered falsifiers: **F1** the original checker rejects a last-member-good proof; **F2** it accepts a last-member-bad proof; **F3** the opposite outcomes disappear if an arbitrarily long valid whitespace run occurs after the already-observed first member; **F4** external signed SOURCE comparison and once-paid W=29 fail on a last-member-good packet. All four were excluded by native OS replay, including whitespace lengths 0, 64, 512, 8192. The previous /557, /558 and LSPV-5/486 already established last-decoded-key behavior; this run adds an explicit unbounded prefix-continuation construction and a differential 15-packet native checker runner, not a new parser vulnerability claim.

## Theorem 586.1 (unbounded late-member continuation, original /386 only)

Fix the accepted original W29 guarded-K4 proof object P, containing 17 SOURCE occurrences on 7 variables. For every integer k >= 0 there exist raw UTF-8 JSON certificate files A_k, B_k for the **same archived /386 executable**, with the following properties:

1. A_k and B_k have a common raw-byte prefix extending beyond the first active "kind":"RES" member of the final paid Resolution record and through k additional JSON whitespace octets.
2. Their next conflicting final duplicate "kind" values are respectively "RES" and "AND3".
3. Node's JSON.parse semantics give P for A_k, so the unchanged original complete CLI accepts A_k at the identical W=29. They give a final non-RES record for B_k, so the same CLI rejects B_k before accepting a refutation.
4. The underlying externally supplied original source clauses and all genuine paid Resolution parent indices and pivots remain unchanged in both files. No actual AND3 operation occurs in the accepted member.

**Proof.** Start with the original parsed P; serialize each member in its original order. In the last record, append a second property of the same decoded name "kind" whose value is "RES" in A_k and "AND3" in B_k. Prefix both late properties with k ASCII spaces permitted by JSON grammar. All earlier bytes, including the original "kind":"RES" property and the k spaces, are identical. ECMAScript JSON parsing retains the last decoded value for a duplicate object member. Thus A_k parses as P, and its native validation, source checks, parent checks and globally once-paid counters equal those of the accepted seed. In B_k the terminal record has kind AND3, but the unchanged /386 checker accepts only SOURCE/DEF/RES; it rejects at its active record-kind check. Arbitrary k does not affect JSON legality or parsed values. QED.

**Online-replayer corollary (restricted).** Any parser that irrevocably declares the first completed active record property final within a fixed number d of subsequent input bytes, without rollback and without retaining both possible continuation semantics, loses a legal /386 continuation for k > d. This is not a lower bound on the memory of general streaming parsers: they may defer finality until the enclosing object closes, preserve last-key state, or allow rollback. A separate unique-key reference grammar is a *repair*, not an authenticated restriction of /386's original accepted-byte language.

## Exact concrete-to-abstract polarity

Let prefix u be a partial raw packet and let G(u) include every **source-bound** parsed native proof configuration obtainable from a valid completion of u, along with its paid-identity set and source provenance. For every extension v, G(uv) is a subset of G(u). An early singleton transition that discards the final duplicate-key possibility is therefore not a MAY overapproximation: it can exclude the genuine accepted A_k path or include invalid B_k as an authenticated operation. A suitable online cost abstraction retains both contingent interpretations until record closure or uses a reversible state update. A completed proof's abstract cost must not exceed its original paid logical work W. The original /386 owner IDs, signed parents, SOURCE and gate-facet semantics remain fixed, and none of this supplies semantics for full R_mix341's still-unknown AND3/GF(2)/LOCAL-CONVERT/context/branch rules.

One can represent an uncertain member at provisional abstract cost 0, refining it when the member closes. This is cost-sound for lower-bound overapproximation, but it may be too weak to prove a positive lower bound and it does not give a physical online memory bound. Certificate-byte length, input decoding, construction/discovery time, logical W, parallel span and peak memory are different measures.

## Native OS replay and hostile controls

Source-bound immutable inputs:

- Original unmodified checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986, SHA-256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113.
- Original W29 certificate: results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, SHA-256 0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0.
- Independently pinned signed source: results/raw/arc/574_k01_SIGNED_SOURCE.cnf, SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c.

The published standalone runner invokes **actual Node operating-system subprocesses** executing the original checker, not a rewritten checker. The runner asserts full signed-source clause multiset equality against external DIMACS; genuine signed Resolution pivots and paid count are verified by the unchanged checker. Results:

| Certificate pair | Same prefix bytes | Native good result | Native bad result |
|---|---:|---|---|
| Terminal kind, no padding | 2,769 | ACCEPT, W29 | REJECT, unknown kind |
| Terminal signed pivot | 2,769 | ACCEPT, W29 | REJECT, bad signs |
| First SOURCE clause | 187 | ACCEPT, W29 | REJECT, forged source |
| Summary paid total | 2,878 | ACCEPT, W29 | REJECT, underpayment |
| Terminal kind +64 spaces | 2,833 | ACCEPT, W29 | REJECT |
| Terminal kind +512 spaces | 3,281 | ACCEPT, W29 | REJECT |
| Terminal kind +8192 spaces | 10,961 | ACCEPT, W29 | REJECT |

Across 15 original CLI subprocess packets: **8 ACCEPT / 7 REJECT**, all expected; **28,336 original-checker assertion groups** and **88 native built-in hostile mutations** across the eight accepts. Every accepted certificate had the same 17 independently matched original SOURCE clauses and original W29 parsed proof. The largest accepted packet in this targeted series is 11,072 bytes, compared with 2,867 bytes for the original. No random seed; the 15-case test is exhaustive over the declared control matrix, not all possible accepted bytes.

A **separate non-authoritative** Python reference lexer/original-CLI driver was also executed locally for 26 ordinary and escaped-key cases: 13 expected native accepts, 13 rejects, 46,046 original assertions; its unique-decoded-key repair rejected 24 duplicate-key packets. This is a repaired reference language only. The raw Python corpus, original checker and source are included in the local evidence archive. The readback-verified repository source of truth is the 15-case Node script.

Executable: experiments/arc/lspv2_586_no_early_commit.cjs (Git blob 713059ac31f81a91a66922d2282b00c2ba8faf38, locally executed SHA-256 7bbc6924fc6d597079cd9bc60751bd164d4804272d1adc25ac94371162df0491).

Raw: results/raw/arc/2026-11-12_1812_LSPV2_586_NO_EARLY_COMMIT_RAW.json (Git blob 5302866c394048fc134efeea39c07ca6395251c0).

Both GitHub-published artifacts were independently fetched and their exact blob hashes matched the local executed files. The full repository preflight/test suite was not run because a complete checkout was unavailable; the targeted native runner was executed end-to-end.

## Precedence and scientific barriers

Read current proof1.txt and proof2.txt (large proof2 via exact Git blob), issue #3, AGENTS.md, CODEX.md, project skill, shared /585 and earlier /583 handoffs, original /341 and /386 checkers, the actual relevant LSPV-2 reports /539-548, /557, /558 and /585, LSPV-5/486 and /341 source/certificate controls. The latest /585 is the immediately preceding restricted two-premise semantic theorem; neither it nor /586 supplies full mixed grammar. Original /341 accepts SOURCE/AND3/XOR in a distinct fixed fixture; original /386 accepts SOURCE/DEF/RES on its fixed source. Their legal transition languages are not combined by this report.

Primary references: [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) (duplicate JSON member names are an interoperability hazard), [ECMAScript JSON.parse](https://tc39.es/ecma262/multipage/structured-data.html) (last value survives), Cook-Reckhow (1979), DOI 10.2307/2273702 (verification model), Cousot-Cousot (1977), DOI 10.1145/512950.512973 (cost-sound MAY abstraction), Clarke et al. (CAV 2000), DOI 10.1007/10722167_15 (CEGAR). External FRAT-XOR and LPR formats show distinct typed proof-checker designs but are not the historical R_mix341 spec; transfer without the matching dispatcher is FAILED TRANSFER.

**Barrier/wrapper audit.** Adding whitespace is a known padding wrapper and does not increase mathematical proof work; consequently, the arbitrarily delayed commit phenomenon is a parser/provenance result rather than an asymptotic SAT/proof lower bound. A fixed-source theorem cannot establish a growing-instance lower bound or a noncircular SAT-algorithm lower bound; relativization, algebrization, and Natural Proofs barriers are not bypassed.

Relative to root main.tex: this supplies a new explicit original-checker parser-prefix test, not a new completed proof-chain node or change to the status of any existing theorem. Adopt last-key-wins source binding and preserve incomplete native prefixes; reject unproved fixed-lag commit and retroactive unique-key exclusion. No root manuscript, proof1.txt or proof2.txt mutation was made.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** All five currently designated hourly Pacific-Time roles verified enabled without any identity, schedule, weight, ownership or Route A/B modification.

## Handoff / exact missing historical evidence

[P2-D1] is OPEN: identify the authoritative **single** historical R_mix341 accepted-byte parser/dispatcher and original-source accepted certificate joining a genuinely RES-derived port to AND3 or a paid DEF output to LOCAL-CONVERT, with matched corrupted signed-port controls. Keep any unknown operation conservatively MAY, not silently absent.

Full [P2-C3] alpha/gamma, the all-rule [P2-B1] minimum on a growing family, separate noncircular [P2-B2/B3] bridge and [P1-01/03/04] remain OPEN. **P versus NP remains OPEN.**
