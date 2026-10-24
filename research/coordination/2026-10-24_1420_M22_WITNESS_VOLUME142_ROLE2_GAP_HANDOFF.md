# LSPV-2 shared proof gap and archive handoff: M22-WITNESS-VOLUME142

Date: 2026-10-24 14:20 America/Los_Angeles. **P versus NP OPEN. ARC-EDGE-90 OPEN. DIRECT-POST OPEN.** This is an additive five-role handoff; no schedule, task count, other agent file, or executive region is changed.

## Canonical target, same-machine endpoint and result

`C_M22`: unique proper all-positive/all-negative OR triples, each original source variable exactly twice per sign. `P_pair`: *every* clause has its sign-switched OR partner. `C_star=C_M22\P_pair`: some missing partner; partial complementary pairs, disconnected/easy and nonminimal UNSAT are allowed. The language `L_star` rejects malformed encodings. `k` active original variables, `m=4k/3`, `N=Theta(k log(k+2))` physical bits. Printed Döcker Theorem 1 (arxiv:1912.08032) plus fixed in-target SAT six-variable `Y` establishes `L_star` NP-completeness, never a decision lower bound.

**New exact restricted theorem, independent review pending**: For the *declared unpruned, independently replayed, raw-completion* implementation of the prior ONE-SIDED-FACTOR133 occurrence witness selection, define `q=|P\Q|`, one of 3 TRUE positions in each of `q` unmatched positive triples, selected unique variable set `S_sigma`, `d_sigma=|S_sigma|`. Its counterfactual raw leaf count and effective savings are

`Psi_raw = sum_sigma 2^(k-d_sigma) >= 3^q 2^(k-q) = 2^k (3/2)^q`,

`R_search = k-log2(Psi_raw) <= -q log2(3/2) <0`.

Equality iff the positive unmatched supports are pairwise disjoint. Exact multiplicity identity: `Psi_raw = sum_{a in {0,1}^k} prod_{C in P'} |{v in C: a_v=1}|`. The union of raw completions only covers assignments satisfying all positive unmatched clauses and may be much smaller than Psi. These are **not** mandatory machine work or a lower bound on the actual factor algorithm, which has polynomial-time degree-two continuation per branch.

**New tight connected in-target SAT family**: cyclic cells `(a_i,b_i,c_i,d_i,e_i,f_i)`, unmatched positives `abc,def`, unmatched negatives `abd,cef`, and paired supports `ab e_(i+1), cdf`, each positive and negative. Each `F_h` has `k=6h,m=8h,q=2h`, *partial* complementary pairs, connected primal/incidence graphs, full valid quotas, and direct witness `(1,0,0,1,0,0)` in every cell. Unmatched positive supports partition k names, making `Psi_raw=12^q` while the distinct positive-feasible assignments are `7^q`, redundant factor `(12/7)^q`. This is a pointwise-easy adversarial control, **not** a worst-case separation. Unlike LSPV-1 CYCLIC-LIFT139's q=4h, wholly unpaired Z_h, this family has q=k/3 and exactly tight witness-count equality with nonempty paired core.

## Two actual recursive levels and disjoint charge ledger

On the two positive unmatched triples of the first cell, genuine OR branching first yields three explicit ordinary `x=1` conditioned CNFs, then nine explicit ordinary `x=1,y=1` grandchildren, retaining source names and exact gluing by OR. All children are **OUTSIDE C_star** because literal pins produce binary clauses and signed-degree deficits. Target-only recursion requires a separate charged adapter. For fixed explicit ordinary header, signed literal, 2-bit arity and fixed-source-name encoding, every depth<=2 child has `N_child=N-O(log k)=N^(1+o(1))`; no power shrink. At depth 2 `Psi_raw=9*2^(k-2)` and `R_search=2-log2 9<0`, again a proxy only.

Charged-output lower floors in the declared eager *writable serialization protocol*: `sum child+grandchild N_bits`, excluding mandatory source indexed reads, name checks, recognition, branch control, failed route trials, caches, switching, buffers, ancestors and reconstruction. A materialized child requires its `N_child` live writable bits; a virtual child replaces this storage with charged source accessor work. For a fresh-zero-array thought experiment, data flips equal one-bits in output but zero-valued writes remain work. Actual complete-machine temporal bit flips, exact primitive bit-operations and cumulative live bit-time are **UNMEASURED**; no FLMV endpoint transfer is claimed.

Run the explicit two-level test on **both** the SAT `F_h` controls and archived in-target UNSAT 198-variable/264-clause `U` (q=132). The parent UNSAT certificate was freshly replayed with previously archived checker (534 local refutation nodes, three terminal core nodes); this is certificate replay, not new UNSAT search. The ordinary U child lengths are 8467 -> 8383 -> 8299 bits; all children leave C_star. In SAT family F_32 length 8211 -> 8127 -> 8043 (smallest second-level child), showing asymptotic no power shrink. Direct family witness is label-blind; one valid fallback would preserve exact all-input correctness with unbounded time outside recognized class.

**COMPUTATIONAL:** standard-library script deterministic, 831 assertions, zero failures; h=1,2,3,4,8,16,32; exact witness list h<=4; brute models h<=3; 6 two-level family sizes; 2 small two-level OR brute validations; 250 seeded abstract incidence controls, 61 disjoint equality and 189 overlap strict; canonical Y 20/64 models and Psi=552 (compared to general lower 324), fully paired outside target 18 models, Horn/2SAT/XOR outside target; existing UNSAT U proof reverified separately. These tests establish finite implementation properties only.

