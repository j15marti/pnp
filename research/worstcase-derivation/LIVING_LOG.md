# Living log: worst-case derivation cost  W_R(N) = max_F min_pi cost_R(pi)

Status of P vs NP: **OPEN**. Nothing below proves it. Labels follow AGENTS.md.

## 2026-11-09 run (scheduled; single-session, all five roles collapsed)

### Lemmas (this run's own reasoning, short proofs, not previously located in the corpus)

**L1 (bridge dichotomy) — PROVED/EXACT (elementary).**
Let R be a system whose derivations are poly-time checkable.
(a) If R has an unconditional superpolynomial lower bound (e.g. resolution, Haken; PHP),
    then "SAT in P => W_R <= poly(N)" is *equivalent* to "SAT not in P". It is the
    target statement itself, not a bridge toward it.
(b) If R contains a "run machine M for t steps at cost t" rule, the bridge is trivially true,
    and "W_R superpolynomial" implies SAT not in P, but is a strictly *stronger-looking*
    statement (it is a lower bound on a system at least as strong as a Cook-Reckhow system
    simulating all poly-time algorithms).
So a useful bridge must sit between: R strong enough to simulate any poly-time SAT algorithm
*with its correctness*, yet weak enough that a lower bound is provable. Known candidates are
Extended Frege / PV-reflection style systems, whose lower bounds are open.

**L2 (min over free strategy) — PROVED/EXACT.** Granting the optimal sequence for free
loses nothing for lower bounds, but W_R poly for some Cook-Reckhow R implies NP = coNP,
so "W_R superpoly for EVERY Cook-Reckhow R" is exactly NP != coNP. A lower bound for one
fixed R is weaker than that (and is open for Frege, EF). Correct reading: the programme
asks for one R that is simultaneously (i) strong enough for the bridge, (ii) provably hard.

**L3 (monotonicity in the worst case) — PROVED/EXACT.** For clause-set formulas under
resolution, min refutation size is monotone under adding clauses, so the max in W_R is
attained on minimally unsatisfiable formulas; enumeration may be restricted to MU sets.

### Computation (COMPUTATIONAL, reproducer `minres.py`, <30 s)
Exact minimal DAG-resolution derived-clause counts (iterative deepening, subsumed clauses pruned):
- PHP_1^2 (2 pigeons,1 hole): 2 steps.
- all 8 width-3 clauses on 3 variables: 7 steps (tree-optimal; equals 2^3-1).
- PHP_2^3: search exceeded the 25 s cap (no value). Chunking plan: bound k by 10..14 in
  separate runs with persisted `seen` tables, or switch to SAT-based size-k refutation encodings.
Small data only; no extrapolation claimed.

### Literature check (standard web search; no minimal-derivation-specific hits)
- Frege vs extended Frege separation still listed as open (arXiv 2104.13681).
- 2026: Davis–Robere ECCC TR26-055 (Res(log) proves bounded-depth Frege lower bounds); CCC 2026
  paper on prover–adversary games with a conditional EF / succinct-circuit-lower-bound statement
  (LIPIcs.CCC.2026.8) — to be read in full next run; semantic tree-like Frege lower bound (arXiv 2604.28172).
- Background to audit as KNOWN THEOREM transfers: Cook–Reckhow; Krajíček–Pudlák (EF and
  consistency); Pich–Santhanam (strong coNP lower bounds not feasibly provable) — the last is
  a barrier relevant to any bridge that must be proved inside weak arithmetic.

### Next steps
1. Read CCC 2026.8 and extract exactly which EF statement is conditional.
2. Decide whether any fixed R of "EF + reflection for SAT-deciders" form makes the bridge provable
   while keeping a candidate hard UNSAT family (Red Team: test PHP, Tseitin, random 3-CNF).
3. Resource Auditor: add peak-space accounting (DAG-like vs tree-like) to the cost model.

Open arrows: lower bound for any R satisfying the bridge (OPEN); NP vs coNP (OPEN); P vs NP (OPEN).
