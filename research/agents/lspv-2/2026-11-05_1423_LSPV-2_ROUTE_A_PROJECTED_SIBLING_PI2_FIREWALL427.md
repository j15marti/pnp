# LSPV-2/427 | Projected sibling equivalence is Π₂^P-complete even for satisfiable 3-CNF parents

**2026-11-05 14:23 PST | Route A PRIMARY | PROVED/RESTRICTED, COMPUTATIONAL finite replay | P versus NP OPEN.**

## IDEA (before search) and falsifiers

Hypothesis: the sibling **decision-label equivalence** test isolated by LSPV-4/422 is not sufficient to merge **projected boundary relations**, and the latter exact operation has a higher, quantified complexity even when the common 3-CNF parent is guaranteed satisfiable. Falsifiers: (F1) existential gate factoring loses original x-to-private-variable correlation; (F2) positive guard branch cannot be satisfied; (F3) Π₂^P-hardness fails for proper exactly-three-distinct-literal 3-CNF; (F4) two siblings may have equal SAT decision labels but different projected boundary functions. F1–F3 were checked/proved; F4 is demonstrated explicitly below, confirming the hypothesis. These are **complexity-model restricted** results, not a proof of SAT machine-time hardness.

## PROVED/RESTRICTED theorem

**Problem PROJ-SIBLING-EQ.** Input: source-authenticated proper 3-CNF $H(z,X,Y)$ with designated selector $z$, public shared variables $X$, private variables $Y$ and the promise that $H$ itself is SAT. Decide whether the two exact existentially projected Boolean relations are pointwise equal:

$$
\forall x\;\left[(\exists y\;H(0,x,y))\leftrightarrow(\exists y\;H(1,x,y))\right].
$$

**Theorem:** PROJ-SIBLING-EQ is $\Pi_2^P$-complete under polynomial many-one reductions, including on guaranteed SAT parents whose clauses contain exactly three distinct variable IDs.

**Hardness.** Begin with the established $\Pi_2^P$-complete **$\forall X\exists Y$ proper 3-CNF** quantified problem, in the exact restrictive form certified by Döcker, Dorn, Linz and Semple (2019), arXiv:1908.05361. For each original clause $C_i=(a_i\lor b_i\lor c_i)$, introduce a new global selector $z$ and one fresh private variable $u_i$. Form

$$
H_G(z,X,Y,U)=\bigwedge_{i=1}^{m}
[(z\lor a_i\lor u_i)\land(\neg u_i\lor b_i\lor c_i)].
$$

Every output clause has exactly three distinct variables; every $u_i$ is private and fresh. For each fixed original assignment, direct two-bit elimination establishes

$$
\exists U\;H_G(0,X,Y,U)\equiv G(X,Y),\qquad
\exists U\;H_G(1,X,Y,U)\equiv\top.
$$

At $z=1$, **all** $u_i=0$ satisfy the parent independently of original variables. Therefore the promise is unconditional, and

$$
R_0(x)=\exists Y\;G(x,Y),\quad R_1(x)=1,\quad
R_0\equiv R_1\iff\forall X\exists Y\;G(X,Y).
$$

**Membership.** A nonequality certificate is a guessed public assignment $x$ for which two NP-oracle questions, $\exists y H(0,x,y)$ and $\exists y H(1,x,y)$, yield different answers. Thus nonequality is in $\Sigma_2^P$ and equality is in $\Pi_2^P$. Promise satisfiability does not change hardness: the reduction always produces a SAT parent.

**Scope and novelty safeguard.** QBF completeness is **KNOWN** from Döcker et al. This exact guarded reduction is a direct extension of already-published **LSPV-4/422** (same gate syntax), which only proves **SAT-hardness of equality of the two zero-boundary SAT decision labels**. The present result distinguishes **public projected relations** and establishes their $\Pi_2^P$-completeness. Do not promote it to a theorem that universal contraction is impossible. Under SAT in P the polynomial hierarchy would collapse, so the conditional FLMV hypothesis is not refuted.

