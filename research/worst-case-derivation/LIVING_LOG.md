# Worst-case derivation complexity: living log

Shared directive (verbatim target): W_R(N) = max_{F in UNSAT, |<F>|<=N} min_{pi: F |-_R bot} cost_R(pi).
Free choice of optimal derivation (no charge for strategy search). Priority bridge: SAT in P => W_R(N) <= poly(N).
Roles: General SAT LB Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates; Time-Space Resource Auditor; Independent Red Team.
Status: P vs NP OPEN. No superpolynomial W_R bound for any system with a proved bridge is known.

## Entries (newest first)

### 2026-11-03 CLAUDE-WC-0001
Report: `research/agents/claude/2026-11-03_CLAUDE_WORSTCASE-BRIDGE-0001.tex`
- Bridge B_R is logically equal to (P!=NP) or (W_R poly). So for every R with a PROVED superpoly lower bound (Res, CP, bounded-depth Frege, PC...), B_R is equivalent to P!=NP: no weaker.
- Only non-circular bridge mechanism: provability. R_T = (T-proof of correctness of M, trace of M). T-provably-correct poly SAT algorithm => W_{R_T} poly. Gap to the displayed bridge = provability of correctness.
- Free-strategy minimization is legitimate but gives the hardest form of the bound; W_R poly => NP=coNP, so a W_R lower bound alone says nothing about P vs NP without B_R.
- Literature: no 2025-26 result gives an EF lower bound or an optimal proof system (Pich-Santhanam 2312.08163; Arteche et al. 2506.16956; Alekseev ToC v22a004).
- Next targets: (T1) find R with B_R provable without assuming P!=NP or provability; (T2) time-space version B_R^{ts}; (T3) red team: is R_T lower bound independent of P vs NP? 
