# Exact caching defeats the cut-tree repeated-work demand

21 November 2026, 22:12 PST, America/Los_Angeles. PNP Independent Counterexamples.
**DYNAMIC-CUT-TREE-CACHE-AUDIT1** under DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT:** exponential node count for one fixed published algorithm, quadratic distinct-residual count for its exact-cache modification, and a polynomial authenticated two-label family fast path. **COMPUTATIONAL:** finite execution and encoded round-trip checks. **FALSIFIED/RETIRED:** polynomial total-node growth for the unmodified fixed rule, and treating its repeated nodes as unavoidable work of every correct solver. Discovery did not assert either stronger claim; this resolves its explicitly identified adversarial-family concern. **OPEN:** polynomial worst-case decision on all inputs and unrestricted superpolynomial lower bounds. This is a role-specific reconstruction of pinned peer evidence, internally reviewed only; external independent review is pending. P versus NP remains OPEN.

## Pinned evidence and exact question

The target is Discovery's report and executable at commit **c5018c0ba81f31c58ea5b9c9ec3d00877ebe1ada** [1], based on Construction's canonical shared-selector dihedral encoding at **9d5005e4b727f0e3483a8b6e98b99d57ce4f3383** [2]. Main was recovered at **cad779aec9e7e2e29f78e6f32f117972db1aec8b**. The original executable hash read by this experiment is recorded in raw evidence. Bounds' projected-cut audit at this main revision distinguishes a universal residual-answer representation from one offline decision [3]. The present result addresses algorithm execution, not that representation theorem.

First fix algorithm A_tree: recover and authenticate the canonical source; at every residual evaluate Discovery's switched-submodular admission test and exact cut minimum when admitted; otherwise select the smallest live variable ID, recurse on zero then one, and combine by OR with SAT short-circuiting. Keep empty clauses in the residual energy. No memoization, component decomposition, or early empty-clause exit is added to the published decision_tree function. These details matter.

Fix A_cache by adding only a table keyed by the entire ordered tuple of residual clauses, with literal IDs/signs, order and empty-clause multiplicities preserved. Compare keys for exact equality. A Python dictionary is just the test implementation: hash collisions still require tuple equality, and the proof permits a sequential list implementation. There is no probabilistic semantic merge. Both algorithms use correct exhaustive SAT fallback outside admitted canonical encodings. Noncanonical is UNKNOWN for the shortcut, not UNSAT for the decision procedure.

Quantifiers: for every integer k>=1, on the particular valid encoded input I_k below, A_tree has exactly 4^k-1 residual visits, while A_cache evaluates exactly 3k(k+1)/2 distinct residuals. The solvers are fixed before k. This is not an existential adversarial input tailored after varying the solver.

Four falsifiers:
1. A residual containing an untouched isolated positive ternary clause passes switched-cut admission.
2. Two allegedly identical cached keys differ in an empty-clause multiplicity, variable, sign or ordering.
3. The source does not round-trip through the authentic compiler, or the SAT control is misclassified.
4. The recurrence silently assumes every correct solver must use this pivot order or revisit this tree.

## Full family, both labels, and encoding

Let P_i=(x_(3i+1) OR x_(3i+2) OR x_(3i+3)), for i=0,...,k-1. Let Q_k contain all eight clauses
(s_1 x_(3k+1) OR s_2 x_(3k+2) OR s_3 x_(3k+3)),
where each s_i independently denotes positive or negative occurrence. Order the signs by the Cartesian product of (positive,negative), as in the code. Put

F_k = P_0 AND ... AND P_(k-1) AND AND(Q_k).

Every assignment falsifies exactly one clause of Q_k. Thus F_k is UNSAT and its core violation energy is identically 1. Remove Q_k's final clause to obtain F_k^SAT. Assign the core triple 111 and, for example, all earlier variables 1. This satisfies F_k^SAT. Conversely any satisfying core assignment must be the removed forbidden pattern. These are proper 3-CNFs, with distinct variables per clause and dense names. This is not an all-UNSAT promise solver.

There are d=3k+3 source variables and c=k+8 clauses for F_k, or c=k+7 for its SAT control. An explicit ordered binary-ID source encoding has M=Theta(k log(k+1)) bits. Apply exactly Construction's compiler, with r the smallest odd integer greater than c and at least 3, and L=10c. It yields

n0=d+(10c+1)r+2,   m0=(20c+4)r,
n=n0+m0+3,        m=2m0+4,
w=ceil(log2(n+1)),
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

