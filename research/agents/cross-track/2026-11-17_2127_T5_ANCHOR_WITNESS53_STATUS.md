# T5-ANCHOR-WITNESS53 | Cross-track hostile synthesis | 2026-11-17 21:27 PST

**Status:** PROVED/EXACT deterministic decision-to-witness reduction for the fixed five-symbol T5-CSP, with fully charged polynomial source construction; a scoped proof-transport counterexample; 431 finite source tests (3,017 assertions, zero failures). The theorem is mathematically elementary and may be viewed as the fixed-template core/constant-pinning search-to-decision principle, NOT a new general lower bound. Independent external review remains open. **P versus NP remains OPEN.**

## (1) Proposed integrations, recorded BEFORE literature/source search

A. Resource contraction + Universal Obstruction: build an honest direct T5-SAT decision-to-witness reduction on the same source, with all oracle-query graph generation, workspace, outputs and time charged, while respecting one identical final satisfiable source across all candidate programs.

B. Nonrelativizing simulation + delayed true constraint: test whether an unavailable edge/clock source bit creates a computation that an assumed polynomial T5 decider cannot bypass by simply rerunning its decision procedure after the edit. Reject a mere temporal surprise as a lower bound.

C. Proof Transport: adversarially test whether refutations of failed pinned T5-decision subqueries can be transported to the original source. A satisfiable original with an unsatisfiable pinned query should falsify this naive bridge.

D. Source/contraction consistency: use a complete five-node anchor whose graph homomorphisms are verified automorphisms, not assumed unary-pinning predicates outside the NP-complete T5 language. Test corrupted anchors.

## (2) Sources searched/read, November 17 research run

**Repository:** TMR-2/075 four-vertex local T5 obstruction (2026-11-17 20:16 PST), TMR-2/075b growing-alphabet extension (20:35 PST; *different* from fixed T5), TMR-4/062 live shared-core charged compiler, LSPV-2/605 exact restricted source-bound Davis-Putnam to Resolution compilation, LSPV-3/621 accepted SAT-source checker counterexample and same-source authority firewall, historical Nonrelativizing TRACEAUDIT23, CLOCKAUTOMATON27 (2026-11-17 20:30 PST) semantic-fiber restriction, prior cross-track T5-FIVEARC-OBSTRUCTION52. TMR-4/069 and /070 relevant newer Library reports were checked and identified as restricted representation-vs-semantic controls; neither establishes a general T5 decision lower bound.

**Project chats/files and Google Drive:** October UWI common-input quantifier reports DIAGONALLIST34 and ORACLELEAK35; KRYLOVGUARD41; Google Drive "P vs NP Research Portfolio - Living Log." The older DRIVE reports provide source-quotient warnings but do not replace newer T5 source checks. No evidence of completed arbitrary-decider-to-Resolution/PC transport or a compulsory nonrelativizing WRAPPER hinge was found.

**Primary literature:** Bang-Jensen, Hell, MacGillivray (1988), The Complexity of Colouring by Semicomplete Digraphs, https://doi.org/10.1137/0401029 : fixed T5 has multiple directed cycles and is NP-complete. Background: Hell and Nesetril, Graphs and Homomorphisms (2004) on cores/retractions; Baker, Gill, Solovay (1975) on relativization barriers. The actual anchor theorem below is independently proved, not imported from the literature.

## (3) Exact integrated theorem: decision-to-witness within the SAME T5 language

Let T5 have vertices 0,1,2,3,4 and directed arcs R(a,b) iff (b-a) mod 5 is in {1,3}. Let G=(V,E) be any finite explicitly encoded T5 source, including isolated vertices, loops and antiparallel constraints. Let Q be a disjoint labelled copy of the complete T5 tournament, with anchor vertices q_0,...,q_4. For each partial pin map p:U -> {0,...,4}, define H(G,p) by taking G disjoint union Q and **identifying** each original source vertex v in U with anchor vertex q_{p(v)}. The operation constructs an ordinary directed T5-CSP source with *only original R arcs*, no constant predicates or unary oracle.

**Lemma (exact pinning semantics).** For every G and p,

  H(G,p) is T5-satisfiable  iff  G has a T5-coloring f with f(v)=p(v) for all v in U.

