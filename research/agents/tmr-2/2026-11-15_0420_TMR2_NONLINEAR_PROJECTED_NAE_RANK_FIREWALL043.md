# TMR-2/043: non-affine projected NAE rank survives the leaf and Gaussian tests, but not a polynomial witness

**2026-11-15 04:20 PST | NONLIN093 | PNP Information Necessity**

**Status:** PROVED/RESTRICTED symbolic construction and exact typed-record tariff, independent mathematical review OPEN. Executed finite V8 evidence COMPUTATIONAL. No unrestricted SAT-machine lower bound. P versus NP OPEN.

## 1. Candidate and four falsifiers fixed before corpus and primary-source search

Candidate: after TMR-2/042, perhaps replacing an affine projected anti-equality relation by a *non-affine*, no-leaf, non-Schaefer projected interface makes exponential rational matrix rank an unavoidable fusion cost.

Four falsifiers: (F1) a correct polynomial-time uniform witness recognizer even after gauge flips and variable renaming; (F2) a small disjoint nonlinear-factor representation or compact circuit after Gaussian quotient; (F3) one authentic terminal step that destroys a source-static terminal-masked rank at cost one; (F4) a genuine paid block check discharging an exponentially large rank component with one shared paid identity. All four defeat the stated proposed lower-bound interpretation. This does NOT falsify a different dynamic machine-history-aware obstruction.

Relevant originals reviewed: the governing 2026-11-14 fusion tariff directive; TMR-2/042's original full R_k construction and source/gauge verifier; TMR-4/042 canonical leaf-core theorem; TMR-5/039 independent original-source rank replay and batched-input tariff; TMR-1/043 dynamic connected-component fan-in-two tariff; TMR-3/042 and TMR-4/043 physical fused I/O tariffs; proof1.txt, proof2.txt, main.tex, AGENTS.md, CODEX.md, repo skill, all five current handoffs, current issue #3. Primary reference points: T. J. Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978, DOI https://doi.org/10.1145/800133.804350 ; E. Kushilevitz and N. Nisan, *Communication Complexity*, Cambridge University Press 1997, Ch. 1 (rectangles, fooling sets, rank), https://www.cambridge.org/core/books/communication-complexity/ . Neither primary source supplies the new family theorem, which is proved below.

## 2. Explicit proper 3-CNF family and encoding

Set k=3b>=3. Retain ALL variables and complementary three-literal NAE clauses of TMR-2/042's authenticated R_k. Write

$$
\operatorname{NAE}(a,b,c)=(a\lor b\lor c)\land(\neg a\lor\neg b\lor\neg c).
$$

The original source is

$$
R_k=\bigwedge_i[\operatorname{NAE}(x_i,y_i,z_i)\land\operatorname{NAE}(x_i,y_i,\neg z_i)]
\land\bigwedge_{i<j}[\operatorname{NAE}(x_i,x_j,u_{ij})
\land\operatorname{NAE}(u_{ij},a_{ij},b_{ij})
\land\operatorname{NAE}(x_i,a_{ij},b_{ij})].
$$

Define the NEW family, with one disjoint nonlinear high-variable triple per block,

$$
S_{3b}=R_{3b}\land
\bigwedge_{t=0}^{b-1}\operatorname{NAE}(x_{3t+1},x_{3t+2},x_{3t+3}).
$$

With M=\binom{k}{2}, there are exactly n_k=3k+3M variables, e_k=2k+3M+b distinct signed-NAE groups, and 2e_k=4k+6M+2b proper width-three clauses. An ordinary explicit indexed source has L_k=Theta(k^2 log k) bits, with no padding. All variable incidence degrees are at least two. The X_i degrees are exactly the integers k+2,...,2k+1; each other original variable has incidence degree two. Therefore canonical signed-NAE degree-one edge peeling does nothing, and the original source primal clique K_k persists, giving treewidth >=k-1. All complementary NAE pairs ensure neither uniform all-true nor all-false assignment satisfies the source.

## 3. Exact non-affine projection, rank, and full affine-hull theorem

**Theorem 043.1 (exact projection).** For every k=3b>=3,

$$
\exists(Z,U,A,B)\ S_k(X,Y,Z,U,A,B)
\equiv
\left(\bigwedge_i(y_i=1-x_i)\right)\land
\bigwedge_{t=0}^{b-1}\operatorname{NAE}(x_{3t+1},x_{3t+2},x_{3t+3}).
$$

