# Living log: worst-case minimal-derivation programme (W_R)

Target: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi); free choice of pi (search not charged).
Weakest bridge sought: B_R :  SAT in P  =>  W_R(N) <= poly(N).
**P versus NP remains OPEN. Nothing below proves a lower bound or the bridge.** Statuses: PROVED/EXACT, KNOWN THEOREM, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## Run 2026-11-05 (scheduled; single agent; corpus review PARTIAL: repo surveyed, `research/explorations/arc/2026-10-31_BINARY_HYPERGRAPH_FORWARD_REVERSE1.md` and AGENTS.md read-listed but not re-audited; no peer .tex reports for this directive existed — no prior W_R log found by grep)

### R1. Hardwiring trivialisation — PROVED/EXACT (elementary)
If a "derivation system" lets a step assert unsatisfiability of F without a polynomial-time local check (e.g. step = "machine e rejects F", e chosen per instance, uncharged), then min-cost is O(|F|) (e prints the answer). So the system R must be a Cook–Reckhow (CR) system: derivations poly-time checkable. Free choice of pi is then exactly nondeterminism, and W_R is a proof-size measure.

### R2. Identification with proof complexity — KNOWN THEOREM (Cook–Reckhow 1979)
For CR system R: W_R poly  <=>  R polynomially bounded. "W_R superpoly for EVERY CR system" <=> NP != coNP. This is sufficient for P != NP but strictly stronger as a target (P != NP does not imply NP != coNP). So a universal-R lower bound is a *harder* goal than P vs NP, not a weaker one. Charging nothing for search moves the problem from P vs NP to NP vs coNP.

### R3. The bridge for a fixed R — PROVED/EXACT (new framing; elementary)
(a) If R has an unconditional superpolynomial lower bound (e.g. Resolution, Haken; Polynomial Calculus, etc.) then B_R is EQUIVALENT to P != NP (its conclusion is false, so B_R says exactly "SAT not in P"). So proving B_R for such R is as hard as the problem; it cannot be a "weaker sufficient bridge".
(b) If SAT in P, then the trivial CR system R_A (empty proof; accept iff A(F)=1) is polynomially bounded. If R is p-optimal (p-simulates every CR system), B_R holds. So B_R is available for p-optimal R. Existence of a p-optimal system for TAUT is OPEN (Krajicek–Pudlak 1989; implied by E=NE; Kobler–Messner–Toran; Boolean-hierarchy equivalences in MFCS 2023). Recent: Egidy–Glasser (STOC 2025) and Egidy (arXiv 2602.02294, Feb 2026, SPARSE relativization) give oracle worlds — relativizable proofs of positive answers are ruled out, so the bridge cannot come from black-box simulation arguments.
(c) Consequence: the only R for which B_R is a nontrivial bridge are R that are (conditionally) p-optimal, i.e. that can internalise correctness of an arbitrary polytime SAT algorithm. Standard systems (Res, PC, CP, Frege, EF) fall in (a) or are unknown; for Frege/EF, B_R holds if the polytime algorithm's correctness is provable in the matching bounded-arithmetic theory (Cook translation, PV -> EF), but P=NP alone does not supply that provability. CANDIDATE reformulation: B_R follows from "P=NP => some PV-provably-correct (or R-reflected) SAT algorithm" — this is a proof-theoretic hypothesis (cf. Krajicek's work on provability of P=NP), not weaker than the target.

### R4. Hard families vs. combined/adaptive systems — status table
- Tseitin on expanders: Res exp. lower bound (Urquhart), but poly-size Frege/EF proofs ⇒ FAILS against strong R (known).
- Random k-CNF: Res/PC exponential; Frege/EF lower bound OPEN. Candidate only.
- Combined system R1⊕R2 (disjoint union, strategy switching): W ≤ min(W_R1, W_R2); still a CR system; lower bound for a combination of weak systems is not evidence for strong ones.
- Circuit-compression / shared DAG: Frege vs. Extended Frege separation is OPEN; DAG-sharing is exactly the EF-type power; no super-poly Frege lower bound known (a 2026 literature check found none; Filmus–Pitassi–Santhanam: exp. AC0-Frege bounds would give super-poly Frege bounds).
- Algebraic route: Alekseev (ToC 22, 2026): exp. lower bound for binary value principle in an extended PC system simulating EF — over Q only, a restricted algebraic system, not Frege.
- Time-space: cost including peak memory (Esteban–Torán clause space etc.) is a *different* measure; bridge to SAT in P with small space would need a space-bounded analogue; unaudited.

### R5. Net assessment and next targets (all OPEN)
1. Retire the claim that B_R is a "weakest sufficient" bridge for generic R: by R3(a) it is equivalent to the conclusion for any R with a known lower bound.
2. Productive remaining form: choose R as a *reflective* system (EF + reflection / p-optimal candidate such as the Levin-style system) and ask whether a superpoly bound is even consistent with known oracle results (Egidy–Glasser).
3. Test multisign hypergraph DAG system R_H: (i) prove it is CR, (ii) place it relative to Res/EF by simulation (does EF p-simulate R_H? does R_H p-simulate Res?). If EF p-simulates R_H, a lower bound for R_H is no evidence for B_EF.
4. Time–space version: define cost = (time, peak memory) and test B for pairs (T,S) against known resolution time–space tradeoffs.
5. Red-team item: derive B_R failure oracle for EF (is there an oracle with P=NP and EF superpoly? — unchecked, candidate question).

Sources: Cook–Reckhow 1979; Krajicek–Pudlak 1989; Egidy arXiv 2602.02294; Egidy–Glasser STOC 2025; MFCS 2023 paper 44 (p-optimal Boolean hierarchy); Alekseev, Theory of Computing 22 (2026) a004; arXiv 2609.00422.
% END_OF_RUN 2026-11-05
