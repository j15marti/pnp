# TMR-4/042: canonical signed-NAE leaf core and exact seven-column tariff

**2026-11-15 02:40 PST | LEAFCORE082 | PNP Cost-Sound Abstraction.** Governing directive: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md` at blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`. **PROVED/RESTRICTED** symbolic results in a specified source-authenticated *typed record calculus*; independent mathematical review OPEN. Finite V8 verification **COMPUTATIONAL**. P versus NP OPEN.

## 1. Candidate and falsifiers, selected before source inspection

**Candidate:** TMR-2/041's authenticated, signed, three-uniform NAE edge-leaf operation has a *unique order-independent terminal residual core*. This makes a nontrivial canonical state component (b(U)=|U|-|K(U)|), whose exact local discharge can be calibrated together with the prior fusion and restoration obligations. The target is a genuine incremental theorem, **not** a SAT-machine lower bound.

Four falsifiers: (F1) different admissible leaf orders produce different terminal edge sets; (F2) a paid PEEL changes (K(U)) or reduces (b) by more than one; (F3) an authentic zero-price transition changes the weighted potential; (F4) an allegedly nonempty core is mistaken for an UNSAT certificate, or source parsing/compact witness construction is charged zero in a physical machine.

Result: F1-F3 are excluded for the unchanged `R_leaf` inventory. F4 survives as a necessary restriction: a nonempty core may be SAT or UNSAT, and an *additional* free-PEEL transition would falsify the certificate.

## 2. Exact qualified state and epistemic boundaries

Fix an immutable, preauthenticated signed paired-NAE source: each distinct unordered triple of distinct source variable IDs contributes exactly its two complementary signed 3-clauses, with duplicate clause occurrences deduplicated by source identity. Let (E) be the finite source edge set. TMR-2/041's typed `R_leaf` concrete state retains the **entire** source and provenance, program/calculus authority, (U\subseteq E) remaining edges, full LIFO signed pivot stack (S), assigned variable values, control phase PEEL or RESTORE, active bit (h), original clause obligations and terminal verification. No free source acquisition is asserted for an ordinary Turing machine.

Legal events are zero-price NOP, zero-price PEEL-to-RESTORE switch only when (U=\varnothing), price-one PEEL of **one** edge with a currently degree-one incident variable and source-indexed stack push, price-one reverse RESTORE of **one** signed pivot with stack pop, and price-one terminal HALT after the original authenticated goal is verified. Distinct paid edge identities count once. A failed grammar, a stuck nonempty core, malformed source, an invalid pivot, or an unverified witness does not produce a completed successful goal. Other SAT algorithms are **MAY** in the unrestricted model, not illegal in a physical machine.

An abstraction retaining ((F,U,|S|,\text{phase},h,\text{goal status})) and existentially forgetting the contents of otherwise authenticated stack entries is a cost-underestimating simulation: each allowed concrete record event projects to a single **equal-price** abstract edge and every completed concrete goal maps to abstract terminal (U=S=\varnothing,h=0). This is an all-step statement about **this record calculus**, not a finite-alphabet machine compiler. Zero-cost phase switching preserves (U,|S|,h); no unverified CEGAR pruning is used.

## 3. Canonical leaf-core theorem

For (U\subseteq E), write (deg_U(v)=|\{e\in U:v\in e\}|). An edge (e\in U) is *eligible* if it contains a vertex (v) with (deg_U(v)=1). A nonempty edge subset (H\subseteq U) is *stable* if every vertex incident with (H) has degree at least two in (H). Define (K(U)) to be the union of **all stable subsets** of (U), with the empty subset included.

**LEAFCORE082-A (PROVED/RESTRICTED).** The union of stable subsets is stable (each incident vertex already has at least two edges in a contributing stable subset); therefore (K(U)) is the unique largest stable edge subset. For **every** legal single-edge PEEL (U\to U\setminus\{e\}),

[
K(U)=K(U\setminus\{e\}).
]

**Proof.** If a degree-one vertex (v) witnesses the eligibility of (e), no stable subset of (U) can contain (e): otherwise (deg_H(v)\le\deg_U(v)=1), violating stability. Hence all stable subsets of (U) lie in (U\setminus\{e\}); conversely stable subsets of the smaller set are stable subsets of (U). Their unions coincide. At any fully peeled terminal (T), (T) itself is stable, so (T\subseteq K(U)); repeated invariance gives (K(T)=K(U)), and stability of (T) gives (K(T)=T). Thus (T=K(U)) **for every maximal legal PEEL sequence**. The rule is terminating, confluent to an identical edge set, and invariant under independent per-edge sign gauges, clause-order permutations, and authenticated exact-clause duplicates. QED.

