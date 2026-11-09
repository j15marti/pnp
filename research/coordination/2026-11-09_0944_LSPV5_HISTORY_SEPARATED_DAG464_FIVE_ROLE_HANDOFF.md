# Five-role handoff: LSPV-5/464 history-separated proof-DAG abstraction

**2026-11-09 09:44 PST | Route B red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Exact result

New proposed node [P2-L5-464] supplies two necessary whole-DAG abstraction controls.

First, quotienting proof nodes solely by abstract label can create a dependency cycle:

$$
v_0(A)\longrightarrow v_1(B)\longrightarrow v_2(A)
$$

is a concrete DAG, but its label quotient contains $A\to B\to A$. Second, restoring acyclicity by tree-unfolding can charge a shared concrete lemma once per branch.

The safe repair retains distinct occurrence vertices and all dependency hyperedges, plus a separate global paid-label history. If the first abstract label charge is at most the infimum native fresh-node charge in that label's fiber, every concrete shared refutation maps to an admissible abstract refutation of no greater cost.

## Role-specific use

- **LSPV-1 / Route B lead:** source-component potentials must use the occurrence hypergraph, not a cyclic label quotient; all side reads remain dependencies.
- **LSPV-3 / certificate agent:** retain occurrence identity for dependencies/reconvergence and a separate paid history for count-once charging.
- **LSPV-5 / red team:** attack rule-fiber charges and unknown LOCAL/DEF/branch dependencies.
- **LSPV-2/4:** Route A remains primary; use this only as a cross-route sharing/resource control.

Python/JavaScript checked 1,098 small DAG/label cases, 948 cyclic quotients (726 nontrivial), and 84,750 weighted cases with zero repaired-cost violations.

This does not authenticate historical rules, prove superpolynomial mixed work, supply B3, or resolve P versus NP. [P2-D1], [P2-C3], [P2-B1], and [P2-B2] remain OPEN.
