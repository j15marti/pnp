# LEAD-0028 — PRE-A-MACRO-SHRINK1 literature attack, exact selectors, and hard controls

Timestamp: 2026-10-07 07:58 PT
Agent: LEAD
Global status: **P versus NP remains OPEN.**

## 1. Target

The live endpoint is the Williams SAT time-space product lower bound. The current sufficient compiler target remains:

- at most (N^{\eta+o(1)}) SAT children,
- each child size at most (N^{\theta+o(1)}),
- local work (N^{r+o(1)}),
- recursive closure (C=\max\{r,\eta/(1-\theta)\}),
- explicit-buffer space exponent (\rho=\max\{\sigma,\theta\}),
- and (C+\rho<2\cos(\pi/7)\).

The calibration pair ((\theta,\eta)=(2/3,1/3)) with (r=1,\sigma=0) gives (C+\rho=5/3).

The unresolved theorem is PRE-A-MACRO-SHRINK1: derive such a source-dependent shrinker from an arbitrary hypothetical polynomial-time exact SAT decider (A), without executing (A) on any current-scale SAT instance.

## 2. Literature checked

### Williams 2024 self-improvement
Williams, *Self-Improvement for Circuit-Analysis Problems* (STOC 2024), explicitly asks whether self-improvement can go all the way to (P=NP), and states that the current proof encounters bottlenecks before reaching the polynomial regime. This is the closest direct precedent and confirms that converting an arbitrary polynomial SAT algorithm into a fixed low exponent is itself an open self-improvement problem.

### Sparsification
Impagliazzo--Paturi--Zane sparsification expresses fixed-width CNF as a disjunction of (2^{\varepsilon n}) sparse formulas. This is valuable for exponential-time reductions but does not provide polynomial fanout plus fixed fractional encoded-length shrinkage. Making (2^{\varepsilon n}) polynomial requires (arepsilon=O(\log n/n)), while the sparsity constant deteriorates as (arepsilon\to0); in any case the lemma is not a (N^{1/3})-by-(N^{2/3}) macro-shrinker.

### Compression barriers
Fortnow--Santhanam and Drucker show that strong OR/AND instance compression for SAT has major complexity consequences. These results cannot terminate the present proof under the contradiction assumption (P=NP), because PH collapse is then absorbed, but they confirm that exact answer-preserving compression is a powerful object and cannot be inserted for free.

### Variable elimination
Subbarayan--Pradhan NiVER and Eén--Biere variable elimination give exact satisfiability-preserving source transformations and explicitly note the exponential-space/clause-growth risk of unrestricted Davis--Putnam variable elimination.

### Resolution lower bounds
Haken's 1985 pigeonhole lower bound gives superpolynomial/exponential resolution lower bounds for pigeonhole tautologies. Haken also notes that extended resolution has polynomial proofs for these formulas. Therefore resolution/DPLL-style elimination is a useful hostile boundary but not a general lower bound against stronger circuit/extension reasoning.

## 3. CLAUSE-DOM-SELECT1 — PROVED/EXACT

Let residual CNFs (R_1,R_2) be over the same remaining variables. If

[
\mathrm{Clauses}(R_2)\subseteq\mathrm{Clauses}(R_1),
]

then (R_1\Rightarrow R_2), so

[
\mathrm{SAT}(R_1)\vee\mathrm{SAT}(R_2)
=
\mathrm{SAT}(R_2).
]

Hence the stronger residual (R_1) can be deleted from an OR self-reduction frontier without any SAT query.

This is a genuine source-dependent, polynomially checkable Mahaney-like selector. It is much stronger than an algebraic/hash collision, because it has a direct SAT-preserving implication proof.

## 4. Finite dominance-pruning experiment — COMPUTATIONAL

At the depth leaving (\lceil n^{2/3}\rceil) variables, exact clause-inclusion dominance was compared with raw syntactic residuals and, for small live sets, exact semantic implication.

Representative (n=18) results:

| family | target (n^{1/3}) | raw residuals | clause-dominance frontier | exact semantic-implication frontier |
|---|---:|---:|---:|---:|
| planted 3-SAT | 2.62 | 463 | 144 | 1 |
| random 3-SAT | 2.62 | 228 | 110 | 5 |
| 2-SAT | 2.62 | 5 | 1 | 1 |
| Horn 3-CNF | 2.62 | 393 | 23 | 2 |
| 3-XOR CNF | 2.62 | 97 | 32 | 16 |
| bounded path | 2.62 | 5 | 2 | 2 |

Conclusion: exact syntactic implication is useful but nowhere near the Williams width target on the general-looking controls. Perfect semantic implication can collapse much further, but computing that implication is itself a semantic SAT-level operation and cannot be credited as free.

## 5. DP-BRANCH-MACRO1 — exact operations, computational heuristic

Built a source-only hybrid using only:
- unit propagation;
- subsumption;
- Davis--Putnam existential variable elimination;
- branching;
- clause-dominance pruning.

Every individual transformation is exact for satisfiability.

On small random/planted/Horn/XOR/path formulas, and on small Tseitin controls, the heuristic often reached the nominal (N^{1/3})-children / (N^{2/3})-child-size budget.

This is **not** asymptotic evidence: these finite instances simplify heavily.

## 6. Pigeonhole hostile control — candidate falsified

The same branch/eliminate compiler fails strongly on pigeonhole formulas.

Representative literal-count normalization:

| instance | (N) | child-count budget (N^{1/3}) | obtained frontier | child-size budget (N^{2/3}) | max child |
|---|---:|---:|---:|---:|---:|
| PHP(5,5) SAT | 125 | 5.00 | 22 | 25.0 | 24 |
| PHP(6,5) UNSAT | 180 | 5.65 | 44 | 31.9 | 31 |
| PHP(6,6) SAT | 216 | 6.00 | 96 | 36.0 | 40 |
| PHP(7,6) UNSAT | 294 | 6.65 | 107 | 44.2 | 80 |

Both SAT and UNSAT pigeonhole controls break the target. This aligns with the known resolution lower bound and shows that the source-only resolution/DPLL candidate is not the universal PRE-A-MACRO-SHRINK1 compiler.

## 7. RESOLUTION-MACRO-GUARD1 — PROVED/EXACT at stated scope

Any recursive macro-shrinker whose UNSAT execution can be unfolded into a resolution refutation with proof size polynomial in its charged total work cannot be the universal Williams-landing compiler: applying it to the pigeonhole family would yield polynomial resolution refutations, contradicting Haken's lower bound.

This guard applies to the declared DP/resolution/branching implementation. It does **not** rule out extended resolution, cutting planes, algebraic reasoning, arbitrary circuits, or arbitrary SAT algorithms.

## 8. BLACKBOX-MACRO-NOGO1 — PROVED/EXACT corollary of RECURCLOSE1 + Williams

Suppose a uniform exact macro-shrinker (R^{SAT}) uses (A) only as a black-box SAT oracle on strictly smaller instances. Since all exact SAT deciders return the same semantic bits, the shrinker is extensionally just a SAT-oracle self-reduction.

If its parameters satisfy the Williams landing inequality, recursively replacing those smaller SAT oracle calls by (R^{SAT}) itself gives an ordinary deterministic SAT algorithm in the forbidden Williams time-space region.

Therefore no such black-box Williams-landing shrinker exists.

[
\boxed{\text{Any successful PRE-A-MACRO-SHRINK1 must use the code of }A\text{ non-black-boxly.}}
]

This identifies a genuine nonrelativizing requirement rather than a stylistic preference.

## 9. PARTIAL-EVAL-K-CARRY1 — PROVED/EXACT accounting

The most direct non-black-box construction is to specialize the fixed code of (A) to a source formula (F), while leaving a block (y) symbolic, producing a circuit for

[
g_F(y)=A(F\upharpoonright y)=\mathrm{SAT}(F\upharpoonright y).
]

If (A) runs in (N^{K+o(1)}) time, standard time-unrolled circuit/tableau simulation has size

[
N^{K+o(1)}.
]

Tseitin/Cook--Levin conversion preserves this polynomial exponent. Thus lowering the number of symbolic inputs to (N^{2/3}) does not lower the encoded instance size to (N^{2/3}); the unknown exponent (K) reappears in the materialized simulation.

This is the non-black-box analogue of SELECTCHARGE1.

## 10. Current dichotomy

The literature and experiments now leave a sharper fork.

### Source-only / black-box transformations
They can be exact and useful on large subclasses, but a Williams-landing version is ruled out by the known endpoint itself; the concrete resolution implementation also fails on pigeonhole formulas.

### Non-black-box code specialization
This is the only surviving route consistent with the contradiction architecture, but naive Cook--Levin/Tseitin materialization carries the unknown exponent (K).

Hence the remaining red arrow can be stated as:

[
\boxed{
\text{compress/summarize the specialized computation of arbitrary polynomial }A
\text{ to fixed exponent }<\gamma
\text{ without materializing }N^K\text{ work.}
}
]

This is precisely the type of self-improvement bottleneck Williams 2024 identifies as open near (P=NP).

## 11. Next target

Build and red-team a **code-specialized macro DAG**:

1. fix a block (Y) of residual variables;
2. partially evaluate (A)'s code on the source formula with (Y) symbolic;
3. preserve the resulting computation as a DAG rather than a time-unrolled tableau;
4. search for exact source/code-dependent quotienting or repeated-state merging that reduces the materialized DAG to (N^c) with (c) independent of the unknown (K);
5. test DEAD/COPY/DELAY/INTERP/RECOMP wrappers immediately;
6. if all generic DAG compaction can be defeated by wrappers, record a formal wrapper-invariance no-go rather than treating syntactic code compression as load-bearing.

No P-vs-NP arrow is closed. P versus NP remains OPEN.

## References

- R. Ryan Williams, *Self-Improvement for Circuit-Analysis Problems*, STOC 2024.
- R. Impagliazzo, R. Paturi, F. Zane, *Which Problems Have Strongly Exponential Complexity?*, JCSS 63(4), 2001.
- S. R. Mahaney, *Sparse Complete Sets for NP*, JCSS 25(2), 1982.
- L. Fortnow, R. Santhanam, *Infeasibility of Instance Compression and Succinct PCPs for NP*, JCSS 77(1), 2011.
- A. Drucker, *New Limits to Classical and Quantum Instance Compression*, SICOMP 44(5), 2015.
- N. Eén, A. Biere, *Effective Preprocessing in SAT through Variable and Clause Elimination*, SAT 2005.
- S. Subbarayan, D. K. Pradhan, *NiVER: Non-Increasing Variable Elimination Resolution for Preprocessing SAT Instances*, SAT 2004.
- A. Haken, *The Intractability of Resolution*, TCS 39, 1985.
