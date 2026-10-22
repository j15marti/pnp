# MINIMAL-CORE-SOURCE-COVERAGE75 handoff

Timestamp: 2026-10-22 23:48 KST

**P versus NP OPEN. P versus RP OPEN.**

## Established restricted results

For the full-cover clauses `C_a`, deleting `C_a` leaves unique shared witness `a`. Hence every block-level UNSAT core is the full parent. Soundness then forces every ordinary resolution refutation to use every input clause; a standard explicit proof has at least `2^k=N/Theta(log N)` source references and the canonical refutation has `Theta(N)` literal materialization.

Counting also shows that some dense exact forbidden-membership functions require fan-in-two circuits of size `N^(1-o(1))`. This obstructs an exact universal membership-circuit representation, not arbitrary SAT decision.

## Retired generic repairs

- small extracted source-block UNSAT cores;
- ordinary explicit resolution certificates as `N^beta` ARC children;
- exact fixed-power sublinear membership circuits for every dense source table;
- transferring proof materialization to ordinary KT, unrestricted time or RP separation.

## Open constructive burden

Produce a non-subset, source-aware semantic constraint of length `N^beta`, exact on all inputs and hereditary under recursion, with source probes, validation, encoding, failed calls and peak space charged. Macro/range proofs must expose expansion and source-validation costs.

Finite audit: 1,404,454 checks, zero failures. Full report: `research/main/2026-10-22_2348_MAIN_MINIMAL_CORE_SOURCE_COVERAGE75.md`.
