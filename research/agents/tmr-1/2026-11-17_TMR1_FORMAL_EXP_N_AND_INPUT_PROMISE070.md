# TMR-1/070 | Formal expN arm and general-density input-promise transfer

Date: 2026-11-17, Pacific. Owner: TMR-1 / PNP Machine Model Lead. Status: exact restricted compiler lemma plus a CONDITIONAL consequence of the pinned formal theorem; independently executed finite V8 checks (COMPUTATIONAL); independent Lean/nanoda kernel reconstruction and independent external mathematics review OPEN. P versus NP remains OPEN.

## Authority, selected dependency, falsifiers

Governing coordination: research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md (main), compatible SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md, and the November 17 PNP_Hostage_Review_and_Agent_Restart_2026-11-17.md, checked against supplied Hostage_Negotiator.pdf. Full pipeline: authentic explicit binary 3CNF -> parser / ordered-clause deduplication -> unique-extension general-density promise compiler -> formal low-first input -> one fixed FinTM2 counter -> physical output read and zero test -> exact subexponential-in-n conclusion for CANONICAL input lengths. The alternative NP bridge remains absent.

Candidate C1e-FORMAL-EXPN-GENERAL-PROMISE: for ALL well-formed encoded width-at-most-three CNFs with declared n original variables and arbitrary duplicate or unused clauses, a uniform deterministic all-input translator creates an Anthropic MainTheorem-valid input with n'=n+4, preserving the EXACT original satisfying-assignment count. No m<=4n density promise is required. The full solver time has an explicit input-length tariff; if the original encoding is canonical of polynomial length in n, the expN ARM yields 2^{o(n)} physical time with ONE fixed counter machine.

Falsifiers checked: (F1) the source might lack the expN arm or require m<=4n; source MainResults.lean explicitly has the min of expM and expN and NO density restriction. (F2) old variables absent or duplicated clauses might corrupt #SAT; forced pins, inserted tautologies and exact outer-list dedup avoid this. (F3) normalization could blow n' up to Theta(m); construction fixes n'=n+4, unlike the older four-density compiler. (F4) an unbounded duplicate-padded input might not admit an n-only 2^{o(n)} bound; it does not, and B remains in the time ledger.

## Primary pinned source audit, no kernel executed

