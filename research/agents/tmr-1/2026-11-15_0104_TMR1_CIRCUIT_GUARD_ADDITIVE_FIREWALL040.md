# TMR-1/040: CIRCUIT-GUARD075, additive-size circuit interpolation firewall

**2026-11-15 01:04 PST (America/Los_Angeles); PNP Machine Model Lead.**
**Scientific status:** PROVED/RESTRICTED, symbolic theorem for ordinary shared-DAG Resolution, independent mathematical review OPEN. Executed finite tests are COMPUTATIONAL. The arbitrary fixed SAT-machine transfer, superpolynomial fusion-Lipschitz potential, and P versus NP remain OPEN.

## 1. Claim and preselected falsifiers

**Candidate:** The preceding TMR-1/039 and TMR-2/039 guard constructions multiply a hard private CNF $F$ by the number of separator-CNF clauses. A stronger, model-matched guard may share a compact **arbitrary Boolean circuit** twice, making the Resolution upper-bound overhead *additive*, not multiplicative, while preserving the hard private $F$ under restriction. This tests whether syntactic source hardness, large interfaces, many cofactors, or non-Schaefer separators force a hard actual interpolant.

Before proof and original-source search, test:

1. A circuit with reconvergent fanout destroys a claimed constant-cost gate-by-gate Resolution equivalence proof.
2. The proposed gate copies share private variables, or a source premise or pivot in the purported refutation is forged.
3. A restriction to a false separator input leaves auxiliary constraints, rather than exactly the original $F$, and invalidates inherited Resolution hardness.
4. A satisfiable private $F$ incorrectly yields an UNSAT instance; malformed/constant predicates are silently admitted to the both-sides-satisfiable assertion.

The qualified system is ordinary source-inclusive, shared-DAG binary Resolution with authenticated original clauses; count one for every derived Resolution inference. Original source premises are included in the formula but are not counted as Resolution inferences. **It is not a general SAT computation model or the historical /341 or /386 authority.**

## 2. Exact theorem

Let $F(U)$ be any finite unsatisfiable CNF, with all variables $U$ private and distinct from $X$. Let $P(X)$ be a nonconstant Boolean function represented by an explicitly given acyclic fan-in-at-most-two circuit $Q$ of $g\ge1$ AND/NOT gates and $k$ input variables. Arbitrary fanout and reconvergence are allowed. Write $E_A(X,Y_A)$ and $E_B(X,Y_B)$ for two independently authenticated standard Tseitin CNF encodings of the **same** $Q$, with disjoint private gate variables $Y_A,Y_B$ and output wires $o_A,o_B$. Each NOT gate uses two clauses; each AND gate three. Define

$$
A=E_A(X,Y_A)\wedge\bigwedge_{C\in F}(o_A\vee C),
\qquad
B=E_B(X,Y_B)\wedge\neg o_B,
\qquad
G=A\wedge B.
$$

There are exactly $k$ shared variables, namely $X$.

**Theorem CIRCUIT-GUARD075 (PROVED/RESTRICTED, peer review OPEN).**

1. Both $A$ and $B$ are individually satisfiable, $G$ is unsatisfiable, and the **unique Boolean Craig interpolant on $X$** is $P(X)$.
2. If $S_{\rm Res}(H)$ denotes the minimum number of native binary Resolution **inferences** in any shared-DAG refutation of unsatisfiable CNF $H$, then

$$
\boxed{
S_{\rm Res}(F)\ \le\ S_{\rm Res}(G)\
\le\ S_{\rm Res}(F)+8g+2.
}
$$

3. The source $G$ contains at most $|F|+6g+1$ clauses, in contrast to the cross-product of separator CNF clauses and private clauses in the earlier guarded lift. If $F$ has width at most three, $G$ has width at most four. For binary-indexed variables, with $F$ using $v$ variables and $m$ clauses, a fixed explicit encoding has length $O((m+g+1)(w_F+1)\log(v+k+g+2))$, where $w_F$ is the maximum clause width. For $w_F=3$ and bounded-width gates, this is $O((m+g)\log(v+k+g))$.

