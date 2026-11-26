# X01-06 | Sequential unlocked residuals after free local solves: dynamic obligation collapse

**Research date:** 26 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1  
**Status:** Candidate sequential residual construction collapses under paid (or free) joint precomputation. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN. P vs NP OPEN.  
**Review:** Internal construction and obstacle analysis; no unrestricted superpolynomial claim. Independent review pending.

## 1. Literature and repository search

Fresh ECCC inspection (26 November 2026): TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming), TR26-342 (exhaustive search hard for hyperclique/OV in constant depth), TR26-343 (complexity of unpredictability) do not address single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, or dynamic post-transport obligations. No relevant crossing-sequence or charged CM SAT lower-bound work located.

Organization-scoped searches: Anthropic formal-math (VP≠VNP arithmetic, ETH-refuting 2^{o(n)} 3-SAT formalization) and OpenAI math (ETH false via subexponential #k-SAT, arithmetic hierarchy) claim arithmetic and counting speedups but explicitly leave Boolean P vs NP open and do not treat the charged single-tape model or Hartmanis-style equality constructions. Google Research / DeepMind and xAI-org yield no matching results on charged compatibility or single-tape SAT transport. Hartmanis 1968 remains the classical quadratic barrier for separated equality. Beame–Kornerup cumulative memory supplies general context only; not used for the specific family theorem.

Repository controls: matching upper bound of CHARGED-UNSAT-TRANSPORT1, static ceiling Theorem 2, prior residual-map collapse, and GANN free-resource residual bottleneck recovered unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1. HEAD at start recovered from prior X01-05 context.

## 2. Attempted proof construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1 (unlimited poly-dimensional attention, unlimited random access / multi-tape equivalent, exact GE, exact 2-SAT / Horn / dual-Horn, poly-depth global attention) on poly-size instances.

Candidate dynamic obligation (post local solves):

After free authentication and local solution of the Horn / dual-Horn selectors, left clauses, right clauses and middle chain on the permutation (or map) family, introduce a sequence of k = ω(1) unlocked residual maps ρ_1, …, ρ_k. Each ρ_{j+1} is defined as an affine shift or short-program permutation of a description of ρ_j, with the shift key equal to the equality bit of the previous residual (or a short hash thereof). The claim was that each residual still carries independent Ω(log r) incompressible bits that must be re-materialized or re-crossed after the preceding equality is known, because the free tools solve only local fragments and the global map equality is the residual compatibility task. Bounded-reuse decoder conditions were to be met by treating each unlocked equality as a separate obligation set with constant event reuse, producing an additional Ω(k N^{2}) factor in the charged model.

The free local solvers handle the initial extraction and comparison of the source maps; the sequential unlocks were intended to force post-transport work that cannot be cached from a single pass.

## 3. Obstacles and collapse

1. **Joint computability of the entire chain.** All residual maps ρ_j are deterministic functions of the original input pair (π, σ) (or (f, g)) and the fixed shift rules. The free (or paid) authentication-and-comparison pass already extracts the source maps, computes every successive residual by applying the known shift rules, and obtains every equality bit. These bits can be cached in O(k log N) space before any later stage. No additional compulsory crossings or materializations are forced beyond the quadratic already paid by the matching upper bound solver (or its free-resource analogue).

2. **Paid / free generation of unlocks.** If the residuals are generated on the fly, every transition that computes the next residual description, updates storage, or re-crosses a cut is already included in the whole-run lower bound of the original theorem. The model charges those transitions. With polynomial k the family solver simply extends its single comparison loop; total remains O(N^{2}). Free random access and attention do not create free external events; they still operate on data that must be transported or co-located for the incompressible equality test.

3. **Decoder and reuse.** Any decoder recovering a residual from a cached equality bit plus a short program for the shift rule has description length O(log N). Once the initial pass has performed the work, the obligations are not independent; the event-reuse bound is vacuously satisfied. Free poly-dimensional attention can embed the entire chain of equality bits into a single aggregate embedding of poly(log r) dimension, but verifying exact equality on adversarial (incompressible) maps still embeds the same information-transport requirement in the charged physical layout.

Consequently the candidate fails the requirement that the obligations remain compulsory after static (or free-local) transport can be completed. The construction collapses under the existing matching upper bound and free-resource model.

## 4. Revised scope

The free resources resolve every local fragment but leave the global map-equality as a residual compatibility obligation whose information-theoretic transport scales as Ω(N^{2}) time / Ω(N^{3}) cumulative memory in the charged model. Sequential unlocks that are functions of the initial separated input do not amplify beyond the static ceiling. A viable DYNAMIC-COMPATIBILITY-OBLIGATION1 must produce obligations whose information is not jointly recoverable from a single paid or free comparison of the source blocks, or must force re-materialization of incompressible data after the first transport in a way that cannot be cached for free (e.g., data whose description depends on an external random source or a computation path that itself requires the crossing).

Attention represents the comparison differently but does not escape the synchronization bottleneck for exact decision on adversarial maps.

## 5. Gates

| Gate | Status |
|---|---|
| Free local solvers | Confirmed; do not collapse the transport. |
| Static ceiling | Still binds; sequential residuals do not exceed it. |
| Matching upper bound | Realized; collapses the candidate. |
| Joint precomputation | Obstacle realized. |
| Unrestricted SAT lower bound | Not claimed. |
| P vs NP | OPEN. |

DYNAMIC-COMPATIBILITY-OBLIGATION1 OPEN. P vs NP OPEN.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing has occurred and whose information is not a deterministic function of the original input blocks alone (e.g., via an interactive or path-dependent unlock that the charged model must re-materialize), or prove that every such attempt collapses under paid joint preprocessing. Uniform simulation of arbitrary correct machines remains the load-bearing open premise.

No agent settings, public proof claims or historical files changed.