Consequently the dynamic *number of currently peelable-to-core edges*

[
 b(U)=|U|-|K(U)|
]

decreases by **exactly one** on every paid PEEL, is invariant on the authentic zero-price events, and is zero on a terminal unpeelable core. This is a *reachability-ticket count*, not a representation-independent SAT-hardness parameter. It is not legitimate to turn mathematical normalization (U\mapsto K(U)) into a **zero-cost concrete PEEL** merely because (K) is canonical: in `R_leaf`, PEEL costs one.

## 4. Exact seven-column reduced product, local rows, and rational primal/dual

In the project column order CNF, XOR, SEP, FUS, GAMMA, INT, MACHINE set

[
p(C)=\bigl(0,0,b(U),2|U|,|S|,0,h\bigr).
]

The `SEP`, `FUS`, and `GAMMA` entries denote **typed edge-record obligations only**. They are not a lower bound on separator communication or all SAT computations. Since the only authentic zero steps preserve these components, directed zero-cost closure leaves (p) invariant; computing (K(U)) is a static abstraction operation, **not** an omitted free physical transition. In the finite 5-variable control projection, Tarjan quotient finds 2,048 zero-cost singleton SCCs (including self-loops and one-way phase switch). An independent 4-node toy control verifies correct collapsing of an actual 2-node zero-cost SCC.

Complete exact tariff constraints for all legal rule types (all other columns zero):

| Event | Cost | \(\Delta p_{SEP}\) | \(\Delta p_{FUS}\) | \(\Delta p_{GAMMA}\) | \(\Delta p_{MACHINE}\) |
| --- | ---: | ---: | ---: | ---: | ---: |
| NOP / zero SWITCH | 0 | 0 | 0 | 0 | 0 |
| PEEL | 1 | 1 | 2 | -1 | 0 |
| RESTORE | 1 | 0 | 0 | 1 | 0 |
| HALT | 1 | 0 | 0 | 0 | 1 |

Thus the *exact restricted nonnegative cone* is

[
\lambda_{SEP}+2\lambda_{FUS}-\lambda_{GAMMA}\le 1,\qquad
\lambda_{GAMMA}\le1,\qquad
\lambda_{MACHINE}\le1,\qquad\lambda_i\ge0.
]

One nontrivial exact rational certificate, independently checked against every row, is

[
\boxed{\lambda=(0,0,1/2,3/4,1,0,1).}
]

Its weighted discharges are (0,0,1,1,1), exactly equal to each event's price. Every successful full typed `R_leaf` goal has (Phi=0). For a completely peelable source (K(E)=\varnothing), with (m=|E|), initial (Phi=m/2+3m/2+1=2m+1). Every valid terminal history contains (m) PEEL, (m) RESTORE and one HALT, yielding an exact matching upper bound **within this calculus**.

For the LP maximizing (m\lambda_{SEP}+2m\lambda_{FUS}+\lambda_{MACHINE}), the *independently checkable nonnegative dual* has (y_{PEEL}=m, y_{RESTORE}=m, y_{HALT}=1). Column feasibility is

[
y_{PEEL}\ge m,\quad 2y_{PEEL}\ge2m,\quad
-y_{PEEL}+y_{RESTORE}\ge0,\quad y_{HALT}\ge1.
]

The dual objective is (y_{PEEL}+y_{RESTORE}+y_{HALT}=2m+1), certifying **exact equality of primal and dual**. This adds an order-independent `SEP` ticket to TMR-2/041's prior certificate without falsely increasing the minimum work.

## 5. Concrete hostile controls and falsifier

**Genuine shortcut control:** If a *different* calculus explicitly authorizes PEEL with zero price, it contributes the very same nonzero vector ((\Delta_{SEP},\Delta_{FUS},\Delta_{GAMMA})=(1,2,-1)) but cost zero. The displayed rational weights discharge **one** and fail immediately. This new operation must be included if genuinely present; it cannot be hidden in closure or removed by CEGAR. In the unchanged `R_leaf` it is **not** a legal free step.

