# VERIFIER-REPLACEMENT-FIREWALL54

**Timestamp:** 2026-10-22 02:48 Asia/Seoul  
**Scope:** one bounded synthesis across the existing five roles. Circuit-SAT remains a comparison experiment, not a third P-vs-NP route or a sixth role.  
**Global status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Repairs proposed before source comparison

1. **Verifier-replacement test.** Before using any certificate, residual, ANF, trace, or digest property, replace the chosen RP verifier by every obviously equivalent easy verifier. A language-level claim survives only if the property is invariant, or if a proved canonicalization theorem transfers it.
2. **Paired Circuit/Tseitin test.** For the same deterministic language, compare a randomness-ignoring verifier, a projection decorator, and a structurally elaborate balanced decorator. Charge circuit reads, forward gate evaluation, Tseitin traces, auxiliary variables, and output materialization separately.
3. **Quantifier repair.** A P-vs-RP separation needs `exists L in RP, for every deterministic polynomial-time D, D fails`; a selected-verifier obstruction has only `exists V for L with property S`. A P=RP proof needs a uniform deterministic simulation for every RP language/machine, not simplification of one favorable representation.

No later substantive role report was accessible after `PARITY-AFFINE-JOINT-BYPASS53`; later repository activity concerned review/restoration rather than a new role construction. This run therefore used the last verified role evidence and the repository's parsimonious Circuit-to-3-CNF theorem.

## 2. Verifier-replacement lemma

Let `D` be a uniform deterministic polynomial-time decider for a language `L`. Let `B_n:{0,1}^{m(n)}->{0,1}` be any uniform polynomial-size balanced circuit family:

\[
\Pr_r[B_n(r)=1]=1/2.
\]

Define

\[
V_B(x,r)=D(x)\wedge B_{|x|}(r),\qquad
V_{\rm bit}(x,r)=D(x)\wedge r_1,\qquad
V_0(x,r)=D(x).
\]

**Lemma 54A (ESTABLISHED).** `V_B`, `V_bit`, and `V_0` recognize the same language `L` with one-sided error. `V_B` and `V_bit` have exact YES-input acceptance probability `1/2`; `V_0` ignores randomness and accepts every random tape on YES inputs. Their circuit, certificate, residual, polynomial, trace, and digest structures may differ arbitrarily with the decorator.

**Proof.** If `x` is not in `L`, then `D(x)=0`, so all three verifiers reject every tape. If `x` is in `L`, then `D(x)=1`; the first two acceptance probabilities are the densities of `B_n` and `r_1`, both `1/2`, while the last accepts surely. Uniformity and polynomial running time follow by composing `D` with the stated circuits. ∎

**Corollary 54B (ESTABLISHED firewall).** Any property of one selected verifier that can be changed by the above replacement is neither a language lower bound nor evidence that `L` is outside P. To use such a property in an unrestricted separation, one needs either:

- a language-level statement quantified over every deterministic decider/equivalent verifier, or
- a canonicalization theorem proving that the property is preserved under all allowed replacements, with the compiler and resources charged.

This does not prove P=RP. It only rules out a class of verifier-specific separation inferences.

## 3. Concrete structural falsifier

For an `n x 2n` binary matrix `H`, split the random tape as `(u,v)` with `|u|=|v|=2n` and take

\[
B_H(u,v)=\operatorname{PARITY}(u)\oplus [Hv=0].
\]

Parity makes `B_H` exactly balanced. On every accepting tape, flipping any `u` bit forces rejection, so a positive subcube certificate must fix all `2n` parity coordinates. Suitable finite matrices also exhibit multiple affine residuals across every balanced partition of `v`. Yet `D(x) AND B_H(u,v)` recognizes exactly the same easy language as `D(x) AND r_1` and `D(x)`.

Thus even a conjunction of exact-half density, broad positive-certificate sensitivity, balanced-cut residual width, high algebraic degree, and a unique deterministic gate trace can be attached to a P language. Easy gate inspection evaluates `D` and the decorator directly; no language hardness follows.

## 4. Circuit-SAT and Tseitin consequence

The repository's parsimonious Circuit-to-proper-3-CNF construction gives each primary input exactly one satisfying gate/auxiliary trace. If a verifier has `m` primary random bits and `q` forced trace bits, projected acceptance probability is counted over `2^m`, while naive full-assignment density is counted over `2^{m+q}`. For exact-half acceptance:

\[
\frac{2^{m-1}}{2^m}=\frac12,
\qquad
\frac{2^{m-1}}{2^{m+q}}=2^{-(q+1)}.
\]

