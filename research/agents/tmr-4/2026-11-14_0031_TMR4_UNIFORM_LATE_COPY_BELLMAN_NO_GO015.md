# TMR-4/015: one fixed correct machine can postpone its complete source copy until after deciding

**Pacific timestamp:** 2026-11-14 00:31 PST (America/Los_Angeles). **Identity:** NEW TMR-4, Cost-Sound Abstraction. **Result status:** CANDIDATE/RESTRICTED, pending TMR-5 or TMR-1 independent mathematical review. Finite tests: COMPUTATIONAL. General 3-SAT time lower bound: OPEN. P versus NP: OPEN.

## 1. New exact scoped construction (TMR4-LC15)

**Model and quantifiers.** Let A be **any one fixed finite total uniform deterministic** multitape machine deciding a binary language, including explicit encoded 3-CNF SAT with a specified malformed-input response. A uses h>=1 **locally moving read-only original-input heads** initially at the left endmarker (position 0), a fixed finite alphabet/control, and finitely many locally moving writable work tapes. The source is x of encoded length L data bits with left and right endmarkers at positions 0 and L+1. Count all physical transitions as time and all visited writable cells as space. Input head movement/revisiting, parsing, algebra, caching, recomputation and output are paid. SAT and UNSAT halt labels (and a declared malformed label, if present) are kept distinct.

**Theorem (CANDIDATE pending independent review).** From every such A, construct **one fixed** correct total uniform machine B_A, with one additional writable copy tape, whose behavior on **every binary input** x is:

1. Physically simulate A(x) exactly, including all work tapes and original-input accesses. Intercept the halting transition and remember its actual output label b in finite control, rather than halting B_A.
2. Return all h original-input heads to the left endmarker, one local step per unit of maximum head distance. Keep all A work-tape contents unchanged.
3. Perform a complete, paid, physical copy of left endmarker, L source bits and right endmarker to the fresh copy tape, moving local heads only. Designate the state **READY** immediately after the right endmarker has been written.
4. On the **next single physical transition**, halt with the b already computed. Both labels, and malformed responses, are unchanged.

Writing p_j(x) for the final original head positions immediately after A's terminal step and R_A(x)=max_j p_j(x), the explicit implementation satisfies

$$
T_{B_A}(x)=T_A(x)+R_A(x)+(L+2)+1,
\qquad
0\le R_A(x)\le\min\{L+1,T_A(x)\},
$$

and under the stated visited-cell accounting with the fresh tape alone as auxiliary storage,

$$
S_{B_A}(x)=S_A(x)+(L+2).
$$

In particular, for **every x**, the paid computation **after completion of B_A's designated full source-copy tape** is exactly one transition:

$$
T_{B_A}(x)-t_{\mathrm{READY}}(x)=1.
$$

This is an all-length **fixed-program** construction: B_A depends on A but does **not** depend on x, L, or its SAT/UNSAT label. The exhaustive or otherwise costly decision made by A is completely charged **before** READY. There is no nonuniform answer table, runtime SAT oracle, unbounded-word primitive or free translation.

**Proof of physical implementation.** A finite compiler places A's transition table inside B_A. Each original unit transition is reproduced once using B_A's original h read-only heads and original writable tapes. A halting transition is redirected to a nonhalting finite-control phase carrying the finite output label. At that moment each original head is at p_j in [0,L+1]; all started at 0 and move locally, hence p_j<=T_A. In RESET, B_A moves all non-leftmost heads left simultaneously and keeps heads at 0 stationary, so exactly R_A physical transitions suffice, with no extra writable memory. In COPY, one head reads positions 0,...,L+1; in each of L+2 actual transitions the fresh tape head writes the current symbol, advancing locally except on the last transition. The complete copied word is source-bound and exact, including both endmarkers. READY retains all original work tapes plus the copy and the recorded output label. A finite transition table can emit the stored label and halt in one more transition. Every phase is total if A is total, and B_A is one fixed program for every L. Each step is charged. The extra work-tape footprint is L+2 visited cells; all original visited cells stay counted.

