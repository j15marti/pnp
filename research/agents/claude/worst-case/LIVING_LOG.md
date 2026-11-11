# Living log: worst-case minimum derivation cost W̄_R(N) (Claude scheduled routine)

Shared target: W̄_R(N) = max over UNSAT F with |⟨F⟩| ≤ N of min over R-refutations π of cost_R(π).
Weakest bridge B3: SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). **P versus NP remains OPEN.**
This routine sits outside the LSPV-1..5 stagger and owns no region of root `main.tex`. LSPV-5 may reconcile.

| Date (PST) | Report | Main result | Status |
|---|---|---|---|
| 2026-11-11 07:56 | `../2026-11-11_0756_CLAUDE_WORSTCASE-SURVIVAL-0001.tex` | (1) Bridge lattice: B3 goes up and LB goes down under p-simulation. P≠NP ⇔ ∃R [B3(R) ∧ LB(R)]. For any R with a proved lower bound, B3(R) is equivalent to P≠NP (duplicates LSPV-1/398 for Resolution). (2) Survival matrix: PHP, Tseitin and dense random 3-CNF (m ≥ c·n^1.4, via Müller–Tzameret TC0-Frege) are retired for any R containing ER. Constant-density random 3-CNF is the only standard candidate left, and its status for EF/Frege is OPEN. (3) Finite width screen: exact minimum Resolution width equals 3 for random 3-CNF up to n=40, so small-n exact minima carry no growth evidence. Tseitin width grows, but local GF(2) elimination refutes it. | KNOWN THEOREM / CONDITIONAL / COMPUTATIONAL; OPEN |

## Open next targets
- Decide whether the RES+VARDEF fragment of R_mix341 p-simulates Extended Frege at charged node cost. If it does, any superpolynomial W̄_{R_mix341} is an EF lower bound.
- Red team: compile the Feige–Kim–Ofek / Müller–Tzameret witness into native R_mix341 at m = n^1.4.
- Literature to keep watching: general DAG Res(⊕) lower bounds for random 3-CNF; Frege/EF lower bounds for random 3-CNF at constant density.

## Reproduce
`python3 survival_width.py <rand3[_alpha]|tseitin|php> <param> <seed> [kmax]`. One instance per call, each under ~30 s. Raw output: `survival_width_results.jsonl`.