The second number is a representation denominator, not a loss of RP acceptance. A faithful simulator samples primary randomness and computes the unique trace. Gate sharing is retained by the circuit and Tseitin variables; expanding a DAG to a tree is an uncharged representation change. Likewise, a digest portfolio over traces cannot lower-bound a solver that reads and evaluates the circuit source unless every alternative information channel is explicitly forbidden or charged.

## 5. Computational consistency check

`experiments/review/2026-10-22_verifier_replacement_firewall54_audit.py` passed **212,424 assertions**:

- 196,608 random-tape checks for three deterministic predicates, confirming identical languages and exact-half YES acceptance for the hard and projection decorators;
- 12,288 accepting-tape flip checks for the hard decorator's parity coordinates;
- 1,266 balanced-cut rank/residual checks on audited matrices for `n=3,4,5,6`;
- 2,016 deterministic trace-assignment checks, confirming one trace per primary input while full-cube density falls from `1/4` through `1/128` as forced bits increase.

These are finite regression controls. Lemma 54A and its corollary are the general arguments; the experiment is not evidence for either class equality or separation.

## 6. Five-role status ledger

| Role | Status | Model / quantifier / peak-resource boundary | Single next discriminating test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** **RETIRED:** use selected-verifier certificate/residual complexity as the HIGH-label source. | Still needs a deterministic total both-label ordinary-KT generator meeting the actual threshold, with source reads, target generation, output, time, and space charged on one machine. | Feed the hard-decorator and projection-decorator encodings of the same language into the proposed generator. Reject the arrow if the KT claim changes without a proved semantic invariant and charged conversion. |
| :12 P≠RP | **OPEN.** **ESTABLISHED:** Lemma 54A. **RETIRED:** one hard RP verifier implies a language outside P. | Required quantifiers are `exists L in RP, for all D in P`. The construction supplies an easy `D`, so it is a falsifier, not a separator. | Rewrite the candidate claim with explicit `exists L, forall D`; test it against `V_B`, `V_bit`, and `V_0` before analyzing any certificate, hash, or Circuit-SAT representation. |
| :24 ARC/FLMV | **OPEN.** | Needs an all-input, hereditary, solver-dependent contractor with acquisition, replay, output, time, and peak workspace jointly charged. Representation-specific residual width can vanish under verifier/encoding replacement. | Run one proposed contractor on parsimonious 3-CNF encodings of both equivalent verifiers and give matched successor inequalities; reject if contraction depends on decorator-only variables. |
| :36 P=RP | **OPEN.** **RETIRED:** hard structure in one verifier refutes derandomization. | A uniform deterministic simulation for every RP language/machine is required. Equivalent easy verifiers show structural hardness is not a language obstruction, but finding the easy replacement is exactly the unresolved task. | Specify a uniform compiler from an arbitrary RP verifier to a deterministic decider or hitting set and test whether it discovers/removes an unknown balanced decorator without advice or oracle leakage. |
| :48 synthesis | **ESTABLISHED:** replacement firewall and density accounting. **OPEN:** both global questions. | Source circuit, primary randomness, trace variables, auxiliary bits, hashes, and encoding metadata are separate resources and quantifiers. | Add a differential representation harness: every new invariant must agree on `V_B`, `V_bit`, and `V_0`, or the report must state the exact canonicalization theorem it needs. |

## 7. P-vs-NP route integration

- **MKTP magnification route:** unchanged main DAG. A verifier decorator cannot provide the missing deterministic total both-label SAT-to-ordinary-MKTP arrow because it can be replaced without changing the language. Ordinary KT thresholds, same-machine costs, and the MMW/FLMV endpoint remain OPEN.
- **ARC/FLMV route:** unchanged independent route. A representation contraction must survive equivalent circuit/CNF encodings and an arbitrary decider's behavior on every input. The firewall strengthens the need for encoding-robust heredity; it supplies no contractor.
- **Compact-history diagnostic:** unchanged supporting diagnostic only. Query/history or circuit structure must be separated from the underlying semantic language, source access, and fast-forwarding; it is not a third route.

## 8. Sources and publication audit

- Repository source: [`PARSIMONIOUS-CIRCUIT-3CNF47`](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-21_1948_MAIN_PARSIMONIOUS_CIRCUIT_3CNF47.md), used for unique trace and projected-density accounting.
- Immediate predecessor: [`PARITY-AFFINE-JOINT-BYPASS53`](https://github.com/j15marti/pnp/blob/f2ad2f918af04683ca62cafd1b1921cf809b5ba8/research/main/2026-10-22_0148_MAIN_PARITY_AFFINE_JOINT_BYPASS53.md), used for the joint structural decorator.

Root manuscripts and role assignments were not modified. No circuit, oracle, proof system, selected solver, random hash, digest, finite experiment, or conditional exponent recurrence is claimed to settle either open problem.
