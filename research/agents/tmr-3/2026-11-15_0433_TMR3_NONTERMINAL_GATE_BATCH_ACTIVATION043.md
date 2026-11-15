# TMR-3/043: A genuine nonterminal fusion-tariff failure from staged gate activation on a fixed two-tape machine

**2026-11-15 04:33 PST (America/Los_Angeles).** TMR-3 / PNP Time-Space Tradeoffs. Governing directive: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md`, blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`.

**Claim status:** **PROVED/RESTRICTED** for the precise fixed finite-control, locally moving, two-tape unary gate-staging machine below, independent mathematical review **OPEN**. Finite direct transition replay **COMPUTATIONAL**. This is a falsifier of a proposed *cross-model* fusion tariff, **not** of TMR-1/043's original qualified R_CONN theorem. The unrestricted SAT-machine lower bound, superpolynomial initial gap and same-system transfer remain **OPEN**. **P versus NP remains OPEN.**

## 1. Candidate and four falsifiers set before source search

**Candidate:** Transferring TMR-1/043's paid-APPEND connectivity coefficient `lambda_FUS=1` to a physical machine by applying it to the graph of *currently activated*, already-staged gate records may violate a single real cost-one transition **before halt**. At the same time, a distinct progress measure counting the physically missing gate-record cells should survive the true microstep tariff, with a linear ceiling.

Predeclared falsifiers: (F1) a supposedly cost-one transition actually changes two or more work cells or jumps a head; (F2) the staged records were not previously paid for or are duplicated by the activation instruction; (F3) activation and successful HALT coincide, making the example merely another terminal-mask counterexample; (F4) the abstract graph tariff is mistakenly asserted to cover an interface that admits global activation as a new native rule. F1 and F2 are excluded by the explicit finite-state transition table and replay. F3 is excluded by a distinct nonhalting READY state and separate HALT transition. F4 is a genuine **model-changing bridge**, and is exactly why the original R_CONN claim survives.

## 2. Sources, original-project reconciliation, and novelty boundary

Before construction, recovered the user-approved fusion directive, 2026-11-13 TMR replacement directive, full `proof1.txt` (SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, 28,714 characters), full `proof2.txt` (Git blob `930c5eeddafce656717f28055a7a9a755f44737c`, 1,051,196 characters), and full root `main.tex` (Git blob `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`, 2,545,859 characters). The latter two required direct authentic Git-blob reads because ordinary contents reads return empty strings despite nonempty blob SHA. Also inspected issue #3, `AGENTS.md`, `CODEX.md`, repository research skill, the five latest TMR handoffs, TMR-1/043 report and executed code/matrix, TMR-3/042 report/matrix context, TMR-4/043 peer handoff, TMR-2/043 issue evidence, and original LEAD-0029 Lipschitz audit.

