# TMR-2/019: linear valid-label input sensitivity in an honest explicit 3-CNF encoding

**Pacific timestamp:** November 14, 2026, 05:12 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity. **New result:** TMR2-HSS19, **CANDIDATE/RESTRICTED**, complete self-contained mathematical proof, pending independent TMR-5/TMR-1 review. **Finite executable evidence:** COMPUTATIONAL. **Universal superpolynomial deterministic 3-SAT lower bound:** OPEN.

## 1. Scientific question and exact machine scope

TMR-2/017 exhibited an ordinary-formula disjoint *block* certificate with zero individual sign-bit sensitivity and an $\Omega(L/\log L)$ source-read requirement. TMR-2/018 exhibited almost-total input necessity for *malformed* one-bit neighbors of an exponentially padded syntax. Can a compact ordinary proper 3-CNF, without syntactic padding or malformed neighbors, force a linear number of *individual* opposite-label source-bit observations while nevertheless having an inexpensive uniform semantic algorithm?

Fix one explicit binary encoding $E$. An encoded formula with $n\ge3$ variables and $c\ge0$ ordered proper 3-clauses is the bit string

$$
E(F)=1^n0\;1^c0\;\prod_{i=1}^c\prod_{t=1}^3
 \bigl(\operatorname{bin}_{w}(v_{it})\,s_{it}\bigr),
\qquad w=\lceil\log_2(n+1)\rceil.
$$

Each occurrence ID lies in $\{1,\ldots,n\}$; $s=1$ denotes the positive literal and $s=0$ the negative literal. The three IDs within a clause are distinct. Clause ordering and duplicated clauses are allowed, and the number of clauses is part of the unary header. All other strings are malformed. This is a conventional explicit occurrence-list grammar, not a promise of free preprocessing, a compressed run-length encoding, or an exponentially inflated encoding.

A is **one fixed finite total uniform deterministic** multitape decider for ALL bit lengths, with one read-only locally moving original-input head initially at the left endmarker, fixed finite alphabet and control, finitely many locally moving writable work tapes, and three terminal labels SAT, UNSAT, MALFORMED. Count every input read, physical head step, parsing operation, buffer/index/tape cell, reread and recomputation. Let $Q_A(x)$ contain original source data-bit positions actually scanned during the complete halting execution. The claim below assumes no one-pass, online, small-workspace, proof-system or solver-template restriction.

## 2. The construction

Use **nine** variable IDs throughout, with $z=v_1$, $x=v_2$, $y=v_3$, and private forcing auxiliaries $u_z=v_4$, $v_z=v_5$, $u_x=v_6$, $v_x=v_7$, $u_y=v_8$, $v_y=v_9$.

For any three distinct variables $a,u,v$, define the four-clause forcing gadget

$$
G(a;u,v)=(a\vee u\vee v)
\wedge(a\vee u\vee\neg v)
\wedge(a\vee\neg u\vee v)
\wedge(a\vee\neg u\vee\neg v).
$$

The four assignments of $(u,v)$ show that $G(a;u,v)$ is satisfiable **if and only if** $a=1$. Likewise $G(\neg a;u,v)$ forces $a=0$. This is a strict proper-3CNF gadget, with three distinct variable IDs in each clause.

For every integer $m\ge1$, construct

$$
F_m=G(z;u_z,v_z)\wedge G(\neg x;u_x,v_x)
\wedge G(\neg y;u_y,v_y)
\wedge\bigwedge_{j=1}^m(x\vee y\vee z).
$$

Write all twelve forcing clauses first, followed by $m$ copies of the ordered pivot clause $(x\vee y\vee z)$. Their clauses are legal although the pivot clause is duplicated. The forcing gadgets mandate $z=1,x=y=0$ and leave their auxiliary variables freely selectable, so $F_m$ is SAT.

For each $j$, define $U_{m,j}$ by changing only the sign of the $z$ occurrence in pivot clause $j$, yielding $(x\vee y\vee\neg z)$ there. All forcing gadgets still require $x=y=0,z=1$, falsifying that clause, hence $U_{m,j}$ is UNSAT. **Both strings are valid encodings of proper 3-CNFs of the same length and clause count**, and differ in exactly one original source bit. No malformed-output assumption is needed.

Here $n=9$, $w=4$, $c=12+m$, every encoded clause occupies $15$ bits, and

$$
L=|E(F_m)|=10+(13+m)+15(12+m)=203+16m.
$$

The sign bit of $z$ in the final pivot clause is the **last bit** of the entire input, position $L$.

