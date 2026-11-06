# LSPV-4/428 five-role handoff | November 5, 2026, 19:39 PST

**Route A primary (LSPV-2 and LSPV-4). PROVED/RESTRICTED read-footprint no-reuse countercontrol; finite tests COMPUTATIONAL. Universal FLMV contraction OPEN, R_mix341 B3 OPEN, P versus NP OPEN.** No role/task/schedule/calculus changes.

## Advance and prior-art correction

LSPV-2/432 proved that actual indexed guest-read positions of a completed deterministic SAT call can be used to soundly reuse its answer on other same-length children when every inspected position agrees. Our LSPV-4/428 test constructs $q=2^k$ distinct equal-length proper 3-CNF descendants $C_\tau=U_H\land\bigwedge_{i<k}(\ell_{\tau_i}(a_i)\lor b_i\lor c_i)$ from any connected bridgeless cubic odd-charge Tseitin source $U_H$. The tail uses fresh disjoint variables, and every descendant is UNSAT. For the legitimate fixed guest $A_D$ that first reads **all** input bits then runs any total correct SAT decider $D$, the actual read footprint is all positions. Hence the LSPV-2/432 **latest-anchor mask policy** yields exactly $q$ guest calls and zero reuse hits, despite identical UNSAT labels. For ascending-address comparisons it inspects $\Omega(qL)$ bits because the core is a shared length-$L-o(L)$ prefix. A different comparison policy or a source-aware projection is outside this restricted lower bound. For target $(q,L)=(N^{3/5+o(1)},N^{1/2+o(1)})$ the cost saturates $N^{11/10+o(1)}$, **not** a violation of the requested ceiling.

The original every-polarity-bit sensitivity property and $\Omega(N/\log N)$ SAT source-probe bound were already proved by LSPV-1/191, LSPV-2/399 and LSPV-4/121; 950 Python and 3095 independent Node checks this run are **historical reproduction only**. There is no new input-sensitivity theorem claimed.

## Controls and legal shortcuts

The standard odd-charge cubic Tseitin 3-CNF has $4H$ clauses, $3H/2$ edge variables, $12H$ literal occurrences, input length $\Theta(H\log H)$ and published $2^{\Omega(H)}$ **ordinary Resolution** proof lower bounds for suitable growing expanders (Urquhart; Ben-Sasson/Wigderson). The extended children preserve those lower bounds under standard restriction $b_i=1$, but the known short $R_{\mathrm{mix341}}$ GF(2) derivation remains a mandatory upper-bound shortcut, not forbidden. The tails can be independently satisfied (set all $b_i=1$), so source-checked projection allows just ONE guest call on the common core. This falsifies any extension of the result to all legal derivations or algorithms.

Finite checks: 24 portfolios, $q=2,4,8,16,32,64$ on K4, cube, Petersen, Heawood; 504 actual guest runs, 0 reuses, 346448 compared bits, 56186 independent Node assertions; separate compact verifier 216 assertions. Host-language measurements, not physical FLMV multitape timings.

## Machine ledger and remaining work

Charge source parses/index reads/head moves, original authentication, child description, guest instrumentation, cache-bit writes, comparisons, failed matches, output, index erasure, and **all-phase peak highest work-tape address**. Bitmap size is $O(L)$ under contiguous allocation; guest workspace and port frame coexist. Materialized children cost $\Theta(qL)$ writes. Distinguish distinct proof nodes from actual runtime, critical path, cache and replay. The selected finite guest is not a polynomial SAT decider; the full-read polynomial guest is a conditional statement if polynomial $D$ exists.

LSPV-2: attempt a sound structural/affine *all-input* shared child-bit generator beyond footprint reuse; check hereditary children. LSPV-4: audit native high-water and local work after any proposed repair. LSPV-1/3/5: treat this as an optional cross-route sharing countercontrol only; no B3 inference and no modification of R_mix341 grammar/weights. All roles retain established hard families and their shortcuts.

Report: `research/agents/lspv-4/2026-11-05_1939_LSPV-4_READ_FOOTPRINT_NO_REUSE428.md`. Executable: `experiments/arc/lspv4_428_compact_checker.mjs`. Raw summary: `results/raw/arc/2026-11-05_1939_LSPV4_428_CACHE_summary.json`. Full independent producers, raw evidence, output logs and SHA-256 manifest in conversation reproducibility ZIP.

Historical and external review includes 2026-11-02 five-role handoff, #3, LSPV-2/432, prior LSPV-1/191 and LSPV-2/399, actual Grok/Claude, FLMV, both required `konard/p-vs-np`, `blkph0x/p-vs-np-proof-research`, FRAT-XOR, CNFgen and OpenAI's costed SAT Lean program. Direct Google-branded search unavailable. Root `main.tex` unchanged.

**Next missing arrow:** uniform, total, both-label/malformed-aware all-input recursive SAT contraction on **the same indexed machine**, charged to $t'\le\max\{11/10,3/5+t/2\}$ and $s'\le\max\{1/2,s/2\}$, remains OPEN. **P versus NP remains OPEN.**
