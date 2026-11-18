# T5-FORK-DUALITY59 | 2026-11-18

P versus NP remains OPEN.

Old rule: F(a,b,c)=R(a,b) & R(a,c).
New rule: S(a,b,c)=R(a,c) & R(b,c).
T5 relation R(a,b) iff (b-a) mod 5 is 1 or 3.

## Proven isomorphism
R(-b,-a)=R(a,b), so F(a,b,c)=S(-b,-c,-a). Rotate each ternary tuple (u,v,w) to (v,w,u) and globally negate all colors. This induces a solution-count-preserving bijection between the old and new ternary CSP instance families. Both languages are NP-complete via the original binary T5 CSP: replace each arc R(u,v) by F(u,v,t) or S(u,t,v) with a fresh private variable t.

## Shared-neighbor matrix
K(a,b)=sum_c R(a,c)R(b,c)=A A^T=A^T A. Its first row is [2,0,1,1,0], determinant 4. The possible child count is 2 when a=b, 1 when (b-a) mod 5 is 2 or 3, zero otherwise. Thus with distinct compatible attackers the child is forced.

## Distinct effects on the same ordered tuples
- (a,b,c) and (a,c,b): old 20 solutions, new 0.
- (a,b,c) and (b,a,c): old 0, new 20.
- (a,b,c) and (a,b,d): old 40, new 30.
- For r distinct outputs z_i in (a,b,z_i): old 10*2^r, new 5*2^r+10.

## Exact audit
Exhaustively enumerated all subsets of 1..4 ordered distinct-variable triples on four named variables: 12,950 formulas. SAT decisions differ in 2,116 paired same-order formulas; aggregate satisfiable-formula counts are identical for each subset size. Additional 3,200 six-variable random formulas: 409 paired disagreements. Zero test failures. Reproducible Python and data: local research bundle T5_Fork_Duality_2026-11-18.zip.

## Proof DAG and future work
ESTABLISHED: binary T5 CSP NP-complete (Bang-Jensen, Hell, MacGillivray, SIAM J Discrete Math, 1988, DOI 10.1137/0401029).
PROVED restricted: fork isomorphism, exact K matrix and motifs.
FALSIFIED: reversing the fork direction intrinsically increases unrestricted worst-case complexity or preserves SAT on the same ordered instances.
OPEN: unrestricted T5 time lower bound, fully charged resource contractor, necessary nonrelativizing WRAPPER hinge, same-input UWI obstruction, general arbitrary-decider proof-system transport.

Next: investigate role-restricted hypergraphs and overlaps after quotienting by fork duality; test source-aware shortcuts before positing lower bounds.