# TMR-4/013: exact copy-ready potential transfer and loss of source-only processing bounds

**Date:** 2026-11-13 22:45 PST (America/Los_Angeles). **Role:** NEW TMR-4 Cost-Sound Abstraction, j15marti/pnp main.

**Scientific status:** The explicit TMR-1/012 bounded-local-input-head simulation receives a favorable INDEPENDENT CONSTRUCTIVE AUDIT at **PROVED/RESTRICTED mathematical model scope**. The new copy-ready potential transfer and full-observation degeneration are **CANDIDATE pending TMR-5/TMR-1 independent mathematical review**. Actual executed finite tests are **COMPUTATIONAL**. This neither proves a superpolynomial SAT lower bound nor P != NP. Both P versus NP routes remain **OPEN**.

## Claim and exactly declared machine scope

Let A be one fixed finite total deterministic h-read-only-input-head, r-writable-work-tape machine, with binary input x of exact L data bits between left/right endmarkers, h initially left-aligned locally moving read-only heads, fixed finite alphabets/control and physical unit-time transitions. At each step the h input heads read their pre-move symbols, may move left/stay/right but cannot cross endmarkers, and all writable tapes are updated by a single transition. Every visited writable work cell is charged. A can be ANY fixed total program for all lengths, including a correct SAT decider using compact algebra, caching, sharing, rereads, preprocessing or recomputation. Malformed inputs and both terminal labels are handled without a promise. No random-address unit-cost input port or input-length-dependent program is silently admitted.

Construct B_A with one physical original-source head and h extra writable source-copy tapes. COPY reads L+2 source/endmarker symbols and writes each simultaneously onto all h clones, using L+2 paid transitions and ending with the original input head at the right endmarker. REWIND moves the h clone heads left together for L+1 paid transitions, restoring their initial left-endmarker position. RUN simulates every A step by reading the clone symbols without modifying clone content, retaining A's fixed program/control and all original writable work tapes. Original source head remains parked. The preparation cost is exactly

$$
b(L)=2L+3.
$$

Let c be an arbitrary concrete configuration of A on x and let iota_x(c) denote the corresponding B_A RUN configuration, with the entire original x and BOTH endmarkers copied on all h clones, each clone head at the appropriate original input-head position, all original work tape contents/head positions preserved, RUN finite control tagged with A's control, and the true original-source head parked at the right endmarker. This is an exact program-dependent injection on A configurations (the source x is fixed and physical). It preserves BOTH terminal labels.

For EVERY concrete legal A step c -> c' of cost 1, including any representation conversion, cache write, input reread, tape rewrite, algebraic operation or recomputation,

