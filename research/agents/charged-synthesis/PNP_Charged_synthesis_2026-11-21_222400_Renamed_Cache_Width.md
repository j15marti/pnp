# Renaming defeats a general bound for exact cut-cache residuals

21 November 2026, 22:24 PST. PNP Charged Proof Synthesis.
**DYNAMIC-RENAMED-CACHE-WIDTH1. PROVED/EXACT** for the fixed algorithm below; **COMPUTATIONAL** finite checks. External independent review pending. This run integrates five peer reports without independently certifying every inherited theorem. P versus NP OPEN.

## Target, quantifiers and result

Fix the uniform algorithm A_cache from Redteam's 22:12 report: authenticate the canonical dihedral image, recover its source, try Discovery's switched-submodular cut test, otherwise branch on the smallest live ID, zero first; cache by the exact ordered residual tuple. No component decomposition, variable canonicalization or extra contradiction detector is included. On failed canonical authentication use a correct exhaustive fallback. UNKNOWN from admission is not UNSAT.

For every k>=1 there is a proper 3-CNF F_k on d=3k+3 variables and c=k+8 clauses whose authenticated image I_k has N=Theta(k² log(k+1)), on which A_cache makes exactly **2^(k+1)-1 distinct residual evaluations, with zero cache hits**. Thus for every fixed K>0,a>=1, its runtime on this sequence eventually exceeds K N^a. This is a counterexample to polynomial growth for this fixed solver, not an arbitrary-solver lower bound.

Three falsifiers: a residual with an untouched positive triple admits a cut; two allegedly distinct keys are identical including IDs and empty clauses; or clause/component processing can be changed while still claiming the exact fixed-algorithm recurrence. The third is a legitimate escape and limits the conclusion.

## Explicit family and proof

For i=1,...,k put P_i=(x_i OR x_(k+i) OR x_(2k+i)). Append Q, all eight signed clauses on x_(3k+1),x_(3k+2),x_(3k+3), in lexicographic sign order positive then negative. F_k is the conjunction. Every assignment violates exactly one clause of Q, so F_k is UNSAT. Removing the final, all-negative clause of Q yields a SAT control, witnessed by all variables true.

This is precisely a variable renaming of Redteam's disjoint-positive-triples family. Its former IDs (3i-2,3i-1,3i) are replaced by (i,k+i,2k+i). The terminal core IDs stay fixed. Formula semantics, incidence graph, number of variables and clauses, and total encoded length are preserved. The fixed smallest-ID rule changes its actual processing order.

After assigning x_1,...,x_j for 0<=j<=k, each processed clause is either absent (assigned bit 1) or the binary clause (x_(k+i) OR x_(2k+i)) (bit 0). Each unprocessed clause remains ternary. Different bit vectors yield different exact keys: their retained binary-clause index sets differ. There are exactly 2^j states at depth j, all UNSAT, with no empty clause or unit clause.

For j<k an untouched positive ternary clause has violation polynomial (1-u)(1-v)(1-w). Its three pair derivatives require opposite coordinate-flip bits on every triangle edge to become submodular, an impossibility. Other clauses use disjoint coordinates; the core energy is constant 1. They cannot cancel these derivatives. Therefore every such state rejects admission.

At depth k, only disjoint binary positive clauses and constant 1 remain. Flip one endpoint of each binary clause. The energy is submodular and has minimum 1, so every leaf is admitted UNSAT. There is no SAT short circuit. States at different depths are distinct because the untouched ternary scopes differ. Consequently the full binary tree to depth k contains
sum_(j=0)^k 2^j = 2^(k+1)-1
different keys. Caching saves nothing on this execution. The smallest case is k=1, three evaluations; the first clear growth comparison with the old quadratic cache formula depends on k, and no small finite threshold proves the asymptotic claim.

This also refutes the hypothesis that the raw residual identity key has polynomial width on every UNSAT root in the new safe-merging theorem. Its collisions are perfectly sound, and acquiring a key is cheap; its range is the failed premise. At depth k there are 2^k keys. Even grouping by encoded length does not repair this: the binomial(k,floor(k/2)) residuals retaining exactly floor(k/2) binary clauses have the same length under a fixed-ID-width residual encoding. This binomial is at least 2^k/(k+1).

## Original encoding and paid controls

Use Construction's exact source encoding: gamma(d+1), gamma(c+1), then signed triples with ceil(log2(d+1))-bit IDs. Its length is M=Theta(k log(k+1)). Let r be the least odd integer >c and >=3, L=10c,
n0=d+(10c+1)r+2, m0=(20c+4)r,
n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)).
The target length remains
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.
It includes unary variable declaration, gamma clause count, every signed literal, both n-bit local witnesses, and release ID. Hence N=Theta(k² log(k+1)). The endpoint is 4 times the number of violated clauses modulo odd r>c; existentially returning to zero is exactly source SAT. The adjacent-witness compiler preserves this decision equivalence. No strict C, ordered R, or exact-counting conclusion is substituted.

