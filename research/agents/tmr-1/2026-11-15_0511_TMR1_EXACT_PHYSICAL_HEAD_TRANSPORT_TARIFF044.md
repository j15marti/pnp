# TMR-1/044: Exact physical source-and-return tariff for the staged gate/marker machine

**2026-11-15 05:11 PST (America/Los_Angeles).** TMR-1 / PNP Machine Model Lead. Governing directive: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md` (blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`). **PROVED/RESTRICTED** exact symbolic theorem in one fixed physical machine; independent mathematical review **OPEN**. Finite tests **COMPUTATIONAL**. P versus NP **OPEN**.

## 1. Candidate and four falsifiers declared before targeted literature/corpus audit

**Candidate:** The genuine fixed multitape `M_STAGE_OUTPUT_m` machine of TMR-5/040 admits a *stronger*, complete seven-column exact-rational potential accounting not only for gate staging and activation, but also source reads and actual reverse-head transport. The resulting certificate exactly matches the machine's full `2n+2` transition count. It should avoid both double-charging synchronous source/gate work and illegally carrying an activated-graph coefficient of one.

Four falsifiers: **F1** a genuine WRITE_GATE reads a new source cell and writes one staged record simultaneously, so separate full weights on both obligations cost two and FAIL; **F2** a genuine EOF_BACK reads EOF and moves the head left simultaneously, so an additional full backward credit on EOF fails; **F3** a real different program, larger tape alphabet/opcode, shortcut, or alternate head policy may complete the same goal faster, destroying any whole-model lower-bound transfer; **F4** a zero-cost operation that advances the proposed progress potential invalidates its zero closure. Here F1/F2 are tested as exact coupled tariff rows, F3 is an explicit transfer gate **OPEN**, and F4 is absent in this specific all-paid microstep system.

## 2. Source recovery and novelty

Read FIRST the fusion refocus, then the 2026-11-13 TMR replacement directive; complete `proof1.txt` SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343` (28,714 chars), complete `proof2.txt` via blob `930c5eeddafce656717f28055a7a9a755f44737c` (1,051,196 chars), complete `main.tex` via blob `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34` (2,545,859 chars), AGENTS.md, CODEX.md, pnp-research skill, five latest TMR handoffs, current issue #3, TMR-1/043, TMR-3/043, TMR-4/044, TMR-5/040 and their source/matrix evidence. The oversized proof2/main contents-file endpoints returned empty strings, so authentic blobs, not fabricated empty files, were used. Historical `/341` remains FAIL full-language, `/386` remains RESTRICTED.

This is **not** a rediscovery of a general time lower bound. TMR-5/040 already established the activated-fusion/output-marker cone and an `n+1` partial potential for this same physical machine. The present theorem specifically adds a program-control-sensitive *source ingress and physical head-return* component, obtains every new exact synchronous tariff row and an exact full-execution primal/dual `2n+2`. The construction is an explicit restricted calibration showing what a real physical transport charge requires; it does not prove such transport unavoidable for every SAT algorithm.

Primary historical context: R. E. Tarjan, *Amortized Computational Complexity*, SIAM J. Alg. Disc. Meth. 6(2), 1985, DOI https://doi.org/10.1137/0606031, discusses amortized resource accounting. Aho and Ullman, *Optimization of Straight Line Programs*, SIAM J. Comput. 1(1), 1972, DOI https://doi.org/10.1137/0201002, illustrates the importance of explicit allowed representation transformations. Neither is attributed this elementary concrete exact-potential theorem.

## 3. Qualified exact physical system, input measure and goal

Fix **m>=1 once** (the number of designated independent output tapes and hence a fixed finite-control multitape program). Every source is the promised unary descriptor `1^n#`, n>=2, with physically encoded length `N_n=n+1` cells. Source is read-only. Stage tape W starts blank; m distinct marker output tapes start blank. Control states INIT, SECOND, EMIT, BACK, READY, HALT, full tape contents, all head locations, paid event identities, original source access history, source provenance and all outstanding interface/goal obligations are part of the concrete state C. Each authentic native step inspects one scanned symbol per tape, writes at most one cell **on each distinct tape**, moves each head by at most one, and costs **one**.

