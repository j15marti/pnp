# TMR-5/014: independent finite-head configuration audit and charged one-head simulation bridge

**Pacific timestamp:** November 14, 2026, 02:51 PST (America/Los_Angeles). **Role:** TMR-5 Machine Bottleneck Redteam and canonical synthesis owner. **New general compiler:** TMR5-HB14 CANDIDATE/RESTRICTED pending independent TMR-1/TMR-3 review. **Independently audited TMR-3/015 configuration bound and finite-head odometer:** PROVED/RESTRICTED at precisely declared machine scope. **Finite executed experiments:** COMPUTATIONAL. **Unrestricted 3-SAT lower bound and P versus NP:** OPEN.

## 1. Exact peer audit, configuration count and a caveat

I read the original TMR-3/015 mathematical report, its exact JavaScript and immutable results, rather than relying on its handoff. In its model, each fixed total deterministic halting machine has `h` locally moving read-only heads on one immutable length-`L` source, `b` one-sided writable tapes, finite control `Q`, alphabet `Gamma`, and actual visited writable footprint `S_A(x)` summed across all work tapes. A repeated *full* configuration on the same fixed source would imply deterministic nontermination. Consequently

$$
T_A(x)\le |Q|(L+2)^h(S_A(x)+1)^b|\Gamma|^{bS_A(x)}.
\tag{HB14-1}
$$

This is independently justified by bounding input-head vectors, work-head positions, symbols in the contiguous visited work interval on each one-sided tape, and fixed control. It is a **ceiling on halting runtime at a given footprint**, not a compulsory decision-time lower bound. The `S=o(log L)` consequence `T\le L^{h+o(1)}` is valid for fixed `h,b,Q,Gamma`, but only on the specified same-execution sequence. A one-tape/work-tape choice cannot be paired with a different machine's runtime.

I independently checked the odometer recurrence `D_0(q)=2q`, `D_j(q)=qD_{j-1}(q)+2q`, hence `D_{h-1}(q)=2 sum_{r=1}^h q^r` for `q=L+1`. The machine's `h` physically independently moving source-head positions suffice to run `Theta_h(L^h)` steps with zero writable workspace, at fixed `h`. On the restricted proper three-variable sign-stream 3-CNF grammar it classifies SAT, UNSAT and malformed encodings using an eight-bit finite-control forbidden-mask, while deliberately doing this semantically unnecessary extra motion. It does NOT require arbitrary 3-SAT to take that long. **Peer verdict: PROVED/RESTRICTED** symbolic model/count and exact clock recurrence, independent of finite test success.

## 2. New uniform transfer theorem: h source heads to one source head, no source copy

**TMR5-HB14 (CANDIDATE, all-program compiler).** Fix an integer `h>=1` and ONE finite deterministic total uniform machine `A` with `h` independently locally moving immutable-input heads, `b` locally moving writable work tapes, fixed work alphabet/control and correct SAT/UNSAT/malformed terminal labels for all encoded source lengths. Its single transition may simultaneously read and update all `h` source-head positions and all `b` work tapes. Then there is ONE fixed deterministic total uniform machine `B_A` with a **single locally moving original-source head**, the original `b` writable work tapes and a fixed number of additional ordinary scratch tapes such that, for `w=ceil(log_2(L+2))`, some finite program-dependent `c_A>0` satisfies for EVERY binary source `x`:

$$
\operatorname{out}_{B_A}(x)=\operatorname{out}_A(x),\qquad
T_{B_A}(x)\le c_A(L+2)(w+1)(T_A(x)+1),
\tag{HB14-2}
$$

$$
S_{B_A}(x)\le S_A(x)+c_A(w+1).
\tag{HB14-3}
$$

All source accesses, work-head movement, head-position encodings, comparisons, increments/decrements and resets are charged. The constants may depend on the **fixed program A and h**, never on `x` or `L`. This is neither a RAM unit-cost model nor an uncharged address port. It establishes a polynomial slowdown with logarithmic extra visited work cells, NOT an exact-time machine equivalence.

**Compiler and every-transition simulation.** `B_A` uses a charged initial left-to-right source sweep to construct the delimited binary representation of `q=L+1`, charging each local read and counter update. It reserves `h` binary position registers `p_i`, initially zero, plus one bounded scratch cursor register, each `O(w)` cells. Each logical step of `A` is simulated thus:

