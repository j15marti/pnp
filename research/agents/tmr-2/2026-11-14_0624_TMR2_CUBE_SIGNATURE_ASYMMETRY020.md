# TMR-2/020: exact SAT/UNSAT sign sensitivity, clause essentiality, and a linear-time falsifier

**Timestamp:** 2026-11-14 06:24 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity. **Mathematical claim:** CANDIDATE/RESTRICTED with complete proofs below, independent TMR-1/TMR-5 review pending. **Native finite execution:** COMPUTATIONAL. **Unrestricted P versus NP:** OPEN.

## 1. Source model and theorem

Use the original finite total deterministic multitape Turing machine model: one fixed program across all lengths, one locally moving read-only original input head starting at left endmarker 0, and all work tapes, writes, rereads, indices, preprocessing, recomputation and output charged. Let L be the encoded bit length, distinct from numbers of clauses and variables.

We analyze an explicitly restricted proper 3-CNF language E3 with **three fixed variables** x,y,z. Each input is an ordered list of m three-bit records, length L=3m. A record sigma=(sigma_x,sigma_y,sigma_z) denotes the proper three-distinct-variable clause

$$
C_\sigma=\ell_x\lor\ell_y\lor\ell_z,\qquad
\ell_i=\begin{cases}x_i,&\sigma_i=0,\\\neg x_i,&\sigma_i=1.\end{cases}
$$

The complete assignment a=sigma **uniquely falsifies** C_sigma. Every single record-bit flip remains a valid, same-length proper 3-CNF input. Lengths not divisible by three are MALFORMED. Let c_sigma be the multiplicity of signature sigma in the source, D={sigma:c_sigma>0}, and s(F) the number of original sign-bit positions whose individual inversion changes SAT versus UNSAT.

**Exact full classification TMR2-CUBE20:**

$$
F\in\mathrm{UNSAT}\quad\Longleftrightarrow\quad |D|=8.
$$

If F is UNSAT,

$$
\boxed{s(F)=3\sum_{\sigma\in\{0,1\}^3}{\bf1}[c_\sigma=1].}\tag{U20}
$$

If F is SAT and has two or more missing record signatures, s(F)=0. If F is SAT with **exactly one** missing signature a, then

$$
\boxed{s(F)=\sum_{j=1}^3 c_{a\oplus e_j}{\bf1}[c_{a\oplus e_j}\ge2].}\tag{S20}
$$

Here e_j flips only the j-th sign bit.

**Proof.** An assignment a satisfies the full source iff C_a is absent, proving the SAT/UNSAT classification. A single sign flip in a record of type b replaces precisely one occurrence of b with b xor e_j. When every type is present, the new source is SAT iff the removed b was its **last** occurrence; every singleton type has three pivotal positions. If at least two types are absent, introducing at most one new type cannot make the source UNSAT. If exactly a is absent, one bit flip makes it UNSAT precisely if b xor e_j=a and there is a second occurrence of b so that no previously present type disappears. Summing over those exact physical records proves S20. This is a full all-length combinatorial proof, not inference from finite tests.

## 2. New hard-looking SAT-side source-read family, and matching easy solver

Fix a=000 and adjacent b=001. Let F_R contain one each of signatures 010,011,100,101,110,111, then R+1 repeated records 001, with the **last** physical source record 001. For every integer R>=1,

$$
L_R=3(R+7),\qquad F_R\in\mathrm{SAT},\qquad
s(F_R)=R+1=\frac{L_R}{3}-6.
$$

The unique satisfying assignment is a. Changing the **physically last sign bit** changes the last 001 to missing 000, filling all eight signatures. The resulting formula is valid UNSAT. For EVERY correct deterministic original-input-local decider A on this grammar, identical-initial-configuration deterministic replay requires that A read that final cell on F_R; otherwise the two opposite-label runs would be identical. A locally moving source head starts at 0 and must traverse L_R cells, so

$$
\boxed{T_A(F_R)\ge L_R.}
$$

This is compulsory linear acquisition on a SAT family, not compulsory superlinear decision processing.

