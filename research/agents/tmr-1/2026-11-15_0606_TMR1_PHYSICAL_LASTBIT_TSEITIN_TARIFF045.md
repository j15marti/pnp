# TMR-1/045: Exact last-bit SAT frontier tariff for arbitrary correct local-head deciders

**2026-11-15 06:06 PST | PNP Machine Model Lead | LASTBIT045**

**Status:** PROVED/RESTRICTED mathematical theorem for a declared physical multitape machine interface; independent mathematical peer review OPEN. Finite experiments COMPUTATIONAL. The lower bound is **linear**, not superpolynomial. P versus NP remains **OPEN**.

## 1. Candidate and four falsifiers declared before literature and corpus review

**Candidate.** Upgrade the program-specific physical tariff of TMR-1/044 to an all-correct-SAT-program, *same-machine* theorem by constructing two valid growing original proper 3-CNF inputs that differ solely in the final physical source bit and have opposite labels. Every correct physical decider must read this bit. This qualifies a machine-level input-frontier obstruction, but its initial value is only the encoded length.

Falsifiers: (F1) the last-bit mutation is malformed, changes other data, or has the same SAT label; (F2) removing the affected cubic vertex disconnects the graph and defeats the claimed SAT witness; (F3) a legal paid or zero-cost physical transition reaches the final source bit without traversing the entire input tape or discharges more than one frontier unit; (F4) an authenticated algebraic or shared-circuit recognizer decides this family in polynomial time. F1 through F3 are excluded in the scoped model; F4 is a **genuine legal easy-family control** and forbids superpolynomial claims.

## 2. Corpus, primary sources and nonduplication

Read FIRST the governing fusion-Lipschitz directive, Git blob SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6, then the TMR 2026-11-13 replacement, root proof1.txt complete (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), root proof2.txt entire authentic Git blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c), and root main.tex entire authentic Git blob (2,545,859 characters, SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34). The ordinary contents API returned empty bodies for the two oversized files; complete Git blobs were fetched instead. Also reviewed current issue #3 and comments, AGENTS.md, CODEX.md, repository research skill, all five latest TMR handoffs, original peer TMR-1/044, TMR-2/044, TMR-3/044 and TMR-4/045 report/code/tariff data, TMR-5/040, October LEAD-0029 Lipschitz audit and historical LSPV-4/506 and /508.

**Novelty boundary.** LSPV-4/506 previously established sign-bit sensitivity and completed-read-trace necessity for suitable original cubic Tseitin sources, and its aggregate multi-input star bound. LSPV-4/508 replaced an asymptotically invalid 12-bit header with an Elias-gamma encoding and established a width-two parity OBDD. TMR-3/042 and TMR-4/045 already gave physical source-frontier tariffs for *copy/output services*. The elementary deterministic indistinguishability technique is not new. Here the additional qualified object is a fully unbounded strictly ternary *opposite-label last-bit pair* plus an exact seven-column all-correct-SAT-machine tariff, not a prescribed output-service DAG.

Primary contextual literature: Hartmanis and Stearns, *On the Computational Complexity of Algorithms*, Trans. AMS 117 (1965), DOI https://doi.org/10.1090/S0002-9947-1965-0170805-7, for genuine local machine time; Tarjan, *Amortized Computational Complexity*, SIAM J. Alg. Discrete Methods 6 (1985), DOI https://doi.org/10.1137/0606031, for potentials; Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48 (2001), DOI https://doi.org/10.1145/375827.375835, whose exponential results are ordinary Resolution only. None supplies an unrestricted SAT-machine lower bound.

## 3. Explicit growing original proper-3CNF inputs and bit length

For $m\ge2$, put $G_m=C_{2m}\square K_2$, a circular ladder with $H=4m$ vertices and $E=6m$ edges. The graph is connected, simple, cubic and bipartite, and deleting any one vertex leaves it connected: the opposite cycle survives and every remaining vertex of the punctured cycle has a surviving spoke. The family is **not** asserted to be an expander.

