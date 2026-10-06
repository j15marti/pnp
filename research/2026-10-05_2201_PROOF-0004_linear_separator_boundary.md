# PROOF-0004 — LINEAR-SEPARATOR-EQUIV1 / SCD boundary

**Status:** PROVED/EXACT in the stated finite Boolean range model.  
**Global status:** P versus NP remains OPEN.

## Formal statement

Let (R\subseteq \mathbb F_2^m) be nonempty. The following are equivalent:

1. There is a nonconstant affine Boolean function (D(x)=a\cdot x+b), (a\ne0), such that (D(r)=0) for every (r\in R).
2. (R) is contained in a proper affine hyperplane of (\mathbb F_2^m).
3. (\operatorname{aff}(R)\ne\mathbb F_2^m).

Whenever these conditions hold, (D) is exactly half-dense on (\mathbb F_2^m).

If (0\in R), then (b=0), so the condition is equivalent to
[
\operatorname{span}(R)\ne\mathbb F_2^m,
]
and the separator can be homogeneous linear.

## Proof

(1) => (2): (D(r)=0) gives (a\cdot r=b) for every (r\in R). Thus (R\subseteq H=\{x:a\cdot x=b\}). Since (a\ne0), (H) is a proper affine hyperplane.

(2) => (3): the affine hull of a subset of a proper affine hyperplane remains inside that hyperplane.

(3) => (1): choose (r_0\in R). Let
[
L=\operatorname{span}\{r-r_0:r\in R\}.
]
Since (\operatorname{aff}(R)=r_0+L) is proper, (\dim L<m). Choose nonzero (a\in L^\perp), and put (b=a\cdot r_0). For every (r\in R), (r-r_0\in L), hence (a\cdot(r-r_0)=0) and (a\cdot r=b). Therefore (D(r)=0). Since (a\ne0), (x\mapsto a\cdot x) is balanced, so (D) has density exactly (1/2).

If (0\in R), (D(0)=0) forces (b=0). Thus a nonzero homogeneous linear separator exists iff (\operatorname{span}(R)) is proper.

## SCD boundary corollary

Succinct constraint detection can efficiently find small-support dual constraints when they exist in the chosen ambient linear code/view. It does not by itself prove existence of a common parity separator for a final Boolean RMV range (R).

By LINEAR-SEPARATOR-EQUIV1, existence of such a separator is exactly an affine-rank deficiency statement about the final Boolean range. If
[
\operatorname{aff}(R)=\mathbb F_2^m,
]
then no affine parity separator exists, regardless of how efficiently constraints of an upstream code can be enumerated.

Therefore the Drive COMMON-LINEAR/SCD clue reduces to a construction-specific Booleanization obligation: prove that the exact final RMV output range lies in a proper affine hyperplane after every nonlinear/adaptive extractor and postprocessing step. Upstream Reed-Muller/Reed-Solomon linear constraints do not automatically survive those steps.

## Relation to existing project results

LSPV-2 WEDGE1 defines (W=\operatorname{span}_v S_v) for linear Hadamard slices. In the zero-containing union-of-subspaces model, the present theorem specializes to:
[
\text{common nonzero linear separator exists}
\iff
W\ne\mathbb F_2^m.
]
WEDGE1 further proves that if (W=V) and the exterior span is full, then no nonzero quadratic relation survives. PROOF-0004 isolates the degree-1 boundary without requiring the exterior-square condition.

LSPV-1 LEAF2 reports COMPUTATIONAL full degree-(le2) feature rank for tested nonconstant SU05/Hadamard leaves. In those finite tested models, full feature rank implies full affine span, so the common-parity route fails there. This remains computational evidence only, not an asymptotic theorem for the exact vMS Boolean output.

## Barrier audit

LINEAR-SEPARATOR-EQUIV1 is finite linear algebra. It **relativizes and algebrizes**. Oracle replacement does not break a load-bearing premise, and an oracle could expose the final range or affine hull directly. Thus this theorem is not the missing nonrelativizing/nonalgebrizing hinge and gives no runtime lower bound.

The result instead prevents a false Booleanization: a field/code-level linear relation cannot be promoted to a final Boolean separator without proving that it survives the actual encoder/extractor/postprocessing map.

## Hostile controls

- Affine/Tseitin: consistent; Gaussian elimination computes affine hull efficiently.
- Horn, 2-SAT, bounded treewidth: no runtime inference is made.
- Wrappers: any wrapper changing the final Boolean encoding can change affine rank and must be retyped. DEAD/DELAY source wrappers preserving the final range leave the theorem invariant.
- Padding: adding fixed output coordinates creates trivial affine constraints and must not be mistaken for hardness.
- Nonlinear extractor/adaptive query selection: may destroy upstream affine constraints; exact final coordinates are required.

## Strict status

- LINEAR-SEPARATOR-EQUIV1: **PROVED/EXACT** in the stated Boolean range model.
- SCD as an existence theorem for a final RMV separator: **NOT ESTABLISHED**.
- Exact final RMV affine-rank deficiency: **OPEN**.
- Arbitrary-algorithm CSE/source compiler: **OPEN**.
- FSC: **OPEN**.
- Nonrelativizing/nonalgebrizing transfer: **OPEN**.
- P versus NP: **OPEN**.

## Handoffs

**LEAD:** Treat the common-linear/SCD route as equivalent to proving construction-specific final Boolean affine-rank deficiency, not as a generic separator theorem.

**RED:** Attack any claimed affine deficiency after the exact nonlinear/adaptive extractor and final encoder. Remove padding/fixed-coordinate artifacts before interpreting deficiency.

**RESEARCH:** Search for primary results proving affine-hull deficiency of exact local-extractor/RMV output ranges after Boolean postprocessing, rather than SCD only for upstream linear codes.

**WRITE:** Keep the theorem in main2/main3 and mark the Drive SCD clue conditional on final-range affine deficiency.
