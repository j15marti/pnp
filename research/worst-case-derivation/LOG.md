# WCD living log (append-only)

## 2026-11-08 run 1 (scheduled)
Corpus: repo surveyed; no prior WCD directive/W_R file existed (grep of research/ and tasks/ found only unrelated hits).
Existing ARC/FLMV spine and AGENTS.md allocation untouched; no edits to main.tex (ownership markers not used this run).

### Findings (status labels per AGENTS.md)
1. W_R is proof-size complexity when cost = length and the optimal pi is free. [PROVED/EXACT, definitional]
   Free strategy choice adds nothing beyond the min; it is exactly the Cook-Reckhow measure.
2. NP != coNP  <=>  for every proof system R, W_R is superpolynomial. [KNOWN THEOREM, Cook-Reckhow 1979]
   So "superpoly W_R for a fixed R" alone is weaker than NP != coNP, and "for all R" is equivalent to it;
   the fixed-R program is therefore a proof-complexity program, not a shortcut.
3. Bridge B(R) for natural fixed R is false-or-open, by cases:
   - R = resolution / cutting planes / bounded-depth Frege: B(R) cannot be used:
     B(R) is an implication whose consequent is false (Haken; Pudlak; Hastad etc. give exp lower bounds),
     so B(R) is equivalent to "SAT not in P" -- i.e. it would ASSUME P != NP. [KNOWN THEOREM lower bounds; consequence PROVED]
     Hence bridge over weak R is circular/useless. Lower bounds there cannot support P != NP via B(R).
   - R = Extended Frege: B(EF) means EF is p-bounded given SAT in P. OPEN. It would follow if the correctness of the
     poly-time decider were provable in PV/S^1_2 (Cook translation) -- CONDITIONAL, but SAT in P does not give
     provability, so not a proof of B(EF).
   - R optimal/p-bounded-universal: B(R) holds for R that p-simulates all systems, but existence of such R is OPEN
     (Krajicek-Pudlak); believed not to exist.
4. Consequence (key obstruction, "uniformity gap"): a bridge must be proven for a R fixed before the algorithm is given.
   The trivial R_M = "accept computation trace of M" is algorithm-dependent and its soundness is not locally checkable.
   Charging for checking soundness is exactly where the cost reappears. CANDIDATE diagnosis, not a theorem.
5. Contrapositive reading: proving EF (or any fixed R) has superpolynomial W_R gives P != NP only through
   B(R). The weakest sufficient transfer theorem is therefore "EF (or a stronger fixed R) p-simulates every
   poly-time SAT decider's refutations", i.e. a uniform reflection principle for SAT-deciders. OPEN.
   Direct-proposal for roles 2/5: find R closed under "decider-trace with certified local invariants" and test if
   hostile controls (Pich-Santhanam 2023: EF not p-bounded + assumptions => P != NP, conditional) are consistent.

### Literature check (this run)
- Pich & Santhanam, "Towards P != NP from Extended Frege lower bounds" (arXiv 2312.08163): conditional implication only.
- Alekseev (CCC 2021): EF-simulating algebraic system with exp lower bound for a specific principle; shows algebraic setting easier.
- Krajicek: no known unconditional superpoly lower bound for EF; existence of p-optimal system open.
- No 2025-26 breakthroughs found by one standard search (limited check).

### Next targets
- Role 1: formalize B(R) for R=EF and the reflection hypothesis in item 5; decide whether it is implied by SAT in P (suspect not provable without more).
- Role 3: hard families vs EF/PC with extension; role 4: cost model (length vs space vs time) so W_R definition is fixed.
- Role 5: attack item 3 first bullet: confirm no weak-R lower bound can feed B(R).

P versus NP remains OPEN. No proof claimed.
