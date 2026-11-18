# Cross-Track Synthesis 69 | 2026-11-18 12:31 PST | Exact T5 DAG Resolution retraction

**NEW: PROVED restricted bidirectional Resolution proof transport. P versus NP OPEN.** Independent mathematical/kernel review pending.

## Four proposals frozen before searching
1. Reverse Resolution transport for exact fixed gadget expansions.
2. Fully charged source-aware contraction and recognition.
3. Same-input UWI quantifiers including derived-query witness extractors.
4. Symmetry/relative-color transport and necessary nonrelativizing WRAPPER audit.

## Newest primary specialist reports reviewed
- Resource Contraction TMR-1/096: https://github.com/j15marti/pnp/blob/tmr1-20261115-independent-lean060/research/agents/tmr-1/2026-11-18_1200_TMR1_PARSIMONIOUS_DAG_FLATTEN096.md
- Resource Contraction TMR-3/090: https://github.com/j15marti/pnp/blob/research/tmr3-t5-block-cut090-20261118/research/agents/tmr-3/2026-11-18_1121_TMR3_T5_BLOCK_CUT_FACTOR090.md
- Nonrelativizing Simulation LSPV-5 SKETCHCRT1: https://github.com/j15marti/pnp/blob/main/research/main/2026-11-18_1206_MAIN_LSPV5_SKETCHCRT1_CONDENSED.tex
- Universal Obstruction TMR-2/090: https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_1112_TMR2_T5_SIGGERS_DIGON090.md
- Proof Transport TMR-4/093: https://github.com/j15marti/pnp/blob/tmr4-20261118-1136-mixed-holonomy093/research/agents/tmr-4/2026-11-18_TMR4_T5_MIXED_LOCALITY_BARRIER093.md
Also checked issue #3, repository commits, past project chat context, Library circuit-contraction audit, Google Drive (older September proof state and contraction notes), Atserias-Dalmau 2008 and Ben-Sasson-Wigderson 2001.

## Theorem A: exact canonical one-hot CNF retraction

Fix R(a,b) iff (b-a) mod5 belongs to {1,3}. TMR-1/096 replaces every nonisolated vertex v by p_v,q_v,a_v,b_v and edges (p,a),(p,b),(q,a),(q,b),(a,b), plus a cross edge p_u->q_v for each source arc u->v. Isolates remain unchanged. The new graph D(G) is a directed four-layer DAG with n+3k vertices and m+5k arcs, k nonisolates; its satisfying T5 assignments are in bijection with source assignments by (p,q,a,b)=(x,x,x+3,x+1).

Let F_G and F_D be the canonical **five-atom one-hot CNF** encodings, with eleven one-hot clauses per vertex (one at-least-one, ten at-most-one) and fifteen forbidden-pair clauses per arc. Define a positive-literal substitution
 sigma(P_v,c)=X_v,c;
 sigma(Q_v,c)=X_v,c;
 sigma(A_v,c)=X_v,c-3;
 sigma(B_v,c)=X_v,c-1
with indices modulo 5 and isolates fixed.

**Exact clause-set identity:** sigma(F_D)=F_G (duplicate clauses collapsed). One-hot clauses map to one-hot source clauses. For any of the five internal gadget arcs, the shifted same-source states always satisfy R, so forbidden pairs must map to distinct source colors, hence source at-most-one clauses. Cross arcs map to source arc clauses. Original p-vertex one-hot clauses and cross arcs supply every original axiom. This covers loops, opposed arcs, empty graphs and isolates.

## Theorem B: genuine reverse Resolution proof translation

For any canonical Resolution refutation pi_D of F_D with S lines and width w, substitute sigma in each clause. Axioms become genuine F_G axioms. If the target proof resolves C∨Y with D∨¬Y, their images resolve on sigma(Y) to a **subclause** of sigma(C∨D). Append at most one weakening to obtain exactly the latter. Each target proof line costs at most two source lines; substitution and weakening do not increase width. Therefore:

 **ResWithWeakSize(F_G) <= 2 ResSize(F_D)**, and **ResWithWeakWidth(F_G) <= ResWidth(F_D)**.

This is an all-proof, source-checkable **reverse** transport theorem for this *specific* DAG flattening, not for arbitrary high-girth edge gadgets or unrestricted SAT deciders.

## Theorem C: forward proof translation

