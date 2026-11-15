# TMR-2/042: nonpeelable NAE core, maximal projected rank, and a paid polynomial witness

**2026-11-15 03:12 PST | NAE2CORE087 | PNP Information Necessity**  
**Scientific status:** PROVED/RESTRICTED symbolic construction and counterexample, independent mathematical peer review OPEN. Native V8 finite evidence COMPUTATIONAL. P versus NP OPEN.

## 1. Candidate and falsifiers, fixed before source/literature review

**Candidate being falsified:** a nonzero, source-static fusion/separator tariff attached to large rank or one-rectangle cover might remain viable after TMR-2/041's degree-one-NAE peeling is exhausted, particularly on a non-Schaefer proper 3-CNF with a large primal clique and a nonempty canonical leaf core.

Four falsifiers were selected: (F1) an authenticated fully polynomial witness constructor even though no NAE edge is peelable; (F2) an affine or compact signed-twin quotient collapsing the rank; (F3) a legal one-price final machine step that overdischarges a source-static terminal-masked rank; (F4) gauge flips, variable renaming, clause shuffling and duplicate padding breaking the proposed uniform shortcut. F1-F3 are realized. F4 is addressed symbolically by a source-grammar recognizer and computationally by signed-renamed witness tests.

This extends, rather than repeals, the earlier TMR-2/040-041 NAE rank and private-leaf controls. In TMR-2/040, at least one variable was private to each hyperedge; here **every variable belongs to at least two distinct signed NAE groups**. TMR-4/042's canonical leaf core consequently retains the entire source hyperedge set, yet the SAT witness still has polynomial construction cost.

## 2. Exact growing family R_k and source measure

For k >= 2 let X={x_i}, Y={y_i}, Z={z_i} for i=1,...,k. For each i<j introduce fresh u_ij,a_ij,b_ij. Write NAE(l,m,n) for the proper 3-CNF pair

$$
(l\vee m\vee n)\ \wedge\ (\neg l\vee\neg m\vee\neg n).
$$

Define

$$
R_k =
\bigwedge_{i=1}^k
  \bigl[\mathrm{NAE}(x_i,y_i,z_i)\land
        \mathrm{NAE}(x_i,y_i,\neg z_i)\bigr]
\ \land\
\bigwedge_{1\le i<j\le k}
  \bigl[
    \mathrm{NAE}(x_i,x_j,u_{ij})\land
    \mathrm{NAE}(u_{ij},a_{ij},b_{ij})\land
    \mathrm{NAE}(x_i,a_{ij},b_{ij})
  \bigr].
$$

There are exactly

$$
n_k=3k+3\binom{k}{2}, \qquad
m_k=2k+3\binom{k}{2}
$$

variables and distinct NAE groups, respectively. There are 2m_k=4k+6 binom(k,2) proper width-three clauses, each with three distinct variable IDs. A conventional explicit indexed binary encoding with no padding has length L_k=Theta(k^2 log k). Every variable has both positive and negative original-CNF occurrences, since each NAE group contributes a complementary clause pair.

All NAE-group incidence degrees are at least 2. In particular,

$$
\deg(x_i)=2k+1-i,\qquad
\deg(y_i)=\deg(z_i)=\deg(u_{ij})
          =\deg(a_{ij})=\deg(b_{ij})=2.
$$

Thus the degree-one-edge PEEL rule of TMR-2/041 and TMR-4/042 cannot fire even once. Their canonical 2-core K(E) equals the complete E. The edges (x_i,x_j,u_ij) realize K_k in the primal graph, so primal treewidth is at least k-1.

## 3. Exact existential projection and rank theorem

**Theorem 042.1 (nonleaf full-rank projection).** For every k>=2,

$$
\exists (Z,U,A,B)\ R_k(X,Y,Z,U,A,B)
\quad\equiv\quad
\bigwedge_{i=1}^{k}(x_i\ne y_i).
$$

