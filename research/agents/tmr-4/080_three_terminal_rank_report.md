# TMR-4/080: maximal three-terminal connection rank and a cheap-source counterexample

**Scope and status (2026-11-17 Pacific).** Owner: TMR-4 / PNP Cost-Sound Abstraction. The object is the fixed five-symbol CSP with alphabet Z5 and directed constraint R(x,y) iff (y-x) mod 5 belongs to {1,3}. This is a restricted exact theorem with a finite integer certificate and computational audit, not an unrestricted machine lower bound. P versus NP remains OPEN. TMR-4/079 and all prior manuscript work are preserved.

## Candidate D4-T5-THREE-TERMINAL-FULL-CONNECTION-RANK

For any T5 source H with three named terminals u,v,w, let F_H(a,b,c) count internal assignments satisfying the original arcs given the three terminal colors. Diagonal translation invariance gives F_H(a+t,b+t,c+t)=F_H(a,b,c), so 25 values f_H(p,q)=F_H(0,p,q) suffice instead of 125 absolute values. The phase quotient is valid for **summed counting messages**, not automatically for pointwise original-label FBDDs.

I constructed 25 unweighted literal T5 source gadgets with at most two private vertices and at most four arcs, no boundary arcs or pinning. Each private vertex has a pattern in {-,>,<}^3, with > meaning hub-to-private and < meaning private-to-hub. Their exact 25x25 count-signature matrix M has **det(M)=-8064**, verified by independent BigInt and Python Bareiss determinant implementations.

The complete source witness list, in determinant row order, is:

```text
 1 >>>             2 >><             3 ><>             4 ><<
 5 <>>             6 <><             7 <<>
 8 ->> >->         9 ->> >-<        10 ->> >>-        11 ->> ><-
12 ->> <->        13 ->> <>-        14 ->< >->        15 ->< >-<
16 ->< >>-        17 ->< ><-        18 ->< <->        19 ->< <>-
20 -<> >->        21 -<> >-<        22 >-> >>-        23 >-> ><-
24 >-> <>-        25 >-< >>-
```

Glue two such source gadgets along only their three named terminals, with distinct private vertices. The full unweighted T5 count is Z(H_i⊕H_j)=5 sum_{p,q} f_i(p,q)f_j(p,q). Consequently, the authentic 25x25 connection matrix C=5MMᵀ has det(C)=5^25 (8064)^2 != 0 and rank 25 over Q. **A linear, exact boundary message paired bilinearly to recover all these source-gluing counts must have dimension at least 25**, and the 25 relative entries attain it. This is not a general lower bound on integer bit-length, nonlinear messages, counting algorithms, FBDDs or deterministic machines. It is an explicit small T5 witness of the classical connection-matrix framework [1,2].

## Full source-to-model counterexample

A source-only recognizer enumerates triples of mutually nonadjacent hubs. It confirms all other vertices have two or three arcs, each to a distinct hub, and that there are no private-private arcs or contradictory orientations. No hubs, witness patterns, coloring, separator, or variable order are supplied as extra input data. The preflight n <= floor(m/2)+3 prevents huge declared-n headers from forcing an uncharged n-sized allocation.

For source-recognized members, if s_z(p,q) is the number of valid colors for private vertex z at terminal colors (0,p,q), the exact count is

```text
Z(G) = 5 * sum_{p,q in Z5} product_{private z} s_z(p,q).
```

Reading all three hubs first and then each private vertex gives a **complete five-way OBDD of width <=126, internal nodes <=126n**, preserving decisions for every source assignment and both terminal multiplicities, with N_accept+N_reject=5^n. Rejected branches continue to read all remaining original variables. The code constructs the OBDD and checks its counts.

The direct parsimonious Boolean encoding needs exactly 3n variables and 3n+15m clauses, with three invalid-code clauses per original symbol and 15 forbidden-pair clauses per arc. Actual CNF clauses are generated and tested. Each five-way node has a seven-internal-node three-bit binary decision-tree replacement, with at most another 3n nodes if full invalid-code rejecting continuation is demanded. Thus the five-valued representation offers no asymptotic advantage on the recognized family.

