# Living log: worst-case minimum derivation cost W̄_R(N)

Scheduled Claude routine. Additive; owns no root `main.tex` region and changes no schedules, roles or allocations. **P versus NP remains OPEN.**

Objective (shared directive):
W̄_R(N) = max over UNSAT F with |⟨F⟩| ≤ N of min over R-refutations π of cost_R(π);
weakest bridge: SAT ∈ P ⟹ W̄_R(N) ≤ poly(N).

## Current state (newest first)

### 2026-11-10 14:51 PST — WORSTCASE-BRIDGE-0001
Report: `2026-11-10_1451_CLAUDE_WORSTCASE-BRIDGE-0001.tex`. Ledger rows L41–L45 in `world-ledger/`.

| Result | Status |
|---|---|
| W̄_R ≤ poly ⟺ R is a polynomially bounded (Cook–Reckhow) proof system | PROVED/EXACT |
| SAT ∈ P ⟹ some proof system R_A has W̄ ≤ poly (so the bridge for a *fixed* R is an optimality claim about R) | PROVED/EXACT |
| Bridge dilemma (a): for every R with a known superpolynomial W̄_R (Res, tree-Res, Res(k), PC, CP, bounded-depth Frege), Bridge(R) ⟺ P ≠ NP | PROVED/EXACT |
| Bridge dilemma (b): Bridge(EF) holds for SAT algorithms whose correctness PV proves (Cook 1975, Krajíček–Pudlák) | KNOWN THEOREM |
| W̄_EF superpolynomial | OPEN |
| Bridge(EF) for all polynomial-time algorithms | OPEN |
| Algorithm-class bridges (CDCL → resolution, DPLL → tree-like) give unconditional lower bounds for those classes only | KNOWN THEOREM |
| Multisign DAG hypergraph calculus: horn (a) if its rules are bounded-arity clause rules; horn (b) if DAG nodes can name arbitrary gates | CONDITIONAL on the rule list |

Main finding: the free choice of the optimal sequence is sound but turns W̄_R into a nondeterministic certificate measure. All deterministic content sits in the bridge. For any calculus we can currently lower-bound, the "weakest sufficient bridge" is equivalent to P ≠ NP, not weaker.

Next targets:
1. Decide which horn the historical R_mix341 lies in (can paid auxiliary definitions name arbitrary gates?).
2. Prove a wider algorithm-class bridge, e.g. CDCL + Gaussian elimination → Res(lin), and pair it with known Res(lin) lower bounds.
3. List candidate EF-hard families (random 3-CNF, PRG tautologies) as OPEN.

Literature this run: Cook–Reckhow 1979; Cook 1975; Krajíček–Pudlák 1989/1990; Pich–Santhanam arXiv:2312.08163; Cook–Krajíček JSL 2007; arXiv:2506.16956; Beame–Kautz–Sabharwal 2004; Pipatsrisawat–Darwiche 2011.
