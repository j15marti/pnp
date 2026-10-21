# BLOCKED-SOURCE-BATCHING59

Timestamp: 2026-10-22 07:48 KST  
Global status: **P versus NP OPEN; P versus RP OPEN.**  
Scope: the two P-vs-NP routes and the independent P-vs-RP question. Circuit-SAT remains a representation/control experiment.

## Repairs proposed before source review

1. **Blocked parent scans:** place `Q=N^(0.6+o(1))` compatibility queries into blocks of `B=N^(0.5+o(1))`, then perform one parent-source pass per block.
2. **Charged source index:** replace repeated scans by a bit-addressable parent index, but count index construction, storage, lookup and same-machine simulation.
3. **Certified hereditary separator:** recurse only when a source-visible separator and its child preservation certificate are supplied and locally checkable.

The first mechanism was built and audited below. The second still risks the `N^(1-o(1))` complete-table space lower bound from CUTSET-TABLE-TRILEMMA58. The third is sound for pure restrictions of a supplied cutset, but remains unavailable for arbitrary ARC children.

Repository sources reviewed after proposing the repairs:

- [`ARC-INDEX34`](https://github.com/j15marti/pnp/blob/main/research/agents/arc/2026-10-22_ARC_INDEX34.md), which gives the canonical keyed INDEX source, the detached `m-1`-bit lower bound, and the `N^1.6` one-scan-per-child failure;
- [`COMPONENT-BIAS23`](https://github.com/j15marti/pnp/blob/e9a196ced58568ab453c12b0e42187ee2ebd30ae/research/agents/rp-derandomization/2026-10-22_0636_RP_COMPONENT_BIAS23_HANDOFF.md), which gives a restricted hitting construction only when factors depend on pairwise-disjoint sets of original random-tape coordinates.

## Lemma 59A — exact blocked source batching

Let a parent be an explicit stream of total encoded length `N`, with each record exposing a uniformly computable key. Let `q_1,...,q_Q` be exact membership queries known before processing starts. For any `1<=B<=Q`, a deterministic algorithm answers all queries exactly using

`ceil(Q/B)` parent passes,  
`O(N ceil(Q/B) log B + Q log B)` time, and  
`O(B log N + parser_scratch)` bits of peak workspace,

provided a deterministic comparison dictionary supports lookup in `O(log B)` time. Duplicate queries are allowed.

**Proof.** For each consecutive block of at most `B` queries, store a balanced dictionary from query key to all positions in that block, initialize the answers to false, and scan the parent once. When a source record's key is in the dictionary, set all corresponding answers to true. Exactness follows because a query is marked iff its key occurs in the complete parent scan. Only the current block and parser state are resident. Dictionary construction and all source-record lookups give the stated time. No random hash, SAT call, or detached summary is used. **Status: ESTABLISHED in this explicit keyed-stream/random-access work-tape model.**

This is not yet a one-tape or arbitrary-machine theorem. If the target model cannot address the `B`-record dictionary in logarithmic time, the simulation overhead must be charged before importing the exponent ledger.

## Exact exponent ledger

Set

`Q=N^0.6`, `B=N^0.5`, and child length `L=N^0.5`,

up to subpolynomial factors. Then there are `N^0.1` source passes. Lemma 59A costs

`N * N^0.1 * polylog(N) = N^(1.1+o(1))` time

and `N^(0.5+o(1))` working space. If `Q` actual children of length at most `L` are emitted one at a time to a write-only output, materialization costs `QL=N^1.1` time and one `N^0.5` child buffer. Thus source scanning and output materialization meet the candidate ARC exponents simultaneously in this restricted model.

The accounting includes negative membership answers and every source pass. It does **not** yet include a proof that arbitrary SAT compatibility has source-visible keys, that all queries are nonadaptive, that a real child can be generated from one membership bit, or that the dictionary implementation matches the eventual FLMV machine.

## Adaptive-query hostile control

If `q_(i+1)` depends on the answer to `q_i`, only one query may be known before each pass. The audited sequential-rescan architecture then performs `Q` parent scans and returns to `NQ=N^1.6` time. This is an architectural counterexample to applying Lemma 59A to adaptive ARC trees.

It is **not** a lower bound for unrestricted algorithms: an indexed source, a different representation, or joint symbolic evaluation might defeat rescanning. The exact missing condition is therefore a nonadaptive exposure theorem (or an equivalent bounded-round theorem) for the children actually used by the ARC recurrence.

## Circuit-SAT and source-channel audit

SOURCE-CHANNEL21, DIGEST-LUMP19 and CLAUSE-COHERENCE20 remain intact:

- a short digest is not a complete state unless all source/timer/history influence factors through it;
- verifying nonlinear same-digest transition congruence can itself be coNP-complete;
- independently sampled Tseitin/clause-occurrence witnesses lose equality of original source variables and can accept UNSAT formulas;
- source-visible forced-3CNF families can be easy by direct gate/clause inspection even when restricted digest/probe inequalities look large.

Lemma 59A deliberately exploits the source channel. Consequently it refutes neither SOURCE-CHANNEL21 nor the detached-summary lower bound: it trades storage for `N^0.1` charged source passes. For a general Circuit-SAT/Tseitin DAG, gate-trace uniqueness does not create the required keys or nonadaptive query list; shared source variables and equality joins still have to be represented exactly.

## COMPONENT-BIAS23 cross-audit

The new :36 handoff is compatible with the existing firewalls. Its hitting set evaluates the **unchanged verifier** and is valid only when

`R(x,r)=AND_j f_j(r restricted to B_j)`

for pairwise-disjoint subsets `B_j` of original random-tape positions with `|B_j|=O(log n)`. That is a genuine restricted derandomization: independence gives the product/density bound, and the small-bias enumeration remains polynomial. Tseitin auxiliary uniqueness is irrelevant unless the original coin dependencies are actually disjoint; independently randomizing auxiliary gates is unsound. Certifying such source factorization for arbitrary verifier circuits is still **OPEN**. The forced-3CNF source scanner is an easy-P hostile control, not evidence for either `P=RP` or `P!=RP`.

## Finite audit

[`2026-10-22_blocked_source_batching59_audit.py`](https://github.com/j15marti/pnp/blob/main/experiments/review/2026-10-22_blocked_source_batching59_audit.py) passed **287,759 assertions**:

- 240 randomized keyed streams;
- 286,522 exact membership queries, including duplicates;
- 11,836,513 charged source-record visits;
- exact pass, visit and peak-block counts;
- symbolic exponent checks through `log2 N=640` for the `(Q,B,L)=(N^0.6,N^0.5,N^0.5)` ledger;
- a 257-round adaptive client requiring 526,336 source-record visits in the explicit sequential-rescan architecture.

Finite tests validate the implementation and ledger only; they do not establish any class separation or general SAT contractor.

## Five-role status ledger

| Role | Status | Current implication | Single next discriminating test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** Source-index KT transfer remains **ESTABLISHED restricted**. | A uniformly source-indexable target risks being ordinary-KT LOW; batching answers labels but does not produce a both-label HIGH target or meet the `p_k` threshold. | Encode the batch algorithm's target bits and charge program length, source reconstruction, per-bit time and total output against the exact ordinary-KT threshold. |
| :12 P≠RP | **OPEN.** SOURCE-CHANNEL21 inequality is **ESTABLISHED restricted**. | Omitting source queries invalidates the digest/probe bound; keyed source scans can make the control family easy. No RP language outside P is obtained. | Run the complete `q,b,t,h` source-channel ledger on one generalized WRAPPER netlist and exhibit either a polynomial source scanner or a rigorously hidden channel. |
| :24 ARC/FLMV | Lemma 59A **ESTABLISHED restricted**; all-input hereditary contractor **OPEN**. | The canonical nonadaptive keyed membership bottleneck fits `N^(1.1+o(1))` time and `N^(0.5+o(1))` space without a full table. Arbitrary SAT keys, query rounds, child construction, hereditary preservation and exact machine simulation are missing. | Instrument one genuine ARC parent to log the time each child query becomes known; accept the repair only if all `N^0.6` queries are exposed in `N^0.1+o(1)` rounds with source-visible keys. |
| :36 P=RP | COMPONENT-BIAS23 **ESTABLISHED restricted**; universal derandomization **OPEN**. | Pairwise-disjoint original-coin factors admit a uniform polynomial hitting set. Gate sharing or source overlap destroys the premise, and factorization certification is not known for arbitrary circuits. | Compute dependency cones of one generalized WRAPPER verifier over original coin coordinates and either certify disjoint factors or output the first overlapping pair. |
| :48 synthesis | Both class questions **OPEN**. | Parent-aware batching is the first exact mechanism to meet the numeric ARC scan/output ledger on ARC-INDEX, but it is a representation lemma rather than the missing theorem. | Prove a bounded-round source-key exposure lemma for all generated ARC children, or retire batching as a route to arbitrary deciders. |

## Two-route conclusion

- **MKTP magnification:** unchanged missing arrow—deterministic, total, both-label SAT-to-ordinary-MKTP generation at the actual KT threshold, with source and same-machine costs charged.
- **ARC/FLMV:** improved from a storage/rescan trilemma to a restricted constructive escape. The canonical keyed, nonadaptive INDEX join now meets the target exponent ledger. The load-bearing all-input/hereditary/bounded-round/source-key theorem remains **OPEN**.
- **P versus RP:** COMPONENT-BIAS23 adds a valid restricted derandomization subclass only. Uniform simulation of every RP machine and an RP language outside all deterministic polynomial-time machines both remain **OPEN**.

No root manuscript, automation, or role assignment was modified.
