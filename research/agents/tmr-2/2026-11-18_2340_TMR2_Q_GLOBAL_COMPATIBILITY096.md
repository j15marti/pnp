# TMR-2/096: exact-one T5, parity-to-cycle-syndrome transfer, and the complete five-class forbidden basis

**Owner:** TMR-2 / PNP Information Necessity. **Date:** 2026-11-18, America/Los_Angeles. **Primary model:** \(\Sigma=\mathbb Z_5\), \(R(a,b)=[b-a\pmod5\in\{1,3\}]\), \(Q(h,u,v)=R(h,u)\oplus R(h,v)\). Variable names within a clause are distinct; assigned letters may coincide. **Classification:** PROVED exact identities and finite-template exhaustive certificate; COMPUTATIONAL test counts; no unrestricted time lower bound. P versus NP remains OPEN.

## 1. Source archive audited before new work

Retrieved the exact owner-supplied `T5_Exact_One_Experiments_2026-11-18.zip` (library ID `libfile_00b4599c2cfc8191a859b757dad101a0`). Its own verifier passed: local Q/P counts 60/20, five-clause deletion counts 10/40/10/30/25, all 236 large-fixture deletion witnesses, and 55,696 direct Q evaluations. Archive SHA256 is recorded in the new local JSON. Its exploratory Q case n=40,m=60,seed=202611580003 is **UNKNOWN due to the 10,000-node cap**, not UNSAT. Do not rerun the completed 2,320-run main comparison grid.

## 2. PROVED exact parity-to-cycle-syndrome identity for arbitrary Q sources

For each distinct *ordered* comparison \(e=(h,u)\) occurring in a clause, introduce the observed bit \(p_e=R(x_h,x_u)\). For each head h, form the graph whose vertices are its compared followers and whose edges are the follower pairs in clauses headed by h. Bipartite-check each such graph, accounting for isolated compared followers as components. An odd cycle makes the entire Q instance UNSAT. If all are bipartite, each comparison is expressible as
\[
p_e(t)=t_{j(e)}\oplus \varepsilon_e,\qquad t\in\{0,1\}^{d},
\]
where d is the total number of connected follower-graph components and \(\varepsilon_e\) is the checked two-color. These patterns are disjoint and exhaust every locally parity-feasible observed-comparison assignment.

