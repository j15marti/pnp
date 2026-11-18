# TMR-5/094: universally satisfiable T5 instances with #P-hard exact counting

**Owner:** TMR-5 PNP Machine Bottleneck Redteam. **Date:** 2026-11-18 Pacific. **Status:** proved Turing reduction, executable finite reproduction, external proof review open. **P versus NP is OPEN.**

## Precise statement and red-team significance

Let (T_5) be the loopless tournament on (mathbb Z_5) given by (a	o b) iff (b-ain{1,3}pmod5). Let (A) be its adjacency matrix.

For a loopless directed source graph (G=(V,E)), define (F_t(G)), for integer (tgeq1), by replacing **each original arc** (u	o v) with (t) internally vertex-disjoint directed paths of **each** length (4,5,6) from (u) to (v); all internal vertices are private. Original vertices remain. The class also allows (t=0), meaning all original vertices isolated.

**Theorem (decision-versus-counting firewall).** Every (F_t(G)) has a homomorphism to (T_5), even under *every arbitrary assignment of its original branch vertices*. Nevertheless, exact counting of (T_5)-homomorphisms on the class of (F_t(G)) is #P-hard under polynomial-time Turing reductions, and belongs to #P on the promise class. Thus it is **#P-complete under polynomial-time Turing reductions despite constant-YES decision complexity**.

This neither implies an unrestricted decision lower bound nor shows P != NP. It is an explicit separation of a restricted **decision task** from exact counting on the same restricted input class. In particular, any TMR-2/TMR-4 invariant lower-bounding decision work solely from the size of a counting tensor, high moments, or large number of solutions yields false positives.

## Exact transfer identity

Direct walk enumeration gives these row-zero entries of the cyclic transfer matrices:

| Path length | First row of (A^ell) |
|---|---|
| 4 | (4,4,1,6,1) |
| 5 | (2,10,5,5,10) |
| 6 | (15,7,20,7,15) |

Every entry is strictly positive. The three parallel paths have effective edge weight
[
w(d)=(A^4)_{0d}(A^5)_{0d}(A^6)_{0d}
     =(120,280,100,210,150)_d,qquad dinmathbb Z_5.
]
Thus every branch assignment extends. An instance with (n) branch vertices and (m) original arcs has (n+12mt) vertices and (15mt) arcs. Its exact count is
[
Z_t(G)=sum_{xinmathbb Z_5^V}prod_{(u,v)in E}w((x_v-x_u)mod5)^t.
]

