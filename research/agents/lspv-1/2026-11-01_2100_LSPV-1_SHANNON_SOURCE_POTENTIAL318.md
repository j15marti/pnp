# LSPV-1 SHANNON-SOURCE-POTENTIAL318

**November 1, 2026, 21:00 PST. Formal Proof Lead.** **PROVED/EXACT restricted gate architecture; COMPUTATIONAL independent controls; unrestricted complexity OPEN; external referee pending. P versus NP OPEN.**

## Exact universal obstruction and falsifiers

A short acyclic fan-in-two evaluator C_F(x), with ORIGINAL source variables as its inputs, computes F(x) for a supplied x but does not decide whether any x satisfies F. The size reduction of a source-clause-private evaluator under Shannon restriction is not a lower bound on existential SAT decision work. A globally minimum circuit obtained after learning SAT/UNSAT is not a free acquisition operation.

Four falsifiers: (1) Equal source-private cofactor gate counts imply equal SAT labels: FALSIFIED by F9 below. (2) Signed delta increasing rules out any decreasing source measure: FALSIFIED by the exact occurrence potential below. (3) Decreasing per-path potential implies polynomial aggregate work: INVALID, because two-child expansion can be exponential. (4) A free exact minimum equivalent circuit can be substituted as the state: INVALID; the prior LSPV-1 MINZERO317 threshold is coNP-complete for canonical originals. No unconditional lower bound or P-vs-NP separation is claimed.

## Model, quantifiers, and Theorem 318A

For EVERY valid, unpinned, proper duplicate-free Docker monotone 3-SAT-(2,2) ORIGINAL F with n variables and m=4n/3 original three-literal same-sign clauses, every variable appears exactly twice positive and twice negative. Malformed source strings are rejected. Ordinary residuals are not canonical target-valid children. Every original clause is source-indexed.

Fix any coherent original-variable partial assignment p. For every source clause not yet covered by a pinned true literal, let ell_j(p) be the number of free literals and define the source-occurrence potential

    S_F(p) = sum_(j uncovered) ell_j(p).

An uncovered empty clause is an immediate original-clause UNSAT terminal. For nonconflicting p with u>=1 uncovered nonempty clauses, the STRICT SOURCE-PRIVATE fan-in-two architecture uses exactly ell_j-1 OR gates for each original uncovered source clause and u-1 binary AND gates to combine the independently produced outputs. Literal negation and constants are free in this DECLARED architecture. Thus

    g_private(F|p) = sum_(j uncovered)(ell_j-1) + (u-1) = S_F(p)-1.

This is exact MINIMUM solely within the prescribed no-sharing/source-private clause and AND-tree architecture. Arbitrary gate sharing, factoring, unrestricted minimum Boolean circuits, and paid discovery can be cheaper or more expensive.

For EVERY such unpinned valid F, EVERY original variable x, and BOTH values b in {0,1}: pinning x=b covers exactly two x-satisfied clauses, shortens the other two opposite-sign clauses to two free literals, and leaves the remaining m-4 clauses ternary. Neither child has a directly falsified clause. Therefore

    g_private(F) = 3m-1 = 4n-1,
    g_private(F|x=b) = 2(m-4)+2+(m-3) = 3m-9 = 4n-9.

The exact first-variable eight-gate drop is **independent of the branch label**. This universally quantified statement is a source-private circuit accounting identity, NOT a SAT search-time bound.

## Theorem 318B: exact source-cofactor potential

