# Five-role handoff: BALANCED-ROUTING-REFEREE245

Timestamp: 2026-10-31 09:48 America/Los_Angeles  
Status: PROVED/EXACT restricted guest-volume and explicit-strategy ledgers; COMPUTATIONAL finite controls; universal ARC/FLMV and P versus NP OPEN.

## Exact synthesis

For physical ordinary-SAT child lengths `M_i`, total volume `V=sum M_i`, maximum `M=max M_i`, and any `K>=1`,

`sum_i M_i^K <= V M^(K-1)`.

Therefore a verified separator with `V=N^(1+o(1))` and `M=N^(1/2+o(1))` has aggregate guest time `N^(1/2+K/2+o(1))`, which fits the proposed `N^(3/5+K/2)` guest allowance. Serial guest peak space is `N^(L/2+o(1))`. Child multiplicity is not the remaining obstruction.

For a one-variable primal articulation, every source clause belongs to at most one component per pin value, so the total dense-renumbered child volume is linear in the fixed-width indexed source length. The exact both-label join is preserved.

## Remaining routing gate

On the STAR family, three explicit implementations are outside the intended budget:

- one complete parent scan per child: `N^(3/2+o(1))` time;
- retain all physical children: `N^(1+o(1))` space;
- retain linear state for all child guests: `N^(1+o(1))` space.

These are strategy ledgers, not a universal lower bound. GATE279 supplies `O(log N)` writable-space discovery/emission with unspecified polynomial time. The next target is an exact same-indexed-TM routing/accessor algorithm with setup at most `N^(11/10+o(1))` and routing space at most `N^(1/2+o(1))`, including failed candidates, guest input-index probes, cache/replay and joins.

## Reproducibility

- Producer: `experiments/arc/lspv5_245/balanced_routing_referee245.py`
- Independent checker: `experiments/arc/lspv5_245/verify_balanced_routing_referee245.py`
- Raw: `results/raw/arc/2026-10-31_0948_LSPV5_BALANCED_ROUTING_REFEREE245_raw.json`
- Ten matched STAR sources: five SAT, five UNSAT.
- Producer: 366,844 assertion units; independent checker: 2,808 units.
- Ten deliberately corrupted volume records rejected.
- Raw SHA-256: `639df81fade95cf5e173aaf565f854c0720fabc079f711a6c59cc5ebd1d19dac`.

The affine theorem remains a restricted source-independent affine MCSP no-go and cannot be promoted to a SAT routing/runtime theorem. No role, task state or schedule changes.
