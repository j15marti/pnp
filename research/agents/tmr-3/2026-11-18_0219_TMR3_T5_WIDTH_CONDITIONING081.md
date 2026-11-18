# TMR-3/081: source-conditioned width, exact five-state elimination, and the nonclique wheel

**Checkpoint:** November 18, 2026, 02:19 America/Los_Angeles. **Owner:** TMR-3 / PNP Time-Space Tradeoffs. **Status:** restricted, source-to-output constructive result; independently reproducible finite audit. **P versus NP OPEN.** The existing identity, title, ownership, hourly schedule, enabled state, and safeguards are unchanged.

## Model and exact preprocessing lemma

The source is an explicitly encoded finite directed graph G=(V,E). Label colors by Z5 and require y-x in {1,3} mod 5 for each arc x -> y. Input source length N explicitly declares vertices and arcs so that n,m <= N. Repeated arcs are idempotent; a loop or opposed pair certifies zero.

Every **original terminal sink** z with outdegree zero and indegree d<=3 can be eliminated without changing the original-coloring count if replaced by a factor on its parent vertices:

    W_z(a_1,...,a_d)=sum_{q in Z5} product_{i=1}^d [q-a_i in {1,3} mod 5].

For d=0 this factor is the constant 5. For 1<=d<=3 its values are in {0,1,2}. One factor must be retained per original sink, including duplicate parent sets. Arcs among surviving vertices remain directed Boolean-valued factors. Thus Z(G) is exactly the sum over remaining vertex colors of the product of these factors, times constants from isolated sinks. The factor graph (primal) puts a clique on each scope, of size <=3 for contracted sinks. This is exact for arbitrary G, not only the pure hub/sink subclass, and all recognition and factor tables are computed from the authenticated source.

All factors are invariant under adding one common element of Z5 to all variables in a connected primal component. For each nonempty component fix the least-numbered surviving vertex to zero, multiply the resulting conditioned answer by 5, and sum no alternative anchor colors. This is a bijection with unrestricted assignments and prevents counting each orbit five times.

## Theorem: width-budget conditioned variable elimination on one physical machine

Build the primal graph after authentic source contraction. Fix one canonical anchor per connected component. Given a nonnegative width budget b, deterministically add variables to a conditioning set C, chosen by greatest current primal degree (ties by source index), until the **explicitly simulated min-fill elimination order** of the remaining primal graph has induced width at most b. No optimal tree decomposition, minimum cutset, or oracle is assumed.

Let c be the number of nonempty primal components, k=|C|, and l=k-c (the freely enumerated conditioning colors). For each of the 5^l choices, substitute the C colors into every factor and eliminate surviving variables in the certified order. Each eliminated variable has at most b surviving neighbors; construct each new table by streaming over the 5^b neighbor assignments and the five values for that eliminated variable. Every original and generated factor is counted once in its elimination bucket. Multiply residual constants, sum the 5^l cases and restore the factor 5^c and isolated-sink constants.

One fixed deterministic single-tape realization with sequential table storage, explicit head motion and table lookup scans has conservative simultaneous bounds

    T(N) = O((N+1)^16 [1 + 5^(l+2b+5)]),
    S_peak(N) = O((N+1)^6 [1 + 5^b]) writable bits.

These deliberately include the potentially O(5^b) physical head travel **per factor-table lookup**. The more optimistic O(poly(N) 5^(l+b+1)) is a RAM-operation count, **not** claimed as a single-tape physical bound. The space term counts all factor entries, values with O(N) bits, the actual source, pointers, cutset, elimination order, and output. Source authentication, failed cutset/ordering proposals, preprocessing, 5-ary states, propagation, caching, recomputation and printing are included. The same implementation realizes both bounds. The bound is valid for every legal input in terms of the source-produced l,b, but need not be polynomial if either grows with input length.

An independently available fallback enumerates the 2^(n-c_original) forest bits as in TMR-3/068 using polynomial space. This is an alternative algorithm, not a claimed simultaneous running-time/space improvement without choosing it. A Boolean CSP would have 2^b table dependence; this template has 5^b, but spanning-forest choices here are binary because each oriented edge allows exactly two of five values.

## Infinite nonclique-separator countercontrol: sink wheel W_r

For r>=5 create one central hub h, rim hubs v_0,...,v_(r-1) and private sinks z_0,...,z_(r-1), with arcs h->z_i, v_i->z_i, v_(i+1 mod r)->z_i. The source has n=2r+1 original vertices, 3r arcs, r+1 surviving hub variables and r original ternary factors. Its primal is the wheel with r-cycle rim and universal center, of treewidth 3.

