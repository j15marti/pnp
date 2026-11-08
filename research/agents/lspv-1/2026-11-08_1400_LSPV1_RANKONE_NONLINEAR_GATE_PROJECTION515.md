# LSPV-1/515: exact rank-one nonlinear-gate affine closure and source-only proof projection

**November 8, 2026, 14:00 PST | Route B lead | PROVED/RESTRICTED semantic criterion and local facet macros; COMPUTATIONAL finite replay; CONDITIONAL full syntactic compilation | P versus NP OPEN.**

**Material node:** [P2-L1-515]. Refines [P2-L1-513] (source-only affine DEF/local3 compiler), [P2-L1-505] (affine isotropy/guard controls), [P2-L1-506] (observable cancellations), [P2-L2-371] (nonlinear-gate branching) and the transfer gap [P2-C3]. **Unchanged OPEN:** [P2-D1] original historical accepted-byte grammar, [P2-C3] complete all-rule normalization, [P2-B1] superpolynomial minimum across full fixed mixed calculus, [P2-B2] noncircular same-calculus B3, Route A [P1-01]/[P1-03]/[P1-04]/[P2-A2]/[P2-A5]. No historical rule, weight, role, schedule, title or enabled-state change.

## IDEA, prediction and four predeclared falsifiers

**Hypothesis.** The prior [P2-L1-513] source-only syntactic Res(PC1/F2) compiler excluded all truth-table-nonlinear charged Boolean DEF gates. Yet some syntactically nonlinear two-input gates remain **affine in the original source variables** because their two previously expanded affine input functions are dependent. These gates should require only constant-size projected Boolean-tautology macros, not an exponential split on their entire original-variable dependency cone. This applies only when **each named gate output** stays affine after full recursive expansion.

Precise falsifiers: (F1) an XOR/AND/OR two-input truth table with quadratic coefficient 1 and linearly independent input masks nevertheless yields an affine original-variable output; (F2) a nonaffine table with dependent input masks produces degree-two original output; (F3) an emitted projected gate facet fails to reduce to a true constant or complementary pair in a single affine form; (F4) the predecessor /513 source-only syntactic rules cannot supply the needed Boolean excluded-middle or weakening macro without new free axioms.

## SEARCH: original sources, peer checks, primary results and deduplication

Read both complete live trackers initially: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, `proof2.txt` blob `cc44d51199d43ab6acd51df0b15fb58d184aea7e`; current issue #3 and its 1,381 comments; historical five-role refocus at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, file blob `033b54b87b7cbe94912af5cf67daa52859143a07`; AGENTS.md blob `19656af1`, CODEX.md blob `754999f5`, and the pnp-research skill blob `b8df83a7`. Recovered original R_mix341 declaration at `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`; checked LOCAL-CONVERT historical addendum `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` blob `bbcdad9a`.

Read exact LSPV-1/513 blob `52e0b679`, /512 blob `6a36cfbe`, /514 blob `3d8d60a3`, predecessor LSPV-2/371 and /397, LSPV-3/488, current LSPV-3/510 (2026-11-08 13:24 PST), and independent LSPV-5/444 (2026-11-08 13:53 PST). Existing [P2-L1-505] already treats common isotropic guards, [P2-L1-506] treats output-only cancellation, and [P2-L2-371] treats four-way cofactor branching; the **only additional statement here** is the exact per-gate original-affinity criterion together with the concrete constant-overhead local facet port into the predecessor /513 compiler. Do not claim this elementary Boolean algebra is a novel academic theorem.

Actual current independent sources: `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70` (stale relative to /514), and Claude `research/agents/claude/world-ledger/README.md` blob `de75a371` (world classification, not a mixed-system checker).

