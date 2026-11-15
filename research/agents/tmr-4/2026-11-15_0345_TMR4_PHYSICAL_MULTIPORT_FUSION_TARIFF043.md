# TMR-4/043: fixed-port physical fusion tariff with matching exact primal and dual

**2026-11-15 03:45 PST, America/Los_Angeles | TMR-4 / Cost-Sound Abstraction.**
**PROVED/RESTRICTED** for a qualified multitape literal-copy service; independent mathematical review OPEN. Finite V8 audit COMPUTATIONAL. P versus NP OPEN.

## 1. Candidate and precommitted falsifiers

**Candidate:** generalize TMR-3/042's physical input/output fusion tariff to m independently headed source/output tape pairs for any fixed integer m. Use a **maximum** residual input frontier and a jointly priced output/HALT obligation, not separate additive prices for every tape.

F1: an authentic transition corrects multiple cells *on a single designated tape*. F2: simultaneous operations on distinct tape heads make additive source charges unsound. F3: an authentic final transition simultaneously authenticates source endmarkers, writes multiple output cells, and halts, violating separate logical budgets. F4: caching, compressed output, or a one-bit result satisfies the literal physical-copy goal without filling the designated output tapes. The explicit one-head-per-tape primitive excludes F1. F2/F3 yield real cost-one counterrows. F4 is excluded only for the explicitly stronger copy contract, not for arbitrary SAT decisions.

## 2. Qualified concrete model and zero closure

Fix **one constant m** and a fixed deterministic finite-alphabet multitape machine. Its m immutable read-only input tapes contain valid arbitrary binary strings x_i followed by an endmarker #. It has m designated initially blank writable literal-output tapes and any fixed number of additional work tapes. Each tape has one locally moving head, and in one physical transition the machine may read the currently scanned symbol of *every* source, write *one* scanned cell on *each* output tape, update work-tape heads/cells and control, and optionally HALT. Every real physical transition costs one; source rereading, caching, conversions, recomputation, overwrite and terminal control are all charged. This is a native fixed-m multitape primitive, not a variable-port circuit gate.

Success requires authenticated inspection of the actual endmarker of every source, exact literal physical x_i# on its corresponding designated output positions, and successful halt. Define B_i=|x_i|+1>=1, M=max_i B_i, S=sum_i B_i. The full concrete configuration retains fixed program/control, exact authenticated input, all tape symbols/heads, paid history and provenance. For abstract accounting, r_i is the historically highest consecutive source frontier read, expressed as a cell count, initially 0; c_i is the number of currently correct mandatory output cells, initially 0; h=1 until successful halt and 0 afterward. These are proof-only ghost observations, not uncharged machine instructions.

Every authentic physical operation costs one, hence the physical zero-cost SCCs are singleton and cl0(C)=C. A **separate metadata VIEW test fixture** permits reversible free aliases, producing genuine size-two zero-cost SCCs with identical obstruction vectors. The fixture does NOT grant a zero-cost physical copy, source read, or output write.

Concrete/abstract relation: a complete physical state is related to its actual tuple of historical r_i, literal output correctness c_i and goal flag h. Each native transition corresponds to **one price-one abstract MAY row** with r'_i-r_i in {0,1}, c'_i-c_i in {-1,0,1} and possible successful terminal h-h'=1 only when goal conditions are met. The abstract MAY system overapproximates all executable controls, including corrupted output, caches, rereads, guesses and arbitrary work-tape operations. No genuine path is deleted and no CEGAR is invoked. Every completed physical goal maps to an abstract goal.

## 3. General theorem: the exact all-transition nonnegative tariff cone

Use the canonical seven-column order (CNF, affine, separator, fusion, Gamma, interface, machine). Define

$$
\mathbf p(C) =
\left(0,0,0,0,0,\ \max_i(B_i-r_i),\
\sum_i(B_i-c_i)+h\right).
$$

One locally moving source head can inspect at most one new rightmost cell in a transition. Every residual B_i-r_i decreases by at most one; therefore their **maximum** decreases by at most one. Every output head can improve at most one physical cell, and successful HALT contributes at most one more unit. All authentic signed discharges consequently satisfy

$$
\Delta_{\mathrm{interface}}\le1,\qquad
\Delta_{\mathrm{machine}}\le m+1.
$$

Let a=lambda_interface>=0 and b=lambda_machine>=0, the remaining five weights zero. The **necessary and sufficient uniform full-envelope tariff cone** is

$$
\boxed{a+(m+1)b\le1.}
$$

Sufficiency follows directly from both per-step inequalities, with negative corruption discharges retained. Every completed goal has potential zero, so telescoping applies to actual physical work.

Necessity is witnessed by a **single authentic cost-one physical transition** on m empty inputs: read all m endmarkers simultaneously, write # in each designated initially blank output cell, and halt. Its signed two-column discharge is exactly (1,m+1). Nonnegative weights violating the cone overcharge this genuine step. The same terminal row appears when all source lengths are equal and the copier processes the last # symbols simultaneously. Separately charging each source read/output write and HALT at unit price incorrectly charges m+2 for this **one** transition. A hypothetical free write would violate a positive machine tariff, but is not authentic and cannot be silently assumed or excluded in a different model.

