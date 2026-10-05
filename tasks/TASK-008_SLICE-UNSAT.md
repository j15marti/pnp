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


## 2026-10-04 SLICEDENSITY2 correction

The preferred density is no longer (t=q).

Scott--Sorkin show that below the pure-literal threshold, rare UNSAT random formulas are typically explained by a unique minimal unsatisfiable subformula of the smallest possible excess. The random-3SAT pure-literal transition is about

[
c_{PL}\approx1.636.
]

Therefore density (c=1) lies in a known local/easy rare-UNSAT regime and is a poor primary positive-distribution target.

The revised rigorous window is

[
\boxed{c_{PL}<c<3.52.}
]

A concrete working slice is

[
\boxed{t=\lceil3.4q\rceil.}
]

At this density:
- exact-layer SAT is still NP-complete by the padding theorem;
- uniform exact-layer formulas are SAT with high probability by the rigorous (3.52) lower bound;
- the known small-MUF characterization below the pure-literal threshold no longer applies;
- the structure of rare UNSAT formulas in this intermediate regime is explicitly unresolved in the literature.

### Revised P1

**INTERMEDIATE-CORE1:** characterize rare UNSAT exact-(lceil3.4qceil) formulas, first computationally at moderate (q), tracking:
- minimum UNSAT core size and deficiency;
- variable-degree and sign profiles;
- clause codegrees/overlap;
- incidence expansion;
- distinguishability by simple polynomial monotone statistics.

Only after finding a locally matched positive distribution should SAT-SUNFLOWER1 become the primary theorem target.

Artifact:
- `research/explorations/monotone-slice/2026-10-04_1950_SLICEDENSITY2.tex`


## 2026-10-04 INTERMEDIATE1 update

The primary rigorously safe slice is now

\[
t=\lfloor 3.5q\rfloor,
\]

which remains below the known (3.52) random-3SAT satisfiable regime while staying above the pure-literal regime.

### Exact structural result: first-order camouflage

Let (G=S_q\ltimes(\mathbb Z_2)^q) act by variable permutations and independent complementation. Any nonempty (G)-invariant exact-(t) family has identical clause-coordinate marginals (t/M). In particular uniform exact-layer UNSAT satisfies

\[
\Pr[C\in A]=\frac tM
\]

for every proper clause (C), and therefore exactly matches the uniform layer in expected variable degree, signed degree, and variable-pair incidence.

So the first possible distinguishing information is at pair order or above.

### Pair-orbit framework

Two clause coordinates are classified under (G) by
- (s): number of shared variables;
- (h): number of shared variables with opposite signs.

For fixed (C),

\[
n_{s,h}
=
\binom3s\binom{q-3}{3-s}2^{3-s}\binom sh
\]

with ((3,0)) excluded.

For a (G)-invariant distribution with pair probabilities (	heta_{s,h}),

\[
\frac M2\sum_{s,h}n_{s,h}\theta_{s,h}=\binom t2.
\]

### Degree-two monotone hostile statistic

Define

\[
T(A)=\sum_i d_i^+(A)d_i^-(A).
\]

Under the uniform exact layer,

\[
\mathbb E_0T
=
q\left(4\binom{q-1}{2}\right)^2
\frac{t(t-1)}{M(M-1)}.
\]

Every threshold (T\ge K) has polynomial-size monotone circuits. More generally, every threshold on the count of a fixed constant-order clause pattern family has polynomial-size monotone circuits. This is recorded as **LOCALPATTERN-GUARD**.

### INTERMEDIATE-PAIR1 computational result

Exact DPLL was checked against brute force on 500 small formulas. Then 5000 exact-layer formulas were sampled for each (q\in\{20,24,28,32\}), seed (5252+q).

Using the fixed predeclared threshold

\[
T\ge\mathbb E_0T+0.5q,
\]

balanced accuracy for distinguishing UNSAT from SAT was:

- (q=20): 0.7049
- (q=24): 0.6888
- (q=28): 0.7034
- (q=32): 0.6801

