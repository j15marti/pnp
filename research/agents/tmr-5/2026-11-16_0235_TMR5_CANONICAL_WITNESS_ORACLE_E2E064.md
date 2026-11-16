# TMR-5/064: canonical witness-bit oracle coherence in the JMV to counting chain

November 16, 2026, 02:35 PST. Named dependency C1f-WITNESS-ORACLE-COHERENCE. Status PROVED/EXACT RESTRICTED for the mathematical oracle-prefix lemma; external mathematical review OPEN. Finite replay COMPUTATIONAL. Actual JMV generator, Anthropic Lean/nanoda, physical final count and hierarchy implication independently OPEN. P versus NP OPEN.

## Candidate, model and falsifiers

Fix any x of n bits and the actual uniform JMV clause decoder D_x with ell(n)=O(n+log n) index bits and 3v+3 output bits, where v(n)=O(n+log n) bits per variable name. Every one of the 2^ell addresses is an authentic clause, and there are at most U=2^v named variables. Candidate: a single deterministic E^NP language W(x,i) returns bit i of one *coherent* lexicographically first satisfying assignment of phi_x, or zero if no witness. It feeds an address-to-violation circuit, unique-extension CNF normalizer, and true Anthropic low-first formal count input. Falsifiers: (1) independently selected existential answers could fail witness consistency; (2) explicit NP query acquisition or number could exceed 2^O(n); (3) duplicate addressed clauses, polarity or functional gate extensions might change zero count. The original JMV theorem and Lean validity are distinct OPEN verification dependencies.

## Exact construction and proof

Uniformly generate D_x and materialize phi_x by evaluating all m=2^ell addresses; write its named literals in L=O(m(v+1)) explicit bits. Define PREFIX-SAT(phi,p) as existence of a satisfying assignment extending a specified prefix p of the U named Boolean variables. This is in NP: guess the U-|p| missing bits and check every explicit clause.

Query PREFIX-SAT(phi,empty). If NO, all canonical W(x,i)=0. If YES, maintain prefix p. For j=0,...,U-1, query PREFIX-SAT(phi,p concatenated with 0). Append 0 when YES, otherwise 1. Induction: at each stage p is the lexicographically first prefix with a satisfying extension. Thus after U queries p is the *same* lexicographically least full satisfying assignment for every separately queried i. The choice of i only selects the final output bit.

At most U+1 NP oracle queries occur, each with at most B=O(m(v+1)+U+poly(n)) explicit bits. A single locally headed deterministic oracle-machine implementation has a conservative same-execution bound T <= T_JMV+O(m poly(n)+(U+1)(B+1)^3), peak writable S <= S_JMV+O((B+1)^2), Q<=U+1. Every source scan, query construction, prefix, sequential seek, failed zero attempt, input and output is charged. These are *oracle-machine* steps; the NP oracle's internal decision work is NOT asserted to cost polynomial physical time. Since m,U,B=2^O(n), W is in E^NP after fixed canonical length padding. No advice, free isolation, or global witness is presumed.

For any proposed indexed assignment A:{0,1}^v->{0,1}, define B_A(z) as the AND of three flags saying each of the three literal values is false under A. Then exactly #B_A authentic clause addresses are violated, including multiplicities for repeated clauses at distinct addresses. Hence #B_A=0 iff A satisfies phi_x. Real shared functional four-row Tseitin constraints and count-preserving fresh-variable promise normalization produce #CNF=#B_A, with formal input length n'+5+3m'(floor(log2(2n'))+1), n'>=4, 2<=m'<=4n', NoDup and AllOccur. Conditional on the pinned Anthropic counting theorem and its physical machine simulation, zero output decides whether a guessed A works.

Smallest falsifier of a tempting but INVALID replacement: with phi=(x0 OR x1), the lexicographically first witness is (0,1), but the independent query SAT(phi AND x0) returns YES. Independent per-bit existence does NOT yield the canonical witness. Our prefix method avoids this. On H-NO, every guessed A yields at least one violating address; on H-YES, a correct small circuit for the coherent W yields zero. This preserves the exact nondeterministic quantifier order. It is not a free NP oracle for the final lower-bound machine.

