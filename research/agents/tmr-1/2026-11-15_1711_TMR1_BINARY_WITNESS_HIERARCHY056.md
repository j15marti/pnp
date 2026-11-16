# TMR-1/056: Binary-input hierarchy witness and paid local-decoder construction

**2026-11-15 17:11 PST | TMR-1 / PNP Machine Model Lead | Track C.** Scientific status: J56 and the conditional binary-input transfer are **PROVED/EXACT RESTRICTED**, independent mathematical review **OPEN**; finite tests **COMPUTATIONAL**; the source #SAT theorem and final E^NP consequence **CONDITIONAL** on source validity. P versus NP **OPEN**.

## Candidate, quantifiers, and four falsifiers

**Candidate C1f-BINARY.** Fix a binary language H in NTIME(2^n) but not NTIME(2^(n/2)). For every binary source x of length n, produce an authenticated local 3CNF clause decoder and a polynomial-gate exact violation checker from a guessed nonuniform circuit for one E^NP witness-bit language W. Compose it with the already specified C1a-C1e source-CNF-totalizer-finite-stack-counter-standard-machine pipeline. If every sufficiently large N-bit W has at most eta N sqrt(log_2 N) binary gates, the resulting ONE nondeterministic decider for H contradicts the binary nondeterministic time hierarchy. This proves only a conditional infinitely-often Omega(N sqrt(log N)) *E^NP* gate lower bound, not NP and not superpolynomial circuit hardness.

Precommitted falsifiers: **F1** the Jahanjou-Miles-Viola binary-x decoder lacks uniform polynomial construction or constant-output locality; **F2** recovering junta supports requires exponential or uncharged work; **F3** witness guessing, source parsing, compiler and counting fail for some legal YES/NO source or exceed the strict time target; **F4** the pinned Anthropic counting theorem lacks a valid kernel proof or applicable Turing-machine semantics. F4 is **OPEN**.

The named integration point is **C1f-BINARY**, the hierarchy witness and local-decoder uniformity link of the existing authentic circuit bits -> unique-extension CNF -> all-input promise totalizer -> formal low-first bits -> exact count -> standard machine -> class consequence chain.

## Primary sources and scope

[1] Jahanjou, Miles and Viola, *Local Reductions* (March 31, 2014), Theorem 1: for a fixed nondeterministic machine, binary input x of length n and constructible T at least 2^n, generate an index-to-3CNF-clause circuit D_x in time polynomial(n,log T); for T=2^n poly(n), clause address length ell=n+O(log n), v=Theta(ell)=O(n) bits per formula-variable name (the formula can have up to 2^v distinct variables), O(n) output bits, each depending on at most a fixed constant w index bits. Satisfiability of the described formula phi_x is equivalent to acceptance of x. The output-bit locality does NOT give a free circuit or free support positions.

[2] Seiferas, Fischer and Meyer, *Separating Nondeterministic Time Complexity Classes*, JACM 25 (1978). The standard nondeterministic time hierarchy supplies an appropriately encoded binary H in NTIME(2^n) outside NTIME(2^(n/2)). This avoids depending on an unstated tally-specific hierarchy assertion in the previous TMR-1/053-055 exposition.

[3] Anthropic formal-math pinned commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5. Inspected exact source blobs MainResults.lean 1c62a550fa1e4cbec65bb7112f92ad67589afddc, Solution.lean 176892178e49792ae41368c13bb4973bae035b29, and proof/maintheorem/CountedRoute/Main.lean c57963f3e805e7288cd6df28dbef1d25f3bbd25a. One fixed finite-alphabet FinTM2 counting machine and one C are quantified before k and all formulas; conditions k>=1, n>=4, m>=2, AllOccur, outer-list NoDup. Exact output is the n+1 low-first bits of the count. Time is bounded by 2^[C min(km/sqrt(log_2 m), k^2 n log_2 log_2 n/sqrt(log_2 n))]. MainResults is a proposition file, Solution references CountedRoute.mainTheoremHolds, and the latter's original proof text was read. **Lean v4.33.1 kernel build, #print axioms and transitive import verification were not executed**. Challenge.lean deliberately contains sorry and is documented as outside the imported proof chain; the documentation is not a substitute for a kernel replay.

