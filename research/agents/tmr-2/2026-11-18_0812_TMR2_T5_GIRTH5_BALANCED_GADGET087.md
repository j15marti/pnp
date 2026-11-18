# TMR-2/087: sharp girth-five, exact-count-preserving T5 edge gadget

Date 2026-11-18 08:12 PST. Owned manuscript: `main2_PNP_INFORMATION_NECESSITY.tex`. Role TMR-2 / PNP Information Necessity. Relation exactly `R(a,b)=[(b-a) mod 5 in {1,3}]` on the five original labels. **PROVED/EXACT restricted algebra**, **COMPUTATIONAL finite verification**, independent mathematical review OPEN, P versus NP OPEN.

## Mechanisms proposed and tested

(i) Try a pair of short disjoint paths to recover the original directed arc's *existential* binary cofactor after the four-step saturation failure /086. (ii) Add a longer saturated path to balance *integer witness multiplicities*, since existential support alone is inadequate for exact counts. (iii) Prove the tradeoff between local girth, smallest gadget size, and source-recognizable contraction. (iv) Test a one-arc-flip same-skeleton mixed YES/NO pair, preserving all original-label weights. Mechanisms (i)-(iii) yield the exact restricted theorem below, but do not establish costly computation.

## Mathematical theorem: 9-edge binary gadget with exactly 12 extensions per legal pair

Let `A=S+S^3` be the T5 adjacency matrix. A path of `k` edges, `q` of them backward relative to its traversal, has integer terminal-cofactor matrix `K(k,q)=A^k S^q`; all internal original T5 labels are summed. For each length, the first row gives the five terminal differences `d=y-x mod 5`:

```
(k,q)   d=0  1  2  3  4
(2,2)     0  2  0  1  1     word --
(3,3)     3  1  1  3  0     word ---
(4,3)     1  6  1  4  4     word ---+
pointwise product:
           0 12  0 12  0  = 12 R
```

Use THREE internally vertex-disjoint oriented paths between terminals x,y, of lengths 2,3,4 with the displayed orientation words. Their respective internal vertices are distinct. The union has 8 vertices, 9 arcs and underlying undirected girth **5**. Every legal assignment `R(x,y)=1` has **exactly 12** internal-label extensions; every illegal endpoint pair has none. This is pointwise exact and is independent of any solver.

The first two paths alone have cofactor row `(0,2,0,3,0)`. Their existential support is the original directed relation R, but their multiplicities differ (2 versus 3). Adding a length-four path, although itself existentially saturated by /086, balances those weights: `2*1*6=1*3*4=12`. Consequently the four-step path saturation result does not prohibit support-preserving *bundles*. This also confirms that weighted and existential invariants should be tracked separately.

## Sharpness within the explicit gadget class

Restrict the gadget class to two or more simple internally vertex-disjoint terminal-to-terminal paths of lengths at least two, with no direct terminal edge; orient individual path arcs arbitrarily and conjunction-combine their constraints. This restriction is essential.

* Every length-two path with traversal-backwards count `q=0,1,2` permits respectively `{1,2,4}`, `{0,2,3}`, `{1,3,4}`. To include both allowed R differences `{1,3}` and exclude `0`, at least one `q=2` length-two path is necessary; every length-three or longer path permits equality.
* Every length-three path forbids exactly the offset `1+q mod5`; lengths four and above forbid none. Among allowed paths, excluding the extra difference 4 requires one length-three `q=3` path. Therefore a 2+3 path bundle (a five-cycle) is necessary for R support. **Girth at most five is unavoidable** within this class.
* With only lengths two and three, all admissible length-two paths have `q=2` and contribute a ratio `K(1)/K(3)=2`. Admissible length-three paths have `q=1` (ratio 1) or `q=3` (ratio 1/3). Writing `a>=1` for the former mandatory length-two copies and `b>=1` for mandatory `q=3` length-three copies, the total ratio is `2^a/3^b != 1`. Hence no constant-integer-multiple-of-R gadget can use only path lengths two and three. At least one length-four-or-longer path is needed. The exhibited 2+3+4 construction has exactly **nine** arcs and is smallest by total arc count within this specified class. A finite 4-to-9-edge multiset enumeration independently found exactly this one 9-edge multiset.

The girth ceiling and minimality do NOT extend to arbitrary branching/two-terminal gadgets and do NOT prove an asymptotic computation lower bound.

## Linear-size source compiler and count identity

Given any loopless oriented simple input `D=(V,E)`, replace each original arc with a fresh copy of the 9-arc gadget, identifying only its two terminals with the corresponding original endpoints. Source compilation uses canonical `min(u,v),max(u,v)` terminal order and flips all gadget arc directions when the base arc direction is reversed. Thus an edge reversal leaves the exact *labeled undirected* output skeleton unchanged.

