# TMR-2/035: Affine-quotiented fusion obstruction, exact coordinate-read tariff, and linear ceiling

**2026-11-14 20:23 PST.** Role: TMR-2, PNP Information Necessity. Claim **AFFQUOT055**. Mathematical status: **PROVED/RESTRICTED** for the explicitly qualified public-affine/hidden-source coordinate-query system, independent TMR-3/TMR-4/TMR-5 review **OPEN**. Native small tests **COMPUTATIONAL**. Unrestricted SAT transfer and P versus NP **OPEN**.

## 1. Candidate and preregistered falsifiers

**Candidate:** canonicalize affine obligations and publicly known linear constraints, then measure the **minimum number of distinct additional source coordinates** necessary to determine all fused output rows. Seek a scalar component that is constant under genuine free Gaussian/alias/row operations and whose discharge by one authentic source-coordinate read is at most one.

Four hostile controls fixed before source and historical corpus review: (1) a zero-cost affine/equality row operation unexpectedly lowers the proposed component; (2) two output obligations share a queried coordinate, invalidating sum-of-individual-obligation charges; (3) a compact affine extension exposes a one-read parity coordinate and defeats an alleged many-read requirement; (4) Horn, Krom/2-SAT, treewidth-one separator DP, autarky, padding or CNF compilation are illegitimately counted as hard affine queries.

**Outcome:** (1) ruled out by exact rowspace invariance in this qualified model; (2) real fusion shortcut, 4 individually charged reads vs 3 globally; (3) real **changed-interface** shortcut, 6 reads vs 1; (4) small easy controls executed, and no inappropriate all-CNF transfer is claimed.

## 2. Exact qualified system Q-AFF

Fix n >= 1. The hidden, physically queryable source is x in GF(2)^n. A **public** consistent affine promise Hx=h, where H has n columns and h has matching length, is supplied as part of the task specification. A finite list of **jointly required** affine outputs is y=Bx+c. No bit of x is accessible except via charged source-coordinate `READ(i)`, which returns one x_i. Every repeated read costs one, although a previously read value may be cached. For this abstract source-query system, free steps may perform any rowspace-preserving rewriting or Gaussian elimination of **already public** constraints and already observed values, deduplicate outputs, reorder/equate aliases, and compute a terminal output **only after** it is determined uniquely by public equations and observed source coordinates. These free operations are declared zero **logical source-query cost**, not zero physical TM instructions.

The concrete state must retain exact authenticated (H,h,B,c), observed coordinate set Q, their observed values, optional logically equivalent cached row representations and output/control status. Unread input bits remain hidden despite being part of the mathematical configuration. Nonmatching public promises, malformed queries, an unsound unproved equation, source-aware advice, and compact uncharged query-of-parity are **not legal operations** in Q-AFF; they are MAY/changed-model controls for unrestricted Q-TM. All valid affine promises contain at least one x. A malformed public specification must be parsed/rejected with charged computation in any physical implementation; it is outside the stated promise.

This qualification is **not** a complete arbitrary-SAT decider, and it is separate from TMR-1's physically charged Q-TM and resolution-only Q-RES-H. No historical /341 or /386 checker is invoked.

## 3. Exact obstruction component

Let U = rowspace(H) and V = rowspace(B) in GF(2)^n. Write E_Q = span{e_i:i in Q} for the queried coordinate rows. Define

$$
p_{\rm aff}(C)=\min\{|R|:R\subseteq[n]\setminus Q,\quad
V\subseteq U+E_Q+E_R\}.
$$

This is a **globally shared** minimum hitting/coordinate-completion quantity, not the sum of one-row costs, the number of satisfying assignments, the rank of B alone, or an additive count of duplicated interfaces. Its definition depends only on canonical rowspaces and the set of already observed coordinate **identities**, not their syntactic derivations. All public row operations, equivalent Tseitin/affine constraints already authenticated as public, paid-cache reuse, row ordering, and duplicate output rows are quotiented before pricing. A new addressable source bit changes the qualified input interface and must be reaudited.

**Theorem AFFQUOT055-A (exact necessity/sufficiency).** On every consistent affine promise and every valid observed transcript Q, every deterministic all-promise correct adaptive coordinate-query program that returns **all** outputs Bx+c must read at least p_aff(C) additional distinct source coordinates on that execution. A fixed, nonadaptive set of exactly p_aff(C) additional coordinates suffices, assuming uncharged affine postprocessing in Q-AFF.

**Proof.** All outputs are determined by Hx=h and x_Q precisely when every row of B lies in rowspace(H)+E_Q. For the forward direction, each output row is a linear combination of public equations and observations. Conversely, if some row of B is outside that span, linear algebra gives z in ker H with z_Q=0 and Bz not equal to zero. For any source x consistent with the promise and observations, x and x+z are both valid, give identical answers on every source query in Q, but require different outputs. An adaptive deterministic machine seeing only those queries follows the same control/transcript on the two inputs and cannot be correct on both. Apply this argument to the **actual** query set of every terminating path. The minimum-cardinality sufficient set is exactly p_aff. Reading one minimizing R and solving the resulting linear system then determines all output bits. QED. No assumption that every correct program follows an enumerating or certificate-producing algorithm is made.

