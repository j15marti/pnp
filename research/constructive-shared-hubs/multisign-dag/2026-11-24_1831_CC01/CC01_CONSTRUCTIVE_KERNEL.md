# CC01: Constructive diamond-chain repair, exact joint states, and the irreducible cubic kernel

**2026-11-24 18:31 PST.** Repository: j15marti/pnp. Coordination: issue #327.  
**Status:** PROVED/EXACT within the stated cubic matching domain; COMPUTATIONAL controls executed; independent mathematical review pending. Universal polynomial progress and P versus NP remain **OPEN**.

## 1. Outcome and integration point

This iteration falsifies the proposed initial neighborhood-dominance escape for the exact two-perfect-matching encoding. Every alternative in every original cubic vertex clause has an opposite-track conflict that distinguishes it from each other alternative. The initial binary relaxation has no forced membership literals. Its conflict graph also fails the disjoint-resource-clique condition. This is a statement about these specified rules, including on easy colorable graphs, not a hardness theorem.

The constructive replacement is an automatically acquired, exact four-state quotient for private two-port diamond strings. It preserves edge-local guards, the minimum of an additive cost, the number of feasible ordered matching pairs, the number attaining that minimum, and an original-source reconstruction. No manifest or frontier order is supplied to the new detector.

For a cubic base graph G, replace edge e by a string of m_e diamonds. The following identities hold for all such graphs, not just the finite examples:

\[
 \kappa(G_{\mathbf m})
 =
 \min_{P,Q\in\operatorname{PM}(G)}
 \sum_{e\in P\cap Q}(2m_e+1),
 \qquad
 \kappa(G_m)=(2m+1)\kappa(G),
\]

where \(\kappa(G)\) is the minimum overlap of two perfect matchings, with infinity when no pair exists. For canonically lifted starting matchings A,B and a zero-overlap target, the minimum repair distance satisfies

\[
 \operatorname{dist}_0(G_m,\widehat A,\widehat B)
 =
 (4m+1)\operatorname{dist}_0(G,A,B).
\]

Thus arbitrarily long repairs can be discovered by solving a fixed kernel and lifted with polynomial work, despite linear repair size. Growing bipartite kernels also admit a polynomial constructive terminal, with no bounded-width requirement.

The universal implication does not follow: inflating every edge of an arbitrary cubic graph and then applying this detector returns that arbitrary graph. Diamond abundance does not guarantee a tractable remaining kernel. This exact obstruction to the proposed completion arrow is part of the result.

The selected pipeline is:

**Explicit cubic source and actual edge IDs → certified unit/binary closure → automatic private diamond discovery → exact joint boundary tables → certified kernel closure → a declared kernel terminal → original matching reconstruction and verification.**

The source is the cubic matching domain of the recovered repair experiments. This report does not provide a strict E4/B4 physical compiler or equate cubic edge coloring with every signed tetrahedral representation.

## 2. Recovery and source discipline

Read AGENTS.md, CODEX.md, the repository pnp-research skill, relevant coordination directives, issue #327, recent comments through M18, and the original BS11, BW12, M18, DO12, DP12 and BD11 reports. Revisited the named hypothesis/resource sections of DO01, DP01 and S06. Exact file blob IDs, bounded searches and review depths are in [CC01_sources.json](CC01_sources.json).

Recovered and read the full earlier constructive_repair_series.py and frustration_2sat_exchange.py, plus the saved repair-series results. Two supplied backing-file IDs were stale. Refreshing their metadata recovered the current files. The original repair-series script is preserved unchanged in [baseline/constructive_repair_series.py](baseline/constructive_repair_series.py). Five of its trap cases were actually rerun and compared with the new compiler. The NetworkX-dependent exchange-acquisition suite was read but not rerun; its matching acquisition success is not assumed universal.

There is no local git checkout and no assigned TMR manuscript. Repository preflight was therefore not executed. Publication is additive in this iteration's directory. No agents, schedules, identities or peer manuscripts were changed. The first twenty branch names were inspected, not all branch contents. This is not an exhaustive audit of every prior chat or agent result.

