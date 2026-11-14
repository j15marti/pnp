# TMR-2 / 006: every polarity bit can be compulsory, but all-bit sensitivity is still cheap

**Run timestamp:** 2026-11-13 17:08 PST (America/Los_Angeles). **Role:** TMR-2, Information Necessity, under the superseding five-TMR directive. **New instantiated claim:** CANDIDATE pending independent TMR-5 review. Finite execution: COMPUTATIONAL. P versus NP and the all-exponent deterministic 3-SAT lower bound: OPEN.

## Exact theorem and transfer

Fix the source encoding from TMR-2/004-005: unary header $1^N 0\,1^M 0$ followed by exactly three signed, distinct variable identifiers per clause. Each literal has one independently encoded polarity bit and $w=\max(1,\lceil\log_2 N\rceil)$ identifier bits. Valid strict proper 3-CNF sources have length

$$
L=N+M+2+3M(1+w).
$$

The target machine is ONE fixed finite total correct deterministic multitape 3-SAT decider $A$ for ALL binary lengths; its read-only input is physically available for revisits, every source access/transition and every writable cell is charged, and it correctly rejects malformed input. No one-pass, solver-template, certificate-output or bounded-workspace assumption is imposed.

**General polarity-flip lemma (elementary symbolic proof).** Let $F$ be a clause-minimally UNSAT CNF with no tautological/repeated-variable clauses and with independent literal-polarity source bits. For each occurrence of a literal $\ell$ in clause $C$, let $F^{(C,\ell)}$ flip only that occurrence's polarity. Then $F^{(C,\ell)}$ is SAT. Hence, for any deterministic decider correct on both valid encodings $F$ and every $F^{(C,\ell)}$, the actual run on $F$ must inspect **each literal-polarity source bit**, even if it can reread the rest of the input arbitrarily often.

**Proof.** Since $F$ is minimally UNSAT, $F\setminus\{C\}$ has a satisfying assignment $\alpha$. Since $F$ itself is UNSAT, $\alpha$ must falsify $C$. In particular, every literal of $C$ is false under $\alpha$. Flipping any one literal makes its new value true while all other clauses remain true. Thus $\alpha$ satisfies the one-bit-flipped source. If the physical run on $F$ never observes the selected polarity bit, induction on complete concrete configurations (including fixed program, input-head positions, control and all writable tapes) shows that the run on the same-length flipped source follows the identical sequence and emits the same label. This contradicts UNSAT versus SAT. This induction does **not** identify distinct source prefixes merely because they share workspace, and it does not postulate correctness for arbitrary syntactic continuations: the explicitly constructed neighbor is valid. QED, subject to peer auditing of the machine interface.

For a standard machine with $h\ge1$ read-only source heads and at most one source symbol observed per head per transition, $T_A(F)+1\ge 3M/h$ (conservative initialization convention); for one input head, $T_A(F)=\Omega(M)$. This is a true all-correct-program **input-acquisition** lower bound, with no streaming restriction, but it is only linear in the number of sensitive input coordinates. It says nothing about compulsory retained memory or further computation.

## Explicit same-length opposite-label family

Use exactly the original odd-charge chained-XOR $K_m$ Tseitin sources $F_{m,b}$ of TMR-2/004-005, for every even $m\ge6$ and $\bigoplus b_v=1$. Original TMR-2/005's constructive lemma asserts that deleting **any** of the $M=4m(m-3)$ original clauses yields SAT, with a complete assignment falsifying only the deleted clause. The proof fixes that clause's forbidden XOR3 gate tuple, satisfies every other local gate, and solves the connected residual $K_m-v$ incidence system of even total charge. All forbidden-tuple extensions and the GF(2) incidence invariant are explicit in /005. This construction and the new polarity-flip implication jointly give, for **every** such $F_{m,b}$,

$$
N=\frac{3m(m-3)}2,\qquad M=4m(m-3),\qquad
P=3M=12m(m-3).
$$

There are exactly $P$ independently Hamming-one SAT neighbors obtained by flipping the $P$ distinct literal-sign source positions of the original UNSAT source. All neighbors have identical header, encoded length, variable identifiers, clause order and proper-width-three syntax. They need not remain inside the affine **promise class**: the universal decider must distinguish them because they remain valid arbitrary strict proper 3-CNF inputs.

$$
\forall A\text{ correct and total},\quad
T_A(F_{m,b})+1\ge \frac{12m(m-3)}h
=\Omega\left(\frac{L}{h\log L}\right).
$$

For our fixed machine model $h$ is a constant, independent of $L$. Thus the consequence is $\Omega(L/\log L)$, not a superlinear or superpolynomial time bound. A single fixed correct total machine authenticates the affine four-clause XOR3 groups and computes GF(2) consistency by paid Gaussian elimination in polynomial time, invoking a paid exhaustive fallback on off-family sources. In particular, **every literal sign can be individually decisive while the original global UNSAT computation is polynomial**. No oracle, unbounded word, advice table or prescribed refutation calculus is used.

This directly closes the source-validity gap identified in /005: deleting a clause alters the source length and alone proves no one-bit observation necessity; flipping a literal's sign preserves length and all validity conditions. It does NOT establish that every ID or unary-header bit is sensitive, or that all bits must be simultaneously stored.

## Executed reproduction, controls and limitations

Published standalone JavaScript:
- $\texttt{experiments/tmr/tmr2_polarity_bit_necessity006.cjs}$
- SHA: $\texttt{09514590e3d1fb73ce23d60daf071dbae6a862fc}$

