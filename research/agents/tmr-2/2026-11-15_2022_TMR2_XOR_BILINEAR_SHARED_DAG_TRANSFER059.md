# TMR-2/059 | 2026-11-15 20:22 PST | Authenticated shared XOR DAGs: exact GF(2) bilinear count

**Directive first:** research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md, main Git blob 8451d955f6cd5397de0895f8ebb46e30818842c3. Primary Track A. Owned living file: main2_PNP_INFORMATION_NECESSITY.tex. Historical proof trackers and old root main.tex not read or edited.

## Candidate and falsifiers stated before source/corpus inspection

**D2-NONCONJUNCTIVE-SHARED-DAG, restricted positive transfer.** For every *authenticated*, finite, canonical ASCII source of the form "p nxor n a b g root" and exactly g records "g id E u v" or "g id X j k", every E gate denotes the AND of one left and one right original input; every X gate denotes XOR of two existing gate IDs. Gate records may be permuted, children repeated, and arbitrary internal fan-out present. The root reaches all gates and the graph is acyclic. All n=a+b original input IDs appear in edge leaves. Invalid sources are rejected. On this declared original circuit class, construct a polynomial-time, polynomial-space exact #ACCEPT algorithm and parsimonious strict proper 3-CNF, charging every source-to-output step.

F1: two paths to a shared gate might be counted as two separate satisfying extensions instead of canceling modulo two. F2: XOR repeated child and the gate-to-CNF bridge might introduce erroneous multiplicities. F3: old union-of-neighborhood states might falsely remain sufficient under parity. F4: malformed/cyclic or enormous declared headers might bypass guards. These are tested independently of the symbolic proof.

## Source and exact end-to-end algorithm

The parser checks every ASCII byte, numeric token, n=a+b, positive shores, n<=2g, g matching the record count, unique gate IDs, exact typed edge endpoints and gate references, use of every original input, the reachable rooted DAG and cycles. It performs iterative three-color DFS, never assuming numbered-gate topological order. If any check fails it rejects, not silently invoking SAT or a restricted oracle.

From the authenticated graph let w[root]=1 in F_2, and traverse nodes in reverse DFS postorder. For X(j,k) with weight w, perform w[j] ^= w and w[k] ^= w. Repeated children are deliberately updated TWICE, and thus cancel. For E(u,v) with weight w, perform A[u,v] ^= w. The result is an explicitly constructed a-by-b binary coefficient matrix A. The original output is, for *every* original assignment x,y,

    C(x,y) = x^T A y (mod 2).

Proof: induction over the acyclic source shows each X node is the F_2 sum of its gate-leaf polynomials; distributing the root coefficient downward counts *all* root-to-leaf paths modulo two. Every E leaf contributes x_u y_v. Repeated leaves, shared subDAGs and repeated children are treated by parity, not by independent-auxiliary multiplication. The construction visits O(g) gate records and materializes O(ab) binary coefficients, without unfolding a shared gate.

Let r=rank_F2(A), computed by actual Gaussian elimination on the constructed matrix. For each fixed x, the inner signed character sum over y is 2^b if A^T x=0 and zero otherwise. Since the kernel has dimension a-r,

    sum_(x,y) (-1)^C(x,y) = 2^(a+b-r).

Consequently the exact original-input count is

    #ACCEPT(C) = 2^(n-1) - 2^(n-r-1)   when r>=1;
    #ACCEPT(C) = 0                      when r=0.

The rejecting count is 2^n - #ACCEPT. Both quantities are <=2^n and have O(n) output bits. This is a *count of original input vectors*, not the number of output paths, not a generic encoded-Circuit-SAT decision complexity statement and not an equivalence of arbitrary functions with small tensors. The register transition invariant for TMR-4 is **D2-PARITY-BILINEAR-TRACE**: authenticated actual gate IDs, a proven reverse topological order, one F_2 path-parity bit per live gate, the materialized coefficient matrix, exact GF(2) row operations and the output integer pair. Its exact transition alphabet is READ_SOURCE, GUARD_HEADER, VERIFY_GATE_ID, DFS_EDGE, CHECK_CYCLE, CHECK_REACHABILITY, XOR_WEIGHT_TO_CHILD (twice even for a repeated child), TOGGLE_COEFFICIENT, ROW_SWAP, ROW_XOR, COUNT_RANK, SHIFT_BIGINT, SUBTRACT_BIGINT, OUTPUT, optional EMIT_CNF and HALT. It is a restricted **correctness** invariant, not a tariff on every SAT solver.

