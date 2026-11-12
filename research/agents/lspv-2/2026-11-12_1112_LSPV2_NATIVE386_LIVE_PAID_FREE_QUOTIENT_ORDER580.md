# LSPV-2/580: Genuine shared-DAG noncommutativity of free-facet and paid-Resolution quotients

**November 12, 2026, 11:12 a.m. PST | LSPV-2 SAT-Circuit Reduction Builder | Historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## One candidate and four falsifiers

**Candidate [P2-D1/P2-C3]:** In the unchanged, source-bound archived /386 SOURCE/DEF/RES proof calculus, the order of two individually cost-sound normalizers matters. Canonicalize zero-extra-cost defining facets first, then identical paid Resolution inferences; compare against Resolution-first normalization. Construct a single genuinely terminal-live shared-DAG refutation where the forward order merges two paid inferences but the reverse single-pass order merges none.

- **F1:** At least one purportedly duplicated paid or free record is outside the final empty-clause ancestor cone.
- **F2:** Signed gate facets, exact pivots, chronological parent indices or original signed SOURCE occurrences prevent native acceptance.
- **F3:** DEF-first and RES-first single sweeps produce the same cost and paid sharing.
- **F4:** Forged SOURCE, invalid facet, undercharged payment, forward parent or wrong signed pivot passes native verification.

The symbolic construction refutes F1 and F3 within the declared sibling calculus. Actual unchanged /386 full-CLI replays accept all five positive variants and reject all five hostile corruptions, addressing F2 and F4 for this finite corpus.

## Source and checker authority

The original archived checker is `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`, SHA-256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`. It is executed unchanged in separate Node.js operating-system processes, including its complete eleven-test CLI self-check wrapper. Original signed guarded K4 SOURCE: `results/raw/arc/574_k01_SIGNED_SOURCE.cnf`, SHA-256 `3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c`, 215 bytes and 17 exact signed original clause occurrences. The original accepted K4 W29 seed is `results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json` (SHA-256 `0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0`).

Distinct archival checker `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, checks a *different* SOURCE/AND3/XOR fixture grammar. These implementations cannot be composed into an authoritative full historical R_mix341 checker. In particular, RES-to-AND3, paid DEF-to-LOCAL-CONVERT, contexts, branching, weakening, discharge, joins, deletion, exported/private wires and any additional fixed charges remain **unrecovered and conservatively possible**.

## Explicit construction, all added proof records terminal-live

Start from the unchanged W29 signed guarded K4 refutation: 17 SOURCE records, 28 oriented paid RES records and one paid conservative gate owner `[0,8,1,4]` representing `z8=x1 AND x4`. Original SOURCE record 7 is the exact clause `S=[-1,-4,-5,-7]`; the original proof contains two different terminal-live uses of that same record.

Insert immediately after all SOURCE records these seven typed records. The three `DEF` views are zero-extra-paid facets of the *already charged* owner zero:

| New record | Kind | Exact signed clause | Exact ports |
| --- | --- | --- | --- |
| 17 | DEF | `[1,-8]` | owner 0 |
| 18 | DEF | `[1,-8]` | owner 0, identical copy |
| 19 | DEF | `[-1,-4,8]` | owner 0 |
| 20 | RES | `[-4,-5,-7,-8]` | parents [7,17], pivot -1 |
| 21 | RES | `[-4,-5,-7,-8]` | parents [7,18], pivot -1 |
| 22 | RES | `[-1,-4,-5,-7]` | parents [20,19], pivot -8 |
| 23 | RES | `[-1,-4,-5,-7]` | parents [21,19], pivot -8 |

Redirect the two original uses of SOURCE record 7 to record 22 and record 23, respectively. Increment subsequent parent indices by seven. Every added record 17 through 23 is in the terminal empty-clause ancestry, including both duplicate facets and all four paid RES steps. The entire exact original signed SOURCE set and the existing gate bank are unchanged. The original full CLI accepts this **W33, 52-record, 3262-byte** certificate.

## Theorem 580.1, strictly noncommuting cost-sound quotient passes (PROVED/RESTRICTED)

