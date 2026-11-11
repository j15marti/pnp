# LSPV-1/573: Same-byte dual-native acceptance with a SAT source is not mixed-calculus authentication

**2026-11-11 07:04 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED source-code composition theorem + COMPUTATIONAL original-body V8 differential | P versus NP OPEN.**

## IDEA: one candidate theorem and four falsifiers, fixed before search

**Candidate 573.1 (P2-D1/P2-C3 authentication firewall).** There is a single exact raw JSON byte string accepted simultaneously by the two distinct, archived and unmodified project checkers, `V341` (SOURCE/AND3/XOR fixture checker) and `V386` (SOURCE/paid-DEF-facet/strict Resolution complete CLI), such that **an original signed strict-3CNF source attached to the accepted `V341` packet is SAT**. This strengthens the previously published *two-UNSAT-source* polyglot LSPV-2/549 by inserting LSPV-3/551's existing SAT-source accepted packet. It constructs **no** cross-rule inference and authenticates **no** complete historical `R_mix341` calculus.

Precommitted falsifiers: **F1**, `V341` requires `summary` to be an actual Array rather than an object with `length`; **F2**, a second SAT-source fixture makes the joined `V341` packet reject; **F3**, `V386` checks or rejects the added `fixtures` and `summary.length` fields; **F4**, the proposed 18-bit assignment falsifies any of the 48 original SAT-side clauses. F1-F3 fail in original-body verification; F4 fails by independently evaluating every clause. Four single-sided hostile mutations discriminate the two actual checker predicates.

## SEARCH: source provenance, corpus and precedent

Read complete root `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (blob `7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3`), the current issue #3 through LSPV-5/488R1, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, current five-role handoffs and materially relevant actual reports: LSPV-1/571-572; LSPV-2/539, /549, /551 and /557; LSPV-3/551, /568, /570; LSPV-4/542-543; LSPV-5/487 and /488R1. Examined archived original checker sources and exact prior accepted packets. Related earlier LSPV-2/539-549 records were reconciled to their original scope; the two most relevant are /539's separate sound typed reference and /549's dual-checker product. The key newer primitive is LSPV-3/551's source-SAT counterexample (and LSPV-3/552's parametric variants). None of those results authenticated a **single** unified mixed-rule checker.

Required external/primary literature checked: Cook–Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44, 36-50, https://doi.org/10.2307/2273702; Cousot–Cousot (1977), *Abstract Interpretation*, POPL, https://doi.org/10.1145/512950.512973; Clarke–Grumberg–Jha–Lu–Veith (2000), *Counterexample-Guided Abstraction Refinement*, CAV, https://doi.org/10.1007/10722167_15; Ben-Sasson–Wigderson (2001), *Short Proofs Are Narrow*, https://doi.org/10.1145/375827.375835. In particular, no externally specified proof grammar or alternate proof system is silently imported into `R_mix341`. The native /341 and /386 checker-source predicates are the only authority in the claim.

Source authority:
- Original fixture checker `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.
- Original archived Resolution/DEF checker `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`.
- Existing `V341`-accepted SAT source packet `results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json`, blob `706947c767361e7c979b8208677eb983d33838f4`.
- Existing `V386` complete-CLI-accepted K4 certificate `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json`, blob `e3eb2a46857776089ab83f4ad50159ef622d2869`.

## Theorem 573.1: an accepted same-byte SAT-side polyglot

Let `A` be the parsed two-fixture packet of LSPV-3/551 and `B` the parsed 29-paid-node original `/386` certificate of LSPV-1/568. Define exactly:

```javascript
const P = {
  fixtures: A.fixtures,
  spec: B.spec,
  gate_defs: B.gate_defs,
  records: B.records,
  summary: { ...B.summary, length: A.fixtures.length }
};
```

Let `b` be `JSON.stringify(P)+"\\n"`, an exact **16,178-byte ASCII JSON packet** (Git blob `cdd96103aa1cff848d03b25872a72a21c0f5d59c`). Let `F_A` be the 48 signed literal clauses of `P.fixtures[1]`, *not* the independent guarded K4 source of `P.spec`.

Then the two unmodified archived programs satisfy:

$$
\boxed{V_{341}(b)=\mathrm{ACCEPT},\quad
V_{386}(b)=\mathrm{ACCEPT},\quad
\mathrm{SAT}(F_A)=\mathrm{TRUE}.}
$$

**Proof.** Direct inspection of the exact original checkers confirms that `V341` reads `fixtures` and `summary.length`, but not `spec`, `gate_defs`, `records` or the other summary counters. `V386` reads precisely its own `spec`, `gate_defs`, `records` and six summary counters, ignoring `fixtures` and `summary.length`. Consequently both accessor projections of `P` equal previously accepted parsed packets. Each original program's complete accepted control flow therefore accepts the joined packet. This is a deterministic program-property statement; no new proof rule is asserted.

For source satisfiability, assign original edge bits `101001000000100000`, i.e. set 0-based edge positions 0, 2, 5 and 12 to 1 and all other positions to 0. These four active edges form a cycle. Every ordinary vertex's even-parity clauses are satisfied. The exceptional vertex 0 clauses jointly enforce exactly `x0 XOR x1 = 1` independently of edge `x12`, so that source also holds. Direct literal evaluation confirms **48 of 48 original signed width-three clauses**. Yet the forged `V341` proof falsely claims `x0 XOR x1 XOR x12 = 1`; it evaluates to 0 on the same assignment. This is the already authenticated LSPV-3/551 source forgery, combined here with the separate original `/386` accepted language. QED.

**Corollary 573.2 (non-composition).** The implication

$$
V_{341}(b)\land V_{386}(b)
\Longrightarrow
\text{one sound, source-bound, mixed-rule refutation of a common source}
$$

is **FALSIFIED** by this byte string. Even two complete original checker acceptances on identical bytes do not bind the two independent in-band source identities or authorize RES-to-AND3, paid-DEF-to-LOCAL-CONVERT, GF(2), assumptions, discharge or cross-checker shared paid-node identity. The charges 47 on the SAT fixture and 29 on the distinct guarded-K4 proof must never be added, minimized together or interpreted as an all-rule `R_mix341` proof.

**Corollary 573.3 (CEGAR semantic firewall).** Any proposed P2-C3 abstraction that both (i) includes **every** checker-accepted `/341` raw trace as a sound semantically entailed source-refutation and (ii) requires all accepted abstract terminal contradictions to be entailed by that same literal CNF source is impossible, since the constructed accepted trace has a satisfying assignment. The SAT-side accepted path is **not spurious relative to the actual `/341` program acceptance relation**; pruning it requires an explicitly changed, separately identified semantic validity predicate or a different authenticated sound native calculus. This is a logic-level incompatibility, not a superpolynomial cost lower bound.

## TEST: exact original-body execution and hostile controls

Executed the unchanged `/341` function body and the complete original `/386` checker body, including all eleven original `/386` bundled corruption tests, in hosted V8. Only the file/argv adapters, `/386` diagnostic SHA256 output (stubbed, **not** represented as a genuine hash) and structuredClone compatibility were adapted. The verifier logic, original record checks and negative mutations were not rewritten.

| Single exact JSON payload | `/341` | Full `/386` |
| --- | --- | --- |
| Constructed dual-source polyglot, SAT on A-side | **ACCEPT**: 2,273 checks | **ACCEPT**: 3,542 checks; 11 bundled negative tests |
| Replace forged A-side string charge with numeric 1 | REJECT: source parity | ACCEPT |
| Replace forged A-side support `"012"` with `[0,1,12]` | REJECT: invalid affine alias | ACCEPT |
| Underpay B-side summary by one | ACCEPT | REJECT: paid cost |
| Corrupt final B-side Resolution pivot to 999999 | ACCEPT | REJECT: bad pivot |

The source witness was checked independently against the 48 literal clauses from the *exact accepted combined packet*, not inferred from either checker verdict. Original B-side paid work **29** covers 28 Resolution nodes and one paid definition owner; 45 B-side records include 17 genuine source clauses. The A-side forged fixture contains 48 original clauses and 47 paid nodes. Neither checker tests the other side's ancestors, contexts or source.

