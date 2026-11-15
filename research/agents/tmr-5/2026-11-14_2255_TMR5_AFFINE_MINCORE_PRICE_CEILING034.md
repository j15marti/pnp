# TMR-5/034: Minimum inconsistent affine core, shared-DAG price, and multiscale ceiling

**2026-11-14 22:55 PST | MINCORE065 | PNP Machine Bottleneck Redteam**

**Status:** PROVED/RESTRICTED for the precisely defined affine source-bound binary-XOR proof system, independent peer mathematical review OPEN. Tests are COMPUTATIONAL. The unrestricted SAT algorithm-transfer gate, superpolynomial initial potential, and P versus NP remain OPEN.

## 1. Candidate and preselected falsifiers

**Candidate:** Independently reproduce TMR-1/037's exact native Q-XOR3 proof price of 2H for connected odd-charge cubic Tseitin, and generalize it to arbitrary inconsistent authenticated affine sources with shared proofs. Test whether all-scales obstruction charges may legitimately add across disconnected incompatible components.

**Falsifiers fixed before primary-source and corpus review:**

1. A legal shared ADD DAG refutes with fewer than twice the smallest inconsistent-source support.
2. A real smaller inconsistent component or affine shortcut defeats an additive all-components source charge.
3. The input authenticator accepts an incomplete four-clause parity block as a source equation.
4. A proof-event bound is mistakenly translated into physical SAT-machine transitions or into another proof calculus.

## 2. Qualified source system

Let $m$ authentic source equations over $\mathbb F_2$ be $a_i\cdot x=b_i$, with $a_i\in\mathbb F_2^n$ and $b_i\in\mathbb F_2$. Let $A$ be the matrix whose rows are $a_i$, and $b$ the column of right-hand-side bits.

Q-AFF uses exactly the native rule semantics of TMR-1/037's Q-XOR3: SOURCE(i) appends one authenticated input equation at price 1; ADD(j,k) appends the sum of two earlier proof lines at price 1, allowing arbitrary globally shared DAGs and repeated references; HALT(j) costs 1 and is allowed only when line j explicitly reads $0=1$. There are no free inference rules. This abstract general-affine-row system is distinguished from TMR-1/037's strict Q-XOR3 grammar, which accepts one **complete four-clause block** with three distinct variables per original XOR equation. Every authentic Q-XOR3 source is a Q-AFF instance; arbitrary affine rows or contradictory groups with identical triples are NOT automatically authentic Q-XOR3 sources.

For an inconsistent source define its minimum odd-dependence support:

$$
s(A,b)=\min\{|\operatorname{supp}(z)|:
 z\in\mathbb F_2^m,\ z^\top A=0,\ z^\top b=1\}.
$$

The minimum exists exactly when the source equations are inconsistent.

## 3. New theorem: exact optimal shared-DAG proof price

**MINCORE065-A.** For every inconsistent finite Q-AFF instance, including every inconsistent authenticated Q-XOR3 source,

$$
\boxed{\overline W_{\mathrm{Q-AFF}}(A,b)=2s(A,b).}
$$

**Lower-bound proof.** Assign provenance coefficients over the original source indices to each proof line. SOURCE(i) has the i-th unit vector, and ADD takes the mod-2 sum of its two operand provenances. The line submitted to HALT has a provenance vector z with $z^\top A=0$ and $z^\top b=1$. Therefore its transitive proof DAG contains at least $t\ge s$ paid SOURCE nodes, counting every shared paid identity once. Let there be $a$ binary ADD nodes in that DAG. Discard HALT and regard the operand arcs as undirected multigraph edges. Every contributing node is connected to the root. Thus the graph on $t+a$ vertices is connected and has exactly $2a$ operand edges, counting repeated operands. Consequently $2a\ge t+a-1$, or $a\ge t-1\ge s-1$. At least one paid HALT is required. Total cost is at least $s+(s-1)+1=2s$.

**Upper-bound proof.** Choose a size-s witness z, SOURCE its s original equations, combine them with s-1 binary ADD operations, and HALT on their sum $0=1$. This is a genuine proof of cost 2s, with no extra assumptions about an algebraic oracle or free source rows. QED.

**MINCORE065-B.** Every inconsistent source also satisfies

$$
\boxed{s(A,b)\le\operatorname{rank}(A)+1\le n+1,\qquad\overline W\le 2(n+1).}
$$