**There are no clique separators of size 1, 2, or 3.** If h is not deleted, the remaining wheel is connected through h. If h is deleted along with at most two other vertices that form a clique, the deleted rim vertices must be adjacent, leaving a connected rim path. Thus the previous clique-only recursion /080 cannot split an unbounded wheel.

The global strong-two-cover for all source sink triples is 1+ceil(r/2). If h is chosen, one must choose a vertex cover of the rim cycle. If h is omitted, both endpoints of every rim edge must be chosen, hence all r rim vertices. Consequently the older global strong-two-cover bound is exponential in r.

For h fixed to color 0, a rim color must lie in {0,2,3}. A sink factor on adjacent rim colors has 3-by-3 transfer matrix

    M = [[2,1,1],[1,1,0],[1,0,1]].

Its eigenvalues are 3,1,0. Closing the rim gives the **original-coloring** formula

    Z(W_r) = 5 tr(M^r) = 5(3^r+1)  for r>=4.

The actual width algorithm anchors h=0, conditions on one rim vertex (l=1), and eliminates the remaining rim path at width b=1. Thus its general worst-case single-tape bound is polynomial on this family, even as the global strong-two-cover and the number of original sinks grow. At r=80: n=161 original vertices, m=240 arcs, k=2, c=1, l=1, b=1, only **5** conditioned evaluations, and the 39-digit count

    739044147071729616580416051031916488010.

This is a rigorous counterexample to *global strong-cover size* and *clique-only separability* being universal obstructions to polynomial exact counting, not a complexity lower bound.

## Executed verification and controls

The Python 3 standard-library implementation was executed in the local container. **350 deterministic assertions passed, zero failures**:
- all 64 loop-free digraphs on three named vertices, including opposed arcs, tested under b=0,1,2 (192 checks), against an independent original-vertex DFS counter;
- 45 random digraphs of at most seven vertices with duplicate arcs, loops, opposed arcs and isolates, under b=0,1,2 (135 checks), independently cross-checked;
- wheels r=4,5 under b=0,1,2,3 compared against original-vertex DFS, independent transfer-matrix powers and formula (8 checks);
- wheels r=6,7,10,20,40,80 under b=1,2 against independent transfer powers and formula (12 checks);
- 3 malformed-source tests.
The complete locally executed source SHA-256 is `14e62e26bbf9bdd43416310d7fb64291bd8321ba7944900d0814f3c3e321ed74`; audit JSON SHA-256 is `4a01e7447acdd316a98fd1ff9cc7f41bb2b4ccff984110a724b10f771fbe447d`. A separate reproducibility package retains the exact source and raw JSON output.

**Four verification gates.** DISJ sanity: PASS restricted, not an all-input lower bound. Relativization/algebrization/natural proofs: NOT APPLICABLE as a separation; no lower bound imported. Simultaneous DTISP: PASS for the stated constructive same-realization upper bound, including physical table access, not merely a RAM time claim. Configuration counting: PASS as upper-bound consistency only; no resource lower bound. Other easy-family controls remain preserved: affine/Horn, bounded width, degree two, twins/modules, padding/selector, cycle rank, caching/recomputation, uncharged preprocessing, and representations with artificially large width.

## SAT transfer guardrail

Bang-Jensen, Hell and MacGillivray (1988) prove the NP-completeness classification for semicomplete targets with more than one directed cycle. The given T5 is a tournament containing the two directed triangles (0,1,2) and (0,3,4). This establishes qualitative NP-completeness, **not** a concrete SAT-to-T5 reduction of a specified linear blowup. If a separately verified reduction sends an n-variable SAT source to T5 sources of size at most an+O(1), then a T5 upper time 2^(alpha N) would give SAT time 2^((a alpha)n+o(n)) after accounting for the reduction. Conversely an independently established SAT lower exponent delta under compatible space limits would force alpha>=delta/a, only if the composition respects those limits. There is no such claimed unconditional exponent here.

References: [1] Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 1988, DOI 10.1137/0401029. [2] Bodlaender, *A Linear-Time Algorithm for Finding Tree-Decompositions of Small Treewidth*, SIAM J. Comput. 25(6), 1996, DOI 10.1137/S0097539793251219. [3] Korhonen and Lokshtanov, *An Improved Parameterized Algorithm for Treewidth*, arXiv:2211.07154, 2022. These are prior-art citations, not proof of a novel general treewidth algorithm.

**Next load-bearing target:** `C3-T5-SYMMETRY-AWARE-BAG082`, derive when all difference-invariant boundary factors can be represented by 5^(w-1) orbit states without breaking symmetry under conditioning and whether this gives an asymptotic source-derived tradeoff. Independent proof review, native TM microcode and full manuscript compilation remain open. No unrestricted same-machine time-space lower bound is proved. **P versus NP OPEN.**