**Theorem AFFQUOT055-B (zero closure and tariff).** In Q-AFF, any authentic zero-cost transition that only changes row bases, aliases, cached derivations from public/observed rows, or outputs already uniquely determined has

$$
p_{\rm aff}(C')=p_{\rm aff}(C).
$$

Thus it is invariant on its authentic zero-cost closure, including SCCs. For every paid READ(i), writing Q'=Q union {i},

$$
0\le p_{\rm aff}(C)-p_{\rm aff}(C')\le1.
$$

**Proof.** Free operations preserve U, V, E_Q modulo equality of subspaces. Hence the minimization defining p_aff is unchanged. Adding e_i to the available coordinate span cannot increase the minimum. If R is an optimal completion after reading i, then R union {i}, with a repeated element removed if necessary, completes the earlier state and has size at most |R|+1. Hence the original minimum is at most the later minimum plus one. QED.

One exact tariff coordinate with lambda_aff=1 is therefore valid for **every** legal Q-AFF operation. Completed correct output goals have p_aff=0. The explicit rule-by-component matrix is:

| Actual Q-AFF rule | Charged source-query cost w | Delta p_aff | Verdict |
| --- | ---: | ---: | --- |
| FREE_ROWSPACE / Gaussian equivalent rows / cache alias | 0 | 0 | PASS |
| FREE_FINISH only when every output fixed | 0 | 0 | PASS |
| READ(i) not previously observed | 1 | 0 or 1 | PASS |
| READ(i) repeated | 1 | 0 | PASS |
| BAD_INDEX paid reject/no-op | 1 | 0 | PASS |
| Source-aware read of derived parity | **not an original rule** | can exceed 1 | interface change, NOT a missing row |

For an individual source-coordinate read the inequality is lambda_aff Delta <= w. This is a source-read lower bound; costs for physically executing Gaussian elimination, parsing public equations and all other machine operations are *not* free under Q-TM.

## 4. Fusion, extension, and hard-family ceiling

**Fusion control.** With n=3, no public equations, and outputs x1+x2 and x2+x3 (indices one-based), the individual minima are 2 and 2, but the fused obligation requires exactly the shared coordinates {1,2,3}, so p_aff=3, **not 4**. Adding the public equality x1+x3=0 makes these outputs equal modulo U and reduces the fused minimum to 2. Duplicating the same output 100 times when n=1 still costs only one distinct source read. This is the reduced-product correction required by TMR-3's and TMR-5's earlier subscriber/cache counterexamples.

**Extension-variable control.** If the goal is parity of six hidden bits, the original six-address interface has p_aff=6. Add a new **independently addressable input coordinate** t with public promise t=x1+...+x6 and allow READ(t): p_aff=1. This is a genuine compact one-read shortcut in the extended seven-coordinate interface. It is NOT a free transformation of the original interface, because constructing or distributing t must be charged. Any purported universal per-obligation tariff must list that operation or restrict its interface; deleting the real shortcut is forbidden.

**Exact family and ceiling.** Let PARITY_n be Q-AFF with public H empty, n hidden independently queryable bits and one all-n parity output. For every n, p_aff(initial)=n; querying all n bits and then using free affine completion costs n. More generally, for *every* Q-AFF state, p_aff<=n-|Q| and a complete all-source read finishes every affine output after <=n source reads. Therefore any nonnegative potential on this same Q-AFF transition system satisfying all authentic tariff inequalities and terminal zero is at most n on its initial state, **even if it stacks many overlapping scale coordinates**. An initial superpolynomial bound derived solely from affine-source query obligations is impossible in Q-AFF. Any multiscale proposal must force computational work **after** source acquisition or demonstrate an exact additional charged operation class on a broader system. This is a **linear-ceiling falsifier**, not a SAT complexity lower bound.

**No unconditional transfer.** The source x here is hidden oracle-like data, not the input encoding of 3-CNF whose syntax a standard Q-TM can inspect. XOR-SAT instances are already polynomial-time solvable from their explicit equations. A Q-AFF query lower bound for a hidden assignment is not a lower bound on deciding a 3-CNF formula. Physical Gaussian elimination is charged in Q-TM. Compact circuit/extension/learning shortcuts and arbitrary preprocessing are conservative MAY in the unrestricted machine. The same-system arbitrary-A gate is **OPEN**.

## 5. Explicit cheap controls and prior restricted 2P2N component

The native program independently checks the 4-clause proper 3-CNF encoding of each 3-variable XOR relation against every 3-bit assignment, confirming the compact Tseitin/affine rewriting control. The Horn implication path, Krom/2-SAT path, equality/2-SAT instance, disjoint positive-clause autarkic padding, and width-one path separator DP are tested against exhaustive SAT on those *finite selected cases*. Generic Horn/2-SAT/treewidth/autarky algorithms are established background results, not implemented or transferred by this script. Unused source-coordinate padding leaves p_aff invariant, and source-renaming preserves the exact minimum. General CNF equations that are not proved affine remain OUTSIDE p_aff's promise; neither a zero component nor a positive SAT lower bound is assigned to them.

An independent older restricted geometric component is LSPV-3 GATE284's exact-(2+,2-) false-clause repair lower bound:

$$
\rho_F(a)=|U_F(a)|-\nu(G_a),
\qquad
|\rho_F(a)-\rho_F(a\oplus e_i)|\le1.
$$

Here U_F(a) is the false-clause set and nu(G_a) is maximum matching on the exact-2P2N false-clause adjacency graph. Its admissible local Hamming repair certificate and bounded-radius pruning do **not** imply global UNSAT or a lower bound on solver work; matching discovery and source accesses cost time. Q-Horn contains the usual Horn/2-SAT tractable islands, and treating their counts as independent component prices would double-count cheap work. These are prior restricted results, NOT new AFFQUOT055 claims.

## 6. Execution, provenance, and research ledger

**Actual native CPython:** locally executed `/mnt/data/tmr2_affine_quotient055.py`, deterministic seed 20261114; 1,133 assertions, zero failures. The locally executed source is an independently written prototype; the GitHub-published refactoring `experiments/tmr/tmr2_affine_quotient055.py` has the same declared model/check coverage but was **not re-executed byte-for-byte** in this run. The exact original stdout JSON is published separately. Finite checks: 90 random valid linear-profile selections over n=1..6, 315 charged-read rows (70 discharging one, 245 discharging zero), 180 free equivalence rows, 36 independent kernel separator witnesses, plus fusion/equality/padding/extension controls, full 3-XOR truth tables and syntactic easy-case controls. Exact `Fraction` checks; no stochastic statistical inference or asymptotic claim from tests.

Published code: `experiments/tmr/tmr2_affine_quotient055.py`.
Original native stdout: `results/raw/tmr/2026-11-14_2023_TMR2_AFFQUOT055_RAW.json`.
This report: `research/agents/tmr-2/2026-11-14_2023_TMR2_AFFINE_FUSION_QUERY_QUOTIENT035.md`.
Compact latest handoff: `research/agents/tmr-2/handoff.md`.

**Preflight and original corpus:** Governing 2026-11-14 fusion tariff handoff FIRST, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; November 13 TMR replacement; proof1 (06f7ebc8...), full proof2 Git blob (930c5eedd..., 1,051,196 characters), full canonical main.tex blob (6ac34c5..., 2,545,859 characters); AGENTS, CODEX, research skill, latest issue #3 and all five handoffs. Original evidence inspected: LEAD-0029 Lipschitz semantic-mass counterexamples, TMR-1/035 Q-TM and Q-RES-H qualification, TMR-3/034 genuine joint FILL_POP, TMR-4/035 exact two-bit parity zero-SCC/LP, TMR-5/031 independent physical message-cache replay, LSPV-3 GATE284 exact-2P2N radius and matching caveats, RSR-0004 q-Horn positive solver, LSPV-3/615 /341 SAT-source false acceptance, and matching affine controls from LSPV-4. AFFQUOT055 is **new relative to TMR-4/035** in handling arbitrary public affine promises, multiple fused output rows and adaptive decision trees via a canonical rowspace-completion invariant. It does not claim novelty for Gaussian elimination, parity input-query lower bounds, or Lipschitz telescoping generally.

**Original external references, no imported hardness implication:** [1] T. J. Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978, pp. 216-226, DOI https://doi.org/10.1145/800133.804350 (tractable affine constraint family). [2] P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977, pp. 238-252, DOI https://doi.org/10.1145/512950.512973 (sound abstract-system methodology). All AFFQUOT055 mathematical inequalities are proved directly above; neither paper is claimed to prove this specific new project calibration.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root `proof1.txt`, `proof2.txt`, or `main.tex` edit. Historical /341 remains **FAIL** as a full logical UNSAT authority and /386 remains **RESTRICTED**; neither is repaired. Five existing TMR schedules untouched. **P versus NP OPEN.**

**Peer handoff:** TMR-3 price the authenticated affine-query interface, including source access and dual-use fusion rows; TMR-4 insert p_aff as a candidate coordinate into the exact SCC/tariff LP and independently verify no legal zero step lowers it; TMR-5 attack it with a source-derived compact parity key, reusable extension wire, Gaussian shortcut or actual Q-TM translation. **Next TMR-2 target:** find a syntax-aware SAT-family separator/fusion component *not already exhausted by affine, Horn/Krom, bounded-treewidth, autarky, equality or circuit sharing*, prove an exact local tariff on a qualified transition class, and try to falsify its initial gap by a compact global representation before claiming any growing-family lower bound.

END_OF_REPORT::TMR2::035::2026-11-14_2023_PST