This is **COMPUTATIONAL finite-size evidence only**. No asymptotic pair gap is claimed.

A deterministic deletion pass found deletion-minimal UNSAT cores using most variables on average, but this does **not** rule out smaller MUFs and therefore does not answer the Scott--Sorkin open question.

### Literature corrections

- Scott--Sorkin's intermediate rare-UNSAT structure remains open and is now recognized as a direct structural dependency.
- Caragiannis--Gravin--Jiang's (k)-wise-independence theorem does not cover linear density from fixed-order moment matching.
- Ahmadi et al. quiet planting is retained only as an analogy for low-order camouflage, not a monotone-circuit theorem.
- ECCC TR25-124 is **RETIRED** as switching-lemma support: the author withdrew it on 2025-08-19 after recognizing a flaw in the main argument.

### New ranked queue

1. **PAIR-CAMOUFLAGE1:** measure and then match the full ((s,h)) pair-orbit vector, not only (T).
2. **INTERMEDIATE-MUF1:** on pair-camouflaged UNSAT samples, search for smaller MUFs using multiple deletion orders and exact search at smaller (q).
3. **SAT-SUNFLOWER2:** attempt a 3CNF-specific approximation lemma only after low-order monotone distinguishers are neutralized.
4. **HIGHER-ORDER-GUARD:** enumerate order-3 signed-overlap pattern counts; any constant-advantage threshold gap is already a polynomial monotone distinguisher.
5. Switching and exact-weight lifting remain secondary; local lifting is retired by SLICELIFT2.

Artifacts:
- `research/explorations/monotone-slice/2026-10-04_2030_INTERMEDIATE1.tex`
- `experiments/monotone_slice/intermediate_pair_signal.py`
- `results/raw/monotone_slice/INTERMEDIATE1_pair_signal.txt`


## 2026-10-04 PAIR-CAMOUFLAGE2 update

A current literature search found no theorem characterizing pair correlations of random 3-SAT conditioned on rare UNSAT in the intermediate regime. Scott--Sorkin still leave the region between the pure-literal and satisfiability thresholds open. Caragiannis--Gravin--Jiang show that bounded k-wise independence does not control linear-density 3-SAT in the way needed here. Ahmadi et al. quiet planting is retained only as an analogy for low-order camouflage.

### Exact guard strengthened

Any polynomial-size exact-layer predicate P(z) can be embedded into the monotone slice extension

\[
H(z)=0\ (|z|<t),\quad
H(z)=P(z)\ (|z|=t),\quad
H(z)=1\ (|z|>t).
\]

Valiant then gives a polynomial-size monotone circuit. Therefore two-sided pair windows, likelihood scores, and other polynomial exact-layer classifiers are all legitimate hostile tests, not only one-sided monotone count thresholds.

### Full pair-orbit result

At density t=3.5q, 20,000 formulas per q for q=20,24,28,32 show a stable signed-overlap pattern:

- (1,0) same-sign one-variable overlap is depleted in UNSAT;
- (1,1) opposite-sign one-variable overlap is enriched in UNSAT;
- (2,0) is depleted;
- (2,1) is enriched;
- s=3 orbit counts are sparse and show no stable separation.

The (1,1) mean excess is roughly 0.8--1.0 SAT standard deviations across these sizes.

### Train/holdout pair camouflage

A separate 40,000-formula run per q used 20,000 SAT-training/UNSAT-training formulas only to calibrate six dominant pair-orbit means/SDs. A held-out formula was pair-camouflaged if all six dominant orbit counts lay within +/-1.5 SAT-training SD.

Held-out survival:

- q=20: SAT 0.4720, UNSAT 0.3684
- q=24: SAT 0.4612, UNSAT 0.3676
- q=28: SAT 0.4744, UNSAT 0.3504
- q=32: SAT 0.4767, UNSAT 0.2970

This is COMPUTATIONAL finite-size evidence only. If a constant survival gap persisted asymptotically, the pair-window predicate itself would be a polynomial-size monotone hostile distinguisher by the slice-predicate guard.

