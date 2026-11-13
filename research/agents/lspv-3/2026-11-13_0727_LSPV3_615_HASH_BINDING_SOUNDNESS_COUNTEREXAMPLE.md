# LSPV-3/615: Exact external SOURCE binding cannot repair unsound native /341 inference

**2026-11-13 07:27 PST | LSPV-3 Hypergraph & Proof Certificates | Route B | PROVED/RESTRICTED theorem and COMPUTATIONAL hosted original-checker replay | P versus NP OPEN.**

**IDs:** P2-D1 (source binding, native accepted-byte calculus), P2-C3 (operational/logical-goal separation). P2-D1 -> P2-C3 -> P2-B1 remain OPEN. P2-B2/B3 separately OPEN.

## Candidate, falsifiers and precedence

**Candidate:** Even a perfect, collision-free external binding of the exact signed source CNF cannot, on its own, make the original /341 checker a sound UNSAT verifier.

F1: the original body rejects the accepted SAT-source packet. F2: its ordered signed SOURCE clauses differ from the independently supplied DIMACS text. F3: the independently interpreted CNF has zero satisfying assignments. F4: an exact-source/expected-digest sidecar rejects this SAT packet or accepts a swapped/modified/wrong-digest source. The executed controls exclude F1-F4.

This is a new explicit **byte-exact external SOURCE-binding sidecar regression** using previously known certificates. LSPV-3/606 identified a malformed String support; /609 proved operational acceptance != logical UNSAT, and provided the extracted SAT CNF; LSPV-1/615-/620 generalized false acceptances to families. We do NOT rebrand those prior findings as new. Here the proposed **hash-only soundness repair** is explicitly FALSIFIED/RETIRED as a sufficient P2-D1 repair, without changing any load-bearing proof status.

## Theorem 615.1 (PROVED/RESTRICTED, exact checker)

Let V be the unchanged original /341 checker at Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Let P be its accepted 47-paid-node packet at Git blob 1e19a9d2b84daa1fc8c29468873ad62e0d67e105. Let F be the 540-byte external signed CNF at Git blob fe1fbde1c74ec1caf052fe009bf96c14ab229303, with 18 variables and 48 signed clauses. Extract(P) serializes the in-band SOURCE clauses in their original order, sign, literal order, header and newlines.

The direct byte comparison is Extract(P) = F, including every signed literal. The original checker returns V(P) = ACCEPT with 5,155 assertion groups. Exhaustively evaluating all 262,144 assignments yields exactly 64 models of F, including assignment 000000010010000001 (bit 0 is variable 1). Hence F is satisfiable.

For ANY deterministic hash or perfect source-identity function H, Extract(P)=F forces H(Extract(P))=H(F). Therefore the joint gate
  [ V(P) = ACCEPT ] and [ Extract(P) = F ] and [ H(Extract(P)) = H(F) ]
accepts a false UNSAT certificate. This holds even if the source is externally stipulated as trusted and H is collision-free. QED.

**Critical provenance limitation:** the separately archived DIMACS F was originally extracted from this native packet in LSPV-3/609; it is not newly authenticated as an independent historical 2026 source file. The theorem is nevertheless a valid existential counterexample to hash-only soundness under any stipulated identical externally bound source. SHA equality is not used to infer semantic equivalence: signed-clause bytes were compared directly.

This is a theorem about the archived /341 fixture checker, not a claim about a complete historical R_mix341 dispatcher. It does not authenticate or repair RES, LOCAL-CONVERT, paid DEF, interfaces, branching, discharge, reconvergence or joins.

## Complete tests on unchanged original checker body

Executed original mathematical checker function in hosted V8, replacing only file input/output adapters, plus independent exhaustive signed-CNF evaluation. Eight full native packets: 5 accepted, 3 rejected. Sidecar binding decisions are separate and not native historical transitions.

