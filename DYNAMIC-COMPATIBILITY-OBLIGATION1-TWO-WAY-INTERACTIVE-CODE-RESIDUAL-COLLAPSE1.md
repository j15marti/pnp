# DYNAMIC-COMPATIBILITY-OBLIGATION1-TWO-WAY-INTERACTIVE-CODE-RESIDUAL-COLLAPSE1

**Research date:** 28 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, PURE-FUNCTION-UNIVERSAL-COLLAPSE1, INDEFINITE-CAUSAL-STRUCTURE-RESIDUAL-COLLAPSE1, TREECODE-INTERACTIVE-RESIDUAL-COLLAPSE1, UNSHARDABLE-CODE-RESIDUAL-COLLAPSE1  
**Status:** PROVED/EXACT for the stated free-resource model on the ordered proper 3-CNF permutation family. Free two-way interactive codes with optimal erasure resilience (TR26-335 quantum-classical 3/5, quantum-quantum 2/3; TR26-320 binary approaching 2/3) used for interactive residual map-component transport and recovery across cuts collapse under free local solves, deterministic whole-run replay and the matching upper bound. Free unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT, polynomial-depth global attention, GIR-style retrieval, frustrated-synchronization oscillators, explicit tree codes, free algebraic circuit / permanent evaluation, targeted-sampler probes, linear unshardable codes, protected Almost 2-SAT / logarithmic Hall-slack terminals and process-matrix / indefinite causal order evaluation leave the residual map-compatibility transport intact. The mathematical resource that must still scale on this adversarial family is the physical co-location or charged crossing transport of incompressible map information across the selected cuts. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction, literature search, obstacle analysis and revision only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (28 November 2026): TR26-335 (Efremenko–Kol–Komech–Saxena–Zhang Two-Way Quantum Codes with Optimal Erasure Resilience) initiates two-way quantum codes in which the receiver participates in the interactive encoding process. Interaction improves resilience: for the quantum–classical channel (return channel classical and adversary-controlled) the sharp threshold is 3/5, achieved by an efficient constant-rate constant-alphabet code; for quantum–quantum the maximum is 2/3; for general interactive coding the optimal erasure resilience is 1/2. Related TR26-320 constructs deterministic binary two-way codes approaching 2/3 erasure resilience with constant rate and linear encoding/decoding. TR26-334 (multi-party adaptive information dissemination with Θ(1/√n) resilience), TR26-327 (process matrices), TR26-338 (unshardable codes), TR26-347 (GIR), TR26-346 (explicit O(1) tree codes) and algebraic VP ≠ VNP claims remain relevant. No recent report addresses single-tape crossing sequences, charged cumulative memory on SAT families, free-resource attention models, two-way interactive-code residuals under charged locality, or dynamic post-transport obligations after static equality transport.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims with Lean formalizations, VP≠VNP arithmetic results, neural SAT solvers, and graph-attention models, but none treat the charged single-tape model, Hartmanis-style equality constructions, free poly-dim attention residual bottlenecks, two-way interactive codes under charged transport, or synchronization/compatibility transport under free GANN resources. Hartmanis 1968 remains the classical quadratic barrier for separated equality constructions. Beame–Kornerup cumulative memory supplies general context only. Nunley arXiv:2606.18694 (Attention as Frustrated Synchronization) introduces FSN oscillator attention; prior residual collapses show it re-encodes comparison but does not escape physical co-location. The two-way model is interactive and (in the quantum case) non-classical; free evaluation is granted only as a local residual primitive.

Repository controls recover pure-function universal collapse, all prior residual collapses (indefinite-causal-structure / process-matrix, Hall-slack/Almost-2SAT, unshardable-code, algebraic-permanent, interactive-map-challenge, tree-code interactive, source-authenticated post-crossing, frustrated-synchronization, synchronization-bottleneck isolation, GIR-attention, free-GANN-synchronization-bottleneck), matching upper bound (eq. 41), and static ceiling Theorem 2 unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1. Prior mentions of TR26-335 treat it only as background, not as a residual collapse target.