### Third-order probe after pair camouflage

Using

\[
U_3(F)=\sum_i
\left[
\binom{d_i^+}{2}d_i^-+
d_i^+\binom{d_i^-}{2}
\right],
\]

with threshold calibrated only from pair-camouflaged SAT training data, held-out balanced accuracy was:

- q=20: 0.5932
- q=24: 0.6034
- q=28: 0.5509
- q=32: 0.6496

The residual cubic signal is weaker and inconsistent in q. No asymptotic order-three gap is claimed.

### Pair-camouflaged multi-order core search

On a separate 20,000-formula run per q, each camouflaged holdout UNSAT formula was reduced under 20 randomized deletion orders. The smallest core found over those runs used on average:

- q=20: 30.97 clauses, 17.74 variables
- q=24: 38.77 clauses, 21.35 variables
- q=28: 46.17 clauses, 24.54 variables
- q=32: 56.22 clauses, 29.04 variables

Minimum variable counts found were 14,17,18,25 respectively. No tiny cores were found, but this does not prove minimum-MUF size.

### Revised next target

**PAIR-MATCH1:** construct a positive UNSAT distribution whose empirical distribution over the dominant pair-orbit cells matches the SAT exact-layer distribution, not merely a rectangular pair window. Then run all order-three signed-overlap hostile tests on fresh holdout data.

If that survives, combine it with stronger core search before returning to SAT-SUNFLOWER2.

Artifacts:
- research/explorations/monotone-slice/2026-10-04_2120_PAIRCAM2.tex
- results/raw/monotone_slice/PAIRCAM2_results.txt


## 2026-10-04 PAIRMATCH3 update

The next experiment replaced rectangular pair filtering by explicit nearest-neighbor pair matching.

### Exact new structural lemma

Three-clause signed-overlap orbits admit a complete canonical form. For a fixed ordering of three clauses, map each variable to its signed incidence vector in ({-1,0,+1}^3), quotient independent variable complementation by (vsim -v), sort the resulting normalized vectors to quotient variable relabeling, then minimize over the six clause permutations. This is complete for the action of variable permutations, independent variable complements, and clause permutations.

### Experiment A: nearest pair matching

For each (qin{20,24,28,32}), (N=6000) formulas were sampled at (t=3.5q). The first half calibrated SAT means/SDs for the dominant six pair coordinates. Every held-out UNSAT formula was greedily matched, without SAT replacement, to the nearest held-out SAT formula in standardized pair space.

Held-out balanced accuracy after matching:

- q=20: pair 0.551, cubic 0.564, sampled canonical triple-orbit 0.474
- q=24: pair 0.548, cubic 0.333, triple 0.333
- q=28: pair 0.500, cubic 0.458, triple 0.542
- q=32: pair 0.577, cubic 0.462, triple 0.500

The mean absolute residual mismatch per dominant pair coordinate was approximately (0.13)--(0.33) SAT standard deviations.

No stable order-three held-out advantage appears across q.

### Experiment B: tighter caliper

The run was repeated with independent seeds and caliper

[
d_{m pair}le0.75.
]

Surviving UNSAT counts were 41,32,29,13 for q=20,24,28,32. Pair mismatch fell to roughly (0.09)--(0.24) SD per coordinate.

Held-out balanced accuracy:

- q=20: pair 0.595, cubic 0.595, triple 0.548
- q=24: pair 0.500, cubic 0.563, triple 0.500
- q=28: pair 0.567, cubic 0.433, triple 0.700
- q=32: pair 0.500, cubic 0.643, triple 0.571

The isolated q=28 triple value 0.70 is not promoted: neighboring q values do not reproduce it and positive evaluation samples are only on the order of tens.

### Interpretation

**COMPUTATIONAL:** pair matching largely neutralizes the previously dominant second-order leakage.

**COMPUTATIONAL:** no reproducible third-order distinguisher was found in this run.

This does **not** prove order-three camouflage. The positive sample remains small and triple orbits were sampled rather than exhaustively enumerated.

