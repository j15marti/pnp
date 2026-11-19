# TMR-2/095: Source-embedded oracle lower bound, correct-path certificates, and an authenticated streaming countermodel

**Owner:** TMR-2 / PNP Information Necessity. **Date:** 2026-11-18, America/Los_Angeles. **Primary object:** the original five-symbol beat-relation CSP with (R(a,b)=[b-a\pmod5\in\{1,3\}]). **Statuses:** theorems below PROVED for stated source family / cell-probe model; exhaustive finite tests COMPUTATIONAL; unrestricted SAT time-space lower bounds OPEN. No assertion that $P\ne NP$ has been established.

## 1. New result: an AND-of-OR oracle table embedded in genuine, explicit CNF

Let $q\ge1$, (r=2^q), $m\ge1$, and let (h=(h_{z,b})\in\{0,1\}^{r\times m}) be arbitrary independent bits. Shared variables are $z_1,\dots,z_q$. For each row index $u\in\{0,1\}^q$, set
$$
G_u(z)=\bigvee_{i=1}^{q}\begin{cases}z_i&u_i=0,\\ \neg z_i&u_i=1.\end{cases}
$$
Thus (G_u(z)=0) if and only if (z=u). Each cell ((u,b)) owns its own new private variable (y_{u,b}); put into the *actual input CNF* the pair of clauses
$$
B_{u,b}^{(h)}(z,y_{u,b})=
 (G_u(z)\lor y_{u,b})\land
 (G_u(z)\lor (-1)^{h_{u,b}}y_{u,b}).
$$
(Here (h=0) means the second literal is (y), and (h=1) means $\neg y$.) The complete source (F_h=\bigwedge_{u,b}B_{u,b}^{(h)}) has exactly (2rm) clauses of width (q+1) and (q+rm) Boolean variables. Private scopes are pairwise disjoint. One genuine literal-sign field, not a freely assumed oracle response, encodes each independent table bit. Its fixed-shape DIMACS rendering has (\Theta(rm(q+1))) literal occurrences and (O(rm(q+1)\log(rm+q))) ordinary encoded bits. In a padded fixed-record model the (rm) flags each occupy a separate addressable record.

**Theorem 095-A (source embedding, proved).** For every (z=u), the existential projection of cell ((u,b)) to its private variable is true exactly when (h_{u,b}=0); all other row cells are automatically true. Consequently
$$
\boxed{\mathrm{UNSAT}(F_h)\iff \bigwedge_{u\in\{0,1\}^q}
                        \bigvee_{b=1}^{m} h_{u,b}.}
