# TASK-008: SLICE-UNSAT monotone lower-bound branch

**Status:** OPEN  
**Priority:** HIGH  
**Created:** 2026-10-04

## Goal

Determine whether a computationally hard fixed-weight slice of clause-presence \(UNSAT_{3,n}\) admits a superpolynomial monotone-circuit lower bound, so that Valiant's slice-function theorem can transfer the result to unrestricted Boolean circuits.

## Load-bearing target

For \(N=8\binom n3\), define the monotone slice function \(U_{n,t}\) that agrees with clause-presence \(UNSAT_{3,n}\) on \(|z|=t\), is 0 below the layer, and 1 above it.

Prove for an explicitly hard slice \(t=t(n)\):

\[
C_{\mathrm{mon}}(U_{n,t})=N^{\omega(1)}.
\]

## First deliverables

1. Exact statement and proof-hypothesis audit of Valiant's slice theorem.
2. Exact padding/hardness lemma for a fixed clause-count slice.
3. Reconstruction of the known full-cube monotone lower bound for \(UNSAT_{3,n}\).
4. Identification of the first proof step that fails on the Hamming slice.
5. Attempted repair using the current chain/correlation/clean-core decomposition.
6. Hostile tests against easy fixed-weight slices, Horn/2-SAT, Tseitin/parity, bounded treewidth, padding, and independent products.

## Guard

Do not infer slice hardness from full-cube monotone hardness. Do not claim a \(P\neq NP\) consequence unless both the slice hardness transfer and the superpolynomial monotone lower bound are proved.

Detailed plan:
\`research/explorations/monotone-slice/2026-10-04_SLICE-UNSAT_PLAN.md\`


## 2026-10-04 SLICEPAD1 update

**Padding/hardness phase:** CANDIDATE with complete elementary proof; independent review pending.

Two explicit hard layers are now available for target formulas on q=2n variables:

\[
t_{\mathrm{sp}}=6q
\qquad\text{and}\qquad
t_{\mathrm{mid}}=\frac{1}{2}\,8\binom q3.
\]

The construction adds n fresh control variables and pads with distinct clauses containing at least one positive control literal. Setting all controls to true satisfies every filler. The exact filler count satisfies

\[
M_{2n}-2R_n=\frac{n(n-1)(5n+2)}3>0,
\]

so more than half of all target clause coordinates are available as fillers. The middle exact layer is therefore NP-complete for SAT and coNP-complete for UNSAT. Using bounded-occurrence 3-SAT gives the sparse exact layer t=6q with the same hardness.

The sparse uniform exact layer also satisfies

\[
\Pr[\mathrm{SAT}]
\le
\left(2(7/8)^6\right)^q,
\qquad
2(7/8)^6\approx0.8975906372<1.
\]

**Critical negative result:** a nonconstant coordinatewise-monotone map cannot have constant output Hamming weight. Therefore the ordinary padding reduction is not a monotone projection, and the known full-cube monotone lower bound for UNSAT cannot be transferred through it. That direct route is retired.

**Current load-bearing target:**

\[
C_{\mathrm{mon}}(S_{q,6q})=M_q^{\omega(1)}
\]

or an intermediate set-circuit/communication theorem that genuinely advances toward it.

Artifacts:
- `research/explorations/monotone-slice/2026-10-04_1630_SLICEPAD1.tex`
- `experiments/monotone_slice/verify_slicepad.py`
- `results/raw/monotone_slice/SLICEPAD1_verify.txt`


## 2026-10-04 SLICEKW1 update

The communication target is now sharper.

For exact-layer UNSAT input (A) and exact-layer SAT input (B), the restricted monotone Karchmer-Wigderson relation asks for a clause in (A\setminus B). There is an immediate (q)-bit deterministic protocol: Bob sends any satisfying assignment (eta) for (B); Alice returns a clause of (A) falsified by (eta), which cannot belong to (B).

Therefore ordinary communication complexity is too weak to establish the desired circuit-size lower bound.

The correct next model is **DAG-like communication protocols**, whose minimum size exactly characterizes monotone circuit size. The next load-bearing target is

[
\mathrm{DAGKWsize}(R_{q,6q})=M_q^{\omega(1)}.
]

A successful superpolynomial monotone lower bound for this slice, combined with Valiant, would actually imply

[
\mathrm{NP}\not\subseteq\mathrm{P/poly},
]

not merely (P\ne NP). This calibrates the difficulty of the branch.

Artifact:
- `research/explorations/monotone-slice/2026-10-04_1650_SLICEKW1.tex`
