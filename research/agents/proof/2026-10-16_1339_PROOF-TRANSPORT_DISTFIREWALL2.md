# PROOF-TRANSPORT DISTFIREWALL2
2026-10-16 13:39 Asia/Seoul. Status: restricted transport, P versus NP OPEN.

Pre-search proposals: (1) randomized multioutput rectangle corruption; (2) uniform-product average-error spread lifting; (3) one-defect Tseitin distribution; (4) arbitrary-decider extraction obstruction.

Search: Oct 16 PROOF-TRANSPORT reports, ROUNDINGSQUEEZE5, PC22_ALLFIELD1 compiler versions, PADCOFINAL5, project library and Drive, and primary randomized lifting/Resolution literature.

RESULT 1. If every rectangle Q and output label a has mu(Q intersect Valid_a) <= rho mu(Q)+Delta, a c-bit public-coin protocol has mu-average success <=rho+2^c Delta. Proof: fix coins, sum over at most 2^c rectangle leaves, average.

RESULT 2. Any proper 3-CNF with nine variable-disjoint clauses has a deterministic public-output protocol solving indexed falsified-clause search on 1-(7/8)^9 > 2/3 of uniform gadget inputs, using at most 27(ceil(log2 b)+1) bits. Cubic expander Tseitin formulas have nine such clauses but arbitrarily high Resolution width. A uniform-average-error replacement of RS5 total correctness would contradict those width lower bounds. INVALID.

RESULT 3. For a connected graph G and odd Tseitin charge, each specified unique parity-defect vertex has exactly 2^(|E|-|V|+1) underlying assignments. K3,3 enumeration: 96 one-defect assignments, 16 per vertex. This suggests a hard correlated indexed distribution instead of the easy uniform distribution.

Independent local audit: 276480 exact gadget pairs; 1080000 sampled cases; 512 graph assignments; 450 rectangles; 4096 protocols; all PASS. Script and JSON stored as local artifacts.

Main bridge OPEN: arbitrary polynomial SAT decider need not emit Resolution, CP, PC/PCR, SoS, or a triangle DAG. Do not promote restricted lower bounds to runtime.
Sentinel: DISTFIREWALL2::P_VS_NP_OPEN.