Let (h_d(x)) count source arcs with difference (d), and let
(N_h=#{xinmathbb Z_5^V:h(x)=h}), for (h_0+cdots+h_4=m).
There are (H=inom{m+4}{4}=O(m^4)) possible histograms. Put
(z_h=prod_{d=0}^4w(d)^{h_d}). Then
[
Z_t(G)=sum_{h}N_h z_h^t.
]

## Crucial uniqueness certificate

The prime-exponent vectors of the five (w(d)), in prime order (2,3,5,7), together with the fixed-sum row, form
[
M=egin{pmatrix}
3&3&2&1&1\
1&0&0&1&1\
1&1&2&1&2\
0&1&0&1&0\
1&1&1&1&1
end{pmatrix},qquad det M=1.
]
If (z_h=z_{h'}), unique prime factorization gives agreement in the first four row-products; (h,h') also both sum to (m). Therefore (M(h-h')=0), and (det M=1) proves (h=h'). The (H) positive integer bases (z_h) are pairwise distinct.

Query the exact-count oracle on (F_t(G)) for (t=0,1,ldots,H-1). The resulting (H) equations form an invertible Vandermonde linear system over (mathbb Q) for the (H) coefficients (N_h). The target original count is
[
#mathrm{Hom}(G,T_5)
=sum_{h:h_0=h_2=h_4=0}N_h,
]
since precisely differences (1,3) are allowed by (T_5).

All oracle inputs have polynomial size, at most (n+12m(H-1)) vertices and (15m(H-1)) arcs. The numbers (z_hle280^m), Vandermonde entries and all queried counts have polynomial bit length; exact rational linear algebra is polynomial-time. The t=0 query is just (5^n), so it can be answered without the oracle. This is a **deterministic polynomial-time Turing reduction** from unrestricted (#mathrm{Hom}(-,T_5)) to universally satisfiable instances.

## Primary #P-hardness source and independent parsimonious bridge

Dyer and Greenhill, *The Complexity of Counting Graph Homomorphisms*, Random Structures & Algorithms 17:260-289 (2000), prove #P-completeness of exact (#H)-coloring for undirected loopless (H=C_5). DOI: https://doi.org/10.1002/1098-2418(200010/12)17:3/4%3C260::AID-RSA5%3E3.0.CO;2-W .

For each arbitrarily oriented edge (u	o v) of an undirected source graph, TMR-1's five-arc gadget inserts private (a,b,c) and arcs (u	o a, a	o b, b	o c, u	o c, c	o v). Exactly **one** private assignment exists if (v-uequiv1,4pmod5), and none otherwise. Indeed the first four arcs force ((a,b,c)=(u+1,u+2,u+3)); then (c	o v) forces (v-uin{1,4}). Therefore this is a parsimonious, linear-time (#C_5	o#T_5) reduction, making unrestricted (#T_5) #P-complete. Composition with the above Vandermonde reduction supplies the claimed restricted-class Turing hardness.

This is **not** claimed as a parsimonious reduction to the universally SAT family: a parsimonious reduction cannot map a zero count to a strictly positive count.

## Reproduction and limits

The standalone standard-library Python verifier independently computed all powers (A^ell) for (ellle6) by matrix multiplication and by enumerating directed walks. It confirmed the weight vector, (det M=1), strict positivity of all path transfers, all **3,125** private gadget assignments, and Vandermonde reconstructions of **660 histogram coefficients across 36 randomly generated** 1-, 2- and 3-arc sources; in every case the reconstructed (T_5) count agreed with independent direct enumeration. A native 14-vertex, 15-arc one-edge three-path CSP backtracker returned **4,300** homomorphisms as predicted ((5sum_dw(d))). Zero assertion failures. Repeated executions returned the same parsed JSON.

**Finite verification is not a substitute for the symbolic theorem.** The verifier's modular Vandermonde checks use the prime (2^{61}-1) only for small graphs where no modular collision occurs; the full theorem explicitly uses exact rational interpolation over (mathbb Q), not fixed-prime reconstruction, and makes no claim of practical efficiency.

## Ranked dependency audit

| Arrow | Status |
|---|---|
| Specific (T_5)-homomorphism NP-completeness | **PROVED** by Bang-Jensen/Hell/MacGillivray 1988 semicomplete theorem |
| (#C_5) #P-completeness | **PROVED** by Dyer/Greenhill 2000 primary counting theorem |
| Parsimonious five-arc (#C_5	o#T_5) gadget | **PROVED**, direct algebra and 3,125-case exhaustive check |
| All F_t(G) SAT, all original branch assignments extend | **PROVED**, (A^4,A^5,A^6>0) |
| Polynomial Turing recovery of arbitrary (#T_5) counts from counts of F_t(G) | **PROVED**, Vandermonde plus determinant-one certificate |
| Restricted decision problem hardness inferred from restricted #P-hard counting | **FALSIFIED** (decision is constant YES) |
| Counting or tensor complexity forces unrestricted decision-machine work | **FALSIFIED as an instancewise inference** |
| Worst-case representation-independent superpolynomial T5 decision bound | **OPEN** |
| Superpolynomial Boolean-SAT decision lower bound | **OPEN** |

**Next priority:** require any candidate TMR-2/TMR-4 machine-cost invariant to distinguish existential projection from exact multiplicity, even when every possible branch labeling extends to a valid solution.

**Further primary source:** Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3):281-298 (1988), https://doi.org/10.1137/0401029.
