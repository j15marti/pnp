# TMR-4/081: unbounded connection rank and easy T5 cactus compilation

**Model.** Source graphs are unweighted directed graphs, with R(a,b)=1 exactly when (b-a) mod 5 belongs to {1,3}. A complete canonical source parser and literal OBDD audit are in the downloadable /081 evidence package; the committed standalone Node audit below independently verifies the central integer certificate. No NP-hardness or arbitrary-machine lower bound is claimed.

## Exact candidate

Put P[l,d]=(R^l)[0,d], for lengths l=2..6 and d=0..4:

```
P = [ [0,1,1,0,2], [3,0,3,1,1], [4,4,1,6,1],
      [2,10,5,5,10], [15,7,20,7,15] ]
det R=2, det P=44.
```

For each k>=1, construct 5^k authentic directed source **trees** H_l with k+1 labeled boundary terminals r,s1,...,sk. Each H_l has a directed path r -> s_j of length l_j in {2,...,6}, private interiors disjoint. Its translation-quotiented extension signature at relative terminal colors d_j is prod_j P[l_j,d_j]. The full matrix of these signatures is M_k=P^(tensor k), with determinant 44^(k*5^(k-1)), hence full rank 5^k. In particular k=3 gives 125 independent relative counting channels on four terminals.

Gluing H_l,H_h on *all* their labeled terminals retains disjoint interiors and yields a cactus with k undirected cycles sharing one root. Its exact T5 count is

```
Z(H_l glued H_h)
  = 5 * product_j sum_d P[l_j,d]*P[h_j,d]
  = 5 * (M_k * transpose(M_k))[l,h].
```

The literal connection matrix thus has rank 5^k and determinant 5^(5^k)*44^(2*k*5^(k-1)). This lower bound concerns only exact *linear messages with bilinear composition*, not nonlinear representation, OBDD size, or deterministic time/space. It is an explicit instance of established connection-matrix theory, not a new general graph algebra result.

## Pointwise, cheap, source-authenticated compiler

Parse the actual canonical graph, discover the unique root (indegree zero, outdegree 2k), sink leaves (indegree two, outdegree zero), and 1-in/1-out internal path vertices. Verify that two internally disjoint directed root-to-sink paths cover each petal, and verify every source arc. No special labels, advice or witness of the correct order are accepted.

Query original five-valued variables in the order root, then each leaf and its two paths to completion. Each live OBDD state retains at most the root color, current leaf color, and current predecessor color: width <=125, internal nodes <=125n. All original assignments are preserved, and every early rejected transition contributes exactly 5^(unread variable count) rejected completions. The exact product count above is computed in polynomial bit time. The parser, recognizer, path enumeration, state sharing, arithmetic, and output are in the same charged realization. Conservative total O(L^4) bit time, O(L^3) writable bits for full input length L, including the output; no free preprocessing or Z5 transform is assumed.

**Fixed-order falsifier.** For k petals with both legs length two and r=0, the viable sink-leaf colors 1,2,4 yield different nonempty local residual pairs:
1 -> {(3,3)}, 2 -> {(1,1)}, 4 -> {(1,1),(1,3),(3,1),(3,3)}.
The bad order root, all leaves, then all interiors produces 3^k distinct nonzero cofactors at the leaf cut, so **every OBDD for that fixed order has width >=3^k**. Yet the preceding *different, source-derived fixed order* has width <=125 on the same inputs and Z=5*6^k. This is an order-specific separation only, not a lower bound under every order or for adaptive FBDDs.

**Boolean comparison.** 3 bits per original five-symbol value; forbid codes 5,6,7 by 3 clauses per vertex, and the 15 disallowed color pairs per original arc by 15 6-literal clauses. Thus exact parsimonious CNF has 3n Boolean variables and 3n+15m clauses, without auxiliary variables; a five-way OBDD node becomes at most seven binary internal nodes. The five-state model aids discovery of the cactus product but no intrinsic asymptotic advantage over this Boolean encoding is proved.

## Falsifiers, ledger and gates

Four falsifiers: maximal 5^k boundary rank coexists with an easy cactus source algorithm; an exponential OBDD bound for one bad order fails for a different source-aware order; 3-bit/CNF translations have constant-factor overhead; the 32 unary domain masks do not track general multi-terminal counting correlations.

SAME_REALIZATION charges canonical parsing, header bounds, graph discovery and rejected candidates, all arcs, variable ordering, active fan-out and hashing, exact early-reject multiplicities, retained states, integer bit lengths, binary encoding, CNF clauses and output. No Fourier, rounding, uncharged eviction, oracle, switch or cache assumption.

Four verification gates: (1) source recognition and malformed/valid-nonmember rejection, (2) 881875 exhaustive original assignments, 400 sampled assignments, 882275 actual valid-code CNF tests plus 1500 invalid-code checks and 13 full five-way OBDDs, (3) 16775 contracted connection entries, 9840 bad-order cofactor cases for k<=8, seven same-input good-order controls through k=64, and (4) independent Node BigInt determinants and 16275 contractions plus 600625 literal assignment checks. Two complete runs gave byte-identical Python and JS reports. Python audit SHA256 a2ecd304f6665fef119c29277ce1e7d5795f7108c733e11be98a6f8603bf8300; JS audit SHA256 d4caf3c5b348ccfb3c3a88f28d4a4e3886f9e52e0873db49ed72964cea7029bc. Zero unexpected assertions.

**Reconciliation and open dependency.** Retain /078 unary domain masks, /079 two-terminal two-orbit interface, /080 three-terminal rank-25 gadget certificate, and TMR-2's separate dynamic results. The prior **D4-T5-4CONNECTED-PRIME-DYNAMIC-TRANSFER** dependency remains OPEN: cactus sources have one-vertex separators, are readily recognized, and do not provide a hard residual family with mixed SAT/UNSAT cases. No unrestricted reverse implication or P versus NP proof. Independent mathematical review, full LaTeX compile and literal bounded-tape microsteps remain outstanding.

References: Lovasz, *Rank of connection matrices and the dimension of graph algebras*, Eur J Combin 27 (2006), https://doi.org/10.1016/j.ejc.2005.04.012; Wegener, *Branching Programs and Binary Decision Diagrams*, SIAM (2000), https://doi.org/10.1137/1.9780898719789.
