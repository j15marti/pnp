# TMR-3/070: Directed-twin quotient for the five-symbol beat CSP

**Date:** 2026-11-17 14:24 Pacific. **Owner:** TMR-3 / PNP Time-Space Tradeoffs. **Status:** PROVED/EXACT within the stated exact counting model, external mathematical review OPEN; finite test evidence COMPUTATIONAL. **P versus NP OPEN.**

## Candidate, falsifiers, and end-to-end chain

Named dependency **C3-T5-CORE-QUOTIENT** from TMR-3/069. Input is an authenticated finite directed graph G on n explicitly declared vertices, with every arc specified in the source. The template is R(a,b) iff (b-a) mod 5 belongs to {1,3}. Output is the exact nonnegative integer Z(G)=#Hom(G,T5), and YES iff Z>0. Duplicate identical arcs are deleted; loops and opposing arcs force count 0. Malformed words reject as INVALID, not as a mathematical UNSAT certificate.

Before reviewing original sources, falsifiers were (F1) equality of the in/out neighborhood signatures does not yield an independent complete-bipartite twin partition; (F2) a 2x2 complete R biclique exists and invalidates the two-color-per-type restriction; (F3) the onto-color weight 2^m-2 double counts or loses original vertex assignments; and (F4) large integer values, class identification or adaptive physical access require uncharged storage/time.

**Pipeline:** original binary graph word -> parse and normalize -> construct exact in/out neighborhood signatures and discover independent twin classes -> certify quotient's complete directed connections -> iterate at most 15 supports per nonisolated class -> exact onto-assignment weights -> integer answer and YES/NO. This is one blank-start, single-machine algorithm, not a free quotient oracle.

## Theorem C3-T5-INDEPENDENT-TWINS

Let the equivalence relation on vertices be u~v iff their complete OUT-neighborhood sets and IN-neighborhood sets agree. After rejecting loops/opposed arcs, this relation partitions G into independent classes C_i, and for any two distinct classes the arcs between them are either absent or form a complete bipartite set in one fixed direction. Let n_0 be the number of isolated vertices, q the number of nonisolated classes, and m_i=|C_i|. Let Q be the quotient oriented graph.

For a nonisolated class C_i, write S_i for the nonempty subset of T5 colors actually used by its original vertices. Define
```
A_i(S) = number of onto maps C_i -> S
       = 1                         if |S|=1,
       = 2^(m_i)-2                 if |S|=2,
       = 0                         if |S|>2 is imposed on a nonisolated class.
```
Then the following is an EXACT count, with no overcounted original colorings:
```
Z(G)=5^(n_0) *
  sum_{S_1,...,S_q subset Z5, 1<=|S_i|<=2}
     [for every i->j in Q, S_i x S_j subset R] *
     product_i A_i(S_i).
```
In particular there is a blank-start, source-authenticated locally headed deterministic multitape exact counter with
```
T(N)=O((N+1)^8 * (1+15^q)),  S_peak(N)=O((N+1)^3) writable bits
```
under the canonical binary format declaring n,m in unary, so N>=n+m. If q=O(log N), this is polynomial-time and polynomial-space. More generally, the same source-derived method selector that retains /068 forest/cycle and /069 degree-two algorithms obtains
```
T(N)=(N+1)^O(1) (1+ min{2^(n-c),5^r,5^h,15^q}),
S_peak(N)=(N+1)^O(1).
```
Here c is the number of weak components, r=m-n+c after normalization, h the number of degree>=3 vertices in the 2-core, and q the number of nonisolated independent twin classes. For invalid or immediately impossible source words, the algorithm outputs INVALID or count zero respectively in polynomial time.

### Proof of class partition

If u and v have equal out/in-neighborhood sets, u and v cannot be adjacent: if u->v, then v is in N+(u) but not N+(v), because there are no self-loops. Equality of signatures is an equivalence relation. If one u in C_i points to v in C_j, identical outgoing neighborhoods imply every u' in C_i points to v; identical incoming neighborhoods imply every v' in C_j receives arcs from all u'. Hence C_i x C_j is complete and uniformly oriented. Identical signatures guarantee no internal arcs. Isolated vertices have empty signatures and can be removed together, with factor 5 per ORIGINAL isolated vertex.

### Proof of the support-size bound

Every color a in T5 has exactly two outneighbors and two inneighbors. If a nonisolated class C_i has an incoming neighbor class C_j, every symbol in S_i must be an outneighbor of every symbol in S_j, so for any b in S_j, S_i lies in the two-element outneighbor set of b. If C_i has an outgoing neighbor, S_i lies in the two-element inneighbor set of any symbol in S_j. Thus |S_i|<=2 in every satisfying original assignment. In addition, for any two distinct a,a' in T5, their outneighbor sets intersect in at most one element (directly check N+(x)={x+1,x+3} mod5). Hence an oriented quotient edge cannot connect two classes BOTH using 2 colors. In other words the pair-support classes form an independent set in the quotient's undirected support. This optional pruning improves real execution but is not needed for the 15^q envelope.

For a fixed support singleton, all m_i vertices must have its one color, giving one assignment. For a fixed two-element support, the 2^(m_i) binary color assignments lose exactly the two constant-color assignments, giving 2^(m_i)-2. Every original assignment determines one support tuple and exactly one independent choice in each class. Since quotient arcs are complete, it satisfies the source iff every cross-product S_i x S_j follows R. Sum over the disjoint support tuples to obtain the formula.

### Same-realization physical time and space ledger

