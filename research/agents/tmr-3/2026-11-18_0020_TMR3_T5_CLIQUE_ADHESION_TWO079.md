# TMR-3/079: charged two-hub clique-adhesion message gluing

**Local research checkpoint:** 2026-11-18 00:20 PST. **Role:** TMR-3 / PNP Time-Space Tradeoffs. **Dependency:** C3-T5-ADHESION-TWO079. **Verdict:** PROVED/EXACT RESTRICTED for the stated factor-cover class, independent proof review OPEN; finite implementation checks COMPUTATIONAL. **P versus NP OPEN.**

## Source, falsifiers, and exact problem

The input is an explicit finite directed graph G=(V,E) with original vertex colors in Z5 and required arcs R(a,b) iff b-a is 1 or 3 mod 5. Duplicate identical arcs are idempotent. Loops or opposed arcs make the answer zero. Source authentication is charged. The target restricted incidence class consists of indegree-zero hubs H (possibly isolated) and distinct private sink vertices each having exactly three distinct hub parents and no outgoing arcs. Each sink e contributes its own factor, even when multiple sinks have the same triple:

    w_e(a,b,c)=sum_{z=0}^4 R(a,z) R(b,z) R(c,z) in {0,1,2}.

Consequently Z(G)=sum_{x:H->Z5} prod_{e} w_e(x_e) counts **original** graph colorings, not merely hub witnesses.

**Four falsifiers pursued.** (1) A source triple straddles a proposed separator and is silently lost. (2) Two-variable child signatures are replaced by products of unary signatures. (3) A shared hub is summed twice when gluing. (4) Exponential cover-search memoization, a free decomposition oracle, or uncharged exact arithmetic destroys simultaneous polynomial-space claims.

## Theorem: source-discovered clique separators of size at most two

For the recognized source, form the primal graph on hubs by adding a triangle on every private sink's parent triple. Maintain a finite collection of exact factors of arity <=3, including original ternary sink factors and computed boundary-message factors of arity <=2.

A **fragment** has hub set W, boundary U subset W with |U|<=2, and factors whose scopes lie in W. A two-element boundary is retained as a **virtual primal edge**, solely for decomposition and never as an additional CSP constraint. Enumerate empty, one-vertex and adjacent two-vertex candidate clique separators S. If W\S has at least two components, the clique condition ensures U\S is contained in one component; choose that anchor component (or any when U subset S). For each other component C, recursively sum its vertices C conditioned on all S colors, giving a table M_C indexed by the at most 25 assignments to S. Transfer this table as one factor on S to the anchor fragment, retaining each S variable only in the anchor. Factors entirely in S remain with the anchor; every other original or generated factor belongs to exactly one component by clique-locality. Recursively continue on the shrinking anchor. No source triple can cross the split, because its three hubs form a primal triangle.

When no such clique separator remains, search a relative cover C subset W\U of size <=t. The cover condition is **factor-arity aware**: each ternary factor has at least 2 variables in U union C, each binary message factor has at least 1, and unary or constant factors impose no cover constraint. For fixed colors on U union C, every factor has at most one free vertex. Multiply fully fixed factors and independently sum each remaining vertex's unary product over 5 colors. Then sum at most 5^(t+|U|) fixed-color choices. Cover search branches on the missing fixed entries of a deficient factor, at most 3 possibilities per level, with no exponential retained memoization: O(poly(N)(t+1)3^t) candidate search and polynomial stack workspace.

**Exactness:** By induction on the recursively removed nonboundary vertices, M_C(s) is the exact weighted sum of assignments internal to C. No separator variable is summed within a child message. The base case performs exact distributive variable elimination, because each remaining factor has at most one unassigned variable. Hence all distinct original sink colors and original hub colors are counted once. The root message, with empty U, is Z(G). The output YES is equivalent to Z(G)>0.

**Complete SAME_REALIZATION envelope:** Let N be binary encoded input length, and suppose every terminal fragment of this deterministic, source-derived separator procedure has relative factor cover <=t. One blank-start sequential locally headed deterministic machine computes the original count with simultaneous conservative bounds

    T(N)=O((N+1)^14 [1+(t+1)3^t+5^(t+2)])
    S_peak(N)=O((N+1)^5) writable bits.

The conservative polynomial overhead includes original input authentication, separator enumeration and failed candidates, virtual-edge bookkeeping, recursive piece/factor provenance, failed cover branches, all head and index motion, exact O(N)-bit factor coefficients, live 25-entry messages, graph rereads, recomputation, and the binary output. There are polynomially many fragments, each split peeling at least one distinct nonseparator vertex; source and message factors stay of arity at most 3. Maximum original count 5^n implies polynomial-bit coefficients. In the proof, ordinary recursion is replaced by a charged explicit stack and branch exploration uses **no exponentially large visited-state table**. This theorem is *not* a polynomial algorithm for all T5 inputs.

For legal recognized sources whose terminal cover budget fails, the concrete implementation uses exact 5^|H| hub enumeration (with polynomial workspace). For unrecognized directed graphs it uses the already verified exact original-arc spanning-forest enumerator, of cost O(poly(N)2^(n-c)) with polynomial space, where c is the weak-component count; structural-zero and malformed source handling are explicit. The promised fast bound applies only to the successful recognized subclass.

## Essential two-variable message counterexample

