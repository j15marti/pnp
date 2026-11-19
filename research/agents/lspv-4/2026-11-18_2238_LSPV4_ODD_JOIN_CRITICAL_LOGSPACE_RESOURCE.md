# LSPV-4: growing intrinsically critical T5 exact-one sources with logspace witnesses

Date: 2026-11-18 22:38 PST. Historical Route A resource auditor. **PROVED/EXACT** on the declared restricted source grammar; **COMPUTATIONAL** for independent raw-label replay; **OPEN** for unrestricted SAT, growing-girth critical promises and P vs NP. No automation identity, schedule, state or manuscript changed.

## Candidate and falsifiers

For every k>=1 the private-head Q lift of J_k=K3 join C_(2k+1) is connected, intrinsically clause-minimal UNSAT but admits a uniform fully charged efficient complete witness for every one-clause deletion. Attempted falsifiers: (1) wrong XOR/AND or tie semantics, (2) missing/duplicate edge, reused head, even rim or malformed source accepted, (3) witness output, source validation, failed head attempts or workspace underestimated.

R(a,b)=1 iff (b-a) mod5 is 1 or 3, R(a,a)=0; Q(h,u,v)=R(h,u) XOR R(h,v). All three *variable names* in a clause are distinct, assigned values may tie. The 125 ordered triples have Q60/P20 successes, disjoint.

## Theorem A: intrinsic criticality at bounded treewidth

For k>=1, put L=2k+1, J_k=K3 join C_L. For each undirected edge e={u,v}, create a unique private head h_e with the original clause Q(h_e,u,v). The Q source F_k has v=2k+4 endpoint variables, m=8k+7=4v-9 clauses and private heads, and n=10k+11 total Q variables. Because for any letters a,b we have (exists h Q(h,a,b)) iff a != b, F_k is SAT iff J_k is 5-colorable. The K3 requires three colors disjoint from the odd rim's three colors: chi(J_k)=6. Thus F_k is UNSAT.

For every deleted original clause, construct a full SAT witness on the original variables by giving exactly that graph edge equal endpoint colors:
1. Deleted clique edge: its endpoints get 0,0, third hub 1; rim colors are 4 then alternating 2,3.
2. Deleted rim edge: hubs are 0,1,2; rim is an even-length path, alternating 3,4.
3. Deleted cross edge: hubs are 0,1,2; removed rim endpoint takes its hub's color, remaining rim path alternates 3,4.

Every other graph edge has distinct endpoint colors. For each retained original Q clause, try h=0,...,4 and select a winning XOR head. The deleted head can be 0. Verify all original Q triples. Hence every deletion is SAT, and every proper subset is SAT. This is a connected intrinsically critical Q-UNSAT family of unbounded size, not an attached fixed gadget.

tw(J_k)=5 exactly: the cycle has width two and adding three universal hubs to its decomposition bags gives width five; chi(J_k)=6 gives matching lower bound tw>=5. Graph/primal girth is 3; the original Q incidence graph has girth **6**, not increasing girth. Its every private-head parity graph has exactly one edge and is bipartite. No known unrestricted SAT lower bound follows.

## Theorem B: SAME-MACHINE RAM ledger

An arbitrary-ID, arbitrary-clause-order source recognizer checks all header/index records, exactly one private head per edge, partition of head-only/tail-only variables, duplicate edges, three universal hubs and one connected odd rim cycle, special-casing K6. INVALID or UNSUPPORTED never becomes false UNSAT. Once authenticated, it constructs and verifies one full n-letter designated deletion witness using at most 5m private-head trials.

With w=Theta(log(n+m))-bit RAM words, read-only source of N ASCII characters, deterministic radix/counting sorting of bounded indices gives O(N+n+m)=O(N) work and O(n+m) writable words for one full original-label witness. Comparison sorting gives O(N+m log m) work. Source materialization costs an additional N writable bytes. All m fully verified witnesses can be streamed in O(N+m log m+m(n+m)) work and O(n+m) live words. All full vectors require Theta(mn) output symbols; no compressed-certificate claim is substituted.

## Theorem C: constructive logarithmic-space variant