## NEW LEMMA J56: exact bounded-junta discovery with paid calls

Let f:{0,1}^ell -> {0,1} depend on at most w coordinates for one fixed w independent of ell. There is one uniform deterministic evaluator-based construction producing an *exact equivalent* fan-in-two circuit of at most O(w 2^w) gates, with no more than

  2 ell sum_{j=0}^{w-1} binom(ell-1,j) + 2^w

paid evaluations of f plus polynomial bookkeeping.

**Proof.** For every position i, test f(1_S) against f(1_(S union {i})) over all S not containing i with |S|<=w-1. A genuinely relevant coordinate i has a witnessing assignment to the at most w-1 other relevant bits. Assign all irrelevant bits zero; that witness is among the tests. An irrelevant coordinate cannot change f in any test. Thus precisely the actual support R is recovered. Query f on all 2^|R| patterns and emit a constant-size Shannon tree (or DNF) on R, with O(w 2^w) fan-in-two gates. No semantic count or oracle query is free: an evaluation of f is a real run of its authentic decoder. Applying this independently to O(n) output bits of D_x produces a uniform O(n)-gate shared clause decoder in polynomial(n) bit time. QED.

This closes the previously unstated support-discovery cost in C1f. It does not establish a generic polynomial-time learning theorem when w is not constant.

## Conditional full-chain theorem, binary H not unary

Define W on words of length N=d n as follows. Parse x of length n, then one appropriately encoded canonical variable index i for phi_x, then zero padding; return bit i of the lexicographically first satisfying assignment of phi_x, or zero if phi_x is unsatisfiable or the word is not canonical. For lengths not divisible by d output zero. Choose constant d large enough for ell(n), the v(n)=O(n)-bit variable-name width and canonical delimiters. A deterministic E^NP machine produces the complete 2^ell poly(n)-size formula using D_x and, with at most 2^v=2^O(n) NP prefix-extension queries of length 2^O(n), identifies this lexicographically first witness bit. All formula generation, queries and outputs cost 2^O(N). Thus W belongs to E^NP.

Assume for contradiction that for all sufficiently large N=d n a general fan-in-two gate circuit A_N computing W on ALL N-bit inputs has s_N <= eta N sqrt(log_2 N) noninput gates. Given the ACTUAL binary x of length n, nondeterministically guess and validate A_N, specialize x and its canonical padding, and evaluate three copies of A_N on each of the three decoded variable labels of a clause. The resulting clause-violation circuit has q=ell(n)=n+O(log n) original address inputs and G<=3s_N+O(n) actual shared gates, including paid recovered decoder gates. Its output is 1 exactly when a selected source clause is violated by the alleged witness. Full C1a-C1d parsing, count-preserving Tseitin encoding, promise totalization, clause and gate indices, input authentication, and formal low-first encoding produce V=q+G, n'=V+O(1), m'<=4n', with O(V log V) explicitly written bits and polynomial construction time.

If the pinned formal counter theorem is valid with the stated physical FinTM2 interface, the SAME conventional multitape run computes the exact number of violation addresses within

  T <= poly(V log V) + 2^[(12C+o(1)) V/sqrt(log_2 V)]
    = 2^[(36 C eta d + o(1)) n],

and peak workspace O(T+V log V). Choose eta>0 below 1/(144 d max(1,C)); then the full nondeterministic execution is eventually below 2^(n/2), including guessed circuit description, source generation, all support-recovery decoder calls, arithmetic, buffers and output.

If x belongs to H, phi_x has a satisfying assignment; a correct circuit A_N representing W supplies it and the checker counts ZERO violations, so at least one nondeterministic branch accepts. If x is outside H, phi_x is unsatisfiable, and EVERY alleged witness produced by ANY guessed circuit violates at least one clause, so every branch rejects. Thus the hypothesized eventually small circuits give a uniform nondeterministic H decider in NTIME(2^(n/2)), contradicting the selected binary hierarchy language. The conditional conclusion is

  exists W in E^NP, exists eta>0, for infinitely many N:
  circuit_size(W|_{0,1}^N) > eta N sqrt(log_2 N).