The physical tape contains unary n and delimiter, gamma(m+1), ordered signed triples, two adjacent n-bit local witnesses and the release ID, in the existing serializer order. We do not replace N by d or by k. Here n,m=Theta(k^2) and N=Theta(k^2 log(k+1)). Each source clause contributes ten explicit reversible instructions. With the same shared source assignment, the final residue is 4E modulo r, where E is the integer number of violated clauses. Since 0<=E<=c<r and r is odd, return to zero is equivalent to E=0. The established adjacent-witness compiler preserves existential SAT equivalence. Therefore I_k is UNSAT, and the seven-core-clause control is SAT. The reduction is explicit polynomial size; a conservative one-tape generator/admission bound O(N^3), O(N) span suffices by rescanning and exact byte regeneration [1,2]. No counting claim or symmetric C/ordered R substitution is involved.

The six new encoded checks give N=121968/167172 for k=1 SAT/UNSAT, 167181/185333 for k=2, and 185342/257931 for k=3. They authenticate the actual layout; they do not establish the all-k proof by extrapolation.

## Exact tree recurrence

The energy of a positive ternary clause is (1-a)(1-b)(1-c). Its three nonzero pair-derivative ranges are nonnegative. Making each nonpositive by coordinate flips requires opposite flip bits on every edge of a triangle, which is impossible. Disjoint scopes cannot cancel these derivatives. Added constants, including violated empty clauses and the eight-clause core, do not change derivatives. An isolated binary positive clause is switchable by flipping one endpoint; a unary positive clause is already admissible. With no untouched ternary positive clause, all remaining energy here is switched-submodular.

While at least two untouched positive triples remain, branching on the first triple generates three internal nodes and four continuations: a=1; a=0,b=1; a=b=0,c=1; and a=b=c=0. Three remove that positive clause; the last leaves one empty clause. The core ensures all continuations return UNSAT, so there is no SAT short circuit. The extra empty clause changes only the energy constant and never future admission. When only one untouched triple remains, branching on its first variable gives two admitted leaves, so there are three nodes. If t(q) denotes the node count with q triples, regardless of the accumulated empty clauses,

t(1)=3,   t(q)=3+4t(q-1),   hence t(k)=4^k-1.

There are exactly 2*4^(k-1) admitted leaves and maximum branching depth 3k-2. Because N=Theta(k^2 log(k+1)), this particular solver's node count exceeds K N^a eventually for every fixed K>0 and a>=1. Each visit needs work, so its runtime is superpolynomial too. This excludes the fixed implementation, not all polynomial SAT algorithms. Reordering to address the core, component decomposition or an empty-clause exit legitimately changes this recurrence.

## Exact cache recurrence and legal bypass

After i earlier positive triples have been fully assigned, e of them may have become empty, for every e=0,...,i. Distinct paths with the same i,e have exactly the same ordered residual, not just the same count or hash. For i<=k-2 there are three residual types for each e: the next triple is intact, reduced to a binary clause, or reduced to a unary clause. Remaining intact triples prevent admission in all three cases. At i=k-1 the three types for each e are instead the intact final triple, its admitted binary child, and the admitted child with that clause removed.

These are all states, they are pairwise distinct by variable scope, remaining literals or empty multiplicity, and every e is reached because all UNSAT branches are explored. Identical states are computed once and reused. Thus

distinct(k)=3 sum_(i=0)^(k-1)(i+1)=3k(k+1)/2.

The internal cache-miss count is 3k(k-1)/2+k. Every such miss creates two calls; other misses and hits create none. Hence calls(k)=1+2[3k(k-1)/2+k]=3k^2-k+1. No variable renaming, isomorphism test, component factoring or altered empty-clause policy is needed.

Cache correctness is induction on the number of live variables: an exact key identifies the identical residual decision function; admitted minima decide it exactly, and Shannon OR combines the two child decisions. It holds for all finite source CNFs covered by the cut evaluator, not only this family. For arbitrary valid target CNFs the authenticated front end either recovers the canonical source or uses exhaustive assignment checking. This defines a globally correct uniform solver; its polynomial bound below is restricted to the demonstrated family.

An even cheaper fixed family fast path is legitimate: after exact canonical extraction, scan for precisely the k disjoint positive triples followed by the ordered seven- or eight-clause terminal core. Accept only exact matches. Return the corresponding proven SAT/UNSAT label; otherwise use the preceding complete solver. This costs polynomial time, does not assume an all-UNSAT input domain, and preserves the constructive SAT assignment. This path is specified by the generator and exact equality test, not by preloaded instance answers. It exposes how weak this family is as a universal lower-bound candidate.

## Full resource ledger on the declared execution

Use the transport model: one finite-alphabet writable tape, one head moving at most one cell per transition, input/work/caches/addresses on the same tape, terminated output at the origin. Peak span charges input from initialization. CM_phys=sum_t S_t in tape-bit units. CM_min is separately the sum of input-charged minimum-description lengths of states; compression does not erase the original input charge.

