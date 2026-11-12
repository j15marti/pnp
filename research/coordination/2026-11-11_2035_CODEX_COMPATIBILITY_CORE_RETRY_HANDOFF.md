# Compatibility retry: exact degree transfer and global algorithms

Date: 11 November 2026, 20:35 PST
Status: **P versus NP remains open.**

## Why this retry differs

The user asked to try again after the adaptive all-prefix-total collision obstruction. This continuation deliberately builds compatibility constraints with locally valid prefixes that have no full continuation. It recovers the exact selector encoding from ATC2, derives a sharper global algorithm, and proves an exact algebraic degree dichotomy.

## Exact recovered construction

For source CNF F with m>=1 nonempty clauses, introduce one selector per literal occurrence. Add pairwise exclusions within each clause and implications selector -> corresponding literal. These are Horn binary clauses. Add odd parity on each selector block.

For proper3CNF: n+3m variables, 6m Horn clauses, m disjoint affine rows of rank m. The projection onto original variables is exactly F. A source witness lifts by selecting one true literal per clause; any target witness projects back.

Actual sources read:

- research/explorations/sat-composition/2026-11-11_AFFINE_TABLE_COMPOSITION2/compatibility_continuation.tex, blob 3809296b0a5f6ea85fc03bf1d8441b04e3017585.
- experiments/sat_composition/2026-11-11_dependent_compatibility/composition_solver.py, blob 575a6aec2c49e21452f1d6b28d6aca87a8c66f85.

The compiler is a recovered component, not a newly invented source attribution.

## New exact transfer: restricted degree

Let M_F be the Horn model family and a_F the parity-acceptance function. Let D(F) be its minimum multilinear GF2 degree on M_F, with zero assigned nonnegative degree0.

$$
D(F)=
\begin{cases}
m,&F\text{ SAT},\\
0,&F\text{ UNSAT}.
\end{cases}
$$

Proof: the product of m block parity sums supplies degree at most m. If F is SAT, fix a satisfying original assignment and one true-literal selector in each clause. Set other selectors0, leave those m chosen selectors free. The entire Boolean m-cube remains inside the Horn model family, and acceptance restricts to AND_m, which has degree m. If F is UNSAT, acceptance is zero on all Horn models.

Consequences:

- On the recognized image with construction metadata, degree below m is exactly UNSAT.
- Degree0 recognition is coNP-complete.
- Computing D(F) in P is equivalent to SAT in P.
- Each fixed quasipolynomial logarithmic degree transfers.
- This is hardness of determining a semantic degree property. Numerical degree m does not lower-bound runtime.
- Connected easy source F_m = AND_j(a OR u_j OR v_j) has immediate model a=1 but D(F_m)=m and rank m.
- Horn closure never creates selectors, so every accepted closure needs at least m selector seeds; that lower bound concerns this closure procedure, not all witness algorithms.

## Stronger controller for this image

For each original variable x_i, let P_i and M_i be the sets of clauses satisfied by x_i=1 and x_i=0. The DP stores reachable covered-clause subsets S, with successors S union P_i and S union M_i.

There are at most 2^m states per variable. This gives a full decision and witness algorithm in 2^m poly(N), including selector lift. General widths are allowed and variable relabelling is charged.

Thus rank m=O(logN) is polynomial on this exact image. This improves the coarse N^{O(m)} closure bound. For proper3CNF, however, the closure universe U=n+3m is at most6m, so the preceding refined binomial bound already gives2^{O(m)}. The new controller improves the explicit base to2 and is especially useful for unbounded widths, where U can greatly exceed m. Under the existing actual-extension/reconstruction/replay hypotheses, a squared-log H amplifier needs m_*=Omega(log²N); this qualitative requirement is already consistent with the refined constant-width seed bound.

## Actual dead-prefix example

The five-clause formula in the report has (x OR y OR z) followed by all four (NOT x OR ±a OR ±b) clauses. It forces x=0 but has12 total models. Selecting x in the first clause is locally feasible and has no full continuation.

The DP returns (x,y,z,a,b)=(0,0,1,0,0), using26 attempted transitions and at most6 states. This is a concrete counterexample to inferring mandatory unrestricted branching from a dead local prefix.

## Collision normal form with compatibility

For each adaptive efficiently invertible permutation P_i on r_i+1 bits, every ordered truncated collision has unique coordinates (z_i,b_i):

$$
u_i=P_i^{-1}(z_i b_i),\qquad
v_i=P_i^{-1}(z_i(1-b_i)).
$$