The pre-experiment target and falsifiers are preserved in [CC01_TARGET.md](CC01_TARGET.md). No novelty priority is claimed for diamond strings, which are established graph-theoretic objects. The contribution here is the costed two-track interface, automatic implementation, exact scaling identities, and their integration into the current repair question.

## 3. Exact source encoding and the dominance obstruction

Let G be an explicitly encoded finite simple cubic graph with edge set E. Introduce Boolean variables \(a_e,b_e\), indicating membership in the two matchings. For each vertex v and track \(c\in\{a,b\}\), impose

\[
 \bigvee_{e\ni v}c_e,
 \qquad
 \neg c_e\lor\neg c_f\quad(e\ne f,\ e,f\ni v).
\]

For a zero-overlap target also impose \(\neg a_e\lor\neg b_e\) for every edge. Exactly one incident edge is selected per track per vertex. Hence models are exactly ordered edge-disjoint perfect matching pairs. Their complement is a third perfect matching, giving a proper labeled three-edge-coloring; any such coloring supplies the converse.

Write F as B together with the positive ternary vertex clauses, where B contains the negative binary exclusions. Canonicalize repeated occurrences by their actual edge-variable IDs. The variable conflict graph is

\[
 K=L(G)\mathbin{\square}K_2:
\]

two copies of the line graph of G, with a vertical conflict joining the two copies of each edge. This notation describes the actual binary conflicts; no independent-copy relaxation is taken.

A selection of one candidate per positive clause extends through B exactly when its selected variables are pairwise nonconflicting: set precisely those variables true and all others false. The same edge variable appearing at both endpoints remains one variable. Every valid group selection therefore reconstructs an actual pair of perfect matchings.

### CC01-A: Initial neighborhood dominance always stalls

Fix a vertex clause on track a and two distinct incident edge alternatives e,f. The variable \(b_f\), occurring outside this clause group, conflicts with \(a_f\) and does not conflict with \(a_e\). Conversely \(b_e\) conflicts with \(a_e\) and not \(a_f\). Thus their exterior neighborhoods are incomparable. The same argument applies to track b and to every vertex.

Therefore no alternative can be deleted by the rule “replace an alternative by one with an exterior conflict-neighborhood subset” at the initial unguarded encoding. This proof applies whether same-literal occurrences have been merged or are retained with source identity.

The binary relaxation has no forced literal: all-zero is a model, and each single-positive variable word is also a model. Its implications go only from positive to negative literals, so there are no nontrivial implication SCC equalities.

Finally, for adjacent edges e,f on track a, the three vertices

\[
 b_e,\quad a_e,\quad a_f
\]

induce a path. Hence K is not a disjoint union of cliques. The resource-clique matching terminal also fails its structural premise.

This refutes Candidate A even for K4 and bipartite cubic graphs, which have easy colorings. It does not say all sound deduction systems stall. Diamond boundary equalities, global matching facts, symmetry handling, and other certified regional reasoning remain legitimate.

Neighborhood dominance is itself an existential replacement rule. Where it does apply in a later state, deleting an alternative is not automatically a certificate that the original source literal is false. Source lift provenance must be retained.

## 4. Private two-port geometry and exact local states

A diamond has four private vertices a,b,c,d and the five edges

\[
 ac,\ ad,\ bc,\ bd,\ cd.
\]

Vertices a,b have one additional incident boundary link each; c,d have no outside incidences. This is the induced graph K4 minus ab. The two boundary links are actual observations, not extra free ports.

For one perfect matching, let x,y be selection bits on the boundary links at a,b. Counting selected incidences on the four private vertices gives

\[
 x+y+2|M_{\rm internal}|=4.
\]

Thus x+y is even and x=y. There are exactly these internal possibilities:

| Common boundary bit | Internal matching |
|---|---|
| 0 | \(X=\{ac,bd\}\) or \(Y=\{ad,bc\}\) |
| 1 | \(Z=\{cd\}\) |

Both directions are immediate: these choices cover the required private vertices exactly once, and the incidence count excludes unequal boundary bits. This is a complete local proof, not an empirical table inference.

For two tracks the boundary word is \(q=(x_a,x_b)\in\{00,10,01,11\}\). It must remain joint. There are respectively 4,2,2,1 raw internal pairs before imposing overlap or other local restrictions. Marginals alone are insufficient: for example a joint domain \(\{00,11\}\) has full marginals but excludes 10 and 01.

