# TMR-2/021: exact polarity-pivotal dichotomy on arbitrary proper 3-CNF

**Date:** November 14, 2026, 07:25 PST (America/Los_Angeles).
**Agent:** TMR-2 Information Necessity, j15marti/pnp main.
**New theorem:** TMR2-SCB21, **CANDIDATE/RESTRICTED** pending independent TMR-1/TMR-5 review. The proof below is symbolic and all-length in its declared clause-sign-edit model.
**Finite evidence:** COMPUTATIONAL.
**Unrestricted uniform 3-SAT superpolynomial processing lower bound and P versus NP:** OPEN.

## 1. Exact model and claim

Fix a completely explicit occurrence-list 3-CNF encoding with a signed bit per literal occurrence. The clause headers, variable IDs, lengths and other syntax remain fixed when one polarity bit is inverted. Each legal clause has exactly three distinct variable IDs. Repetition of clauses is allowed. Let

$$
F=\bigwedge_{i=1}^{m} C_i,\qquad
C_i=\ell_{i1}\vee\ell_{i2}\vee\ell_{i3},\qquad
H_i=\bigwedge_{h\ne i}C_h.
$$

Write $C_i^{(j)}$ for $C_i$ with only the $j$th literal negated, and $F_i^{(j)}=H_i\wedge C_i^{(j)}$. These are valid same-bit-length original-source inputs. Define $s(F)$ as the number of individual polarity-bit positions whose inversion changes the SAT/UNSAT decision label. Here $L=|E(F)|$ is the full encoded number of bits, not the variable count $n$ or clause count $m$.

**Theorem TMR2-SCB21 (candidate, all-length combinatorial proof).** The complete clause-by-clause behavior is:

1. **UNSAT side.** For each $i$, either *all three* sign bits in $C_i$ are pivotal, or none is. All three are pivotal **if and only if** $H_i$ is SAT. Consequently, with $e(F)=|\{i:H_i\text{ is SAT}\}|$,

   $$
   \boxed{s(F)=3e(F)}
   \qquad(F\text{ UNSAT}).
   $$

   For proper width-three 3-CNF with $n$ variables,

   $$
   s(F)\le 3\min\left(m,2^n,8{n\choose3}\right).
   $$

   In particular, UNSAT sign sensitivity is a multiple of three. This strengthens the earlier G20 upper bound into the exact essential-clause equality.

2. **SAT side.** For each $i,j$, the single-bit change makes the source UNSAT **if and only if**

   $$
   H_i\models
      \ell_{ij}\wedge\bigwedge_{k\ne j}\neg\ell_{ik}.
   \tag{SCB21-S}
   $$

   Thus the entire model set of $H_i$ agrees on the three variables of $C_i$, with **exactly the $j$th original literal true**. Necessarily $H_i\models C_i$, so $C_i$ is *logically* redundant, not merely removable without changing the satisfiability status. Each SAT clause has **at most one** pivotal polarity bit:

   $$
   \boxed{s(F)\le m}\qquad(F\text{ SAT}).
   $$

   If a satisfiable formula has fewer than three distinct backbone variables, then $s(F)=0$ for proper width-three clauses. The per-clause selector condition, rather than a generic backbone count, is the exact criterion.

This theorem is purely about valid **one-bit formula edits**. It does not impose an online input, a proof calculus, a one-pass machine, a fixed workspace bound, or a delayed query interface.

## 2. Proof including both decision labels

If $F$ is UNSAT and $H_i$ is UNSAT, every $F_i^{(j)}$ is UNSAT because it still contains the UNSAT conjunction $H_i$. Conversely, if $H_i$ is SAT, every assignment $a\models H_i$ must falsify the original $C_i$, since $F=H_i\wedge C_i$ is UNSAT. Consequently $\ell_{i1}(a)=\ell_{i2}(a)=\ell_{i3}(a)=0$. Negating any one literal makes $C_i^{(j)}(a)=1$ while all other clauses remain true. Hence **each** $F_i^{(j)}$ is SAT. This proves the UNSAT dichotomy and equality.

