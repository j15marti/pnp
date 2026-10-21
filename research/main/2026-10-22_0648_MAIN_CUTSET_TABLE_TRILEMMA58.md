# CUTSET-TABLE-TRILEMMA58

Timestamp: 2026-10-22 06:48 KST  
Global status: **P versus NP OPEN; P versus RP OPEN.**  
Scope: two P-vs-NP routes plus the independent P-vs-RP question. Circuit-SAT remains a comparison and hostile-control representation.

## Repairs proposed before report and literature review

1. **Source-checkable interface table:** replace a detached SAT-label portfolio by the exact feasible-assignment table on a shared source cutset; verify every table entry from the source components.
2. **Streaming/rescan alternative:** avoid storing the full table by answering requested interface memberships from a source scan, while charging every rescan and the peak buffer.
3. **Restriction heredity:** retain a cutset through partial assignments and test whether component width can increase. Reject any transfer from this restricted heredity to arbitrary generated children without a representation theorem.

The subsequent review used three new repository reports: LOCALITY-LEDGER33 (:00), SOURCE-CUTSET22 (:12), and ARC-INDEX34 (:24). Primary references checked were Fortnow–Lipton–van Melkebeek–Viglas, [*Time-Space Lower Bounds for Satisfiability*](https://lance.fortnow.com/papers/files/tst.pdf), and Yannakakis, [*Algorithms for Acyclic Database Schemes*](https://www.vldb.org/conf/1981/P215.PDF). These sources support charged random-access/index tapes and efficient acyclic-join evaluation; neither supplies the missing all-input contractor.

## Lemma 58A — exact cutset table and worst-case tightness

Let two source fragments interact only through a `k`-bit interface `s`. For a left fragment `A`, define its feasible set

`X_A = {s in {0,1}^k : A has a satisfying extension at s}`.

The `2^k`-bit characteristic table of `X_A` is an exact context-independent summary: a singleton right context fixing `s=j` joins satisfiably exactly when the `j`th table bit is one.

**ESTABLISHED.** This upper bound is worst-case tight. If every subset of `{0,1}^k` can occur as `X_A`, singleton right contexts distinguish all `2^(2^k)` subsets, so any deterministic detached exact summary needs at least `2^k` bits. If one interface value is promised feasible in every `X_A`, there remain `2^(2^k-1)` possibilities and the lower bound is `2^k-1` bits.

This exactly identifies ARC-INDEX34's binary-selector lower bound: with `m=2^k` interface values and value zero forced feasible, the necessary detached message is `m-1` bits. The complete cutset table is not a better asymptotic repair; it matches the lower bound.

## Lemma 58B — restricted hereditary cutset evaluation

Suppose a CNF has a supplied cutset `S` of size `k` such that deleting `S` leaves source-primal components `B_j` of size at most `b`. Then model counting and SAT can be evaluated by

`sum over s in {0,1}^k of product over j of #extensions of B_j at s`,

using `O(2^k sum_j 2^|B_j|)` local valuations, plus explicitly charged input access, arithmetic and table space.

**ESTABLISHED, restricted.** Under a pure partial assignment, clauses, variables and primal edges are only deleted. Therefore `S` minus the fixed cutset variables remains a cutset and every residual component is a subset of an old `B_j`; neither `k` nor `b` increases. This is genuine heredity for restrictions of the same representation.

It is **not** heredity for arbitrary ARC children produced by reductions, Tseitin conversion, source duplication or added equality constraints. Those operations may create new interface variables and edges.

If `k+b=O(log N)` and the cutset is supplied or uniformly found in polynomial time, this gives a polynomial algorithm. Naive discovery over all `k=O(log N)` subsets need not be polynomial; discovery is a separate charged obligation.

## Real WRAPPER audit

For the 20-clause, 14-variable root in [`example_dag.json`](https://github.com/j15marti/pnp/blob/main/experiments/DOUBLE_WRAPPER_2026-10-07/example_dag.json), all 106 source subsets of size zero, one or two were checked. The unique cutset leaving components of size at most three is `{x1,x2}`. The four residual components are

`{3,4,5}`, `{6,7,8}`, `{9,10,11}`, `{12,13,14}`.

| `x1x2` | Component counts | Product |
|---|---|---:|
| 00 | 3, 4, 5, 6 | 360 |
| 01 | 4, 4, 3, 6 | 288 |
| 10 | 5, 4, 6, 5 | 600 |
| 11 | 7, 5, 5, 4 | 700 |

The total is `1,948`, matching exhaustive source enumeration. The component-feasibility interface uses only 16 Boolean cells; storing all four-bit component counts uses 64 bits. This is a finite easy fixture. The wrapper-DAG separator two, source cutset two and earlier greedy clause frontier five are distinct parameters and are not interchangeable without proof.

## ARC storage/rescan trilemma

For ARC-INDEX34's binary selector, `m=2^k` and the explicit source size is `N=Theta(m log^2 m)`. Lemma 58A forces a detached complete table of

`Theta(m) = N^(1-o(1))` bits.

That exceeds both the candidate `N^0.6` summary/query budget and `N^0.5` peak-space target. The source-aware alternative answers membership by scanning the parent in `O(N)` time and `O(log N)` scratch, but independently rescanning for `N^0.6` children costs `N^1.6`, exceeding the candidate `N^1.1` generation budget.

Therefore the current architecture has three options:

1. store the complete detached table and violate peak space;
2. rescan once per child and violate time;
3. construct a new parent-aware batched/indexed compatibility mechanism that shares acquisition without materializing the complete table.

Only option 3 remains a plausible constructive interface. Lemma 58A says it cannot be a context-independent exact summary shorter than the table on the full INDEX family. It would need to exploit the actual requested children, source indexing or additional structure while remaining all-input and hereditary.

## Finite audit

`experiments/review/2026-10-22_cutset_table_trilemma58_audit.py` passed **1,062,732 assertions**:

- all 106 cutset candidates through size two;
- the exact four-branch component table and 1,948 total;
- 12,000 random partial restrictions preserving residual component size at most three;
- 1,050,696 singleton-membership checks over all interface functions through `k=4`;
- table-space exponents for `k=10` through `128`, rising from `0.60082` to `0.90141` relative to `N=m k^2`;
- the `N^1.6` rescan versus `N^1.1` target comparison.

Finite tests validate the implementation, not unrestricted complexity claims.

## Five-role ledger

| Role | Status | Consequence | Single next test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** LOCALITY-LEDGER33 restricted transfer **ESTABLISHED**. | A locally indexed succinct source makes derived targets LOW; an arbitrary interface table can carry `Theta(m)` source information and is not automatically succinct. Source description, indexer and output traffic remain charged. | Apply the exact ordinary-KT ledger to a parent-aware batched membership structure; test whether its description plus query time falls below `p_k` on either label. |
| :12 P≠RP | **OPEN.** Concrete source-cutset factorization **ESTABLISHED restricted**. | One easy WRAPPER fixture and its polynomial d-DNNF do not give a growing-family theorem or a language outside P. Projected primary density remains `1948/2^14<1/2`. | Generate a growing WRAPPER family and measure minimal source cutset, discovery cost and primary density; run verifier replacement on every member. |
| :24 ARC/FLMV | **OPEN.** Cutset heredity under pure restrictions **ESTABLISHED**; general child heredity **OPEN**. | Complete storage violates space; per-child rescans violate time; detached compression is tight on INDEX. | Build one source-indexed batched join algorithm and charge acquisition, index tapes, output children and peak memory against `(1.1,0.5)`. |
| :36 P=RP | **OPEN.** Bounded supplied-cutset simulation **CONDITIONAL**. | Exact propagation works for polynomial cutset tables and bounded components, not arbitrary RP verifiers. Cutset discovery and verifier replacement remain obstacles. | Apply the cutset compiler to a nonlinear verifier and its dummy-padded equivalent; require a uniform polynomial discovery algorithm and preserved primary randomness. |
| :48 synthesis | Both class questions **OPEN**. Cutset-table tightness and restricted heredity **ESTABLISHED**. | Distinguish wrapper separator, source cutset, clause frontier and circuit live frontier in every ledger. | Promote only mechanisms surviving INDEX tightness, source-aware escape, verifier replacement and same-machine peak accounting. |

## Two-route impact

- **MKTP magnification:** unchanged missing arrow—deterministic total both-label SAT-to-ordinary-MKTP generation at the actual ordinary KT threshold. Cutset tables are upper-bound/evaluation objects, not HIGH-KT proofs.
- **ARC/FLMV:** the restricted cutset contractor is now genuinely hereditary under partial assignments, but the all-input parent-aware batched compatibility mechanism is still missing. The storage/rescan trilemma makes that missing arrow more precise.
- **P-vs-RP:** bounded-cutset derandomization is a restricted simulation only. No uniform simulation of all RP machines and no RP language outside P has been obtained.

No root manuscript or role assignment was modified.