### Proof of the interpolant assertion

Tseitin definitions force their output bits to equal $P(x)$ on each fixed shared assignment $x$. If $P(x)=1$, the guards $(o_A\vee C)$ are tautologically satisfied, and $A$ has a satisfying extension. If $P(x)=0$, satisfying $A$ would satisfy the UNSAT $F$, which is impossible. Thus the projection $\exists U,Y_A\,A$ is exactly $P$. The projection $\exists Y_B\,B$ is exactly $\neg P$. A Boolean separator $I(X)$ with $A\models I$ and $B\models\neg I$ must agree with $P$ at every $x$ because these two projections exhaust all assignments. Since $P$ is nonconstant, both sides are individually satisfiable. Their conjunction is UNSAT.

### Proof of the lower Resolution inequality

Choose any $x_0$ for which $P(x_0)=0$. Restrict every shared input bit to $x_0$ and **both** private copies of every gate wire to its uniquely forced, correctly evaluated value. All clauses in $E_A,E_B$ become true, as does the unit $\neg o_B$. Every guarded original clause $(o_A\vee C)$ becomes exactly $C$. Nothing else remains: $\rho(G)=F$ on the untouched original private variables $U$. The standard restriction of any native Resolution refutation yields a refutation of $\rho(G)$ with no more Resolution inferences (remove satisfied lines and replace surviving lines by their restricted/subsuming predecessors). Therefore $S_{\rm Res}(F)\le S_{\rm Res}(G)$. This is a **source-preserving proof-system restriction**, not a simulation of an arbitrary deterministic SAT decider.

### Proof of the additive upper inequality

Take an arbitrary native Resolution refutation of $F$ with $s$ inferences. Replace every source clause $C$ by the actual authenticated guard source $(o_A\vee C)$, and carry the guard through each original pivot, without changing the DAG or its shared reuse. This derives the unit $o_A$ in exactly $s$ inferences.

For each gate of $Q$ in topological order, derive both implications
$(\neg y^A_j\vee y^B_j)$ and $(\neg y^B_j\vee y^A_j)$ using the original gate clauses of the two copies and the previously derived equivalences of its inputs:

- If the gate is NOT, at most two Resolution inferences per implication suffice. With identical shared input variables, only one is needed.
- If the gate is AND, first transport the two defining implications from the source-side gate to the target-side gate inputs, and resolve each into the target-side positive-output ternary clause. At most four inferences per direction suffice. Both input wires may be independently shared by many later gates; already derived equivalence clauses are **reused once**, not unfolded as trees.

Thus at most $8g$ Resolution inferences derive all gate-wire equivalences, including $(\neg o_A\vee o_B)$. Resolve that clause against the derived unit $o_A$ to get $o_B$, and against the authentic B-source unit $\neg o_B$ to obtain the empty clause. Total $s+8g+2$. Minimizing over all source refutations of $F$ proves the theorem. No unbounded arity, free oracle, or uninterpreted semantic equivalence step occurs. Actual physical serialization of this source-inclusive proof is a separate charged model.

## 3. Growing example and exact proof-system scope

Choose $F_H$ as the standard odd-charge cubic-expander Tseitin CNF on $H$ vertices, with four proper 3-clauses per vertex. The known Ben-Sasson-Wigderson width/size result for ordinary shared-DAG Resolution gives $S_{\rm Res}(F_H)=2^{\Omega(H)}$ for an appropriate bounded-degree expander sequence. Choose $P_H$ to be the comparison-and-exact-one function

$$
P_H(X,Y,Z)=[X=Y]\wedge[\operatorname{weight}(Z)=1]
$$

on $\Theta(H)$ common inputs, implemented by a uniform $g_H=O(H)$ AND/NOT circuit. This predicate is nonconstant, has many distinct local cofactors and is nonaffine and non-Schaefer, but is computed by only $O(H)$ gates. With explicit binary variable identifiers,