**Proof.** Distinct vertices of the complete loopless tournament Q have a directed arc between them. Under any homomorphism Q -> T5, they cannot collapse, since T5 has no loops. Hence the five anchor images are a permutation of T5 vertices, and a bijective homomorphism of the finite tournament is an automorphism alpha. Given a coloring h of H, alpha^{-1} composed with h gives a valid G-coloring and fixes each q_j at j; original vertices identified with q_{p(v)} therefore have prescribed colors. Conversely, a G-coloring respecting p extends with the identity coloring on disjoint Q and agrees at every identified vertex, giving a homomorphism of H. QED.

**Theorem (fully charged T5 decision-to-witness reduction).** Given any correct T5 decision procedure D, there is an explicit Turing witness extractor W^D such that on any source with n original vertices and L input bytes, W^D outputs a valid 5-coloring if the source is SAT and reports UNSAT otherwise. It makes at most 5n calls to D, each on a genuine canonical T5 source of length B=O(L log(L+2)), and uses no witness/proof/oracle other than those decision calls.

Algorithm: If n=0, output the empty coloring. Otherwise iterate v=0,...,n-1, keeping earlier chosen colors p. For c=0,...,4 generate H(G,p union {v:c}), submit to D, and keep the first c yielding SAT. If all five candidates fail at any step, report UNSAT. Finally output p in source order. Every extension step preserves existence by the lemma. For UNSAT G, the five first-variable queries all fail. In all cases the output is correct.

**Resource statement:** The canonical source contains explicit vertex declarations, so n,m<=L. Each quotient contains at most n+5 vertices and m+10 unique arcs. Build it by scanning the source, computing equivalence representatives, merging arcs, sorting/deduplicating and writing the complete authenticated source. A conservative conventional bit-machine bound per query is O(B^3) generation time and O(B^2) peak generation workspace, including input reading, vertex/edge indexing, full output materialization, sorting, and source replay. With a decider having time T_D(B) and workspace S_D(B), a sequential same-realization implementation has

  time O(n [T_D(B)+B^3]),  peak workspace O(S_D(B)+B^2),

including persistent pins, inputs and answer output. No free source oracle, recursive call stack, skipped graph materialization or uncharged witness output. Thus if T5-SAT were in P, its witness search would be in FP. Conversely, any total polynomial-time witness producer valid on all SAT sources yields a polynomial-time decision procedure by checking the returned coloring. This is an exact conditional equivalence, **not** a P!=NP proof.

**Important quantifier consequence for same-final-input UWI:** Any proposed UWI portfolio that claims all eligible programs fail on one fixed SAT graph must include the hypothetical source-aware extractor W^D if D in P and its code and time budgets admit W^D. An unrestricted per-input program allowance is trivially defeated by a program hardcoding one valid coloring of that exact graph. Therefore meaningful UWI claims must specify a code bound, a common final input, one common clock, and a valid family-wide uniformity requirement. With an unbounded increasing code allowance and quantification over all polynomial exponents, a proven common-input witness obstruction would itself imply T5 not in P and hence P!=NP; it cannot be assumed as a preliminary shortcut.

## Hostile falsifications and strict other-track firewalls

**Proof transport fails without a genuine theorem:** Take G containing just the original arc 0->1, which is SAT (colors 0,1). The numerical pin p(0)=0, p(1)=2 is impossible because R(0,2)=false; H(G,p) is UNSAT by the lemma. Therefore even an authentic one-hot Resolution refutation of H(G,p) cannot generically be transported into an UNSAT refutation of original G: such a refutation would be unsound. It transports at most a rejection of *that pinned branch*. A complete exhaustive branch-discharge proof requires actual combination rules and size accounting. LSPV-2/605 covers a specified DP/Resolution path, not arbitrary T5 deciders.

**WRAPPER:** A delayed real T5 source edit may change SAT, but if a polynomial D existed the updated source can simply be parsed and decided again. Temporal unpredictability, source hashes, and proof-agnostic clock provenance are not alone correctness-forced costly operations; the specific nonrelativizing hinge remains OPEN. This decision-to-witness theorem itself relativizes and cannot independently cross the Baker-Gill-Solovay barrier.

