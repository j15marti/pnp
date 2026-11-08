# CLAUDE worst-case log: B3 reduces to a reflection hypothesis (2026-11-08)
Status: KNOWN THEOREM transfer + OPEN gap. Not a proof of P vs NP.

## Statement (KNOWN, Cook 1975 / Cook-Reckhow / Krajicek-Pudlak)
Let R = Extended Frege (EF). If A is a poly-time SAT decider AND PV (equivalently EF, via
translation of the Pi^b_1 reflection statement) proves "A is correct on UNSAT answers", then
Wbar_EF(N) <= poly(N). So B3 holds for R=EF under the extra hypothesis REFL(A,R).

## Consequence
Superpoly lower bound for Wbar_EF excludes only SAT-in-P by algorithms with PV-provable correctness,
not P=NP. B3 unconditional for fixed R=EF is the open question "P=NP => EF polybounded"
(related to Pich-Santhanam arXiv:2312.08163: EF lower bounds + extra hypotheses => P!=NP).
For weak R (Resolution, PC, Res(PC_r)) B3 is FALSE-looking: lower bounds exist while SAT in P is
not contradicted; B3 forces R strong enough to simulate any provable-correct algorithm.

## Levin-search illustration
Levin universal search is sound on SAT answers (assignment checkable) but its UNSAT answers are
correct only if a good program exists, i.e. exactly the unproved reflection step. This is why a
machine trace alone is not an UNSAT certificate (matches the 2026-11-02 directive).

## Next target
T-REFL: find the weakest R-provable form of REFL that follows from SAT in P without
assuming provable correctness (e.g. via witness-free / improper-algorithm arguments), or show
relativized model where P=NP but EF is superpoly (known open; Krajicek).

## Literature checked this run
- Alekseev, Theory of Computing 22 (2026): exp lower bound for PC with extension rule (algebraic, not EF).
- Pang arXiv:2610.00837 already in corpus; arXiv:2506.16956 (Proof Analysis Problem): P=NP makes every system automatable.
No literature clue closes T-REFL. P versus NP OPEN.