## Actual independent restricted implementation

Executed local CPython source revision tmr5-canonical-witness-oracle064-v1, random seed 20261116. Canonical ASCII p jwit ell v source contains exactly 2^ell signed triple records with genuine v-bit names. The tested parser authenticates all source records; a finite brute-force stand-in implements NP prefix queries, independently checks the lexicographic witness, builds an actual shared Boolean gate DAG of address selectors, name bits, assignment lookup and falsity flags, evaluates all authentic clauses, emits functional Tseitin CNF and fresh promise pins, and round-trips every low-first bit of the formal word. Single-gate corruption controls and all possible guessed assignments on NO instances are checked. This tests a complete **explicit-table** chain, not the original succinct JMV generator or the Anthropic counting machine.

Observed: 130 authentic sources, 107 SAT and 23 UNSAT; 432 logical oracle queries, 790 finite brute-force oracle trials, 676 clause-address evaluations, 30,858 executed gates, 20,106 normalized clauses, 434,269 formal bits, 1,976 corrupt-gate rejections, 188 universal-NO assignment controls, 5 malformed source rejections. **124,284 assertions, zero failures**. This is COMPUTATIONAL. Exact locally executed script SHA256 70f3e17da8a2f715043ada50c0233e115a016cda112c62440c5d5c56a2b333c3. Raw JSON SHA256 b050eb6d97ac0fc71271d17bfb19b2bb59c3c417a9b50e60171df18254dfc269. No native Turing microtrace, Lean, nanoda or independent mathematical peer review executed.

## Four gates and controls

DISJ sanity: PASS restricted, no rank-to-work lower bound. Relativization: PASS intermediate only, no P-vs-NP claim; BGS, algebrization and Natural Proofs remain gates for any NP promotion. Simultaneous DTISP: PASS for the same explicitly charged oracle-machine upper T/S run, no FLMV forbidden pair and no physical NP decision charge. Deterministic configurations: PASS only as a total deterministic fixed-oracle upper-bound consistency check, not a necessary-work statement or randomized/quantum extension. Horn/dual-Horn, 2-SAT, affine/Gaussian, treewidth, equality/autarky, products, padding/auxiliaries, selector/count-normalizer, field/basis changes, unique-solution rank one, sharing, caching and recomputation remain legitimate. /341 FAIL as full UNSAT authority; /386 RESTRICTED.

## Ranked pipelines and next lemma

(1) TMR-1 source/solver/hierarchy: coherent E^NP witness-bit semantics closed within the JMV theorem hypothesis; original generator and dual-kernel Lean 4.33.1/nanoda execution OPEN, model and hierarchy auditing separately OPEN.
(2) TMR-3 checkpoint provider/evaluator: /063 candidate graph screening restricted; generic adaptive provider and faster evaluator, matched Q/T/S OPEN.
(3) TMR-4 cost-sound compiler/model: /064 diamond-module discovery restricted; unrestricted source representation necessity OPEN.
(4) TMR-2 constructive invariant: /063 relative-degree-two exact count restricted; general dynamic necessary-cost invariant OPEN.

ONE next target: independent successful Lean 4.33.1/Mathlib and nanoda kernel check with exact transitive axioms for Anthropic MainResults.mainTheorem and ethIsFalse at commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, then separately replay FinTM2-to-standard-machine and E^NP quantitative hierarchy translation. No successful independent kernel build is claimed.

Primary sources: Jahanjou, Miles, Viola, Local Reductions, ECCC TR13-099 rev.3, Theorem 1 (https://eccc.weizmann.ac.il/report/2013/099/); Anthropic formal-math pinned MainResults.lean and Solution.lean; TMR-1/056 binary witness report and /064 vector decoder source, TMR-5/063 original full typed source-to-count report.
