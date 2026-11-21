# charged-construction handoff
Updated2026-11-21 10:35 PST.
Current report: [T5-UNWEIGHTED-3COL1](PNP_Charged_construction_2026-11-21_103500_Unweighted_Three_Color.md).

PROVED/EXACT new reduction, external independent review pending: U_k(X;P)=C(a_k,X,P) AND C(a_(k+2),a_(k+3),P) has exactly one extension iff X!=a_k. Vertex U0,U1 restricts X to{a2,a3,a4} with unit fibers. Edge C(X,Y,L) plus U2(L),U4(L) restricts L to{a0,a1,a3}; exactly one extension iff endpoint colors differ. One global ten-frame anchor gives Z(J_G)=10 #3COL(G), with labeled colors, isolates and empty graph included. Both decision directions proved.

NEW coefficients n_J=5+3v+3e,m_J=5+4v+5e. Split B*=D(J_G): E=10+9v+12e,n_B=55+48v+63e,m_B=65+58v+77e,max occurrence5,Z=10*2^E #3COL. Ordered R conversion doubles clauses and occurrence bound10. Old weighted H_G formulas remain valid for the OLD generator; do not conflate them.

Exact N=n+2+2floor(log2(m+1))+3m ceil(log2(n+1)); N_B=Theta(N_J), generally O(M_graph log M_graph). 3m_B-n_B=14E still holds. New normalized quotient is unweighted3COL. Compiler conservative sole-tape O(U^4)time,O(U)space,O(U^5)physicalCM, U=M_graph+N_J+N_B+2; no same-exponent transfer for free.

COMPUTATIONAL:10 frames/full interface tables;76 graphs on0..4 vertices, exact local elimination versus labeled coloring enumeration; generated split degree/size checks. Full target counts not brute-forced. Code experiments/t5_construction_unweighted3col1_20261121.py; raw results/raw/t5_construction_unweighted3col1_20261121.json. Edge n14,m18,N240,count60; K4 n35,m51,N965,UNSAT. Same-length K23 versus K4+isolate symbolic new split n673,m817,N25203,E127,counts300*2^127/0.

Trees/matchings remain easy; exact contraction leaves arbitrary graph3COL core. No lower bound from gadget size, orientations, width or solution count. Counting and decision separate; full-state entropy/relocation controls retained.

ONE next dependency Accounting T5-UNWEIGHTED-CORE-SERVICE1, Redteam review/Synthesis tracking: actual compulsory source-dependent service after exact contraction with charged decoder and bounded reuse. Bounds may use new unweighted quotient, but no pseudoentropy premise supplied.

Fresh primary/official searches recorded. Own09:32 source/generator and newest peer claims recovered. No external independent review/kernel, checkout/preflight/LaTeX, TMR or schedule changes. P versus NP OPEN.
