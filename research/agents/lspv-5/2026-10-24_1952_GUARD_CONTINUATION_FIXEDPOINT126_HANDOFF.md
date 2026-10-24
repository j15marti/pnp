# LSPV-5 GUARD-CONTINUATION-FIXEDPOINT126 handoff

Status: **PROVED/EXACT** for the guard transform; **COMPUTATIONAL** finite audit; ARC all-input edge **OPEN**; P versus NP **OPEN**.

## Exact recovered link / rejection

For a proper 3CNF `F`, replace each clause `(l1∨l2∨l3)` by
`(¬x∨l1∨a) ∧ (¬a∨l2∨l3)` with a shared fresh guard `x` and clause-local `a`.
After `d` fresh iterations, the feasible relation on guards is all of
`{0,1}^d`, except that the all-one word is absent exactly when `F` is UNSAT.
The guarded root is always SAT; exact membership at the all-one corner is
the original SAT bit.

Pinning all `d` guards to one with proper four-clause unit gadgets gives an
ordinary proper 3CNF equivalent to `F`, with

- `2^d m + 4d` clauses;
- `n + (2^d-1)m + 3d` variables.

For each fixed `d`, this child has encoded length `N_parent^(1+o(1))`, so
the continuation exponent is `lambda=1`, not `1/2`. A one-call transport
has `t' <= max(r,t)` and yields no strict contraction. Full boundary
materialization still includes this one full-size corner.

## Adaptive/resource consequence

The parent is always SAT, so a uniform source-aware decider may select the
outer guard `0` witness and never acquire the exact boundary table. Exact
boundary acquisition is a stronger compilation task than one-bit SAT
decision. Count primitive bit work, source/workspace traffic, unchanged
writes, control/addressing, switching, generated records, actual state
flips, peak live bits, bit-time and representation/program size separately.

## Peer reconciliation

- Role 3's depth-one theorem is accepted; arbitrary fixed depth reaches a
  continuation fixed point, not a power shrink.
- Role 1's anonymous local-depth barrier and Role 5's named-profile identity
  meet here: dropping names loses the hard corner, retaining names preserves
  the source compatibility.
- Role 4's typed-oracle result remains restricted; stronger partial queries
  can escape.
- Role 2's SCC-plus-one-parity result is a constructive polynomial control,
  not an ARC edge.

## Reproducibility

`experiments/guard_continuation_fixedpoint126.py` checked 325 bases,
including all 255 nonempty signed-clause subsets on three variables, six
affine/Horn/padded-2SAT SAT/UNSAT controls, and 64 seeded random formulas.
It performed 11,198 assertion-accounted semantic checks with zero failures.
Script SHA-256:
`2c1c1f1c61926cccfbf8ad6755f7454437919df87b30c6d93f3ed2ad097e0cc7`.

## Exact remaining obligation

Supply an all-input, jointly charged achievable-pair route into a verified
FLMV forbidden box. A boundary proposal must remove the full-size all-one
continuation without deciding the source first or hiding compatibility in
an oracle. Next artifact: original HEREDITARY-SCOPED10 proof/executable,
instantiated on this family with every ordinary child bit and reconstruction
step charged.