**Important stage qualification.** READY is the completion of a **specified new charged copy tape**, not necessarily the *first* time any source-like data occurs somewhere in A's workspace, nor the first input-bit observation. An assertion mandating copy-first-before-compute is a restriction on algorithms, not an unrestricted machine-model theorem. TMR-4/003 already disproved a late-input-read processing premise with speculative two-completion work; the present construction establishes the different **late-completed-copy** consequence with one fixed A-dependent program for all inputs. TMR-4/014 instead used a *different hardwired program per chosen F* to defeat **program-oblivious** prepared-state potentials; LC15 defeats even program-indexed post-copy progress potentials on this specified checkpoint. These claims must not be conflated.

## 2. Full-configuration abstraction and maximal potential ceiling

Let C be the exact configuration graph of **this fixed B_A on fixed x**, including B_A's program, input, all input and work heads, all visited writable contents, phase and remembered true output b. Every actual edge costs one. The exact identity abstraction relates a concrete state to itself, so initial, **every-transition** and SAT/UNSAT terminal preservation all hold. No different-machine configurations are merged. In the general MAY case, require for *every* related concrete step c->c' and every related abstract state a a finite abstract path to some a' related to c' of cost at most 1, with the correct terminal goal G_b related to B_A's actual halt.

The real READY->HALT edge is a one-step computation of B_A, not a spurious abstract path. Thus every such cost-sound abstraction includes a related path of cost at most one from a_READY to G_b. For **every** Bellman-valid potential obeying

$$
\Phi(u)\le w(u,v)+\Phi(v)\quad\text{on every abstract edge},
\qquad \Phi(G_b)\le0,
$$

telescoping along the genuine READY-to-goal abstract path gives

$$
\boxed{\Phi(a_{\mathrm{READY}})\le1.}
$$

This no-go holds even if a_READY retains the complete copied source, **the fixed program identity**, all work tapes and heads, and actual output cache. A candidate Phi(READY)=2, Phi(G_b)=0 fails on the genuine cost-one edge and must not be repaired by deleting it.

**Maximal-potential lemma (self-contained, scoped).** On any nonnegative-cost abstract graph restricted to states with some finite-cost path to an appropriate terminal goal G, define d(a,G) as the infimum cost of such paths. For each edge a->v, concatenating that edge with a nearly shortest v-to-G path proves d(a,G)<=w(a,v)+d(v,G), and d(G,G)=0. Conversely any Bellman-valid Phi telescopes on every finite a-to-G path and satisfies Phi(a)<=d(a,G). Hence **d is the pointwise greatest admissible potential on terminal-reachable states**. Zero-cost edges and cycles cause no exception. This dual statement is a mathematical *ceiling*, not an efficiently constructible SAT lower-bound potential: defining d by unknown machine paths is not a proof that it is superpolynomial. Here the explicit genuine length-one path proves d(a_READY,G_b)<=1 without solving any global reachability problem.

## 3. Implication and exact unrestricted gap

The stronger proposed post-copy processing target

$$
\forall A\,\forall k,C,L_0\,\exists F:
|F|\ge L_0\ \land\
T_A(F)-t_{\mathrm{READY}}(F)>C(|F|+1)^k
$$

is **FALSIFIED/RETIRED** when READY means the completion of an arbitrary program-designated exact physical copy tape: take B_A above, for which the residual is 1 on **every** x. It is **not** the team's actual full-run complexity target, whose quantified T_A(F) includes the early computation and remains **OPEN**. To use a stage-local necessity theorem for the latter, one must first prove a correct unrestricted, resource-charged normalization that anchors the checkpoint before computation, or instead maintain a full-trace potential that charges early and late work without double-counting.

This proof imposes no space restriction. For B_A, all original computation and polynomial or superpolynomial workspace remain charged. It cannot be converted into an all-exponent SAT time lower bound by T<=S, S<=T, source entropy, crossing sequences, or any proof-system argument.

## 4. Executed computational evidence and hostile controls

The **exact published Node-compatible standalone JS** was executed in hosted V8, implementing a physical one-head parity-deciding finite-control machine A and the four physically charged B_A phases CORE/RESET/COPY/READY. Its source head and copy work head move by at most one cell per transition, the copy includes both endmarkers, every full trace is checked, and an *independent* parity-from-string check verifies output. This is a real finite-control local-head test for the parity language, **NOT** a physical general 3-SAT TM implementation.

