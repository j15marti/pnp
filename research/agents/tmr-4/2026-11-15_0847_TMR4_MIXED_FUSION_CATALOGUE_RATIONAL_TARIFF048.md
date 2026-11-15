# TMR-4/048: exact tariff for a heterogeneous catalogue of last-b-gate fusion operations

**2026-11-15 08:47 PST | PNP Cost-Sound Abstraction | MIXEDFUSE134**

**Scientific status:** PROVED/RESTRICTED for the explicitly qualified *preauthenticated shared-gate record calculus* below; native V8 finite verification COMPUTATIONAL; independent mathematical peer review OPEN. This does NOT prove a SAT machine lower bound. P versus NP remains OPEN.

## 1. Falsification-first candidate and four falsifiers

**Candidate, stated before focused source review.** TMR-3/047 has a genuine price-one FUSE_b for one fixed b, and TMR-4/047 and TMR-5/043 handle b=1 exactly. Consider one NEW record grammar with a whole finite catalogue B of legal fused bundle widths, each genuine FUSE_b simultaneously checking the final b unpaid globally unique gate identities and activating one batch. Could a state-dependent *maximum still-available fusion credit* produce one exact seven-column tariff across the heterogeneous catalogue, preserving every legal cheap transition?

Predeclared falsifiers: (F1) any legal free VIEW or NOP changes paid identities or pending AND scales; (F2) a price-one authentic FUSE_b, CHECK, BATCH, or HALT decreases the weighted potential by more than one; (F3) a genuine second/earlier fusion, undeclared wider bundle, free batch, shared-gate reuse or compact affine representation makes a cheaper completion; (F4) confusing this preauthenticated calculus with a physical machine changes source, tapes, heads, preprocessing, proof construction, output or price. F1/F2 are ruled out in the declared model. The explicitly *expanded* systems in §6 show real counterexamples for F3; F4 remains OPEN and prevents unrestricted promotion.

## 2. Corpus and prior-work boundary

