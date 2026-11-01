# DELTA-NOT-LYAPUNOV1: Exact canonical signed-spill counterexample

**November 1, 2026, America/Los_Angeles.** Independent falsification related to INTEGRATED-HYPERGRAPH-WRAPPER-ARC1. P versus NP OPEN.

The prior signed-spill inequality is sound for SAT completions, but computed slack delta=e-eta-nu need not decrease as a source-variable partial assignment grows, even along a SAT-extendible path. Thus delta alone cannot be a monotonically decreasing global computation-progress potential.

**Source:** connected valid duplicate-free proper clause-monotone 3-SAT-(2,2) Y6, exactly eight clauses:
positive (1,2,3),(1,4,5),(2,4,6),(3,5,6);
negative (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6).
Each variable appears exactly twice of each sign. Y6 has 20 satisfying assignments.

Take p: x2=0, x3=1, x5=0. The uncovered original one-based clause IDs are 2,3,6; the three binary residual clauses on x1,x4,x6 form an odd triangle. Therefore (f,u,e,eta,nu,delta)=(3,3,3,2,1,0). Here nu=1 is the true maximum odd edge-disjoint cycle packing.

Add x1=0 to obtain q. Uncovered original IDs are 2,3; no odd cycle remains. Therefore (f,u,e,eta,nu,delta)=(2,2,2,1,0,1). Thus delta increases from zero to one.

The full original-source satisfying witness (x1,x2,x3,x4,x5,x6)=(0,0,1,1,0,0) extends both p and q. Every one of the eight original clauses is true. An independent, no-producer-import Python script checked all original clauses, the edge-degree triangle and budget arithmetic, and both nonempty completion sets.

This does not disprove the signed-spill theorem. It falsifies only delta as a guaranteed decreasing path potential. Free-variable count f decreases, but this alone does not bound recursive branching work; paid selection, proof reuse and a stronger resource-aware potential remain necessary. Binary hypergraph XOR conclusions remain representation-specific.

**Previous verified files:** [integrated report](https://github.com/j15marti/pnp/blob/main/research/review/reports/wrapper/2026-11-01_INTEGRATED_HYPERGRAPH_WRAPPER_ARC1.md), [compact Gray and root budget check](https://github.com/j15marti/pnp/blob/main/experiments/review/integrated_sat_wrapper_dag_core_repro.py). The separate full verifier is attached in the conversation and not claimed GitHub-mirrored.

**No automation/task/schedule/root main.tex changes. P versus NP OPEN.**

END_OF_VERIFIED_REVIEW::DELTA_NOT_LYAPUNOV1::P_VS_NP_OPEN