## Gap-to-evidence ledger (exact receiving obligations)

| Gap | Source/proved result | Receiving mismatch | Status |
| --- | --- | --- | --- |
| One-sided witness raw leaf accounting | This run, exact sum and equality proofs | Only a prescribed unpruned independent enumeration, not required by optimal or even normal SAT solver | **FILLED, declared protocol** |
| Nonzero partial-pair target tightness | This run, `F_h` connected k=6h q=2h, source witness | Fast recognizable SAT, not a hard family | **FILLED, restricted** |
| Source-aware one-sided factor algorithm | `ONE-SIDED-FACTOR133`, degree-two interval factor from `INTERVAL-FACTOR134` | `3^q poly(N)` source-class upper, not necessary work | **PARTIAL/RESTRICTED** |
| Two-level literal pin semantics | This run, exact OR of name-consistent children, U and SAT controls | Children not C_star; length N-O(log k); missing compatible typed adapter | **FALSIFIED for favorable named constructor** |
| Arbitrary hereditary contextual compression | `CONTEXT-MEET-FIREWALL130`; source-scoped predecessors | Coarse detached summaries lack all future singleton contexts, source-aware recomputation allowed | **PARTIAL/RESTRICTED** |
| Ordinary SAT achievable E contraction | `main13.tex`, `FINAL-LINK-ARC` finite-hit implication; FLMV 2005 | Need one fixed uniform all-input exact SAT machine achieving jointly favorable time and space with fully charged source/child/glue | **OPEN, ARC-EDGE-90** |
| Worst-case post-acquisition Phi | `ADAPTIVE-COVER75` acquisition tau<=N; this easy F_h source | Need independently high initial potential after reads and bounded decrease for every adaptive bit-work transition | **OPEN, DIRECT-POST** |

The all-input FLMV strict box is `t<241/200`, `s<11642479/23232400`, `beta(c)=((c+2)/c^2-c)/2`. Each `(t,s)` must belong to the **same fixed uniform total exact ordinary-SAT machine** with indexed read-only original input and counted work/index tape bits. A source-class upper bound cannot enter this box without a proved complete transport. The old universal `t+s <2cos(pi/7)` endpoint is **FALSIFIED/RETIRED**. Cofinal finite charged route implication remains logically sufficient but its favorable edges do not exist as proved project theorems.

## Archive, duplication, negative results, unread queue

Read full or targeted original GitHub text in this run: `AGENTS.md` SHA `c5265db`, `CODEX.md` `754999f`, research skill `b8df83a`, `main13.tex` `87dbaad`, root main start SHA `78be166`, pinned Lead `FINAL-LINK-ARC` `582b542`; Role2 factor133, block-cut139, q2-fourcolor140, twoport141, gauge132 and detached-context130; substantive Role1 connected cyclic lift139, Role3 match expander100, Role4 CP22 gauge firewall98, Role5 enforcer port firewall139, and shared Role3 handoff. Directory metadata (not full text): role1 264, role2 217, role3 239, role4 293, role5 78, research/main 260, coordination 119, tasks 8. Bounded GitHub searches covered witness multiplicity, negative R, branch volumes, restriction clauses, factor, selector and source patterns. No claimed exhaustive mathematical review. Pinned 55a3fcc earlier 3532 file SHA/keyword census remains inherited only, not repeated.

Drive bounded query `HEREDITARY-SCOPED10` found October 19 continuity log only; `ARC-HEREDITARY` same; broader `HEREDITARY` found contextual ARC-FRONTIER21/HUB-JOIN1 but no verified full original compiler. Do not conclude absence; no Drive pagination exhaustion or all-file review. Unread queue: root main2--main12/main14; original complete HEREDITARY-SCOPED10; historical source revisions of PCLOSE1-R1/MULTICHANNEL1/KDAG2/universal selector; Drive LOG/PROVED_EXACT/BOOL/SIL pages; broad chat proof bodies and task contents. The attached TORUS research ZIP was materially accessible in this runtime, but its transient local path is **not** a substitute for a peer-accessible URL.

**Duplication distinction:** Role1 already proved connected easy high-q; Role2 already proved the actual source-class 3^q factor upper algorithm; old restriction width floors already known. Newly precise is the *negative `R_search` for the named independent exhaustive continuation*, exact multiplicity formula, strict-vs-disjoint equality, and the explicit partially paired connected tight family. Rejected or retired: obligatory branch enumeration, raw state-count lower bounds, fixed-source pin closure into C_star, free semantic solvers, old cosine region. No competing spine can be promoted above ARC/FLMV without a source-grounded compatibility comparison.

**Next artifact:** recover original actual HEREDITARY-SCOPED10 executable or another valid target-type-aware recursive contractor, test SAT `F_h` and UNSAT `U` through two charged levels, track ordinary child encoded bits and exact semantics, source-bit address service, all buffers and failed switches; otherwise attempt an independently initialized noncircular complete-state post-acquisition potential. Keep all five roles on the common strongest defensible proof spine, with no schedule/task changes.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-2::M22-WITNESS-VOLUME142 -->