Keys may depend on earlier pairs. Sequential inverse evaluation gives a polynomial bijection E from all label/orientation strings to valid primary chains.

Arbitrary global compatibility K becomes K(E(z,b)). If compatibility is simply source F(z), source SAT and compatible-chain search have efficient witness maps. Dead prefixes can occur, but a source model lifts without backtracking. Fixed-seed replay still rules out the proposed amplifier for this architecture.

Removing efficient inversion identifies an exact alternative: for P(x,b)=(Q(x),b), prescribing the collision label y makes collision search equivalent to finding Q^{-1}(y). No inverse lower bound is proved; for a fixed uniform permutation family the inverse-bit language is in UP intersection coUP. If Q is arbitrary circuit input, bijectivity is a promise. A known preimage used to generate y is already a replay shortcut.

## Semantic scope

Ordinary explicit existential Boolean DAG constraints compile once to SAT. Hypothetical polynomial SAT then handles any explicit depth with a polynomial bound in total description size.

Ordinary SNSAT has actual semantic SAT/UNSAT answer bits. Deciding its last bit is P^NP-complete. False answers cannot be guessed freely. An explicitly listed chain still evaluates with one SAT call per stage; polynomial and fixed-degree quasipolynomial upper bounds remain in the same respective class. Succinct recursion and growing alternation require separate paid analysis.

## Computational record

Selector controller:394 formulas,385 SAT and9 UNSAT, zero mismatches. All256 subsets of the8 proper3 clauses on3variables were exhausted. Additional128 cases use seed20261111, with9 hostile controls and the dead-prefix example. Projection checks cover5372 source assignments and273481 local selector patterns. All385 lifted witnesses verify.

The SAT degree audit checks all32 points of an AND5 subcube. The UNSAT degree audit enumerates all6912 Horn models of the8-clause contradiction and finds zero accepted models.

Collision coordinates:256 coordinate strings and256 independently forward-enumerated valid primary chains match. All4352 forward candidate-pair tests and1024 completed primary/padding checks agree. The proper compiled instance has201 variables and805 clauses;8 of16 first oriented prefixes are dead. There are64 compatible primary chains and256 accepted padding completions.

Recorded runtimes: about1.02 seconds and0.478 seconds.

Script SHA256:
- selector DP:5bc4907bd3e865d221433d9819405e5c7a657ce3a2f51c7a2632ce8fc65b39d5.
- collision coordinates:068118e72ad3d923e47bca3701f4afd6151ef27c3a3970e094789367343d076e.
- prior verified collision dependency:9197bc468d255e7746f6d2f6c8a421c6186bce887584ef12212c8cd26c6a5ff8.

Finite results are COMPUTATIONAL; the report contains separate symbolic proofs with independent temporary-agent review. No finite check measures H or proves a runtime lower bound.

## Validation and reconciliation

Root snapshot inherited from the ongoing survey:ca1c40a11155442a7ecdf74d0e05db3f83abae9a. Both trackers and governing instructions were reviewed earlier in this same active continuation, with direct reads of the exact new compiler and source.

Local report/preflight hygiene passed on the partial snapshot. LaTeX structure, citations, and code/result hashes were checked. The previously diagnosed missing pdflatex format prevents claiming PDF render validation.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to load-bearing OPEN status. No root ownership region, previous timestamped report, schedule, or automation is changed.

## Single next target

A lower bound on the uniform computational cost of the exact global compatibility core or degree-decision problem, respecting the available 2^m controller. The number of dead prefixes, rank, degree, and seed count do not by themselves exclude global state compression.

## Artifacts

- research/agents/codex/2026-11-11_2035_COMPATIBILITY_CORE_AND_DEGREE_TRANSFER.tex
- research/agents/codex/2026-11-11_2035_COMPATIBILITY_CORE_AND_DEGREE_TRANSFER_refs.bib
- research/coordination/2026-11-11_2035_CODEX_COMPATIBILITY_CORE_RETRY_HANDOFF.md
- experiments/review/compatibility_selector_dp_20261111.py
- experiments/review/compatibility_collision_coordinates_20261111.py
- results/raw/review/2026-11-11_COMPATIBILITY_CORE_RETRY/selector_dp.json
- results/raw/review/2026-11-11_COMPATIBILITY_CORE_RETRY/collision_coordinates.json
- results/raw/review/2026-11-11_COMPATIBILITY_CORE_RETRY/dead_prefix.cnf
