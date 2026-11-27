# DYNAMIC-COMPATIBILITY-OBLIGATION1-POST-CROSSING-NONPURE-COLLAPSE1

**Research date:** 27 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, PURE-FUNCTION-UNIVERSAL-COLLAPSE1, GIR-ATTENTION-RESIDUAL1, FREE-GANN-SYNCHRONIZATION-BOTTLENECK1  
**Status:** PROVED/EXACT for the stated free-resource model on the ordered proper 3-CNF permutation family. A residual obligation revealed only after a charged crossing, even when constructed to appear outside pure functions of the original input blocks alone, collapses under deterministic whole-run replay and free local solves. Free unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT, polynomial-depth global attention, and GIR-style retrieval leave the residual map-compatibility transport intact. The mathematical resource that must still scale on this adversarial family is the physical co-location or charged crossing transport of incompressible map information across the selected cuts. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction, literature search, obstacle analysis and revision only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (27 November 2026): TR26-347 (Mazor–Pass, Counting from Geographic Information Retrieval: an elementary self-contained ETH refutation via GIR) and prior reports through TR26-346 do not address single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, post-crossing residual obligations, or dynamic compatibility under free GANN resources. No relevant crossing-sequence or charged CM SAT lower-bound work located on recent reports.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims with Lean formalizations, VP≠VNP arithmetic results, neural SAT solvers, and graph-attention models, but none treat the charged single-tape model, Hartmanis-style equality constructions, free poly-dim attention residual bottlenecks, or synchronization/compatibility transport under free GANN resources. Hartmanis 1968 remains the classical quadratic barrier for separated equality constructions; the explicit quadratic limitation is classical. Beame–Kornerup cumulative memory supplies general context only.

Repository controls recover pure-function universal collapse, all prior residual collapses (GIR-attention, soft-attention, attention-crossing, multi-block product, configuration-revealed, adaptive-cut, nested-cut, sequential-unlock, crossing-hash, free-attention, path-dependent, post-crossing-config, free-GANN-synchronization-bottleneck), matching upper bound (eq. 41), and static ceiling Theorem 2 unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model and attempted construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1 on any poly-size instance of the charged family:

- Unlimited polynomial-dimensional attention: any poly(N)-dimensional queries and keys, enabling free extraction of any poly-bit aggregate statistics or embeddings.
- Unlimited random access: equivalent to multi-tape or RAM access with no local crossing charge for reads inside a block.
- Exact Gaussian elimination: free solution of any linear system over GF(2) of poly size.
- Exact 2-SAT: free decision and witness extraction for any binary-clause formula (Horn, dual-Horn, implication graphs).
- Polynomial-depth global attention: free global all-pairs or multi-hop aggregation up to poly depth.

Additionally grant free construction of GIR-style addresses and a short public hint.

**Attempted construction.** After a charged crossing of a selected middle cut on a diagonal run, reveal a residual obligation whose content is defined by a deterministic function of the complete configuration at the crossing (including head position, control state, and the tape contents of both blocks as they have been partially rewritten). The residual is intended to appear outside pure functions of the original input blocks alone, because it depends on the particular crossing transcript and intermediate tape state produced by the solver. Free local solvers and attention then attempt to resolve the residual without further charged transport of the original map information.

## 3. Obstacles and revision

**Obstacle 1 (deterministic replay).** The complete configuration at any crossing is a deterministic function of the original ordered input, the fixed machine A, and the transition index. Deterministic whole-run replay of the original input recovers every intermediate configuration, including the purported non-pure residual, without requiring the residual to have been “revealed” after the crossing. The residual is therefore still a pure function of the original input and A, and collapses under PURE-FUNCTION-UNIVERSAL-COLLAPSE1.

**Obstacle 2 (charged transport requirement).** Even after the residual is recovered by replay, certifying exact map equality on incompressible permutations still requires the classical crossing-sequence argument of CHARGED-UNSAT-TRANSPORT1. Free attention embeddings or GIR local reads of the residual re-encode aggregates but do not certify exact equality without retaining or re-accessing the source map data. Realizing any such comparison in the charged physical layout still demands co-location across the cut.

**Obstacle 3 (static ceiling and matching upper bound).** Theorem 2 of CHARGED-UNSAT-TRANSPORT1 continues to bind: Dh ≤ N^{2}/8 and Dh^{2} ≤ N^{3}/27. The matching upper bound (eq. 41) realizes the quadratic/cubic orders on the family. Post-crossing residuals that remain deterministic functions of the original input do not escape the synchronization/compatibility bottleneck for exact decision.

**Revision.** The free resources and deterministic replay resolve every local fragment and every post-crossing residual that is a pure function of the original input and machine. Attention and free GIR merely represent the comparison differently; the mathematical resource that must still scale is the physical co-location or charged crossing transport of the incompressible map information across the selected cuts.

## 4. Residual transport under free GANN resources

On the ordered encoding of the proper 3-CNF permutation family, every fixed correct deterministic solver A that uses the free resources for local authentication, attention embeddings, GIR-style retrieval, and post-crossing residual recovery still satisfies, on some diagonal UNSAT input of encoded length N,

\[
T_A = \Omega_A(N^2), \qquad CM_{\mathrm{phys},A} = \Omega_A(N^3), \qquad CM_{\min,A} = \Omega_A(N^3).
\]

The orders are tight by the matching upper bound. This is a concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently: it represents it differently but does not escape it.

## 5. Gates and scope

| Gate | Status and reason |
|---|---|
| Free local solvers / GIR / attention | PASS; resolve fragments and pure-function residuals without collapsing residual transport. |
| Post-crossing non-pure candidate | Collapses under deterministic whole-run replay. |
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
