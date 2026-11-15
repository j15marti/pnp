# TMR-3/048: Exact physical multihead-frontier tariff and max-versus-sum cost

**2026-11-15 09:28 PST | PHYSFRONTIER148 | PNP Time-Space Tradeoffs**

**Status: PROVED/RESTRICTED for the declared marker-prepared finite-alphabet multitape service suffix; independent mathematical review OPEN. Executed finite Node 22 evidence COMPUTATIONAL. P versus NP remains OPEN.**

## 1. Candidate, predeclared falsifiers and predecessor boundary

Before searching original papers and repository history, the candidate was that authentic concurrent input reading and two physically distinct target writes require a maximum-of-head-frontiers tariff, not an additive head-distance charge. Four falsifiers: (F1) a real zero-price step changes the frontier, (F2) one physical step discharges more than its weighted tariff, (F3) a compact shared representation avoids actually writing mandatory output cells, (F4) transferring a prepared suffix to blank-work-tape SAT computation omits marker setup, original-source parsing or indexing. F1 and F2 are excluded below; F3 is excluded only by the declared physical-output contract; F4 is an OPEN transfer blocker.

TMR-3/042 had already constructed a synchronized physical I/O and HALT tariff. TMR-3/043 had already shown batch physical activation, and TMR-3/047, TMR-4/048, TMR-5/044 and TMR-1/048 independently scoped preauthenticated one-use, mixed-width and repeatable fusion record calculi. This result does NOT modify their legal rule sets. Its new contribution is an exact physical *unequal head-distance* joint tariff and a matching one-fixed-controller service, with an audited same-realization visited-writable-space measure.

## 2. Qualified concrete system

A fixed finite-alphabet machine has one read-only input tape with one locally moving head, and **two individually headed writable tapes** designated as mandatory physical outputs. All three heads begin at cell 0 of the service suffix. The input is a filler prefix followed at cell d0>=0 by an authenticated terminal symbol E0 or E1. Each output tape i=1,2 initially has an **already staged** distinct target marker @ at cell di>=0 and blanks otherwise, with contents independent of E0/E1. The successful task is to read that original source symbol, overwrite each of those two physically distinct target cells with the source bit, and halt. No substitute pointer, reference or compressed output meets this particular service contract.

**Critical scope:** the staged markers on writable tapes are NOT a standard free blank-work-tape initial condition. Their creation and any source-index conversion must be charged in a whole-program construction. This theorem concerns a precisely described physically reachable/prepared service *suffix*, not a blank-start SAT machine. The fixed program used for the upper bound reads actual @ and E0/E1 markers, not unbounded integers or length-specific advice.

A genuine transition costs exactly one: inspect the symbols under all heads, write each current writable cell, independently move each head left, right or stay by at most one, and change control state, potentially HALT, all in ONE unit-price step. Extra work tapes, caching, source rereads, overwrites, long detours, re-computation and arbitrary control changes are allowed and charged as additional authentic transitions. A complete concrete configuration stores all tapes, heads, control, immutable source and a ghost history bit s recording whether the source position d0 has ever been inspected. The ghost is an analysis annotation, not machine advice. Define gi=1 precisely when output tape i's physical target cell currently equals the source bit.

There are no authentic physical cost-zero machine transitions. Optional abstract VIEW/VIEW^-1 changes only an inert metadata view v at zero charge. Its exact two-view SCC keeps all tape contents, heads, original source, s and gi unchanged, hence the obstruction is invariant. Unknown operations not covered by this *specific* physical model remain MAY outside the qualified service.

## 3. Seven-component signed tariff theorem

For any complete state C define:

$$
a_0=(1-s)(|h_0-d_0|+1),\qquad
a_i=(1-g_i)(|h_i-d_i|+1),\ i=1,2,\qquad
m=\max\{a_0,a_1,a_2\}.
$$

These quantities are nonnegative; source observation, output correctness and current local heads are genuine state/history facts. The canonical seven-component reduced product is

$$
\mathbf p(C)=(p_{\rm CNF},p_\oplus,p_{\rm SEP},p_{\rm FUS},p_\Gamma,p_{\rm Interface},p_{\rm Machine})
=(0,0,0,a_1,a_2,a_0,m).
$$

