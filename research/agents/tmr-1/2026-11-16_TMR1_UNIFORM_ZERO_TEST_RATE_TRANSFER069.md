# TMR-1/069: uniform zero-test rate and hard succinct YES witnesses

Date: November 16, 2026, PST. Role: TMR-1 / PNP Machine Model Lead. Track C. Named dependency **C1f-ZERO-TEST-RATE**. Classification: PROVED/EXACT as a conditional restricted mathematical implication; external independent review OPEN. P versus NP remains OPEN.

## Target and falsifiers fixed before source inspection

Selected chain: authentic binary hierarchy input x -> Jahanjou--Miles--Viola (JMV) uniform clause decoder -> authenticated guessed implicit assignment circuit A -> literal-evaluation/violation circuit B -> functional Tseitin and all-promise normalization -> **ordinary deterministic promised 3CNF ZERO-test**, NOT necessarily an exact counter -> one nondeterministic branch's accept/reject bit -> the precise infinitely-often YES-witness lower bound. The rate and peak space are charged on the same branch.

Candidate: make the existing C1f/067 witness-to-hierarchy implication *solver-agnostic*, show exact quantitative sufficient conditions on any uniform decision or counting implementation, and separate a single rate bound from the weaker statement "for each fixed epsilon a different 3SAT machine runs in 2^(epsilon n)." This closes the named C1f-ZERO-TEST-RATE interface, not a P-versus-NP bridge.

Falsifiers: (F1) JMV might expose an explicit 2^v-bit assignment, rather than v-bit variable names. Theorem 1 has a 3v+3-output local decoder on ell-bit clause addresses, so a v-input circuit A is the appropriate representation. (F2) Computing D_x might cost exponential time. Theorem 1 constructs it in poly(n,log T), and r=2 gives constant-depth output decision trees; the paid batched junta reconstruction costs polynomial time. (F3) A 3CNF decision algorithm might not cover malformed or nonpromised inputs. The compiler explicitly authenticates and maps every valid B to its AllOccur/NoDup/n>=4/m>=2 promised domain; all malformed x or A reject before the solver. (F4) An arbitrary nonuniform threshold s(n) might be used as free advice. The theorem requires an explicit uniform source-computable s(n) and charges its computation and the full guess.

## Fully quantified theorem

Fix a binary language H in NTIME(2^n) \ NTIME(2^(n/2)), with a fixed nondeterministic machine realizing the first inclusion. For each x of length n let Phi_x be the **actual** JMV Theorem 1 indexed 3CNF at T=2^n n^O(1) and r=2. Then Phi_x is satisfiable iff x is in H. Its clause addresses have ell=n+O(log n) bits; the possible variable labels have v=Theta(ell) bits, and the total 3-literal decoder output has 3v+3=O(n) bits.

Let Z be any ONE fixed deterministic finite-alphabet locally headed multitape algorithm that correctly decides SAT (or UNSAT) for every width-at-most-three CNF with no duplicate outer ordered clauses, all variables occurring, at least four declared variables, at least two clauses, and m<=4N clauses on N declared variables. Assume its *complete* physical time on such instances of N variables is bounded by a nondecreasing F(N), including the actual O(N log N) input and one-bit output. Let S_Z(N) be a nondecreasing upper envelope for its peak writable space.

Let s(n)>=1 be an integer function uniformly computable by one machine within polynomial time and workspace in u(n)=n+s(n)+2 (and not supplied as advice). For fixed constants K,d,c>=1 depending on the JMV machine, decoder and compiler but NOT n or x, the construction below has, on each nondeterministic branch, the SAME-RUN bounds

    N_normalized <= K*u;
    total sequential branch time <= c*(u^d+F(K*u));
    peak branch writable space <= c*(u^d+S_Z(K*u)).

If this complete time bound is o(2^(n/2)) as n increases, then **for infinitely many n some genuine YES input x in H has no satisfying assignment to Phi_x represented by any v-input shared fan-in-two circuit with <=s(n) noninput gates**.

The result requires only an ordinary *decision* zero-test, not exact model counting. Its conclusion is a restricted implicit-witness circuit lower bound, NOT an NP circuit lower bound and NOT a separation.