$$
iota_x(c)\ \longrightarrow\ iota_x(c')
$$

is one actual B_A transition of cost 1. In particular, no source-only proof calculus or solver template is imposed. The complete B_A initial configuration reaches iota_x(c_0) by exactly b(L) paid steps. Thus, for every x,

$$
T_{B_A}(x)=T_A(x)+b(L), \qquad
S_{B_A}(x)=S_A(x)+h(L+2)
$$

under the explicit visited-cell convention with no additional auxiliary tape. These are equality statements for the declared construction, not for other machine conventions. The model-independent bounded-overhead statement is O_A(T_A+L) time and O_A(S_A+L) space.

## New scoped transfer theorem

Fix ANY MAY abstraction of actual configurations of this fixed B_A, with a relation R, such that (i) the initial and prepared states have related abstract representatives, (ii) EVERY physical transition from EVERY related concrete state is representable by a finite abstract path costing at most that physical transition, and (iii) both actual terminal labels relate to appropriate abstract decision goals. Allow zero-cost abstract edges and arbitrary cycles. Let Phi be any real-valued potential that satisfies

$$
\Phi(u)\le c(u,v)+\Phi(v)
$$

on EVERY abstract edge and Phi(goal)<=0 on every terminal goal.

Then for every abstract state a_ready related to iota_x(c_0) for which the transition-simulation obligation holds, and for every appropriate abstract initial state a_cold related to the true initial B_A configuration,

$$
\boxed{\Phi(a_{\mathrm{ready}})\le T_A(x)}
$$

and

$$
\boxed{\Phi(a_{\mathrm{cold}})-(2L+3)\le T_A(x).}
$$

**Proof:** Begin at the related prepared RUN state. Inductively represent all T_A(x) physical A transitions using the explicit embedding iota_x and the stipulated all-step abstract simulation; follow the appropriate SAT or UNSAT goal, telescope Phi along that entire abstract path and use Phi(goal)<=0. For the cold state prepend the actual L+2 COPY and L+1 REWIND transitions of B_A, whose abstract images together cost no more than 2L+3. The same telescoping argument applies. This charges every operation of A, including its original workspace; it does not use A's unknown runtime to define Phi. Nor does it prove that Phi(a_ready) is large. The theorem holds for any correct SAT decider A, not only a prescribed algorithm family, provided the initial all-transition cost simulation premises are actually proved.

## New obstruction: all source-only necessity is already discharged at the prepared state

Augment B_A's physical trace with a GHOST set V of data coordinates read by its original physical source head, without giving the machine this information as advice. Each L+2 step COPY pass reads the L data positions once, so

$$
V_{\mathrm{ready}}=\{0,\ldots,L-1\}.
$$

For ANY family of independently certified nonempty same-length opposite-label difference supports D_i, the source-observation potential of TMR-4/009 through /012 is exactly zero at the prepared state:

$$
\Psi(H_{\mathrm{ready}},V_{\mathrm{ready}})=0
$$

because every D_i is hit. This conclusion holds even when A has not performed a SINGLE simulated computational transition, and even if B_A's extra writable clone tapes contain the complete source. Hence all-source-observation potentials can yield an O(L) bound at B_A's cold initial state but yield **no positive processing bound on the simulated A** through the sharper prepared-state transfer. This is a precise limitation, not a claim that SAT can be decided in O(L).

Any proposed abstraction that tries to traverse COPY/REWIND at zero cost while retaining a positive source-observation potential is unsound: it violates the all-edge potential inequality. Equally, omitting clone contents or restricting memory retention is not a legal proof of unavoidable processing. A new computational potential must attach to the FULL RUN state, including prepared stored source, program/control, writable tapes/heads, remaining work and all costs.

## Executed independent replay, corrections and hostile controls

A fresh standalone hosted-V8 JavaScript emulator was authored independently of TMR-1/012's wrapper. It explicitly executes each COPY, REWIND and RUN transition with actual per-clone stored symbols, separate clone head coordinates, work tape maps, visited cells, parked physical read-only head, finite machine control and both final labels. The source is a finite transition construction over seven fixed deterministic synthetic control modes (all lengths share each fixed mode), not an implementation of general SAT. Exact GitHub source:

- experiments/tmr/tmr4_copy_potential_bridge013.cjs
- results/raw/tmr/2026-11-13_2236_TMR4_COPY_POTENTIAL_BRIDGE013_RAW.json

**Executed corrected full run:** 5,355 A/B pairs (all binary inputs of lengths 0 through 7, h=1,2,3, seven finite-control modes), 38,147 exact paired simulated A/RUN transitions, 43,008 actual COPY steps, 37,653 actual REWIND steps, 38,147 full-state comparisons, 3,162 accepting and 2,193 rejecting final outputs, 5,334 complete-data-bit ghost-set checks and three hostile tests. **Zero failures**. The complete paid runtime identity and extra h(L+2) visited-clone-cell count held for every pair. This is a stepwise emulator, not merely two calls reading the same original array.

The FIRST attempted V8 run had 5,335 failed assertions because its tester recorded source position p in zero-indexed ghost V as p rather than p-1. It did NOT publish any artifacts. The physical A/B full-trace comparisons already matched. Correcting this test-only data-coordinate indexing and rerunning the entire exact suite yielded zero failures; the corrected exact runnable source and raw JSON are what is published. Historical failures are not silently discarded or promoted as physical counterexamples.

Hostile controls: stopping REWIND one tick early leaves clone heads off the required starting location; mutating a copy-bit breaks the correspondence invariant; and adding a purported zero-cost edge from an unobserved source state with positive last-bit potential directly to the fully observed prepared state violates Bellman soundness. All three detected the intended defect.

**Not executed:** native OS Node.js replay of the newly published source; general arbitrary-SAT TM; native instruction-level formal implementation; all-input complexity verification; LaTeX compilation. The test is finite COMPUTATIONAL evidence, separate from the mathematical construction.

## Dependencies, primary sources, conflicts and status

- TMR-1/012: research/agents/tmr-1/2026-11-13_2204_TMR1_MULTI_INPUT_HEAD_COPY_BRIDGE012.md and exact original experiments/tmr/tmr1_input_head_copy012.cjs. Original /012 actually emulates A and B core traces with replicated arrays; this run separately executes every paid preparation step and checks exact head/tape state.
- TMR-4/012 and TMR-5/009: original multihead MAY potential and its independent review; this run identifies precisely why a pre-copy source lower bound is not automatically a post-copy processing lower bound.
- TMR-3/011: restricted crossing-splice and same-machine space accounting. The copy bridge adds h(L+2) writable cells, and therefore small-space crossing-product statements on B_A cannot be transferred unchanged to A.
- Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973, https://pcousot.github.io/publications.html (general sound overapproximation, not a resource lower bound).
- Hennie and Stearns, JACM 1966, DOI 10.1145/321356.321362, https://www.cs.toronto.edu/tss/files/papers/HennieStearns66.pdf (historical tape-model simulation; its T log T theorem is DIFFERENT from this exact h-read-only-head copy construction).
- Hartmanis and Stearns, Transactions AMS 1965, DOI 10.1090/S0002-9947-1965-0170805-7 (classical machine-model/time foundation, not a specific SAT lower bound).
- Historical original checker and abstraction hazards also read: research/agents/lspv-3/2026-11-10_1224_LSPV3_ACCEPTED_SAT_SOURCE_NATIVE_CHECKER551.md, research/agents/lspv-5/2026-11-12_1748_LSPV5_NATIVE341_EDGE_SUFFIX_NORMALIZER514.tex and research/agents/lspv-5/2026-11-09_0944_LSPV5_HISTORY_SEPARATED_DAG_ABSTRACTION464.md. Their source-authentication and quotient/charge counterexamples survive; their restricted checker scope does not bind these actual TM transitions.

**Mandatory controls:** Horn, 2-SAT, XOR/Tseitin with GF(2), bounded-treewidth, products, padding, variable renaming, auxiliary variables, sharing, compact algebra, input rereading, and caching/recomputation are ALLOWED by the arbitrary-A embedding. They were NOT separately physically executed in this synthetic test. No uncharged oracle, nonuniform advice, proof-system assumption, hidden ETH/SETH or unknown-runtime-defined potential appears. Programs that exploit such algorithms are legitimate possible A.

**Resource target:** For every one fixed correct total deterministic SAT decider A across all lengths, and all k>=1, C>0, L0, some valid F of |F|>=L0 must satisfy T_A(F)>C(|F|+1)^k. TMR1's copy preserves this exact all-exponent time quantifier under its declared machine model but does not preserve sublinear-space lower-bound premises. A conditional telescoping transfer is NOT an existence theorem for a superpolynomial Phi. This missing implication remains **OPEN**.

**Repository corpus/read audit:** Superseding TMR replacement directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 read first and rechecked before shared publication. proof1.txt full 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2.txt full authentic Git blob 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c (ordinary fetch blank), root main.tex authentic Git blob 2,511,782 characters SHA c04a02a97492f88938791f363ff91d99b67cd78b (ordinary fetch blank); AGENTS.md, CODEX.md, pnp-research skill, issue #3, all five current TMR handoffs, relevant original reports/checkers and primary literature. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex unchanged because TMR-5 owns whole-document synthesis. No scheduled task was modified.

**One next target:** TMR-5 should independently audit the prepared-state transfer and source-potential-zero conclusion, preferably native Node replay of the exact Git blob. Then construct or falsify a nonzero FULL RUN-state processing potential under arbitrary stored-source representations and polynomial workspace. All-exponent SAT lower bound and P versus NP stay OPEN.
