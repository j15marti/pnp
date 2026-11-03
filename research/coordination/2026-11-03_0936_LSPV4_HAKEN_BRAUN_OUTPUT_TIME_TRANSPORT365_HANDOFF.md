# LSPV-4 handoff: Haken / Braun explicit-output cost and B3 firewall (November 3, 2026, 09:36 PST)

**PROVED/EXACT, a corollary of Haken (1985) and Cook (1976):** An explicit-output algorithm translating any short authentic Rmix341 refutation of unary PHP(h+1,h) into an ordinary DAG-Resolution refutation of the same source requires at least exp(Omega(h)) output steps. The input has N=Theta(h^3 log h) ASCII bits, so the lower bound is exp(Omega((N/log N)^(1/3))). This is a proof-format-converter lower bound, not unrestricted SAT time or space.

**CONDITIONAL external Braun preprint (arXiv:2609.23015):** wide BPHP has Res(XOR) refutations with >exp(n/(32768 ell^2)) nodes, n=2^ell, ell>=32. The same source has short mixed ER proofs as already established in LSPV-3 BPHP343. Since encoded bit length is N=Theta(n^3 ell^2), an explicit reverse Res(XOR) proof writer would take exp(Omega(N^(1/3)/(log N)^(8/3))) time, assuming the published theorem. The Lean kernel was not replayed here.

**No novelty claim:** Logical reverse-proof nonprojection was previously proved in LSPV-2 HAKEN-ER2-NONPROJECTION364 and LSPV-5 REFEREE299; this audit makes its output-time and exact ASCII bit-length charges explicit. It does not prove a growing mixed lower bound or B1, B2 or B3.

**Independent folder review:** Actual root GROKPROOF/ reports 2026-11-03_1217/1518_PROGRESS.md, Claude reports research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex and 0939_CLAUDE_DIRECTPRODUCT-0001.tex. Grok's query-volume lemma incorrectly derives a per-query lower bound from an algorithmic upper bound; Claude's arguments are restricted to sequential-access or particular portfolios. Neither supplies B3.

**Finite controls:** Python full producer and separate no-import Node verifier tested 494 clause-deletion SAT witnesses, 2250 single-sign-flip SAT witnesses, 12 source-encoding checks, 5 small UNSAT enumeration controls, 10 malformed-DIMACS rejections, and odd/even K4 Tseitin (0/8 models). Independent Node passed 3322 assertions. Full reproducibility package is attached to the run, with source, raw JSON, report and SHA-256 manifest. The GitHub compact verifier is an additional, narrower code artifact: 327 assertions.

**Resource ledger:** Host RSS ~109196 KiB is not FLMV space. Sequential output work does not impose writable-space lower bounds. All-phase rho includes parsing, source/index/head access, proof generation, conversion and any allocate-then-free materialization. T_A^wc(N) in B2 maximizes over all binary inputs including malformed; B3 remains SAT in P => polynomial worst-case minimum for this same fixed Rmix341.

**Next:** obtain a genuine lower-bound-preserving transfer covering every mixed rule and separately a nonrelativizing B3. Preserve all five task identities, enabled states and schedules. P versus NP OPEN.
