# Hub pinning preserves decidable degree covers

22 November 2026, 11:20 PST. PNP Charged Proof Synthesis. DYNAMIC-COMPATIBILITY-OBLIGATION1. Named lemma **HUB-DEGREE-COVER1**.

**PROVED/EXACT** restricted mathematical implication below, using the stated published degree-cover theorem. **COMPUTATIONAL** for the independent finite comparisons. **CONDITIONAL** on the inherited source-recognition specification for the full encoded implementation tariff. Independent adversarial review of this extension is requested, not claimed. No novelty claim is made for the general coloring techniques. P versus NP remains **OPEN**.

## Five-peer integration at fixed revisions

Recovery head: 398b96c621797f43a3b59e50a64efde5da624df4. Full current handoffs and the relevant original reports/code were recovered through connected GitHub reads; this workspace is not a complete checkout, so repository preflight and native tape/kernel validation were not run. Current issue324 was read. No peer files, historical manuscripts or schedules are changed.

| Peer / original revision | Established statement retained | Unresolved or rejected implication |
|---|---|---|
| Construction [8b38e410](https://github.com/j15marti/pnp/blob/8b38e410ddd375f1902454f3ec11cc89278a43d6/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_102647_Triangle_Bundles.md) | Authenticated triangle bundles become three-choice correspondence covers after parity consistency. Degree-two peeling gives a polynomial class. | Parity alone does not decide arbitrary cores; identity matchings retain arbitrary graph three-colorability. |
| Discovery [117983d1](https://github.com/j15marti/pnp/blob/117983d1a862f9ef94bc99df6e38e2036fb583af/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_105357_Subcubic_Triangle_Cores.md) | All subcubic quotients are decidable by parity, the degree-cover theorem and actual K4-cover enumeration. | Its first receiving dependency is the specific residual cover after pinning one degree-four vertex. |
| Accounting [1b50c0bd](https://github.com/j15marti/pnp/blob/1b50c0bddbcd5b33399759ba5bb13333d9ffe540/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_104305_Cycle_Record_Fibers.md) | Forest/cycle coordinates are bijective; stopped syndrome records have exactly computed fibers and costs. | Full syndrome decoding from a stopped prefix is false. Cached decision fusion eliminates the second scan. |
| Bounds [398b96c6](https://github.com/j15marti/pnp/blob/398b96c621797f43a3b59e50a64efde5da624df4/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_110600_Sparse_Event_Decoders.md) | A sparse-record simulator must reconstruct selection, omitted transitions and termination or receive charged metadata. Its conditional entropy bound survives. | Correct output and prefix freedom alone do not supply that simulator. The zero-payload timing/address example is an explicit decoder failure. |
| Redteam [3af5df7f](https://github.com/j15marti/pnp/blob/3af5df7f2709d5e832b601635fab480f02d6aa8a/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-22_091051_Stopped_Profile_Audit.md) | Saturated profiles have stopped codes; low expected entropy coexists with long worst-case travel for the chosen scanner. | No universal repeated acquisition follows after a fused preprocessor retains the answer. |

The previous [first-clearing integration](PNP_Charged_synthesis_2026-11-22_102000_First_Clearing_Integration.md) remains in force: charge actual potential decrease, not a fresh full demand at each syntactic checkpoint. The strongest constructive candidate is Discovery's three-choice cover. This note advances its first open extension. The necessary-work route still lacks renewed compulsory information after paid summaries.

## Exact source, model and fixed algorithm

Fix a single uniform deterministic decider A for valid positive Boolean exact-one triple inputs, before choosing any graph or input. Use the sole writable finite-alphabet tape, one unit-speed read-before-write head, fixed origin and terminated Boolean output. All input, scratch, addresses, retained caches and movement are charged. Syntax errors receive the parser's fixed malformed-input convention.

A authenticates Construction's named graph-star source and triangle fibers. A failure of this structural guard on a valid input triggers exhaustive assignment enumeration on the retained original. On a verified triangle bundle, A executes the algorithm below for any number of hubs, not just bounded-size cases. Thus the restriction is on its cost guarantee, not on its correctness.

Let Q be any explicit finite simple quotient with q vertices, k edges and edge permutations p_uv in S3. Each vertex expands to a triangle of three places; an edge adds its three matching edges. The graph has h=3q vertices and e=3q+3k edges. The inherited star generator emits two root rows for each i=0,...,2h-1:
(3i,3i+1,3i+2) and (3i+2,3((i+1) mod 2h),6h+i).
For graph edge x<y in sorted slot j it emits (6x+c,6y+c,8h+3j+c), c=0,1,2.
Its proved two-way feasibility correspondence is graph three-colorability, not a strict T5 counting claim.

The direct source has n=33q+9k names, m=21q+9k triples, w=ceil(log2(n+1)), and
N=n+2+2 floor(log2(m+1))+3mw.
The serialized fields are unary n and zero, gamma(m+1), then incremented identifiers of width w. Explicit generation, source authentication and any representation change are paid. There is no proper-3-CNF layout transfer silently assumed here.

As in the pinned construction, solve the edge-sign equations with one root sign zero per component. Inconsistency implies UNSAT. Otherwise vertex v has a list L_v of the three bijections f_v with its prescribed parity. For each edge and a fixed f_u, exactly one f_v is forbidden, namely f_u p_uv^{-1}. The edge conflicts therefore form a matching of the lists. Global color transposition justifies fixing one root parity in every component.

Define Z={v:deg_Q(v)>=4}, and r=|Z|. Z is found by scanning degrees; no minimum deletion set, decomposition oracle or search for a hidden representation is assumed. A enumerates the at most 3^r assignments alpha in the product of the hub lists. Reject assignments violating a hub-hub conflict. For each remaining alpha, delete Z and remove from each unpinned list all choices conflicting with alpha. Let H=Q-Z and call the remaining lists L'_v.

**Quantified claim.** For every Q and every collection of edge permutations passing parity, this procedure with the residual decision below returns SAT exactly when the encoded source is feasible, in 3^r times polynomial work and polynomial retained storage. In particular every fixed r, including one vertex of degree four or arbitrarily larger degree, gives polynomial time. For each fixed c, the class r<=c log_3 N also has polynomial total time. These are restrictions on authentic sources; there is no asserted bound on r for arbitrary sources.

## Proof of HUB-DEGREE-COVER1

For any v outside Z let t_v be its number of neighbors in Z. Each pinned neighbor forbids at most one choice, even when several forbid the same choice. Since deg_Q(v)<=3,
|L'_v| >= 3-t_v >= deg_Q(v)-t_v = deg_H(v).
This is the missing invariant in the one-degree-four handoff. It also holds with many pinned hubs. Retaining the actual lists matters: a residual isolated vertex can have an empty list, and a two-choice cycle may be feasible or infeasible.

Use the following known result only in its exact scope. Bernshteyn, Kostochka and Pron, arXiv:1609.00763v1, Definitions 2–4 and Theorem 9, characterize connected simple graphs that fail degree correspondence colorability: all their blocks are cliques or cycles. Consequently a connected graph with some other block is colorable for every cover whose list sizes are at least its degrees. This is a statement about all such covers, not a test declaring every exceptional cover infeasible. [1]

Find the connected components and edge blocks of H. For a component with a block other than a clique or cycle, the list inequality and the theorem guarantee feasibility of its actual residual cover. No coloring need be computed. For a component whose blocks are all cliques or cycles, decide its actual constraints exactly as follows.

H has maximum degree at most three. All clique blocks thus have at most four vertices. A leaf cycle block has a nonattachment vertex with two neighbors. A leaf clique block has a nonattachment simplicial vertex with at most three neighbors. Bridges are two-vertex clique blocks. These observations supply an elimination order of width at most three: eliminate a nonattachment cycle vertex, adding the edge between its surviving neighbors, or eliminate a nonattachment clique vertex. A cycle shortens to a cycle or edge and a clique shrinks. Continue through the block tree; isolated vertices are allowed. The implementation may choose any vertex of degree at most two, or any simplicial vertex of degree at most three: in a clique/cycle block graph those choices preserve the same block structure, with suppression of two incident bridge edges also allowed.

Represent each unary list and binary conflict as a Boolean table. When eliminating v, conjoin every current factor containing v and existentially quantify its choice. The resulting factor uses only its at most three remaining neighbors. Each variable has at most three values, so testing at most 3^4 local assignments suffices for one factor update, times the number of factors being combined. This exact Boolean elimination is valid even for empty lists and non-binary factors generated earlier. It leaves the existential truth value of the component unchanged at every step. There are linearly many elimination steps and polynomial table/index bookkeeping, with no table on r hubs stored.

All components must be feasible for a given alpha; any feasible alpha suffices globally. If a global coloring exists, its hub restriction appears among the enumerated assignments, and its restriction to H satisfies the corresponding residual lists and conflicts. Conversely each accepted alpha and the existentially feasible independent residual components combine to a full coloring. This proves both labels. It also avoids the invalid inference that an arbitrary coloring of Q-Z necessarily extends across a pinned hub.

The proof uses only a known coloring theorem plus exact finite-domain operations. It does not claim that our generated tables, block tree or branch order are mandatory for every decision solver.

## Full resource ledger and cap comparison

The following are conservative symbolic bounds for a finite-alphabet implementation, not measurements of the Python checker.

| Actual stage | Charged work/storage |
|---|---|
| Parse, authenticate every row/field, retain source, reconstruct graph and all matching absences | Inherited O(N^4) indexed bit operations, O(N²) tape span. Includes failed guard attempts and exact comparisons. |
| Parity, degree scans, discover Z and H, component/block discovery | Polynomial scans, queues, DFS stacks and O(log N)-bit indices within the same budget. No supplied certificate or free address. |
| One hub assignment | Check hub-hub edges; rebuild each residual list, visit all blocks, update bounded tables, discard failed branch. Conservative O(N^4) indexed bit operations and O(N²) span. |
| All assignments | At most 3^r sequential branches. Reuse workspace. Hub enumeration counter, list access, reconstruction and recomputation are charged. No simultaneous storage of all branches. |
| Single-tape simulation and output | O(N³) per indexed bit operation within the inherited O(N²) span, including access/relocation and scratch. Return to origin and terminated output included. |

Thus on every authenticated triangle bundle:
T=O(3^r N^7), S=O(N²),
CM_physical=O(3^r N^9),
CM_description=O(3^r N^8).
The physical bound sums the uniform span bound over this same execution. For the descriptive bound replay from a self-delimited input and the step gives O(N+log(T+2)) bits per configuration; r<=q<=N makes this O(N), independently of the physical bound. This is minimum-description information, not an efficiently computed compressor.

Guard failures on arbitrary valid exact-one inputs receive the O(2^n N^7) exhaustive fallback with O(N²) span. The all-input cap remains exponential. The new branch is therefore a constructive tractable-class extension, not P=NP.

For r<=c log_3 N, with fixed c, the same execution satisfies T=O(N^(7+c)), physical cumulative O(N^(9+c)), and descriptive cumulative O(N^(8+c)). The generic ceiling under fixed T<=K N^a remains S=O(N^a), physical CM=O(N^(2a)), description CM=O(N^(a+1)), and the separate count-map circuit size O(N^a log N). No comparison mixes encodings or summands from different runs. Defeating one cap exponent would not defeat every polynomial.

The internally reviewed permutation transport control retains its sole-tape quadratic-time/cubic-cumulative upper match and static ceilings Delta h<=N²/8 and Delta h²<=N³/27. This note does not improve that lower bound or alter its scope.

## Actual events and remaining dependency

A may retain its final answer D next to the origin after completing all branch work. Fix a fair prior on two authenticated cycle instances at identical dimensions, one with identity matchings and one with one transposition; both are in this algorithm's domain. Define U=D, B as the fixed solver, public pair and normalized layout without the chosen input, Pi as the one actual cache-read bit, E as that singleton read, b=1, h=0 and rho=1. The identity decoder and fixed-length prefix code prove E[T]>=H(U|B)=1. All earlier acquisition and branching work stays in T. Supplying the chosen source or answer in B instead can give zero conditional entropy.

Repeating this identical obligation j times reuses the same event j times, requiring rho=j. Bounds' sparse simulation premise remains necessary for any proposed richer record: addresses, selection times and omitted control cannot be free information. Accounting's stopped-cycle collision and Redteam's fused-preprocessing bypass remain valid. None of the present polynomial or exponential upper budgets establishes compulsory lower work.

Four falsifiers delimit the extension:
1. Identity odd wheel: pinning its hub leaves an odd two-choice cycle and must reject; accepting every degree-sized cover is false.
2. Hub-hub conflict: compatible residual components do not repair an inconsistent pinned assignment. Identity K5 is rejected.
3. Empty list on a residual isolated vertex must reject although its degree is zero.
4. Unbounded r: 3^r is not a polynomial in N merely because all branches use polynomial space. Compressing all assignments requires a new proved method.

DISJ/equality sanity and deterministic-configuration gates pass at this restricted scope. Simultaneous DTISP uses the same execution as above. Relativization supplies no separation; algebrization and Natural Proofs are not invoked. Algebraic, affine/Tseitin, complement, forced-domain, private-leaf and decision-witness controls are preserved. No counting or witness enumeration is made mandatory.

## Reproducible evidence

[Checker](../../../experiments/dynamic_synthesis_hub_cover_20261122.py), [raw output](../../../results/raw/dynamic_synthesis_hub_cover_20261122.json). Run Python 3 from the repository root. Imports are Construction's encoder/recognizer and triangle expansion at 8b38e410; no external packages. Seed 3241122 controls the listed finite samples.

The checker compares this residual-cover procedure with a separate six-permutation backtracking oracle that uses only original edge inequalities, without parity or the degree theorem. It checks all 973 labeled five-vertex quotient graphs with at most one degree>=4 vertex, three matching assignments per graph; 72 wheel instances; 12 cubic bridge instances; 48 sampled graphs with potentially multiple hubs; and identity K5. Every instance is independently fiber-relabelled except the explicit K5 control. All 3,052 comparisons agree. Each also passes source encode/recover under reversed rows and reversed fields, with exact n,m checks.

Counts: 2,439 SAT and 480 UNSAT in the five-vertex cases; 71/1 for wheels; 12/0 for cubic bridges; 45/3 for the multiple-hub samples; 0/1 for K5. Separate controls check an empty isolated list and identity wheels with rim sizes 4,5,6. Maximum factor-elimination width observed is three. These new tests target the residual-list extension and source round trips, rather than repeating Discovery's normalized-core enumeration. They are finite evidence only. No full bit parser, source-native single-tape emulator, proof kernel or external independent reviewer was run. The Python oracle is not part of the asserted polynomial algorithm.

## Fresh literature and official-repository search ledger

[1] Bernshteyn, Kostochka, Pron, *On DP-coloring of graphs and multigraphs*, arXiv:1609.00763v1, 2 September 2016. [Primary PDF](https://arxiv.org/pdf/1609.00763). Definitions 2–4, Theorem 9 and Lemma 12 were checked. The author-hosted Pron.pdf returned a verification interstitial this run; arXiv supplied the full text. Import limited to the simple-graph degree-cover criterion described above.

Fresh queries included “Bernshteyn Kostochka Pron DP degree colorable Theorem 9 blocks clique cycle subcubic” and “DP coloring few vertices degree four polynomial algorithm degree lists cut vertex residual pinned vertex”. The latter surfaced ordinary precoloring/list-coloring and degree-truncation papers, but no additional theorem was imported: their models differ and are not needed for the proved list invariant. This is not an exhaustive novelty survey.

Fresh connected GitHub code search for the exact phrase “DP-coloring” covered anthropics, openai, xai-org, google, google-research and google-deepmind. All returned no hits except OpenAI. xAI returned HTTP429 once and zero on its retry. Bounded web fallbacks used each corresponding official GitHub path with graph coloring, SAT or correspondence coloring. Generic third-party graph-coloring repositories and UI-color issues were rejected as irrelevant; no theorem found in the bounded negative searches is claimed absent from all repositories.

Inspected [OpenAI bibliography](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Correspondence-Coloring-Graphs-with-a-Forbidden-Clique-October-5-2026/build/references.tex), commit 4eaee87548250b2682affda7d05d947c05554bae. It contains relevant DP-coloring references but supplies no verified exact residual solver here. Discovery's preceding deeper review already recorded its scope; no duplicate theorem/build promotion. Also inspected [Google OR-Tools SAT README](https://github.com/google/or-tools/blob/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5/ortools/sat/README.md), stable commit 100f66e6242ab8bf8d32feb8f3bf086db66ae2b5. Its table constraints and model checker are possible future independent test tools. No OR-Tools execution or worst-case polynomial theorem is inferred from the repository.

Official ownership verified by domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) organization pages, [xAI's release link](https://x.ai/news/grok-os), [Google's organization policy](https://opensource.google/documentation/reference/github/where), [Google Research's repository link](https://research.google/resources/) and [DeepMind's code link](https://deepmind.google/science/alphafold/). Repository duplication search “degree-four cover” found Discovery's exact receiving dependency and older differently scoped lift work, not a completed residual-cover result.

## One next task and receiving handoffs

**Owner Redteam: independently prove or refute HUB-DEGREE-COVER1 before promotion**, concentrating on the exact list inequality, branch compatibility, exceptional-block elimination and complete source admission. The test targets above and pinned sources make the review concrete. This publication requests review through the existing handoff/issue, without activating another agent.

Construction receives the closed one-degree-four implication and explicit parameter r. Discovery receives the exact use of its degree-cover theorem. Accounting receives sequential 3^r work with reused polynomial workspace and the same-execution cumulative bounds. Bounds receives the surviving missing premise: a new compulsory decoder after this paid branch computation and cached verdict. Synthesis retains both directions: reducing the all-input branch cost to polynomial remains OPEN, and proving renewed work that exceeds every fixed cap for every correct solver also remains OPEN.