All 2,047 binary strings of lengths 0 through 10 were enumerated, seed none. Results: 1,023 accepting, 1,024 rejecting; 22,528 A-CORE steps, 20,481 physical RESET steps, 22,528 physical COPY steps, 2,047 single-terminal transitions, **67,584** total B transitions, and 67,584 per-edge Bellman checks, all passing. The deliberately invalid READY potential of 2 failed on all 2,047 genuine final edges, as required. **Zero assertion failures.** Distinct parity values, both endmarkers, zero length, repeated bits, alternating bits, long padding and complemented inputs occur in the exhaustive binary sweep. The separate cited historical SAT, Horn, 2-SAT, XOR/Tseitin, bounded-treewidth and independent-product example families were **not** run through a physical 3-SAT interpreter in this run; the universal construction is syntax-agnostic and applies if A decides them correctly.

Published exact code: `experiments/tmr/tmr4_late_copy015.cjs` (Git blob `b2b6c2b2d4c6deb7c227e17d370092d6e0a73239`), executed in hosted V8. Raw machine-readable output: `results/raw/tmr/2026-11-14_0031_TMR4_LATE_COPY015_RAW.json` (blob `3912ece70dd163ec72fa9839a7969a5b138171c3`). No native OS Node, independent Python, physical SAT solver, full repository preflight or LaTeX compilation was executed. Tests are COMPUTATIONAL; theorem proof is the explicit symbolic machine compiler.

## 5. Sources, provenance, and historical safeguards

- Patrick and Radhia Cousot, *Abstract Interpretation*, POPL 1977, pp. 238-252, primary author bibliography https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml, DOI https://doi.org/10.1145/512950.512973. Its overapproximation principle is background; neither the phase theorem nor the graph-potential dual is attributed to it.
- Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, primary publisher https://doi.org/10.1145/1101821.1101822. Its random-access-machine bounds rule out certain simultaneous n^c time and n^d **small-space** pairs, not all polynomial-time uniform deciders.
- Original TMR-4/003: `research/agents/tmr-4/2026-11-13_1440_TMR4_DEFERRED_FINAL_SYMBOL_FALSIFIER003.md`, post-final-read temporal relocation counterexample; original TMR-4/013: `research/agents/tmr-4/2026-11-13_2245_TMR4_COPY_READY_POTENTIAL_TRANSFER013.md`, copy-**first** transfer; original TMR-4/014: `research/agents/tmr-4/2026-11-13_2336_TMR4_PROGRAM_OBLIVIOUS_READY_NO_GO014.md`, program-**blind** prepared-state no-go. LC15 complements, does not retroactively strengthen their original scopes.
- Historical original restricted abstraction and genuine accepted counterexamples: `research/agents/lspv-5/2026-11-09_0944_LSPV5_HISTORY_SEPARATED_DAG_ABSTRACTION464.md`, `research/agents/lspv-5/2026-11-12_1748_LSPV5_NATIVE341_EDGE_SUFFIX_NORMALIZER514.tex`, `research/agents/lspv-3/2026-11-10_1224_LSPV3_ACCEPTED_SAT_SOURCE_NATIVE_CHECKER551.md`. These concern a pinned proof checker or proof DAG, and are not a general-TM restriction. No actual accepted counterexamples were deleted or reclassified.

**Repository read contract.** Read the superseding 12:49 PST TMR-five directive FIRST, then complete proof1 (28,714 characters; blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), full authentic proof2 via Git blob (1,051,196 characters; blob `930c5eeddafce656717f28055a7a9a755f44737c`), full root main.tex via Git blob (2,518,238 characters; blob `0233cb0ca16a63a2a63a83af6a61ffe985632945`), AGENTS.md, CODEX.md, repo pnp-research skill, newest five TMR handoffs and issue #3 (1,993 comments through TMR-2/014). A blank content-API body with nonblank SHA was **not** interpreted as an empty file. Historical conflicting old role allocations were superseded; scientific evidence preserved.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No proof1/proof2 rewrite and no root main.tex change. TMR-5 remains whole-document synthesis owner and should add this new CANDIDATE in its authorized region only after independent checking. No scheduled tasks, identities, schedules or enabled states were changed.

**One next target:** TMR-5/TMR-1 should independently verify the finite-control phase-relocation compiler and physical `R_A=max p_j` accounting. After that, TMR-4 should seek or falsify a **checkpoint-invariant, full-execution** cost potential whose lower bound charges A's work wherever it occurs and remains sound for every compact algorithmic representation.

END_OF_REPORT::TMR4::LATE_COPY015::2026-11-14_0031_PST
