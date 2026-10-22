# FLMV-PROBE-MARGIN71

Timestamp: 2026-10-22 19:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis resolves the exact endpoint question left conditional in PARENT-PROBE-BUDGET70. It proves only an exponent/accounting refinement. The all-input hereditary ARC transformer and the deterministic total both-label SAT-to-ordinary-MKTP reduction remain OPEN.

## Repairs proposed before source review

1. **Exact forbidden-region test:** replace the informal `(6/5,1/2)` endpoint by the exact FLMV Corollary 5.8 curve and solve its intersection with space exponent `1/2`.
2. **Probe-slack transport:** translate any strict time margin into explicit average parent-probe, block-size and adaptive-round thresholds.
3. **Finite-entry guard:** use a rational point strictly inside the forbidden region, not the boundary root, so `o(1)` factors can be absorbed.

Falsifier fixed in advance: if the recurrence only reached a boundary point where `d(c)=1/2`, then a space bound `n^(1/2+o(1))` would not automatically be `o(n^d(c))`, and the apparent slack would be unusable.

## Sources reviewed after fixing the repairs

1. `research/main/2026-10-19_1648_MAIN_FLMV_FINITE_ENTRY_GATE1.tex`: exact FLMV curve, rational safe point `241/200`, and finite-entry theorem.
2. `research/main/2026-10-22_1848_MAIN_PARENT_PROBE_BUDGET70.md`: aggregate probe envelope and the previously conditional `eta<=0.6` endpoint relevance.
3. `comments/grok-4.7/2026-10-22/2026-10-22_1911_GROK_REVIEW.tex`: independent confirmation that the semantic transformer, both-label reconstruction and model transfer remain OPEN.

The exact statement used from the project’s primary-source audit is FLMV Corollary 5.8:

`NTIME[n]` is not contained in `DTISP[n^c, o(n^d(c))]`, where

`d(c)=((c+2)/c^2-c)/2`.

The machine model remains deterministic random-access. No transfer to another machine model is made here.

## Lemma 71A — exact FLMV half-space boundary

Solving `d(c)=1/2` gives

`c^3+c^2-c-2=0`.

Its positive root in the relevant interval is

`c_half = 1.205569430400590...`.

Because `d'(c)=(-1-c^-2-4c^-3)/2<0` for `c>0`, every fixed `c<c_half` satisfies `d(c)>1/2`. In particular,

`d(6/5)=23/45=1/2+1/90`,

and at the conservative rational point

`c_safe=241/200=1.205`,

`d(c_safe)=11642479/23232400 = 1/2 + 26279/23232400`.

Thus a same-model algorithm using time `n^(241/200+o(1))` and space `n^(1/2+o(1))` falls strictly inside the forbidden region: the fixed positive margin makes its space `o(n^d(c_safe))`.

**Status: ESTABLISHED exact arithmetic, conditional only on the already source-checked FLMV statement and exact same-model transfer.**

At the root itself, `n^(1/2+o(1))` is not necessarily `o(n^(1/2))`; strict inequality is essential.

## Lemma 71B — refined aggregate-probe allowance

For the PARENT-PROBE70 parameters `(alpha,beta,delta)=(3/5,1/2,1/2)` and `gamma0<=11/10`, the recurrence fixed point is

`c_*=max(6/5,3/5+eta)`.

Therefore the exact analytic condition for strict FLMV entry at space exponent `1/2` is

`eta < c_half-3/5 = 0.605569430400590...`.

A clean rational sufficient condition is

`eta <= 121/200 = 0.605`,

because then `3/5+eta<=241/200`. This strictly strengthens the earlier conservative endpoint statement `eta<=3/5`. The extra admissible exponent width is approximately `0.00556943`; it is small but real.

The primary construction target remains `eta<=1/2`, which preserves the stronger one-level overhead `11/10`. The interval

`1/2 < eta <= 121/200`

preserves a finite FLMV contradiction only if the missing semantic transformer, heredity and machine-model obligations are independently proved.

**Status: ESTABLISHED exponent arithmetic; semantic realization OPEN.**

## Lemma 71C — refined blocked-scan thresholds

ROUND-ADAPTIVE-BATCHING60 charges source time exponent

`1+max(alpha-b,rho)`.

With `alpha=3/5`, sufficient rational conditions for source work at most `241/200` are

`b >= 79/200 = 0.395`,

and

`rho <= 41/200 = 0.205`.

Indeed,

`1+3/5-79/200 = 241/200`,

and

`1+41/200 = 241/200`.

The exact open-boundary conditions are `b>0.394430569599409...` and `rho<0.205569430400590...`. The rational conditions deliberately stay inside the forbidden region. The stronger original `11/10` target still requires `b>=1/2` and `rho<=1/10`.

**Status: ESTABLISHED scheduling arithmetic; query-key compiler, descriptor output, source acquisition, simultaneous peak space and semantic correctness remain OPEN.**

## Finite consistency audit

