# TMR-4/076: exact T5 source-aware semicomplete-module compiler

**2026-11-17 18:36 PST.** PROVED/EXACT restricted source class, external mathematics review OPEN. Computational audit is finite. P versus NP OPEN.

## Authentic source and theorem
For a canonical explicit loopless directed graph G with no opposite arcs, form the graph H of missing adjacencies: uv is an undirected edge iff neither u->v nor v->u appears. Recover all connected components M_1,...,M_q of H and require q>=2. Authenticate that every pair of components has a complete, uniformly directed cross join. Nonmember graphs are reported **NONMEMBER**, not UNSAT. The quotient is a tournament.

Every color support of a component in a satisfying T5 labeling is in the ten-element family S={{a}:a in Z5} union {{a,a+2}:a in Z5}. Proof: any external vertex of color b imposes a common in-neighbor or out-neighbor domain, both two-element sets of the displayed form.

For an induced module G[M], let z be its count of internally isolated vertices. Exact support weights are:
* singleton support {a}: weight 1 iff M has no internal arcs, otherwise 0;
* pair support {a,a+2}: if a vertex has both internal in- and outdegree, weight 0; otherwise, if M has any arc, weight 2^z, since the restricted two-color target has one directed arc and every nonisolated source/sink is forced; if M has no arcs, weight 2^{|M|}-2.

Let W_i(S) denote this exact weight and K_ij(S,T) be 1 when the complete cross product S x T respects the uniform quotient arc, otherwise 0. Then

Z_T5(G) = SUM_{(S_1,...,S_q) in S^q} PROD_i W_i(S_i) PROD_{i<j} K_ij(S_i,S_j).

Exact supports make the sum disjoint. If q>5, the quotient contains a q-tournament, which cannot map noninjectively to loopless T5, so Z=0. Otherwise enumerate <=10^5 profiles, with exact integers of O(n) bits. Hence polynomial-time exact counting on the recognized class.

## Deterministic source-to-OBDD compiler
Use a module-by-module original-vertex variable order. Completed modules retain their observed exact support, one of ten. The active module retains its observed colors and a 10-bit mask of candidate supports consistent with all original vertex colors queried thus far. Each candidate imposes a per-vertex unary role mask derived from the internal arcs. Reject on a third color, a forbidden two-color pair, an empty candidate mask, a failed exact support at module completion, or an incompatible cross join. Include one 5-labeled reject-tail state at every remaining layer. The resulting five-way OBDD is **pointwise exact**, with Z accepted and 5^n-Z rejected original-label paths.

An active module has at most 1+5*2^3+5=46 nonreject states: empty seen set, one observed color with at most three candidate supports, or one of the five allowed observed pairs with one candidate. With q<=5, the OBDD has width at most 46*10^(q-1)+1 <=460001 and at most n(46*10^(q-1)+1) internal nodes. q>5 admits a width-one all-reject OBDD. A 3-bit-per-symbol Boolean OBDD costs at most seven nodes per 5-way node; direct auxiliary-free CNF has 3n+15m clauses.

## Counterexample to naive hardness transport
For k>=3 let M have U_1..U_k and V_1..V_k, with arcs U_i->V_j iff i!=j. The nonadjacency graph of M is connected; all original directed in/out signatures are distinct. Attach a vertex z with every M vertex pointing to z. This recognized connected, directed-false-twin-prime SAT graph has n=2k+1, m=k^2+k, beta=k^2-k and exactly five T5 assignments.

For the NO sibling join two copies of M with every cross arc directed from the first to the second. This has n=4k, m=6k^2-2k, beta=6k^2-6k+1, all false-twin signatures distinct and exactly zero solutions. Both modules require two target colors, while two distinct colors have at most one common successor, making a 2x2 complete directed join impossible. Both graphs have polynomial exact source-aware algorithms despite large cyclomatic rank and no false twins.

## SAME_REALIZATION, reproducibility, and scientific firewall
The parser reads the *complete* canonical ASCII JSON source and validates vertex and edge indices, duplicates, loop/digon exclusion and canonical order. Costed objects are the n^2 adjacency index, discovered nonadjacency components, authenticated complete joins, internal role/isolates, ten-support masks and exact integer weights, all q-support products, source-ordered live OBDD states, five transitions per internal node, reject-tail paths, addresses, output and verification. One conservative deterministic multitape upper pair with constant C=460001 is T=O(C^2(L+1)^6) bit time, S_peak=O(C(L+1)^3) bits. These are same-realization *uppers*, never universal lowers. No free source oracle or uncharged Z5 transform.

**Executed twice, identical results:** Python source SHA256 37427fc77e85f03b668838a1f4fe92b5c70a7c1ced0d7dd96df8eb5ed6b3ec34; original raw JSON SHA256 511a9b3c1f864f98344aa9c64186894976084f603b7e01ebb989d11dab3e964c. 80 accepted small graphs matched independent exhaustive counts and complete OBDD path counts, 104100 pointwise original-assignment comparisons, 250 valid NONMEMBER controls, 339 parser cases, 12 dense twin-prime YES/NO controls and one q=6 pigeonhole check, zero unexpected failures. Max observed OBDD width 26, nodes 1000. Largest k=48 YES: n=97, m=2352, beta=2256, Z=5; NO: n=192, m=13728, beta=13537, Z=0. Large k>16 use exact counting tests, not actual large OBDD construction. Original full Python source and raw output preserved in local conversation bundle, **not claimed pushed to GitHub**.

**Four gates:** DISJ PASS for restricted source algorithm; naive density/rank-to-necessity FAIL. Relativization PASS intermediate, nonrelativizing NP transfer OPEN. Simultaneous DTISP PASS same-execution upper only, forbidden lower OPEN. Deterministic configuration counting PASS upper consistency only. /341 FAIL full UNSAT; /386 RESTRICTED. No all-machine separation.

**Next D4-T5-PRIME-2CONNECTED-NONGAUGE:** combine directed-false-twin, semijoin, articulation, affine/domain and feedback decompositions on one authenticated source, seek genuinely mixed-answer residual cores and audit source-aware switching/alternative algorithms. An unrestricted lower bound remains OPEN.

Background on directed modular decomposition: McConnell and de Montgolfier, "Linear-time modular decomposition of directed graphs" (https://www.cs.colostate.edu/~rmm/digraphDecomp.pdf). Our elementary n^2 recognizer is independently specified and implemented, not an uncharged use of their algorithm.
