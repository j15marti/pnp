# Living log: worst-case derivation cost W_R(N)

Directive: `research/governance/2026-11-09_WORST_CASE_DERIVATION_DIRECTIVE1.md`. Status of P vs NP: OPEN. Append newest entries at the bottom.

## 2026-11-09 WCD-0001 (report: research/agents/claude/2026-11-09_WCD-0001.tex)
- PROVED/EXACT: free strategy search makes W_R proof size (nondeterminism), not algorithm time.
- PROVED/EXACT Dichotomy: if W_R is already known superpolynomial (resolution, PC, bounded-depth Frege), BRIDGE(R) <=> SAT not in P. Circular; useless as a route.
- PROVED/EXACT: for optimal R, BRIDGE holds but W_R superpoly <=> NP != coNP (stronger than needed). Optimal systems not known to exist.
- PROVED/EXACT: for Frege/EF-strength R, W_R poly <=> Ref_M^n has poly R-refutations (uniform reflection of a poly SAT algorithm M). This is the weakest sufficient bridge. Proving it unconditionally or finding a world where it fails is OPEN.
- Next targets: (1) decide whether Ref_M can be shown EF-feasible for a canonical M (e.g. Levin universal search with proof-checking) under P=NP; (2) check literature on "P=NP provable in PV/U^1_1" vs EF; (3) hard-family work only matters for R above Frege.
- Literature: Krajicek-Pudlak; Messner (P=NP => optimal acceptor <=> p-optimal system); magnification/locality barrier (Oliveira-Santhanam, Chen et al.). No 2025-26 result found directly bearing on the bridge.
- Not done: root main.tex untouched (not an LSPV role); no experiments.
