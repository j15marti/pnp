# TMR-4/093: Mixed T5 sources with identical bounded-radius local observations

**Status:** RESTRICTED theorem, finite COMPUTER verification, not a P-versus-NP proof. Continue TMR-4 and /092 without changing owner, title, schedule or end-to-end controls.

## Candidate and exact result

Let R(a,b) mean (b-a) mod 5 in {1,3}. For original source vertices u,v, a successor cell introduces auxiliary z and three arcs (u,v),(u,z),(z,v). Its only satisfying extension given u=a is v=a+1, z=a+3 modulo 5.

Let B=(U,W,F) be a connected source with all arcs directed U to W and choose sender root s. Attach two successor-cell rings at s. On the SAT side G+ give them lengths (5t,5t); on the UNSAT side G- use (5t-1,5t+1), t>=1. Both graphs have N=|V(B)|+20t-2 original five-symbol vertices and M=|F|+30t arcs.

**Theorem /093A:** Z(G+)=Z(B), and Z(G-)=0. Each B assignment has exactly one G+ extension. The ring holonomy enforces L=0 mod 5, so neither G- ring can be completed. Every induced subinstance of G- on fewer than 5t-1 vertices is satisfiable because it omits a spine vertex from each ring and leaves only open successor paths attached to an otherwise satisfiable sender/receiver source.

**Theorem /093B, locality:** At any radius p with 5t-1>4p+4, the multisets of center-rooted, directed radius-p induced neighborhoods of G+ and G- are exactly isomorphic, including multiplicities. The radius cannot see ring closure; neighborhoods near the attachment each contribute a fixed number of types per ring, and periodic interior types depend only on the sum of ring lengths, which is 10t on each side. This does not assert global graph isomorphism.

**Theorem /093C, legal cheap-source counterexample:** A source-only expected-linear-time recognizer scans degree-(1,1) auxiliaries whose predecessor u and successor v are linked by the direct arc u->v, verifies the three-arc successor cell cover, traverses the two rooted successor cycles, checks that residual arcs have only sender and receiver vertices, and tests the two cycle lengths modulo 5. The recognizer requires no supplied ring labels or assignment advice. Inputs outside the recognized source class retain an exponential general fallback. The construction is not a polynomial-time algorithm for unrestricted T5-CSP.

For an even-r checkerboard-oriented grid base B, restricting all added variables and the common root to their uniquely consistent values leaves the exact assignment function of the grid with one sender fixed to zero. The /092 induced-matching argument, losing at most four crossing edges upon fixing that vertex, yields an every-fixed-order five-way OBDD width lower bound at least 2^floor(max(0,r/2-4)/64) on G+. On G-, the assignment function is identically zero, so a width-one complete-query rejecting OBDD with N nodes suffices. Both source SAT decisions remain expected linear. This proves a representation-to-source *transfer obstruction*, not an adaptive-FBDD or Turing-machine lower bound.

## Four falsifiers

F1: At t=1, the (5,5) and (4,6) ring pairs agree locally at radius one but not radius two; locality bounds must retain their explicit radius condition.

F2: A growing shortest induced UNSAT subinstance does not entail a hard source decision. Global modular holonomy is cheaply source-discoverable.

F3: High minimum frontier and SAT-side all-order OBDD width do not imply any hard SAT-vs-UNSAT distinction. The UNSAT complete assignment function is simply constant zero.

F4: The 32 unary-domain masks, grouped validity-coded 3-bit FBDDs, and unrestricted interleaved-bit Boolean FBDDs are different interfaces. No unrestricted reverse-transfer theorem follows.

## SAME_REALIZATION ledger

Input parsing, canonical-byte SHA-256, malformed input rejection, adjacency construction, triangle discovery, graph-order recovery, residual sender/receiver check, modulo arithmetic, full five-way fan-out, rejected assignment continuations, state merges, cache, BigInt multiplicity, materialized output, Boolean conversion and any model switches are charged. Finding a suitable order or gadget is not free. The audited native complete OBDD uses an exponential base-state enumeration for the SAT side; it is not a polynomial-size universal compiler. No Fourier or tensor arithmetic was used in this construction. Direct auxiliary-free CNF: 3N+15M clauses, 9N+90M literal occurrences. Local contiguous-block Boolean expansion: at most six binary nodes per native five-way node. Unrestricted interleaved reverse direction OPEN.

## Four verification gates, COMPUTATIONAL

G1: Twelve canonical source files across six parameter pairs passed source-only discovery; eleven malformed variants rejected. Ten independently read JS source files matched canonical Python SHA-256.

G2: Independent constraint-search enumerated 30/0 assignments at (r,t)=(2,1), and 410/0 at (3,1). The complete original-assignment OBDD checked 5^N accepted/rejected path conservation; at (r,t)=(2,3), SAT OBDD has 386 nodes, width 21 and count 30, while UNSAT OBDD has 62 nodes, width one and count zero. On the r=2 base all 625 assignments were examined, with 6,960 one-symbol ring falsifiers at t=3. All induced subgraphs of size <=3 of the 22-vertex t=1 UNSAT instance (1,793 total) were separately verified satisfiable.

G3: The two independent implementations checked 2,048 directed domain-mask support cases each. Original-valid-code and invalid-code signed-literal CNF evaluations agreed with direct five-symbol semantics.

G4: Exact rooted directed ball isomorphism/multiplicities passed at (r,t,p)=(2,1,1),(2,3,2),(2,5,4),(3,1,1),(3,3,2),(4,4,3). Python and JavaScript deterministic repeats were byte identical, with zero unexpected failures. Finite experiments do not prove lower bounds.

## Manuscript and handoff

Add /093 to main4_PNP_COST_SOUND_ABSTRACTION.tex and archive /092 handoff, preserving all earlier sections. New dependency D4-T5-BEYOND-LOCAL-OBSTRUCTIONS-094: search for *mixed* SAT/UNSAT sources not removable by charged affine, palette, successor, holonomy, sender/receiver, nesting or nonaffine quotients. Demand genuinely equivalent machine models before any reverse lower-bound transfer.

Related structural references: Barto, Kozik and Niven, SIAM J. Comput. 2009, DOI 10.1137/070708093; Razgon, arXiv:1709.08890 and arXiv:2103.09115. Independent mathematical review and physical TM microsteps remain OPEN. **P versus NP remains OPEN.**
