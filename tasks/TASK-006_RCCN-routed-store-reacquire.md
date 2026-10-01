# TASK-006 — RCCN routed store/reacquire theorem

**Status:** OPEN.

Source component:
`research/explorations/random-challenge/2026-10-01_RCCN1_ROUTED-CAUSAL-COMPUTATION-NETWORK.md`

## Proved guards

- A fixed deterministic routed network flattens to one DTM.
- An NDTM can run that DTM verbatim.
- Cycles do not recreate discarded information.
- In a no-reacquisition delayed-coordinate model, total persistent state obeys `s >= K-r`.
- If `s < K-r`, some post-cut X-dependent reacquisition is necessary.
- Necessity of reacquisition is not a lower bound on its cost.

## Primary target

Find an explicit dependency family D and exact machine model for which every correct routed implementation satisfies a nontrivial inequality of the form

`S_persistent + C_communication + C_reread + C_recompute + C_sequential >= L(D)`

and then test whether the theorem survives arbitrary implementation changes rather than only one chosen modular decomposition.

## Mandatory attacks

- flatten to one DTM;
- unit-cost static reread;
- recomputation;
- memoization/pointer jumping;
- compressed summaries;
- alternate routing decompositions;
- semantic SAT oracle;
- affine/Tseitin, Horn, 2-SAT, bounded treewidth;
- wrappers DEAD/COPY/DELAY/INTERP/RECOMP;
- relativization/algebrization.

## Success criterion

A result becomes relevant to the P-vs-NP spine only if it is paired with a proved model-preserving compiler from arbitrary static SAT computation to the routed/dependency model. Restricted pebbling or branching-program lower bounds alone are not enough.
