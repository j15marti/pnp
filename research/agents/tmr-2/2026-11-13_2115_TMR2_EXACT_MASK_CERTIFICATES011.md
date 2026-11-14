# TMR-2/011: exact certificate complexity of the eight-mask 3-CNF superclass

**Date:** 2026-11-13 21:15 PST (America/Los_Angeles). **Role:** TMR-2, Information Necessity. **Repository:** j15marti/pnp, main. **Claim:** TMR2-CERT11, **CANDIDATE pending TMR-5 independent mathematical review**, with a self-contained proof below. **Finite verification:** COMPUTATIONAL. **Unrestricted superpolynomial 3-SAT lower bound and P versus NP:** OPEN.

## 1. Novel exact claim and dependency

Use the *original* strictly proper 3-CNF template $\mathcal G_r$ of TMR-2/010, TMR-5/007, and TMR-1/010. For each $r\ge1$ it has eight ordered clauses on each of $r$ disjoint three-variable blocks; each block has 24 freely chosen clause-polarity bits. All other source bits, including unary counts, core even-parity identifiers, and positive dummy filler, are fixed by the template. The full valid source encoding is $1^N0\,1^M0$ followed by three signed fixed-width IDs in each clause, with

$$
w=\lceil\log_2(6r+2)\rceil,\quad N=2^w-1,\quad
K=\lceil(N-3r)/3\rceil,\quad M=8r+K,\quad
L=N+M+2+3M(w+1).
$$

The family contains $2^{24r}$ distinct fully valid original 3-CNF sources, both SAT and UNSAT. Clause mask $m\in\{0,\dots,7\}$ forbids the unique three-variable assignment equal to $m$. Thus one block is UNSAT precisely when its eight masks are a permutation of all eight values; the full formula is UNSAT precisely when at least one block is UNSAT. Positive filler variables can all be set to true.

Fix the SAT source $z_r$ having mask list $(1,2,3,4,5,6,7,7)$ in **every** block, precisely the TMR-5/007 three-bit-radius source. A *template bit certificate* for an input $x\in\mathcal G_r$ is a set $Q$ of the **free sign-bit coordinates** such that every $y\in\mathcal G_r$ agreeing with $x$ on $Q$ has the same SAT/UNSAT answer.

**Theorem candidate TMR2-CERT11.** The exact minimum sign-bit certificate size on $z_r$ is

$$
\boxed{C_{\mathcal G_r}(z_r)=5r.}
$$

For **every UNSAT** $u\in\mathcal G_r$, the exact minimum certificate size is

$$
\boxed{C_{\mathcal G_r}(u)=24.}
$$

This quantifies a substantial SAT/UNSAT asymmetry: one fixed UNSAT block certifies UNSAT, whereas every independent SAT block needs its own evidence. It strengthens the earlier $r$ disjoint three-bit neighbor lower bound to $5r$ *distinct first-read bits* on $z_r$. It is a certificate lower bound and not an obligation to retain $5r$ bits in workspace, not a superlinear processing bound, and not a claim about all possible source encodings.

## 2. Proof of the 5-bit single-block minimum

Consider any selection of at most four observed polarity bits among eight ordered three-bit masks. For each row $i$, let $A_i\subseteq\{0,\dots,7\}$ be the set of masks consistent with observations made in that row. If $b_i\in\{0,1,2,3\}$ bits are observed in row $i$, then $|A_i|=2^{3-b_i}$. By Hall's distinct-representatives criterion, the partial source can be completed to an UNSAT block exactly when the $A_i$ admit a matching onto all eight masks.

**Every observation set of size at most four admits such a matching.** For any subset $R$ of $k$ rows, with $1\le k\le8$, if $k\ge5$, at least one row of $R$ has no observed bit because no more than four rows can be observed; its domain has eight masks, so $|\bigcup_{i\in R}A_i|\ge8\ge k$. If $k=4$, at least one row has at most one bit observed and its domain has at least four masks; if $k=3$ the same gives at least four masks; if $k=2$ at least one row has at most two observed bits and a domain of at least two masks; if $k=1$ its domain is nonempty. Hence $|\bigcup_{i\in R}A_i|\ge k$ in every case. Hall's criterion gives a complete permutation consistent with the four or fewer observations, regardless of the initially selected masks. Therefore **no SAT block has a certificate of size at most four**.

For the specific $z_1=(1,2,3,4,5,6,7,7)$, the first sign bit (the $2^0$ coordinate) in rows $0,2,4,6,7$ is 1. Observing those **five** sign bits certifies SAT: five masks must have that bit equal to 1, yet only four distinct 3-bit masks have it equal to 1. The eight masks cannot be a permutation. Thus $C_{\mathcal G_1}(z_1)=5$. The position set within each row's three sign bits is $\{0,6,12,18,21\}$, with canonical source-field offsets given by $N+M+2+3(8g+c)(w+1)+0\cdot(w+1)$ for $c\in\{0,2,4,6,7\}$ in block $g$.

The $r$ blocks are disjoint and their 24-bit sign fields are freely independent. A certificate of SAT must forbid an UNSAT completion **in every block**: if any block is observed in at most four positions, complete that block to all eight masks, hold the remaining blocks at their original values, and obtain an agreeing UNSAT source. Hence the lower bound $5r$. The union of the five-bit certificates, one per block, proves the matching upper bound $5r$.

## 3. Proof of the 24-bit UNSAT certificate