On a read-only two-way input tape with a write-only output tape, guard n<=3m<=3N before looping over IDs. Compute head/tail frequencies and graph degrees by repeated source rescans, reject repeated pairs by nested indexed rescans, retain only 3 hubs and O(1) O(log N)-bit counters/indices. Verify the 2-regular odd rim is one connected cycle by a previous/current walk, recover any rim position by rescan-walking, compute any endpoint color by the three explicit formulas, and recover any private head color by looking up its clause and testing the five values. Emit all original n colors in ID order, then rescan and verify every retained native Q clause. This gives **O(N^3) time and O(log N) writable bits** for a designated deletion witness; all m outputs can be replayed in O(N^4) time and O(log N) space. These are the same-execution read-only tape bounds, not CPython RSS claims.

## Independent finite work counters

The reproducibility ZIP T5_LSPV4_ODD_JOIN_CRITICAL_LOGSPACE_20261118.zip (available in the run's conversation artifacts) contains standard-library RAM and read-only-rescan scripts, every exact original input, physically emitted binary witness streams, SHA256 manifest, raw JSON, mathematical report and separate independent Q verification.

| k | n | m | full witnesses | producer retained-clause Q checks | failed/successful head trials | output letters |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 21 | 15 | 15 | 210 | 351 | 315 |
| 2 | 31 | 23 | 23 | 506 | 855 | 713 |
| 3 | 41 | 31 | 31 | 930 | 1583 | 1271 |
| 4 | 51 | 39 | 39 | 1482 | 2535 | 1989 |
| 7 | 81 | 63 | 63 | 3906 | 6735 | 5103 |
| 16 | 171 | 135 | 135 | 18090 | 31431 | 23085 |
| 32 | 331 | 263 | 263 | 68906 | 120135 | 87053 |
| 64 | 651 | 519 | 519 | 268842 | 469575 | 337869 |

Total 1,088 **physically streamed** full deleted-clause witnesses and 362,872 producer checks. A standalone independent arithmetic verifier read the actual source and output bytes and checked **363,960 original Q clauses**, including the deleted clause: all retained constraints true, the deleted constraint false. The k=64 stream physically wrote 339,945 bytes; the CPython solver-phase peak allocated heap proxy was 486,053 bytes, **not a word-TM or RSS measurement**. Six malformed/unsupported controls rejected. An independent brute check of the k=1 and k=2 original graph showed UNSAT; the read-only rescan variant at k=1,2,3 produced SHA256-identical complete designated witnesses to the indexed algorithm.

The exact-title user Library archive T5_Exact_One_Experiments_2026-11-18.zip (libfile_00b4599c2cfc8191a859b757dad101a0) passed its own independent verification: Q=60, P=20, five-clause deletion counts 10/40/10/30/25, and 236 283-variable fixture deletion witnesses with 55,696 checks. The single n40,m60 appendix UNKNOWN remains UNKNOWN. Previous experiment grids were not rerun.

## Transfer status and next gate

The source-critical family is a **positive low-space/witness algorithmic control**, not growing-girth difficulty: it has a fixed six-cycle incidence obstruction, simple structure and bounded treewidth. The uniform algorithm recognizes just this source family and returns UNSUPPORTED outside it, so no arbitrary-CNF SAT, uniform shared-z universal-cover specialist, general n^1.33/square-root-space claim, or unrestricted lower bound follows. General SAT alternation-trading exclusions are not transferred to this promise. Free polarity, nondeterministic k-bit guesses, and external proof systems are not free deterministic discovery or global forall-z coverage. DISJ, relativization, natural-proofs and configuration-counting restrictions are not bypassed. Next: genuine increasing-incidence-girth intrinsically critical Q families with shared-head global constraints and audited alternative GF(5), treewidth and compact-circuit shortcuts. **P versus NP remains OPEN**.

References: [1] Hell and Nesetril, H-coloring dichotomy (1990), https://doi.org/10.1016/0095-8956(90)90132-J ; [2] Arnborg, Corneil, Proskurowski (1987), https://doi.org/10.1137/0608024 ; [3] Fortnow et al., SAT time-space (2005), https://doi.org/10.1145/1101821.1101822 ; [4] Buss and Williams (2015), https://doi.org/10.1007/s00037-015-0104-9 .