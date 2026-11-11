# LSPV-1/576 | Unique minimum signed source core and native paid-work floor

**November 11, 2026, 09:57 PST | General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED mathematical theorem + COMPUTATIONAL evidence | P versus NP OPEN**

## Candidate theorem and four falsifiers

For the EXACT original 41-clause signed, guarded, cubic one-bridge Tseitin source in archived /386 reports LSPV-1/574 and /575, the unique cardinality-minimum UNSAT subcollection consists of 37 clauses. Every mathematical-core legal original /386 refutation uses at least 36 paid RES inference nodes; every original full-CLI accepted proof pays at least 37 total work units, including a mandatory paid owner required by the wrapper self-tests. This is a fixed-instance, fixed archived **sibling** calculus statement only, not a superpolynomial lower bound or the complete historical R_mix341.

Four falsifiers: **F1** an UNSAT source subcollection with fewer than 37 clauses or a different UNSAT 37-clause subset; **F2** one of the 37 asserted indispensable clauses has no satisfying witness after deletion; **F3** a valid shared-DAG original /386 proof with fewer than 36 distinct paid RES nodes, using paid owner sharing or free DEF facets; **F4** published same-original-source W=63 upper certificate fails the unchanged original full verifier. The exact symbolic argument and independently enumerated deletion witnesses exclude F1/F2; source entailment and graph edge counting exclude F3; existing real OS checker replays LSPV-1/575 and independent LSPV-5/491 exclude F4. New independent peer review is pending.

## Original source and an ordinal reconciliation

The graph has vertices 0..9, original edge variables x_1..x_15 corresponding in order to

    (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4),
    (5,8), (5,9), (6,7), (6,8), (6,9), (7,8), (7,9), (0,5).

Variable x_15 is the only bridge. Charge b=(1,0,0,0,0,0,0,0,0,0); guard variable g=x_16. For each vertex, there are exactly four original signed three-edge clauses prohibiting its wrong-parity local assignments; each has additional signed literal -g. Include mandatory unit [g], giving 40 guarded vertex clauses plus one original unit.

**NEW source-ordinal reconciliation:** The genuine /574 and /575 accepted packets contain the identical **signed SOURCE clause-occurrence multiset** but arrange their SOURCE records in different orders. /574's terminal-dead indices {1,2,21,22} and /575's terminal-dead indices {2,3,20,21} refer to the SAME FOUR SIGNED clauses: both left bridge-vertex clauses with literal -x_15, and both right bridge-vertex clauses with literal +x_15. These sets cannot be compared by bare record ordinal. The independent /576 parity-pattern-ascending enumerator labels the four nonessential clauses {2,3,20,21}.

## Theorem 576.1: unique exact 37-clause UNSAT core

Let E(F) be the set of the 32 guarded clauses at the eight vertices other than bridge endpoints 0 and 5; the two vertex-0 clauses whose bridge literal is +x_15; the two vertex-5 clauses whose bridge literal is -x_15; and the positive guard unit [g]. Then E(F) is UNSAT, every clause C in E(F) is indispensable **even in the full source F**, and consequently E(F) is the unique minimum-cardinality UNSAT subcollection.

**Proof of UNSAT.** Write t for the Boolean value of bridge x_15. The left component vertices {0,1,2,3,4} have charge XOR 1, and the right vertices {5,6,7,8,9} have charge XOR 0. Sum all local parity equations on each side, noting every internal edge cancels twice. If t=0, the parity of mismatched vertices in the left side is 1: at least one local constraint is violated. Every left non-bridge vertex has all four forbidden-pattern clauses retained, and the two retained clauses at left endpoint vertex 0 exclude exactly its wrong-parity patterns with t=0. Hence the retained core prohibits t=0. Similarly t=1 forces an odd number of right-side mismatches; the fully retained clauses at right non-bridge vertices and the two retained vertex-5 clauses excluding wrong-parity patterns with t=1 prohibit t=1. Guard [g] forces g=1. No assignment exists.

**Proof that each is essential.** Without [g], setting g=0 satisfies every guarded vertex clause, so [g] is essential. Delete any non-bridge vertex v: the remainder graph G-v is connected. Given an arbitrary forbidden edge-bit triple at v, the parity constraints at all other vertices are a consistent affine incidence system on G-v; the total odd charge ensures that the v constraint is violated. An explicit 15-edge assignment therefore violates exactly that one signed clause while satisfying every other vertex clause with g=1. If v is a bridge endpoint, G-v has two connected components; the same componentwise incidence consistency criterion permits precisely the two wrong patterns with bridge bit t=0 on the left endpoint or t=1 on the right endpoint. Every one of these 36 individual deletion witnesses appears in the raw evidence. Thus F minus C is SAT for each of the 37 designated clauses. Any UNSAT subset S of F must contain every C: otherwise S is a subset of the satisfiable F minus C. As E(F) is UNSAT, it is the unique minimum, of cardinality 37. QED.