In the explicitly pinned /386 calculus, define `F` as a left-to-right duplicate `DEF` pass keyed by (native owner identity, exact signed canonical facet), redirecting all later dependent parent ports to the earliest existing matching facet. Define `R` as a left-to-right duplicate paid `RES` pass keyed by (already-remapped ordered parent identities, signed pivot, exact signed conclusion), also redirecting later uses to the earliest matching RES. Keep all SOURCE occurrences, the original gate-owner bank and chronological inference order; recompute exact native summary fields on each pass.

Both passes preserve native mathematical acceptance on their specified domains. `F` preserves paid work; `R` reduces it by exactly the number of eliminated paid RES identities. They are cost-nonincreasing and preserve the terminal empty clause. The underlying individual transformations were established by LSPV-2/579 (DEF) and /561 (RES); those results are explicitly credited, rather than reclaimed.

**New concrete counterexample.** On the terminal-live packet `P` above:
```
R(P)     : 0 paid RES rows removed
F(R(P))  : 1 free DEF row removed; W remains 33
F(P)     : 1 free DEF row removed; W remains 33
R(F(P))  : 2 paid RES rows removed; W falls to 31
```
Thus `F(R(P))` and `R(F(P))` are different native-accepted normal forms, with a strict **two-paid-unit** cost gap. Neither quotient loses a legal proof; rather, one syntactic rewrite *enables* further identical paid signatures. An abstraction that first merges paid nodes and assumes a single pass is complete can miss genuinely permitted cheaper concrete paths.

**Proof.** Records 17 and 18 have identical owner and signed facet and are both parent-eligible. After `F`, record 21's old parent 18 becomes the earlier 17; hence old records 20 and 21 have identical ordered parent indices, pivot and signed conclusion. `R` then identifies them and redirects old record 23's dependency to old record 20. Consequently old records 22 and 23 also have identical ordered parent indices and identical pivot/conclusion, so `R` identifies them in the same chronological sweep. All rewrites redirect to strictly earlier records; every oriented signed RES check is unchanged and no source, paid owner, gate freshness condition or final contradiction is removed. In the reverse order, old records 20 and 21 have distinct parent identities (17 versus 18); old records 22 and 23 likewise differ. Thus `R` initially removes no paid row, and the subsequent one-time `F` removes the duplicate facet but does not revisit the newly equal paid signatures. The distinct work counts are as stated. The original full CLI accepts all four constructions, independently confirming wrapper compatibility for this witness. QED.

**Important qualification:** This is a noncommutation result for **single sweeps**, not a claim that a fixed-point rewrite system cannot eventually converge or that the forward order is universally optimal. Repeat fair cost-decreasing passes to saturation if the chosen abstraction seeks a normal form. Even W31 is *not* a minimum refutation of this source: the pre-existing W29 certificate remains accepted under free optimal proof choice.

## Actual original operating-system verification

The executable `experiments/arc/lspv2_580_joint_paid_free_cegar.cjs` is published at Git blob `8065cfbe815cfff8df8e23c72b5ba1f2b9368982`. It is a separate **constructor, reference transformer and differential replayer, not an authoritative checker**. The executed byte-identical published code regenerates the original signed SOURCE corpus, checks its SHA-256, constructs the terminal-live dependency DAG, invokes the unchanged archived checker in OS subprocesses for each packet, checks the expected verdicts and writes complete native JSON packets plus a raw manifest.

| Candidate | Native full CLI | W | Records | Bytes |
| --- | :---: | ---: | ---: | ---: |
| Original unchanged seed | ACCEPT | 29 | 45 | 2867 |
| Fully terminal-live added two-path proof | ACCEPT | 33 | 52 | 3262 |
| Paid RES then free DEF quotient | ACCEPT | 33 | 51 | 3214 |
| Free DEF quotient only | ACCEPT | 33 | 51 | 3214 |
| Free DEF then paid RES quotient | ACCEPT | 31 | 49 | 3091 |
| Five hostile corruptions | REJECT | not valid | | |

