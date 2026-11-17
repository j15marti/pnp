# CROSS-TRACK T5-TRANSFER-RANK46 | 2026-11-17 14:55 PST
Status: PROVED/EXACT restricted algebraic theorem; finite audit COMPUTATIONAL; external peer review OPEN. P versus NP remains OPEN.

PRE-SEARCH COMBINATIONS: (1) private path SAT saturation versus exact-count cofactor; (2) TMR-2/069 local high-girth path consistency versus final semantic-zero rank; (3) WRAPPER/UWI versus source-aware shortcuts and same-final-input witnesses; (4) path elimination versus encoding-specific proof transport.

SOURCES: Historical four specialists (Resource Contraction, Nonrelativizing Simulation, Universal Obstruction, Proof Transport) through latest retrievable cross-track reports, current TMR-2/069, TMR-4/069-070, TMR-3/049, TMR-5/057, Google Drive KRYLOVGUARD41, current Library and project-chat records, Bang-Jensen/Hell/MacGillivray 1988, Lovasz 2006, Focke/Marx/Rzazewski 2024. No other agents' files or schedules changed.

THEOREM TR46: For the T5 beat tournament R(a,b)=1 iff (b-a mod5) in {1,3}, an L-edge oriented path with p forward and q reverse edges has exact endpoint-color count transfer M=A^p(A^T)^q. A and A^T are circulant, commute and have determinant 2, so det M=2^L over integers. Rank is five over Q or any odd-characteristic field; rank four over GF2 for L>=1. For L>=4 all 25 entries are positive, so deleting *private* path interiors and the constraints they carry is SAT-preserving. But it is NOT #Hom preserving or even universally multiplicative.

NATIVE CONTEXT COUNTEREXAMPLE: all-forward length-four path has row 0 [4,4,1,6,1]. Without other constraints, free endpoint core has 25 assignments and augmented core 80. With native edge u->v, core has 10 and augmented graph 50. Ratios 16/5 versus 5 differ. Therefore no scalar counting substitution can be correct for all native graph contexts.

SOURCE-AWARE SHORTCUT: A and A^T commute. After complete paid source parsing, the direction sequence need only retain the counts p,q (O(log L) bits). Full M can be recomputed from these, despite rank five. A free isolated path has exactly 5*2^L assignments. Full-rank boundary data is NOT a general computation lower bound. TMR-2/069's globally UNSAT LPS graph has globally zero semantic cofactor despite nontrivial local transfer, another firewall.

AUDIT: Python standard library; 2,046 complete orientation patterns length 1..10, 2,046 exact Bareiss det checks, 2,046 GF2-rank checks, 50,800 saturation-entry checks, 1,550 independently enumerated endpoint counts, 96 source-graph contexts, 2,048 semigroup checks including length-1000 path, and controls. 70,865 recorded checks, zero failures. Local verified script t5_transfer_rank46_audit.py, results 2026-11-17_T5_TRANSFER_RANK46_results.json, report 2026-11-17_1455_CROSS_TRACK_T5_TRANSFER_RANK46.md; full report SHA256 5ef1481d07a8bc9a29128914a7d20cdc39a6bdbbe6ceffe1679c5d840aa5c680.

DAG: T5 NP-completeness ESTABLISHED; T5 4-edge SAT saturation PREVIOUSLY PROVED; exact oriented transfer and det/rank PROVED RESTRICTED; uniform counting multiplier FALSIFIED; source-aware p,q compression PROVED RESTRICTED; actual proof-system lower-bound transport CONDITIONAL/NOT SUPPLIED; arbitrary-decider fully charged hereditary contraction OPEN; correctness-forced nonrelativizing WRAPPER OPEN; common-clock same-input UWI OPEN; P!=NP OPEN.

ASSIGNMENTS: Resource Contraction: implement full source-authenticated weighted path contraction with parsers/counters/recursion charged and test cyclic/reconvergent cores. Nonrelativizing Simulation: delayed status-changing challenge with precompute, source and oracle replay controls. Universal Obstruction: one identical final SAT graph and clock, include private-path witness reconstruction. Proof Transport: field/encoding-specific proof certificate transport through path suppression and counterexamples first.

NEXT SINGLE DEPENDENCY: a nontrivial source-authenticated hereditary contraction on cyclic/reconvergent T5 cores with all costs charged; no unrestricted lower bound inferred.

READBACK_MARKER::T5_TRANSFER_RANK46_P_VS_NP_OPEN