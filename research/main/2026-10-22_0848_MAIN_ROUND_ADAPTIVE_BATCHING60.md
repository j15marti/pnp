# ROUND-ADAPTIVE-BATCHING60

Timestamp: 2026-10-22 08:48 KST  
Global status: **P versus NP OPEN; P versus RP OPEN.**  
Scope: two P-vs-NP routes plus the independent P-vs-RP question. Circuit-SAT remains a comparison and hostile-control representation.

## Repairs proposed before source review

1. **Round-adaptive batching:** weaken BLOCKED-SOURCE-BATCHING59's full nonadaptivity to `R` adaptive exposure rounds, with every query in a round fixed before that round's parent scans.
2. **Semantic-to-syntactic key compiler:** attach a locally checkable provenance map that turns each semantic child condition into a source-visible key, charging compilation, validation and lookup.
3. **Certified hereditary separator:** recurse only when a supplied separator certificate is source-checkable and preserved by the actual child operation, not merely by an abstract restriction.

The first repair was proved and tested. The second and third remain candidates, not established arrows.

Subsequent repository review covered:

- [`BLOCKED-SOURCE-BATCHING59`](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-22_0748_MAIN_BLOCKED_SOURCE_BATCHING59.md), the preceding nonadaptive construction;
- [`ARC-INDEX34`](https://github.com/j15marti/pnp/blob/main/research/agents/arc/2026-10-22_ARC_INDEX34.md), the keyed source and detached-summary lower-bound control;
- the [08:11 independent review](https://github.com/j15marti/pnp/blob/1b4a93889871f88b82825b6b1fa01ee3984e1db1/comments/grok-4.7/2026-10-22/2026-10-22_0811_GROK_REVIEW.tex), which independently leaves every load-bearing implication open and recommends exact model and quantifier accounting.

## Lemma 60A — exact round-adaptive source batching

Fix an explicit keyed parent source of encoded length `N`. An adaptive client proceeds through `R` rounds. In round `r`, after seeing all earlier answers, it exposes `Q_r` exact membership queries; all queries of that round are fixed before its source scans. Let

`Q = sum_r Q_r`.

For any block capacity `B`, the queries are answered exactly using

`P = sum_r ceil(Q_r/B) <= Q/B + R`

complete parent passes. With deterministic comparison dictionaries on `O(log N)`-bit keys, the charged resources are

`T = G + O(N (Q/B+R) polylog N + Q polylog N) + T_output`,

`S = O(B log N + parser_scratch + S_generator + S_output)`,

where `G,S_generator` charge the adaptive query generator and `T_output,S_output` charge actual child materialization.

**Proof.** Once round `r` begins, partition its fixed query list into blocks of at most `B` records. Build a dictionary for one block, scan the complete parent, and mark precisely those query keys encountered. This is exact even though the next round depends arbitrarily on the current answers. Summing `ceil(Q_r/B) <= Q_r/B+1` gives the pass bound. Only the current query block, parser, generator state and current output are resident. **Status: ESTABLISHED restricted to this explicit keyed-source/work-tape model.**

## Exponent phase law

Write

`Q=N^(alpha+o(1))`, `B=N^(beta+o(1))`, `R=N^(rho+o(1))`.

Ignoring polylogarithmic factors, the source-scan exponent is

`1 + max(alpha-beta, rho)`.

If every child has length `N^(lambda+o(1))`, streamed output has exponent `alpha+lambda`, while the query-block space exponent is `beta`.

At the current ARC candidate values

`alpha=0.6`, `beta=0.5`, `lambda=0.5`,

the simultaneous candidate bounds are met precisely when

`rho <= 0.1`,

provided query generation, parser state, child construction and exact target-machine simulation also fit. Then both source acquisition and output take `N^(1.1+o(1))` time, and the block/current-child buffers use `N^(0.5+o(1))` space.

At `rho=0.11`, source time becomes `N^(1.11+o(1))`; at `R=Q=N^0.6` singleton rounds, it becomes `N^1.6`. Therefore bounded-round exposure, rather than full nonadaptivity, is the exact missing scheduling condition for this batching architecture.

**RETIRED as necessary:** the earlier requirement that all `Q` queries be exposed before any scan. Full nonadaptivity remains sufficient, but Lemma 60A permits arbitrary cross-round adaptivity up to the round budget.

## What the lemma does not supply

The quantifiers are deliberately narrow:

- for every explicit keyed source and every adaptive client already satisfying the round interface, the batching algorithm is exact;
- there is no proof that every arbitrary polynomial SAT decider, every ARC parent, or every real child family admits such keys or `R<=N^(0.1+o(1))` rounds;
- a query generator may itself call the SAT decider or retain large ancestral state; `G` and `S_generator` cannot be hidden;
- a membership answer is not automatically an ordinary SAT child of length `N^0.5`;
- random-access dictionary access is not automatically valid on a one-tape/same-machine endpoint.

Thus the result is a representation/scheduling lemma, not the all-input hereditary ARC contractor.

## Source, circuit and RP firewalls

The existing barriers remain active. A semantic Circuit-SAT condition is not a keyed source record merely because its Tseitin trace is unique. Equality joins among repeated source variables, provenance-map construction, failed-key handling and role-map access must all be charged. DIGEST-LUMP19 still blocks incomplete quotient states; CLAUSE-COHERENCE20 still blocks independently sampled clause occurrences; SOURCE-CHANNEL-COMPLETENESS57 still requires every accessible source/timer/solver/history channel in the interface ledger.

For P versus RP, round-adaptive batching is only a deterministic algorithm for an already keyed query interface. It neither constructs an RP language outside P nor uniformly simulates every RP verifier. COMPONENT-BIAS23 remains restricted to pairwise-disjoint dependency sets on original coin coordinates; round batching does not certify that factorization.

## Finite audit

[`2026-10-22_round_adaptive_batching60_audit.py`](https://github.com/j15marti/pnp/blob/main/experiments/review/2026-10-22_round_adaptive_batching60_audit.py) passed **544,787 assertions**:

- 260 random explicit sources and answer-dependent round clients;
- 542,964 exact membership queries;
- 33,740,739 charged source-record visits;
- exact verification of `sum ceil(Q_r/B) <= Q/B+R`;
- phase-boundary checks at `rho=0,0.05,0.1,0.11,0.2,0.6`;
- a 513-query singleton-round control with exactly 513 parent passes and 525,312 source-record visits.

Finite execution validates this algorithm and its accounting, not an unrestricted asymptotic class claim.

## Five-role status ledger

| Role | Status | Consequence | Single next discriminating test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** Round-batching lemma **ESTABLISHED restricted**. | A source-indexable, bounded-round target may be easier to evaluate and hence ordinary-KT LOW; batching supplies no HIGH lower bound or both-label generator. | Construct the best indexed evaluator for the batched target and compare program length plus per-bit runtime with the exact `p_k` threshold. |
| :12 P≠RP | **OPEN.** SOURCE-CHANNEL firewall **ESTABLISHED**. | The round transcript is another charged source channel. No verifier obstruction survives an easy independent language decider automatically. | On one generalized WRAPPER, log every original source/gate/timer read and test whether the accepting language has a direct deterministic bypass. |
| :24 ARC/FLMV | Lemma 60A **ESTABLISHED restricted**; bounded-round keyed exposure **OPEN**; all-input hereditary contractor **OPEN**. | Full nonadaptivity is no longer necessary. The exact target is at most `N^0.1` exposure rounds, with all generation and machine costs charged. | Instrument one genuine ARC recurrence and measure `Q_r`, key length, query-generation time/state, child size and parent passes on both SAT and UNSAT inputs. |
| :36 P=RP | **OPEN.** COMPONENT-BIAS23 remains **ESTABLISHED restricted**. | Batching cannot certify disjoint original-coin factors or provide a universal hitting set. | Produce dependency cones over original randomness for one nonlinear verifier and report a disjoint-factor certificate or first overlap. |
| :48 synthesis | Both class questions **OPEN**. | The ARC scheduling gap is narrowed from nonadaptivity to a quantitative phase boundary `rho<=0.1`. | Prove a source-key compiler plus the `R<=N^(0.1+o(1))` exposure theorem, or falsify it with a concrete adaptive ARC child family. |

## Route conclusion

- **MKTP magnification:** unchanged missing arrow—deterministic total both-label SAT-to-ordinary-MKTP generation at the actual threshold, with source and same-machine costs.
- **ARC/FLMV:** substantive restricted advance—the keyed batching escape tolerates `N^(0.1+o(1))` adaptive rounds. The arbitrary-input keyed-exposure/compiler/heredity theorem remains **OPEN**.
- **P versus RP:** both equality and separation remain **OPEN**; no language-level implication was added.

No root manuscript, automation, or role assignment was modified.
