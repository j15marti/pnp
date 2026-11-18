# TMR-5/088: exact Fourier/flow FPT and all-arity affine audit

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Date:** November 18, 2026, Pacific Time. **Status:** independent symbolic theorems plus exact executed finite reproduction. Formal kernel/external mathematics review OPEN. **P versus NP OPEN.**

## Theorem 1: exact flow-space expression and FPT algorithm

For a directed multigraph (G) with (n) vertices, (m) arcs, and (c) weak components, put (r=m-n+c). The fixed template is (R(a,b)) iff (b-a pmod 5 in\{1,3\}). With (zeta=e^{2pi i/5}), (Lambda(k)=zeta^{-k}+zeta^{-3k}), and (B) the oriented vertex-edge incidence matrix over (mathbb Z_5),

[
  #operatorname{Hom}(G,T_5)
  =5^{n-m}sum_{kinker B} prod_{ein E}Lambda(k_e).
]

**Proof.** Expand each edge indicator as (5^{-1}sum_{k=0}^4Lambda(k)zeta^{k(x_{m head}-x_{m tail})}). Summing over every vertex variable annihilates every term except those with (Bk=0). Since rank (B=n-c), the flow space has dimension (r).

**Exact integer implementation.** Choose a spanning forest, enumerate all (5^r) assignments to the chord flow variables, and uniquely recover forest-edge flows by leaf balance. For each flow compute the product (prod_e(z^{-k_e}+z^{-3k_e})) in (mathbb Z[z]/(z^5-1)), using 5-element integer coefficient vectors. Sum the vectors to (S=(S_0,ldots,S_4)). Multiplication of every flow by a unit of (mathbb Z_5) permutes the flow set, giving (S_1=S_2=S_3=S_4). At a primitive fifth root, the polynomial evaluates to (S_0-S_1), so (#operatorname{Hom}(G,T_5)=5^{n-m}(S_0-S_1)), with exact integer division when (m>n). Arithmetic complexity is (O(m5^r)), using polynomial-bit-length integers. Thus exact counting and decision are FPT in underlying cycle rank (r), but no general polynomial-time algorithm follows since (r) may grow linearly.

**Special case.** On any oriented forest (r=0), the count is precisely (5^c2^m). Directed cycles are evaluable with the constant-size transfer matrix (A), namely (operatorname{tr}(A^ell)).

## Theorem 2: full rank is no computational lower bound

For the circulant T5 adjacency matrix (A), eigenvalues are (zeta^j+zeta^{3j}), (j=0,ldots,4). Their product is **(det A=2)**. Hence A has full rank 5 in every characteristic other than 2 and has rank 4 in characteristic 2. Nevertheless the oriented-forest problem is exactly solvable in linear arithmetic time, and bounded-cycle-rank inputs admit the exact algorithm above. Full local tensor rank cannot imply unavoidable individual-instance work.

## Theorem 3: all-arity (mathbb Z_5)-affine polymorphism classification

Suppose (f(x_1,ldots,x_t)=b+sum_i c_ix_i pmod5) preserves R. For every (s_iin\{1,3\}), its coefficient form (sum_i c_is_i) must lie in ({1,3}). Let (C=sum_i c_iin\{1,3\}). Replacing one (s_i=1) by 3 forces each (c_i) to be either zero or the same fixed nonzero coefficient (d). Two nonzero coefficients would let us replace two positions and obtain (C+4d
otin\{1,3\}), a contradiction. With a single nonzero coefficient, multiplication by 3 fails to preserve ({1,3}), so its coefficient must be 1. Therefore **every affine polymorphism, at every positive arity, is exactly (f(x)=x_j+b)**. There is no genuine multi-input affine polymorphism. This is not an exclusion of Fourier algorithms: Theorem 1 explicitly uses Fourier characters.

## Executed independent verification

Standalone Python used distinct implementations of character/flow exact counting and direct assignment backtracking, plus fraction-free determinant, GF(2) rank, and affine-coefficient exhaustive checking. All **69** test graphs matched exact backtracking, including trees, reversed paths, directed/transitive triangles, directed five-cycle, a K4 tournament, complete T5, disconnected graphs, and **60** seeded random directed graphs with possible two-cycles. The independent affine sweep checked **19,530** coefficient vectors, arities 1 through 6, with precisely coordinate projections valid. Zero assertions failed. Examples: five-vertex directed path 80 assignments, directed triangle 15, transitive triangle 5, oriented K4 0, complete T5 5.

Executed Python SHA256: `1a937e141ba5ce632723c8fd360681bcd77f5c1ee2595fda98374281236a7401`. Executed JSON SHA256: `aaac06a15f294226e246862055a418cfadb86c3b64f888fe3635aaf685262e4c`. Complete verifier, raw JSON and proof report are also in the TMR5_088_Fourier_Flow_Affine_evidence.zip conversation artifact.

## Ranked chain and safeguards

| Arrow | Audit |
|---|---|
| Private C5-to-T5 gadget, exact CSP NP-completeness | PROVED restricted, primary-source independently audited |
| All-arity Z5 affine polymorphisms | PROVED essentially unary |
| Flow-space/Fourier formula and cycle-rank FPT algorithm | PROVED, exactly reproduced |
| Full local tensor rank implies mandatory machine work | FALSIFIED as general instancewise inference |
| This FPT algorithm implies unrestricted T5 tractability | NOT ESTABLISHED |
| Fixed OBDD/cofactor/tensor metric implies adaptive/global machine lower bound | OPEN, representation false-positive controls |
| TMR-2/TMR-4 invariant to arbitrary-machine necessary work | OPEN |
| T5 to Boolean SAT polynomial encoding | PROVED |
| Unrestricted superpolynomial Boolean-SAT lower bound; P != NP | OPEN |

Retain DISJ, source inversion, bounded-treewidth, padding, selector, algebraic-shortcut, adaptive FBDD, relativization, DTISP and configuration-counting safeguards. The results show no new SAT lower bound. PR #209 remains draft; no peer agent, title, schedule or ownership should be modified.

## Primary references

[1] Hell & Nešetřil, *On the Complexity of H-Coloring*, JCTB 48 (1990) 92-110. https://doi.org/10.1016/0095-8956(90)90132-J

[2] Barto, Kozik & Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Comput. 38(5) (2009), 1782-1802. https://doi.org/10.1137/070708093

[3] Barto & Kozik, *Constraint Satisfaction Problems Solvable by Local Consistency Methods*, JACM 61(1) (2014). https://doi.org/10.1145/2556646