Complete successful-promise transition table: INIT reads first `1`, writes W[0]=0, advances source/work heads; WRITE_GATE reads each subsequent `1`, writes one distinct W[j]=g and advances both heads; EOF_BACK inspects `#` and moves stage head left one cell; BACK_G traverses the n-1 stage records to W[0]; ACTIVATE_AND_MARK writes W[0]=1 plus one marker `@` on each of m distinct output tapes **in one nonterminal step**; HALT enters the actual terminal state in a separate step. Every staged `g` identity is paid exactly once. All steps and head movements are charged even when no proposed obstruction changes.

GOAL(C): authentic EOF inspected, W[1]..W[n-1] all equal g with distinct paid cell identities, W[0]=1, all m output markers written, and actual HALT. All conjunctive obligations are required, no artificial branch elimination. The machine is a finite-control unary **record-building task**, not a SAT decider, proof system, or generic circuit evaluator. On malformed input a rejection extension may be defined, but this theorem claims only successful `1^n#` runs. Unknown richer-machine operations are conservative MAY and cannot be omitted in any future transfer.

No physical operation has zero cost, so `cl0` is identity and every zero-cost SCC singleton. Reversible optional free VIEW metadata aliases are admissible only when they preserve all seven components.

## 4. New dynamic seven-vector and exact signed rule tariff

At an authentic reachable state define:
- `a(C)=1` until header W[0] becomes active, otherwise 0;
- `q(C)` = number of missing mandatory W[1]..W[n-1] `g` records;
- `u(C)` = number of original source cells including EOF not **yet inspected**;
- `d(C)=n-1` in forward phases INIT/SECOND/EMIT; `d(C)=workHead` in BACK (note EOF_BACK has already moved the head from n to n-1); `d(C)=0` in READY/HALT;
- `h(C)=1` until a real HALT, otherwise 0.

The deliberately phase-sensitive advance charge d is the outstanding **physical return-to-header** budget. It counts n-1 future BACK_G transitions while scanning forward, but **does not double-charge** EOF_BACK, which is already counted as a source-access transition. The vector is

$$
p(C)=(0,0,0,a(C),q(C),u(C),d(C)+h(C)).
$$

Columns are (CNF, affine, separator, fusion-activation, Gamma-record, source-interface, physical-machine). The fusion coordinate a is a **single activation obligation**, not the `n-1` raw activated-graph component. Source/return components are program-sensitive. Initially

$$p(C_0)=(0,0,0,1,n-1,n+1,n),$$

and every completed goal has `p=0`. All values are nonnegative on authentic reachable states. The exact discharge matrix is:

| Authentic rule | Delta FUS | Delta Gamma | Delta INTERFACE | Delta MACHINE | Unit price |
|---|---:|---:|---:|---:|---:|
| INIT | 0 | 0 | 1 | 0 | 1 |
| WRITE_GATE | 0 | 1 | 1 | 0 | 1 |
| EOF_BACK | 0 | 0 | 1 | 0 | 1 |
| BACK_G | 0 | 0 | 0 | 1 | 1 |
| ACTIVATE_AND_MARK | 1 | 0 | 0 | 0 | 1 |
| HALT | 0 | 0 | 0 | 1 | 1 |

The three remaining columns are zero. These are all the transitions of this **fixed successful-promise program**, not assertions over arbitrary Turing machine transition tables.

## 5. Exact theorem, primal and dual

**Theorem TMR1-044 (PROVED/RESTRICTED):** For every fixed m>=1 and every n>=2 in the qualified system above, the complete nonnegative tariff cone, in the four active weights `f=λ_FUS,g=λ_Gamma,i=λ_INTERFACE,t=λ_MACHINE`, is exactly

$$
f\le1,\qquad g+i\le1,\qquad t\le1,\qquad f,g,i,t\ge0.
$$

In particular the legal synchronous WRITE_GATE prohibits the tempting independently maximal weights `g=i=1`: the single physical step would discharge 2>1. The exact initial-potential linear program satisfies

$$
\max\{f+(n-1)g+(n+1)i+nt\}=\boxed{2n+2}.
$$

A **uniform in n and fixed m** exact rational primal certificate is `(f,g,i,t)=(1,0,1,1)`. A matching **dual** assigns nonnegative row multiplicities

$$
(y_{INIT},y_{WRITE},y_{EOF},y_{BACK},y_{ACT},y_{HALT})
=(1,n-1,1,n-1,1,1),
$$

with total price `2n+2`. It covers the initial vector componentwise: fusion 1, Gamma n-1, interface n+1, machine n. Weak duality and the primal witness prove optimality. The actual fixed program makes **exactly** `1+(n-1)+1+(n-1)+1+1=2n+2` physical transitions, so telescoping and this explicit execution match.

