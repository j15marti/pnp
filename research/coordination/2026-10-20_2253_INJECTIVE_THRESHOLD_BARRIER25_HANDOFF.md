# INJECTIVE-THRESHOLD-BARRIER25 role handoff

Timestamp: 2026-10-20 22:53 Asia/Seoul  
Status: ESTABLISHED counting barrier; load-bearing reductions OPEN; P versus NP OPEN.

## New exact result

For a fixed finite fan-in-two basis, let `R_N:{0,1}^N->{0,1}^M` be injective,
`M=N^(a+o(1))`, and `a*beta' < beta < 1`. For all sufficiently large
power-of-two lengths, some source truth table has circuit size at most
`N^beta` while its image has circuit size greater than `M^beta'`.

Proof witness family: the `2^h` tables arbitrary on a prefix of
`h=floor(N^gamma)` entries and zero elsewhere, where
`a*beta' < gamma < beta`. Each has a canonical DNF of size
`O(h log N) < N^beta`, while only
`2^(N^(a*beta'+o(1))) = 2^o(h)` target tables have circuit size
`<=M^beta'`. Injectivity forces one image outside the target YES set.

Consequence: every near-linear strict threshold descent must be lossy and must
prove source-label-monochromatic fibers. Reversible or injective mixing is now
RETIRED as a descent mechanism. The boundary `a*beta'=beta` is not resolved.

Audit: 7,949 exact checks, zero failures; 1,102 strict rational triples, 52
equality cases explicitly excluded, three finite circuit-count controls through
`n=800`, and 156 exhaustive small DNF instances.

## Peer integration

- `CHMY-QUERYFRONTIER24`: source-valid CHMY oracle tradeoff recovered; its
  adjacent-pair transform is a special case of the injective barrier.
- `ARC-HEREDITARY-SCOPED10`: fixed-depth heredity is exact for valid scoped
  streams with `w=o(log N)`, but the promise is directly solvable in
  `N^(1+o(1))` time and `N^o(1)` space. It is a control, not the all-input ARC
  arrow.
- COMPACT-HISTORY20 remains diagnostic only; its `exists W forall i` size
  premise is OPEN.

## Next tests

- **:00 MCSP:** propose a many-to-one map plus checkable fiber invariant; find
  the smallest mixed-label collision.
- **:12 Universal Solver:** test canonical fiber representative selection
  without an M-bit table; audit whether the unknown exponent C is merely moved.
- **:24 ARC:** instrument arbitrary-CNF acquisition, charging reads, emitted
  bits, live width, replay, output, and all-input correctness.
- **:36 Redteam:** attack the circuit encoding/equality boundary and minimize a
  mixed-label collision or high-width ARC failure.
- **:48 Synthesis:** require a monochromatic-fiber proof or matched all-input
  random-access ledger before promotion.

Root `main.tex` was not modified. No schedule or third route was created.
