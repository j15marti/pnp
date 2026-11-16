# TMR-4/065: An authentic shared-circuit obstruction to polynomial OBDD compilation at every input order

**Date:** 2026-11-16 PST. **Owner:** TMR-4 / PNP Cost-Sound Abstraction, Tracks A/C. **Status:** KNOWN THEOREM (Bryant 1991, Theorem 2) plus a new, restricted authenticated-source/costed integration (PROVED/EXACT restricted, external mathematical review OPEN). Executed small-instance checks are COMPUTATIONAL. P versus NP OPEN.

## Named dependency, candidate and falsifiers

**D4-UNBOUNDED-MODULE-INTERFACE, universal-OBDD subclaim FALSIFIED.** Candidate: for all n>=1 build an explicit fan-in-two Boolean shared-gate DAG C_n from complete authentic source bytes, with O(n log n) original gates and O(n log² n) encoded bits, computing HWB_n; prove every fixed-order OBDD for this very same source function has exponential size regardless of an adaptive polynomial-time order search, while a fully charged source-aware exact counter is polynomial. This is a full source-to-output *counterexample to extending the /062-/064 OBDD compiler with a polynomial-size guarantee for all shared circuit DAGs*. It does not refute an adaptive FBDD compiler or a non-OBDD counting algorithm.

Falsifiers fixed before source consultation: (i) an original gate is dead or the circuit is only an exponentially unfolded formula; (ii) a Hamming-weight indexing mistake changes the output or original-input count; (iii) a better variable permutation yields a polynomial OBDD, contradicting the claimed all-order barrier; (iv) the purported cheap exact count is uncharged advice, omits source validation, or counts gate extensions instead of original inputs.

The complete pipeline is source bytes -> canonical authentication -> original gate DAG (no target schedule) -> independent original gate evaluation on any specified assignment -> the original-input HWB function -> source-certified exact-count recognizer/output; alongside the explicit source -> any same-function fixed-order OBDD -> Bryant's all-order exponential node lower bound. This second arrow is a **representation-output obstruction**, not an algorithmic SAT-time lower bound.

## Explicit source, semantic coverage and original-input count

For n>=1, inputs x_1,...,x_n, let r=ceil(log2(n+1)). The source is canonical printable ASCII JSON with keys gates,n,root,version, version=1, each gate a unique original ID g_i with fields id,a,b,op, and op in {0,...,15} the real binary truth-table opcode. Source order does not provide or assume a variable schedule. Authentication checks all keys and shape, the n<=2g guard before n-sized allocation, every original operand ID, acyclicity, all gates root-reachable, and use of every original input. Malformed input is rejected, never deemed UNSAT. The executable generator emits increasing original gate IDs and a complete shared DAG; the parser/evaluator accepts a permutation of gate records. Source lengths L_n count every ASCII byte.

One shared ZERO gate is op=0(x_1,x_1). Initialize r count bits to ZERO. For each original x_i, perform an ordinary ripple increment: from the low bit upward, emit actual XOR(old_bit,carry), and for every nonfinal counter bit emit AND(old_bit,carry) for the next carry. The r-bit register now equals the integer sum of the inspected input values, by the standard binary addition induction. For every k=1,...,n construct an original AND-of-comparators for (count=k), using NOR(z,z) to negate a counter bit z and AND truth-table gates to conjoin the tests, then AND with original x_k. OR the n terms to obtain the original root. Gates have arbitrary genuine sharing and reconvergence, including the repeated counter bits and original input uses. Every generated gate lies on a root dependency path: each intermediate counter value is used at the next update, all final counter bits feed the comparators, and every selected term feeds the root. Each original x_i occurs in the ripple and in its own selected term.

