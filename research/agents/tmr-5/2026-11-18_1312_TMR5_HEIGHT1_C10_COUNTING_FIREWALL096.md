# TMR-5/096: #P-hard counting on one-level, universally SAT T5 DAGs

**Date:** November 18, 2026 (Pacific). **Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Status:** exact mathematical reduction, independently tested; external review pending. **P versus NP remains OPEN.**

## Main theorem

Let T5 have universe Z/5Z and R(x,y) iff y-x mod 5 belongs to {1,3}. Restrict T5 input digraphs D to those having a partition V=U disjoint union W with every arc directed from U to W. Such graphs have **no directed walk of length two**. Every instance is satisfiable: assign 0 to all U vertices and 1 to all W vertices.

Nevertheless, exact counting of T5 homomorphisms on this class is **#P-complete under polynomial-time Turing reductions**, even when the underlying bipartite graph has maximum degree three. The reduction requires no edge-replacement gadgets, interpolation, or subdivisions.

## Ten-cycle isomorphism

Construct the bipartite double cover B of T5, with left vertices L_x and right vertices R_y for x,y in Z/5Z, and undirected edge L_x-R_y iff y-x mod 5 belongs to {1,3}. Map its vertices into the ordinary undirected cycle C10 (integer labels modulo 10):

    phi(L_x) = 4*x mod 10
    phi(R_y) = (4*y+7) mod 10.

This is a bijection respecting the two sides. For d=y-x mod 5, the image difference phi(R_y)-phi(L_x) equals 4d+7 mod 10, which is +1 or -1 modulo 10 exactly when d belongs to {1,3}. Thus B is **isomorphic to C10**, not merely homomorphically equivalent. It is connected, has ten edges and degree two at every vertex.

## Exact source reduction and component correction

Given an undirected graph H, return zero immediately if H is not bipartite, because #Hom(H,C10)=0. Otherwise compute a bipartition independently for each connected component, orient every edge from the first side toward the second, and denote the height-one directed graph by D(H).

For each connected source component, homomorphisms into C10 map its two parts into the two target sides in one of two orientations. Rotating the target C10 by one step exchanges sides and bijects these two possibilities. The side-preserving orientation is, through the explicit phi isomorphism, equivalent to a T5 homomorphism of D(H). This remains valid for isolated vertices: C10 allows ten target labels, versus five for T5. Thus, with c(H) connected components,

    #Hom(H,C10) = 2^c(H) * #Hom(D(H),T5).

The multiplier 2^c is exactly computable in polynomial time and has polynomially many bits. One oracle query for the height-one T5 count therefore evaluates #Hom(H,C10), after a polynomial-time bipartiteness test. By the primary Dyer–Greenhill counting-homomorphism dichotomy (2000), read with its 2004 corrigendum, exact #C10 is #P-complete. The bounded-degree-three restriction in their theorem is preserved by orienting the same edges. Membership in #P follows by guessing all five-symbol labels and checking every arc.

The reduction is **not parsimonious**; the factor 2^c is explicitly paid. The restricted decision problem is identically YES, so #P hardness of counting gives **no existential machine-time lower bound** for this class.

## Independent reproduction

An executed third-party-free Python verifier established the target isomorphism on all 100 ordered target pairs, target degree/connectivity certificates, and exact identities on **594** bipartite source graphs (including isolated vertices). It independently directly enumerated both target assignment spaces for **22 small instances**, checked **all 512 graphs** with three left and three right vertices via side-enumeration, and tested **60 seeded random instances** with up to ten vertices. A separately executed compact script checked 528 exhaustive cases. All assertions passed.

Examples:
- K3,3 oriented source-to-sink: 70 T5 homomorphisms; 140 C10 homomorphisms.
- C4 oriented source-to-sink: 30 T5 homomorphisms; 60 C10 homomorphisms.
- Six isolated vertices: 15,625 T5 homomorphisms; 1,000,000 C10 homomorphisms, ratio 2^6.
- Four disjoint edges: 10,000 T5 homomorphisms; 160,000 C10 homomorphisms, ratio 2^4.

Executed full and compact verifiers and raw results are provided in the separately preserved evidence archive.

## Ranked dependency synthesis

| Arrow | Verdict |
|---|---|
| Unrestricted fixed T5 CSP is NP-complete | PROVED by Bang-Jensen–Hell–MacGillivray (1988) and checked C5 gadget |
| All height-one source-to-sink T5 instances are SAT | PROVED, explicit uniform assignment |
| Bipartite double cover B of T5 is C10 | PROVED, explicit bijective isomorphism |
| #C10 counting to height-one #T5 counting | PROVED, component-corrected Turing reduction |
| Height-one #T5 counting #P-complete | PROVED based on corrected Dyer–Greenhill primary theorem |
| #P-hard exact counting implies difficult existential decision | FALSIFIED for this class |
| Any static rank or fixed-order OBDD measure forces machine work | OPEN as a general inference; restricted counterexamples established previously |
| Representation-independent superpolynomial T5 machine lower bound | OPEN |
| Unrestricted Boolean SAT superpolynomial lower bound | OPEN |

**Next priority:** require TMR-2 and TMR-4 invariants to correctly classify these height-one DAGs as trivially satisfiable despite #P-complete exact counting, and to distinguish Boolean existence from partition-function evaluation. **P versus NP remains OPEN.**

## Primary literature

[1] M. Dyer and C. Greenhill. *The complexity of counting graph homomorphisms*. Random Structures & Algorithms 17, 260–289 (2000). https://doi.org/10.1002/1098-2418(200010/12)17:3/4<260::AID-RSA5>3.0.CO;2-W

[2] M. Dyer and C. Greenhill. *Corrigendum: The complexity of counting graph homomorphisms*. Random Structures & Algorithms 25, 346–352 (2004). https://doi.org/10.1002/rsa.20036

[3] J. Bang-Jensen, P. Hell, G. MacGillivray. *The Complexity of Colouring by Semicomplete Digraphs*. SIAM J. Discrete Math. 1, 281–298 (1988). https://doi.org/10.1137/0401029
