# Living log: worst-case derivation cost (overline W_R)

P vs NP remains OPEN. Newest entries on top.

## 2026-11-06 WORSTCASE-0001 (Claude)
- Report: `research/agents/claude/2026-11-06_CLAUDE_WORSTCASE-0001.tex`
- Free optimal sequence = nondeterminism: W_R poly <=> R p-bounded (PROVED).
- B(R) for any R with a *known* superpoly lower bound is equivalent to SAT not in P (PROVED) -> not a weaker step.
- Sufficient bridge: R p-simulates trace systems Q_A of all correct poly-time A (PROVED); with PV-provable correctness, EF does (KNOWN-based, CONDITIONAL).
- Net: EF lower bound would only yield "no PV-provably-correct poly-time SAT algorithm". Dropping provability is the open arrow.
- Literature: Krajicek (PV & P vs NP), Pich-Santhanam 2023, Atserias-Muller PAP 2025/26, Krajicek arXiv 2606.13367. Abstracts only.
- Next: separate provably-correct vs merely-correct algorithms; hard UNSAT family surviving EF still unknown.
- Repo-note: no `main.tex` edit (not an LSPV ownership role).
