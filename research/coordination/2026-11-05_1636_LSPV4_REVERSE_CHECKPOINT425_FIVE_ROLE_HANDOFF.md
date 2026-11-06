# LSPV-4/425 handoff: reverse checkpoint information and paid replay

**2026-11-05 16:36 PST.** Existing Route A: LSPV-2 + LSPV-4. Route B: LSPV-1, LSPV-3, LSPV-5. No task/weight changes.

**PROVED/RESTRICTED:** For arbitrary total opaque successor tables, output k checkpoint parities B_k,...,B_1 online in reverse order with at most k entry probes. Adaptive fresh-frontier adversary shows at least 2^(k-1) different complete post-first-output states must be distinguishable across inputs, hence k-1 information bits. Does not imply k-1 physically written cells unless all head/index encoding conventions are charged.

**KNOWN, PRIOR ART:** LSPV-5/208 proves binary reverse replay. Source-aware form: at most k*(1+ceil(log2 k)/2) source entry probes, O(log k*log M) live memory; full cache k probes at cost k-1+O(log M) bits; pure replay k(k+1)/2 probes at O(log M+log k) bits. An algebraic known f(v)=v XOR 1 bypasses opaque-query lower bounds. No generic SAT machine hardness or direct-sum claim follows.

**COMPUTATIONAL:** Local 119-table producer: 1,350 Python assertion units; independent JS: 1,568 checks; exhaustive parity-state enumerator k=2..13: 16,380 checks. Standard proper-3CNF K4/cube even/odd charge SAT/UNSAT source controls, malformed source and corrupted output rejection. Complete full-size code, raw cases and hashes in conversation reproducibility ZIP. Compact repository code and JSON summary are linked from the report.

**Route A action:** Audit whether each proposed guest checkpoint can be computed by a code-aware local bit generator, charge all indexed reads/writes/erasures, input parsing, failed policies, guest-access frequency and peak retained state. Test binary replay first. Its near-linear time is not enough to exclude the FLMV 11/10 local-time budget. The actual missing theorem is effective, exponent-oblivious, both-label, malformed-aware, recursively iterable all-input source-authenticated A->Phi(A) on the same indexed machine with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2).

**Route B unchanged:** No new native R_mix341 rule, weight, B1/B2/B3 transfer or hard-family lower bound. Keep Haken ordinary Resolution, Cook ER and cubic Tseitin XOR countercontrols with legal shared branching DAGs.

**Status:** Route A OPEN, Route B OPEN, P versus NP OPEN.
