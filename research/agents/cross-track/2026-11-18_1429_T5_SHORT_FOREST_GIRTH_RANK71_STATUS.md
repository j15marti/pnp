# Cross-Track Synthesis 71: Short-Core Forest SAT Certificate and Girth/Rank Firewall

**2026-11-18 14:29 PST. P versus NP OPEN.** Restricted theorem; no unrestricted computational lower bound.

## Pre-search proposals
Frozen before search in local `PRESEARCH_CANDIDATES.md`: (1) multi-clone reverse Resolution proof translation and collapsed pivots; (2) fully charged source-aware contraction; (3) same-input common-clock UWI under derived-query costs; (4) WRAPPER necessity and matched-oracle firewalls. Following source review, the strongest surviving target is (2) combined with TMR-2/092's girth-versus-cyclomatic-rank obstruction.

## Newest specialist outputs read
- **Resource Contraction:** [TMR-1/096](https://github.com/j15marti/pnp/blob/tmr1-20261115-independent-lean060/research/agents/tmr-1/2026-11-18_1200_TMR1_PARSIMONIOUS_DAG_FLATTEN096.md), parsimonious four-layer depth-three T5 DAG reduction and paid bit-machine source costs; [TMR-3/091](https://github.com/j15marti/pnp/pull/299), mod-five two-terminal counting vectors and source-authenticated easy high-width bouquets.
- **Nonrelativizing Simulation:** [LSPV-5 MOVINGPROVENANCE1](https://github.com/j15marti/pnp/blob/main/research/main/2026-11-18_1406_MAIN_LSPV5_MOVINGPROVENANCE1_CONDENSED.tex), restricted polynomial last-writer provenance certificate, not universal PFCERT or a lower bound.
- **Universal Obstruction:** [TMR-2/092](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_1312_TMR2_T5_GIRTH6_BETA3_092.md), every simple oriented girth-six T5 source of cyclomatic number at most three is SAT.
- **Proof Transport:** [TMR-4/093](https://github.com/j15marti/pnp/blob/tmr4-20261118-1136-mixed-holonomy093/research/agents/tmr-4/2026-11-18_TMR4_T5_MIXED_LOCALITY_BARRIER093.md) and [PR #300](https://github.com/j15marti/pnp/pull/300), mixed SAT/UNSAT examples with high local/OBDD complexity but cheap global source-recognized decisions.
Also consulted newest project conversation context, prior Cross-Track 69/70 file audits, relevant Library sources, Drive's KRYLOVGUARD41 and wrapper quantifier review, repository history, and primary Resolution/CSP literature. Drive did not yield a newer November 18 specialist report.

## Theorem 71-A: Source-certified short-core forest
For the five-state tournament R(a,b) iff (b-a) mod 5 is 1 or 3, strip degree-zero/one vertices from a directed constraint multigraph, suppress maximal degree-two paths, recording orientations, and represent a pure cycle by one closed anchored path. Let K_<4 consist only of the resulting branch-to-branch paths of length 1, 2 or 3, counted as multiedges. **If K_<4 is a forest, G is SAT and a T5 witness is constructible in deterministic polynomial time.**

Proof: each traversed original arc contributes a two-element difference set {c,c+2} modulo five. A path of length ell has exactly min(5,ell+1) possible endpoint differences; thus ell>=4 permits every endpoint pair, regardless of directions. Each short path has nonempty forward and backward endpoint fibers. Color every tree of short paths outward; fill long paths independently for their now-chosen terminal colors; finally extend pruned trees. Check all original arcs. Source parsing, peeling, path recognition, transfer checks, color reconstruction and witness output are charged; a conservative sequential-bit implementation uses time O((L+1)^3) and writable space O((L+1)^2) for source length L. No oracle, recursion or WRAPPER is needed.

## Theorem 71-B: Girth/cyclomatic-rank obstruction
For any simple oriented UNSAT T5 source with undirected girth g>=7 and cyclomatic number beta=|E|-|V|+c:
```
g <= 6(beta-1)      and      beta >= ceil(g/6 + 1).
```
Equivalently, when beta>=2 and g>6(beta-1), the source is SAT. Proof: in each connected 2-core with beta>=2, suppress degree-two paths. Every kernel vertex has degree>=3, and sum(deg-2)=2(beta-1), so there are at most 2(beta-1) branch vertices. Any short-edge kernel cycle contains at most that many edges, each an original path of length<=3. It would give an original cycle of length<=6(beta-1), contradicting girth. Hence short edges form a forest; invoke Theorem 71-A. Tree and unicyclic components of girth>=7 are SAT directly. This is a structural necessary condition for UNSAT, **not** a SAT decision-time lower bound. TMR-2/092 yields the stronger beta>=4 bound at girth six.

## Executed hostile tests
- Exhaustively audited **4,166** directed multiarc/no-loop source cases on up to four vertices: **273** certified SAT with explicit witnesses, **400** other SAT inputs conservatively declined and **3,493** UNSAT inputs declined. No false-positive witness.
- **150** randomly oriented long-path subdivided cliques and **150** tree-short/other-path-long hybrid cores also received verified witnesses. A K8 core example has beta=21, 121 vertices, 141 arcs, and a simple polynomial-time witness.
- Independent checker ran **316** path support tests over every orientation word of lengths 1 through 7, including brute internal enumeration for lengths<=5. Supports are 2,3,4,5,5,5,5. **Zero failures.**
- Hostile controls include all 16 orientations of a four-cycle, 15 loop cases and an opposed-arc digon. The certifier is deliberately incomplete, not an unrestricted T5 SAT algorithm.
Code and full raw data are in the accompanying conversation reproducibility bundle; physical Turing-machine microsteps and independent external review remain open.

## Explicit proof DAG
| Implication | Status |
|---|---|
| General T5-CSP NP-complete | Established published classification |
| T5 path length>=4 has full endpoint support | PROVED |
| Short-core forest => SAT and constructive witness | **PROVED restricted theorem** |
| Girth>=7 UNSAT => beta>=ceil(g/6+1) | **PROVED structural theorem** |
| TMR-2/092 girth>=6 beta<=3 => SAT | Project finite-core theorem, independent external review OPEN |
| Degree-five depth-three DAG parsimony and canonical CNF retraction | Synthesis 70, restricted |
| Multi-clone full reverse Resolution proof-file translator | OPEN |
| Same-input common-clock UWI against all source-aware candidates | OPEN |
| Necessary nonrelativizing WRAPPER resource hinge | OPEN |
| Arbitrary-decider-to-Resolution lower-bound transport | OPEN |
| Unrestricted T5 superpolynomial time lower bound; P != NP | **OPEN** |

UWI must use the *same final original input*, a *common clock*, and charge all generated-query algorithms. An unrestricted class allowing input-specific hardcoded advice cannot satisfy a single-input universal failure claim without additional uniformity/code-size constraints. Resolution restrictions/OBDD width do not measure arbitrary decision computation.

## Next assignments
1. **Resource Contraction:** exact source bit-parser, 2-core and transfer-path SAT recognizer with every read, parse, bit operation, memory and emitted witness charged. Compare with TMR-3's source-aware vector contractions.
2. **Nonrelativizing Simulation:** locate a WRAPPER operation that cannot be performed by this source-aware algorithm or a legal derived-query reduction. Keep oracle machines matched; no lower-bound claim from restricted endpoint certificates.
3. **Universal Obstruction:** determine whether girth-six, beta-four UNSAT sources exist; use beta>=ceil(g/6+1) for growing-girth screening and high-beta subdivided-clique SAT families as controls.
4. **Proof Transport:** implement a checked multi-clone Resolution-with-weakening proof-file retraction, including tautological images and collapsed pivots. Do not infer arbitrary-decider lower bounds.

**References:** Bang-Jensen, Hell & MacGillivray (1988), DOI 10.1137/0401029; Atserias & Dalmau (2008), DOI 10.1016/j.jcss.2007.06.025; Focke, Marx & Rzążewski (2024), DOI 10.1145/3640814.

Independent mathematical review and native bit-machine replay are outstanding. **P versus NP OPEN.**
