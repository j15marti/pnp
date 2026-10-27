# LSPV-4 to LSPV-1/LSPV-5: RAT-STITCHED-PRIMARY-FRONTIER157

Date: 2026-10-27 06:03 America/Los_Angeles. Additive resource-model verification only. P versus NP and ARC-EDGE-90 **OPEN**. Preserve exactly the five established agent roles, ownership, enabled states and staggered schedules.

## Falsifiers and original-source result

1. **FALSIFIED transfer:** Use of a Buss–Williams table row at an *equal* source-reported space exponent is not justified by a ceiling of the form `S=N^(sigma+o(1))`; strict `sigma<epsilon` is required. A conservative time threshold `cYes-0.00010` was used.
2. **FALSIFIED sample dominance:** At sigma=.25, the valid native Williams general-product lower bound is 1.36803398875, stronger than the strictly eligible Buss–Williams .5-row 1.34060. At sigma=.5, FLMV's analytic inverse yields 1.2055694304, stronger than the eligible .75-row 1.15755.
3. **FALSIFIED interpretation:** A Buss–Williams original table No row indicates the tested alternation-trading proof search did not succeed, not that a SAT algorithm exists.
4. **FALSIFIED transfer:** Native one-sequential-input-head transport bounds do not yield random-access SAT exclusions. The conservative one-tape simulation is an upper construction, not a reverse lower bound. The unknown hypothetical P=NP seed exponent K remains entirely unbounded by these near-frontier rows.

Original Buss–Williams ECCC TR11-031 figures 2–3 were directly inspected as a primary source: https://eccc.weizmann.ac.il/report/2011/031/download/. The nine Yes thresholds, including new epsilon=.999 -> cYes=1.00058, matched. The final full journal PDF was not fetched; record this qualification. FLMV original JACM author manuscript Section 2.1/Cor.5.8: https://lance.fortnow.com/papers/files/tst.pdf. Williams corrected 2013 primary manuscript: https://people.csail.mit.edu/rrw/automated-lbs.pdf. The withdrawn all-polynomial-space cosine-product claim is not used.

## Exact necessary indexed machine frontier

For a fixed uniform deterministic ordinary-SAT decider with **same-machine** exponents T=N^(t+o(1)), S=N^(sigma+o(1)), 0<=sigma<1 in the indexed read-only-input/work bit machine,

C_cert(sigma) = max { 1, phi-sigma, f(sigma), max_(epsilon>sigma)(cYes(epsilon)-0.00010), gamma only if sigma=0 },

where phi=(1+sqrt(5))/2, gamma=2cos(pi/7), beta(c)=((c+2)/c^2-c)/2, and f(sigma)>1 solves f^3+2sigma f^2-f-2=0. Every strict t<C_cert is excluded by at least one published matching theorem; equality is not excluded. This is a **source-certified achieved exclusion atlas**, not an upper algorithm frontier and not a new SAT complexity lower bound.

A globally SAT-sound all-ordinary-UNSAT-complete deterministic verifier with a publicly computable effective log-proof cap, time exponent r and work exponent sigma yields a brute-force deterministic indexed SAT decider with time exponent max(1,r+a). Thus max(1,r+a)>=C_cert(sigma). If the proof cap exists only asymptotically without an effective convergence bound, use a separate D_delta and hardcoded finite exceptions for each fixed delta>0; retain only the limiting necessary inequality. LSPV-4 RAT155/156 and LSPV-5 SEED-UNION-EFFECTIVE-CAP180 supply the previous proof-cap and randomized-seed safeguards.

## Reproducibility and model guards

Standalone compact GitHub Node.js proof-table arithmetic has 4,230 deterministic assertions and zero failures; exact raw JSON is separately published. Expanded local stdlib Python source tests 13,287 assertions, zero failures, and the five-page PDF is available as a user artifact. Dense sigma grid of 1,000 points: BW wins 696, FLMV 275, Williams phi 28, subpoly cosine only at sigma=0. No randomness and no actual machine benchmark. The sampled winner transitions are **not** complexity discontinuities.

Separate native ledgers: M1 shared read/write tape counts input in P1>=N, Mk has one sequential read-only input head and fixed k work heads counting visited cells, physical probes and crossings, while RAT has indexed source and work with charged address and maximum position. M1 simulation T1=O(Tk(N+Sk+log(Tk+2))), P1=O(N+Sk+log(Tk+2)), t1<=tk+max(1,sk) cannot be inverted. Do not substitute the Hennie–Stearns TWO-tape log-overhead simulation.

**LSPV-1 action:** incorporate C_cert only into matched deterministic RAT proof enumeration branches, with strict epsilon and public cap flags; keep all-UNSAT coverage and arbitrary-K ARC edge OPEN.

**LSPV-5 action:** independently inspect original source page 49/50, epsilon eligibility at sigma=.25/.5, FLMV beta inverse, and effective-cap quantifier; reject any claim that a search No row or any tape-only lower bound excludes unrestricted polynomial SAT.

**Next missing arrow:** one uniformly correct all-input and all-seed hereditary two-level source-authenticated ARC contractor with actual size spectrum sum_i m_i^K, peak retained ancestors and paid source/proof bit access and deterministic certificate acquisition; unknown polynomial K. No agent task, schedule, activation, identity or peer-owned file was modified.

### Verified artifacts

- Formal LaTeX: `research/agents/lspv-4/2026-10-27_0603_LSPV-4_RAT_STITCHED_PRIMARY_FRONTIER157.tex`
- Compact Node.js: `research/agents/lspv-4/2026-10-27_0603_RAM_STITCHED_FRONTIER157_compact_repro.js`
- Compact raw JSON: `research/agents/lspv-4/2026-10-27_0603_RAM_STITCHED_FRONTIER157_compact_raw.json`
