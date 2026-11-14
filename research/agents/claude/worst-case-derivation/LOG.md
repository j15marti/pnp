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
| B_EF ⇔ (SAT ∈ P ⇒ poly A with UNSAT ⊆ Rej_A and short EF proofs of one-step restriction invariance Down_A, Base_A) | PROVED/EXACT (WR-BRIDGE-0002); target OPEN |
| Intermediate R (Res, RAT⁻, bounded-depth/regular Res(⊕)) with both LB and bridge | RETIRED as a route: B_R ⇔ P ≠ NP; proof search blocked; simulation needs extension (≡ ER/EF) |
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

### 2026-11-14 11:20 PST — WR-BRIDGE-0002 (user: "try that")
- Report: `research/agents/claude/2026-11-14_1120_CLAUDE_WR-BRIDGE-0002.tex`
- Target A (EF self-certification) reduced to an inductive-invariant form: Rej_A must be forward-invariant under single restrictions, exclude true closed formulas, and contain UNSAT, all with poly-size EF proofs. This matches the shape of a barrier certificate; no theorem transfers. Still OPEN.
- Target B (system between Res and EF): fails as predicted. Proof search through A cannot produce short proofs that don't exist; Cook-style simulation needs new variables, which gives ER ≡ EF.
- Code: `experiments/claude_wr/certificate_closure.py`; raw: `results/raw/claude_wr/2026-11-14_certificate_closure.json`. 2-SAT certificates give checked Resolution refutations of ≤ 2m+1 steps. Tseitin (K4, K33, prism, Q3): Gaussian elimination takes 3/5/5/7 row ops, exact minimum tree-like Res leaves are 28/76/48/128.
- Next: build A with EF-short Down proofs from SAT ∈ P, or prove a black-box barrier against it.
