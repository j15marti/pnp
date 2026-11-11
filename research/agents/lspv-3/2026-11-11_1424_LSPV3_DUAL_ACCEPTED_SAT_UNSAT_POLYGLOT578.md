# LSPV-3/578: Same JSON accepted by two archived native checkers with incompatible SAT/UNSAT sources

**2026-11-11 14:24 PST | LSPV-3 Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED checker-language separation + COMPUTATIONAL original-body replay | P versus NP OPEN.**

## Candidate and four pre-search falsifiers

**Candidate [P2-D1] / [P2-C3]:** The *two distinct* recovered archived checkers (/341 SOURCE/AND3/XOR, /386 SOURCE/paid-AND2/DEF-facets/RES) accept the same serialized JSON even though the in-band original signed CNFs have opposite satisfiability labels. This defeats the shortcut claiming that intersection of original checker-accepted byte languages is one source-bound mixed proof.

F1: /341 rejects the added /386 fields or composite summary. F2: /386 rejects the retained /341 fixtures or summary length, or double-counts paid owners. F3: the 48-clause /341 source is not SAT under a complete assignment, or odd-charge /386 source is not UNSAT. F4: source/pivot/payment corruption in one section triggers rejection in the other section because the checkers share an authenticated source. All four proposed falsifiers failed in the exact 10-case differential and direct source analysis.

## Historical byte authority and precedence

Pinned original /341 checker: experiments/arc/lspv2_341_independent_verify.js, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**, dispatches AND3 and XOR only. It **does not** implement RES, DEF, LOCAL-CONVERT, joining, weakening, assumption discharge, exported/private ports or a complete mixed grammar.

Pinned original /386 checker: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**, dispatches signed original SOURCE, conservative globally paid AND2 gate definitions and their zero-additional-cost authentic facets, and strict oriented Resolution. It does not implement AND3 or GF(2) as its own native step.

Inputs were the already published LSPV-3/568 accepted SAT-source forgery (blob **adb4864906029ecf7b1cd1cf7a4bf513218a13a8**) and the separately valid LSPV-3/577 terminal-live complementary gate packet (blob **5edeac8fbbe39764cfd3d075acd3c6ce7b5c87fe**). No novelty is claimed for the earlier individual certificate constructions.

**Prior-art control:** LSPV-2/549 already exhibited a dual archived-checker JSON polyglot using two separate **UNSAT** sources. The new /578 distinction is a common accepted envelope with a genuinely **SAT** /341 source alongside a genuinely **UNSAT** /386 source. LSPV-5/413 already proved that the surviving /341 checker is not the full historical R_mix341 rule system. The stronger, independently typed LSPV-2/539 reference is a separately proposed repair, not historical accepted syntax.

## Theorem 578.1 (exact differential source-boundary witness)

Let A be the pinned LSPV-3/568 packet; let B be the pinned LSPV-3/577 packet. Construct one JSON object P by retaining all properties of A, then setting P.spec=B.spec, P.gate_defs=B.gate_defs, P.records=B.records, and P.summary to a single object containing the key length equal to A.fixtures.length together with every key and value of B.summary. Serialize via JSON.stringify(P) followed by a single newline.

The published serialized P has **14,032 UTF-8 bytes** and Git blob **1c3b400857ab2cfb7d78f37b2723945e6521a83a**. Both unchanged original checker bodies independently accept these exact bytes:

- The /341 checker validates only its own fixture/proof/source subobject and a summary-length equality. It accepts **47 paid AND3/XOR** records, passing **3,273** original assertions including its five built-in corruptions and seven malformed-CNF controls. Its in-band signed original CNF has **48 clauses on 18 variables** and is SAT. The explicit assignment a=**101001000000100000** satisfies **48/48** clauses.
- The /386 checker validates its own separate guarded odd-charge Tseitin source, three globally paid owners, 32 RES nodes, four free facet rows, and the relevant summary counters. It accepts at **W=35**, with **49 genuine SOURCE records and 85 total records**, passing **6,523** original assertions including eleven built-in corruptions. Its original guarded source is UNSAT: summing all graph incidence equations mod 2 gives zero on the left and odd-charge one on the right.

The original /341 source forgery works because its numeric first charge is 2^32+1=4294967297, bitwise-XOR-truncated to one in JavaScript, while its preexisting malformed support string "012" bypasses an intended typed affine-annotation check. This is **an acceptance defect in the actual recovered checker**, not a new sound logical rule of R_mix341.

The /386 checker never reads or certifies the /341 original clauses. The /341 checker never certifies the /386 original clauses. Hence:

$$
P\in L_{\mathrm{acc},341}\cap L_{\mathrm{acc},386}
\quad\not\Longrightarrow\quad F_{341}=F_{386}.
$$

The exhibited sources even disagree on SAT versus UNSAT. Therefore a genuine shared refutation requires an independently bound single immutable original-source identity and a single historically authenticated mixed-rule dispatcher. This is a proof about the **existing two checker languages**, not a claim that their composition authenticates any mixed inference. QED.

