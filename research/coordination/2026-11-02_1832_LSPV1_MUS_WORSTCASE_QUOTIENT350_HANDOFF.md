# LSPV-1 MUS-WORSTCASE-QUOTIENT350 five-role handoff | 2026-11-02 18:32 PST

USER-APPROVED WORST-CASE W_R + WEAKEST SUFFICIENT B3 unchanged. No role/state/task/schedule changes. Proof calculus stays exactly unit-weight binary-premise Rmix341 with RES/AND3/XOR/LOCAL-CONVERT/charged conservative VARDEF. Input is a fixed explicit signed DIMACS-like clause list, with deletion and dense variable reindexing not increasing encoded bit length.

PROVED/EXACT: for every bit budget N, Wbar_R(N) is exactly attained on some clause-minimally UNSAT formula, hence also on one of its signed-isomorphism orbits, indexed by the orbit's minimum encoded bit length. Reason: choose a minimum UNSAT core, replay its optimal R proof on the source superset, and compact the core without growing encoding. The quotient is mathematical, NOT an algorithmic core extractor, and is inapplicable to source-dependent clock rules or encodings with deletion penalties.

PROVED/EXACT: if mu(F) is the cardinality of a minimum UNSAT source core, then mu(F)-1 <= W_Rmix341(F) <= 3^(mu(F)-1). Lower is prior source-ancestry; upper uses Tarsi's classical v<=mu-1 for minimally UNSAT CNFs, plus resolution completeness and <=3^v distinct clauses. Hence W_R(F)>C(N+1)^k requires mu(F)>1+log_3(C)+k log_3(N+1). A candidate with small core cannot be proof-hard in this fixed calculus, but large core alone is far from sufficient: even odd cubic Tseitin, Horn chains and blockers have short proofs. This is the new combined exact worst-case MUS reduction and parameterized candidate screen, not a new generic complexity separation or claim of academic novelty.

COMPUTATIONAL: all 512 distinct-clause subsets on two variables, 417 UNSAT and 95 SAT, of which 12 are MUS. The minimum-core frequency is 256/112/48/1 for mu=1/2/3/4. Using already-established <=3-var optimum W=mu-1, the full versus MUS-only maximum agrees at every one of 59 byte budgets 0..58. Independent no-import JS enumeration passed 1,731 assertions; four malformed-input controls rejected; short SAT vs UNSAT and empty-core controls passed. No full arbitrary mixed-DAG optimizer was run.

LSPV-1: Keep weakest B3 and general encoded worst-case as active load-bearing arrow; explicitly localize B3 to MUS orbits for a mathematical proof target without asserting efficient enumeration. Pursue any directly justified conditional reflection theorem, not P=NP yielding an unspecified proof system.

LSPV-2: Apply signed-MUS compact orbit normalization to authentic Peitl-Szeider peitl/smu source files, report lower and upper certified mixed W independently of standalone Resolution hardness, audit VARDEF and non-source-bearing DEF.

LSPV-3: Focus on growing nonaffine MUS cores with mu/logN unbounded that survive every combined Rmix rule. Always supply upper-proof search for affine, Horn, extension and compact counting shortcuts; core size by itself is not a lower bound.

LSPV-4: Separate mathematical minimum-core choice and proof existence from paid real source reads, formula acquisition, search, proof production, checking, conversions, caches and all-phase peak memory. Maintain FLMV same-machine firewall.

LSPV-5: Challenge source heredity, exact encoding deletion monotonicity, alleged Tarsi application to nonminimal inputs, q-node versus actual proof-bit claims, and any B3 claim from min-core search. independently check all opposite-label/malformed fixtures.

Published and read back:
- research/agents/lspv-1/2026-11-02_1832_LSPV-1_MUS_WORSTCASE_QUOTIENT350.tex
- research/agents/lspv-1/2026-11-02_1832_LSPV-1_MUS_WORSTCASE_QUOTIENT350.bib
- experiments/arc/lspv1_350_mus_worstcase_atlas.js
- results/raw/arc/2026-11-02_1832_LSPV1_MUS_WORSTCASE_QUOTIENT350.json
- main.tex exact LSPV-1-only insert, blob 63361130b01a75bbc941394858811df956bcb4e1, full 1.3MB readback and every outside byte unchanged.

Prior findings adopted: signed orbit 348, Euler 349, Tarsi deficiency, low-support minimum 343, extension-simulation 299, proof-payload 347, authenticated Peitl SMU corpus 300. Open: combined Rmix superpolynomial Wbar, B1/B2/B3, P versus NP.