### Revised queue

1. **PAIR-MATCH2:** increase rare-UNSAT sample counts, especially q=28,32.
2. **ORDER3-EXACT1:** at q=20,24, exhaustively enumerate all (inom t3) canonical clause-triple orbits on pair-matched formulas.
3. **MATCHED-MUF1:** stronger multi-start and exact/branch-and-bound minimum-core search on pair-matched positives at smaller q.
4. Only if exact order three remains quiet, advance to order-four guards or SAT-SUNFLOWER2.

Artifacts:
- `research/explorations/monotone-slice/2026-10-04_2250_PAIRMATCH3.tex`
- `experiments/monotone_slice/pair_match_order3.py`
- `experiments/monotone_slice/pair_match_caliper.py`
- `results/raw/monotone_slice/PAIRMATCH3_results.txt`


## 2026-10-04 ORDER3EXACT1 update

The low-order camouflage program now has an exact algebraic interpretation on the Johnson slice.

If two exact-layer distributions match every clause moment

\[
\mathbb E\prod_{i\in S} z_i
\]

for all (|S|\le d), then they give identical expectation to every multilinear polynomial test of degree at most (d). This is the elementary **MOMENT-CAMOUFLAGE** lemma. Filmus/Mossel slice harmonic analysis and the Filmus--Ihringer/Filmus constant-degree junta results confirm that low harmonic degree is a natural structural hierarchy on the slice, but they do **not** imply that small general monotone circuits have low degree.

### Exact order-three census

Every retained pair-matched formula was exhaustively scanned over all (inom t3) clause triples using the exact canonical signed-overlap orbit representation.

Manual pilots:
- q=16: 14 matched UNSAT, 82 triple orbits, held-out score BA 0.643, logistic BA 0.571
- q=18: 12 matched UNSAT, 80 triple orbits, score BA 0.417, logistic BA 0.500
- q=20 tiny hostile check: BA 0.500
- q=24 tiny hostile check: BA 0.500

A concurrent stronger scheduled run at q=20 used

[
N=3000,qquad t=70,
]

with 38 holdout UNSAT formulas and 20 pair-matched survivors. It exhaustively enumerated all

[
\binom{70}{3}=54{,}740
]

clause triples per retained formula, observed 81 canonical triple orbits, and obtained held-out balanced accuracy

[
\boxed{0.45}.
]

Thus the q=16 value does not reproduce in the better-powered q=20 run.

### Matched core search

The stronger q=20 run used 50 randomized deletion orders per matched UNSAT formula and found:

[
\overline m_{core}=31.30,quad m_{min}=26,
\]

[
\overline n_{core}=17.85,quad n_{min}=15.
]

Manual multi-start runs similarly found:
- q=16: mean 13.67/16 variables, minimum 11
- q=18: mean 15.63/18 variables, minimum 14

These are cores found, not proofs of minimum MUS size.

### Current interpretation

**COMPUTATIONAL:** no replicated exact order-three distinguisher has been found after pair matching.

**OPEN:** asymptotic degree-three camouflage.

**OPEN:** proof that matched UNSAT formulas require large minimum MUS.

**OPEN:** circuit-to-low-degree/local approximation theorem for general monotone DAGs.

### Revised queue

1. **MOMENT-BALANCE3:** explicitly weight/reject samples so all degree-one and degree-two moments match on training data, then retest complete degree-three moments.
2. **ORDER3EXACT2:** increase q=20,24 matched positive evaluation counts further.
3. **MATCHED-MUF2:** exact/branch-and-bound MUS search at smaller q.
4. **SAT-SUNFLOWER2:** only after the exact order-three census remains quiet under larger samples.

Artifacts:
- `research/explorations/monotone-slice/2026-10-04_2355_ORDER3EXACT1.tex`
- `results/raw/monotone_slice/ORDER3EXACT1_results.txt`
- `results/raw/monotone_slice/ORDER3EXACT1_manual_pilot.txt`


## 2026-10-04 MOMENTBALANCE3 update

