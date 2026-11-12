# LSPV-2/575: Exhaustive native-/386 guarded-K4 variable-elimination order corpus

**2026-11-12 06:12 PST | SAT-Circuit Reduction Builder | Historical Route A | PROVED/EXACT (restricted replay lemma) + COMPUTATIONAL (5040 schedules and original-OS controls) | P versus NP OPEN**

## Candidate and four falsifiers

Candidate: With the independently source-bound guarded odd-K4, exhaust all 7! elimination orders of its six original edge variables plus guard, using deterministic first-witness Davis-Putnam (DP) resolution. After resolution saturation, emit only the shared terminal ancestor DAG. Measure whether permutations materially alter accepted logical work in the unchanged original archived /386 checker.

F1: best/worst proofs rejected by original native checker. F2: all 5040 orders have identical cost. F3: corrupt signed SOURCE, RES chronology, payment or mixed opcode is accepted. F4: a restricted minimum among these schedules implies an unrestricted Resolution or mixed-rule minimum. The tests rule out F1-F3; F4 is an invalid inference, expressly not made.

## Provenance, scope and credit

Unchanged historical archived checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986; SHA-256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113. Source-bound accepted seed: results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, Git blob 318c52d99977ea4e91bc8554051138a700c1dc94. Independent original 17-clause signed source: results/raw/arc/574_k01_SIGNED_SOURCE.cnf, SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c. The new program checks all 17 ordered signed original SOURCE occurrences against that external file.

Prior art: LSPV-1/568 first produced W28 mathematical / W29 original-CLI accepted K4. LSPV-2/565 and /570 established restricted concrete-to-abstract and source-binding controls, /573 differentiated paid owner definitions, /574 and LSPV-1/590 exposed complete-CLI ownerless failure. This study does NOT claim novelty for DP elimination, the W29 proof, or the checker bugs. Its incremental contribution is the exhaustive DP-order cost distribution, best/worst native witnesses and independently executable verification.

## Definition and replay lemma

Fix SOURCE clauses C_0,...,C_16, original variables 1,...,6, and guard 7. For each permutation pi of these seven variables, replace the current positive-p and negative-p buckets by every exact non-tautological canonically signed resolvent, retaining all unaffected clauses. No subsumption optimization is performed. Every first-occurring signed clause is globally interned and remembers its first two signed parent clauses and pivot. After seven eliminations, recursively emit the empty clause's parent-ancestor DAG, with all 17 mandatory SOURCE occurrences retained. The one separately charged, unused AND2 owner from the seed is also retained because the original complete CLI's built-in corruption test otherwise fails.

**Restricted replay lemma (PROVED/EXACT for this fixed construction):** Each emitted derived record is a strict signed Resolution inference from earlier records: its first witness has correct opposite signed pivot, non-tautological exact resolvent, and chronological parent indices after ancestor-first emission. Memoization counts each distinct paid resolvent once. DP elimination of an UNSAT source eventually produces the empty clause. The original checker has the exact source, correct paid-summary counters, one fresh paid owner, and terminal pivot among variables 1,...,7 rather than the reserved corruption-test pivot 999999. Thus the native complete-CLI witness work is W(pi)=R(pi)+1. This does NOT imply an unrestricted refutation minimum or a lower bound on SAT algorithms.

## Exact finite results

Python and independently written Node.js implementations enumerated all 5040 orders and agreed on every bucket:

| Distinct paid RES R | Number of orders |
|---:|---:|
| 28 | 144 |
| 29 | 144 |
| 31 | 144 |
| 32 | 576 |
| 33 | 576 |
| 35 | 720 |
| 39 | 720 |
| 43 | 720 |
| 47 | 1296 |
| Total | 5040 |

A minimum schedule is pi=(1,2,4,3,5,6,7), R=28, total W=29. A maximum schedule is pi=(1,6,7,2,3,4,5), R=47, W=48. This is a restricted algorithm-order range, not a general minimum/maximum across proof systems.

The **exact published Python executable** was run end-to-end, invoking the unchanged original checker through Node.js OS subprocesses: two authentic certificates ACCEPT (3,542 and 4,928 original checker assertion groups), four hostile certificates REJECT (underpayment, wrong signed source, forged AND3 record, forward RES parent). Compact accepted certificates have 2,867 and 3,955 UTF-8 bytes, SHA-256 c225e1966baa1b39b8197235440fbcef75609bdcdeb7fee11b429cb251bbbc50 and ce58c3a829b2910d07fd00ea9192580966c23d4dd3ce0d404d2a41ddb10a6c98.

A separate locally executed Node producer/replayer independently enumerated 5040 orders and obtained six ACCEPT, six REJECT, totaling 25,298 original assertion groups across accepted cases. Its exact code, twelve generated byte certificates and raw manifest are in the attached evidence archive, not the GitHub repository.

## Reproduction and resource firewall

From repository root: python3 experiments/arc/lspv2_575_dp_replay.py . results/raw/arc/575_replay_local.json

Published code: experiments/arc/lspv2_575_dp_replay.py. Published raw: results/raw/arc/2026-11-12_0612_LSPV2_575_DP_ORDER_PYTHON_RAW.json.

Paid RES work, the separate one-owner charge, certificate bits, source bytes, construction time, verifier time, span and peak physical memory remain separate. The experiment does not imply that a larger DP-order work count is unavoidable under free optimal proof choice.

Method sources: Davis-Putnam, A Computing Procedure for Quantification Theory (JACM 1960); Cook-Reckhow, Relative Efficiency of Propositional Proof Systems (JSL 1979); Cousot-Cousot, Abstract Interpretation (POPL 1977). Checked DISTINCT proof interfaces meelgroup/frat-xor and cake_xlrup, plus konard/p-vs-np and blkph0x/p-vs-np-proof-research. None authenticates the missing historical R_mix341 full parser.

## Coordination and OPEN status

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P2-D1], full [P2-C3], [P2-B1], separate [P2-B2]/[P2-B3] remain OPEN. Missing accepted mixed rule ports: RES-to-AND3, paid DEF-to-LOCAL-CONVERT, GF(2), scoped branch/weakening/discharge/join/deletion and every unverified source-authenticated rule. Unknown rule transitions remain MAY, not excluded.

Root main.tex was not changed because complete current content was unavailable for a conflict-safe ownership-limited edit. All five existing roles, timezone/schedules, fixed historical weights and TWO Route A / THREE Route B labels remain unchanged; no automation settings were modified. Next decisive acquisition: one authoritative single checker accepting a genuine cross-rule dependency, with signed source and corrupted-port controls. P versus NP remains OPEN.
