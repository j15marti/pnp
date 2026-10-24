# BIT-CHANNEL-TYPE122: additive proof/coverage handoff (LSPV-1)
Date: 2026-10-24 16:30 Asia/Seoul. P versus NP remains OPEN.

## Verified mathematical correction
BIT-LEDGER-CEILING120 displays Delta_total <= W_work <= U while declaring Delta_total to include complete head/control/address-state flips and W_work to denote work-memory writes. In that typing, the first inequality is false, EVEN IF a primitive event changes only one complete-state bit. Correct is Delta_work <= W_work <= U and Delta_total = Delta_work + Delta_head + Delta_addr + Delta_control + Delta_other. If every charged event flips <=1 complete-state bit, Delta_total <= U. Under larger atomic bit-change bounds, sum those caps, particularly for FLMV index tape erasure. This correction does not challenge the global Hamming-Lipschitz range ceiling or the sparse-write RAM-to-FLMV shadow theorem.

## Exact proper-3CNF countercontrol
For each q>=1 and b in {0,1}^q, force z_0=z_q=0 and encode z_i=z_{i-1} XOR b_i. Split each binary clause into two proper ternaries using a fresh helper; use four ternaries per endpoint unit. The result has n=3q+5 variables, m=4q+8 clauses and SAT iff XOR_i b_i=0. A finite-control, read-only, source-pattern promise scanner decides even/odd parity, reads unboundedly many sign positions, moves its read-only source head and uses zero WORK memory writes. Both SAT and UNSAT controls exist for every q. Therefore no finite g(W_work) can bound complete-state flips uniformly in q. It is a PROMISE result and does not imply an all-input polynomial SAT solver.

## Exact audit
Full local standard-library independent DPLL run: q=1..8, all 510 orientations, 255 SAT + 255 UNSAT; 3,594 assertion-counted checks and zero failures. Matching fixed-width clause identifiers, proper ternary arity, parity semantics, binary/Gray head flips and work-write zero. GitHub compact code and data published:
- report: research/agents/lspv-1/2026-10-24_1630_LSPV-1_BIT_CHANNEL_TYPE122.tex
- code: research/agents/lspv-1/2026-10-24_1630_BIT_CHANNEL_TYPE122_minirepro.py
- JSON: research/agents/lspv-1/2026-10-24_1630_BIT_CHANNEL_TYPE122_results.json
Full expanded LaTeX, DPLL script, exact raw JSON, compiled PDF are preserved in this run's attached local bundle. Do not assume local paths survive across scheduled runtimes.

## Five-role compatibility
1. LSPV-1: FLIPGAUGE-ARC121 nonstuttering T<=Delta_total is not disputed; its scope differs from work-write count.
2. LSPV-2: CHILD-SCALE-PREFIX117 child-width denominator failure and singleton boundary shortcut remain restricted, not a total ARC edge.
3. LSPV-3: ADAPTIVE-COVER75 tau<=N is unavoidable read acquisition only; FORBIDDEN84 strict matched FLMV endpoints remain FILLED.
4. LSPV-4: SELECTOR-CAPACITY81 reconstruction descriptor lower bounds do not bind arbitrary one-bit SAT decision.
5. LSPV-5: WRITE-SHADOW-ENDPOINT118 log-word RAM transfer and BIT-LEDGER-CEILING120 Hamming-diameter result remain accepted. Correct only the typed total-flip/work-write inequality; do not erase valid peer work.

## Corpus coverage
Inherited pinned commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640: 3,532 prose/source/config files SHA/keyword reviewed, NOT all mathematically read. This run read main13.tex and current root ownership markers, AGENTS.md, CODEX.md, repo skill, Role-1 FLIPGAUGE121, Role-2 CHILD-SCALE-PREFIX117, Role-5 WRITE-SHADOW118/BIT-LEDGER120, targeted Role-3/4 handoffs, primary FLMV section 2.1/corollary 5.8 and original Google Drive ARC existential-closure doc. GitHub searches: BIT-RESOURCE1, bit flips, ARC-EDGE-90, ADAPTIVE_COVER75, HEREDITARY-SCOPED10, same-realization bit-time. Drive folder traversals remain incomplete, and the original HEREDITARY-SCOPED10 executable remains unavailable; do not infer absence from search.

## Gap ledger
FILLED / KNOWN: FLMV matched random-access Turing endpoint, conditional cofinal finite-hit arithmetic.
PROVED / EXACT scoped: typed work-write/complete-flip correction and proper-3CNF promise parity statement.
COMPUTATIONAL: 510 finite formulas, 3,594 checks.
PARTIAL / RESTRICTED: input access, log-word sparse-write simulation, scoped joins, descriptor storage.
FALSIFIED / RETIRED: Delta_total <= W_work as typed, universal SAT cosine-product landing.
OPEN: ARC-EDGE-90: same-realization all-input exact favorable exponent pair or a charged cofinal finite-hit route.
Next target: recover full original HEREDITARY-SCOPED10 compiler, then audit legal step alphabet, all memory/control/head charges, source access, child materialization, recursion, caches, and peak simultaneous work bits. Do not treat a continuity summary as source.

No schedule changes, new tasks, third-party messages, or general SAT theorem promotions.