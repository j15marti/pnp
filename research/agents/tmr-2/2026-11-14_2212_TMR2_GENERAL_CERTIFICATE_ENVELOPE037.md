# TMR-2/037: Universal certificate-envelope tariff for hidden-source Boolean functions

**2026-11-14 22:12 PST | GENCERT063 | PNP Information Necessity**

**Scientific status:** PROVED/RESTRICTED for the exact indexed hidden-source query model; independent mathematical peer review OPEN. Tests COMPUTATIONAL. Same-system unrestricted SAT transfer and a superpolynomial initial potential OPEN. **P versus NP OPEN.**

## 1. Candidate and preregistered falsifiers

**Candidate:** Generalize TMR-2/036, TMR-4/037 and TMR-5/033's AND-of-ORs fixed-source and MAY envelopes to *every* total Boolean function f on hidden source coordinates. Determine the pointwise greatest sound scalar potential and the exact three-component nonnegative tariff cone for cheapest compatible certificate B, minimax depth W and fixed-source certificate D_x.

Preselected falsifiers: (F1) a genuine one-price READ eliminates many minimax obligations; (F2) source-forgetting may accidentally grant adaptive oracle replies inconsistent with a fixed x; (F3) free affine, equality or a newly independently queryable compact parity hint defeats the selected interface; (F4) a hidden-source query result is falsely transferred to arbitrary syntax-aware SAT computation.

F1 occurs sharply for OR_n, F2 is avoided by a separate fixed-source graph and MAY graph, F3 remains a real changed-interface counterexample, and F4 remains OPEN.

## 2. Exact qualified system and definitions

Fix n>=1, a public total f:{0,1}^n -> {0,1}, one immutable hidden x in {0,1}^n, and a compatible partial observation transcript sigma in {?,0,1}^n. Add a redundant tag/cache-alias field. Zero-cost TAG toggles and transcript equivalence rewrites preserve the complete compatible-source set X_sigma and the identities of observable coordinates. Authentic unknown-coordinate READ(i) costs exactly 1 and returns the predetermined x_i. Repeated physical reads cost 1 and reveal no new fact. Free local Boolean reasoning is allowed **only in this query-cost laboratory**. The two terminal labels are legal if and only if f is constant on X_sigma. No public formula parsing, free lookup advice, parity-summary source or uncharged multi-coordinate READ is provided. An arbitrary public f might itself be an exponential-length table; its evaluation is not charged. This is not a full SAT machine.

Let U_sigma be the unobserved positions. For fixed compatible x, define the cheapest additional x-consistent completion certificate:

$$
D_x(\sigma)=\min\{|S|:S\subseteq U_\sigma,\ 
\forall y\in X_\sigma,\ 
[y|_S=x|_S\ \Longrightarrow\ f(y)=f(x)]\}.
$$

Define the cheapest compatible certificate B and optimal worst-case remaining online decision-tree depth W:

$$
B(\sigma)=\min_{x\in X_\sigma} D_x(\sigma),
$$

$$
W(\sigma)=
\begin{cases}
0,&f\text{ constant on }X_\sigma,\\
1+\min_{i\in U_\sigma}\max_{b\in\{0,1\}}W(\sigma[i\leftarrow b]),&\text{otherwise}.
\end{cases}
$$

Every valid goal has B=W=D_x=0. Zero-cost equivalent representations leave all three components unchanged. A genuinely different public source promise or newly queryable extension changes the system and requires recalibration.

## 3. GENCERT063-A: sharp scalar potential for every f

**Theorem (PROVED/RESTRICTED).** For every f, fixed x and compatible sigma, the pointwise greatest nonnegative potential h(f,x,sigma) respecting every zero-cost edge, each actual READ inequality h(C)<=1+h(C'), and h(goal)<=0 is exactly D_x(sigma). If h is source-oblivious and must respect both outcomes as MAY edges, the pointwise greatest is exactly B(sigma).

**Proof.** An actual read of unknown i changes D_x by either 0 or 1: any old certificate remains valid after the read, while prepending this read to a shortest new certificate yields D_x(sigma)<=1+D_x(sigma'). Hence D_x is admissible, nonnegative, zero at goals, and invariant under authenticated free tag/alias rewrites. For any admissible h, choose a genuine fixed-x path reading a shortest x-consistent certificate. This path has D_x(sigma) paid reads and finishes with the correct forced label, hence telescoping gives h(C)<=D_x(sigma). The **path selector may know x with hindsight**. It is a comparison for the lower-bound potential and NOT a single uniform online decision algorithm for all x.

For source-oblivious h the same inequality holds for every compatible x, hence h(sigma)<=B(sigma). Conversely for any possible READ successor sigma' choose compatible x minimizing D_x(sigma'). Then B(sigma)<=D_x(sigma)<=1+D_x(sigma')=1+B(sigma'), so B is sound for every MAY edge. QED.

In the notation of TMR-4/037's paid Bellman envelope with seed W, the generalized identities are

$$
\mathcal E_W^x(\sigma)=D_x(\sigma),\qquad
\mathcal E_W^{MAY}(\sigma)=B(\sigma).
$$

Indeed W(tau)>=D_x(tau) for each compatible fixed x and every transcript tau. An x-consistent path plus its terminal W=0 attains D_x, and minimizing over x attains B. Earlier TMR-5/033 proved this for the specific q-by-q AND-of-ORs function, not for all Boolean f.

## 4. GENCERT063-B: exact universal three-column tariff cone

Take correlated vector p=(B,W,D_x) and actual paid transition discharge Delta=p(C)-p(C'). **Across ALL total f on n source bits, ALL fixed compatible x and ALL legal transitions**, the exact cone of nonnegative weights is

$$
\boxed{\lambda_B+n\lambda_W+\lambda_D\le1,\quad
\lambda_B,\lambda_W,\lambda_D\ge0.}
$$

**Sufficiency:** Every real unknown-coordinate READ has Delta B<=1 and Delta D_x<=1 from the previous theorem. Also 0<=W<=n, so Delta W<=n, even if it decreases by a very large amount. Consequently lambda.Delta<=lambda_B+n lambda_W+lambda_D<=1. Every zero-cost alias has Delta=0, and all completed goals have zero potential.

**Necessity:** Choose f=OR_n, entirely unread sigma, and a fixed source x with the first bit 1. Initially (B,W,D_x)=(1,n,1). The genuine cost-one first-bit READ yields the completed TRUE goal (0,0,0), so Delta=(1,n,1). It forces the stated inequality. QED.

Exact rational saturating witness: lambda=(1/4,1/(2n),1/4). Its weighted discharge inequality was checked for every enumerated paid edge by multiplying both sides by 4n and using integer arithmetic.

For nonnegative weights independent of n, the full all-n cone forces lambda_W=0 and lambda_B+lambda_D<=1. At OR_n, the optimum initial potential equals 1 even though its minimax adaptive online decision-tree depth is n. On PARITY_n, B=D_x=W=n. Every such scalar potential is at most n initially, because a genuine n-read path always completes the public function. **Therefore no superpolynomial multiscale initial lower bound arises in this qualified source-query model alone.** This is a legal-path/tariff ceiling, not an entropy argument or a SAT runtime theorem.

## 5. Hostile controls, provenance and model limits

Affine PARITY4 has (W,B)=(4,4), public equality EQUAL4 has (2,2), Horn implication has (2,1), the public Krom two-clause example has (4,2), and disjoint AND-of-two-OR2 blocks have (4,2). All were checked by complete truth-table evaluation. MAJORITY4 and an XOR-extension *relation* over four coordinates were also exercised. The latter is a public Boolean relation, **not** a source-extension oracle.

A true new one-price READ_PARITY oracle for parity of n hidden independent source bits would discharge D_x=B=W=n on a single paid operation, invalidating the original tariff as soon as n>1. This is a real cheap path in the enlarged interface and must never be CEGAR-pruned. In the existing model free Gaussian manipulations of *known* source facts do not reveal unobserved independent coordinates. Public equality promises instead alter X_sigma and require a new quotient. Irrelevant/padded inputs, renaming, caching and shared views cannot create new independent certificate obligations. Actual Horn/2SAT preprocessing, bounded-treewidth separator DP, autarkies, learned clauses, compact circuits, real extensions, physical tape movement, input rereads and recomputation are not simulated here, and remain conservative MAY operations in any proposed SAT-machine transfer.

Historical checker /341 remains FAIL as full logical UNSAT authority; /386 remains RESTRICTED. Neither is modified or used.

## 6. Independent execution and exact evidence

Published byte-identical JS code was fetched from its GitHub feature branch and executed in a **native V8 isolate**. This was not a Node process, a compiled finite-state Turing machine, or native SAT execution. It exhaustively tested **all 256 three-input Boolean functions**, nine four-input public controls, **7,641 transcripts**, **18,688 fixed-source states** and **15,768 labeled authentic paid READ edges**. The independent certificate enumeration and Bellman recurrences agree in every case, with terminal and tariff checks. **179,821 exact/integer checks, zero failures**. The symbolic OR_n tariff frontier was additionally enumerated for n=1..25, but only the proof above establishes the all-n statement.

Files:
- experiments/tmr/tmr2_general_certificate_envelope063.js
- results/raw/tmr/2026-11-14_2212_TMR2_GENCERT063_V8_RAW.json
- results/raw/tmr/2026-11-14_2212_TMR2_GENCERT063_TARIFF_SCHEMA.json

**Novel within this project relative to TMR-2/036, TMR-4/037, TMR-5/033:** all-f generalization of the source-fixed and source-forgotten maximal scalar tariff, exact entire-class n-dependent *three-component* cone and OR_n sharp row, and explicit distinction of omniscient shortest certificates from uniform online decision trees. This is a formal extension of classical certificate complexity and the previous project Bellman theorem, not a claim of literature-wide novelty.

### Dependency status and next peer target

PROVED/RESTRICTED: source-fixed D_x and source-oblivious B all-step scalar potentials; exact all-n universal cone. COMPUTATIONAL: exhaustive small Boolean cases. FAIL: uniform positive unscaled W tariff across increasing n; importing an independently readable parity hint without rebalancing tariffs. OPEN: original-CNF syntax-aware dynamic component, arbitrary polynomial time/space Q-TM all-step simulation, true fusion-safe superpolynomial initial gap, same-system algorithm transfer, and P versus NP.

Next TMR-2: qualify one authentic original-CNF transition slice with full finite-alphabet source parsing, paid compact affine summaries and learning. Seek a source-aware residual relation across separators that is not just an online/omniscient query-depth gap. Peer requests: TMR-4 independently replay generic Bellman equality and exact n-cone; TMR-3 check physical correlated discharge; TMR-5 attack the OR witness and interface extension.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex is TMR-5-owned and unchanged. All five TMR schedules preserved. P versus NP OPEN.

## References

[1] Buhrman H, de Wolf R. Complexity measures and decision tree complexity: a survey. Theoretical Computer Science. 2002;288(1):21-43. https://doi.org/10.1016/S0304-3975(01)00144-X.

[2] Nisan N. CREW PRAMs and decision trees. STOC. 1989:327-335. https://doi.org/10.1145/73007.73038. SIAM J Comput. 1991;20(6):999-1007. https://doi.org/10.1137/0220062.

[3] Cousot P, Cousot R. Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints. POPL. 1977:238-252. https://doi.org/10.1145/512950.512973.