## Complete proof

Given actual source bits x, authenticate their length and invoke the fixed JMV reduction. The original source theorem constructs D_x:{0,1}^ell -> {0,1}^{3v+3} in poly(n,log T) time. If necessary, invoke the already proved C1f-JMV-VECTOR-SUPPORT batch: each output bit, being a fixed-depth decision tree, depends on at most a constant w address coordinates. Pay Q(ell,w)=sum_{j=0}^w binom(ell,j) full-vector evaluations of D_x, each polynomial in n; reconstruct all output functions as one O(n)-gate shared circuit. Thus g_D<=a*n and every access, result bit and circuit gate is physically generated.

On a nondeterministic branch, compute s(n), guess a complete topologically ordered source encoding of a v-input shared Boolean gate circuit A with at most s(n) gates, and validate every index, truth table, length and output. Reject malformed encodings. Guess representation length O((v+s(n))log(v+s(n)+2)), and pay it in sequential branch time and peak space.

Compile the genuine ell-input clause-violation circuit B_{x,A} using the decoder and three actual copies of A. The exact previously proved C1f-NAME-ADDRESS bound is g_B<=g_D+3s(n)+11. For each real address z in {0,1}^ell, B(z)=1 iff the full implicit assignment a(j)=A(j), j in {0,1}^v, falsifies the genuine decoded clause D_x(z). Duplicated decoded clauses remain separately addressed; this is harmless because the theorem uses whether the violation count is zero.

Apply C1b's functional shared-gate Tseitin compiler to B, preserving the exact number of accepting *addresses*, then apply the repaired C1c density/promise totalizer to obtain H_{x,A}. Here q=ell and G=g_B, so its promised variable count N=O(n+s(n)), its clause count is at most 4N, and every source address has a unique gate-variable extension. All ordered-clause deduplication and fresh forced pins are charged. Serialize the exact low-bit-first clause format, including all actual source bits, pointers and signs. Thus #H_{x,A}=#{z:B_{x,A}(z)=1}. In particular H_{x,A} is UNSAT iff A encodes a satisfying assignment of Phi_x.

Run Z *once* on this explicit promised H_{x,A} and accept the nondeterministic branch iff Z reports UNSAT. For x not in H, Phi_x is unsatisfiable, so every complete assignment circuit A violates at least one addressed clause. Sound Z therefore rejects all branches. If for all sufficiently large YES x there exists such an A of <=s(n) gates, some guessed branch accepts for each YES x. Finite exceptional source lengths are handled by hardwired correct answers in the single finite nondeterministic machine.

The parser, paid decoder calls, vector truth-table synthesis, circuit guess, shared wire encoding, CNF clauses, hash/dedup, auxiliary pins, bit-order serialization, solver input, one solver query/run, and final bit all use at most a fixed polynomial u^d before/after Z, on **the same branch**. Materialized source, decoder, A, B, CNF, indices, byte buffers, retained live gates, and solver workspace give the stated same-branch peak bound. Distinct nondeterministic guesses are NOT treated as parallel processors or as sequentially explored alternatives. The assumed strict total-time condition would therefore put H in NTIME(2^(n/2)), contradicting its fixed nondeterministic hierarchy selection. Hence infinitely many genuine YES lengths contain a source with no circuit A in the budget. QED.

## Two precise quantitative consequences

**Quantitative one-machine rate.** Suppose the same physical Z obeys F(N)<=poly(N)*2^(a*N/sqrt(log_2 N)) for some *fixed* constant a>0 and all sufficiently large promised N. Set s(n)=floor(eta*n*sqrt(log_2 n)), uniformly constructible. With the fixed compiler constant K, the simulator exponent is at most (a*K*eta+o(1))*n plus polynomial o(n) overhead. Any sufficiently small eta, for example eta<1/(8*a*K) after enlarging K to cover constant-size terms, yields the strict hierarchy-time condition. Hence infinitely many YES x have **all** implicit satisfying assignment circuits larger than eta*n*sqrt(log_2 n). This recovers C1f/067 from a *decision-only* premise. Anthropic's typed MainTheorem plus the fixed FinTM2 physical simulation would conditionally supply such a Z; an independently executed local Lean rebuild remains OPEN.