The pair-matching branch has now been strengthened from nearest-neighbor matching to explicit **pair-moment balancing**.

### Method

On the training split, let (Z(F)inmathbb R^8) be the standardized vector of the eight independent signed pair-orbit counts

[
(1,0),(1,1),(2,0),(2,1),(2,2),(3,1),(3,2),(3,3).
]

The SAT training distribution is exponentially tilted by

[
w_lambda(F)propto exp(lambdacdot Z(F))
]

so that its weighted mean exactly matches the UNSAT training mean in all eight coordinates.

Every reported solve reached maximum training pair-moment error at most about (4.4	imes10^{-11}).

The learned tilt is frozen before holdout evaluation.

### Runtime rule added project-wide

AGENTS.md and CODEX.md now require every individual Python experiment invocation to be designed to finish in roughly 30 seconds or less. Larger experiments must be split into independent/checkpointed stages or parameter/seed/input-size chunks, with intermediate results persisted. Increasing timeout is explicitly not a substitute for decomposition.

The active SLICE automation was also updated explicitly to enforce this rule. The active LSPV agents inherit it through their mandatory repository-governance preflight.

### Chunked runs

All sampling programs completed below 15 seconds:

- q=16, N=10000, seed 41616: 4.81 s
- q=18, N=12000, seed 41818: 8.44 s
- q=20, N=14000, seed 42020: 9.15 s
- q=24, N=16000, seed 42424: 14.06 s
- q=20 replicate, N=10000, seed 52020: 6.80 s
- q=20 replicate, N=10000, seed 62020: 6.69 s
- q=24 replicate, N=12000, seed 52424: 10.61 s

### Held-out pair balance

Primary chunks had maximum held-out pair-orbit residuals of

- q=16: 0.197 SAT SD
- q=18: 0.177 SAT SD
- q=20: 0.158 SAT SD
- q=24: 0.224 SAT SD

Pooling same-q replicate chunks while preserving train/holdout separation gave

[
q=20:quad max|Delta_{pair}|=0.126 {m SD},
]

[
q=24:quad max|Delta_{pair}|=0.126 {m SD}.
]

Effective weighted SAT holdout sample sizes remained large:
- q=20 pooled: ESS 3499
- q=24 pooled: ESS 3040

### Held-out cubic probes

Five predeclared cubic/local statistics were tested after pair-moment balancing.

Pooled q=20 standardized residuals:

[
(0.056,0.047,0.063,0.039,0.073).
]

Pooled q=24 residuals:

[
(-0.056,-0.082,-0.077,-0.090,-0.040).
]

The direction is not stable across q or replicate chunks. In particular, independent q=20 chunks changed sign before pooling, and a q=24 replicate moved the original negative vector close to zero.

**COMPUTATIONAL:** after explicit pair-moment balancing, the tested cubic local statistics show no stable replicated direction.

This does **not** prove degree-three moment equality or circuit indistinguishability.

### Exact algebraic interpretation

If two exact-layer distributions match every squarefree clause moment through degree (d), then every multilinear polynomial test of degree at most (d) has identical expectation under them.

MOMENTBALANCE3 currently matches the complete signed-permutation quotient of the empirical degree-two moment vector, not every individual monomial at finite sample size.

### Revised queue

1. **MOMENTBALANCE3-ORBIT:** with the frozen pair-moment tilt, compute the complete canonical degree-three orbit vector in bounded <30-second chunks.
2. **ORDER3EXACT2:** increase q=20,24 positive counts without violating the per-invocation runtime rule.
3. **MATCHED-MUF2:** stronger exact/branch-and-bound core search, similarly decomposed.
4. **SAT-SUNFLOWER2:** only after degree-three hostile tests remain quiet under moment balancing.

Artifacts:
- `experiments/monotone_slice/moment_balance3.py`
- `research/explorations/monotone-slice/2026-10-04_2040_MOMENTBALANCE3.tex`
- `results/raw/monotone_slice/MOMENTBALANCE3_results.txt`