Read FIRST the approved `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md` (blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`), then the TMR replacement directive, both root proof trackers, root main.tex, issue #3, AGENTS.md, CODEX.md, repository research skill, all five current TMR handoffs, and relevant original material. The ordinary Contents API supplied empty *bodies* for proof2/main, but the authentic Git blobs were independently recovered and their complete 1,051,196- and 2,545,859-character bodies inspected. Current root blob SHAs: proof1 `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, proof2 `930c5eeddafce656717f28055a7a9a755f44737c`, main.tex `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`.

Original direct dependencies: TMR-2/046 fractional versus integer batch covers; TMR-3/046 first authentic last-CHECK-plus-BATCH FUSE; TMR-4/047 dynamic cover and single-gate credit; TMR-5/043 independently computed exact Bellman tariffs; TMR-3/047 newly introduced the *fixed* b-wide FUSE and its exact potential. These are prior results, not claims of this report. The NEW claim is one mixed-width catalogue in a single precisely specified authority, its exact all-state Bellman formula, all seven-coordinate row verification, catalogue-switch credit, and rational primal/dual verification. TMR-1/047's indexed-family theorem and TMR-2/047's physical sign-fusion audit supply explicit hostile uniformity and machine-cost boundaries. Historical /341 remains FAIL as a full UNSAT authority; /386 remains RESTRICTED.

Primary context checked: Cousot and Cousot, *Abstract interpretation*, POPL 1977, DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973); Lovasz, *On the ratio of optimal integral and fractional covers*, Discrete Mathematics 13 (1975), DOI [10.1016/0012-365X(75)90058-8](https://doi.org/10.1016/0012-365X(75)90058-8); Cook and Reckhow, *The relative efficiency of propositional proof systems*, JSL 44 (1979), DOI [10.2307/2273702](https://doi.org/10.2307/2273702). These works give background about abstraction, covers and proof-model dependence, **not** a theorem about the catalogue below. In particular no claim that this finite record grammar is a Cook-Reckhow proof system.

## 3. Complete qualified concrete transition system and zero closure

Fix G>=1 distinct globally authenticated shared gate IDs D, a nonempty finite set J of conjunctively required scale IDs, and a nonempty covering family E of nonempty batches S subseteq J. Fix a nonempty catalogue B subseteq {1,...,G}. The source F, signed provenance, complete shared proof/circuit DAG D, batch authority E, assumptions, definitions, and private/exported interfaces are **immutable, preauthenticated**. They are part of the full state (F,D,E,B,P,U,h,v), not constructed here. The mutable P subseteq D records distinct globally paid gate IDs, U subseteq J is the remaining AND-obligation set, h=1 denotes the distinct unpaid HALT, and v in {0,1} is reversible metadata. Goal: P=D, U=empty, h=0. Only that h=0 state is legal. No semantic proof acceptance or SAT output is inferred.

The complete transition grammar is:

| Rule | Preconditions | Actual cost | Effect |
|---|---|---:|---|
| VIEW | any state | 0 | toggle v, without changing any other field |
| NOP | any state | 0 | same state |
| CHECK(g) | h=1 and g not in P | 1 | P:=P union {g} |
| BATCH(S) | h=1,P=D,S in E,S intersects U | 1 | U:=U minus S |
| FUSE_b(S) | h=1,U=J, exactly b unpaid gates remain, b in B, S in E | 1 | P:=D and U:=J minus S in the SAME NONTERMINAL event |
| HALT | h=1,P=D,U=empty | 1 | h:=0 |

A FUSE is usable AT MOST ONCE, since it exhausts all unpaid gate IDs and changes U away from J. No undeclared earlier/second fusion, zero-cost source parsing, compact circuit expansion, Gaussian shortcut, simultaneous interface conversion, machine-head positioning, or extra permission exists *inside this grammar*. Those behaviors remain conservative MAY in a wider model, not replay-proved spurious paths.

The authentic zero-price SCC of every state is exactly its {v=0,v=1} pair. Thus cl0(C) is this pair, and the canonical quotient α(C)=(F,D,E,B,P,U,h) preserves all immutable evidence and the paid history. For every related concrete/quotient state and every concrete step, VIEW/NOP simulates by the empty abstract path of price 0, and every paid transition simulates by its identically priced quotient edge. The related successor and completed goal predicate are preserved. This is a precise all-step cost-underestimating simulation, not a simulation of arbitrary physical SAT code.

## 4. Exact heterogeneous-catalogue theorem

For U subseteq J define the minimum integral *residual* batch-cover number

$$
\tau_E(U)=\min\{|K|:K\subseteq E,\ U\subseteq\bigcup_{S\in K}S\},\qquad\tau_E(\emptyset)=0.
$$

Every permitted batch satisfies 0 <= tau(U)-tau(U minus S) <=1: removing obligations cannot increase cover cost, and appending S to an optimal residual cover gives the upper inequality.

Let t=G-|P| and let b_B(t)=max({b in B:b<=t} union {0}). Define the *phase-qualified maximum option credit*

$$
\chi_B(C)=\mathbf1\{h=1,\ U=J\}\,b_B(t).
$$

This is a credit for one feasible, still-unused fused operation; it is neither an unpriced physical optimization nor a multiplicity of separate scale credits. The nonnegative seven-vector in canonical order is

$$
p(C)=(0,0,\tau_E(U),0,t-\chi_B(C),0,h).
$$

With the **exact rational certificate**

$$
\boxed{\lambda=(0,0,1,0,1,0,1),\quad
\Phi(C)=t+\tau_E(U)+h-\chi_B(C)}
$$

every legal paid or zero-price transition satisfies the tariff inequality λ·(p(C)-p(C'))<=w. Every goal has potential zero.

**All-step proof.** Let b(t)=b_B(t), which is nondecreasing in t. A CHECK from t to t-1 when U=J has signed Gamma discharge 1-b(t)+b(t-1)<=1. This may be NEGATIVE when CHECK forfeits a wide fuse option. When U!=J, CHECK has Gamma discharge 1. A genuine FUSE_b is enabled only at t=b, hence b_B(t)=b and Gamma=t-chi_B=0 both before and after. Its sole charged discharge is tau(J)-tau(J minus S)<=1. A BATCH is enabled only at t=0; Gamma stays zero, and the residual cover decreases by at most one. HALT decreases h by exactly one. VIEW and NOP change no component. Consequently λ is cost-sound for every transition, including ALL signed rows. Telescoping to the completed goal yields the lower bound.

**Exact all-state Bellman identity.** For any legal state h=1, U=J, a fused operation of width b<=t is achieved by t-b authentic CHECK events, then exactly one FUSE_b using a first batch in an optimal cover, then the remaining tau(J)-1 BATCH events, then one distinct HALT. The cost is t+tau(J)+1-b. If no width is feasible, ordinary CHECKs+BATCHes+HALT cost t+tau(J)+1. If U!=J, no fusion is possible now or later, because pending obligations only decrease, so exact work is t+tau(U)+1. For h=0 the goal costs zero. These cases prove the uniform formula

$$
\boxed{W(C)=\Phi(C)=t+\tau_E(U)+h-\chi_B(C)}
$$

for **every viable quotient state**, not only full initial states. This includes all globally shared gate-ID subsets and states with partial prior batch discharge. Nonnegativity follows from b_B(t)<=t. Because a cheapest authentic completion attains W, telescoping shows that Φ is pointwise maximal among all cost-sound scalar potentials with goal<=0.

For a fully unpaid source state the restricted exact minimum is

$$
\boxed{W(C_0)=G+\tau_E(J)+1-\max(\{b\in B:b\le G\}\cup\{0\}).}
$$

The formula is not a superpolynomial SAT lower bound: tau_E(J)<=|J|, and this entire initial gap is at most G+|J|+1, polynomial whenever the inherited authenticated record counts are polynomial.

## 5. Machine-readable seven-column tariff, rational LP and independent dual

Write the active coordinates (SEP,Gamma,Machine). The complete symbolic rule rows are:

| Rule | SEP delta | Gamma delta | Machine delta | Price |
|---|---:|---:|---:|---:|
| VIEW, NOP | 0 | 0 | 0 | 0 |
| CHECK with U=J | 0 | 1-b(t)+b(t-1) | 0 | 1 |
| CHECK with U!=J | 0 | 1 | 0 | 1 |
| FUSE_b(S), t=b | tau(J)-tau(J minus S) | 0 | 0 | 1 |
| BATCH(S) | tau(U)-tau(U minus S) | 0 | 0 | 1 |
| HALT | 0 | 0 | 1 | 1 |

All four inactive columns CNF,XOR,FUS,Interface are zero, **not** implied lower bounds on those resources. The exact feasible tariff cone for the declared full state space includes and is bounded by 0<=lambda_SEP,lambda_Gamma,lambda_Machine<=1; each coordinate has an authentic unit-discharge row, while no genuine row combines two positive coordinates. Setting all three weights to one is therefore feasible and maximizes the nonnegative initial objective.

The independent rational LP routine uses BigInt numerator/denominator pairs, exact Gaussian elimination, and exhaustive vertex enumeration for the three active dimensions; it consumes every signed legal row and explicit nonnegative-weight rows. There are no floating-point feasibility comparisons. A matching authentic shortest-completion trace supplies the LP upper/dual certificate because summing its genuine tariff constraints gives λ·p(C0)<=sum w(r) for *every* feasible λ, not just the displayed one.

Example G=4, q=3, E={{0,1},{0,2},{1,2}}, B={1,3}: tau(J)=2, initial p=(0,0,2,0,1,0,1), λ·p=4. Authentic cost-four upper/dual witness: CHECK one gate, FUSE_3 on batch {0,1}, BATCH {0,2}, distinct HALT. The four respective weighted discharges are 1,1,1,1. By contrast, importing the **unchanged** b=1 phase-credit formula into this **new b=3 grammar** gives initial 6; the genuine FUSE_3 row would overdischarge, a proper model-changing falsifier rather than an error in TMR-4/047's original b=1 result.

The published matrix includes every physical rule-row instance for the feature case, including VIEW/NOP: **258 concrete states, 129 authentic zero SCCs, 1,114 legal edges (598 paid, 516 zero), six unique exact signed tariff rows**, and exact rational LP optimum 4 at active λ=(1,1,1).

## 6. Independent computation and real hostile controls

Executed the exact self-contained V8 function serialized into `experiments/tmr/tmr4_mixed_catalogue134.js`. It independently generated the full legal graph, computed Tarjan zero-cost SCCs, quotient edges, recursive cheapest legal completion for every quotient state, all-rule signed potential inequalities, and a separate exact-rational three-dimensional vertex LP. Results: **13 valid case grammars, 55,299 assertions, 8,278 paid rows, 7,364 zero-price rows, 1,841 zero-price SCCs, 94 real signed negative-Gamma rows, zero unexpected failures**. Included singleton, full batch, overlapping triangle, multiwidth catalogue and seven-scale cover controls; the deliberately malformed uncovered grammar was rejected. Every genuine shared identity is a P bit, counted once. All branches preserve AND-scale obligations until an authentic BATCH or FUSE.

Three **genuine shortcuts if independently ADDED to a DIFFERENT rule authority**, independently calculated, are mandatory failing controls:

1. **Second early FUSE:** G=2, E={{0},{1}}, B={1}. An expanded FUSE that allows a second one-gate check+batch even after the initial full-U phase has an authentic row from P={0},U={1},h=1 to P=D,U=empty,h=1, price1 and delta=(0,0,1,0,1,0,0), weighted drop **2>1**. In the expanded system the two fused operations plus HALT cost 3, defeating the former initial 4.
2. **Free batch:** At P=D,U={0},h=1, adding a zero-price BATCH produces delta=(0,0,1,0,0,0,0), drop **1>0**.
3. **Undeclared wider fuse:** G=2,B={1},E={{0},{1}}. Adding a price-one FUSE_2 from P=empty,U=J to P=D,U={1} produces delta=(0,0,1,0,1,0,0), drop **2>1**. A compact affine/circuit macro with comparable multi-obligation discharge would be the same kind of fatal tariff row if physically real.

These edges are NOT present in the exact authenticated grammar, so they are recorded as precise model-changing counterexamples rather than removed by CEGAR. In any physical machine extension an authenticated zero-price or joint-discharge shortcut must be retained and the abstraction requalified. A wide fanout, shared DAG, high semantic rank, or length of a prescribed computation is not a substitute for such a transfer proof. Horn, Krom, affine Gaussian, bounded-treewidth, autarky, extension, learning, input rereading, caching, recomputation, compact circuits and cheap uniform recognizers remain MAY outside this record-only calculus.

## 7. Model/resource ledger and independent transfer gate

Logical record work is the number of paid CHECK/BATCH/FUSE/HALT events, with a global count-once P ledger and no artificial per-scale multiplication. Sequential abstract paid work and record-program span coincide in this sequential grammar; reversible zero-price VIEW cycles can make physical elapsed step count arbitrary. Preauthenticated gate DAG, batch lists, source, assumptions, definitions and interface contents are *already supplied*; no acquisition, original input access, tape/head position, serialization, proof checker, clauses, line encoding, resource allocation, read/write index or storage tradeoff is charged. Mutable record bits number G+|J|+2 in the abstract logical model, not a bound on actual work-tape cells. No physical messages are claimed.

**Transfer remains OPEN:** no all-step cost-underestimating simulation from arbitrary correct fixed deterministic 3-SAT deciders into this record calculus; no native 3-SAT family construction forcing these records; no superpolynomial initial gap; no source-complete proof authority of the historical mixed checker. Cheap actual SAT executions and algebraic shortcuts cannot be treated as spurious. TMR-1/047's fixed-family recognizer ceiling is retained. Historical /341 full logical authority FAIL, /386 RESTRICTED. **P versus NP remains OPEN.**

## 8. Publication and next precise target

- Report: `research/agents/tmr-4/2026-11-15_0847_TMR4_MIXED_FUSION_CATALOGUE_RATIONAL_TARIFF048.md`
- Executed code: `experiments/tmr/tmr4_mixed_catalogue134.js`
- Immutable raw: `results/raw/tmr/2026-11-15_0847_TMR4_MIXEDFUSE134_V8_RAW.json`
- Complete case matrix: `results/raw/tmr/2026-11-15_0847_TMR4_MIXEDFUSE134_TARIFF_MATRIX.json`
- Handoff: `research/agents/tmr-4/handoff.md` (prepend; preserve old content).

**NEXT:** TMR-3/5 should independently replay the catalogue-switch CHECK loss-of-credit rows and attempt a genuine earlier or repeated FUSE in a physically charged representation. TMR-2 should seek a SAT-specific obstruction beyond authenticated G+q metadata, and TMR-1 should maintain separate every-decider same-input, same-machine transfer. No root tracker or main.tex edits; **TRACKERS REVIEWED; NO MATERIAL CHANGE**. No schedule changes.