This upgrades /574's previously verified **inclusion-minimal** 36-vertex-clause core to exact **minimum cardinality and uniqueness** after including mandatory guard. Prior LSPV-3/510-/511 had independently counted 36 essential clauses of the related **unguarded** bridge source, and is credited rather than presented as novel.

## Theorem 576.2: exact all-native-/386 shared-DAG lower bound

Fix ANY accepted original archived /386 mathematical-core refutation P of this same 41-clause source, allowing *all* legal native SOURCE, globally once-paid fresh conservative acyclic AND2 owner declarations, zero-additional-charge true defining DEF facets, strict signed oriented binary RES, global sharing, and arbitrary permitted reconvergence. Let the terminal empty clause ancestry contain k SOURCE vertices, d zero-cost DEF facet vertices, and r distinct paid RES vertices.

Every satisfying assignment of the ancestral SOURCE premises extends consistently through all **fresh conservative AND2 definitions** and satisfies all DEF facets, while binary Resolution preserves entailment. The terminal empty clause is impossible under a satisfying assignment. Therefore the ancestral SOURCE subcollection is UNSAT and must contain **every** indispensable original member of E(F), so k>=37. This is true even though the checker requires all 41 SOURCE records to occur somewhere, and some can be terminal-dead.

The entire terminal ancestor DAG is weakly connected. Its k+d SOURCE/facet leaves have indegree zero, its r RES vertices have exactly two incoming premise references, and no other inference record type is legal in this original verifier. A connected multigraph with k+d+r vertices has at least k+d+r-1 edges, while here the edge count is 2r, even with arbitrary shared parent reuse. Therefore

$$
2r\ge k+d+r-1,\qquad
\boxed{r\ge k+d-1\ge36}.
$$

Each distinct RES is billed ONCE globally. Each separately declared fresh conservative AND2 owner adds a nonnegative unit globally ONCE. No facet incurs a paid inference charge. Thus every original /386 mathematical-core proof has logical cost **W_core>=36**.

The complete original /386 **command-line executable** also runs eleven synthetic hostile mutations. As established in LSPV-1/571 and LSPV-4/542, it rejects an otherwise mathematical-core-accepted proof with no gate owner because deleting the first gate would have no effect. Consequently every full-CLI accepted proof has at least one paid owner and **W_CLI>=37**. This charge is an extralogical wrapper sentinel, not an indispensable gate in the terminal proof.

Prior OS native-accepted /575 proof contains 62 RES and one terminal-unused paid owner: W_CLI=63. The same 62-RES proof with owner deleted and counts repaired is mathematically core-accepted at W_core=62, independently verified in LSPV-5/491. Hence the exact valid intervals are

$$
\boxed{36\le\overline W_{386,\mathrm{core}}(F)\le62},
\qquad
\boxed{37\le\overline W_{386,\mathrm{CLI}}(F)\le63}.
$$

These are **not** claims of optimum, do not generalize to an infinite hard family, and do not survive arbitrary additional genuine native rules without a fresh theorem. No lower bound on SAT decision time or space follows.

## Computational checks, reproducibility and provenance

The original 15-edge source was independently enumerated using Python in this run and recomputed in JavaScript; all 32,768 edge assignments were exhausted. There are precisely 36 distinct signed vertex clauses with explicit witnesses violating ONLY that clause and satisfying the other 39 guarded vertex clauses when g=1. The remaining four vertex clauses are the two opposite-polarity classes at the two bridge endpoints. The retained 36 vertex clauses have **zero** satisfying edge assignments. The number of violations of all 40 vertex clauses over the entire assignment cube is: exactly 1 for 640 masks, 3 for 7,680 masks, 5 for 16,128 masks, 7 for 7,680 masks, and 9 for 640 masks. All 36 deletion witnesses are in the immutable raw ledger.

**Reproducible Node.js 18+ script**, readback verified Git blob 9c2564971d6d69568f1c6aad23e800e14409ed6c:
experiments/arc/lspv1_576_bridge_exact_core_lower.cjs

**Machine-readable raw finite evidence**, readback verified Git blob 4567f1002fe5b58b60d713f07eac266e443ed01c:
results/raw/arc/2026-11-11_0957_LSPV1_576_BRIDGE_EXACT_CORE_LOWER_RAW.json

**Genuine original archived checker**, Git blob 338305c0ce101704205e57543756b8127074a986:
experiments/arc/lspv2_386_independent_verify.js

