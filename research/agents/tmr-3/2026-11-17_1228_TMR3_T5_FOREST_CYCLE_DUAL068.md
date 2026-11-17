# TMR-3/068: A polynomial-space dual exact algorithm for the five-symbol beat-relation CSP

**Date:** 2026-11-17, 12:28 PST (America/Los_Angeles). **Identity:** TMR-3 / PNP Time-Space Tradeoffs. **Status:** PROVED/EXACT for the explicit fixed-template algorithms, with independent mathematical review OPEN. Finite audits COMPUTATIONAL. P versus NP OPEN.

**Latest science priority:** The November 17 T5 directive supersedes the prior TMR-3 checkpoint-first priority but preserves the five ownership, schedules, end-to-end workflow and safeguards. Owns only `main3_PNP_TIME_SPACE_TRADEOFFS.tex` and TMR-3 files. Does not read or modify retired proof trackers.

## Candidate and falsifiers stated before source review

For EVERY finite directed graph G with explicitly enumerated vertices, let n=|V|, m=number of distinct oriented arcs, c=number of weak components, and r=m-n+c after loops/opposite arcs have been rejected. Candidate **C3-T5-FOREST-CYCLE-DUAL**: a single uniform blank-start exact counter decides CSP(T5) using either (i) 2^(n-c) binary forest increments or (ii) a 5^r streaming cyclotomic character sum with polynomial physical workspace. Everything, including graph parsing and basis construction, is charged.

Targeted falsifiers: (F1) automorphism by adding a global Z5 offset fails for some edge; (F2) a chord or reversed tree arc has an incorrectly signed difference; (F3) a fundamental cycle basis over Z5 does not characterize gradients; (F4) integer cyclotomic arithmetic causes an uncharged precision, retention or cancellation cost. Self-loops, opposite arcs, disconnected and empty graphs are adversarial controls.

## Source domain and known complexity

T5 has vertices Z5 and arcs a->b iff b-a in {1,3} modulo 5. The ten arcs are the user's A/B/C/D/E beat relation, with 0=A,1=B,...,4=E. Every unordered pair has precisely one directed arc; loops and reciprocal pairs are absent. In particular 0->1->2->0 and 0->3->4->0 are two distinct directed cycles.

**KNOWN THEOREM imported with correct scope:** Bang-Jensen, Hell, and MacGillivray (1988), *The Complexity of Colouring by Semicomplete Digraphs*, SIAM Journal on Discrete Mathematics 1(3):281-298, DOI 10.1137/0401029: H-colouring for a fixed semicomplete digraph H is NP-complete if H has more than one directed cycle. Hence **CSP(T5) is NP-complete**, independently of this construction. This is a general complexity classification, not an explicit quantitative 3-SAT-to-T5 reduction or ETH-rate transfer.

Executable reference input uses ASCII `n m` on the first line and exactly m lines `u v` for zero-based vertices 0..n-1. It rejects malformed records/endpoints and deduplicates repeated arcs. For the formal bit-machine upper bounds, use a canonical binary source with **unary n and m** followed by fixed-width binary endpoint fields, so N >= n+m and malformed sources have a defined reject response. This prevents the ambiguity of a huge hidden n written in a short binary header. No free adjacency matrix or decomposition is given.

## Exact theorem A: binary spanning-forest increments

For a graph with no self-loop or opposed arc pair, take any spanning forest of its underlying simple graph. Fix each root colour to zero. For each oriented forest edge u->v, the difference x_v-x_u is either 1 or 3; traversing v->u reverses the sign. Thus one binary bit per forest edge chooses the child colour from its parent's colour. A forest has n-c edges. Every non-tree arc is then checked against the reconstructed labels.

There is a **bijection** between surviving bit strings and homomorphisms with every component root fixed to zero. Indeed a satisfying labelling uniquely induces all tree differences, and the chosen tree differences uniquely reconstruct all vertex labels. For each weak component, adding any of five offsets to all labels preserves all differences and yields five distinct labelled solutions. Therefore
```
#Hom(G,T5) = 5^c * sum_{b in {0,1}^{n-c}} [all non-tree arcs satisfied].
```
For a forest this specializes to exactly `5^c 2^(n-c)` solutions. Immediate rejection of loops/antiparallel arcs is sound because T5 is loopless and antisymmetric. Empty G with n=0 has one empty homomorphism.

