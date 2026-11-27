# DYNAMIC-COMPATIBILITY-OBLIGATION1-CROSSING-HASH-RESIDUAL1

**Research date:** 26 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, PURE-FUNCTION-COLLAPSE1, NESTED-CUT-COLLAPSE1  
**Status:** Crossing-hash residual candidate collapses under free local solves, deterministic whole-run replay and the matching upper bound. Free poly-dimensional attention, random access, exact GE, exact 2-SAT and poly-depth global attention leave the residual map-compatibility transport intact. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction and obstacle analysis only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (26 November 2026): TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming completions), TR26-343 (complexity of unpredictability), TR26-342 (exhaustive search hard for hyperclique/OV in constant depth), TR26-332 (Resolution Is Automatable on Tseitin Formulas) do not address single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, crossing-hash residuals, or dynamic post-transport obligations after static equality transport. No relevant crossing-sequence or charged CM SAT lower-bound work located on recent reports.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims with Lean formalizations (anthropics/formal-math eth/, openai/math), VP≠VNP arithmetic results, and neural SAT solvers, but none treat the charged single-tape model, Hartmanis-style equality constructions, free poly-dim attention residual bottlenecks, or hash-dependent residuals after crossings. Hartmanis 1968 remains the classical quadratic barrier for separated equality; the explicit quadratic limitation of separated equality constructions is classical. Beame–Kornerup cumulative memory supplies general context only; not used for the specific UNSAT-family theorem.

Repository controls: matching upper bound of CHARGED-UNSAT-TRANSPORT1 (eq. 41), static ceiling Theorem 2 (eq. 44), residual transport under free resources, pure-function collapse, nested-cut, adaptive-cut, sequential-unlock and path-dependent collapses recovered unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model and attempted construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1 on any poly-size instance: unlimited polynomial-dimensional attention, unlimited random access (multi-tape equivalent, no local crossing charge), exact Gaussian elimination, exact 2-SAT (Horn/dual-Horn/implication graphs), and polynomial-depth global attention.

Candidate dynamic obligation (crossing-hash residual):

On the source-authenticated proper 3-CNF permutation family of CHARGED-UNSAT-TRANSPORT1, after the first charged crossing of a selected cut on a diagonal run, compute a short collision-resistant hash of the complete crossing sequence CS_b(π) (or of the configuration at a designated crossing). The residual obligation is then an equality test between this hash and a pre-encoded target derived from a second incompressible map σ' that is itself a deterministic function of the original maps, or a verification that the hash matches a value that unlocks a secondary selector whose satisfaction depends on the exact sequence. The claim was that free local solvers can authenticate the Horn/dual-Horn fragments and extract maps, but the hash is only materializable after the physical crossing has occurred, forcing a second independent transport of incompressible information under the bounded-reuse lemma, multiplying the quadratic/cubic demand.

Free 2-SAT/GE handle each local selector and chain; poly-depth attention was intended to be unable to precompute the exact crossing sequence without performing the physical crossings already charged.

## 3. Obstacles and collapse

1. **Deterministic whole-run replay and pure-function dependence.** In the deterministic single-tape model the complete crossing sequence CS_b(π) on any diagonal is a pure function of the original ordered input blocks L_π, M, R_π and the fixed machine A. A decoder (or the machine itself, using free random access and attention to extract the maps) can replay the first transport of the source blocks, recover every crossing sequence, compute the hash, and verify the residual equality, all within the single charged (or free-access) pass already accounted for by the matching upper bound solver. No additional independent obligations are forced; the hash is internal to the deterministic computation of the original blocks.

2. **Paid joint preprocessing and free generation.** Every transition used to compute, store, or re-cross for the hash residual is already included in the whole-run lower bound of the original theorem. Free random access and poly-dimensional/poly-depth attention allow embedding the maps and simulating the crossing transcript in one global pass; verifying exact equality on adversarial (incompressible) maps still embeds the same information-transport requirement in the charged physical layout for each cut, but the total remains O(N²)/O(N³) CM, because the family solver simply extends its single comparison loop across the ordered blocks and caches the hash-derived bit.

3. **Static ceiling and matching upper bound.** Theorem 2 continues to bind for each separated pair and for the whole family: Dh ≤ N²/8 and Dh² ≤ N³/27. The matching upper bound (eq. 41) authenticates the entire family, compares every map pair once, computes any deterministic function of the resulting crossing sequences, and caches the result. Soft statistics or attention weights do not certify exact multi-map equality or exact hash matches without retaining or re-accessing the source data; they represent the comparison differently but do not escape the residual transport.

Consequently the candidate fails the requirement that the obligations remain compulsory after static (or free-local) transport can be completed. The construction collapses under deterministic replay, paid joint preprocessing, free local solves, and the existing matching upper bound. It is a pure function of the original input blocks and the fixed machine, exactly as characterized by PURE-FUNCTION-COLLAPSE1.

## 4. Revised scope: residual compatibility bottleneck under free resources

The free resources resolve every local fragment (2-SAT, GE, Horn/dual-Horn, local embeddings of each pair) but leave the global multi-map equality as a residual compatibility obligation. On the charged permutation family, incompressible maps still require Ω(N²) time and Ω(N³) cumulative memory for exact decision, because the information of each map must be co-located or transported across its physical cut. Attention (even unlimited poly-dimensional and poly-depth) represents the comparison differently—via embeddings, soft weights, multi-hop aggregates or parallel message passing—but does not escape the synchronization/compatibility bottleneck for exact decision on adversarial maps. The static ceiling continues to bind; no superpolynomial amplification is obtained from crossing-hash residuals that remain pure functions of a single paid comparison of the source blocks.

The mathematical resource that must still scale on this adversarial family is the physical co-location or charged transport of the incompressible map information across the selected cuts. This is a concrete test: attention re-encodes the equality test inside its weights or aggregates but does not eliminate the quadratic time / cubic cumulative memory demand of the charged model.

## 5. Gates

| Gate | Status |
|---|---|
| Free local solvers | Confirmed; resolve each Horn/dual-Horn, 2-SAT, GE fragment and compute pure-function hashes without collapsing the residual transport. |
| Static ceiling | Still binds; hash candidates do not exceed Dh ≤ N²/8 or Dh² ≤ N³/27. |
| Matching upper bound | Realized; collapses the candidate via deterministic replay and caching. |
| Crossing hash | Pure function of original blocks and machine; no external independent obligation. |
| Attention representation | Differs from direct comparison but does not escape residual transport. |
| Unrestricted SAT lower bound | Not claimed. |
| P vs NP | OPEN. |

DYNAMIC-COMPATIBILITY-OBLIGATION1 OPEN. P vs NP OPEN.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed.
