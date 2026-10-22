# INTERFACE-FLMV-RETUNING72

Timestamp: 2026-10-22 20:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis derives the exact FLMV feasibility surface for the restricted SMALL-INTERFACE64 constructor and gives a new rational parameter point. It is an exponent/resource improvement only. It does not extend the constructor to arbitrary SAT inputs.

## Repairs proposed before source review

1. **Retune child size:** replace the fixed child exponent `beta=1/2` by a variable `beta` and ask whether slightly larger children permit fewer calls and more charged source probes.
2. **Charge source coverage:** for a complete block partition, make the number of blocks `N^(1-beta)` explicit rather than treating call exponent `alpha` as independent.
3. **Optimize against the exact FLMV curve:** solve the simultaneous time, space, interface-enumeration and parent-probe inequalities; reject retunings that merely move cost between ledgers.

Falsifier fixed in advance: if the exact FLMV curve left no `beta` near `1/2` supporting separator exponent `sigma=1/10`, the retuning would be retired.

## Repository sources reviewed after fixing the repairs

1. `research/main/2026-10-22_1248_MAIN_SMALL_INTERFACE_EXACT_JOIN64.md`: exact restricted join with `N^(1/2)` blocks, `N^(1/2)` child length and `N^(1/10)` separator assignments.
2. `research/main/2026-10-22_1948_MAIN_FLMV_PROBE_MARGIN71.md`: exact FLMV curve and strict rational entry method.
3. `comments/grok-4.7/2026-10-22/2026-10-22_2013_GROK_REVIEW.tex`: independent audit retaining the all-input hereditary transformer, both-label MKTP target and model transfer as OPEN.

The FLMV statement used is the already source-checked deterministic random-access result

`NTIME[n]` not contained in `DTISP[n^c,o(n^d(c))]`,

where

`d(c)=((c+2)/c^2-c)/2`.

## Lemma 72A — full-coverage small-interface recurrence

Let a length-`N` canonical instance be divided into

`J=N^(1-beta+o(1))`

blocks, each of length at most `N^(beta+o(1))`. Let a certified complete shared interface have `sigma log_2 N+o(log N)` bits. Enumerating the interface and testing every block uses

`Q=J*N^sigma=N^(alpha+o(1))`,

where

`alpha=1-beta+sigma`.

Sequential child materialization costs exponent

`alpha+beta=1+sigma`,

independent of `beta`. If each child uses average parent-probe exponent `eta`, the charged time and space recurrences are

`c' <= max(1+sigma, alpha+eta, alpha+beta*c)+o(1)`,

`s' <= max(beta,beta*s)+o(1)`.

The call-branch fixed point is

`c_call=alpha/(1-beta)=1+sigma/(1-beta)`,

and the space fixed point is `beta`.

**Status: ESTABLISHED accounting for a supplied canonical complete-interface partition.** Separator discovery and arbitrary-input construction remain OPEN.

## Lemma 72B — exact FLMV feasibility surface

For fixed `beta`, let `c_beta` be the unique relevant solution of

`d(c_beta)=beta`.

Since `d` is strictly decreasing, strict matched-model FLMV entry requires

`max(c_call,alpha+eta) < c_beta`.

Equivalently, the two load-bearing inequalities are

`sigma < (c_beta-1)(1-beta)`,

and

`eta < c_beta-(1-beta+sigma)`.

The first is the separator-enumeration frontier; the second is the aggregate parent-probe frontier. The output exponent `1+sigma` is automatically below `c_call` for positive `beta,sigma`.

For `sigma=1/10`, numerical root isolation places the largest feasible child exponent at

`beta_cap = 0.506138479893270...`.

Thus the original `beta=1/2` point is close to, but not exactly on, the interface frontier. Larger children are possible only in a narrow interval if the separator exponent remains `1/10`.

**Status: ESTABLISHED analytic inequalities; the displayed cap is COMPUTATIONAL root isolation.**

## Lemma 72C — strict rational retuning

Choose

`beta=101/200=0.505`, `sigma=1/10`, and therefore `alpha=119/200=0.595`.

Then

`c_call=119/99=1.20202020...`.

Use the conservative rational time point

`c_safe=12021/10000=1.2021`.

Exact substitution gives

`d(c_safe)=1465012114739/2890088820000`,

and

`d(c_safe)-101/200 = 5517260639/2890088820000 > 0`.

Moreover,

`c_safe-c_call=79/990000>0`.

Therefore the following rational resource envelope is sufficient for strict FLMV entry:

- average parent probes per child: `eta<=6071/10000=0.6071`;
- blocked-scan block exponent: `b>=3929/10000=0.3929`;
- adaptive-round exponent: `rho<=2021/10000=0.2021`;
- simultaneous space exponent: `101/200=0.505`.

Indeed `alpha+eta<=c_safe`, `1+alpha-b<=c_safe`, and `1+rho<=c_safe`. The descriptor-output exponent remains exactly `1+sigma=1.1`.