Number all edges $1,\ldots,E$. Set $b_0=1$ and all other vertex charges $b_v=0$. Each vertex $v$ with incident variables $x_{e_1},x_{e_2},x_{e_3}$ requires

$$
x_{e_1}\oplus x_{e_2}\oplus x_{e_3}=b_v.
$$

Encode this by the four proper width-three clauses excluding exactly the four triples $s$ with parity $s_1\oplus s_2\oplus s_3\ne b_v$. The clause for $s$ is $\ell(x_{e_1},s_1)\vee\ell(x_{e_2},s_2)\vee\ell(x_{e_3},s_3)$, where $\ell(x,0)=x$ and $\ell(x,1)=\neg x$. It is false exactly at $x_{e_i}=s_i$. Use sorted vertices and incident edges; within each vertex's packet order a wrong-parity triple with final sign zero last. There are $4H=16m$ original clauses and $12H=48m$ signed original literal occurrences.

Our exact unbounded counted binary grammar is: 8-bit magic 00110101; Elias-gamma encodings of positive integers $E$ and $4H$; and for each signed occurrence a $w=\lceil\log_2(E+1)\rceil$-bit positive edge ID plus one actual polarity bit. Thus physical source length is

$$
\boxed{
N_m=8+\ell_\gamma(6m)+\ell_\gamma(16m)
 +48m(\lceil\log_2(6m+1)\rceil+1),
\quad \ell_\gamma(t)=2\lfloor\log_2t\rfloor+1
=\Theta(m\log m).
}
$$

The final original source bit is a polarity zero. The formula $F'_m$ is obtained from $F_m$ by flipping **only that final bit** to one. Both retain exactly the same identifiers, strict arity, clause count, encoding and length. No padding or semantic table is charged as computational work.

**Theorem 045-A (PROVED/RESTRICTED).** For every $m\ge2$, the above original proper 3-CNF $F_m$ is UNSAT, the last-bit mutant $F'_m$ is SAT, and both are valid original inputs of $N_m$ bits differing in exactly one final bit.

**Proof.** Summing all the parity equations over GF(2) cancels every edge variable twice but leaves right-hand side one, so $F_m$ is UNSAT. Let $v$ be the last vertex and $s$ the locally forbidden edge triple encoded by its final clause. Fix the three incident edge bits at $v$ to $s$. The other three wrong-parity clauses at $v$ are true on $s$; the last clause, previously false, becomes true after its final literal sign is flipped. The remaining vertex equations are on connected $G_m-v$. Their modified right-hand sides sum to

$$
\bigoplus_{u\ne v}b_u\ \oplus\ \bigoplus_{e\ni v}s_e
=(1\oplus b_v)\oplus(1\oplus b_v)=0.
$$

Every even-parity right-hand side lies in the GF(2) incidence matrix column space of a connected graph. Equivalently, assign non-tree edges zero and solve each tree edge upward from leaves. This produces an explicit satisfying assignment for every other vertex, while all four modified clauses at $v$ are true. Therefore $F'_m$ is SAT. The serial encoding modifies one final sign bit and nothing else. QED.

## 4. Exact physical model, quantifiers and completed goal

Fix **any** correct total deterministic SAT decider $A$ having a fixed finite control/alphabet, **one original immutable binary input tape with one initially-left head**, a fixed finite number of ordinary writable work tapes and heads, arbitrary finite program and unbounded work space. Its machine receives no other copy, index oracle, answer bit or free source advice. Each genuine step reads scanned tape symbols, writes at most one cell on each distinct work tape, moves each head by at most one cell, and costs one unit. It may perform arbitrary preprocessing, sharing, branching, caching, learning, algebraic elimination, new definitions, rereading, recomputation, conversions and output; **all are paid by actual machine steps**, not independently charged again when simultaneous.

The complete concrete state includes $(F,A,G,P,\Gamma,\mathcal D,\mathcal I,\mathcal O)$ with exact source, machine control, all tape contents/head positions, original input-read history, paid identities, any shared representations and active/discharged obligations, and actual SAT/UNSAT terminal label. Genuine zero-cost physical operations do not exist, so the authentic closure $\operatorname{cl}_0$ is identity with singleton zero-cost SCCs. Optional reversible VIEW aliases are mathematical and may be free only if they preserve the obstruction.

