# DYNAMIC-COMPATIBILITY-OBLIGATION1-UNSHARDABLE-CODE-RESIDUAL-COLLAPSE1

**Research date:** 28 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, PURE-FUNCTION-UNIVERSAL-COLLAPSE1, ALGEBRAIC-PERMANENT-RESIDUAL-COLLAPSE1, INTERACTIVE-MAP-CHALLENGE-COLLAPSE1, TREECODE-INTERACTIVE-RESIDUAL-COLLAPSE1, GIR-ATTENTION-RESIDUAL1  
**Status:** PROVED/EXACT for the stated free-resource model on the ordered proper 3-CNF permutation family. Free linear (\(\ell, s\))-unshardable codes (TR26-338) used for joint encoding of residual map components with local recovery and unshardability collapse under free local solves, deterministic whole-run replay and the matching upper bound. Free unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT, polynomial-depth global attention, GIR-style retrieval, frustrated-synchronization oscillators, explicit tree codes, free algebraic circuit / permanent evaluation and targeted-sampler probes leave the residual map-compatibility transport intact. The mathematical resource that must still scale on this adversarial family is the physical co-location or charged crossing transport of incompressible map information across the selected cuts. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction, literature search, obstacle analysis and revision only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (28 November 2026): TR26-338 (Amireddy–Dodis–Goyal–Mook–Sudan–Wichs Unshardable Codes) introduces a coding-theoretic primitive motivated by censorship resistance: encode \(k\) data components into a codeword such that every component is locally recoverable from at most \(\ell\) symbols, and any erasure either uniquely determines all components or leaves at least \(s\) undetermined. Linear constructions achieve \(s = (1-\varepsilon)k\) with locality \(\ell = O_\varepsilon(1)\), with a matching-style lower bound \(s \le k - k/\ell + 1\) for linear codes; LDCs convert to unshardable via extension-field basis change. TR26-347 (Mazor–Pass GIR elementary ETH refutation), TR26-346 (Dittmer–Ostrovsky explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming completions) and algebraic VP \(\ne\) VNP claims remain the most recent interactive, retrieval and hardness primitives. No recent report addresses single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, unshardable-code residuals under charged locality, or dynamic post-transport obligations after static equality transport.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting \(2^{o(n)}\) #k-SAT claims with Lean formalizations, VP\(\ne\)VNP arithmetic results (Anthropic formal-math Claude paper and OpenAI counterpart, neither settling Boolean P vs NP), neural SAT solvers, and graph-attention models, but none treat the charged single-tape model, Hartmanis-style equality constructions, free poly-dim attention residual bottlenecks, unshardable-code residual recovery under charged locality, or synchronization/compatibility transport under free GANN resources. Hartmanis 1968 remains the classical quadratic barrier for separated equality constructions; the explicit quadratic limitation is classical. Beame–Kornerup cumulative memory supplies general context only. Nunley arXiv:2606.18694 (Attention as Frustrated Synchronization) introduces FSN oscillator attention; prior residual collapses show it re-encodes comparison but does not escape physical co-location. The algebraic VP \(\ne\) VNP separations (if accepted) separate arithmetic circuit complexity from VNP but do not transfer to Boolean circuit complexity or to single-tape charged transport of map equality; free exact GE already solves linear systems, and free 2-SAT solves binary fragments.

Repository controls recover pure-function universal collapse, all prior residual collapses (algebraic-permanent, interactive-map-challenge, tree-code interactive, source-authenticated post-crossing, frustrated-synchronization, synchronization-bottleneck isolation, GIR-attention, free-GANN-synchronization-bottleneck, attention-crossing, multi-block product, configuration-revealed, adaptive-cut, nested-cut, sequential-unlock, crossing-hash, free-attention, path-dependent, soft-attention, post-crossing-config, post-crossing-adaptive-challenge, charged-adaptive-challenge), matching upper bound (eq. 41), and static ceiling Theorem 2 unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Free-resource model and attempted construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1 on any poly-size instance of the charged family:

- Unlimited polynomial-dimensional attention: any poly(N)-dimensional queries and keys, enabling free extraction of any poly-bit aggregate statistics or embeddings.
- Unlimited random access: equivalent to multi-tape or RAM access with no local crossing charge for reads inside a block.
- Exact Gaussian elimination: free solution of any linear system over GF(2) of poly size.
- Exact 2-SAT: free decision and witness extraction for any binary-clause formula (Horn, dual-Horn, implication graphs).
- Polynomial-depth global attention: free global all-pairs or multi-hop aggregation up to poly depth.
- Free GIR-style address assignment and short public hint (TR26-347 style).
- Free frustrated-synchronization oscillator attention (Kuramoto-Sakaguchi, FSN-style kernels with harmonics and delays).
- Free explicit O(1) tree codes of constant rate and relative distance (TR26-346).
- Free algebraic circuit evaluation for any poly-size arithmetic circuit, and (for the purpose of this residual test) free evaluation of the permanent or Hamiltonian cycle polynomial on poly-size matrices.
- Free linear (\(\ell, s\))-unshardable codes with constant locality and near-full unshardability parameter (TR26-338 style), enabling joint encoding of residual map components such that local recovery of any component requires reading only O(1) symbols, and selective erasure cannot isolate individual residual bits without destroying many others.