Immutable V8 raw data:
- $\texttt{results/raw/tmr/2026-11-13_1708_TMR2_POLARITY_BIT006_RAW.json}$
- SHA: $\texttt{14d0c6fb7f86f69021e99a04654b275d88a8f489}$

**ACTUAL V8 execution:** 9 distinct odd-source cases for $m=6,8,10,12,14$ (the first four sizes with two odd charge vectors each and one new $m=14$ case), 5 even-charge SAT controls, **2,504/2,504** distinct clause-deletion full-variable certificates with exactly the selected clause false, and **7,512/7,512** distinct, actually constructed, parsed same-length single-bit SAT neighbors whose *complete mutated source clause set* was evaluated against its explicit satisfying assignment. All encoded-length/variable-ID/strict-proper validity controls passed; zero failed assertions. Largest source $L=17,481$, with 1,848 independent polarity-bit changes.

**Independent local Python implementation:** separately generated chained-XOR clauses and used a different GF(2) elimination/back substitution to verify **1,392/1,392** literal polarity flips across $m=6,8$, two charge patterns each. Zero failures. This Python code was not published and its result is secondary; the exact published standalone V8 source and raw JSON are the reproducible evidence.

**Hostile tests and limitations:** In each of the 9 V8 cases, the algebraic negative controls checked that an intact original odd system remains UNSAT when one flips a newly added duplicate clause; likewise the second untouched odd component of a disjoint product remains UNSAT. These are **symbolic negative controls**, not separate exhaustive SAT runs over the modified product. Renaming and clause ordering preserve the syntactic polarity-flip theorem by bijection. Adding unused variables does not destroy any original sensitive sign bit, but increases input length and can dilute the $P/L$ ratio. Even-charge affine systems are SAT and are not covered by the odd-UNSAT polarity-flip conclusion. A Gaussian algorithm recognizes the ORIGINAL affine family even though its one-bit neighbors are generally non-affine.

The hosted V8 executed the abstract source/witness auditor, **not** a physical Turing-machine emulator. Native Node CLI download, full repository preflight, report validator and LaTeX compilation were not executed; the connector environment does not expose a local repository checkout. The quantified theorem is a symbolic argument subject to independent TMR-5 review; the finite checks alone do not prove it.

## Primary literature and relationship to prior work

[1] H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science **288** (2002), 21-43. Author PDF: https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf . This paper defines deterministic adaptive bit-query trees and sensitivity on total Boolean functions; our specific valid-source argument is proved directly, not imported as a machine-time theorem.

[2] C. Lee, *On the Size of Minimal Unsatisfiable Formulas* (2008), https://arxiv.org/abs/0811.0427 . Context for clause-minimal unsatisfiability, not authority for the specific chained-XOR construction.

[3] D. Itsykson, A. Riazanov and P. Smirnov, *Tight Bounds for Tseitin Formulas*, SAT 2022, https://doi.org/10.4230/LIPIcs.SAT.2022.6 . Its regular-resolution and OBDD refutation lower bounds are restricted to those proof models and do not imply unrestricted SAT decision-time lower bounds.

[4] **Original project constructions:** TMR-2/004 $\texttt{research/agents/tmr-2/2026-11-13_1512_TMR2_CLIQUE_TSEITIN_COMPRESSION004.md}$; TMR-2/005 $\texttt{research/agents/tmr-2/2026-11-13_1623_TMR2_MINIMAL_TSEITIN_CLAUSE_NECESSITY005.md}$; historical exact four-clause XOR3 source compiler LSPV-1/452. This run uses their actual canonical clauses rather than inferring the result from abstract Tseitin parity alone.

## Project state, claims and next falsifier

Read the superseding 12:49 PST directive first, then root proof1.txt (full 28,714 chars, SHA $\texttt{06f7ebc8c2283304a0f5200b518c6e48fa41e343}$), proof2.txt recovered in full by authentic Git blob (1,051,196 chars, SHA $\texttt{930c5eeddafce656717f28055a7a9a755f44737c}$), root main.tex recovered by authentic Git blob (2,494,937 chars, SHA $\texttt{873daeec6e11d4a7448f3b0547c9ed1ccfebd805}$), AGENTS.md, CODEX.md, repository pnp-research skill, all newest TMR handoffs through TMR-1/005, newest issue #3 comments (1,956 total at inspection), relevant original /004, /005 and LSPV-1/452, and primary source [1]'s original PDF (including the decision-tree model page). The old LSPV role text in historical files remains historical; the replacement directive governs current ownership.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This scoped near-linear input-query necessity does not close [P2-00] or any unrestricted all-exponent transfer, nor does it establish P1-01/P1-03/P1-04. Root main.tex is TMR-5 synthesis-owned; no TMR-2 manuscript edit. No schedules or tasks created or modified.

**Precise TMR-5 peer check:** independently inspect original minimality certificates, the literal-sign single-flip in exact source bytes, both SAT/UNSAT labels, complete deterministic no-read coupling including the input head and pre-halt configuration, and the $h$-heads-per-step charge. Do not promote the source-sensitive $\Omega(L/\log L)$ statement into superlinear time, communication, memory or general P versus NP hardness.

**ONE NEXT TARGET:** identify whether any lower bound on *processing already-read source bits* can hold for all fixed total correct deciders without postulating a particular algebraic or proof representation. This requires all-transition computational charging beyond source observation, and must survive the genuine GF(2) fast path and arbitrary rereading/recomputation.

**Overall:** general representation-independent superpolynomial 3-SAT lower bound OPEN; P versus NP OPEN.

END_OF_REPORT::TMR2::POLARITY-BIT-006::2026-11-13_1708_PST
