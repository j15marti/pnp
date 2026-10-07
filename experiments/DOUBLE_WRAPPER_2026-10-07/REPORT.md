# Double WRAPPER: forward alternatives with recursive evaluation

Date: 2026-10-07. Status: implemented exact prototype; conditional resource target remains open; no P versus NP separation.

## Result

A forward inner wrapper now constructs a genuine AND/OR DAG of small standard SAT instances without calling a SAT solver. The outer wrapper recursively evaluates unresolved leaves using the same construction. This fixes the specific dependency-interface problem of asking a large SAT question to decide which route to construct. It does not fix the worst-case cost of constructing all the alternatives, their number, or their memory footprint.

This is a new explicit prototype, not a reconstruction of unavailable original transition code. Its basic algorithmic ingredients are established branching, unit propagation, component decomposition and caching. Its novelty here is the experimental interface and accounting in this project, not a new general SAT algorithmic theorem.

## Literature clues and scope

1. Mählmann, Siebertz and Vigny, Recursive Backdoors for SAT (2021), introduce recursive backdoors based on recursing separately into components created by assignments. This is the closest structural match to the proposed double wrapper. It is evidence for the architecture, not a general low-cost separator theorem.
2. Dreier, Ordyniak and Szeider, SAT Backdoors: Depth Beats Size (ESA 2022), give FPT approximation algorithms for backdoor depth into Horn/Krom and obtain linear-time SAT algorithms when that depth is bounded. This suggests tracking depth and component structure rather than a single global set of branching variables. It does not make unrestricted formulas bounded-depth.
3. Sang, Bacchus, Beame, Kautz and Pitassi, Combining Component Caching and Clause Learning for Effective Model Counting (SAT 2004), explain exact reuse of dynamically exposed disjoint components. Our prototype uses exact normalized formula keys, not hash collision as an equivalence test, and does not implement clause learning.
4. Williams, Self-Improvement for Circuit-Analysis Problems (STOC 2024), discusses efficient representation of the assumed algorithm inside problem instances and explicitly poses extending self-improvement toward the polynomial regime as an open problem. This remains adjacent to the missing use of hypothetical solver code. The present implementation is entirely source-based and does not supply that step.

Primary sources and BibTeX are included in REFERENCES.bib. Searches were performed during this run. The source matches support restricted structural algorithms; no source found supplies the requested universal Williams-landing compiler.

## Exact combination rule

Choose boundary variables B using source structure alone. For each assignment a to B, form the restricted CNF F|a. Split it into components C_(a,j) on disjoint remaining variable sets. Then

SAT(F) = OR_(a in {0,1}^B) AND_j SAT(C_(a,j)).

Proof: existentially enumerate the assignment on B, then use variable disjointness to combine independent witnesses within that assignment. False constants invalidate the corresponding alternative; empty conjunctions are true. Unit propagation preserves satisfiability before further decomposition. Bijective variable renaming preserves each component's SAT answer. Duplicate normalized components can share an answer node; duplicate terms in AND or OR are idempotent.

The same boundary assignment must be applied to every component in an alternative. The implementation explicitly checks the elementary hostile control x AND NOT x: both one-clause components are separately SAT, but their conjunction is UNSAT. A naive AND of independent SAT bits would be incorrect. The code only splits actual disjoint residual components.

This theorem is unconditional and elementary. It establishes correctness of the interface, not an efficient universal construction.

## Architecture

The inner wrapper uses an iterative work list. It performs unit propagation, structural component tests and forward branching; it has no calls to the reference SAT routine or outer solver. It stops a branch at a constant or at a CNF whose explicit encoded bit length is at most floor(N^(2/3)), where N is the input size for that invocation. All logical DAG edges lead to reduced residuals or proper independent components. Node-number order is not used as proof of acyclicity.

The outer wrapper recursively invokes the inner wrapper on unresolved leaves and memoizes their SAT answers. It asserts that each recursive leaf input is strictly smaller. For decision-only semantics, caches may erase provenance; they do not promise to reproduce a unique wrapper transcript or a fixed original witness.

