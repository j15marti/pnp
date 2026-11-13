# LSPV-3/609: Operational native acceptance cannot be conflated with semantic UNSAT

**2026-11-13 01:24 PST | LSPV-3 Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED theorem and COMPUTATIONAL fresh hosted original-checker replay | P versus NP OPEN.**

## Candidate and four precise falsifiers

Candidate: an abstraction covering **every** accepting execution of the recovered /341 SOURCE/AND3/XOR checker cannot also interpret **every** reached acceptance goal as a mathematically sound refutation of the same in-packet signed CNF.

F1: the pinned /341 SAT-source packet is rejected by the unchanged original mathematical checker. F2: the alleged satisfying assignment fails one of the 48 exact signed SOURCE clauses. F3: restoring the string-typed charge to a canonical integer permits the same malformed-source certificate to pass. F4: corrupting a signed clause or terminal GF(2) row is accepted. All were tested: F1 and F2 did not occur, F3 and both F4 mutations rejected. The distinction is a theorem about the original **restricted /341** checker, not the missing full R_mix341.

## Corpus, provenance and prior art

Read both root trackers (proof1 blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 blob f678f707880da4dfc97dabf778430c6dc816cb1f through immutable-blob fallback), issue #3, AGENTS.md, CODEX.md, research skill, current handoffs, original /341 and /386 checker source, LSPV-3/539 and /549, LSPV-4/539, LSPV-2/549 and /582, LSPV-3/589 and /606-608, contemporary Grok and Claude records, and the primary proof-system/abstract-interpretation/CEGAR literature. The relevant LSPV reports 539-549 and later work already distinguish proposed CANON grammars from historical checker syntax.

**Prior art, not newly claimed:** LSPV-3/606 established the original accepted SAT-source packet and malformed support-string behavior. LSPV-3/589 already constructed a separate stricter source-bound soundness gate. LSPV-2/549 and LSPV-3/607-608 already proved that two individually recovered original checkers do not authenticate one shared mixed-rule dispatcher.

**New /609 increment:** a precise impossibility theorem for a conflated abstract goal, independent exhaustive rechecking of the source SAT witness and exact signed CNF, fresh original-body acceptance and three hostile controls, and a standalone complete Node OS regression program. The Node OS program was published and syntax-checked but not run in an OS subprocess during this turn.

Authority: original /341 checker, experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Previously accepted exact packet: results/raw/arc/2026-11-12_2219_LSPV3_606_X10_NATIVE341_ACCEPTED.json, blob 1e19a9d2b84daa1fc8c29468873ad62e0d67e105. Neither is the complete historical R_mix341 mixed checker.

## Theorem 609.1: impossibility of a single logically sound abstract acceptance goal

Let $B_{341}$ be all finite JSON byte strings accepted by the **specific** archived /341 checker, and let $F(b)$ denote the signed CNF stated by the clauses of packet $b$. Suppose an abstract transition system $A$, abstraction map $\alpha$, and terminal predicate $G$ satisfy BOTH:

(1) **Acceptance coverage:** every $b\in B_{341}$ has an abstract run from $\alpha(b)$ to $G$; in particular, all native accepted malformed-source traces are retained.

(2) **Sound semantic goal:** for every such run reaching $G$, the original signed source formula $F(b)$ is UNSAT.

Then **no such triple $(A,\alpha,G)$ exists.**

**Proof.** Take the pinned certificate $b_*$ above. The unchanged original checker accepts it (5,155 native assertion groups), so $b_*\in B_{341}$. Independent evaluation of its 48 actual signed clauses establishes that the assignment 000000010010000001 satisfies all 48. Exhaustive checking of $2^{18}=262144$ assignments finds 64 satisfying models. Thus $F(b_*)$ is SAT. Condition (1) gives an abstract goal for $b_*$ and condition (2) declares the same formula UNSAT, a contradiction. QED.

No nonnegative cost transformation can repair this *logical* contradiction while retaining both assumptions; the theorem is independent of what fixed paid weights are chosen. It does not rule out two **different** goal predicates, one operational and one source-bound logical, or a separately proven sound repair that excludes some accepted malformed-source packets.