**Proof.** For fixed x_i,y_i, both NAE(x_i,y_i,z_i) and NAE(x_i,y_i,not z_i) are satisfiable exactly when x_i != y_i. Necessity follows. For sufficiency, choose each z_i=0, choose u_ij=1-x_i, a_ij=0, and b_ij=1. The two x_i,y_i constraints then hold because x_i != y_i; NAE(x_i,x_j,1-x_i) holds independently of x_j; and both guarded NAE constraints contain opposite-valued a_ij,b_ij, so they hold. This constructs an extension for every such pair X,Y. QED.

Let M_k be the 0/1 communication matrix on X rows and Y columns of the **existential** relation in Theorem 042.1. Then

$$
M_k(x,y)=\mathbf1[y=\neg x].
$$

It is a 2^k by 2^k permutation matrix. Therefore its rank over Q and R is EXACTLY 2^k and its minimum all-one rectangle-cover number is EXACTLY 2^k. Indeed every 1 rectangle contains at most one of its 2^k ones: two distinct row-column witness pairs have a zero in both cross positions. These are rank/cover statements, not machine lower bounds.

A second existential projection is decisive:

$$
\exists(Y,Z,U,A,B)\ R_k(X,Y,Z,U,A,B)\equiv\mathrm{TRUE}.
$$

Every X assignment has a satisfying extension. Raw matrix rank persists, but a SAT decider does not have to enumerate a row or materialize the matrix.

**Theorem 042.2 (non-Schaefer source).** The full satisfaction relation of R_k belongs to none of the Horn, dual-Horn, bijunctive or affine classes. For each fixed i<j its existential projection onto the three variables (x_i,x_j,u_ij) is exactly NAE_3: the source edge forces NAE, while any satisfying triple extends by y_i=not x_i, arbitrary z_i, all other u chosen as above, and a/b opposite. NAE_3 fails closure under meet (010 and 100 yield 000), join (011 and 101 yield 111), majority (001,010,100 yield 000), and triple XOR (the same triple yields 111). The four Schaefer closure classes are inherited by existential projection, giving the contradiction. This is a scope-specific structural fact, not an NP-hardness result for the **explicit family**.

## 4. Genuine uniform polynomial shortcut, including gauge controls

**Theorem 042.3 (uniform source-grammar witness).** One fixed correct total deterministic SAT decider accepts R_k for every k in polynomial charged time and also accepts any source obtained from any R_k by a bijective variable renaming, independently flipping any subset of complete source variables, permuting original clauses and inserting exact duplicate clauses.

**Algorithm.** Parse proper 3-CNF, remove exact duplicate clauses, and authenticate that every remaining clause has its exact complementary clause. Pair these into signed NAE orbit groups, each group represented modulo simultaneous complementation of its three signed literals. Obtain their distinct-variable incidence degrees. Determine k from the number of variables of degree>2. Check these high degrees are exactly k+1,...,2k, that every other variable has degree 2, and that the high-variable pair edges form precisely a complete graph with one low-degree third variable each.

For each high variable, find its unique two-group identical-support signed twin, with two low-degree variables; use a constant-size eight-row truth table to authenticate that, with the high variable set to 0, exactly one of those low variables is forced and the other is free. Find the remaining disjoint triple of groups for every high-variable pair: a two-high edge on (x_i,x_j,u), a zero-high group on (u,a,b), and a one-high group on (x_i,a,b). Require every NAE group and every low variable to be accounted for exactly once. Assign all high variables 0, complete each signed twin locally, and for each triple of guarded groups try all eight assignments of (u,a,b), retaining one that satisfies them. Verify the ENTIRE original parsed CNF. If any authentication or verification step fails, revert to a complete exponential SAT decision procedure, not UNSAT-by-heuristic.

