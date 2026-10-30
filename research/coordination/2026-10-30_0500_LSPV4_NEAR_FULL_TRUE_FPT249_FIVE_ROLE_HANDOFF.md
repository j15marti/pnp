# LSPV-4 NEAR-FULL-TRUE-FPT249, five-role handoff

Date: 2026-10-30, 05:00 America/Los_Angeles. Active coordination: https://github.com/j15marti/pnp/issues/3 . User's 2026-10-29 21:53 clause-extreme clarification remains primary.

## Established restricted result

**PROVED/EXACT, mathematical referee pending; known technique combination.** For every globally coherent ordinary SAT assignment, the original clauses with t=1 or 2 true literals form a vertex cover of the original opposite-polarity clause conflict graph (SS-incompatible graph). Consequently any matching of k+1 source conflict edges excludes all SAT assignments with at most k middle clauses, but NOT all SAT assignments. Recursively branching on an uncovered source conflict edge, forcing every outside clause to full S, and checking at most 3k remaining source variables exactly decides MiddleSAT3(F,k) in O(N^2+2^k N+k16^k) deterministic indexed word-RAM work, using O(N+m^2+k) streamed working words. This is a restricted parameterized problem, not arbitrary SAT. Uses known graph vertex cover branching and Kullmann clause conflicts.

**Sharp restricted firewall.** Every satisfying proper signed exact-(2+,2-) 3CNF has at least 3m/4 middle clauses; equality is attained in the connected H1 strict22 SAT source (n=6,m=8, M=6, four witnesses). For strict22, k=o(m) misses ALL SAT witnesses, so a parameter-budget NO must never become a full formula UNSAT assertion.

**FALSIFIED/RETIRED.** Matching and SS conflict-cover feasibility alone decides ordinary SAT; failure of the small-k parameterized test proves UNSAT; this FPT parameter is uniformly small on the NP-complete strict22 source class.

## Mandatory indexed experiment and resource checks

For every ORIGINAL clause C_j and original signed occurrence x_(i,j), the raw source records local all-TRUE S_j, its inverted U_j, local all-FALSE U_j, its inverted S_j, the exact original indexed SS/SU/US/UU matrix, and bounded triple modes. It separately records globally coherent all-zero/all-one and every included intermediate flip/complement, per-original-clause t_j=0/1/2/3, sound original source-parent resolution forbidden cubes, source-checked SAT witnesses, and complete replayed UP-DPLL UNSAT refutations. Original occurrences share their global variable identity.

Fourteen SAT/UNSAT hostile controls with 4,128 pair modes, 472 triple modes, 70,536 complete coherent assignment/complement comparisons, 438 original signed occurrences, 57 parameter-budget tests and 108 checked source certificates passed. Independent Node.js checker reproduces full clause and witness assertions. The complete 912,961-byte raw JSON SHA256 is d0c3404120945373056e657420a8d9def72087f6d25be88cb0a354acbb28aef9 .

Selected same-source work including source discovery, failed branches and identical fallback: allpositive SAT 94->43, one-conflict SAT 100->49, H1 strict22 SAT 236->322 (k=2; at the sharp k=6 boundary 236->519), W1 strict22 UNSAT 12075->12290 (plus 6206 independent proof replay on either complete path), W1 two-sign-swap SAT 1670->1885, odd K4 Tseitin UNSAT 952->1196, planted dense SAT 966->1319. These are indexed logical events, not native CPU/Turing operations. Python tracemalloc peaks W1 34720 vs 36640 bytes, H1 k6 3848 vs 11440 bytes, not tape bits.

## Ownership and next handoff

Retain existing five enabled hourly tasks, no new task or role. Root main.tex owned LSPV-4 region may be augmented only against a fresh full verified blob without altering other regions; LSPV-5 remains overall synthesis arbiter. Full source data and manifest are delivered in the reproducibility zip and can be persistently uploaded to Library. Do not misdescribe raw experiment output as a free part of a SAT decision path.

**Next OPEN lemma:** Identify a source-proof carrying nontrivial 3+ original-parent forbidden partial cube surviving saturated UP and residual 2SAT, then demonstrate a uniform, fully charged time and peak-space benefit on specified unbounded matched SAT/UNSAT connected strict22 formulas. Both P=NP and P!=NP remain OPEN.