Required external repository reads: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3` and `proofs/complexity/README.md` blob `7ee9a11e` (finite-machine P subset NP only); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea` (explicitly restricted methods); `meelgroup/frat-xor/format.md` blob `986a21aa` (different XOR certificate grammar); `tanyongkiam/cake_lpr/README.md` blob `e94f45e9`; `peitl/short-proof/README.md` blob `93d2090d`; `openai/math/README.md` blob `cc5b0a03` and `lean/README.md` blob `f1ab6183`; `anthropics/formal-math/README.md` blob `1df53bfc`. Neither code badges nor external checker versions authenticate historical R_mix341 or B3.

Project code-search queries included "rank one affine input nonlinear gate normalizer", "dependent affine inputs arbitrary truth table gate source projection", "nonlinear gate affine closure rank-one", "affine input dependency rank 1 ResPC gate", and "degenerate gate affine input rank source proof". Search revealed the above older related fragments, not an identical independent accepted-byte projection theorem. Indexed web searches examined Pang's October 24, 2026 arXiv:2610.00837v2 degree-size result, Urquhart (1987), Ben-Sasson–Wigderson (2001), Carenini's August 2026 ECCC random 3-CNF Res(k) result, and general GF(2) Boolean quadratic rank facts. Direct Google-branded execution was not used; general indexed web search was available.

## ITERATE: fixed distinct extension, exact algebraic theorem

Fix a **new, separate, source-explicit, sound and complete** system `R_affine-closed-DEF515`, for all encoded CNF sources before instances are chosen. It consists of the original-only three-variable semantic AND3/LOCAL, unrestricted ordinary RES on authenticated source and paid auxiliary clauses, globally shared GF(2) affine sums, and paid conservative, fresh, acyclic two-input Boolean truth-table DEF owners. It follows the scoped syntax of [P2-L1-513], except the DEF gate may have any four-bit truth table *provided its output remains affine after full original-input substitution*. The latter condition is decidable from two previously computed n-bit affine masks, so it is a uniform effective rule, not a semantic oracle. Each DEF costs its fixed one paid node and supplies only its authenticated four positional defining facets; any other inference costs its declared historical-fragment weight. Shared owners and derived nodes are counted once. Complete by ordinary RES. This is **not** an assertion that the historical /341 accepted-byte language includes precisely these gates or these ports; case splitting/assumption discharge, unrestricted nonlinear DEF and unchecked circuit-valued LOCAL are excluded.

Represent predecessor affine wires by `u(x)=u0 + U·x`, `v(x)=v0 + V·x` in F2; each binary truth table has the unique algebraic normal form

$$
g(u,v)=a_0+a_1u+a_2v+a_{12}uv.
$$

**Theorem 515.1 (PROVED/RESTRICTED, exact necessary and sufficient condition).** For arbitrary n and affine inputs u,v, the expanded output g(u(x),v(x)) is affine in the original x **if and only if**

$$
\boxed{a_{12}=0\quad\text{or}\quad \operatorname{rank}_{\mathbb F_2}(U,V)\le 1.}
$$

For `a12=1`, this permits a syntactically nonlinear gate even when its transitive original-variable cone has size n, so long as the two input linear masks are dependent.

**Proof.** On the Boolean cube x_i^2=x_i. For every i<j the degree-two coefficient of the expanded g is exactly `a12(U_i V_j+U_j V_i)`. All such coefficients vanish precisely when `a12=0` or every two-by-two minor of the two-row matrix [U;V] vanishes. The latter is exactly rank at most one over F2. There are no monomials of degree above two; therefore the output is affine exactly in these cases. The test uses O(n) bit operations on each pair of stored coefficient masks under an appropriate bit-vector machine representation. QED.

The cases are *maximal for the stated all-named-wires-affine requirement*: a nonlinear gate with independent affine inputs creates a genuine degree-two output and cannot be accepted while maintaining that invariant. This criterion is not claimed for final *observable-only* outputs where later nonlinear gates cancel, as in [P2-L1-506].

**Lemma 515.2 (PROVED/RESTRICTED, exact local facet port).** Suppose g is truth-table-nonlinear (a12=1) and rank(U,V)<=1. Define the expanded affine output H(x)=g(u(x),v(x)). Each of the four paid DEF-owner facets