A legal competing solver detects source incidence components, solves the eight-clause three-variable component by eight assignments, and returns UNSAT immediately. On the seven-clause control every positive component and the terminal component is satisfiable, hence their conjunction is SAT. Recognize the exact family and use correct fallback elsewhere if a fully specified globally correct shortcut is desired. Authentication and component discovery are paid. This preserves the useful polynomial bypass and demonstrates why the fixed-order counterexample supplies no general hardness.

Under the existing conservative canonical decoder bound, exact regeneration and admission take O(N³) time and O(N) span on one finite-alphabet writable tape. A family recognizer checks all source rows and the fixed core, using scans and O(log N)-bit counters. Combined T=O(N³), S=O(N), CM_phys=O(N⁴); separately CM_min=O(N⁴) by input-plus-time replay. Both labels are handled, and no answer is provided free.

For A_cache itself, let B=2^(k+1)-1. It stores at most B residuals, each O(N) bits, including clause framing and IDs. A conservative sequential implementation uses S=O(BN). Comparing each new key against the retained list and running the sparse cut evaluator can be bounded by T=O(B³ N^6), allowing full-span scans for every record operation. CM_phys<=O(B^4 N^7) on that same execution. Separately replay from input and time gives CM_min<=O(B³ N^7), since log T=O(k+log N)=O(N). These are loose constructive upper envelopes, not measured Python costs. The exact necessary lower bound for this fixed evaluator is T>=B. Parsing, failed cut attempts, copies, actual addresses, table lookup, retained caches, arithmetic, recomputation and output are included. No claim of a sharp CM lower bound follows from counting keys.

For arbitrary proposed T<=K N^a, the unchanged generic ceilings are S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)). Only the fixed A_cache is excluded for every fixed exponent by the exponential visit theorem. The polynomial competing solver remains compatible. Count-map circuit size O(N^a log N) belongs to a separate counting simulation.

## Integration and dependency status

All five reports below are pinned to the recovery snapshot 938eba97b5c90d34ed591ecd8b66b114d6d6df62; the source revision links resolve their original evidence. Their internal-review/pending-review statuses remain unchanged.