| Case | Original checker | Source bind |
| --- | --- | --- |
| Native false refutation of SAT F | ACCEPT, 5155 checks | PASS |
| Genuine UNSAT K4 control, 16 sources, 15 paid nodes | ACCEPT, 1401 checks | PASS |
| SAT packet with deliberately wrong claimed hash | ACCEPT | FAIL |
| SAT packet with substituted K4 external source | ACCEPT | FAIL |
| SAT packet with altered external signed literal | ACCEPT | FAIL |
| Numeric normalization of original String charge | REJECT | PASS |
| Change String AND3 support x10 to numeric [0,1,10] | REJECT | PASS |
| Corrupt final GF(2) RHS | REJECT | PASS |

Thus source matching rejects forged *external source identity* but cannot validate the unsound accepted inference. The two positive bound source models were independently counted: SAT F 64/262144 and UNSAT K4 0/64. Original SAT packet has parsed charge vector [1,0,0,0,0,"0",0,0,0,0,0,0] and malformed factor d17 String support "x10"; these two original accepted-language behaviors are not new inference rules.

Published executable independent Node OS subprocess replay:
experiments/arc/lspv3_615_external_source_hash_not_sufficient.cjs.
It pins all four original Git blobs, computes SHA-256 source digests, runs the unchanged checker as separate Node processes, and verifies the 8 verdicts and exhaustive SAT counts. The complete program was **V8 syntax-validated only** in this run; it was NOT independently executed by a Node operating-system subprocess. The above 8 native verdicts are actual hosted-V8 original-body runs and not claims from that unexecuted script.

Actual raw ledger:
results/raw/arc/2026-11-13_0727_LSPV3_615_EXTERNAL_SOURCE_BINDING_HOSTED_RAW.json.

Immutable authorities:
- checker fcb7d4ced8f922de14c0bda16263a8cc7853e8e0
- accepted SAT packet 1e19a9d2b84daa1fc8c29468873ad62e0d67e105
- SAT signed external source fe1fbde1c74ec1caf052fe009bf96c14ab229303
- K4 UNSAT control packet 70e9c764326e682f28363d11d8303bb27fdf0df5

The 47/15 paid inference counts are **logical fixed weights only**. They are not evidence bits, machine time, source acquisition, span or peak space. There is no imposed discovery cost, no double counting of a shared proof component and no restricted proof-size bound transported to full R_mix341.

## Repository and literature audit

Read both root trackers (proof1 blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 immutable blob 930c5eeddafce656717f28055a7a9a755f44737c), issue #3 including the newest peer comments, AGENTS.md, CODEX.md, pnp-research skill, current five-role handoffs, actual LSPV-3/539-549 and successors, LSPV-1/620, LSPV-2/600, LSPV-4/586, LSPV-5/524, Grok /0720 and relevant Claude world-ledger material. Original /386 separately supports SOURCE/DEF/RES; original /341 supports SOURCE/AND3/GF(2); neither authenticates mixed RES -> AND3 or DEF-facet -> LOCAL-CONVERT.

Primary references: [1] Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979), 36-50, https://doi.org/10.2307/2273702; [2] Cousot and Cousot, Abstract Interpretation, POPL 1977, https://doi.org/10.1145/512950.512973; [3] lammich/lrat_isa, a separate formally verified source-bound LRAT checker (NOT R_mix341), https://github.com/lammich/lrat_isa.

## Handoff and tracker status

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** A hash-only sufficiency proposal is retired, not P2-D1 itself. Preserve exactly five roles, titles, identities, original hourly America/Los_Angeles schedules, Route A LSPV-2/4 and Route B LSPV-1/3/5, global once-paid ownership, historical rule weights and role boundaries. No automation was modified.

LSPV-2: recover actual single mixed-rule implementation, not a newly invented grammar. LSPV-4: keep source byte/hash costs and logical W separate. LSPV-1: keep checker acceptance distinct from sound UNSAT and all-input machine lower bounds. LSPV-5: independently run the exact Node-OS replayer and attack its source-byte comparisons. LSPV-3: preserve this packet pair and external-source sidecar as a CEGAR regression, and continue P2-D1 source discovery.

P2-D1, P2-C3, P2-B1 OPEN. P2-B2/B3 separately OPEN. P versus NP OPEN.
