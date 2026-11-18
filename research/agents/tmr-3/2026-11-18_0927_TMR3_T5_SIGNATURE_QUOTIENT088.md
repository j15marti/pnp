# TMR-3/088: signature-quotient exact counting on oriented complete bipartite sources

Owner: TMR-3 / PNP Time-Space Tradeoffs. November 18, 2026, America/Los_Angeles.
Status: PROVED restricted exact counting upper bound with finite computational audit; no general lower bound. P vs NP OPEN.

## Model and recognition

The fixed target tournament T5 is Z5 with R(x,y) iff y-x in {1,3} mod 5. A source digraph is recognized as an orientation of K_{p,q} (p,q>=1) only after checking the ENTIRE arc set: vertices, lack of loops/opposed and duplicate arcs, bipartition, connectedness, all pq cross-pairs present and no within-part arcs. Nonmembers retain exact exponential brute-force fallback. No graph oracle or supplied decomposition is assumed.

## Theorem A: necessary signature budget

For u in U define its binary orientation signature (1[u->v]) indexed by all v in V. For v in V define (1[v->u]) indexed by all u in U. Let a and b count distinct signatures in U and V. If two vertices on the same side have different signatures, a witness on the opposite side sees them in opposite directions. They therefore cannot be assigned the same T5 color because T5 is antisymmetric. Two vertices on opposite sides likewise cannot share a color because they are adjacent. Consequently one representative from each signature class must occupy a distinct color:

  a + b <= 5 is NECESSARY for a T5 homomorphism.

If a+b>5, exact coloring count is ZERO. In the other case, min(a,b)<=2 because both sides are nonempty. This is a source-specific obstruction, not an unrestricted algorithm.

## Theorem B: support-sum identity and 45-orbit algorithm

Choose a side A with at most two signature classes C_i, sizes m_i and representatives u_i. For any original coloring, let S_i be the EXACT set of colors used on class C_i. Since all arcs between one class and any opposite vertex v have the same direction, and each T5 color has exactly two in-neighbors and two out-neighbors, |S_i| can only be 1 or 2 in a valid coloring.

Define h_m(S)=1 for singleton S, and h_m(S)=2^m-2 for |S|=2, counting all assignments of the m labeled source vertices onto S. For each opposite vertex v define

  c_v(S_1,...,S_a)
   = number of colors y in Z5 for which, for every i and x in S_i,
     R(x,y) holds if u_i->v, otherwise R(y,x) holds.

Then EXACT original-vertex count, with no omitted twin multiplicities, is

  Z(G) = SUM_{S_i subset Z5, 1<=|S_i|<=2}
             PROD_i h_{m_i}(S_i) * PROD_{v in B} c_v(S).

Partition colorings by their class supports. Given these supports, all B vertices choose their colors independently, giving the product of c_v; h counts the original labeled assignments on A. This proves the formula.

There are 15 allowable nonempty supports per class. Simultaneous translation by d in Z5 preserves all constraints and all summands. Every one- or two-element support has orbit length exactly 5, since Z5 has prime order. Therefore the sum reduces to 15^a/5 at most 3 cases if a=1, or 45 cases if a=2; multiply each representative term by five. All arithmetic is exact integers.

## Theorem C: simultaneous deterministic same-machine bounds

For encoded input length N, a single blank-start deterministic sequential-tape realization parses and authenticates the graph, forms the signature classes, checks a+b, enumerates at most 45 support orbits, evaluates all c_v with explicit graph access, computes integer powers and products, and outputs the full integer answer. With conservative overcharging for head travel, input/adjacency access, signature comparisons, state, arithmetic bit length, indexing and output, one simultaneous upper bound on recognized Kpq sources is:

  T(N) = O((N+1)^8),
  S_peak(N) = O((N+1)^3) bits.

The output has at most O(N) bits because Z<=5^n; all intermediate sums are nonnegative and at most constant times 5^n. The explicit incidence representation uses polynomial memory. Both limits refer to the SAME sequential machine, not different time-optimized and space-optimized realizations. Native microcode was NOT executed; these are symbolic conservative implementation bounds. The exact fallback for nonmembers has O(poly(N)5^n) time and polynomial space.

## High-treewidth SAT and UNSAT controls

An all-forward orientation of K_{p,q}, with every arc U->V, has the closed-form exact count

  Z(K_{p,q}^{U->V}) = 5 (2^p + 2^q - 2).

Proof: on the U side, the five singleton supports each permit two V colors, contributing 5*2^q. Exactly five two-color support sets have one common T5 out-neighbor; each contributes 2^p-2. Larger supports impossible. At p=q=1000 the original source has 2,000 vertices, one million arcs, treewidth 1000, and a 303-digit exact count. All vertices have degree 1000. Large width and lack of private (1,1) paths are therefore not necessary-work certificates.

For an UNSAT control orient K_{3,3} by u_i->v_j iff i=j and v_j->u_i otherwise. The source is bipartite, 3-regular, has 6 vertices and 9 arcs, has no private (1,1) paths, and has THREE distinct signatures on EACH side. Thus a+b=6>5 and Z=0, confirmed independently by brute force. This disproves using source chromatic number <=5 as a sufficient condition for T5 solvability. Since it contains a small forbidden subsource, the example remains deliberately easy; it is NOT a certified difficult family.

## Actual execution and evidence

The full local independent-reference implementation completed 1,236 deterministic assertions with zero failures, twice with byte-identical output. Coverage: every orientation of Kpq for pq<=6, 400 seeded random Kpq instances compared with original-vertex brute force, identity K3,3 UNSAT, uniform all-forward examples through K1000, analytic counts, malformed/nonmember rejection and alternative two-signature families. The separately authored compact published executable passed 610 self-contained exhaustive checks and 200 additional independent cross-implementation random checks. These are FINITE COMPUTATIONAL observations, not a proof of an unrestricted theorem.

Published: experiments/tmr/tmr3_t5_signature_quotient088_repo.py. The full executed source, compact source, report and raw audit are also supplied as one reproducibility ZIP in this run. The existing main3 manuscript is appended, not replaced, and agent identity/title/ownership/schedule/safeguards remain unchanged.

Four gates: DISJ sanity PASS restricted constructive upper; relativization NOT APPLICABLE to nonseparation; same-machine DTISP PASS restricted symbolic simultaneous upper, no lower; configuration counting upper-bound consistency only, no necessity. Preserve forest/treewidth, SAT/UNSAT, affine, degree-two, twin/module, cyclic Fourier, chromatic, padding, and all alternative-algorithm controls. /341 full UNSAT FAIL, /386 RESTRICTED. No quantitative SAT time-space exponent follows from the NP-completeness classification without auditing a concrete reduction's blowup.

Next: C3-T5-SIGNATURE-PERTURB089. Study h omitted cross edges in near-complete bipartite sources. Test whether the signature injection proof survives: it may FAIL when the witnessing cross arc is absent. Develop a charged exact correction, preferably parameterized in h, rather than assuming the quotient remains valid.

Reference: Bang-Jensen, Hell and MacGillivray, The Complexity of Colouring by Semicomplete Digraphs, SIAM J Discrete Math 1(3) (1988), 281-298, https://doi.org/10.1137/0401029. Their classification confirms general T5 NP-completeness. P versus NP OPEN.
