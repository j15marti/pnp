# SATURATED-CYCLE-AFFINE-TERMINAL1

**November 1, 2026, 01:44 PST. Independent synthesis / role handoff.**

**Status:** PROVED/EXACT restricted original-source theorem (external referee pending), COMPUTATIONAL independent exhaustive checks, CONDITIONAL overall SAT/WRAPPER and ARC/FLMV composition, **P versus NP OPEN**. No changes to preexisting tasks, enabled states, or schedules are required by this research result.

## Canonical language and model

The sole NP-complete target is every valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) source: exactly three distinct all-positive or all-negative literals per original clause, exactly two occurrences of each polarity per variable, and no duplicate clauses. Reject malformed encodings. A partial assignment p is a coherent assignment to **original variable names**, not independently assignable occurrence bits. Let U(p) be original clauses with no literal made true by p, f the number of free variables, and u=|U(p)|. If any original clause is completely falsified by p, UNSAT is immediate and needs no affine theorem.

Let s_x^+ and s_x^- count positive and negative occurrences of a free x in original clauses already satisfied by p. Put eta=sum_x min(s_x^+,s_x^-), e=2f-u, and b_x=0 for s_x^+>s_x^- and b_x=1 for s_x^->s_x^+. Select ANY authenticated original-clause-edge-disjoint family of odd cycles among uncovered binary clauses. Let their lengths be l_1,...,l_nu, and define delta=e-eta-nu.

## New exact theorem: disjoint union of affine solution spaces

**Theorem.** For every valid source F and coherent p with no original empty clause, for every authenticated edge-disjoint odd binary-clause cycle family C, if delta=0, the satisfying original-source extensions of p are **exactly a disjoint union of affine solution spaces** indexed by choosing one edge in each cycle.

For each choice (j_1,...,j_nu), construct a GF(2) system on the original unassigned variables as follows:

1. Fix x=b_x whenever s_x^+ != s_x^-.
2. For each uncovered clause **outside** the chosen cycles, impose that its residual literal-truth parity is odd: for a positive clause with free-literal support V, XOR_(x in V) x = 1; for a negative clause, XOR_(x in V) x = 1 XOR (|V| mod 2). This covers residual widths 1, 2, 3. Pinned literals in uncovered clauses are already false.
3. For each chosen cycle, its selected edge must have **both** literals true, so its two variable values are fixed to 1 for a positive edge or 0 for a negative edge. Every other edge in that cycle has exactly one true literal and therefore obeys x XOR y = 1.

If every system is inconsistent, return **UNSAT with row-XOR refutations**. If any system is consistent, Gaussian elimination produces a **checked SAT witness**. Furthermore, if the branch indexed by j has GF(2) rank r_j, the total exact number of satisfying extensions is

    #SAT(F extending p) = sum_{consistent j} 2^(f-r_j).

The distinct branches do not double count models.

**Proof.** Signed-occurrence conservation gives, for every satisfying extension a,

    e = sum_{j in U(p)}(t_j(a)-1) + eta + sum_x |s_x^+-s_x^-| [a_x != b_x].

Every SAT uncovered clause has t_j>=1. On each odd binary cycle all clauses are SAT; if no edge had both literals true, each edge would have opposite Boolean endpoints, an impossible proper 2-coloring of an odd cycle. Each selected cycle therefore consumes at least one unit of the first nonnegative sum. Edge-disjoint source-clause IDs prevent double counting. At delta=0, **all slack is exhausted**: every preferred value holds, every original clause outside the chosen cycles has exactly one true literal, and each cycle has exactly one doubly true edge, all its other edges having exactly one true literal. Hence every SAT extension belongs to one of the specified affine systems, with a **unique** selection vector.

Conversely, every assignment in one specified affine system satisfies each original source clause. Clauses already covered by p remain satisfied; outside-cycle clauses have odd literal-truth parity and therefore at least one true literal; on-cycle selected edges have two true literals and other edges exactly one. Thus every such assignment is SAT. The branch solution sets are disjoint, and a consistent affine system of f free variables and rank r has 2^(f-r) solutions. QED.

