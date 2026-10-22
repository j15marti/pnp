# VIRTUAL-CHILD-COMPOSITION61

Timestamp: 2026-10-22 09:48 KST  
Global status: **P versus NP OPEN; P versus RP OPEN.**  
Scope: two P-vs-NP routes plus the independent P-vs-RP question. Circuit-SAT remains a representation and hostile-control tool.

## Repairs proposed before source review

1. **Canonical restriction provenance:** encode each pure-restriction child by a short assignment/path descriptor and reconstruct its syntax locally.
2. **Solver-charged semantic key:** compute child compatibility with the assumed SAT decider, charging every call as `Q*T(L)` rather than hiding semantic work in a “key.”
3. **Representation-invariant virtual child:** replace literal source-key membership by a short descriptor `d` and a local evaluator `g(x,d,i)` for the `i`th bit of the ordinary child encoding.

The third repair was formalized and tested. It subsumes the useful part of the first and gives the correct accounting for the second, but it does not construct the required descriptor/evaluator for arbitrary ARC children.

Repository sources reviewed after fixing these proposals:

- [`ARC-INDEX34`](https://github.com/j15marti/pnp/blob/main/research/agents/arc/2026-10-22_ARC_INDEX34.md), including its FLMV bit-addressable-reduction ledger and the exact target recurrence;
- [`ROUND-ADAPTIVE-BATCHING60`](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-22_0848_MAIN_ROUND_ADAPTIVE_BATCHING60.md), which supplies bounded-round descriptor acquisition;
- [`AFFINE-BASIS25`](https://github.com/j15marti/pnp/blob/main/research/agents/rp-derandomization/2026-10-22_0836_RP_AFFINE_BASIS25_HANDOFF.md), the latest restricted P=RP-side result and source-channel audit.

## Lemma 61A — virtual-child composition

Let `A` be any deterministic decider on an ordinary read-only input `y` of length at most `L`, with time `T_A(L)` and work space `S_A(L)`. Let a parent input `x` have length `N`. Suppose a descriptor `d` has `polylog N` bits and there is a deterministic evaluator

`g(x,d,i) = the i-th bit of child y_d`

using `polylog N` time and `O(log N)` auxiliary space, with read-only random access to `x`.

Then `A(y_d)` can be simulated without materializing `y_d` in

`T_A(L) polylog N`

time and

`S_A(L)+O(log N)`

space. The claim holds for every deterministic `A`, including adaptive rereads of its input.

**Proof.** Simulate the complete configuration of `A`. Whenever its input head or index mechanism requests position `i`, run `g(x,d,i)` and return that bit. Every step of `A` causes at most a polylogarithmic simulation overhead; the evaluator workspace can be reused after each bit request. No child buffer persists. **Status: ESTABLISHED composition lemma under the stated input-access model.**

This is a machine-composition statement, not an all-input ARC construction. A final proof must show that the exact FLMV machine conventions permit this simulation with only the claimed polylogarithmic overhead.

## Corollary 61B — matched ARC recurrence

Assume a parent procedure produces and validates

`Q=N^(0.6+o(1))`

short descriptors for virtual children of length

`L=N^(0.5+o(1))`,

using `N^(1.1+o(1))` time and `N^(0.5+o(1))` peak space. Sequentially simulate a SAT decider `A` of exponents `(t,s)` on each virtual child. Lemma 61A gives

`t' <= max(1.1, 0.6+t/2)+o(1)`,

`s' <= max(0.5, s/2)+o(1)`.

This is exactly the intended ARC successor. For `t>1.2`, the time exponent contracts toward the fixed point `1.2`; space contracts toward `0.5`. At `(t,s)=(1.203,0.505)`, one step gives `(1.2015,0.5)` before lower-order terms. Iteration can approach the FLMV-forbidden neighborhood only if the descriptor constructor, all-input correctness, heredity, acquisition ledger and exact model transfer are all proved.

**Status: CONDITIONAL recurrence instantiated from an ESTABLISHED composition lemma.** The load-bearing constructor hypotheses remain **OPEN**.

## Materialization trilemma

At the target parameters, literal child materialization has three incompatible options:

1. Holding `B=N^0.5` children of length `L=N^0.5` simultaneously costs `BL=N` bits, violating the `N^0.5` space target.
2. Rebuilding one child from a complete parent scan for each of `Q=N^0.6` children costs `NQ=N^1.6` time.
3. Writing all children once costs `QL=N^1.1` time, but a write-only stream does not supply the random-access input needed by an arbitrary decider.

The virtual-child evaluator is the exact fourth option: keep one short descriptor and simulate input reads on demand. It avoids both `N`-bit batch storage and `N^1.6` rescanning.

**RETIRED at the target exponents:** storing a full `B`-child batch as the implementation of ROUND-ADAPTIVE-BATCHING60. Query/descriptor batching remains viable; child bodies must be virtual, streamed to a compatible online solver, or otherwise locally indexable.

## Source-key and representation consequences

A literal syntactic key is sufficient for ARC-INDEX34 because its blockers expose membership directly. Arbitrary SAT compatibility is semantic and need not appear as a source record. Lemma 61A therefore changes the constructive target:

- descriptor generation must be source-checkable on every input;
- `g` must reproduce the **ordinary encoded child bit-for-bit**, including Tseitin/source-join conventions;
- equivalent circuit/CNF representations must not silently change correctness or resource bounds;
- descriptor generation, failed branches, ancestor state, source acquisition and validation are charged;
- pure-restriction heredity does not imply heredity after reductions, source duplication or added equality joins.

Circuit-SAT gate-trace uniqueness helps compute auxiliary bits only after all primary/source bits and the gate role map are available. It does not supply semantic child descriptors by itself. DIGEST-LUMP19 and CLAUSE-COHERENCE20 remain unchanged.

## RP cross-audit

AFFINE-BASIS25 proves a uniform hitting set only when the complete verifier factors through certified full-row-rank affine coordinates with conditionally independent local factors. Its 46-gate control correctly evaluates the unchanged verifier on original random tapes; independently sampling Tseitin auxiliaries remains unsound. The theorem is **ESTABLISHED restricted**, while generalized-WRAPPER factorization and universal derandomization remain **OPEN**.

Virtual-child composition neither strengthens nor refutes that theorem. It provides no RP language outside P and no uniform deterministic simulation of every RP machine.

## Finite audit

[`2026-10-22_virtual_child_composition61_audit.py`](https://github.com/j15marti/pnp/blob/main/experiments/review/2026-10-22_virtual_child_composition61_audit.py) passed **340,047 assertions**:

- 7,362 virtual children over 180 random parents;
- 1,181,492 adaptive input reads by deterministic rereading procedures;
- bit-for-bit and final-answer equality with materialized execution;
- exact recurrence checks for seven `(t,s)` pairs, including `(1.203,0.505)`;
- materialization controls `BL=N^1`, `QL=N^1.1`, `NQ=N^1.6`, and one-child buffer `N^0.5`.

Finite tests validate the simulator and algebraic ledger only.

## Five-role status ledger

| Role | Status | Consequence | Single next discriminating test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** Virtual-index composition **ESTABLISHED**. | A target with a short descriptor and fast bit evaluator is evidence toward ordinary-KT LOW, not HIGH. The same local indexability useful for ARC is hostile to MKTP magnification. | Apply the exact ordinary-KT accounting to `g`: program length, parent reconstruction and per-bit simulation time versus `p_k`. |
| :12 P≠RP | **OPEN.** Source-channel firewall **ESTABLISHED**. | A virtual child must expose every source/timer/history dependency used by its bits. No verifier obstruction yields a language lower bound. | Run a generalized-WRAPPER bit-dependency trace and test for a deterministic direct decider before any RP claim. |
| :24 ARC/FLMV | Lemma 61A **ESTABLISHED**; recurrence **CONDITIONAL**; constructor/heredity **OPEN**. | Physical child materialization is no longer necessary if a short, locally indexable ordinary-child descriptor exists. This is now the most precise constructive interface. | Build `d,g` for one real nontrivial ARC child family and verify every emitted bit against independently materialized CNF on SAT and UNSAT parents. |
| :36 P=RP | AFFINE-BASIS25 **ESTABLISHED restricted**; universal derandomization **OPEN**. | Certified affine factorization supplies a restricted hitting set only. Virtual input access does not certify the factorization. | Propagate original-coin affine masks through one generalized WRAPPER until the first nonlinear overlap; output a certificate or counterexample. |
| :48 synthesis | Both class questions **OPEN**. | The ARC recurrence now has an exact conditional implementation avoiding child storage; all burden moves to the all-input hereditary bit constructor and model match. | Attempt the descriptor/bit constructor before any further exponent optimization. |

## Route conclusion

- **MKTP magnification:** still missing the total both-label SAT-to-ordinary-MKTP HIGH generator. Local bit indexability is primarily a LOW-side audit.
- **ARC/FLMV:** substantive interface advance. Given an all-input hereditary virtual-child constructor, arbitrary deciders compose with precisely the desired recurrence without materialization. Constructing that `d,g` interface remains **OPEN**.
- **P versus RP:** both equality and separation remain **OPEN**; AFFINE-BASIS25 remains a restricted subclass theorem.

No root manuscript, automation, or role assignment was modified.