$$
L_{ab}=(u\ne a)\vee(v\ne b)\vee(H=g(a,b)),\qquad (a,b)\in\{0,1\}^2,
$$

is syntactically obtainable with constant target steps from already justified Boolean excluded-middle lines and the target true axiom, without source substitution or a free equivalence oracle.

**Proof.** All nonconstant u,v,H now have the *same* nonzero original linear mask T, up to complemented constants, and the constant case is immediate. After substitution, every disjunct of L_ab is either a constant, T=0 or T=1. Semantic conservativity makes L_ab true at both T values. Consequently either one disjunct is true identically, or the disjunction contains both complementary equations. In the first case use the syntactic true axiom and paid weakening; in the second use the already derived Boolean excluded-middle `(T=0)∨(T+1=0)` and paid weakening. The previously derived T excluded-middle is maintained per paid affine predecessor gate by [P2-L1-513]'s source-preserving constant-size gate macro. Thus each positional facet costs O(1) target nodes, regardless of support |T|. Every duplicated facet source is traceable to the charged owner, never an original-source axiom. QED.

For gates with a12=0 (ordinary affine binary tables), the bounded four-case synthetic tautology derivation from excluded-middle lines of u and v is already available from [P2-L1-513]'s source-only compiler. The new rank-one nonlinear facets require only the simpler one-form construction above.

**Corollary 515.3 (CONDITIONAL composition, not new full-calculus theorem).** Provided [P2-L1-513]'s syntactic RES/XOR/three-original-local compilation is valid as specified in the *exact* target Res(PC1/F2) grammar, replacing its affine DEF macro by the above two-case gate macro yields, for every source-authenticated shared-DAG refutation pi in R_affine-closed-DEF515,

$$
\boxed{S_{\operatorname{Res}(\operatorname{PC}_1/\mathbb F_2)}(F)
\le C(m+g+q+1).}
$$

Here m is the exact number of original source clauses, g the number of distinct charged definitions, q the number of distinct paid inference nodes, and C an absolute constant independent of source n or transitive gate cone support. The proof follows the full DAG topologically, substitutes every wire by its justified original affine form, derives each paid projected gate facet as above, and then uses the predecessor's original-source syntactic macros for RES, global GF(2), AND3 and LOCAL on at most three **fully expanded original variables**. No branch/discharge, uncharged source inference or arbitrary nonlinear gate is included. The semantically exact new gate-facet port is proved here; a fresh end-to-end replay through a primary ResPC1 checker was **not** executed.

With Pang's separately stated October 24, 2026 **preprint** theorem for original random proper signed 3-CNF with n variables and 8n clauses, the conditional composition would imply exponential node lower bounds in R_affine-closed-DEF515 along suitable sources, with N=Theta(n log n) original indexed binary bits. It still would **not** prove [P2-B1] or [P2-B2] for the historical full R_mix341.

## Independent verification and hostile controls

Independent Python `/mnt/data/lspv1_515_rank_one_gate.py` (SHA-256 `c0bb8374982c5b7971bde9424d3236e916155e7d47ec3e6d45f34736a610fe98`) exhaustively checked **87,296** affine-input pairs and 4-bit truth-table combinations over n=1,...,5, including **5,632** rank-one nonlinear cases and **38,016** independent-mask nonlinear cases. All **137,337** assertions passed. It also tested 175 randomized deep shared/reconvergent circuits of up to 32 gate attempts and 12-original-variable-support negative/positive controls; invalid tags and corrupted outputs rejected. Fixed random seed 51520261108. Host Python 3.13.5 peak ru_maxrss approximately 95,888 KiB, wall about 3–4 seconds in separate runs (not a machine-model complexity claim).

