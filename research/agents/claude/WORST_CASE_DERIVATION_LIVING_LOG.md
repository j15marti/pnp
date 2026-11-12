# Living log: worst-case minimum derivation cost (Claude routine)

Shared target (all five roles):

    Wbar_R(N) = max over UNSAT F with |<F>| <= N of  min over R-refutations pi of cost_R(pi)

B1(R): Wbar_R is superpolynomial.  B2(R) (weakest sufficient bridge): SAT in P => Wbar_R(N) <= poly(N).
Optimal derivations are chosen for free; search is not charged. **P versus NP remains OPEN.**

Append-only. Newest entry at the bottom. Statuses follow AGENTS.md.

---

## 2026-11-12 00:48 UTC — BRIDGE-CONSERVATION-0001

Report: `research/agents/claude/2026-11-12_0048_CLAUDE_BRIDGE-CONSERVATION-0001.tex`

- PROVED/EXACT. If P != NP, B2(R) is true for every R, because its hypothesis is false. So no counterexample to B2 can exist unless P = NP. Red-teaming B2 means attacking proposed *proofs* of it, not looking for counterexamples.
- PROVED/EXACT, using KNOWN THEOREMS. For Resolution, Cutting Planes, PC, bounded-depth Frege and Res(PC_1/F_3), B1 is already known, so B2(S) is equivalent to P != NP. Free choice of the optimal derivation does not make B2 easier.
- PROVED/EXACT, red-team filter (the "Resolution test"). Suppose an argument derives B2 from some property that Resolution also has. Then that argument proves P != NP outright. So soundness, completeness, polynomial-time checking, DAG sharing, free optimal choice, locality and restriction closure cannot carry the bridge.
- KNOWN THEOREM, from Cook 1975 and Krajicek–Pudlak 1989. The only known mechanism is reflection: PV-provable correctness of a SAT algorithm gives polynomial-size EF proofs. B2(EF) is CONDITIONAL on the open hypothesis H_PV.
- Literature clue. Arteche–Khaniki–Pich–Santhanam (ICALP 2024) give a conditional reflection bridge for iEF via sum-check. They also report the Pich–Santhanam meta-barrier: an unconditional link "EF lower bound => NP not in P/poly" would already give NEXP not in P/poly. DAG-like Res(⊕) lower bounds are still OPEN; only tree-like, regular and bounded-depth cases are known.
- CONDITIONAL on P2-D1. Placing R_mix341 is a dichotomy:
  - Weak case: R_mix341 sits below a system with a known lower bound. Then B2 is equivalent to P != NP, and no bridge mechanism is known.
  - Strong case: R_mix341 simulates Res(⊕) or ER/EF. Then B1 is a frontier-open lower bound, and reflection is available for B2.
- Next target: determine the support of the DEF rule and whether GF(2) rows can be disjoined with clauses.
