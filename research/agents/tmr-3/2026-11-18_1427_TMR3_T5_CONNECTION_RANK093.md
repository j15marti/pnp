# TMR-3/093: sharp T5 terminal connection rank versus polynomial SAME_REALIZATION

**Date:** 2026-11-18, America/Los_Angeles. **Agent:** TMR-3 / PNP Time-Space Tradeoffs. **Status:** proved sharp rank within linear/bilinear separator summaries; separately proved polynomial exact solver for an authenticated graph class. Neither is an unrestricted T5 machine lower bound. P versus NP remains OPEN.

## Model and sharp connection-rank theorem

Fix T5 with vertices Z5 and R(a,b) iff b-a in {1,3} modulo 5. A q-boundaried directed graph is a graph with q distinct labeled terminals t_0,...,t_(q-1). For each such H define f_H(alpha) as its number of valid original-vertex T5 assignments with terminal colors (0,alpha_1,...,alpha_(q-1)), alpha in Z5^(q-1). Under gluing along all q terminals, with private vertices otherwise disjoint,

    Z(H union_T K)=5 sum_alpha f_H(alpha) f_K(alpha).

**Theorem (sharp rank).** The full q-terminal connection matrix M_q(H,K)=Z(H union_T K), over all q-boundaried directed source graphs and over Q, has rank EXACTLY 5^(q-1).

**Proof.** Simultaneous translation of every color gives the displayed factorization, hence rank at most 5^(q-1). For the reverse inequality consider the unit increment source U(u,v;w) with genuine arcs (u,v), (u,w), (w,v). The number of colors of private w for fixed a=x_u and b=x_v is

    R(a,b)*sum_{z in Z5} R(a,z)R(z,b)=1[b-a = 1 mod 5].

Indeed the only allowed z when b=a+1 is z=a+3. Thus U forces an increment +1 with exactly ONE internal completion per admissible terminal pair. Compose d copies in series for d=1,2,3,4, or five copies for d=0, yielding a source path P_d with endpoint matrix 1[b-a=d], exact integer entries 0/1 and polynomial size. For each alpha form B_alpha by joining a private P_(alpha_i) between t_0 and t_i for every i=1,...,q-1. Each boundary profile f_(B_alpha) is the Kronecker delta at alpha. Consequently

    M_q(B_alpha,B_beta) = 5 * 1[alpha=beta].

The 5^(q-1) by 5^(q-1) submatrix is 5I, so rank at least 5^(q-1). QED.

**Scope:** any linear map to d rational coordinates followed by a fixed bilinear gluing pairing must have d >= 5^(q-1). This is a lower bound for that representation model, NOT for arbitrary algorithms, encoding lengths, nonlinear messages, same-machine time, or memory. It is a constructive T5 instance of the connection-matrix framework of Lovasz (2006).

## Counterexample: maximum interface rank but easy graphs

The union of any number of B_alpha sources is constructed entirely from unit increment triangles. More generally, authenticate an unlabelled input source as follows: identify private vertices w with exactly one in-arc u->w and one out-arc w->v, with direct arc u->v. Require that no selected w is an endpoint of another selected triangle, and every original edge belongs to one of those triangles. Retain the direct arcs, each encoding x_v-x_u=1 modulo 5. Traverse the resulting graph with potential-color BFS. Contradictory cycles yield Z=0. For consistent constraints, each connected component can be shifted by five choices and every removed w has one forced color, hence Z=5^c. Actual source arcs are checked; no supplied annotations or boundary patterns are assumed.

On adjacency-list RAM input the recognizer and solver take polynomial time and space, O(N^2) time and O(N) words with conservative implementations. One explicit deterministic one-tape implementation has deliberately loose simultaneous upper bounds

    T(N)=O((N+1)^8),  S_peak(N)=O((N+1)^3) bits

for recognized members, including graph access, scans, source checking, addresses, modular propagation, exact arithmetic and output. If recognition fails, use correct original-arc backtracking, with O(poly(N)*5^n) time and polynomial space. No polynomial general T5 bound is asserted.

Each B_alpha union B_beta is a series-parallel graph (undirected treewidth at most two), although the connection-matrix rank across the q labeled terminals is exactly 5^(q-1). At q=40, rank is 1,818,989,403,545,856,475,830,078,125; one consistent authenticated union has n=430, m=694, and Z=5. A single different coordinate yields exact Z=0. Therefore the exponential rank is not a necessary-time or necessary-space lower bound for these sources.

## Executed computational checks

Standard-library Python reference: 622 deterministic assertions, zero failures, exact integer arithmetic, repeated execution yielding byte-identical audit JSON. Verified unit triangle's full 5x5 matrix, ten matrix powers, all 25 glued 2-terminal pairs against an independent general domain-filtering/backtracking T5 solver, 25 diagonal 3-terminal and 60 random 3-terminal pairs, 75 random 4-terminal pairs, 100 random small original graphs against 5^n brute force, nonmember and inconsistent source controls, and q=40 source verification. SHA256 of reference code: e1324d9d3e4b066cd3c8c38151a4d33cfb1ca2e54e0b8cce2f041d715c30d669. SHA256 of audit JSON: f220045551bce86122226ad9a87b4786729d1eb321f40d5f4cc87bbaa377b85f. Finite checks remain COMPUTATIONAL. Full native TM execution, independent formal review, and compilation of the full combined manuscript remain outstanding.

## Four proof gates and controls

1. DISJ sanity: PASS only for constructive restricted claims; unrestricted lower bound OPEN.
2. Relativization: not applicable to claimed P vs NP separation, since no such separation is claimed.
3. SAME_REALIZATION: PASS restricted positive simultaneous time/space upper bound; representation rank is not transferred to DTISP.
4. Configuration counting: rank theorem proved for linear/bilinear separator representation only; cannot imply same-machine work lower bound.

Controls: isolated nodes, plain arcs, directed trees and cycles, opposed arcs, loops, equality/increment affine components, SAT and UNSAT unions, treewidth <=2, brute-force original graph counts, primal/dual and Fourier opportunities, articulation/terminal formulas, and arbitrary unrecognized fallback.

**Next dependency:** C3-T5-NONLINEAR-CONNECTION094. Search for authenticated 3-connected or high-adhesion sources with no low-degree gadget interiors where the full interface rank persists *and* no small nonlinear source summary is apparent. Quantify preprocessing versus direct SAT on one identical machine. Never infer P != NP from rank alone.

**References:** [1] Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J Discrete Math 1(3), 281-298 (1988), DOI 10.1137/0401029. This gives NP-completeness of general T5 because T5 is a tournament with more than one directed cycle, not a quantitative transferred SAT time bound. [2] L. Lovasz, *The Rank of Connection Matrices and the Dimension of Graph Algebras*, Eur J Combin 27 (2006) 962-970, DOI 10.1016/j.ejc.2005.04.012.
