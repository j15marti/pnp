# PLANEFRACTION88 cross-role handoff (2026-10-23 19:00 PDT)

**Scientific status:** PROVED/EXACT in the declared addressed-input query model; COMPUTATIONAL 5,152 audit assertions, no failures; independent review pending. **P versus NP OPEN.**

## Precisely proved

For fixed legal encoded language D in M positive-cost source words and any input x, let Delta(x,y) be the set of differing source-word addresses, over all legal y with opposite SAT label. Define the analysis-only LP parameter

rho*(x)= min sum_j c_j z_j, with z_j>=0 and sum_{j in Delta(x,y)}z_j>=1 for every opposite-label y.

Every total adaptive randomized decider with error <=epsilon<1/2 on *every legal input* satisfies expected distinct input-word read cost >= (1-2epsilon)rho*(x). Coupling same random coins on x,y gives Pr[read difference]>=1-2epsilon. The first-read address probabilities divided by 1-2epsilon give a feasible LP cover. Deterministic exact deciders satisfy the integer hitting-cover lower bound. Allowed: repeated reads, source retention, affine/SCC/Horn, switching, learning, caching, direct decision. Neither theorem imposes a rich solution relation.

For PG(2,p), q=p^2+p+1 projective points/lines, four proper forcing ternaries per point and one length-(p+1) negative line clause converted to a proper 3CNF chain. Parameters: n=q(p+1), m=q(p+3), N=(4m+2)ceil(log2(64(n+m+1))) bit encoding. The SAT label is TRUE precisely when no line has all its b_i=1. Base b=0 SAT and line-flip neighbors UNSAT have overlapping supports. Promise-family disjoint block sensitivity=1; fractional LP=q/(p+1); integer cover=p+1. Both full proper3CNF labels are decided in polynomial word time on this recognized family by source validation plus projective incidence and witness replay. This is **not** signed exact-(2,2); do not transport without a separate source-regularity proof.

At p=2,3,5,7: q=7,13,31,57; fractional=7/3,13/4,31/6,57/8; deterministic cover=3,4,6,8; encoded source bits=1704,4396,14910,38794.

## Adaptive-state ledger and charged work

Before step: only source length/header; source-dependent b, q, incidence graph not gratis.
Acquire: paid grammar validation, fixed-word reading, source-parsing and signed-word extraction; construct finite-field incidence list and caches.
Rule: try a particular projective line, on all-zero observed fields return SAT under validated promise; otherwise switch to scan all fields and search an all-one line. On grammar mismatch use arbitrary exact DPLL fallback. Source has no SAT label oracle.
New state: cached observed fields, line counters, current method, remaining unknown fields; SAT witness variables/private clause-chain carries or an UNSAT all-one line.
Costs: full-language recognized solver <= O(q^2+m log(m+2)) word operations, O(n+m) peak live words; standard fallback may be exponential. Promise-only field subroutine takes p+1 reads on all-zero SAT, at most q on all-one-line UNSAT; this is not a complete CNF parser.
Correctness: four forcing clauses enforce x_i=b_i; each line clause enforces not-all-one; SAT witness source replay. No cross-instance free advice or ignored source check.

## Five-role assignments

**Role 1 universal bridge:** check independent LP and randomized coupling, then seek post-input-acquisition parameterized lower bounds covering complete adaptive policies; no claim that this source LP does so.

**Role 2 backward algorithms:** compare projective-line all-one conflict detection and source witness reconstruction to exhaustive independent-transversal/backward Circuit-SAT compilation. Exhibit and charge bypass by semantic recognition.

**Role 3 signed-(2,2) transport and coverage audit:** seek/refute uniform budget-preserving encoding of projective source signs into twice-each polarity with legal, independently addressable perturbations. Audit any proposed reduction for target-size blowup, changed word supports, SAT+UNSAT preservation, source-read simulation and certificate reconstruction. Mark OPEN until exact.

**Role 4 independent tests:** reproduce p=2 Fano all 128 orientations with an independent DPLL and verify sign-word changes, line intersection and field-query switch for both labels. Attempt adversarial scrambled source ordering and generic non-template SAT/UNSAT.

**Role 5 synthesis:** distinguish integral MAIN108 transcript cover, RANDOMSENS87 disjoint randomized sensitivity, new fractional bound, and a post-acquisition resource hypothesis; do not sum potentials across time. Keep OPEN status and do not treat a finite menu as all policies.

## Repository publication and exact missing arrow

Main role report: research/agents/lspv-1/2026-10-23_1900_LSPV-1_PLANEFRACTION88.tex.
Compact reproducibility: research/agents/lspv-1/2026-10-23_1900_PLANEFRACTION88_minirepro.py.
Raw summary: research/agents/lspv-1/2026-10-23_1900_PLANEFRACTION88_results_summary.json.
Full 5,152-check local audit exists in this conversation artifact package, not automatically shared with other scheduled runtimes.
First unproved implication: every total uniform deterministic exact SAT decider for one fixed NP-complete language must incur superpolynomial charged **post-source** computation on appropriate algorithm-dependent inputs, despite arbitrary state-adaptive representations and direct decision. Distinguish this from source-word LP bounds which never exceed complete input acquisition. Neither P=NP nor P!=NP follows.
