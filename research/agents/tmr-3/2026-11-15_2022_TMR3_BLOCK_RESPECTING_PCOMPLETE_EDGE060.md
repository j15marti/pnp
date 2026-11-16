# TMR-3/060: P-complete genuine first-visit edge at b >= log T

**2026-11-15 20:22 PST | TMR-3 / PNP Time-Space Tradeoffs, Track B**

**Status:** PROVED/EXACT within the explicitly constructed padded, block-respecting machine; independent mathematical review OPEN. Finite execution COMPUTATIONAL. This is not a SAT lower bound, not an improved Tree Evaluation evaluator, and not a statement about the output of an unspecified Hopcroft--Paul--Valiant compiler. P versus NP remains OPEN.

## Candidate, named dependency and four falsifiers

C3-BR-INDEX060: there is ONE fixed, total, deterministic, blank-start b(N)-block-respecting multitape machine W with b(N)>=log T_W(N), b(N)=Theta(sqrt(T_W(N))), for which the authentic fixed indexed Section 3.2 Williams first-visit edge ((MARK,0,2),(MARK,3)) is P-complete as a function of the original binary input. Consequently a uniform logspace source-only true-edge provider for all such machines would imply L=P, which is OPEN.

F1: the phase clock depends on the Circuit Value output. F2: some head crosses a b-cell tape-block boundary at a nonmultiple of b. F3: the public MARK source edge exists on a NO input or is absent on YES. F4: clock phases, parser, workspace retention or postphase padding are left out of the simultaneous machine ledger.

## Original source grammar and references

Use the established /059 authenticated one-hot monotone Circuit Value grammar. For n gates the original binary length is N=2n^2+3n+1: a unary 1^n0 header, then n records with 2-bit opcode (constant 0, constant 1, AND, OR) and two n-bit one-hot predecessor masks. The output is the last gate. Invalid strings reject. A fixed native locally headed interpreter A reads the original encoded source, computes every needed gate value, and halts in conservative T_A(N)<=c(N+2)^4 time and S_A(N)<=T_A(N) visited work cells. Ladner (1975) proves Circuit Value P-complete. The /059 explicit logspace dual-rail compiler (including NOT gates) maps arbitrary Circuit Value to this monotone grammar, preserving the bit f(x). No oracle is supplied.

