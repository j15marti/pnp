# LSPV-1/489: Paid unit-assumption discharge of a nonaffine three-template cover

**November 7, 2026 PST | Route B | PROVED/RESTRICTED (standard Resolution argument applied to authenticated guarded cover), COMPUTATIONAL (finite explicit certificate) | P versus NP OPEN.**

**Exact proof-chain IDs:** material refinement [P2-F13]; remaining OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]; cross-route [P1-X1], [P1-01], [P1-03], [P1-04]. No change to historical R_mix341 rule language or weights.

## IDEA -> SEARCH -> ITERATE and falsifiers

**Initial hypothesis:** The 3-template local cover from LSPV-1/488 permits fully paid, assumption-scoped recombination of branch refutations by ordinary source-authenticated Resolution, without adding a case-split, weakening, or branch-discharge inference rule. An independent cover may use fewer RES inferences than the previous 18-step witness.

**Four falsifiers:** F1, every unit-assumption elimination implicitly needs weakening; F2, one AND-case is skipped or branch-local conclusions leak across branches; F3, an alleged cover output is not derivable from authentic defining facets; F4, a 17-step candidate has a wrong signed RES pivot. None occurred in the **separate** ordinary RES plus paid conservative Tseitin definition calculus. Historical applicability remains OPEN.

**Continuity and actual sources:** Read both full root trackers (initial proof1 SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2 SHA ad317008264aa0f0c75cdd5fc6a059437f16a815), governing Nov 2 five-role handoff, AGENTS.md, CODEX.md, pnp-research skill, issue #3 with newest comments, LSPV-1/488, LSPV-3/477, LSPV-5/413/418, Grok GROKPROOF/2026-11-07_1920_PROGRESS.md and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Required repository change-aware reads: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. None authorizes historical R_mix341 rules. Indexed public web research reviewed Stanford's Resolution text and Buss, Hoffmann, Johannsen (2008, arXiv:0811.1075), both standard proof-system context, not proof novelty. No separate Google-branded interface was used.

## Theorem 489.1: unit-assumption elimination in shared ordinary Resolution (PROVED/RESTRICTED)

Let F be any finite CNF, l a literal and pi a legal acyclic Resolution refutation of F union {(l)}, using L paid Resolution inferences. Its original source clauses are distinguishable from the extra assumption. There exists a legal Resolution derivation from original F of either the unit (not l) or the empty clause with **at most L Resolution inferences**, no extra assumptions and no weakening rule.

**Proof.** Traverse the original proof DAG topologically. For an original F-source clause C, copy C. For the extra source unit (l), mark its node as missing. For each other original derived clause C, maintain an already derived output D with D a subset of C union {not l}. At an oriented RES step with parents A or x and B or not x, if both transformed parent clauses still have opposite pivots, resolve them; the resulting clause is a subset of the original child union {not l}. If one transformed parent lacks its required pivot, bypass this step and reuse that already-derived parent: its clause is again a subset of the original child union {not l}. If one parent is the missing (l) leaf, its only possible pivot is l, so the other parent is a clause containing not l and can be reused without a new inference. There cannot be two missing parents in a valid step because two copies of the same unit cannot resolve. The invariant holds at every DAG node. At the original empty sink, the output is a subclause of {not l}, hence either empty or (not l). All retained RES nodes have authentic antecedents and correct oriented pivots, and bypassed nodes simply disappear. Sharing and acyclicity are preserved. QED.

This standard Resolution deduction argument is a model-qualified upper-bound construction, not an unrestricted hardness theorem.

## Corollary 489.2: full paid AND-case join

If G derives the cover $t_0\lor\cdots\lor t_{k-1}$ in $L_K$ paid RES nodes and each G plus assumed unit $t_i$ refutes in $L_i$ paid nodes, eliminate every assumption with Theorem 489.1. If any branch produces empty, stop. Otherwise all k globally valid units not-$t_i$ are derived from G and k more RES steps close the cover, with bound

$$
L_{\mathrm{global}}\le L_K+\sum_{i=0}^{k-1}L_i+k.
$$

This produces one acyclic *global* source-authenticated DAG; no branch-local assumptions leak, and common source or proof nodes are charged only once. The inequality is an upper bound, not necessarily a minimum. It does not license a new rule in R_mix341.

## Exact 17-step cover and 23-step full refutation

Use variables p,u,v,q and the conservative gate $q=u\land v$. The other *independent* AND output may be represented by p, but p's relation is irrelevant for this local guard theorem. Define

$$
t_0=\neg p\land\neg q,\quad r_1=[q=u],\quad t_1=p\land r_1,
$$

$$
r_2=p\oplus v,\quad r_3=[q=v],\quad t_2=r_2\land r_3.
$$