**Satisfiable nonempty core:** the four triples on four variables form a stable 4-edge core but admit a two-TRUE/two-FALSE NAE assignment. **Unsatisfiable nonempty core:** all ten triples on five variables have no eligible leaf and are UNSAT by the pigeonhole principle. A core-size obstruction must not classify either case without an independent SAT/UNSAT authority.

**Exponential-rank but empty-core control:** TMR-2/040's (Q_k) has (m=k(k+1)/2) authenticated NAE edges, each with a private edge variable, so (K(E)=\varnothing); its original X/private evaluation matrix still has rank (2^k). Its signed existential projection onto X is identically TRUE by TMR-2/041. The canonical `SEP` ticket is merely (m), and the **full** typed replay tariff is (2m+1), polynomial in encoded size. Arbitrary per-edge literal signs do not change the core or local witness constructor.

**Other required controls:** affine/Gaussian shortcuts, Horn, dual-Horn, 2-SAT, bounded-treewidth DP, equality and autarkies, extension variables, compact circuits, learned clauses, preprocessing, renaming, padding, input rereading, caching, recomputation, sharing and alternate source encodings are never ruled out in an arbitrary SAT machine. Duplicate signed clauses are not new paid edge identities. This analysis neither uses nor upgrades historical `/341` (FAIL full logical UNSAT authority) or `/386` (RESTRICTED guarded odd-charge fragment).

## 6. Reproducibility and independent scope

The **exact V8-executed `audit()` function**, serialized into `experiments/tmr/tmr4_leafcore_tariff082.js`, ran **17,487 assertions, zero failures**. Exhaustively enumerated **all 1,024** hypergraphs formed by subsets of the ten triples on five vertices, every legal PEEL (**430** local rows), all maximal peeling terminal sets via memoized recursion, the canonical core, and all applicable rational tariff checks. All 1,024 terminal sets are singletons and equal their computed cores; 156 inputs peel completely. Separate signed (Q_k) checks cover (k=2..8), **508** boundary assignments and **14,844** authenticated signed-edge evaluations. SAT K4 and UNSAT K5 core controls, toy nontrivial SCC, and added-free-PEEL violation passed. All enumerations are finite **COMPUTATIONAL** evidence; the unbounded theorem is the independent symbolic argument above.

- **Source:** `experiments/tmr/tmr4_leafcore_tariff082.js`
- **Native raw:** `results/raw/tmr/2026-11-15_0240_TMR4_LEAFCORE082_V8_RAW.json`
- **Seven-column exact matrix and LP:** `results/raw/tmr/2026-11-15_0240_TMR4_LEAFCORE082_TARIFF.json`

Sources actually read: governing 2026-11-14 directive; November 13 TMR replacement; both root trackers and `main.tex` (the latter two recovered from full authentic Git blobs since contents API exposed empty text); current issue #3 (2,126 comments), `AGENTS.md`, `CODEX.md`, repository research skill, five latest TMR handoffs; TMR-2/041 original report, executed JS, raw and tariff; TMR-2/040 and TMR-5/037 originals; TMR-4/041; LEAD-0029 Lipschitz audit. Primary contextual literature: Schaefer, STOC 1978, DOI [10.1145/800133.804350](https://doi.org/10.1145/800133.804350); Jiang, Mitzenmacher and Thaler, *Parallel Peeling Algorithms* (2013), [arXiv:1302.7014](https://arxiv.org/abs/1302.7014). The latter concerns a related hypergraph-core peeling process, **not** this exact signed-edge rule or its tariff theorem. The proof here is self-contained.

**Exact limitations:** The record-calculus bound does not force an arbitrary correct uniform multitape SAT decider to PEEL, RESTORE, materialize a full signed stack, or use this source grammar. If a nonempty core prevents a successful typed record goal, absent proof coverage cannot be mistaken for a time lower bound. No general machine transition simulation, no superpolynomial fusion-safe initial potential, and no same-system algorithm-transfer implication is established. P versus NP OPEN.

**Next peer repair:** TMR-2 verify signed leaf-core confluent quotient independently; TMR-3 compile the complete authenticated signed witness constructor to charged finite-tape operations; TMR-5 test batch/shared shortcut and objective/goal scope; TMR-1 maintain proof-system versus machine quantifiers. TMR-4 next: an actual fixed-program SAT front-end where this core-reducer is a *paid* subroutine and all Gaussian and compact learned paths remain conservative MAY. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root manuscript and all five existing schedules untouched.