For EVERY genuine machine transition C to C', regardless of extra computation or tape contents, each signed discharge satisfies a_i(C)-a_i(C')<=1. If a task remains unfinished, its local head decreases distance by at most one. When a task first completes, its required input read or target output write must occur at the target, where the previous a_i equals exactly one. An erasure of a correct output may increase a_i (negative discharge); it cannot overcharge. The elementary maximum inequality implies m(C)-m(C')<=1, even if several a_i decrease simultaneously. Thus the exact rational certificate

$$
\lambda=(0,0,0,0,0,0,1)
$$

has lambda^T Delta<=1 for every genuine paid step; VIEW has Delta=0 and cost 0; every completed goal has potential m=0.

**Exact all-state active coefficient cone:**

$$
\boxed{\lambda_{\rm FUS}+\lambda_\Gamma+
\lambda_{\rm Interface}+\lambda_{\rm Machine}\le1,\quad\lambda\ge0.}
$$

Sufficiency follows by summing the four componentwise one-step upper bounds. Necessity uses a genuine local transition with all three heads poised over their targets, source not previously read, and two incorrect target cells. That ONE transition reads E_x, co-writes both correct outputs, and may HALT. Its seven-component discharge is EXACTLY (0,0,0,1,1,1,1) at price 1. The smallest legal instance uses d0=d1=d2=0. Independent unit tariffs would charge three (or four including m) for one authentic operation. No CEGAR may remove this true execution.

The complete signed row classes, including source authenticate, correcting each target, move closer, move away, erasure after correctness, all simultaneous combinations, source reread, cache, control, non-target write, HALT and inert VIEW, appear in the machine-readable exact tariff matrix. Every physical step is reduced to these factual updates; the abstraction does not assert a source-dependent SAT/proof calculus.

## 4. Quantitative lower bound and a ONE fixed uniform matching machine

Let D=max(d0,d1,d2). For any fixed deterministic total service program correct on *both* E0 and E1, its physical source head must inspect position d0 on each input: otherwise those inputs produce indistinguishable read histories and cannot emit distinct mandated output bits. Reaching and reading it requires d0+1 transitions from head cell zero. Independently, the output i head must reach cell di and actually overwrite its unique mandatory target, which requires di+1 transitions. These three obligations can run concurrently, so their valid joint bound is their MAXIMUM:

$$
\boxed{\forall A\text{ correct on both source labels},\quad T_A(d_0,d_1,d_2,x)\ge D+1.}
$$

One fixed finite-control two-output-head program achieves **exactly D+1 steps on every distance triple and both source values**: sweep all heads to their visible target markers, leave any early output head parked at @, read E_x as soon as the source head reaches it and retain x in finite control, write each physical target once its head is on @ and x is available, and HALT in the final coincident read/write step. No advice depending on distances or growing number of tape heads is used. The program works because all tape symbols under all heads are visible to each synchronous transition.

Both outputs' physically visited writable cells are simultaneously counted, separately per tape:

$$
\boxed{T_{\rm sweep}=D+1,\qquad S_{\rm visited,writable}=(d_1+1)+(d_2+1).}
$$

This work-space pair refers to THE SAME prepared-suffix execution. Every correct program with the two designated physical targets must visit at least d_i+1 cells on each of their tapes, regardless of any extra work tapes. Read-only input cells are excluded. This uses a declared visited-writable-cell metric; traditional space conventions that exempt designated write-only output tapes are not silently substituted. If initially staged @ cells were created earlier, staging must also be counted for any whole-machine time bound. Multiple work heads supply simultaneous physical write bandwidth, NOT cost-free parsing or superconstant time compression from a growing number of tapes.

For a prepared initial state, all three a_i equal di+1 and m=D+1. The exact nonnegative LP maximize lambda^T p(C0) over the above active cone has value **D+1**, attained by lambda_Machine=1. Its dual is the cost-one simultaneous-discharge constraint with right hand side D+1, and the uniform physical sweep attains that value in real transitions. This is an exact same-realization local resource statement, not a general SAT lower bound.

## 5. Complete cost and hostile-control ledger

| Resource | Qualified audit |
|---|---|
| Logical obligations | One authenticated original source-bit observation, and TWO physically distinct output writes; they may coincide in one real transition. |
| Elapsed time | Exactly D+1 physical microsteps for the matching fixed sweep; >=D+1 for every correct program. |
| Parallel span | D+1 synchronous rounds; do not sum simultaneously headed operations as sequential time. |
| Evidence bits | One actual source bit reused twice, two materialized output bit symbols; unary target-marker placements are extra PREPARED context. |
| Messages | Zero; one machine with constant number of tapes. |
| Live retention | A source bit and fixed number of arrival/done flags in finite control; no variable-size auxiliary cache. |
| Peak visited writable space | Exactly (d1+1)+(d2+1) in the monotone sweep on two required output/work tapes. |
| Retrieval, recomputation, deletion, rereads | Every microstep is paid; signed negative discharges occur when outputs are erased or heads retreat. |
| Indices, buffers, address authentication | Targets are physical @ cells already staged. Constructing markers and parsing original-source index encoding MUST be charged in a blank-start compiler. |
| Definitions, interfaces, branch AND obligations, joins | Not present as proof obligations in this service; no claim these are covered for SAT. |
| Shared identities | One genuine source observation may support two different physical writes; source authentication is counted ONCE, outputs are each mandatory cells. |

Mandatory controls: d=(0,0,0) displays the smallest full fusion; unequal distances reject the false additive tariff; negative discharges from head backtracking and output erasure are legal; a compact pointer does not meet the two-cell physical-output contract; arbitrary extra head motion and rereads cannot improve the distance barrier; an arbitrary family of SAT instances with just one yes/no output is NOT this service. The number of tapes is fixed. Taking it to grow with input length is a new machine model.

## 6. Evidence, source scope and next target

Actual native Node 22 deterministic run: 64,000 fully enumerated abstracted physical states for target distances 0..3, head positions 0..4 and all source-observation/output-correctness flags; **2,725,632 genuine price-one microtransition rows**, **64,000 zero-price inert metadata rows**, **16,489,200 assertions**, zero failures. Exhaustive different-distance fixed-sweep runs over 0..12 for each distance and both bits: **4,394 complete traces**, **44,954 paid rounds**, exact output and visited-space checks in each. The row generator admits arbitrary current-target symbol corrections and erasures, all signed local head moves, and all cost-one control/nontarget operations. No random seed. Finite results COMPUTATIONAL; symbolic inequalities proved above. This is not a compiled physical TM transition table, and does not run a SAT program.

Read in order: governing fusion tariff directive SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; TMR replacement directive; complete proof1, proof2 and root main.tex blobs; issue #3; AGENTS.md, CODEX.md and repo skill; all five active TMR handoffs; original TMR-3/042, /043, /047 and TMR-1/048, TMR-4/048, TMR-5/044 reports/code/result matrices. External scope check: Lean cslib visited-work-tape definition https://api.cslib.io/docs/Cslib/Computability/Machines/Turing/MultiTape/Space.html, noting our explicitly INCLUDED writable output tapes are a different convention. The scoped theorem is elementary and independently proved here, not asserted as new primary literature.

Files:
- research/agents/tmr-3/2026-11-15_0928_TMR3_PHYSICAL_MULTIHEAD_FRONTIER_TARIFF048.md
- experiments/tmr/tmr3_multifrontier148.js
- results/raw/tmr/2026-11-15_0928_TMR3_PHYSFRONTIER148_NODE_RAW.json
- results/raw/tmr/2026-11-15_0928_TMR3_PHYSFRONTIER148_TARIFF_MATRIX.json

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex and proof1/proof2 untouched. /341 full logical authority FAIL, /386 guarded odd-charge authority RESTRICTED, no historical repair. No schedules altered. **Unrestricted SAT decider transfer OPEN; fusion-safe superpolynomial initial gap OPEN; P versus NP OPEN.**

**Next:** compile a truly blank-work-tape version with charged target-marker setup and original SAT source indexing, and independently audit which concurrent fusion operations survive the physical interface.

END_OF_VERIFIED_REPORT::TMR3::PHYSFRONTIER148::2026-11-15_0928_PST