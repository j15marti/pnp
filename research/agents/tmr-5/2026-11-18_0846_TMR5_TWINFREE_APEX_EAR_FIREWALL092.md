# TMR-5/092: twin-free, 2-connected high-treewidth T5 instances with polynomial exact counting

**Owner:** TMR-5 Machine Bottleneck Redteam. **Date:** 2026-11-18 Pacific. **Scope:** exact restricted theorem, independent executable validation. **P versus NP remains OPEN.**

## Source problem and primary-theorem gate

The fixed target is the loopless tournament T5 with R(a,b) iff (b-a) mod 5 is in {1,3}. The semicomplete-digraph theorem of Bang-Jensen, Hell, and MacGillivray (1988, DOI 10.1137/0401029) classifies this particular fixed-template CSP as NP-complete: T5 contains multiple distinct directed triangles. NP-completeness does **not** imply an unconditional deterministic superpolynomial lower bound.

## 2-connected, twin-free augmentation of TMR-5/091

For s,t >=3 let G+ and G- be the oriented complete-bipartite K_(s,t) pair with row-0 and column-0 clones of the respective seeds:

    YES 001 / 001 / 110
    NO  001 / 010 / 101

A 1 means L_i -> U_j, 0 means U_j -> L_i. The two cores differ in four reversed arcs and preserve each individual vertex's in/out degree. The YES core has exactly 5(2^(s-1)+2^(t-1)) T5 assignments. The NO core has an explicit unsatisfiable six-arc oriented K_(2,3). These facts were independently rechecked.

Add two hubs h_L,h_R, with a native arc h_L -> h_R. For each left core vertex v insert a fresh directed length-four path

    v -> p(v,1) -> p(v,2) -> p(v,3) -> h_L

and analogously for each right core vertex with endpoint h_R. Call the augmented instances H+ and H-. All arcs remain actual T5 constraints with no fixed labels.

**Exact graph invariants, for both H+ and H-:**

- N=4(s+t)+2 vertices; M=st+4(s+t)+1 arcs; cycle rank r=st.
- Identical labeled undirected graphs and identical directed in/out degree for *each* corresponding vertex; exactly four original arcs reversed.
- Underlying bipartite and 2-vertex-connected graph, minimum degree two, with treewidth at least min(s,t) because it contains K_(s,t).
- No identical incoming/outgoing neighborhood signatures at distinct vertices: every vertex is its own false-twin class, hence raw twin-class count kappa=N.

2-connectivity follows from the core being 2-connected, and each private length-four ear joining its core endpoint to one of two hubs; each hub has at least three ears. Deleting a core vertex, hub, or ear-internal vertex leaves every remaining ear fragment attached to the still-connected core/hubs. No leaf elimination, articulation decomposition, or direct bounded-raw-twin quotient applies.

## Exact transfer and counting theorem

Let A be the 5-by-5 T5 adjacency matrix. For a directed ear of length four, summing its three private labels gives the transfer matrix W=A^4. In row 0,

    W[0,:]=[4,4,1,6,1]

and all other rows are its cyclic shifts. **All 25 entries are positive.** Hence any satisfying core assignment extends for any of the ten allowed hub-color pairs; the NO core remains unsatisfiable. Thus Z(H+)>0, while Z(H-)=0 for all s,t>=3.

There is an exact polynomial-time counting algorithm on both entire families, using only generally recognizable graph operations. Suppress degree-two private directed paths, recording their constant-domain (5-by-5) transfer matrices. Enumerate both hub colors, at most 25 possibilities. After their values are fixed, each original core vertex has a unary weight w_v(a)=W[a,h_L] or W[a,h_R]. The remaining core has at most six false-twin classes C_i, with identical unary weights within each class.

For a nonempty color support S and class size n, define the weighted surjection sum

    U_C(S)=sum_(T subseteq S) (-1)^(|S|-|T|) (sum_(a in T)w_C(a))^n.

Enumerate the 31 possible nonempty supports for each class, reject assignments where a required core class-to-class arc fails for any pair of support colors, and multiply U_C across classes. Summing over allowed hub pairs yields the **exact** count. Complexity: O(10*31^kappa * poly(N,M)) arithmetic operations, with kappa<=6 *after path suppression and hub elimination*. Integer bit length is O(N).

This is a genuine fixed-parameter exact-counting algorithm for the recognizable class of native T5 cores with a bounded set of hubs, degree-two internal paths to hubs, and bounded false-twin quotient after elimination. The published verifier uses the explicitly constructed source partition; a fully automatic recognizer for the larger class is not included. No polynomial algorithm for general T5-CSP is asserted.

## Independent reproduction

The full self-contained verifier was executed twice with byte-identical result output and no failed assertions. It checks all 3,125 assignments of the earlier C5-to-T5 five-arc gadget; all 25 ear endpoint pairs with independent direct enumeration of all 125 private triples; eight core/augmented pairs through (s,t)=(20,23); degree identity, exact arc switch, bipartiteness, absence of articulations and twins; 200 arbitrary relabelings; and independent exhaustive small-core assignment enumeration with ten hub choices for (3,3),(3,4),(4,3),(4,4). The run recorded 3,678 grouped checks.

| s,t | N | M | Raw twin classes | #Hom(H+,T5) | #Hom(H-,T5) |
|---|---:|---:|---:|---:|---:|
| 3,3 | 26 | 34 | 26 | 194,960 | 0 |
| 3,4 | 30 | 41 | 30 | 1,054,160 | 0 |
| 4,4 | 34 | 49 | 34 | 5,042,000 | 0 |
| 9,11 | 82 | 180 | 82 | 15,996,955,470,691,280 | 0 |
| 20,23 | 174 | 633 | 174 | 58,572,445,949,923,639,974,502,263,808,246,160 | 0 |

The exact results are proved symbolically; experiments are reproducibility checks, not a substitute. The extended raw ZIP has the complete independently executed script and JSON. Formal proof-kernel certification, full LaTeX compilation and external mathematics review are outstanding.

## Ranked dependency status

| Arrow or inference | Status |
|---|---|
| Specific T5 homomorphism NP-complete | **PROVED**, primary semicomplete-digraph theorem |
| Four-reversal degree-preserving Kst pair | **PROVED**, restricted |
| Twin-free 2-vertex-connected bipartite high-treewidth augmentation | **PROVED**, restricted |
| Exact length-four transfer and weighted-support counting | **PROVED**, restricted |
| Growing treewidth, cycle rank, raw twin number, 2-connectivity and no leaves force hard *individual* instances | **FALSIFIED** as an inference |
| Any particular OBDD/FBDD/tensor measure implies unavoidable arbitrary-machine work | **OPEN**, and must survive direct path elimination |
| TMR-2/TMR-4 invariant to representation-independent time/space lower bound | **OPEN** |
| Superpolynomial Boolean SAT time lower bound | **OPEN** |
| P versus NP | **OPEN** |

**Next test:** any proposed machine-resource invariant must remain valid after exact 5x5 path-transfer compression, bounded-hub conditioning, and weighted false-twin quotienting, not merely raw graph simplification.

**Primary reference:** Bang-Jensen, J., Hell, P., & MacGillivray, G. *The Complexity of Colouring by Semicomplete Digraphs.* SIAM J. Discrete Math. 1(3):281-298 (1988). https://doi.org/10.1137/0401029