A fixed finite-state scanner solves **all E3 inputs** in O(L) transitions and zero visited writable work cells: it maintains an eight-bit mask of observed clause signatures and a three-bit finite-control phase register, reads the next physical bit, and adds the signature after each complete third bit. At the endmarker it rejects malformed incomplete records, otherwise returns UNSAT iff all eight mask bits are set. The number of control states is constant, independent of m. No oracle, unbounded word, hidden advice, assignment enumeration or uncharged read is used.

Under an ordinary explicit general 3-CNF encoding with identifiers, these remain valid proper formulas, and the source sign bits are legitimate opposite-label neighbors. ONE fixed total general SAT decider can recognize and solve any n=3 source by at most eight fully charged assignment scans, with an exhaustive correct fallback for all other n and malformed-input handling. It is polynomial on this family but not claimed polynomial on all 3-SAT inputs. Source-bit query lower bounds cannot by themselves exclude any polynomial exponent.

## 3. Exact UNSAT-side asymmetry, and a structural bound beyond E3

The formula comprising each of the eight clause signatures **once** is UNSAT, and all its 24 raw sign bits are pivotal: changing any sign produces SAT. If every signature is repeated at least twice, the result remains UNSAT while its individual sign sensitivity becomes **zero**, since every original signature remains present after a single flip. Formula U20 gives the **absolute upper bound s(F)<=24** for all UNSAT E3 instances, regardless of arbitrary clause count. At m=8 it is tight at 24; for m=9 the maximum is 21. The SAT family above has s(F_R)=Theta(L_R), so the two labels behave differently under raw single-sign-bit sensitivity.

**General essential-clause lemma G20.** Let F be any UNSAT proper three-distinct-variable CNF with n variables and m ordered clauses, under an explicit encoding in which changing a literal polarity retains all clause identities and variable IDs. Restrict s_UNSAT,sign(F) to those literal-sign bit flips that make SAT. Then

$$
\boxed{s_{\mathrm{UNSAT,sign}}(F)
\le 3\min\{m,\ 2^n,\ 8\binom n3\}.}\tag{G20}
$$

**Proof.** If flipping the sign of one literal in clause occurrence C_i makes the formula SAT, deletion of C_i must make it SAT. Such an occurrence is deletion-essential. For each essential clause choose a full assignment a_i satisfying every other clause. Since F is UNSAT, a_i falsifies C_i. Different essential occurrences i,j require different a_i,a_j because a_i satisfies C_j while a_j falsifies C_j. This injection bounds essential occurrences by 2^n. Identical duplicate clauses cannot be essential; the number of distinct proper width-three clause signatures is at most 8*binomial(n,3). There are at most m occurrences and at most three candidate sign flips per occurrence. This proves G20. For n=3 and m=8 the E3 full-cube example attains equality. The bound says nothing about multi-bit blocks, identifier changes, proof size or unrestricted 3-SAT time.

This is a statement about the clause-essentiality of specific physical source occurrences, not a general claim of efficiently finding the assignments a_i. It improves on prior TMR-2/019 only within the restricted information/sensitivity problem; previous project work already established linear valid SAT-label sensitivity with nine variables, and TMR-2/017 established block-query necessity with zero singleton sensitivity on a different UNSAT construction.

## 4. Executed reproduction and adversarial controls

**Published exact natively executed CPython:** experiments/tmr/tmr2_cube_signature020.py, Git blob 86de36517fd9e4c24d4a7ac99e1f0f2d6cef74ea. **Immutable exact raw JSON:** results/raw/tmr/2026-11-14_0622_TMR2_CUBE_SIGNATURE020_RAW.json, Git blob 2dd51dc27ac95e95e20d32bcc8339dd14f560659. Both are original, not peer wrappers; their uploaded bytes match local Git hashes. Reproduce with Python 3 by invoking the published script directly.

