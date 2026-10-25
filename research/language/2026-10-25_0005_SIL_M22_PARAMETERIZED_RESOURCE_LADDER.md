# SIL/M22 Parameterized Resource Ladder — exact first prototype

**Prepared:** 2026-10-24 (America/Los_Angeles)  
**Status:** Elementary structural lemmas proved below; exact six-variable finite tests independently reproducible with `sil_m22_ladder.py`; preexisting one-sided factor upper bound credited; unrestricted SAT decision-time lower bound OPEN.

## 1. Target, semantic type, and proof obligations

The source language C_star is the set of valid **non-fully-paired** monotone exact-(2,2) 3-CNF formulas: each unique clause has three distinct variables, all literals have the same sign, and each active variable occurs twice positively and twice negatively. Individual sign-complement-paired clauses are allowed. For k active variables, m=4k/3 clauses, m+=m-=2k/3, and a dense indexed input has length N=Theta(k log(k+2)). SAT on C_star is NP-complete by Döcker's result plus the fixed nonpaired SAT anchor. This is **not** a lower bound.

Use the project's existing derived SIL-RC 0.1 catalogue and **do not alter canonical SIL semantics**:

- `E`: logical equivalence on the visible signature;
- `P`: exact existential boundary projection with possible private-variable removal or introduction, and explicit witness reconstruction;
- `S`: equisatisfiability of a whole formula, not generally a safe context replacement;
- `CTX`: conditional equivalence only under the certified surrounding context.

Each rewrite must name its original source-variable IDs, full occurrence environment, boundary, dependency certificate, representation type, charged discovery/search, output cost, witness-lift data, and live storage. **Most intermediate ordinary-CNF states are not in C_star.**

## 2. A structural lemma already present in M22-DEFECT-ADAPTER131

Let P denote the unsigned supports of positive clauses and Q those of negative clauses, H=P∩Q, P'=P\Q, Q'=Q\P, and q=|P'|. Since each variable appears twice in each polarity, deleting all paired supports leaves identical per-variable degree vectors in P' and Q'. Therefore

- |P'|=|Q'|=q and deg_P'(x)=deg_Q'(x) in {0,1,2} for every x;
- q=1 is impossible: the two unmatched supports would be identical;
- C_star is exactly the valid class with q≥2;
- D=union(P')=union(Q'), with d=|D|≤3q;
- the paired supports H become exact NAE3 constraints `1≤sum(x_e)≤2` (`FA5`, E-mode).

The previously established project algorithm `M22-DEFECT-ADAPTER131` enumerates 2^d boundary assignments and performs a polynomial-time generalized matching/degree-factor test on the paired core. This gives `O*(2^d)` time and polynomial space. The stronger `M22-ONE-SIDED-FACTOR133` chooses one true literal for each positive unmatched clause and then solves all remaining signed degree-two interval constraints by polynomial-time graph factors. This gives **O*(3^q)** time and polynomial space in the declared model. These are **upper bounds** for correctly handled C_star sources, not lower bounds for arbitrary deciders.

The published general degree-four sparse-SAT bound of Jain–Neoh–Stephan is `O*(1.25417601^k)` with polynomial space. An adaptive implementation can precompute q,k and choose between the factor enumeration and the published generic algorithm. Ignoring polynomial factors, `3^q` is better when `q/k < ln(1.25417601)/ln(3) ≈ 0.20615`.

## 3. A concrete exact trace within C_star

Take variables `a,b,c,d,e,z`, with positive clauses

```
(a∨b∨z)  (c∨d∨z)  (a∨b∨e)  (c∨d∨e)
```

and negative clauses

```
(¬a∨¬b∨¬z)  (¬c∨¬d∨¬z)  (¬a∨¬c∨¬e)  (¬b∨¬d∨¬e).
```

Every variable occurs exactly twice per sign, all eight clauses are proper, unique, and pure-sign; H={abz,cdz}, q=2, D={a,b,c,d,e}, d=5.