A direct source reader validates unary counts and every binary endpoint, normalizes duplicate arcs and checks self/opposed arcs, builds two n-by-n adjacency bit arrays, compares every ordered pair of full n-bit neighborhood signatures and forms the quotient in O((N+1)^6) locally headed bit operations (conservative bound). Each class has size <=n. Store at most n classes, q^2 quotient adjacency bits, q support masks of 5 bits, and 15 q exact nonnegative weights; each weight and every intermediate result has O(n) bits, because every partial product counts assignments to disjoint classes and every accumulated sum counts a disjoint subset of original assignments. Isolated count and final answer have at most ceil(n log_2 5)+1 bits. All live data and physical head/counter positions consume O((N+1)^3) writable bits including parsed-source buffers. Enumerate at most 15^q tuples; each checks q^2 quotient edges and multiplies at most q O(n)-bit weights, using charged original-graph access, indexing, per-bit arithmetic and output. A full scan implementation on fixed locally headed tapes fits O((N+1)^8) steps per tuple, including precomputation and unsuccessful candidates. No implicit RAM unit-cost table or uncharged physical checkpoint is used.

The original /068 and /069 branches remain legal, and selection costs at most a polynomial in N. The selector computes integer exponent bounds explicitly and executes only ONE chosen algorithm, so these are simultaneous time and peak space for the same realization, not minima of separate time/space accomplishments. This is only an algorithmic upper bound; representation size is not a lower bound on arbitrary solver work.

### Dense degree-three-core witness and exact closed form

For every a,b >=1 orient all edges of K_(a,b) from its a-vertex part to its b-vertex part. Its independent twin quotient has q=2 regardless of a,b. For a,b>=3 every vertex lies in the degree>=3 2-core, so h=a+b, while the cycle rank r=ab-a-b+1 increases rapidly.

Either all a source vertices use one color (5 choices) and then the b sink colors each have two choices, or all b sink vertices use one color and the a source colors each have two choices. These cases overlap on exactly ten constant ordered color pairs following R. Thus:
```
#Hom(K_(a,b) directed left->right,T5)
 = 5*2^b + 5*2^a - 10
 = 5(2^a+2^b-2).
```
For K_(120,120), q=2 despite h=240 and r=14161. The exact count is 13292279957849158729038070602803445750. The quotient algorithm takes polynomial bit time in its true input length, contrasting exponential worst-case iterations for the older parameter bounds. This does not disprove NP-completeness or show a general subexponential bound.

## Original sources and connection to other tracks

Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3):281-298 (1988), DOI 10.1137/0401029, prove the H-colouring dichotomy for semicomplete targets. T5 has more than one directed triangle; its general CSP is NP-complete. This is a known decision classification, not a quantitative same-space SAT lower-bound transfer. TMR-1/072 separately gives a parsimonious undirected-C5 to directed-T5 gadget with n_T=n_C+2m_C and m_T=4m_C, but SAT->C5 encoded-size and workspace budgets must independently be provided before transferring precise SAT DTISP exponents. A source reduction using Theta(n) writable workspace may already violate a sublinear-space transfer even if its output has linear length.

## Computational evidence, exactly as executed

Self-contained CPython 3.13.5 source, revision `tmr3-t5-directed-twins-070-v1`, seed 202611171424, tested locally TWICE with byte-identical output. Total 1091 cases, zero errors: 761 complete simple-oriented graphs on at most four vertices, 280 randomized general digraphs with loops/duplicate/opposite arcs, 36 small complete-bipartite checks with reversal, 4 large dense blowups, 7 malformed parser controls, 1 valid source parser control, 2 complete checks of the 15 supports and absence of two-by-two R bicliques. Every small exact count was compared against independent brute-force 5^n enumeration. Code SHA256 0a51744d9efd4ac1ef7a1713c16f0e8df4264126fcdf9abfb7daaabb8a52f7d2. Raw SHA256 1d12710d772ffd8925ffa940fdb6341093252f10ee77847e4716d8857b4fc9ea.

Files: `experiments/tmr/tmr3_t5_twin_070.py` (intended repository publication; local original /mnt/data/tmr3_t5_twin_070.py) and `results/raw/tmr/2026-11-17_1424_TMR3_T5_TWIN070_PY_RAW.json` (local original /mnt/data/tmr3_t5_twin_070_raw.json). Local repository checkout failed because github.com name resolution is unavailable. Repository preflight and native physical machine microcode were NOT run. Independent external mathematical review OPEN.

## Four required gates and safeguards

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS RESTRICTED: constructive count upper bounds, no static-rank/mass-to-general-work claim. Dense bicliques with huge cycle rank are easy. |
| Relativization | NOT APPLICABLE WITH REASON: no claimed complexity separation; BGS, algebrization and Natural Proofs audits would be required for an NP-level claim. |
| Simultaneous DTISP | PASS for one selected upper-bound machine; lower-bound SAT transfer and forbidden-region inclusion OPEN. Physical preprocessing and all searches are in the same T,S ledger. |
| Configuration counting | PASS as an upper-bound consistency check only: polynomial working space allows exponential configurations; it does not force exponential time and gives no quantum/randomized result. |

All source/easy controls remain admitted: empty/isolated components, loops and antiparallel rejection, duplicate arcs, exact count versus decision, fixed-template rotations, Horn/2-SAT and affine source classes, treewidth, equality, autarky, product, padding, auxiliary, selector, unique solution, field/basis variants, other compact DP, cached sharing and recomputation. Historical /341 FAIL as full UNSAT authority and /386 RESTRICTED. P versus NP OPEN.

**ONE next load-bearing lemma: C3-T5-MODULE-BEYOND-TWINS.** Construct and charge an exact quotient for source-recognizable modules with internal arcs or nonuniform external interfaces, and show a genuine gain beyond independent twins while retaining exact original homomorphism counting and the full physical ledger. Do not infer a necessary runtime lower bound from quotient size.