**Attempted construction.** After a charged crossing of a selected cut in the ordered encoding \( I_{\pi,\sigma} = L_\pi M_r R_\sigma \) of the proper 3-CNF permutation family, jointly encode residual map-difference components (or decision-sensitive equality challenges) into a free unshardable codeword. Use free local recovery of individual residual components from O(1) symbols, combined with free attention embeddings, GIR local reads, tree-code interactive recovery, algebraic permanent evaluation and targeted-sampler probes, to extract and verify the residual without additional charged crossings, claiming that the unshardability property forces any attempt to censor or isolate residual information to pay for many components at once, thereby creating an independent residual obligation outside pure functions of the input that escapes the synchronization bottleneck or reduces the asymptotic charged transport cost.

## 3. Obstacles and revision

**Obstacle 1 (pure-function collapse of unshardable residual).** The complete configuration at the crossing, any unshardable codeword encoding residual map components, the local recovery predicates, the decoder states, and any verification predicate are pure functions of the original ordered input blocks \( L_\pi, R_\sigma \) and the fixed deterministic machine A. By PURE-FUNCTION-UNIVERSAL-COLLAPSE1 and prior post-crossing residual collapses (including algebraic-permanent, interactive-map-challenge and tree-code), the entire unshardable residual is jointly recoverable by free local solves and deterministic whole-run replay within a single authentication-and-comparison pass. No information outside the original input and A is introduced; the unshardable encoding is an efficiently computable function of the residual bits already determined by the blocks. Unshardability re-encodes existing map information; it does not create new information outside pure functions.

**Obstacle 2 (charged transport of residual symbols).** Realizing the local recovery or verification of residual components still requires the head (or message) to transport the unshardable codeword symbols (or the residual map-difference information they encode) across the cut. Because the maps are incompressible, the information length remains \( \Theta(r) \) (or \( \Theta(N) \) in the encoding) in the worst case; the number of crossings needed to deliver or verify the residual is asymptotically the same as the classical argument of CHARGED-UNSAT-TRANSPORT1. Free unshardable codes improve local recovery and censorship resistance but do not eliminate the need to co-locate or transport the incompressible information. Free random access removes only local charge. Constant locality reduces the number of symbols read locally but does not reduce the asymptotic charged transport of the global residual map across the cut.

**Obstacle 3 (static ceiling and matching upper bound).** Theorem 2 continues to bind: \( Dh \le N^2/8 \) and \( Dh^2 \le N^3/27 \). The matching upper bound (eq. 41) realizes the quadratic/cubic orders on the family by authenticating and comparing the maps in one pass. Unshardable residual encodings do not force additional independent work beyond what is already paid; they re-encode the comparison differently.

**Revision.** The free resources resolve every local fragment and every pure-function unshardable-code residual, but leave the global map-equality as the residual compatibility obligation. Attention (including GIR and FSN), tree-code interactive recovery, adaptive challenges, free permanent evaluation, targeted-sampler probes and unshardable codes represent the comparison differently but do not escape the synchronization/compatibility bottleneck for exact decision on adversarial maps. The mathematical resource that must still scale is the physical co-location or charged crossing transport of the incompressible map information across the selected cuts. Coding-theoretic unshardability does not transfer to a free Boolean transport primitive under charged locality.

## 4. Residual transport under free GANN resources

On the ordered encoding of the proper 3-CNF permutation family, every fixed correct deterministic solver A that uses the free resources for local authentication, attention embeddings, GIR retrieval, FSN oscillators, tree-code recovery, adaptive map challenges, free algebraic circuit / permanent evaluation, targeted-sampler residual probes and unshardable-code residual recovery still satisfies, on some diagonal UNSAT input of encoded length N,

\[
T_A = \Omega_A(N^2), \qquad CM_{\mathrm{phys},A} = \Omega_A(N^3), \qquad CM_{\min,A} = \Omega_A(N^3).
\]

The orders are tight by the matching upper bound. This remains a concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently: it represents it differently but does not escape it.

## 5. Gates and scope

| Gate | Status and reason |
|---|---|
| Free local solvers / GIR / attention / FSN / tree codes / permanent / unshardable codes | PASS; resolve fragments and pure-function residuals without collapsing residual transport. |
| Unshardable-code residual | Collapses under deterministic whole-run replay and still requires charged transport of residual symbols. |
| Pure-function residuals | Universal collapse under deterministic replay. |
| Static ceiling | Still binds; Dh ≤ N²/8 and Dh² ≤ N³/27. |
| Matching upper bound | Realized; collapses all pure-function candidates. |
| Synchronization/compatibility | Residual resource that must still scale. |
| Unrestricted SAT lower bound | Not claimed. Superpolynomial amplification remains OPEN. |
| P vs NP | OPEN. VP ≠ VNP (if accepted) and unshardable codes do not settle Boolean P vs NP. |

No ETH, SETH, cryptographic or circuit-hardness assumption is used. The argument is confined to the deterministic single-tape charged model with the stated free local resources. External randomness, nondeterminism, or oracles would change the model and do not yield an unrestricted deterministic lower bound. Recent ETH-refuting claims (TR26-347), explicit tree codes (TR26-346), targeted samplers (TR26-345), algebraic VP \(\ne\) VNP results and unshardable codes (TR26-338) are compatible: free GIR, tree codes, samplers, FSN, permanent evaluation and unshardable encodings collapse local retrieval/computation and re-encode comparison but leave charged transport intact.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed. MANUSCRIPT REVIEWED; NO MATERIAL CHANGE to living LaTeX manuscripts.
