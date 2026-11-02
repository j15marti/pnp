# LSPV-2 FACTORED-PAIR-GROUP323: exact signed-pair distributive circuit factoring
**2026-11-01 20:35 PST. Status: PROVED/EXACT only for a declared circuit architecture, COMPUTATIONAL independently checked. P versus NP OPEN.**

## Universal obstruction and falsifiers
Building a fan-in-two evaluator C_F(x) from an original canonical Döcker Monotone 3-SAT-(2,2) F does not decide whether there exists an accepting x. An after-answer constant circuit cannot supply a free decision. Four falsifiers were attempted: (1) 322's signed-pair optimum remains optimal after distributive factoring, **FALSIFIED**; (2) grouped factoring changes the original Boolean function, **FALSIFIED by exact identity and no-import verification**; (3) Circuit-SAT necessarily beats direct CNF SAT, **FALSIFIED on measured F9/Y6 controls**; (4) unrestricted SAT deciders must construct this group circuit, **OPEN/unsupported**.

## Theorem 323A: exact optimum in the specified group-factor architecture
Let n be the original variable count, m=4n/3 the number of original same-sign triple clauses, and d(F) the number of same-sign unordered variable pairs repeated in two distinct original clauses. In the architecture that permits each such two-clause group to be implemented by exactly three AND2/OR2/NAND2 gates, each other clause by two gates, and the remaining group outputs by a binary AND tree, the exact number of gates is

g_group(F)=3m-1-2d(F)=4n-1-2d(F).

Positive group identity: (a OR b OR c) AND (a OR b OR d)=(a OR b) OR (c AND d). Negative group identity: (NOT a OR NOT b OR NOT c) AND (NOT a OR NOT b OR NOT d)=NOT((a AND b) AND (c OR d)). Both need 3 gates. Because each signed variable occurs twice, repeated signed pair groups are disjoint on original clause IDs; otherwise a common signed variable would occur at least three times. Proper duplicate-free grammar makes the two third variables distinct. Group d disjoint pairs, leaving m-2d singletons and m-d group outputs. The total is 3d+2(m-2d)+(m-d-1). Every available group saves two gates, so all must be used for the exact minimum in this architecture. All are discovered by sorting the 3m source signed-pair occurrences, O(m log m) word comparisons, with parser/source/index/head/output costs paid. This is NOT a universal minimum circuit or a SAT-decision lower bound.

## Verified canonical controls
| Original | n | m | d | 322 gates | New gates | Output-one Tseitin clauses | Exhaustive original models |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Y6 | 6 | 8 | 0 | 23 | 23 | 70 | 20 |
| F9 | 9 | 12 | 1 | 34 | 33 | 100 | 70 |
| F15 | 15 | 20 | 1 | 58 | 57 | 172 | 1032 |
| U198 | 198 | 264 | 45 | 746 | 701 | 2104 | separate UNSAT proof |
| V198 | 198 | 264 | 45 | 746 | 701 | 2104 | separate SAT witness |

Independent no-producer-import Python verification passed **4,222,603 assertions**, including **33,600 complete original-input gate evaluations** (full Y6/F9/F15; 128 sampled each U198/V198), all 16 local truth rows for each repeated-pair group, and complete Tseitin gate constraints on Y6/F9 inputs. Six malformed sources rejected. Fresh rerun of the independently authored U198/V198 original-source verifier: 384 six-bit boundary queries, 19,488 DPLL nodes and 6,099,608 literal visits, U198 UNSAT and V198 original-clause SAT witness valid.

Same-original F9: pins x3=x6=x7=x8=0 and x5=1; with x1=1, **zero** satisfying completions and each of 8 free (x2,x4,x9) leaves falsifies a recorded original clause; changing only x1=0 yields exactly **two** satisfying completions. Neither label is fed into the compiler.

Ordinary output-one biconditional Tseitin encoding gives 3g+1 mixed-width clauses, n+g variables, and exactly one gate-wire extension for each original complete accepting assignment. It is NOT a canonical Döcker target child. Naive width-2-to-width-3 padding may introduce additional witness extensions.

## Charged benchmark and recurrence
Same source, same original-variable-first UP-DPLL implementation: F9 SAT/UNSAT original-CNF uses 1/1 nodes and 40/34 literal visits; factored Circuit-SAT needs 2/1 nodes and 3653/3490 visits, excluding the compiler. Y6 unpinned uses 4 nodes, 92 visits (CNF), versus 4 nodes, 2793 visits (Circuit-SAT). No industrial CDCL or native FLMV calibration.

Source scan 3m signed occurrences; sort 3m signed-pair tuples; write g fan-in-two gates. With w=ceil(log2(n+g+1)), fixed gate descriptor components require g(2w+2) bits; source-group clause-ID references m ceil(log2(m+1)) more bits, excluding sorter/indices/headers. Tseitin output has 7g+1 signed literal records. Simultaneous peak includes all live parser, sorter, circuits, gate values, proof, cache, output, index/head, guests and ancestors. Logical XOR is OFFLINE absent charged implementation.

T_D(R) <= C_grammar,source,index,head + C_acquisition,gate,sort,compile + sum(attempts) C_failed,check,switch,GE + C_cache,replay,output,guests + sum(evaluated successors R') [C_child,bit,reencode + T_D(R')].
An exact fallback terminates but the successor sum may be exponential. No uniform polynomial all-input total-work bound, no hereditary canonical reduction, no arbitrary polynomial-decider power-short A->Phi(A), and no separate strict numerical same-machine FLMV transfer is proved. P versus NP OPEN.

## Literature and duplication
Read FIRST the published 19:50 SAT/Circuit-SAT five-role handoff, then F9-FORWARD-CIRCUIT-OBDD321, SIGNED-PAIR-CIRCUIT-UP322, CIRCUIT-TSEITIN-TRACE-AUDIT46, PARSIMONIOUS-CIRCUIT-3CNF47, HWB-OBDD-BARRIER68, and issue #3. Primary literature: Döcker 2019 (https://arxiv.org/abs/1912.08032); Bryant 1986 (https://doi.org/10.1109/TC.1986.1676819); Darwiche and Marquis 2002 (https://doi.org/10.1613/jair.989); FLMV 2005 (https://doi.org/10.1145/1101821.1101822). GitHub searches: j15marti/pnp `factor circuit Tseitin`; github.com/openai `OBDD`, `Tseitin`, `logic minimization`. No novelty is claimed for elementary Boolean distributivity or standard circuit factoring. 