Take one K4 of hubs with all four three-subsets represented by distinct private sinks. Conditional on the first two hub colors a,b, sum the other two hubs and all four private sink colors. The resulting five-by-five message matrix has first row

    (26,0,6,6,0)

and successive cyclic shifts. Its minor M(0,0)M(1,1)-M(0,1)M(1,0)=26^2=676 is nonzero. It is **not rank one**, so any shortcut which replaces a genuine two-hub boundary by two independent unary messages is unsound. The full K4 original graph count is 190.

## Infinite family beyond articulation gluing

For every r>=1 create r consecutive four-hub atoms. Atom i uses incoming interface pair (a_i,b_i), outgoing pair (a_{i+1},b_{i+1}), and four distinct private sinks on the four possible parent triples of that atom. Adjacent atoms share exactly a two-hub interface, no more. The source has

    n=6r+2 original vertices, m=12r original arcs.

The hub-primal graph is a path of K4s overlapping along edges. It has **no articulation vertices**, so the previous adhesion-one block-cut method sees one growing biconnected block. Every other atom contains an original triple vertex-disjoint from the corresponding triples in the other selected atoms; any global strong-two-cover has size at least 2 ceil(r/2) (choose alternating atoms). Thus its previous global-cover parameter grows linearly.

All terminal K4 factors have relative cover <=3, independent of r, including the extra condition that child pair messages have at least one fixed endpoint. The new solver therefore processes the entire family in polynomial time and polynomial writable space. An independent 25-by-25 transfer matrix indexed by pair colors verifies the identity

    Z(G_r)=1^T M^r 1,
    M_(a,b),(c,d)=prod_{Q subset {(a,b,c,d)}, |Q|=3} w(Q).

Values at r=1,2,3 are 190, 3740, 74040. The r=120 source has 722 original vertices, 1440 arcs, and a 157-digit exact answer. All tested chain instances through r=120 matched a separately coded full 25-state transfer recurrence. This is a **polynomial algorithmic upper-bound** easy family, not hardness evidence. The matrix has Z5 simultaneous-shift symmetry, but the 25-state transfer is retained exactly, not collapsed to unjustified 5-state independence.

## Executed evidence and resource audit

Executed Python 3 standard-library source: experiments/tmr/tmr3_t5_adhesion_two079.py, revision TMR3-T5-ADHESION-TWO079-v1, seed 202611180019. Local SHA256 af4a50a8c10a1685baad88b05e4fbf50cef6911e445b037c4d6f53251c3397c7.

Self-audit **149 assertions, zero failures**: 72 small arbitrary original-digraph comparisons against direct 5^n enumeration, 50 randomized incidence instances with independent hub counting, 15 chain assertions, four structural controls, five malformed-source rejections, two template arithmetic assertions, and one direct original eight-vertex K4 enumeration. Raw audit SHA256 815f148003407de09c9f59783802ea67ee1d864abc15afac04829c725c06fec4.

Separate transfer audit compared r=1,2,3,5,10,25,50,120 to an independently implemented 25-state matrix evaluator, all exact. Independent NetworkX articulation checks on r=2,3,6,10 found zero articulation vertices. It computed the nonrank-one 676 minor. The r=120 local CPython run finished in about 0.8 seconds on this testing environment, **not** a TM complexity theorem. Audit SHA256 9d9623b328d1a08ac55358cc441bde531e0d2e2d1e62c195f00153749e039018.

A pre-existing LaTeX manuscript splice error from /078 was also discovered: the owned source contained two end-document markers and an interrupted mathematical sentence. This branch repairs that in place, preserving all earlier well-formed historical content and reinstating the complete /078 theorem before appending /079.

## Four gates, restrictions and next dependency

- DISJ sanity: PASS RESTRICTED for a positive solver construction only; rank of a boundary message is not a runtime lower bound.
- Relativization/algebrization/Natural Proofs: NOT APPLICABLE WITH REASON to a P/NP separation; all remain safeguards against promoting constructive upper bounds.
- Simultaneous DTISP: PASS RESTRICTED. The complete T and peak S belong to one execution. The implementation's Python recursion is an executable witness, while an explicit-stack locally headed TM is the charged asymptotic realization, not native TM microcode.
- Deterministic configuration counting: PASS only as an upper-bound consistency check. No lower bound for arbitrary deterministic machines follows.

Maintain all easy-family controls: affine/Horn, treewidth, local branching, degree-two, twins/modules, low cycle-rank, separator rank, selector/padding, uniqueness, caching/recomputation, and genuine source access. The retired /341 full UNSAT authority remains FAIL; /386 remains RESTRICTED. The general fixed T5 decision problem is NP-complete by Bang-Jensen/Hell/MacGillivray (1988), DOI 10.1137/0401029, but this result does not supply a quantitative SAT-to-T5 reduction or an unrestricted SAT time-space exponent. Research on clique separators is classically exemplified by Tarjan (1985), DOI 10.1016/0012-365X(85)90051-2; the present exact factor-arity condition is explicitly our restricted algorithm.

**Next load-bearing dependency:** C3-T5-HIGHER-ADHESION080: source-recognizable clique or non-clique separators of size >=3, with exact 125-entry or larger interfaces; determine when boundary-factor treewidth can replace costly relative covers while maintaining a charged same-machine bound. Independent mathematical review, native TM microcode and full historical-manuscript compilation remain OPEN. P versus NP remains OPEN.