## 3. Exact necessity theorem and proof

**TMR2-HSS19 (CANDIDATE/RESTRICTED, pending peer review).** For every correct fixed total deterministic machine A on encoding E and every $m\ge1$,

$$
\{p_{m,1},\ldots,p_{m,m}\}\subseteq Q_A(E(F_m)),
\qquad
|Q_A(E(F_m))|\ge m=(L-203)/16.
$$

If the input head starts at the left endmarker and moves at most one source cell per charged transition, then

$$
T_A(E(F_m))\ge L.
$$

**Proof.** Let $q$ denote the actual complete execution on $E(F_m)$. Suppose a pivot sign position $p_{m,j}$ was never scanned. Couple q with the execution on the same-length valid opposite-label string $E(U_{m,j})$. Their complete initial configurations agree except for this original-input cell. Induct on charged machine transitions: while the control, work tapes, all heads and all scanned input symbols agree, the deterministic next transition and every resource effect agree. Since the sole differing input cell is never read on q, the coupled execution follows the **same entire trace and terminal label**. This contradicts SAT on $F_m$ versus UNSAT on $U_{m,j}$. Each distinct pivot occurrence has its own sign bit; thus A must scan all $m$ of them. The final such sign is at input position $L$, reached only after at least $L$ locally moving source-head steps from the left endmarker. QED.

This proof refers to the complete original-input-aware configurations, **not** an invalid rule that equal intermediate workspaces erase differences in still-readable source input. It does not posit unrestricted correctness for arbitrary suffix continuations; the $m$ specific *valid* same-length opposite-label continuations suffice.

The same first part holds for any deterministic finite number $h$ of source heads, with exact per-head source observations; at least $m$ distinct positions must collectively be observed. The physical $T\ge L$ statement assumes locally moving input heads all initially at the left endmarker. Other input-access models require a separate charged translation.

## 4. Matching fully uniform easy algorithm and the transfer gap

There exists **one fixed total correct 3-SAT decider** $A_9$ on this entire E-grammar that, on every valid source with $n=9$, uses $T_{A_9}(x)=O(L)$ and $S_{A_9}(x)=O(L)$, including the constructed SAT/UNSAT neighbors. Parse/validate with a linear physical sweep, using a unary writable counter for the declared clause count and checking fixed-width occurrence IDs and within-clause distinctness. Then enumerate the **constant** $2^9=512$ assignments in finite control, rescanning the immutable source once per assignment and checking every clause; resetting and scanning are physically charged. Across 512 passes, time is $O(512L)=O(L)$ with a fixed program and no oracle. On any $n\ne9$, use an ordinary finite, total, fully paid exhaustive search fallback, which need not be polynomial. All binary inputs, including malformed inputs, halt correctly. No length-dependent advice or per-input program is used.

Thus this honestly encoded, all-valid-opposite-label family has an **asymptotically tight** $\Theta(L)$ source-geometry bottleneck for a correct standard machine, while it imposes **no superlinear necessary SAT processing cost**. Even one-bit sensitivity on a constant fraction of encoded bits is not evidence for P != NP. The global general-SAT behavior of $A_9$ is not claimed polynomial.

This strengthens the *scope of the counterexample* relative to TMR-2/018 by removing exponential padding and malformed neighbors, not the all-machine lower bound. The forced literals and duplicated pivot clauses are elementary constant-variable structure. Deduplication changes the encoding (and may destroy these exact occurrence coordinates); encoding-invariance of this **query** lower bound is not claimed. TMR-1/018's uniform polynomial-translation theorem concerns complexity-class membership, not preservation of individual source-bit sensitivity.

The overall target

$$
\forall A\;\forall k\ge1\;\forall C>0\;\forall L_0\;
\exists F\text{ valid},\ |F|\ge L_0:\
T_A(F)>C(|F|+1)^k
$$

remains **OPEN**. The construction proves the $k=1$ order only on a specialized family and, in fact, exhibits a single total correct machine running in $O(L)$ **there**. It cannot be used to exclude any polynomial exponent across all valid 3-CNFs.

## 5. Executed tests, raw evidence and limits

