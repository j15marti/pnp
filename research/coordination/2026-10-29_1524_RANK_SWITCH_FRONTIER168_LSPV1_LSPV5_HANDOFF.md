# LSPV-3 to LSPV-1/LSPV-5: RANK-SWITCH-FRONTIER168
**October 29, 2026, 15:24 PDT.** Preserve the five existing task IDs, enabled states, hourly schedules and repository ownership. P=NP and P!=NP are OPEN.

## Narrowed mathematical obstruction

**PROVED/EXACT, elementary with precedence:** A uniform complete-state SAT controller with fully charged transitions costing at most N^c, complete-state peak work space at most N^s, a global nonnegative integer rank initially <=N^d which strictly decreases after each *whole* action, and sound SAT/UNSAT terminal behavior, takes at most O(N^{c+d}+output+discovery). See LSPV-1 ARC212 for precedent; this run makes selection, failure, joins, and output explicitly charged.

**FALSIFIED/RETIRED:** Local ranks rA,rB in {0,1} decreasing on each *own* strategy invocation do NOT bound arbitrary strategy switching. An O(n)-bit counter and alternating A/B strategy produce exactly 2^{n+1} charged actions, while each strategy resets the other rank. A positive weighted sum would require alpha>beta and beta>alpha, contradiction. This is an abstract controller counterexample, NOT an SAT hardness theorem.

**RESTRICTED PROVED/COMPUTATIONAL:** One total deterministic SAT controller tries charged, source-authenticated 2CNF SCC, original four-clause 3XOR Gaussian elimination, recognizable connected proper strict signed exact-(2,2) cyclic-and-block clause grammar, then exponential DPLL fallback. The bounded-frontier route is a previously known tractable architecture, not an unrestricted SAT algorithm. On 2 n=1200 exact22 cases (1600 clauses each), 31,106/38,006 candidate DP transitions, 13/16 maximum states, 74,196/89,992 abstract charged operations, 2 rejected recognizers, and verified original SAT witnesses. The same controller detects UNSAT on other source-authenticated 2CNF and XOR controls, but this particular cyclic sample need not contain UNSAT. Native tape costs are conservatively polynomial and must not be transferred as lower bounds.

## Exact curves and crossing cautions

The inherited necessary STATIC syntactic coverage inequality n<=3b+12bq is NOT a SAT time-space lower bound. LSPV-5 STATIC-PROXY-PARETO-REFEREE206 already proved continuous permitted b*=sqrt(n/12), t*=sqrt(n/3)-1/4; n=1200 integer minimum exponent 20 occurs at b=9,10,11, only b=9 nondominated in both enumeration/table proxies; first log-proxy equality q=0 is at b=400. A streaming enumerator avoids mandatory 2^b space.

Independent operation-count crossing scan over n=6,9,...,6000 has 32n < 2^{b+q} first at n=612; fixed e=2 affine enumeration count sum binom(n,j) first crosses at n=1002, reverses at 1026 and crosses again at 1113; e=3 first crosses at n=2931, reverses 2955, recrosses 3123. Different admissible input classes and primitive costs invalidate treating any as a measured Pareto frontier.

Accumulating O(log N) fresh names at O(log N) levels produces O(log^2 N) total live names and N^{Theta(log N)} naive contexts. Exact binary messages, SCC-affine quotient and bounded-treewidth techniques can bypass some naive state tables, but their selectors/discovery must be paid.

## Provenance and publications

Verified actual file blobs: AGENTS.md 19656af1; CODEX.md 754999f5; research skill b8df83a7; root main.tex 4b283ea8 (substantive, five markers); SOURCE_RUP_CHAIN164 89d79fdd; BINARY_ADHESION166 ba0d3f54; GRAFT167 91b784b9; LSPV-5 206 1b1d650f; ARC212 027494df; ARC231 0e70b378; CaDiCaL src/restart.cpp 4c991de7; DPMC tensor/src/join_tree.py 4ab8ffca. Primary literature: Fomin-Grandoni-Kratsch JACM2009; Arvind-Guruswami IPEC2021 Theorems 2,17,19 (fixed e P, parameter e W[1]-hard). Three user Library ZIPs were retrieved and their selected metadata/witness records independently inspected; full original benchmark replays are NOT asserted.

Published GitHub substantive timestamped standalone report: research/agents/lspv-3/2026-10-29_1524_LSPV-3_RANK_SWITCH_FRONTIER168.tex, blob fd092c43c3b70f6caa3bc884e7235ae4de8d14a7. Compact separately verified arithmetic/counter Python: research/agents/lspv-3/2026-10-29_1524_RANK_SWITCH_FRONTIER168_proxy_counter_repro.py, blob 9a94e28bdb6c69518e4bf2cfba0f830e350d79ac. Selected raw excerpt: research/agents/lspv-3/2026-10-29_1524_RANK_SWITCH_FRONTIER168_raw_excerpt.json, blob faef66fed8984710d2ae294be790f535248f50a6. Readback of all files matches uploaded strings. **The longer eight-page full PDF, 21-KB Python controller and full 17-KB raw JSON are only in the current run's sandbox archive**, not cross-run shared; the persistent Library upload returned container_session_unavailable. Do not claim GitHub compact reproducer is equivalent to the full SAT-controller script. SHA-256 checksums of local artifacts are in the raw excerpt.

## Next strict lemma

Construct a polynomial-time source-authenticated selector on an unbounded-treewidth connected strict exact-(2,2)-3CNF subclass whose `complete global outstanding-work state` has a polynomial-*VALUE* rank decreasing after all failed choices and representation switches. If a proposed selector resets measures, construct an actual input family witnessing its cost. Do not require universal polynomial ordinary Resolution certificates. One-program SAT/UNSAT restrictions and same-run time/space remain mandatory.