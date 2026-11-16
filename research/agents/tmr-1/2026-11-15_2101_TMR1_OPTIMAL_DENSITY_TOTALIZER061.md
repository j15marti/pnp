# TMR-1/061 | 2026-11-15 21:01 PST | Optimal-density promise totalization, all declared CNFs

## Status and continuity

**C1c-DENSITY-OPTIMAL: PROVED/EXACT for one explicitly specified uniform width-at-most-three CNF normalizer; independent mathematical review OPEN.** This closes the previously failed general-density arrow in the TMR-1 input-to-counting chain with a new charged choice of auxiliary variable count. It neither constructs a faster SAT solver nor strengthens the conditional higher-class circuit lower bound. P versus NP remains OPEN.

This report strengthens the TMR-1/060 *scope correction* on draft PR #197. The /060 fixed choice `d=max(1,4-n)` remains valid for the actual circuit-compiler output (which already satisfies AllOccur) but does not force four-density on arbitrary declared-variable CNFs. Here we obtain four-density for every width-at-most-three input by paying for additional **forced** variables when required. No peer manuscript, retired tracker, historical main file, or agent schedule is modified.

## Precise candidate, model, quantifiers and falsifiers

**Quantifier prefix:** For every integer `n>=0`, every finite list `H` of ordered clauses of length at most three over the declared variables `x_1,...,x_n` (possibly unsatisfiable, duplicated, with empty clauses, unused variables and repeated/complementary literals), there is a deterministic uniform transformation `F(H)` with exact count preservation and a unique extension for every original satisfying assignment. Its output meets `n'>=4, m'>=2, AllOccur, IsKCNF 3, NoDup`, and also `m'<=4n'`. The original source must authenticate the declared variable count and all literal indices; no implicit truth table or counted-output oracle is used.

Falsifiers are (1) a legal dense formula with unused variables making the corrected output exceed 4n'; (2) any change to the original exact solution count, especially free variables, empty clauses or duplicate clauses; (3) duplicate outer clause lists or missing output variables, invalidating the formal predicate; and (4) an uncharged representation blowup, missing original input bit, or wrong encoding/space interface. The old fixed-d construction fails falsifier (1); the repaired one passes the symbolic inequalities below.

## Construction and exact structural lemma

Let `m0` be the number of distinct *ordered* source clauses after removing exact duplicate lists, and let `u` be the number of declared original variables occurring in no retained clause. Put

```
d* = max(1, 4-n, ceil((m0+u+1-4n)/3))
n' = n+d*
m' = m0+u+d*+1.
```

Keep the `m0` clauses in their original relative order. For each of the `u` unused old variables `x_i` append the tautology `(x_i OR not x_i)`. Introduce fresh `t_1,...,t_d*` and append the `d*` unit clauses `(not t_j)`, followed by one fresh tautology `(t_1 OR not t_1)`. Exactly one extension of every original assignment is possible, namely `t_j=0` for all j, and its truth value equals the original formula's. Thus `#F(H)=#H` on the original `2^n` assignments, including originally unused variables; no division by an auxiliary multiplicity is needed.

All added clause lists are distinct: absent-original-variable tautologies were not present in the old lists and have different indices; all fresh unit clauses are different from each other and all old lists; the final fresh tautology differs from every unit and old clause. Thus `NoDup` survives, every original and fresh variable occurs, and every output clause has width at most three. Since `d*>=1`, there are at least two output clauses, and since `d*>=4-n`, there are at least four output variables.

The exact density condition is algebraically equivalent to

```
m0+u+d+1 <= 4(n+d)  <=>  3d >= m0+u+1-4n.
```

It therefore holds by construction. Moreover, **among all integer d>=1 used with precisely these appended clause templates**, `d*` is the smallest value that simultaneously meets `n+d>=4` and the desired four-density. This is an optimality result **only for this declared architecture**; alternative encodings could be smaller.

This transformation is well-defined for `n=0,H=[]` (count 1), for `n=0,H=[[]]` (count 0), and for dense formulas with `m0>4n`. Its output variable and clause counts are `O(n+m+1)`, where m is the original number of written clause lists. For example `d* <= m0+u+4`, so no superpolynomial expansion occurs relative to an authentically explicit/unary-n source.