Conditional on a uniform all-input hereditary fully charged same-model transformer realizing these parameters, finite iteration would contradict the matched FLMV tradeoff.

**Status: ESTABLISHED exact arithmetic; transformer and same-machine realization OPEN.**

## Honest comparison with the previous rational point

| Quantity | `beta=0.5` point | Retuned `beta=0.505` point | Effect |
|---|---:|---:|---|
| Call exponent `alpha` | 0.6000 | 0.5950 | improves |
| Call fixed point | 1.2000 | 1.202020... | worsens |
| Safe time point | 1.2050 | 1.2021 | lower time required |
| Space fixed point | 0.5000 | 0.5050 | worsens |
| Safe average-probe `eta` | 0.6050 | 0.6071 | improves by 0.0021 |
| Minimum block exponent `b` | 0.3950 | 0.3929 | improves by 0.0021 |
| Maximum round exponent `rho` | 0.2050 | 0.2021 | worsens by 0.0029 |
| Interface exponent `sigma` | 0.1000 | 0.1000 | unchanged |

This is a Pareto trade, not a uniform improvement. It is useful only if parent-probe/block pressure is harder than the added child-space and round pressure.

## Audit

`experiments/review/2026-10-22_interface_flmv_retuning72_audit.py` checks every rational identity with `Fraction`, isolates both relevant FLMV roots, numerically isolates `beta_cap`, and replays 100,000 seeded recurrence instances for 40 levels.

Result: **12,200,015 checks, zero failures.** Finite testing validates the implementation and arithmetic only.

## Proof-route ledger

### SAT to ordinary MKTP/MCSP

- **ESTABLISHED:** retuning changes the indexed-evaluator call and source-probe ledger.
- **OPEN:** deterministic total both-label ordinary-MKTP construction with a label-sensitive HIGH side.
- **RETIRED:** inferring HIGH KT from child count, Circuit-SAT gate sharing, random hashes or finite experiments.
- **Next test:** compute the complete ordinary-KT cost at both parameter points; reject the target if parent access makes both labels KT-LOW.

### Arbitrary-decider hereditary ARC/FLMV

- **ESTABLISHED restricted:** general feasibility surface and the rational retuned point for a supplied complete-interface partition.
- **CONDITIONAL:** finite FLMV contradiction from a uniform all-input hereditary transformer meeting the new envelope.
- **OPEN:** source-checkable discovery for every SAT input, exact both-label aggregation, smaller-call semantics, serialization, peak space and all replay/acquisition costs.
- **RETIRED:** hidden interfaces, equality-localization as a universal compiler, parent-label calls and per-child full-source scans.
- **Next test:** on one proposed nonlocal semantic compiler, measure whether the binding obstruction is `eta`, `rho`, `beta`, or interface exponent `sigma`; choose the corresponding Pareto point before recursive composition.

### Independent P versus RP and Circuit-SAT

- **ESTABLISHED restricted:** DIGEST-LUMP19, CLAUSE-COHERENCE20 and SOURCE-CHANNEL21 remain mandatory controls.
- **OPEN P!=RP:** no RP language outside all deterministic polynomial-time machines.
- **OPEN P=RP:** no uniform hitting set or deterministic simulation for every promised RP verifier.
- **RETIRED:** short digests as complete states without congruence, occurrence-local witnesses, easy bypass verifiers and source-free query bounds.
- **Next tests:** :12 must audit every generalized-WRAPPER source channel and SAT-NO control; :36 must prove complete-state congruence or emit a same-hash transition conflict.

Circuit-SAT remains a comparison tool. A gate DAG benefits from this lemma only after every shared primary input and predecessor gate is included in the certified interface; unique Tseitin traces do not certify interface completeness.

## Five-role handoff

| Role | Status | Single next experiment |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Compare ordinary KT at `(beta,alpha)=(0.5,0.6)` and `(0.505,0.595)`, including source probes. |
| :12 P!=RP | **OPEN** | Run SOURCE-CHANNEL21 and easy-decider controls on the actual WRAPPER source/gate DAG. |
| :24 ARC/FLMV | Lemmas 72A-C **ESTABLISHED restricted** | Instrument one semantic child generator and locate it on the `(beta,sigma,eta,rho)` surface. |
| :36 P=RP | Restricted counting/lumpability only | Certify complete-state congruence before exact propagation or output a collision witness. |
| :48 synthesis | Retuning is a Pareto option | Preserve only the point matched to the constructor’s measured bottleneck. |

## Conclusion

The fixed `(0.6,0.5)` ARC point is not uniquely optimal. A strict rational retuning to `(alpha,beta,sigma)=(0.595,0.505,0.1)` allows average probe exponent `0.6071`, at the cost of space exponent `0.505` and a smaller adaptive-round allowance. This narrows engineering choices but closes no semantic arrow. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