## 2. Free-resource model and attempted construction

Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1, plus free two-way interactive coding, on any poly-size instance of the charged family:

- Unlimited polynomial-dimensional attention: any poly(N)-dimensional queries and keys, enabling free extraction of any poly-bit aggregate statistics or embeddings.
- Unlimited random access: equivalent to multi-tape or RAM access with no local crossing charge for reads inside a block.
- Exact Gaussian elimination: free solution of any linear system over GF(2) of poly size.
- Exact 2-SAT: free decision and witness extraction for any binary-clause formula (Horn, dual-Horn, implication graphs).
- Polynomial-depth global attention: free global all-pairs or multi-hop aggregation up to poly depth.
- Free GIR-style address assignment and short public hint (TR26-347 style).
- Free frustrated-synchronization oscillator attention (Kuramoto-Sakaguchi, FSN-style kernels with harmonics and delays).
- Free explicit O(1) tree codes of constant rate and relative distance (TR26-346).
- Free algebraic circuit evaluation for any poly-size arithmetic circuit, and free evaluation of the permanent or Hamiltonian cycle polynomial on poly-size matrices.
- Free linear (ℓ, s)-unshardable codes with constant locality and near-full unshardability parameter (TR26-338 style).
- Free protected Almost 2-SAT and logarithmic Hall-slack terminals.
- Free process-matrix computation with indefinite causal structure (TR26-327 style).
- Free two-way interactive codes with optimal erasure resilience (TR26-335 / TR26-320 style): free efficient encoding and interactive decoding that tolerate a 3/5 (quantum-classical), approaching 2/3 (binary or quantum-quantum) fraction of adversarial erasures on the residual symbols, with constant rate, so that residual map-difference components can be transported and recovered with high resilience to missing crossings.

**Attempted construction.** After a charged crossing of a selected cut in the ordered encoding I_{π,σ} = L_π M_r R_σ of the proper 3-CNF permutation family, encode residual map-difference components (or decision-sensitive equality challenges) into a free two-way interactive codeword. Use interactive participation of the "receiver" side (post-crossing configuration or free local solver) to recover the residual under a constant fraction of erased crossings, combined with free attention embeddings, GIR local reads, tree-code recovery, algebraic permanent evaluation, targeted-sampler probes, unshardable-code joint encoding, Hall-slack terminals and process-matrix evaluation, claiming that the improved erasure resilience and interactivity force an independent residual obligation outside pure functions of the input that escapes the synchronization bottleneck or reduces the asymptotic charged transport cost (fewer crossings needed for exact certification).

## 3. Obstacles and revision

**Obstacle 1 (pure-function collapse of two-way residual).** The complete configuration at the crossing, any two-way interactive encoding of residual map components, the interactive protocol transcript, the local recovery predicates, the decoder states, and any verification predicate are pure functions of the original ordered input blocks L_π, R_σ and the fixed deterministic machine A. By PURE-FUNCTION-UNIVERSAL-COLLAPSE1 and prior post-crossing residual collapses (including process-matrix, unshardable-code and tree-code), the entire two-way residual is jointly recoverable by free local solves and deterministic whole-run replay within a single authentication-and-comparison pass. No information outside the original input and A is introduced; the two-way code is an efficiently computable function of the residual bits already determined by the blocks. Interactivity and erasure resilience re-encode existing map information; they do not create new information outside pure functions. The quantum/process aspects are classicalized here as free local function evaluations.

**Obstacle 2 (charged transport of residual symbols).** Realizing the interactive recovery or verification of residual components still requires the head (or message) to transport the two-way coded residual symbols (or the residual map-difference information they encode) across the cut. Because the maps are incompressible, the information length remains Θ(r) (or Θ(N) in the encoding) in the worst case; even with constant-rate coding and constant-fraction erasure tolerance, the number of crossings needed to deliver or verify the residual is asymptotically the same as the classical argument of CHARGED-UNSAT-TRANSPORT1 (a constant-factor improvement does not change the Ω(N^{2}) order). Free two-way codes improve local recovery and resilience to missing symbols but do not eliminate the need to co-locate or transport the incompressible information. Free random access removes only local charge. Constant-rate interactive coding does not reduce the asymptotic charged transport of the global residual map across the cut.