$$
L_H=\Theta(H\log H),\qquad
2^{\Omega(L_H/\log L_H)}
\le S_{\rm Res}(G_H)
\le S_{\rm Res}(F_H)+O(H).
$$

**Important:** The rightmost upper bound does NOT make the proof short; it says the added guard-circuit difficulty costs at most linear extra Resolution work on top of the already hard private source. Relative to the earlier CNF guard-cross-product construction, the new guarded source has only $O(H)$ clauses, not a quadratic or cubic count. Its separator nevertheless has a linear-size circuit. The hardness is inherited from $F_H$ after restriction, not from the interpolant.

The source is generally **4-CNF**, not claimed proper 3-CNF. An arbitrary 4-to-3-CNF reduction could introduce auxiliaries that invalidate this **native proof-size** lower bound; no such transfer is asserted. A correct uniform SAT machine can recognize a source-authenticated affine contradiction and/or a polynomially generated known-label family and then use exhaustive search elsewhere, so this example cannot furnish a universal runtime lower bound. The current program's same-system algorithm bridge remains OPEN.

## 4. Actual executed replay and falsification controls

The exact published V8 function was executed and later rerun from the fetched GitHub branch source after the final negative-control patch. The seeded test ranges over $k\in\{2,3,4\}$, one to five AND/NOT gates, seven fixed trials per gate count, and two authentic private UNSAT source refutations (all four binary 2-CNF sign clauses, and opposite unit clauses). Constant-output circuits are excluded from the individually-satisfiable assertion. Circuits are generated with fanout and reconvergence enabled. Every produced Resolution inference is independently replayed from its two actual earlier parents, signed pivot, and original source indices.

- **46,300 assertions, 194 nonconstant circuit/source cases, 7,348 total source-plus-derived lines, 3,372 derived Resolution lines, zero failures**.
- **48** cases exercise reused internal gate outputs. **8** candidate constant circuits were rejected by the nonconstancy precondition.
- **389** negative controls include invalid pivots, forged source clauses, and one authentic SAT-private-source assignment satisfying **both** sides, demonstrating that unsatisfiability of $F$ is essential.
- All tested shared assignments obey the exact $A$ and $B$ projections, gate-wire functionality and restriction $\rho(G)=F$; per-proof derived Resolution counts satisfy the symbolic $s+8g+2$ bound.

These are finite **COMPUTATIONAL** tests, not an asymptotic proof or a compiled multitape Turing machine. The theorem above is symbolic, with independent mathematical peer review pending. There was no randomized benchmark outside the deterministic seeded circuit generator.

**Executable:** $\texttt{experiments/tmr/tmr1_circuit_guard_additive075.js}$.

**Original raw result:** $\texttt{results/raw/tmr/2026-11-15_0104_TMR1_CIRCUIT_GUARD075_V8_RAW.json}$.

## 5. Prior work, literature and exact novelty

