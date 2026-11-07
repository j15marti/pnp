# CLAUDE WORSTCASE-LOG-0001 — living-log entry (2026-11-07)

**P versus NP remains OPEN.** No task, schedule, weight, role or rule changed. Status labels per AGENTS.md.

## Corpus reviewed
Directive `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; MAIN REFEREE295 (B1/B2 single-decider separation); LSPV-1/395 handoff (uncomputable worst-case profile); issue #3 comments (LSPV-3/397, LSPV-4/389); LSPV-1 notes 412/456 (B3 meta-barrier).

## Literature check (this run)
- Cook–Reckhow: a polynomially bounded propositional proof system exists iff NP = coNP. [KNOWN THEOREM]
- Krajíček–Pudlák: NE = coNE implies an optimal proof system; E = NE implies a p-optimal one. Existence of an optimal system unconditionally is open. [KNOWN THEOREM]
- Cook–Krajíček; Beyersdorff–Müller: NP ⊆ P/poly provable in PV iff PH collapses to the Boolean hierarchy (with advice). [KNOWN THEOREM]
- Candidate clue for B3 with R = Extended Frege: if "SAT-decider A is correct" is provable in PV, Cook's translation gives polynomial-size EF proofs, hence B3-like behaviour for EF. This was NOT verified against a primary source in this run. [CANDIDATE]
  - It is a conditional bridge only. It needs a PV-provable correctness proof of the unknown decider, which is stronger than SAT ∈ P.
  - Soundness is the crux: a transcript is not an R-proof unless R can verify A's correctness.

## Duplication audit
The meta-barrier "B3(R) is equivalent to P != NP for any R with a known unconditional superpolynomial bound (e.g. Resolution, Haken)" is already in the corpus (LSPV-1 notes). Not claimed as new here.

## Reading of the required shape of the bridge
- Any R with a proved unconditional lower bound makes B3(R) equivalent to the target, so it carries no information.
- A useful R must therefore be strong enough that LB(R) is open (EF-like or stronger) and weak enough that LB(R) might be provable.
- B3(R) then says "P = NP implies R is p-bounded".
- The only known route to that is a provable-correctness hypothesis (PV or similar). Plain SAT ∈ P gives no such proof.
- Next target: state the weakest provability hypothesis H such that H ⇒ B3(R_mix341) and H is implied by SAT ∈ P for some natural reading, or show H is strictly stronger. [OPEN]

## What changed relative to root main
Nothing; no root main.tex edit in this run (log entry and literature pointers only).

END_OF_VERIFIED_REPORT::CLAUDE::WORSTCASE-LOG-0001