For the exact-cache execution on I_k, each residual key uses O(k log(k+1)) bits and there are O(k^2) keys. Total table length is O(k^3 log(k+1)), safely O(N^2). DFS buffers, source, counters, pointer/address bits, clause coefficients, parity constraints and cut-network records also fit O(N^2). The depth stack itself is polynomial and may reconstruct residuals instead of retaining duplicates.

For a deliberately conservative tape implementation, store the cache as a list and compare full keys. A lookup/insertion uses at most O(N^4) transitions by nested scans and bit comparisons within O(N^2) span. One invocation of the peer evaluator needs at most O(N^3) sparse-record operations; implement each with scans and arithmetic in O(N^3) transitions in this enlarged span. This gives O(N^6) per cache miss. There are O(N^2) calls/misses. All bounds include failed admissions, reaggregation, network construction, all augmentations, source regeneration, literal copying, address manipulation, retention, cleanup and output. There are no uncharged oracle calls or assumed unit-cost unbounded integers.

| Execution | Time | Peak span | Physical CM | Input-charged descriptive CM |
|---|---:|---:|---:|---:|
| Exact cache, on this family | O(N^8) | O(N^2) | O(N^10) | O(N^9) |
| Exact family recognition plus label/assignment, on the two-label family | O(N^3) | O(N) | O(N^4) | O(N^4) |

These loose upper bounds come from the same respective execution. The descriptive bounds use a fixed program, the N input bits, and self-delimited t; log T=O(log N) on these paths. They are not estimates of the Python wall time, not optimality claims, and not products of unrelated observed maxima. The general noncanonical fallback may take O(2^n N^3) time and O(N) span if implemented by sequential exhaustive assignment checking; that path is not claimed polynomial. A cache on arbitrary canonical sources can also grow exponentially.

For fixed T<=K N^a, the program's generic ceilings remain S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)). The cache construction admits a family cap with a=8 and some fixed K; the specific fast path admits a=3. Our tighter physical-span bounds are consistent with those ceilings. No “forbidden” region has been proved. Count-map circuit size O(N^a log N) is a separate simulation convention, not a decision separation obtained here.

## Compulsory-work correction and controls

The invalid transfer is: A_tree has exponentially many syntactic residual nodes, therefore every correct decision execution must pay that many independent obligations. A_cache is an explicit contrary execution. It pays discovery, lookup and storage while sharing equal residuals. The eight-clause core makes all these residual decisions false, so choosing U_j as those bits on the UNSAT subfamily gives H(U_j|B_j)=0, not a positive entropy demand.

More generally a READY checkpoint may retain the already computed decision Y after paid recognition and solving. With U=Y and B including that retained bit, Pi=empty is conditionally prefix-free, E=empty, h=0, b=1 and rho=1 by convention. The actual decoder reads B and has zero conditional demand. If B excludes it, an actual read of the cached bit must be included; if that one read is used to decode q copies of Y, rho must allow q uses. The inequality
E[T] >= (sum_j H(U_j|B_j)-sum_j E[h_j])/(b rho)
does not justify counting the same cached answer repeatedly at rho=1. No nontrivial universal decoder/locality premise is established by this experiment.

The smallest corrected statement is the exact fixed-rule recurrence together with the exact shared-state recurrence. A lower-bound argument needs a separate compulsory-execution theorem that survives preprocessing, relocation, algebra and cache sharing. It cannot use the uncached recurrence as that premise.

Controls tied to this claim: the seven-clause core gives a positive decision witness; the eight-clause core supplies a cheap scalar constant and forbids hardness promotion; disjoint components and alternate variable naming show why this order-specific tree is not universal; coordinate complements are already allowed by admission; actual key reuse defeats shared-computation multiplicity. No online arrival or forced revisit is imposed. Affine/Tseitin, forced-domain and private-leaf solvers remain legal alternate fast paths, not things all algorithms must simulate. The permutation calibration theorem remains internally reviewed, single-tape and polynomial; it is not amplified here.

DISJ sanity: PASS, no communication lower bound is imported. Simultaneous DTISP: PASS for the two specified executions, with the general lower-bound gate OPEN. Deterministic configuration counting: used only for possible descriptions/replay, never as runtime necessity. Relativization, algebrization and Natural Proofs do not establish an unrestricted step here; no claimed nonrelativizing separation. Counting, proof construction and model enumeration are not compulsory for the Boolean output.

## Reproduction, fresh searches, and next dependency

Run from the repository root:
python experiments/dynamic_redteam_cut_cache_20261121.py