**Complexity and full charging:** Given an authenticated cycle family with lengths l_i, the decision and exact-count algorithm performs at most prod_i l_i Gaussian eliminations and their verification, each polynomial in the original explicit input length N. A concrete polynomial-acquisition policy greedily selects edge-disjoint **triangles** from the original residual binary-clause graph, so it runs in O(poly(N)+3^nu poly(N)) time. If nu=0 and delta=0, it becomes an exact **polynomial-time terminal**, requiring one GF(2) solve. The implemented triangle scanner is a conservative O(m^3) Python candidate enumeration, not near-linear. Peak Gaussian-matrix and graph workspace are polynomial (and may be near-linear or larger), **not proved at the FLMV N^(1/2) target**. On general inputs delta can be positive and nu can be large. Polynomial recognition on a subset is not universal polynomial SAT.

## Four falsifiers and concrete counterexample

F1. **Parity outside selected cycles alone certifies SAT. FALSIFIED.** A new 9-variable, 12-clause valid canonical source has positive clauses (1,5,6), (2,3,8), (1,3,5), (4,6,9), (2,4,7), (7,8,9), and negative clauses formed by negating (4,6,8), (1,6,7), (2,3,4), (3,5,8), (1,2,9), (5,7,9). It has 70 complete SAT models in total. Pin original variables {x8=0,x3=0,x7=0,x6=0,x1=1,x5=1}, leaving x2,x4,x9 free. This cube has **zero** SAT completions, despite no original empty clause and delta=0 with (e,eta,nu)=(1,0,1). Its certified cycle uses zero-based source clause IDs (3,4,10). The *outside-cycle* affine constraints are consistent and force x2=x4=x9=1, but then positive cycle clauses 3,4 each have two true literals while negative clause 10 has zero. All three possible overfull-edge choices yield contradictory GF(2) systems. Independent original-source enumeration of all eight completions and 264 original pair-extreme masks confirms the refutation. Thus cycle choices cannot be omitted.

F2. **Two different selected-edge vectors may describe the same SAT extension. FALSIFIED at delta=0 by exact conservation; independently checked finite controls had zero overlaps.**

F3. **The saturated terminal is sufficient for all inputs. FALSIFIED by unresolved positive-budget cubes.** On two checked source families, 235 of 729 Y6 coherent partial assignments and 51 of 1,458 specified F15 coherent cubes remain unresolved, requiring a correct exact fallback. This is a partial-state policy, not an all-input polynomial decider.

F4. **The numerical FLMV bound follows from the new SAT deduction or from logical XOR. INVALID.** Neither virtual residuals nor affine work are target-canonical hereditary power-short children; the Python matrix and selected-work traces do not give the requisite same-machine simultaneous time/space exponents. DELAY/COPY/RECOMP, lazy state, and strict SAT-to-target local-bit reduction are still mandatory controls.

## Reproducibility and actual work

A producer with polynomial-time **greedy** authenticated triangle acquisition and separate independent no-import verifier enumerated all 729 Y6 coherent cubes and all 1,458 coherent partial states over the free six-variable windows of F15. Complete independent assignment-by-assignment checks verified the **disjoint union equality** on all 504 delta=0 states, counting 402 Y6 SAT extensions and 80 F15 SAT extensions across the checked cubes. Producer-side independent GF(2)-rank count sums match the same totals, with 302 Y6 and 276 F15 affine systems assessed. The F15 saturated 210 states consist of 66 SAT and 144 UNSAT. Six malformed grammars were rejected.

A separate 9-variable independent verifier checked the false-positive parity shortcut, all three overfull-edge selections, all eight original-source cube completions, the 70 global SAT models, 264 four-way S/U pair-extreme claims, and the 0^9/1^9 clause-status histograms. The new terminal correctly returns UNSAT; parity alone incorrectly suggests SAT.

### Selected-work proxy comparison (not native FLMV)

