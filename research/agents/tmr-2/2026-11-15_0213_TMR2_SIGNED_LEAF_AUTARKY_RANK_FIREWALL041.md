# TMR-2/041: Signed NAE edge-leaf quotient, full-X transparency and an exact typed tariff

**2026-11-15 02:13 PST | LEAF081 | PNP Information Necessity | PROVED/RESTRICTED symbolic theorem, independent mathematical review OPEN; executed finite controls COMPUTATIONAL. P versus NP OPEN.**

## 1. Claim and preselected falsifiers

**Candidate being tested.** The exponentially high rational separator rank and exact one-rectangle-cover of the proper 3-CNF family Q_k from TMR-2/040 might remain a positive dynamic SAT-machine fusion obligation after the degree-profile witness is quotiented away.

**Falsifiers fixed before inspection:** (F1) an authenticated per-edge *private variable* permits a satisfying extension for every separator assignment, eliminating the projected interface entirely; (F2) arbitrary independent literal sign gauges or clause permutations defeat the earlier degree-profile witness but admit a different polynomial witness constructor; (F3) a correct source recognizer needs uncharged isomorphism, clause pairing, or an illegal shortcut; (F4) any proposed unit PEEL tariff fuses multiple source obligations, or an already valid zero-cost step decreases the potential. F1 and F2 are proved for the declared family and much larger syntactic class. F3 is addressed by explicit parsing, source verification and fallback. F4 is tested in a fully qualified **separate typed edge calculus**, not asserted for a physical SAT machine.

The actual fixed finite total SAT decider and the authenticated edge-record protocol below are **distinct transition systems**. The latter is a calibration laboratory. Source authentication, parsing, deduplication, proof discovery and physical operations are never free in the former.

## 2. Exact signed NAE grammar and edge-leaf reduction

A proper width-three source clause uses three distinct variable identifiers. For a triple of signed literals (l_1,l_2,l_3), define the two-clause conjunction

$$
N(l_1,l_2,l_3)
=(l_1\lor l_2\lor l_3)
\land(\neg l_1\lor\neg l_2\lor\neg l_3).
$$

In the **authenticated paired NAE sublanguage**, clauses are grouped by their **unordered triple of absolute variable IDs**, and each nonempty group contains exactly two complementary sign vectors, with optional exact-clause duplicates. There are no additional distinct sign vectors in the same group. Reject the sublanguage parser if a group has one, three or more distinct signs, or noncomplementary pairs. This is a conservative recognizer: an arbitrary rejected 3-CNF passes to exact SAT fallback, NOT to an UNSAT verdict. Retain the original source clause indices and verify the final witness against every original clause.

After authenticated grouping, a distinct triple/group is one edge identity e in a signed three-uniform hypergraph H=(V,E). Different edge groups may use different, completely independent sign gauges; no global variable-flip consistency is required.

An **edge-leaf step** chooses an edge e in the CURRENT remaining hypergraph and a variable v of degree exactly one in that remaining hypergraph, with v in e, then deletes e and records (source-edge ID e, pivot v, three signed literals). Repeat. The final remaining subhypergraph H_core is the signed edge-leaf core of the chosen sequence. No claim that this is the conventional alpha/beta-acyclicity notion is made.

**Theorem LEAF081-A (exact existential quotient, PROVED/RESTRICTED).** For every finite authenticated signed paired-NAE source F and every valid edge-leaf deletion sequence leaving F_core, every satisfying assignment of F_core extends to an assignment satisfying F. Equivalently, after existentially eliminating variables absent from F_core, the formula F has precisely the same projected Boolean relation as F_core on its surviving variables. In particular, if the sequence deletes every edge, F is SAT and a complete witness can be constructed in polynomial time. This holds for arbitrary independent edge sign vectors and even when the original support graph has large primal treewidth.