The new [code](../../../experiments/dynamic_redteam_cut_cache_20261121.py) imports the pinned peer implementation. [Raw JSON](../../../results/raw/dynamic_redteam_cut_cache_20261121.json) contains exact node counts for k=1,...,6, cached cases k=10,20,30, four SAT controls, six new encoded round trips and input hashes. At k=6, the uncached algorithm visits 4095 nodes; the cache has 63 distinct evaluations, 103 total calls and 40 hits. At k=30 the cache has 1395 distinct evaluations. These finite tests corroborate the symbolic proof; no transition counts or asymptotic proof were inferred from timings. This is a new fixed-rule/shared-key audit, not a repetition of the previous 256-energy or cache-fiber experiments.

Recovered the current dynamic continuation, transport document, applicable T5 definitions, AGENTS, CODEX and repository research instructions; prior Redteam cache-fiber report/code/raw; current Discovery original report/code/raw; Construction generator; Bounds projected-cut and Accounting first-passage reports; and issue #324. This workspace is a partial source recovery, without .git, so the full-checkout manuscript preflight was not run. No historical TMR manuscript is claimed or edited.

Fresh task-specific literature query: “Bacchus Dalmao Pitassi algorithms complexity SAT model counting component caching 2003 pdf”. Read the authors' camera-ready PDF [4], including its definition of memoized DPLL. It supplies historical support for sharing residual computations and width-dependent counting algorithms. Its counting/time-space results are not imported as unrestricted decision bounds; the exact recurrence here is proved directly.

Fresh connected GitHub code queries used the words “component caching” and SAT separately within org:anthropics, org:openai, org:xai-org, org:google, org:google-research and org:google-deepmind. Only Google's OR-Tools sat_parameters.proto was relevant, pinned at 4782dbd0aa85621c8115cf33de1574a2e6757004 [5]. Its phase-saving documentation cites a lightweight component-caching paper. Phase saving is not the exact residual decision table proved here; no code or theorem was imported. The other scopes produced no applicable hits. Google DeepMind's initial rate-limit error was retried successfully. A web fallback over those six GitHub scopes with SAT, memoization and component caching mostly returned unrelated prompt/cache systems. No relevant result from those pages is asserted. Repository query “4^k” with “cut” returned older strict-C/frontier material, not this shared-choice recurrence; those old results were not substituted.

Official ownership was checked using the verified Anthropic/OpenAI/Google GitHub profiles; x.ai/news/grok-os links xai-org/grok; research.google/resources links Google Research open source; deepmind.google/research/publications/122591 links its google-deepmind code. These checks establish search provenance, not mathematical authority.

**One next dependency: DYNAMIC-SHARED-RESIDUAL-GROWTH1**, owned by Discovery with Bounds, Construction and Redteam review. Analyze a specified uniform solver with exact memoization, component decomposition and early contradiction detection: either prove a polynomial worst-case bound on total paid work for every proper source 3-CNF, or give a legal family forcing superpolynomial work for that precise solver. Accounting should count actual cache misses/accesses with reuse, and Synthesis should retain both the exponential fixed-rule result and its polynomial bypass. An arbitrary-solver lower bound would still need a separate universality bridge. Independent adversarial review is requested before any larger promotion.

Publication reconciliation: main advanced to d33ab73654a83ecdcffc54380ec661220af3fca5 while preparing this report. Its new [local-obligation/safe-merging note](https://github.com/j15marti/pnp/blob/d33ab73654a83ecdcffc54380ec661220af3fca5/research/main/Postprocessing_Local_Obligations_and_Safe_Merging_2026-11-21.md) and directive addition were read. The four owned publication paths and pinned peer code were untouched. Exact residual keys are decision-safe universally; the polynomial distinct-key theorem proved here covers this family alone and does not discharge that note's all-UNSAT-root width premise. No new theorem from the concurrent note is used to prove our recurrence.

1. [Discovery report and code revision](https://github.com/j15marti/pnp/blob/c5018c0ba81f31c58ea5b9c9ec3d00877ebe1ada/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-21_215300_Switched_Violation_Cut.md).
2. [Construction and original evidence](https://github.com/j15marti/pnp/blob/9d5005e4b727f0e3483a8b6e98b99d57ce4f3383/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_213600_Dihedral_Shared_Choice.md).
3. [Bounds projected-cut audit, main snapshot](https://github.com/j15marti/pnp/blob/cad779aec9e7e2e29f78e6f32f117972db1aec8b/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_220100_Projected_Cut_Decoder.md).
4. Bacchus, Dalmao and Pitassi. Algorithms and Complexity Results for #SAT and Bayesian Inference, FOCS 2003, author camera-ready PDF hosted under [BDPFOCS2004.pdf](https://www.cs.toronto.edu/~fbacchus/Papers/BDPFOCS2004.pdf). Bibliographic year and filename differ; consulted version identified by this URL.
5. [Google OR-Tools phase-saving documentation](https://github.com/google/or-tools/blob/4782dbd0aa85621c8115cf33de1574a2e6757004/ortools/sat/sat_parameters.proto).
