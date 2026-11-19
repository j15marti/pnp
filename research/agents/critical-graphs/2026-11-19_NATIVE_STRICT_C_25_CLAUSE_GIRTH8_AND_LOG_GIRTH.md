# Native strict-C 25-clause critical source and direct-C logarithmic-incidence-girth existence
2026-11-19. **PROVED:** exact probabilistic existence theorem. **COMPUTATIONALLY VERIFIED:** 25-clause native-C critical source with full refutation and all deletion witnesses. P vs NP remains OPEN.

## Predicate
Colors are Z5. R(a,b) iff (b-a) mod 5 belongs to {1,3}; C(x,y,z) iff x,y,z form a directed triangle in either orientation. Every physical clause uses three distinct variable names. Independent exhaustive counting gives 30 accepted triples out of 125. Neither historical Q, P, nor designated-head S is interchanged with C. No gadget translates source clauses.

## Small certified source
Random triple greedy: n=26, seed **2026111946**, Python random.Random, shuffle all 3-name subsets; add a clause only if each pair of its three names is at primal distance at least three, which excludes incidence 4- and 6-cycles. This yields 28 physical clauses. Exact GAC/backtracking, reverse greedy clause removal, and deletion-witness extraction leave 25 clauses. Remove one isolate and renumber to 25 variables.

Canonical clause list:
```
(10,16,17) (5,8,15) (7,14,21) (1,5,16) (8,12,20)
(11,13,24) (7,15,23) (3,5,6) (3,9,21) (9,10,24)
(7,20,22) (0,4,12) (6,13,20) (8,14,24) (10,18,23)
(1,2,20) (18,19,21) (2,3,17) (0,1,9) (4,6,18)
(1,11,23) (13,17,19) (0,14,17) (4,7,16) (2,4,24)
```
An independent Python implementation replayed a *complete* strict-C UNSAT proof tree of **1,046 nodes, 600 contradiction leaves, max depth 8**, with no fixed-color symmetry or answer-polarity advice. It checked all **25** full clause-deletion satisfying assignments: 600 retained original-C evaluations true, 25 deleted original-C evaluations false. Direct bipartite incidence BFS gives girth **8**. Only **one** variable has incidence degree one, thus these 25 clauses cannot be a direct private-head graph-coloring encoding (which needs at least one distinct degree-one head for each edge clause). Primal graph girth is not high.
Canonical source JSON SHA-256: `a372c198871f73ec9ebf6665e597f0fae7b3af8613aeae325c07bd6e3ca5bd75`.
Proof-tree JSON SHA-256: `2e386cc59ebb1e7c8c4a7f2d418ab23178b6294f9fd7b17b0264ee3ac86b6ef9`.
The complete independent checker, generator, full deletion witnesses, and proof tree are in the per-run reproducibility ZIP; the compact canonical clause source is also published in this directory. No global order-minimality is claimed.

## Probabilistic direct-C existence theorem (PROVED)
For every integer n>=100, there exists a physically clause-minimal UNSAT strict-C formula on at most n named variables with at most 8n original constraints and **incidence girth at least 2(floor((log_49 n)/2)+1)=Omega(log n)**.

**Proof.** Independently sample m=8n ordered triples of distinct variable names, with replacement between clauses. For fixed a in Z5^n, the chance that three independently sampled variable colors are pairwise distinct is at most 6e3(p_0,...,p_4)<=6*C(5,3)/5^3=12/25 by Maclaurin's inequality. Conditioning on distinct variable names divides by at most (1-1/n)(1-2/n). Therefore any strict-C clause is satisfied with probability <=(12/25)/((1-1/n)(1-2/n))<1/2 for n>=100. The count of violated clauses Y_a stochastically dominates Bin(8n,1/2). Hoeffding and a union bound over all 5^n colorings give
```
P[exists a with Y_a <= n] <= exp(-(9/4-ln 5)n).
```
For a fixed pair of original variable names, a randomly sampled clause includes the pair with probability 6/[n(n-1)]. Let X_2ell be the number of simple incidence cycles length 2ell. By counting ordered sets of ell distinct variables and ell distinct clause indices and dividing by 2ell,
```
E[X_2ell] <= (6m/(n-1))^ell/(2ell) <= 49^ell/(2ell).
```
For L=floor((log_49 n)/2), let X count cycles lengths 4,6,...,2L. Then E[X]<=49 sqrt(n)/192, so Markov gives P[X>=n]<=49/(192 sqrt(n)). This plus the prior failure probability is <1. Thus there exists a source with every assignment violating >n clauses and with fewer than n short cycles. Remove one physical C clause from each short cycle. At most n-1 deletions leave UNSAT and girth >=2(L+1). Remove any further clause whose deletion preserves UNSAT, using a *complete exact* 5-color solver. Monotonicity preserves girth; each remaining physical clause has a complete deletion witness. QED.

This is a project-specific probabilistic existence proof in the tradition of Erdős (1959), not a claimed priority result and **not** a polynomial-time explicit construction. An exhaustive lexicographic source search and exact critical extraction are deterministic but expensive. Outputting all witnesses may require quadratic-size source output. No machine time/space lower bound follows.

## Complexity firewall and blocker
No valid transfer into <=N^0.195 explicit shared rows, <=N^0.65 private blocks or <=N^0.35 private size is proved. No unrestricted SAT-to-critical-promise reduction is proved. Cover acquisition, source encoding, preprocessing, failed branches, both answer polarities, memory and certificates must all be charged. Girth and clause-minimality do not establish superpolynomial deterministic runtime.
**Next task:** construct a materialized and independently verified **incidence-girth 10** native strict-C clause-critical source and all physical deletion witnesses, then seek a resource-preserving generator/verifier rather than relying on a source promise.

Sources: [Erdős 1959](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/LargeGirthAndChromaticNumber.html); [Exoo and Goedgebeur 2019](https://doi.org/10.23638/DMTCS-21-3-9); [Goedgebeur 2020](https://doi.org/10.1002/jgt.22467). Prior project: `research/agents/critical-graphs/2026-11-19_LPS73_GIRTH_SOURCE_K6_LIFT_FALSIFIER.md`, `2026-11-19_HAJOS_CRITICAL_WITNESS_WIDTH_FIREWALL.md`.
