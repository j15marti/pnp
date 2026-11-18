# TMR-4/091: Source-only chain-graph exact compilation

2026-11-18, America/Los_Angeles. TMR-4 identity, title, enabled hourly schedule, ownership and additive manuscript history unchanged. Status: restricted theorem plus finite COMPUTATIONAL verification; P versus NP OPEN.

## Candidate and proof
Let \(T_5\) have \(R(a,b)\iff b-a\in\{1,3\}\pmod5\). A forward-oriented chain graph has bipartition \(U,W\), all arcs from \(U\) to \(W\), and nested source neighborhoods \(N^+(u_1)\supseteq\cdots\supseteq N^+(u_p)\). Discover U/W from incidence direction, sort U by decreasing outdegree and verify each target w has exactly a prefix \(\{u_1,\ldots,u_{t_w}\}\) of in-neighbors. This is verified **from the source** in polynomial time, not supplied as advice.

**Theorem A:** The source admits a complete original-variable 5-way OBDD of width at most 11 and at most 11n internal nodes, preserving both exact terminal decisions and all accepting/rejecting multiplicities. Query each \(u_i\) and then every target whose prefix ends at i. Carry the exact intersection \(S_i=\bigcap_{h\le i}N^+_{T_5}(x_{u_h})\), and check the next target color lies in \(S_i\). Only five 2-color out-neighborhoods, five singleton masks and the empty mask can occur; initial full mask occurs before rejection is possible. Rejected paths continue through a layer-specific complete-query dead state. The count uses <=55n five-way transitions and O(n)-bit integer additions, in addition to charged source discovery and output.

**Theorem B:** The directed halfgraph \(H_k\), arcs \(u_i\to v_j\iff i\le j\), has \(n=2k\), \(m=k(k+1)/2\), cycle rank \(q=(k-1)(k-2)/2\), all k row profiles distinct, full adjacency rank k over every field, and minimum frontier at least \(\lfloor k/2\rfloor\) for every ordering. The last follows from the induced \(K_{r,r}\) on the first r sources and last r targets. Still,
\[
Z_{T_5}(H_k)=5k2^k,\quad
\text{width}=11,\quad
\text{nodes}=22k-21\quad(k\ge2)
\]
for the source-discovered interleaved order. Proof of count: fixing first U color gives 5 choices; the all-equal U case contributes \(5\,2^k\). For each first differing source index \(r=2,\ldots,k\), exactly two alternative colors leave one common beaten color, later U colors have two choices each and later targets are forced. Each r contributes \(5\,2^{r-1}\cdot2\cdot2^{k-r}=5\,2^k\). The ten live masks and rejecting mask are all reachable after U_2, making width 11 exact **for that order**.

## Four falsifiers
F1. High frontier/cycle rank/full adjacency rank cannot alone imply high semantic OBDD width.
F2. All k distinct source row profiles do not prevent a constant-state *nested* quotient; /090's \(10^t\) bound is not a lower bound.
F3. Reversed/missing source arcs and non-chain directionality make specialized recognition decline; no assumed graph promise or free variable order.
F4. Eleven reachable suffix masks are not an all-graph reduction of the 32 unary masks; rejected assignments must remain counted; block-respecting 3-bit FBDD decoding costs <=6 nodes per native node and arbitrary interleaved reverse implication remains OPEN.

## SAME_REALIZATION and four gates
Charge encoded source reading/canonical SHA, incidence scans, profile order reconstruction, sorting, verification, each original 5-way branch, fanout/sharing, cache, complete rejecting sink chain, exact integer arithmetic and output. No free Z5/Fourier transform, switch or Boolean conversion. Direct 3-bit literal CNF has 3n+15m clauses (9n+90m literals). Nonmembers require a separately costed general exponential fallback.

G1: 11 halfgraph sizes, 12 independently relabeled cases, 55 random forward chain graphs, six negative controls, three large-source SHA cross-language checks.
G2: 1,287,575 pointwise original-source Python assignments and 594,400 independent JavaScript assignments; all accepted/rejected counts conserved.
G3: 370,597 executed Python signed-literal CNF evaluations, 19,785 independent JS CNF evaluations, all 2,048 orientation and pair-of-32-domain masks.
G4: two byte-identical Python and JS reruns, zero unexpected assertions; no full LaTeX build, referee review or physical TM microstep audit.

At k=400, n=800, m=80,200, q=79,401, minimum frontier >=200 and adjacency rank 400, yet exact complete OBDD width 11, 8,779 nodes and Z=2000*2^400. This entire forward chain family is SAT (all U color A, W color B), so it is a cheap-source counterexample, NOT a mixed SAT/UNSAT hard family.

Next dependency D4-T5-HIGH-FRONTIER-HIGH-ROWDIVERSITY-CHAIN-IRREDUCIBLE-092: mixed SAT/UNSAT families resisting nested-profile, affine, palette, row-type, separator, support-mask and low-cost local-obstruction reductions. Arbitrary native/bit-interleaved FBDD transfer remains open. P versus NP OPEN.

Context: Barto, Kozik, Niven, SIAM J Comput (2009), https://doi.org/10.1137/070708093. Halfgraph terminology: https://en.wikipedia.org/wiki/Half_graph. Mathematical arguments above are this run's restricted derivations.