**Reproducibility:**
- Exact accepted bytes: `results/raw/arc/2026-11-11_0704_LSPV1_573_DUAL_NATIVE_SAT_POLYGLOT_PACKET.json` (blob `cdd96103aa1cff848d03b25872a72a21c0f5d59c`).
- Complete OS subprocess reproduction and four hostile tests: `experiments/arc/lspv1_573_dual_native_sat_polyglot.cjs` (blob `a209125fb8b6cc1d497e23b1b20c8d8530081815`).
- Actual executed V8 raw ledger: `results/raw/arc/2026-11-11_0704_LSPV1_573_DUAL_NATIVE_SAT_POLYGLOT_V8_RAW.json` (blob `fd561c31831dc777297e4012ad6c28835a91815d`).

**Execution limitation:** The standalone Node.js reproducer was syntax-checked and published with source/packet Git-blob guards. It was **not executed as an operating-system subprocess in this hosted run**; independent LSPV-5 OS replay remains requested. The V8 source-level run is not a claim to have authenticated missing historical grammar.

## Dependency ledger, hostile controls and barrier audit

**P2-D1 OPEN.** This is a new *negative accepted-byte authentication regression* for the two already archived **distinct** checkers. It tightens the LSPV-2/549 noncomposition falsifier but neither produces nor disproves a possible recovered single full `R_mix341` dispatcher. Authentic SOURCE, RES, AND3, GF(2), LOCAL-CONVERT, paid definitions/facets, wire visibility, contexts, discharge, joins, deletion, weakening and fixed historical tariffs in one parser remain unrecovered.

**P2-C3 OPEN.** The actual concrete program-acceptance languages may be modeled separately, but a cost-sound, sound-refutation abstract model cannot silently identify either with a semantically sound common native calculus. Cost constraints alone do not repair false source entailment. Genuine original accepted checker paths cannot be eliminated by claiming they are mere abstract spurious traces.

**P2-B1 OPEN.** The SAT source shows an unsound checker can issue a false refutation. It is **not** a legal cheap refutation in a properly defined sound calculus and no hard-family superpolynomial lower bound follows. Algebraic, extension, learning, branching, reconvergence, compact-circuit and sharing shortcuts all remain admitted for a future authenticated calculus.

**P2-B2 and P2-B3 separately OPEN.** Neither two original checkers, polynomial checking, a forged short proof nor SAT in P establish a polynomial upper bound on `Wbar` in the same fixed calculus without an explicit transfer theorem. Logical work, raw bytes, discovery, actual checker time, DAG span and peak memory remain different resources.

**Hardness barriers:** Cook–Reckhow soundness is not automatically inherited by a buggy parser; the proof checker itself must implement the source-binding semantics. CEGAR may refine only paths spurious in the actual concrete system. Resolution width-size theorems are grammar restricted and do not transfer to unknown GF(2)/extension rules. No relativization, algebrization or Natural Proofs barrier is overcome. The hostile SAT witness and independent-source polyglot defeat source-invariance and model-transfer claims directly.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both roots were completely fetched; neither has a change in a load-bearing theorem truth value or in an already known logical counterexample requiring another tracker entry. Original evidence is appended as a role-owned report, exact packet, code, raw results and handoff; no tracker write was attempted.

**Root manuscript blocker:** Fresh `main.tex` fetch at blob `311964326384409e944cb675e2cc6da689ee2dff` returned **zero content bytes** for the approximately 2 MB root manuscript. An ownership-safe edit cannot be made from this response. The original was deliberately untouched. LSPV-5 should incorporate this report in its whole-manuscript reconciliation once full content is available.

**Next decisive target:** LSPV-2 and LSPV-3 should obtain **one** immutable, original historical full mixed-rule checker and a source-bound accepted RES-to-AND3 or paid-DEF-to-LOCAL-CONVERT edge, plus exact cost; LSPV-5 should independently run the published OS replay and challenge both original languages' accessor projections. LSPV-4 must continue distinguishing checker/program resources from proof work. No existing agent, title, schedule, Pacific timezone, historical rule weight, ownership boundary or TWO Route A / THREE Route B allocation was altered.

**P versus NP remains OPEN.**
