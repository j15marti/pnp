# GANN with free polynomial resources: residual compatibility bottleneck

**Research date:** 26 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN expressivity vs SAT  
**Status:** Free local solvers do not eliminate the quadratic transport demand on the permutation family. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN. P vs NP OPEN.  
**Review:** Internal construction; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (26 November 2026): TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming completions), TR26-331 (o(N log N) sorting on multitape TM), TR26-339 (deterministic linear-time MST) do not address single-tape crossing sequences, charged cumulative memory on SAT families, or free-resource attention models for k-SAT. Organization-scoped searches on OpenAI, Anthropic, Google Research, and DeepMind yield ETH-refuting 2^{o(n)} #k-SAT claims and formalizations, but none treat the charged single-tape model or Hartmanis-style equality constructions. Hartmanis 1968 remains the classical quadratic barrier for separated equality. Beame–Kornerup supplies general cumulative-memory context only.

Repository controls: matching upper bound of CHARGED-UNSAT-TRANSPORT1 and static ceiling Theorem 2 recovered. Prior residual-map candidate collapsed under paid joint preprocessing. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model

Grant a Graph Attention Neural Network (or equivalent message-passing architecture) the following for free on any poly-size instance:

- Unlimited polynomial-dimensional attention: any poly(n)-dimensional queries and keys, enabling free extraction of any poly-bit aggregate statistics or embeddings.
- Unlimited random access: equivalent to multi-tape or RAM access with no crossing charge for local reads.
- Exact Gaussian elimination: free solution of any linear system over GF(2) of poly size (covers affine/XOR slices).
- Exact 2-SAT: free decision and witness extraction for any binary-clause formula (Horn, dual-Horn, implication graphs).
- Polynomial-depth global attention: free global all-pairs or multi-hop aggregation up to poly depth.

The question is what mathematical resource must still scale on adversarial k-SAT. This tests whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

## 3. Attempted construction

Apply the free tools to the permutation family of CHARGED-UNSAT-TRANSPORT1. The source is a conjunction of Horn and dual-Horn parts with supplied adjacent witnesses differing in one bit, compiled to proper 3-CNF, with left/right blocks depending on independent maps π, σ.

- Exact 2-SAT (or Horn/dual-Horn solvers) freely authenticates and solves the local selector, left clauses, right clauses, and middle OR-chain, confirming the local witnesses and the exact decision relation F is UNSAT iff π = σ.
- Exact GE freely handles any residual linear dependencies introduced by the compiler padding or chain variables.
- Poly-dimensional attention and poly-depth global attention freely compute embeddings of the left block L_π and right block R_σ, or extract the map lists themselves by attending over the clause identifiers.

The candidate claim was that free global attention could then compare the extracted maps in O(1) or O(log N) layers without charged crossings, collapsing the quadratic lower bound.

## 4. Obstacles and residual bottleneck

1. **Encoding and extraction cost.** Extracting the explicit map lists from the ordered unary/gamma encoding still requires reading every literal identifier. In the charged single-tape model these reads are transitions; free random access removes the charge only for local access, but the global comparison of incompressible maps still requires the information to be co-located or transported. Poly-dimensional attention produces an embedding of dimension poly(log r) or poly(r), but matching two arbitrary permutations requires either an explicit table (size r!) or a collision-resistant hash whose verification still embeds the equality test.

2. **Attention represents rather than escapes.** A poly-depth attention layer that attends from left-block tokens to right-block tokens computes a soft comparison. For exact decision on incompressible permutations, the attention weights or the resulting softmax must encode the equality bit. In the physical layout of the charged model, realizing that attention still requires the head (or message) to cross the middle cut the same number of times as the classical crossing sequence argument, because each independent bit of the map difference must be verified. The free tools solve the local Horn/dual-Horn fragments but leave the global map-equality as a residual compatibility obligation.

3. **Paid joint preprocessing still collapses independent residuals.** Any residual maps that are deterministic functions of (π, σ) can be generated and compared during the single free authentication pass already available. No additional compulsory post-transport work is forced beyond the quadratic already paid by the matching upper bound solver.

Thus the free resources resolve every local fragment (2-SAT, GE, Horn) but the synchronization of the two global maps remains a resource that scales as Ω(N^{2}) time / Ω(N^{3}) cumulative memory in the charged model. Attention either pays the same transport or re-encodes the equality test inside its weights, which for adversarial (incompressible) maps still demands the information to cross.

## 5. Revised scope and next target

The construction shows that unlimited poly-dim attention, random access, exact GE, exact 2-SAT and poly-depth global attention do not eliminate the compatibility bottleneck on this family; they represent the comparison differently but do not escape the information-transport requirement for exact decision. A viable DYNAMIC-COMPATIBILITY-OBLIGATION1 must force re-materialization of incompressible data after the free local solves, or produce obligations whose information is not jointly recoverable from a single paid (or free) comparison of the source blocks.

| Gate | Status |
|---|---|
| Free local solvers | Confirmed; do not collapse the transport. |
| Static ceiling | Still binds; free attention does not exceed it without new encoding. |
| Matching upper bound | Realized in the charged model; free tools do not improve the quadratic. |
| Unrestricted SAT lower bound | Not claimed. |
| P vs NP | OPEN. |

DYNAMIC-COMPATIBILITY-OBLIGATION1 OPEN. P vs NP OPEN.

HEAD at start: 687a17d0acf5fbb28b8e1d55b617dfcbc19d7c13