Anthropic formal-math pinned commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5:
- eth/MainResults.lean blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc: MainTheorem has one M, one natural C, finite every-stack alphabets, and then ALL k>=1,n>=4, IsKCNF k, m>=2, AllOccur. CountsWithin uses nonempty TM2OutputsInTime for exactly (n+1) low-first bits. For k=3, expN(3,n') = 9 n' lg(lg n') / sqrt(lg n'); no m<=4n.
- eth/Solution.lean blob 176892178e49792ae41368c13bb4973bae035b29: proof terms point to CountedRoute.mainTheoremHolds and the Wrap chain. Top-level proof text is not a transitive axiom audit.
- eth/lean-toolchain blob a8afa7d1b02d96f0671eba854a8dc4b416beb473 pins Lean 4.33.1; eth/lakefile.toml blob 055ec8b4132a38fc96dc4fd0c8cb9b6b6ef8b62a pins mathlib 0df444a360eaa60ab8c11dca51a86af692955474.
- Mathlib/Computability/TuringMachine/StackTuringMachine.lean blob 916694942a3bfefa0bd9085e2f48735dbe8e0f5b: stepAux is a fixed statement tree of push/pop/peek/load/branch/goto/halt for fixed M.
- Mathlib/Computability/TuringMachine/Computable.lean blob 7779a00f0c3c3909923a5f1bde6b3120b5c2d28a: FinTM2 has finite K, labels and internal states; initList fills only input stack; haltList requires all other stacks empty and initial state restored; TM2OutputsInTime is EvalsToInTime.

No executable Lean, Lake, elan or nanoda was available in the working container and git ls-remote failed DNS resolution for github.com. No checkout was mounted, so the updated repository preflight could not be run. Connected source-file reads succeeded. Neither #print axioms nor either kernel was executed here; earlier upstream CI reports remain UPSTREAM, not independent verification.

## Exact compiler theorem (PROVED/EXACT, restricted; mathematics review OPEN)

Fix n>=0 and an explicit finite list F of clauses, each an ordered list of at most three signed literals on the declared n variables. Let m0 be the number of DISTINCT ordered clauses of F and u the number of original variables absent from all clauses. Build G:
(i) retain one instance of each ordered old clause;
(ii) append (x_i OR NOT x_i) for each unused original variable;
(iii) introduce four fresh names t0,t1,t2,t3, each pinned false by unit (NOT t_j);
(iv) append the new tautology (t0 OR NOT t0).
No other change, and no four-density enforcement.

All newly added clauses are pairwise distinct and distinct from retained source clauses, as every new pin uses fresh names and the unused-variable tautologies use originally ABSENT names. Thus

    n'=n+4,      m'=m0+u+5>=5,
    IsKCNF 3 G,  AllOccur G,  NoDup G,  n'>=4.

Every assignment on the original n variables has exactly one extension to all four pins, with all t_j=false. Tautologies and duplicate deletion leave satisfaction unchanged, including old empty clauses. Consequently

    #G = #F,

with exactly the original n+1 low-order count bits carrying the full result. This holds for n=0 and for contradictory, repeated, tautological, disconnected or unused-variable sources.

A fixed source parser authenticates every bit and rejects invalid indices, lengths, trailing data and malformed encodings; exact ordered-duplicate removal can be done by a polynomial-time stable sort or a conservative quadratic scan. Let B be the COMPLETE original source length; n<=B for a unary-n source. There are at most sum_{j=0}^3 (2n)^j distinct ordered clauses, hence m0=O((n+1)^3). With w=floor(log2(2n'))+1, the EXACT formal input length is

    B_A = n'+5+3m'w = O((n+1)^3 log(n+2)).

On the SAME deterministic locally headed multitape realization, all parsing, dedup, pinning, authentication, low-first serialization, FinTM2 simulation, exact (n'+1)-bit output capture, recovery of the original n+1-bit count, and the zero/nonzero decision satisfy, for fixed source machine M,

    T_phys=O((B+B_A+1)^4 + T_M),
    S_peak=O(B+B_A+T_M).

The fixed stack-to-tape simulation uses O(B_A+T_M) physical steps and visited tape cells, with one tape per fixed stack, finite alphabets and bounded statement-block paths. Shared objects are counted once; no preloaded proof access is assumed.

## Conditional quantitative consequence, exact source-scope

IF the pinned MainResults.mainTheorem proposition is true under the physical semantics, then for k=3 and n'=n+4, its SECOND (variable) exponent arm gives

    T_M <= 2^{9 C (n+4) lg lg(n+4) / sqrt(lg(n+4))}.

Because lg lg n /sqrt(lg n) ->0, on canonical sources B=poly(n) one FIXED deterministic machine (not a length-dependent family or different epsilon-specific machines) computes #F and SAT(F) in 2^{o(n)} ordinary physical time. This derived rate is O(n loglog n/sqrt(log n)) in the exponent, not the stronger O(n/sqrt(log n)) available for the four-density special circuit reductions using the expM arm. There is no contradiction with P=NP. The independent kernel audit and the full ordinary-machine interpretation remain separate open trust obligations.

On arbitrary finite encoded input words of unbounded length B, only the honest T_phys=poly(B)+2^{o(n)} bound is established. This distinction matters: let an n-variable encoded formula contain an enormous number (e.g. 2^{n^2}) of repeated (x0) clauses and choose the final clause to be either (x0) or EMPTY. The two input words agree everywhere until the last fixed-width clause slot, but one is satisfiable and the other is not. A locally headed input machine must traverse Omega(B) positions to distinguish them. Thus the stronger claim of an n-only 2^{o(n)} bound for arbitrary duplicate-padded binary sources is FALSE without an input-length restriction. This is a canonicalization/encoding issue, not a counterexample to pinned MainTheorem, which only covers NoDup formulas.

## Independent finite checks

Executed the exact published JavaScript verifier revision tmr1-formal-expn-general070-v1 in a V8 isolate, deterministic xorshift32 seed 20261117. Cases: 482 (480 randomly constructed n=0..5 explicit sources, the genuine DISJ_3 control and a deliberately dense 216-distinct-clause source). 3,376 semantic/structural assertions and 86,904 assignment evaluations, zero failures. Dense case n=3,m0=216 normalized to n'=7,m'=221>4n'=28, count=0 on both sides, proving by a finite counterexample that this *general* normalizer does NOT satisfy four-density but DOES satisfy MainTheorem's actual promises. DISJ_3 original and normalized counts both equal 27. Finite evidence only checks the converter, not any claimed asymptotic solver or Lean kernel. Executable experiments/tmr/tmr1_formal_expn_general070.js (Git blob adf7d990ac1c6f402ef3573f36495d4e07f8c3b2); raw results/raw/tmr/2026-11-17_TMR1_FORMAL_EXP_N070_V8_RAW.json (Git blob 1dd47503da0c401622b6fd8264c4e131e5237481).

## Gates, negative controls, and integration

DISJ sanity: PASS restricted, exact DISJ_3 count=27; no inferred work lower bound. Relativization: PASS for the Boolean semantic/count compiler; an NP-level complexity separation is NOT derived and the general NP promotion remains OPEN (Baker-Gill-Solovay, algebrization, Natural Proofs). Simultaneous DTISP: PASS for the same execution UPPER time/space ledger; NOT APPLICABLE to any FLMV forbidden deterministic pair. Deterministic configuration counting: PASS only as an upper-bound consistency control, NEVER a work lower bound or randomized/quantum transfer.

Horn, 2-SAT, affine, treewidth, equality, autarky, product, padding, auxiliary, selector, unique-solution and cached/shared circuits remain legitimate cheap controls; the converter assigns no intrinsic hardness. Hostage_Negotiator.pdf's globally consistent proof and fresh-query observations do not imply a small evaluator or necessary information gain; this work does not invoke them as a solver.

Integration point: replace any improper *four-density* premise in a general explicit 3CNF-to-formal-counter transfer with this density-free converter and the expN arm. Preserve the stronger special C1b/C1c density compiler and expM bound for the JMV implicit-witness hierarchy pipeline. The present lemma does NOT close the independent Lean kernel rebuild or an NP-level nonrelativizing bridge.

ONE next load-bearing dependency: independently compile MainResults.mainTheorem and ethIsFalse at the pinned source/mathlib revisions and inspect #print axioms plus Lean/nanoda kernel acceptance and FinTM2 semantics. No full LaTeX build or repository preflight was executed.

## Source links

- https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean
- https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/Solution.lean
- https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Computability/TuringMachine/StackTuringMachine.lean
- https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Computability/TuringMachine/Computable.lean
- https://github.com/j15marti/pnp/blob/main/research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md
