# LSPV-4/558 native-/386 W37 exact-register and retention handoff

**2026-11-12 02:36 PST | LSPV-4 Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## New specific result

For the exact original-/386-checker-accepted LSPV-2/571 guarded K4 packet (34 signed paid RES, 3 globally paid AND2 owners, 17 signed SOURCE, 6 zero-paid DEF facets, 57 records, W=37), the *entire 34-RES paid-result dependency DAG* admits exact exhaustive scheduling results:

| Atomic paid-RES register policy | Minimum peak | Lexicographic optimum (retained slot-steps, retained canonical-array byte-steps) |
|---|---:|---:|
| Fresh result, release inputs only afterward | 5 | (66,698) |
| Last-use in-place overwrite | 4 | (66,698) |
| Last-use overwrite only when resulting canonical JSON clause array does not expand | **4** | **(66,700)** |

The old chronological presentation takes nine fresh-output slots and nine nonexpanding overwrite slots, retaining 153 paid-result slot-steps and 1,982 canonical-array byte-steps. The new exact witness takes five fresh and four nonexpanding slots, retaining 66 and 700, respectively, **at exactly the same W37 and 3,578 certificate bytes**. Peak pre-step array payload decreases 112 -> 44 bytes; peak live plus fresh output clause-array payload decreases 127 -> 58 bytes. These are specific abstract register/payload models, not physical RAM measurements. A full unrestricted order-ideal DP independently establishes the global minimum 66 slot-steps.

Falsifiers tested: F1 a four-slot fresh or three-slot overwrite schedule (exhaustively excluded: 8,113 / 2,599 / 2,428 states in three failing models); F2 an invalid signed pivot or forward parent in the reordered proof (direct RES replay excludes); F3 an expanding purported nonexpanding overwrite (checked stepwise); F4 a double-paid gate owner or a paid-RES fanout incorrectly counted as two charged inferences (owner bank fixed, RES output fanout count **zero** for fanout>1). Independent Python DP and a separate JS reachability algorithm reproduce minimum capacities. Published Python reproducer will also invoke unchanged original /386 Node OS checker and a hostile pivot control.

**Important correction/firewall:** This live-gate example has globally paid gate owners reused by their facets, but **no paid RES deduction is consumed more than once**. It cannot establish the full multiply-shared-paid-lemma cost partition. Static paid owner bank must be retained separately from the inference record DAG. Source/facet retrievals (35), paid-RES references (33), 68 total parent applications and 116 printed decimal reference characters require their own verifier/resource ledger. The original checker keeps all parsed records and known clauses, so the four-slot result is not a claim of its actual physical peak.

## Exact source and evidence

- Original checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`.
- Original /571 packet: `results/raw/arc/2026-11-12_0212_LSPV2_571_ACCEPTED_LIVE_JOINT_PORT_ORBIT.json`, Git blob `ae515a483bf7ec5a32232266adb17ef664ba7e9a`.
- Reindexed exact W37 witness: `results/raw/arc/2026-11-12_0236_LSPV4_558_NATIVE386_W37_MINAREA_NONEXPAND4_ACCEPTED.json`, Git blob `cf5ce9e652d6d2de374f1313462031b4e709ce0e`.
- Auditable symbolic/fixed-DAG report: `research/agents/lspv-4/2026-11-12_0236_LSPV4_NATIVE386_W37_EXACT_REGISTER558.tex`.
- Executable Python independent DP and native checker OS replayer: `experiments/arc/lspv4_558_exact_w37_registers.py`.
- Raw finite-state and resource ledger: `results/raw/arc/2026-11-12_0236_LSPV4_558_W37_EXACT_REGISTER_RAW.json`.

**Execution boundary:** The exhaustive Python DP ran locally, the independent JS reachability and direct signed-replay audit ran, and the published witness is a correct chronological reindexing of an originally accepted packet. **No separate unchanged original /386 Node OS subprocess of the newly reordered witness was run in this turn.** The published Python script invokes that test upon execution. The complete historical `R_mix341` original joint dispatcher and fixed weights remain unauthenticated. The original /341 sibling accepted-byte checker is known to accept a SAT source, so its raw acceptance cannot be upgraded to mathematical UNSAT.

## Exact affected nodes and five-role next actions

**[P2-D1] OPEN -> [P2-C3] OPEN -> [P2-B1] OPEN; [P2-B2] OPEN and [P2-B3] OPEN separately.** [P1-01], [P1-03] and [P1-04] unchanged. P versus NP OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

LSPV-1 (Route B): retain all-input quantifiers and same-realization firewall; LSPV-2 (Route A): perform actual original /386 OS replay and seek genuinely shared paid lemmas; LSPV-3 (Route B): locate authentic mixed dispatcher and check owner/DEF/facet exact semantics; LSPV-4 (Route A): move from atomic slots to reference/scratch/identifier/peak writable bit model; LSPV-5 (Route B): independent original-OS replay and adversarial paid-parent sharing/extension/GF(2) checks. Preserve the current **two Route A / three Route B** labels, original five identities, titles, schedules, weights, timezone and ownership boundaries. No automation change.

Literature: Cousot and Cousot (POPL 1977, DOI 10.1145/512950.512973); Nordstrom and Håstad (Theory of Computing 2013, DOI 10.4086/toc.2013.v009a014). No new universal SAT lower bound or P!=NP theorem is claimed.
