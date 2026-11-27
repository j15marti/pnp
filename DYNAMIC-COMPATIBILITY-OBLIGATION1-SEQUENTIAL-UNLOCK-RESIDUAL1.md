# DYNAMIC-COMPATIBILITY-OBLIGATION1-SEQUENTIAL-UNLOCK-RESIDUAL1

**Research date:** 26 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1, FREE-RESOURCE-RESIDUAL-TRANSPORT1, PATH-DEPENDENT-COLLAPSE1, NESTED-CUT-COLLAPSE1  
**Status:** Sequential-unlock residual candidate collapses under free local solves, deterministic whole-run replay and the matching upper bound. Free poly-dimensional attention, random access, exact GE, exact 2-SAT and poly-depth global attention leave the residual map-compatibility transport intact. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN for superpolynomial amplification. P vs NP OPEN.  
**Review:** Internal construction and obstacle analysis only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh primary-literature search (26 November 2026): Hartmanis 1968 one-tape crossing sequences remain the classical quadratic barrier for separated equality constructions; no recent single-tape cumulative-memory SAT lower bounds located beyond Beame–Kornerup general context. ECCC TR26-346 through TR26-331 address tree codes, samplers, Gap Hamming, constant-depth hyperclique/OV and multitape sorting; none treat free-resource attention residuals or post-transport sequential obligations on charged permutation families.

Organization-scoped searches: Anthropic formal-math (commit 11b6c7e) and OpenAI math (VP≠VNP manuscripts) establish arithmetic circuit separations that do not transfer to Boolean SAT decision in the charged single-tape model. Neural SAT solvers (SAT-GATv2, Attn-JGNN) and synchronization models of attention (frustrated Kuramoto) represent equality differently but supply no charged crossing lower bound. Repository controls recover FREE-RESOURCE-RESIDUAL-TRANSPORT1, NESTED-CUT-COLLAPSE1 and matching upper bound (eq. 41) unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Candidate sequential-unlock family

Attempt: construct a source-authenticated family of proper 3-CNF formulas containing two independent incompressible maps π_{1}, π_{2}. The encoding places a first middle block M_{1} separating left/right fragments of π_{1}, then a charged unlock token that is released only after the first equality bit is obtained, then a second middle block M_{2} for π_{2}. The decision is UNSAT iff both maps match their duals. Free local 2-SAT/GE/attention resources authenticate each fragment; the residual is the sequential transport of each map across its own cuts after the previous bit is known.

The candidate claimed that the second transport cannot be paid by a pure function of the original input blocks alone, because the unlock depends on the first comparison outcome.

## 3. Collapse under free resources and deterministic replay

**Obstacle theorem.** On every diagonal input of the attempted sequential family the second residual is a pure function of the original ordered blocks once the first comparison has been performed. Deterministic whole-run replay of the source blocks, using free exact 2-SAT and poly-dimensional attention to extract both map lists, computes both equality bits in a single joint pass. The unlock token is then a free local function of the first bit; no independent post-transport information is generated. The matching upper-bound solver of CHARGED-UNSAT-TRANSPORT1 (eq. 41) authenticates the whole formula and compares both maps in O(N^{2}) time and O(N^{3}) physical CM, realizing the bound already charged by the static ceiling (eq. 44). Nested cuts collapse exactly as in NESTED-CUT-COLLAPSE1: free random access and attention re-encode the sequential dependence inside aggregates but do not force additional independent crossings beyond those already required for the joint equality.

Thus the sequential-unlock residual collapses. The mathematical resource that must still scale remains the physical co-location or transport of each incompressible map across its selected cuts; attention represents the sequential comparison differently but does not escape the residual map-compatibility transport.

## 4. Gates and scope

| Gate | Status and reason |
|---|---|
| Free local solvers | PASS; resolve fragments and unlocks without generating independent residual information. |
| Deterministic replay | Collapses pure functions of original blocks. |
| Static ceiling | Still binds; sequential nesting does not exceed Dh ≤ N^{2}/8. |
| Matching upper bound | Realized by joint comparison. |
| Attention representation | Differs from direct comparison but does not escape residual transport. |
| Unrestricted SAT lower bound | Not claimed. |
| P vs NP | OPEN. |

No ETH, SETH or circuit-hardness assumption is used. The argument is confined to the deterministic single-tape charged model with free local GANN resources.

## 5. Next named lemma

Construct a source-authenticated, decision-sensitive family in which a residual obligation is revealed only after a charged crossing and whose information cannot be recovered by deterministic replay of the original input blocks alone (outside pure functions of the input and machine), or prove that every deterministic attempt collapses under paid joint preprocessing and free local solves. The residual map-compatibility transport under free GANN resources remains the concrete test of whether attention escapes the synchronization/compatibility bottleneck or merely represents it differently.

No agent settings, public proof claims or historical files changed. MANUSCRIPT REVIEWED; NO MATERIAL CHANGE to living LaTeX manuscripts.
