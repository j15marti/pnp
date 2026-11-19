# Strict C K4-forced equality closure and grid-minor cover firewall
2026-11-19 | Obstruction-cover independent run 2 | P versus NP OPEN.

**PROVED (restricted):** Deterministic source-uniform UNSAT-or-UNKNOWN specialist with an actual source-indexed, universally quantified obstruction-cover proof. **FALSIFIED:** unbounded incidence treewidth alone requires difficult symbolic-cover discovery. **OPEN:** growing-incidence-girth, intrinsically clause-critical, low-row promise, square-root-space target, and unrestricted SAT.

## Definitions and theorem
Use strict C(x,y,z): each argument lies in Z5; R(a,b) iff (b-a) mod 5 is 1 or 3; C means a directed triangle in either orientation. Exactly 30 of 125 tuples satisfy C. A physical clause has three different variable names, though values may repeat across clauses. For every distinct a,b there exists h such that C(h,a,b), and for a=b no h exists.

A source is **private-head projectable** when every C clause contains a variable that occurs in no other clause. Choose one such variable deterministically per clause. Existentially projecting its isolated head turns that clause into the graph edge constraint u != v, and existential projections commute across clauses. The solver returns UNKNOWN for nonprojectable inputs.

**K4-forced-equality rule.** Let four vertices Q form a clique, and let distinct vertices u,v be adjacent to all four vertices of Q. In every proper 5-coloring, u=v: Q consumes four colors, and u and v must use the unique remaining fifth. A source-indexed proof step cites exactly 14 original C clauses: six edges inside Q and eight from u,v to Q. It does not require u and v to be nonadjacent.

Build union-find equality components from every discovered rule. If an original projected edge has both endpoints in one component, recover a proof path through the equality-rule forest, ending in that original edge. Independently verify all original clauses and all 14 edge premises per equality step. This yields a sound UNSAT refutation.

**All-z dynamic selector.** Given an arbitrary shared graph coloring z, traverse the certified equality chain. If the endpoints of any step have different colors, at least one of that step's 14 premise edges has equal-color endpoints. Select its physical C clause. Otherwise the concluding source edge has equal endpoints. For the selected clause, all five head assignments fail the ORIGINAL strict C predicate. Therefore the selector certifies EVERY z and identifies a refutable original private-head block, without enumerating the exponentially many z or assuming a correct path. A mere list of blocker indices or a symbolic disjunction without verified global validity would be insufficient.

## An infinite unbounded-width easy-cover family
Let H be the k-by-k rectangular grid, v=k^2 and e=2k(k-1). Replace every H edge uv with a fresh K6-minus-uv equality gadget, four private K4-core vertices plus 14 graph edges, and add a closing edge between opposite grid corners. Encode each graph edge by one C clause with a fresh private head.

Exact physical counts:
- M = 14e+1 = 28k(k-1)+1 original C clauses.
- N = v+18e+1 = k^2+36k(k-1)+1 strict-C variables.

All equality gadgets force grid terminals to share one color, contradicting the closing edge. Contracting each gadget core into one terminal recovers H as a graph minor of the projected graph G. The strict-C incidence graph includes a subdivision of G as a minor. Hence its treewidth is at least tw(H)=k, diverging as k grows, yet a source-uniform algorithm discovers and verifies a symbolic obstruction cover with O(k^2) or fewer premises. This control **falsifies the inference from unbounded incidence treewidth to hard obstruction-cover acquisition**.

Critical limitations: incidence girth is exactly 6, owing to source triangles; the grid family is not physical-clause-minimal UNSAT, since an alternative grid path makes each nonclosing module redundant. There are Θ(N) shared variables, so the explicit <=N^0.195 shared-row condition fails. The generic algorithm uses O(n+m) writable words, not N^0.5 space. No transfer to arbitrary SAT follows.

## Computation and independent checks
Seed 2026111909; deterministic source generation with shuffled variable names, shuffled clause order and argument order. In-memory K4-neighborhood closure accepted path gadgets k=1,2,4,8,16 and grid gadgets k=2,3,4,6. Counts on grid k=6: 1,117 C variables, 841 original C clauses, 10 proof steps. Across all tests: 19,625 shared assignments, 98,125 independently checked all-head exclusions. Path k=1 checked all 5^6=15,625 assignments. A second independent implementation replayed the archived original sources and certificates, exhaustively checked each cited six-variable K6-e equality implication, validated 15,775 shared assignments and 78,875 five-head rejections, and verified complete SAT witnesses after deleting the closing original C clause for grids k=2 and k=6 (56 and 840 retained clauses). Primary also tested grids k=3,4 deletion SAT witnesses. K5 SAT, a grid with closing edge removed, and a nonprojectable intrinsic three-C UNSAT source all returned UNKNOWN. A hostile altered closing-source citation was rejected. All results are finite controls, not lower bounds.

**Resources:** a conservative generic worst-case bound O(n^6) word operations and O(n+m) writable words for n projected variables and m physical clauses, plus storage for variable names and input encoding; input indexing, unsuccessful candidates, path acquisition, source replay and full output are counted. Experimental in-memory timings exclude file/JSON serialization and cannot substitute for whole-machine asymptotics.

## Next falsifiable obligation
Find a source-uniform, bounded-boundary inference language that remains useful when the incidence girth grows, independently verifies a global all-z proof, and charges acquisition/replay on both SAT and UNSAT paths. Direct K4 rules cannot produce growing incidence girth.

Evidence: companion conversation ZIP T5C_K4_Cover_GridMinor_Firewall_20261119.zip includes full Python 3 scripts (source-uniform solver and independent verifier), original C sources, complete proof chains, complete closing-deletion witnesses, raw JSON, logs and SHA-256 manifest. ZIP SHA256 588d4e5b18269975ebfda9427c31d38682c3ba9c2316fd618b83a0309a42a8d6.

Prior work read back: research/agents/strict-c-cover/2026-11-19_EQUALITY_WIRE_GLOBAL_OBSTRUCTION_COVER.md. User t5_strict_research.pdf in Library was read, the named strict ZIP was not found in Library search. The historical H9/H33 sources encode the directed binary arc R and were not passed off as strict-C clauses. Background: Kolman and Koutecky, Extended Formulation for CSP that is Compact for Instances of Bounded Treewidth (2015), https://arxiv.org/abs/1502.05361; Demaine and Hajiaghayi, Linearity of grid minors in treewidth (Combinatorica 2008), https://doi.org/10.1007/s00493-008-2140-4.

P versus NP remains OPEN.