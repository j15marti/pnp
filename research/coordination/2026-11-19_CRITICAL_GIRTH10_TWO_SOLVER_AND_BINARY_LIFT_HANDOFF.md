# Shared six-role handoff: girth-10 native strict-C and binary-cover firewall (2026-11-19)

**Critical graphs:** The earlier native strict-C 150-variable, 176-clause girth-10 seed-20 candidate (4,500 attempted clauses) is now **UNSAT in two independently complete source-uniform GAC searches**, 17,107,989 nodes (R/orientation algorithm) and 7,227,289 nodes (five cyclic-window algorithm). It is connected with 528 incidence edges and exactly girth 10, but **NOT physically clause-minimal**: removing original clause index 0 leaves an UNSAT instance (independent 5,794,153-node exhaustive run). JSON SHA256 `ecb0b31b1487f8747b582d97de26e2c77e4e1b5e173d89c4c86097e0fcd402a8`.

**Red team:** The earlier independently certified 25-variable/25-clause girth-8 native-C source has a three-path incidence theta between variables 16 and 0, via pairs of physical clauses (0,22), (23,11), (3,18). Binary edge voltages on the three paths cannot make all three length-eight cycles lift to 16: (p1 xor p2) xor (p1 xor p3) xor (p2 xor p3)=0. **PROVED:** no binary 2-cover of this base has incidence girth above 8. Further, random 2-cover seed 20261119 is connected and SAT, with a complete independent 50-color strict-C witness on all 50 physical clauses; UNSAT is not preserved by arbitrary covers.

**Witness specialist:** Produce all *full physical-C deletion witnesses* for any extracted girth-10 critical core. Two complete 150-color SAT controls were already generated and individually checked after dropping the first 40 clauses, each satisfying all 136 retained original C clauses.

**Obstruction cover:** Materialize a replayable *static* UNSAT refutation for the 150/176 source. Two exhaustive deterministic GAC solvers agree but static proof acquisition, verification and compression still need accounting. No selected-row blocker assignment establishes the universal claim.

**Resource auditor:** Distinguish the completed finite runs from uniform bounds, and charge input generation (4,500 attempts), all unsuccessful branches, both answer polarities, preprocessing, proof materialization/replay and output/space. Neither the 150/176 source nor its prospective MUS is proved to satisfy the N^.195 rows/N^.65 blocks/N^.35 private promise.

**Lead:** No unrestricted SAT reduction into a critical low-row family, asymptotic time-space contradiction or P vs NP resolution. Do not transfer graph girth, deletion criticality, resolution width or 2-lift properties into unrestricted machine lower bounds.

**Next actionable milestone:** Efficiently extract a clause-minimal subformula from 150/176, preserve incidence girth>=10, then publish complete original-C UNSAT refutation and every single-physical-clause deletion witness. Separate the 2-lift theta obstruction from possible 3+ degree covering constructions.

Detailed GitHub report: https://github.com/j15marti/pnp/blob/main/research/agents/critical-graphs/2026-11-19_NATIVE_STRICTC_GIRTH10_150_TWOSOLVER_THETA_COVER.md. Full source, C++ solvers, witnesses, static verifier and SHA-256 manifest: conversation ZIP `T5C_Girth10_DirectC_TwoSolver_20261119.zip`.

**Status:** PROVED binary-lift obstruction; COMPUTATIONALLY VERIFIED girth-10 UNSAT source; FALSIFIED criticality of untrimmed source and UNSAT-preservation by arbitrary lifts; OPEN full girth-10 MUS certificates. **P vs NP remains open.**
