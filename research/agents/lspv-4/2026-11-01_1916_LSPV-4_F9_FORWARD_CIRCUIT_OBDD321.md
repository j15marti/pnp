# LSPV-4 / F9-FORWARD-CIRCUIT-OBDD321: Same canonical source as SAT and Circuit-SAT

**Research started:** 2026-11-01 19:16 PST. **Statuses:** PROVED/EXACT elementary restricted lemmas; COMPUTATIONAL exhaustive F9 checks; OPEN all-input adaptive decomposition and P versus NP. Not externally peer-reviewed.

## Source, distinction, and precise obstruction

Original target: valid duplicate-free proper Döcker monotone 3-SAT-(2,2) only, rejecting malformed strings. Its ordinary residuals may be noncanonical. The F9 source here has 9 variables, 12 clauses, positive supports `(156),(238),(135),(469),(247),(789)` and negative supports `(468),(167),(234),(358),(129),(579)`. Every variable occurs positively twice and negatively twice; all supports in each signed clause are distinct and no signed source clause repeats. The full source has 70 SAT assignments. We analyze **the identical source** as F9-CNF and an AND/OR/NAND forward circuit C_F(x) computing its truth value on each assignment.

Exact universal obstruction: a short circuit computing `F(x)` is a *verification circuit* with a free input x. Its size and evaluation time do not bound the cost of deciding whether there exists an x with output 1. Likewise, obtaining a minimum circuit after knowing F is UNSAT is not a polynomial-time reduction without paying for acquiring that answer. Quantifiers must refer to arbitrary F and arbitrary correct solvers, not one instance solved offline.

## Four falsifiable hypotheses and results

1. **H1:** A canonical M22 formula requires a large direct forward evaluation circuit. **FALSIFIED:** each positive triple is `OR2(OR2(a,b),c)` and each negative triple is `NAND2(AND2(a,b),c)`. Balance `m` outputs with `m-1` AND2 gates. For every valid canonical source with `n` variables, `m=4n/3`, so `g=3m-1=4n-1` two-input AND/OR/NAND gates and gate depth <= `2+ceil(log2 m)`; source discovery, gate output and physical bit addressing are charged separately. F9 gives 35 gates, depth 6, full 512-row agreement. AND/OR/NOT instead gives 41 gates, depth 7. These are explicit **upper bounds**, not globally minimum circuits.
2. **H2:** Exact forward Shannon decomposition yields an informative *representation-specific* minimum. **PROVED restricted / COMPUTATIONAL:** for every fixed variable order, reduced ordered binary decision diagram (OBDD) node count is the sum of distinct essential residual cofactors at each tested variable. An exhaustive finite subset-lattice dynamic program covering every one of the 9! orders gives F9 min 52 nodes at order `(2,6,7,9,8,4,3,1,5)`, natural 66, max 80. An independently generated reduced BDD verifies each returned size, but the compiler need not construct an OBDD; the 35-gate general DAG is smaller.
3. **H3:** Exponential size of an OBDD for a chosen order implies exponential mandatory decision work. **FALSIFIED restricted:** take t disjoint variable-renamed copies of F9, an admissible canonical original `F_t`. Order x1 from *all t copies first*, then all remaining variables. The two x1 cofactors of F9 are both nonzero, distinct, and each depends on x2. The `2^t` prefix assignments therefore induce `2^t` different nonzero residual Boolean functions, all depending on the next variable x2 of block 1. Exact OBDD width at that level is at least `2^t`. Nonetheless, a block-grouped variable order yields an OBDD of at most `52t` nodes, the same original has an ordinary forward circuit of `36t-1` gates, and a paid source inspection can recognize disjoint F9 blocks and answer SAT in polynomial work on this family. (General-source fallback may still take exponential time.) Thus fixed-order exponential OBDD width is not a universal SAT lower bound.
4. **H4:** A uniform paid source-authenticated optimal controller, or arbitrary-decider power-short contractor with strict same-machine FLMV transfer, follows from these circuit facts. **OPEN.** No such transfer is claimed.

## Exact restricted gate lower bound and its limitation

For this particular F9 Boolean function, all nine input variables are essential: the numbers of pairs `(x_i=0, x_i=1)` on which the output differs are 46,44,52,50,40,52,40,38,40 for i=1..9. With fan-in at most 2, an output connected to n essential input sources needs at least `n-1=8` binary merging gates, and the maximum input-to-output depth must be at least `ceil(log2 n)=4` (unary NOT gates do not improve fan-in). The explicit 35-gate depth-6 construction leaves a substantial *circuit-complexity* gap; none of these bounds is a search-time lower bound.

The F9 x1 cofactors are both satisfiable: witness x1=0 is `010110100` and x1=1 is `110100100` (strings x1 through x9). Setting x2..x9=`10100100` gives F9(x1=0)=0 but F9(x1=1)=1, proving cofactors differ. Both cofactors depend on x2 (22 pivotal pairs in each cofactor).

**Proof of bad-order OBDD width:** Let f0 and f1 denote F9 restricted to x1=0 and 1. For each `b∈{0,1}^t`, the residual after testing t designated inputs is `R_b(y_1,...,y_t)=∏_{j=1}^t f_{b_j}(y_j)` on disjoint remaining variables. Every f0 and f1 is nonzero, so existentially projecting R_b onto any block i recovers `f_{b_i}`. Hence R_b=R_c implies f_{b_i}=f_{c_i} for all i and therefore b=c. Moreover each R_b depends on the very next tested variable x2 of block1, because both f0 and f1 do and the remaining factors are satisfiable. Every R_b requires a different OBDD node at that level. QED. The restricted width result does not extend to all orderings; grouping blocks avoids it.

## SAT/UNSAT controls on one original, no oracle inference