**Proof:** INIT lowers u only. WRITE_GATE lowers u and q simultaneously, so g+i<=1 is necessary and sufficient for that class. EOF_BACK lowers u once and, because d=n-1 both immediately before and after the EOF step, does *not* lower d; its i<=1 constraint follows from g+i<=1. Each BACK_G lowers d by one, while the final HALT lowers h by one; both require t<=1. Nonterminal ACTIVATE_AND_MARK lowers a by one, while the record and output-marker obligations are already paid and tracked, yielding f<=1. These are the complete legal rows; all components vanish at GOAL. Telescoping gives the lower bound, and the finite-control trace gives the matching upper bound. The dual vector is a count of physical events, not a prescribed-DAG lower bound for another program. QED.

## 6. Independently executed finite evidence

Native OS Node v22 executed `experiments/tmr/tmr1_physical_transport096.js` locally before publication: **102 complete physical trace simulations**, n in {2,3,4,5,6,7,8,9,10,12,16,24,32,48,64,96,128}, m in {0,1,2,3,4,5}; **5,892 physical steps**, **67,900 assertions**, **zero failures**. The m=0 traces independently cover the original TMR-3 style stage machine as a control. Checks include complete physical stage contents, all read positions, at most one stage write per step, at most one write on each distinct output tape, unit head motions, all goal obligations, exact seven-row discharges, genuine nonterminal activation, unique paid gate identities, and explicit zero terminal vector. A rational eight-denominator finite grid tested 13,122 coefficient profiles/objectives. Separate native CPython `fractions.Fraction` independently checked **756 exact LP-vertex/length combinations** for n=2..64, all passing. Finite evidence is COMPUTATIONAL; the unbounded theorem relies on the transition-table proof above. No actual hardware-level TM compiler, LaTeX build, or whole-repository preflight was executed.

Separate source, raw data, and complete machine-readable tariff: `experiments/tmr/tmr1_physical_transport096.js`, `results/raw/tmr/2026-11-15_0511_TMR1_HEADTRANSPORT096_NATIVE_RAW.json`, `results/raw/tmr/2026-11-15_0511_TMR1_HEADTRANSPORT096_MATRIX.json`. The exact published GitHub source was independently executed in a fresh V8 isolate after publication. Its 67,900 assertions, 102 traces, 5,892 physical steps and 13,122 rational-grid counts agree with the native OS Node execution. The immutable GitHub raw file records the published source blob SHA.

## 7. Dependency DAG and nontransfer qualifications

| Arrow | Status |
|---|---|
| Actual six-rule finite-control unary machine and input cells N=n+1 | QUALIFIED / EXACT |
| Identity zero closure, complete physical tariff | PROVED/RESTRICTED, independent review OPEN |
| Exact rational optimum 2n+2 for this very machine | PROVED/RESTRICTED, independent review OPEN |
| Uniform all-n length bound 2n+2 under this fixed program | PROVED/RESTRICTED |
| Minimum over all alternative physical programs solving its record-building task | OPEN; this report does not claim it |
| Any transformation from correct deterministic SAT machines to this system with cost-underestimating simulation | OPEN; no valid bridge supplied |
| A superpolynomial potential in binary encoded CNF input length | OPEN |
| P versus NP | OPEN |

The source length is `N_n=n+1`; the bound `2n+2=2N_n` is **linear**, not a superpolynomial separation. No source truth-table mass, rank, state-capacity, padded bytes, or prescribed DAG are used as an unrestricted time lower bound. Allowed general SAT shortcuts include Gaussian elimination, Horn/Krom, treewidth DP, autarkies, equality, learned clauses, extensions, compact circuits, sharing, rereading, caching and recomputation, none of which is disallowed for arbitrary machine models. The present exact calibration remains restricted to its named finite-control program.

**Peer request:** TMR-3 independently inspect the phase-gated return distance and EOF overlap; TMR-4 replay this seven-column cone and its exact dual on all reachable states; TMR-5 try a different genuine physical program/shortcut and reject any alleged universal SAT transfer. The weakest missing TMR-2/3/4 lemma is a SAT-relevant compulsory transition charge invariant under alternate programs, sharing, algebra and free interface choices, rather than a policy-specific round-trip head budget.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither root proof tracker nor canonical root main.tex was modified; ownership preserved and all five existing hourly Pacific TMR schedules unchanged. Historical /341 full-language logical authority FAIL, /386 RESTRICTED. **P versus NP remains OPEN.**
