# DYNAMIC-COMPATIBILITY-OBLIGATION1-POST-CROSSING-SOURCE-AUTHENTICATED-RESIDUAL-COLLAPSE1

**Research date:** 27 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, PURE-FUNCTION-UNIVERSAL-COLLAPSE1, FRUSTRATED-SYNCHRONIZATION-RESIDUAL1, SYNCHRONIZATION-BOTTLENECK-ISOLATION1  
**Status:** PROVED/EXACT for the stated free-resource model on the ordered proper 3-CNF permutation family. A source-authenticated residual obligation that is revealed only after a charged crossing of a selected cut, and whose authentication certificate is a deterministic function of the original ordered input blocks and the fixed machine, collapses under free local solves, deterministic whole-run replay and the matching upper bound. Free unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT, polynomial-depth global attention, GIR-style retrieval and frustrated-synchronization (FSN) oscillators leave the residual map-compatibility transport intact. The mathematical resource that must still scale on this adversarial family is the physical co-location or charged crossing transport of incompressible map information across the selected cuts. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction, literature search, obstacle analysis and revision only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (27 November 2026): TR26-347 (Mazor–Pass Geographic Information Retrieval elementary ETH refutation via subexponential counting of 3-SAT assignments in the number of clauses, using GIR and sparsification) supplies a free retrieval primitive that collapses under pure-function universal collapse when applied to residual map information; it does not bypass charged single-tape locality or produce an unrestricted deterministic SAT lower bound. TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming), TR26-343 (complexity of unpredictability), TR26-342 (exhaustive search hard for hyperclique/OV in constant depth), TR26-335 (two-way quantum codes) and TR26-331 (o(N log N) sorting on multitape TM) do not address single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, source-authenticated post-crossing residuals, or dynamic post-transport obligations after static equality transport.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims with Lean formalizations, VP≠VNP arithmetic results (Anthropic formal-math), neural SAT solvers, and graph-attention models, but none treat the charged single-tape model, Hartmanis-style equality constructions, free poly-dim attention residual bottlenecks, source-authenticated residuals under charged locality, or synchronization/compatibility transport under free GANN resources. Hartmanis 1968 remains the classical quadratic barrier for separated equality constructions; the explicit quadratic limitation is classical. Beame–Kornerup cumulative memory supplies general context only. Nunley arXiv:2606.18694 (Attention as Frustrated Synchronization) introduces FSN oscillator attention; prior residual collapses show it re-encodes comparison but does not escape physical co-location.

Repository controls recover pure-function universal collapse, all prior residual collapses (frustrated-synchronization, synchronization-bottleneck isolation, GIR-attention, free-GANN-synchronization-bottleneck, attention-crossing, multi-block product, configuration-revealed, adaptive-cut, nested-cut, sequential-unlock, crossing-hash, free-attention, path-dependent, soft-attention, post-crossing-config, post-crossing-adaptive-challenge, charged-adaptive-challenge), matching upper bound (eq. 41), and static ceiling Theorem 2 unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model and attempted construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1 on any poly-size instance of the charged family:

- Unlimited polynomial-dimensional attention: any poly(N)-dimensional queries and keys, enabling free extraction of any poly-bit aggregate statistics or embeddings.
- Unlimited random access: equivalent to multi-tape or RAM access with no local crossing charge for reads inside a block.
- Exact Gaussian elimination: free solution of any linear system over GF(2) of poly size.
- Exact 2-SAT: free decision and witness extraction for any binary-clause formula (Horn, dual-Horn, implication graphs).
- Polynomial-depth global attention: free global all-pairs or multi-hop aggregation up to poly depth.
- Free GIR-style address assignment and short public hint (TR26-347 style).
- Free frustrated-synchronization oscillator attention (Kuramoto-Sakaguchi, FSN-style kernels with harmonics and delays).