### SIL actions and exact combinatorial resource counts

| Stage | Exact action | Variable/constraint state | Concrete charge to log |
|---|---|---|---|
| 0 | Read and validate input; build signed support incidence records | 6 variables, 8 ordinary 3-clauses, 24 signed literal occurrences | Read source records; validate quotas, uniqueness, signs; discover H, q, D; count comparisons and stored index bits |
| 1 | `FA5` on the two sign-complement pairs | 4 unmatched OR clauses + 2 NAE3 relations, *exactly equivalent* on all six variables | Match both polarity records for each support; create 2 semantic relation nodes and source-ID links |
| 2 | `VE5` eliminate private z, full positive/negative occurrence environment | 5 variables, 6 ordinary clauses (four original 3-clauses plus two mixed 4-clauses), exact existential projection | 2 positive × 2 negative = 4 candidate resolvents; 2 tautologies; 2 retained; 4 old parents removed; witness-lift rule retained |
| 3a | One-sided signed-factor continuation | ≤3^2=9 witness choices, each with a polynomial factor test | Charge every false choice, graph construction/solution, source-name reconstruction and assignment checking |
| 3b | Alternative full-D enumeration | 2^5=32 boundary words, each with polynomial paired-core factor test | Charged upper bound only; could be worse than 3a |
| 3c | Alternative exhaustive enumeration | 2^6=64 full assignments | Baseline upper bound only; a solver is not required to enumerate |

The two width-four output clauses from eliminating `z` are

```
(a∨b∨¬c∨¬d)
(¬a∨¬b∨c∨d).
```

The other four clauses are the unmatched original clauses. The simplified ordinary CNF has 20 literal occurrences (versus 24 initially), **16 projected satisfying assignments** (versus 22 complete source satisfying assignments), and an exact witness lift. This is P-mode, not E-mode: the 22 source assignments project to 16 distinct visible assignments. The output **is not** an M22 source formula; it has signed width-four clauses and broken occurrence quotas. The declared sample serialization proxy (`3` bits per clause-width field, `1+w` bits per literal, `2w` header bits, `w=3`) is **126→104 bits**. Those numbers are NOT actual Turing-machine operations, a universal encoding guarantee, nor a lower bound.

### Scope of the six-variable census

Enumerating all 75 possible four-triple positive support families on six names with degree exactly two, and all 75 such negative families, yields 5,625 syntactically valid formulas. By full evaluation of all 64 assignments per formula, every one is SAT. The q histogram is `0:75, 2:1260, 3:1680, 4:2610`. Model counts range from 18 to 26. This is an exhaustive **finite** fact in the fixed six-variable grammar, not asymptotic hardness. The result agrees with existing project finite audits.

## 4. Resource objective for an ideal adaptive parameterized solver

For source input F, let C_t be the **complete** currently reachable state: original read-only input, current semantic formula, boundary provenance, learned constraints, branch stack, representation and cache. Let θ(C_t) be a vector of *observable/certifiable parameters*: `k,m,q,d,component structure, affine rank, separator size, clause-width histogram, certified contextual exclusions, cache/live bits`, and all other useful features actually discovered.

A concrete adaptive policy π selects and executes *only certified legal* actions `r_t` (SIL rules, direct graph-factor continuation, SCC/Horn/Gaussian solution, search, etc.). Its charged work and workspace are

```
T_π(F) = scan_cost + Σ_t [test_cost(r_t) + selection_cost(r_t)
                           + actual_rule_cost(r_t) + failed_trials_t
                           + replay_t + source_reads_t]
S_π(F) = max_t (all simultaneously writable and index bits, including
                  live ancestor states, buffers, cache and witnesses).
```

The **offline** minimum over a restricted action library,

```
Opt_R(F)=min_{π legal using R} T_π(F),
```

is a valuable finite-model comparison but does **not** represent the optimal unrestricted SAT algorithm. The runtime of discovering the best rule is also not free for a real solver. SIL rules do not exhaust all algorithms, including more direct symbolic decisions.

