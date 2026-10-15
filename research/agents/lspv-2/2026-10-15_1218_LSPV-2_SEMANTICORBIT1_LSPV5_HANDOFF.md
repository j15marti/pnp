LSPV-5 handoff: SEMANTICORBIT1, 2026-10-15 12:18 KST.

PROVED/EXACT within the explicitly specified rational LP/Farkas source model, independent review pending: A variable permutation g that carries a nonnegative rational whole-source implication certificate for every permuted original row preserves the full LP polyhedron, not just a matched residual. Its action on branching contexts is therefore globally sound. This extends GUARDORIGIN1 / KNAPSACKMERGE1's literal automorphism requirement, without allowing a free unverified selector.

Concrete family: odd knapsack 2 sum x_i = n, with n additional primitive, individually weighted and box-implied rows x_i+(i+1) sum_{j != i} x_j >= 0. Its only literal source automorphism is identity, but its full LP relaxation is S_n symmetric. Pure coordinate LP-conflict trees need exactly 2 binom(2k+1,k) leaves; a Farkas-certified semantic-orbit DAG needs (k+1)(k+3) nodes and O(n^4 log n) explicit proof bits. The same source has a five-line ordinary syntactic CP refutation. No general CP or SAT lower bound results.

Smallest obstruction to a stronger rule: Q={0<=x,y<=1; 2x+2y>=1; x+2y>=1} has Boolean models 01,10,11 and Boolean swap symmetry, but LP point (0,1/2) maps to infeasible (1/2,0). An LP implication certificate cannot recognize all integer symmetries. No universal short-certificate claim.

Seven bounded exact test batches checked 28,344 assertions with no final discrepancies. Full local LaTeX, independent Python scripts and raw JSON are preserved. Published report is research/agents/lspv-2/2026-10-15_1218_LSPV-2_SEMANTICORBIT1.tex.

The complete RS5 hypothesis (H) remains CONDITIONAL, including actual-dimension normalized spread, saved-strip same-row lifting and selector compiler. Arbitrary fixed-language polynomial decider -> uniformly polynomial ordinary binary semantic CP proof generator remains OPEN separately. The next targeted test is the original FHL clique-versus-colouring family, with exact LP source and coefficient/bit costs.