**Proof.** At a removal step the chosen variable v occurs in no other *remaining* edge. Fix every other literal value in e, including all previously fixed interface variables. At least one of the two values of v makes N(l_1,l_2,l_3) true: if the other two literal values agree, choose the opposite for the pivot literal; otherwise either value works. Hence existential elimination of v makes the removed signed NAE constraint TRUE and leaves every remaining constraint unchanged. Iterate and reconstruct in reverse. At reverse stage the pivot of the restored edge does not occur in any later-removed edge, hence has not been assigned by a later restoration. Assign any as-yet-unassigned nonpivot variables arbitrarily, then choose the pivot value as above. Earlier restored edges remain true; source clause verification confirms the result. The cost bound follows from repeated finite indexed scans and stack reconstruction. QED.

**Crucial provenance limitation.** The theorem requires a genuine two-clause complementary NAE pair per edge. A single positive three-clause, an arbitrary signed 3-CNF, or a source with multiple contradictory pairs on one triple does NOT automatically admit this projection. Do not treat a partial or competing group as a complete NAE edge.

## 3. Stronger Q_k control: exponential evaluation rank but constant existential interface

Use the identical Q_k from TMR-2/040, with k>=2, n_k=3k+binom(k,2), m_k=k+binom(k,2)=k(k+1)/2 NAE edges, 2m_k proper clauses and encoded length L_k=Theta(k^2 log(k+2)):

$$
Q_k=\bigwedge_i N(X_i,Y_i,W_i)
\land\bigwedge_{i<j}N(X_i,X_j,Z_{ij}).
$$

Every edge has an initially degree-one variable outside X: W_i in the first kind and Z_ij in the second kind. Therefore for **every** assignment x to X, there exists an extension to Y,W,Z satisfying Q_k. The stronger exact interface statement is

$$
\boxed{\exists(Y,W,Z)\ Q_k(X,Y,W,Z)\equiv\top.}
$$

For the first edge choose a private literal opposite to X_i; for each pairwise edge with Xi=Xj choose Z_ij opposite, and if they differ choose Z_ij arbitrarily. All private choices are independent. This remains true under arbitrary independently chosen signs inside every NAE pair, not merely consistent global variable complementation.

Nevertheless TMR-2/040 already proved, and TMR-5/037 independently rechecked, that the X versus (Y,W,Z) **evaluation matrix** M has rational rank exactly 2^k and minimum all-one rectangle cover exactly 2^k. The original rank witness uses the aggregated matrix

$$
K_k(x,y)=2^{t(x)(k-t(x))}\prod_i(x_i\lor y_i)
=\operatorname{diag}(2^{t(x)(k-t(x))})
\begin{pmatrix}0&1\\1&1\end{pmatrix}^{\otimes k}.
$$

The new quotient observation concerns existential quantification, not ordinary matrix rank: **all 2^k distinct rows have a 1-entry, and OR-aggregation across all private columns is simply the constant 1**. These two facts coexist without contradiction. Consistent variable permutations/complementations merely permute matrix rows/columns, so the 2^k rank persists under those transformations. For arbitrary *independent per-edge* sign gauges, the polynomial witness theorem persists, but the exact rank of the newly gauged evaluation matrix is NOT asserted.

The family also has a K_k primal clique and non-Horn, non-dual-Horn, non-bijunctive, non-affine existential projection onto a selected local three-variable NAE relation in its original signs. These structural features do not prevent the global existential X-interface from being TRUE.

**New relative to TMR-2/040:** The previous successful assignment used a degree threshold to distinguish X variables and assigned all non-X variables TRUE. This new constructor does not need to identify X, does not depend on the sign of a shared vertex across edges, admits arbitrary independently signed NAE triples, and extends *every specified boundary assignment* rather than constructing just one chosen assignment. It isolates a previously unchecked certified leaf/autarky quotient of the exponential-rank example. The general mathematical idea of eliminating locally private variables is elementary, not claimed as a newly discovered complexity theorem.

## 4. One fixed correct total physical SAT decider

On every binary source string, a fixed finite-alphabet deterministic locally moving multitape machine D:

1. Parses the complete fixed CNF encoding, handling malformed strings according to the same total SAT decision convention.
2. Groups clauses by sorted absolute triple; deduplicates equal source clauses using **paid** comparisons, and checks that each distinct sign pair is complementary and that no other sign is present.
3. On an authenticated paired-NAE source, repeatedly scans remaining edge/variable incidence to locate a genuine degree-one variable. Stores a list of original source edge IDs and pivots; on success reconstructs an assignment in reverse.
4. Evaluates **every original clause** on the reconstructed assignment and accepts only if this actual witness passes. On a failed grammar, stalled peel, or failed verification it invokes ordinary exact exhaustive SAT search. Thus both SAT and UNSAT answers remain correct on every input.

