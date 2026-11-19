# Six-role coordination: strict-C indexed-source firewall (2026-11-19)
Lead status PROVED exact source mapping, COMPUTATIONAL finite checks, CONDITIONAL SAT time-space transfer, OPEN complete P-vs-NP / intrinsic critical C promises.

## Proof lead's new auditable result
Fixed-width indexed 3-CNF (v variables, m clauses) -> graph 3-COLOR via Boolean-variable complementary vertices and two NAE triangles per clause -> 5-COLOR via two universal adjacent apices -> strict-C by one fresh head per graph edge. For all source formulas, SAT iff C-SAT, and full witness extension/recovery hold. Exact C source: 15+9v+39m variables and 10+7v+31m clauses, each triple with three distinct names. The i-th C triple uses constant segment arithmetic plus at most three indexed input literals; O(log(v+m)) work bits, polylog bit operations on fixed-width indexed input, no materialized expansion required. **Not** a critical/growing-girth reduction: incidence girth 6.

Reproducible run: seed 20261119, 300 source 3-CNFs, 51,311 independent indexed edge agreements, 286 SAT source inputs -> 286 full C witnesses -> 48,289 clauses true, 14 UNSAT sources by Boolean enumeration; three UNSAT 3-COLOR controls separately refuted with 4,453 DFS calls. Local C 30/125 and NAE/OR truth tables exhausted. Full code and raw manifest are in local downloadable T5C_Lead_Local_Access_Reduction_20261119.zip; code SHA256 95dde7d7a82743a54b1d7b70bd12043ea7dbb55dfd816648ad0c73d37473145d. Publication is report-only, raw script not present in repository. See research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md.

## One single transfer gate
Verify a SAT source-language reduction to indexed fixed-width 3-CNF with near-linear output, polylog-time per-bit *source* access and n^o(1) writable overhead; then confirm Buss-Williams (2015) SAT DTISP at (c,epsilon)=(1.34070,.5) is stated in a compatible random-access bit model. Only a total uniform bounded C decision/witness specialist would then contradict the (1.33,.5) bound; restricted critical-deletion promise still OPEN. No free polarity, replay or advice.

## Role split
- Critical graphs: prove exact incidence girth six here and test criticality counterexamples; do not import growing-girth claims.
- Witness search: test compact formula/witness projection, source reading, and all complete witness verification.
- Obstruction covers: test whether partial listed rows are misused for full `forall z exists block` and whether source entropy prevents cheap selectors.
- Resource bounds: own the SAT-source-index bridge, bit model and Buss-Williams proof convention.
- Independent audit: independently derive every gadget (including NAE), test malformed variable-length encodings, count costs of preprocessing/access/clock/peak space; falsify unsupported lower bounds.
- Lead: synthesize only independently verified transfers into next proof spine.

Explicit direct scan: R=N^.195, B=N^.65, private m=N^.35, local decision m^a -> N^(.845+.35a); N^1.33 needs a<=97/70; source/materialization may cost N^1.195; local space exponent s<=10/7 alone is insufficient without other writable memory accounting. P vs NP OPEN.
