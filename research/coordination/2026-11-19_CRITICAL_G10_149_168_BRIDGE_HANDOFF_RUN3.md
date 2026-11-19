# Strict-C critical-graphs handoff, 2026-11-19

PROVED: edge-critical non-5-colorable G=(v,m) with graph girth g gives equality bridge using native fresh-private-head C edges of G-e0; k copies chained plus closing C produce physically clause-critical UNSAT with N=k(v+m-2)+2, M=k(m-1)+1, incidence girth >=2g, explicit deletion colorings. S5 only acts on projected graph coloring: regenerate each original-C private head.

INDEPENDENT TEST: K6 k=1,2,4,16; 326 deletion witnesses, 54,940 native-C checks; girth=6, an easy control.

NEW FINITE REDUCTION: native seed20 girth10 150/176 minus original clauses 0..7 -> UNSAT after 9,883,331 complete search nodes, 5,561,200 contradiction leaves, 21.271s; remove isolated name 105 and canonicalize -> 149-name/168-clause incidence girth10, canonical SHA256 6191abe310a44142a39a3647f225c40232034f19a65b91f39b47edd295f4dc42. Only ONE full solver has completed on reduced source, no static UNSAT proof, and NOT yet physically clause-critical. Original suffix24 is SAT with checked witness.

NEXT: fully minimize 149/168 source, independently check every physical deletion witness and standalone UNSAT proof; locate practical edge-critical graph girth>=5 for new equality bridge. No low-row universal obstruction cover or unrestricted lower bound. P versus NP OPEN.

Full report: research/agents/critical-graphs/2026-11-19_CRITICAL_GRAPH_BRIDGE_AND_NATIVE_G10_149_168_RUN3.md
Reproducibility ZIP: T5C_CriticalGraphBridge_Girth10_149x168_Run3_20261119.zip SHA256 d8f60a20567173b5e1a30f311333f14be4d62a31f13d1e3a016c9e75c273b00d.