Build the directed **comparison multigraph** F on the original variable names, with one arc for each distinct ordered comparison. Antiparallel comparisons remain separate multiedges. Set \(m=|E(F)|\), \(c=\#\) weak components (including isolated original variables), and \(\beta=m-|V(F)|+c\). Choose an oriented fundamental-cycle matrix \(H\in\mathbb Z_5^{\beta\times m}\), so a vector of edge differences \(a_e=x_u-x_h\pmod 5\) comes from vertex potentials iff \(Ha=0\). Define
\[
D_1=\{1,3\},\qquad D_0=\{0,2,4\}.
\]
The zero in \(D_0\) is essential: **ties are nonwins**. The exact original-letter solution count is
\[
\boxed{ Z_Q(F)=5^c\sum_{t\in\{0,1\}^d}
       \sum_{a_e\in D_{p_e(t)}\ \forall e}
       [Ha=0\pmod 5].}
\]
Proof: every legal assignment induces exactly one head-parity pattern and a difference vector with zero cycle syndromes. Conversely, any valid difference vector reconstructs exactly five choices of the additive root value in each component; no overcounting occurs. This identity does **not** eliminate private heads for counts and preserves their 2/4 witness multiplicities.

A reproducible dynamic program enumerates t and updates the \(5^\beta\) syndrome states for each comparison, using two or three transitions per state. A safe arithmetic-operation upper bound is \(O(2^d m(\beta+1)5^\beta)\), plus source parsing, pattern construction, forest/cycle construction and integer-bit costs. The two live syndrome arrays use \(O(5^\beta)\) integer cells; counts may have \(O(|V|\log 5)\) bits. Therefore this is a genuine source-aware FPT algorithm in \(d+\beta\), *not* a lower bound. Witness extraction requires charged backtracking or replay; UNSAT means all patterns exhausted, not an unverified negative child response.

## 3. PROVED five-class tournament completion, with a smallest capacity-only counterexample

Fix an equality partition into k **known distinct** letter classes, 1<=k<=5, and impose any specified partial directions between the classes. Only at this stage is \(R(b,a)=\neg R(a,b)\) valid. A **complete** tournament of k<=5 distinct classes embeds in T5 iff every class has at most two specified wins and at most two specified losses. For k=5 this is the unique regular five-tournament up to isomorphism; for k=4 it is the unique bounded-degree four-tournament; for k<=3 all tournaments occur. Exhaustive labeled counts for k=2,3,4,5 are respectively 2,8,24,24 complete orientations, with no capacity/embedding discrepancy.

This **fails for partially specified orientations**. On four distinct classes, the four arcs \(0\to2,0\to3,1\to2,1\to3\) obey both degree limits but cannot embed: two distinct T5 heads cannot share two distinct outneighbors. No fewer than four directed observations can fail the degree-only test.

Stronger finite-template result: among *all* \(3^{10}=59,049\) partial orientations on five labeled, pairwise-distinct classes (each unordered pair absent, forward or reverse), after removing degree-capacity violations, exactly 3,120 are nonembeddable. Every one contains a four-arc forbidden subpattern. There are exactly **three isomorphism types** of such minimal patterns, with labeled multiplicities 30,60,60:
\[
\begin{array}{ll}
F_1:& 0\to1,\ 0\to2,\ 3\to1,\ 3\to2,\\
F_2:& 0\to1,\ 0\to2,\ 3\to1,\ 3\to4,\\
F_3:& 0\to1,\ 0\to2,\ 3\to1,\ 4\to2.
\end{array}
\]
For four distinct classes only F1 appears (six labeled copies). Proof certificate: enumerate all 5!=120 injections into T5, collapse their induced complete orientations to 24 labeled patterns; exhaust all three-state partial orientations, reject any with in/outdegree greater than two, and check completion against the 24 patterns. Every uncompletable pattern contains one of the 150 minimal labeled four-arc patterns, and the three orbits above exhaust these patterns. The compact checker and independent full Python audit make this finite case check reproducible.

**Important scope limitation:** this is a completion theorem for a *specified equality partition*. In an original Q source, distinct variable names may have equal values. Rejecting a hypothesized all-distinct quotient is not a proof that the original Q instance is UNSAT. Selecting a feasible equality partition is a separate, generally NP-hard global task.

## 4. Why globally compatible equality partitions remain difficult

With one fresh private head for every follower edge, \(\exists h\,Q(h,u,v)\iff u\neq v\). Hence the decision problem is exactly graph five-colorability, even though every individual head is parity-consistent and locally capacity-feasible. The new complete five-class forbidden basis does not decide which variable names should share one of the five classes. In the K6 control, 21 Q variables and 15 clauses are UNSAT by the six-clique pigeonhole certificate, yet removing any of its 15 clauses permits a full checked 5-letter Q assignment; all 15 such witnesses were constructed anew. Full source inspection and this polynomial-time clique detector are legitimate shortcuts.

The original 47-vertex, 236-edge, 6-chromatic Mycielski graph was *independently regenerated* by three lifts of C5 and its exact 236 follower edges matched the imported 283-variable Q source. Every one of the 236 imported single-clause deletion witnesses was rechecked against all 236 Q clauses (55,696 checks). The short Mycielski chromatic argument is the real UNSAT certificate. Its original graph girth remains four and its Q incidence girth eight, not growing with n.

## 5. PROVED unbounded-local-obstruction barrier, but NOT a runtime lower bound

Erdos's high-girth/high-chromatic graph existence theorem supplies, for every g, a finite graph with girth >=g and chromatic number >=6. Delete edges until it becomes edge-minimal with chromatic number >=6; edge deletion changes chromatic number by at most one, so the result is 6-chromatic and edge-critical, with girth still >=g. Replace every edge by Q(h_e,u,v) with a fresh private head. The resulting Q formula is UNSAT, parity-feasible at every head, and clause-critical. Every subset of fewer than g clauses corresponds to a forest and is 2-colorable, hence Q-satisfiable. Its factor-incidence graph has girth at least 2g (private heads are leaves).

Thus **for every fixed local clause bound k**, there exist UNSAT Q sources for which *every* <=k-clause subformula and every independent head-parity check passes, and every single-clause deletion has a genuine SAT witness. These are formal limitations on bounded-local-obstruction methods, not lower bounds on all algorithms. This proof is existential; computable exhaustive graph search can select a family but would charge potentially enormous instance-generation time. An efficiently constructible and source-aware-hard family is not furnished. A source solver may exploit global graph structure.

## 6. New finite computational audit and explicit costs

The independent local script completed **56,080 assertions with zero failures**, dominated by 55,696 source-level imported deletion-witness checks. There were 80 new independent seeded small Q sources (seed 20261119096), checked by 5^n original-label enumeration and independently by parity-syndrome DP. No completed old random grids were repeated.

* Critical five-clause Q UNSAT: 8 directed comparisons, d=3 parity bits, beta=5, eight parity patterns, exact count 0, **15,552** candidate DP transitions, **1,818** maximum simultaneously live current+next state entries, and **29,858** maximum logical DP payload bits by the declared bit-accounting formula. These counts omit source storage, Python object overhead and OS RSS.
* Its clause deletions have exactly **10,40,10,30,25** original-letter extensions, checked independently. The new cycle DP performs 5,944; 5,944; 5,696; 5,673; and 1,064 transitions respectively.
* The three-clause same-head XOR triangle is rejected during bipartiteness with zero cycle-DP transitions, not mislabeled as a hard five-letter obstruction.
* One Q triple has 60 assignments; the old P triple has 20, disjoint accepted sets. One arbitrary three-clause four-variable control has 65 Q assignments and 2,140 parity-syndrome transitions.

These are logical operation counters for tested source transitions, not optimized machine runtime, measured peak physical RAM, proof complexity or a numerical lower bound. The syndrome DP is *deliberately* worse than legal K6 graph-projection, Mycielski recognition, bounded-treewidth dynamic programming, and one-head bipartiteness on their natural promise families.

Named handoff invariant: **D2-Q-PARITY-CYCLE-SYNDROME-FIVE-CLASS-BASIS096**, reporting (a) parity component dimension d, (b) multigraph cycle rank beta, (c) exact fiber support/count and DP update costs, (d) equality-class completion violations in F1/F2/F3, and (e) the cheapest legitimate source-aware shortcut.

## 7. Correct-path and simultaneous time-space safeguards

**SAT output** means a complete five-letter assignment, directly checked against all Q clauses. A supplied correct path of k bits is a *read-only witness* only if all path-dependent choices are genuinely checked. A wrong SAT path rejects. **UNSAT output** requires a uniform exhaustive decision proof, a completely checked formal refutation, or a mathematically justified recognized source family. A guessed single refutable block per shared assignment is insufficient without independently verifying both its refutation and complete coverage of shared assignments. Invalid UNSAT paths must reject, not establish negative membership. Free routing between polarities does not alter these requirements. An adaptive/alternating correct strategy must charge the whole strategy and universal branches, not only one successful existential branch. Certificate replay, all failed guesses, child calls, materialization and peak *writable* workspace are charged; read-only input/certificate tape length is separately reported.

If the \(N^{.195}\) rows already enumerate all shared z, do **not** multiply by another \(2^q\). Scanning all \(N^{.195}N^{.65}=N^{.845}\) blocks and using a hypothetical total deterministic SAT child solver of exponent c on block size \(N^{.35}\) yields the **conditional** time ledger \(N^{.845+.35c+o(1)}\) plus source and witness processing. At c=1.33 this gives 1.3105; to fit 1.33 requires c<=97/70 approx 1.385714, *provided* the child solver's writable space, negative correctness, uniformity and complete source processing also meet budget. A merely unspecified polynomial SAT seed is not sufficient. If the row index and shared assignment enumeration are independent axes, their extra cost must be added.

Sources and exact model exclusions: Fortnow--Lipton--van Melkebeek--Viglas (JACM 2005) give a deterministic random-access SAT exclusion below golden-ratio time with some strictly positive space exponent, and a co-nondeterministic SAT exclusion below sqrt(2) time with some strictly positive space exponent [2]. The published Fortnow/van Melkebeek tradeoff expression at time exponent c=1.33 yields space threshold \(((c+2)/c^2-c)/2\approx0.276263\), **not 0.5** [3]. Williams and Buss--Williams yield the c<2cos(pi/7) approx 1.80194 threshold for deterministic RAM **subpolynomial** space; this is not an exclusion at \(N^{.5}\) space [4,5]. Diehl--van Melkebeek--Williams give a nondeterministic TAUT simultaneous tradeoff for c^2 d<4, in particular equal exponent d<4^(1/3) with *some sufficiently small positive* space exponent [6]; again \(N^{.5}\) is not excluded by that statement. Nondeterministic SAT has short ordinary witnesses and should not be conflated with nondeterministic UNSAT/TAUT. Exponential lower bounds for Resolution are proof-system-specific, not a universal algorithm bound [7]. No cited tradeoff rules out the full proposed deterministic \((N^{1.33+o(1)},N^{.5}\mathrm{polylog}N)\) pair. P versus NP is OPEN.

## References

[1] Erdos, P., *Graph theory and probability*, Canad. J. Math. 11 (1959), 34-38; high-girth/high-chromatic existence, also discussed at https://doi.org/10.1002/jgt.1017.

[2] Fortnow, Lipton, van Melkebeek, Viglas, *Time-space lower bounds for satisfiability*, JACM 52 (2005), https://doi.org/10.1145/1101821.1101822.

[3] Fortnow and van Melkebeek, *Time-Space Tradeoffs for Nondeterministic Computation*, DIMACS TR 2000-06, https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html.

[4] R. Williams, *Inductive time-space lower bounds for SAT and related problems*, Computational Complexity 15 (2006), https://doi.org/10.1007/s00037-007-0221-1.

[5] Buss and Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Computational Complexity 24 (2015), https://doi.org/10.1007/s00037-015-0104-9.

[6] Diehl, van Melkebeek, Williams, *An Improved Time-Space Lower Bound for Tautologies*, J. Combin. Optim. 22 (2011), https://doi.org/10.1007/s10878-009-9286-x.

[7] Haken's Resolution pigeonhole lower bound, summarized in https://arxiv.org/abs/0909.5038.

**Remaining gap:** prove something about the unavoidable global cost of choosing five-letter equality classes that survives arbitrary algorithms' explicit source access. The finite forbidden basis and syndrome count are exact solvers/certificates; neither yields an unrestricted lower bound. Physical low-space replay, full LaTeX compilation and external mathematical review remain outstanding.