All arrays/counters can be encoded over fixed finite tape alphabets; binary IDs, dynamic workspace, head motion, comparisons, source rereads, edge deletion marks, signed pivots and final verification are included. With at most O(L) clause records and naive repeated scans/comparisons, a deliberately loose bound of O((L+1)^8) physical transitions suffices on successful peelable inputs; polynomial workspace suffices. This is a standard constructive finite-tape upper-bound compilation, not a compiled physical machine trace; independent machine-level cost audit remains OPEN.

Consequently D accepts all Q_k, all renamed/reordered/duplicated/global-sign-flipped Q_k and indeed all well-formed signed paired-NAE sources with complete edge-leaf elimination in polynomial time. Arbitrary extra source clauses are accepted early only if the *whole* authenticated paired grammar remains valid and the eventual witness verifies; otherwise the exact fallback retains correctness. There is no free advice, hidden assignment oracle or unit-cost unbounded arithmetic.

## 5. Authentic typed edge protocol and joint tariff

Define a **separate preauthenticated abstract record calculus R_leaf**. An initial state includes the exact immutable signed edge list E, once-owned edge identities, remaining-edge set U=E, empty stack S, empty partial assignment, control phase PEEL and active flag h=1. Its **declared** legal transitions are:

| Legal event | Event price | Change (Delta p_FUS, Delta p_GAMMA, Delta p_MACHINE) |
| --- | ---: | --- |
| NOP, identity or zero-cost PEEL-to-RESTORE phase switch when U is empty | 0 | (0,0,0) |
| PEEL one currently degree-one edge, push one authenticated (edge,pivot) record | 1 | (2,-1,0) |
| RESTORE one most-recent pivot, satisfying its signed pair and popping one record | 1 | (0,1,0) |
| HALT once every source edge is restored and the full authenticated goal verifies | 1 | (0,0,1) |

These are **abstract record events**, not single physical Turing-machine transitions. Original-source grouping and verification are preauthenticated premises of this calculus; if charged in a physical implementation they are additional costs. Illegal pivot, malformed source, failed restoring, and stuck nonempty core cannot reach the declared successful goal. An external fallback SAT machine is a *different* system and cannot inherit R_leaf lower bounds without all-step simulation. Unknown operations in an arbitrary SAT machine are MAY, not forbidden.

Define the seven-coordinate reduced-product vector in the customary column order CNF, XOR, SEP, FUS, GAMMA, INT, MACHINE:

$$
p(C)=(0,0,0,\underbrace{2|U|}_{\text{peel plus future restore tickets}},
\underbrace{|S|}_{\text{outstanding restore debt}},0,
\underbrace{\mathbf1_{\text{active}}}_{\text{HALT ticket}}).
$$

The FUS and GAMMA labels here denote **typed protocol tickets**, NOT a representation-independent fusion/assumption invariant for SAT. Zero-cost NOP and phase switching preserve all three varying coordinates, so authentic directed zero-cost closure and SCC quotient do not decrease p.

The exact nonnegative rational weight certificate is

$$
\lambda=(0,0,0,1,1,0,1).
$$

Each of the complete five legal row classes has weighted decrease 0,0,1,1,1 respectively, no more than its authentic event price. In particular, a PEEL decreases the first ticket by 2 but **creates** one restore debt, giving net discharge 2-1=1. Do not add the two apparent charges independently. The initial potential is 2m+1 and terminal potential is zero. Every successful R_leaf transcript must peel each of the m distinct owned edges, restore each exactly once, and execute HALT, so its minimum native record-event price is exactly

$$
\boxed{\overline W_{R_{\mathrm{leaf}}}(F)=2m+1=\Phi(C_0).}
$$

This is proved for a completely peelable authenticated input in this intentionally restricted typed protocol. For Q_k, m=k(k+1)/2 and exact record price k(k+1)+1=O(L_k). Shared literal/variable appearances are *not* charged once per consumer; edge identities are charged exactly once, while each created restore obligation is discharged once. There is no exponential initial gap.

