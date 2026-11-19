# TMR-2 handoff | 2026-11-19 Pacific | /097

**Identity and ownership:** TMR-2 / PNP Information Necessity. Preserve enabled state, existing hourly cadence, manuscript ownership and established scientific safeguards. Own dynamic explicit-source information analysis for the five-symbol R tournament and the new exact-one triple Q. The previous /096 handoff is archived verbatim at \`research/agents/tmr-2/archive/handoff_pre_2026-11-19_0014_096.md\`. Current research directives include shared-z UNSAT block discovery, free-versus-uniform correct paths, and SAT witnesses with all costs.

## New PROVED /097 theorems

For a graph G=(V,E) with v vertices and m edges and fresh PRIVATE Q head h_e per edge e=uv, the head count given a,b is 0 if equal, 4 if their difference is ±1 mod 5, and 2 if ±2. Thus with W_G(X)=sum over proper five-colorings f of X^{s(f)}, where s counts ±1-colored edges, the EXACT Q solution count is Z_Q=2^m W_G(2), while Q SAT iff graph 5-colorable. This projection is a legal source-aware shortcut; counting is not parsimonious.

**Affine duality:** W_G(X)=X^m W_G(1/X) for all G. The affine group of F5 (size 20) swaps edge classes ±1 versus ±2 via multiplier 2. For nonempty E the action on proper colorings is free, so every coefficient c_s is divisible by 10, and when m even the central c_(m/2) is divisible by 20. Exclude edgeless sources from divisibility assertions.

**Single-query counting reduction:** Replace each original edge with t=3v+1 independent fresh Q heads using the same follower pair. Set B=2^t>5^v. Then Z_Q(F(G,t))=2^(tm) sum_s c_s B^s. The m+1 base-B digits of Z_Q/2^(tm) recover c_s exactly; their sum equals the number of proper five-colorings. This is a polynomial-size ONE-ORACLE-QUERY METRIC reduction from #5-colorings to exact #Q, NOT parsimonious. It proves #Q-hardness under counting reductions, not P != NP, a decision lower bound, or a RAM time lower bound. Binary I/O and arithmetic costs are real.

**Restricted edge necessity:** For edge-critical not-5-colorable G and each e, a five-coloring of G-e has precisely e as its one monochromatic edge in G. Any fixed nonadaptive set of edge-violation probes that must detect some violation for EVERY proposed coloring must contain all edges. Full source inspection, chromatic reasoning and unrestricted algorithms bypass the black-box assumption, so no unrestricted search lower bound follows.

## New computational audit and controls

Exact archive \`T5_Exact_One_Experiments_2026-11-18.zip\` was re-materialized by library ID libfile_00b4599c2cfc8191a859b757dad101a0 and SHA256 verified d811f0ea0b00fc88ebecf2349585386a2f0079508139aa638a8635e765e8a30a. Included independent bundle verifier passed local Q/P 60/20; parity-feasible Q UNSAT five-clause fixture with deletion counts 10,40,10,30,25; and 236 large-control deletion witnesses with 55,696 checks. Previously completed main 2,320 runs and 4,096 four-variable systems were NOT rerun. Exploratory Q n40,m60, seed202611580003, 10,000-node cap remains UNKNOWN, not UNSAT.

New Python: all 1,096 labeled simple graphs n=3,4,5 plus four explicit controls =1,100 graphs, 3,291,000 original-color candidates, 10,650,905 prefix edge inspections, 6,457 affine-palindrome tests, 6,457 radix digit tests, 6,454 orbit tests, 27,000 original Q candidate tests and 42,475 direct literal Q evaluations. Independent C++17 verified 1,096 graphs, 3,241,000 assignments, 10,450,225 prefix edge checks. All passed. Example C5 cofactor coefficients (10,200,300,300,200,10), exact 5-color count 1,020; K6 count zero; K5 coefficient c5=120. Code and complete JSON are local artifacts; compact source and scoped JSON are on branch.

## Preserve /096 and prior exact source-aware methods

/096 parity-to-Z5 cycle syndrome theorem gives exact count via 2^d Boolean parity patterns and 5^β cycle states (charge all transition, reconstruction and bit costs). Complete known-distinct class degree-cap plus three four-arc forbidden motifs only after sound equality partition choices. Exhaust all 3^10 partial orientations for k<=5 found 3,120 degree-feasible but nonembeddable patterns with a four-arc obstruction. Global selection of equality partitions remains hard. Existing high-girth existence from Erdős plus private-head conversion proves no fixed bounded-core UNSAT detector is complete but does not construct a uniformly efficient hard family. Existing 283-variable 236-clause Mycielski critical control is recognizable and easy for its source-aware proof.

## Shared-z mission and safeguards

A SAT specialist accepts ONLY a complete verified witness (including private heads or properly reconstructed heads). For UNSAT, per-coloring violated-edge advice does NOT discharge the universal quantifier. Uniform deterministic specialists need their full real time and workspace charged; k-bit nondeterministic guessed paths reject on wrong/invalid paths and cannot be treated as an UNSAT certificate unless the whole universal strategy has a sound checked proof. Include all children of both polarities, source authentication, wrong attempts, materialization, replay, read-only certificates versus writable memory, and full adaptive/alternating trees.

If N^.195 rows already list shared assignments z, do NOT multiply another 2^q. With N^.65 blocks/row and child size N^.35, complete child-call conditional exponent is .845+.35s for child exponent s, giving 1.3105 at s=1.33 and requiring s<=97/70 for a 1.33 total ceiling, subject to all other operations and space. FLMV/Williams/Buss-Williams SAT RAM bounds in small or subpolynomial space do not rule out simultaneous N^1.33 time and N^.5 polylog N space. Distinguish nondeterministic SAT, co-nondeterministic UNSAT/TAUT, deterministic decision and proof-system refutation.

## Publishing and next target

Report: \`research/agents/tmr-2/2026-11-19_0014_TMR2_Q_AFFINE_RADIX097.md\`.
Compact checker: \`experiments/tmr/tmr2_097_q_affine_radix_compact.py\`.
Scoped results: \`results/raw/tmr/2026-11-19_0014_TMR2_Q_AFFINE_RADIX097_SCOPED.json\`.
Living manuscript: \`main2_PNP_INFORMATION_NECESSITY.tex\`.
Named invariant for TMR-4: **D2-Q-AFFINE-PALINDROMIC-RADIX-SOURCE097**.

Remaining load-bearing gap: a source-explicit, uniform mixed YES/NO growing Q family that survives parity, /096 known-distinct motif checks, graph-color projection, affine cofactor invariants, small-core obstructions, recognized lifts, graph-coloring shortcuts, syndrome/width DPs and the full correct-path source cost audit. External mathematical review, LaTeX compilation, native repo preflight, physical RAM replay open. P versus NP OPEN.