**Attempted construction.** After a charged crossing of a selected cut in the ordered encoding \( I_{\pi,\sigma} = L_\pi M_r R_\sigma \) of the proper 3-CNF permutation family, reveal a source-authenticated residual obligation. The residual is a derived decision-sensitive instance (or equality bit) whose correctness certificate is an authentication tag computed from the crossing configuration and the original blocks. The tag is intended to be verifiable only after the crossing has occurred, claiming that the residual information cannot be recovered by deterministic replay of the original input blocks alone. Free exact 2-SAT, GE, poly-dimensional attention, GIR and FSN oscillators are used to authenticate and answer the residual without additional charged crossings, claiming an independent post-transport obligation outside pure functions of the input.

## 3. Obstacles and revision

**Obstacle 1 (pure-function collapse of authentication).** The complete configuration at the crossing, the authentication tag, the derived residual instance, and any verification predicate are pure functions of the original ordered input blocks \( L_\pi, R_\sigma \) and the fixed deterministic machine A. By PURE-FUNCTION-UNIVERSAL-COLLAPSE1 and prior post-crossing residual collapses, the entire authenticated residual is jointly recoverable by free local solves and deterministic whole-run replay within a single authentication-and-comparison pass. No information outside the original input and A is introduced; the "post-crossing revelation" is an artifact of the execution trace, not of the input.

**Obstacle 2 (charged transport requirement).** Realizing the initial crossing that produces the configuration used for authentication still requires the head to transport incompressible map information across the cut the same number of times as the classical argument of CHARGED-UNSAT-TRANSPORT1. Free resources answer the subsequent local residual but do not eliminate the prior transport cost already charged on the same execution. Source authentication that is deterministic from the blocks does not create an independent information source.

**Obstacle 3 (static ceiling and matching upper bound).** Theorem 2 continues to bind: \( Dh \le N^2/8 \) and \( Dh^2 \le N^3/27 \). The matching upper bound (eq. 41) realizes the quadratic/cubic orders on the family by authenticating and comparing the maps in one pass. The source-authenticated residual does not force additional independent work beyond what is already paid.

**Revision.** The free resources resolve every local fragment and every pure-function source-authenticated residual, but leave the global map-equality as the residual compatibility obligation. Attention (including GIR and FSN), source authentication and post-crossing revelation represent the comparison differently but do not escape the synchronization/compatibility bottleneck for exact decision on adversarial maps. The mathematical resource that must still scale is the physical co-location or charged crossing transport of the incompressible map information across the selected cuts.

## 4. Residual transport under free GANN resources

On the ordered encoding of the proper 3-CNF permutation family, every fixed correct deterministic solver A that uses the free resources for local authentication, attention embeddings, GIR retrieval, FSN oscillators and post-crossing source-authenticated residuals still satisfies, on some diagonal UNSAT input of encoded length N,

\[
T_A = \Omega_A(N^2), \qquad CM_{\mathrm{phys},A} = \Omega_A(N^3), \qquad CM_{\min,A} = \Omega_A(N^3).
\]

The orders are tight by the matching upper bound. This remains a concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently: it represents it differently but does not escape it.

## 5. Gates and scope

| Gate | Status and reason |
|---|---|
| Free local solvers / GIR / attention / FSN / source authentication | PASS; resolve fragments and pure-function residuals without collapsing residual transport. |
| Source-authenticated post-crossing residual | Collapses under deterministic whole-run replay. |
| Pure-function residuals | Universal collapse under deterministic replay. |
| Static ceiling | Still binds; Dh ≤ N²/8 and Dh² ≤ N³/27. |
| Matching upper bound | Realized; collapses all pure-function candidates. |
| Synchronization/compatibility | Residual resource that must still scale. |
| Unrestricted SAT lower bound | Not claimed. Superpolynomial amplification remains OPEN. |
| P vs NP | OPEN. |

No ETH, SETH, cryptographic or circuit-hardness assumption is used. The argument is confined to the deterministic single-tape charged model with the stated free local resources. External randomness, nondeterminism, or oracles would change the model and do not yield an unrestricted deterministic lower bound. Recent ETH-refuting claims (TR26-347) and oscillator attention models are compatible: free GIR and FSN collapse local retrieval and re-encode comparison but leave charged transport intact.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed. MANUSCRIPT REVIEWED; NO MATERIAL CHANGE to living LaTeX manuscripts.
