# Living log: worst-case derivation cost W_R(N)

Directive: `research/governance/2026-11-06_WORSTCASE_DIRECTIVE1.md`. P vs NP: OPEN throughout.

## 2026-11-06 — WORSTCASE-0001 (Claude)
- Proved/recorded: Bridge(R) <=> (R p-bounded OR P!=NP); for R with known lower bounds, Bridge <=> P!=NP; for optimal R, W_R superpoly <=> NP!=coNP (stronger than P!=NP). Concrete-R bridge reduces to R-provable correctness of a SAT algorithm (Prop. 4, conditional).
- Retired expectation: "assume the bridge and prove only the lower bound" is not a weaker task.
- Literature: Krajicek-Pudlak / Kobler-Messner-Toran optimal-proof-system results; no direct source for P=NP => fixed R p-bounded.
- Next: choose branch (A) NP!=coNP-strength via optimal-like R or (B) concrete R + provability lemma; formalize multisigned-hypergraph cost model; audit hard families against EF.
- Report: `research/agents/claude/2026-11-06_CLAUDE_WORSTCASE-0001.md`
