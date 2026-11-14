# TMR-5/016: Independent TMR-4/019 mirror-tape audit and fixed-offset extension

**Pacific timestamp:** 2026-11-14 04:59 PST (America/Los_Angeles). **Role:** TMR-5 Machine Bottleneck Redteam and whole-document synthesis. **Peer verdict on original TMR-4/019:** PROVED/RESTRICTED under its exact model, preserving two physical tape heads and visited-cell charges. **New TMR5-SM16 extension:** CANDIDATE/RESTRICTED pending independent TMR-1/TMR-4 mathematical review. **Native and hosted tests:** COMPUTATIONAL only. **General SAT lower bound:** OPEN.

## 1. Original material and precise claim under audit

Read the original report [TMR-4/019](../../agents/tmr-4/2026-11-14_0447_TMR4_INDUCTIVE_MIRROR_CERTIFICATE019.md), its independently authored original [source](../../../experiments/tmr/tmr4_inductive_mirror019.cjs) and [raw evidence](../../../results/raw/tmr/2026-11-14_0444_TMR4_INDUCTIVE_MIRROR019_RAW.json). It proposes a finite, all-symbol, on-diagonal certificate: if full writable tapes B,C initially agree cellwise and their physical heads align, and every diagonal transition writes equal symbols and moves both heads equally, then B's symbol values can be discarded while a charged dummy tape remains. All original source reads, other tapes, control, terminal labels, and visited-cell footprints are retained.

**Independent verdict:** valid as a restricted exact-replay theorem, not as a requirement applying to arbitrary 3-SAT machines. This audit independently checked the initial and terminal bindings, every transition type, the original parity-gated optional detour, source-cell timing and all six phase-potential expressions. An off-diagonal gate pair (b=1,c=0) is a genuine failure of unrestricted symbol erasure, but it is unreachable from the blank mirrored initial state under the verified inductive condition. Its cheap MAY path is replay-spurious, so restricting to the inductive diagonal does not delete any real execution. The physical dummy tape MUST remain to claim identical visited-work-cell space.

## 2. New strictly broader fixed-offset invariant

Let A be one fixed finite total deterministic multitape machine on every input length. In a certified phase region, designated writable tapes B,C have the same finite alphabet and a **fixed integer offset d>=0** satisfying, over all cell indices j,

$$
I_d(c):\quad h_C=h_B+d,\qquad B[j]=C[j+d].
$$

All other control, immutable source x, input-head positions, work contents, other work-head positions, and visited-cell histories are retained exactly. Fix d in the finite machine description, not as size-dependent advice. The offset need not be zero.

**Effective sufficient local certificate.** For every certified control state, every original source-symbol vector, every other writable scanned tuple, and every diagonal pair of scanned B,C symbols (which are equal by I_d), require the same B,C write symbol and the same signed one-cell head displacement. Demand that all remaining actions and terminal outputs be retained exactly, without an oracle or chosen proof calculus. The check is finite over the machine's explicit instruction table. It may reject semantically safe programs and does not decide reachability.

**Theorem TMR5-SM16 (new CANDIDATE/RESTRICTED, mathematical proof supplied):** If the region is entered only through a separately audited exact prefix that establishes I_d, and its transition-table certificate holds for every eligible control/symbol tuple, erasing all symbol contents of B while keeping a charged dummy B tape and both physical work heads gives a source-bound quotient with cost-one two-way strong simulation on every related state. For any actual execution, source, SAT/UNSAT/MALFORMED terminal output, step count T, and peak visited writable work-cell count S remain identical.

**Proof.** At the certified entry, the entire functions B[j],C[j+d] and both heads satisfy I_d. Their scanned symbols coincide. The diagonal certificate gives identical written symbols at the corresponding cells and identical head displacements, so I_d holds after every concrete legal transition. The entire unscanned tape remains equal by shift. The projected abstract state contains C and h_C,h_B,d, so for each j it uniquely recovers the erased B[j]=C[j+d] on the certified relation. Hence every concrete transition maps to exactly one cost-one abstract transition; every related abstract transition replays to a unique concrete successor under the same source and control. Source reads are still the actual current input-head symbols. Exact terminal labels and all physical head trajectories are unchanged. Since the B dummy tape retains its original head and physical visited set, S is equal rather than merely bounded. Induction proves execution- and terminal-exactness for both labels and malformed strings. No global SAT theorem or uncharged semantic reconstruction is used.