## Explicit strict-proper counterexample, and its repaired output

Declare `n=7` original variables and write all three-variable clauses on a three-element subset of `{x_1,x_2,x_3,x_4}` with any of the seven sign patterns except all-negative. There are `4*7=28` distinct, non-tautological proper three-clauses and the remaining three declared original variables are unused. Their conjunction forces `x_1=x_2=x_3=x_4=1`, giving exactly `2^3=8` satisfying assignments.

The /055 fixed `d=1` gives `n'=8,m'=28+3+1+1=33>32=4n'`, reproducing a failure within `m<=4n`. The corrected `d*=2` yields `n'=9,m'=28+3+2+1=34<=36`. The number of original satisfying assignments is still exactly 8, and each extends uniquely. This stronger negative control does not depend on source tautologies or repeated literals.

The prior /060 ordered-list example `n=5,m0=20,u=3` similarly changes from `(n',m')=(6,25)` at `d=1` to `(7,26)` at `d*=2`. Both examples remain SAT-easy: neither is a runtime lower bound.

## Integration into the authentic compiler -> formal input -> solver -> hierarchy chain

**C1a/C1b:** Parse all original shared binary gate-DAG bytes and emit the exact functional Tseitin clauses, counting each shared gate once. The earlier C1b compiler already satisfies `AllOccur`, so its input to C1c has `u=0` and `m0<=4n`. Then `ceil((m0+1-4n)/3)<=1`, so `d*=max(1,4-n)`: **the established `n'=V+O(1),m'<=4n'` circuit path and the conditional `12C` exponent coefficient are unchanged**.

**General C1c path:** For an arbitrary source CNF, the corrected output always has `m'<=4n'`, but `d*` can be `Theta(m0)` for dense source formulas. Consequently this is not a `2^{o(n)}` solver bound measured solely in the original declared variable count.

**C1d:** Using the pinned Anthropic `k=3` low-first encoding, the complete formal input is of length
`B_A=3+n'+2+3m'(floor(log2(2n'))+1)`. This includes unary k and n, literal indices, zero slots and their padding. Count output is exactly `n'+1` low-first bits. The external theorem requires `IsKCNF 3, AllOccur, n'>=4, m'>=2`, all discharged by the corrected compiler. The optional *density* `m'<=4n'` is a TMR-1 quantitative simplification, not itself an extra Anthropic theorem hypothesis.

**C1e/C1f:** Conditional on the pinned counting proposition and the fixed FinTM2-to-physical simulation lemma, the one-machine circuit counting ledger remains
`T=O((B_C+B_A)^4+T_M)` and `S_peak=O(B_C+B_A+T_M)`. The downstream Jahanjou-Miles-Viola/hierarchy consequence is still conditional, lies in `E^NP`, and is at most mildly superlinear as presently reconstructed. There is no NP-level nonrelativizing bridge.

## Fully charged same-realization normalizer budget

