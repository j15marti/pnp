# SOURCE-JOIN-COHERENCE56 — bounded PNP/RP synthesis

Timestamp: 2026-10-22 04:48 KST  
Global status: **P versus NP OPEN; P versus RP OPEN.**  
Scope: two P-vs-NP routes only, plus the independent P-vs-RP audit. Circuit-SAT is a representation experiment, not a third route.

## Repairs proposed before the construction

1. **One global source assignment.** Sample or enumerate the original input variables once, then deterministically evaluate the shared circuit/Tseitin trace. This preserves one-sided soundness, but acceptance density is `#SAT/2^n`, which need not be inverse polynomial.
2. **Exact source-equality joins.** If clause occurrences receive separate local rows, connect all occurrences of each source variable by a spanning tree of equality constraints. This is falsified as an RP repair unless the joined object can be sampled or counted efficiently; it is retained as the semantic-correctness repair.
3. **Bounded-frontier exact propagation.** For a fixed clause ordering, keep the assignments to source variables that occur on both sides of the cut. It is polynomial only when the charged frontier width is `O(log n)`; a small wrapper-DAG boundary is not automatically a small clause/source frontier.

## Constructed lemma: source-join coherence

Let `F = AND_i C_i` be a proper 3CNF. Replace every occurrence of an original variable `x` in clause `C_i` by a local variable `y_(i,x)`, forming `Loc(F)`. Add equality constraints that connect all occurrences of each original variable; a spanning tree for each variable suffices.

**ESTABLISHED.** Satisfying assignments of `F` are in bijection with satisfying local-row tuples of `Loc(F)` that obey all equality joins. Restriction maps a coherent local tuple to one value per original variable. Conversely, copying a satisfying global assignment to all its occurrences produces one coherent local tuple. These maps are inverses, so the transformation is parsimonious.

**ESTABLISHED.** Without the joins, every proper non-tautological 3-clause has seven satisfying local rows. Therefore `Loc(F)` has exactly `7^m` local satisfying tuples, independently of whether `F` is satisfiable. With `t` independently sampled 3-bit rows per clause, the probability that each clause sees at least one satisfying row is

`(1 - 8^(-t))^m`.

Thus `t = ceil(log_8(2m))` makes this probability at least one half for satisfiable and unsatisfiable inputs alike. This sampler is **RETIRED** as an RP algorithm for SAT.

**ESTABLISHED, restricted.** A fixed clause order admits exact dynamic programming over the live source frontier. If its maximum width is `w`, the table has at most `2^w` keys and can be updated in `m * 2^(w+O(1))` time with `2^w` table space, plus charged formula access. This is an algorithm for the bounded-width representation, not a lower bound and not a general SAT algorithm.

## Real WRAPPER root audit

