# LSPV-1 COFACTOR-SENSITIVITY-CIRCUIT324
**2026-11-02 02:00 PST, Formal Proof Lead. Status: PROVED elementary all-valid-source Boolean-function/gate bounds, finite independent controls, external review pending. All-input P versus NP OPEN.**

## Exact obstruction and duplicate-work audit
An exact circuit C_F(x)=F(x) over the ORIGINAL source inputs is cheap to evaluate once x is supplied. The time required to decide whether some input x makes it true is different. One cannot infer a lower bound for ALL SAT decision algorithms from a lower bound on the complexity of a forward evaluation circuit or from a post-answer minimum circuit.

The project already proved the sharp witness-sensitivity n/3 lemma in **LSPV-3 GATE292** (October 31, 2026). The F9 35-gate source-private evaluator was also known, and LSPV-1 MINZERO317 already explained the coNP-complete zero-gate minimum-circuit acquisition barrier. These prior results are explicitly credited. This run derives an **exact forward/reverse cofactor boundary identity and an unrestricted fan-in-two evaluation-circuit size/depth corollary**, not a new unrestricted SAT lower bound.

Four falsifiers: (F1) a satisfiable original with witness sensitivity < n/3, refuted by GATE292; (F2) a SAT original with no nonzero cofactor-difference miter, disproved by the exact boundary theorem; (F3) sublinear binary-gate and sublogarithmic binary-depth forward circuits for SAT canonical originals, ruled out in the declared model; (F4) a large cofactor boundary forces expensive *decision* work, disproved on authenticated easy disjoint G6 products.

## Theorem 324A: all-input cofactor boundary
For every valid proper duplicate-free Döcker monotone 3-SAT-(2,2) original F with n original variables and m=4n/3 three-literal original clauses, let f(x)=F(x). For every ORIGINAL variable i, use its Shannon cofactors f_i0(z)=F(z,xi=0), f_i1(z)=F(z,xi=1), and the Boolean XOR difference miter M_i=f_i0 XOR f_i1, on the remaining n-1 source names. Let s_F(a) count single-variable flips from a satisfying original assignment a to an unsatisfying assignment.

Then, with ALL original clause/index provenance retained,

