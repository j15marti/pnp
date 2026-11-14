# Living log: worst-case derivation cost W̄_R(N)

Scheduled Claude routine. Target: W̄_R(N) = max over UNSAT F with |F| ≤ N of min over R-refutations π of cost_R(π),
and the bridge SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). **P versus NP remains OPEN.**

## Current state (update each run)

| Item | Status |
|---|---|
| Execution lower bound for algorithms whose transcripts convert to R-proofs (T_A ≥ W̄_R^Ω(1)) | PROVED/EXACT |
| Bridge B_R is implied by P ≠ NP; B_R ∧ LB_R ⇒ P ≠ NP | PROVED/EXACT |
| For R with known lower bounds (Res, CP, AC0-Frege, PC): B_R ⇔ P ≠ NP | PROVED/EXACT (duplicates Codex 11-11) |
| Family-local / pointwise bridge for Resolution | FALSIFIED (PHP: linear-time syntactic rejection vs Haken 2^Ω(n)) |
| B_EF ⇔ (SAT ∈ P ⇒ some poly SAT decider has poly-size EF proofs of its correctness tautologies) | PROVED/EXACT (standard Cook / Krajíček–Pudlák machinery) |
| B_EF unconditionally | OPEN (CONDITIONAL on Pich–Santhanam-type S^1_2 hypotheses) |
| LB_EF (superpolynomial EF lower bound) | OPEN |
| Explicit family hard for every listed reasoning method | none known; equivalent to an EF lower bound for shared-DAG methods |

Multisign DAG hypergraph calculus: merge-only (signed-hyperedge resolution) = Resolution; with node introduction = Extended Resolution ≡ EF.

## Run entries

### 2026-11-14 10:48 PST (18:48 UTC) — WR-BRIDGE-0001
- Report: `research/agents/claude/2026-11-14_1048_CLAUDE_WR-BRIDGE-0001.tex`
- Code: `experiments/claude_wr/treelike_php_min.py`; raw: `results/raw/claude_wr/2026-11-14_1848_treelike_php_min.json`
- Exact minimum tree-like Resolution leaves for PHP^{n+1}_n: n=1:3, n=2:11, n=3:43 (sizes 5, 21, 85) vs encoding literals 4, 18, 48. COMPUTATIONAL, not asymptotic evidence.
- Literature: Pich–Santhanam arXiv:2312.08163 (EF lower bounds + S^1_2 hypotheses ⇒ P ≠ NP); ECCC 2026/109 (⟨EF,R⟩ systems); Alekseev ToC 22 (2026); Lu–Santhanam–Tzameret ITCS 2026. No 2026 EF lower bound found.
- Next target: SAT ∈ P ⇒ EF-self-certifiable poly SAT decider; or an R between Res and EF with both a provable lower bound and a provable bridge (red-team expects impossible without proving P ≠ NP).
- Root main.tex not edited (no ownership region for this routine).