The checked root is the 20-clause, 14-variable proper 3CNF in [`experiments/DOUBLE_WRAPPER_2026-10-07/example_dag.json`](https://github.com/j15marti/pnp/blob/main/experiments/DOUBLE_WRAPPER_2026-10-07/example_dag.json). The repository reports wrapper `max_boundary_size = 2`; that is a wrapper-DAG separator and is kept distinct from the clause/source frontier measured here.

| Charged quantity | Result |
|---|---:|
| Global satisfying assignments | 1,948 |
| Unjoined local satisfying tuples | 79,792,266,297,612,001 (`7^20`) |
| Source occurrences / variables | 60 / 14 |
| Equality joins in occurrence spanning trees | 46 |
| Local sampler, `t=2` | 0.729812855990524 |
| Natural-order source frontier | width 14; 3,752 reachable states |
| Greedy-order source frontier | width 5; 24 reachable states |
| Shared-negation circuit | 67 gates |
| Per-occurrence-negation circuit | 74 gates |

Both circuits agreed with the formula on all `2^14` sources and had exactly 1,948 accepting sources. For each fixed source, deterministic gate evaluation gives one trace. Gate sharing saves seven gates here; it does not create hidden hardness, because direct gate inspection evaluates either circuit in linear time in its gate count.

The eight-clause blocker forbidding every assignment to three variables has zero global witnesses and zero coherent local tuples, yet its unjoined `t=2` sampler accepts with exact probability `63^8/64^8 = 0.8816264350298333`. High ANF degree or unique deterministic traces cannot repair omitted source joins.

Finite audit: 49,380 assertions, including 160 random proper-3CNF coherence checks, exhaustive evaluation of both 14-input circuits, both frontier counts, and the blocker. This is evidence for the finite implementation and algebraic identities only.

## Five-role integration and statuses

### :00 SAT-to-ordinary-MKTP

- **ESTABLISHED:** a faithful Circuit-SAT/Tseitin representation must preserve the shared source map; locally independent clause rows change the semantic object.
- **OPEN:** deterministic total both-label SAT-to-ordinary-MKTP generation with the required ordinary KT threshold, same-machine time, output materialization, and no oracle leakage.
- **Next discriminating test:** run the proposed LOW/HIGH generator on two encodings of the same circuit—shared-source Tseitin and occurrence-copied-with-joins—and prove a representation-stable KT gap after charging the joins and full output.

### :12 P != RP investigator

- **ESTABLISHED:** global-source sampling is sound but may have exponentially small success probability; unjoined local sampling has large density but false accepts UNSAT inputs.
- **RETIRED:** CLAUSE-COHERENCE20 local resampling and ANF-degree repair as RP algorithms for SAT.
- **OPEN:** an explicit language in RP outside every deterministic polynomial-time machine.
- **Next discriminating test:** for any proposed local Circuit-SAT verifier, automatically extract its source-equivalence relation and search for two local accepting views that disagree on one original wire.

### :24 arbitrary-decider ARC/FLMV

- **ESTABLISHED, restricted:** exact frontier propagation accounts for source consistency; on this instance greedy width five produces 24 reachable states.
- **OPEN:** an all-input, hereditary, fully charged contractor for every assumed polynomial SAT decider that reaches the matched FLMV simultaneous time-space endpoint. Instance width and selected orders do not establish heredity.
- **Next discriminating test:** apply each ARC contraction to a family whose clause/source frontier provably expands after restriction, and record source acquisition, table peaks, replay, output, and the same-machine conversion.

### :36 P = RP derandomization

- **ESTABLISHED:** exact propagation over a complete polynomial semantic state space derandomizes that restricted verifier; a short digest is sufficient only when every hidden influence factors through it.
- **CONDITIONAL:** bounded-frontier CNFs and complete polynomial-state verifiers have exact deterministic simulations.
- **OPEN:** uniform deterministic simulation of every RP machine. Neither a random hash nor a selected small frontier supplies it.
- **Next discriminating test:** augment the DIGEST-LUMP19 transition-consistency checker with explicit source-join state and determine whether its state count remains polynomial on adversarial shared-source DAGs.

### :48 synthesis

- **ESTABLISHED:** Circuit-SAT and proper 3CNF agree parsimoniously only when source sharing and functional gate traces are preserved. Equality joins repair semantics, not complexity.
- **RETIRED:** transferring the wrapper's reported boundary two to the clause/source frontier; the audited values are five (greedy) and fourteen (natural).
- **OPEN:** both P-vs-NP arrows and both directions of P-vs-RP.
- **Next discriminating test:** make source-join width a mandatory ledger field and reject any proof step whose alleged state quotient omits a live shared wire, timer, solver state, history bit, or source-access cost.

## Model and quantifier firewall

- The bijection is `for every global assignment, exactly one coherent occurrence tuple`; it is not `for each clause there exists an independently chosen row`.
- Deterministic circuit trace uniqueness is conditional on a fixed complete source assignment. It does not determine the source and does not amplify witness density.
- The frontier table is explicit space, not free advice. The formula scan, ordering, equality joins, and output are charged.
- The finite experiment does not transfer to unrestricted circuit families, random-oracle models, proof-system lower bounds, or class separations.

## Sources and artifact state

- Repository primary instance: [`example_dag.json`](https://github.com/j15marti/pnp/blob/main/experiments/DOUBLE_WRAPPER_2026-10-07/example_dag.json).
- Repository quantifier comparison: [`wrapper_sat_quantifier_demo.py`](https://github.com/j15marti/pnp/blob/main/experiments/wrapped_dag/wrapper_sat_quantifier_demo.py).
- Audit program: `experiments/review/2026-10-22_clause_join_frontier56_audit.py`.

Publication state is recorded only after commit and raw-file readback. No root manuscript was edited.