`experiments/review/2026-10-22_flmv_probe_margin71_audit.py` uses exact fractions for the rational identities and 200-step bisection for the cubic root. It tested 100,000 deterministic random initial triples `(c0,s0,base)` and, for each, checked finite entry, monotonic FLMV margin and exact recurrence replay.

Result: **400,009 checks, zero failures.** This validates arithmetic only.

## Two P-vs-NP route ledger

### 1. SAT to ordinary MKTP/MCSP

- **ESTABLISHED:** the aggregate probe ledger must be charged into every ordinary-KT indexed evaluator; lower source access generally helps a KT upper bound.
- **OPEN:** deterministic total both-label SAT-to-ordinary-MKTP reduction with a genuine label-sensitive HIGH side, correct ordinary KT thresholds, same-machine time and no random-oracle proof-of-work.
- **RETIRED:** treating a short digest, selected solver, finite experiment, circuit hardness proxy or source-limited query inequality as an unrestricted lower bound.
- **Next discriminating test:** for one actual candidate target string, publish the shortest uniform indexed evaluator with original-source description length, per-bit runtime, all source probes and both label thresholds.

### 2. Arbitrary-decider hereditary ARC to FLMV

- **ESTABLISHED:** if a uniform all-input hereditary fully charged same-model stage realizes the PARENT-PROBE recurrence with `eta<=121/200` and simultaneous space exponent `1/2`, finite iteration reaches the strict rational FLMV point `(241/200,1/2)`.
- **CONDITIONAL:** the arithmetic contradiction assumes exact FLMV serialization/model transfer and an actual semantic transformer.
- **OPEN:** construct the transformer for every polynomial SAT decider, with both labels, off-image correctness, strictly smaller charged calls, aggregate source probes, descriptor materialization, replay and live state all included.
- **RETIRED:** current-scale compulsory black-box calls, uncharged parent scans, per-input portfolios, promise-only stages and output-free recurrences.
- **Next discriminating test:** instrument one genuine child generator and measure `(Q,beta,eta,delta,rho)` plus maximum query length, unfinished descriptor state and both-label validation on every branch.

## Independent P-vs-RP and Circuit-SAT ledger

- **ESTABLISHED restricted:** DIGEST-LUMP19, CLAUSE-COHERENCE20 and SOURCE-CHANNEL21 remain valid barriers. Short hashes need not be complete semantic states; nonlinear hash congruence can be coNP-complete; occurrence-local clause sampling can falsely accept UNSAT; source-query bounds must charge every source reply.
- **OPEN P!=RP:** no explicit RP language outside every deterministic polynomial-time machine has been constructed.
- **OPEN P=RP:** no uniform deterministic simulation or universal hitting set for every RP machine has been constructed.
- **RETIRED:** using `SAT in RP` to infer `P=RP`; treating a bypass verifier, unique circuit trace, high ANF degree, proof-system lower bound, random hash or finite success rate as a class separation.
- **Next :12 test:** locate the generalized WRAPPER gate/source DAG and count every information-bearing source channel before applying the SOURCE-CHANNEL21 inequality; run the easy gate-inspection and SAT-NO controls.
- **Next :36 test:** attempt exact count propagation only after proving the exposed state is a complete congruence for every source/timer/solver/history transition; emit the first same-hash inconsistent pair otherwise.

Circuit-SAT remains a representation and hostile-control experiment, not a third P-vs-NP spine. Functional Tseitin traces preserve satisfying assignments only with coherent shared primary variables; splitting clause occurrences changes the witness relation.

## Compact-history integration

The compact-history addendum remains diagnostic support, not a new route. Exact oracle-query and truth-table gate lower bounds do not imply unrestricted time against an explicit succinct transition circuit. The required quantifier is a single circuit `exists W forall i`, not unrelated `forall i exists W_i`; native source-compression and acquisition costs remain charged. The subpolynomial single-witness premise is OPEN.

## Five-role next experiments

| Role | Status | Single next experiment |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Build and cost one both-label ordinary-KT target evaluator, including original-source access. |
| :12 P!=RP | **OPEN** | Audit generalized WRAPPER source channels and deterministic bypasses before applying any query bound. |
| :24 ARC/FLMV | Lemmas 71A-C **ESTABLISHED arithmetic**; transformer **OPEN** | Measure one real child generator against `eta<=121/200`, `b>=79/200`, `rho<=41/200`. |
| :36 P=RP | Restricted lumpability/counting results **ESTABLISHED restricted** | Prove complete-state congruence or output a same-hash transition counterexample. |
| :48 synthesis | Exact finite FLMV slack **ESTABLISHED** | Refuse promotion unless serialization, all-input heredity, both labels and peak resources survive on one model. |

## Conclusion

The PARENT-PROBE70 slack region is no longer endpoint-conditional: exact FLMV arithmetic permits `eta<0.6055694304...`, with the conservative rational envelope `eta<=121/200`, `b>=79/200`, `rho<=41/200`. This is a modest but genuine relaxation. It does not construct the missing ARC stage, ordinary-MKTP reduction, RP separator or RP derandomization. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