### Suggested reduction-state classification

1. Grammar and duplicate/polarity patterns: `CL`, `CP`, `SS`.
2. Complement-paired NAE region and signed support defect `(H,q,D)`: `FA5` + graph factors.
3. Implication/Horn/bijunctive and parity/gate modules: `UP`, `EQ`, `IM`, `XR`, `GT` with complete certificates.
4. Private bounded-degree variables: `VE5/VE6`, logged change in *actual encoded size* and width.
5. Separators and interfaces: `DC1/DC3` with source-name-correct boundary relations, not independent child SAT bits.
6. Contextual pattern elimination: `SP3/CTX` and the project's type-1 I2-pruning certificate, charging all seven local pattern tests when used.
7. Residual continuation chosen adaptively by total expected actual cost: factor, sparse-SAT solver, forward/reverse dynamic programming, symbolic search or other correct algorithm.

All stages must be permitted in any order when their preconditions hold. `Type-1 I2` contextual pruning can rule out one local pattern and improve a particular *algorithm's upper analysis*, but no theorem guarantees such pruning across every hard input.

## 5. What would turn the ledger into a lower bound?

The ledger measures **actual operations or certified upper budgets** of selected algorithms. To prove L_star not in P we would need an algorithm-independent theorem: for every fixed uniform total correct decider A and every polynomial budget, an arbitrarily large F in C_star makes A exceed that budget. One possible method is a noncircular complete-state invariant Φ, initialized independently from unknown optimal time and charged across **every** correct adaptive transition, including operations not expressible in SIL; this remains OPEN. A lower bound against only this finite SIL policy class is useful but insufficient.

Even q=Theta(k), a large hypergraph cycle rank or many apparently conflicting patterns can coexist with easy recognized instances. A fixed q gives a polynomial algorithm, but a growing q alone is not a lower bound. Keep same-source SAT/UNSAT controls, affine and graph-factor counterexamples, and direct witness recognition in all audits.

**Next precise task:** Run rule-by-rule checked reductions on a scalable connected M22 family with both SAT and UNSAT controls, recording the full θ(C_t) sequence and charges. Compare certified 3^q, 2^d, general sparse-SAT and contextual pruning bounds. Attempt to identify a structural resource remaining after all these *affordable* reductions; test a new claimed lower-bound bridge against algorithms outside SIL before promoting it.

## 6. Provenance

- SIL derived alias source: `research/language/2026-10-24_SIL_RC_0_1_CATALOGUE.md`, [GitHub](https://github.com/j15marti/pnp/blob/main/research/language/2026-10-24_SIL_RC_0_1_CATALOGUE.md). It expressly does not change canonical SIL grammar.
- Canonical M22 defect and source-factor baseline: `research/agents/lspv-2/2026-10-24_1112_LSPV-2_M22_DEFECT_ADAPTER131.tex`, [GitHub](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1112_LSPV-2_M22_DEFECT_ADAPTER131.tex).
- Improved 3^q factor theorem: `research/agents/lspv-2/2026-10-24_1231_LSPV-2_M22_ONE_SIDED_FACTOR133.tex`, [GitHub](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1231_LSPV-2_M22_ONE_SIDED_FACTOR133.tex).
- Exact six-variable paired-core interface: `research/agents/lspv-3/2026-10-24_2223_LSPV-3_M22_WEIGHTED_LEAF_FACTOR110.tex`, [GitHub](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-24_2223_LSPV-3_M22_WEIGHTED_LEAF_FACTOR110.tex).
- Doecker (2019), arXiv:1912.08032; Jain-Neoh-Stephan (2024), arXiv:2411.07389; Gabow (1983), degree-constrained subgraphs.
- Contextual pattern theorem from user-supplied `type1_I2_contextual_pruning_theorem.txt` and `type1_pruned_or_easy_target.txt`.

**Do not describe the script's scans as a measured computational lower bound.**