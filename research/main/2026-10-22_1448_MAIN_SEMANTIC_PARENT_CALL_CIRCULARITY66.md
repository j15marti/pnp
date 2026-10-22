# SEMANTIC-PARENT-CALL-CIRCULARITY66

Timestamp: 2026-10-22 14:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

Scope: the two existing P-vs-NP routes and the independent P-vs-RP question. Circuit-SAT and the audited WRAPPER root are controls, not new proof spines.

## Repairs proposed before source review

1. **Nonlocal truth-table projection:** use the assumed SAT decider to compute a small exact semantic relation and encode that relation as small children.
2. **Solver-produced separator certificate:** let the assumed decider select a separator or decomposition that need not be syntactically evident.
3. **Witness-preserving component quotient:** replace high-treewidth source structure by a small exact quotient whose joint label reconstructs the parent.

The first has a trivial exact implementation but is circular when it calls the same decider on the full parent. The second cannot create a syntactic separator on the wall controls. The third remains the only live possibility, but must expose a sub-full-size construction with exact source-complete semantics.

## Repository sources reviewed after recording the repairs

1. EQUALITY-LOCALIZATION-MINOR-BARRIER65: exact occurrence localization preserves the source incidence graph as a minor, retiring equality splitting as a universal separator compiler.
2. SMALL-INTERFACE-EXACT-JOIN64: the target recurrence is valid for supplied logarithmic interfaces and square-root children.
3. SOURCE-JOIN-COHERENCE56: on the real 20-clause, 14-variable WRAPPER root, the wrapper boundary is two, but the natural source frontier is 14 and the greedy frontier is five; source equality cannot be omitted.

The independent 14:11 KST repository review also confirms that no unrestricted bridge is closed and recommends a nonlocal semantic contraction with wall/expander controls.

## Definition — charged semantic compiler

Fix a deterministic SAT decider \(A\). A compiler \(C^A\), on an ordinary parent encoding \(F\) of length \(N\), outputs a descriptor or child list \(D(F)\), and a fixed polynomial-time aggregator \(J\) satisfies

\[
SAT(F)=J(D(F)).
\]

Every source read, query to \(A\), descriptor bit, child bit, validation step, replay step and aggregator step is charged on the target machine.

The compiler is **parent-calling** if it invokes \(A\) on \(F\) itself, or on an instance of length \(N^{1-o(1)}\) whose certified running-time exponent is inherited from the parent scale.

## Lemma 66A — trivial semantic collapse is exact but circular

Run \(A(F)\). If it accepts, output the constant satisfiable child \((z)\); otherwise output the constant unsatisfiable child

\[
(z)\wedge(\neg z).
\]

Then the child label equals the parent label for every input. The transformation is uniform, nonlocal, hereditary in the vacuous constant-child sense, and destroys the incidence minor.

However, it has already executed the complete parent decision. If the certified time and space of \(A\) are

\[
T_A(N)=N^{c+o(1)},\qquad S_A(N)=N^{s+o(1)},
\]

the compiler's charged ledger contains \(T_A(N)\) and \(S_A(N)\) before the small child is used.

**Status: ESTABLISHED accounting identity.**

This is not a lower bound on \(A\). It says that this construction cannot certify a better exponent than the parent call it contains.

## Lemma 66B — the ARC exponent recurrence loses contraction

Without a full parent call, SMALL-INTERFACE64 targets

\[
c_{\mathrm{child}}=\max(1.1,\,0.6+c/2)+o(1).
\]

Adding one charged call to \(A(F)\) yields

\[
c_{\mathrm{parent}}=
\max(c,\,1.1,\,0.6+c/2)+o(1)\ge c-o(1).
\]

For every fixed \(c>1.2\), the child-only expression is strictly below \(c\), while the parent-calling expression is not.

Similarly, for \(s\ge 1/2\),

\[
\max(s,\,1/2,\,s/2)=s,
\]

so the intended space contraction disappears as well.

More generally, a call on length \(N^\beta\) contributes exponent \(\beta c\). A fixed contraction requires \(\beta<1\) bounded away from one. Merely reducing the instance to \(N/\operatorname{polylog}N=N^{1-o(1)}\) cannot provide a fixed fractional exponent decrease.

**Status: ESTABLISHED for the certified recurrence ledger.**

**RETIRED:** any purported ARC improvement whose semantic compiler first asks the assumed decider for the full parent label.

## Truth-table projection

For interface \(S\), the exact projection