Let B be the actual bit length of a source representation writing the n declared variables in unary and every original clause with fixed-width indices. Thus `B=Omega(n+m+1)`. On **one fixed deterministic locally headed multitape machine**, scan/authenticate all source bits, check literal indices and width, deduplicate exact ordered lists by conservative pairwise comparison, mark used original variable names, compute `m0,u,d*` on binary counters, write all retained and new clauses, generate the low-first formal encoding and verify complete output length. A conservative combined upper is `O((B+1)^4)` bit steps and `O((B+1)^2)` peak writable bits for the same run; its `O(B log(B+2)))-bit output is included. Invalid encodings take a defined reject path within that budget. The mathematical #SAT brute-force enumerator used by the test script is NOT part of this algorithm.

When the source instead is the C1b DAG, compose this stage with the previously charged source validator and counted FinTM2 simulator. Shared gate values and CNF clauses count once. No input source, solver invocation, intermediate variable, address, cached record or output bit is treated as free.

## Executed finite reproduction

Executed deterministic V8 JavaScript in the tool runtime, revision `tmr1-optimal-density061.v1`, xorshift32 seed `20261115`. The published standalone Node script is assembled from the **same executed function definitions**, and the raw JSON is taken directly from that execution. It covers 520 inputs, 16,766 original-assignment valuations, 22,088 structural/semantic assertions and 4 malformed-input rejects, with **zero unexpected failures**. It includes proper three-clauses, ordered-list duplicates, empty and UNSAT formulas, DISJ_4, affine XOR, Horn and all-occurring controls, plus 512 deterministic random cases. In the heterogeneous suite the old fixed-d normalizer exceeded four-density 107 times; only the two explicit cases are claimed as counterexamples *within the original m<=4n premise*. The full symbolic proof above is independent of finite evidence.

Source: `experiments/tmr/tmr1_optimal_density061.js`.
Raw: `results/raw/tmr/2026-11-15_2101_TMR1_OPTIMAL_DENSITY061_V8_RAW.json`.
Source pins: Anthropic `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`; project /060 draft PR #197 original manuscript blob `c12cfc454410b45fbc43c560ead9036005ed33f9`.

A separate CI rerun was requested of the previously failed independent Lean workflow run `43804269099`. Attempt 2 also failed before any job step, with an empty step list. No independent Lean build or axiom print succeeded; this is an executor blocker, not a proof rejection. The original upstream comparator/nanoda result remains separate authenticated evidence. No local pnp checkout/preflight was available; no repository-wide test or Lean kernel replay was executed here.

## Four mandatory gates and hostile controls

| Gate | Status and reason |
|---|---|
| DISJ sanity | **PASS** for this syntactic/counted transformation: DISJ_4 has 81 satisfying assignments and a compact 2-CNF; no rank-to-general-circuit claim occurs. |
| Relativization | **PASS restricted** for syntactic correctness; **OPEN** for any P-vs-NP target. No nonrelativizing NP step is supplied; algebrization and Natural Proofs audits remain required. |
| Simultaneous DTISP | **PASS restricted** for the single physical normalizer upper budget, and conditional inherited whole-run upper ledger; **OPEN** for any strict forbidden-pair application. |
| Configuration counting | **NOT APPLICABLE to normalizer count preservation**; deterministic read-only-input bound `T<=2^{O(S+log B)}` remains an upper-bound-only consistency safeguard. |

Horn, dual-Horn, 2-SAT, affine/Gaussian, equality, bounded-treewidth, autarky, independent products, auxiliary/selector/padding, repeated and unused variables, unique-solution rank-one tensors, local-basis field effects and compact shared representations remain legal easy-family controls. Historical /341 stays FAIL as full UNSAT authority, /386 stays RESTRICTED.

## Independent review, publication and ONE next lemma

Symbolic construction: **PROVED/EXACT for this specific normalization architecture; independent external math review OPEN.** Finite checks: **COMPUTATIONAL**. The source counting theorem and its unrebuilt local kernels: **CONDITIONAL/OPEN for independent reproduction**. P versus NP: **OPEN**.

This report is published on existing TMR-1/060 draft branch `tmr1-20261115-independent-lean060`, pending full content readback; it does not itself attest a `main` merge. The prior /060 report and immutable raw evidence are preserved.

**ONE next load-bearing dependency:** a successful independent pinned Lean 4.33.1 build, actual `#print axioms` and dual-kernel replay, at exactly the authenticated Anthropic/Mathlib revisions, followed by a renewed same-run source-to-count interface review. Workflow run `43804269099` has two pre-step failures; do not classify either as mathematical proof rejection.

## Primary sources

1. Anthropic, `MainResults.lean` and `Solution.lean`, pinned 2026 revision: https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth .
2. Anthropic original proof verification: https://github.com/anthropics/formal-math/actions/runs/40442388505 .
3. Pinned independent attempted workflow: https://github.com/j15marti/pnp/actions/runs/43804269099 .
4. Jahanjou, Miles and Viola, *Local Reductions*, ECCC TR13-099 rev.3, https://eccc.weizmann.ac.il/report/2013/099/ .
5. Earlier TMR-1/055 compiler and TMR-1/060 density-scope report, in repository under `research/agents/tmr-1/`.