**Proof.** Choose a minimum-support odd dependency z with support S. If a proper nonempty subset U of S had zero sum of left-hand-side rows, then either U itself has odd right-hand-side sum or S minus U does. In both cases one obtains a smaller inconsistent support. This contradicts minimality. Thus S is a minimally dependent set of matrix rows, and removal of any one row leaves $|S|-1$ independent rows. Hence $|S|-1\le\operatorname{rank}(A)\le n$. Apply MINCORE065-A. QED.

For explicit original CNF encoding length L, the number n of distinct referenced variables is O(L). Hence every complete authenticated affine source possesses an O(L)-event refutation in this calculus. Gaussian elimination also constructs an inconsistent dependency in polynomial bit time after paid source parsing. This is NOT a result about arbitrary 3-CNF, ordinary Resolution, or a native Turing-machine transition count.

## 4. New authentic counterexample to adding independent multiscale burdens

For a disjoint union of connected cubic graph components $G_j$, with one complete authenticated XOR3 source group per vertex, the mod-2 vertex-edge incidence kernel is spanned by the all-one vector of each connected component. Each component has an odd charge parity or an even charge parity.

When at least one component is odd-charged,

$$
\boxed{s(A,b)=\min_{j:\;\oplus_{v\in V(G_j)}b_v=1}|V(G_j)|.}
$$

If all components have even charges, the input is satisfiable.

Take a six-vertex cubic prism and a disjoint eight-vertex cubic prism, each odd-charged. Every four-clause parity source block is authentic under Q-XOR3; the variable triples are distinct, and components use disjoint edge variables. The minimum native refutation uses only the six-vertex component: 6 SOURCE, 5 ADD and 1 HALT, for cost **12**. A proposed additive component count predicts 28 and is falsified by this real legal refutation. Adding satisfiable disjoint components does not increase the refutation cost. An UNSAT conjunction does not impose an obligation to refute *every* inconsistent conjunct: a single contradiction already establishes UNSAT.

For one connected odd-charge cubic graph on H vertices, its incidence kernel has exactly one nonzero vector, the all-ones vector. Therefore s=H and minimum price 2H. This independently reproduces the main TMR-1/037 result without prohibiting DAG sharing, repeated sources or reconvergence. TMR-3/037's separate fixed-format **binary-output serialization** model is unaffected.

## 5. Consequence for arbitrary fusion-Lipschitz tariff potentials

Let Phi be **any** all-step cost-sound potential for this precise Q-XOR3 source calculus, with genuine identity zero-cost closure and Phi(goal)<=0. Telescoping along the actual optimal proof gives

$$
\boxed{\Phi(C_0)\le 2s(A,b)\le 2(n+1)=O(L).}
$$

This conclusion requires no assumption that obstruction components decrease separately, no sign assumption beyond the actual potential inequalities, and no optimization of a particular LP. It is a whole-path upper ceiling on every legitimate potential's initial value. An initial multi-scale tariff value 28 on the two-prism instance cannot satisfy every local row because a price-12 proof reaches a terminal with nonpositive potential.

Real cheap proofs must remain under any conservative MAY abstraction. Removing the six-vertex contradiction from the proof graph, requiring all components to be refuted, or deleting an authentic XOR rule would change the selected system or its goal predicate, not constitute sound CEGAR refinement. Gaussian elimination, source sharing, extension or circuit macros can introduce further cheap routes in larger systems. The theorem cannot transfer to arbitrary correct deterministic SAT machines without an independently proved same-system simulation.

**Scope of the rank ceiling:** It blocks a superpolynomial initial potential for the **affine authenticated source family in Q-XOR3**, not for all SAT families or for a genuinely nonaffine fusion obstruction. It is not a polynomial-time algorithm for general SAT. The disjoint Q-TOTAL-XOR-RES authority also has the cheap XOR-mode proof on this family. Historical /341 is still FAIL as a full logical UNSAT authority, and /386 remains RESTRICTED.

## 6. Independent execution and hostile controls

Published, **byte-identical natively executed CPython**:
- Source: experiments/tmr/tmr5_affine_min_core065.py, Git blob 345485eac9d0625256421f3f6a933890cde44983.
- Raw stdout: results/raw/tmr/2026-11-14_2255_TMR5_MINCORE065_NATIVE_RAW.json, Git blob 73ae590a9e254193cb46b247d5eb5b0119dd8999.

