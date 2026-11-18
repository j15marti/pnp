# TMR-5/094: exact #P-hard counting on universally SAT native T5 instances

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Date:** 2026-11-18 Pacific. **Status:** symbolic theorem with finite independent reproduction; external proof review pending. **P versus NP remains OPEN.**

## Theorem and correct hardness scope

Let the fixed loopless tournament $T_5$ have edge relation $a\to b$ iff $(b-a)\bmod 5\in\{1,3\}$. For every arc $u\to v$ in a directed source $G$, create $t$ internally vertex-disjoint **directed paths of each length 4, 5, and 6** from $u$ to $v$. The internal vertices of all paths are private. Denote the native T5 instance by $F_t(G)$. At $t=0$, retain only the original isolated vertices.

**Theorem:** Every $F_t(G)$ is satisfiable, even if every original branch vertex has an arbitrary prescribed label in $\mathbb Z_5$. Nevertheless, exact T5 homomorphism counting restricted to this *universally SAT* family is #P-complete under **polynomial-time Turing reductions**. The restricted **decision** problem is therefore constant YES despite #P-hard exact counting.

This is a counting-versus-decision counterexample, **not** a separation of P and NP or a superpolynomial lower bound. In particular, large tensor counting complexity cannot alone certify difficulty of existential T5 decision.

## Fully explicit weighted path elimination

Let $A$ be the $5\times5$ adjacency matrix of $T_5$. Independent direct-walk enumeration and matrix multiplication give the following first rows (the matrices are circulant):

| Length $\ell$ | $(A^\ell)_{0,*}$ |
|---|---|
| 4 | (4,4,1,6,1) |
| 5 | (2,10,5,5,10) |
| 6 | (15,7,20,7,15) |

Each matrix is strictly positive, proving that **every original-vertex assignment extends** to every private path. Three parallel paths, one of each length, give effective edge weight
$$
w(d)=(A^4)_{0d}(A^5)_{0d}(A^6)_{0d}
=(120,280,100,210,150)_d
$$
where $d=(x_v-x_u)\bmod5$. Therefore
$$
Z(F_t(G))=\sum_{x\in\mathbb Z_5^{V(G)}}\prod_{(u,v)\in E(G)}w((x_v-x_u)\bmod5)^t.
$$
For $n=|V(G)|$, $m=|E(G)|$, $F_t(G)$ has exactly $n+12mt$ vertices and $15mt$ arcs.

## Determinant-one certificate and polynomial Turing reduction

For branch assignment $x$, let $h_d(x)$ be the number of source arcs having difference $d\in\mathbb Z_5$. Each histogram $h=(h_0,\ldots,h_4)$ has $\sum_dh_d=m$. Let $N_h$ be the number of branch assignments with histogram $h$ and put $z_h=\prod_dw(d)^{h_d}$. Then
$$
Z(F_t(G))=\sum_{h:\sum_dh_d=m}N_h z_h^t.
$$

