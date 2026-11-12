# Living log: worst-case derivation cost W̄_R(N) directive (Claude scheduled routine)

Target: W̄_R(N) = max over UNSAT F with |<F>| ≤ N of min over R-refutations π of cost_R(π).
Bridge B3(R): SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). **P versus NP remains OPEN.**

## 2026-11-12 01:52 PST — WCD-BRIDGE-0001
- Report: `research/agents/claude/2026-11-12_0152_CLAUDE_WCD-BRIDGE-0001.tex`
- PROVED/EXACT (elementary): if LB(R) is already a theorem (Resolution, bounded-depth Frege, PC in char ≠ 2 on 3-CNF), then B3(R) ⇔ P ≠ NP. So the bridge is the goal itself, not something weaker.
- PROVED/EXACT: B3 relative to TQBF is false for those R, and so is its algebrized version (multilinear extension of TQBF). Any proof of B3 for them must be nonrelativizing and nonalgebrizing.
- Consequence: a bridge weaker than the goal can only exist at Frege/EF strength or above, where LB(R) is itself OPEN. The known positive route is Cook PV-provable soundness (KNOWN; it fails for all deciders by LSPV-1/357's Gödel wrapper).
- Literature clues: Pich–Santhanam 2023 (conditional EF→P≠NP); Fleming–Grosser–Pitassi–Robere 2026 ⟨EF,R⟩ systems (the B3 bottleneck is EF-provable reduction correctness); Lu–Santhanam–Tzameret ITCS 2026.
- COMPUTATIONAL: exact min tree-like Resolution sizes: PHP^2_1=5, PHP^3_2=21, PHP^4_3=85, odd Tseitin K4=55 (`wcd/treeres_exact.py`, all < 1 s).
- Next: pick a fixed R at ≥ Frege strength (the FGPR ⟨EF,R⟩ normal form). Look for a nonrelativizing argument that SAT ∈ P yields *provable* soundness for some decider, or find an obstruction to one.
