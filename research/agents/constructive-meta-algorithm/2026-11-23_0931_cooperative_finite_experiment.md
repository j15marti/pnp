# Cooperative same-residual SAT experiment, 2026-11-23 09:31 PST

Status: finite computational evidence, NOT a universal polynomial bound. Linked issue #324.

## Implementation and scope
A local Python 3 prototype ran three configurations on identical explicitly represented CNFs: baseline unit propagation plus 2-SAT SCC and exact branching; independent adds parity-pattern recognition/GF(2) elimination and variable-disjoint component decomposition but does not cross-feed affine forced values; cooperative additionally feeds certified affine singleton deductions back into CNF and repeats the recognizers. Memoization by sorted syntactic CNF is used. The Gaussian extractor recognizes fully represented 2/3-variable parity patterns; it does not claim to discover hidden XOR in arbitrary encodings. The code does not yet implement treewidth, matching, symmetry, proof-producing clause learning, or full cumulative-memory instrumentation.

## Test set and oracle
31 cases: 3-variable 8-clause UNSAT cube and 7-clause SAT neighbor; contradictory XOR; satisfiable XOR; five-variable 12-clause XOR crossfeed; three disjoint UNSAT cubes; three disjoint SAT neighbors; 24 random 3-CNF cases (8, 10, 12 variables, eight cases each), deterministic seed 20261123. Every one of 93 solver results matched independently enumerated Boolean assignments.

## Results (one local execution; wall-clock timings not statistically meaningful)
baseline: 110 branch nodes, 213 recursive calls, aggregate 0.0228 s.
independent: 104 branch nodes, 205 calls, aggregate 0.0320 s.
cooperative: 103 branch nodes, 204 calls, aggregate 0.0310 s.
On XOR-crossfeed: baseline 2 branches/3 calls, independent 2 branches/3 calls, cooperative 1 branch/2 calls with one affine-to-CNF crossfeed. Thus crossfeeding can reduce branching on a concrete instance, but only one case in this suite showed the effect. Overhead outweighs overall gains in this small sample.

## Exact XOR crossfeed instance
Three equations over GF(2):
x1 xor x2 xor x3 = 0
x1 xor x2 xor x4 = 0
x3 xor x4 xor x5 = 0.
Their first two imply x3=x4; the third then forces x5=0. Each equation is encoded as four 3-clauses forbidding the wrong parity, for 12 total clauses. RREF derives x5=0; cooperative propagation reduces the residual before branching. This is a rigorously justified deduction, not a heuristic.

## Interpretation and caveats
The prototype's full Gaussian extraction, graph discovery, cache work, Python object allocation, and measured runtime are included in elapsed time, but peak space and cumulative memory have not been instrumented. The 31 cases are tiny and are not evidence of polynomial worst-case behavior. No universal coverage theorem has been established. The next implementation should add verified separators/treewidth, equivalence certificates, structural backdoor discovery, and a controlled ablation matrix with measured memory and all residual-level transformation costs.

## Reproducibility
Local full script: /mnt/data/pnp_coop/test.py; machine-readable results: /mnt/data/pnp_coop/results.json; console log: /mnt/data/pnp_coop/log.txt. Run: python3 test.py. The local paths are conversation artifacts, not GitHub files; report is committed separately.
