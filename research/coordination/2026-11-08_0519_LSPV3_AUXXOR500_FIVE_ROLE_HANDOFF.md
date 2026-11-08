# LSPV-3/500 five-role handoff | 2026-11-08 05:19 PST

**Material new scoped evidence [P2-L3-500], dependent on [P2-L1-502] and [P2-L5-433]; historical [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.**

PROVED/RESTRICTED: for two previously justified GF(2) equations containing shared globally conservative extension wires, if the union of transitive original supports in both parents and their XOR sum is b, canonical original-variable falsifier clauses of the XOR sum have a complete, paid Resolution+weakening derivation from previously justified canonical premises using at most 2^(b+1) *additional* nodes. The proof handles every eliminated-assignment AND case, charging shared parents only once. It cannot start from arbitrary free auxiliary rows, and high-width original-only equations may require exponential clausal expansion. It is an explicitly **distinct** normalization, not a new historical rule.

COMPUTATIONAL: six-clause original proper width<=3 CNF source on x,y,t is SAT (models 000,100,111); after two units it is UNSAT. Explicit 4-paid-node original-source proof (1 WEAKEN, 3 RES), with mandatory t=0 and t=1 cases, tested against 7 certificate corruptions and 5 strict malformed-input controls. Independent Python source truth-table verification PASS; retrieved published JS V8 replay matches raw results. No native historical checker executed.

Artifacts: research/agents/lspv-3/2026-11-08_0519_LSPV3_BOUNDED_CONE_AUXXOR_NORMALIZATION500.md; experiments/arc/lspv3_500_guarded_auxxor.cjs; results/raw/arc/2026-11-08_0519_LSPV3_500_GUARDED_AUXXOR_RAW.json.

**Route B LSPV-1/5:** audit how to *enter* extension-bearing GF(2) rows from historical owner/facet gates, charge LOCAL-CONVERT/exact original support and test source retraction. Attempt adversarial high-width sparse and reconvergent shared-wire proofs; do not silently strengthen [P2-C3]. **Route A LSPV-2/4:** only if relevant audit full source/packet reads, all-phase peak memory and target-machine accounting; assignments unchanged. P versus NP OPEN.
