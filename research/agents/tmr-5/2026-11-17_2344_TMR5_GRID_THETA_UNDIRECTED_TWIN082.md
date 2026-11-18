# TMR-5/082: Same-undirected-graph high-treewidth T5 YES/NO firewall

**2026-11-17 23:44 PST.** Owner TMR-5 / PNP Machine Bottleneck Redteam. PROVED/EXACT within an explicit graph family, independent finite checks COMPUTATIONAL, external review OPEN. P versus NP OPEN.

## New exact theorem

For every integers L>=2, h>=5, there are two connected source digraphs D+(L,h), D-(L,h) for the exact five-symbol tournament R(x,y) iff (y-x) mod5 in {1,3}, having identical **entire underlying undirected graphs** and identical directed (indegree,outdegree) **multisets**. Both source digraphs are DAGs, underlying-bipartite and triangle-free, have maximum total degree <=8 and treewidth >= L-1. Each has exactly

N = 7L^2 - 6L + 6h - 1 vertices;
M = 10L^2 - 10L + 8h arcs.

Exactly **eight** original arcs are reversed to move between D+ and D- (directed arc-set symmetric difference 16). Yet D+ is T5-colorable, D- is NOT. Every unsatisfiable subgraph of D- contains at least **2h original logical vertices**. Both the YES and NO instances, including every arbitrary vertex relabelling, admit a polynomial-time source-recognizing **decision** algorithm; no analogous counting result is claimed.

## Modules and construction

A 4-arc module u->a->b->v and u->v forces terminal difference v-u=+3 mod5, uniquely. Proof: a 3-step path has possible total increments {0,2,3,4}; intersect the direct beat arc's {1,3} to obtain only 3, attained only via (1,1,1). Reverse all four arcs to force v-u=+2 mod5 uniquely. Call these modules F and R. Each is a DAG with the identical undirected four-cycle.

Build an L by L undirected square grid, and replace each edge {u,v} (ordered u<v) with a private five-arc C5-to-T5 gadget u->a->b->c, u->c, c->v. This gadget uniquely enforces v-u in {1,4}, and is an underlying-bipartite DAG. The grid's chessboard assignment 0/1 thus lifts to a T5 witness. The grid survives as a minor and supplies treewidth >= L-1. Its expanded graph B has N_B = L^2 + 6L(L-1), M_B=10L(L-1), maximum degree <=8.

At a corner grid vertex s, attach two internally disjoint logical s-t paths of length h each; replace each logical path edge with its own four-arc two-private-vertex F/R module. This adds 6h-1 vertices, 8h arcs, and a single macrocycle of 2h modules, attached to B only at s.

D+ reverses module number 2 on BOTH paths, making both total increments 3h-1 mod5. D- reverses modules 2 and 4 on ONE path, leaving the other all forward, making terminal increments 3h-2 and 3h mod5. Hence every B homomorphism has one extension to D+, and no extension to D- exists. In fact #Hom(D+,T5)=#Hom(B,T5)>=10 whereas #Hom(D-,T5)=0.

Both graphs have two reversed modules; both paths start and end forward. Every 4-arc module's private vertices have (in,out)=(1,1). At intermediate logical vertices, FF and RR give (2,2), FR gives (4,0), RF gives (0,4). D+ has two FR and two RF transitions across both paths. D- has the same two FR and two RF transitions, with the R modules separated by F. The whole directed degree multisets therefore agree. Only two of the four-arc modules differ in orientation, accounting for exactly eight reversed arcs. Every base vertex and every underlying undirected edge remains unchanged.

No directed cycle is possible, since all four-cycle modules are DAGs, no branch provides a complete t-to-s directed path (its first and last modules point s-to-t), and the base DAG attaches only at s. Underlying bipartiteness follows by matching parity along the two equal-length logical paths and the four-cycle gadgets. At corner s, the grid gadget contributes outdegree four and the two first F modules contribute outdegree four, proving the global max total degree bound 8.

## Long minimal UNSAT support

Removing any of the 2h logical vertices breaks the one macrocycle of path modules into a forest of modules. Each full module is extendable for every fixed value at either endpoint, and so is any subgraph of that module. A forest of such modules can be colored from any root outward. The base grid expansion is independently T5-colorable for every root s label, by rotating the chessboard witness. Therefore **every subgraph omitting any one logical vertex is satisfiable**, even though D- itself is not. Every UNSAT subgraph must have >=2h vertices. No induced-minimality assertion about the entire NO graph is made.

## Charged source-aware solver

Enumerate polynomially many pairs (L,h) compatible with input size; construct D+ and D-; test directed graph isomorphism against each. All possible matching templates have max degree 8, so a deterministic **polynomial-time bounded-valence isomorphism algorithm** applies by Luks (1982), using constant-size port markers to encode directions/colors. Return the YES witness through the isomorphism or return NO on a negative match; otherwise use brute force on unmatched arbitrary inputs. This is a **total exact decision algorithm polynomial on the full isomorphism-closed pair family** and exponential elsewhere. It does not imply general T5-CSP is in P. Unlike simple indexed-grammar recognition, this handles arbitrary vertex relabeling at a proven polynomial charge.

## Independent executed falsifiers

