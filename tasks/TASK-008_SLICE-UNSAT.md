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


## 2026-10-04 SLICEDEPTH2 update

A symbolic restricted-model lower bound is now available on the sparse hard slice (t=6q).

Every UNSAT exact-(t) input is a minterm of the slice extension, and every SAT exact-(t) input is a maxterm. Therefore:

[
\mathrm{DNFsize}_{\mathrm{mon}}(S_{q,6q})
\ge
\left(1-\rho^q\right)\binom{M_q}{6q},
\qquad
\rho=2(7/8)^6<1,
]

and

[
\mathrm{CNFsize}_{\mathrm{mon}}(S_{q,6q})
\ge
\binom{7M_q/8}{6q}.
]

Both are

[
\exp(\Omega(q\log q))
=
M_q^{\Omega(M_q^{1/3})}.
]

This is a genuine unconditional lower bound for monotone depth two, but it does not control multi-level DAG sharing. It is therefore an intermediate baseline, not the load-bearing general monotone-circuit theorem.

Artifact:
- `research/explorations/monotone-slice/2026-10-04_1715_SLICEDEPTH2.tex`


## 2026-10-04 SLICENEXT1 literature reconciliation

The literature search materially changes the branch.

### New hostile controls and obstructions

1. **XOR-SLICE-EASY.** Full-cube 3XOR-UNSAT has exponential monotone circuit lower bounds via GGKS/GKRS, but every Valiant slice of 3XOR-UNSAT has polynomial-size monotone circuits because exact-layer XOR consistency is decidable by Gaussian elimination and Valiant removes negations. Therefore generic CSP hardness, Resolution width, or incidence expansion cannot imply slice hardness.

2. **Existing lifting has the wrong weight orientation.** In GKRS Lemma 7, Alice carries a sparse unsatisfiable source CSP while Bob includes all target constraints satisfied by one assignment. Alice is sparse and Bob is dense, while an exact slice requires equal weight.

3. **Output-inert padding cannot fix this.** Any Alice-only fresh coordinate is a legal KW answer; if it does not decode to a source answer, it cannot be used. Common/inert padding therefore cannot reverse the Alice/Bob weight gap.

4. **Proper-clause local bundle rigidity.** Distinct proper 3-clauses cannot imply one another, blocking the simplest local replication gadget.

5. **Generic robust-sunflower parameter barrier.** For any nonempty (t)-uniform family, the spread parameter is at most (M/t). The CKR theorem against a product negative distribution with expected size (ct<t) requires
[
r=Theta!left(rac{M}{t}log tight),
]
which eventually exceeds the maximum possible spread. The off-the-shelf theorem therefore cannot directly attack the full exact-(t) minterm family.

6. **Natural SAT negative distribution is not pseudo-independent.** Choosing an assignment and then a uniform (t)-subset of its satisfied clauses gives exact SAT negatives with uniform one-coordinate marginals, but the eight signed clauses on one variable triple can never all appear. Hence it fails the September 2026 pseudo-independence hypothesis for (kge8).

### New positive structure

For (t=6q), the exact UNSAT minterm family is (M/(2t)=Theta(q^2))-spread.

For every fixed (L), a (1-o(1)) fraction of exact-(6q) UNSAT formulas have **no UNSAT subformula of at most (L) clauses**, by Tarsi deficiency plus a direct union bound.

### Ranked queue

**P1: SAT-SUNFLOWER1.** Develop a SAT-specific robust-sunflower lemma for the large hard-core family with no small UNSAT cores, against the exact SAT-supported negative distribution.

**P2: SMALLCORE growth.** Extend fixed (L) to the largest useful (L(q)), using 2026 random-3CNF proof-complexity structure where applicable.

**P3: SLICELIFT1.** Try one solution-carrying exact-weight balancing gadget, then prove an impossibility theorem for a declared local gadget class if it fails.

**P4: restricted-model extensions.** Krieger prime-implicant, multislice-formula, and ranked-spreadness routes remain intermediate targets only.

Artifacts:
- `research/explorations/monotone-slice/2026-10-04_1805_SLICENEXT1.tex`
- `experiments/monotone_slice/slicenext_preflight.py`
- `results/raw/monotone_slice/SLICENEXT1_preflight.txt`


## 2026-10-04 SLICEDENSITY1 + SLICELIFT2 update

### Primary target changes from density 6 to density 1

The control-variable padding works for every constant density (c>2/3). For (q=2n), the bounded-occurrence source has (m\le 2q/3), so padding to

[
t_q=\lceil cq\rceil
]

preserves NP-completeness of exact-layer SAT and coNP-completeness of exact-layer UNSAT.

For (2/3<c<3.52), the uniform exact-(t_q) layer is SAT with high probability. The transfer uses the known random-3-SAT satisfiability lower bound below density 3.52 plus the fact that with (t=O(q)) and (M=\Theta(q^3)), the collision probability in the with-replacement model is (O(1/q)).

**Recommended primary slice:**

[
\boxed{t=q.}
]

This layer is computationally hard, while the uniform exact-layer distribution is already an asymptotically valid zero-input distribution. That makes it a better target for a SAT-specific approximation/sunflower lower bound than (t=6q).

### Local exact-weight lifting is ruled out

SLICELIFT2 formalizes the standard block-local KW gadget abstraction. If (V) has at least three source variants, Bob states have a surjective unique-violated-variant map (b:F\to V), and local soundness/completeness require

[
v\ne b(f)\Rightarrow A_v\subseteq B_f,
\qquad
A_{b(f)}\setminus B_f\ne\varnothing,
]

then constant per-block weights obey

[
\boxed{|A_v|<|B_f|.}
]

Therefore a block-separable exact-weight reduction cannot place Alice and Bob on the same Hamming layer. Proper 3CNF has eight variants per variable triple, so the theorem applies to the natural local encoding.

Only genuinely cross-block/nonlocal balancing remains for the lifting route.

### Current ranked queue

1. **DENSITY1-POSITIVE1:** construct a large, spread family/distribution of exact-(q) UNSAT formulas with no compact planted-pattern detector.
2. **SAT-SUNFLOWER1:** prove a 3CNF-specific sunflower/approximation lemma against the uniform exact-(q) SAT distribution.
3. **SMALLCORE growth:** quantify large-core structure for the chosen positive family.
4. **SLICELIFT-NONLOCAL:** only if a concrete cross-block balancing mechanism is found; local block gadgets are retired.
5. **Restricted-depth/formula extensions:** useful intermediate results, but lower priority than the general monotone DAG target.

New artifacts:
- `research/explorations/monotone-slice/2026-10-04_1840_SLICEDENSITY1.tex`
- `research/explorations/monotone-slice/2026-10-04_1900_SLICELIFT2.tex`


## 2026-10-04 DENSITYPOSFAIL1 update

The density-one branch now has a stronger positive-distribution guard.

### P/POLY positive-family barrier

If an exact-layer positive test family (mathcal Y_q\subseteq\binom{[M]}q) has polynomial-size unrestricted membership circuits, then its Valiant slice extension has polynomial-size monotone circuits. Therefore (mathcal Y_q) can be perfectly separated from every disjoint exact-layer negative family by a polynomial-size monotone circuit.

Consequences:
- fixed-deficiency minimally unsatisfiable classes are poor candidates because fixed-deficiency MU recognition is polynomial/FPT;
- a useful positive test family must itself resist compact nonuniform recognition.

### Naive hidden high-density core is retired

A natural candidate was:
1. choose (q/6) active variables;
2. choose (q) clauses on those variables, giving density six;
3. condition on UNSAT.

This is UNSAT with overwhelming probability, but it is easily distinguished from uniform density-one formulas by a polynomial monotone degree-profile circuit.

Let (H_6) count variables appearing in at least six clauses. Then asymptotically

[
H_6/q\to \Pr[\mathrm{Pois}(3)\ge6]\approx0.083918
]

for uniform density one, while for the planted active-core distribution

[
H_6/q\to \frac16\Pr[\mathrm{Pois}(18)\ge6]\approx0.166613.
]

The monotone predicate (H_6\ge0.12q) is polynomial-size: each local degree threshold is a constant-width monotone DNF and the (q) indicators are counted with a monotone sorting network.

So simple hidden relabeling of a dense UNSAT core is **FALSIFIED/RETIRED**.

### New primary constructive target

**DENSITY1-BALANCEDCORE1:** construct or rule out an exact-(q)-clause UNSAT distribution that:
- matches the uniform density-one variable-degree profile;
- matches low-order clause overlap/codegree statistics;
- has no small/fixed-deficiency recognizable UNSAT core;
- retains large-core/expansion structure;
- survives the 3XOR-SLICE-EASY control.

Artifact:
- `research/explorations/monotone-slice/2026-10-04_1925_DENSITYPOSFAIL1.tex`
