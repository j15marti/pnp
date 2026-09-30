# TASK-003 — Primitive-trace battery laboratory

## Objective

Test whether any independently defined source/computation potential survives actual primitive execution traces.

## Core principle

A high-level shortcut K is expanded:

`C_0^K -> C_1^K -> ... -> C_l^K`.

Success and failure are both charged by their actual primitive operations.

For a candidate potential Phi, test:

`Phi(C_t) - Phi(C_{t+1}) <= L * cost_t`.

## Mandatory no-go tests

1. **Circular potential:** detect or reject definitions equivalent to remaining shortest runtime.
2. **Optional shortcut:** show that a solver may skip speculative tests and run a fallback.
3. **Gaussian control:** affine/Tseitin must permit polynomial discharge through explicit elimination.
4. **Treewidth control:** a valid compact DP summary must not be charged once per original incidence.
5. **Wrapper controls:** DEAD/COPY/DELAY/INTERP/RECOMP.
6. **Model simulation:** distinguish one-tape locality results from unrestricted RAM/TM claims.
7. **Oracle seam:** record exactly which microtrace disappears under oracle replacement.
8. **Algebraic oracle:** test whether low-degree/algebraic access similarly bypasses the proposed accounting.

## Starter implementation

Use `pnp_lab.trace.TraceStep` for exact finite traces.

Next, implement at least:
- a primitive Gaussian-elimination trace;
- a small 2-SAT SCC trace;
- a bounded-treewidth DP trace;
- one synthetic failed-shortcut/fallback trace.

## Success criterion

A useful potential must be fixed independently of unknown future runtime and must stay cheap on all easy controls while exhibiting a rigorously forced large drop on the target architecture.

Until that theorem exists, status is `CANDIDATE`.
