# SLICE-UNSAT: Monotone Slice Lower-Bound Plan

**Date:** 2026-10-04  
**Status:** OPEN RESEARCH BRANCH  
**Repository:** \`j15marti/pnp\`  
**Canonical target:** fixed-weight slices of clause-presence \`UNSAT_{3,n}\`

## Objective

Revive the earlier genuine monotone-circuit lower-bound work in a form that can potentially transfer to unrestricted Boolean circuits without requiring an ad hoc "arbitrary SAT solver -> monotone circuit" bridge.

The central established bridge is Valiant's theorem that negation is essentially powerless for Boolean slice functions. Therefore the proposed target is:

\[
U_{n,t}(z)=
\begin{cases}
0,&|z|<t,\\
UNSAT_{3,n}(z),&|z|=t,\\
1,&|z|>t,
\end{cases}
\]

where the coordinates of \(z\) indicate presence/absence of the \(8\binom n3=\Theta(n^3)\) possible proper signed 3-clauses.

The branch succeeds at the circuit level if one proves, for a suitable hard slice \(t=t(n)\),

\[
C_{\mathrm{mon}}(U_{n,t})=N^{\omega(1)},\qquad N=8\binom n3.
\]

Valiant then transfers this to a superpolynomial lower bound for unrestricted Boolean circuits for the slice function, subject to verifying the exact theorem hypotheses and the hardness/padding statement for the chosen slice.

## Established ingredients

1. **Clause-presence UNSAT is monotone.** Adding clauses cannot turn an unsatisfiable CNF into a satisfiable one.
2. **Full-cube monotone lower bounds exist in this vicinity.** Known monotone lower-bound machinery yields strong lower bounds for explicit monotone functions related to 3-CNF unsatisfiability.
3. **Valiant slice simulation.** For Boolean slice functions, unrestricted circuits can be converted to monotone circuits with only low overhead. This is the key pre-existing bridge.
4. **Earlier CCF/minimal-clause geometry.** The clause-presence UNSAT function has a natural monotone CNF indexed by assignments. This supplies a useful maxterm/minterm geometry but does not by itself prove a general monotone DAG-circuit lower bound.
5. **Current 3-SAT structural decomposition.** The Liu/chain work separates local pruning, direct pair/triple correlations, high-degree outside mediators, and a residual low-degree externally mediated clean core. These may provide structural coordinates for a monotone lower-bound measure.

## Known barrier

Do **not** infer slice hardness from full-cube monotone hardness.

Canonical monotone functions can become easy on fixed Hamming layers. In particular, known work on slice functions shows that obvious candidates such as CLIQUE do not automatically preserve their full monotone hardness on the canonical slice.

Therefore the load-bearing theorem is not

\[
C_{\mathrm{mon}}(UNSAT_{3,n})\text{ is large},
\]

but specifically

\[
C_{\mathrm{mon}}(U_{n,t})=N^{\omega(1)}
\]

for an explicitly chosen \(t=t(n)\) whose slice retains the required computational hardness.

## Research plan

### Phase 1: exact theorem import and hardness statement

1. Reconstruct Valiant's slice theorem with exact quantifiers, input convention, monotonicity convention, size measure, and additive overhead.
2. Define the exact clause universe and \(U_{n,t}\).
3. Prove or refute a polynomial-time padding/reduction that maps arbitrary 3-CNF UNSAT instances to an exact-\(t\)-clause slice for a useful \(t=t(n)\).
4. Track whether the resulting target is NP-hard, coNP-hard, or merely circuit-hard under the chosen reduction. Do not conflate these.

### Phase 2: reconstruct the full-cube monotone lower bound

5. Identify a published full-cube monotone lower bound applicable to clause-presence \(UNSAT_{3,n}\), including its exact function definition.
6. Reconstruct the proof line by line.
7. Mark the first step that fails after conditioning on \(|z|=t\).
8. Record whether the failure is combinatorial, distributional, approximation-theoretic, or due to loss of independent coordinates.

### Phase 3: import the current 3-SAT structural decomposition

9. On the exact-\(t\) layer, classify formulas by:
   - locally pruned chains,
   - direct pair correlations,
   - direct triple correlations,
   - outside-mediator degree profile,
   - low-degree externally mediated clean core.
10. Test whether these coordinates induce a monotone progress measure or gate approximation measure.
11. Determine whether the clean-core dichotomy can be rephrased as a positive/negative distribution separation suitable for approximation-method or robust-sunflower lower bounds.

### Phase 4: attack the slice directly

12. Start with \(t=\Theta(n)\), unless the hardness/padding lemma forces a different regime.
13. Attempt Razborov-style approximation and modern robust-sunflower machinery directly on the exact-weight layer.
14. Compare against Hrubeš-Pudlák fixed-layer unsatisfiability methods and determine precisely why their strong result for growing \(k\) does not close fixed \(k=3\).
15. Search for a 3-CNF-specific invariant unavailable in the generic \(k\)-CNF proof.

### Phase 5: hostile controls

Every proposed lemma must be tested against:

- easy fixed-weight CLIQUE slices;
- Horn, dual-Horn, and 2-SAT clause-presence slices;
- parity/Tseitin controls where algebraic structure defeats naive monotone intuition;
- bounded-treewidth formulas;
- padded and renamed formulas;
- independent products;
- duplicate/dead clause coordinates;
- random exact-\(t\) formulas;
- formulas engineered to preserve all local chain states while changing global satisfiability.

A successful hostile counterexample retires the lemma.

## Success thresholds

### Strong success

An unconditional theorem of the form

\[
C_{\mathrm{mon}}(U_{n,t})=N^{\omega(1)}
\]

for a slice with a rigorous hardness transfer.

### Intermediate success

Any of:

- \(N^{\Omega(\log N)}\) lower bound for a restricted but materially stronger circuit model on the slice;
- a theorem isolating exactly why the fixed-\(k=3\) Hrubeš-Pudlák route fails;
- a new slice-preserving reduction from a monotone-hard source;
- a structural theorem showing the low-degree externally mediated clean core forces a known hard monotone subfunction.

### Failure criteria

Retire a route if:

- the chosen slice admits a polynomial-size monotone circuit;
- the padding step destroys hardness;
- the full-cube lower-bound proof uses independence that provably cannot survive the slice;
- the proposed bridge applies only to monotone algorithms rather than arbitrary circuits;
- the argument silently assumes the result it is meant to prove.

## Relationship to the existing program

This is a separate lower-bound branch from the Liu exact-algorithm branch.

- **Liu/chain branch:** improve upper bounds for deterministic 3-SAT by exploiting formula structure.
- **SLICE-UNSAT branch:** turn formula structure into a lower-bound invariant on a fixed clause-count layer.

The two branches may share structural lemmas, especially the pair/triple-correlation hypergraph and the low-degree externally mediated clean core, but they have different proof obligations.

## Immediate next theorem

> **Slice Hardness/Padding Lemma.** Find an explicit \(t=t(n)\) and a polynomial transformation from arbitrary 3-CNF instances to the exact-\(t\)-clause layer such that satisfiability/unsatisfiability is preserved and the transformed clause-presence universe remains polynomially related to the original input size.

Only after this lemma is exact should the monotone lower-bound attack be treated as potentially relevant to \(P\neq NP\).

## Status guard

\(P\neq NP\) remains open. Existing monotone lower bounds, Valiant's slice theorem, and the current chain/correlation structure do not by themselves establish a lower bound for unrestricted 3-SAT circuits. The load-bearing missing statement is superpolynomial monotone hardness of a computationally hard fixed-weight 3-CNF UNSAT slice.


## 2026-10-04 progress: SLICEPAD1

The first planned obligation, exact fixed-clause-count computational hardness, now has a complete candidate proof in `2026-10-04_1630_SLICEPAD1.tex`.

Two targets are retained:
- sparse: \(t=6q\), technically closest to random-CNF and Hrubeš-Pudlák style methods;
- middle: \(t=M_q/2\), the clean central-slice formulation.

The direct attempt to transfer the known full-cube monotone lower bound through this padding is retired. Any coordinatewise-monotone map whose image lies entirely in one Hamming layer is constant, so ordinary padding hardness is not a monotone projection.

The next phase is therefore a direct set-circuit / monotone-Karchmer-Wigderson attack on the exact-layer transversal family

\[
\mathcal U_{q,t}
=
\{A\in\binom{\mathcal C_q}{t}: A\cap B_\alpha\ne\varnothing
\text{ for every assignment }\alpha\},
\]

using the exact intersection law

\[
|B_\alpha\cap B_\beta|
=
\binom{q-d_H(\alpha,\beta)}3.
\]