The coherent UNSAT pin is `{x1=1,x3=0,x5=1,x6=0,x7=0,x8=0}` with free `{x2,x4,x9}`. It has no already-empty original clause yet **zero** completions. Each of the eight possible completions has a stored original-clause-indexed falsification leaf in `independent_controls.json`.

Flip only x1 to 0, keeping the other five pins. The same F9 original has **two** SAT completions, with complete witnesses `010010001` and `010110001`. Independent verifier checked all 264 four-mode S/U clause-pair extremes, 6,144 complement-clause counts, and rejection of six malformed originals. No global inference from local conflicting S/U targets is made.

The previously verified canonical U198 (198 variables, 264 clauses) is UNSAT, while V198 has an original-clause-checked SAT witness. This run **did not reprove U198**; its prior authenticated status is inherited. For any UNSAT original U, the Boolean evaluation function `f_U(x)` is identically zero and has a one-constant output representation **after its UNSAT status is known**. Hence a minimum-instance circuit cannot supply a nontrivial universal UNSAT-solving time lower bound. This is a direct falsifier to reverse-inference from post-solution minimization.

## Circuit-SAT translation and resource audit

Every gate of the 35-gate NAND/OR/AND circuit can be encoded by three biconditional Tseitin clauses (mixed binary/ternary), with a unit clause forcing the output to 1. This yields exactly `35*3+1=106` clauses and `9+35=44` variables. The 70 accepting input assignments each have **one** gate-trace extension because the circuit is acyclic and its gate relations are biconditional. These derived Tseitin clauses are neither proper canonical M22 originals nor to be confused with the target language; additional padding introduces charged work and potentially witness multiplicity. The project's established `CIRCUIT-TSEITIN-TRACE-AUDIT46` and `PARSIMONIOUS-CIRCUIT-3CNF47` already handle the equivalence/uniqueness issue.

For a source of n variables and m=4n/3 clauses, explicit forward circuit construction uses O(N polylog N) conservative indexed-bit work, with `g=4n-1` gates and O(g log N) bits for gate descriptors if fully materialized. Evaluating one complete input assignment uses O(g) indexed-word gate operations plus source/input access, index-head motions and output read/write. An exact fallback that enumerates all 2^n original assignments has fully charged bound

`W_enum(F) ≤ W_grammar+W_build+Σ_{a∈{0,1}^n}(W_set(a)+W_eval(C_F,a)+W_check_original(F,a)) = O(2^n N polylog N)`

under a specified straightforward indexed-bit implementation. Writable peak depends on whether the circuit is materialized, streamed or replayed; a straightforward bit-array implementation uses O(g log N + n log N) writable bits plus index/head storage, excluding the read-only original. This is a correct all-input fallback, not a polynomial total-work result.

A general adaptive controller must charge `W(F)=W_grammar(F)+W_discovery(F)+W_policy(F)+Σ_failed W_trial+W_compose(F)+Σ_{children} (W_reencoder+W_bit_accessor+W(child))+W_proof+W_output+W_guest`, with DAG-shared work counted once and simultaneous ancestor/guest peak space tracked as a *maximum over actual overlapping live states*, not by adding asymptotic per-child bounds. Here no proof bounds `Σ W(child)` polynomially on all canonical inputs, and no universal A->Phi(A) with unknown exponents or strict matched FLMV transfer is established.

For F9 the exhaustive truth-table acquisition performed 512 clause evaluations, and the subset DP evaluated 512 prefix subsets and 2,304 candidate subset-extension marginal costs. The 52-node optimum is **not** free to discover; the exact finite routine does not promise poly(N) cost for arbitrary n. All source sign/cycle provenance and original SAT/UNSAT witness checking are preserved. Logical XOR is an offline diagnostic only.

## Prior art and overlap

Already in this repo: `research/main/2026-10-21_1848_CIRCUIT_TSEITIN_TRACE_AUDIT46.md`, `research/main/2026-10-21_1948_MAIN_PARSIMONIOUS_CIRCUIT_3CNF47.md`, `research/agents/lspv-3/2026-10-23_2340_LSPV-3_HWB_OBDD_BARRIER68.tex` (even an all-order OBDD lower bound can coexist with easy source-specific decision), and the bidirectional exact boundary-DP reports. This experiment is a same-source F9 fully quantitative bridge and restricted bad-order example, not a claim of new BDD principles.

External primary references:

1. J. Döcker, *Monotone 3-Sat-(2,2) is NP-complete*, 2019, https://arxiv.org/abs/1912.08032.
2. R. E. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE TC 35(8), 1986, https://doi.org/10.1109/TC.1986.1676819.
3. A. Amarilli et al., *Connecting Knowledge Compilation Classes and Width Parameters*, 2018/2020, https://arxiv.org/abs/1811.02944. Its monotone-CNF lower-bound hypotheses do **not** directly apply to globally mixed-positive/negative canonical M22 source formulas.
4. L. Fortnow et al., *Time-Space Lower Bounds for Satisfiability*, JACM 2005, https://doi.org/10.1145/1101821.1101822. No numerical transfer from plain NP-completeness is assumed.

GitHub source audit: `j15marti/pnp` searches `Circuit-SAT`, `OBDD`, `F9`, `U198` and `openai` organization searches `sat`, `boolean circuit`, `decision diagram`, `tseitin`. No alternative algorithm or novelty inferred from empty/irrelevant search results.

**Next load-bearing test:** On the same canonical original, compare exact *boundary/cofactor* counts and charged acquisition across forward/reverse elimination orders and source-indexed mixed SAT/UNSAT pins, then seek a theorem forcing high cost under **every adaptively selected order and every alternative method**, without accidentally proving only a restricted compiler lower bound. Keep exactly five tasks and their schedules untouched. P versus NP OPEN.