For EVERY valid F, EVERY coherent p without a previously falsified clause, EVERY unpinned source variable x, and BOTH b in {0,1}, define U_x(p) as the uncovered original clauses incident to x. Then

    S_F(p)-S_F(p,x=b)
      = sum_(j in U_x(p)) [ell_j(p) if x's literal is TRUE under b, else 1].

Proof: nonincident uncovered clauses do not change. Every incident clause either becomes satisfied and loses all ell_j currently free literal occurrences, or loses the now-false x literal and decreases width by one. Sum these disjoint original-clause-ID changes. The equality holds even when a child becomes immediately contradictory. If U_x(p) is nonempty, BOTH branches strictly decrease S; if U_x(p) is empty, x is a semantically irrelevant original-variable don't-care and its two branches have the same decision. Since the free-variable count f also decreases, the integer f+S is well-founded even when the signed delta parameter increases. This bounds depth but does NOT bound the sum of all executed children polynomially.

For the SAME original Boolean function, Shannon expansion gives

    F|p = ((NOT x) AND (F|p,x=0)) OR (x AND (F|p,x=1));
    SAT(F|p) = SAT(F|p,x=0) OR SAT(F|p,x=1);
    UNSAT(F|p) = UNSAT(F|p,x=0) AND UNSAT(F|p,x=1).

Model counts of mutually exclusive x children add. These are KNOWN Boolean identities. No free semantic quotient or minimum-choice oracle is assumed.

## New same-original SAT / UNSAT cofactor collision

Use the canonical F9 original positive triples (156),(238),(135),(469),(247),(789) and negative triples -(468),-(167),-(234),-(358),-(129),-(579), all clause IDs starting at 1. It has 70 global models. Set common original pins

    p = {x2=0, x3=0, x6=1}.

The parent residual has one satisfying completion, source-occurrence potential S=15, covered/unit/binary/ternary histogram (5,1,4,2), and 14 exact source-private gates. Pin the SAME original variable x7 in the two directions:

    SAT child p+{x7=1}: 1 completion; widths (7,2,3,0); S=8; 7 private gates; no empty clause.
    UNSAT child p+{x7=0}: 0 completions; widths (7,2,3,0); S=8; 7 private gates; no empty clause.

The only complete original-model witness is x1...x9=000011110. On the SAT child, the Boolean function on five remaining free inputs {x1,x4,x5,x8,x9} equals (NOT x1) AND (NOT x4) AND x5 AND x8 AND (NOT x9). All five inputs are essential, so a fan-in-two circuit with free unary NOT needs at least four binary gates; four AND gates attain this. Its unrestricted exact minimum is 4. On the UNSAT child the unrestricted minimum is 0. The parent has a six-literal point function and exact unrestricted minimum 5. The **same restricted forward evaluator cost 7** on opposite decision labels falsifies a claimed decision discriminator based on the width histogram, S, or source-private gate count.

A complete 32-leaf original-source UNSAT certificate for the x7=0 child records first falsified ORIGINAL clause IDs 2 (16 leaves), 3 (4), 5 (6), 7 (6). The SAT witness was checked against all 12 original clauses. No gate-input Tseitin auxiliary was called a canonical child.

## Independent reproducibility

Standalone producer and completely independent no-import verifier passed. Independent checker: 127,969 counted assertion groups, including 87,900 precise cofactor mass-change assertions over 12,683 conflict-free source-pin states of F9; 33,344 exhaustive CNF-vs-forward-circuit rows on Y6/F9/F15 with 20/70/1032 models; 60 first-cofactor source profiles; 264 original-clause SS/SU/US/UU compatibility cases; 6,144 complements; six malformed-original rejections. The verifier found 5,026 inactive-variable branch comparisons with zero mass decrease, precisely covered by the theorem's active-variable condition. U198/V198 certified original labels are inherited, not freshly replayed. No native FLMV instruction counting, industrial CDCL, or general solver improvement is asserted.


## Original-source UP-DPLL baseline on the same SAT/UNSAT pair

A separate source-clause-only UP-first DPLL baseline was executed with a complete step-proxy ledger. On the common parent pins it used **one recursive node, 49 source-clause visits, 111 counted literal inspections, six forced unit assignments, and one original witness check**. On the SAT x7=1 child it used **one node, 44 source-clause visits, 96 literal inspections, five units, one checked witness**. On the UNSAT x7=0 child it used **one node, 14 source-clause visits, 37 literal inspections, two units and one checked original-clause contradiction**. No recursive search branches were required on this pair, so the 32-leaf exhaustive UNSAT cover is a **certificate control, not necessary DPLL search work**. This also demonstrates why converting a structural circuit-gate count (seven for either child) into algorithmic time would be invalid. Clause visits, literal inspections, compiled gates and native FLMV machine steps are different units; the measured proxies exclude code runtime, source grammar and compiler acquisition, and do not establish general speedup. An industrial CDCL benchmark was not run.

The independent standalone implementation is [dpll318.py](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_318/dpll318.py) with [raw work ledger](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-01_2100_LSPV1_DPLL318.json). The expanded local reproducibility archive includes its actual Python stdout.


## Fully charged recurrence, quantifier gap, and FLMV

For a uniform adaptive source-authenticated controller D on the declared indexed read-only-input model, all executed work is charged:

    W_D(z) = C_grammar/source/index/head(z) + C_gate/semantic-acquisition(z)
             + sum_(attempted policies) C_selection/switching/failed(z,pi)
             + C_GE/proof/matroid/exact-equality/cache/replay(z)
             + sum_(executed children y) (C_child/output/bit/guest(z,y)+W_D(y)).

S_peak is the maximum simultaneous live physical writable/index/head, ancestors, source maps, circuit tables, proof, cache, staged output, and DELAY/COPY/RECOMP guest state. Explicit materialization of g gates takes Omega(g log(n+g)) output bits, and a conservative direct scan/emit compiler uses polynomial total bit work; neither is mandatory for an arbitrary SAT decider. Logical XOR is offline unless the machine pays to compute it.

The **constructive target remains OPEN**:

    EXISTS uniform D, c, C > 0, FOR ALL binary inputs z:
      D(z) correctly decides the canonical target SAT language and
      W_D(z) <= C(|z|+1)^c.

The **unrestricted separation target remains OPEN**:

    FOR ALL correct uniform D, ALL c, ALL C>0, ALL N0,
      EXISTS valid canonical F with |F|>=N0 and W_D(F)>C(|F|+1)^c.

The alternative ARC route additionally requires a genuinely power-short fully charged arbitrary A->Phi(A) for unknown K,L AND a separate numerical strict SAME-MACHINE FLMV transport. Neither is proved. The source potential is at most 3m initially, but a full Shannon tree can have 2^n paths. Deciding the same source after a free minimum circuit would reverse the unpaid-acquisition quantifiers.

## Corpus and literature / novelty firewall

Read first the verified 2026-11-01 19:50 five-role SAT/Circuit-SAT handoff and earlier decision-only handoff. Surveyed AGENTS.md, CODEX.md, pnp-research skill, LSPV-1 MINZERO317, LSPV-2 GROUP323, LSPV-3 GATE319, LSPV-4 F9-OBDD321, LSPV-5 matching-factor REFEREE280, earlier circuit-Tseitin TRACE46 and parsimonious TRACE47, and issue #3. External primary references: Bryant, Graph-Based Algorithms for Boolean Function Manipulation, IEEE Trans. Computers (1986), doi:10.1109/TC.1986.1676819; Docker, Monotone 3-SAT-(2,2) is NP-complete (2019), arxiv:1912.08032; Fortnow et al., Time-Space Lower Bounds for Satisfiability, JACM (2005), doi:10.1145/1101821.1101822. Project GitHub search for cofactor/potential and separately github.com/openai code searches for Shannon-cofactor/OBDD and Circuit-SAT/Tseitin found no duplicate source; absence is not a novelty claim. This is elementary gate accounting and an independently verified new finite F9 collision, not a new hardness method.

**Next target:** find or refute a fully charged *aggregate* Shannon-child amortization inequality that is sound under arbitrary adaptive gate factoring, cofactor semantic merging, paid policy acquisition, failed alternatives, and SAT/UNSAT asymmetry. All preexisting five tasks/status/schedules unchanged. P versus NP OPEN.

END_OF_VERIFIED_REPORT::LSPV-1::SHANNON-SOURCE-POTENTIAL318::P_VS_NP_OPEN