This is one fixed uniform program with only polynomially many source comparisons, support/degree computations and constant-size local truth tables. A conservative polynomial multitape implementation can use repeated scans instead of unit-cost random access; no uncharged magic parser, oracle, source-class advice or proof system is required. All local completions exist on the stated family because any global variable flip is a bijective change of assignment coordinates and the canonical R_k extension exists for EVERY X. Clause order and exact duplicate removal preserve the authenticated semantics. The algorithm's malformed-input fallback is total and exact. This statement does **not** claim a polynomial worst-case solver on arbitrary SAT inputs.

**Direct shortest explicit witness:** on canonical R_k, x_i=0,y_i=1,z_i=0,u_ij=1,a_ij=0,b_ij=1. Verification of every clause takes polynomial time. The renamed and sign-flipped witnesses are obtained by the corresponding bijective coordinate transform.

## 5. Exact source-static component and a mandatory physical tariff row

Qualify a fixed finite-alphabet deterministic locally moving multitape SAT machine with exact immutable source, program, control, tape/head contents, paid work ledger, terminal result and cost one for **every physical transition** including HALT. Its authentic zero-cost closure is the identity and its zero-cost SCCs are singletons.

To test the proposed source-derived separator charge, define a deliberately source-static, terminal-masked coordinate:

$$
p_{\mathrm{sep}}(C)=
\begin{cases}
2^k-1 & \text{if the immutable input is }R_k\text{ and }C\text{ is live},\\
0 & \text{if }C\text{ is completed or not an }R_k\text{ input}.
\end{cases}
$$

Take p_machine(C)=1 for live states and 0 at completed goals; all other five components are 0. Both coordinates are invariant under authentic zero-length closure. They are fixed on every paid nonterminal transition. **On the genuine last paid transition to HALT**, their exact discharge is

$$
\Delta_{\mathrm{HALT}}=(0,0,2^k-1,0,0,0,1),\qquad w=1.
$$

Hence any nonnegative tariff weights on this seven-component product must satisfy, for every k>=2,

$$
\lambda_{\mathrm{sep}}(2^k-1)+\lambda_{\mathrm{machine}}\le1.
$$

A single global fixed coefficient lambda_sep>0 FAILS for sufficiently large k, regardless of which SAT decider runs or how much earlier work it did. Uniform feasibility forces lambda_sep=0 and 0<=lambda_machine<=1. The rational certificate (0,0,0,0,0,0,1) satisfies every actual physical transition and has initial potential exactly 1. At a fixed k any feasible nonnegative weights produce initial potential at most 1. Completed goals have Phi=0.

This is a **mandatory exact tariff falsifier of this specific terminal-masked source-static rank coordinate**. It does not disprove dynamic, machine-history-dependent rank/fusion components that discharge gradually through genuinely charged operations. In particular, one must not give the parser or Gaussian/NAE quotient a fictitious zero physical cost.

The fully charged recognizer of Theorem 042.3 independently gives an O(poly(L_k)) genuine SAT execution. Therefore even replacing the terminal mask by a hypothetical smoother dynamic coordinate cannot establish a positive fixed-coefficient exponential *initial* lower bound on this same family while preserving all legal executions. Any such claim must retain the genuine paid witness path and has a missing or violated tariff row.

The separate R_leaf typed record calculus of TMR-2/041 and TMR-4/042 has no PEEL execution on R_k, since K(E)=E. Its absence of a typed completed proof record is **not** an SAT lower bound. No model-changing bridge or all-machine implication is inferred.

The machine-readable exact symbolic tariff is:
results/raw/tmr/2026-11-15_0312_TMR2_NAE2CORE087_TERMINAL_TARIFF.json.

## 6. Mandatory hostile-control ledger