| Role/source | Established scoped advance | First missing or rejected implication |
|---|---|---|
| [Construction](https://github.com/j15marti/pnp/blob/938eba97b5c90d34ed591ecd8b66b114d6d6df62/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_213600_Dihedral_Shared_Choice.md) | Shared-selector proper-3-CNF reduction, both-label equivalence, exact M,N | Completeness does not force intermediate trajectory decoding |
| [Accounting](https://github.com/j15marti/pnp/blob/938eba97b5c90d34ed591ecd8b66b114d6d6df62/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-21_214300_Star_First_Passage.md) | Star first-passage decoder, b=1,h=0,rho=1 per checkpoint; prior reads can prepay it | Repeated overlapping suffix charges or renewed post-cache demand |
| [Discovery](https://github.com/j15marti/pnp/blob/938eba97b5c90d34ed591ecd8b66b114d6d6df62/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-21_215300_Switched_Violation_Cut.md) | Uniform switched-energy minimum-cut subclass, O(N^5) time/O(N) span/O(N^6) CM | Universal cut admission or general polynomial branching |
| [Bounds](https://github.com/j15marti/pnp/blob/938eba97b5c90d34ed591ecd8b66b114d6d6df62/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_220100_Projected_Cut_Decoder.md) | Coordinate projections of minimum cuts must be lattices; offline decision need not answer residual queries | Transfer from that representation obstruction to arbitrary scalar decision |
| [Redteam](https://github.com/j15marti/pnp/blob/938eba97b5c90d34ed591ecd8b66b114d6d6df62/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_221200_Cut_Tree_Cache_Audit.md) | Original variable order: 4^k-1 tree nodes, 3k(k+1)/2 cached evaluations | Extrapolating that family/order's cache bound to all inputs |
| Present synthesis | Renamed order: 2^(k+1)-1 cache misses, no hits | Arbitrary adaptive decomposition remains outside the fixed-rule result |

The strongest constructive advance retained is Discovery's authenticated polynomial subclass, not a general SAT algorithm. Redteam's cache improvement is real and order-sensitive. This synthesis falsifies an unproved generalization, not the peer's carefully scoped theorem.

Dependency structure: canonical reduction -> paid selector/energy acquisition -> either admitted exact cut or branch/restrict -> paid sound merging -> bounded actual frontier -> polynomial decision. Sound exact merging holds; a general polynomial frontier bound fails for identity keys and this fixed order. In the alternative lower-bound chain, reachable post-cache opposite-label configurations -> actual decoder/events -> capacities/reuse -> disjoint phases -> fixed-cap excess still has its universal recurrence edge OPEN.

The [safe-merging continuation](https://github.com/j15marti/pnp/blob/938eba97b5c90d34ed591ecd8b66b114d6d6df62/research/main/Postprocessing_Local_Obligations_and_Safe_Merging_2026-11-21.md) remains CONDITIONAL as a P=NP implication: polynomial acquisition plus decision-safe collisions and small UNSAT width suffice, but no all-input constructor satisfying them is supplied. Our counterexample does not refute existence of a better key.

The transport calibration retains internally reviewed single-tape Omega(N²) time and Omega(N³) CM with matching polynomial upper bounds. Static-method ceilings N²/8 and N³/27 remain. For a fixed polynomial cap, its time and descriptive CM exclude only a<2, its physical CM alone a<3/2. These are different resources, not multiplicative demands.

For entropy accounting, require actual U_j,B_j,Pi_j,E_j and exact decoding before using
sum H(U_j|B_j)-sum E[h_j] <= b rho E[T].
This run posits no fresh universal decoder. The fixed family is all UNSAT on the negative side, so residual decision bits have zero entropy there. A paid answer cache makes U=answer known in B, Pi empty prefix-free, E empty, h=0, b=rho=1 sufficient for zero demand. Both-label correctness is provided by the explicit solver and fallback, not by that one-label distribution.

## Evidence, searches and limits

New code: experiments/dynamic_synthesis_identity_width_20261121.py. Raw: results/raw/dynamic_synthesis_identity_width_20261121.json. Run python on that script from the repository root. It imports the original Redteam memoized evaluator and Discovery cut routine at the pinned recovery revision. Standard Python, deterministic k=1,...,10. It checks all exact frontier keys, equal-length binomial counts, preserved contradictory cores, positive witnesses, dimension arithmetic, and the actual imported evaluator's cache statistics. k=10 gives 2047 calls, 2047 distinct keys and zero hits; the depth-10 frontier has 1024 members, including 252 of one length. These are COMPUTATIONAL checks; the proof above establishes all-k growth. N is calculated from the established compiler formula, not a new serialized round-trip claim. Existing peer raw and code were inspected; their prior experiments were not rerun.

Fresh literature query “Mahaney theorem sparse co sparse pruning SAT Grochow 2016” found [ECCC TR16-162](https://eccc.weizmann.ac.il/report/2016/162/), dated 18 October 2016. The original PDF fetch returned 502, and the arXiv HTML endpoint was unavailable. The primary abstract was accessible; it supplies only sparsity context here. No inaccessible theorem is imported. The exact counterexample and frontier argument are proved directly.

Fresh official-repository web searches used “SAT residual caching” for paired scopes github.com/anthropics and github.com/openai, github.com/xai-org and github.com/google-research, then “SAT component caching” for github.com/google and github.com/google-deepmind. Retrieved prompt-cache issues and Google Research cache-replacement material do not establish semantic SAT merging or a width bound. No relevant new implementation or theorem was imported, and no external commit is claimed inspected. Ownership checks used verified corporate GitHub profiles for Anthropic/OpenAI, x.ai/news/grok-os for xai-org, opensource.google/documentation/reference/github/where for Google, research.google/resources and deepmind.google/research/publications/122591 for Research/DeepMind. Search coverage is bounded, not a claim of global absence. Prior logs identify the already inspected OR-Tools phase-saving lead; that distinct notion was not re-reviewed deeply.

Current instructions, six handoffs, transport model/encoding/ceiling, applicable T5 definitions, latest own report and relevant peer original evidence were recovered through connected reads. Issue324 was read through Redteam's current publication. No full checkout/preflight or manuscript compilation was run. No TMR ownership is assumed. No peer file, schedule, identity or enabled state is changed.

Four scientific gates: DISJ/equality sanity PASS, since no universal demand is inferred; simultaneous DTISP PASS within each separately declared execution; deterministic configurations are not used to infer runtime; unrestricted relativization/barrier bypass NOT CLAIMED. Affine/Tseitin, complement, forced-domain, private-leaf and shared computation remain legal shortcuts. In particular component decomposition defeats this easy family and must be retained.

**One next dependency: DYNAMIC-COMPONENT-SAFE-KEY1, owner Discovery with Construction.** Specify a uniform component-aware key/evaluator, including exact authentication and every discovery/access cost, then bound its actual UNSAT frontier or produce a counterexample to that precise algorithm. Bounds should state the required global or contextual width quantifiers; Redteam should test renaming and connected variants; Accounting should charge actual cache accesses and separately prove any renewed opponent events; Synthesis should keep the all-input width and all-solver recurrence gates OPEN. Independent adversarial review of this renamed-order proof and ledger is requested before promotion.
