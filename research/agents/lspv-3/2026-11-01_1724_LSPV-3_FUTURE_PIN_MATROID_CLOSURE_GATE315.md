# LSPV-3 GATE315: Future-Pin-Closed Affine Matroid Certificate

**2026-11-01 17:24 PST. PROVED/EXACT restricted theorem; COMPUTATIONAL independent no-producer-import verification (8,512 assertions); external mathematical referee pending. P versus NP OPEN.**

## Exact obstruction and quantifiers

A static saturated-cycle affine matroid certificate need not remain decomposable when a later source-variable pin is added. A later variable's affine form can couple previously independent factor components. SAT-label equality, syntactic pin-key counts and first-order marginals are not sufficient continuation equivalences. The decision-only controller must pay for discovery of source-authenticated semantic representatives; it cannot use a free label oracle.

The sole original language is all valid duplicate-free proper Döcker monotone 3-SAT-(2,2), malformed encodings rejected. All original clause IDs and signed occurrences remain authenticated. Ordinary pinned residuals need not satisfy the target grammar.

## Restricted theorem, with complete proof

For any valid target original F and any coherent pinned cube p, acquire a polynomial greedy *source-clause-edge-disjoint* triangle packing in the uncovered binary clauses and compute f, u, signed spill eta, nu and delta = 2f-u-eta-nu. Assume delta=0, with no original empty clause. Use the previously verified saturated-cycle theorem: the extensions of F|p are exactly the assignments satisfying the exterior GF(2) equations E (preferred signed-spill units and odd parity on every uncovered noncycle source clause), together with all original selected-cycle clauses.

If E is inconsistent, its row-XOR contradiction is a complete UNSAT certificate. Otherwise choose a particular solution and nullspace basis x=x0+Bz, z in GF(2)^d, d=f-rank(E). Declare **before compilation** an allowed future-pin vocabulary S of free original-variable names. Collect the GF(2) coefficient forms of (a) each literal of each selected original cycle clause, and (b) every source-variable value x_s, s in S, expressed in z coordinates. Let h be the rank of their span. Acquire a checked basis of h forms. Compute the binary representable vector matroid's direct-sum components, merging forms in the same original selected-cycle clause. Let the resulting component dimensions be h_1,...,h_c; their sum is h. Include constant literals, sign bits and original clause IDs.

For every coherent future pin cube q with domain contained in S, let M_i(q) be the number of assignments to the h_i independent form evaluations satisfying all selected original cycle clauses and future-pin equations belonging to component i. Then the **exact model-count identity** is

