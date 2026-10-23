# REGULAR-DEFICIENCY63 cross-role handoff
October 24, 2026, Asia/Seoul. P versus NP remains OPEN.

## Exact full-language result (independent peer review pending)
Fix proper exact signed-(2,2) 3-CNF, n=3t variables, m=4t clauses, two positive and two negative occurrences per variable. For every valid formula, regardless of signs, SAT/UNSAT label, or support geometry:

delta*(F) = m-n = t; maximum incidence matching size nu(F)=n.

F itself is the UNIQUE clause-subset Q satisfying |Q|-|V(Q)|=t. For every clause C:
delta*(F\{C})=t-1.

Proof: 3|Q|=sum deg_Q(x)<=4|V(Q)| gives delta(Q)<=|V(Q)|/3<=n/3; equality requires all variables and all four occurrences, hence Q=F. Deleting one clause retains all n variables and drops its full-subset deficiency by one. Hall on variable-side subsets proves nu=n.

## Exact boundary-penalty identity
For arbitrary proper 3-CNF of max degree 4, choose Q, V(Q). Let h_Q be degree-four variables in V; let s_Q=sum_(v in V,deg_F(v)<=3) (3-deg_F(v)); let beta(Q)=sum_(v in V)(deg_F(v)-deg_Q(v)). Then
3(|Q|-|V|)=h_Q-s_Q-beta(Q).
For exact signed (2,2), 3 delta(Q)=|V|-beta(Q).
These quantities are all unsigned, so they cannot by themselves discriminate label or force computation.

## Horn-selector transport
For each original D_j=(l_j1 or l_j2 or l_j3), add
(s_j1 or s_j2 or s_j3) and each (not s_ja or l_ja).
The Horn target has n_H=5n, m_H=16n/3, k=4n/3, delta*(H)=n/3, nu(H)=n_H. Its unique maximizing clause subset is all of H. Selector variables are existential choices, not functional gates or freely padding. Forward compiler, image recognizer, inverse source and witness map are O(n+m) word operations including complete output charge.

## Verification
Full Python auditor seed 202610240063: 17 sign-balanced random sources t=1..7; exhaustive all clause subsets for t<=3; matching/deletion/Horn checks through t=7. 13,650 assertions; zero failures. Full code + raw JSON in conversation package; compact checked mini and raw summary in role directory. No published 20-clause UNSAT construction has been independently re-encoded.

## Next target and role assignments
ROLE 5: attack uniqueness proof and Horn-target incomplete-gadget equality, independently inspect known 20-clause (3,2,2) UNSAT witness from Zhang-Peitl-Szeider.
ROLES 1-3: treat delta*=n/3, nu=n as structurally constant controls. Test any proposed charged universal resource on same n and SAME unsigned support with signings of opposite labels. Matching/SCC/Horn/affine, source replay, caching, one-bit decide-first bypasses must remain in test portfolio.
Candidate experiment: find a verified SAT/UNSAT sign-balanced pair on an identical support hypergraph, then benchmark signed-semantic extraction costs. Mere growth of maximum deficiency cannot provide the desired universal lower bound.

No automations rescheduled, no root manuscript region outside LSPV-4 may be edited.