The goal is the **correct completed classification** SAT on $F'_m$ and UNSAT on $F_m$, for the same machine $A$ that is correct on *every* encoded SAT input. It is not a prescribed proof DAG or ordered gate-record output.

**Theorem 045-B (PROVED/RESTRICTED, every such $A$).**

$$
\boxed{\forall m\ge2:\qquad
T_A(F_m)\ge N_m,\quad T_A(F'_m)\ge N_m.}
$$

**Proof.** If the run on either original input did not inspect its final source bit, its entire deterministic input-observation sequence, control and work-tape trace would be identical on the other input. Both valid sources agree on every earlier bit, but require opposite labels, contradicting total correctness. Thus both runs must inspect source cell $N_m-1$. With one head starting at cell 0 and advancing at most one position per unit step, at least $N_m$ paid native transitions are needed even if the last read and HALT happen in the same step. QED.

## 5. Complete rule-by-component tariff, exact primal/dual and telescoping

For a concrete actual computation on either paired source let $r(C)$ be the **maximum original input cell index ever genuinely inspected**, initially $-1$. Put

$$
u(C)=\max(0,N_m-1-r(C)),
\qquad
\mathbf p(\operatorname{cl}_0(C))
=(0,0,0,0,0,u(C),0).
$$

Columns in order: CNF, XOR, separator, fusion, Gamma, interface, machine. The initial vector has interface entry $N_m$. Every actual completed correct goal must have inspected the last bit, hence $\mathbf p(\mathrm{goal})=0$ by Theorem 045-B.

| Authentic complete transition class | Physical cost | Signed seven-column discharge |
|---|---:|---|
| Genuine paid native microstep first reading next original source frontier cell, possibly simultaneously writing, branching, learning, outputting or halting | 1 | $(0,0,0,0,0,1,0)$ |
| Any genuine paid native microstep without frontier advancement, including work, input rereads, storage, retrieval, recomputation, circuit/affine preprocessing, output, or terminal step | 1 | $(0,0,0,0,0,0,0)$ |
| Mathematical zero-cost identity or faithful reversible metadata alias | 0 | $(0,0,0,0,0,0,0)$ |

**Exhaustiveness and fusion safety:** In any real local-input-head microstep, the maximum input position *already inspected* rises by at most one. There are exactly the two paid discharge cases above; no paid activity is independently duplicated when performed in the same step. All legal alternative programs on the specified physical interface are included, not just the construction's promise scanner. Unknown richer input operations are conservative MAY and require a new matrix, not deletion of real paths.

The exact active nonnegative tariff cone is $0\le\lambda_{\rm int}\le1$; all other seven-vector coordinates are identically zero. The exact rational certificate

$$
\boxed{\lambda=(0,0,0,0,0,1,0),\qquad
\Phi(C_0)=N_m}
$$

satisfies $\lambda^\top(\mathbf p(C)-\mathbf p(C'))\le w(C,C')$ on **every authentic paid or zero transition**. Every correct completed goal has $\Phi=0$. Telescoping yields $N_m\le T_A(F_m),T_A(F'_m)$ with no proof-system change.

A matching rational row-multiplicity dual assigns unit mass to the $N_m$ compulsory *distinct first-frontier-read events*. Their total price is $N_m$, so the initial obstruction optimum under this one active-coordinate LP is exactly $N_m$. This is **not** a claim that each complete SAT decider finishes in exactly $N_m$ steps. The full machine-readable tariff is at
results/raw/tmr/2026-11-15_0606_TMR1_LASTBIT045_TARIFF_MATRIX.json.

## 6. Real cheap upper controls and representation limitations

A *separate two-source promise reader* traverses the input, remembers the last sign bit, checks the EOF and emits the appropriate label using $N_m+1$ source-local steps. It is **not** an all-input SAT decider. A **single total correct** SAT decider can instead authenticate exactly these canonical families in polynomial time (generate the $G_m$ and signed source templates, compare, and handle the one-bit mutant) and fall back to exhaustive SAT search outside the recognized source image. It remains correct on every other valid and malformed input, although it can be exponential off-family. Hence this family's actual SAT-machine difficulty is at most polynomial. Gaussian elimination resolves authenticated original Tseitin parity in polynomial time; a spanning-tree witness resolves the mutant. Compact circuits, equality, autarkies, Horn/Krom controls, bounded-treewidth DP where applicable, renamings, extensions, learning, sharing, caching, rereading and recomputation remain legitimate, potentially cheaper methods.

These methods cannot produce opposite correct answers for two bitstrings without observing their only distinguishing bit under this exact physical input interface, but **no superpolynomial lower bound follows**. A changed source layout, padding length or random-access word/indexed interface can invalidate the $N_m$ physical distance; transfer is separately OPEN.

## 7. Native executable finite evidence

Executed locally with standard-library native CPython:

    python experiments/tmr/tmr1_lastbit_tseitin045.py 20

Published the exact source as experiments/tmr/tmr1_lastbit_tseitin045.py and the original JSON data values as results/raw/tmr/2026-11-15_0606_TMR1_LASTBIT045_PY_RAW.json. The instrumented run tested **19** sizes $m=2$ through $20$ (bit lengths **506** through **7,718**), verified genuine one-bit source difference, connected vertex-deleted spanning-tree witnesses, signed clause validity, original formula parity contradiction, and all per-bit source-frontier discharges. It exhaustively checked all $2^{12}=4,096$ edge assignments for $m=2$. Instrumentation reported **236,963 assertion checks, zero failures**. No randomness, SAT oracle, official historical checker, assembled TM binary, complete repo preflight or LaTeX build was executed. Finite status COMPUTATIONAL; all-$m$ conclusions rest on proofs above.

## 8. Dependency DAG, peer handoff and guards

| Node | Verdict | Dependency |
|---|---|---|
| A. Valid unbounded authentic signed strict3 opposite-label last-bit pair | **PROVED/RESTRICTED**, peer review OPEN | Explicit circular ladder, incidence parity, spanning-tree extension |
| B. All-correct deterministic deciders must inspect last input bit | **PROVED/RESTRICTED**, peer review OPEN | A, same fixed read-only source interface |
| C. Every genuine local-head step discharges at most one physical input frontier unit | **PROVED/RESTRICTED**, peer review OPEN | Complete actual local-head machine model |
| D. Full seven-column tariff and exact rational initial $N_m$ | **PROVED/RESTRICTED**, peer review OPEN | A, B, C, terminal preservation and telescoping |
| E. Superpolynomial SAT-specific initial obstruction on an explicit family | **OPEN**, this source family is a hostile easy control | Need genuinely computational, not access-only, obstruction |
| F. All-program same-system **superpolynomial** SAT transfer | **OPEN** | Not implied by a linear lower bound |
| Historical /341 full UNSAT authority | **FAIL** | Preserve accepted SAT-source counterexample |
| Historical /386 | **RESTRICTED** | Guarded odd-charge domain only |
| P versus NP | **OPEN** | No separation or general polynomial-time decider |

**Next weakest lemma.** TMR-2: propose an adaptive dynamic residual SAT obstruction after *all* Gaussian and compact shared-circuit quotients. TMR-3: verify truly simultaneous last-bit-read/output HALT is not double charged. TMR-4: independently replay the $r(C)$ all-step abstraction and exact rational LP, retaining any genuine MAY new input port. TMR-5: independently check last-bit SAT witness and source grammar; audit whether a richer physical source interface defeats the claimed model scope. Neither this report nor TMR-1/044 gives an unrestricted superpolynomial SAT time lower bound.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and canonical main.tex were fully read and not edited; TMR-5 retains manuscript synthesis ownership. Existing five TMR identities, schedules, enabled states and role ownership unchanged. P versus NP **OPEN**.

END_OF_TMR1_REPORT::045::LASTBIT045::2026-11-15_0606_PST
