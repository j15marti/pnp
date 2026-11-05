# LSPV-1/413: Unconditional RUP/DRUP output obstruction, 2026-11-05 01:00 PST

**PROVED/KNOWN COROLLARY; P vs NP OPEN.** LSPV-1/412 proves any explicit original-source additive RUP log of encoded length E can be translated to ordinary strict RES with at most poly(N+E) paid nodes. Haken's classical explicit unary pigeonhole PHP_h gives lower bound 2^{Omega(h)} for every ordinary shared-DAG RES refutation, while the input bits N_h=Theta(h^3 log(h+2)). Thus all additive RUP logs of PHP_h (and all DRUP logs where deletion does not authorize non-RUP additions) must have E=2^{Omega(h)} bits.

**Consequence:** the proposed strategy “an arbitrary polynomial-time SAT decider returns polynomial-size additive RUP/DRUP UNSAT logs for all inputs” is **unconditionally impossible**, independent of SAT in P. Result 412's restricted B1 for solvers that actually emit charged RUP logs remains correct, but a *polynomial-time all-input* member of that restricted class does not exist. This is the main new practical route retirement, a corollary of known Haken and existing project /412, not a new classical lower bound.

**Falsifiers:** (i) RUP strict-subclause simulation from /412 succeeds; (ii) clause deletion is harmless when omitted from verification because UP conflicts are monotone under extra clauses; (iii) PHP bits remain polynomial in h; (iv) RAT/PR/ER/DEF **escape**, so no lower bound on mixed calculus or arbitrary SAT machines. No strengthening of B3 or all-input transfer claimed.

**Finite verification:** Python original-source generator and independent no-import JS both checked 6 PHP cases (SAT h pigeons, UNSAT h+1 pigeons for h=1,2,3), original-source RES parent/pivot replay and RUP of each added resolvent. UNSAT h=3 certificate has 139 steps. JS 392 assertions and 6 negative controls; full local code and raw attached as conversation artifacts. Source verification, encoded bits, output, proof checking and peak writable memory separately charged. Host tests are not physical FLMV measurements.

**SEARCH:** Governing refocus and original /341, /384, issue #3, peers /411 /415 /407 /412, REFEREE357 and earlier /398; actual Grok GROKPROOF/2026-11-05_1218_PROGRESS.md and Claude TPORT/ONETAPE reports. Primary Haken 1985, Cook ER 1976, Cook-Reckhow 1979, Heule DRUP documentation and Buss-Thapen LMCS 2021. Authenticated GitHub OpenAI queries ExecCNFNodeSearchCosts, CookLevin, reflection proof checker SAT, LRAT verifier; no native compiler. Direct Google UI unavailable; general web used.

**Next obligation:** Replace additive RUP-only logging by a typed original-source-authenticated native certificate language capable of DEF/ER/LOCAL/GF2 shortcuts, **then** independently prove polynomial native proof existence if SAT in P. Exact source-export grammar and B3 remain OPEN. The established five roles, fixed calculus/weights, enabled schedules and manuscript ownership are unchanged.

Artifacts:
- report research/agents/lspv-1/2026-11-05_0100_LSPV-1_RUP_PHP_OUTPUT_BARRIER413.tex
- executable experiments/arc/lspv1_413_php_rup_finite.js
- summary results/raw/arc/2026-11-05_0100_LSPV1_RUP_PHP_BARRIER413_summary.json
- full conversation-run raw and independent checker /mnt/data/lspv1_413/
