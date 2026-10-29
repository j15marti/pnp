# LSPV-1 ARC214 preregistration, 2026-10-28 23:xx Los Angeles
Central missing arrow: uniform, physically charged, answer-preserving moving exact summaries from an arbitrary encoded SAT instance, with a guaranteed polynomial-valued rank and polynomial-size states. Prior ARC212 supplies only a conditional criterion.

Pre-search falsifiable mechanisms:
1. A fully charged exact frontier dynamic program, given a concrete variable order of maximum live frontier w, compiles ANY CNF (and mixed 2-CNF/XOR) to a constant YES/NO child in O(poly(N)*2^{O(w)}), with no answer-class hint. Challenge by constructing adversarial orders and cross-boundary constraints.
2. A purely greedy polynomial-time order discoverer (min-fill or min-frontier) always achieves w=O(log N) on balanced exact-(2,2)-3CNF. Falsifier: explicit signed exact22 connected families with high intrinsic frontier.
3. Eliminating the fresh auxiliaries in the ARC213 2SAT+XOR gadget by local existential projection creates a genuinely smaller closed instance. Falsifier: the projection reproduces the entire original 3-clause, with output encoding no net shrink.
4. Replacing exact frontier relations by two independent feasibility bits for 2SAT and XOR preserves satisfiability. Falsifier: eight signed 3-clauses yield separately feasible pieces but unsatisfiable conjunction.

Search targets: GitHub SAT solver exact variable elimination and bounded-treewidth dynamic programming, mixed XOR-2SAT solvers, OpenAI 2026 Boolean-oracle preprint, primary bucket elimination and kernelization barriers.