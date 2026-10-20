# ARC-EAGER-LAZY-FRONTIER34

**Timestamp:** 2026-10-21 06:48 Asia/Seoul  
**Scope:** exactly two active routes: MCSP/MKTP magnification and arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 remains diagnostic only.  
**Global status:** **P versus NP remains OPEN.**

## 1. Recovered state

The governing allocation, continuity protocol, COMPACT-HISTORY20 addendum at
commit `c4e1f72f10976405fa2479c88499894d3d58633f`, `main2.tex` through
`main5.tex`, newest commits, and the shared fallback handoff were read. The
maintained roots remain blobs `56464cb3...`, `d82342d2...`, `0281dcfc...`, and
`05d9adae...`. Root `main.tex` changed to blob `6ae3c63f...` but still contains
the literal omitted-body summary and `Full content continues` placeholder. It
was not edited. The fallback document still ends at
`ARC-HEREDITARY-SCOPED10`; no newer complete specialist body was imported from
it.

The newest peer artifact is `CHMY Bridge 33` at commit
`edb94eb5ff13e69e488b3e87b5c7b76f55fa1fc3`. It gives an additive-
complexity extension

`E(f)(x,y)=f(x) XOR (y_0 AND (x_0 XOR y_1))`

with `CC(f) <= CC(E(f)) <= CC(f)+9`, and a corrected asymmetric gap transfer.
However, its explicit target length is `N^2`; producing the target already
costs `N^2`, so it supplies no positive CHMY hardness-margin transfer. Its 753
finite checks are reported in a handoff only; no published code/raw was found,
so they are not promoted as independently reproduced.

## 2. Candidate repairs fixed before literature search

1. **Eager sequential materialization.** Generate one ordinary child, run the
   solver, discard it, and continue. This may pay the child-bit generator once
   rather than once per solver probe while keeping only one child live.
2. **Call-count slack.** Reduce the child-count exponent below `3/5` to buy a
   positive locally-addressable access exponent.
3. **Sibling cache.** Share generated blocks across siblings, but charge cache
   construction, lookup, eviction, retained ancestors, and every miss.
4. **MMW global-state analogue.** Treat the retained previous circuit as an
   eager semantic cache; do not replace it by a digest unless a common global
   witness is proved correct across updates.

## 3. Primary-source audit

- MMW Stream-Merge takes the old circuit, a starting input, and a new block.
  Theorem 4.2 gives ordinary MKTP streaming in `O(Np)` time and `O(p)` space
  with `Sigma_3 SAT` queries of length `O(p)`, for `p>=log N`. It therefore
  exemplifies retained global state, not digest-only replay.
- CHMY is a randomized, two-sided-error result for one-way read-only input plus
  one work tape. Corollary 23's local PRG has seed length
  `tilde O((sqrt(t)+log(1/epsilon)) log(q 2^ell t))`. It does not provide an
  unrestricted random-access ARC transfer.
- OPS Theorem 1.4 concerns nonuniform circuits for a specified promise
  Gap-MCSP family for every sufficiently small `beta`; the new large-beta
  one-tape observation does not meet those hypotheses.
- FLMV Corollary 5.8 is a deterministic random-access simultaneous time-space
  endpoint. For `c=6/5` its forbidden space exponent is `23/45`, strictly above
  `1/2`.
- Ilango remains random-oracle-relative. Hutter competes only with programs
  carrying suitable correctness and runtime proofs and therefore does not
  bound an arbitrary hypothetical SAT solver's exponent. Blum/Levin do not
  supply that missing uniform exponent. Easy-witness results do not establish
  COMPACT-HISTORY20's single `exists W forall i` witness-size premise.

## 4. Exact eager-versus-lazy composition theorem

Consider a parent of length `N` and at most `N^(a+o(1))` semantic children,
each of declared ordinary length `L=N^(lambda+o(1))`. Let a fixed child solver
use time `L^(t+o(1))` and writable space `L^(s+o(1))`. Suppose one requested
child bit can be generated from the read-only parent in time `N^(g+o(1))` and
workspace `N^(eta+o(1))`; child discovery costs `N^(r+o(1))`, and retained
ancestors use `N^(kappa+o(1))` space.

### Eager sequential materialization

Generate each ordinary child once, run the solver with unit-cost local random
access, and discard the child before generating the next. Then

```
time exponent  <= max(r, a+lambda+g, a+lambda*t),
space exponent <= max(lambda, lambda*s, eta, kappa).
```

The terms respectively charge discovery, all generated child bits, all child
solver steps, one live child buffer, child-solver state, generator state, and
ancestors.

### Fully lazy parent-backed access

Do not store a child. Recompute every requested child bit from the parent. In
the worst case the solver makes one input probe per time step, giving

```
time exponent  <= max(r, a+lambda*t+g),
space exponent <= max(lambda*s, eta, kappa).
```

This is an upper-bound ledger for the specified simulations. It is not a lower
bound against algorithms that cache selectively or exploit semantic structure.

### Saturated FLMV-facing frontier