\[
\boxed{\#\mathrm{SAT}(F\mid p\cup q)=2^{d-h}\prod_{i=1}^c M_i(q).}
\]

A conflicting prior pin yields zero. A future pin not in S returns UNRESOLVED_OUTSIDE_VOCAB, not a guessed label. A zero component table plus checked affine and source-clause provenance is a complete replayable UNSAT certificate. A positive table product gives SAT; if an explicit witness is requested, solve the independent-form basis rows, lift x=x0+Bz and check every original source clause. A decision-only caller need not output/recover that witness.

**Proof.** The authenticated delta-zero theorem gives the exact E-plus-cycle-clause characterization. The map z -> the h independent form evaluations is surjective onto GF(2)^h, with exactly 2^(d-h) lifts per evaluation by rank-nullity. Fundamental circuits give direct-sum vector-matroid components. Source-clause co-occurrence unions make every nonlinear cycle predicate component-local, and inclusion of *all* declared future-pin forms makes every q constraint component-local. The satisfying evaluation set is therefore the Cartesian product of the independently tabulated component sets. Multiplication and the uniform lift count prove the formula, with zero-table proof and checked witness correctness. QED.

The method is **closed under every subsequent original-variable pin** if S includes all initially free source variables. In that case h=d and the multiplicity factor is one. With a limited S the factor 2^(d-h) can be nontrivial.

## Quantitative charged total work

With m source clauses, greedy triangle discovery checks at most O(m^3) candidate triples, followed by paid source/cycle provenance and bit-access checks. Gaussian elimination, the nullspace basis and matroid circuit discovery are polynomial bit-time algorithms on explicit inputs, not free oracles. Put K=sum_i 2^(h_i). Explicit component compilation, including proof tables and pin forms, costs poly(N)(1+K), with poly(N)+O(K) live data before ancestor/guest retention. For r later pin-update queries, exhaustive charged table filtering takes at most

\[
W_{\rm compile+updates}(N,r)\leq\mathrm{poly}(N)[1+(r+1)K].
\]

For a coherent monotone ADD path, at most |S| effective pins are added, so the explicit potential |S|-|dom(q)| strictly decreases. This bounds **one actual path**, not aggregate recursive branching. Freshly recomputed signed delta may increase; the already compiled E and component tables remain valid because q only adds constraints.

The full controller still pays grammar/source/index/head scans; unsuccessful acquisitions and policy switching; GE, matroid and proof work; cache/replay; child/output/source bit access; DELAY/COPY/RECOMP guests; and all actually visited AND/OR successors. Simultaneously live ancestor, index, source, matrix, cache, proof, guest and output space is counted at its peak. Exact DPLL fallback can be exponential on arbitrary originals; no uniform all-input bound max h_i=O(log N) has been established. Python operation proxies are **not** FLMV native indexed-machine time, physical XOR or peak space measurements.

## Exact hostile families and falsifiers

F1 (FALSE): static affine components automatically support future pins. An original variable may have coefficient form e1+e2, coupling distinct original components e1 and e2. Future-pin closure explicitly includes the form before factoring. This illustrative two-coordinate affine example is not asserted to be a canonical M22 gadget.

F2 (FALSE): nu=t source-certified triangles force 3^t work. Form a connected canonical source from t copies of Y6, swapping one original negative occurrence between already covered clauses of adjacent copies. With pins x2=0,x3=1,x5=0 in each block, each residual has x4=1 and the exact surviving predicate NOT(x1 AND x6). Every connected source remains valid, with n=6t,m=8t, delta=0, nu=t, d=h=2t, component dimensions [2] repeated t times and exactly 3^t source models. The nominal 3^t edge-choice tickets are replaced by 4t component table rows, after charged polynomial discovery. At t=16: **43,046,721 nominal tickets versus 64 materialized component rows**.

F3 (FALSE): the terminal must be reacquired whenever delta rises. A subsequent original pin x1=0 changes the signed gate's delta 0 -> 1 on this family, but the source-closed table still reports exactly 2·3^(t-1) models. Pin x1=1 leaves 3^(t-1) models; pin x1=x6=1 yields UNSAT, with original negative clause (-x1 OR -x3 OR -x6) false. This is a same-original SAT/UNSAT control.

F4 (OPEN): logarithmic maximum pin-closed component dimension can always be acquired on every target original at polynomial total cost. Neither current proof nor finite evidence shows this.

A rank-multiplicity control on the same Y6 original uses p'={x3=0,x4=1}, delta=0, nu=0, d=2, S=empty, h=0 and 4=2^(d-h) satisfying extensions. A later undeclared pin returns UNRESOLVED. F9 root has 70 models; the established source-identical F9 six-pin UNSAT cube has zero despite outside parity consistency; a different F9 pinned SAT cube has two. F15 pinned SAT/UNSAT controls have 2/0 models; six malformed input variants are rejected.

## Independent source verification and provenance

Full no-import verifier passed **8,512 assertions**, including all 729 coherent future-pin patterns on connected Y6 t=2, 128 seeded t=3 updates, source-grammar/connectivity checks through t=16, F9/Y6/F15 full root model counts 70/20/1032, all 264 signed F9 clause-pair SS/SU/US/UU modes, 36 per-occurrence local target and inverse records, 512 F9 assignment/complement trails and an original source resolution-proven forbidden cube. Offline complete aligned logical-state XOR sums are 4,977 binary and 3,585 Gray, not physical tape events. UP-first DPLL was independently compared on same-original SAT and UNSAT controls; no native machine speedup is claimed. U198/V198 are inherited controls and were not freshly replayed here.

The full archive available in the associated research run contains the standalone producer, **independent verifier**, full source-extremes/flip diagnostics, raw JSON, complete 17k-character report and SHA-256 integrity manifest. Compact runnable and verifier files linked below reproduce the central connected-source results; they do not replace the full proof-bearing archive.

## Prior work and literature audit

Read first the five-role decision-only directive, integrated 01:48 handoff and 01:44 saturated-cycle theorem; then AGENTS.md, CODEX.md, pnp-research skill, issue #3, prior LSPV-3 GATE300 (affine quotient), GATE301 (static matroid components), GATE312-314 (continuation collisions), LSPV-1 PAID-LOGWIDTH-SOURCE-HEREDITY313, and LSPV-2 PAID-SEMANTIC-CUTOFF317. This result is an **extension to future-pin closure**, not a new GF(2), matroid, bucket-elimination or general #SAT algorithm.

Primary web queries: Döcker Monotone 3-SAT-(2,2) (https://arxiv.org/abs/1912.08032); Fortnow-Lipton-van Melkebeek-Viglas SAT time-space bounds (https://doi.org/10.1145/1101821.1101822); Dechter bucket elimination (https://doi.org/10.1016/S0004-3702(99)00059-4); Samer/Szeider #SAT treewidth (https://doi.org/10.1016/j.jda.2009.06.002). GitHub searches separately examined project j15marti/pnp for "SATURATED CYCLE treewidth", "saturated affine variable elimination", "triangle packing bucket elimination", "semantic cutoff rank-nullity", and github.com/openai for "Boolean satisfiability" and "bucket elimination". openai/math contains generic formalized SAT/Boolean material, not an M22 all-input certified compiler. Failed/empty searches establish no novelty.

**OPEN:** no polynomial aggregate-work controller on every valid original, no arbitrary-A hereditary power-short ARC mapping, and no strict numerical same-machine FLMV transfer. Both P=NP and P!=NP remain OPEN. Existing five task identities, enablement, Pacific hourly staggering and ownership are unchanged.