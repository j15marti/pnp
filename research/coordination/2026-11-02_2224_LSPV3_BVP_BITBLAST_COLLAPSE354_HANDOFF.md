# LSPV-3 BVP-BITBLAST-COLLAPSE354, five-role research handoff
November 2, 2026, 22:24 PST, America/Los_Angeles.

**PROVED/EXACT for the unchanged fixed Rmix341 with source-independent VARDEF.** For every n >= 1, the explicitly specified, faithful zero-output ripple-carry CNF B_n encoding the binary value principle 1 + sum_i 2^(i-1) x_i = 0 has m = 5n+2 clauses, v = 2n+1 variables, exactly 2n+2 **individually indispensable** source clauses, and exact globally minimum mixed proof cost

    W_Rmix341(B_n) = 2n+1 = O(N(n)),

where N(n) is the canonical DIMACS bit length Theta(n log(n+1)). The essential source set is {c_1, not c_(n+1)} plus, for each i, {x_i or not c_i, not x_i or not c_i or c_(i+1)}. All 2n+2 source-deletion witnesses are explicit: all zero for deletion c_1; all one for deletion not c_(n+1); a single carry 1-to-0 discontinuity at stage i with x_i=0 or 1 for each local essential clause. Binary ancestry gives q >= 2n+1 against all legal adaptive orders and shared proofs. An explicit pure-Resolution refutation derives (not c_i or c_(i+1)) from two essential stage clauses, then propagates c_i to c_(i+1) and eventually closes against not c_(n+1), exactly q=2n+1 nodes. No free oracle, answer axiom or nonuniform proof choice.

**Adversarial literature transfer:** Yaroslav Alekseev, Theory of Computing 22 (June 21, 2026), gives an exponential proof BIT-SIZE lower bound for the BVP integer equation over Q in an algebraic polynomial calculus with extension/square-root operations. This does **not** transfer to arbitrary CNF carry encodings or to the different fixed Rmix341 node metric. The authentic per-variable arithmetic relation is correctly encoded by local XNOR-for-zero-output and AND-for-carry clauses. This is a rigorous example that changing source encoding and proof calculus can collapse proof cost, not a contradiction of Alekseev or a P-vs-NP result.

**Independent controls:** standalone Python producer/RES replayer 872 assertion groups, independently written no-import JavaScript checker 781 assertion groups, n=1..8,12,16,32,64. Both-label controls use c_1=0 (all-zero satisfying extension) and final c_(n+1)=1 (all-one satisfying extension); exact model counts 0/1/1 for n<=7. Every indispensable source deletion SAT; malformed DIMACS and corrupt/truncated proof checks reject. Rmix341 itself was not changed. Certificate length and checker work O(n log n) with explicit clause-index access; implementations materializing full source have all-phase rho>=1, not an FLMV improvement.

**Falsifiers:** F1 rational algebraic hardness automatically transfers across bit-blasting = FALSIFIED; F2 mixed algebraic rules are necessary to shorten the proof = FALSIFIED, pure RES suffices; F3 both-label zero-output boundary = checked; F4 new nonaffine extension-resistant superpolynomial minimum = OPEN.

**Search/duplication:** inspected user-approved 12:04 refocus, issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, MIXED-TSEITIN341, LSPV-3 ONECYCLE351/SPLIT353 and LSPV-4 MIXED-SPLIT350. External primary sources: Alekseev (2026), Peitl/Szeider (2021), Bryant/Heule (2021), Kiesl/Rebola-Pardo/Heule (2018). Search terms: "A Lower Bound for Polynomial Calculus with Extension Rule", "proof complexity extended resolution superpolynomial lower bounds", "BVP" and "binary value principle" in j15marti/pnp, and "resolution proof checker" and "extended resolution" in github.com/openai. No exact BVP carry-CNF mixed-optimum predecessor found; broad keyword search is not exhaustive.

**Precise next work:** (i) require proof-preserving translation theorem with overhead in the correct lower-bound direction before importing an external proof-hard family, (ii) seek a nonaffine family resisting each Rmix341 subsystem AND its combination, (iii) separately establish B3 for SAME fixed R rather than conflating a family failure with worst-case bridge failure. B1/B2/B3 and P versus NP remain OPEN.

**Published artifacts**
- [Formal LSPV-3 report](../agents/lspv-3/2026-11-02_2224_LSPV-3_BVP_BITBLAST_COLLAPSE354.tex)
- [No-import executable verifier and reproducer](../../experiments/arc/lspv3_354_bvp_bitblast_compact.js)
- [Raw results and controls](../../results/raw/arc/2026-11-02_2224_LSPV3_BVP_BITBLAST_COLLAPSE354.json)

No agent IDs, titles, schedules or task statuses were modified. Publication root reconciliation must preserve all content outside LSPV-3 markers. P versus NP remains OPEN.