It is NOT a lower bound for every N, NOT an NP circuit lower bound, NOT a superpolynomial lower bound, and NOT P!=NP. The source JMV and pinned counter hypotheses are substantive. Independent reproduction of the original full hierarchy transfer remains OPEN.

## Same-realization resource ledger and mandatory gates

| Paid stage, same nondeterministic branch | Sequential bit time | Peak workspace |
|---|---|---|
| Binary x validation, uniform JMV source and decoder | poly(n) | poly(n) |
| J56 tests of O(n) output-bit juntas; all authentic D_x evaluations | n^O(w), with w constant | poly(n) |
| Guess/validate A_N, specialize x, build shared violation circuit | poly(n+s_N) | poly(n+s_N) |
| C1a-d compiler, totalizer, formal encoding | O((B_C+B_A)^4), B_C+B_A=O(V log V) | O(B_C+B_A) |
| Single FinTM2 simulation, exact answer and zero test | O(T_M+B_A^2+V), CONDITIONAL | O(T_M+B_C+B_A) |

All numbers belong to one real sequential execution, with shared gate identities only once. **No strict sublinear-space DTISP forbidden pair follows.**

| Four-gate requirement | Status and reason |
|---|---|
| DISJ sanity | **PASS scoped.** The compact linear-gate DISJ circuit is admitted despite full static cut rank. Horn, 2SAT, affine/Gaussian, bounded treewidth, equality, autarky, products, selectors, unique witnesses and compact representations stay legal. |
| Relativization | **PASS intermediate / OPEN NP promotion.** A conditional E^NP implication is not a fully relativizing P!=NP proof. Any NP-level bridge needs an independent nonrelativizing argument plus algebrization and Natural Proofs audits. |
| Simultaneous DTISP | **NOT APPLICABLE to an FLMV contradiction.** This is a nondeterministic time-hierarchy proof; no small-space guarantee. |
| Deterministic configuration counting | **PASS upper-bound guard.** T<=2^O(S+log B) for fixed deterministic read-only-input total machines is an upper bound, not compulsory work and not a randomized/quantum bound. |

Historical /341 is FAIL as unrestricted logical UNSAT authority; /386 is RESTRICTED. P versus NP OPEN.

## Finite evidence, exact provenance, and review

Executed native Node v22, code revision tmr1-binary-hierarchy056.v1, xorshift32 seed 20261115. Source SHA-256 d6ee056af6aa43b3e8f6e076210e855b503713e09ab6b27fa778bd1aca363430; raw SHA-256 00d82ffe07a0d9100b1057fc039c4e4ce0fcbea8bf9c5ecc13fd21c3e0a890f9. Git code blob 2db5a4711d66c3fc26fd534e97a6d868b48909c1. The verifier checked **495** random truth-table juntas, **224,840** exhaustive junta evaluations, **93,689** charged junta support probes, **56** binary-x encoded clause cases, **448** candidate assignments and **3,584** source-clause checker evaluations: **229,899 assertions, zero failures**. These tests do not execute a hierarchy witness or prove a general #SAT algorithm.

Files: experiments/tmr/tmr1_binary_hierarchy056.js and results/raw/tmr/2026-11-15_1711_TMR1_BINARY_HIERARCHY056_NODE_RAW.json. No local Git repository checkout/preflight, independent Lean v4.33.1 kernel build, transitive axiom audit, complete CVP/TreeEval transfer, or mathematical peer review was executed. Pending TMR-3 draft PRs #164/#169 remain separate and OPEN as generic interfaces. Retired proof trackers were not read or edited; the five existing agent schedules and peer-owned manuscripts were not modified.

**ONE next load-bearing lemma:** independently rebuild the pinned Anthropic Solution.lean under Lean v4.33.1, check #print axioms MainResults.mainTheorem and transitive imports, and validate actual FinTM2 step/input/output semantics against the physical simulation. Without it the lower-bound consequence remains CONDITIONAL.

References: [1] https://www.khoury.northeastern.edu/home/viola/papers/explicit.pdf ; [2] https://doi.org/10.1145/322047.322061 ; [3] https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth .
