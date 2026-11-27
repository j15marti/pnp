# DYNAMIC-COMPATIBILITY-OBLIGATION1-PURE-FUNCTION-COLLAPSE1

**Research date:** 26 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, GANN-FREE-RESOURCES-COMPATIBILITY1, FREE-RESOURCE-RESIDUAL-TRANSPORT1, ADAPTIVE-CUT-COLLAPSE1  
**Status:** PROVED/EXACT. Every residual obligation that is a pure function of the original ordered input blocks and the fixed deterministic machine collapses under free local GANN resources, deterministic whole-run replay, and the matching upper bound. Free poly-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT and polynomial-depth global attention leave the residual map-compatibility transport intact. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction and obstacle analysis only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh primary-literature search (26 November 2026): Hartmanis 1968 one-tape crossing sequences remain the classical quadratic barrier for separated equality constructions; no recent single-tape cumulative-memory SAT lower bounds or pure-function residual variants located beyond Beame–Kornerup general context. ECCC TR26-346 (explicit O(1) tree codes), TR26-345 (targeted samplers), TR26-344 (complex-analytic Gap Hamming completions), TR26-342 (exhaustive search hard for hyperclique/OV in constant depth), TR26-331 (o(N log N) sorting on multitape TM) do not address free-resource attention residuals, pure-function post-transport obligations, or charged permutation families.

Organization-scoped searches on OpenAI, Anthropic, Google Research, DeepMind, and xAI-org yield ETH-refuting 2^{o(n)} #k-SAT claims, formalizations (anthropics/formal-math, openai/math), VP≠VNP arithmetic results, and neural SAT solvers, but none treat the charged single-tape model, Hartmanis-style equality constructions, or free poly-dim attention residual bottlenecks. Repository controls recover FREE-RESOURCE-RESIDUAL-TRANSPORT1, ADAPTIVE-CUT-COLLAPSE1, NESTED-CUT-COLLAPSE1 and matching upper bound (eq. 41) unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Pure-function residual theorem

**Theorem (pure-function residual collapse under free resources).**  
Grant the free resources of GANN-FREE-RESOURCES-COMPATIBILITY1: unlimited polynomial-dimensional attention, unlimited random access, exact Gaussian elimination, exact 2-SAT, and polynomial-depth global attention. Let F be any source-authenticated proper 3-CNF family whose decision depends on equality of two incompressible maps π, σ encoded in ordered left/right blocks L_π, R_σ as in CHARGED-UNSAT-TRANSPORT1 (eqs. 8–22). Suppose a residual obligation ρ is any deterministic function of the original ordered input blocks and the fixed machine A (including any intermediate configuration, adaptive cut index, sequential unlock bit, attention aggregate, or hash of the maps). Then every fixed correct deterministic solver A that uses the free resources for local authentication and fragment solution still satisfies, on some diagonal UNSAT input of encoded length N,

\[
T_A = \Omega_A(N^2),\qquad
CM_{\mathrm{phys},A} = \Omega_A(N^3),\qquad
CM_{\mathrm{min},A} = \Omega_A(N^3).
\]

Moreover, the residual ρ itself can be generated and verified inside the same charged (or free-access) pass already accounted for by the matching upper bound of CHARGED-UNSAT-TRANSPORT1 (eq. 41). No additional independent post-transport crossings are forced. The static ceiling of Theorem 2 (eq. 44) continues to bind.

**Proof.**  
Free exact 2-SAT and Horn/dual-Horn solvers authenticate the selector, left clauses, right clauses and middle chain and confirm the exact decision relation (eq. 9/16). Exact GE handles residual linear dependencies from the compiler. Poly-dimensional and poly-depth attention extract embeddings of the left block L_π and right block R_σ or the explicit map lists themselves. Unlimited random access removes local crossing charges inside a block.

Because ρ is a pure function of the original blocks and the fixed machine, deterministic whole-run replay of the source blocks, using free local solvers and attention to extract both maps, computes ρ in a single joint pass. The subsequent equality transport across any selected cuts is identical to the static case already charged by the matching O(N^{2})/O(N^{3}) solver. Free resources re-encode the residual dependence inside aggregates or embeddings but do not force additional independent crossings beyond those already required for the joint equality of the incompressible maps. Nested, sequential, adaptive or path-dependent dependence collapses exactly as in prior documents.

Thus every pure-function residual collapses. The mathematical resource that must still scale remains the physical co-location or transport of each incompressible map across its selected cuts; attention represents the comparison differently but does not escape the residual map-compatibility transport.

## 3. Interpretation for attention and the synchronization bottleneck

Unlimited polynomial-dimensional and polynomial-depth attention represents the map comparison differently—via embeddings, soft-weighted aggregates or multi-hop message passing—but does not escape the synchronization/compatibility bottleneck for exact decision on adversarial (incompressible) maps. Soft statistics alone do not certify exact equality on incompressible permutations without retaining or re-accessing the source data. Any residual that remains a pure function of the original input can be paid by the single joint comparison already present in the matching upper-bound solver.

The concrete test remains: attention re-encodes the equality test inside its weights or aggregates but does not eliminate the quadratic time / cubic cumulative memory demand of the charged model on this family.

## 4. Gates and scope

| Gate | Status and reason |
|---|---|
| Free local solvers | PASS; resolve fragments and compute pure-function residuals without generating independent residual information. |
| Deterministic replay | Collapses pure functions of original blocks. |
| Static ceiling | Still binds; pure-function nesting does not exceed Dh ≤ N^{2}/8 or Dh^{2} ≤ N^{3}/27. |
| Matching upper bound | Realized by joint comparison. |
| Attention representation | Differs from direct comparison but does not escape residual transport. |
| Unrestricted SAT lower bound | Not claimed. |
| P vs NP | OPEN. |

No ETH, SETH, cryptographic or circuit-hardness assumption is used. The argument is confined to the deterministic single-tape charged model with free local GANN resources.

## 5. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed. MANUSCRIPT REVIEWED; NO MATERIAL CHANGE to living LaTeX manuscripts.
