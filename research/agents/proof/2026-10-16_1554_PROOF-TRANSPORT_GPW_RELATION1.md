# PROOF-TRANSPORT GPW-RELATION1
2026-10-16 15:54 Asia/Seoul. Restricted transport established; P versus NP OPEN.

## Proposals recorded before search
(1) General-relation randomized GPW lifting for Tseitin falsified-clause search. (2) Party-local exact-(2,2) compiler and index-gadget transport. (3) SAT self-reducibility as an arbitrary-decider interface, attacked. (4) ROUNDINGSQUEEZE5 triangle-DAG scope audit.

## Sources inspected
Recent DEFECTCOMP1, DISTFIREWALL2, ORDEPTH_ORACLE1, SPLITRECT_INDEXFRONT1 chats; GitHub ROUNDINGSQUEEZE5, RS5REVIEW1, PC22_ALLFIELD1, ALLFIELD22, and historical source compiler; Google Drive SIL-PR-20260918-PROOF-007 and LBO3SAT priorities; Göös-Pitassi-Watson, Query-to-Communication Lifting for BPP, SIAM J. Comput. 2020 (Section 2 applies to arbitrary search relations), and Göös-Pitassi, Communication Lower Bounds via Critical Block Sensitivity, SIAM J. Comput. 2018.

## Theorem and proof
Fix connected cubic expander G_n with n vertices, m=3n/2 edge variables, constant edge expansion and odd Tseitin charge. The source Tseitin CNF F has 4n clauses. The original occurrence-halving compiler H=C(F) has N=24m=36n variables and M=32m=48n clauses, exact-(2,2), proper, distinct signed 3-CNF; encoded length Theta(n log n). The canonical extension Phi sets four clones of each edge variable equal and all Q-padding variables zero. For EVERY source assignment z, the set of false clauses of H(Phi(z)) is exactly the transformed source false-clause set.

Let pi map target variables to their source index or 0. Given source Alice index pointers a_i and Bob index tables y_i, lift each clone locally to pointer a_pi(j) and table y_pi(j), while auxiliary variables receive fixed pointer 1 and all-zero table. Then IND_b^N(a',y')=Phi(IND_b^m(a,y)), identically for all a,y. The two parties do not communicate during this embedding. Every public-output protocol for target false-clause search therefore induces a protocol of identical cost and error for source false-clause search. This is a valid restriction of the FULL target communication input domain.

DEFECTCOMP1 shows randomized source decision trees need Omega(n) edge-bit queries, using the correlated single-defect distribution and expansion. GPW's general-relation theorem with index table b=m^256 converts any c-bit source protocol with error <=1/3 into O(c/log m) source queries with error <=1/3+o(1), giving c=Omega(n log n). The local embedding transfers this to the SAME H. Alice sending all N pointers and Bob returning N indexed bits plus a false-clause label costs O(n log n). Thus target randomized indexed-search communication is Theta(n log n)=Theta(encoded formula length).

## Hostile checks
The GPW theorem simulates randomized transcript distributions; it does not fix one seed globally, so RAND-SEEDFIREWALL1 does not block it. The correlated source distribution is used only to establish a worst-case query bound, not as an invalid uniform-product corruption claim. A protocol lower bound does not give a lower bound for unrestricted triangle DAGs. Full-scan polynomial communication already matches this bound, and an arbitrary polynomial-time SAT decider need not emit any proof or search protocol.

Finite audit: 12,496 indexed input pairs, 434,880 actual target-bit equality checks, 4,736 full source-assignment search identities across K4, K3,3 and Q3, with deliberately corrupted clone/auxiliary mappings rejected. Python: proof_transport_gpw_relation_audit.py; JSON: proof_transport_gpw_relation_audit.json. Finite checks do not prove GPW asymptotics.

Compiler distinction: historical balanced 24m/32m; all-input selector 72q/96q; compiled OR shield 144q/192q. Syntactic integer CP and its depth bounds, field-dependent PC/PCR, real SoS, strict Resolution and spread-budget triangle DAGs remain separate models. In particular, Tseitin is not the separate all-field PC/PCR-hard family.

## Handoff
Closed: source randomized query to same-realization target randomized communication. Not closed: arbitrary-decider to a structure with superpolynomial unconditional lower bounds. Next bridge must be nonrelativizing, program-dependent and fully charged.

References: https://eccc.weizmann.ac.il/report/2017/053/ ; https://doi.org/10.1137/16M1082007
GPW-RELATION1::P_VS_NP_OPEN