The executable checks every previously assigned neighbour during backtracking; this is safe because any tree completion keeps assigned colours fixed. A locally headed deterministic multitape implementation parses and validates N bits, stores two directed adjacency bits per vertex pair, builds the forest with actual traversals, enumerates binary increment bits, checks all arcs, accumulates an exact O(n)-bit integer and emits it. One conservative same-run physical upper envelope is
```
T_forest(N) = O((N+1)^6 (1+2^(n-c))),
S_peak,forest(N) = O((N+1)^3) bits.
```
These are intentionally loose polynomial tariffs, not a Python-runtime estimate. The head movements, input materialization, output and every failed branch are covered. At most 2^(n-c) complete binary branches occur, and the finite search tree has O(n 2^(n-c)) nodes. No witness or guessed graph is preloaded.

## Exact theorem B: cycle-space residue DP and streaming Fourier count

Retain an arbitrary fixed orientation of each of the m distinct graph edges. Write a chosen difference d_e in {1,3} on each edge. Let C be the r-by-m signed fundamental-cycle matrix of the spanning forest, with one row per non-tree edge and entries in {-1,0,1}, interpreted modulo 5. Each row follows its chord forward and its unique forest return path backward.

**Integrability lemma.** These differences are induced by some vertex assignment iff C d = 0 in Z5^r. Necessity follows by telescoping around cycles. Conversely, fix one zero-labelled root per component, integrate the differences along the forest and use C d=0 to verify each chord. Every admissible d yields exactly 5^c original labelled solutions. Thus
```
#Hom(G,T5) = 5^c * sum_{d in {1,3}^m} [C d = 0 mod 5].
```

**Method B1, exact residue DP.** Initialize a dictionary D[0]=1 over Z5^r. For each edge column C_e and every retained residue s, add D[s] to both D_new[s+C_e] and D_new[s+3 C_e]. At the end return 5^c D[0]. Up to 5^r states and m transitions rounds are used. Integer weights have at most O(m) bits. This produces a simple correct algorithm with `T=5^r poly(N)` and `S=5^r poly(N)` bits; no subexponential worst case is claimed.

**Method B2, exact streaming Fourier count with POLYNOMIAL space.** Let zeta=e^(2pi i/5). Orthogonality yields
```
#Hom(G,T5) = (5^c/5^r) *
   sum_{lambda in Z5^r} product_{e=1}^m
       ( zeta^(lambda.C_e) + zeta^(3 lambda.C_e) ).
```
Crucially, do NOT approximate complex numbers. Work in the exact rank-four integral algebra `Z[z]/(1+z+z^2+z^3+z^4)`. For each lambda, stream across m edges, multiplying four-integer-coordinate polynomials and reducing by the fixed monic cyclotomic polynomial. Stream the 5^r lambda values using a radix-five counter and accumulate four exact integers. The final sum is an **integer scalar divisible by 5^r**; all three nonconstant basis coordinates cancel exactly. Multiply its quotient by 5^c and emit the answer. Each intermediate polynomial coefficient has at most O(m+r) bits because the unreduced product has at most 2^m terms and the sum has at most 5^r products; fixed-degree reduction changes the magnitude by at most a constant exponential in m, still O(m+r) bits. The stored C is O(mr) small signed entries. Therefore one uniform bit machine has conservative simultaneous
```
T_Fourier(N) = O((N+1)^8 (1+5^r)),
S_peak,Fourier(N) = O((N+1)^3) bits.
```
This bound includes parsing, constructing/testing the fundamental cycles, loop/opposite-arc controls, complete radix-five enumeration, per-edge dot products, exact polynomial multiplication/reduction, arithmetic precision, retained accumulator, division and output. No complex oracle, FFT unit-cost operation or preloaded cycle basis exists.

**Combined uniform solver:** compute n,m,c,r with charged preprocessing; compare binary integers 2^(n-c) and 5^r in polynomial time; choose exactly one of the forest and streaming Fourier methods. It has
```
T(N) = (N+1)^O(1) * (1 + min{2^(n-c),5^r}),
S_peak(N) = (N+1)^O(1) bits.
```
This is a nontrivial exact upper bound for the NP-complete CSP(T5), not a lower bound. In a sparse connected graph with m=n-1+O(log N), the cycle-rank branch is polynomial; for arbitrary graphs the binary-forest branch is at most 2^(n-1) up to polynomial factors.

## Further baseline and controls

Plain 5-label exhaustive search takes 5^n poly(N) time, polynomial storage. On a supplied elimination order with induced width w, exact factor elimination
`F_v(y)=sum_{a=0}^4 product_{f: v in scope(f)} f(y,a)`
has time `5^(w+1) poly(N)`; storing full tables requires `5^w poly(N)` bits and must be charged. A natural orientation of an underlying simple cycle with a forward edges and b backward edges has
```
#Hom(Cycle,T5) = 5 * sum_{k=0}^a sum_{l=0}^b
 binom(a,k) binom(b,l) * [(a-b+2(k-l)) == 0 mod 5].
```
Every attached forest vertex contributes a factor two. For the fully oriented three-cycle the count is 15, a transitive directed triangle has count 5, a directed five-cycle has count 10, and T5 itself has five automorphisms/homomorphisms. A single oriented edge has 10 labels. The 1988 NP-completeness does not imply that any single input is hard.

The TMR-2/067 current main result supplies a separate exact cofactor quotient with domain-mask intersections and an important easy oriented-complete-bipartite family (count `5(2^a+2^b-2)`). It is NOT superseded by this algorithm: our binary spanning-forest and Z5 cycle-space algorithms are alternative source-grounded representations and jointly prove a new parameterized time/space upper envelope. Its 12-mask domain alphabet and source-aware shortcuts remain permitted.

## Actual execution and evidence

**Executed locally using CPython and standard library, seed 202611171228:**
- Public readable runner `experiments/tmr/tmr3_t5_forest068.py`, revision `tmr3-t5-forest068-v4`, Git blob `4a586c0a45c937e1176e16bbe02fb56ff8b03727`.
- Immutable raw result `results/raw/tmr/2026-11-17_1228_TMR3_T5_FOREST068_PY_RAW.json`, Git blob `75a70ee578bb7f94d9e56f41f51b5d7c7264d29a`.
- 1,867 counted checks, 650 random directed graphs, 350 exact cycle-rank DP crosschecks and 350 independent integer-cyclotomic Fourier crosschecks, zero failures. Small-graph forest counter compared with independent full 5^n brute force; disconnected forests, cyclic orientations, loops, opposed arcs and malformed parser strings also tested. Counts of the four named controls were 15, 5, 10 and 5.
- A separate longer original local reference also compared full 5-state variable-elimination counting, pseudoforest closed forms and brute-force counts; 3,535 checks, zero failures. That longer reference was run locally but NOT published to this GitHub branch, so it is not a reproducible repository claim. Local source `/mnt/data/tmr3_t5_20261117/tmr3_t5_exact068.py`, raw `tmr3_t5_exact068_raw.json`.
- An initial larger cycle test exceeded a 30-second stage budget; it was bounded and a revised audit ran successfully. No native locally headed Turing-machine microcode, full repository preflight, independent theorem peer review or compiled LaTeX check is claimed. Local git checkout was blocked by GitHub DNS resolution; connector readback was used instead.

## Four gates and all-model scope

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS RESTRICTED: constructive count/decision upper bounds only. No static-rank-to-hardness inference; DISJ, affine and easy complete-bipartite paths remain legal. |
| Relativization | NOT APPLICABLE WITH REASON to a separation: none attempted. The fixed-template classification is a sourced known theorem, not a nonrelativizing lower-bound breakthrough; BGS, algebrization and Natural Proofs guards retained for future transfer. |
| Simultaneous DTISP | PASS for the separate declared complete uniform algorithm branches, each with its own same-run upper time and peak memory. A prohibited FLMV pair, quantitative 3SAT reduction and any all-algorithm lower bound remain OPEN. |
| Deterministic configuration counting | PASS as an UPPER-bound consistency check: a fixed deterministic halting machine with polynomial writable space admits at most 2^poly(N) complete configurations, compatible with these algorithms. It is not a work lower bound, nor a randomized/quantum theorem. |

Preserve Horn/2SAT, affine/Gaussian, bounded treewidth, equality, autarkies, independent products, source-sharing, padding, selector, unique-solution, local-basis/field, compact caching/recomputation, malformed-input, count-normalization and optional source-aware solver alternatives. Every proof above is constructive upper bound and must NOT be promoted to P versus NP. Historical /341 FAIL as full UNSAT authority, /386 RESTRICTED. No majority, quantum, randomized or circuit-to-CNF claims are used.

## ONE next load-bearing lemma: C3-T5-RATE-TRANSFER

Recover or construct an explicit authenticated sparse 3-SAT to T5 reduction with fully specified vertex/arc blowup n_T5,m_T5, source conversion time and simultaneous peak space. Determine precisely which existing 3-SAT TIME/SPACE or ETH-type conditional bounds survive via the correct direction SAT <= T5. A generic 1988 NP-completeness classification alone does NOT provide a linear-size reduction or subcritical deterministic time-space transfer. Independently review this report and the original semicomplete theorem before promoting any quantitative lower-bound corollary.

**Primary citation:** J. Bang-Jensen, P. Hell, G. MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3):281-298 (1988), DOI 10.1137/0401029, https://epubs.siam.org/doi/10.1137/0401029. Other project source: TMR-2/067 exact domain cofactor report, merged PR #223.
