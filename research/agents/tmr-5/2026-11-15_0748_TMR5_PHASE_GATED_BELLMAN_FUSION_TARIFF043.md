# TMR-5/043: Exact phase-gated Bellman tariff for the fused shared-gate record calculus

**2026-11-15 07:48 PST | TMR-5 / PNP Machine Bottleneck Redteam | PHASEBELLMAN043**

**Status:** PROVED/RESTRICTED for a declared preauthenticated record calculus, independent mathematical review OPEN. Exhaustive finite independent V8 evidence COMPUTATIONAL. Unrestricted SAT-machine transfer and a superpolynomial initial potential OPEN. P versus NP OPEN.

## 1. Claim and four predeclared falsifiers

**Claim.** The original, unchanged TMR-3/046 last-gate FUSE calculus admits a nonnegative, phase-aware, three-coordinate reduced-product potential that exactly equals the cheapest remaining paid completion work for every viable state. A sound potential need not decrease componentwise.

Falsifiers: (F1) a genuine zero-price VIEW or NOP changes the proposed phase component; (F2) an actual price-one CHECK, BATCH, FUSE, or HALT changes the weighted potential by more than one; (F3) an independent cheapest-path replay, shared-identity reuse, or actual fusion shortcut is strictly cheaper than the proposed bound; (F4) an ordinary SAT machine has a cheaper compact algebra/circuit/learning path or a different original source-access mechanism, defeating any attempted unrestricted transfer. F1-F3 are eliminated at the declared record-system scope; F4 remains an essential hostile model boundary.

## 2. Corpus, sources, scope

Read FIRST the approved 2026-11-14 fusion-Lipschitz priority directive, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. Then read the TMR replacement directive, both root proof trackers, root main.tex, issue #3 through TMR-3/046, AGENTS.md, CODEX.md, the repository research skill, all five current TMR handoffs and original TMR-2/046, TMR-3/046, TMR-1/046, TMR-4/046, TMR-5/042 and historical TMR-4/038 materials, code and matrices. Original proof2.txt (1,051,196 characters) and root main.tex (2,545,859 characters) were recovered in full using Git blob SHA because ordinary content reads returned blank. Tracker blobs: proof1 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 930c5eeddafce656717f28055a7a9a755f44737c; main 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Corpus search did not locate this exact phase-credit cover theorem. The prior TMR-3/046 LP characterization and its reported shortest initial record count are explicitly preserved as prior work.

Primary set-cover context, not a premise of this proof: L. Lovasz, On the ratio of optimal integral and fractional covers, Discrete Mathematics 13 (1975), 383-390, DOI https://doi.org/10.1016/0012-365X(75)90058-8. The theorem below follows directly from the declared transitions and elementary finite-cover properties.

## 3. Unchanged authentic system

Fix G>=1 distinct globally authenticated gate identities D and q>=1 scales J, and a nonempty covering family E of nonempty batches S subset J. State is C=(F,D,P,U,h,v), where P subset D holds globally paid identity records, U subset J is the unfulfilled scale set, h indicates unfinished separate HALT, and v is reversible view metadata. Initial P=empty, U=J, h=1; completed goal P=D, U=empty, h=0.

The *complete* authentic transitions are: VIEW toggles v at cost zero, NOP at cost zero, neither touching P,U,h; CHECK adds one previously unpaid gate identity at cost one; BATCH(S) costs one, requires P=D and S intersection U nonempty, removes U intersection S; FUSE(g,S) costs one, requires exactly one unpaid gate g and U=J, adds that last gate and simultaneously removes S from U, leaving HALT pending; HALT costs one and is enabled only if P=D and U=empty. No further free operations are asserted. The zero-cost SCC consists exactly of the two reversible views and NOP loops for fixed P,U,h. Quotient state is (P,U,h).

All completed obligations remain mandatory, one global identity is paid once, and one FUSE event pays only one unit regardless of two simultaneous updates. This is not an ordinary SAT-machine model.

## 4. Exact shortest-distance theorem

Define tau(U) to be the minimum number of allowed batches from E that cover U, with tau(empty)=0. For any batch S with U intersection S nonempty,

$$
0\le \tau(U)-\tau(U\setminus S)\le1.
$$

Monotonicity proves the lower inequality; taking S plus an optimal cover of U outside S proves the upper inequality.

Put t=G-|P|, and chi=1 exactly when h=1, t>0, U=J; otherwise chi=0. On every viable state (h=1 and arbitrary P,U, or the completed goal h=0,P=D,U=empty) set

$$
\boxed{V(P,U,h)=t+\tau(U)+h-\chi.}
$$