- Prior project baseline: $\texttt{research/agents/tmr-1/2026-11-15_0004_TMR1_EXACTONE_NON_SCHAEFER_GUARDLIFT039.md}$ proves the exact-one separator using $q=1+\binom{k}{2}$ CNF guards, $qS_{\rm Res}(F)+k^2$ upper bound. This run replaces those **$q$ replicated private guards** by one authenticated circuit-output guard, gives an **additive** $8g+2$ upper overhead, and reduces guarded source size to $|F|+O(g)$.
- $\texttt{research/agents/tmr-2/2026-11-15_0020_TMR2_EQUALJ_INTERPOLANT_COFACTOR_FIREWALL039.md}$ has an equality-plus-exact-one separator with many local cofactors and separate B-side gate authentication. The new theorem accommodates *any* AND/NOT circuit $P$ with two copied gate definitions and authentic shared-DAG proof of their equality. It is not a new claim about exponential cofactor counting.
- $\texttt{research/agents/tmr-5/2026-11-15_0052_TMR5_SHUFFLED_GAUSS_CORE_REDTEAM036.md}$ constructs a polynomial-time SAT-machine recognizer for affine contradiction cores. This is the mandatory hostile machine control, and it precludes promoting inherited Resolution hardness to unrestricted decision-time hardness.
- Project legacy guards: $\texttt{research/agents/lead/2026-10-07_0855_LEAD-0029_LIPSCHITZ_SQUEEZE_AUDIT.md}$, root $\texttt{proof1.txt}$ and $\texttt{proof2.txt}$, canonical $\texttt{main.tex}$, and the five current TMR handoffs. Historical /341 is **FAIL** on its full accepted language; /386 is **RESTRICTED**.
- Primary published restricted anchor: Eli Ben-Sasson and Avi Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2):149-169 (2001), DOI 10.1145/375827.375835, ECCC TR99-022 (1999), https://eccc.weizmann.ac.il/report/1999/022/. This theorem concerns ordinary Resolution width/size on suitable expanders, **not arbitrary SAT deciders**. The original page-specific theorem was inspected in TMR-1/039; this run checked the original ECCC report page and the journal metadata, not a new PDF screenshot.
- Interpolation background only: Jan Krajíček, *Interpolation Theorems, Lower Bounds for Proof Systems, and Independence Results for Bounded Arithmetic*, JSL 62(2) (1997), https://doi.org/10.2307/2275541. The new unique-interpolant and additive-lift claims are directly proved here rather than imported from that paper.

## 6. Tariff and dependency consequences

For the native shared-DAG Resolution transition system, each original clause is authenticated and all binary RES steps are paid once, including reconstructed gate-equivalence work. Every legal alternate proof remains allowed. The additive construction provides a genuine complete proof path of cost $S_{\rm Res}(F)+O(g)$ in this qualified system. Therefore any all-step terminal-zero tariff $\Phi_R$ for this **same system** must satisfy

$$
\Phi_R(C_0(G))\le S_{\rm Res}(G)
\le S_{\rm Res}(F)+8g+2.
$$

This does **not** show $\Phi_R(C_0(G))$ is small when $F$ is Resolution-hard, and it does **not** falsify Resolution's known exponential lower bound. It shows the interpolant/circuit component itself cannot be assigned an independent large lower-bound price merely because the source proof is hard. The source-to-interpolant extraction arrow is directionally an **upper** bound on circuit complexity in terms of refutation work, not a reverse implication from a hard refutation to a hard interpolant.

**Dependency verdicts:** unique circuit interpolant, shared-DAG additive guarded Resolution lift and source restriction: PROVED/RESTRICTED, independent review OPEN. Ordinary Resolution expander-Tseitin lower bound: KNOWN THEOREM at its exact model. Tractable compact separator: PROVED/RESTRICTED. All-step seven-component tariff on arbitrary SAT machines: OPEN. Fusion-safe superpolynomial machine initial gap: OPEN. Same-system bridge from every correct SAT machine into this restricted proof system: OPEN/FALSIFIED for naive cost-preserving native Resolution transport by prior TMR-1/036. P versus NP OPEN.

**Peers:** TMR-2 independently audit whether any proposed separator component survives this duplicated-circuit shortcut; TMR-3 charge the actual bit-level gate/source serialization and comparisons; TMR-4 add both gate-copy proof routes as real MAY paths and check the rule-by-component tariff; TMR-5 independently check restriction, all intermediate equality clauses, the additive $8g+2$ bound, and the UNSAT precondition.

**Next weakest lemma:** identify a source-and-machine-state-specific fusion obstruction for a genuinely nonaffine family that stays positive after both compact circuit gate-copy shortcuts and authentic Gaussian elimination, without relying on hard *proof* syntax alone. The current example is a falsification control, not that missing positive lemma.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full proof1 fetched, authentic full proof2 and main.tex recovered via Git blob SHAs (contents API blank is not empty), issue #3 and all TMR handoffs checked. No root tracker, root main.tex, historical checker, or scheduled task was edited.
