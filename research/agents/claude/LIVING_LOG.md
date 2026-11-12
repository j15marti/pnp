# Claude routine living log: worst-case derivation cost directive

Append-only. Each entry: run, result, statuses, next target. P versus NP remains OPEN.

## 2026-11-12 13:00 PT: WORSTCASE-BRIDGE-0001
- Report: `research/agents/claude/2026-11-12_1300_CLAUDE_WORSTCASE-BRIDGE-0001.tex`
- Lemma (PROVED/EXACT): a *local* multisign hypergraph reducer (at most k premises, width at most w, no new nodes) is simulated by resolution with factor 3^{kw}. So W̄_R(N) >= 2^{Ω(N)} unconditionally, and Bridge(R) <=> P != NP. The bridge is not weaker than the whole problem.
- Dichotomy: (L) a lower bound is known and the bridge is the entire problem; (E) extended or Frege-strength systems have no known lower bound.
- Bridge(EF) <=> [SAT in P => some correct poly-time A has poly-size EF proofs of its soundness RFN_A] (KNOWN THEOREM transfer; Cook 1975, Krajíček–Pudlák 1989). OPEN.
- COMPUTATIONAL: 10,583 implied clauses checked, 0 failures (`locality-dichotomy/`).
- Next: compare the cost of deciding with A against the EF/Frege cost of proving RFN_A on restricted classes (XOR-SAT, 2-SAT, Horn).
- LaTeX not compiled: no TeX engine in this container.