## Multiplicity-preserving gate-to-3CNF compiler

Take one gate-wire z_i per gate and three new pin variables p,q,r, constrained to zero by seven proper ternary clauses forbidding all seven nonzero pin assignments. For E(u,v), impose

    (-z_i OR x_u OR p), (-z_i OR y_v OR p), (z_i OR -x_u OR -y_v).

For X(j,k) with distinct gate IDs and wire literals a=z_j,b=z_k, impose

    (-z_i OR a OR b), (-z_i OR -a OR -b),
    (z_i OR -a OR b), (z_i OR a OR -b).

For repeated j=k, impose only (-z_i OR p OR q), which forces the XOR output zero and retains proper 3-distinct-variable syntax. Assert (z_root OR p OR q). Every original input has **one and only one** extension satisfying the gate equations plus pin constraints, and that extension satisfies the output clause iff C(x,y)=1. Thus n+g+3 variables, at most 4g+8 width-exactly-three clauses, and #3CNF=#ACCEPT(C), regardless of shared fan-out or cancellation. A genuine XOR of the same gate twice is forced to zero; it must NOT be treated as an independent duplicated witness.

## Two exact counterexamples to proposed necessity measures

**Smallest connected union-state failure in this grammar:** three originals x1,x2,y with E1=x1*y, E2=x2*y and X(E1,E2). Both x=(1,0) and x=(1,1) have identical union of neighborhoods {y}; nevertheless for y=1 the first yields 1 and the second yields 0, and the two right-side continuation counts are 1 and 0. This falsifies the attempt to transplant D2-CERTIFIED-COUNT-FRONTIER's *union-only* state to a parity circuit without an additional parity/coefficient register. It does not falsify its original AND/Horn source-domain lemma.

**Exponential chosen unrolling, linear authentic DAG:** put m disjoint bipartite E_i=x_i*y_i leaves; define h1=E1 and h_i=X(h_(i-1),X(h_(i-1),E_i)). The source has g=3m-2 gates and genuine fan-out two, but every h_i=E_i pointwise. The naive copied formula has U1=1, U_i=2U_(i-1)+3, hence U_m=4*2^(m-1)-3 occurrences. A discovered coefficient matrix has just one nonzero entry, rank one, and #ACCEPT=2^(2m-2). At m=80 the executed source has 160 original inputs, 238 true gate IDs, and an enormous formal unrolling that the evaluator never creates. No general-circuit lower bound is inferred.

## One-realization resource ledger

N is the complete authentic ASCII source **bit length**; g and n are O(N) after early guards, while a*b=O(N^2). A fixed locally headed deterministic multitape program can perform all source scans, canonical decimal parsing, authenticated record-table construction, cycle/reachability DFS, reverse coefficient propagation, O(ab) materialization, GF(2) elimination, exact n-bit integer shifts/subtractions, optional O(g)-clause CNF construction, all indices and source seeks, final printing and error output on a single execution. A deliberately coarse conservative upper envelope on every accepted source is

    T(N)=O(N^8) bit-machine steps, S_peak(N)=O(N^3) writable bits.

The matrix occupies O(N^2) bits; gate identities/DFS stacks occupy O(N log N); integer count/output registers occupy O(N) bits; source and optional linear-size CNF buffers can be stored without exceeding O(N^3). The rank computation has at most O(a*b*min(a,b)) single-bit row operations and is performed once on the materialized matrix; no rank oracle, circuit expansion, uncharged choice of basis or exponential source authentication is invoked. The same execution performs parsing and output. These are proved safe asymptotic upper envelopes, not a physical TM instruction microtrace. The published Node test harness also performs optional exponential-size brute comparisons, which are explicitly **excluded** from the production counter and from its polynomial envelope.

On invalid sources the parser rejects within polynomial resources; it does not claim to solve arbitrary XOR/AND/OR source circuits. Networks and probabilistic/quantum runs are not used.

## Four mandatory gates and hostile controls

