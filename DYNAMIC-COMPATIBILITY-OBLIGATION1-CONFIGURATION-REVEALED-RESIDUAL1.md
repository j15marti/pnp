# DYNAMIC-COMPATIBILITY-OBLIGATION1-CONFIGURATION-REVEALED-RESIDUAL1

**Research date:** 27 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, PURE-FUNCTION-COLLAPSE1, MULTI-BLOCK-PRODUCT-RESIDUAL1, CROSSING-HASH-RESIDUAL1  
**Status:** Configuration-revealed residual candidate collapses under free local solves, deterministic whole-run replay and the matching upper bound. Unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT and polynomial-depth global attention leave the residual map-compatibility transport intact on the charged family. The mathematical resource that must still scale on this adversarial family is the physical co-location or transport of incompressible map information across the selected cuts. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction and obstacle analysis only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (27 November 2026): TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming completions), TR26-343 (complexity of unpredictability), TR26-342 (exhaustive search hard for hyperclique/OV in constant depth), TR26-331 (o(N log N) sorting on multitape TM), TR26-339 (deterministic linear-time MST) do not address single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, configuration-revealed residuals, or dynamic post-transport obligations after static equality transport. No relevant crossing-sequence or charged CM SAT lower-bound work located on recent reports.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims with Lean formalizations, VP≠VNP arithmetic results, neural SAT solvers, and graph-attention MaxSAT/SAT models (SGATs, GAT-SAT, Attn-JGNN), but none treat the charged single-tape model, Hartmanis-style equality constructions, free poly-dim attention residual bottlenecks, or configuration-dependent residuals after crossings. Hartmanis 1968 remains the classical quadratic barrier for separated equality; the explicit quadratic limitation of separated equality constructions is classical. Beame–Kornerup cumulative memory supplies general context only.

Repository controls recover PURE-FUNCTION-COLLAPSE1, MULTI-BLOCK-PRODUCT-RESIDUAL1, CROSSING-HASH-RESIDUAL1, matching upper bound (eq. 41) and static ceiling Theorem 2 unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model and attempted construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1: unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT, and polynomial-depth global attention.

Candidate dynamic obligation (configuration-revealed residual):

On the source-authenticated proper 3-CNF permutation family of CHARGED-UNSAT-TRANSPORT1, after the first charged crossing of a selected cut on a diagonal run, extract from the complete configuration C_{b,j}(π) a short encoding of a residual 3-CNF instance whose clauses are a deterministic function of the crossing states and a subset of the map bits not yet transported. The residual obligation is the decision of this secondary 3-SAT instance, claimed to be hard under free resources (since free tools cover only 2-SAT/GE) and revealed only after the physical crossing, forcing an independent post-transport computation under the bounded-reuse lemma.

Free 2-SAT/GE authenticate the original Horn/dual-Horn fragments and extract maps; poly-depth attention embeds configurations but is intended not to pre-materialize the exact residual without the charged crossings.

## 3. Obstacles and collapse

1. **Deterministic whole-run replay and pure-function dependence.** In the deterministic single-tape model the complete configuration C_{b,j}(π) at any crossing is a pure function of the original ordered input blocks L_π, M, R_π and the fixed machine A. Using free random access and attention, a decoder can extract the maps, simulate the entire first transport, recover every configuration, extract the residual 3-CNF, and decide it (or cache its decision bit), all within the single charged pass already accounted for by the matching upper bound solver. No additional independent obligations are forced; the residual is internal to the deterministic computation of the original blocks.

2. **Paid joint preprocessing and free generation.** Every transition used to compute, store, or re-cross for the configuration residual is already included in the whole-run lower bound of the original theorem. Free random access and poly-dimensional/poly-depth attention allow embedding the maps and simulating the configuration transcript in one global pass; verifying exact equality on adversarial (incompressible) maps still embeds the same information-transport requirement in the charged physical layout for each cut, but the total remains O(N²)/O(N³) CM, because the family solver simply extends its single comparison loop across the ordered blocks and caches the residual decision.

3. **Static ceiling and matching upper bound.** Theorem 2 continues to bind for each separated pair and for the whole family: Dh ≤ N²/8 and Dh² ≤ N³/27. The matching upper bound (eq. 41) authenticates the entire family, compares every map pair once, computes any deterministic function of the resulting configurations (including residual 3-CNF decisions via the generic fallback), and caches the result. Soft statistics or attention weights do not certify exact multi-map equality or exact residual decisions without retaining or re-accessing the source data; they represent the comparison differently but do not escape the residual transport.

Consequently the candidate fails the requirement that the obligations remain compulsory after static (or free-local) transport can be completed. The construction collapses under deterministic replay, paid joint preprocessing, free local solves, and the existing matching upper bound. It is a pure function of the original input blocks and the fixed machine, exactly as characterized by PURE-FUNCTION-COLLAPSE1.

## 4. Revised scope: residual compatibility bottleneck under free resources

The free resources resolve every local fragment (2-SAT, GE, Horn/dual-Horn, local embeddings of each pair) but leave the global multi-map equality as a residual compatibility obligation. On the charged permutation family, incompressible maps still require Ω(N²) time and Ω(N³) cumulative memory for exact decision, because the information of each map must be co-located or transported across its physical cut. Attention (even unlimited poly-dimensional and poly-depth) represents the comparison differently—via embeddings, soft weights, multi-hop aggregates or parallel message passing—but does not escape the synchronization/compatibility bottleneck for exact decision on adversarial maps. The static ceiling continues to bind; no superpolynomial amplification is obtained from configuration-revealed residuals that remain pure functions of a single paid comparison of the source blocks.

The mathematical resource that must still scale on this adversarial family is the physical co-location or charged transport of the incompressible map information across the selected cuts. This is a concrete test: attention re-encodes the equality test inside its weights or aggregates but does not eliminate the quadratic time / cubic cumulative memory demand of the charged model.

## 5. Gates

| Gate | Status |
|---|---|
| Free local solvers | Confirmed; resolve each Horn/dual-Horn, 2-SAT, GE fragment and compute pure-function residuals without collapsing the residual transport. |
| Static ceiling | Still binds; configuration-revealed candidates do not exceed Dh ≤ N²/8 or Dh² ≤ N³/27. |
| Matching upper bound | Realized; collapses the candidate via deterministic replay and caching. |
| Configuration residual | Pure function of original blocks and machine; no external independent obligation. |
| Attention representation | Differs from direct comparison but does not escape residual transport. |
| Unrestricted SAT lower bound | Not claimed. |
| P vs NP | OPEN. |

DYNAMIC-COMPATIBILITY-OBLIGATION1 OPEN. P vs NP OPEN.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed. MANUSCRIPT REVIEWED; NO MATERIAL CHANGE to living LaTeX manuscripts.
