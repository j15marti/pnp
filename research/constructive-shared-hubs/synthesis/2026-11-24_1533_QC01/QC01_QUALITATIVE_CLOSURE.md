# QC01: Exact guarded activation–repair closure and the remaining universal selection problem

24 November 2026, Pacific time. Constructive proof continuation for `j15marti/pnp`, issue #327.

**Status:** PROVED/EXACT at the explicitly stated affine selector layer; FALSIFIED rank-only guard-accumulation lemma; COMPUTATIONAL finite controls; universal polynomial closure OPEN. Independent review requested. No P=NP or P!=NP claim. No new agents or scheduler changes.

## 1. Outcome and exact target

The proposed qualitative route can be made exact: for every activation word, either its repair system has an explicit Boolean lift, or Gaussian elimination produces a guarded parity obstruction. All such obstructions together characterize the feasible activation relation exactly. This closes a correctness/completeness step of the representation.

It does not close the uniform algorithm. A new obstruction need not add an independent syndrome direction. On a connected infinite family, linearly many syndrome coordinates generate exponentially many individually necessary, linearly independent *guard functions*. The family is nevertheless easy through a compact reachability representation. Therefore this result refutes a particular rank-only progress argument, not polynomial-time solvability.

There is a second, exact scope check: arbitrary 3-SAT compiles to rank-one local repair blocks glued by affine activation equalities. The local blocks have complete constant-size descriptions, but selecting one globally compatible activation is precisely the original satisfiability problem. Thus the current gap is a substantive global algorithm theorem, not just a missing final sentence or a minor estimate.

Named candidate tested, **RANK-GUARD-CLOSURE**: after certified forced-information closure, every necessary new activation obstruction contributes a linearly independent syndrome functional, so a syndrome rank bound bounds the total necessary guard work. This candidate is false in the boundary relation domain below.

Falsifiers examined: linear dependence of certificate directions without logical implication of their guarded constraints; loss of a conditional guard during feedback; cheap local repairs with incompatible shared activation choices; exponential explicit obstruction lists despite an easy exact compact representation. All four are addressed by exact constructions, not inferred from finite tests.

## 2. Model, quantifiers and source semantics

All vector arithmetic in Sections 2–7 is over GF(2). Input consists of explicit vectors c_i,d_i,t in GF(2)^q, i=1,...,m. Its complete encoded length N includes these vectors, source identities, affine constants, retained guards and reconstruction maps. Consider

\[
\sum_{i=1}^m c_i a_i+\sum_{i=1}^m d_i a_i b_i=t,
\qquad a_i,b_i\in\{0,1\}. \tag{1}
\]

This is the exact selector form of an affine system on punctured pairs. Given source columns p_i,q_i and target s with every (u_i,v_i) different from (0,0), set

\[
(u_i,v_i)=(a_i,1+a_i+a_i b_i),\quad
c_i=p_i+q_i,\quad d_i=q_i,\quad t=s+\sum_iq_i.
\]

The map reaches exactly (0,1),(1,0),(1,1). Conversely, take a_i=u_i; when u_i=1 take b_i=v_i, and when u_i=0 choose b_i=0. Substitution proves both SAT directions. A source witness is reconstructed and checked in polynomial time. This is an existential surjection, not a model-count-preserving bijection: the two b_i choices coincide when a_i=0.

The theorem below quantifies over every explicitly encoded c,d,t. It is not automatically a physical E4/B4 compiler theorem. For a narrower signed tetrahedral network promise, a source-authenticated adapter must establish that promise and charge its construction. Neither low port count nor a drawing on a surface supplies that adapter by itself.

## 3. QC01-A: exact guarded dual characterization (PROVED)

For an activation a, write

\[
J(a)=\{i:a_i=1\},\quad W(a)=\operatorname{span}\{d_i:i\in J(a)\},\quad
r(a)=t+\sum_i c_i a_i.
\]

For a dual vector lambda in GF(2)^q define