**Direct hosted V8 execution, COMPUTATIONAL:** 11 family sizes $m\in\{1,2,3,4,5,8,12,17,24,32,48\}$. Checked 11 SAT base strings, 156 distinct valid single-bit UNSAT neighbors, 234 independent solver-result comparisons (straight 512-assignment enumerator versus independently implemented 512-bit BigInt literal masks), 66 renamed controls with paired SAT/UNSAT, 44 malformed encodings, sixteen exhaustive forcing-gadget truth-table cases, sixteen three-variable XOR parity truth-table cases and one Horn satisfiable control. Maximum encoded length was 971 bits, maximum 60 clauses, and 11 final-position pivotal sign checks passed. **Zero assertions failed.** The source prints complete raw JSON when invoked with Node.

**Source:** `experiments/tmr/tmr2_honest_valid_sign_sensitivity019.cjs`

**Immutable raw:** `results/raw/tmr/2026-11-14_0512_TMR2_HONEST_SIGN_SENSITIVITY019_RAW.json`

**Reproduce:** `node experiments/tmr/tmr2_honest_valid_sign_sensitivity019.cjs`

Actual execution was hosted V8 in the connected code environment. The test does **not** constitute a native instruction-table Turing-machine implementation. No native Node process or independently authored CPython program was executed, and no bounded-treewidth DP, general Gaussian solver, full source-cache simulation, or large algebraic/circuit preprocessing benchmark was run. XOR truth tables and Horn controls test logical structure only, not those algorithmic costs. The statement for all $m$ rests on the symbolic proof, **not** finite testing.

## 6. Original evidence, literature and scientific status

- Original TMR-2/017 report: `research/agents/tmr-2/2026-11-14_0326_TMR2_SIGN_BLOCK_CERTIFICATE017.md`. The older example proves disjoint *multi-bit* block necessity while every singleton sign flip is inert.
- Original TMR-2/018 report: `research/agents/tmr-2/2026-11-14_0420_TMR2_PADDING_SYNTAX_CERTIFICATE018.md`. Its nearly-all-bit observation theorem concerns exponentially padded syntax; our construction concerns valid opposite-label CNFs of ordinary linear size.
- TMR-1/018: `research/agents/tmr-1/2026-11-14_0400_TMR1_PADDING_ENCODING_FRONTIER018.md`. Its polynomial-time encoding transfer preserves the **uniform P** question, not sign-coordinate query complexity.
- Noam Nisan, "CREW PRAMs and Decision Trees," *SIAM Journal on Computing* **20**(6), 999-1007 (1991), [DOI](https://doi.org/10.1137/0220062). Primary source for block sensitivity and query measures in the stated restricted models, not a general sequential 3-SAT time lower bound.
- Harry Buhrman and Ronald de Wolf, "Complexity Measures and Decision Tree Complexity: A Survey," *Theoretical Computer Science* **288**(1), 21-43 (2002), [DOI](https://doi.org/10.1016/S0304-3975(01)00144-X). Query-measure background; our fully input-aware deterministic coupling is independently proved above.

**Corpus/preflight:** Authoritative five-TMR replacement directive read first and rechecked before publication; current full proof1.txt read (28,714 characters; blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), full proof2.txt recovered via blob (1,051,196 characters; blob 930c5eeddafce656717f28055a7a9a755f44737c), full canonical main.tex recovered via blob (2,533,636 characters; blob 867c9b7512a51d59a50c479e81dda6c65615026f), AGENTS.md, CODEX.md, repository skill, issue #3 through TMR-5/016, all five current TMR handoffs, and original reports above. The Contents API's blank proof2/main bodies were **not** treated as empty stored files. Legacy proof-calculus checker falsifiers are preserved as unrelated historical evidence, not used as a machine lower-bound transfer. Full OS repository checkout/preflight and LaTeX compilation were unavailable. The present mathematical result does not change the status of any root proof-chain node.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt and proof2.txt. Root main.tex is reserved for TMR-5 synthesis and was not modified. No tasks or schedules were created, revived or modified.

**Requested independent audit:** TMR-5 should verify the forced-literal gadget, exact binary sign offsets, valid SAT-to-UNSAT single-bit neighbors, and the physically charged 512-pass uniform $n=9$ fast path. TMR-1 should review honest encoding and all-length malformed behavior. TMR-3 should audit same-input physical linear scanning and storage. TMR-4 should ensure a MAY graph preserving all actual source reads cannot claim superlinear necessity on this linear-time controller.

**Next single target:** Find or falsify a compulsory distinction-processing invariant that survives this $\Theta(L)$ valid-label sensitivity example, a cached complete source, and compact Horn/2-SAT/GF(2)/bounded-treewidth computation, while still quantifying over every correct fixed uniform unrestricted deterministic machine.

END_OF_REPORT::TMR-2::019::2026-11-14_0512_PST
