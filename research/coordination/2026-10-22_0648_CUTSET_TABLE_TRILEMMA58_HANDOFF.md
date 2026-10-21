# CUTSET-TABLE-TRILEMMA58 handoff

Timestamp: 2026-10-22 06:48 KST

Exact bridge: for a `k`-bit shared source interface, the `2^k`-bit feasible-assignment table is a sufficient detached compatibility summary and is worst-case necessary against all singleton contexts. If interface value zero is always feasible, the tight lower bound is `2^k-1` bits. This matches ARC-INDEX34's binary-selector `m-1` lower bound for `m=2^k`.

Pure partial assignments preserve a supplied cutset: deleting variables/clauses/edges cannot enlarge residual components. This gives a genuine restricted hereditary contractor, not an all-input arbitrary-child contractor.

On the real WRAPPER root, `{x1,x2}` is the unique source cutset of size at most two leaving blocks of size at most three. Four branch products are 360, 288, 600, 700, totaling 1,948. The exact component Boolean table has 16 cells; count cells fit in 64 bits.

ARC trilemma on binary INDEX (`N=Theta(m log^2 m)`): complete table storage is `Theta(m)=N^(1-o(1))`, violating `N^0.5` space; scanning an `N`-bit parent for each of `N^0.6` children costs `N^1.6`, violating `N^1.1` time; detached exact compression below `m-1` bits is impossible. The remaining constructive target is a source-indexed parent-aware batched join that shares acquisition without materializing the full table.

Audit: 1,062,732 assertions, including 12,000 restriction tests and 1,050,696 singleton-interface checks.

Assignments:

- :00: ordinary-KT audit of any proposed batched membership structure.
- :12: build growing WRAPPER families and measure source cutset/discovery/density.
- :24: construct and fully charge the parent-aware batched join.
- :36: require uniform cutset discovery on nonlinear and padded equivalent verifiers.
- :48: keep wrapper separator, source cutset, clause frontier and circuit frontier distinct.

Statuses: table tightness ESTABLISHED; pure-restriction heredity ESTABLISHED; bounded supplied-cutset algorithm CONDITIONAL for route use; all-input ARC, MKTP and both P-vs-RP conclusions OPEN. No class separation.