### Edge-local guards and costs

Give every actual source edge e an explicit table

\[
 w_e:\{00,10,01,11\}\longrightarrow
 \mathbb Z_{\ge0}\cup\{\infty\}.
\]

Infinity forbids that joint word. This includes pins, equal/different track membership, overlap prohibitions, a no-new-overlap condition, and a seed edge that must stop being shared. It also includes additive overlap cost \(1_{q=11}\), arbitrary binary-encoded nonnegative costs, or movement from a supplied reference pair:

\[
 w_e(q)=
 [q_a\ne 1_{e\in A}]+[q_b\ne 1_{e\in B}].
\]

For each boundary word, enumerate the at most four local internal pairs, check the five actual edge tables, and retain:

\[
 (\text{minimum cost},\ \text{all feasible count},\
   \text{minimum-cost count},\ \text{one minimizing lift}).
\]

Impossible entries remain impossible. This is constant-size local acquisition with explicit source checks. Costs and counts are not replaced by support or affine hull.

**Scope:** arbitrary guards comparing private edges of different diamonds, protected global parity tags on private choices, external integer quotas, and unspecified physical observations are not covered by these four entries. They must be retained in a larger authenticated interface or the contraction must decline. A small table is justified here by the proved private-boundary contract.

## 5. Automatic discovery and exact composition

### CC01-B: Discovery without a manifest

For each source edge cd, inspect the common neighbors of c,d. It is the center edge of an induced diamond precisely when it has two common neighbors a,b and ab is absent. Cubic degrees ensure that the five internal edges and the two external link incidences are the whole local structure.

Distinct induced diamonds in a simple cubic graph are vertex-disjoint. To see this, in a diamond the center vertices already have all three neighbors inside it. A center-tip edge has only one common neighbor because the two tips are nonadjacent. A tip's outside neighbor cannot be adjacent to either center, whose degree is saturated. Consequently a second center edge cannot share a center or a tip with the first diamond. If an overlapping vertex were a tip of the second diamond, its two adjacent centers must be the first diamond's centers, giving the same diamond. K4 is excluded by the ab test and remains a constant-size core.

After detection, follow the unique external link at each tip. Every diamond component is either a maximal string between retained vertices or a closed necklace. Each private diamond and each connecting source edge is visited once. Retain the actual IDs of all links and internal edges. The verifier checks that these blocks partition the source edge set exactly.

Contraction can produce parallel edges or loops. Parallel edges remain distinct resources. A loop is unusable in a perfect matching because it meets its vertex twice; the kernel includes this restriction explicitly. Closed necklaces are independent components and are handled as four-state closed tables. These cases are implemented and tested.

With explicit indexed adjacency lists, discovery and traversal require linear graph work, plus deterministic indexing/sorting overhead. A conservative polynomial bit-time bound includes all identifiers. The implementation uses Python dictionaries and sets; no unit-cost assumption for arbitrary-size arithmetic is used in the theorem.

### CC01-C: Pointwise composition

On a string, each diamond forces equality of the left and right boundary bit separately for each track. Hence the same joint word q runs through the whole string. For that q:

\[
 T_{\rm string}(q)
 =\sum_{\text{links }e}w_e(q)
  +\sum_{\text{diamonds }D}T_D(q).
\]

An infinite summand makes the entry impossible. The feasible count is the product of the local feasible counts; the minimizing count is the product of local minimizing counts. Internal edge sets are disjoint and the boundary bits are fixed, so both products are exact. One minimizing local choice per diamond gives a minimizing lift.

For a closed necklace, sum feasible counts over all feasible q, and minimize cost over those q. No preferred boundary state is silently assumed.

For a fixed kernel pair P,Q, each kernel edge has a determined joint word. Its exact expansion count is the product of the corresponding string counts, and its minimum expansion cost is the sum of the string costs. Different kernel pairs have disjoint source fibers. Therefore a kernel solver may sum those counts or minimize those costs without overcounting or losing a source solution.

Conversely, restrict any source matching pair to its string boundary words. The local equality proof makes them consistent, and exactly-one constraints at retained vertices make each track a kernel perfect matching. Thus every source solution projects. This proves both SAT directions, exact counts in the stated source language, optimization, and reconstruction.