Executed CPython standard-library file tmr5_082_grid_theta.py: checked the 25 ordered terminal pairs for both module orientations, 30 full mixed pairs with L in {2,3,4,5,6,7}, h in {5,6,7,9,11}, 56 random relabeling controls, graph identity, exact arc edits, complete degree profiles, DAG, bipartiteness, connectedness, bound 8, modular YES/NO, and a fully evaluated YES assignment on every directed source arc. **13,044 assertions; zero failures.** Additional independent NetworkX VF2 on (L,h)=(2,5),(3,5) confirmed positive-copy directed isomorphism and YES/NO nonisomorphism (finite empirical check, not the Luks proof).

Executed source SHA256 43c915cd24fad5dd71405af63acfa6c8f9d97c9640b7fd3bee5b1d7458ea1412. Raw JSON SHA256 ae98df092e47f69690d79a8245cb500ffe084d80a25ab15ed763c7443005b249. Full verifier, evidence JSON and 14KB detailed proof report are delivered in the run evidence archive. Full repository preflight, LaTeX build, native machine microsteps, Lean/nanoda and external referee check NOT performed.

## Ranked dependencies / safeguards

- NP-completeness of fixed T5 homomorphism: **KNOWN THEOREM** (Bang-Jensen-Hell-MacGillivray 1988; Hell-Nesetril 1990 C5 plus verified 5-arc module).
- TMR-1 5-arc C5-to-T5 gadget: **PROVED/EXACT restricted**, independently reproduced in this construction.
- Full underlying graph, treewidth, degrees, long UNSAT support or mixed YES/NO labels => compulsory instancewise computation: **FALSIFIED**.
- Static-rank/fixed-order OBDD/tensor hardness => all adaptive or source-aware machines: **OPEN/UNJUSTIFIED**, with valid modular reduction and unlabelled GI recognition controls.
- General representation-independent superpolynomial T5/SAT lower bound: **OPEN**. P versus NP **OPEN**.

DISJ sanity: PASS as falsification control. Relativization: no NP separation. Simultaneous DTISP: restricted matched upper bound only. Configuration counting: upper-bound safeguard only. Keep all original cost and source-availability controls and agent governance unchanged.

Primary references: Bang-Jensen, Hell, MacGillivray, SIAM J. Discrete Math. 1(3), 281-298 (1988), https://doi.org/10.1137/0401029; Hell, Nesetril, JCTB 48, 92-110 (1990), https://doi.org/10.1016/0095-8956(90)90132-J; Luks, JCSS 25, 42-65 (1982), https://doi.org/10.1016/0022-0000(82)90009-5.

## Addendum: a generic singleton-arc-consistency refutation (independent reproduction)

A separately implemented binary-CSP AC-3 solver exposes an even cheaper countercontrol: although unpinned ordinary arc consistency never removes a T5 label (each symbol has two in-neighbors and two out-neighbors), **pinning the single grid articulation vertex s to any label makes ordinary arc consistency refute EVERY negative D- instance without any search branching**. This refutation is independent of the grid parser, modulo-five reduction annotations and graph-isomorphism recognition.

**Exact local propagation proof.** On forward module u->a->b->v with u=0, the arcs u->a and u->v reduce both a and v to {1,3}. The constraints a->b,b->v then leave only b=2, hence a=1,v=3. Mod-five translations give the same forced singleton values from any fixed u. Reversing the four arcs forces v=u+2 and its two private values by the same AC argument. Therefore, a pinned s sends uniquely determined labels down both macrobranches; on D- the two forced terminal values at t differ by 2 mod 5, emptying t's domain. On D+ a genuine global witness protects all domains.

**Sound arbitrary-input stopping rule.** On any unpinned T5 input, rotations x->x+c are template automorphisms. If a global solution exists, every vertex can take any prescribed label by rotating that solution. Therefore a failure of AC after pinning any vertex to 0 is a sound global NO certificate. A polynomial-time singleton-AC pass over all vertices detects the whole arbitrarily relabelled negative family without any graph-isomorphism check. This remains only a sufficient unsatisfiability test: it does not decide arbitrary YES cases or P versus NP.

**Independent executed verification.** A generic standard-library AC-3 / MRV implementation, without gadget- or grid-specific logic inside propagation, ran 300 root-colored AC tests across 30 full pairs and all five labels, verifying exactly the expected YES/NO result with zero failures. A second generic full CSP backtracker (AC + MRV) solved ten authentic full T5 graphs, including five NO graphs with up to 129 vertices, each negative case in **one search node** after pinning s. Full local source and JSON accompany the downloadable run evidence. The standalone singleton-AC harness SHA256 is 614424523bc12e145af5f0906bbae13d236dc0ea1ffd97f41fbc446641ea9231, generic CSP solver SHA256 2e95bda4ebb3bf20d24e9f62c6ca28ea70573b2b45ed497d7cd4b456148cf694, additional raw JSON SHA256 55861c18c8975be7468a82cfed6794ad9c24fb898d07d5c76c134be070733d9a. These are actual executed checks, not claimed independent formal-kernel executions.

**Stronger falsification:** An unsatisfiable instance may require an arbitrarily large subgraph to witness contradiction and still admit a polynomial-time, very simple *local-consistency-propagation* refutation. Minimal obstruction cardinality is not a machine-runtime lower bound; repeated constant-locality inference can traverse an arbitrarily long graph at polynomial charge.
