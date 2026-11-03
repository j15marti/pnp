# LSPV-5 to five-role handoff: FACTOR-EARLY-CONTRADICTION-REFEREE311

**November 3, 2026, 03:48 PST · PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393`**

## New proved restricted correction

Keep `Rmix341` and all weights unchanged. REFEREE310's explicit at-most-three-variable factor compiler paid at most six nodes for each of at most eight blockers, giving coefficient 48. DPLL-IMPLICATE-PRUNE358 correctly sharpened a single local clause consequence, but its statement that this could not improve the complete-factor coefficient is false.

If the local source factor is satisfiable, every entailed output factor is nonfalse and therefore has at most seven blockers. If the source is unsatisfiable, PRUNE358 derives contradiction in at most seven nodes and no blockers are needed. Hence

$$
W_{L_3}(F)\le W_E(F)\le42W_{L_3}(F)+O(1).
$$

This is a restricted upper simulation, not a global mixed optimum or lower bound. The DPLL branch compiler remains sound.

## Reproduction

- Exhaustive entailed relation pairs: 6,561 total; 6,305 satisfiable inputs; 256 false inputs.
- Maximum corrected accounting: 42, on exactly eight singleton pairs.
- Explicit recipe: unique-model `000` binary source; seven authenticated six-node blocker weakenings; total 42.
- False factor: eight blockers resolve to contradiction in seven nodes.
- Both labels: even/odd parity each have four models; wrong entailment rejected.
- Malformed/corrupt: ten malformed records and five certificate mutations rejected.
- Independent Node replay: all 42 weakening nodes and seven contradiction nodes PASS.
- Raw SHA-256: `9f484c07ed07c2c42fe7557c00389943a91cb4792c6227844d49b0d1e585c9d7`.

## Quantifier firewall

- **PROVED/RESTRICTED:** coefficient 42 for explicit local factors in the existing Resolution-plus-source-independent-extension implementation.
- **COMPUTATIONAL:** complete finite relation-pair enumeration and proof replay.
- **FALSIFIED:** only the concrete claim that all eight blockers may need payment in the complete-factor case.
- **OPEN:** legal cross-blocker sharing below 42; global XOR and circuit-valued conversion; B1; B2; B3; superpolynomial worst-case minimum; P versus NP.

The run does not infer that a rejecting trace proves UNSAT, does not add a semantic oracle or tailored axiom, and does not charge proof discovery to the logical minimum. Host work and peak RSS are logged separately in the full report.

## Peer action

Use coefficient 42, not 48, in any downstream `L3`-to-`E` local simulation. Do not describe 42 as exact for the full mixed calculus: the explicit 42-node control saturates the prescribed independent-blocker recipe only. The next red-team target is cross-blocker sharing and then unbounded-support typed conversion; B3 remains an independent primary gap.

Full report: `research/main/2026-11-03_0348_MAIN_FACTOR-EARLY-CONTRADICTION-REFEREE311.md`.

**P versus NP remains OPEN. No task/state/schedule mutation.**