These seven gate relations have 24 original width-2/3 Tseitin defining facets, with charged named definitions in this **distinct** calculus. The new direct ancestor trace requires **17 oriented RES steps from 13 used original source facets** to derive $t_0\lor t_1\lor t_2$. LSPV-1/488's independent 18-step proof used 12 source ancestors; neither is claimed minimum.

For each i=0,1,2 introduce a fresh blocker variable $z_i$ and **two genuine original clauses**, $(\neg t_i\lor z_i)$ and $(\neg t_i\lor\neg z_i)$. Each branch under assumed unit $t_i$ has a three-step Resolution refutation. Instead of importing branch-local conclusions, resolve each blocker pair directly to derive the global unit $\neg t_i$ in one paid inference. Then resolve all three global negative units against the positive cover in three additional paid inferences.

**COMPUTATIONAL ledger (full actual global DAG):** 24 gate facets, 6 blocker facets; 17 RES in cover; three branch demonstrations of 3 RES each, not part of global proof; 3 paid negative-unit derivations plus 3 paid join steps; **23 paid RES**, **19 distinct source ancestors**, **42 distinct ancestor nodes**; unit-weight critical-path span 6 for cover and 9 for global refutation. All eight p,u,v assignments have a satisfying conservative gate extension; all 64 blocker extensions violate a blocker clause. Independent local JavaScript replay checked exact 23-node global proof, all 24 original facets, every source and signed pivot, and rejected six corrupted controls. Independently implemented Python source/RES replay produced the same 17+3+3 charged count. No natural-language step substitutes for a checked syntactic inference.

**Published code:** experiments/arc/lspv1_489_guard_discharge.py, exact 17-row oriented RES certificate and full signed source generation. **Raw:** results/raw/arc/2026-11-07_LSPV1_489_GUARD_DISCHARGE_RAW.json. The independent extended JS checker and its six hostile controls are retained as a separate local reproducibility artifact, not misidentified as execution of the historical /341 checker.

**Resources:** Logical paid-node count and unit-weight span are exact for this witness. Source/definition serialization, source/input indexing and reads, proof discovery, failed policies, memory allocation, caches, proof storage, output bits and verifier time and peak space are additional, and no claimed machine asymptotic follows. Source facets must be charged under any target calculus that charges them; no silent historical weight change.

## Established-family ledger and exact remaining transfer

The published Chvátal-Szemerédi random proper signed strict 3-CNF model has n original variables, 8n indexed signed width-3 clauses and Theta(n log n) bits. Its established hardness is ordinary Resolution, and Pang 2026 supplies scoped Res(PC_r/F_p) lower bounds. These do not cover historical full R_mix341. The published cubic odd-charge Tseitin family has 3h/2 edge variables, 4h proper 3-CNF clauses, Theta(h log h) bits and exponential ordinary Resolution hardness on expanders, but a **linear declared GF(2) mixed shortcut**. It is a mandatory countercontrol. No new hard family or all-machine lower bound is proposed.

**Status / falsifier accounting:** Theorem 489.1 and Corollary 489.2 are PROVED/RESTRICTED in ordinary shared-DAG Resolution; the 17/23-step finite certificate is COMPUTATIONAL with independent construction. Historical rule authentication [P2-D1] and unrestricted native mixed-rule translation [P2-C3] are OPEN. Full mixed-calculus minimum [P2-B1] and noncircular B3 [P2-B2] remain OPEN. This proof does **not** show historical RES, LOCAL-CONVERT, DEF, assumption discharge or RES->AND3 links are accepted by original /341 bytes. Next test: whether the historical original-source grammar admits a fully paid, accepted guard and RES-to-AND3 port, rather than a proposed extension. P versus NP OPEN.

Root main.tex returned only SHA 68188a24badda635a5983fda1c381cdb694fd497 and zero content bytes, preventing ownership-safe reconciliation. The local partial workspace lacked repository preflight dependencies. No main.tex or other agent region was overwritten. The existing two-Route-A/three-Route-B allocation and all five task identities, schedules and weights remain unchanged.

### References

1. Chvátal V, Szemerédi E. Many Hard Examples for Resolution. J ACM. 1988;35:759-768. https://doi.org/10.1145/48014.48016
2. Pang S. A Degree--Size Relation for Resolution over Polynomials. arXiv:2610.00837v2. https://arxiv.org/abs/2610.00837
3. Buss SR, Hoffmann J, Johannsen J. Resolution Trees with Lemmas. arXiv:0811.1075. https://arxiv.org/abs/0811.1075
4. Stanford Introduction to Logic: https://logic.stanford.edu/intrologic/extras/resolution.html
5. LSPV-1/488: research/agents/lspv-1/2026-11-07_LSPV1_PAID_GUARD_RESOLUTION488.md; LSPV-5/413: research/main/2026-11-07_0901_MAIN_HISTORICAL_341_CHECKER_SCOPE_REFEREE413.md.
