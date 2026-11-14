# TMR-5/006: no-unused-identifier repair for dense SAT/UNSAT one-bit sensitivity

**Date:** 2026-11-13 18:48 PST, America/Los_Angeles. **Role:** NEW TMR-5 Machine Bottleneck Redteam and synthesis. **Scientific status:** TMR-2/008 EPI8 even-parity identifier sensitivity is independently verified **PROVED/RESTRICTED** under its actual permissive unary-header grammar; the new no-unused-ID repair **TMR5-NUP6 is CANDIDATE pending TMR-1/TMR-2 peer review**. Executed finite evidence **COMPUTATIONAL**. An unrestricted SAT processing lower bound and P versus NP remain **OPEN**.

## Scope and exact new theorem candidate

Take a clause-minimally unsatisfiable proper 3-CNF $F$ with $M$ clauses and $t\ge3$ occurring variables. Proper means three distinct nonzero variable identifiers per clause. Use the explicit grammar $1^N0\,1^{M'}0$ followed by $M'$ three-literal records, each literal a sign bit and exactly $w=\lceil\log_2(N+1)\rceil$ identifier bits. **Strengthen this grammar by requiring every declared identifier $1,\ldots,N$ to occur in at least one clause**, on both the UNSAT base and every SAT neighbor.

Set

$$
w=\max\{2,\lceil\log_2(2t+2)\rceil\},\quad
N=2^w-1,\quad
\rho(i)=2i+(\operatorname{popcount}(i)\bmod 2).
$$

Rename all original $t$ variables injectively by $\rho$. Each $\rho(i)$ is positive, at most $N$, and has even binary Hamming parity. Let $U=[1,N]\setminus\rho([1,t])$, so $|U|=N-t\ge3$. Add $K=\lceil |U|/3\rceil$ **positive** proper 3-clauses using only variables from $U$: partition $U$ into triples, and if 1 or 2 identifiers remain, add one final triple using these and distinct earlier identifiers. Every identifier in $U$ occurs in at least one filler clause. Every filler clause has three distinct identifiers and is satisfiable whenever all but at most one of the $U$-variables are set to 1.

Call the resulting all-declared-IDs-used formula $F^\star$. It has $M'=M+K$ clauses, encoded length and source-sensitive count

$$
L=N+M'+2+3M'(w+1),\qquad Q=3M(w+1).
$$

**New candidate theorem:** $F^\star$ is UNSAT; changing any ONE of the $Q$ original (not filler) sign or identifier bits gives a valid *same-length*, proper, all-declared-variables-occurring SAT formula. Every correct total deterministic multitape 3-SAT decider $A$ with a fixed number $h$ of ordinary local read-only input heads must therefore satisfy

$$
T_A(F^\star)+1\ge Q/h.
$$

There is NO memory bound in this statement. All revisits, input copies, compact algebra, cache, sharing and recomputation are allowed. For a random-access input port, a separate correctly charged port theorem is necessary.

## Symbolic proof and previously missing grammar condition

1. Clause-minimal UNSAT implies every occurring variable appears in **at least two distinct clauses**. Otherwise, if variable $x$ appears only in clause $C$, a satisfying assignment of $F\setminus\{C\}$ extends by a choice of $x$ satisfying its sole literal, contradicting UNSAT. This prevents the original identifier from becoming unused after a one-occurrence identifier-bit mutation.
2. Renaming and positive filler cannot repair the UNSAT original, so $F^\star$ is UNSAT. Every declared identifier occurs: original IDs occur in renamed $F$, all others in the filler.
3. For any original clause $C$, minimality supplies assignment $\alpha_C$ satisfying every other original clause. Since $F$ is UNSAT, $\alpha_C$ necessarily falsifies $C$.
4. Flip one original sign bit. The selected literal becomes true under $\alpha_C$; assign every $U$-variable 1 to satisfy all filler clauses. The modified complete source is SAT and every declared ID still occurs.
5. Flip one original identifier bit. Its even-Hamming-parity ID becomes an **odd-parity ID** $j\in U$. This is nonzero: a positive even-parity binary word has at least two set bits, and a single flip cannot produce zero. It is at most $2^w-1=N$, distinct from the two unchanged IDs in the clause, and is present in the filler. Extend $\alpha_C$ by choosing $j$ to satisfy the altered literal, and set all other $U$-variables to 1. Each filler clause contains three distinct $U$-variables, at most one of which is $j$, hence every filler clause remains satisfied. The original ID remains present elsewhere by step 1, so the strict no-unused grammar holds. Only the selected source bit has changed.
6. On the UNSAT source, a deterministic correct machine must observe each of these $Q$ positions. Otherwise the original run and its opposite-label Hamming-one valid neighbor would be identical by induction on ALL configurations and input observations. With at most $h$ source-bit observations per physical transition, $T_A(F^\star)+1\ge Q/h$.

This proof is independent of TMR-2's particular GF(2) witness implementation. It repairs the explicit **no-unused-declared-identifier grammar gap** of TMR-2/008 without assuming a SAT oracle or compulsory solution enumeration. It does **not** prove a superlinear cost.

## Dense infinite cubic-prism instantiation

For the odd-charge cubic prism $G_r=C_r\square K_2$, $r\ge3$, the original TMR-5/005 and TMR-1/007 graph proof certifies clause-minimal UNSAT. It has $t=3r$ original variables and $M=8r$ original proper 3-clauses. Here $N<12r+3$, $K\le3r+1$, and the exact formulas above give

$$
Q=24r(w+1),\qquad
\liminf_{r\to\infty}\frac{Q}{L}\ge\frac8{11}>0.
$$

Thus the fixed-$h$ acquisition lower bound is $\Omega(L)$ even with the new strict grammar. The filler costs only $O(r)$ clauses. It is not a family of hard SAT instances: the authenticated canonical prism/GF(2) charge system has a cheap global parity invariant, and a fixed total deterministic algorithm can use a paid recognizer plus correct exhaustive fallback for other sources. No general polynomial SAT decider is claimed.

## Hostile controls and executed evidence

**Independent hosted-V8 implementation, not a wrapper around TMR-2/008:** exact source regeneration, all-declared-occurrence parser, independent spanning-tree solution of $G_r-v$ after one forbidden local tuple, complete serialized Hamming-one bit flips, and SAT witness validation. Executed over $r=3,4,6,8,12,24$ and two odd-charge vertices per $r$:

| Check | Actual result |
| --- | ---: |
| Complete strict no-unused source cases | 12 |
| Independently constructed clause-deletion witnesses | 912 |
| Original sign-bit SAT neighbors | 2,736 |
| Original identifier-bit SAT neighbors | 18,960 |
| All parsed same-length opposite-label SAT neighbors | 21,696 |
| Strict no-unused malformed-source rejections | 12 |
| Exhaustive nine-original-variable UNSAT assignments | 512 |
| Maximum encoded length | 7,341 bits |
| Observed minimum / maximum $Q/L$ | 0.673947 / 0.764070 |
| Failures | 0 |

A **separate locally executed native Python implementation**, not a JS wrapper, passed the same 12 cases, 912 deletion witnesses and 21,696 actual SAT neighbors, plus 24 malformed/structural negative controls and 512 exhaustive base UNSAT assignments. Its first negative-control probe accidentally deleted an ORIGINAL, rather than a filler, clause and failed the intended grammar rejection. The test harness was corrected to delete a filler clause with uniquely occurring identifiers, then completed successfully. This was a **test-control bug**, not a failed mathematical witness. The Python source and its raw JSON are local-only and are **not** claimed as shared GitHub artifacts. Neither run was a physical multitape-TM simulation. No native OS Node replay, LaTeX compilation or full repository preflight was executed.

**Readback-verified shared executable:** [experiments/tmr/tmr5_no_unused_padding006.cjs](../../../experiments/tmr/tmr5_no_unused_padding006.cjs), Git blob b5d2585bfa30c8bc4ad96f8aab6355193395b800. **Raw finite evidence:** [results/raw/tmr/2026-11-13_1848_TMR5_NO_UNUSED_PADDING006_RAW.json](../../../results/raw/tmr/2026-11-13_1848_TMR5_NO_UNUSED_PADDING006_RAW.json), Git blob e3680a08fa38450b99e41518454fa9f2cb55c8cf.

**Additional hostile models checked symbolically, not run as benchmarks:** repeated clauses break clause minimality; grouped and interleaved equality sources can have different access costs; two input heads and erasing INDEX change transport bounds; affine/Gaussian elimination defeats semantic-count processing conjectures. Horn, 2-SAT, bounded treewidth, arbitrary products, genuine full SAT fallback, arbitrary extension encodings and native physical transition tables were **not newly executed** here.

## Other-role independent audit and integrated dependency

TMR-4/006's sensitive-prefix MAY product has a valid **restricted conditional** core when the opposite-label $P$ is externally certified, the exact trace prefix has run, and every physical step observes at most $q$ input symbols: actual postprefix steps reveal at most $q$ fresh sensitive bits; all real terminals require $P$ fully observed. The abstract potential $\Phi=B+\lceil|P\setminus V_B|/q\rceil$ is lower-bounded by a concrete execution, with zero-cost stutters and goal edges allowed only under stated guards. This is **not** a proof of efficiently constructing $P$, nor a superpolynomial initial potential. Independent formal review of its exact published transition-graph implementation remains requested. Similarly TMR-3/007's same-CNF clause reordering is a serious source-locality falsifier; it defeats an ordering-independent crossing claim but does not contradict TMR-3/002's grouped encoding premise.

The strongest surviving general statement is still first-read input necessity on an explicit family, now extended to a stricter source grammar. The next missing arrow is a **representation-independent, post-acquisition computational cost** on arbitrary fixed uniform total SAT programs, valid with arbitrary polynomial workspace and enough to beat EVERY polynomial exponent. There is no such proved arrow. P versus NP remains **OPEN**.

## Provenance, primary literature and repo state

Read first and rechecked the replacement directive at SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Read both root trackers, with proof2.txt recovered by its authentic 1,051,196-character Git blob (SHA 930c5eeddafce656717f28055a7a9a755f44737c) because ordinary fetch returned a blank body. Read entire root main.tex via authentic 2,497,977-character Git blob 4e0dc7a81c3757289e87661b6df29e458cd03daa, AGENTS.md, CODEX.md, repository skill, issue #3 latest peer updates, and all five current TMR handoffs. Reviewed original TMR-2/008 code/raw, TMR-1/007, TMR-3/007, TMR-4/006, TMR-5/005 and historical LSPV-5/511 checker failure. Historical superseded allocation has no authority.

Primary literature verified at publisher/author pages: [1] Aharoni and Linial, *Minimal non-two-colorable hypergraphs and minimal unsatisfiable formulas*, JCTA 43(2):196-204 (1986), https://doi.org/10.1016/0097-3165(86)90060-9 (MU context only). [2] Buhrman and de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, TCS 288:21-43 (2002), https://doi.org/10.1016/S0304-3975(01)00144-X (decision-tree sensitivity, not TM-time exponent). [3] Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52:835-865 (2005), https://doi.org/10.1145/1101821.1101822 (bounded time-and-space exponent, not unrestricted separation). [4] Cousot and Cousot, *Abstract interpretation: a unified lattice model*, POPL 1977, https://doi.org/10.1145/512950.512973 (abstract semantic soundness context, not an existential superpolynomial potential).

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The new result adds a restricted countermodel/source-grammar repair but changes no all-program P1/P2 status. Both label correctness and full uniform quantifiers remain separate obligations. No tasks/schedules created, revived or modified.

**One next target:** TMR-1/TMR-2 should independently verify the new filler construction and its all-occurring-ID property on every Hamming-one neighbor; TMR-4 should determine whether a nontrivial post-acquisition cost potential can avoid the paid Gaussian-elimination fast path. TMR-5 must retain the OPEN all-algorithm bridge.
