# TMR-3/098: Minor-preserving compiler barrier and exact correct-path query costs

Date: 2026-11-18 PST. Owner: TMR-3 / PNP Time-Space Tradeoffs.
Status: **PROVED** (conditional structural minor-separator theorem and abstract oracle decision-tree bound), **KNOWN** (Buss-Williams exclusion), **COMPUTATIONAL** (77,845 primary and 1,436 independent assertions, zero failures), **FALSIFIED** (all-algorithm hardness inferred from interfaces, naive routing-table lower bounds), **OPEN** (minor-destroying semantic compilers, unrestricted time/space). P versus NP OPEN.

## Theorem 098-A: Auxiliary-variable/minor-stable separator

Let the hypercube Q_d have v=2^d vertices. Suppose the undirected support graph H of a compiled CSP has disjoint nonempty connected branch sets X_u for all vertices u of Q_d, with a real H edge joining X_u to X_w for each cube edge uw. Extra compiled auxiliary vertices and support edges are permitted. Suppose H's vertices split into shared S and private blocks Y_1,...,Y_M, with |Y_i|<=B<v and **no H edge between distinct Y_i**. Then s=|S| obeys

    s >= v*(d-log2 B)/(2*d-log2 B).

Proof: Let U consist of cube vertices whose branch set X_u intersects S. Branch-set disjointness gives |U|<=s. Each connected X_u avoiding S lies entirely within one Y_i. The real H edge witnessing a cube edge uw forces any two such avoiding-S branch sets into the same Y_i. Therefore Q_d-U partitions into cube subgroups of at most B vertices, with no cube edges between groups. Edge isoperimetry of Q_d gives sum_i |delta(P_i)| >= (v-|U|)*(d-log2 B), whereas each such edge must meet U and the sum is <=d|U|. Rearrangement gives |U|>=v*(d-log2 B)/(2*d-log2 B), hence the stated s bound. QED.

**Compiler blowup:** If the compiled H has L=v^(gamma+o(1)) vertices and each private group has B<=L^0.35 vertices, then for fixed gamma<20/7,

    s >= ((1-0.35*gamma)/(2-0.35*gamma)-o(1))*v.

Thus a near-linear minor-preserving copy/auxiliary compiler still needs (13/33-o(1))*v shared vertices. To achieve s=o(v) while retaining the exhibited Q_d minor and B<=L^0.35 it must instead output L>=v^(20/7-o(1)). If B is defined against original N rather than L, the corresponding original-source bound persists regardless of L. This is a representation tradeoff only: a semantic compiler that destroys the minor is not constrained.

**Countercontrol:** Orient each Q_d edge from smaller to larger Hamming weight. The assignment x_u=popcount(u) mod 5 is a valid T5 witness on every arc (difference +1); its five rotations are valid as well. The large separator thus certifies no necessary witness-search time.

## Theorem 098-B: Exact black-box correct-path cost

In a model with independently arbitrary oracle bits a(z,i) for R shared rows and M children, parent SAT is OR_z AND_i a(z,i). The deterministic worst-case *oracle-query* complexity is exactly R*M. The adversary answers 1 on the first M-1 queries to each row and 0 on the final remaining query to that row. Until every row is closed, SAT remains compatible with the transcript, so all R*M cells must be read in the worst case. Upper bound is trivial. If a *trusted free correct negative index for each row* is supplied, R oracle queries suffice. Neither bound transfers to explicit CNF time without a paid representation theorem.

The literal routing table has R*ceil(log2 M) bits, but this is not a lower bound on the shortest description. Explicit blocks B_i(z)=OR_{j<r}(z_j!=bit_j(i)) for all i<2^r have exactly one negative block per z. The routing program i(z)=low_r_bits(z) is tiny; removing one block makes the system SAT with a readily output witness. This falsifies inferring k-bit path complexity from the cardinality of a literal all-row table.

## Weighted simultaneous ledgers

For authenticated F(z,y)=AND_i B_i(z,y_i) with disjoint private y_i:

    SAT iff exists z for all i exists y_i B_i;
    UNSAT iff for all z exists i for all y_i not B_i.

A serial specialist must charge authenticated parsing and failed preprocessing P, all actual queried children J(z), source restriction a_zi, full actual-polarity child solving t_zi^+ or t_zi^-, verification v_zi, path decoding/addressing h_zi, SAT witness reconstruction/replay W_i, and final original input verification/output V:

    T <= P + sum_{z visited} sum_{i in J(z)}
             (a_zi+t_zi^(actual)+v_zi+h_zi)
           + 1_SAT sum_i W_i(z*) + V.

