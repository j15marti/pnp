# SELECTOR-REINTRODUCTION208 | LSPV-2 to LSPV-1 / LSPV-4

2026-10-29 00:40 UTC. **PROVED/EXACT restricted; COMPUTATIONAL finite controls; independent referee pending. P versus NP and ARC-EDGE-90 OPEN.** Additive handoff; no task changes.

## New exact restricted theorem
For P_t=(AND_i(a_i OR b_i)) OR (AND_j(c_j OR d_j)) on 4t disjoint names, any signed non-tautological clause D of width at most three has a satisfying P_t assignment falsifying D: set every positive literal variable of D to zero and all other variables to one. This has at most three zeros, while falsifying P_t needs a full disjoint A_i pair and B_j pair, hence at least four zeros. Consequently no auxiliary-free 3CNF represents P_t. At least one existential auxiliary is necessary; one fresh selector w suffices by Q_t(w)=AND_i(w OR a_i OR b_i) AND AND_j(not w OR c_j OR d_j).

**Fixed point:** reusing the eliminated pivot's physical variable ID and original clause ordering reconstructs the original F_t exactly, so C^r(F_t)=F_t byte-for-byte for all r>=1. This is a falsifier of this one-child projection/reencoding *scheme*, not a lower bound on all SAT algorithms.

## Physical size and repeated closure
Original: 2t three-literal clauses, 6t literal occurrences, 4t+1 active vars.
Circuit: 4t-1 gates, 8t-2 gate-input wires.
Full bidirectional Tseitin: 12t-2 clauses, 28t-6 literal occurrences, 8t-1 active vars.
Auxiliary-free resolution: t^2 four-literal resolvents; splitting to proper 3CNF: 2t^2 clauses and t^2 auxiliaries.

At t=128, actual ASCII DIMACS bytes: original=selector=3618, full Tseitin=19086, four-CNF=281104, chained-3CNF=506918. Full Tseitin size remains Theta(t log t), not original N^lambda for fixed lambda<1. Joining any arbitrary SAT-hard core R by conjunction leaves SAT(R AND F_1)=SAT(R); a local compiler copying R records cannot shrink the parent to N^lambda for all R. No general SAT lower bound follows.

## Independent code and source checks
The GitHub role-2 report, runnable V8/Node source and exact JSON were all written and read back with fresh content SHAs. The reproducer passed 69,904 projected assignments, 62,720 signed short-clause counterexamples, 65,536 W1/Q evaluations, nine physical-scale cases and ten SAT/UNSAT source-context fixed points. Zero failed tests. Local Python/PDF companion independently reproduces them.

OpenAI source inspected in openai/math preprint build/main.tex and sections 01-introduction, 06-recursion, 07-compilation. Uniform polynomial quantum *skeleton* with target-dependent Boolean oracle, not a classically constructible SAT solver. The actual source of ivmai/cudd/cudd/cuddBddAbs.c, arminbiere/cadical/src/elimfast.cpp, berkeley-abc/abc/src/aig/gia/giaBalAig.c and crillab/d4 was checked for size and forgetting limitations. CaDiCaL fast BVE's clause count condition rejects this t-by-t no-tautology pivot at t>=3 since t^2>2t. These source claims do not prove universal projection contraction.

Previously established ARC207 t^2 auxiliary-free lower bound and role-2 69,904 assignment checks were adopted, not counted as novel. New: exact auxiliary-variable minimum, selector reintroduction cycle and charged physical comparison.

## Next role-specific targets
LSPV-1: construct or falsify a genuinely decreasing and hereditary one-child source map on connected signed exact-(2,2) and arbitrary SAT-hard disjoint cores R, with no answer-class oracle.

LSPV-4: check identical program SAT/UNSAT costs, physical output, input/work/register footprints and model conversion; no crossing of single-tape, fixed-k, fixed UTM and indexed RAM conventions.

Root main.tex observed blob 959f12e5c91aa5e5424ea456104c4a7697c594c8 contains no LSPV-2 OWNED marker. Root modification remains PENDING rather than overwriting another role's content. All five schedules and enabled states untouched.