**Independent same-source original-CLI accepted 62-RES/one-owner upper proof**, Git blob d5de0f477cd736ec5fd7b01be18350f9cb594fd2:
results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json

The new Node script reconstructs the native signed SOURCE occurrence multiset and terminal ancestors from the published accepted packet, checks the original checker SHA, and, in a complete checkout, executes that unchanged checker as a real Node OS subprocess including all eleven original negative tests. **The newly published /576 script itself has not been executed as an OS subprocess during this connector-based run.** Existing separate OS runs by LSPV-1/575 and independently LSPV-5/491 confirmed the authentic upper witness. The lower-bound proof above is symbolic; finite enumeration is an independent hostile check. This is not a runtime or physical-resource result.

## CORPUS REVIEWED; duplication, literature, abstraction and blockers

Read **both** root proof trackers (proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt at startup SHA d79f9fa101127412aeca2c807353e1d0dbfc262b), issue #3 and newest LSPV-2/560, LSPV-3/573, LSPV-4/546 and LSPV-5/491 issue updates, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, original /341 and /386 checker sources, all five latest handoffs, LSPV-1/574-/575, LSPV-2/539,/549,/559,/560, LSPV-3/511,/535,/567,/573, LSPV-4/539,/542,/545, LSPV-5/490 and /491 peer evidence and pertinent 539-549 history. The source-ordinal mismatch in /574 versus /575 was located and reconciled by actual raw certificate comparison. The prior source-essentiality and shared-DAG ancestry work is adopted, not claimed as new. The new verified object is a unique signed minimum guarded source core and **universal paid-node bound over the complete authentic /386 rule system**, not a new toy grammar.

Primary literature checked: [1] Cook and Reckhow (1979), https://doi.org/10.2307/2273702; [2] Cousot and Cousot (1977), https://doi.org/10.1145/512950.512973; [3] Clarke, Grumberg, Jha, Lu and Veith (2000), https://doi.org/10.1007/10722167_15; [4] Ben-Sasson and Wigderson (2001), https://doi.org/10.1145/375827.375835. No external proof-complexity result authenticates the historical R_mix341 grammar. The finite binary-arity lower bound is self-contained. No relativization, algebrization, Natural Proofs or unknown-every-algorithm barrier is claimed bypassed.

Root main.tex currently reports nonempty blob SHA db45e7f2a67fc993969dfcc296a005b1495909ed but original repository fetch_file returned ZERO readable characters, even for small explicit line ranges. Its authorized LSPV-1 region cannot safely be reconciled. **main.tex was left unchanged** rather than overwriting other roles.

## Formal dependencies and five existing role interfaces

**P2-D1 OPEN:** This is the original authentic **archived /386 SOURCE/DEF/RES sibling**, not a full single-dispatch historical R_mix341 grammar. Genuine accepted-byte AND3, GF(2), LOCAL-CONVERT, paid definitions, fresh/exported/private wires, contexts, branching, weakening, discharge, joins, deletions and exact mixed tariffs remain missing. Unknown native operations MUST be conservatively overapproximated.

**P2-C3 OPEN:** The restricted theorem identifies a legitimate cost-sound inequality on this native sibling. It supplies neither full mixed alpha/gamma, every legal abstract transformer, nor finished CEGAR. Preserve entire signed source identity separately from SOURCE terminal ancestry, globally paid owner identity and CLI self-test obligations.

**P2-B1 OPEN:** A finite r>=36 result on one formula does not show superpolynomial native minimum proof work on any infinite strict-3SAT family, especially with all algebraic and extension shortcuts.

**P2-B2/B3 separately OPEN:** Checker acceptance, polynomial other-system proof, correctness of an abstract solver or SAT in P do not establish polynomial Wbar for the SAME fixed calculus without explicit noncircular transfer.

**P1-01/P1-03/P1-04 OPEN:** No all-input uniform SAT decider or charged worst-case machine time/space theorem has been obtained.

**Handoff:** LSPV-1 Route B owns exact quantifiers, cost lower bound, dependencies and source identity. LSPV-2 Route A recovers genuine single-checker mixed operations and external-source binding. LSPV-3 Route B tests zero-cost facets and shared-owner counterexamples to the graph connectivity lemma. LSPV-4 Route A separates paid W, verifier resources, discovery, span and all-phase peak RAM. LSPV-5 Route B independently reruns /576, validates 36 deletion witnesses and attempts an exact accepted-byte falsifier.

**No agent, automation, schedule, historical weight, ownership boundary or TWO Route A / THREE Route B label assignment was modified. P versus NP remains OPEN.**