\[
S_\lambda=\{i:\lambda\cdot d_i=1\},
\]

and the guarded constraint

\[
G_\lambda(a):\quad
\left(\bigvee_{i\in S_\lambda}a_i\right)
\ \lor\ 
\left[\sum_i(\lambda\cdot c_i)a_i=\lambda\cdot t\right]. \tag{2}
\]

**Theorem.** For every explicit c,d,t and every activation a, the following are equivalent:

1. There exists b satisfying (1).
2. r(a) belongs to W(a).
3. Every G_lambda(a) holds.

**Proof.** With a fixed, equation (1) is a linear system in its active b_i, so the first two statements are equivalent. If a satisfies (1) and all activations in S_lambda are zero, apply lambda to (1): every repair contribution vanishes, so the displayed parity equation holds. Hence every G_lambda holds.

Conversely, if r(a) is outside W(a), elementary linear algebra provides lambda annihilating W(a) with lambda dot r(a)=1. All a_i with lambda dot d_i=1 are then zero, while the required parity is false. This violates G_lambda. Such lambda is computed by solving the linear equations lambda dot d_i=0 for active i and lambda dot r(a)=1. This is a polynomial-time rejection certificate for this activation. QED.

The complete system is an unconditional identity

\[
\exists b\;(1)\ \Longleftrightarrow\ \bigwedge_{\lambda\in\mathbb F_2^q}G_\lambda(a). \tag{3}
\]

The parity equation *inside* each G_lambda is conditional. It may be exported as an unconditional equation only when the guard a_i=0 for every i in S_lambda is already certified in the current protected source context.

Equivalently, in the Boolean polynomial ring on activation variables,

\[
h_\lambda(a)=\left(\lambda\cdot t+\sum_i(\lambda\cdot c_i)a_i\right)
\prod_{i\in S_\lambda}(1+a_i)=0. \tag{4}
\]

There is no general linearity law h_(lambda+mu)=h_lambda+h_mu. The multiplication by different guards is essential.

This theorem gives polynomial-time testing and repair of a *specified* activation. It does not give polynomial-time search for a feasible activation, or an efficiently decidable description of all activation choices after arbitrary further gluing.

## 4. QC01-B: exact track-switch and gauge invariance (PROVED)

Switch the local repair convention by b_i'=b_i+epsilon_i. Then c_i'=c_i+epsilon_i d_i and d_i'=d_i. The guarded Boolean function in (4) is unchanged. Its difference is

\[
\left(\sum_i\epsilon_i(\lambda\cdot d_i)a_i\right)
\prod_{i\in S_\lambda}(1+a_i)=0,
\]

because every summand has a_i(1+a_i)=0. Thus exchanging these repair tracks is an exact representation change; it does not remove an incompatible activation.

For any supplied invertible syndrome transformation T, replace c_i,d_i,t by Tc_i,Td_i,Tt and lambda by T^{-T}lambda. Every dot product in (2) stays the same, so the guard family is merely reindexed. Gaussian construction and verification of T are charged.

This does not say all adaptive topological or nonlinear transformations are useless. It says these two explicitly defined reversible operations preserve the exact obstruction relation. A Möbius/Klein drawing or double cover would need a separately proved operation with a paid simplification benefit. No claim is made that every possible topology change is a gauge transformation.

## 5. QC01-C: a connected infinite counterfamily to rank-only guard accumulation (PROVED)

For each k>=1 take the graph with terminals s,t and internally disjoint paths s-w_i-t, i=1,...,k. Let alpha_i,beta_i activate the two edges of path i. Use its binary vertex-edge incidence columns for d, put c=0, and target t_vec=e_s+e_t. There are 2k activation variables, k+2 vertex coordinates and repair rank k+1.

**Exact feasible boundary relation.** An activated edge set admits a repair iff s and t are connected. Necessity follows because the sum of an incidence vector on each connected component is even; sufficiency follows by selecting a path. Here the relation is exactly

\[
R_k(\alpha,\beta)=\bigvee_{i=1}^k(\alpha_i\land\beta_i). \tag{5}
\]