**SAME_REALIZATION ledger:** canonical source parsing and byte-authentication; declared vertex preflight; failed hub-triple candidates; adjacency recovery and edge orientation; deterministic source-only order; precise 25-relative counting factors with O(n)-bit integers; explicit OBDD reachable states, five-way fan-out and reject continuations; in-memory DAG sharing and output; emitted CNF; source assignment validation. No external model advice, cache spill/eviction, hidden switch, Z5 Fourier transform, floating-point rounding or assumed arithmetic unit-cost. Conservative total for recognized members: O(L^5) bit time, O(L^3) writable bits with L the full source byte length. Literal single-tape microsteps remain unverified.

## Four falsifiers

F1: Maximum exact linear connection rank **does not force expensive source decision or counting**. All hub-star glue instances admit the stated polynomial-time recognizer and width-126 pointwise diagram; both SAT and UNSAT examples occur.

F2: The full 32 unary-domain masks from TMR-2 and TMR-4/078 do **not** encode these ternary correlations. Unary arc consistency can leave all five colors present even in UNSAT sources.

F3: A special five-symbol representation **does not bypass Boolean recoding**. The 3-bit OBDD and parsimonious CNF have only constant overhead.

F4: A restricted linear-compositional boundary rank **does not transfer to arbitrary machines**. A source-only algorithm enumerates 25 boundary differences and multiplies private-vertex factors in polynomial time.

## Four verification gates

**Gate 1, source:** 25 source-authenticated witness graphs, 12 malformed byte strings rejected, four valid out-of-family graphs rejected (including an enormous declared-n graph). No pre-labeled hub or solution advice.

**Gate 2, semantics:** 25 full source signatures checked by brute force, 50 source-derived glued OBDDs tested pointwise, **2,866,875 original assignments**, exact acceptance/rejection multiplicities, **122,785 actual CNF evaluations**, **3,125 diagonal-shift checks**.

**Gate 3, adversarial:** 25x25 exact integer determinant -8064 and 625 gluing contractions; eight larger YES/NO controls up to 203 vertices/600 arcs. Largest observed complete OBDD width125, internal nodes7320. Graph recognition is easy despite full rank.

**Gate 4, reproducibility:** Two complete Python runs and two independent Node runs produce byte-identical summaries. The independent Node implementation verifies 60,625 single-gadget and 1,378,125 glued assignments, and the source-standalone committed JavaScript verifies the exact 25x25 determinant with BigInt. Zero unexpected failures. Native TM microsteps, full LaTeX build and third-party mathematical peer review remain OPEN.

The runnable **standalone** integer certificate is `experiments/tmr/tmr4_t5_three_terminal080_standalone.js` and requires only Node.js. The complete Python compiler, source encodings, raw signed audit, independent JS, detailed ledger and run logs are retained in the user-facing TMR-4/080 evidence archive.

**Cross-agent reconciliation:** TMR-2/074 already has a different three-separator orbit-count theorem, and TMR-2/076 audits T5 polymorphisms. This work does not claim originality for general connection-rank/orbit theory. Keep source counting rank, pointwise FBDD representation size, and source-decision time separate.

**NEXT:** D4-T5-4CONNECTED-PRIME-DYNAMIC-TRANSFER. Construct mixed SAT/UNSAT sources remaining after all charged 1-, 2- and 3-separator, unary/domain, affine, cover, twin, quotient and easy-source checks. Transfer a necessary bound only between genuinely equivalent charged computational models. P versus NP remains OPEN.

## References

[1] L. Lovász, *The rank of connection matrices and the dimension of graph algebras*, European Journal of Combinatorics (2006), DOI 10.1016/j.ejc.2005.04.012; https://arxiv.org/abs/math/0408232.

[2] J.-Y. Cai and A. Govorov, *Perfect matchings, rank of connection tensors and graph homomorphisms*, Combinatorics, Probability and Computing (2021), DOI 10.1017/S0963548321000286.