## Critical counterexample: identical decision labels, unequal relations

Take $X=\{x\}$, private $Y=\{y,w\}$ and

$$
G=(x\lor y\lor w)\land(x\lor\neg y\lor w)
\land(x\lor y\lor\neg w)\land(x\lor\neg y\lor\neg w).
$$

Then $\exists_{y,w}G(x,y,w)=x$. For its guarded $H_G$, both global sibling decision labels are SAT, but $R_0(x)=x$ and $R_1(x)=1$ are not equivalent. Therefore **cache equivalence of SAT/UNSAT labels cannot authorize reuse of an entire boundary relation**. Shared branch data must carry its public assignment context and an independently justified equivalence or valid implication proof. This applies to Route A shared computations, not to the historical native $R_{mix341}$ branching grammar.

## Fully explicit encoding and resources

Let original $G$ have $m$ strict proper 3-clauses over $n$ variables, with public/existential partition. Relabel used variables into $[1,n]$ and use a self-delimiting fixed-slot signed-literal binary 3-CNF grammar. The mapped parent has exactly $2m$ clauses, $n+m+1$ variable IDs, and $O(m\log(n+m))$ bits plus polylogarithmic headers. Under standard dense used IDs $n\le3m$, input length $N=\Omega(m)$ and parent size $M=O(N\log(N+2))$. Every output bit can be generated on demand from a source clause position or known selector/auxiliary ID using $O(\log N)$ scratch and $\log^{O(1)}N$ indexed operations; parse, ID checks, index writes and erasure incur real costs. **Materializing** the entire parent as writable guest input would consume $\Omega(M)$ peak space; an indexed virtual input only avoids that materialization. This bound is for the **reduction**, not for deciding the projected-relation equivalence predicate or for transforming an arbitrary SAT decider.

Separate cost ledgers: (a) no paid $R_{mix341}$ derivation nodes, since this is a complexity reduction; (b) $2m$ explicit 3-clauses and $O(M)$ proof/data bits if materialized; (c) deterministic construction $O(N\log^{O(1)}N)$ time, $O(\log N)$ scratch on the stated indexed tape; (d) semantic equality check costs are **not bounded** by the Route A local budget; (e) full producer stores sources/results in host memory and is **not** an FLMV-machine execution. Shared logical DAG weights and scheduled machine work remain distinct.

## FINITE COMPUTATIONAL tests, independently verified

Producer: 261 complete source cases. Enumerated all $2^8=256$ subsets of the eight proper width-three clauses over variables $x,y,w$ (with $x$ public). Exact results: **225 equal**, **31 unequal** projected sibling pairs. Of those unequal pairs, **30 have equal global SAT decision labels**, making label-only merge unsound. The remaining unequal pair has UNSAT $z=0$. Four historical source controls: even/odd charges on K4 (16 proper 3-clauses, 6 variables) and cube (32 clauses, 12 variables). For even charge each public edge value extends to a satisfying assignment (bridgeless cycle); for odd charge neither does. Predicted sibling equivalence true for even and false for odd. Fifth control is the explicit 4-clause label-only trap. All 261 cases have guaranteed SAT parents. Three malformed 3-CNF inputs rejected.

The standalone Python producer passed all assertions and wrote a **313,282-byte** raw JSON with SHA-256 **0b7060b2f457b8b2b15098f8f1250d52f02b46ac2053de4985e36af927c71bc5**. Independent JavaScript replay passed **12,111 assertions** (after correcting a verifier-only JSON property-order comparison and a histogram-scope error). A separate compact Node checker executed **1,342 assertions**. Tests enumerate public/existential models, pairwise auxiliary truth values, and (up to five gates) every auxiliary assignment; corrupted gate and forged projected-relation records are rejected. These finite controls do not establish the $\Pi_2^P$ hardness theorem, which follows from the symbolic reduction and cited QBF theorem.

## Established hard-family / shortcut ledger

