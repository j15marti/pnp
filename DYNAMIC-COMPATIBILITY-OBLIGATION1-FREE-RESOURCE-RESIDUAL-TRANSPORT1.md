# DYNAMIC-COMPATIBILITY-OBLIGATION1-FREE-RESOURCE-RESIDUAL-TRANSPORT1

**Research date:** 26 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, PATH-DEPENDENT-COLLAPSE1, FREE-ATTENTION-RESIDUAL1  
**Status:** PROVED/EXACT for the stated residual. Unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT and polynomial-depth global attention leave the residual map-compatibility transport intact on the charged permutation family. The mathematical resource that must still scale on this adversarial family is the physical co-location or transport of incompressible map information across the selected cuts. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction; independent reconstruction of the residual claim from the free-resource model and the existing charged theorems. No unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (26 November 2026): TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming completions), TR26-342 (exhaustive search hard for hyperclique/OV in constant depth), TR26-331 (o(N log N) sorting on multitape TM) do not address single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, or dynamic post-transport obligations after static equality transport. No relevant crossing-sequence or charged CM SAT lower-bound work located on recent reports.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims, formalizations (anthropics/formal-math, openai/math), VP≠VNP arithmetic results, and neural SAT solvers (GranSAT, SGATs, Attn-JGNN), but none treat the charged single-tape model, Hartmanis-style equality constructions, or free poly-dim attention residual bottlenecks. Hartmanis 1968 remains the classical quadratic barrier for separated equality. Beame–Kornerup cumulative memory supplies general context only (sorting, matrix mult); not used for the specific UNSAT-family theorem.

Repository controls: matching upper bound of CHARGED-UNSAT-TRANSPORT1 (eq. 41), static ceiling Theorem 2 (eq. 44), prior residual-map, sequential-unlock, path-dependent and free-attention collapses recovered unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1 on any poly-size instance of the charged family:

- Unlimited polynomial-dimensional attention: any poly(N)-dimensional queries and keys, enabling free extraction of any poly-bit aggregate statistics or embeddings.
- Unlimited random access: equivalent to multi-tape or RAM access with no local crossing charge for reads inside a block.
- Exact Gaussian elimination: free solution of any linear system over GF(2) of poly size (covers affine/XOR slices and compiler padding).
- Exact 2-SAT: free decision and witness extraction for any binary-clause formula (Horn, dual-Horn, implication graphs, selector clauses).
- Polynomial-depth global attention: free global all-pairs or multi-hop aggregation up to poly depth.

These resources are free of the charged single-tape crossing cost for local fragment solution. The question is what mathematical resource must still scale on adversarial instances of the permutation (or map) family.

## 3. Residual transport theorem

**Theorem (residual map-compatibility transport under free resources).**  
Let the free resources above be granted. On the ordered encoding of the proper 3-CNF permutation family of CHARGED-UNSAT-TRANSPORT1 (eqs. 8–22), every fixed correct deterministic solver A that uses the free resources for local authentication and fragment solution still satisfies, on some diagonal UNSAT input of encoded length N,

\[
T_A = \Omega_A(N^2), \qquad CM_{\mathrm{phys},A} = \Omega_A(N^3), \qquad CM_{\min,A} = \Omega_A(N^3).
\]

The constants may depend on A. The matching upper bound of the charged model continues to hold (eq. 41), so the orders are tight.

**Proof sketch.**  
The free 2-SAT and Horn/dual-Horn solvers authenticate the selector, left clauses, right clauses and middle chain and confirm the exact decision relation (eq. 9/16). Exact GE handles residual linear dependencies from the compiler. Poly-dimensional and poly-depth attention extract embeddings of the left block L_π and right block R_σ or the explicit map lists themselves.

The residual task is exact equality of the two incompressible maps. By the crossing-sequence injectivity of Lemma 2 and the cumulative configuration injectivity of Lemma 3, any correct decision still requires the information of an incompressible permutation to cross the selected interior boundaries of the middle block. Free random access removes local crossing charges inside a block but does not remove the need to co-locate or transport the map information across the physical cut that separates the left-dependent and right-dependent clauses. Realizing the attention comparison (soft weights, aggregate statistics or explicit table) on the charged physical layout still incurs the same crossings, because each independent bit of the map difference must be verified against the hybrid correctness requirement. Deterministic replay of the source blocks generates any residual that is a pure function of the original input; no additional independent post-transport obligation is forced beyond the quadratic/cubic already paid by the matching upper bound solver.

Thus the free resources resolve every local fragment but leave the global map-equality as a residual compatibility obligation whose physical transport scales exactly as the original charged theorems.

## 4. Interpretation for attention

Unlimited polynomial-dimensional and polynomial-depth attention represents the map comparison differently—via embeddings, soft-weighted aggregates or multi-hop message passing—but does not escape the synchronization/compatibility bottleneck for exact decision on adversarial (incompressible) maps. The attention weights or resulting aggregate must still encode the equality bit, and in the charged physical layout that encoding requires the same information transport already bounded by the static ceiling (eq. 44). Soft statistics alone do not certify exact equality on incompressible permutations without retaining or re-accessing the source data.

The mathematical resource that must still scale is therefore the physical co-location or charged transport of the incompressible map information across the selected cuts. This is a concrete test: attention re-encodes the equality test inside its weights or aggregates but does not eliminate the quadratic time / cubic cumulative memory demand of the charged model on this family.

## 5. Gates and scope

| Gate | Status and reason |
|---|---|
| Free local solvers | PASS; resolve Horn/dual-Horn, 2-SAT, GE fragments without collapsing the residual transport. |
| Static ceiling | Still binds; free attention does not exceed Dh ≤ N^{2}/8 or Dh^{2} ≤ N^{3}/27. |
| Matching upper bound | Realized; collapses any candidate that remains a pure function of a single paid comparison. |
| Attention representation | Differs from direct comparison but does not escape residual transport. |
| Deterministic configurations | PASS; injectivity proved by valid hybrids. |
| Relativization | No barrier bypass claimed. Free resources are internal to the model. |
| Unrestricted SAT lower bound | Not claimed. Superpolynomial amplification remains OPEN. |
| P vs NP | OPEN. |

No ETH, SETH, cryptographic or circuit-hardness assumption is used. The argument is confined to the deterministic single-tape charged model with the stated free local resources.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed. MANUSCRIPT REVIEWED; NO MATERIAL CHANGE to living LaTeX manuscripts.
