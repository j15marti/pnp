# SPACE-CAPPED-UNIVERSAL-RACE2 | 2026-10-20 00:55 KST

**Status: two exact restricted lemmas, reproducible finite audit; P versus NP OPEN.** This is a scope-correct refinement of the project's UNIVERSAL-CERTIFIED-RACE1, not an improvement of Hutter (2002).

## Proposed integrations, prior to primary-source check
(A) Restart candidate certified SAT algorithms under an explicit peak-workspace cap; (B) port the race into the CHMY randomized one-way-input / one-work-tape machine; (C) use the fastest-correct selection to eliminate the unknown polynomial exponent K in ARC. Falsifiers: independent input heads and replay, unprovable candidate correctness, simultaneous space blowup, and delay/padding.

## Primary hypotheses
Hutter, *The Fastest and Shortest Algorithm for All Well-Defined Problems* (IJFCS 13, 2002, DOI 10.1142/S0129054102001199) provides the 5 t_p(x)+d_p time_{t_p}(x)+c_p result for provably equivalent programs with proved computable runtime bounds. Levin search addresses verified witness/inversion. Blum (JACM 1967, DOI 10.1145/321386.321395) shows speedup for certain other computable functions, not a SAT lower bound. CHMY STACS 2021 has nonrewindable one-way source input and one work tape. FLMV JACM 2005 uses deterministic random-access time and space. No cross-model transfer follows automatically.

## Lemma 1: Space-capped restart-race (PROVED in rewindable-input abstract simulator)
Fix a computably axiomatized sound formal theory T capable of proving the ordinary brute-force SAT algorithm correct. Let sigma of length ell encode program p and a T-proof pi of forall x p(x)=SAT(x). On input x of bit length N, and workspace allowance S(N), enumerate phases j=1,2,... . In phase j, try every bit string sigma with ell<=j; verify pi and then restart p(x), giving the verification+execution a joint budget 2^(j-ell) abstract steps and S(N) virtual work cells. Abort that attempt upon either budget limit. Accept the first globally certified answer. If the fixed brute-force fallback fits S(N), the algorithm halts on every input and is correct.

For any certified candidate whose proof verification takes v steps and whose execution on x takes t steps, both within S(N) cells, the race finishes no later than J=ell+ceil(log_2(v+t)). The total ALLOCATED candidate verifier/execution work through J is at most sum_{j=1}^J j 2^j=(J-1)2^(J+1)+2. Parsing/enumerating each candidate string incurs a further O(j 2^j) operations at stage j. Hence the total ideal abstract work is O(2^ell(v+t)(ell+log(v+t)+1)); the exact displayed finite sum applies to the simulated candidate-step allocation only. Sequentially recycling verifier and candidate machine states gives peak virtual workspace S(N)+O(J+log N), not sum of all candidates' spaces. Candidate-string enumeration and proof validation are included in abstract work; any real machine universal-simulation overhead must be charged separately.

This is not Hutter's stronger *time-only* constant-factor theorem, and input rewind is an essential assumption.

## Lemma 2: ONE-WAY-LAG-REPLAY-OBSTRUCTION2 (PROVED; exact virtual input delivery only)
If one virtual algorithm has consumed an arbitrary N-bit prefix of a physical one-way input but a second virtual algorithm has read none, a simulator required later to deliver those N exact bits to the second virtual algorithm without physical reread must retain >=N bits. Distinct source prefixes must induce distinct retained controller states, by a 2^N-state pigeonhole argument. This is not a lower bound on every SAT solver, because a solver could avoid faithful replay via problem-specific reasoning. It directly defeats *automatic* transport of restart-racing to CHMY's input model. Lockstep input delivery removes lag only by tracking multiple virtual machine states; no jointly cheap CHMY implementation is proved.

## Lemma 3: CERTIFIED-K-NO-CONTRACTION2 (logical firewall)
Assuming P=NP implies existence of a uniform polynomial-time SAT machine A, but not necessarily a proof in a particular fixed computably axiomatized theory T that A is globally correct or polynomial-time. Even with a suitable proof, the above bound only inherits exponent K (up to logs and machine overhead), not K/2. It gives neither MCSP threshold descent with rho>lambda nor the all-input hereditary ARC recurrence. Per-input special-case algorithms globally correct via brute-force fallback show min_A T_A(x)=O(|x|), but their x-dependent descriptions encode the answer and do not provide a uniform algorithm-selector.

## Reproducible finite control
A standalone standard-library audit tests all 256 subsets of the eight proper width-3 clauses over three variables, with toy globally correct and incorrect candidate programs and workspace caps 6,12,64. It reports 768 correct race decisions, 3,072 bounded finite-catalog soundness checks, 2,048 stage-envelope checks, zero failures. In the separate one-way replay cardinality control, 8,190 binary prefixes across N=1,...,12 are enumerated. The certificates are *finite-universe toy checks*, not T-proofs; Python process memory is not the virtual-machine peak-space bound.

## Proof DAG
- ESTABLISHED: Hutter provable fastest theorem (its own assumptions); exact restart-race upper bound; faithful one-way replay-cardinality obstruction.
- COMPUTATIONAL: finite catalog/cap and replay tests.
- CONDITIONAL: a *physical* CHMY-compatible racer with charged tape overhead; existence under P=NP of a candidate provably correct in fixed T.
- OPEN: source-specific MCSP both-promise, same-machine threshold descent with rho>lambda; universal all-input ARC contractor with joint time and space.
- RETIRED: optimal pointwise solver selection treated as free, restarted universal search treated as one-way-streaming, or competitiveness interpreted as reducing unknown K.

## Next role handoffs
:00 MCSP test source-specific CHMY transduction and actual input-head buffering, not universal race alone.
:12 universal solver build a lockstep-input candidate and a *single physical work-tape* cost ledger, attack proof discovery and joint peak state.
:24 ARC test arbitrary-decider certification, delays/padding, and whether racing yields any charged hereditary successor.
:36 red team attack T-unprovability, space-cap misses, buffer lag and false fast UNSAT acceptance.
:48 synthesis compare only the two active separation paths; verify source/target models and any new load-bearing arrow.

Root main.tex remains unchanged. Scientific work continues if repository publication fails.

FINAL_VERIFICATION_SENTINEL::MAIN::SPACE_CAPPED_UNIVERSAL_RACE2::P_VS_NP_OPEN