**Contraction and representation:** The 5-node anchor is constant size, but every hypothetical decision call must be charged and can still be NP-hard. The theorem makes no claim about unconditional polynomial-time T5 decision, no small-space forbidden pair, no universal descriptor contraction and no high-rank-to-general-work promotion. The /070 source-recognizable high-width families and /075 tiny local UNSAT motif remain legal cheap-algorithm controls.

**Corrupted-anchor falsifier:** Remove the ten anchor arcs, keeping pins 0->q0, 1->q2 and original 0->1. The resulting ordinary graph is SAT even though the intended numerical pin 0->2 is illegal. Thus anchor completeness and the finite tournament core property are load-bearing; a free list/constant encoding is not silently assumed.

## Independent finite audit

Ran complete Python standard-library audit with deterministic seed 202611172123: **431 exact source graphs, 329 SAT, 102 UNSAT, 3,017 assertions, zero failures.** Includes all 64 four-vertex DAGs under a fixed topological order, random loops and antiparallel arcs, empty graph, six-variable complete acyclic orientation, and the earlier five-arc UNSAT motif. Oracle was a genuinely generic backtracking T5 decider applied to the **fully materialized augmented graph**, compared to independent direct exhaustive original-source enumeration. 1,665 actual oracle queries, 1,020 independent numerical-pinning equivalence checks, 191,597 total emitted query bytes, maximum query length 232 bytes. Verified all five T5 automorphisms are cyclic shifts. Corrupted-anchor test created the expected spurious SAT. The implemented finite oracle is exponential, **not** a polynomial-time T5 solver. Executable local file: t5_anchor_witness53_audit.py; raw JSON: 2026-11-17_T5_ANCHOR_WITNESS53_results.json. Mathematical theorem supplies the all-input conclusion; finite checks do not prove an asymptotic lower bound.

## Proof DAG

| Arrow / claim | Status |
|---|---|
| Fixed-template T5 homomorphism NP-complete | ESTABLISHED, Bang-Jensen/Hell/MacGillivray |
| Full five-node anchor homomorphisms are automorphisms | PROVED exact |
| Ordinary T5 quotient encodes numerical pins | PROVED exact |
| At most 5n charged T5 decision calls recover any SAT witness | PROVED exact CONDITIONAL upper reduction |
| If T5-SAT in P, then its witness search is in FP | PROVED conditional |
| Pinned-query UNSAT refutation generically refutes original SAT graph | FALSIFIED by 2-vertex one-arc source |
| Hardcoded witness defeats unrestricted fixed-input UWI portfolio | PROVED for unrestricted description/time admission; not a bounded-uniform lower bound |
| WRAPPER's delayed edge necessarily forces more than polynomial D-recomputation | OPEN |
| Arbitrary decider traces transport to a fixed hard proof system | OPEN |
| Fully charged universal T5 resource contraction contradiction | OPEN |
| Unrestricted superpolynomial T5 decision-time lower bound / P!=NP | OPEN |

## Four next specialist assignments

**Resource Contraction:** Use H(G,p) as a formally valid, fully charged decision-oracle interface. Determine whether a proposed universal contractor actually reduces T_D(B) rather than hiding it in O(n) queries; test all parsing, generation, workspace, serialization and recursion costs. Focus on genuine 3-connected cores after local motif filtering.

**Nonrelativizing Simulation:** Specify a SAT-status-changing delayed constraint which cannot be neutralized merely by calling the hypothetical D on the updated source. State a precise model where direct recomputation is forbidden *by correctness rather than by an algorithm restriction*, and test relativization/oracle replay.

**Universal Obstruction:** Use one identical final satisfiable T5 source, common clock and explicit code-length budget; include the anchored W^D conditional program among challengers. Audit whether the claimed UWI quantifiers entail T5 not in P or merely exclude an explicitly restricted portfolio.

**Proof Transport:** For a pinned query H(G,p), prove a legal branch-discharge/certificate composition that derives the original result with exact calculus, encoding, line count and space charges. The 2-vertex false pin prevents an illicit one-branch refutation projection.

**Highest-value OPEN implication:** A representation-independent superpolynomial T5 decision lower bound, or an honest time-space contradiction for all hypothetical polynomial-time T5 deciders. The current exact reduction is a quantifier and cost firewall, not a shortcut to that conclusion.

No other agents or schedules changed.
