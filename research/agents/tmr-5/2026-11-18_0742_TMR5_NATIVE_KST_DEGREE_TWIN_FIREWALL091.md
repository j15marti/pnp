# TMR-5/091: four-arc degree-preserving SAT/UNSAT switch in native T5 bicliques

**Owner:** TMR-5, PNP Machine Bottleneck Redteam. **Date:** 2026-11-18, Pacific. **Status:** exact symbolic theorem with independent executable checks. P versus NP OPEN.

## Primary-theorem gate

The target is the loopless tournament on Z5 with R(a,b) iff (b-a) mod 5 belongs to {1,3}. It contains the distinct directed triangles 0->1->2->0 and 0->3->4->0. The Bang-Jensen, Hell and MacGillivray semicomplete-digraph dichotomy (1988, DOI 10.1137/0401029) therefore proves NP-completeness for this exact fixed-template homomorphism problem. The Barto-Kozik-Niven no-source/no-sink dichotomy (2009, DOI 10.1137/070708093) independently corroborates this. Neither paper proves a deterministic superpolynomial running-time lower bound.

## Theorem: four flipped arcs, unchanged vertex degrees, opposite satisfiability

For s,t >= 3, use the underlying undirected K_{s,t}, with left vertices L_0,...,L_(s-1) and right vertices U_0,...,U_(t-1). A matrix bit 1 denotes L_i->U_j, and bit 0 denotes U_j->L_i. Start from these 3x3 orientation matrices:

    YES:   0 0 1      NO:   0 0 1
           0 0 1            0 1 0
           1 1 0            1 0 1

For i>=3 clone row 0; for j>=3 clone column 0, with the shared (0,0) entry defining every new/new arc. The matrices differ at exactly (1,1),(1,2),(2,1),(2,2). Row sums and column sums of the seeds are each (1,1,2); the first row and column are identical across seeds. Hence every corresponding *labeled individual vertex* has the same indegree and outdegree, including the clones, in both families.

For both inputs: n=s+t, m=st, maximum degree max(s,t), no undirected triangles, cycle rank (s-1)(t-1), and underlying treewidth exactly min(s,t), unbounded as both dimensions grow. Both are native T5 instances with no pins or reduction gadgets and both contain directed 4-cycles. Their exact counts are

    #Hom(G^+_(s,t), T5) = 5(2^(s-1) + 2^(t-1)),
    #Hom(G^-_(s,t), T5) = 0.

## Direct UNSAT certificate

The two left rows L_0 and L_1 of the NO instance together with U_0,U_1,U_2 realize the three two-bit patterns 00,01,10, where a bit is the direction left->right. If both left colors agree, mixed patterns are impossible. If they differ, rotation symmetry sets the first color x=0 and the second to d in {1,2,3,4}. The sets of possible (R(x,z),R(d,z)) for right colors z distinct from x and d are:

    d=1: {01,10}
    d=2: {00,10,11}
    d=3: {00,01,11}
    d=4: {01,10}.

No set contains 00,01,10 simultaneously. Thus the induced oriented K_(2,3) is UNSAT. This is an unconditional finite combinatorial certificate for every NO instance. An independent exhaustive test found that deleting any one of its six arcs restores satisfiability.

## Direct positive exact-count proof

In YES, all left vertices other than L_2 form one false-twin class A of size p=s-1; all right vertices other than U_2 form one class B of size q=t-1. Write x=L_2 and y=U_2. The orientations are y->x->B->A->y. Choose x arbitrarily (five possibilities); y->x permits exactly two y labels. Rotate x to 0. For y=2, B all 1 permits one A assignment, B all 3 permits 2^p A assignments, and B using both labels gives (2^q-2) assignments with A forced. The subtotal is 2^p+2^q-1. For y=4, B all 3 and A all 1 is the only solution. Thus the total is 5(2^p+2^q).

## Generic source-independent false-twin compression

Partition any loopless oriented instance by equality of full incoming and outgoing neighborhood signatures. Vertices in each class are nonadjacent, and relations between classes are uniform. With kappa classes C_i and nonempty color-support sets S_i subseteq Z5, exact counting has the universal identity

    Z(G) = SUM over nonempty S_1,...,S_kappa:
               1[every class-pair arc holds for every symbol pair]
               PRODUCT_i onto(|C_i|, |S_i|),

where onto(n,j)=sum_(h=0)^j (-1)^(j-h) binom(j,h) h^n. It gives O(31^kappa poly(n)) arithmetic operations with polynomial-bit-length integers. For bipartite orientations, enumerate supports only on the left classes and independently count legal right-class colors, yielding O(31^(kappa_left) poly(n)) arithmetic operations.

These paired families have respectively 4 and 6 total false-twin classes; hence their exact counts are computable in polynomial time as their treewidth and cycle rank diverge. A five-valued ordered decision diagram in **any vertex-variable order** may store only the observed color support (including empty) of each class and a rejection state: width at most 32^kappa+1, independent of n. This is a uniform structural quotient algorithm, not prior recognition of the seed, and is a strong countercontrol to structural and representation-only lower bounds.

## Reproduction and scope

Independent standard-library verifier:
- all 3125 private assignments and 25 endpoint cases of TMR-1's five-arc gadget, exact unique extension iff endpoint difference is {1,4};
- the K_(2,3) obstruction and six single-arc deletion controls;
- 12 YES/NO size pairs through (101,103), checking identical per-vertex degrees, exactly four flipped arcs, correct twin-type counts, and exact formulas;
- 320 randomly relabeled source instances, bipartition rediscovery, and generic twin counting;
- distinct complete backtracking and left-side elimination counters on small instances;
- a separately executed compact verifier checking five size pairs.

All assertions passed. Exact identities have symbolic proofs; external review and proof-kernel certification remain OPEN. The full run evidence includes source, JSON results, standard output, and mathematical report.

## Ranked dependencies

| Proposed dependency | Verdict |
|---|---|
| Exact T5 fixed-template CSP complexity | **PROVED** NP-complete by primary theorem |
| TMR-1 five-arc undirected-C5 gadget | **PROVED, scoped**, rechecked all private assignments |
| Native four-arc degree-preserving Kst YES/NO switch | **PROVED**, scoped infinite family |
| Generic false-twin exact-count algorithm | **PROVED** parameterized algorithm |
| Identical underlying graph, degrees, treewidth, cycle rank determine satisfiability | **FALSIFIED** |
| High treewidth or high cycle rank implies expensive individual instances | **FALSIFIED** as an instancewise inference |
| Fixed-order OBDD/tensor complexity entails arbitrary-machine work | **OPEN**, naive inference disproved by /090 |
| Representation-independent worst-case superpolynomial T5 lower bound | **OPEN** |
| General Boolean SAT superpolynomial deterministic lower bound | **OPEN** |
| P versus NP | **OPEN** |

**Next audit gate:** apply twin-quotient preprocessing and degree-preserving four-arc switches to TMR-2/TMR-4 candidate resource invariants. Demand a lower bound that holds against all source-aware algorithms, variable orders, adaptive decompositions and algebraic methods.

**Primary references.** [1] Bang-Jensen J, Hell P, MacGillivray G. *The Complexity of Colouring by Semicomplete Digraphs*. SIAM J Discrete Math. 1988;1(3):281-298. https://doi.org/10.1137/0401029. [2] Barto L, Kozik M, Niven T. *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*. SIAM J Comput. 2009;38(5):1782-1802. https://doi.org/10.1137/070708093.

All agent titles/identities, schedules, owners, peer manuscripts, safeguards and unmerged PR state remain unchanged.
