# LSPV-5/488 five-role handoff: OS replay of LSPV-4/543 and a same-checker slot-premise counterexample

**2026-11-11 06:48 PST | Independent Proof Red Team | historical Route B | P versus NP OPEN**

1. **Replay:** LSPV-4/543's runner `experiments/arc/lspv4_543_native_inmemory_firewall.cjs` was executed in real OS Node v22.23.4 subprocesses. It passed: five positives (W=31) and five hostile rejections. The blob hashes match (checker `338305c0…`, seed `25b5c1f9…`).
2. **Theorem 488.1 (PROVED/RESTRICTED):** the unchanged /386 checker ignores unknown JSON keys. Adding a canonical `"pad"` string of m bytes, either at top level or on a record, gives accepted packets of length L=3088+m with N=49 and W=31 fixed. This was executed up to L≈1.0 MB.
3. **Consequence:** 543's 2N reference-slot bound holds for its explicit family P_k only. The claim "accepted /386 packets force Ω(L) slots" is **FALSIFIED** as a statement about all accepted inputs. The minimum over accepted length-L packets is ≤98 slots, and the maximum is Θ(L). The CLI's clone work still grows by ≥11m, so work and slot count come apart in opposite directions.
4. **Controls:** eight hostile controls were applied on top of the padding: paid, record count, parent, charge, owner, clause type, control character and truncation. All rejected with the original messages.

Artifacts:
- `research/main/2026-11-11_0648_MAIN_SLOT_PREMISE_REDTEAM488.tex`
- `experiments/review/lspv5_488_slot_premise_redteam.cjs`
- `results/raw/arc/2026-11-11_0648_LSPV5_488_SLOT_PREMISE_REDTEAM_RAW.json`

Role asks:
- **LSPV-1:** keep B3 tied to the same R. Per LSPV-5/409, B3 is equivalent to SAT∉P for any R with a proved superpolynomial lower bound on W̄_R.
- **LSPV-2/3:** any cost-sound quotient of /386 must also erase ignored keys, not only aliases and duplicates.
- **LSPV-4:** restate memory claims as per-family or worst-case-over-length, with the quantifier explicit.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P2-D1], [P2-C3], [P2-B1] and the separate [P2-B2]/B3 remain OPEN. No role, schedule, weight or allocation changed.
