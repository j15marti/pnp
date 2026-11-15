# TMR-3/045: Exact online head-reversal gap for a uniform physical staged-record service

**2026-11-15 06:37 PST (America/Los_Angeles).** TMR-3, PNP Time-Space Tradeoffs. Governing five-agent fusion-Lipschitz directive: \`research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md\`, Git blob \`54c9177fc211dfca6c94d89d6ebbf3f3908809d6\`.

**Status:** **PROVED/RESTRICTED** for the precisely specified unary service, with independent mathematical review **OPEN**. Native V8 simulator tests **COMPUTATIONAL**. No superpolynomial SAT lower bound, no same-system SAT transfer. **P versus NP OPEN.**

## 1. Candidate and four predeclared falsifiers

**Candidate.** The one-step gap left by TMR-5/041 is a quantifier distinction. For the same fully ordered physical service, the **pointwise** minimum over eligible programs at each source length is exactly **2n**, but no single uniform program can attain 2n on two different input lengths. Therefore every uniform eligible program costs at least **2n+1 on all but at most one length**, and TMR-5's fixed 2n+1 program is asymptotically optimal with additive slack exactly one.

(F1) A purported 2n run writes a distant W cell without first moving the single W head to it, or skips paid W[0] activation / separate HALT. (F2) Two optimal lengths have distinguishing source symbols before the forced reversal. (F3) The length-k specialized fast program uses a free lookahead, teleports to reset, writes two cells on one tape per step or fails on other unary lengths. (F4) The pointwise program choice is treated as one uniform SAT machine, or the protocol's header/gate ordering is secretly removed. All four are ruled out in the declared scope; an unrestricted SAT implication remains OPEN.

## 2. Corpus reconciliation and primary literature

Read **FIRST** the governing fusion directive, then TMR replacement directive, both root proof trackers, root \`main.tex\`, issue #3 and latest comments, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, all five current TMR handoffs, and the materially relevant original TMR-3/044, TMR-4/045, TMR-5/041 and TMR-1/045 reports, code/data provenance and historical Lipschitz audit. The authentic large tracker and canonical manuscript were recovered using complete Git blobs rather than interpreting the ordinary oversized contents API's empty response as empty. Current root blob identities examined: proof1 \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`, proof2 \`930c5eeddafce656717f28055a7a9a755f44737c\` (1,051,196 characters), and main.tex \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\` (2,545,859 characters). No root document write is authorized or attempted.

The **new** part is the precise pointwise-versus-uniform optimality theorem and its honest finite-state recovery program, not another proof of the previously reported 2n geometric bound or 2n+1 fixed upper. Hennie and Stearns, *Two-Tape Simulation of Multitape Turing Machines*, JACM 13 (1966), DOI [10.1145/321356.321362](https://doi.org/10.1145/321356.321362), provides machine-model context, **not** this elementary online lower bound. Hartmanis and Stearns, *On the Computational Complexity of Algorithms*, Trans. AMS 117 (1965), DOI [10.1090/S0002-9947-1965-0170805-7](https://doi.org/10.1090/S0002-9947-1965-0170805-7), contextualizes uniform machine quantifiers. The proof below is self-contained. No simulation theorem or communication lower bound is imported across a machine model.

## 3. Exact unchanged physical model and ordered obligations

Fix one number m>=1 of independent marker-output tapes, not dependent on n. The original read-only input is \`1^n#\` with n>=2. One original input head, one W staging-tape head, and m independent marker-tape heads all start at cell zero. W and all marker tapes are initially blank. Each single physical unit-cost transition reads symbols under its heads, writes **at most one scanned cell per distinct writable tape**, and moves each head by at most one cell. It may read input, write W and m markers, change phase and halt **simultaneously**, without charging these subactions again.

The ordered service requires: W[0] is physically written \`0\`; every W[j], 1<=j<n, receives its own paid \`g\` write; **after** every gate has been written, a later nonterminal physical transition changes W[0] from \`0\` to \`1\`; all m O_i[0] cells contain \`@\`; original input \`#\` at position n is actually inspected; a separate **later true HALT transition** occurs. One W head must physically return to zero for activation. Gate identities are count-once, even if a rejected speculative path later overwrites or erases them. The task is an explicitly **ordered materialization protocol**, not ordinary SAT and not TMR-4's weaker extensional-output service.

Let T_A(n) be the number of paid microsteps of a **single fixed deterministic finite-control program A** that fulfills this service for **every** n>=2 in the promised unary language. Writable visited cells are counted separately from transitions. No input-length oracle or second source head exists.

## 4. Sharp universal geometric bound

**Theorem A (PROVED/RESTRICTED).** Every eligible program A and every n>=2 obey

$$
T_A(n)\ge 2n.
$$

**Proof.** Let t_g be the step in which W[n-1] first receives the final required gate write before activation. Starting with the one W head at cell zero and allowing at most one move per paid step, the head cannot scan n-1 early enough to write it before step n. Thus t_g>=n. Immediately after that write its head is at distance at least n-2 from cell zero. It therefore requires at least n-2 further paid steps to reach zero and then a **distinct** activation step; finally a **distinct later** HALT is mandatory. Hence T>=t_g+(n-2)+1+1>=2n. Other heads, buffers, caching, sharing and recomputation cannot move the one mandatory W head faster. Simultaneous authentic input reads and marker writes are allowed throughout. QED.

**Forced equality geometry.** If T_A(n)=2n, every inequality above must be tight. In particular, W moves **right on each of the first n-1 steps**, scans W[n-1] at step n, writes g and **moves left on that very step**; it subsequently travels left with no delays, activates at step 2n-1 and truly halts at step 2n. No alternative motion schedule achieves equality.

## 5. New online indistinguishability theorem

**Theorem B (PROVED/RESTRICTED).** For every fixed correct uniform eligible A, the set

$$
E_A=\{n\ge2:T_A(n)=2n\}
$$

has cardinality at most one. Consequently

$$
\forall A\;\exists n_A\;\forall n\ge n_A:\quad T_A(n)\ge2n+1.
$$

**Proof.** Suppose n<r are both in E_A. The forced equality geometry for input length n makes W move **left** on physical step n. The forced equality geometry for length r makes W move **right** on every step before r, including step n. However, before and during step n the single original input head cannot have inspected beyond source position n-1, since it starts at zero and moves at most one cell per transition. Every original source symbol it can observe is \`1\` on **both** \`1^n#\` and \`1^r#\`. All work tapes and control start identically, so deterministic induction makes their first n microsteps, including W's move on step n, identical. They cannot move W both left and right. Contradiction. Since integer step counts are at least 2n, every length except at most one requires 2n+1 or more. QED.

This is stronger than a neighboring-length argument: **no fixed correct program achieves geometric equality at two distinct lengths**. In particular it does not depend on programs being online by declaration. Online inability to know the source's end before actually reading \`#\` is derived from authentic head locality.

## 6. Constructive pointwise upper and exact uniform envelope

**Theorem C (PROVED/RESTRICTED).** For each fixed k>=2 there exists an eligible finite-control program A_k that works on **all** unary lengths n>=2 and performs exactly T_Ak(k)=2k transitions on its selected input. However the program depends on k, so these separate programs are not one uniform length-independent family realization.

**Construction.** A_k encodes k in its finite control. On a matching prefix it writes W[0]=0 and moves W right on the first source 1, writes gates at W[1] through W[k-2] on the next source 1s while moving right, then on the kth source 1 writes the final W[k-1]=g and *speculatively reverses* W left. On the next actual physical transition it reads input position k. If it is truly \`#\`, it continues moving W left (k>=3) and eventually activates W[0] after the final gate; for k=2 it **fuses EOF inspection and nonterminal activation** on the same step. A distinct HALT follows. The step count is 2k.

If any source position does not match the guessed \`1^k#\`, the machine takes a real priced mismatch step. It physically returns its W head to the fixed location k, sweeps left erasing its speculative W records, moves the original input head left to position zero with ordinary unit steps, clears W[0] and invokes the **uniform** TMR-5/041 M_EOFWRITE_m routine from genuinely clean tapes. No marker is written before the correct activation. The program is finite and total on the unary promise for **every** source length; its reset has O(k) finite-control states and takes only priced physical transitions. This is *not* a free path, and it has no polynomial-time SAT correctness claim outside the unary service.

The uniform M_EOFWRITE_m (already TMR-5/041) performs exactly 2n+1 authentic transitions on every n>=2. Combining A, B, C:

$$
\boxed{\inf_{A\;\mathrm{uniform\ eligible}} T_A(n)=2n
\quad\hbox{for every fixed }n\ge2,}
$$

and

$$
\boxed{\inf_A\sup_{n\ge2}\bigl[T_A(n)-2n\bigr]=1.}
$$

The infimum on the first line is **pointwise**, choosing a potentially different program A_k for every n. The second line selects one fixed program for **all** n; M_EOFWRITE_m attains additive gap one, and Theorem B excludes gap zero.

## 7. A complete signed seven-component tariff slice, scoped to the fast branch

For the **length-k successful fast branch of A_k only**, define phase-sensitive obligations after authentic physical zero closure (all real transitions cost one, so zero-cost SCCs are singletons):

$$
\mathbf p(C)=
(0,0,0,f(C),g(C),i(C),d(C)+h(C)).
$$

Here f is the number of two outstanding *physically distinct* W[0] writes (initial 0 and subsequent 1); g is the number of missing distinct W[j]=g writes; i is the number of original unread cells among positions 0..k, including #; h=1 before the separate true HALT and 0 afterward. For fast-branch phase states, d=k-2 until the last gate write and thereafter equals the actual W-head return distance to zero, reaching zero by ACT. This is an authenticated **phase-gated** debt definition, not a free physical distance oracle. The initial vector and completed goal are

$$
\mathbf p(C_0)=(0,0,0,2,k-1,k+1,k-1),
\qquad \mathbf p(C_{\mathrm{goal}})=0.
$$

Every genuine fast-branch row has price one. Abbreviating columns to (FUS,Gamma,Interface,Machine):

| Concrete rule / precondition | Signed discharge | Multiplicity k>=3 | k=2 |
|---|---|---:|---:|
| FAST_INIT: first 1, W0=blank, write W0=0, W right | (1,0,1,0) | 1 | 1 |
| FAST_GATE: interior original 1, W[j]=blank, write g, W right | (0,1,1,0) | k-2 | 0 |
| FAST_LAST_GATE: kth original 1, W[k-1]=blank, write g, W left | (0,1,1,0) | 1 | 1 |
| FAST_EOF_BACK: genuine # at k, W>0, W left | (0,0,1,1) | 1 | 0 |
| FAST_BACK: W>0, W left | (0,0,0,1) | k-3 | 0 |
| FAST_ACT: W0=0 after all gates, write 1 and m distinct @ markers | (1,0,0,0) | 1 | 0 |
| FAST_EOF_ACT: only k=2, source # with W0=0 after final gate, activate and mark | (1,0,1,0) | 0 | 1 |
| FAST_HALT: READY, after activation, truly halt | (0,0,0,1) | 1 | 1 |

Unlisted coordinates CNF/XOR/SEP are zero; no symbolic semantics of these is charged. Repeated symbol reads after EOF, source rereads, actual head return, marker writes, final output and HALT are paid in real steps even when their **separate tariff weight is zero**. The separate m markers are emitted simultaneously on m distinct tapes, not m writes to one tape.

For k>=3 the exact nonnegative fast-branch cone includes

$$
f_\lambda+i_\lambda\le1,\quad
g_\lambda+i_\lambda\le1,\quad
i_\lambda+t_\lambda\le1,\quad
t_\lambda\le1,\quad f_\lambda\le1.
$$

For k=2 replace the EOF_BACK plus ACT inequalities by the authentic fused FAST_EOF_ACT constraint f_lambda+i_lambda<=1. The exact rational certificate, in seven-column order, is

$$
\boxed{\lambda=(0,0,0,1,1,0,1),\quad
\Phi(C_0)=2+(k-1)+(k-1)=2k.}
$$

All fast-path rows satisfy \`lambda^T Delta <= 1\`. Their actual occurrence counts form a **matching exact primal/dual row cover**: weighted discharges sum to 2k and the physical row costs sum to 2k. No gate is charged twice and all completed fast-path obligations vanish. These constraints have been given to TMR-4's exact-rational LP work as a versioned machine-readable matrix.

**Critical model boundary:** This is **not** asserted to be a full all-step tariff for A_k's reset and fallback or an all-machine SAT tariff. Those genuine reset/rewrite transitions remain permitted MAY behavior and must be added with their signed deltas before any program-wide extension. Importing this phase-sensitive cone into another program without its complete transition inventory is forbidden. The all-program Theorems A and B above are proved directly by W-head geometry and deterministic prefix indistinguishability, independently of this restricted LP.

## 8. Same-machine resource accounting, controls and test evidence

On successful length k, sequential time **2k**, parallel span **2k** (one deterministic processor), distinct input cells first inspected **k+1**, repeated input scans **k-1** (the input head remains on # during return/ACT/HALT), physical W cells visited and retained **k**, m distinct marker cells **m**, peak visited writable space **k+m**, distinct mandatory gate identities **k-1**, one staged W header with an additional activation rewrite, **zero intermachine messages**, and no gate recomputation. The concrete emulator records all transition/read/write/head events. On mismatch, every speculative write, reset/erase, retrieval and fresh input scan is charged; no failed branch is discarded for free.

**Actual native V8 test:** \`experiments/tmr/tmr3_unary_online_reversal109.js\`, same self-contained \`audit()\` function executed before publication. Across k=0 (uniform baseline), 2..18, m=1..3 and n=2..42, plus five extra exact tariff calibrations at k=2,3,4,7,18: **2,219 complete runs**, **651,656 instrumented assertions**, **147,791 authentic price-one transitions**, **2,040 charged reset/fallback runs**, **56 successful targeted fast runs**, and **zero failures**. All mandatory stage/gate/activation/EOF/HALT obligations, tape contents, physical locality and count-once gates are checked. The exact row audit has matching primal and event-count dual for each calibration. This finite replay is **COMPUTATIONAL** and is not a compiled low-level Turing-machine implementation or an exhaustive proof over all n/programs.

Hostile controls: alternative early-header/direct-output ordering changes the problem and yields TMR-4/045's genuine n+1 path; a second original-input head or indexed/random-access port is a new machine interface; an input-length hint is explicitly **nonuniform** and belongs only to A_k; every failed speculation is fully paid; changing k at every length is not one uniform decider; circuit/XOR/Gaussian, Horn, Krom, separator, shared DAG, autarky, renaming, padding, caching, recomputation and learning remain available to unrestricted SAT solvers and are not forced through this unary materialization service. Historic checker /341 remains **FAIL** as full-language logical UNSAT authority; /386 remains **RESTRICTED** and neither is repaired.

## 9. Dependency map and peer handoff

| Claim | Result |
|---|---|
| Ordered service mandatory W-head travel 2n lower | PROVED/RESTRICTED (prior TMR-3/044, independently reproved) |
| One fixed M_EOFWRITE_m takes 2n+1 for all n | PROVED/RESTRICTED (prior TMR-5/041; independent fast baseline replay) |
| Pointwise eligible-machine optimum is 2n for each fixed n | **NEW PROVED/RESTRICTED; independent peer review OPEN** |
| A single eligible uniform machine is 2n-optimal at no more than one n | **NEW PROVED/RESTRICTED; independent peer review OPEN** |
| Uniform eventual additive minimum equals 1 | **NEW PROVED/RESTRICTED; independent peer review OPEN** |
| Fast-branch seven-column exact tariff and matching rational primal/dual | **NEW PROVED/RESTRICTED; entire fallback cone NOT claimed** |
| Unrestricted SAT-machine superpolynomial obstruction and same-system transfer | **OPEN** |
| P versus NP | **OPEN** |

**What changed relative to root main:** A new sharp **online/uniformity** quantifier distinction, replacing the ambiguity of \`2n <= OPT_ORDERED(n) <=2n+1\` with the two correctly different optimization objectives. No existing fixed-program TMR-1/044, TMR-5/041 or TMR-4/045 claim is invalidated. No root tracker or manuscript status is promoted. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

**Next single target:** TMR-4 independently verify Theorems B/C and model the paid fallback as MAY without reusing the fast-only tariff; TMR-5 independently seek a second uniform length attaining exactly 2n, or an illegal hidden input peek in the speculative program. Then move beyond the mandatory materialization protocol to an authentic charged source parser or SAT recognizer whose dynamic obstruction is not equivalent to input access alone.

## Published evidence

- Executable native JS: \`experiments/tmr/tmr3_unary_online_reversal109.js\`
- Immutable raw assertions/traces: \`results/raw/tmr/2026-11-15_0637_TMR3_ONLINE_REVERSAL109_V8_RAW.json\`
- Seven-component rule tariff: \`results/raw/tmr/2026-11-15_0637_TMR3_ONLINE_REVERSAL109_TARIFF_MATRIX.json\`

END_OF_REPORT::TMR3/045::ONLINE_REVERSAL109::2026-11-15_0637_PST
