# TMR-5/088: exact Fourier/flow FPT and all-arity affine audit

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Date:** November 18, 2026, Pacific Time. **Status:** independent symbolic theorems and executed finite reproduction; external review and formal kernel checking OPEN. **P versus NP OPEN.**

## 1. Exact flow-space identity and FPT algorithm

For a directed graph G with n vertices, m arcs and c weak components, let r = m - n + c. The fixed tournament has R(a,b) exactly when (b-a) mod 5 is in {1,3}. Let ζ be a primitive fifth root of unity, Λ(k) = ζ^(-k) + ζ^(-3k), and B be the oriented vertex-edge incidence matrix over Z5, with +1 at heads and -1 at tails.

**Exact identity:**

    #Hom(G,T5) = 5^(n-m) * SUM_(k in ker B) PRODUCT_(e in E) Λ(k_e).

**Proof.** Each edge indicator 1[d in {1,3}] equals (1/5) SUM_(k=0..4) Λ(k) ζ^(kd). Multiplying these expansions and summing all 5^n vertex assignments imposes Bk=0 by orthogonality of fifth roots of unity. The incidence matrix has rank n-c, so ker B has dimension r over Z5.

**Exact integer algorithm.** Choose a spanning forest. Enumerate the five possible flow values on each of its r nonforest edges, then uniquely solve all tree-edge flow values by eliminating leaves. For each flow k, multiply the m two-term polynomials (z^(-k_e) + z^(-3k_e)) inside Z[z]/(z^5-1), storing a 5-entry integer vector. Sum these products over all 5^r flows to obtain S=(S0,S1,S2,S3,S4). Multiplication of every flow by a nonzero scalar mod5 permutes the flow space, proving S1=S2=S3=S4. Evaluating at ζ gives S0-S1 because ζ+ζ²+ζ³+ζ⁴=-1. Thus

    #Hom(G,T5) = 5^(n-m) * (S0-S1),

with exact integer division when m>n. Runtime is O(m*5^r) arithmetic operations on polynomial-bit-length integers, plus spanning-forest preprocessing. This yields **fixed-parameter tractable exact counting and decision in cycle rank r**. It does NOT imply polynomial-time general T5-CSP, because r can grow with m.

On an oriented forest r=0, the answer simplifies to exactly 5^c * 2^m, independently of orientation. On directed cycles, the count is trace(A^length) for the fixed 5×5 adjacency matrix A.

## 2. Full local adjacency rank is a false-positive hardness signal

The circulant adjacency matrix A has eigenvalues ζ^j+ζ^(3j), j=0,...,4, and determinant exactly **2**. Thus rank(A)=5 in every field of characteristic not equal to 2, while rank over GF(2) is 4. In spite of local full rank, oriented forests admit linear arithmetic-time counting and bounded-cycle-rank instances admit the exact algorithm above. Local tensor rank does not establish unavoidable global machine work.

## 3. All-arity affine-polymorphism classification

Suppose f(x1,...,xt)=b+SUM_i c_i*x_i mod5 preserves R. For every choice s_i from {1,3}, the value SUM_i c_i*s_i must be in {1,3}. Put C=SUM_i c_i, so C is in {1,3}. Switching any one s_i from 1 to 3 shows C+2c_i is in {1,3}, forcing each c_i to be zero or the same nonzero coefficient d. If two coefficients were nonzero, switching both gives C+4d outside {1,3}. Thus at most one nonzero coefficient is possible. That coefficient must be 1 since multiplying S={1,3} by 3 does not preserve S.

**Every Z5-affine polymorphism, at every positive arity, equals f(x)=x_j+b.** These are the five rotations of coordinate projections. There is no genuine multi-input affine polymorphism. This does not rule out Fourier algorithms: the flow algorithm is itself Fourier based.

## 4. Independent execution

The executed standard-library Python verifier implements spanning-forest Z5 flow enumeration with exact integer polynomial arithmetic and independently implements ordinary assignment backtracking. It also uses fraction-free integer determinant, GF(2) rank and exhaustive affine coefficient classification.

- **69 graph cases** matched exact brute-force homomorphism counts, including paths, reverse paths, cycles, both triangle orientations, K4, the exact T5 template, disconnected cases, and 60 seeded random graphs.
- **19,530 affine coefficient vectors** checked across arities 1 through 6, with only the predicted projections passing.
- **Zero assertion failures.** Determinant 2 and GF(2) rank 4.
- Selected counts: five-vertex directed path 80; directed triangle 15; transitive triangle 5; oriented K4 0; target T5 itself 5.

Executed source SHA256: 1a937e141ba5ce632723c8fd360681bcd77f5c1ee2595fda98374281236a7401.
Raw JSON SHA256: aaac06a15f294226e246862055a418cfadb86c3b64f888fe3635aaf685262e4c.
The exact executed code, raw JSON and longer mathematical report are archived in the run's evidence ZIP, TMR5_088_Fourier_Flow_Affine_evidence.zip.

## 5. Ranked dependency audit

| Proof arrow | Verdict |
|---|---|
| Exact C5-to-T5 gadget, general T5 NP-completeness | PROVED restricted via primary-source and independently checked gadget |
| All-arity affine polymorphism classification | PROVED symbolic, finite checks through arity 6 |
| Fourier/flow identity and O(m*5^r) parameterized algorithm | PROVED symbolic and independently reproduced |
| Full local tensor rank implies mandatory algorithmic effort | FALSIFIED as instancewise inference |
| General polynomial algorithm from cycle-rank method | NOT ESTABLISHED: r unrestricted |
| Fixed-order OBDD or tensor representation hardness implies adaptive/global time lower bound | OPEN; representation-only false positives remain |
| TMR-2/TMR-4 invariants imply arbitrary-machine necessary work | OPEN |
| Standard polynomial Boolean encoding of T5 | PROVED |
| Unrestricted superpolynomial Boolean SAT lower bound; P versus NP | OPEN |

DISJ false positives, source inversion, selectors, padding, bounded treewidth, adaptive FBDD, relativization, simultaneous DTISP and deterministic configuration-counting safeguards remain in force. There is no new unrestricted machine lower bound. No peer manuscript, agent, owner or schedule was changed.

## Primary references

[1] Hell and Nešetřil, *On the Complexity of H-Coloring*, J. Combin. Theory Ser. B 48 (1990), 92-110. https://doi.org/10.1016/0095-8956(90)90132-J

[2] Barto, Kozik and Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Comput. 38(5) (2009), 1782-1802. https://doi.org/10.1137/070708093

[3] Barto and Kozik, *Constraint Satisfaction Problems Solvable by Local Consistency Methods*, JACM 61(1) (2014). https://doi.org/10.1145/2556646