It has a binary circuit with k AND gates and k-1 OR gates. A witness is found by a linear scan, and the repair uses the two edges of one full path. The source itself has linear graph size. This is an easy family.

**All minimal dual cut guards.** A cut separating s from t puts each w_i on either side. The cut therefore contains exactly one edge from every path. Equation (2) becomes

\[
\bigvee_{i=1}^k \gamma_i,
\qquad \gamma_i\in\{\alpha_i,\beta_i\}. \tag{6}
\]

There are 2^k distinct such guards. All their certificate directions lie in a space of dimension k+1, after the constant vertex functional is quotiented out.

**Each guard is necessary in this cut-guard conjunction.** Fix one choice of gamma. Set precisely those k selected edge variables to zero and their k partners to one. There is no full path, so the activation is infeasible. It violates its selected cut guard. Any different cut selects a partner variable somewhere, which is one, and hence its guard is satisfied. Deleting this one guard from the conjunction changes the boundary relation. This proof works for every k and every cut.

The same assignment has an immediate SAT neighbor: change any one of its zero variables to one. One path becomes full. Fully pinned UNSAT/SAT neighbors are decided by Gaussian repair; they are not claimed to survive all available terminals.

**Linear independence of the guard functions.** The failure indicator of the guard in (6) is

\[
h_\gamma=\prod_{i=1}^k(1+\gamma_i).
\]

Its degree-k monomial is the product of its selected variables and occurs in no other h_gamma. The 2^k failure indicators are therefore linearly independent as Boolean functions, although the syndrome directions span only k+1 dimensions. This directly falsifies RANK-GUARD-CLOSURE.

**Concrete basis failure, k=3.** The four cut directions corresponding to choices
alpha_1 alpha_2 alpha_3;
beta_1 alpha_2 alpha_3;
alpha_1 beta_2 alpha_3;
alpha_1 alpha_2 beta_3
span the full relevant dual space. The activation
(alpha_1,beta_1,alpha_2,beta_2,alpha_3,beta_3)=(1,0,1,0,0,1)
satisfies all four clauses. It fails the omitted clause beta_1 OR beta_2 OR alpha_3 and has no full path. The omitted certificate direction is the XOR of three of the listed directions. Directional linear dependence has not supplied logical implication of the guarded clause.

**No hidden low-degree unconditional activation equation.** Let z_i=1+alpha_i and w_i=1+beta_i. A multilinear polynomial f vanishes on every feasible activation iff it vanishes whenever z_i=w_i=0, for each i. Setting that pair to zero removes only monomials containing z_i or w_i. Uniqueness of multilinear Boolean representation forces every surviving monomial of f to contain at least one variable from each pair. Consequently every nonzero such polynomial has degree at least k. Translation preserves degree. At degree exactly k the vanishing space has dimension exactly 2^k, with the products above as basis.

Thus for k>=2 the feasible relation has full affine hull and no forced activation bit. Complete closure *within activation equations of degree below k* gives no information, even if that particular restricted closure were acquired for free. This is a theorem about the projected boundary representation. It is not a lower bound for full-source reasoning with repair variables, auxiliary definitions, reachability, or another representation. The compact expression (5) is the explicit escape.

The graph is planar and series-parallel. If a graph-degree-three realization is desired, replace each high-degree terminal by a binary tree of permanently active edges. Contracting those edges recovers the same boundary relation, and the total size remains O(k). This graph construction does not claim an unproved strict signed E4/B4 physical gadget.

**Scope of the falsification.** An explicit registry of these individual cut guards has Theta(k 2^k) literal occurrences and can be forced to distinguish all 2^k critical boundary queries. This is not a lower bound for decision: a compact circuit or a connectivity procedure answers them cheaply. The family is not a candidate simultaneous hard sequence for a portfolio that includes that procedure.

## 6. QC01-D: arbitrary 3-SAT already occurs with rank-one local repair (PROVED)

Let F be any explicit strict 3-CNF with M clauses and L=3M occurrences. Create an activation a_o and repair bit b_o for each occurrence o. For a positive occurrence of x_v set a_o=x_v; for a negative occurrence set a_o=1+x_v. Eliminate explicit x_v by chaining successive occurrences of each variable with affine equations

\[
a_o+a_{o'}=\operatorname{neg}(o)+\operatorname{neg}(o'). \tag{7}
\]

The copy chain is consistent and has exactly one free bit per used source variable. Each activation appears in at most two such binary copy equations. Signs are retained exactly.

For each clause j impose

\[
\sum_{o\in j}a_ob_o=1. \tag{8}
\]

All three d_o of that clause are the same unit vector e_j in its repair-coordinate block. Different clause repair blocks are independent. Put the copy rows (7) in C, zero D in those rows, and their affine right-hand sides in t. Put zero C, the unit D columns and RHS 1 in the clause rows. This is exactly (1).

**Forward direction.** Given a satisfying source assignment, set its literal activations. In each clause choose one true occurrence, set its b_o=1 and the other repair bits to zero. Equations (7)–(8) hold.

**Reverse direction.** Equation (7) reconstructs a consistent value of every used source variable. Equation (8) requires at least one activated literal in every clause. Therefore the reconstructed source assignment satisfies F. Unused source variables may be set arbitrarily. No counting preservation is asserted.

Construction, discovery of the copy chains, reconstruction and verification take polynomial bit time. The sparse representation has O(L) nonzero entries and O(L) equations; a dense bit matrix is still polynomial size. Every isolated clause repair block has rank one and a constant-size local truth table.

Since ordinary 3-SAT is NP-complete [1], general activation selection is NP-complete, including this rank-one-block subclass. This is a direct reduction with both directions, not an inference that it needs superpolynomial time. A uniform polynomial global gluing method for this subclass would prove P=NP and is exactly what remains to be constructed.

**Local feasibility does not imply global feasibility.** Take all eight signed clauses on three variables, one forbidding each of the eight assignments. Every isolated local block is feasible, the copy chart is affine and consistent, and no source literal is forced by the implemented elementary closure. The conjunction is UNSAT. Deleting any clause gives a SAT neighbor. This finite example refutes only the local-to-global inference. It is not difficult for the complete cooperative portfolio.

This result agrees with the direction of GD14's separate guarded-nonreach reduction, but here the reduction stays in the activation–repair representation of the current proof attempt. It also explains why replacing a large block by many easy wheel or hub blocks does not complete the argument unless their shared guards can be composed efficiently.

## 7. Certified closure and what was actually executed

The checker implements a declared, incomplete polynomial closure repertoire. It first projects the target equation away from all not-forced-zero repair columns and adds the resulting unconditional affine activation equations. Gaussian elimination detects inconsistency and certifies forced activation coordinates. Coordinate dual guards and any supplied learned dual guards are retained. A guarded parity is added only when all its repair-enabling activations are certified zero; a final remaining enabling activation is forced to one only when the parity alternative is certified false. Every deduction immediately restarts closure. Stagnation returns UNKNOWN.

Protected branch pins remain part of the input context. The checker applies closure before reference enumeration, after every deduction, to a fixed point at stagnation, and on both fully pinned neighboring inputs. It does not silently invoke complete semantic closure, a SAT oracle or every peer's terminal. In particular, older collective quadratic reasoning can refute the small Fano root; its elementary closure stagnation here is not a claim that the whole portfolio stalls there.

### Executed controls

Complete standard-library script: `QC01_check.py`. Seeds 202611241515 and 202611241516. All stages exited successfully. Each saved raw stage records the same script SHA-256:

`00765a91b9479cf0c0936e0fb2fa5e85c3f20afd605850acf347ef079c278f45`