An independently written JavaScript (`experiments/arc/lspv1_515_rank_one_gate.cjs`) checked all **5,632** rank-one nonlinear cases and all **22,528** projected positional facets over n<=5. Every facet was certified as either containing a constant-true disjunct (14,320) or a pair of complementary one-form literals (8,208). Five malformed tag controls rejected. It is a finite exact semantic/facet checker, **not** the historical checker and **not** an execution of Pang's original proof system.

Host-level logic work: all candidate gates are checked by n-bit masks and a fixed 4-entry truth table, with O(gn) worst-case bit work using straightforward per-bit arrays. For a source of bit length N and a supplied mixed certificate of B bits, full simulated output/verification/search-free construction is bounded by a polynomial in N+B+n+g+q; individual projected affine equations may contain Θ(n) bits despite constant logical-node charge. Failed search, proof discovery, caches, serialization, exact source reads, external GitHub readback, rebuilding all printed lines, and simultaneous output/input/scratch memory are **not** part of W_R and require separate fully charged machine ledgers. No same-machine FLMV claim is made. Distinct-node work, weighted critical path and physical time/space are not interchanged.

## Family / theorem / encoding / shortcut / remaining-transfer ledger

| Family | Exact encoding and size | Published theorem / model | Strong legal shortcut | Transfer gap |
| --- | --- | --- | --- | --- |
| Random proper signed 3-CNF | n original variables, 8n proper signed three-literal clauses sampled with replacement, indexed bit length Theta(n log n) | Pang 2026-10-24 arXiv:2610.00837v2 Theorem 7.2(a): exponential size in syntactic Res(PC1/F2), w.h.p.; **preprint** | Arbitrary paid nonaffine gates, source sharing, nonlocal exported LOCAL and extensions may be stronger | /513 and /515 cover only affine-closed definitions + original-3-local mixed rules; full [P2-C3] OPEN |
| Odd-charge cubic-expander Tseitin | h vertices, 3h/2 edge variables, four signed proper three-clauses per vertex, 4h clauses, Theta(h log h) encoded bits | Urquhart 1987 and Ben-Sasson–Wigderson 2001: exp ordinary shared-DAG Resolution size | Original /341 AND3+GF(2) gives 4h−1 paid nodes; /514 sparse replay | Cannot be used for all-mixed lower bounds |
| Haken pigeonhole | h+1 pigeons, h holes, h(h+1) variables, standard unbounded-width CNF | Haken 1985: exp ordinary Resolution | Cook 1976 Extended Resolution polynomial proofs | Proper 3-CNF transport and lower-bound-preserving simulation must be separately proved |

**Scope firewall:** This expands one restricted compiler to syntactically nonlinear **but semantically affine** DEF owners. It does not cover nonlinear gates with independent affine inputs, later observed-only cancellation, unbounded-local mixed conversions, arbitrary branch/split/discharge, nonconservative definitions, or an unrestricted SAT decider. A restricted proof-size theorem, even with explicit source-preserving translation, is not general computational hardness.

## Publication and next proof obligation

Code `experiments/arc/lspv1_515_rank_one_gate.cjs`; raw `results/raw/arc/2026-11-08_1400_LSPV1_515_RANKONE_GATE_RAW.json`; handoff `research/coordination/2026-11-08_1400_LSPV1_RANKONE_GATE515_FIVE_ROLE_HANDOFF.md`. Proof-chain node [P2-L1-515] to be inserted only with a current complete `proof2.txt` blob and optimistic SHA guard; `proof1.txt` has no mathematical change. Post affected node to coordination issue #3 after publishing and verify readback. No edit to unreadable root main.tex; preserve all agents' authorship regions.

**Actual advance:** necessary-and-sufficient per-gate affine-closure criterion including dependent-input nonlinear truth tables, and a constant-overhead projected defining-facet macro; exhaustive and independent controls succeeded. **Still OPEN:** historical full mixed-rule authentication/transfer [P2-D1]/[P2-C3], full-R superpolynomial lower bound [P2-B1], and noncircular same-R B3 [P2-B2]. P versus NP remains OPEN.