One native execution chunk ran for **18.022 seconds**. It exhaustively checked all **125,970 count multisets** of eight signatures with total clause records m=0 through 12, comparing U20 and S20 against **4,031,040 explicit one-bit source mutations**. Of those multisets 125,475 were SAT and 495 UNSAT. All formula/mutation assertions passed. Additional actual controls: nine SAT repeated-neighbor family lengths through L=1521 with physically final sign pivotal; seven UNSAT repetition examples through L=1200; 180 order shuffles; 880 independently implemented literal-by-literal eight-assignment tests; 48 renaming/sign-complement symmetries; eight 2-SAT ternary auxiliary truth-table checks; two Horn controls; three XOR/parity controls; 48 independent UNSAT-product nonadditivity controls; two randomized n=4 UNSAT G20 controls; nine malformed strings. Seed 20261114. Zero assertion failures.

The three-variable family has bounded treewidth and a tiny exact mask summary. Two independent UNSAT full-cube factors form a product in which flipping any one source sign leaves the **other** factor UNSAT; sensitivities do not add. XOR parity four-mask partitions each yield a SAT source, their union the trivial full-cube UNSAT source; no Gaussian-elimination lower bound follows. Padding and duplicate records change raw query geometry, not the semantic memory requirement. The Python code's sequential position loop is an input-head **observation audit**, not a generic charged physical Turing-machine compiler. Host Python string operations and brute-force mutation generation are external testing infrastructure. No general Gaussian solver, arbitrary-treewidth dynamic program, generic Turing-machine emulator, full repository preflight or LaTeX compilation was executed. Finite evidence remains COMPUTATIONAL.

## 5. Original corpus, primary sources, and status

**Authority:** First read and rechecked research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md, Git SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Older LSPV Route A/B assignments superseded, verified old counterexamples preserved. **Trackers:** complete proof1.txt 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and complete proof2.txt 1,051,196 characters recovered via authentic Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c. Blank Contents API body was not treated as an empty tracker. **Manuscript:** canonical main.tex recovered via full blob 2,536,131 characters, SHA f0054c990e11602b4b60ead3bccffa73f11d0d7b. Also read AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, latest issue #3, all five TMR handoffs and relevant ORIGINAL TMR-2/017, TMR-2/019, TMR-3/018, TMR-5/017, TMR-1/020 reports. No original solver or historical checker counterexample was erased.

Primary literature checked at its actual model scope:

1. Noam Nisan (1991), *CREW PRAMs and Decision Trees*, SIAM J. Computing 20(6), 999-1007, https://doi.org/10.1137/0220062 . Block/critical sensitivity in a restricted decision-tree/PRAM setting, not a general SAT-machine superpolynomial bound.
2. Harry Buhrman and Ronald de Wolf (2002), *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288(1), 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X . Query and certificate terminology, no unrestricted transfer.
3. Oliver Kullmann and Xishun Zhao (2013), *On Davis-Putnam Reductions for Minimally Unsatisfiable Clause-Sets*, Theoretical Computer Science 492, 70-87, https://doi.org/10.1016/j.tcs.2013.04.020 . Minimal UNSAT concepts, not the source of our independently proved injection G20.

**Duplication/contradiction audit:** Prior TMR-2/019 already had an n=9 infinite valid SAT-to-UNSAT sign-sensitive family. New material is the exact n=3 all-input classification, both-label formula, sharp unsat 24-bit barrier, general G20 essential-clause bound and **zero-workspace O(L) semantic scanner**. These strengthen a restricted falsification control, not any node proving P!=NP. **TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt or proof2.txt. Root main.tex remains TMR-5 owned, not modified here. No scheduled tasks created, revived or changed.

**Independent review request:** TMR-5 verify the exact U20/S20/G20 formulae and the physically final sign bit. TMR-1 audit full-encoding/quantifier scope; TMR-3 audit paid input moves and same-machine constant-state controller; TMR-4 test cost-sound mask-state abstraction with all source transitions. **Next open arrow:** a lower bound on compulsory SAT-versus-UNSAT semantic processing beyond complete source acquisition, robust to caching, sharing, XOR/Horn/2-SAT simplification, arbitrary rereads and arbitrary polynomial workspace. The all-A, all-k superpolynomial target and P versus NP remain OPEN.

END_OF_REPORT::TMR-2::020::2026-11-14_0624_PST