Williams (2025), Sections 2 and 3.2, defines b-step time blocks, b-cell tape blocks and labels m_(h,i). Its source node (h,0,k) has an edge to (h',j) iff tape head h accesses its k-th tape block for the first time during time block j. Authentic graph edges depend on the source's real head movements; the published square-root-space simulation enumerates possible movement records rather than requiring a free oracle for the correct one.

## Construction lemma: exact repeatable length-only phase clock

Define a fixed logspace clock C_N that first physically scans the original read-only source to the endmarker and back to the left edge, ignoring source bits and obtaining N in binary. Next, on a private small work tape it initializes k(N)=ceil(12 log_2(N+2))+O(1) counter bits and increments a binary counter until overflow, returning the counter head to its left edge after every increment; it resets any private phase state before exit. The aggregate number of physical bit flips, head movements and carries in a full 2^k cycle is Theta(2^k), because the carry lengths have geometric total. Include actual source scans, counter setup and reset in the exact duration b(N).

Then b(N)=Theta((N+2)^12) depends on length N only, on all well-formed and malformed sources. C_N is a fixed O(log N)-work-space program, so b(N) is logspace-computable by running this length-only clock while counting its polynomial transitions with O(log N) additional bits. It is time-constructible. Its clock work head stays within O(log N) cells of the first physical b-cell tape block.

Use three consecutive phases of exactly b(N) real transitions each, rerunning the same C_N routine. During phase 1, perform the source-length scan, then run A simultaneously with the long counter phase on separate heads, and reset A's read-only input head physically to cell zero before the phase ends. The polynomial A and reset finish well before b, by the exponent-12 padding. Save its Boolean result in finite control; all A heads stay in the first b-cell blocks since their total travel is o(b).

In phase 2, freeze A, rerun the identical source-blind clock, and move a new MARK tape head right for the first b-1 paid transitions, writing a fixed marker into every visited cell. On the last phase-2 transition, move MARK one more cell iff f(x)=1, otherwise stay. This sole optional crossing from tape block 1 into tape block 2 occurs at time 2b, a legal block boundary. In phase 3, rerun the identical clock while MARK is stationary. All non-MARK tape heads scan only O(N) or O(log N) cells and remain inside their first tape blocks; A heads are parked.

After phase 3, a separate k'=ceil(2 log_2 b(N)) bit-counter makes all 2^k' increments in Theta(b(N)^2) actual physical steps and O(log b) writable cells. Its head stays in the first tape block, and every other head is parked, so no later boundary crossing occurs. Finally W outputs the saved decision and halts. All this is one fixed uniform finite-control multitape program, not a family of nonuniform input-specific tables or a free clock oracle. Its running time is length-only.

## Exact graph predicate and P-completeness

In time blocks one and two, MARK is active only on its first tape block. In time block three, its active block is 2 iff f(x)=1, otherwise 1. Therefore the authentic Williams source first-visit edge

    ((MARK,0,2),(MARK,3)) in G_(W,x) iff f(x)=1.

These source/node IDs are constant and publicly known, so no source-dependent graph-index lookup is smuggled into the query. Logspace reduction from Circuit Value proves P-hardness; direct execution of W proves membership in P. Consequently a uniform original-source-only deterministic logspace edge provider would put Circuit Value in L, implying L=P. This is conditional, not a proved logspace lower bound or any P-vs-NP claim.

## Same-execution resource ledger

| Item | Real sequential work | Peak live/visited writable space |
|---|---|---|
| Three resettable phases C_N | exactly 3b transitions | O(log N) clock scratch, input read-only |
| A, authentic source reads, return to cell zero | O(N^4), embedded in phase 1; NOT added again | S_A(N)<=N^4 retained |
| MARK movement during phase 2, active block in phase 3 | b steps embedded in C_N's second phase | b or b+1 actually visited and written tape cells |
| Postphase fixed binary counter | Theta(b^2) physical transitions | O(log b) cells |
| Termination and output | O(1) | O(1) additional |

Hence the one original W has T_W(N)=Theta(b(N)^2) and S_W(N)=Theta(b(N)), the MARK sweep dominating space. b(N)=Theta(sqrt T_W)>=log T_W, and the authentic graph contains B=Theta(T_W/b)=Theta(b) time blocks. Sharing, source repositioning and clock head movements are charged and never counted as zero-cost or duplicated work. No Cook--Mertz evaluator, no query-volume theorem and no forbidden FLMV realization are obtained from this example.

The heavy polynomial padding is crucial. It deliberately gives the original W a large writable MARK region while leaving the underlying Circuit Value problem polynomial-time. A direct source-aware evaluation is legal. The result covers an explicit b>=log T block-respecting machine (even the square-root b scale), NOT an arbitrary b=1 machine after a particular uninspected converter; it also does not establish the near-minimal b=Theta(log T) regime.

## Reproducibility and scope limitations

The actually executed standalone CPython file, revision tmr3-block-marker060-v1 and seed 202611152022, parses one-hot sources, evaluates their gate functions, and physically traces all b paid microsteps in the three MARK phases. It checks exact first-visit source-edge status and the absence of interior block crossing. Two executions gave byte-identical raw JSON: 630 valid sources, 637 malformed rejections, 302 true MARK edges/physical final crossings, 191842 assertions, zero failures. Exact local SHA-256 source 95bdd240681a9ab923cc65b7de2bc32fedcfe367883706b0174732980346b551; raw 9f2c948b516a3850707cde9f8a4c3ab638cff94afe5eb23c7cf4da794caf75c1.

The full native TM finite transition table for the length-only phase clock, source parser and final counter was NOT microtraced; the proof of its existence is constructive via the standard finite-control/logspace binary-counter procedures. The finite tests do NOT verify P-completeness, a specific Hopcroft--Paul--Valiant compiler, a generic Tree Evaluation algorithm, or new SAT hardness. Local Git clone failed DNS, so repository preflight, full native integration and TeX build were NOT run. External independent mathematical review remains OPEN.

## Mandatory four gates

| Gate | Verdict |
|---|---|
| DISJ | PASS, restricted: no cut-rank-to-general-runtime inference; DISJ and Horn/2-SAT/affine/equality/treewidth/selector/compact families stay cheap |
| Relativization | NOT APPLICABLE WITH REASON to a separation (none); a future nonrelativizing NP-level bridge, algebrization and Natural Proofs audits remain OPEN |
| Simultaneous DTISP | PASS for one padded W with fully charged time and space; OPEN for strict SAT/FLMV or a claimed improved evaluator |
| Configuration counting | PASS as deterministic halting-run upper-bound consistency only, never a work lower bound or randomized/quantum statement |

Historical /341 remains FAIL as a full logical UNSAT authority and /386 RESTRICTED. P versus NP OPEN.

## Next load-bearing lemma

C3-NEARLOG-BR-INDEX061: eliminate clock padding and construct a b=Theta(log T) authenticated public P-complete source edge under a specified block-respecting converter with all original input, time and space costs, OR prove an actual cheap graph-index promise for the intended Williams simulation. Only after that is an improved height-sensitive nonassociative evaluator plus Q/per-query T/S justified.

Sources: [1] R. R. Williams, Simulating Time With Square-Root Space, STOC 2025, arXiv:2502.17779v1 Sections 2--3, https://arxiv.org/html/2502.17779 . [2] R. E. Ladner, The Circuit Value Problem Is Log Space Complete for P, SIGACT News 7(1), 1975, https://doi.org/10.1145/990518.990519 . [3] Original TMR-3/059 report and native audit on PR #191; TMR-3/058 and TMR-5 independent tests, current five role handoffs.

Artifacts: research/agents/tmr-3/2026-11-15_2022_TMR3_BLOCK_RESPECTING_PCOMPLETE_EDGE060.md; experiments/tmr/tmr3_block_marker060.py; results/raw/tmr/2026-11-15_2022_TMR3_BLOCK_MARKER060_RAW.json; updated root main3_PNP_TIME_SPACE_TRADEOFFS.tex; role handoff. Retired trackers, other agents and their schedules untouched.