1. Leave the original `A` work tapes, heads and state unchanged while reading each of the `h` source cells indexed by `p_i`. From the real original-source left marker, move right while physically incrementing a bounded binary cursor and comparing it, bit by bit with charged locally moving counter heads, against `p_i`. Read only the currently reached source cell (including both genuine endmarkers). Return the sole physical head to the left marker and decrement/zero the scratch cursor, charging every movement and counter operation. Retain the `h` fetched symbols in finite control, since `h` and the source alphabet are fixed.
2. Read the original `b` work-head symbols at their unchanged physical work-head positions. Apply `A`'s exact deterministic transition to its state, original work tapes and writable heads in paid local steps. Sequentially update every virtual input-head position by at most one with paid little-endian carry/borrow scans, never allowing an endmarker crossing prohibited by `A`'s declared model.
3. Restore every auxiliary counter-head position to its delimiter and enter the next simulation phase. A completed logical transition is paired with the complete current original-work configuration and virtual source-head vector. These steps give an exact one-logical-step to finite-paid-path forward simulation; the immutable source and all terminal labels are preserved. No free source oracle or source correctness certificate is introduced.

Each of the `h` physical source lookups costs at most `O((L+2)(w+1))` transitions, since each cursor advance and comparison/reset is charged `O(w+1)` and there are at most `L+1` advances. Work updates and head-register changes add `O_A(w+1)`. The initial length sweep costs `O((L+2)(w+1))`. Induction over every genuine transition proves (HB14-2/3). Halting and malformed-input behavior transfer because `A` is total and every bounded microphase terminates. Cached symbols occupy constant finite control for fixed `h`.

**Quantifier transfer.** If the full every-exponent separation were proved for all correct one-input-head ordinary multitape deciders, (HB14-2) would imply it for all fixed-`h` multi-read-only-head deciders: any polynomial-time such `A` would compile to a polynomial-time one-head `B_A`. More quantitatively, applying the one-head target at an exponent at least `k+2` and sufficiently large constant gives an input witnessing a violation of an assumed `C(L+1)^k` bound on `A`. This conditional implication is NOT the missing all-program SAT lower bound.

## 3. A restricted optimality distinction: forced clock playback vs semantic decision

For the TMR-3/015 `h`-head clock, `T_{D_h}(x)=Theta_h(L^h)` and `S_{D_h}(x)=0`. Any ONE-source-head finite deterministic machine `B` with a fixed number `b>=1` of ordinary writable tapes that **faithfully performs at least one real transition per simulated clock step**, rather than skipping semantically inert clock steps, has `T_B(x)>=Theta_h(L^h)`. For `h>=2`, applying the h=1 case of (HB14-1) to **that same B and same x** yields

$$
S_B(x)\ge \frac{h-1}{b\log|\Gamma|}\log(L+2)-O_B(\log\log(L+2)).
\tag{HB14-4}
$$

The logarithm is natural, and this inference applies along all sufficiently long inputs on which the stipulated clock playback takes place. If `b=0`, the one-head configuration ceiling is linear and such playback is impossible for large `L`. Our charged one-head compiler achieves `O_h(\log L)` extra visited cells, so the order of workspace is tight **for this clock-playback requirement**. A semantic classifier may discard the pointless odometer and decide the restricted sign-stream language in `O(L)` time and constant memory. Hence no SAT-hardness lower bound follows from the playback requirement.

## 4. Independent execution, controls and exact reproducibility

**Independent native CPython** implementation, not the original TMR-3 executable or a wrapper, was executed from `/mnt/data/tmr5_multihead_bridge014.py`: 677 inputs including exhaustive source lengths `h=1:0..8`, `h=2:0..6`, `h=3:0..4` and additional complete SAT, all-eight-mask UNSAT, malformed and repeated-clause inputs. It checked 31,763 simulated logical transitions, 6,254,782 charged single-source-head binary-counter/source microsteps, 60,466 actual current-cell reads and zero assertions. This Python file and its local raw result were **not** published to GitHub; do not claim a shared Python executable.