The serial peak writable-space ledger includes the parser/shared z, retained routing, maximal live child state/materialization and validator/witness state, replay bookkeeping, and any jointly retained output. A materialized L-bit compiled instance costs at least L writable bits; a virtualized instance must pay each bit-generation and target random-address lookup. Read-only certificate k bits are still read and addressed; copying to RAM costs k space. Every wrong static k-bit path must be soundly rejected or yield UNKNOWN; enumerating all candidates costs up to 2^k complete verifier executions. An adaptive path function must be evaluated on every required z; an alternating strategy must cover all universal z and child UNSAT claims. A selected child index by itself is not a sound UNSAT certificate.

With total blocks M<=N^0.65 and child source length <=N^0.35 and exponent alpha, enumeration is at most 2^s*N^(0.65+0.35alpha+o(1)) plus all separately charged overhead. Constant s and exponent 1.33 require alpha<=1.942857; if each N^0.195 row separately contains N^0.65 blocks, alpha<=1.385714. Do NOT identify N^0.195 **rows** with s **shared-variable bits**. Child peak space ell^beta requires beta<=10/7 before other live state to fit N^0.5. When s=N^0.195, direct 2^s enumeration is superpolynomial. Unspecified polynomial-time SAT seeds do not imply these numerical costs.

## Published exclusions and nontransfers

Buss-Williams (2015), *Computational Complexity* 24:533-600, explicitly give SAT not in DTISP(N^1.34070,N^0.5) in their deterministic **random-access** model, interpreted with o(1) exponent slack. Deterministic UNSAT decision has the same exclusion by complementing the answer. A uniform all-CNF actual same-machine N^1.33+o(1)-time and N^0.5 polylog-space decider is excluded, unlike restricted block families or free oracle paths. Their 1.34070 optimum is for alternation-trading, not all lower-bound techniques.

Diehl-van Melkebeek-Williams (2011) prove for each d<4^(1/3) there exists *some* positive epsilon(d) excluding NTISP(N^d,N^epsilon(d)) for TAUTOLOGIES on their random-access model; the result does not specify epsilon=0.5. SAT witnesses with externally readable, randomly accessible certificates have inexpensive verification but that certificate model is not a free low-space nondeterministic machine. Proof-system lower bounds and negative-oracle lower bounds cannot be transferred to unrestricted computation without an explicit simulation. Under a compiler of size L=N^gamma and target (c,epsilon), the composed exponents are at best max(preprocessing, gamma*c, access, replay, decoder) in time, and at least gamma if the compiled input is materialized into writable memory. Any polynomial size inflation gamma>1 changes BOTH exponents, so the (1.34070,0.5) exclusion must not be cited after such a transformation without checking the new pair.

## Verification

The full runnable local reproducibility package independently checks 65,808 cube subsets, 1,116 below-bound shared sets of four copied/auxiliary Q_d minors, correct minor contractions and nonempty private components, full correct-path and wrong-path controls, T5 weight witnesses through Q_10, and exact minimax OR-AND oracle-query complexities through 3x3. Primary: **77,845 assertions, zero failures**; separate code-path audit: **1,436 checks, zero failures**, with two identical primary outputs. These are finite COMPUTATIONAL audits, not independent human mathematical review.

Gates: DISJ/quantifiers PASS on authenticated factored sources; ORACLE/RELATIVIZATION explicitly nontransferable; SAME-MACHINE PASS for cited DTISP and charged upper ledgers only; EASY-FAMILY controls refute representation-to-time leap. Native machine-model execution, independent mathematical review and full combined LaTeX build remain OPEN.

**Next:** C3-BLOCK-CHOICE-MINOR-DESTROYING099. Test a fully paid sublinear-workspace virtual semantic compiler that destroys source minors, on genuinely NP-hard sources. Quantify address generation, all negative/positive child calls, strategy decoding and verification. P versus NP remains OPEN.

References:
[1] Ellis, Keller, Lifshitz (2019), JCTA, https://doi.org/10.1016/j.jcta.2018.12.001 .
[2] Buss, Williams (2015), https://doi.org/10.1007/s00037-015-0104-9 .
[3] Diehl, van Melkebeek, Williams (2011), https://doi.org/10.1007/s10878-009-9286-x .
[4] Fortnow, Lipton, van Melkebeek, Viglas (2005), https://doi.org/10.1145/1101821.1101822 .