For each original vertex, the fixed equality gadget has precisely one extension for equal terminal colors and none for unequal colors. Resolution completeness on its fixed 20 Boolean atoms and discharge of terminal assumptions derive all clauses forbidding mismatched p/q colors, with absolute constant proof size and width per vertex. Combine q-at-least-one with mismatch clauses to derive p_j=>q_j, then resolve with each actual cross-arc forbidden pair to derive the original forbidden clause on p_u,p_v. Replay any source Resolution proof using p-colors.

Hence there exist absolute constants C,W0 with:
 **ResWithWeakSize(F_D) <= ResWithWeakSize(F_G)+C(n+m)** and
 **ResWithWeakWidth(F_D) <= max(ResWithWeakWidth(F_G),W0)**.

Theorem C has a mathematical fixed-gadget completeness proof; explicit numeric C was not claimed or tested.

## Hostile computational audit

- Exhaustive **531** directed source graphs for n=0,1,2,3, including loops and opposed arcs, checking clause-set identity on **216,161** target CNF axioms.
- Another **200** seeded random graphs up to 15 vertices; **411** canonical witness validity checks.
- Generated a **234-line complete Resolution refutation** of the loop-free four-layer 4-vertex, 6-arc image of a one-vertex self-loop: 134 input axioms, 100 Resolution inferences, width 6.
- Directly translated to a **236-line source refutation**, with 100 Resolution steps, **2 necessary weakening repairs**, width 6, ending with empty clause.
- An **independent separate standard-library Python checker** rebuilt source/target axioms and replayed all proof parents, resolvents, weakening steps and final empty clauses. Zero failed assertions.
- Full local artifact bundle includes the 15k-character mathematical report, both JSONL certificates, generator, independent checker, raw results, frozen proposals and SHA-256 manifest.

This catches a false naive statement: substituting a collapsed pivot does NOT always give an *identical* Resolution resolvent. The correct transport includes weakening (two such steps occurred).

## Explicit proof DAG

| Claim | Status |
|---|---|
| T5-HOM NP-complete | ESTABLISHED, Bang-Jensen/Hell/MacGillivray 1988 |
| TMR-1 four-layer DAG count-preserving compiler | PROVED restricted, independent review pending |
| Canonical sigma(F_D)=F_G | **PROVED A** |
| Every expanded Resolution proof -> source Resolution+weakening | **PROVED B**, independent replay |
| Every source Resolution proof -> expanded Resolution+weakening | **PROVED C**, constant-gadget derivation |
| Source superpoly Resolution hardness -> DAG-image superpoly Resolution hardness | CONDITIONAL B, specific proof system |
| Same-arrow arbitrary-decider lower bound | **OPEN**, no proof-system-to-unrestricted-machine transport |
| Uniform all-input contraction with charged access/generation/workspace/recursion | **OPEN** |
| Necessary nonrelativizing WRAPPER operation | **OPEN** |
| Same-input common-clock universal witness obstruction | **OPEN** |
| P versus NP | **OPEN** |

## Four next specialist assignments

**Resource Contraction (TMR-1/TMR-3):** Compose fully charged source recognition with the DAG/compiler plus block-cut cover; measure reading, parsing, canonicalization, all output, integer arithmetic, workspace and recursion on noncanonical mixtures.

**Nonrelativizing Simulation (LSPV-5):** Seek one truly indispensable nonrelativizing WRAPPER hinge surviving the literal-substitution and derived-decision-query shortcuts, using the same-oracle obstruction; absent such a hinge, leave OPEN.

**Universal Obstruction (TMR-2):** Treat the new bidirectional proof compiler as a cheap challenger; quantify over every polynomial witness algorithm on one same final source and clock, including adaptive decision queries, and search for growing obstructions not recognized by source-only parsers.

**Proof Transport (TMR-4):** Independently kernel-check A/B/C and attempt a genuine reverse transport for C9 or the 65-vertex girth-eight gadget. Do not identify Resolution, OBDD, FBDD and arbitrary algorithms.

## Literature
[1] Atserias & Dalmau (2008), JCSS, https://doi.org/10.1016/j.jcss.2007.06.025
[2] Ben-Sasson & Wigderson (2001), JACM, https://doi.org/10.1145/375827.375835
[3] Bang-Jensen, Hell & MacGillivray (1988), SIDMA, https://doi.org/10.1137/0401029

**Final status: This closes one previously OPEN restricted reverse proof transport arrow, but leaves every computational separation arrow OPEN.**