| Stage | Executed scope | Result |
|---|---|---|
| Generic selectors | All q=1 systems with m=1,2,3 and both targets, plus 240 seeded systems with m<=7,q<=6 | 408 instances: 351 SAT, 57 UNSAT |
| Fixed activations | Exhaustive repair-bit control, Gaussian repair and all dual guards on 10,264 activations | 5,262 repairable, 5,002 rejected; zero discrepancies |
| Track switches | Every dual guard at every tested activation before/after a seeded local b-bit switch | Exact Boolean agreement; no gauge-basis test was separately executed |
| Previous repair-basis terminal | Independent-basis enumeration compared against all activations of every generic instance | 408 agreements, every returned source lift checked |
| Connected cut family | k=1 through 8; all activation words for k<=6 | 5,460 complete activation checks; 256 essential guards at k=8 with repair rank 9 |
| Neighbor pairs | Every minimal cut's unique rejecting activation and one-bit satisfying neighbor, k=1 through 8 | 510 UNSAT and 510 SAT pinned controls; every SAT lift checked |
| Consequence degree | Evaluation-matrix rank for degrees k-1 and k, k=1 through 4 | No nonzero degree<k equation; degree-k vanishing dimension 2^k |
| Exact 3-CNF compiler | All 256 subformulas of the 8-clause cube; Fano root, 14 single-clause and 7 whole-NAE deletions; 120 seeded formulas | 398 source instances: 371 SAT, 27 UNSAT |
| Source assignments and reverse maps | 8,808 assignments of the compiler inputs | 1,973 verified satisfying source lifts; no label or reconstruction discrepancies |

Total assertions: **313,760**. The assertion count is an execution ledger, not evidence of an asymptotic theorem. The infinite-family claims in Section 5 follow from the symbolic proof, not an extrapolation of the tested k values.

Fano root has zero models; each single-clause neighbor has five; each whole-NAE deletion has ten. The elementary compiler closure reports UNKNOWN on all 398 inputs, including the 27 UNSAT cases. This is expected and explicitly recorded, not an omitted failure. The reference enumerator supplies the finite controls; no polynomial decision claim is made for it.

Observed stage elapsed times in this environment: generic 0.240 s; cuts 0.157 s; compiler 28.175 s. Process high-water RSS: approximately 12.6–12.9 MiB (Linux ru_maxrss). These are runtime observations for the controls, not theoretical bounds or a measured cumulative-memory trace.

## 8. Paid resource ledger and conditional universal theorem

Parsing and source compilation operate on the complete encoded input. Gaussian tests, certificate construction and source lifts for a fixed activation have polynomial bit cost. The supplied guard registry costs O(m+q) bits per direction/constraint, plus its authentication and consumers. No exponential truth table is acquired for free.

The complete list of all dual directions can cost 2^q polynomial-sized jobs. The prior independent-repair-basis algorithm costs

\[
\operatorname{poly}(N)\sum_{j=0}^{r}\binom mj,
\qquad r=\operatorname{rank}\{d_i\}.
\]

This is polynomial for each fixed r, generally XP, not a polynomial theorem for r=O(log N). The experiments verify it only on the stated finite inputs. In the cut family, a direct compact terminal avoids this enumeration entirely.

For J actually acquired guard jobs, the implemented closure and exact fixed-activation checks have polynomial work per job and polynomial storage per retained authenticated guard. Time, peak storage and cumulative memory must refer to the same schedule. With serial live storage S and total charged steps T, the generic bound CM<=(T+1)S is available; cumulative memory was not measured here. Parallel tracks change span, not the sum of their work or aggregate live memory.

For a shared DAG, retain complete source IDs, chart, target and guard in the key. Charge node creation, each attempted edge/consumer, canonicalization, cancellation, failed discoveries, rebuilds and reconstruction. A final small expression does not bound intermediate growth or the cost of constructing or deciding it.

The conditional universal theorem remains valid: suppose a uniform deterministic source-authenticated routine, for every residual, either finishes in a polynomially paid terminal or returns exact children R_i with a polynomially bounded numerical potential mu>=1 and fixed c>0 satisfying