For any deletion-essential clause $i$, choose a witness $a_i\models H_i$. We have $a_i\not\models C_i$ and $a_i\models C_h$ for all $h\ne i$. For distinct essential clauses $i\ne h$, the witnesses differ because $a_i\models C_h$ but $a_h\not\models C_h$. Thus the number of essential clauses is at most the number $2^n$ of full assignments. It is at most $m$, and duplicate identical clauses cannot be deletion-essential, giving the bound of $8{n\choose3}$ distinct proper signed clauses.

If $F$ is SAT, then $H_i$ is also SAT. The modified formula $F_i^{(j)}$ is UNSAT precisely when **every** $H_i$-model falsifies $C_i^{(j)}$. The negation of the modified clause is exactly the conjunction in (SCB21-S). This gives equivalence, not merely necessity. All $H_i$-models then satisfy the original $\ell_{ij}$, so $H_i\models C_i$. Conditions (SCB21-S) for two distinct $j,k$ demand mutually contradictory literal truth assignments on the same distinct variable, and cannot both hold because $H_i$ is satisfiable. Therefore at most one sign bit in a SAT clause is pivotal.

## 3. What any unrestricted deterministic decider must read

For any fixed finite correct total deterministic 3-SAT machine $A$, starting from a standard read-only original-source input tape, a pivotal polarity bit $p$ **must actually be scanned** during $A(E(F))$. If not, couple the complete computation to the valid opposite-label input $E(F^{(p)})$: all finite-control, input-head, work-tape, caching, rereading, and output actions remain identical by transition induction. That contradicts both-label correctness. This is an input-aware argument on **two complete valid sources**; it never assumes correctness for artificial online continuations.

Thus $|Q_A(F)|\ge s(F)$ for physical input positions scanned by $A$ on that realization. It remains an **input acquisition** charge. A machine may read the bits once and compute a compact certificate. It is invalid to infer a superlinear runtime from the existence of many distinct witnesses, essential clauses or backbone variables. With a fixed number of locally moving source heads, counting source positions alone remains at most linear in $L$.

## 4. Hostile examples and failure of the unrestricted transfer

**UNSAT, all pivotal:** The proper three-variable formula with each of its eight polarity signatures exactly once is UNSAT. Each clause is deletion-essential, so all $24$ sign bits are pivotal.

**UNSAT, none pivotal:** Duplicate every one of those eight clauses. The formula remains UNSAT, but $H_i$ remains UNSAT after deleting any one occurrence, so $s(F)=0$.

**SAT, linearly many pivotal:** Let the source consist of signatures $001,010,\ldots,111$, with $001$ occurring $R+1$ times and each other signature once. The only missing signature is $000$. For $R\ge1$, flipping the appropriate sign bit of any $001$ copy fills that missing signature while leaving $001$ present, causing UNSAT. Hence $s(F)=R+1=\Theta(L)$ in its three-bits-per-record E3 encoding, even though a fixed 8-bit finite-control signature mask decides **all E3 sources in $O(L)$ time**. In an ordinary general occurrence-list encoding, the same family forces linear-bit acquisition but remains easy for a fixed total correct decider with a constant-size three-variable fast path and an arbitrary total correct general fallback.

**Falsification controls:** Horn formulas, 2-SAT auxiliary-clause encodings, XOR clauses with contradictory parity equations, disjoint UNSAT products, padding/duplication, renaming, finite-width path/tree structures and freely duplicated clauses do not require assignment enumeration to decide their labels. A universal lower bound must permit their compact or shared solutions. No such all-machine semantic charge has been proved.

The crucial asymmetry is structural: a SAT-to-UNSAT sign edit requires a **logically redundant, locally backbone-forced clause**, whereas an UNSAT-to-SAT sign edit requires a **deletion-essential clause**. Neither property creates a mandatory expensive internal reconstruction algorithm.

## 5. Actually executed finite evidence

**Published direct hosted V8 execution:** The exact CommonJS source evaluated 43,758 exhaustive clause multisets for all $n=3$ E3 formulas with $m\le10$, 3,000 deterministic random $n=4$, 1,500 $n=5$, 500 $n=6$ sources and four explicit cube/product controls. It checked **48,762** sources, **1,379,646** individual sign mutations, **6,290** SAT pivotal edits, **13,041** UNSAT pivotal edits, **4,347** deletion-essential clauses and **300** variable renamings, with **zero failed assertions**. All classifications used independently constructed complete model-set bitmasks, and the predicted clause-level relation was compared to direct modified-source satisfiability. Explicit controls: all-eight-unique, all-eight-double, repeated-neighbor SAT and disjoint double-UNSAT products. The direct published V8 script does **not** implement separate padded 2-SAT or Gaussian elimination algorithms.

