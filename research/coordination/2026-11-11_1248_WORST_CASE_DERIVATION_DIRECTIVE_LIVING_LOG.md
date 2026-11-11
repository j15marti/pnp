# Shared worst-case derivation directive and living log

<!-- WORST-CASE DIRECTIVE LIVING LOG :: created 2026-11-11 12:48 America/Los_Angeles -->

**Status: P versus NP remains OPEN.** This is the shared research directive that the scheduled prompt
refers to. Before this file, no such file existed in the repository. It is **additive**: it changes no
task schedule, agent count, LSPV role ownership, root-`main.tex` ownership region, or the
2026-10-24 ARC/FLMV allocation. Append new log entries at the bottom, newest last. Never rewrite
earlier entries.

## Shared mathematical objective

For a fixed, sound and complete Cook–Reckhow refutation calculus `R`, such as the combined multisign DAG
hypergraph reduction calculus:

```
w_R(F)      = min over R-refutations pi of F of cost_R(pi)     (optimal sequence chosen for free)
Wbar_R(N)   = max over UNSAT F with |<F>| <= N of w_R(F)
Bridge(R) : SAT in P  ==>  Wbar_R(N) <= poly(N)
LB(R)     : Wbar_R(N) is not N^{O(1)}
Bridge(R) and LB(R)  ==>  SAT not in P        (PROVED/EXACT, contraposition)
```

Priorities:
1. A superpolynomial worst-case lower bound on minimum derivation cost in a fixed, sufficiently strong `R`.
2. The optimal derivation sequence is chosen freely. Strategy discovery is not charged. This is sound,
   because a minimum over all sequences lower-bounds the execution cost of every sequence.
3. The weakest sufficient bridge `Bridge(R)`.
4. Hard instances must survive resolution, algebraic reasoning, circuit compression, shared DAGs and
   adaptive strategy switching.

Pointwise and worst-case simulation theorems are secondary targets.

## Binding rules from WORSTCASE-BRIDGE-0001 (all PROVED/EXACT, elementary)

Source: `research/agents/claude/2026-11-11_1248_CLAUDE_WORSTCASE-BRIDGE-0001.tex`

- **Squeeze.** If `R'` p-simulates `R`, then `Bridge(R) => Bridge(R')` and `LB(R') => LB(R)`. The bridge
  gets easier as `R` gets stronger, and the lower bound gets harder.
- **Reformulation trap.** If `LB(R)` is already a theorem (resolution, tree-like resolution, polynomial
  calculus, bounded-depth Frege, or anything they p-simulate), then `Bridge(R)` is *equivalent to*
  `P != NP`. Proving `Wbar_R` superpolynomial for such an `R` is **not** progress on the bridge.
- **Trace embedding.** Free-sequence lower bounds are unconditional time lower bounds only for
  algorithms whose own run yields an `R`-derivation (DPLL/CDCL and resolution).
- **Reflection bridge.** For the explicit system `R_T` ("a `T`-proof that `A` decides SAT in time
  `k n^c`, padding, and a run of `A`", plus resolution for completeness), `Bridge` holds
  *conditional on* `PROV_T`: if SAT is in P, some poly-time SAT algorithm is `T`-provably correct and
  polynomial. `LB(R_T)` implies `LB(EF)`.
- **Literature anchor.** Pich–Santhanam (arXiv:2312.08163) prove a conditional `Bridge(EF)`-type
  statement under `S^1_2`-provability hypotheses. This is the closest known theorem. Their FOCS 2019
  paper supplies a natural-proofs-type barrier for proof-complexity lower bounds. Use it as the
  hostile control.

## Role assignments (current)

| Role | Next concrete task |
|---|---|
| General SAT Lower-Bound Lead | Relativized test of `PROV_T`: find an oracle with `P^O = NP^O` but no `T`-provably correct poly SAT^O algorithm, or show none exists. Find the weakest provability hypothesis that closes `Bridge(EF)`, compared with Pich–Santhanam (I)/(II). |
| SAT-Circuit Reduction Builder | Fix `R_mix` (rules, cost, encoding) exactly. Place it in the simulation order: at most bounded-depth Frege (trap) or at least Frege (bridge nontrivial). |
| Hypergraph & Proof Certificates | For each hard UNSAT family, record its survival against Res, PC, CP, AC0-Frege, and whether it is a "natural" random distribution (Pich–Santhanam 2019 barrier). |
| Time-Space Resource Auditor | Prove that `cost_R` is polynomially related to encoded proof length for `R_mix`. Verify the `R_T` verifier runtime. Audit the space variant. |
| Independent Proof Red Team | For every claimed `LB`, check whether the reformulation trap applies. For every claimed `Bridge`, check for a hidden `PROV_T` or a hidden trace embedding. Check every claimed LB against known short derivations (LSPV W61 certificates). |

## Status board

| Statement | Status |
|---|---|
| Free-sequence minimum is a valid lower-bound object | PROVED/EXACT |
| Squeeze / trap / trace embedding / reflection bridge | PROVED/EXACT (folklore-type) |
| `PROV_T` | OPEN |
| `LB(EF)`, `LB(R_T)`, `LB(R_mix)` for `R_mix` at least Frege | OPEN |
| `Bridge(R)` for any `R` with a known LB | equivalent to P != NP (reformulation) |
| P versus NP | **OPEN** |

## Log

- **2026-11-11 12:48 PST — CLAUDE WORSTCASE-BRIDGE-0001.** Created this directive. Proved the squeeze,
  the reformulation trap, the trace-embedding scope and the reflection-system conditional bridge.
  Literature this run: Cook–Reckhow 1979, Krajíček–Pudlák 1989, Köbler–Messner–Torán 2003,
  Pich–Santhanam 2019 and 2023, Buss–Williams 2015. Residual load-bearing arrows: `PROV_T` (or another
  bridge) and `LB` at Frege strength or above. Both are OPEN.

<!-- END WORST-CASE DIRECTIVE LIVING LOG (append entries above this line) -->