**Theorem (all-parameter, restricted).** V is the true minimum paid remaining cost in the authenticated grammar. It is nonnegative, is invariant under every authentic zero-cost edge, has V(goal)=0, and is the pointwise greatest scalar lower-bound potential satisfying all cost-one and cost-zero transition tariffs and the goal boundary.

**Proof.** Every completion must check t unrecorded distinct identities, cover U by at least tau(U) batch events, and pay one distinct HALT. Only a last-gate FUSE may combine a CHECK and a batch, and FUSE may occur at most once. When t>0 and U=J, perform t-1 CHECKs, choose the first S from a minimum cover for FUSE, finish the other tau(J)-1 batches, then HALT, attaining t+tau(J). No cheaper execution exists because at most one of the t+tau(J)+1 obligatory events can be overlapped. When t=0 or U differs from J, FUSE cannot occur, so t CHECKs, tau(U) BATCHes and HALT are required and sufficient, costing t+tau(U)+1. At a completed goal cost is zero. These cases yield precisely V.

For maximality, let H be any cost-sound scalar potential with H(goal)<=0. Telescoping along a shortest genuine completion gives H(C)<=V(C). Hence V is pointwise optimal among all such potentials, including nonlinear ones. QED.

## 5. Exact nonnegative reduced-product tariff

Use a seven-column product vector in original column order (CNF, XOR, SEP, FUS, Gamma, Interface, Machine), with the first four coordinates zero, and define

$$
p_{\Gamma}=t,\qquad
p_{\mathrm{int}}=\beta=\tau(U)-\chi,\qquad
p_{\mathrm{machine}}=h.
$$

All three are nonnegative: chi=1 implies U=J nonempty and tau(J)>=1. Choose nonnegative *exact integer* weights

$$
\boxed{\lambda=(0,0,0,0,1,1,1),\qquad \Phi=V.}
$$

The **complete seven-row signed tariff matrix**, with every other discharge zero, follows. Each paid action costs one.

| Exact rule/precondition | Delta Gamma | Delta beta | Delta Machine | Total |
|---|---:|---:|---:|---:|
| VIEW or NOP (cost 0) | 0 | 0 | 0 | 0 |
| CHECK: t>=2, U=J | 1 | 0 | 0 | 1 |
| CHECK: t=1, U=J | 1 | -1 | 0 | 0 |
| CHECK: t>=1, U!=J | 1 | 0 | 0 | 1 |
| BATCH(S): t=0 | 0 | tau(U)-tau(U\S) | 0 | 0 or 1 |
| FUSE(g,S): t=1, U=J | 1 | tau(J)-tau(J\S)-1 | 0 | 0 or 1 |
| HALT | 0 | 0 | 1 | 1 |

The single-batch inequality proves every variable row. Some **real paid** CHECK or FUSE events *increase* beta; a monotone-by-component condition would incorrectly exclude this sound potential. All zero-cost SCCs preserve all three components and completed goals have zero. This is a genuine cost-sound all-rule certificate, not separately multiplied stage inequalities.

The machine-readable matrix, with concrete preconditions and signed discharges, is in results/raw/tmr/2026-11-15_0748_TMR5_PHASEBELLMAN043_TARIFF_MATRIX.json.

## 6. Strict gap beyond fractional set-cover integrality

The earlier TMR-3/046 *constant per-scale linear* cone is sound but has exact initial optimum

$$
\Phi_{\mathrm{linear}}^*=1+\max\{G,\tau^*(E)\},
$$

where tau* is the fractional set-cover optimum. The new phase-aware vector attains the actual integer minimum

$$
\boxed{\Phi_{\mathrm{phase}}^*=G+\tau(E)=W_{\mathrm{record,min}}.}
$$

Even when tau=tau*, the old linear tariff has an unbounded additive deficit: choose G=q=t and allow only the q singleton batches, so tau=tau*=t. Then

$$
\Phi_{\mathrm{linear}}^*=t+1,\quad
\Phi_{\mathrm{phase}}^*=2t,\quad
\text{gap}=t-1.
$$

At t=5, these are 6 and 10. The ratio approaches two. The deficit is due to requiring constant uncoupled nonnegative per-scale coefficients despite a *single possible last-CHECK fusion*, not fractional-cover integrality. A new nonnegative phase-sensitive component repairs it without deleting any real operation.

Fano seven-scale, G=3: exact integer tau=3, fractional tau*=7/3, old linear tariff=4, new exact tariff=6, genuine paid record work=6. Triangle G=2: old 3, new 4. A legal full-batch shortcut has tau=1 and both tariffs equal G+1. The smallest counterexample to independently maximal unfused weights remains the genuine G=q=1 FUSE rule, which discharges two old nominal units for one paid event.

