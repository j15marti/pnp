# LSPV-4/398: Restricted 2-CNF certificate resource calibration
**2026-11-04 16:36 PST. Status PROVED/EXACT (2-CNF and ordinary Resolution), COMPUTATIONAL for finite controls. General B1/B2/B3 and P versus NP OPEN.**

IDEA: Derive uniform, source-authenticated proof-DAG upper bounds using implication paths with all construction, indexing, and verification charged. Falsifiers included unit-clause pivot failure, claiming optimality from chosen BFS paths, invalid SAT certificates, and uncharged space.

SEARCH: controlling five-role 2026-11-02_1204 handoff, issue #3, Grok 2026-11-04_1617, Claude TPORT/ONETAPE, LSPV-4/393 and REFEREE347. Aspvall/Plass/Tarjan (1979) give the SCC 2-SAT method; Buresh-Oppenheim/Mitchell (2006) explain why implication shortest paths do not necessarily minimize Resolution proofs. OpenAI GitHub search found no relevant proof compiler. No direct Google-branded search.

ITERATE: Fixed R_mix341 contains strict binary RES. Every nonempty-clause UNSAT 2-CNF on n>=1 appearing variables has a source-authenticated Resolution refutation with at most 4n-3 paid nodes. Two simple mutual reachability paths, each at most 2n-1 edges, derive complementary units in at most k-1 resolutions apiece, followed by one final resolution. An internal unit implication short-circuits a path by yielding the required unit directly. This is an upper bound on W_R only for the 2-CNF sublanguage, not a minimum or all-SAT B3.

Exact hostile control: Exhaust all 256 signed 2-variable 2-CNFs. There are 95 SAT and 161 UNSAT, and in 41 of the UNSAT cases the first-conflicting-variable BFS construction uses more nodes than an independently exhaustive minimum Resolution derivation. Source {-x,y,-y,x or y} needs one node, whereas the implementation uses two. Selecting the better of the two variables removes these gaps for this finite domain only. Full R_mix341 minima could be even shorter.

Resource ledger: original signed input N bits; indexed adjacency/source IDs, BFS frontier, failed choices, source rereads, emission and certificate checking give conservative O(N^3) native work, O(N log N) all-phase peak writable bits, O(n log N) serialized derived proof bits. This is not a square-root-space FLMV construction: rho near 1. No proof discovery cost was imputed to the ideal lower-bound relaxation.

Producer Python 1280 random sources, 2420 assertion groups, 11 malformed rejections, K4 odd/even parity models 0/8. Separate JS 1280 cases, 642 SAT / 638 UNSAT, 1918 checks, eight malformed rejections. Independent JS readback referee: 64 stored cases, 219 checks. Seeds and complete local artifact bundle retained.

Hardness control: Haken's 1985 exponential theorem is for ordinary unrestricted shared-DAG Resolution on unary pigeonhole CNF with bit encoding Theta(h^3 log h), not mixed R or machine time. Cook's Extended Resolution PHP constructions supply a polynomial escape. The 2CNF construction is a restricted upper bound, not superpolynomial hardness.

Published paths:
research/agents/lspv-4/2026-11-04_1636_LSPV-4_2CNF_PATH_CERT_RESOURCE398.tex
experiments/arc/lspv4_398_2sat_certificate.js
results/raw/arc/2026-11-04_1636_LSPV4_398_2SAT_PATH_CERT_RESOURCE.json

Next: apply the same fully authenticated derivation and bit-length ledger to a genuine nonaffine established hard family without accidentally assuming a polynomial backtranslation or a decider-to-refutation compiler. B3 for same fixed R_mix341 remains OPEN. No task or rule changes.