**Strict improvement over TMR-4/019:** aligned-head certificate rejects d=1 even though the shifted relation is exact. A fixed d-step physically charged prefix can move C from the ordinary initial work-head position 0 to d while both blank full tapes satisfy B[j]=C[j+d]. During this prefix the quotient preserves both original heads and steps and erases only an unused B symbol. The entry relation then holds. After the entry, the finite shift certificate applies. The prefix is necessary if both ordinary blank work heads are initially at 0. For d>0 the original aligned-head condition fails, so the extension is nontrivial. No transition in the prefix is omitted.

**Cost warning:** The abstract retained C tape at position j+d is a logical relation used to certify the quotient, not a free translation executed by a new SAT solver. If one implements a new ordinary machine requiring physical C-head repositioning rather than maintaining the certified head offset, every repositioning step must be charged. Here C is already at j+d on every actual trace. In general, an arbitrary A need not admit any such relation.

## 3. Independent physical controller with exact potential

Construct a fixed local-input-head controller for each fixed d. Start with B and C blank, both heads at 0, and spend exactly d physical transitions moving C's head right; B stays at 0. The original single input head stays at left. During the source parity scan, write XOR parity at B[0] and C[d] on each read data bit. Both tapes remain shifted mirrors; subsequent gate reads B[0] concretely and C[d] abstractly. If parity is odd, execute a physical optional outward/return detour. Rewind and parse triples of literal-sign bits into an eight-bit exclusion mask, reporting SAT if at least one of eight assignments survives, UNSAT otherwise, and MALFORMED if incomplete. The restricted sign-stream is NOT unrestricted NP-complete 3-SAT.

Write q=L+1, z(x)=XOR of source bits, and p for the actual source-head position. The exact trace and writable visited-cell charges are

$$
T_d(x)=d+3q+1+2qz(x),\qquad S_d(x)=d+2.
$$

The source-aware abstract graph retains x, correct prefix parity, physical head positions, the surviving C symbol, source parser and exact halt label. Extend TMR-4's Bellman potential by bootstrap states U(r) with r moves remaining:

$$
\Phi(U(r))=r+3q+1+2qz(x).
$$

In each phase below, q and z(x) refer to this same immutable x:

$$
\begin{aligned}
\Phi(S,p)&=3q-p+1+2qz(x),&
\Phi(R,p)&=p+q+1+2qz(x),\\
\Phi(D,p)&=3q-p+1,&
\Phi(E,p)&=p+q+1,\\
\Phi(A,p)&=q-p+1,&
\Phi(H)&=0.
\end{aligned}
$$

Every legal abstract edge, including all d bootstrap movements, gate branches, the source-right-end transitions, and the SAT/UNSAT/MALFORMED terminal, has cost exactly 1 and satisfies Phi(pre)=1+Phi(post). Therefore Phi(start)=T_d(x). This is an **O(L+d)** candidate for each fixed d, not a superpolynomial potential. The use of z in a mathematical, source-bound certificate is not an algorithmic zero-cost SAT oracle.

**Hostile off-invariant test:** At a physical gate configuration with B[0]=1 and C[d]=0, replacing B with C skips 2q genuine transitions. Such a concrete configuration is outside I_d and cannot arise from the certified initial/prefix conditions. The original unconstrained MAY quotient would include the fake skip. The source-aware inductive quotient rightly excludes it. This differs categorically from the historical original-checker accepted literal-order cost aliases: those are real accepted paths and must NOT be discarded as spurious.

## 4. Executed evidence, independence and limits

**New direct hosted-V8 implementation, independently written rather than calling TMR-4/019:** [source](../../../experiments/tmr/tmr5_shifted_mirror_redteam016.cjs), [raw](../../../results/raw/tmr/2026-11-14_0458_TMR5_SHIFTED_MIRROR016_RAW.json). Executed 6,168 complete traces with shifts d=0,1,2,3,4,7, 249,502 actual and abstract charged transitions, 249,502 Bellman edge checks, 3,534 SAT / 6 UNSAT / 2,628 MALFORMED, 18 off-invariant hostile gate witnesses with 192 omitted physical transitions, zero failures. Distinct abstract and concrete state updates and full tape-shift/head/cell checks were used.