**Separate directly executed hosted-V8 implementation** is published verbatim at `experiments/tmr/tmr5_onehead_multihead_bridge014.cjs`, immutable raw at `results/raw/tmr/2026-11-14_0251_TMR5_ONEHEAD_MULTIHEAD_BRIDGE014_RAW.json`. It tested 341 sources, 14,949 logical transitions, 4,186,007 paid microsteps, 27,152 source lookups and current-cell reads, 95 SAT/2 UNSAT/244 malformed outputs, maximum 15 visited auxiliary register cells and zero failed assertions. Both physically move one source head, read only the current source cell, scan charged ordinary binary tapes and compare an independent set-based semantic oracle. The V8 and Python implementations differ in fixture counts and executable text and are independently authored; they are not independent generated transition tables for arbitrary `A`.

**Original peer audit distinction:** TMR-3/015's original JavaScript was inspected and its exact recurrence symbolically checked. I did not claim native OS execution of the peer's original V8 source. The two new experiments are independent simulations of the same restricted positional controller, not tests of every arbitrary A. Finite work is COMPUTATIONAL and does not promote HB14 to an unrestricted result.

**Hostile controls:** SAT, UNSAT, malformed, repeated clauses and the complete eight-mask UNSAT sign stream were actually executed in both implementations. Horn, 2-SAT, Gaussian-elimination XOR/Tseitin, bounded treewidth, sharing, products, padding, renaming, auxiliary variables, cache/recompute, arbitrary algebraic compression and an unrestricted 3-SAT solver were NOT individually executed. Symbolic HB14 permits any such algorithm inside A without choosing a template, but no time lower bound is inferred for any of them. No advice, oracle, truth-table lookup or unbounded-word free arithmetic is assumed. The source is bound throughout, including initial and terminal configurations.

## 5. Literature, required corpus, current status and next arrow

Primary scope sources checked: F. C. Hennie and R. E. Stearns, *Two-Tape Simulation of Multitape Turing Machines*, JACM 13(4) (1966), 533-546, https://doi.org/10.1145/321356.321362 (different k-tape to two-tape `O(T log T)` result, **not** the claimed h-source-head to one-source-head logspace accounting); the IEEE original 1973 conference record *On tape-bounded complexity classes and multi-head finite automata*, https://doi.org/10.1109/SWAT.1973.20 (fixed-head computation and logarithmic tape models, not an all-variable SAT lower bound). The detailed compiler is argued directly rather than importing an unsupported classical theorem. Relevant originals inspected: TMR-3/015 report/source/raw, TMR-1/015 indexed-port no-copy compiler, TMR-1/016 one-head paid-counter compiler, TMR-3/014 original physical crossing construction, TMR-4/016 parity-erasure MAY failure and TMR-5/013 charged multihead clock.

The 2026-11-13 12:49 PST NEW-TMR replacement directive was read first, SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4`. Root `proof1.txt` is nonempty, 28,714 characters, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`. The contents API returned **blank** bodies with valid SHA for root `proof2.txt` and `main.tex`; authenticated Git blob reads recovered their **full nonempty** 1,051,196 and 2,525,134 characters, SHA `930c5eeddafce656717f28055a7a9a755f44737c` and `d3db01d221df39f096f31237643268132edfcd87`. Root AGENTS.md, CODEX.md, repo research skill, issue #3 (through TMR-3/015), all five newest TMR handoffs and materially relevant original reports were inspected. Historical checker/normalizer counterexamples remain preserved and are not asserted to transfer to arbitrary deterministic TM execution.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The new bridge adds no new unconditional P=NP algorithm or P!=NP lower bound; neither tracker merits a material status change. TMR-5 owns whole-document reconciliation of canonical main.tex and must preserve all older contributions. New HB14 remains CANDIDATE/RESTRICTED until independent peer review. P versus NP remains OPEN.

**Next single load-bearing target:** Find or falsify a source-aware *unavoidable* processing or distinction-acquisition cost on actual unrestricted SAT machine executions that survives compiler HB14, arbitrary polynomial writable space and polynomial-time specialized semantic algorithms. Require TMR-1/TMR-3 independent compiler review. A source-head counting ceiling, even tight, does not yield such a lower bound.

END_OF_REPORT::TMR-5::014::2026-11-14_0251_PST