**Obstacle 3 (static ceiling and matching upper bound).** Theorem 2 continues to bind: Dh ≤ N^{2}/8 and Dh^{2} ≤ N^{3}/27. The matching upper bound (eq. 41) realizes the quadratic/cubic orders on the family by authenticating and comparing the maps in one pass. Two-way residual encodings do not force additional independent work beyond what is already paid; they re-encode the comparison differently.

**Revision.** The free resources resolve every local fragment and every pure-function two-way interactive-code residual, but leave the global map-equality as the residual compatibility obligation. Attention (including GIR and FSN), tree-code interactive recovery, adaptive challenges, free permanent evaluation, targeted-sampler probes, unshardable codes, protected Almost 2-SAT / Hall-slack terminals, process-matrix evaluation and two-way interactive codes represent the comparison differently but do not escape the synchronization/compatibility bottleneck for exact decision on adversarial maps. The mathematical resource that must still scale is the physical co-location or charged crossing transport of the incompressible map information across the selected cuts. Interactive coding with optimal erasure resilience does not transfer to a free Boolean transport primitive under charged locality.

## 4. Residual transport under free GANN resources

On the ordered encoding of the proper 3-CNF permutation family, every fixed correct deterministic solver A that uses the free resources for local authentication, attention embeddings, GIR retrieval, FSN oscillators, tree-code recovery, adaptive map challenges, free algebraic circuit / permanent evaluation, targeted-sampler residual probes, unshardable-code residual recovery, protected Almost 2-SAT / logarithmic Hall-slack terminals, process-matrix / indefinite causal order evaluation and two-way interactive-code residual transport still satisfies, on some diagonal UNSAT input of encoded length N,

\[
T_A = \Omega_A(N^2), \qquad CM_{\mathrm{phys},A} = \Omega_A(N^3), \qquad CM_{\min,A} = \Omega_A(N^3).
\]

The orders are tight by the matching upper bound. This remains a concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently: it represents it differently but does not escape it.

## 5. Gates and scope

| Gate | Status and reason |
|---|---|
| Free local solvers / GIR / attention / FSN / tree codes / permanent / unshardable codes / Almost 2-SAT / Hall-slack / process matrices / two-way codes | PASS; resolve fragments and pure-function residuals without collapsing residual transport. |
| Two-way interactive-code residual | Collapses under deterministic whole-run replay and still requires charged transport of residual symbols (constant-factor resilience does not change asymptotic order). |
| Pure-function residuals | Universal collapse under deterministic replay. |
| Static ceiling | Still binds; Dh ≤ N^{2}/8 and Dh^{2} ≤ N^{3}/27. |
| Matching upper bound | Realized; collapses all pure-function candidates. |
| Synchronization/compatibility | Residual resource that must still scale. |
| Unrestricted SAT lower bound | Not claimed. Superpolynomial amplification remains OPEN. |
| P vs NP | OPEN. VP ≠ VNP (if accepted), unshardable codes, process-matrix NP solving and two-way interactive codes do not settle Boolean P vs NP in the charged single-tape model. |

No ETH, SETH, cryptographic or circuit-hardness assumption is used. The argument is confined to the deterministic single-tape charged model with the stated free local resources. External randomness, nondeterminism, quantum oracles or interactive oracles outside the free local evaluation would change the model and do not yield an unrestricted deterministic lower bound. Recent ETH-refuting claims (TR26-347), explicit tree codes (TR26-346), targeted samplers (TR26-345), algebraic VP ≠ VNP results, unshardable codes (TR26-338), process-matrix computation (TR26-327) and two-way codes (TR26-335/TR26-320) are compatible: free GIR, tree codes, samplers, FSN, permanent evaluation, unshardable encodings, protected Almost 2-SAT, indefinite causal order and two-way interactive coding collapse local retrieval/computation and re-encode comparison but leave charged transport intact.

## 6. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed. MANUSCRIPT REVIEWED; NO MATERIAL CHANGE to living LaTeX manuscripts.