The transformed original source `F(D)` has `n'=n+6m` vertices and `m'=9m` arcs. Summing the six fresh internal T5 labels for every original edge independently proves

`Z(F(D)) = 12^m Z(D)`, and `F(D)->T5 iff D->T5`.

For every nonempty simple oriented source, the result has girth exactly five: each gadget contains a 5-cycle, and any cycle traversing distinct gadgets corresponds to a base cycle with at least three edges, whose replacement path length is at least 2 per edge, giving cycle length at least six. Sources containing loops or antiparallel pairs already have zero solutions; a reduction from all directed sources to the girth-at-least-five promise replaces those trivial NO sources with the fixed expanded UNSAT motif below. Duplicate directed arcs may be deduplicated. Hence the original Bang-Jensen--Hell--MacGillivray 1988 NP-completeness result implies **T5-homomorphism remains NP-complete on oriented input graphs of undirected girth at least five**. This is a restricted decision complexity classification, not P != NP.

The full source is structurally reversible if produced in the canonical gadget grammar. Recovering each base edge, checking the three oriented paths, and charging source parsing, graph construction, verification and factor multiplicities is polynomial time. A solver may simply contract this gadget and return to the base source. No hardness amplification or necessary-work statement follows.

## Same-labeled-skeleton finite YES/NO controls

Base four-variable obstruction (source /075): `0->1, 1->2, 0->3, 1->3, 2->3`; exact Z=0. Reversing ONLY `0->1` to `1->0` yields Z=5 by independent exhaustive `5^4` enumeration. Both have the same unordered five-edge skeleton. The canonical compiler creates a pair of 34-variable, 45-arc, girth-five sources with exactly the same labeled undirected edges but different directions:

`Z(NO)=12^5*0=0`, `Z(YES)=12^5*5=1,244,160`.

The executed full standard-library Python audit enumerated all path endpoint/interior labels for every `k=2,3,4`, all 25 terminal pairs of the eight-variable gadget by direct 5^6 internal enumeration, all path bundles with at most nine total arcs, and the four-original-variable pair. It checked girth via BFS, matched the undirected output skeleton, and constructed an independently checked full original-label YES witness for all 45 arcs. **360 assertions, zero failures.** Full script SHA256 `4930791e5eb9c08b59ab96bea3e40ae099ba0ca0f948df0dde60a7f459bf86df`; full raw output SHA256 `a8cb9c78af7007748a9349fc50424e04004c23f025f50335e2b454b59315d75c`. Complete executed script and raw results are conversation artifacts; repository contains a separate compact independent standalone verifier. The expanded NO count is certified algebraically using the exact factor identity and base four-variable exhaustive check, not by an infeasible 5^34 enumeration.

## Named paid dynamic invariant and four scientific gates

**D2-T5-GIRTH5-EXACT-EDGE-TRANSFER-LIFT** carries per genuine source edge `(u,v)`, the orientation, three full original-label path cofactors, their pointwise tensor product `12R`, internal count multiplicities, the source grammar, reconstructed base instance, and the charged compiler/recognizer/witness trace. READ/PARSE/GUARD, EDGE-DISCOVER, PATH-BUILD, ORIGINAL-LABEL BRANCH, INTERNAL-SUM, FACTOR-MULTIPLY, GAUGE, VERIFY, CACHE/RECOMPUTE, OUTPUT (including big integers), and all failed recognition branches are paid. This is a fast *compilation/verification* routine, not a polynomial-time general T5 decider; counting the recovered base source may still require exponential work.

DISJ restricted algebra PASS, all-model necessary-work inference FAIL. Relativization/algebrization/Natural Proofs unrestricted OPEN. Simultaneous time-space only an upper compiler, unrestricted lower OPEN. Deterministic configuration counting no lower transfer. Preserve legitimate cheap alternate algorithms, recognition, degree-two suppression, weighted elimination, separators, Fourier/cycle space, adaptive branching, OBDD/FBDD, certificate tests, caches and shared representations. /341 unrestricted UNSAT authority FAIL, /386 RESTRICTED. No new asymptotic lower bound, P versus NP OPEN.

**Next dependency:** D2-T5-HIGH-GIRTH-SOURCE-AWARE-NONLOCAL-GADGET: to reach girth >=6 while preserving R, leave this entire direct-arc-free parallel-path-bundle class; independently test richer branching gadgets and all source-recognizable contractions. Independently review the sharpness proof and seek actual growing mixed YES/NO families resistant to short certificates. External mathematical review, full manuscript LaTeX compilation, native repo preflight and physical TM replay remain OPEN.

Reference [1]: Bang-Jensen, J., Hell, P., MacGillivray, G., "The Complexity of Colouring by Semicomplete Digraphs", *SIAM J. Discrete Math.* 1(3):281-298 (1988), DOI 10.1137/0401029, https://doi.org/10.1137/0401029.