- **Affine/Tseitin/Gaussian and 2-SAT:** each signed twin is a two-variable XOR or equivalence constraint after elimination of its local z. Thus large rank of the X/Y relation coexists with a compact affine description; Gaussian or Krom/SCC is a permitted cheap route. The full relation is nonetheless non-affine/non-bijunctive.
- **Horn/dual-Horn:** the full relation fails the closure tests, but class failure does not obstruct a polynomial *family-specific* recognizer.
- **Treewidth and 2-core:** primal width >=k-1 and K(E)=E, yet SAT is polynomial for the family. Bounded-width DP is not used or asserted.
- **Autarky, local learning, source extensions:** the explicit full witness is a total satisfying autarky. Signed pair cancellation and independent guarded extension eliminate all decision obligations without leaf PEEL; u/a/b are real source variables, not free oracle values.
- **Equality/union-find:** each signed y_i is determined by its x_i; propagate this inexpensive relation before counting interface distinctions.
- **Compact circuits, sharing, caching, recomputation and input rereads:** one O(k^2) generator/evaluator and one verified witness serve all blocks, and the charged recognizer is polynomial. No prescribed DAG or rectangle materialization is forced.
- **Padding, permutations, gauge flips, malformed input:** exact duplicate clauses are deduplicated; renaming/order/gauge invariance and missing-companion negatives were tested. Full source verification and exact fallback prevent false SAT or UNSAT classification.

Historical /341 remains FAIL as a full logical UNSAT authority and /386 remains RESTRICTED; neither is used as a checker.

## 7. Reproducible tests, literature, and provenance

The **exact published V8 audit() source function** was executed in the tool-hosted native V8 runtime, then fetched and independently re-evaluated from its Git blob. It passed **3,102 assertions, zero failures**: k=2..10 degree/leaf/primal source checks, all explicit X witnesses through 64 masks per k, 270 seeded complete-variable gauge/renaming controls, deliberate missing-clause corruption, exact 0/1 permutation-matrix entries and BigInt exact integer determinants for k=2..4. Deterministic seed 20261115. This verifies finite cases only. No standalone Node OS execution or compiled physical multitape simulator has been performed. The unbounded statements above rely on the symbolic proofs and finite-loop recognizer argument, not on these finite tests.

- Report: research/agents/tmr-2/2026-11-15_0312_TMR2_NAE_2CORE_RANK_GAUGE_FIREWALL042.md
- Executed source: experiments/tmr/tmr2_nae_2core_gauge087.js
- Native raw JSON: results/raw/tmr/2026-11-15_0312_TMR2_NAE2CORE087_V8_RAW.json
- Exact symbolic seven-column matrix: results/raw/tmr/2026-11-15_0312_TMR2_NAE2CORE087_TERMINAL_TARIFF.json

Primary external context checked: T. J. Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978, pp. 216-226, https://doi.org/10.1145/800133.804350. Schaefer's four relation-closure classes are background; the family construction is proved directly here. Project primary corpus: TMR-2/040, TMR-2/041, TMR-3/041, TMR-4/042, TMR-1/041, TMR-5/038 and their code/raw/handoffs, plus LEAD-0029 Lipschitz audit, November 13 and 14 directives, issue #3, AGENTS/CODEX/skill. The canonical leaf-core theorem is accepted at its restricted record-calculus scope and is *not* contradicted by the present nonpeelable example.

**Tracker and ownership audit:** proof1.txt fully recovered (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt fully recovered via Git blob (SHA 930c5eeddafce656717f28055a7a9a755f44737c), canonical root main.tex fully recovered via Git blob (SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34). No status promotion or TMR-5-owned root manuscript edit justified. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No existing agent title, schedule or enabled state modified.

**Peer repair:** TMR-3 audit a finite-tape source canonicalizer and the polynomial exponent under arbitrary gauge transformations. TMR-4 add a legal source-authenticated recognition+verified-witness MAY branch and test any proposed dynamic separator row. TMR-5 independently replay signed twins and rank under source renaming, and seek a compact UNSAT or alternate-encoding shortcut. TMR-1 retain the same-system transfer gate as OPEN. The next TMR-2 target remains a **dynamic, syntax- and history-aware interface obstruction** surviving the signed-twin and guarded-extension quotients; neither the initial superpolynomial gap nor the all-SAT-machine transfer is currently established. P versus NP remains OPEN.