**Qualitative ETH-failure family of machines.** Suppose only the usual quantified failure of ETH: for every fixed epsilon>0 there is SOME deterministic standard 3SAT decider Z_epsilon with complete time O(2^(epsilon N)) on promised, at-most-four-density formulas. For each fixed constant c0>0, set s(n)=floor(c0*n). Choose ONE sufficiently small epsilon depending on c0 and the fixed compiler constant K, not on n or x. The preceding proof then yields, for infinitely many n, some YES x whose every succinct satisfying assignment circuit has >c0*n gates. Thus the per-length worst-case minimum witness-circuit complexity divided by n has unbounded limsup. This is NOT a claimed explicit growth rate such as sqrt(log n): quantifier swapping to choose epsilon=epsilon(n) would improperly introduce an input-dependent machine. The mere formal ETHIsFalse statement does not give the fixed quantitative rate needed for the preceding sqrt(log n) conclusion.

## Four gates, controls and exact status

DISJ: PASS, restricted. DISJ_k has a small shared circuit and exact count 3^k; no hardness of all instances follows from the source-specific theorem. Horn, 2SAT, XOR/affine-Gaussian, treewidth, equality, autarky, products, padding, auxiliary and selector/unique-witness controls remain legitimate compact paths.

Relativization: PASS for this conditional source/solver/hierarchy implication as a restricted statement; an unrestricted NP lower-bound promotion is OPEN and must pass Baker--Gill--Solovay, algebrization and Natural Proofs. TQBF-oracle countermodels C1h remain applicable to a purely relativizing NP-promotion proposal.

Simultaneous DTISP: PASS, for a single charged nondeterministic upper-time/peak-space realization. NOT APPLICABLE to an FLMV deterministic forbidden pair, which is not established.

Configuration counting: NOT APPLICABLE to the nondeterministic hierarchy machine. For its deterministic subroutines it is an upper-bound consistency safeguard T<=2^O(S+log N), never a work lower bound.

All unknown legitimate alternate algorithms remain MAY. Prior /341 is FAIL as a universal UNSAT authority, /386 RESTRICTED. No majority-tie/quantum-amplitude assertion is made.

## Exact references, evidence and workflow

[1] Jahanjou, Miles and Viola, *Local reductions*, ECCC TR13-099 revision 3, March 31, 2014, printed Theorem 1 and Corollaries 2-3, https://eccc.weizmann.ac.il/report/2013/099/revision/3/download/ . Original theorem verified against the page-image, including ell, v, output width, time poly(n,logT) and O(log r) decision-tree depth.

[2] Anthropic formal-math commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/MainResults.lean blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc, eth/Solution.lean blob 176892178e49792ae41368c13bb4973bae035b29, pinned Lean v4.33.1 and Mathlib 0df444a360eaa60ab8c11dca51a86af692955474. Source terms and archived upstream dual-kernel acceptance are evidence; independent local replay OPEN.

[3] TMR-1/062 C1f-NAME-ADDRESS, /064 vector-junta batch, /067 all-witness conditional theorem, /068 NP-collapse firewall. Current active living file main1_PNP_MACHINE_MODEL_LEAD.tex and handoff.md.

[4] Nondeterministic binary time hierarchy (Seiferas--Fischer--Meyer, 1978); the fixed H is required to be a binary language with the stated strict separation, not an unverified tally witness.

**Execution and publication:** This /069 proof is a source-verified symbolic argument, not an empirical algorithm run. No new numerical test, raw benchmark or executable solver was run. GitHub-connected source reads completed; no local pnp checkout, so active preflight was NOT run. Container has no Lean/Lake/Cargo, and its GitHub git network cannot resolve github.com. No independent Lean, nanoda, native Turing-machine trace or complete LaTeX build was run. External mathematical review OPEN.

**ONE next load-bearing lemma:** execute a genuinely independent pinned Lean v4.33.1 / Mathlib rebuild of MainResults.mainTheorem and ethIsFalse, with actual #print axioms and Lean/nanoda dual-kernel replay. The current /069 implication is self-contained conditional mathematics; it does not substitute a source build, does not yield a direct NP target, and makes no P-versus-NP resolution.