\[
\sum_i\mu(R_i)^c\le\mu(R)^c-1.
\]

Include every node's acquisition, closure, discovery, representation, edge, aggregation and lift costs in a fixed polynomial in original N. Then telescoping bounds all paid nodes by mu(root)^c, yielding a polynomial-time 3-SAT decider. A DAG implementation may save work but must still account for every context and consumer. Polynomial bit length of mu is insufficient: its numerical value must be polynomially bounded.

QC01 supplies neither the universal routine nor its potential. It specifically shows why the dimension of the learned *syndrome directions* cannot alone certify the required progress of a guarded obstruction registry. It does not exclude another potential or an alternate terminal.

### Diagonal quantifiers

If a fixed total exact cooperative portfolio A has no uniform polynomial time bound, then for every j one can choose a larger input F_j with T_A(F_j)>|F_j|^j. Otherwise a fixed exponent would bound all sufficiently large inputs and finitely many exceptions could be absorbed into a constant. Under a fair polynomial-overhead schedule this sequence eventually escapes each fixed implemented polynomial terminal with its paid source adapter.

This quantifies over one A, not every possible algorithm. The cut family has a linear-size constructive terminal and is not asserted to belong to this sequence. The rank-one source compiler authenticates a remaining selection problem but supplies no simultaneous hard family. No structural contradiction to the diagonal assumption was obtained.

### Scientific gates

| Gate | Status and scope |
|---|---|
| Both-label / disjointness sanity | PASS for the stated exact transformations and executed SAT/UNSAT controls; no communication lower bound imported |
| Simultaneous time/space | PASS restricted to the explicit algorithms and stated ledger; universal polynomial bound OPEN |
| Deterministic configuration counting | Not used as a lower bound or as a polynomial termination proof |
| Relativization | No nonrelativizing separation or oracle-based closure asserted; unrestricted claim remains OPEN |
| Natural Proofs / algebrization | No inference from these barriers and no unrestricted circuit lower bound |
| Representation domain | Activation boundary, explicit affine selector and graph-incidence models kept separate from strict physical E4/B4 networks |
| Closure | Scoped certified repertoire, with guards retained; full semantic closure and the full peer portfolio not assumed free |

## 9. Peer integration and the next necessary theorem

Sources were recovered through the GitHub connector: current AGENTS.md, CODEX.md, research skill, issue #327 and 170 comments, current coordination excerpts, and original DO09, DP09, DS08, GD14 and BS08 reports. Earlier DO01/DP01/S06 are available in the same-session audited source files; their prior scope is retained. There is no full local checkout, so repository preflight was not run. This continuation has no assigned TMR manuscript and publishes an additive synthesis report, preserving peer manuscripts and existing artifacts.

**GD14:** rank/nullity controls a particular sparse witness search under its stated graph predicate. QC01 makes the guard nonlinearity explicit in the selector model. Do not replace all guarded directions by an ordinary linear basis without a logical implication certificate.

**DP09:** its sharp branch-credit law already distinguishes nominal rank from aggregate capacity. QC01 adds a connected family with exponentially many essential boundary guards and no low-degree unconditional activation equation, while explicitly retaining the cheap compact escape. Neither result licenses a generic exponential runtime claim.

**DS08:** its exact syndrome-tree messages remain useful. The cut relation can be kept compact and queried through its graph. What still needs control is a common representation after affine copy gluing and additional guarded consumers, not each local region's width in isolation.

**BS08:** its all-exterior-fibers Hall certificate proves a real existential deletion, with exact reverse maps, on the certified domain. That is stronger progress than exporting a conditional parity. Nothing here proves that every residual admits such a deletion or that its fallback count is polynomial.

**DO09:** the report states a simultaneous obstruction to several *raw-registry* rank/width parameters. Those claims are not used as a universal lower bound here, and the entire probabilistic family proof was not independently formalized in this iteration. QC01 addresses a different missing implication: even a small syndrome ambient space does not by itself bound guarded closure work.

