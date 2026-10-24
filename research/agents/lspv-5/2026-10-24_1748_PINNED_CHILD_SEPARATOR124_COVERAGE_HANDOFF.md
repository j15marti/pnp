# LSPV-5 PINNED-CHILD-SEPARATOR124 — additive audit handoff

24 October 2026, 17:48 Asia/Seoul. **P versus NP remains OPEN.**

## Exact new result

For the MINIMAL-UNSAT-PROJECTION20 pair in the clause ordering used by
CYCLIC-VIRTUAL-SELECTOR82, the unique changed clause has zero-based index
`d=M-4`.  Add ordinary proper-3CNF unit gadgets pinning
`x_m=1, a_m=0, b_m=0` to every cyclic K-clause child.  Then

`j*=floor((M-4)/K)`

is the first cyclic index whose complete child encodings can differ.  All
earlier pinned children are byte-identical.  At `j*`, the F child is UNSAT
because its changed clause is falsified, while the G child is SAT by the
global G assignment.  The child adds 12 clauses and 6 variables, so its
ordinary bit length remains `N^(1/2+o(1))`.

This is **PROVED/EXACT restricted**.  A controller may jump directly to `j*`;
after canonical-family recognition, reading the single changed source field
is cheaper still.  Therefore the result defeats the pair as a universal
counterexample to *pinned* gluing, but supplies no acquisition lower bound.

## Rejection ledger

- Pure strict-deletion labels distinguish the pair: **FALSIFIED/RETIRED**;
  every such child is SAT on both labels.
- One fixed pinned child decides arbitrary parents: **FALSIFIED/RETIRED**.
  A SAT parent can have an incompatible UNSAT pinned child; an UNSAT parent
  can have a SAT selected child.
- Distinct cyclic index windows imply distinct ordinary child contents:
  **FALSIFIED/RETIRED**, accepting Role-4 PERIODIC-CHILD-COLLISION83's
  correction.
- All-input favorable ARC successor: **OPEN**.

## Reproducibility

The standard-library audit covers `M=16,32,64,128,256,1024,4096`, every
unpinned child, every pinned prefix through `j*`, both unrestricted promise
escapes, and SAT/UNSAT controls for canonical direct field, Horn, SCC 2-SAT,
affine Gaussian and DPLL fallback.  It completed 7,375 assertion-accounted
checks with zero failures.  Canonical payload SHA-256:
`e3c6101c9c9a5a034d1e3c485b0316179acf20db92b9ad9d3c9c7ec4535a2eed`.

Artifacts:

- `research/agents/lspv-5/2026-10-24_1748_LSPV-5_PINNED_CHILD_SEPARATOR124.tex`
- `research/agents/lspv-5/2026-10-24_1748_PINNED_CHILD_SEPARATOR124_audit.py`
- `research/agents/lspv-5/2026-10-24_1748_PINNED_CHILD_SEPARATOR124_results.json`

## Coverage increment and next target

At repository head `d6685274dc85dd00633e3d52f55082afbc825799`, full reads included governance,
skill/protocol, root `main.tex`, `main13.tex`, all task files, newest MAIN108,
MINIMAL-UNSAT-PROJECTION20, virtual-child handoffs, latest Roles 1--4 reports,
and Role-4's new PERIODIC-CHILD-COLLISION83.  The inherited 3,532-file audit
was not repeated; broad Drive pagination and the original full
HEREDITARY-SCOPED10 executable remain unread/unavailable.

Next: apply coherent shared-boundary pins to the periodic opposite-label
same-count pair, then account for two recursive levels, compatibility, source
queries, caches, failed trials and same-machine peak bits.  The missing theorem
is still a total uniform all-input parent equivalence with a favorable joint
resource pair.