\[
R_F(\alpha)=SAT(F\upharpoonright\alpha)
\]

is semantically sufficient. Computing all entries by invoking \(A\) on restrictions of size \(N^{1-o(1)}\) gives an exact table but inherits the parent-scale exponent and may also require \(2^{|S|}\) bits, matching CUTSET-TABLE-TRILEMMA58.

A viable projection repair must therefore build its descriptor from strictly smaller calls or source-local operations before the label is known.

**Status: exact semantics ESTABLISHED; exponent-improving construction OPEN.**

## Solver-produced separator certificates

If the certificate names an actual syntactic separator, wall inputs from BARRIER65 have no logarithmic separator tree to discover. \(P=NP\) may make the search for an existing certificate efficient; it does not make a nonexistent certificate exist.

If instead the certificate describes a semantic quotient, it falls under Lemmas 66A and 66B: verification must not obtain correctness by running \(A\) on the full parent.

**Status: RETIRED as a purely syntactic universal repair; OPEN only as a charged semantic quotient.**

## WRAPPER and Circuit-SAT control

SOURCE-JOIN-COHERENCE56 identifies the actual root at experiments/DOUBLE_WRAPPER_2026-10-07/example_dag.json. It has 20 clauses, 14 variables and 1,948 satisfying assignments. Its reported wrapper boundary two is not the source frontier: the audited source frontiers are 14 in natural order and five in a greedy order.

A semantic compiler cannot use the wrapper boundary as its complete state. It must either retain every live source influence or prove an exact quotient. Computing that quotient by first deciding the root is the circular construction above. Unique Tseitin traces do not change this accounting.

## MKTP route audit

The constant child and any descriptor containing \(A(F)\)'s answer are ordinary-KT LOW. The answer bit itself carries no ordinary-KT lower bound, and the computation time spent obtaining it must be charged. Thus semantic collapse does not supply the missing UNSAT-HIGH target or deterministic both-label SAT-to-MKTP generator.

**SAT-to-ordinary-MKTP status: OPEN.**

## RP audit

For a promised valid RP verifier, one accepting original random tape on a YES input suffices. A procedure that first deterministically decides the verifier's language and then emits an accepting tape or constant child is again parent-call circularity: it is a deterministic decider, not a derivation of one.

UNIVERSAL-SHIFT29 remains **ESTABLISHED restricted** for logarithmic coin backdoors and constant residual ANF degree. Extending it to every promised RP verifier remains **OPEN**.

No actual RP language outside P is produced, and no uniform simulation of every RP machine is proved.

## Finite accounting audit

The stdlib-only audit:

- generated 960 random CNFs on one through eight variables;
- computed each parent label by brute force;
- verified exact equality with the constant semantic child;
- checked the time identity on 91 exponent values \(1.0\le c\le10.0\);
- checked the space identity on 96 values \(0.5\le s\le10.0\);
- tracked the effective exponent of length \(N/\log N\) through \(\log_2N=128\).

Result: **2,311 checks, zero failures.**

The finite test validates the implementation and arithmetic only. Lemmas 66A and 66B are symbolic accounting statements, not class separations.

## Five-role ledger

| Role | Status | Single next discriminating test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | For one proposed both-label target, construct the best indexed evaluator including the parent-answer acquisition cost. |
| :12 P!=RP | **OPEN** | Reject any accepting-tape generator that first decides the whole language; run SAT-NO and direct-decider controls. |
| :24 ARC/FLMV | Parent-call semantic collapse **RETIRED**; arbitrary contractor **OPEN** | Produce exact semantic children using only calls of length \(N^\beta\) for fixed \(\beta<1\), with no full-parent oracle call. |
| :36 P=RP | UNIVERSAL-SHIFT29 **ESTABLISHED restricted**; general simulation **OPEN** | Verify the hitting list using original random coordinates after dummy padding and verifier replacement. |
| :48 synthesis | Circularity ledger **ESTABLISHED** | Require every semantic compiler to publish maximum query length, query count, source acquisition, validation and peak space. |

## Conclusion

Nonlocality alone does not solve the ARC gap. A semantic compiler can evade the incidence-minor barrier trivially, but if it learns the parent label through the assumed full-size decider, the desired time-space contraction vanishes. The live target is now narrower:

> construct an exact, all-input, hereditary semantic quotient from strictly smaller charged computations, with maximum query length \(N^\beta\) for some fixed \(\beta<1\), virtual bit access, and matched FLMV resources.

No root manuscript, automation or role assignment was modified.
