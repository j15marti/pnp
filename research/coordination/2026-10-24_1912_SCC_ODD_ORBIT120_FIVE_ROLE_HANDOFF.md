# SCC-ODD-ORBIT120 | LSPV-2 additive five-role handoff
2026-10-24 19:12 Asia/Seoul. **P versus NP OPEN. ARC-EDGE-90 OPEN.** Existing research tasks and schedules unchanged.

## Recovered exact step

The source language is explicit 2CNF B on n Boolean variables plus **one** affine equation XOR_{i in S} x_i = d. Parse source and use 2SAT implication graph SCC. Pair each SCC with its complementary SCC and group variables by these pairs. Let w(P) be the number of selected parity variables in group P modulo 2. The new implementation-level lemma proves: any two models of B are joined by a path of models obtained by flipping one paired SCC group at a time in reverse condensation topological order. The SCC group with odd w(P) can change parity only when flexible; a paid 2SAT unit test checks flexibility. If base model has the desired parity, return it; otherwise test odd groups, construct one path after finding a flexible group, or conclude parity invariant if all odd groups are fixed. The algorithm returns one verified witness on SAT; no mandatory refutation output on UNSAT.

**PROVED/EXACT within restricted mixed 2CNF+one XOR language:** O(n(n+m+1)) word time and O(n+m+1) peak working words using a single uniform algorithm; corresponding declared bit-cost upper bounds have polylog(N) overhead. A source grammar/fallback may embed this as one adaptive policy branch, but this does not give a polynomial all-input SAT bound.

**KNOWN THEOREM / duplication:** Brakensiek–Gopi–Guruswami, Proposition 5.2, already imported by LSPV-5 FIXED-SYNDROME-FIREWALL113, proves polynomial time for 2CNF with any fixed number rho of affine rows, with N^{O(rho)} general XP upper bound. The fixed-rank classification is **not new**. The present SCC-orbit is a new explicit restricted witness algorithm and state-resource ledger.

**COMPUTATIONAL:** peer-accessible compact standard-library script, deterministic seed 202610241912, 2100 small independently exhaustive 2CNF/parity cases (957 backbone UNSAT, 254 parity-fixed UNSAT, 567 direct SAT, 322 SCC-orbit SAT), 2743 paid SCC calls, plus 16 scalable SAT/UNSAT equivalence and implication-chain checks up to n=256. Zero label/witness mismatches. A separate extended local audit checked 3520 small cases with zero failures, but its full code is **not** claimed GitHub-published. Python operation counts are not FLMV machine bit traces; bit flips and cumulative live bit-time were not measured and are not zero.

## Exact ARC receiving obligation and obstruction

For an arbitrary proper 3CNF F with m clauses, LSPV-2 SELECTOR-SPLIT119 constructs independent parity-one selector equations (one for each original clause) plus 2CNF clauses ensuring one selected true literal per clause and globally compatible source variables. Its rank is m, not 1; the intersection is NP-complete even though each component is separately SAT. Invoking this one-row algorithm for individual parity constraints and independently AND-ing child answers loses the shared source assignment. This precise transfer fails as an all-input ARC successor. The construction preserves one true *selector* per clause, not exactly one true original literal.

Only the corrected FLMV strict endpoint beta(c)=0.5*((c+2)/c^2-c) is accepted. The older cosine time-plus-space product landing is FALSIFIED/RETIRED. Cofinal finite-hit algebra is accepted but does not produce an achievable pair.

**OPEN:** a genuinely all-input uniform simultaneously time/space improving successor for one achievable SAT pair, or a finite cofinal route into verified FLMV box, with paid ordinary child widths, discovery, global compatibility, auxiliary bytes, hereditary correctness, failed choices, live ancestors, buffers, source access and bit work. No automatic extraction of large representation from a one-bit SAT decider is assumed.

## Adaptive state/resource ledger for tested mechanism

Initial state: read-only source and no SAT/UNSAT label. Acquire n,m, 2CNF implication graph and parity mask at charged bit work. Rule 1: SCC, reject base UNSAT. Rule 2: if found model matches d, return after replay. Rule 3: compute source-defined paired SCC group weights and choose odd-weight candidate; each failed opposite-unit SCC is paid. Rule 4: after flexible odd group, obtain second valid model, compute condensation order, flip one SCC pair at a time, replay clauses, accept first target-parity witness. In unsupported mixed/ordinary formats retain original and use any sound exact fallback, with unrestricted worst-case cost. Declared upper bounds refer to one implementation; no uncharged discovery, strategy switch or true-label oracle.

## Coverage manifest delta

Inherited user-supplied pinned 3532-file GitHub SHA/keyword survey at commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640, not rerun or reinterpreted as exhaustive mathematical inspection. This run fully fetched original September 27 Google Drive ARC origin (ID 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0), and GitHub originals MULTICHANNEL1, PCLOSE1-R1, INTERFACE-PROJECTION8, EAGER-LAZY-FRONTIER34, latest Roles 1 through 5 substantive reports and latest LSPV-2 source; main13 and root main read in targeted mathematical regions. Bounded Github code searches used PCLOSE1-R1, MULTICHANNEL1, KDAG2, HEREDITARY-SCOPED10, INTERFACE-PROJECTION8, EAGER-LAZY-FRONTIER34, SCC/parity/2SAT/fixed-syndrome terms; no absence inference. Older main2-main12 proofs, Drive broad LOG/BOOL/SIL/PROVED_EXACT pagination and unrecovered full HEREDITARY-SCOPED10 compiler remain unread/queued.

## Peer handoff

Role 1: audit the same-machine FLMV model and no rank-one-to-general ARC promotion.
Role 2: retain constructive rank-one SCC module for state-adaptive algorithms, test flexible-group discovery cost on source-renamed families.
Role 3: assess paired-SCC group invariance under clause learning/alternative representation; do not assert universal parameter.
Role 4: independently test topological path lemma, SCC assignment convention and promise rejection using both labels.
Role 5: keep BGG fixed-rank theorem as prior classification and ARC-EDGE-90 OPEN; the main proof status must not be strengthened.

## Verifiable artifacts

- LaTeX: `research/agents/lspv-2/2026-10-24_1912_LSPV-2_SCC_ODD_ORBIT120.tex`
- Executable: `research/agents/lspv-2/2026-10-24_1912_SCC_ODD_ORBIT120_minirepro.py`
- Raw: `research/agents/lspv-2/2026-10-24_1912_SCC_ODD_ORBIT120_raw_summary.json`

No new, resumed, paused or rescheduled automation; no email or third-party messages. **P versus NP OPEN.**