**Next necessary theorem, PAID-GUARDED-ABSORPTION:** construct a uniform, source-authenticated procedure that absorbs a whole correlated obstruction family into a representation supporting exact joint composition and witness reconstruction, with polynomial total acquisition and query work, or produces children with the aggregate credit inequality above. It must cover the rank-one repair-block compilation of arbitrary 3-SAT, preserve arbitrary affine copy guards, and survive reconstruction and subsequent consumers. A compact existential circuit with an unimplemented emptiness query does not satisfy this theorem. The new connected cut family should be a positive regression test: its exponentially many flat guards should be absorbed without enumeration.

This is a concrete remaining algorithmic obligation. It is not a theorem proved by the existence of local witnesses, a finite number of vertex types, reversible switching, or qualitative eventual termination.

## 10. Fresh literature / official repository scan

Fresh task-specific search targeted Schaefer's Boolean constraint classification, exact SAT verification, affine guarded composition and official research repositories. Schaefer's original paper was opened and its NP-completeness baseline and dichotomy hypotheses inspected. The current reduction is self-contained; no broad tractability conclusion is imported from the paper.

Official-namespace repository reads were obtained for Anthropic `formal-math/eth/README.md`, OpenAI `math/README.md`, Google `or-tools/ortools/sat/README.md` and Google DeepMind `alphaproof-nexus-results/README.md`, with blob pins recorded in the sources manifest. The Anthropic README states a subexponential 3-SAT/counting claim; it is not a polynomial-time claim, and its Lean development was not built or independently verified here. OpenAI's README explicitly describes raw research artifacts at different verification stages. OR-Tools provides practical clause-learning/constraint solver infrastructure, not a universal polynomial bound. DeepMind's proof repository is relevant to verification practice; no result from it is imported into QC01.

Bounded searches also targeted `xai-org` and `google-research` for SAT/formal-verification methods. No applicable verified theorem was recovered from those searches. This is not a claim that none exists. No external repository code was executed or copied into the checker. No novelty or priority claim is made for standard linear algebra, cut duality, Boolean ideal facts, or the SAT reduction pattern.

### References

[1] Thomas J. Schaefer, *The complexity of satisfiability problems*, STOC 1978, pp. 216–226, DOI https://doi.org/10.1145/800133.804350. Original paper: https://www.khoury.northeastern.edu/home/lieber/courses/csg260/f06/materials/papers/max-sat/p216-schaefer.pdf.

[2] DP09, *Separator-local guard multiplexing and sharp branch-credit law*, 2026-11-24 14:45 PST. https://github.com/j15marti/pnp/blob/a2350413e55d56f83fc87d0120369d0ca3215fc8/research/hcl208/potential/2026-11-24_1445_DP09.md.

[3] DS08, *Joint cut/syndrome separator terminal*, 2026-11-24 14:25 PST. https://github.com/j15marti/pnp/blob/49c730e5d0d63fa4bb9177fb7ae608393c5f2400/research/hcl208/synthesis/2026-11-24_1425_DS08.md.

[4] GD14, *Sparse dual-syndrome guarded nonreachability*, 2026-11-24 14:00 PST. https://github.com/j15marti/pnp/blob/9fa163ea6c692ec479c38749226b73feef0d634c/research/hcl201/guarded-dag/2026-11-24_1400_GD14.md.

[5] BS08, *Weighted Hall-fiber elimination and exact wheel/matching cooperative solver*, 2026-11-24 14:50 PST. https://github.com/j15marti/pnp/blob/14fa557a95f8215bf185f263a2be71133d0e05a9/research/constructive-shared-hubs/solver/2026-11-24_1450_BS08.md.

[6] DO09, *Bounded-degree logarithmic-girth critical NAE cores with linear treewidth; sparse-background rank/width tradeoff*, 2026-11-24 14:55 PST. https://github.com/j15marti/pnp/blob/0c59cae322d25a6d3403c58ec7639ccf0967998c/research/hcl208/obstruction/2026-11-24_1455_DO09.md.