## Original-code replay and hostile near-misses

Both full historical JS bodies were executed in hosted V8, with only input/output and printed-diagnostic-digest adapters, plus a JSON-value structuredClone adapter. **Native operating-system Node execution of the separately published reproduction script was not performed during this run.** The hosted diagnostic hash is not cryptographic SHA-256; the files themselves were checked against Git blob hashes through complete readback.

| Fully materialized certificate | /341 checker | /386 checker |
|---|---|---|
| Original 14,032-byte polyglot | **ACCEPT** | **ACCEPT** |
| Make malformed /341 charge binary numeric one | REJECT | ACCEPT |
| Replace /341 string support with actual array [0,1,12] | REJECT | ACCEPT |
| Flip /341 signed SOURCE literal | REJECT | ACCEPT |
| Corrupt /341 terminal XOR rhs | REJECT | ACCEPT |
| Corrupt /386 RES pivot | ACCEPT | REJECT |
| Forge /386 SOURCE signed clause | ACCEPT | REJECT |
| Underpay /386 owners/RES | ACCEPT | REJECT |
| Collide /386 fresh output with guard | ACCEPT | REJECT |
| Corrupt both the /341 charge and /386 payment | REJECT | REJECT |

**10/10 exact predictions matched**, and the baseline triggered the complete original internal negative tests in each checker. The two original checker acceptances are genuine; **no source join, mixed-rule legality, or common source formula follows**.

## Abstract and cost-sound implications

Under a legitimate *single* historical calculus R, keep original-source bytes and provenance, typed signed literals and affine annotations, full shared-DAG parent identities, global paid-owner uniqueness, fresh/external/private wire visibility, contexts/discharge/reconvergence and fixed historic weights. Two parsers independently accepting two different sources cannot be rebranded a common source-bound certificate. The original /341 SAT acceptance must be distinguished from a semantically valid UNSAT derivation. A CEGAR routine cannot discard a genuine checker acceptance; it must precisely explain this missing source-authentication step. Any stricter repair is a distinct, clearly labelled proof system until historical equivalence is proved.

Paid work **47** (/341) and **35** (/386) are separately counted, **not** a composable 82-step mixed proof. The complete evidence payload is 14,032 bytes, not logical work, checker machine time, span or peak space. The evidence does not establish a full historical alpha/gamma, paid lower bound, proof-system normalization, SAT time lower bound, or B3. Free optimal legal proof selection, genuine assumption-aware sharing and all legitimate shortcuts remain allowed.

## Read sources, primary literature and next steps

Reviewed complete root proof1.txt, blob **f46f6aae25571340a5fd17a5181d51c271509947**, root proof2.txt, blob **42943fe447c6061fb8009a526f46ac8a6684765c**, issue #3, AGENTS.md, CODEX.md, the pnp-research SKILL, historical source producer and both checkers, LSPV-5/413, LSPV-2/539 and /549, LSPV-3/544, /555, /568, /577 and current handoff, LSPV-5/495, original 539-549 corpus and subsequent work, relevant Grok 2026-11-11 report and Claude world ledger. Full untruncated repository-tree search found no authenticated complete original R_mix341 mixed dispatcher.

Primary literature: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), https://doi.org/10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL (1977), https://doi.org/10.1145/512950.512973; original FRAT-XOR format, https://github.com/meelgroup/frat-xor/blob/main/format.md. FRAT-XOR is **external** to this historical grammar.

Published complete independent evidence:

- Accepted byte packet: results/raw/arc/2026-11-11_1424_LSPV3_578_DUAL_CHECKER_SAT_UNSAT_PACKET.json, blob **1c3b400857ab2cfb7d78f37b2723945e6521a83a**.
- Ten-case raw V8 original-body differential: results/raw/arc/2026-11-11_1424_LSPV3_578_DUAL_CHECKER_DIFFERENTIAL_V8_RAW.json, blob **d06d242c8e0d01fa59bc7405bec0622930c33456**.
- Standalone exact OS Node reproducer: experiments/arc/lspv3_578_dual_native_sat_unsat_polyglot.cjs, blob **afdb72b6745e5cb4a603af618afba8a259e73cbe**.
- Role-owned report: this file. Five-role handoff: research/coordination/2026-11-11_1424_LSPV3_DUAL_SOURCE_FIREWALL578_FIVE_ROLE_HANDOFF.md.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1 -> P2-C3 -> P2-B1 remain **OPEN**; P2-B2/B3 separately OPEN; P1-01/03/04 OPEN. Preserve exactly the five current research roles, titles, identities, America/Los_Angeles schedules, historical weights and their TWO Route A / THREE Route B assignments. P versus NP remains OPEN.

**Next decisive load-bearing goal:** recover **one** original-source-bound checker accepting an actual historically legal mixed RES-to-AND3 or paid-DEF-facet-to-LOCAL-CONVERT/GF(2) transition. Separate-checker byte intersection is demonstrably insufficient.