**Proof.** The two signed twins NAE(x_i,y_i,z_i) and NAE(x_i,y_i,not z_i) require x_i!=y_i and, if this holds, any z_i works. Independently, for EVERY chosen X with Y=not X, the original pair guards have the simultaneous extension u_ij=1-x_i, a_ij=0, b_ij=1. The newly added NAE blocks involve X only, so they impose precisely the displayed remaining condition. This proves both directions without choosing a prescribed derivation.

For each of the 6^b X assignments satisfying the b disjoint NAE_3 conditions, exactly one Y, namely not X, appears in the existential communication matrix. Every other row is zero. Hence the rational rank, real rank, number of one entries, exact largest fooling set and minimum all-one rectangle-cover number all equal

$$
\boxed{6^b}.
$$

The nonzero submatrix is a permutation matrix. A one-rectangle cannot cover two different ones because each row and column has at most one nonzero entry. This is a matrix property, not an SAT runtime lower bound.

The existential X-only projection is exactly b disjoint NAE_3 relations. It is itself **not Horn, dual-Horn, bijunctive, or affine**. The NAE_3 relation is not closed under componentwise meet, join, majority or ternary XOR. Fixing all but one block to satisfying values transfers these closure failures to the whole X projection. Closure under each operation is inherited by existential projection, so the full source and XY projection are also outside those four Schaefer classes. In particular, this strengthens TMR-2/042, whose XY projection was purely affine.

Moreover NAE_3 has full affine hull F_2^3. For each bit position there are two NAE assignments differing only in that bit; a parity functional constant on NAE_3 must therefore have coefficient zero in every position. Thus Gaussian elimination of affine equalities y_i=1-x_i leaves **b genuinely nonlinear NAE blocks**, rather than silently explaining away the rank by an affine-only quotient. But those blocks form an explicit disjoint constant-size representation and have O(b) gate descriptions and trivial local solving. The full source clique does not force that projected factor graph to have high treewidth.

## 4. Genuine fixed correct total SAT-machine shortcut

On canonical S_k, choose every high-variable block X=(0,0,1), let Y=not X, each z_i=0, each u_ij=1-x_i and a_ij=0,b_ij=1. This satisfies EVERY original and added clause.

The separately published executable contains one fixed deterministic **structural recognizer** for the whole class of canonical S_k, all bijective variable renamings, independent flips of complete source variables, shuffled clauses, and exact duplicate clauses. After deduplication and signed-complement pairing, it locates high-incidence variables by the degree signature k+2,...,2k+1. It checks that all high-only NAE groups form a disjoint triple partition, all two-high groups realize a complete graph, each one-high twin is authenticated, and the remaining guards partition into the original u/a/b motifs. It first picks a satisfying assignment independently for each high-only signed NAE triple, then completes all signed twins and all u/a/b triples by constant-size local truth-table searches. It verifies every original clause before accepting. Any failed recognition or witness verification triggers an exact exhaustive SAT solver fallback on ALL other proper and malformed sources.

Only polynomially many loops over clauses and variables and constant-size truth tables are needed on this class. All comparisons, source rereads, local table evaluations, witness storage and final checking are to be charged in a physical multitape compilation; no O(1)-cost random access or polynomial arbitrary-input SAT solver is postulated. An ordinary conservative multitape implementation remains polynomial in the explicit encoded length L_k, without claiming a specific exponent. Thus there exists ONE fixed correct total SAT decider with polynomial work on this entire signed/renamed family. Exponential rank is a real, legal **cheap-path** countercontrol.

## 5. Independent exact dynamic tariff laboratory and terminal firewall

Qualify separately the **authenticated NAE-block certificate record calculus**: the original source, one correct completed witness, all b original high-only NAE obligations, and a paid-verification set are supplied as exact state. Legal free operations are reversible VIEW/NOP which never inspect additional source or change the checked set, and GOAL only if all b high-only NAE blocks have been checked. The sole paid operation CHECK(t) verifies one previously unchecked high-only NAE block against the witness and adds that block to the checked set, at cost 1. Shared checked identities count once; all b conjunctive obligations are mandatory. This is NOT a SAT decider, physical-TM work model, or free-authentication claim.

Let v be the number of unchecked blocks, and define a seven-vector