This is not an appeal to compact DAG size alone. The only private work compressed is a disjoint product conditioned on a complete, constant-size interface. Global kernel coverage remains an explicitly charged separate obligation.

## 6. Infinite-family identities and large repair discovery

Write \(G_{\mathbf m}\) for the graph obtained by replacing edge e with \(m_e\) diamonds and \(m_e+1\) links. Zero is allowed, meaning the original edge.

### CC01-D: Exact minimum overlap

If both kernel matchings select e, both expanded matchings must use every link and every center edge cd in that string. This forces \(2m_e+1\) shared edges.

For joint states 10 and 01, one track uses Z plus links and the other uses X or Y, so no edge is shared. For 00, choose X in the first track and Y in the second at every diamond, again giving no shared edge.

Every expansion therefore has overlap at least the weighted kernel intersection, and these local choices attain that lower bound simultaneously. This proves the identity in Section 1, including nonuniform lengths. The source minimum need not be logarithmic or bounded: it can grow linearly even when a constant-size exact certificate explains it.

For a fixed zero-overlap kernel pair, every diamond has exactly two disjoint internal lifts in each of the three allowed joint boundary modes. Hence

\[
 \#\{\text{ordered disjoint pairs in }G_{\mathbf m}\}
 =
 2^{\sum_e m_e}
 \#\{\text{ordered disjoint pairs in }G\}.
\]

The kernel count is not supplied for free. This formula concerns ordered matching pairs, equivalently labeled three-edge-colorings of this graph, not physical wheel counts or counts of arbitrary original SAT assignments.

### CC01-E: Exact movement scaling

The canonical lift of a matching uses Z and all links on selected kernel edges; on unselected edges, use X for the first track and Y for the second.

When one track changes a kernel edge's membership, all \(m_e+1\) links change and each of the \(m_e\) diamonds changes between a one-edge Z and a disjoint two-edge X or Y. Thus exactly

\[
 (m_e+1)+3m_e=4m_e+1
\]

source membership bits must change. Any lift of the changed boundary mode incurs at least this cost. An unchanged mode can retain its canonical pattern at zero cost.

Canonical target lifts of disjoint kernel matchings attain these lower bounds simultaneously, including at joint mode 00. Therefore

\[
 \operatorname{dist}_0(G_{\mathbf m},\widehat A,\widehat B)
 =
 \min_{\substack{P,Q\in\operatorname{PM}(G)\\P\cap Q=\varnothing}}
 \sum_e(4m_e+1)
 \bigl([e\in A\triangle P]+[e\in B\triangle Q]\bigr).
\]

The uniform-length formula follows. A similar restriction to permissible kernel intersections handles the canonical no-new-overlap guard. Arbitrary noncanonical starting internal choices remain covered by the actual cost tables, but need not obey the simple scalar formula.

The previously saved eight-vertex unilateral trap has five perfect matchings. Keeping either starting track fixed has minimum overlap one, while the minimum joint zero-overlap movement is ten. These finite base facts are independently checked by enumerating the five matchings. The identities imply, for every integer m>=0:

\[
 |V|=8+48m,\quad
 \text{initial overlap}=2m+1,\quad
 \text{minimum joint repair movement}=10(4m+1).
\]

The unilateral minimum remains \(2m+1\). Thus this is a genuine cooperative family: every successful zero-overlap repair changes both tracks. The repair length grows without bound, but automatic contraction, a constant-size kernel solve, and explicit reconstruction discover it with polynomial work. There is no search through all large repairs.

## 7. Both-label infinite controls and a wider positive terminal

### Petersen minimum and a one-clause neighbor

The standard Petersen graph has six perfect matchings. Here is a short structural verification. Count selected spokes between its outer pentagon and inner pentagram. The number must be odd. Three spokes would leave two outer vertices and the corresponding two inner vertices: those indices would have to differ by both one and two modulo five, impossible. Five spokes give one matching. For each of the five choices of a single spoke, the remaining four outer and four inner vertices each form a path with a unique perfect matching. These give the other five.

