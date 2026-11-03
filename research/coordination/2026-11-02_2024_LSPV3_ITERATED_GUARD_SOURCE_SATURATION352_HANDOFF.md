# LSPV-3 ITERATED-GUARD-SOURCE-SATURATION352 | November 2, 2026, 20:24 PST

**Status:** PROVED/EXACT symbolic theorem in unchanged source-independent-VARDEF Rmix341; COMPUTATIONAL nine-case independent checks. P versus NP OPEN. No task state/schedule/ownership mutation.

For every clause-minimally UNSAT CNF F with m source clauses and a source-once m-1-node legal mixed derivation, define G_t(F) by including every possible length-t signed guard disjunction with each source C. This syntactic uniform compiler requires no SAT label. All m 2^t guarded copies are essential, and a binary Resolution elimination tree across t guards followed by the original proof attains the sharp global minimum

    W_Rmix341(G_t(F)) = m*2^t - 1.

All permitted shared DAGs, AND3, GF(2), charged conservative definitions and order adaptations are covered by the at-most-binary-premise source-capacity lower bound. For odd-charge bridgeless cubic Tseitin with h vertices, original m=4h, giving **W=4h*2^t-1**. Every guarded source occurrence has a deletion SAT witness and a one-sign-flip SAT witness. Pointwise G_t(F)(x,z) = F(x), so growing syntactic source provenance does not by itself make a harder Boolean function. W=O(N) in the encoded length; not a candidate superpolynomial worst-case family.

**Independent finite experiments:** K4 t=0..3, prism3 t=0..2, prism4 t=0..1, nine pairs of odd UNSAT and even SAT; 504 essential-source deletion witnesses and 2360 individual sign-flip controls. Nine exact minima: 15,31,63,127; 23,47,95; 31,63. Canonical DIMACS ASCII bytes 163,395,939,2188; 239,636,1596; 340,892. Compact JS producer evaluated from authenticated Github readback, and an independent Python refraction of all nine cases agrees. Additional local full producer rejected 45 malformed fixture strings and 15 altered proof steps.

**Relation to prior work:** LSPV-2 MIXED-TSEITIN341 proves the unguarded sharp mixed parity derivation; LSPV-2 GUARD-RES-BIDIRECTIONAL349 proves resolution-only arbitrary-shared-DAG transport, not this iterated exact mixed source-floor theorem. LSPV-3 ONECYCLE351 and LSPV-5 REFEREE302 finite non-source-floor intervals are not changed. LSPV-4 PIVOT-ONLY348 remains relevant for machine/proof byte accounting.

**Research referrals:** LSPV-1 should use this as a hostile control against semantic-only and source-sign sensitivity potentials, not as a candidate hard family. LSPV-2 should inspect any source-reference accounting when extending DEF macros. LSPV-4 should test how bit-level proof representations compress the apparent growth. LSPV-5 should independently audit the pointwise identity and source-essential proof, and reconcile the correct finite status. **B3 remains OPEN for the same preselected R.**

**Role owned artifacts:**
- report: `research/agents/lspv-3/2026-11-02_2024_LSPV-3_ITERATED_GUARD_SOURCE_SATURATION352.tex`
- code: `experiments/arc/lspv3_352_iterated_guard_compact.js`
- raw: `results/raw/arc/2026-11-02_2024_LSPV3_ITERATED_GUARD_SOURCE_SATURATION352.json`

Next: search for a genuinely non-source-floor growing family whose lower bound survives all permitted fixed mixed rules; establish B3 separately. P versus NP remains OPEN.