**Forbidden extrapolation.** The record price of 2m+1 is NOT a lower bound for all physical SAT solvers. An algorithm may construct an assignment in another order, use one global pattern, eliminate clauses without materializing this stack, cache, recompute, or use compact circuits. The same-system transfer gate is OPEN. A hypothetical extension allowing a one-price BATCH-PEEL of two edges would discharge (4,-2,0) and violate the displayed positive weight certificate; such an extension requires a new cost/transition audit, not silent exclusion.

Machine-readable exact tariff schema: results/raw/tmr/2026-11-15_0213_TMR2_LEAF081_TARIFF.json.

## 6. Hostile controls and zero-cost/shortcut ledger

| Control | Exact scope and disposition |
| --- | --- |
| Arbitrary independent literal gauges | PASS: each signed NAE edge admits local pivot completion, even if sign choices are inconsistent across shared variables |
| Bijective renaming, literal/clause reordering, exact duplicates | PASS in the charged recognizer; duplicate signed clauses are deduplicated, never turned into new edge identities |
| Missing companion or competing third sign vector | REJECT paired-NAE early route; fall back to complete SAT, no false UNSAT |
| Non-leaf hypergraph and UNSAT | Full all-triples K5 NAE is UNSAT and has no degree-one pivot, so peel route stalls and fallback is required |
| Gaussian/Tseitin and compact circuits | Already legitimate easy mechanisms, and the new leaf quotient is additional; no affine-based lower bound is inferred |
| Horn, dual-Horn, Krom/2-SAT | NAE3 is outside these *relation languages*; leaf-peel tractability is a different source-structural mechanism |
| Bounded treewidth separator DP | Q_k has primal treewidth at least k-1 but still entirely private-leaf extendible |
| Certified autarky and private variables | Exact existential source projection is certified by the reverse witness, not presumed from a raw count |
| Extension/learning/other representations | All remain legal in arbitrary SAT machines. This is a shortcut/falsifier, not a model-independent exclusion |
| Shared computation, rereading, caching and recomputation | D reuses the authenticated edge list and witness; all physical accesses are charged polynomially |
| Zero-cost closure | R_leaf has only genuine declared NOP/switch zero-price events, preserving p; a physical TM has no free event |
| Historical logical authorities | Archived /341 full accepted-language checker remains FAIL; /386 remains RESTRICTED; neither is silently used |

The 2P2N near-q-Horn backdoor radius is a different restricted component, not an exhaustive branch-count theorem, and is not invoked here. No conclusion about MCSP/MKTP, nonuniform circuit lower bounds or unrestricted P-vs-NP follows from this construction.

## 7. Executed tests, provenance and literature

The exact V8 function serialized in experiments/tmr/tmr2_signed_leaf_autarky081.js was executed in the tool's V8 isolate. It completed **14,057 assertions, zero failures** with deterministic seed 417003. It tested 190 independently renamed, globally polarity-flipped, reordered and duplicate-padded Q_k sources for k=2..11 (5,415 source leaf records); exhaustively enumerated all 5^4=625 signed/absent configurations on the four possible 3-edges of four variables (113 peelable, 512 not); tested 1,200 seeded signed six-variable hypergraphs; rejected malformed companion/overlapping-sign/nonproper controls; checked an UNSAT nonpeelable five-variable complete 3-hypergraph; and computed full modular rank 2^k for the rank-witness aggregated matrices k=2..5 over F_1000003. All five exact tariff rows were checked; m=66 gives initial potential=exact typed event price=133. Finite modular rank checks support but do not replace the independent rational full-rank symbolic proof.

Code: experiments/tmr/tmr2_signed_leaf_autarky081.js. Original V8 raw: results/raw/tmr/2026-11-15_0213_TMR2_LEAF081_V8_RAW.json. Matrix: results/raw/tmr/2026-11-15_0213_TMR2_LEAF081_TARIFF.json. The function body in published JS is serialized from the **exact function actually run**; the final Node console wrapper was not independently executed in a separate OS process, and there is no compiled physical TM.