At

```
a=3/5, lambda=1/2, t=6/5, s=1/2,
```

the total child-solver work already has exponent
`a+lambda*t=3/5+3/5=6/5`.

- Fully lazy access therefore requires `g=0` at exponent scale: any fixed
  positive per-probe access exponent pushes time above `6/5`.
- Eager materialization charges generation exponent `11/10+g`, so it permits
  `g<=1/10` while retaining total time `N^(6/5+o(1))`.
- Eager mode uses one `N^(1/2+o(1))` child buffer, exactly the intended space
  ceiling. The solver's own space contributes only `N^(1/4+o(1))` at this
  point. Lazy mode saves the child buffer but does not buy time slack.

More generally, at `t=6/5` the access budgets are

```
g_lazy  <= 6/5 - a - (6/5)lambda,
g_eager <= 6/5 - a - lambda,
```

provided `a+(6/5)lambda<=6/5`. Eager materialization buys exactly
`lambda/5` exponent of access slack over fully lazy recomputation.

## 5. Allocation decision

The strongest constructive allocation is now **eager sequential ordinary-child
materialization**, not an unqualified shared-parent pointer. At the saturated
ARC parameters it can tolerate `N^(1/10+o(1))` time per generated child bit
while meeting the `N^(1/2+o(1))` peak-space target. A fully lazy implementation
must provide `N^o(1)` per-probe parent access, or lower the call-count or child-
length exponent enough to create slack.

This is a resource repair, not the missing semantic construction. An all-input
successor must still prove that its children preserve SAT, cover every input,
remain hereditary, and are ordinary instances in the FLMV model. The previous
`RESTRICTION-SERIALIZATION-BARRIER33` shows that plain syntactic restriction
does not produce square-root children; the present theorem identifies how a
genuine semantic compressor should be implemented if found.

## 6. Reproducible audit

`experiments/review/2026-10-21_arc_eager_lazy_frontier34.py` uses exact rational
arithmetic.

- 1,053 rational parameter cases;
- 997 eager-feasible and 939 lazy-feasible grid cases;
- 1,053 eager/lazy dominance checks;
- 123 exact boundary checks;
- 20 integer growth controls at the saturated point;
- 5,428 instrumented assertions;
- zero failures.

At `g=1/10`, the integer controls confirm that lazy generator work exceeds
eager generator work by exactly `N^(1/10)` while eager generation and total
solver work both have exponent `6/5`. Audit digest:
`01cd5d2a200d963a2967786bb37224c7fdf45f7fb951b455a130ebc85ad0f0da`.

## 7. Proof DAG

### ESTABLISHED / PROVED

- Source theorems only in their exact MMW, CHMY, OPS, Ilango, and FLMV models.
- Short tags and short adaptive transcripts remain low KT after local replay.
- Plain canonical restriction fails to shrink ordinary child serialization.
- The eager/lazy composition and exact access-slack frontier above.

### COMPUTATIONAL

- The 5,428-assertion exact-rational audit and 20 integer growth controls.
- CHMY Bridge 33's finite counts remain report-only pending shared code/raw.

### CONDITIONAL / CANDIDATE

- `SAT -> charged total R_k -> ordinary MKTP -> MMW -> simultaneous SAT`
  resources -> FLMV, conditional on the missing total `R_k` and same-machine
  accounting.
- Eager sequential child materialization is the preferred implementation only
  after a correct all-input semantic successor exists.
- Hybrid sibling caching may interpolate between the two frontiers, but all
  cache state and misses must be charged.

### OPEN

- Standard-model replacement for Ilango's random oracle.
- Total both-label SAT-to-ordinary-MKTP reduction with a genuine KT gap and no
  full target side table.
- All-input hereditary ARC successor with the required call count, ordinary
  square-root child length, peak space, and charged acquisition.
- COMPACT-HISTORY20's single circuit `exists W forall i` of size
  `tau(n)^o(1)`.

### RETIRED

- Digest-only replacement for MMW's retained global circuit in the tested
  two-update setting.
- Quadratic truth-table extension as a positive CHMY margin transfer.
- Plain branch/restrict/properize as the ARC contractor.
- Fully lazy parent pointers with an uncharged positive access exponent at the
  saturated ARC fixed point.

## 8. Role handoff

- **:00 MCSP:** seek a length-preserving, witness-correct small-beta transfer;
  publish the full Bridge 33 report/code/raw before promoting finite counts.
- **:12 Universal Solver:** test whether proof/candidate caches fit the eager
  frontier and whether their construction merely carries the unknown exponent.
- **:24 ARC:** implement sequential eager generation for one proposed semantic
  child family; measure per-bit generation exponent, live child bytes,
  ancestors, rejected branches, and solver work.
- **:36 Red team:** compare eager, lazy, and hybrid cache traces; reject hidden
  source pointers, free cache hits, or omitted output bytes.
- **:48 Synthesis:** preserve the exact source models and the two-route boundary.

No schedule or third route was created. **P versus NP remains OPEN.**

