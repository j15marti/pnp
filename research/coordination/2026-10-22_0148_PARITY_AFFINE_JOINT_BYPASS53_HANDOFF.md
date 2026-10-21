# PARITY-AFFINE-JOINT-BYPASS53 handoff

Timestamp: 2026-10-22 01:48 Asia/Seoul

## Shared construction

For input x=(n,H,b), random u,v in {0,1}^{2n}, define

F_H(u,v)=PARITY(u) XOR 1[Hv=0],
R(x;u,v)=b AND F_H(u,v).

R is a uniform RP verifier for the trivial language b=1: NO acceptance is zero and YES acceptance is exactly 1/2. Every positive subcube certificate fixes all 2n u-bits. For robust H from ARC-ROBUSTORDER29, every variable order has residual width at least 2^(n-2 ceil(2 sqrt(n))+2) after the nth v-variable. Both obstructions coexist, but a deterministic language algorithm returns b.

## Role actions

- **:00 MKTP:** test any target on this family against the direct indexed evaluator using the explicit H record and selector. Structural width is not a KT lower bound.
- **:12 P!=RP:** treat POSITIVE-CERT17 only as sufficient. For the actual WRAPPER DAG, report certificate width and a separate language-level bypass.
- **:24 ARC/FLMV:** ordered residual compilation is ruled out on the affine family. Add a nonaffine shared constraint and charge a source-aware alternative, failed calls, output, recursion, and peak workspace.
- **:36 P=RP:** any proposed certificate normal form must transform this verifier without using the pre-existing deterministic decision b.
- **:48 synthesis:** replace every verifier-specific claimed invariant by the deterministic verifier R'(x)=b. If it disappears, it is not a language invariant.

## Model and quantifier firewall

1. H is part of the ordinary input; verifier uniformity does not rely on advice.
2. Robust H inputs exist asymptotically by the ARC probabilistic theorem, but no uniform robust-H generator is needed for the language counterexample.
3. Residual width quantifies over ordered residual diagrams, not all algorithms.
4. Certificate width quantifies over subcubes of one verifier's random tape, not all verifiers for the language.
5. Circuit/Tseitin conversion preserves primary acceptance and adds deterministic trace variables; full assignment density is representation-dependent.
6. P versus NP and P versus RP remain OPEN.

## Artifacts

- `research/main/2026-10-22_0148_MAIN_PARITY_AFFINE_JOINT_BYPASS53.md`
- `experiments/review/2026-10-22_parity_affine_joint_bypass53_audit.py`
- `results/raw/synthesis/2026-10-22_0148_PARITY_AFFINE_JOINT_BYPASS53_raw.json`

No root manuscript was modified.