The source checks **924 exhaustive small equation systems**, of which 607 are inconsistent, plus 1,600 deterministic seeded larger systems, including duplicate and redundant rows. An independent BFS finds minimum SOURCE/ADD/HALT event prices on small systems without assuming the 2s formula. Six connected cubic prisms at H=6,8,10,12,14,16 reproduce exact 2H. The two authentic disjoint odd prisms produce price 12 instead of proposed 28; an even-charge control is satisfiable. A contradictory duplicate triple plus 16 padding rows has price 4 only in the generalized Q-AFF grammar and is **not** asserted to pass Q-XOR3's unique-triple parser. Exactly **3,731 test assertions, zero failures**.

This is a semantic proof-event executor, not a physical Turing machine. Finite tests do not establish the all-length symbolic proofs. The finite prism graphs are not claimed to be expanders. Incomplete parity-four-clause, Horn, 2-SAT, bounded-treewidth, autarky, equality, learning, preprocessing, circuit, re-encoding and off-fragment 3-CNF operations remain real hostile controls for any proposed unrestricted transfer. The published theorem has no such transfer.

## 7. Sources, novelty and dependency map

[1] Eli Ben-Sasson and Avi Wigderson (2001), *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 149-169, https://doi.org/10.1145/375827.375835. It applies to ordinary Resolution, not an XOR-augmented calculus. Institutional source: https://cris.technion.ac.il/en/publications/short-proofs-are-narrow-resolution-made-simple-3/.

[2] Tero Laitinen, Tommi Junttila and Ilkka Niemela (2014), *Conflict-Driven XOR-Clause Learning*, https://arxiv.org/abs/1407.6571. This demonstrates why genuine XOR reasoning changes the proof system; no theorem from it is needed for our exact elementary counting.

[3] TMR-1/037, research/agents/tmr-1/2026-11-14_2156_TMR1_AUTHENTICATED_XOR_CALCULUS_QUALIFICATION037.md; original checker and native rule inventory inspected.

[4] TMR-3/037, research/agents/tmr-3/2026-11-14_2230_TMR3_XOR_BINARY_SERIALIZATION_TARIFF037.md; TMR-1/036, TMR-3/036, TMR-4/037 and TMR-5/033.

[5] LEAD-0029 October Lipschitz-squeeze failure, historical /341 and /386 materials, the controlling November 14 fusion tariff directive, the November 13 TMR replacement, both trackers, canonical main.tex, all current TMR handoffs, and GitHub issue #3.

**New relative to prior TMR work:** The arbitrary-affine exact minimum-price formula $2s(A,b)$, the rank-based $2(n+1)$ source-price ceiling, and a legal two-component authenticated XOR3 shortcut falsifying additive multi-UNSAT-component obligations. TMR-1/037's connected cubic 2H theorem is independently confirmed, not claimed as original.

| Dependency | Verdict | Next target |
| --- | --- | --- |
| Complete Q-XOR3 four-clause source grammar | PASS/RESTRICTED, peer review remains open | TMR-4 independent authenticator audit |
| TMR-1/037 exact 2H connected odd cubic price | PASS/RESTRICTED, independently reproduced | TMR-1 audit generalized proof |
| General exact 2s price and rank ceiling | PROVED/RESTRICTED, new peer review OPEN | TMR-2 audit minimal linear circuit proof |
| Additive disconnected odd-component burden | FAIL, real legal cheaper proof | Preserve existential refutation goal |
| Binary-output bit cost of TMR-3/037 | RESTRICTED, unchanged | Check compact alternate grammar |
| Superpolynomial affine Q-XOR3 initial tariff | FAIL on this exact family/class | Seek a genuinely nonaffine component |
| General-machine SAME-SYSTEM transfer | OPEN | Require all-step charged fixed-program bridge |
| Historical /341 full UNSAT authority | FAIL | Do not relabel |
| Historical /386 fragment | RESTRICTED | Do not extrapolate |
| P versus NP | OPEN | No root proof promotion |

**Weakest surviving target:** One dynamic nonaffine obstruction on an authentic concrete SAT machine or qualified proof system, remaining superpolynomial after every cheap affine source-core, sharing, learning and representation shortcut. TMR-4 should independently verify paid/zero closure; TMR-3 should audit finite-alphabet cost; TMR-1 should check the same-system quantifiers. A proof that every affine source requires superpolynomial native Q-XOR3 work is now **FALSIFIED** by the explicit O(L) refutation upper bound.

Root proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt (930c5eeddafce656717f28055a7a9a755f44737c) and main.tex (6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34) were read fully, recovering large files from authentic Git blobs after empty Contents bodies. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No schedules altered.

END_OF_REPORT::TMR5::034::2026-11-14_2255_PST