Cubic graph Tseitin, $h$ vertices, $3h/2$ edge variables, four width-three forbidden-parity clauses at each vertex ($4h$ clauses), $N=\Theta(h\log h)$ for usual dense variable-ID encoding; odd charge **UNSAT**. For suitable bounded-degree expander sequences, Urquhart (JACM 1987) and Ben-Sasson–Wigderson (JACM 2001) imply $2^{\Omega(h)}$ ordinary shared-DAG **Resolution** refutation size. This is **not** an all-machine or full mixed-calculus lower bound. Project LSPV-2/341 already supplies a $4h-1$ paid-node native AND3/GF(2) refutation on bridgeless cubic sources. The even-charge SAT control and this algebraic shortcut defeat attempts to treat these as hard against unrestricted solvers. The finite K4 and cube controls are not themselves an infinite expander lower-bound family. Haken PHP ordinary Resolution and Cook ER remain distinct controls. **Missing transfer:** zero-boundary SAT labels and authenticated algebraic relations do not provide a universal exponent-oblivious, recursively iterable all-input FLMV solver transformation.

## IDEA -> SEARCH -> ITERATE provenance

**Project and peer:** Governing handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e; current issue #3; AGENTS.md 19656af1; CODEX.md 754999f5; skill b8df83a7; LSPV-2/426 blob c7e4563e; LSPV-4/422 blob 6046c02a and coordination handoff blob 6ef6a84c. **Actual external reviews:** GROKPROOF/2026-11-05_1913_PROGRESS.md blob 8a004bf4; research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727. Neither solves all-input contraction.

**Required repositories actually read:** konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e (finite one-tape semantics unlike FLMV); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea and PROJECTION_DISCOVERY_BARRIER_REPORT.md blob a24f4fd (SAT-hard existential projection; does not resolve quantified boundary relation). openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4 (costed particular bit program, not a generic solver oracle); CNFgen cnfgen/families/tseitin.py blob 4bb5fd1 (source family construction only). Also inspected prior sibling-label lemma source, ensuring this is a **strictly different question**, not a re-report of LSPV-4/422.

**Primary sources:** Döcker, Dorn, Linz, Semple, *Placing quantified variants of 3-SAT and Not-All-Equal 3-SAT in the polynomial hierarchy*, arXiv:1908.05361, theorem-level premise exact-three-distinct variable 3CNF; Fortnow, Lipton, van Melkebeek, Viglas, JACM 2005 DOI 10.1145/1101821.1101822 (paper §§2.1,3,5 and Corollary 5.8 verified); Urquhart 1987 and Ben-Sasson–Wigderson 2001 for ordinary Resolution. Search queries: `forall exists 3CNF Pi2 complete`, `equivalence existentially quantified Boolean formulas projected CNF Pi2P complete`, `QBF 2 universal existential 3CNF Pi2 complete`, `site:github.com/openai/math QBF`, `site:github.com/konard/p-vs-np QBF`. **Direct Google-branded UI unavailable**; indexed web search was used, not described as a Google session.

**Iteration:** Initial proposal of free identical SAT-label reuse was rejected by the 4-clause trap. Strengthened theorem is about exact projected **functions**, not scalar labels. Rechecked all 261 cases, and corrected two verifier bookkeeping errors before independent acceptance. Explicit syntax and input-access accounts replace any unjustified zero-cost guard. Nothing assumes native $R_{mix341}$ case-split authority.

## Precise remaining obligation

**OPEN:** derive a solver-dependent, exponent-oblivious, original-source/malformed-aware, same-machine transform $A\mapsto\Phi(A)$ for *every* total correct polynomial SAT decider, with recursively applicable fully charged
$$
t'\le\max(11/10,3/5+t/2),\qquad
s'\le\max(1/2,s/2),
$$
including all local phases, guest access, reconvergent context, cache storage and correctness. Semantic branch equivalence is not a free primitive. Historical $R_{mix341}$ B1/B2/B3 are Route B and remain OPEN. P versus NP OPEN.