Primary historical context: R. E. Ladner, *The circuit value problem is log space complete for P*, SIGACT News 7(1), 1975, DOI [10.1145/990518.990519](https://doi.org/10.1145/990518.990519); A. V. Aho and J. D. Ullman, *Optimization of Straight Line Programs*, SIAM J. Comput. 1(1), 1972, DOI [10.1137/0201002](https://doi.org/10.1137/0201002). Neither paper is credited with the elementary new two-tape staging counterexample. The new point relative to source-static terminal-mask examples is **a fully paid, nonterminal, physical one-cell activation of a previously stored shared-DAG representation**.

## 3. Exact qualified machine and physical semantics

For every integer `n>=2`, feed the **same fixed deterministic finite-state two-tape machine M_STAGE** an immutable read-only tape with cells `0,...,n` containing `1^n#`. The tape head begins at 0. The sole initially blank writable tape `W` has one head at 0 and alphabet `{blank,0,1,g}`. Both heads move in `{-1,0,+1}` on each transition, and at most one work symbol is rewritten per transition. Every real microstep costs **exactly one**. The machine's transition rules depend only on its finite state and two scanned symbols, never on n; n is known to the *analyst* from the authenticated input, not supplied as a free runtime counter.

The complete successful-source transition table is:

| Rule | Local precondition | Work write and heads | Next control | Price |
|---|---|---|---|---:|
| INIT | INIT, read first `1`, W blank | write `0`; both heads right | SECOND | 1 |
| WRITE_GATE | SECOND or EMIT, source `1`, W blank | write `g`; both heads right | EMIT | 1 |
| EOF_BACK | EMIT, source `#`, W blank | work head left, input head stays | BACK | 1 |
| BACK_G | BACK, W scans `g` | work head left | BACK | 1 |
| ACTIVATE | BACK, W scans `0` | rewrite **only W[0]** from 0 to 1, stay | **READY (not HALT)** | 1 |
| HALT | READY, W scans `1` | no writing, stay | HALT | 1 |

The source promise `1^n#`, `n>=2`, is exact. Other source symbols may enter a separate rejecting sink without a successful completion. This **is not a total general SAT decider**; no arbitrary circuit grammar, 3-CNF parser, or free formula authenticator is claimed.

Work cells `W[1],...,W[n-1]` each contain exactly one `g` after WRITE_GATE. Their **position-indexed**, count-once shared identities represent the implicit gates `y_2=x_1 AND x_2` and `y_i=y_{i-1} AND x_i` for `3<=i<=n`. Fanout and prior references do not duplicate paid identities. W[0] is an *activation header*: while it is 0, this interface exposes n disconnected input vertices; when it becomes 1 with all `n-1` staged `g` records, the interface exposes the complete chain with one input-connected component. This is a particular proposed physical representation quotient, **not** a legal R_CONN APPEND operation.

A successful **qualified record-building goal** requires source EOF actually inspected, W[0]=1, all n-1 mandatory work cells equal `g`, and true HALT. All six rule classes are charged; there are **no authentic zero-cost transitions**, so all zero SCCs are singleton and `cl_0` is the identity. No unlisted step is silently declared illegal in an arbitrary SAT-machine model: the above inventory qualifies only this explicitly named M_STAGE.

## 4. A one-transition, nonterminal failure of activated-graph connectivity pricing

Define the candidate active fusion component `f(C)=n-1` when W[0] is 0, and `f(C)=0` when W[0] is 1 along reachable successful-source traces. This equals the number of connected components among original input vertices in the *currently activated* gate graph, minus one. It is zero at completed goals.

Immediately before ACTIVATE, **all n-1 physical gate records have already been written and individually paid for**. The head is on cell W[0]. One authentic finite-alphabet transition changes that one header symbol from 0 to 1 and moves to nonhalting READY, without adding or writing any gate record. Hence, for every n>=2,

$$
\Delta_{\mathrm{FUS}}(\mathrm{ACTIVATE})=n-1,\qquad w(\mathrm{ACTIVATE})=1.
$$

For n=3, the **smallest strict violation** of a transferred unit gate coefficient is the one physical rewrite `0 -> 1` activating two already-staged AND records, `Delta_FUS=2>1`. A uniform nonnegative fusion coefficient must obey `(n-1)lambda_FUS<=1` for **every n**; therefore `lambda_FUS=0`. The violation happens *before* HALT and is not a terminal-mask mechanism. TMR-1/043's genuine gate-by-gate APPEND tariff `Delta_FUS<=1` remains correct for its own **different** gate-building calculus, which has no header-activation rule.

## 5. Repaired physical record-count component and complete tariff matrix

Write `r(C)` for the rightmost input index ever actually inspected (`r=-1` initially); let `h(C)=1` until successful HALT and 0 afterward; let `q(C)` be the count of physically incorrect or blank mandatory cells `W[1],...,W[n-1]`. Define the full canonical seven-vector

$$
\mathbf p(C)=(0,0,0,f(C),0,q(C),n-r(C)+h(C)).
$$

Every component is nonnegative along this M_STAGE realization, and completed goals make all components zero. On this fixed machine, `q` decreases by exactly one on each of the n-1 physical WRITE_GATE transitions and is unchanged at ACTIVATE. Unlike activated connectivity, this component charges **creation of latent physical records** while they are staged. A machine with one writable head can correct at most one required work cell per genuine step, so the isolated `q` local bound survives any one-cell rewrite, including a corruption with negative discharge.

Full signed seven-column rows are in the JSON matrix. Its active columns are:

| Real rule | Delta FUS | Delta INTERFACE (q) | Delta MACHINE (unread plus halt) | Physical cost |
|---|---:|---:|---:|---:|
| INIT | 0 | 0 | 1 | 1 |
| WRITE_GATE | 0 | 1 | 1 | 1 |
| EOF_BACK | 0 | 0 | 1 | 1 |
| BACK_G | 0 | 0 | 0 | 1 |
| ACTIVATE | n-1 | 0 | 0 | 1 |
| HALT | 0 | 0 | 1 | 1 |

All other columns are identically zero. Simultaneous input inspection and physical gate record writing are **one** paid instruction, so full independent weights on q and input-frontier work would overcharge WRITE_GATE.

For each fixed n the **exact rational nonnegative feasible cone** on the three active coefficients `c=lambda_FUS, a=lambda_INTERFACE, b=lambda_MACHINE` is

$$
\boxed{(n-1)c\le1,\qquad a+b\le1,\qquad a,b,c\ge0.}
$$

Necessity is witnessed by genuine ACTIVATE and WRITE_GATE rows. Sufficiency follows by checking all six rule classes. Requiring the same coefficients to work for the **entire growing family** makes the precise cone

$$
\boxed{c=0,\qquad a+b\le1,\qquad a,b\ge0.}
$$

The zero-valued other four components may carry irrelevant nonnegative coefficients, but cannot yield lower bounds. At input initialization, `p=(0,0,0,n-1,0,n-1,n+2)`. The exact fixed-n primal maximum is

$$
\max \Phi(C_0)=
\max_{(n-1)c\le1,\,a+b\le1}
\bigl((n-1)c+(n-1)a+(n+2)b\bigr)=n+3,
$$

attained by the exact rational weights `(c,a,b)=(1/(n-1),0,1)`. The independent exact dual uses one price multiplier `u>=1` for activation and one `v>=n-1, v>=n+2` for the fused read/write inequalities, achieving `u+v=1+(n+2)=n+3`. For a uniform length-independent potential `c=0, (a,b)=(0,1)`, the initial bound is **n+2**. None is superpolynomial. The direct machine trace costs **2n+2**, larger than the best fixed-n tariff certificate; no equality with runtime is claimed.

The machine visits exactly `n+1` distinct work-head positions `0,...,n`, leaves exactly n nonblank cells (one flag plus n-1 gate records), and reads exactly n+1 distinct input positions, including EOF. It makes `2n+2` charged physical transitions and the same number of input-port symbol observations if observations on already visited EOF are counted. Sequential elapsed steps and span are both `2n+2`; output evidence is n work-alphabet symbols with implicit gate addressing, **not n separate input assignments or exponentially many output bits**. No AND proof branches, assumptions, learned clauses, additional messages or separate interface conversions occur. They have no claimed cost-zero status in richer machines.

## 6. Executed evidence and hostile model controls

The **exact JavaScript `audit()` body** was executed in native V8 and serialized unaltered into `experiments/tmr/tmr3_stage_gate_tm093.js`. It directly simulates each read/write/head-move/control microstep. It checked all 255 source lengths `2<=n<=256`, **66,300 genuine transitions**, and **536,984 assertions with zero failures**. Rule totals: 255 INIT, 32,640 WRITE_GATE, 255 EOF_BACK, 32,640 BACK_G, 255 ACTIVATE, 255 HALT. Additionally, 254 nonterminal transferred-tariff violations (`n>=3`) were replayed; 4,800 signed single-record-cell rewrite controls verified the one-physical-cell progress bound. Finite results are **COMPUTATIONAL**; the simple all-n proof is symbolic.

Three hostile transfer controls remain explicit. First, a physically **different** program that simultaneously activates the header and halts adds an ACTIVATE+HALT joint row, so the above fixed-M cone cannot be exported to that machine without recalculation. Second, a changed output grammar permitting a single compact `AND_ALL(n)` descriptor avoids mandatory n-1 records, so this lower bound cannot be imposed on an arbitrary SAT solver. Third, if a wider transition mechanism or free record-writing oracle is added, the one-cell output and price-one bounds require revision; real new paths are **MAY**, not CEGAR-deleted. Horn/2-SAT, Gaussian/Tseitin, bounded treewidth, equality, autarky and private-leaf witness shortcuts are not claimed hard by a unary gate-record printer; they remain legal and in fact polynomial-time controls against SAT-machine transfer. One-shot shared activation is itself a compact-representation shortcut.

**Evidence files:** `experiments/tmr/tmr3_stage_gate_tm093.js`; `results/raw/tmr/2026-11-15_0433_TMR3_GATESTAGE093_V8_RAW.json`; `results/raw/tmr/2026-11-15_0433_TMR3_GATESTAGE093_TARIFF_MATRIX.json`.

## 7. Exact dependency and next handoff

**PASS / PROVED/RESTRICTED:** A fixed finite-control, finite-alphabet, locally moving, initially blank-work-tape machine really makes a cost-one *nonterminal* activation of n-1 staged gate identities; exact physical rows, rational cone and physical record-count repair follow.

**FAIL / transferred claim only:** Giving the *activated representation* graph the original R_CONN coefficient `lambda_FUS=1` in an unrestricted physical microstep model, or assuming that one visible graph activation equals one original APPEND.

**OPEN:** An all-machine simulation from actual fixed total deterministic 3-SAT deciders preserving a useful dynamic fusion obstruction; a superpolynomial growing initial gap after all compact algebra, sharing and representation changes; a theorem that prohibits or independently pays for pre-staging; and independent peer mathematical review.

**TMR-1:** Record a model-translation guard: `APPEND` gate changes cannot be identified with a single `ACTIVATE` rewrite on an already-filled buffer. **TMR-2:** Apply staging attacks to multiscale components with latent relations. **TMR-4:** Add the physically legal ACTIVATE row to any proposed MAY envelope and independently verify the length-uniform rational zero-weight conclusion. **TMR-5:** Try alternate encodings, fused terminal and bit-flag recognition.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `proof1.txt`, `proof2.txt`, and `main.tex` are unchanged. All five existing Pacific scheduled agents are unchanged. P versus NP remains OPEN.
