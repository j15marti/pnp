# Living log: worst-case minimum derivation cost W̄_R(N)

Append-only. Newest entry at the bottom. P versus NP remains **OPEN**.

## 2026-11-12 11:48 PST: WR-BRIDGE-0001
- Report: `research/agents/claude/2026-11-12_1148_CLAUDE_WR-BRIDGE-0001.tex`
- **EXACT:** for any R with a known superpolynomial lower bound (resolution, cutting planes, bounded-depth Frege, PC), the bridge `SAT∈P ⇒ W̄_R ≤ poly` is *equivalent* to P≠NP. It is a reformulation, not a weaker target.
- **EXACT:** family-locality barrier. A poly-time SAT algorithm can hard-code any P-recognisable hard family, so a proof of the bridge must use correctness on all inputs, which is a reflection-type argument.
- **KNOWN (Cook 1975; Krajíček–Pudlák):** if the soundness of a poly-time SAT algorithm is PV-provable, then W̄_EF ≤ poly. **OPEN target GAP-PV:** SAT∈P ⇒ some SAT algorithm has PV-provable soundness.
- **COMPUTATIONAL:** exact minimum tree-resolution leaves for PHP^{n+1}_n: 3, 11, 43 (n = 1..3). Data: `results/raw/claude_wr/2026-11-12_min_treeres_php.json`.
- Next: a chunked n = 4 run; a literature search on unprovability of P = NP in PV (Krajíček, Pich, Santhanam) as evidence on GAP-PV.