Audit edges record local variable assignments, one of the four typed labels TRUE/NOT TRUE/FALSE/NOT FALSE, its prime, and a hash tag. Variable identifiers are local to normalized formulas. Source-local formula keys and assignment edges ground correctness. Prime/hash equality is not used to infer semantic equality or to certify a global SAME_REALIZATION history.

The inner wrapper is allowed to derive constants by unit propagation and exhaustive branching. Therefore zero SAT-solver calls does NOT mean zero SAT work. The expensive work may occur entirely within construction, which is why it is counted separately.

## Variants and experiment design

All variants use identical unit propagation and normalized formula caching:

* flat: choose the most frequent variable, branch, no component splitting;
* components: additionally split existing independent components;
* separator: also search all one- and two-variable deletion sets for structural separation;
* separator_fast: restrict separator candidates to the four most frequent variables, at most ten candidate sets per connected state.

The separator score minimizes an upper estimate of largest projected component encoding, not satisfiability or witness quality. If no candidate disconnects the variable graph, it falls back to a single frequent variable. These are prototype heuristics, not implementations of the published FPT backdoor-depth algorithms.

The 296 cases comprise all 256 subsets of the eight full-width three-literal clauses on three variables; 24 random cases at 5, 8 and 12 variables; 10 planted cases with two shared boundary variables and four three-variable blocks; and 6 controls (pigeonhole SAT/UNSAT, XOR SAT/UNSAT, Horn and disjoint components). Formula seeds are 17 and 29. In the planted sweep, bridge clauses are added one at a time, keeping the original formula for that seed otherwise fixed.

Each formula receives eight checks: four inner-DAG evaluations using an independent exhaustive reference after construction, and four complete outer-solver executions. All 2,368 checks passed. Each inner wrapper made zero SAT-solver calls, and each full outer execution made zero reference-solver calls. This is finite correctness validation only.

## Representative measurements

Literal visits are a reproducible partial work counter, not wall-clock time or a complete RAM/bit-operation count. Sorting, some normalization and metadata overhead are omitted. These counters cannot establish a near-linear bound.

| Case | Mode | Leaf SAT instances | Literal visits during construction | Separator candidates |
|---|---|---:|---:|---:|
| planted_separator_bridges_0, seed 17 | flat | 3 | 2260 | 0 |
| planted_separator_bridges_0, seed 17 | separator | 15 | 7932 | 105 |
| planted_separator_bridges_0, seed 17 | separator_fast | 15 | 2232 | 10 |
| planted_separator_bridges_4, seed 17 | flat | 18 | 4714 | 0 |
| planted_separator_bridges_4, seed 17 | separator | 20 | 38548 | 664 |
| planted_separator_bridges_4, seed 17 | separator_fast | 14 | 12346 | 160 |
| planted_separator_bridges_4, seed 29 | flat | 15 | 3537 | 0 |
| planted_separator_bridges_4, seed 29 | separator | 22 | 36470 | 659 |
| planted_separator_bridges_4, seed 29 | separator_fast | 22 | 9327 | 120 |
| random_12var, seed 1700 | flat | 1 | 4041 | 0 |
| random_12var, seed 1700 | separator | 0 | 42588 | 378 |
| random_12var, seed 1700 | separator_fast | 0 | 11394 | 80 |
| PHP_4_3, seed 0 | flat | 0 | 1344 | 0 |
| PHP_4_3, seed 0 | separator | 0 | 10085 | 229 |
| PHP_4_3, seed 0 | separator_fast | 0 | 3115 | 50 |

On the no-bridge planted seed-17 case, the fast separator is exactly variables 1 and 2. The produced root is OR over all four assignments; each alternative is an AND of four residual components. Exact normalized sharing leaves 15 distinct small CNFs, each at most 45 bits, against a 52-bit child limit. This structure is recorded in example_dag.json.

