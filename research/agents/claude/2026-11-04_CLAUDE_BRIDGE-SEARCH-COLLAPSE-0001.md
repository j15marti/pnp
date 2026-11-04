<!-- CLAUDE REPORT::BRIDGE-SEARCH-COLLAPSE-0001::2026-11-04 -->
# BRIDGE-SEARCH-COLLAPSE-0001 — the weakest bridge, restated under SAT in P

**Status:** PROVED (short, standard-technique proof, hand-checked, not machine-verified) for the equivalence below. Superpolynomial `Wbar_R`, B1/B2/B3 for `Rmix341`, and **P versus NP remain OPEN**. No task, schedule, calculus or weight changed.

Objective: `Wbar_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)`. Priority bridge: `SAT in P ==> Wbar_R(N) <= poly(N)`.

## Corpus reviewed (survey, not byte-for-byte)
`research/main` REFEREE305, 317, 318, 326; `research/coordination` LSPV5 REFEREE326 handoff; Claude world-ledger rows L34-L40; repository search for "p-optimal", "self-reduction", "search-to-decision". Literature: Cook–Reckhow 1979 (standard), Krajíček ECCC 2021/053 (proof-search information vs. proof length), survey material on polynomially bounded and p-optimal systems. A search for 2025-26 work on "P=NP implies fixed Frege/EF bounded" found nothing new.

## Duplication audit
REFEREE317 proves: under a fixed correct decider `A`, B3 for `R` is exactly *length* simulation of the trace system `D_A`, and says p-simulation (a poly-time translator) is *stronger* and "moves toward B1". REFEREE326: minimax with description charge is P/poly. Neither records the collapse below.

## New statement (Proposition S)
Let `R` be a Cook–Reckhow refutation system (poly-time verifier, sound and complete for UNSAT CNF) with cost at least proof size up to a fixed polynomial. Assume `SAT in P` via decider `A`. The following are equivalent:

1. `Wbar_R(N) <= N^O(1)` (the bridge consequent; B3-type length bound);
2. there is a poly-time algorithm that, given UNSAT `F`, outputs an `R`-refutation of `F` (B1-type proof acquisition);
3. `R` p-simulates every Cook–Reckhow system (`R` is p-optimal).

**Proof.**
(1 => 2). The language `L = {(F, u) : some R-refutation of F with |.| <= q(|F|) has prefix u}` is in NP, hence in P by assumption. Prefix search with `|u|<=q(|F|)` queries to `L` outputs a refutation. (Here `q` is the polynomial from (1).)
(2 => 3). Let `S` be a Cook–Reckhow system with poly-time proof-to-formula map `f_S`. Given an `S`-proof `pi`, compute `F = f_S(pi)`, then run the algorithm from (2). Output length and time are polynomial in `|pi|`.
(3 => 1). `D_A` (statement `F`, proof = copy of `F`, accept iff `A(F)=UNSAT`) is a poly-time verifiable, sound and complete system with proofs of size `O(|F|)`. Its p-simulation into `R` gives `R`-proofs of polynomial size. Soundness of `D_A` uses the quantified premise that `A` is correct everywhere (as in REFEREE317). `QED`

## What follows
* **Collapse of B3 to B1 under the premise.** Given `SAT in P`, the length bound (REFEREE317's B3) already yields the poly-time proof finder. The B3-versus-B1 gap exists only in worlds where `SAT notin P`, and the bridge is vacuous there.
* **Bridge restated.** `SAT in P ==> Wbar_R poly` is equivalent to `SAT in P ==> R is p-optimal`. Since `P=NP` gives a polynomially bounded system (Cook–Reckhow) and (1<=>3) shows any such system is p-optimal in that world, the bridge says exactly that the fixed `R` is a representative of the optimal class whenever one exists. This is a precise measure of the bridge's strength, not an obstruction, and not a proof.
* **Consequence for the plan.** A direct proof of the bridge for `Rmix341` cannot use a *weaker* intermediate than "`Rmix341` simulates all of `D_A`". Reflection-family routes (REFEREE318) and restriction routes target the same quantity. The *only* freedom left is the choice of `R`.
* **Free-optimal-sequence remark.** Allowing a free minimizing derivation is compatible with Proposition S: step (1=>2) is exactly where search cost would be charged, and it is polynomial under the premise. It is never charged inside `Wbar_R`.

## Controls and honest limits
* Both-label check by definition: if `F` is SAT, `D_A` and `R` both reject; a corrupted proof copy is rejected by `D_A` (malformed-string case).
* No computation was run. The proof uses only standard Cook–Reckhow facts; no experiment backs it.
* Not shown: `Rmix341` (or any fixed `R`) actually satisfies (1) unconditionally, and no hard UNSAT family for the fixed calculus is exhibited. Haken PHP and Tseitin remain ordinary-Resolution-only families (defeated by ER / GF(2) in `Rmix341`).

## Next obstacle (assigned to all five roles)
Find an `R`-restricted family `H_N` with `Wbar_R(N) >= W_R(H_N)` (REFEREE318 form) whose `W_R(H_N)` is superpolynomial, or show the three-clause trilemma of REFEREE326 closes. Red-team target: any candidate whose lower bound survives the all-rules axiom-monotonicity firewall (REFEREE305).

<!-- END_OF_VERIFIED_REPORT::CLAUDE::BRIDGE-SEARCH-COLLAPSE-0001 -->