Two distinct members intersect in exactly one edge. The all-spoke matching shares the unique spoke of each other matching. For two one-spoke matchings, cyclic symmetry reduces the check to spoke indices differing by one or two; the outer/inner path matchings give exactly one common edge. Each Petersen edge lies in exactly two of the six matchings. Thus \(\kappa(\mathrm{Petersen})=1\).

Uniform inflation gives an infinite family with minimum overlap exactly \(2m+1\), and zero-overlap UNSAT. An exact certificate consists of the acquired quotient map, the fixed six-matching base certificate, and the local overlap lower bounds.

For a closer opposite-label control, keep one distinguished Petersen edge e0 uninflated and inflate all other fourteen edges by m diamonds. Impose every zero-overlap clause. This is UNSAT. Delete only

\[
 \neg a_{e_0}\lor\neg b_{e_0}.
\]

The two distinct base matchings containing e0 now give a legal pair whose only shared edge is e0. Every other string has a non-11 boundary mode and two choices per diamond. Thus the SAT neighbor has exactly

\[
 2^{14m+1}
\]

ordered matching-pair models and minimum overlap one. The two inputs have the same graph and differ in exactly one binary source clause. The minimum is a matching-overlap count; no identification with arbitrary parity-frustration minima is assumed.

### Arbitrarily growing bipartite kernels

For the zero-overlap problem, with source state 11 forbidden on every edge, suppose the automatically obtained loopless cubic kernel is bipartite and every kernel edge allows states 00,10,01. Construct a perfect matching by deterministic augmenting paths. Hall's condition follows from cubic regularity: for a subset U of one side, its \(3|U|\) incident edges meet at most \(3|N(U)|\) incidences, so \(|N(U)|\ge|U|\).

The complement is a disjoint union of even cycles, including length-two cycles from parallel edges. Alternating their edges gives two further perfect matchings. Select two color classes and lift them through the stored string tables.

This handles an infinite class with an arbitrarily growing core and does not require a frontier-width bound or enumerating all core matchings. On the executed unpinned controls all source overlap clauses are enforced, so the produced pair is disjoint.

It is a constructive feasibility terminal. The implementation does not claim minimum movement or a global count for these growing bipartite kernels. Arbitrary additional pins, correlated missing boundary states or general color-dependent costs are not covered by this simple terminal. It conservatively declines unsupported instances.

## 8. Precisely why the universal proof remains open

For any simple cubic graph G, inflate every edge by at least one diamond. The old vertices then have pairwise nonadjacent new neighbors, so they are not part of a new induced diamond. The detector finds the inserted diamonds and contraction returns exactly G with actual edge IDs.

Consequently the presence of arbitrarily many distributed diamond gadgets does not force the quotient to become bipartite, bounded, or otherwise easy. The four-state interface can represent the unresolved original graph exactly.

Deciding cubic three-edge-colorability is NP-complete [3]. The two-disjoint-perfect-matching equivalence above connects that known problem directly to the remaining kernel. This is a diagnostic equivalence, not a proof that no polynomial kernel solver exists. Proving one would be the desired breakthrough.

The missing universal lemma is now stated in operational terms:

> Given an arbitrary authenticated cubic kernel after certified closure, discover, in deterministic polynomial total work, either a valid pair of disjoint perfect matchings, a complete negative decision, or an exact further reduction whose total descendant work has a uniform polynomial bound.

A polynomial-size exchange description, a compact circuit for its guards, or an existential coloring supplying the needed exchanges does not by itself prove that lemma. Nor does failure of the present dominance rule or diamond reduction imply P!=NP.

For a fixed total exact portfolio A with a fair polynomial-overhead schedule, if A has no uniform polynomial time bound, increasing-size inputs can be chosen with \(T_A(F_j)>|F_j|^j\). Efficiently acquired members of the terminals proved here cannot persist in such a sequence for sufficiently large j. This excludes covered inputs for that fixed portfolio; it neither constructs a sequence hard for all algorithms nor supplies a contradiction on the remaining kernels.

## 9. Closure, representation and complete resource ledger

The implementation runs unit propagation and complete forced-literal inference in the current binary relaxation before discovery. It retains every longer clause, simplifies it after every new pin, rebuilds the binary relaxation, and repeats to a fixed point. Implication SCC equalities are registered without deleting original clauses. An all-negative binary relaxation has a direct fixed-point certificate from the all-zero and single-positive models.

