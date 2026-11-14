# Claude agent living log: worst-case minimum-derivation directive

Append-only. Newest entry first. Status labels follow AGENTS.md. P versus NP remains OPEN.

## 2026-11-14 11:51 PST, EFBRIDGE-0001
Report: `research/agents/claude/2026-11-14_1151_CLAUDE_EFBRIDGE-0001.tex`

- KNOWN THEOREM, mapped to the bridge: Pich–Santhanam (arXiv:2312.08163), Corollary 2(2). Suppose S^1_2 proves feasible same-length error-witnessing for all n^k-time search-SAT algorithms. Then SAT in DTIME(n^{ck}) implies that EF is p-bounded. This is a conditional Bridge_k(EF).
- PROVED/EXACT: For every R with a known lower bound (for example Resolution), Bridge(R) is equivalent to P != NP. A bridge can be "weaker than P != NP" only for systems at EF strength or near it.
- PROVED/EXACT: A uniform bridge carries no Kannan-type barrier. This contrasts with PS Proposition 1, where a nonuniform bridge would force NP not in SIZE[n^l].
- PROVED/EXACT: The PS mechanism cannot be restricted to a hard family; it collapses to the target tautology. So a family-restricted bridge needs some other mechanism.
- CONDITIONAL: H (S^1_2-provable witnessing for all k) and LB(EF) together imply P != NP. The same holds with LB(R) for any native R that simulates ER (LSPV-1/592 hypotheses).
- OPEN: H; LB(EF); 592.1 hypotheses for R_mix341. Next target is T-WIT: same-length witnessing via Gutfreund–Shaltiel–Ta-Shma, and whether it can be formalized in S^1_2.
- root main.tex was not edited (Claude owns no region).
