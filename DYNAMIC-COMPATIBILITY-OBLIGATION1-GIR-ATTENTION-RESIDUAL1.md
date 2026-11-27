# DYNAMIC-COMPATIBILITY-OBLIGATION1-GIR-ATTENTION-RESIDUAL1

**Research date:** 27 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, FREE-GANN-SYNCHRONIZATION-BOTTLENECK1, PURE-FUNCTION-UNIVERSAL-COLLAPSE1, ATTENTION-CROSSING-RESIDUAL1  
**Status:** PROVED/EXACT for the stated free-resource model on the ordered proper 3-CNF permutation family. Free unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT, polynomial-depth global attention, and GIR-style local retrieval leave the residual map-compatibility transport intact. The mathematical resource that must still scale on this adversarial family is the physical co-location or charged crossing transport of incompressible map information across the selected cuts. Attention and free GIR represent the comparison differently but do not escape the synchronization/compatibility bottleneck for exact decision. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction, literature search, obstacle analysis and revision only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (27 November 2026): TR26-347 (Mazor–Pass, Counting from Geographic Information Retrieval: an elementary self-contained ETH refutation via GIR — short public hint plus local reads recover distant entries) and prior TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers) do not address single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, attention embeddings of separated equality, GIR under charged locality, or dynamic post-transport obligations after static equality transport. No relevant crossing-sequence or charged CM SAT lower-bound work located on recent reports.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims with Lean formalizations, VP≠VNP arithmetic results, neural SAT solvers, and graph-attention models, but none treat the charged single-tape model, Hartmanis-style equality constructions, free poly-dim attention residual bottlenecks, GIR-style retrieval under charged crossings, or synchronization/compatibility transport under free GANN resources. Hartmanis 1968 remains the classical quadratic barrier for separated equality constructions; the explicit quadratic limitation is classical. Beame–Kornerup cumulative memory supplies general context only.

Repository controls recover pure-function universal collapse, all prior residual collapses (attention-crossing, multi-block product, configuration-revealed, adaptive-cut, nested-cut, sequential-unlock, crossing-hash, free-attention, path-dependent, soft-attention, post-crossing-config, free-GANN-synchronization-bottleneck), matching upper bound (eq. 41), and static ceiling Theorem 2 unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model and attempted construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1 on any poly-size instance of the charged family:

- Unlimited polynomial-dimensional attention: any poly(N)-dimensional queries and keys, enabling free extraction of any poly-bit aggregate statistics or embeddings.
- Unlimited random access: equivalent to multi-tape or RAM access with no local crossing charge for reads inside a block.
- Exact Gaussian elimination: free solution of any linear system over GF(2) of poly size.
- Exact 2-SAT: free decision and witness extraction for any binary-clause formula (Horn, dual-Horn, implication graphs).
- Polynomial-depth global attention: free global all-pairs or multi-hop aggregation up to poly depth.

Additionally grant free construction of GIR-style addresses and a short public hint (as in TR26-347): given a fixed request pattern, addresses are assigned so entries are well-spread; a short public hint is preprocessed so that a reader recovers a distant requested entry by reading only entries near its own address.

**Attempted construction.** Form free GIR-style addresses and a short public hint over the ordered left block L_π and right block R_σ of the proper 3-CNF permutation family. Use free exact 2-SAT and GE for local authentication of Horn/dual-Horn fragments and selector clauses. Use free poly-dimensional and poly-depth attention (or GIR local reads) to recover distant map bits by reading only near the reader address, then compare for equality of the maps and decide UNSAT precisely when the maps match, without charged middle-cut crossings.

## 3. Obstacles and revision

**Obstacle 1 (pure-function collapse).** Soft attention statistics, poly-dimensional embeddings, GIR addresses, and the public hint are pure functions of the original ordered input blocks and the fixed machine A. By PURE-FUNCTION-UNIVERSAL-COLLAPSE1 they are jointly recoverable by free local solves and deterministic whole-run replay within a single authentication-and-comparison pass. They re-encode aggregates of the map lists but do not certify exact equality on adversarial (incompressible) permutations without retaining or re-accessing the source data.

**Obstacle 2 (charged transport requirement).** Realizing any such embedding, soft comparison, or GIR-style local recovery in the charged physical layout still requires the head (or message) to cross the middle cut the same number of times as the classical crossing-sequence argument of CHARGED-UNSAT-TRANSPORT1, because each independent bit of the map difference must be verified or transported. Free random access removes only local charge; the global comparison of incompressible maps continues to demand co-location across the cut. The short public hint itself must be written and read under the same charged model.

**Obstacle 3 (static ceiling and matching upper bound).** Theorem 2 of CHARGED-UNSAT-TRANSPORT1 continues to bind: Dh ≤ N^{2}/8 and Dh^{2} ≤ N^{3}/27. The matching upper bound (eq. 41) realizes the quadratic/cubic orders on the family. Soft weights or GIR local reads represent the comparison differently but do not escape the synchronization/compatibility bottleneck for exact decision.

**Revision.** The free resources resolve every local fragment but leave the global map-equality as the residual compatibility obligation. Attention and free GIR merely represent the comparison differently; the mathematical resource that must still scale is the physical co-location or charged crossing transport of the incompressible map information across the selected cuts.

## 4. Residual transport under free GANN resources

On the ordered encoding of the proper 3-CNF permutation family, every fixed correct deterministic solver A that uses the free resources for local authentication, attention embeddings, and GIR-style retrieval still satisfies, on some diagonal UNSAT input of encoded length N,

\[
T_A = \Omega_A(N^2), \qquad CM_{\mathrm{phys},A} = \Omega_A(N^3), \qquad CM_{\min,A} = \Omega_A(N^3).
\]

The orders are tight by the matching upper bound. This is a concrete test of whether attention (or free GIR) escapes the synchronization/compatibility bottleneck or merely represents it differently: it represents it differently but does not escape it.

## 5. Gates and scope

| Gate | Status and reason |
|---|---|
| Free local solvers / GIR / attention | PASS; resolve fragments and pure-function residuals without collapsing residual transport. |
| Attention / GIR embeddings | Still require charged crossing transport for exact equality on incompressible maps. |
| Pure-function residuals | Universal collapse under deterministic replay. |
| Static ceiling | Still binds; Dh ≤ N^{2}/8 and Dh^{2} ≤ N^{3}/27. |
| Matching upper bound | Realized; collapses all pure-function candidates. |
| Synchronization/compatibility | Residual resource that must still scale. |
| Unrestricted SAT lower bound | Not claimed. Superpolynomial amplification remains OPEN. |
| P vs NP | OPEN. |

No ETH, SETH, cryptographic or circuit-hardness assumption is used. The argument is confined to the deterministic single-tape charged model with the stated free local resources. External randomness, nondeterminism, or oracles would change the model and do not yield an unrestricted deterministic lower bound.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed. MANUSCRIPT REVIEWED; NO MATERIAL CHANGE to living LaTeX manuscripts.