After exact projection, closure is repeated on the kernel, including forbidden joint boundary states, loops and shortened vertex clauses. Necessary pins restrict the tables, followed by a recheck. At stagnation the same fixed-point archive can be reused for unchanged clauses. A source pin is distinct from a selected witness bit or an existential reduction choice.

This is a specified certified closure repertoire. It is not complete semantic closure on the unresolved kernel. No cost-free SAT query is used to discover all global consequences. The small-kernel reference terminal does exact paid enumeration; the bipartite terminal uses the explicit augmenting-path construction. Unsupported large cores return UNKNOWN.

Let N be the complete bit length of the explicit graph, edge IDs, four-entry costs/guards, reference pair and required output. Let k be the retained kernel vertex count.

| Work item | Charged scope |
|---|---|
| Source acquisition and validation | Read explicit graph, validate simplicity/cubic degrees, retain every actual edge ID and table. |
| Closure | Repeated clause scans and implication reachability, all failed searches included; polynomial in N for this fixed repertoire. |
| Discovery | All center-edge tests, common-neighbor checks, exact partition verification, string/ring traversal and indexing. |
| Local compilation | Nine raw internal pair choices total across the four boundary words per diamond; four entries per string/ring. |
| Arithmetic | Exact costs and counts. Counts need O(N) bits because there are at most \(4^{|E|}\) edge-state words. Cost bit lengths include input magnitudes and sums. |
| Canonicalization and reuse | Fixed source edge IDs and current explicit joint guards. No graph-isomorphism oracle or semantic cross-guard equivalence test. |
| DAG and aggregation | O(N) local choice/lift records; four states per private block. Every consumer and every kernel matching-pair check is charged. |
| Kernel discovery/decision | Bounded-kernel enumeration is exponential in variable k. For a fixed cap it is a polynomial terminal. The supported bipartite feasibility backend is polynomial for unbounded k. |
| Reconstruction | One source-edge state per actual edge, followed by exact source perfect-matching, cost and guard verification. |
| Peak space and memory | Polynomial source, table, count and lift storage on covered executions. Same serial execution has CM <= (T+1)S; physical cumulative memory was not measured. |

There are polynomial bit-time implementations using deterministic indexing. A conservative bound for the specified closure plus private compilation is polynomial, for example O(N^4) with straightforward repeated reachability and bit operations; this is not a tight performance claim. Cubic bipartite augmenting paths use O(k^2) graph operations with the simple implementation. Fixed-kernel enumeration has at most \(3^{k/2}\) matching branches per track and at most \(3^k\) pair combinations, with additional polynomial work.

The acquired unary contraction removes four vertices per diamond and has only polynomial private interface/lift growth. That supplies unary progress credit. It does not establish the aggregate inequality \(\sum_i\mu(F_i)^c\le\mu(F)^c-1\) for unrestricted branching. Discovery failures and the remaining kernel still require their own budget.

The separate experimental stages were launched as independent processes. Each timing and peak below belongs to its own full executed process; a fast time from one process is not combined with low space from another. These measurements include assertions and reference checks and are not asymptotic evidence.

## 10. Executed controls and results

All final stages used the same checker SHA-256:

\[
\texttt{b79915ad1dca698363bd4021b1ad0bc333e80ae9a5544396afffcbb23f5b867b}.
\]

Standard library only, Python 3.12.14. Seeds are 2082401 and 2082402. The code, compact results and full compressed raw data are separate artifacts.

| Stage | Exact checks | Elapsed seconds | Traced Python peak bytes | Process peak RSS, KiB |
|---|---|---:|---:|---:|
| controls | Local tables, source-reference comparisons, dominance, neighbors and exceptional topologies | 5.436 | 757,493 | 16,640 |
| scaling | Infinite-family formulas at seven scales; growing bipartite cores | 13.924 | 27,964,981 | 109,260 |
| replay | Five actual calls to the recovered frontier solver, compared with the new quotient | 4.053 | 6,148,002 | 27,064 |

The 193,217 successful assertions are verification counters, not evidence of an unrestricted theorem.