**Primary context, not assumed as an unproved shortcut theorem:**

1. T. J. Schaefer, "The Complexity of Satisfiability Problems," STOC 1978, pp. 216-226, DOI https://doi.org/10.1145/800133.804350. Schaefer's relation dichotomy is background only. The exact paired-NAE projection and leaf-extension theorem are proved directly in this report.
2. O. Kullmann, "Constraint Satisfaction Problems in Clausal Form I: Autarkies and Deficiency," Fundamenta Informaticae 109 (2011), 27-81, DOI https://doi.org/10.3233/FI-2011-428. General autarky context; NOT a citation for the present exact Q_k rank.
3. S. Ordyniak, D. Paulusma and S. Szeider, "Satisfiability of Acyclic and Almost Acyclic CNF Formulas," Theoretical Computer Science 481 (2013), 85-99, DOI https://doi.org/10.1016/j.tcs.2012.12.039. Acyclic hypergraph structural SAT context, not a claim that Q_k has bounded treewidth or is alpha/beta-acyclic.

**Original corpus ledger, direct source reads:** TMR-2/040 NAERANK075 (source path research/agents/tmr-2/2026-11-15_0113_TMR2_NAE_RANK_FOOLING_DEGREE_FIREWALL040.md); TMR-5/037 NAEGUARD079 (research/agents/tmr-5/2026-11-15_0143_TMR5_NAE_RANK_GUARD_COMPOSITION037.md); TMR-2/039 EQUALJ072; LEAD-0029 Lipschitz audit; historical research/main/2026-10-18_1655_MAIN_NAECOMPANION1.tex; LSPV-2/284 NAE gadget scope and original /341 /386 qualifications via proof2; five TMR handoffs; issue #3; both proof trackers, canonical root main.tex, AGENTS.md, CODEX.md and research skill. NAECOMPANION1 uses *leaf edges* appended to a potentially UNSAT core and separately uses the word "peeling" for spread terms; it did **not** establish the edge-leaf projection of this Q_k or a degree-free signed source recognizer. The elementary local gadget transparency was already known in that earlier work, so no priority claim is made for the general private-variable trick.

**Corpus reconciliation:** TMR-2/040's rank and rectangle theorem retained at original scope, its degree-based polynomial witness strengthened by the present independent signed/private-leaf quotient; TMR-5/037's guarded Resolution and small interpolant retained as a different model; LEAD/0029's raw-semantic-mass warning reinforced. No prior actual theorem is retired. The **proposed** positive fixed tariff on unquotiented Q_k evaluation-rank obstruction remains FALSIFIED for this family; the new typed 2m+1 tariff is restricted and does not repair it. The strict /341 FAIL and /386 RESTRICTED statuses remain unchanged.

**Barrier audit:** Relativizing or granting compact local NAE witness construction only makes the current family easier; no oracle separation is inferred. No algebrization or Natural Proofs transfer is invoked, because there is no general circuit lower bound. Shared-path selection, semantic vs machine-state mismatch, finite-alphabet compilation and uniform all-algorithm quantifiers remain the critical OPEN gates.

## 8. Next target and peer requests

**Next TMR-2 target:** construct a *nonleaf* signed NAE or CNF interface family with no certified private-edge elimination, no cheap Gaussian/equality/Horn/2-SAT/treewidth/autarky quotient, a formally authenticated surviving interface relation, and a **dynamic** obstruction whose local discharges are evaluated against both genuinely cheap and proof-producing transitions. Explicitly test alternative shared circuits and learning before proposing a positive weight.

**TMR-3:** independently check finite-tape polynomial implementation and all physical source-grouping/verification work. **TMR-4:** audit the five-row typed ticket potential including the negative PEEL stack change and exact zero-cost closure; do not equate typed PEEL with one physical step. **TMR-5:** independently check all-Q boundary transparency under independently signed edges, the source grammar and opposite-label controls. **TMR-1:** record that this family remains P-easy despite exponentially high rank and high primal width, and that R_leaf-to-arbitrary-machine transfer is OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, recovered complete proof2.txt, and root main.tex remain unchanged. No TMR title/schedule/enable state was touched. P versus NP remains OPEN.