\[
\boxed{B(F):=\sum_{i=1}^n\#SAT(M_i)
=\sum_{a:F(a)=1}s_F(a)
\ge \frac n3\#SAT(F).}
\]

**Proof.** Each variable occurs twice positive and twice negative, contributing exactly two true literal occurrences to each complete assignment, so \(\sum_Ct_C(a)=2n=3m/2\). For a satisfying a, no clause has zero true literals and the moment equations imply \(N_1(a)=m/2+N_3(a)\ge m/2\). A one-true-literal clause becomes false if its unique satisfying source variable flips. One variable can uniquely satisfy at most two source clauses. Thus at least \(N_1/2\ge n/3\) distinct flips destroy SAT, a **previously established** GATE292 lemma. Each assignment to M_i represents one hypercube edge between f=0 and f=1. Counting those edges by pivot i equals counting by their unique SAT endpoint. QED.

Corollary: **B(F)>0 iff F is SAT.** Testing whether at least one of the n exact forward/reverse cofactor-difference miters has a satisfying input is NP-complete on this canonical language. A YES witness is a source pivot i and remaining assignment z, verified by two polynomial-time source-clause evaluations; the identity map from canonical SAT gives NP-hardness. This rephrases the original SAT decision and does not supply a free way to find a witness or compute miter labels.

## Theorem 324B: unrestricted fan-in-two evaluation-circuit size/depth
Fix the precise model: one-output acyclic Boolean netlists with arbitrary binary Boolean gates, free source-input wires, constants and unary NOT, but NO unbounded fan-in. Size g counts binary gates; depth d counts binary-gate levels. The circuit computes F(x) correctly for **every** full original input assignment, not simply the one-bit SAT label.

**For every valid SAT canonical original**,
\[
\boxed{n/3-1\le g_{\min}(F)\le 4n-1},\qquad
\boxed{\lceil\log_2(n/3)\rceil\le d_{\min}(F)
\le2+\lceil\log_2(4n/3)\rceil.}
\]

**Proof.** Every SAT witness has at least n/3 pivotal source coordinates by 324A and GATE292; each is an essential input of F. A single-output fan-in-two DAG with g binary gates cannot have more than g+1 distinct essential input leaves in its backward cone, so g>=n/3-1. A depth-d circuit depends on at most 2^d distinct inputs, giving d>=ceil(log2(n/3)). Conversely, each source three-literal clause is evaluated by two binary OR gates, and all m clause gates combined by m-1 balanced AND gates. This costs 3m-1=4n-1 gates and depth <=2+ceil(log2 m), acquired through fully paid source reads and gate writes. QED.

The bounds establish **Theta(n) unrestricted minimal forward netlist size and Theta(log n) minimal forward depth for the SAT-labelled canonical originals**, in this declared gate model. The n/3 pointwise sensitivity coefficient is sharp on the GATE292 G6 family, but the lower gate-size constant is NOT claimed optimal. If F is UNSAT, its Boolean function is constant zero and has a zero-gate *post-answer* evaluator. Finding which case applies is the original NP-complete question; minimum evaluation-circuit complexity is NOT necessary universal SAT decision work.

## Independent finite controls
G6 has positive clauses 123,124,356,456 and the identical four negative clauses, valid distinct 2,2 monotone original. It has 26 satisfying assignments, 76 SAT/UNSAT hypercube boundary edges, sensitivity minimum 2, six pivot miter counts (14,14,10,10,14,14), 23 source-private binary gates and depth 5. The GATE292 witness 001100 has precisely the two critical variables x3,x4, so the n/3 pointwise bound is attained. Two disjoint G6 blocks have n=12, 676 models, 3952 boundary edges, sensitivity minimum 4, 47 gates and depth 6.

Independently authenticated F9 has n=9,m=12, 70 models, 402 boundary edges, sensitivity minimum 4, pivot miter counts (46,44,52,50,40,52,40,38,40), 35 gates and depth 6. Both G6 and F9 were checked under all full assignments with independent Boolean-function, cofactor-pair and original-clause computations; all S/U pair extremes and assignment-complement identities were replayed.

**Same ORIGINAL both-label controls:** on G6 pins (x1,x2,x3)=(0,0,1) leave 3 SAT completions; changing x3 to zero leaves 0, each of its eight complete leaves falsifying an original clause. Direct UP-first DPLL used respectively 2 nodes/36 literal visits and 1 node/3 visits. On F9 the known six-pin pair differing only at x1 has 2 versus 0 completions and direct UP-first DPLL used 1 node/40 visits versus 1 node/34 visits. Six deliberately malformed self-delimiting binary encodings per source were rejected. U198/V198 remain inherited crosschecks, not freshly replayed; the general theorem has no dependency on their finite labels. Separate no-producer-import bitmask verification passed at least 5528 counted clause-pair and complement assertion groups, plus exhaustive miter, sensitivity, grammar and source truth checks. No industrial CDCL or native FLMV comparison is claimed.

**XOR diagnostics:** full aligned original clause true-literal count vectors were compared in binary/Gray assignment orders. Adjacent XOR popcounts, endpoint XOR and changed source clause IDs were computed OFFLINE and separately replayed, not confused with physical writable/index tape changes.

## Work/space and the open implication
For a uniform source-authenticated adaptive decider, exact *executed* work is local grammar/source/index/head + circuit/semantic acquisition + every failed policy + switching + proof/GE/cache/replay + the sum of actually executed child/output-bit/guest DELAY-COPY-RECOMP work. Simultaneous peak is the maximum co-live ancestor/index/source-derived/cache/proof/output/guest writable space. Explicit forward compilation writes O(n log n) gate/address bits in polynomial bit work. Exhaustively acquiring all n exact miter counts by brute force costs O(n 2^n poly(N)) time, and is NOT a polynomial selector or a free SAT oracle.

The family of recognized source-disjoint G6 blocks is easy: a fully paid polynomial grammar and signed-incidence component recognizer can certify each constant-size block and return SAT without recovering a witness, despite 26^t satisfying assignments and \(B=t\cdot76\cdot26^{t-1}\) boundary edges. Thus the derived forward-circuit lower bound is **not** a necessary all-algorithm SAT decision-work lower bound.

The constructive target remains \(\exists D,C,k\ \forall w:\ D(w)=1[w\in L]\) and fully charged \(W_D(w)\le C(|w|+1)^k\); the separation target would require superpolynomial worst-case work for **every** correct all-input D. Neither is proved. The arbitrary unknown-exponent A->Phi(A) power-short hereditary canonical compiler and strict numerical SAME-MACHINE FLMV transfer remain unproved. **P versus NP OPEN.**

## Audit and references
Read FIRST the verified November 1 19:50 PST five-role redirect, then the decision-work directive, saturated-cycle theorem, issue #3, GATE292 and latest LSPV roles. Google/web queries: "Boolean function sensitivity circuit depth lower bound fan in two essential variables"; "regular monotone 3SAT each variable twice positive twice negative model isolated satisfying assignments sensitivity"; "Döcker monotone 3SAT (2,2) is NP complete"; "Bryant 1986 Boolean function manipulation OBDD cofactor Shannon decomposition"; "bounded occurrence CNF satisfying assignment uniquely satisfied". Primary: Döcker, arXiv:1912.08032 (2019); Bryant, IEEE Trans Computers 1986 DOI 10.1109/TC.1986.1676819; Nisan, SIAM J Comput 1991 DOI 10.1137/0220062; Rossman, Computational Complexity 2018; Fortnow-Lipton-van Melkebeek-Viglas, JACM 2005 DOI 10.1145/1101821.1101822.

Separate **GitHub** searches: repo:j15marti/pnp "witness fragility", "sensitivity" "n/3", "cofactor" "fragility"; repo:openai/math sensitivity, circuit. Prior project exact match: [GATE292](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-31_2324_LSPV-3_FIRST_RESOLUTION_AND_WITNESS_FRAGILITY_GATE292_PUBLIC.tex). OpenAI math repository has general Boolean sensitivity formalization but no project-specific canonical source result was authenticated. This is a narrow elementary corollary, not a novelty assertion.

Public compact reproducer: [source and miter code](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_324/cofactor_boundary324_compact.py); [raw summary](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_0200_LSPV1_COFACTOR_SENSITIVITY_CIRCUIT324_summary.json). Full separately implemented no-import verifier and expanded clause/XOR raw records are retained in the local user-facing reproducibility archive. Repository root is not to be overwritten without full authenticated nonempty blob and LSPV-1-only marker reconciliation.

**No task identity, status, title or hourly Pacific schedule changes. P versus NP OPEN.**

END_OF_VERIFIED_REPORT::LSPV1::COFACTOR_SENSITIVITY_CIRCUIT324::P_VS_NP_OPEN
