# CLAUDE / WORSTCASE-LOG-0001 — living log entry, worst-case derivation cost

2026-11-04 (scheduled run). Status: **OPEN**. P versus NP remains OPEN. No new theorem is claimed.

## Objective (unchanged)
W̄_R(N) = max over UNSAT F with |<F>| ≤ N of min over refutations π in R of cost_R(π); search cost for the optimal π is not charged.
Weakest bridge B3: SAT ∈ P ⟹ W̄_R(N) ≤ poly(N) for one fixed R.

## Corpus reviewed (survey, not byte-by-byte)
AGENTS.md; LSPV-1/391 (encoding invariance, Haken anchor, R_mix341); LSPV-1/398 B3 back-translation firewall; MAIN referees 343/345 (sandwich, certificate-work P-equivalence); coordination 344 (balanced p-min / p-optimal); GROKPROOF 2026-11-04_2315 (black-box child-generation bound Ω(M·m), white-box extraction OPEN); existing research/agents/claude/ ledger and tport notes. Nothing here duplicates or contradicts those; this entry adds literature pointers only.

## Obstacle restated (two)
1. **Weak R:** if W̄_R is unconditionally superpolynomial (Haken for Resolution), B3(R) is *equivalent* to SAT ∉ P — so B3 is no easier than the goal (already recorded in the corpus, LSPV-1/391, 398).
2. **Strong R (EF-like):** B3(R) needs "SAT ∈ P ⟹ R has poly proofs of all tautologies". That requires R to *prove the correctness* of the unknown polynomial-time algorithm (or a p-optimal-style simulation of every Cook–Reckhow system). Neither is known; a poly-bounded system exists iff NP = coNP, but one *fixed* R being poly-bounded is strictly stronger.

## Literature clues found this run (classification per AGENTS.md)
- Pich–Santhanam, *Towards P≠NP from Extended Frege lower bounds*, arXiv:2312.08163. **KNOWN THEOREM (conditional).** Gives conditional links between EF lower bounds and P≠NP; relevant to obstacle 2: the bridge SAT∈P ⟹ EF p-bounded is exactly what needs the "EF proves the algorithm correct" input. Classification: useful structural analogy; the missing theorem is unconditional provability of the algorithm's correctness in EF.
- Khaniki–Pich–Sokolov, *Efficient Adversaries*, CCC 2026 (LIPIcs.CCC.2026.8). **ANALOGY/CANDIDATE.** Constructive-lower-bound / prover–adversary framing; suggests asking whether a lower bound for fixed R can be made constructive (anticheckers). Not a transfer to our R_mix341; no object correspondence yet.
- arXiv:2506.16956v2 (Proof Analysis Problem): proof analysis for EF is NP-complete. **FAILED/IRRELEVANT TRANSFER** for the lower bound, since our min ignores search cost.
- Alekseev (ToC 22, 2026): exponential bit-size lower bounds for an EF-simulating Polynomial Calculus extension (subset-sum principle). **KNOWN THEOREM** for a system that simulates EF; check whether its "algebraic circuit extension variables" system can serve as a candidate R in which a superpolynomial W̄_R is provable AND B3 is plausible. This is the most promising new lead: a provable lower bound in an EF-strength system would sit on the other side of the weak-R equivalence, so it must then fail to be simulated polynomially by any algorithm-correctness-carrying system unless P ≠ NP.
- Hidden-structure caution: extension variables are also the hidden algebraic structure an algorithm can exploit.

## Next decisive gap
Decide whether Alekseev's EF-simulating algebraic system, with its cost model charged as bit-size, can be compared to R_mix341 (does it polynomially simulate it, or vice versa), and whether the subset-sum lower bound survives the corpus' charged-cost conventions. If it simulates EF *and* the lower bound holds for a fixed family, state exactly the missing bridge: SAT ∈ P ⟹ that system has poly bit-size refutations of subset-sum.

I did not read the full text of the cited papers this run (search summaries only); statements about them are **UNVERIFIED pending primary-text check**. Root main.tex not modified (Claude role has no ownership region).

% END_OF_LOG::CLAUDE::WORSTCASE-LOG-0001
