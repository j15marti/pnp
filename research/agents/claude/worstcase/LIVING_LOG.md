# CLAUDE living log: worst-case minimum derivation cost W̄_R(N)

Append-only. One entry per scheduled run. P versus NP remains **OPEN**.
Target directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.

## 2026-11-11 06:50 UTC: WORSTCASE-0001
Report: `research/agents/claude/2026-11-11_0650_CLAUDE_WORSTCASE-0001.tex`

- **PROVED/EXACT, seesaw theorem.** For any fixed R where LB(R) (superpolynomial W̄_R) is already a theorem, the bridge B3(R): SAT∈P ⇒ W̄_R ≤ poly is *logically equivalent* to P≠NP. For resolution, CP, PC, Res(k) and bounded-depth Frege, B3 is a restatement, not a weaker target.
- **PROVED/EXACT.** For a theory-indexed system R_T (a T-proof of soundness of a clocked algorithm, plus its trace), B3(R_T) holds whenever some polynomial-time SAT algorithm has T-provable soundness. The only residual gap is independence. The price is that LB(R_T) implies the open EF lower bound.
- **PROVED/EXACT, plus a COMPUTATIONAL check.** A k-premise semantic signed-hyperedge rule is simulated by resolution in ≤ 2^(k-1)−1 steps (Tarsi's lemma). So the extension-free multisign hypergraph calculus is resolution-strength: its W̄ is exponential (random 3-CNF), and its bridge is exactly P≠NP. Exhaustive sample check: `tarsi_sim_check.py` and `tarsi_sim_results.jsonl`.
- **Survival test.** PHP fails, since EF and CP give polynomial proofs. Tseitin fails, via PC over F2 and quasi-polynomial CP. Random 3-CNF survives Res, PC and CP. Its Frege and EF status is OPEN.
- **Next.** Classify each multisign extension (auxiliary hyperedges, counting, XOR) by the weakest standard system that p-simulates it. Any LB claim for an extension-bearing calculus must clear the AC0[p]-Frege frontier, which is still open (Lu–Santhanam–Tzameret, ITCS 2026).