**Independent native CPython local-only implementation:** Actual separate Python script evaluated **53,468** sources, **1,586,727** sign edits, **4,674** essential-clause witnesses and 346 renamings, plus local controls for forcing gadgets, XOR, 2-SAT padding, Horn, duplicates, disjoint products and bounded-path patterns. Its native run took approximately **8.46 seconds** of measured Python time, with zero failed assertions. **This independent Python source and raw file remain local-only and are not represented as published repository evidence.** Neither finite experiment is an arbitrary Turing-machine compiler or an asymptotic lower-bound proof.

Reproducible published source: [experiments/tmr/tmr2_sign_dichotomy021.cjs](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr2_sign_dichotomy021.cjs).

Immutable published summary: [results/raw/tmr/2026-11-14_0722_TMR2_SIGN_DICHOTOMY021_RAW.json](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0722_TMR2_SIGN_DICHOTOMY021_RAW.json).

## 6. Source scope, dependencies and project integration

Primary contextual sources (definitions and adjacent scope, **not claimed to establish SCB21**):

1. O. Kullmann, *An application of matroid theory to the SAT problem*, ECCC TR00-018, 2000, https://eccc.weizmann.ac.il/eccc-reports/2000/TR00-018/index.html . Minimal UNSAT and deletion necessity.
2. O. Kullmann, *Constraint Satisfaction Problems in Clausal Form II: Minimal Unsatisfiability and Conflict Structure*, Fundamenta Informaticae 109 (2011), https://doi.org/10.3233/FI-2011-429 .
3. B. Kiesl, M. Seidl, H. Tompits, A. Biere, *Local Redundancy in SAT: Generalizations of Blocked Clauses*, Logical Methods in Computer Science 14 (2018), https://lmcs.episciences.org/4915 . Satisfiability-preserving redundancy versus our stronger literal entailment.
4. O. Dubois, G. Dequen, *A backbone-search heuristic for efficient solving of hard 3-SAT formulae*, IJCAI 2001, https://ijcai.org/proceedings/2001/35 . Backbone terminology.
5. N. Nisan, M. Szegedy, *On the degree of Boolean functions as real polynomials*, Computational Complexity 4 (1994), https://doi.org/10.1007/BF01263419 . Boolean sensitivity background, not a physical multitape time lower bound.

Original project dependencies: TMR-2/019 exact valid opposite-label source rereading, TMR-2/020 E3 cube classification and G20 bound, TMR-1/021 fixed-machine and unrestricted bridge audit, TMR-3/019 restricted delayed-INDEX locality and TMR-5/018 representation-sensitive cost replay. No prior original report is overwritten. The obsolete LSPV role assignments in root tracker history are superseded by the authoritative 2026-11-13 replacement directive.

The proof1.txt / proof2.txt root chains were recovered at full authentic length (proof2 via Git blob), and full canonical main.tex was read from its Git blob. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The result strengthens a restricted information statement but closes no P1-01/P1-03/P1-04 or P2 all-machine arrow. Root main.tex remains reserved for TMR-5 synthesis, and no schedules were created, revived or modified. The hosted full-repository preflight executable and LaTeX build were not run.

**Peer audit requested:** TMR-5 to independently verify both directions of (SCB21-S) and the all-or-none UNSAT lemma. TMR-1 to check valid explicit encoding and same-machine quantifiers. TMR-3 to distinguish physically scanned bits from compulsory processing work. TMR-4 to test any cost-sound MAY abstraction against the finite-state E3 controller.

**Next target:** Derive or falsify a necessity of expensive **post-acquisition semantic processing** for unrestricted all-length 3-SAT computation, without a delayed query, a small-space premise, a restricted proof calculus or mandatory backbone reconstruction. This all-machine implication is OPEN.

END_OF_REPORT::TMR-2::021::2026-11-14_0725_PST