| Gate | Verdict | Explanation |
|---|---|---|
| DISJ sanity | PASS restricted; unrestricted static rank transfer FAIL | DISJ has matrix rank 2^k and an O(k) circuit. No claim converts such rank into necessary work. Our algorithm instead admits legal mod-two Gaussian cancellation. |
| Relativization | PASS for local exact algebra; OPEN for any NP bridge | There is no P-vs-NP separation here. No nonrelativizing step is asserted; BGS, algebrization and Natural Proofs remain an OPEN obligation for a future unrestricted lower bound. |
| Simultaneous DTISP | PASS restricted upper envelope; OPEN unrestricted lower transfer | Input, gate table, coefficient matrix, row operations, exact integers, buffers and output are charged in the SAME deterministic source-to-count realization. No forbidden time-space region is claimed. |
| Configuration counting | PASS upper-bound guard | The deterministic total read-only-source machine obeys T<=2^O(S+log N), a halting-run upper bound only. No probabilistic or quantum extension is inferred. |

The disjointness, Horn expanders, affine/Gaussian, 2-SAT, bounded-treewidth and equality controls remain legal; parity is a conspicuous cheap algebraic path. Products, autarkies, padding, auxiliary variables, duplicate-gate multiplicity, unique selectors, rank-one full indicators for unique solutions, compact shared circuits and adaptive switching are not excluded. The field F_2 is essential to XOR path cancellation; it is not the characteristic-independent assignment-matrix rank in the DISJ control. Invertible local basis changes cannot alter cut rank; the characteristic-two Walsh-Hadamard matrix is singular. Valiant-Vazirani is randomized and promise-sensitive; no isolation is used. The source circuit's evaluation polynomial is not the SAT-decision function on encoded formulas. Historical /341 is FAIL as full UNSAT authority; /386 RESTRICTED.

## Independent execution and pinned provenance

Primary comparisons consulted: original TMR-2/058 report and exact published executable, TMR-4/060 genuine shared XOR/OR DAG source compiler, classical Tseitin functional gate encoding (Tseitin 1968, overview https://www.cs.jhu.edu/~jason/325/PDFSlides/04sat.pdf), binary bilinear character orthogonality (proved above), and Bryant's BDD source semantics (1986, DOI 10.1109/TC.1986.1676819). No new general-circuit hardness theorem is claimed.

**ACTUALLY RUN** local Node v22.16.0 source revision TMR2_XOR_BILINEAR_E2E059_v3, seed 20261115, exactly matching verified Git blob SHA d5da510006f68d4eee0089a14a54c9aea271cc9f: 241 assertions, zero failures; 74 independent exhaustive original-input counts; five full auxiliary-3CNF enumerations; six malformed-source rejections. Authenticated 72-input shared source had coefficient rank 2, #accept 1770887431076116955136. The 160-input cancellation-chain had rank 1 and #accept 365375409332725729550921208179070754913983135744. Finite evidence is **COMPUTATIONAL** and does not independently validate the symbolic all-input proof.

Executable: experiments/tmr/tmr2_xor_bilinear_e2e059.js.
Immutable raw: results/raw/tmr/2026-11-15_2022_TMR2_XOR_BILINEAR059_NODE_RAW.json.
This dated report: research/agents/tmr-2/2026-11-15_2022_TMR2_XOR_BILINEAR_SHARED_DAG_TRANSFER059.md.
Owned root: main2_PNP_INFORMATION_NECESSITY.tex.

No native repository checkout, so repository preflight not executed. LaTeX compilation will be reported separately if a complete owned manuscript is materialized. No physical-TM microtrace, independent mathematical peer review, general-Circuit-SAT transfer or P-versus-NP proof has been executed or established.

## ONE next load-bearing lemma

**D2-OR-OF-BILINEAR-LAYERS:** Generalize the authenticated source grammar to a genuinely shared OR of q root-reachable XOR-bilinear subcircuits, authenticate the q boundaries and coefficient matrices, and construct the precise O(2^q poly(N))-time exact-count character-sum transfer (polynomial for q=O(log N)), including cancellation, all 2^q combined ranks, auxiliary counts and source costs. Alternatively find an authentic minimal OR/XOR source refuting a proposed four-register generalization. Arbitrary circuits and P versus NP remain OPEN.