$$
Moreover, with (g(h)=\#\{u: h_{u,1}=\cdots=h_{u,m}=0\}),
$$
\boxed{\#\mathrm{SAT}(F_h)=g(h)\,2^{(r-1)m}.}
$$
The latter counts every private-variable assignment, not merely distinct shared (z). This construction realizes *all* (2^{rm}) independent bit tables as genuine, syntactically almost identical CNFs. Unlike /094's oracle-only theorem, this result survives access to the explicit original source, within the indicated restricted family.

**Duplicate-free source strengthening (proved).** If the chosen CNF grammar prohibits repeated clauses, replace each two-clause cell by three *pairwise distinct* clauses, using two fresh private variables per cell: \((G_u\lor y)\), \((G_u\lor ((h=0)?y:\neg y)\lor t)\), and \((G_u\lor\neg t)\). At its selected row, \(h=0\) has exactly the unique local assignment \((y,t)=(1,0)\), whereas \(h=1\) is contradictory. An inactive cell has four free private assignments. The exact count becomes \(g(h)\,4^{(r-1)m}\), and the same independent sign-cell lower bound and SAT/UNSAT predicate survive. Each cell still has one independently switchable literal-sign position, the same width \(q+1\) to \(q+2\) up to constants, and no duplicate clauses. An additional 100 matrices were directly brute-counted in this variant. This removes reliance on a duplicate-permitting CNF syntax.

## 2. What deterministic information lower bound actually survives

**Theorem 095-B (source-sign-probe bound, proved).** On the promise that all non-flag fields have the preceding fixed form and the (rm) sign fields are independent, every correct deterministic adaptive decision tree using individual sign-cell probes has worst-case cost exactly (rm). Proof: answer zero to the first (m-1) *distinct* probes in each row and answer one to the final probe in that row, regardless of row interleaving. The resulting source is UNSAT. Until every cell of every row has been probed, an incomplete row can still be completed all-zero (SAT) or with a one (UNSAT), consistently with the transcript. Thus every cell must be visited; a full scan matches the bound.

With a word that can expose at most (w) independently encoded signs, this gives only (\Omega(rm/w)) word probes; with one dedicated sign per input record, the stronger (rm) record-probe bound holds. Syntax authentication of *arbitrary* non-promised sources costs additional time and must not be omitted.

**Barrier (proved for this family).** The source already contains at least (rm) independent flag bits; its explicit text length is (N=\Omega(rm)), and a direct authenticated parser decides the entire family in (O(N)) time. Hence these source-surviving search lower bounds do *not* prove any superlinear lower bound in input size (N), let alone a superpolynomial one. With $r\le N^{.195}$ and $m\le N^{.65}$, the flag count is at most (N^{.845}), with logarithmic representation overhead. The simultaneous literal-size caps have slack on this family; neutral source padding is possible but is not a hardness amplifier.

The prior /094 three-step Resolution refutation provides the complementary source-compression counterexample: on a *correlated* matrix, original-source algebra can reduce even a seemingly complete refutable-block cover to a constant-length proof. These are consistent findings, not rival global lower bounds.

## 3. Ideal correct-path algorithm and wrong-path soundness, separately by polarity

For this explicit family an UNSAT correct-path proof supplies one column index (b(u)\in\{1,\dots,m\}) *for each of all (r) shared rows*. Its read-only advice length is $k_{-}=r\lceil\log_2m\rceil$ bits (zero data bits per index when (m=1)); verification tests the (r) identified original signs and checks the complete source grammar. A SAT correct path supplies one all-zero row (u), with (k_{+}=q) bits, and checks *all* (m) signs of that row. All one-sided accepting outputs are source-verified: a bad UNSAT choice on any row is rejected, and a SAT row containing a one is rejected. When no valid certificate exists, output INVALID/UNKNOWN; no wrong-path acceptance is allowed.

There is a single-pass authenticated parser for this fixed source family, using (O(N)) time including *all* source records and (O(q\log(rm)+\log m)) writable bits with sequential read-only input/certificate tapes (plus constant parser state and counters). If the entire negative advice is instead stored in writable space, charge an additional (k_{-}) bits. The Python execution implements these semantics but is **not** a physical low-space RAM implementation: Python object/materialized-file storage is much larger. For a nondeterministic supplied read-only path, certificate generation is free only by explicit model assumption, never in a deterministic solver. Enumerating all candidate negative paths costs up to (m^r=2^{\Theta(k_{-})}) verifier executions. A programmatic selector that scans each row is sound but incurs its failed queries; it does not magically supply a free global correct path.

For the *arbitrary-CNF* block grammar, local NO certificates additionally require real, checked child refutations; an index alone is insufficient. SAT certificates require all positive private witnesses. Neither free polarity routing nor a single successful trajectory implements the universal proof obligation. Alternating strategies must charge every universal branch or supply a verifiable, fully specified strategy with its own cost.

## 4. Quantitative resource ledger and sourced model firewall

For an authenticated external iterator over at most (N^{.195}) rows, (N^{.65}) blocks/row, and child strings of length at most (N^{.35}), a sequential all-children composition with child SAT time (L^{a}) costs, *conditionally on those caps actually coexisting and charged materialization*,
$$
 T\ \le\ T_{\mathrm{auth}}+
 O\big$2^q N^{.845}\big[N^{.35}+N^{.35a}\big]\,\mathrm{polylog}\,N\big$.
$$
For (a=1.33) the stated per-shared-assignment exponent is (0.195+0.65+0.35(1.33)=1.3105). To fit (N^{1.33+o(1)}), the enumeration (2^q) has at most an extra (N^{.0195+o(1)}) multiplicative allowance. This is **not** an impossibility theorem for clever source-aware solvers and assumes (N^{.195}) rows *and* an extra independent (2^q) outer factor; if rows are precisely the (2^q) shared assignments, do not multiply the same row count twice. The fixed-cell family here is the latter case and runs in linear source time.

The following results apply to their stated computation models, *not* to externally supplied free proof bits: Fortnow--Lipton--van Melkebeek--Viglas obtain deterministic random-access SAT time-space exclusions; a quantitative precursor states the region (b<((a+2)/a^2-a)/2) for time (N^a), space (N^b). At (a=1.20), the threshold is $23/45\approx .5111$, whereas at (a=1.33) it is $977363/3537800\approx .2763$; therefore this stated curve does not exclude ((1.33,.5)). Williams improves subpolynomial-workspace deterministic SAT time bounds to the (2\cos$\pi/7$\approx1.8019) regime; Buss--Williams show the limit of the **specified alternation-trading framework**, not a barrier to every possible method. For conondeterministic SAT / nondeterministic TAUT, Diehl--van Melkebeek--Williams give (N^{4^{1/3}-o(1)}) time lower bounds when workspace is (N^{o(1)}); this does not rule out (N^{.5}) space. Ordinary nondeterministic SAT already has linear-time witness verification in appropriate encoded-access models; no corresponding unrestricted NP-versus-coNP separation follows. Resolution proof-size lower bounds remain proof-system-specific.

## 5. Executed finite audit and five-symbol T5 controls

The standalone, fully executed Python implementation checked every flag matrix for ((q,m)=(1,1),(1,2),(1,3),(2,1),(2,2)), respectively (4,16,64,16,256) sources (total **356**), plus **100 duplicate-free-source variants**. It rendered, reparsed, directly counted all Boolean assignments, compared the analytic exact count, accepted correct source-authenticated SAT/UNSAT paths, rejected false UNSAT paths on every SAT source, and rejected corrupted/truncated/trailing sources. It also ran multiple source-cell probe orderings against the adaptive last-one adversary. **13,396 assertions, zero failures**. These are computational finite checks, not a general formal-machine replay.

As required, the unchanged original T5 girth-five four-path matched sources were independently counted with the published /093 cycle-syndrome dynamic program. Both use 9 vertices, 11 arcs, $\beta=3$, 119 peak states and 644 charged updates; their exact solution counts are **0** and **135**. A four-bit first-violated-real-arc selector exists on both; short-path reduction remains a legal source-aware shortcut. No inference of a search lower bound is justified by their equal state counts.

**TMR-4 handoff invariant:** `D2-SOURCE-EMBEDDED-SIGN-CELL-FRONTIER095`. It separates independent source cells, authenticated syntax parsing, correct-path certificate length, wrong-path soundness, read-only advice, writable peak space, and genuine source-visible shortcuts. It rules out transporting an (rm)-probe lower bound as $N^{1+\delta}$ runtime without a source-compression or computation lower-bound argument.

## 6. References and outstanding work

[1] Fortnow, L., Lipton, R., van Melkebeek, D., Viglas, A. *Time-space lower bounds for satisfiability.* JACM 52(6), 835–865 (2005). https://doi.org/10.1145/1101821.1101822

[2] Fortnow, L. and van Melkebeek, D. *Time-Space Tradeoffs for Nondeterministic Computation* (2000); quoted quantitative random-access curve. https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html

[3] Williams, R. *Time-Space Tradeoffs for Counting NP Solutions Modulo Integers* (2007), ECCC TR07-036. https://eccc.weizmann.ac.il/eccc-reports/2007/TR07-036/index.html

[4] Buss, S. and Williams, R. *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds.* Computational Complexity 24, 533–600 (2015). https://doi.org/10.1007/s00037-015-0104-9

[5] Diehl, S., van Melkebeek, D., and Williams, R. *An Improved Time-Space Lower Bound for Tautologies.* Journal of Combinatorial Optimization 22, 325–338 (2011). https://doi.org/10.1007/s10878-009-9286-x

Remaining OPEN: unrestricted simultaneous (N^{1.33+o(1)}) time and $N^{.5}\mathrm{polylog}\,N$ work-space status for arbitrary SAT, fully sourced native-machine instruction counts, the existence of a general authenticated child iterator respecting each original structural cap, full LaTeX compilation and external mathematical review. No project schedule, agent identity or other agent-owned manuscript is changed. **P versus NP remains open.**
