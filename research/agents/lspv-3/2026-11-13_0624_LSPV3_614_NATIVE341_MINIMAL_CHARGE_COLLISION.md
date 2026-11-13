# LSPV-3/614: Minimum-size complete /341 charge-canonicalization collision

**13 November 2026, 06:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED accepted-language counterexample + COMPUTATIONAL original-body replay | P versus NP OPEN.**

**Affected ID:** [P2-L3-614], a regression-corpus repair for SOURCE charge typing under [P2-D1]. Main [P2-D1] -> [P2-C3] -> [P2-B1] and separate [P2-B2/B3] remain OPEN.

## Candidate and preregistered falsifiers

**Candidate.** Even on the *minimum admitted K4 graph* and in a **complete** original-/341 certificate, pointwise conversion of all parsed JSON source charges to ECMAScript 32-bit integers is not acceptance-preserving. A pair differing only in the four charge fields, with identical pointwise integer coercions and global XOR, should have opposite native checker verdicts.

F1: the mixed-type packet fails the original odd-charge XOR assertion. F2: the local SOURCE assertion coerces its operands before strict comparison, making the verdicts identical. F3: some additional charge-dependent rule, witness, source-parent, or terminal test prevents complete acceptance. F4: the numeral-canonicalized counterpart or a wrong RES opcode, parent, sink or signed source is accepted.

All four were defeated in the directly executed original-body tests below. The original source's complete charge reads occur at lines 55, 61-66 of `experiments/arc/lspv2_341_independent_verify.js`.

## Complete accepted-byte pair and precise theorem

Let P be the genuine original K4 fixture in `minimal.packetBytes` of the immutable LSPV-2/537 corpus. It has a simple cubic K4 graph, 16 signed SOURCE clauses, 15 paid binary AND3/XOR inference records, essential deletion witnesses, a zero-mask/RHS-one terminal affine row, and fixed native paid work W=15.

Define P(q) by replacing only its `charges` array with q, preserving every other property and the entire rooted proof DAG. Take

```json
q_accept = [false, "1", 0, 0]
q_reject = [0, 1, 0, 0]
```

Both charge vectors have **identical pointwise** `ToInt32` values `[0,1,0,0]` and total bitwise XOR 1. However, in the original source, forbidden local-pattern parities are number 0 at vertex 0 and number 1 at vertex 1. For the accepted packet, JavaScript strict comparison evaluates `0 !== false` and `1 !== "1"` to true. For the normalized packet, `0 !== 0` fails (and the analogous vertex-1 check would fail).

**Theorem 614.1 (PROVED/RESTRICTED; complete fixed-fixture collision).** Under the exact archived checker semantics,

```
V341(P([false,"1",0,0])) = ACCEPT
V341(P([0,1,0,0]))      = REJECT
ToInt32([false,"1",0,0]) = ToInt32([0,1,0,0]) coordinatewise.
```

Proof: the original checker reads `charges` only through array length, the total bitwise XOR, and SOURCE-clause strict parity comparisons. The first two observations agree and pass in both cases; the local comparisons differ exactly as above. The accepted packet is the otherwise unchanged, fully passing K4 proof, so all subsequent assertions remain valid. The rejected packet fails during SOURCE validation. This is a counterexample to a concrete-to-abstract rule that *executes* proofs after losing the charge value's exact parsed type. A sound MAY abstraction may retain both outcomes; an exact quotient and CEGAR replayer cannot replace native charges solely by their integer coercions. QED.

The fixture uses the smallest graph size admitted by the checker (`g.n>=4`) and the required `4V-1=15` paid proof records, **not** a claim that its complete JSON byte count is globally minimal.

**Prior art, not rebranded.** LSPV-1/613 already proved the general fixed-packet charge-observation congruence and a 48-source all-Boolean SAT false acceptance. LSPV-3/610 classified a 70-element K4 SOURCE-prefix fiber, without full terminal packets. This run's incremental artifact is a concise **opposite-verdict full native K4 packet pair** with identical 32-bit charge normalization, complete signed sources and 15 paid nodes. LSPV-3/597 established a different source-and-charge *coupled* edge gauge and is not a fixed-source normalization rule.

## Authoritative execution versus reimplementation

The full exact checker body from Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0` was compiled and executed in hosted V8; only its file-input and output adapters were replaced. Original K4 corpus Git blob `d5e2d22674b0af365e9b82e4f1b2af8307182ba6` supplied the native fixture. **22 complete packet runs: 12 ACCEPT, 10 REJECT, zero unexpected; 16,812 positive checker assertions.** All accepted packets passed 1,401 native assertion groups. Hostiles included a RES opcode, forged parent, corrupted terminal row and altered signed SOURCE.

This is *original mathematical body hosted execution*, not a claim of independent original Node operating-system subprocess replay. The standalone pinned Node OS replayer is supplied below and syntax validated but was **not executed in an OS subprocess** in this run. It must be run from a complete repository checkout to close that separate execution-control item. The raw ledger records each accepted/rejected variant and exact host error.

The normalizer collision is a **native-language** counterexample, not a contradiction in mathematics. The original checker lacks an independently bound external source hash, and acceptance must remain separate from genuine UNSAT. The full historical `R_mix341` mixed dispatcher remains missing. No native RES->AND3, DEF->LOCAL-CONVERT, branch, discharge, private/exported interface, full-cost abstraction, or general lower bound was authenticated.

## Corpus and primary source audit

Read both root trackers (proof1 blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; proof2 blob `930c5eeddafce656717f28055a7a9a755f44737c` via immutable blob), issue #3, `AGENTS.md`, `CODEX.md`, the pnp-research skill, current handoffs, LSPV-3/539,/544,/549,/597,/610-/613, LSPV-1/613 and /616, LSPV-5/510, LSPV-4/583, GROK progress through 13 November 05:26 PST, and Claude world-ledger README. Historical semantic/statically typed extensions and the separate /386 checker do not establish this verifier's accepted-byte language. The original program body and source-bound fixture are the direct authorities.

[1] ECMAScript 2026, strict equality and binary bitwise XOR, https://tc39.es/ecma262/2026/ .
[2] Cook and Reckhow (1979), JSL 44:36-50, https://doi.org/10.2307/2273702 .
[3] Cousot and Cousot (1977), POPL, https://doi.org/10.1145/512950.512973 .
[4] Clarke et al. (2000), CAV, https://doi.org/10.1007/10722167_15 .
[5] FRAT-XOR/XLRUP, https://github.com/meelgroup/frat-xor . This is a distinct externally source-bound proof format, **not** historical `R_mix341` authority.

## Handoff and exact status

LSPV-2: retain exact JSON-native charge value/type and signed SOURCE bytes in the complete mixed grammar. LSPV-4: preserve count-once paid W=15 separately from evidence-bit count, machine parsing time, span and peak space. LSPV-1: do not promote checker acceptance to UNSAT or all-SAT lower bounds. LSPV-5: OS-replay both packets and attack strict-equality type fidelity and malformed-source authenticity. LSPV-3: add this paired full-certificate test to canonical accepted-byte CEGAR corpus and continue search for original cross-rule checker.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root tracker proof node status changes. Preserve exactly five roles, unchanged identities/schedules/timezone, 2 Route A / 3 Route B ownership, and all fixed historical rule weights. **P2-D1, P2-C3, P2-B1 OPEN; P2-B2/B3 separately OPEN. P versus NP OPEN.**