## 4. Explicit fixed-machine exact minimum and rational LP dual

A fixed m-port synchronous machine copies one next source symbol to its corresponding output cell per still-unfinished pair on each transition. Its finite control remembers which streams already reached and copied their #. It halts in the transition that copies the last endmarker from the longest stream. Because m is fixed, the required done-bit finite control is fixed, not nonuniform per input length. Every input tuple completes in exactly

$$
W_{\min}(x_1,\ldots,x_m)=M=\max_i(|x_i|+1)
$$

transitions. Conversely every correct literal-copy service must physically read the rightmost endmarker of a longest stream, and no local input head can reach it in fewer than M steps.

The initial seven-vector has p_interface=M and p_machine=S+1. The exact rational primal is

$$
\max_{a,b\ge0} Ma+(S+1)b
\quad\text{subject to}\quad a+(m+1)b\le1.
$$

Certificate a=1,b=0 attains M. The dual is min y subject to y>=M, (m+1)y>=S+1, y>=0. Exact certificate y=M is feasible because S+1<=(m+1)M for B_i>=1. Thus **primal = dual = actual machine cost = M**, not the sum S of per-tape milestones. The bound is linear in physical source length. The number of physical ports m may not grow with length inside a fixed machine without a separately charged model compilation.

## 5. Complete row schema and independent replay

The accompanying seven-column exact-tariff JSON contains source read (interface=1, machine=0), one output correction (0,1), shared read/write across all m tape pairs (1,m), real shared terminal read/write/HALT (1,m+1), cache/revisit/recompute (0,0), signed corruption (0,-1), and HALT after completion (0,1), all at **physical cost one**. It describes the larger signed MAY row family and a separate zero-cost metadata VIEW SCC fixture. The independent finite implementation tests all legal finite overapproximation rows with per-stream input frontier increments 0/1 and output correctness changes -1/0/1, including terminal co-discharge. The proof of sufficiency is **symbolic for all physical transitions**, not inferred from enumerating a bounded test space.

Exactly published and executed V8 audit source:
- experiments/tmr/tmr4_multiport_tariff090.js
- results/raw/tmr/2026-11-15_0345_TMR4_MULTIPORT090_V8_RAW.json
- results/raw/tmr/2026-11-15_0345_TMR4_MULTIPORT090_TARIFF_MATRIX.json

**Execution:** 361,572 V8 assertions, zero failures; 165 fixed-m/length profiles; 1,518 physical synchronous-copy transitions; 118,297 bounded signed MAY rows including output corruption; 671 two-state metadata zero-SCCs; 495 completed literal-copy traces with zero, one and alternating-bit controls. All numerical inequalities are integer-scaled rational conditions. A separate native CPython reconstruction using Fraction tested the same 165 profiles/1,518 actual steps/118,297 MAY rows and passed 959,025 checks without failures, but the independent local script is **not** described as a byte-identical repository publication. Finite checks are COMPUTATIONAL.

## 6. Corpus, scope, and dependencies

Read first the governing fusion priority (SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6), then TMR replacement, root proof1 (28,714 chars; SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), full recovered root proof2 blob (1,051,196 chars; SHA 930c5eeddafce656717f28055a7a9a755f44737c), full recovered root main.tex blob (2,545,859 chars; SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34), issue #3, AGENTS, CODEX, project skill, current TMR-1..5 handoffs, LEAD-0029 original Lipschitz audit, and relevant reports/code/matrices of TMR-3/042, TMR-4/036-042, TMR-1/042, TMR-2/042, TMR-5/038. Primary methodological references: P. and R. Cousot, Abstract Interpretation (POPL 1977), https://doi.org/10.1145/512950.512973; Hartmanis and Stearns, On the Computational Complexity of Algorithms (Trans. AMS 117, 1965), https://doi.org/10.1090/S0002-9947-1965-0170805-7. Feasible interpolation is not used to establish a lower bound; see J. Krajíček, Interpolation theorems, lower bounds for proof systems, and independence results for bounded arithmetic, JSL 62 (1997).

**Dependency status:** concrete fixed-m physical primitive, all-step signed potential, exact cone, actual synchronous copier, and matching rational dual PASS/PROVED RESTRICTED; small tests COMPUTATIONAL; additive logical-event pricing FAIL; literal-copy contract RESTRICTED to this task; growth of m within one fixed machine forbidden without translation; authentic physical zero closure identity; generalized SAT-specific fusion obstruction, superpolynomial initial potential and all-correct SAT-machine same-system transfer OPEN. /341 remains FAIL on its full accepted language; /386 remains RESTRICTED to its guarded fragment.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root file, canonical main.tex or existing scheduled task was modified. P versus NP remains OPEN.
