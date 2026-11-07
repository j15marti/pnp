# Worst-case derivation complexity — living log

Target: $\overline W_R(N)=\max_{F\in UNSAT,|F|\le N}\min_{\pi:F\vdash_R\bot}\mathrm{cost}_R(\pi)$; bridge $B(R)$: SAT∈P ⇒ $\overline W_R\le$ poly. **P vs NP remains OPEN.**
Roles: General Lower-Bound Lead / SAT-Circuit Reduction Builder / Hypergraph & Certificates / Time-Space Auditor / Red Team. (This is a task-spec pointer only; it changes no schedules or ownership.)

## 2026-11-07 WORSTCASE-0001
- Report: `research/agents/claude/2026-11-07_WORSTCASE-0001.tex`; data: `results/raw/worstcase/`; code: `experiments/worstcase/`.
- PROVED/EXACT: free strategy = nondeterminism, so $\overline W_R$ = Cook–Reckhow proof length.
- PROVED/EXACT: $B(R)\iff(P\ne NP)\vee(\overline W_R\le poly)$. For any R with a known unconditional lower bound (resolution, CP, bdd-depth Frege, PC) the bridge is *equivalent to P≠NP*, so not a reduction. Only Frege/eF and stronger are non-circular.
- Constructive content of a bridge: poly-size R-proofs of $\mathrm{Ref}_{A,n}$ (algorithm correctness) for some A. The ∀A form likely fails via finitistic Gödel (CANDIDATE, verify Pudlák 1986).
- RETIRED: "P=NP ⇒ eF p-bounded" via NP=coNP (invalid; only some system).
- COMPUTATIONAL: exact tree-like resolution sizes, PHP n=1..3 → 5,21,85; Tseitin cycles linear; random 3CNF m=6n max 23/27/33 at n=6/8/10.
- Literature: no Frege lower bound known; CCC 2026 paper LIPIcs.CCC.2026.8 on prover–adversary barriers; NW-generator tautologies remain the eF candidate.
- Next: test whether Levin-optimal A has short eF proofs of $\mathrm{Ref}_{A,n}$ (is $T_\exists$(eF) consistent with barriers?).
