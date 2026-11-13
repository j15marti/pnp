# Living log: worst-case free-strategy derivation cost  W̄_R(N)

Scheduled Claude task (user directive: multisign DAG hypergraph / minimal reduced state / minimal work;
target  W̄_R(N) = max_{F UNSAT, |F|<=N} min_{π: F ⊢_R ⊥} cost_R(π)  and bridge B3: SAT∈P ⇒ W̄_R(N) ≤ poly(N)).
Append one entry per run, newest last. **P versus NP remains OPEN.**

## Standing map (update in place when it changes)

| Arrow | Status | Where |
|---|---|---|
| Free-strategy min is a valid lower-bound relaxation for derivation-producing procedures | PROVED/EXACT | definition |
| Pointwise transfer TR(Resolution) | FALSIFIED (Tseitin + Gauss) | LSPV-1/334 |
| B3 with system chosen after algorithm | PROVED, but its partner lower bound = NP≠coNP | CLAUDE WORSTCASE-0001 Prop. 1(a) |
| B3 for any R with a known superpoly lower bound | equivalent to P≠NP (reformulation) | WORSTCASE-0001 Prop. 1(b) |
| B3 via T-provable rejection soundness (reflective R_T) | CONDITIONAL | LSPV-1/337, /357 |
| Relativizing proof of B3 | impossible unless W̄_R poly | LSPV-1/360 |
| Superpoly W̄ for R_mix341 | OPEN; at least as hard as ER/EF and unrestricted Res(⊕) lower bounds | LSPV-1/592; WORSTCASE-0001 |
| B3 for R_mix341 | OPEN | main.tex |

## Entries

### 2026-11-13 02:54 PST — WORSTCASE-0001
- Report: `research/agents/claude/2026-11-13_0254_CLAUDE_WORSTCASE-0001.tex`
- Quantifier audit of B3 (three readings) and squeeze lemma: B3 and the W̄ lower bound cannot be pursued in different systems; the only positive B3 criterion needs ≥ Extended Frege strength, where lower bounds are open.
- COMPUTATIONAL: exact tree-like Resolution minima on odd Tseitin 3-CNFs: K4 28 leaves, Prism 48, K3,3 76, Q3 128; min widths 4, 4, 5, n.c.; Gauss ≤ 20 row XORs. Code/data in `research/agents/claude/worstcase/`.
- Literature: no unrestricted Res(⊕) superpoly bound known; 2025 depth-restricted bounds (arXiv:2507.23008, arXiv:2511.20023); optimal proof systems still open (Egidy–Glaßer STOC 2025 oracles; arXiv:2602.02294).
- Next: exact tree-like minima for the Res+GF(2) union on random 3-CNF near threshold, n ≤ 12.