The exact source-type defect is visible in the original program: charges[5] is the **string** "0". The global XOR computation coerces that value to zero, whereas the strict comparison of local forbidden-pattern parity with the same string is type-sensitive. Consequently, malformed original clauses pass the original source check. Changing charges[5] to integer 0 causes original-checker rejection at source forbidden pattern parity. This is a checker-language weakness, not an authentic new SAT inference.

## Native replay and independent verification

| Exact test | Result |
| --- | --- |
| Full original /341 checker on pinned accepted packet | ACCEPT, 5,155 assertion groups |
| SAT witness on 18 edge variables | 48 of 48 source clauses satisfied |
| Exhaustive signed-source assignments | 64 satisfying out of 262,144 |
| Change only charges[5] from string to integer | REJECT: source forbidden pattern parity |
| Alter first SOURCE literal to 999 | REJECT: signed incidence mismatch |
| Alter final GF(2) RHS to 0 | REJECT: bad GF2 elimination |

The unmodified original mathematical checker was compiled and run in hosted V8 with a filesystem input adapter. The 18-bit CNF SAT count was independently recomputed; the source material is directly extracted from the packet, NOT an independently trusted historical external-source file. Original 47 paid inference nodes, parent DAG, and witness records are retained. Distinct resource axes: logical work W=47; packet evidence 28,120 UTF-8 ASCII bytes; actual OS time, proof span and peak space were not measured. The authored standalone Node program was syntax-validated but not executed in an OS subprocess; full preflight and LaTeX compilation were also not run.

Published machine artifacts, with complete content and Git blob SHA readback:
- Signed DIMACS extraction: results/raw/arc/2026-11-13_0124_LSPV3_609_SAT_SIGNED_SOURCE.cnf, fe1fbde1c74ec1caf052fe009bf96c14ab229303.
- Complete standalone replayer: experiments/arc/lspv3_609_goal_soundness_no_go.cjs, e62d6f54e2f19588d6f150d91f546350f9c408c2.
- Hosted source/body raw verification: results/raw/arc/2026-11-13_0124_LSPV3_609_SAT_GOAL_NO_GO_HOSTED_RAW.json, 049fafc056078d8edc0383682836a043c7c18e6c.

## Consequence for the open chain

**P2-D1 OPEN.** The missing complete historical accepted-byte dispatcher must still be authenticated with exact SOURCE binding, RES, AND3, GF(2), LOCAL-CONVERT, paid DEF facets, fresh/private/exported wires, contexts, branching, discharge, joins, deletion, and shared DAG rules. None of their unknown behavior is declared illegal on evidence from these two checkers.

**P2-C3 OPEN.** The necessary *dual-goal interface* is

$$
G_{\mathrm{accept}}(b)=\text{archived checker acceptance},
\qquad
G_{\mathrm{logical}}(b,F)=\text{sound, externally source-bound UNSAT proof}.
$$

A CEGAR replay must preserve genuine historical checker acceptances as operational paths, but a malformed native-accepted packet cannot be promoted to a mathematical refutation. A sound abstraction of a **different, strictly repaired** calculus must be identified as such, not silently substituted as the complete historical byte grammar. The true full-calculus model must preserve source provenance, assumptions, complete paid shared DAG and exact fixed work separately from evidence length and machine resources.

**P2-B1 OPEN. P2-B2/B3 separately OPEN.** No general SAT machine or minimum-proof lower bound follows. P versus NP OPEN.

## Primary methodological references

1. Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, *Journal of Symbolic Logic* 44 (1979), 36-50, https://doi.org/10.2307/2273702.
2. Cousot and Cousot, Abstract interpretation, POPL 1977, https://doi.org/10.1145/512950.512973.
3. Clarke et al., Counterexample-Guided Abstraction Refinement, CAV 2000, https://doi.org/10.1007/10722167_15.
4. ECMA-262, Structured Data, https://tc39.es/ecma262/multipage/structured-data.html.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Five original roles, schedules, historical two Route A/three Route B allocation, ownership, and fixed weights untouched. No automations modified.