Specific independent controls:

- Twenty-five cubic graphs, including easy and obstructed examples: 2,832 directed neighborhood-incomparability witnesses and an induced conflict path per graph. Initial unit/binary closure produced no pin.
- Eighty random edge-cost/forbidden-word diamond tables: all four boundary entries compared with independent enumeration of all \(2^{10}\) private two-track edge words.
- Seventy full-source instances, including random costs, movement costs, pins, no-new-overlap restrictions and equality/disequality joint boundary guards: 69 feasible and one infeasible. Full source matching-pair enumeration agrees on feasibility, minimum cost, total count and minimizing count.
- Fifteen Petersen distinguished-edge neighbor pairs, with a diamond on a different edge: all fifteen zero-overlap roots UNSAT, all fifteen one-clause-deleted neighbors SAT with exactly four models.
- Parallel kernel edges, closed necklaces and loop-producing contraction checked against independent full-source enumeration. The parallel-edge control has 48 ordered disjoint pairs.
- Total independent full-source pair inspections: 15,880. These enumeration calls are reference work, not claimed polynomial arbitrary-source acquisition.
- The recovered frontier solver was actually rerun at m=0,1,2,4,8 and agreed with the new exact movement optimum in all five cases.

Largest executed examples:

| Family | Source vertices | Source edges | Exact outcome |
|---|---:|---:|---|
| Uniform Petersen inflation, m=128 | 7,690 | 11,535 | Minimum overlap 257, so zero overlap impossible |
| Petersen one-clause neighbor pair, m=128 on fourteen edges | 7,178 | 10,767 | Root UNSAT; neighbor SAT with overlap one and \(2^{1793}\) models |
| Cooperative trap inflation, m=128 | 6,152 | 9,228 | Initial overlap 257; minimum zero-overlap movement 5,130 |
| Automatically recovered growing bipartite kernel | 10,076 | 15,114 | 1,024-vertex kernel; overlap reduced from 1,984 to zero; 8,432 membership changes |

The last row is a constructive witness, not an asserted minimum-movement solution. Its graph was relabeled before discovery; the generating manifest was not passed to the solver.

The finite experiments support implementation correctness on their stated cases. The infinite identities rest on the local proofs and exact composition above. No formal proof assistant or independent external reviewer was used. No universal solver, strict physical compiler, general private-edge tag interface, unrestricted guarded bipartite optimizer, full prior exchange-acquisition suite or measured cumulative-memory experiment was executed.

### Reproduction

From this directory:

~~~bash
python3 CC01_check.py --stage controls --out rerun_controls.json
python3 CC01_check.py --stage scaling --out rerun_scaling.json
python3 CC01_check.py --stage replay --prior baseline/constructive_repair_series.py --out rerun_replay.json
~~~

These stages each finished under thirty seconds in the recorded environment. Machine timings may differ. The exact input generators, raw small inputs, edge tables, graph digests and expected/actual outputs are in [CC01_raw_results.json.gz](CC01_raw_results.json.gz). No external packages are required.

## 11. Peer feedback and proof gates

**BS11:** Higher-weight collective changes can be discovered on these actual matching regions without enumerating their full changes. The compiler preserves exact four-state joint fibers, which is stronger than marginal parity information. It does not establish a universally available occurrence-code repair space.

**BD11 and DP12:** The local interface has directly proved Boolean support and, separately, exact multiplicity and optimum counts. It can be consumed as a four-word factor with actual source IDs. Do not replace that factor by its marginal supports, and do not interpret a decision-only peer projection as supplying these counts. Polynomial private compilation does not bound global factor-graph contraction.

**BW12:** This is a two-port matching gadget with explicit private interiors, not a three-way single-vertex spare-port splitter in the pure signed four-color exclusion language. The port-deficit theorem is not bypassed. Cross-region consumers would invalidate the simple private-interface contract.

**M18:** Actual occupancy and distinct parallel edge IDs are retained. These string tables are suitable local factors for a separately authenticated matching/interface backend, but two simultaneous perfect matchings with their no-overlap condition are not silently reduced to M18's one-matching terminal.

