# CLAUDE WORSTCASE-0001: the bridge `SAT in P => W_R(N) <= poly(N)` — audit
2026-11-07 | all five roles' shared objective W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi) | **P vs NP remains OPEN. No lower bound is claimed.**

## 1. Formalization (PROVED/EXACT, elementary)
R = fixed proof system (poly-time verifier V_R(F,pi), cost = size, or size+space). Free choice of the best pi (no charge for discovery) makes W_R a *nondeterministic* quantity: W_R(N) <= poly iff UNSAT-refutations in R are certificates in the Cook–Reckhow sense.
- **Prop 1 (Cook–Reckhow 1979, KNOWN).** Some R has W_R poly iff NP = coNP. So any single-R superpolynomial W_R bound is *weaker* than NP != coNP; a bound for *every* R is *equivalent* to it, hence strictly stronger than P != NP (NP != coNP => P != NP).
- Consequence: freeing the derivation order puts the target on the coNP side. The "min over sequences" strategy is legitimate (it only lower-bounds), but the strongest version of it proves more than P != NP, and the weak version (fixed R) proves nothing about P vs NP without the bridge.

## 2. The bridge is logically trivial as a bare implication (PROVED/EXACT)
Let B(R) := (SAT in P => W_R poly). Classically B(R) <=> (P != NP) or (R poly-bounded).
- If R has a *known* superpolynomial lower bound (Resolution, PC, CP, bounded-depth Frege), R is not poly-bounded, so B(R) <=> P != NP. **Proving B(R) for such R is exactly proving P != NP**; the bridge adds no leverage there. It is also why Resolution/PC/CP hard families (Haken, Urquhart, BGIP, LSPV-3/468) cannot be the bridge's R.
- If R = Extended Frege (or a stronger "combined" system), the lower bound is OPEN, so B(R) is a genuine claim that needs a *uniform proof inside R*: from any poly-time decider A and F, build a poly-size R-proof of UNSAT. That requires R to prove "A is sound" for an *unknown* A. This is Cook–Krajicek-type provability (PV/EF proving correctness of the SAT algorithm). Not known; also not known to fail.
- **Prop 2 (KNOWN folklore).** Under P = NP the decider itself is a poly-bounded and p-optimal system. A *fixed explicit* R achieving the same unconditionally is an optimal proof system; existence of one is OPEN (Krajicek–Pudlak 1989; EF is the pivotal candidate). So the weakest sufficient bridge is *as hard as*: "EF (or the chosen combined system) is p-optimal, or at least poly-bounded under P=NP." CANDIDATE only.
- **Adding rules cannot cheaply repair this.** A rule "e halts in t steps with UNSAT on F" for every program e is unsound unless e is correct; a *guarded* version needs a correctness proof of e, which is the same missing provability statement (Loeb/Godel-type obstruction for uniform soundness). Classification: FAILED TRANSFER for the naive "add a universal-algorithm rule".

## 3. What a viable route must look like (CANDIDATE)
Two non-circular shapes only:
1. (Pich–Santhanam type, 2023 preprint, conditions unverified here) pair an *unconditional* lower bound for a function class with *unprovability in EF* of that bound -> P != NP. Needs a hard-family + unprovability theorem; both open.
2. A direct W_R lower bound for R = EF/Frege-with-extension and a **separate** proof of B(R) via uniform correctness-provability. Neither piece exists. Note that (2) would prove P != NP only through B(R), which is not weaker than the goal (section 2).
Honest status: the project's conditional bridge is reduced to "EF proves soundness of every P-algorithm for SAT", equivalently conditional p-optimality of the fixed system. OPEN.

## 4. Hard-family survival checklist (carry-over to Role 3/5, from existing corpus)
Resolution: expander-Tseitin exponential (known). PC char != 2: BGIP/AR exponential (known). Mixed AND3/GF(2): LSPV-2/341 poly via gadgets (corpus). Hence any candidate "hard" family must be tested against Res(XOR)/PC_GF2/EF; for EF the best-known candidates are open (no superpoly EF lower bound for any family).

## 5. Literature clues this run
Existence of optimal/poly-bounded systems and Extended Frege as pivotal: [Propositional proof system](https://en.wikipedia.org/wiki/Propositional_proof_system), Krajicek [frege.pdf](https://msekce.karlin.mff.cuni.cz/~krajicek/frege.pdf); Pich–Santhanam conditional separation (2023). No 2025–26 result found that closes either piece (standard search; low yield).

## 6. Time-space/resource-auditor note
Costing space too (size+space of the derivation) is the Ben-Sasson–Nordstrom regime; tradeoff lower bounds exist only for weak systems (Res/PC), none for EF. Lower bounds there cannot feed the bridge (section 2).

## 7. Repo reconciliation
Duplication/overlap: proof-system fallback LSPV-5/163 (fixed verifier under P=NP), worst-case routes 335/341/350 (RUNTIME-POLLUTION referee 295). Nothing here strengthens any status; root main.tex not edited (LSPV ownership regions untouched). Recommended ledger tag: statement "B(R) for R with known lower bound" is equivalent to P != NP (reformulation, not progress).

STATUS: P vs NP OPEN. # END_OF_VERIFIED_REPORT::CLAUDE::WORSTCASE-0001