| Same source / cube | Label | Baseline UP-DPLL nodes / selected work | Earlier adaptive nodes / work | Saturated-cycle adaptive nodes / work |
|---|---|---|---|---|
| Y6 root | SAT | 4 / 291 | 4 / 366 | 4 / 363 |
| F15 root | SAT | 7 / 1386 | 7 / 1777 | 7 / 1771 |
| F15 p_U | UNSAT | 3 / 662 | 1 / 298 | 1 / 270 |
| F15 p_S | SAT | 4 / 783 | 2 / 553 | 1 / 432 |
| F15 p_U with x6=0 | UNSAT | 3 / 602 | 1 / 365 | 1 / 328 |

Selected work counts tracked original clause/literal checks, odd-cycle candidate/selection work, GF(2) rows/operations and branching. They exclude some Python bookkeeping and are not native indexed-TM machine steps. Gate costs can **worsen** easy cases; there is no uniform speedup claim.

## Joint WRAPPER/DAG/ARC integration

Represent the original signed hypergraph read-only. A typed computation DAG node stores a coherent partial source assignment, clause true/unassigned counts (materialized Gray XOR only as OFFLINE diagnostic), authenticated weighted signed-spill and cycle-cut certificates, optional affine row-XOR proof DAG, and a fully charged source/index/child/guest/selector/cache/peak-space ledger. The adaptive order is: authenticate target, UP/source structure, δ<0 UNSAT, δ=0 exact saturated-cycle affine terminal (bounded paid budget), Horn/2SAT/XOR and certified bounded-interface DP, exact AND/OR splitting and memo, then correct fallback. SAT only with full original-clause witness; UNSAT only with complete proof or exhaustive branching. Rejected/overbudget policies return UNRESOLVED, never UNSAT.

The conceptual main opportunity is no longer to make logical XOR decrease; prior tests show it can be identical across opposite SAT/UNSAT labels and δ itself can increase along a SAT-preserving path. Instead, use a **certificate-derived parameter vector** (delta, authenticated cycle count and total length, affine rank/nullity, component interface, proof/reuse costs) to select exact terminal actions. Source reads and certificate acquisition remain charged. The saturation theorem itself yields no hereditary canonical reduction, no arbitrary-A -> Phi(A) contraction, and no quantitative transport of the actual FLMV forbidden region to the target. **P versus NP remains OPEN**.

## Source and prior-work audit

- Repo `j15marti/pnp`: integrated hypergraph-wrapper ARC1, REFEREE260, LSPV-1 weighted-spill296 and cut-defect297, LSPV-2 SATURATED-AFFINE-CLOSURE292; prior CYCLE-AFFINE-SWITCH123 handled a different supplied block-interface language. The new contribution is the **exact disjoint affine-cycle union and rank counting** from the earlier saturated necessary conditions. Independent external mathematical review pending.
- Peer literature: Döcker (2019), https://arxiv.org/abs/1912.08032; Fortnow et al. (2005), https://doi.org/10.1145/1101821.1101822; Arvind and Guruswami (IPEC 2021), https://doi.org/10.4230/LIPIcs.IPEC.2021.5; Mählmann et al. (MFCS 2021), https://doi.org/10.4230/LIPIcs.MFCS.2021.73; Soos et al. / CryptoMiniSat (CNF-XOR engineering), https://github.com/msoos/cryptominisat. These establish relevant method families, not novelty or a universal contractor.
- GitHub searched `j15marti/pnp` for saturated affine, odd-cycle edge, cycle-affine, ARC cut-defect and independent roles. Separately searched `github.com/openai/math` for mathematical SAT formalization/algorithms and `github.com/msoos/cryptominisat` for XOR+CDCL methods. No novelty inference from search absence.

## One unified next target

Use this genuinely complete saturated terminal **inside** the typed Double WRAPPER, then prove or refute whether a polytime source-authenticated selector can (i) reach such terminals or (ii) emit power-short canonical M22 descendants for **every** connected valid instance. Develop a lower-cost triangle/MaxCut certificate finder and a low-space GF(2) trace, while separately seeking a local-bit near-linear SAT-to-canonical-target reduction needed to transport the FLMV numerical bound. Maintain all five existing research roles and schedules, and keep P versus NP OPEN.

`END_OF_VERIFIED_REVIEW::SATURATED_CYCLE_AFFINE_TERMINAL1::P_VS_NP_OPEN`