For any UNSAT template source $u$, at least one block is a permutation of all eight masks. Observing all its 24 sign bits proves UNSAT, so $C\le24$. Conversely, suppose no complete UNSAT block has all 24 of its sign bits queried. Every full-permutation block then has an unobserved sign bit. Flipping one such unobserved bit changes one row's mask into a mask already held by another row, so that block becomes SAT; leave blocks already SAT unchanged. Because the blocks are independent, these changes produce an agreeing globally SAT source. Thus any UNSAT certificate must contain all 24 bits of some UNSAT block, proving $C=24$.

## 4. Exact transfer to one fixed unrestricted-workspace machine

For **any one fixed total correct deterministic multitape SAT decider** $A$ over all lengths, let $V_A(x)$ be the set of original binary input positions actually observed on its **halting** execution on source $x$, including all input rereads. For any same-length valid $y$ that agrees with $x$ at every position in $V_A(x)$, induction on the full machine configuration gives the *identical entire run* on $y$: same control, every work-tape symbol, all heads, each next input symbol, and terminal label. The proof does not require online continuations, one-pass access, prescribed encoding of workspace, or erasing previously read input. It requires a standard read-only physical-input interface with no uncharged indirect source oracle. Hence $V_A(x)$ must contain a sign-field certificate relative to the template promise.

For $z_r$, at least $5r$ **distinct original sign positions** must be observed by $A$. If there are $h\ge1$ read-only heads and each physical transition reads at most $h$ input symbols, then

$$
\boxed{T_A(z_r)\ge\lceil5r/h\rceil
=\Omega(L/\log L)\quad\text{for fixed }h.}
$$

All writable memory, precomputation, algebraic encodings, alternate representations, sharing, adaptive querying, and rereading are unrestricted and included in the actual machine run. If an interface reveals extra original bits per transition, the numerical charge must be changed: it does not transfer freely to indexed RAM. The stricter *physical input-transport* $\Omega(L)$ already available from TMR-4/009 and TMR-5/008 can dominate this query count under left-aligned sequential heads.

**Transfer gap:** This proof establishes only how many source bits a correct execution must physically acquire. It does not require retaining those bits, enumerating eight-way alternatives, performing exponential work, or ever constructing a proof in a particular calculus. TMR-2/010 gives a fixed general all-input-correct decider with a polynomial-time authenticated mask-table fast path on this entire two-label class (symbolic all-length TM compilation still pending peer review). Thus neither $5r$ nor $24$ yields a representation-independent superpolynomial SAT processing bound. The quantifiers needed for P != NP remain OPEN.

## 5. Hostile controls, actual execution and provenance

**ACTUAL native Node.js v22.16.0 execution:** exact bipartite augmenting-path matcher tests all $1+24+276+2024+10626=12,951$ bit-subsets of sizes zero through four against the original 8-mask SAT block and finds an UNSAT-completing permutation for every one. It additionally tests all $\binom{24}{5}=42,504$ five-bit subsets, finding three SAT certificates (a finite fact, not needed for the theorem), 24 one-bit changes of a full UNSAT permutation, and 500 independent mask/assignment semantic cases. Zero failures.

**ACTUAL independent Python 3.13.5 execution:** enumerates all $8!=40,320$ full UNSAT permutations, constructs a different bit-parallel agreement index, and audits all 55,455 query sets of sizes zero through five. It independently returns exactly 0 certificates of sizes $\le4$, exactly 3 of size 5, and 24 sensitive sign bits on a full permutation. Zero failures. This is an independently coded verifier of the same finite 8-row subproblem, not another representation of the Node matcher.

Controls: both SAT and UNSAT mask labels; duplicates versus complete permutations; all possible partially known input sign locations up to size five; arbitrary mask configurations in 500 deterministic assignment checks; multi-block disjoint product reasoning; source identifiers and fillers held canonical. No new native physical TM execution, full 3-CNF parser run, Horn/2-SAT/GF(2) regression run, or unbounded-size machine implementation was performed in this run. The original TMR-2/010 source parser and structured fast-path tests are separate evidence, not silently relabeled as new tests.

**Source reading:** First the current 2026-11-13 12:49 PST replacement directive; both root trackers (proof1 complete 28,714 characters, proof2 recovered **complete original 1,051,196-character Git blob**, ordinary fetch blank); root main.tex recovered complete authentic Git blob 2,507,300 characters; current issue #3, AGENTS.md, CODEX.md, pnp-research SKILL.md, all five latest TMR handoffs, original TMR-2/010 encoder and report, TMR-4/008, TMR-5/007, TMR-1/010, TMR-4/009, and historical TMR-2/009. Prior certificate bounds remain valid and are quantitatively sharpened only for the eight-mask *promise*. Earlier legacy instructions do not supersede the replacement.

Primary literature independently checked: P. Hall, *On Representatives of Subsets*, J. London Math. Soc. (1935), 26-30, https://doi.org/10.1112/jlms/s1-10.37.26 (matching criterion); H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theor. Comput. Sci. 288 (2002), 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X (certificate/query model). This report's 5r and 24 exact computations are new local deductions, not claims quoted from those papers.

**Tracker decision:** TRACKERS REVIEWED; NO MATERIAL CHANGE. [P1-01], [P1-03], [P1-04] and unrestricted [P2-00] remain OPEN. No authorized TMR-2 main.tex changes made. No schedules, task identities or allocations touched.

**Independent audit requested of TMR-5:** reproduce Hall matching argument and disjoint-product 5r necessity with no assumption of streaming or bounded workspace. **One next target:** find an information *processing* lower bound after all decisive source bits are acquired that survives the polynomial mask-table fast path, Gaussian-elimination controls and full-memory/recomputation freedom.

END_OF_REPORT::TMR2-CERT11::2026-11-13_2115_PST
