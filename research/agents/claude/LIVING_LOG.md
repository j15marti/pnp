# Living log — external Claude research track

Append-only, newest first. This track is **external to LSPV-1..5**: it edits no
root `main.tex` ownership region, changes no task schedule, agent count or role
allocation, and adds no mandatory preflight read. Findings are offered to the
five roles as inputs. **P versus NP remains OPEN.**

Status vocabulary follows `AGENTS.md`: PROVED/EXACT, KNOWN THEOREM,
COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

---

## 2026-11-13 01:48 PST — BRIDGE-EQUIV-0001 (red team on the shared worst-case directive)

**Report:** `research/agents/claude/2026-11-13_0148_CLAUDE_BRIDGE-EQUIV-0001.tex`
**Repo head reviewed:** `6a9ccb7c` (main, 2026-11-13 01:45:43 -0800)
**Target audited:** the shared objective
`W_R(N) = max_{F ∈ UNSAT, |F| ≤ N} min_{π : F ⊢_R ⊥} cost_R(π)` and the
prioritized bridge `Bridge(R): SAT ∈ P ⟹ W_R(N) ≤ poly(N)`.

**Findings (all negative, all PROVED/EXACT but elementary):**

1. **Bridge collapse.** For a fixed system `R`,
   `P ≠ NP ⟹ Bridge(R)` vacuously, and if `W_R` is superpolynomial then
   `Bridge(R) ⟹ P ≠ NP`. Hence for **every** `R` with a *known* unconditional
   superpolynomial lower bound — resolution (Haken), tree-resolution, Res(k),
   NS/PC/PCR over a fixed field, cutting planes (Pudlák), bounded-depth Frege
   (Ajtai; Pitassi–Beame–Impagliazzo) — `Bridge(R)` is **logically equivalent to
   P ≠ NP**, and is *false* in Algorithmica. Ledger row **L41**.
2. **No decomposition gain.** For every fixed `R`, the conjunction
   "superpolynomial lower bound on `W_R`" ∧ `Bridge(R)` is equivalent to
   `P ≠ NP`. Splitting the goal in two transfers difficulty, it does not reduce
   it. The decomposition carries information only where the lower-bound half is
   **OPEN**: Frege, Extended Frege, TC⁰-Frege, and unrestricted-sharing /
   extension multisign DAGs. Ledger row **L42**.
3. **What P = NP actually buys.** `SAT ∈ P` makes every Cook–Reckhow
   system *automatable*: a **minimum-length** refutation is computable in time
   `poly(N + min_π |π|)` (binary search on the size bound + prefix
   self-reduction). It yields **no** bound on `min_π |π|` for a fixed `R`.
   So the directive's deliberate "no charge for finding the optimal sequence"
   convention is sound as a lower-bound convention and simultaneously discards
   the single known link between the hypothesis `SAT ∈ P` and a fixed proof
   system. Atserias–Müller (non-automatability of resolution is NP-hard) cannot
   restore the link: it is conditional, and an unconditional version would
   already imply `P ≠ NP`. Ledger row **L43**.
4. **Cost-measure collapse.** Any cost measure dominated by resolution
   clause space (`≤ n+2`), width (`≤ n`) or derivation depth (`≤ n`) has
   `W_R(N) ≤ poly(N)` unconditionally, so it cannot carry the target at all;
   Torán's `Ω(n)` space bound for PHP already matches the trivial ceiling. The
   shared objective must be read as a **length-like** measure. Peak memory
   should be an auditing quantity only, not part of the objective. Ledger
   row **L44**.

**COMPUTATIONAL (exact, free-strategy minima, stage-split, < 30 s per stage):**
`experiments/claude_wr/exact_treeres_min.py`,
`experiments/claude_wr/cost_measure_collapse.py`;
raw `results/raw/claude_wr/2026-11-13_0148_treeres_exact.json`,
`results/raw/claude_wr/2026-11-13_0148_cost_measure_collapse.json`.

| instance | vars | clauses | N | min tree-res leaves | min nodes | min depth | space ≤ |
|---|---|---|---|---|---|---|---|
| PHP(2,1) | 2 | 3 | 7 | 3 | 5 | 2 | 4 |
| PHP(3,2) | 6 | 9 | 27 | 11 | 21 | 4 | 6 |
| Tseitin K₄ odd | 6 | 16 | 64 | 28 | 55 | 5 | 7 |
| PHP(4,3) | 12 | 22 | 70 | 43 | 85 | 7 | 9 |

These confirm the inner minimum is well-defined and computable at small scale;
they are **not** evidence of superpolynomial growth and must not be cited as
support.

**Literature checked this run:** Cook–Reckhow 1979 (p-bounded system exists iff
NP = coNP); Krajíček–Pudlák 1989 and Köbler–Messner–Torán on (p-)optimal
systems, existence for TAUT still **OPEN**, with Egidy–Glaßer (STOC 2025) /
Egidy (arXiv:2602.02294, preprint, unverified) oracles ruling out relativizing
positive proofs; Krajíček ECCC TR21-053 (time-optimal proof search exists iff a
p-optimal system exists — the exact home of the "free optimal sequence" grant);
Atserias–Müller JACM 2020; Pich–Santhanam arXiv:2312.08163 (the live route in
the only non-vacuous regime, via bounded-arithmetic provability of
soundness/reflection, not derivation-cost minimization).

**Recommendation to the five roles:** state which regime a run is in; fix a
length-like cost measure explicitly; above the frontier, write down the missing
object correspondence between a multisign-DAG cost and an EF-provable
reflection principle. No schedule, role or allocation change is implied.

---

## Earlier entries (reconstructed from the artifacts, not from this run's work)

- **2026-10-28 15:21 — ONETAPE-0001.** One-tape crossing-sequence review;
  bound holds nondeterministically, so it cannot separate P from NP; ledger
  rows L38–L40.
- **2026-10-28 14:52 — TPORT-0002.** Asymptotics of the provable exponent,
  `1 + Θ(1 − d)`; ledger row L37.
- **2026-10-28 13:26 — TPORT-0001.** Alternation-trading barrier at the UWI
  portfolio size; ledger rows L34–L36.
- **2026-10-28 09:39 — DIRECTPRODUCT-0001.** Direct-product route to the UWI
  common-input statement is dominated; ledger rows L29–L33.
- **2026-10-28 09:24 — WORLD-LEDGER-0001.** The 40-statement five-worlds ledger
  (`world-ledger/`), with the classifier that flags a statement equivalent to
  P = NP or P ≠ NP as a reformulation rather than progress.
