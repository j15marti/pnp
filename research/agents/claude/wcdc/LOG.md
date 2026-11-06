# Worst-case derivation cost (WCDC) living log
Target: W_R(N) = max over UNSAT F of min derivation cost; weakest bridge SAT in P => W_R <= poly. P vs NP remains OPEN.

## 2026-11-06 WCDC-0001 (`../2026-11-06_CLAUDE_WCDC-0001.tex`)
- Free choice of best derivation = Cook-Reckhow proof size; "all R superpoly" <=> NP != coNP (stronger than P != NP).
- Bridge Br(R) is circular (equals P != NP) wherever W_R is already known superpoly (Resolution etc.); for open R it equals "P=NP => R p-bounded" (true if R optimal; open).
- Known: PV-provably-correct poly SAT algorithm => EF p-bounded. So an EF lower bound gives P != NP only with provability of soundness. Missing arrow = T-PROV.
- Hard-family audit: PHP, Tseitin die at Frege; random 3-CNF is the only live candidate; open for Frege/EF.
- Next: T-PROV; require any multisign-DAG-hypergraph system to be sound, p-verifiable, and compared to EF.