**DO01/DO12:** The examples demonstrate an exact nonlocal projection escape for a specific inflated family. They do not settle ungrafted high-girth affine/NAE cores or show those cores satisfy this compiler's hypotheses. Restricted stagnation and linear raw defects remain compatible with a cheap exact quotient.

**DP01/S06:** A count-box or flow consumer must retain the four-state correlation and all source costs/guards. No independent row-product or tag-constant flow contract is inferred from the existence of a small diamond table.

| Gate | Status and scope |
|---|---|
| DISJ/product sanity | PASS for the declared private-region product: both SAT directions, exact guards and disjoint counting fibers are explicit. No communication lower-bound transfer. |
| Relativization | NOT APPLICABLE as a separation argument; no nonrelativizing universal step is claimed. |
| Simultaneous DTISP | Restricted same-execution polynomial upper bounds; universal decision bound OPEN. |
| Deterministic configuration counting | No configuration-count-to-time lower bound. Used only ordinary finite-state accounting. |
| Natural Proofs / algebrization | No claimed bypass and no unrestricted circuit lower bound. |
| Physical/source-domain transfer | OPEN outside the explicitly authenticated cubic matching domain. |

## 12. Sources and next dependency

[1] Recovered prior implementation, unchanged: [baseline/constructive_repair_series.py](baseline/constructive_repair_series.py). The earlier supplied-order frontier method is the replay comparator, not a free ordering oracle for the new algorithm.

[2] This iteration's [complete checker](CC01_check.py), [compact results](CC01_results.json), [raw results](CC01_raw_results.json.gz), and [source/search ledger](CC01_sources.json).

[3] Ian Holyer, *The NP-Completeness of Edge-Coloring*, SIAM Journal on Computing 10(4), 718-720 (1981). DOI [10.1137/0210055](https://epubs.siam.org/doi/abs/10.1137/0210055). The primary abstract states the cubic restriction. No new hardness result is inferred from it.

[4] M. Abreu, J. Goedgebeur, D. Labbate, G. Mazzuoccolo, *A note on 2-bisections of claw-free cubic graphs*, [arXiv:1707.04452v1](https://arxiv.org/abs/1707.04452), Section 2. The primary PDF was read from the authors' university repository. Diamond strings/rings and Oum's decomposition are prior context. A 2-bisection is not a proper three-edge-coloring, so their theorem is not imported as a solver for this target.

[5] Peer reports: [BS11](https://github.com/j15marti/pnp/blob/79327bbb3710ce14ad90068e72c9ade2d4cb9a92/research/constructive-shared-hubs/solver/2026-11-24_1750_BS11.md), [BW12](https://github.com/j15marti/pnp/blob/97af44289e1993aa58dffdc2d5f38775f7989202/research/constructive-shared-hubs/wheels/2026-11-24_1810_BW12.md), [BD11](https://github.com/j15marti/pnp/blob/4831dc8f4fadcd4e50368a5d61d03f50a42c9d61/research/constructive-shared-hubs/multisign-dag/2026-11-24_1720_BD11.md), [M18](https://github.com/j15marti/pnp/blob/8013d12201a4ddd5513e8b2e2b177dfe00814b8c/research/hcl201/matching/2026-11-24_1810_M18.md), [DO12](https://github.com/j15marti/pnp/blob/97d28dc84ff933fe0e7aa77b3dee0600100b41ff/research/hcl208/obstruction/2026-11-24_1755_DO12.md), and [DP12](https://github.com/j15marti/pnp/blob/8a662e6774845e55568317b4f9aa6c94d3937041/research/hcl208/potential/2026-11-24_1745_DP12.md).

Fresh bounded literature and official-repository searches covered OpenAI, Anthropic, xAI, Google, Google Research and Google DeepMind. Repository ownership was checked with repository metadata. Relevant-looking results included graph/SAT/formalization code, but no universal repair theorem or external implementation was imported. Search terms, inspected repository revisions and failures are in the source ledger.

**Next precise dependency:** acquire a comparable exact reduction on a diamond-free cubic kernel that preserves simultaneous matching occupancy and all retained correlations. A useful positive result must give a discoverable structural certificate and a paid total-work bound, not obtain its exchange family from an already known three-edge-coloring. The present detector cannot supply that certificate for every kernel.