All **five accepted** cases passed the checker's full eleven negative-test subchecks each, and together ran **17,796 original assertion groups and 55 built-in negative controls**. Five hostile exact packets were rejected: bad signed DEF facet, underpaid summary, illegal forward RES parent, reversed incorrect pivot and signed original SOURCE forgery. Raw per-packet hashes, checker verdicts and resource fields: `results/raw/arc/2026-11-12_1112_LSPV2_580_JOINT_QUOTIENT_NATIVE_OS_COMPACT.json`. Exact published native-accepted witness bytes: `results/raw/arc/580_LIVE_TWO_BRANCHES_W33.json` (Git blob `1879118e4e4f4244961f75f62e6207da67f0f345`) and `results/raw/arc/580_DEF_THEN_RES_W31.json` (Git blob `6b2c343ab68634767b87bf0f7bce771529cb0c41`).

## Abstract transformer, CEGAR, and distinct resources

Concrete /386 state records source bytes/hash, signed source occurrence IDs, gate-owner table and fresh wire IDs, individual zero-extra-cost DEF view identities, paid RES node identity, oriented ports, chronological dependencies and terminal ancestor closure. A source-bound MAY abstraction retaining this information admits both legal transformation orders. Collapsing DEF-equivalent states before testing paid-node congruence reveals an additional lower-cost path. Conversely, a path that redirects a parent to a forward row, changes an owner or changes a signed clause is spurious and fails native replay; refine that path without excluding actual zero-cost duplicate views. Shared paid identities are counted once **per distinct actual retained node**, never per syntactically same clause alone.

Logical work is 33 versus 31 versus the pre-existing 29; witness length is 3262 versus 3091 bytes; source acquisition remains 215 bytes. Proof construction time, normalizer/replayer time, native checker time, dependency span, and simultaneous peak memory are separate ledgers. No native deterministic machine upper/lower-bound exponents are inferred. Branch AND obligations, assumption discharge and unrecognized full-calculus rules must be MAY-overapproximated, not silently excluded.

## CORPUS REVIEWED, duplicate/contradiction audit, and implication limits

Reviewed both live trackers `proof1.txt` and `proof2.txt` (P versus NP OPEN), issue #3, AGENTS.md, CODEX.md, `.codex/skills/pnp-research/SKILL.md`, live root `main.tex`, /341 producer/verifier, /386 original checker, recent LSPV-2/539–549, /552, /560–563, /573, /579 and recent five-role handoffs; pertinent LSPV-1/576 and LSPV-3/510–511, plus historical original calculus declaration and repository search. Prior /561 and /579 already contain the **individual** quotient theorems; new material is the **strict, terminal-live, checker-accepted composition-order counterexample**. External original sources: Cook–Reckhow (1979) DOI https://doi.org/10.2307/2273702; Cousot–Cousot (1977) DOI https://doi.org/10.1145/512950.512973; Clarke et al. (2000) DOI https://doi.org/10.1007/10722167_15. FRAT-XOR https://github.com/meelgroup/frat-xor and DRAT-trim https://github.com/marijnheule/drat-trim remain **different** proof grammars; their checkers are not imported as historical authority. Required outside P-vs-NP repos https://github.com/konard/p-vs-np and https://github.com/blkph0x/p-vs-np-proof-research also supply no authenticated mixed checker.

**Adopt:** original accepted SOURCE, original body of /386 checker, /561 paid congruence and /579 free facet quotient, zero-cost exact facet identity and complete signed-port provenance. **Reject:** the inference that a single paid-congruence sweep followed by free facet deduplication reaches the same cost as the converse order. **Retire:** no other theorem. **Change relative to root main:** an additional strictly restricted /386 CEGAR normalization-order counterexample; no generalized native calculus, lower-bound, proof-chain status or complexity conclusion is promoted.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P2-D1] full historical accepted bytes and operations, [P2-C3] full-calculus alpha/gamma, [P2-B1] hard-family all-rule lower bound, and the separate [P2-B2/B3] time/space computation bridge remain **OPEN**. P versus NP remains **OPEN**.

**Next precise acquisition target:** authenticate one genuine historical shared-DAG cross-rule RES-to-AND3 or paid DEF-to-LOCAL-CONVERT positive certificate, then test full-rule abstract replay and signed corrupted-port controls. Preserve exactly five research roles and the historical two Route A/three Route B allocation.
