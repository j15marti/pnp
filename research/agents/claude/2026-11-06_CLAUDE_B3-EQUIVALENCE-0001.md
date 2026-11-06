% CLAUDE REPORT::B3-EQUIVALENCE-0001::2026-11-06 (scheduled run; living-log entry)
# CLAUDE/B3-EQUIVALENCE-0001: what the bridge SAT in P => poly worst-case cost actually requires

**Status: PROVED/EXACT (elementary logic), KNOWN THEOREM (cited). P vs NP remains OPEN. No lower bound or transfer theorem is claimed.** Does not touch `R_mix341` grammar, schedules, or `main.tex` ownership regions (non-LSPV role; LSPV-5 may absorb).

## Setting
`W_R(F)` = min size of an R-derivation of `bot` from F (strategy discovery free). `Wbar_R(N)` = max over UNSAT F, |F|<=N. B3(R): `SAT in P => Wbar_R(N) <= poly(N)`. R is a Cook-Reckhow system (poly-time verifier, sound, complete).

## Fact 1 (B3 is exactly "lower bound for R => P != NP")
B3(R) is the implication `P=NP => R poly-bounded`; contrapositive: `R not poly-bounded => P != NP`.

## Fact 2 (B3 is vacuous-as-a-reduction for every R with a known lower bound)
If R has a proved superpolynomial lower bound (Resolution: Haken 1985, Urquhart 1987, Ben-Sasson-Wigderson 2001; also Res(parity)/PC/cutting planes in their ranges), then `Wbar_R` is superpolynomial is a THEOREM, so B3(R) is *logically equivalent* to `P != NP`. Proving B3(R) for such R is the whole problem, not a bridge. (Consistent with LSPV findings that Tseitin/PHP families are shortcut controls only against weak R.)

## Fact 3 (what a useful R must satisfy)
Assume P=NP via decider M. Then `Q_M` (empty proof; verifier runs M) is a polynomially bounded system (Cook-Reckhow). B3(R) holds iff R polynomially simulates `Q_M` in size on UNSAT, for whichever M exists. Thus the useful R must (a) have no known superpolynomial lower bound, yet (b) be able, under P=NP, to prove correctness of an *unknown* polynomial algorithm. Uniform sufficient condition: R p-optimal (simulates all systems); existence of optimal/p-optimal systems is OPEN (Krajicek-Pudlak 1989: NE=coNE => optimal, E=NE => p-optimal).
For R=EF: B3(EF) holds if bounded arithmetic (PV/S^1_2) proves the correctness of some P algorithm for SAT; the Levin-style universal algorithm need not have a feasible correctness proof. Related: Cook-Krajicek 2007 (consequences of provability of NP in P/poly); Pich-Santhanam STOC 2021 (strong co-nondeterministic lower bounds for NP are unprovable in S^1_2 under hardness assumptions), which says the *lower bound* side for strong R also meets a provability barrier (EF lower bounds <-> unprovability).

## Fact 4 (free strategy search is no loophole)
Min over derivations with free choice = proof length in R. Charging nothing for search gives a valid lower bound on execution, but also makes `Wbar_R` equal the Cook-Reckhow measure; a superpoly bound for general Frege/EF is a decades-open problem. Hardness of finding optimal proofs (Atserias-Muller: automating Resolution is NP-hard; Krajicek-Pudlak: EF not weakly automatable under RSA) is irrelevant to the charged quantity but shows the objects are not algorithmically accessible.

## Consequence for the research plan
1. Treat the weakest sufficient bridge as `B3(R) for an R with no known LB`; B3 for Resolution-like R is equivalent to P != NP and must never be listed as progress.
2. Any proposed R should come with an explicit simulation argument: either (i) R p-simulates a known strong system (EF) and a bounded-arithmetic proof of some SAT algorithm's correctness is *assumed as a stated hypothesis* (then result is conditional: P=NP provably in PV => EF poly), or (ii) an optimality argument. (i) yields at best a conditional separation, not an unconditional one.
3. Red-team target: find R whose B3 follows from a weaker, independently plausible hypothesis than "optimal proof system exists".

## Literature check this run
Cook-Reckhow 1979; Krajicek-Pudlak 1989; Pich-Santhanam (arXiv 2305.15235 and STOC 2021 line); Atserias-Muller 2019. No new clue closes B3; no source treated as proof.

% END_OF_VERIFIED_REPORT::CLAUDE::B3-EQUIVALENCE-0001
