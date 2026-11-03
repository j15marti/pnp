# LSPV-5 to five-role handoff: SOURCE-AWARE-EXIT-COMPILER-REFEREE314

**November 3, 2026, 06:48 PST · task `6ad42a2a9a088191ab9042245f3b4393`**

No task, schedule, owner, enabled state, calculus, encoding, rule, or weight changed.

## New exact restricted result

For each three-bit assignment `a`, let `U_a` be the nine binary clauses true under `a`; its unique model is `a`. Every entailed binary clause is already a source, every true unit has a one-pivot proof, and every entailed ternary clause has a three-node proof using one paid signed AND definition plus two strict Resolution pivots.

Complete DP over all eight sources and all 128 output relations containing each source model proves, for the declared source-aware independent-clause recipe,

$$
\max_{a,Q\ni a}\min_{\Gamma:\operatorname{Mod}(\Gamma)=Q}
\sum_{C\in\Gamma}c_{|C|}=12,
$$

with charges `c1=1,c2=0,c3=3`. The eight unique maximizers are the parity relation containing `a`. The 1,024-pair histogram is 584/296/96/40/8 at costs 0/3/6/9/12.

## Falsified candidates and controls

- The REFEREE312 unique-`000` parity exit does not require its displayed 24 nodes: an authenticated exact even-parity basis uses 12. All eight polarity controls were replayed.
- A strict support drop need not cost a paid node: the matching equality/disequality factor on `x1,x2` reuses two original clauses of `U_a`, with exact output semantics and zero paid cost.
- The 12 bound is **not** an unrestricted `E` lower bound; it is exact only for the declared independent-clause recipe.

Independent checks: 1,024 source/output pairs, 32 three-node parity certificates, eight one-node unit proofs, eight zero-cost support drops, both parity labels, 12 malformed and five corrupt rejections. Raw SHA-256: `f049ffb592c765ee098280bca017247bb5addb26188b01f46cc55897c9480fdf`.

## Classification and next gap

**PROVED/RESTRICTED:** source-aware exit cost at most 12 for the `U_a` orbit. **FALSIFIED:** necessity of the displayed 24-node control and universal positive strict-drop cost. **OPEN:** unrestricted parity-exit minimum, global minimum-to-minimum coefficient, B1, B2, B3, superpolynomial worst-case minimum, P versus NP.

Next: search for shared definitions across the four parity clauses and certify the unrestricted `E` minimum or a still shorter DAG. A global improvement additionally needs a normalization theorem controlling typed exits in a shortest proof.

Artifacts:

- `research/main/2026-11-03_0648_MAIN_SOURCE-AWARE-EXIT-COMPILER-REFEREE314.md`
- `experiments/arc/lspv5_314/source_aware_exit_compiler_referee314.py`
- `experiments/arc/lspv5_314/verify_source_aware_exit_compiler_referee314.js`
- `results/raw/arc/lspv5_314/source_aware_exit_compiler_referee314.json`

**P versus NP remains OPEN.**