**Upper ceiling:** tau(J)<=q always, hence V(C0)<=G+q. The original overlapping Feistel laboratory has G_m=O(m^3), q=m-4. Even its repaired exact potential is polynomial, not superpolynomial. Exponential separator ranks 4^j are not runtime evidence.

## 7. Independent replay

An independent V8 source reconstructs every TMR-3/046 legal rule and computes shortest completion by memoized cheapest-path recursion *without using the proposed formula*. Separately it computes tau(U) by integer minimum-cover recursion. It compares independent shortest paths with the theorem on every viable state, checks every exact signed tariff row, tests zero-cost VIEW/NOP closure, completed goals and actual beta-increase events. No random seeds.

| Finite evidence | Count |
|---|---:|
| Hypergraph/gate cases | 112 |
| Viable quotient states | 50,728 |
| Genuine paid transitions | 118,099 |
| Genuine zero-price transitions | 101,456 |
| Assertions | 659,196 |
| Negative beta discharge transitions | 314 |
| Failures | 0 |

Families include singleton, full batch, cycles, Fano, triangle and triple-overlap controls. Finite evidence is COMPUTATIONAL; independent symbolic mathematical peer review remains OPEN. This native V8 program is not a compiled Turing machine. Exact published runner: experiments/tmr/tmr5_phase_bellman043.js; immutable raw: results/raw/tmr/2026-11-15_0748_TMR5_PHASEBELLMAN043_V8_RAW.json.

## 8. Hostile controls, ranked map, peer repair

This theorem covers a **preauthenticated shared-gate record calculus**, not the cost of generating, authenticating or understanding a SAT source. No free original input read, free proof discovery, free gate construction, or physical SAT-machine transfer is claimed. The family has compact nonlinear circuits and polynomial SAT witnesses. Gaussian elimination, Horn/dual-Horn, Krom/2-SAT, bounded-treewidth DP, autarkies, learned clauses, extension variables, circuit sharing and reconvergence, padding, renaming, preprocessing, input rereads, caching, recomputation and arbitrary physical simultaneous actions all remain MAY outside this record grammar. A real cheap SAT execution is retained, not CEGAR-deleted. Logical work, event count, elapsed physical time, messages and writable space remain distinct. Here shortest paid record count is G+tau(E); there is no physical workspace or input-access lower bound.

| Rank | Dependency | Verdict | Peer repair |
|---|---|---|---|
| 1 | TMR-3/046 authentic fusion grammar and exact constant-weight cone | PASS/RESTRICTED by independent replay | TMR-3 review negative beta CHECK/FUSE rows |
| 2 | New phase-gated integer-cover Bellman potential | PROVED/RESTRICTED, independent peer review OPEN | TMR-4 rederive all-state maximality and closure |
| 3 | TMR-2/046 fractional-cover distinction | PASS/RESTRICTED | TMR-2 test tractable phase-credit quotients and other full-batch actions |
| 4 | Transferring independently maximal old constant per-scale weights | FAIL on genuine FUSE, unchanged prior scopes | Replace with full phase-aware matrix |
| 5 | Superpolynomial initial record potential for these Feistel sources | FAIL, G+tau<=G+q polynomial | Seek actual computation-dependent obstruction |
| 6 | All-correct SAT-machine same-system transfer and a superpolynomial initial gap | OPEN | TMR-1/3 audit a real fixed total SAT decider |
| 7 | Historical /341 full-language logical authority and /386 | FAIL and RESTRICTED respectively | Preserve exact scopes; do not relabel |
| 8 | P != NP | OPEN | No unrestricted separation |

**Weakest surviving lemma:** a *computational* obstruction remaining superpolynomial on algorithm-dependent actual SAT inputs after all cheap and shared real machine operations, together with all-machine transition soundness. A cost-to-go formula for a declared service alone does not supply it.

**Next peer repair:** TMR-4 independently prove/check the phase credit and every original TMR-3/046 row, including real simultaneous FUSE and possible additional closure. TMR-1 keep the polynomial labeled-family ceiling and same-machine transfer gate; TMR-2 seek a true dynamically unavoidable computational obligation rather than rank of a compact relation.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, authentic complete proof2.txt and canonical root main.tex remain unchanged. No existing task identity, hourly Pacific schedule, enabled state or ownership was altered. Historical /341 remains FAIL as full logical UNSAT authority and /386 RESTRICTED. **P versus NP remains OPEN.**

END_OF_TMR5_REPORT::043::PHASEBELLMAN043::2026-11-15_0748_PST
