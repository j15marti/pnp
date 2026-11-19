# TMR-5/097: all-order OBDD hardness on trivially satisfiable T5 instances

**2026-11-18, TMR-5, PNP Machine Bottleneck Redteam.** Symbolic theorem with finite verification, external proof review pending. **P versus NP OPEN.**

## New theorem and scope

Let H=(U,W;E) be an undirected bipartite graph, maximum degree Δ, with even N vertices. Orient every edge U→W to obtain a native T5 instance D(H), where R(a,b) holds iff b−a mod 5 belongs to {1,3}. Its satisfaction-indicator function is F_H(x)=∏_{u→v} R(x_u,x_v). Every such D(H) is a height-one DAG and is **always satisfiable**, by assigning 0 to U and 1 to W.

For **every order of the five-valued vertex variables**, take the first N/2 vertices S. The minimum width of a deterministic ordered decision diagram representing **the complete assignment indicator** F_H is at least

    width ≥ 2^( |δ(S)| / (2 Δ²) ).

This holds as a rank argument over **every field**. It is not an algorithmic time lower bound for deciding existential SAT.

### Proof of rank lower bound

Each chosen crossing edge uv in an **induced matching in the full graph** may have its U endpoint restricted to {0,3} and W endpoint to {1,3}. Fix all other vertices to the uniform SAT witness (0 on U, 1 on W). All edges other than matching edges stay satisfied, since R(0,1)=R(0,3)=R(3,1)=1. A matched edge contributes exactly

    Q = [[1,1],[1,0]], det(Q) = −1.

The prefix/suffix communication matrix has a restricted submatrix Q⊗k, where k is the number of crossing induced-matching edges. The transpose is the same Q if a matching edge crosses backward relative to the variable order. Hence its rank is 2^k over every field, and at least 2^k residual functions must occur in any ordered decision diagram.

Greedy selection from the cut δ(S) extracts an induced matching of size k≥|δ(S)|/(2Δ²): selecting uv removes candidate edges incident to N(u)∪N(v), at most 2Δ vertices and at most 2Δ² incident edges. Requiring inducedness in the **full graph** (not merely the cut bipartite graph) prevents a hidden tensor-product error.

### Explicit hypercube, all static orders

Take H=Q_d, the d-dimensional hypercube. N=2^d, Δ=d, bipartitioned by parity. The edge-isoperimetric inequality |δ(S)|≥min(|S|,N−|S|) is proved by induction: split the cube into two size-M cubes, with chosen-set sizes a and b. The inductive internal boundaries plus connecting-coordinate crossings are at least min(a,M−a)+min(b,M−b)+|a−b|, which is at least min(a+b,2M−a−b) in the cases a,b≤M/2, a,b≥M/2, and the mixed case. Every balanced order prefix therefore has at least N/2 crossing edges. Consequently

    width(ODD(F_Qd)) ≥ 2^(N/(4d²)) = 2^Ω(N/(log N)²)

**for every static symbol-variable ordering**, although a satisfying assignment is written down in O(N+|E|) time.

For any known constant-degree bipartite edge-expander family with |δ(S)|≥h|S| when |S|≤N/2, the identical argument yields width≥2^(hN/(4Δ²))=2^Ω(N) for **every** static symbol ordering. Existence of bounded-degree expanders is standard (Reingold–Vadhan–Wigderson, 2002; a bipartite family can be obtained by a standard bipartite variant).

## Independent reproducibility

The standard-library Python verifier executed twice with byte-identical JSON. Checks:

| d | N | balanced cuts | minimum crossing boundary | minimum greedy induced matching | #Hom(T5) |
|---|---:|---:|---:|---:|---:|
| 2 | 4 | 6 | 2 | 1 | 30 |
| 3 | 8 | 70 | 4 | 1 | 190 |
| 4 | 16 | 12,870 | 8 | 2 | not enumerated |

Every one of **65,808 vertex subsets** of cubes Q2,Q3,Q4 passed the isoperimetry check; all **12,946 balanced cuts** passed inducedness and matching extraction. **142** restricted matrices, with **4,504** independently checked entries, agreed exactly with Q⊗k and had full rank by Gaussian elimination modulo 101. Two independent exact counting methods agreed for Q2 and Q3. **Zero failures**. The compact GitHub verifier is independently executed and checks 4,616 restricted entries.

## Adversarial proof-chain firewall

| Claim | Status |
|---|---|
| Fixed-template T5-CSP NP-complete | PROVED by Bang-Jensen, Hell, MacGillivray (1988) |
| Height-one native T5-CSP always YES | PROVED, explicit 0/1 witness |
| Full-indicator rank≥2^k for any crossing induced matching | PROVED |
| Explicit hypercube indicator has superpolynomial **all-static-symbol-order** ODD width | PROVED |
| Bounded-degree bipartite expander indicators have exponential all-symbol-order ODD width | PROVED with established expander existence |
| Even the **minimum over variable orders** of ODD width implies difficult existential SAT | **FALSIFIED by this family** |
| Adaptive FBDD or arbitrary interleaving of Boolean bits inherits the bound | OPEN; not established |
| Representation-independent worst-case T5/SAT machine-time lower bound | OPEN |
| P versus NP | OPEN |

**Encoding caveat:** the theorem directly covers five-way symbol ODDs and binary OBDDs for grouped, non-interleaved 3-bit symbol codes. It does not justify a claim for arbitrary bit-interleaved Boolean orders. **Adaptive FBDD caveat:** the fixed-prefix proof does not apply unchanged. **Counting caveat:** no polynomial exact-count algorithm on this hypercube family is claimed. The old TMR-5/090 ladder only forced a bad order; this result forces all static symbol orders.

Next challenge for TMR-2/TMR-4: apply their necessary-work invariant to the source→sink hypercube and expander instances. Any invariant inferring hard satisfiability from minimum-order indicator ODD width is falsified by an explicit linear-time solution.

## Primary literature
1. J. Bang-Jensen, P. Hell, G. MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3):281–298 (1988). https://doi.org/10.1137/0401029
2. O. Reingold, S. Vadhan, A. Wigderson, *Entropy Waves, the Zig-Zag Graph Product, and New Constant-Degree Expanders*, Ann. Math. 155(1):157–187 (2002). https://doi.org/10.2307/3062153
3. I. Razgon, *On OBDDs for CNFs of bounded treewidth* (2013). https://arxiv.org/abs/1308.3829 (context only; rank proof above self-contained).