All-step induction on increment events and on the topologically evaluated original gates proves, for every assignment x, exact input/gate and final-output correspondence:
\[
  C_n(x)=\mathrm{HWB}_n(x)=
  \begin{cases}0,&|x|=0,\\x_{|x|},&1\le|x|\le n.\end{cases}
\]
No auxiliary Boolean variables are counted as original inputs. For each k>=1, exactly binom(n-1,k-1) inputs have total weight k and x_k=1. Therefore
\[
   \#C_n=\sum_{k=1}^{n}\binom{n-1}{k-1}=2^{n-1}.
\]
A deterministic source recognizer first authenticates the actual byte string and compares the complete original gate map, root and n against the uniform constructed grammar, without trusting source record order. Only if every original record matches does it write the exact count (one followed by n-1 zero bits) and SAT=YES. A malformed or valid nonfamily source receives an explicit not-in-class outcome; no claim of general #CircuitSAT is made.

With r=O(log n), the original ripple has at most n(2r-1) gates, the n equality selectors have O(nr) gates, and the OR aggregation adds n-1. Thus g=O(n log n), each ASCII record uses O(log(g+n)) identifier bits, and L_n=Theta(n log²(n+2)) for the concrete JSON grammar. Generating the source uses polynomial bit-time and does not unfold repeated gates.

## The unconditional all-variable-order OBDD barrier

**KNOWN THEOREM (Bryant 1991, Theorem 2).** For this precise hidden-weighted-bit function, every ordered binary decision diagram, irrespective of the variable permutation and reduction/merging policy, requires Omega(1.14^n) vertices. The original paper's fooling-set argument selects a 0.6n/0.4n split, extracts n/5 same-side central variables and at least binom(n/5,n/10) distinguishable left restrictions for n divisible by ten, with other n handled by embedding. Its lower bound is not one static grouped-cut assumption for a particular guessed input order. Original: R. E. Bryant, "On the Complexity of VLSI Implementations and Graph Representations of Boolean Functions with Application to Integer Multiplication," IEEE Trans. Computers 40(2):205-213 (1991), Theorem 2, DOI 10.1109/12.73590; author-hosted PDF https://www.cs.cmu.edu/~bryant/pubdir/ieeetc91.pdf , PDF page 11. The stronger/more detailed OBDD literature includes Bollig, Löbbing, Sauerhoff and Wegener (1999), DOI 10.1051/ita:1999108.

**Restricted integration corollary.** There cannot exist a uniform or nonuniform compiler that maps every original fan-in-two circuit with L source bits to an explicitly materialized equivalent fixed-order OBDD of L^{O(1)} total vertices. If such a compiler existed, apply it to the authentic C_n, where L_n=Theta(n log² n); its polynomial-in-L_n bound contradicts Bryant's Omega(1.14^n). A serialized full OBDD must pay at least Omega(1.14^n) output vertices/records and therefore exponential total serialization time. If it is explicitly retained on writable tapes, it also requires that much node storage up to encoding factors. **Do not infer exponential peak work space for a streaming writer**, since output may be write-only. The theorem does not apply to an adaptive FBDD, repeated-test BP, tensors, dynamic rank contraction, or an arbitrary solver. In fact the source-aware exact counter is polynomial, making precisely this distinction unavoidable.

## SAME_REALIZATION resource partition

For any actual source word of bit length L, the fixed multitape family-recognizer/count program may read and authenticate the entire input, reject invalid JSON and overlarge declared n, build a bounded indexed gate map and topological cross-check, reconstruct the expected uniform ripple/comparator tree, compare each authentic original gate exactly once for semantic identity while charging every lookup/identifier, and then emit count and SAT. A deliberately conservative **simultaneous** upper bound is T_total=O((L+n+1)^6), S_peak=O((L+n+1)^3) writable bits. A pointwise verification with n additional supplied bits uses the same coarse pair and physically seeks/reads each input and original gate. The budget includes parse failures, graph discovery, optional record permutation sorting, shared wire IDs, fan-out reads and cache retention, index/head movement, all intermediate gate truth-table evaluations, membership checks, arithmetic/precision, and actual output. This is an asymptotic implementation upper bound, not a measured physical Turing-microstep trace. Each physical shared gate is counted once for stored object identity; any re-evaluation during validation is separately paid. No network span or separate-machine best-case resource is substituted.

For explicit OBDD construction, the SAME run must additionally materialize its Omega(1.14^n) nodes and output them. Hence its complete serialization work cannot be polynomial in L_n, regardless of compiler scheduling, sharing, or variable-order search. This is a costed output lower bound for this *required target format*, not a lower bound on the source decision or count computation. Compact circuit/counter outputs remain fully legal.

## Executed evidence and independent check

The exact locally run Node v22.16.0 standard-library code revision TMR4_HWB_OBDD_BARRIER065_v1 has SHA-256 8f86d7aa03e6567f18b31e911da7e63665cecfce40ec8307a833ee4a39caf1b4. No random seed. Its SHA-checked zlib/base64 source and loader reproduce the same output byte-for-byte, including after publication. It authenticated 12 original source circuits (n=1..12); independently evaluated all 2,046 original assignments for n<=10; rejected four malformed variants; and checked the exact 2^{n-1} count. A separate exhaustive *cofactor-set* dynamic program computed the globally minimum number of reduced OBDD internal nodes over **all input orders** for n=2..10:
\[
  (1,3,7,14,21,31,44,61,80).
\]
A structurally separate literal permutation-and-hashcons ROBDD constructor checked **all 872 variable orders at n=2,...,6**, agreeing with the cofactor DP on every n. These finite numbers do not prove an exponential growth law; the unbounded law is Bryant's known theorem. All assertions passed, zero failures. Executed raw SHA-256 7d757d42b403cc696a164a98439c3911bc21ef78d1fee7c68d5fc0c019dc143f. Exact executable archive at experiments/tmr/tmr4_hwb_barrier065.js.zlib.b64, validated loader experiments/tmr/tmr4_hwb_barrier065_loader.js, raw results/raw/tmr/2026-11-16_TMR4_HWB_ALL_ORDER_BARRIER065_NODE_RAW.json. Source "sha256" records for n=2,6,10 are recorded inside raw. The finite tests are COMPUTATIONAL. No complete physical TM microcode, local cloned repository preflight, independent external peer review, or full LaTeX manuscript compilation was executed.

## Mandatory gates and retained controls

| Gate | Verdict | Reason |
|---|---|---|
| DISJ sanity | **PASS, restricted** | The counterexample concerns HWB's all-order OBDD size, not static DISJ rank. DISJ has linear circuit and a cheap interleaved order; grouped rank cannot imply general circuit hardness. |
| Relativization | **PASS for representation no-go; unrestricted NP bridge OPEN** | Bryant's combinatorial representation theorem relativizes as a model statement; it does not yield a relativizing P-vs-NP separation. Algebrization/Natural Proofs remain outstanding for any different general lower-bound bridge. |
| Simultaneous DTISP | **PASS for charged source-aware upper; strict lower bridge OPEN** | Matched T=O((L+n)^6), S=O((L+n)^3) source-aware evaluation/count; explicit OBDD output takes exponential work. There is no forbidden (T,S) pair for SAT. |
| Deterministic configuration counting | **PASS upper-bound guard only** | Total deterministic locally headed machines have T<=2^{O(S+log L)}; the inequality is not a required-work lower bound, nor a probabilistic/quantum theorem. |

Horn, dual Horn, 2-SAT, affine/Gaussian, equality, bounded treewidth, products, autarkies, padding, auxiliaries, selectors and unique-solution rank-one tensors remain legal comparison algorithms and model controls. Source function HWB is not assumed to belong to any of these restricted classes. Invertible local basis changes preserve field rank, but no tensor-rank implication is inferred. Randomized isolation is not free. There is no majority, quantum error or amplitude transfer. Historical /341 remains FAIL as complete UNSAT authority; /386 remains RESTRICTED. P versus NP remains OPEN.

## ONE next load-bearing dependency

**D4-ADAPTIVE-FBDD-ESCAPE (OPEN):** source-authenticate and actually construct a polynomial-size *input-adaptive, read-once free branching program* for HWB, if such a representation is available, paying branch-dependent variable selection, state identity, access, exact labelled-path counts and complete same-run T/S. This is a controlled comparison of OBDD versus genuine adaptive FBDD, **not** a promise that every arbitrary Boolean circuit has such a representation. The source-to-all-equivalent-algorithms lower-bound bridge and a nonrelativizing NP implication remain OPEN.