$$
p(C)=(0,0,6^v-1,0,v,0,0).
$$

All authentic free transitions preserve p exactly, so its zero-cost SCC quotient is sound. On CHECK from v>=1 to v-1, the **complete signed tariff row** is

$$
\Delta_{\rm CHECK}=(0,0,5\cdot6^{v-1},0,1,0,0),\quad w=1.
$$

All free rows have Delta=0 and completed goals have p=0. The v=b first CHECK witnesses the largest SEP discharge; hence the exact nonnegative feasible cone for all legal states at this fixed b is

$$
\boxed{5\cdot6^{b-1}\lambda_{\rm SEP}+\lambda_{\Gamma}\le 1}.
$$

For b>=2, the ratio (6^b-1)/(5*6^(b-1)) is less than 6/5<=b. At b=1 the ratio is exactly one. Therefore the exact rational initial-potential LP has optimum b, attained by lambda_SEP=0, lambda_Gamma=1, matching exactly b authentic checks. Uniform nonnegative weights across UNBOUNDED b require lambda_SEP=0. Thus the exponential dynamic rank coordinate cannot receive a fixed positive all-scale price even after the initial affine and leaf quotients, while the block obligation has an honest unit tariff. Full rows and solver-friendly symbolic schema are in the JSON matrix.

An independent *physical machine* objection remains: if one instead defines a source-static (6^b-1)*1[live] component, the genuine final cost-one HALT transition discharges it entirely, forcing lambda_SEP(6^b-1)<=1 for every b and thus lambda_SEP=0. The typed record calculus and the physical HALT objection have different legal transition inventories and are not conflated.

## 6. Executed evidence and hostile-control status

The EXACT audit() function serialized into experiments/tmr/tmr2_nonlinear_projection093.js was executed in native hosted V8 before publication. It completed **5,004 assertions with zero failures**, including 4,160 independent local existential-projection matrix cells, 112 signed/renamed/shuffled/duplicate source-recognizer fixtures, complete k=3,6 source X projection scans and exact count, k=9,12 sampled X sources, 10 typed record-tariff rows, affine-hull masks, degree, clique, grammar, missing-complement and complete original-clause witness checks. Tested k=3,6,9,12. No standalone operating-system Node rerun, complete machine binary trace, or full repository preflight has been executed.

Control ledger: Gaussian/affine elimination removes XY anti-equality but not NAE_3; Horn and dual-Horn closure fail; Krom/2-SAT and simple literal propagation are allowed but not assumed hard; disjoint NAE_3 factors admit constant-size SAT witnesses and easy separator DP despite full primal K_k; no degree-one source-variable peeling is possible; signed-twin constraints, autarkies, equality and global gauge flips are explicitly tested; compact circuits, extensions, clause learning, reuse, caching, rereading and recomputation remain allowed and could only make a real decider cheaper; padding and clause duplicates are not charged as semantic complexity. No CEGAR path was removed. TMR-5/039's batch-query row and TMR-1/043's connected-DAG bound remain separate restricted systems. Historical /341 remains FAIL as a full logical UNSAT authority, /386 remains RESTRICTED.

**Status/dependency ledger:** exact S_k projection/rank/cover PROVED/RESTRICTED (peer review OPEN); structural recognizer correct on authenticated class with exhaustive fallback PROVED/RESTRICTED (native finite tests COMPUTATIONAL); typed CHECK tariff cone and LP PROVED/RESTRICTED (peer review OPEN); positive uniform rank tariff FAIL in the qualified record system; unrestricted real SAT-machine obstruction, all-transition abstraction, superpolynomial initial gap and same-system all-decider transfer OPEN.

**Next peer repair:** TMR-3 must charge a physical signed-NAE recognizer and final witness verification; TMR-4 must replay the CHECK row and preserve the real SAT witness as MAY in any broader abstraction; TMR-5 independently audit the projection/non-Schaefer and variable-rename arguments; TMR-1 keep the all-machine transfer gate open. TMR-2's next target is a *nonfactorizing*, truly dynamic cross-scale obstruction that survives both affine and constant-block NAE quotienting and cannot be completed by a family-specific polynomial witness.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full proof1.txt SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, authentic full proof2.txt blob SHA 930c5eeddafce656717f28055a7a9a755f44737c, authentic full main.tex blob SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 recovered. No root modifications, no task/schedule changes. P versus NP OPEN.