The prime valuations of the five weights, with rows for $2,3,5,7$ and a final row encoding $\sum h_d=m$, form
$$
M=\begin{pmatrix}
3&3&2&1&1\\
1&0&0&1&1\\
1&1&2&1&2\\
0&1&0&1&0\\
1&1&1&1&1
\end{pmatrix},
\qquad \det M=1.
$$
If $z_h=z_{h'}$, uniqueness of prime factorization yields equality in the first four rows, while both histograms have equal sum in the last row. Since $M$ is invertible over $\mathbb Q$, $h=h'$. Thus the $H=\binom{m+4}{4}=O(m^4)$ distinct histograms have **pairwise distinct positive integer bases** $z_h$.

Obtain the $H$ oracle counts $Z(F_t(G))$ for $t=0,\ldots,H-1$. This is an invertible Vandermonde system over $\mathbb Q$, which exactly recovers all coefficients $N_h$. The unrestricted original T5 count is
$$
Z(G)=\sum_{h:\,h_0=h_2=h_4=0}N_h
$$
since the original edge relation permits only differences $1$ and $3$.

Each oracle instance has $O(n+m^5)$ vertices and arcs, and all interpolation values have polynomial bit length: $z_h\le280^m$ and $t<H=O(m^4)$. Exact rational linear algebra takes polynomial bit complexity. The $t=0$ count is simply $5^n$, and need not be sent to the oracle.

This is **a polynomial-time Turing reduction**. It is not parsimonious, and that distinction is mandatory because a zero-count source cannot be mapped parsimoniously to a strictly positive target count.

## Primary theorem grounding: #T5 is #P-complete

Dyer and Greenhill, *The complexity of counting graph homomorphisms* (2000), established #P-completeness of counting homomorphisms to an undirected five-cycle $C_5$ [1]. The already independently verified TMR-1 five-arc gadget is an exact parsimonious reduction from #C5 to native #T5: for each source undirected edge choose an orientation $u,v$, introduce private $a,b,c$ and add
$$
u\to a,\quad a\to b,\quad b\to c,\quad u\to c,\quad c\to v.
$$
The first four arcs uniquely force $(a,b,c)=(u+1,u+2,u+3)$ modulo five. The final edge holds precisely when $(v-u)\bmod5\in\{1,4\}$, the undirected $C_5$ adjacency. Exactly one private extension exists per valid source edge; none exists otherwise. The composed interpolation therefore proves **Turing #P-completeness for exact counting restricted to the universally SAT family**.

Independent decision NP-completeness of unrestricted T5-CSP follows from the Bang-Jensen, Hell and MacGillivray semicomplete-target theorem [2], but is not being used incorrectly to assert counting hardness.

## Reproduction

The standalone CPython standard-library verifier independently computed $A^\ell$ for $\ell=1,\ldots,6$ by matrix multiplication and by enumeration of all two-choice directed walks. It verified strict positivity for lengths 4,5,6, the five weights and $\det M=1$, exhaustive truth of all **3,125** private gadget assignments, and exact modular Vandermonde reconstruction in **36** random source instances with one to three edges, recovering **660** histogram coefficients. Every recovered original T5 count agreed with independent direct enumeration. A separate native graph backtracker counted **4,300** homomorphisms on the one-source-edge gadget containing a 4-, 5-, and 6-path in parallel, with 14 vertices and 15 arcs. **Zero assertion failures.** Two executions returned identical parsed summaries.

The finite verifier used $2^{61}-1$ modular interpolation for small tested cases only. The theorem relies on exact **rational** interpolation with arbitrary precision; no fixed-prime claim is promoted. Independent formal proof-kernel verification and external mathematical review have not occurred.

## Ranked proof-chain synthesis

| Arrow | Status |
|---|---|
| Specific T5 homomorphism NP-complete | PROVED, primary theorem [2] |
| #C5 exact count #P-complete | PROVED, primary theorem [1] |
| Parsimonious C5-to-T5 five-arc count gadget | PROVED, exact symbolic gadget + exhaustive finite audit |
| Every $F_t(G)$ SAT under all original branch labelings | PROVED, strictly positive transfer powers |
| #T5 counting Turing-reduces to counts of always-SAT instances | PROVED, determinant-one Vandermonde reduction |
| #P-hardness of the restricted count implies hard restricted SAT decision | **FALSIFIED**, restricted SAT always YES |
| Representation/counting complexity implies arbitrary machine decision cost | **FALSIFIED as an instancewise inference** |
| Unrestricted T5 decision superpolynomial bound and Boolean SAT lower bound | **OPEN** |

**Next red-team criterion:** candidate TMR-2/TMR-4 cost invariants must charge **existential decision** separately from exact multiplicity after path suppression, weighted transfers and global source-aware algorithms.

### Primary references

[1] M. Dyer and C. Greenhill, *The complexity of counting graph homomorphisms*, Random Structures & Algorithms **17** (2000), 260–289. [Publisher record](https://doi.org/10.1002/1098-2418%28200010/12%2917%3A3/4%3C260%3A%3AAID-RSA5%3E3.0.CO%3B2-W).

[2] J. Bang-Jensen, P. Hell and G. MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. **1** (1988), 281–298. [DOI](https://doi.org/10.1137/0401029).