**Independent native CPython implementation, locally executed (not shared to GitHub):** 12,330 traces for the same six shifts, 548,385 concrete and abstract steps, 548,385 Bellman equalities, 3,534 SAT / 12 UNSAT / 8,784 MALFORMED, 24 off-invariant witnesses with 528 omitted steps, zero failures. Local exact source and raw remain in this run's container; they are NOT claimed as repository publications. The native implementation uses explicit tape dictionaries and visited-cell sets, not a wrapper around the JS. Both simulations compare source bits through the tracked physical input-head position. Native and hosted workloads differ and their counts should not be expected to match.

Neither implementation compiles the transition table for **arbitrary** multitape machines. Neither tests unrestricted 3-SAT deciders using Horn, 2-SAT, Gaussian elimination, bounded treewidth, sharing, general preprocessing or arbitrary polynomial workspace. Those strategies remain legitimate falsifiers for any universal SAT-hardness claim. The abstract quotient certificate is symbolic for each machine satisfying its stated fixed-shift premise, and finite tests remain COMPUTATIONAL.

## 5. Primary literature and historical control

- Patrick Cousot and Radhia Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints," POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973. Established abstract semantics and fixpoint soundness; does not prove SAT-machine cost lower bounds.
- Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu and Helmut Veith, "Counterexample-Guided Abstraction Refinement," CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15. Refines replay-spurious paths under concrete checks, not genuine accepted computations.
- Fortnow, Lipton, van Melkebeek and Viglas, "Time-space lower bounds for satisfiability," JACM 52(6):835-865 (2005), https://doi.org/10.1145/1101821.1101822. Random-access time-space exclusions assume sufficiently small workspace at specific fixed time exponents; they do not exclude every arbitrary polynomial-workspace solver.
- Original project record: [LSPV-5/523 accepted order alias](../../coordination/2026-11-13_0210_LSPV5_ACCEPTED_ORDER_ALIAS_FIVE_ROLE_HANDOFF523.md), together with original checker-driven source experiments/arc/lspv5_523_accepted_order_alias.cjs. That unrepaired acceptance is real; its old role allocations have been superseded.

Original TMR-4/018, TMR-1/017 and TMR-3/017 original reports/code were read. TMR-3/017's source-replay caching achievability permits full-source retention at R=L+2 with T_B=O(L+T_A) and extra S_B=O(L), so compulsory repeated input rereading cannot be inferred. Its generic compiler is still symbolic and unreviewed here. TMR-1/018 and TMR-2/018 establish that exponential padding and almost-complete syntax-bit reads can coexist with polynomial time in the padded length, not a shortcut on an honest standard encoding.

## 6. Integrated dependency chain and next target

1. **PROVED/RESTRICTED peer review:** TMR-4/019 has an exact all-transition, both-label physical-tape quotient for the specifically certified mirrored-tape programs. It is a safe *upper/identity* cost-model transformation, not a SAT lower bound.
2. **CANDIDATE/RESTRICTED new proof:** fixed-offset mirror certificate d adds genuinely unaligned heads, charged d-step bootstrap and retained actual dummy tape; request independent TMR-1/TMR-4 review before promotion.
3. **COMPUTATIONAL:** direct hosted V8 and independent native CPython finite tests, without a compiled universal TM instruction interpreter.
4. **OPEN:** an abstraction covering every correct uniform deterministic SAT machine that derives a noncircular superpolynomial Phi(start), accounting for all source reads, compact representations, sharing, caches, polynomial workspace and actual steps. Every fixed d here gives only O(L) initial Phi.
5. **OPEN:** the all-A, all-k separation quantifier for ordinary honest 3-CNF encoding; no inequality established here excludes any polynomial-time correct SAT machine. A general polynomial-time algorithm remains an acceptable alternative endpoint.

**Reads and mutation discipline:** The authoritative TMR replacement directive was read FIRST, plus both full root trackers (proof2 via Git blob because the file endpoint returns blank), canonical 2,530,965-character main.tex via Git blob, issue #3 through TMR-4/019, root AGENTS.md/CODEX.md/skill, five current handoffs, and materially original abstraction and historical accepted-alias evidence. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** This report requests a cautious TMR-5-owned canonical manuscript synthesis only; do not promote OPEN lower-bound arrows. No scheduled tasks were created, revived or modified.

**Single next target:** Give TMR-1 or TMR-4 an independent finite-table proof audit of fixed-offset mirror induction, then seek a counterexample to any proposed universal post-acquisition distinction cost using same-source fully cached input and a compact GF(2)/Horn/2-SAT simplification.

END_OF_REPORT::TMR-5/016::2026-11-14_0459_PST
