# DYNAMIC-COMPATIBILITY-OBLIGATION1-PATH-DEPENDENT-COLLAPSE1

**Research date:** 26 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, X01-06 sequential residual collapse  
**Status:** Path-dependent residual candidate collapses under deterministic whole-run replay and free local solves. Free polynomial resources do not escape the residual map-compatibility transport. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN. P vs NP OPEN.  
**Review:** Internal construction and obstacle analysis only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (26 November 2026): TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming completions), TR26-343 (complexity of unpredictability), TR26-342 (exhaustive search hard for hyperclique/OV in constant depth), TR26-331 (o(N log N) sorting on multitape TM) do not address single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, or dynamic post-transport obligations after static equality transport. No relevant crossing-sequence or charged CM SAT lower-bound work located on recent reports.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims, formalizations (anthropics/formal-math, openai/math), VP≠VNP arithmetic results, and neural SAT solvers (GranSAT, SGATs, Attn-JGNN), but none treat the charged single-tape model, Hartmanis-style equality constructions, or free poly-dim attention residual bottlenecks. Hartmanis 1968 remains the classical quadratic barrier for separated equality. Beame–Kornerup cumulative memory supplies general context only (sorting, matrix mult); not used for the specific UNSAT-family theorem.

Repository controls: matching upper bound of CHARGED-UNSAT-TRANSPORT1, static ceiling Theorem 2, prior residual-map and sequential-unlock collapses, and GANN free-resource residual bottleneck recovered unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model and attempted construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1 on any poly-size instance: unlimited polynomial-dimensional attention, unlimited random access (multi-tape equivalent, no local crossing charge), exact Gaussian elimination, exact 2-SAT (Horn/dual-Horn/implication graphs), and polynomial-depth global attention.

Candidate dynamic obligation (path-dependent post-transport unlock):

After free authentication and local solution of the Horn/dual-Horn selectors, left clauses, right clauses and middle chain on the permutation (or map) family of CHARGED-UNSAT-TRANSPORT1, force a residual map ρ that is unlocked only after a charged crossing of a selected cut has occurred. The unlock key is defined as a short hash or affine function of the specific crossing sequence states (or head-position timestamps) observed during the first transport of the source maps π, σ. The claim was that ρ carries independent Ω(log r) incompressible bits whose description depends on the actual execution path, so it is not a deterministic function of the original input blocks alone and must be re-materialized after the crossing, producing additional compulsory crossings under the bounded-reuse lemma.

The free local solvers handle the initial extraction and comparison; the path-dependent unlock was intended to force re-materialization that cannot be cached from a single precomputation of the source blocks.

## 3. Obstacles and collapse

1. **Deterministic whole-run replay.** In the deterministic single-tape model, the entire execution path, including every crossing state and head position, is a deterministic function of the input and the fixed machine. A decoder (or the machine itself) can replay the first transport from the original input blocks, recover the exact crossing sequence, compute the unlock key, generate ρ, and obtain the residual equality bit, all within the same charged (or free-access) pass already accounted for by the matching upper bound solver. No additional independent obligations are forced; the path dependence is internal to the deterministic computation.

2. **Paid joint preprocessing and free generation.** Every transition used to compute, store, or re-cross for the residual is already included in the whole-run lower bound of the original theorem. Free random access and poly-depth attention allow embedding the entire path-derived residual into an aggregate of poly(log r) dimension, but verifying exact equality on adversarial (incompressible) maps still embeds the same information-transport requirement in the charged physical layout. The total remains O(N^{2}) / O(N^{3}) CM when the number of such residuals is polynomial.

3. **Decoder and reuse.** Any decoder recovering the residual from the cached source maps plus a short program for the path-hash rule has description length O(log N). Once the initial pass has performed the work, the obligations are not independent after paid (or free) joint preprocessing; the event-reuse bound is vacuously satisfied. External random sources or interactive oracles would change the model (relativization or randomized), which is outside the stated deterministic single-tape scope and does not yield an unrestricted deterministic lower bound.

Consequently the candidate fails the requirement that the obligations remain compulsory after static (or free-local) transport can be completed. The construction collapses under deterministic replay and the existing matching upper bound.

## 4. Revised scope: residual compatibility bottleneck under free resources

The free resources resolve every local fragment (2-SAT, GE, Horn/dual-Horn, local embeddings) but leave the global map-equality as a residual compatibility obligation. On the charged permutation family, incompressible maps still require Ω(N^{2}) time and Ω(N^{3}) cumulative memory for exact decision, because the information must be co-located or transported across the physical cut. Attention (even unlimited poly-dimensional and poly-depth) represents the comparison differently—via embeddings, soft weights, or aggregate statistics—but does not escape the synchronization/compatibility bottleneck for exact decision on adversarial maps. The static ceiling continues to bind; no superpolynomial amplification is obtained from path-dependent residuals that remain functions of the deterministic execution.

A viable DYNAMIC-COMPATIBILITY-OBLIGATION1 must produce obligations whose information is not jointly recoverable from a single paid or free comparison (including path replay) of the source blocks, or must force re-materialization of data that cannot be generated by deterministic replay of the original input (e.g., data whose description depends on an external source outside the deterministic model). Uniform simulation of arbitrary correct machines remains the load-bearing open premise.

## 5. Gates

| Gate | Status |
|---|---|
| Free local solvers | Confirmed; do not collapse the transport. |
| Static ceiling | Still binds; path-dependent residuals do not exceed it. |
| Matching upper bound | Realized; collapses the candidate via deterministic replay. |
| Path dependence | Internal to deterministic model; no external obligation. |
| Unrestricted SAT lower bound | Not claimed. |
| P vs NP | OPEN. |

DYNAMIC-COMPATIBILITY-OBLIGATION1 OPEN. P vs NP OPEN.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed.