The bounded candidate search reduces this case's separator candidates from 105 to 10 and literal visits from 7,932 to 2,232. Under four bridge clauses it gives 14 leaves versus the flat baseline's 18 on seed 17, but 22 versus 15 on seed 29. Thus it does not dominate even these small tests. Fewer gates or leaves may require more discovery work.

Zero leaf count means the inner construction resolved the formula using its own branching/inference work. It is not evidence of a free constant-size SAT compressor. The small pigeonhole controls now simplify strongly with unit propagation; this does not override known asymptotic limitations of restricted proof systems or prove a polynomial general solver.

## Conditional resource target suggested by separators

Suppose, as an additional unproved hypothesis, that every relevant invocation can cheaply expose a boundary of b variables such that EVERY boundary assignment leaves components of encoded size at most N^theta. If tiny components are packed into disjoint groups of size at most N^theta, ordinary greedy packing yields O(N^(1-theta)) groups per assignment, up to encoding overhead. Component packing is an analytical possible refinement, not implemented here.

Across all boundary assignments the resulting child-count bound is

q = O(2^b N^(1-theta)).

If b = sigma log_2 N and generation costs N^(1+sigma+o(1)), the idealized exponents are eta = 1-theta+sigma and

C = max(r, 1 + sigma/(1-theta)).

For theta=2/3 and an ADDITIONALLY justified streamed space bound rho=2/3, the Williams product target would require

5/3 + 3 sigma < 2 cos(pi/7),

or sigma < 0.04509035638, together with r+rho below the same threshold. This arithmetic is only a sufficient target under all stated premises. It does not follow from the finite tests or the existence of any small separator. Constant b contributes a constant multiplicative factor, not an exponent penalty.

In particular, observing 15 leaves versus N^(1/3) about 7.27 on one small instance is not an asymptotic disproof: constants and subpolynomial factors matter. The real issues are universal structural availability, discovery cost, repeated recursive applicability and space.

## Limitations and barriers

* Exhaustive two-variable separator discovery can cost O(n^2) candidate examinations, each with nontrivial source scans. It is not the desired near-linear construction.
* Bounded candidate search is cheaper but may miss useful separators.
* Small separators or small backdoor depth need not exist for general SAT instances. Bounded backdoor depth yields a restricted tractability result, not P != NP.
* The implementation stores entire intermediate formulas and the DAG. Stored-formula bit totals are recorded, but are not complete peak memory; no N^(2/3) space theorem is claimed.
* A small output frontier is insufficient if generating it requires a large search.
* There is no use of the code or special properties of a hypothetical polynomial SAT decider A. Therefore this prototype supplies no nonrelativizing step and no conditional P=NP-to-forbidden-speedup implication. Raw prime/hash provenance does not change that.
* Existing earlier cycle and dominance experiments motivated the interface; this run adds correctly conditioned AND decomposition, safe local renaming, matched unit-propagation baselines, a two-seed bridge sweep and a bounded-discovery repair. It does not repeat their results as a new theorem.

The current exact statement is: for every finite CNF F, these constructions yield a satisfiability-preserving forward DAG and a terminating outer solver. No claim of the form 'for every F, fixed-exponent low-resource bounds hold' is established. The needed contradiction theorem would have to derive those bounds from the existence of a polynomial SAT decider, with all quantifiers, setup, generation and replay costs specified.

## Next test

Implement a budgeted recursive backdoor interface with efficient recognition of Horn and 2-CNF terminal components, and test whether it avoids searching for a single large global separator. Record both successful structural reductions and explicit cases where the discovery budget is exhausted. This is the best literature-guided next engineering step; it remains a structural experiment unless linked to the hypothetical solver A.

## Reproduction

Run `python3 double_wrapper.py`. The script uses only the Python standard library and writes results.json and example_dag.json. The raw results include every case, seed, child-size bound, number of alternatives, work counters and outer recursion counters. summary.json is an aggregate of the included run. REFERENCES.bib contains primary sources.
