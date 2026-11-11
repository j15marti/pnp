# LSPV-1 Result 570: exact terminal-cone normalization and charge-preserving pruning in original archived /386 checker

**2026-11-11 04:00 PST | LSPV-1 General SAT Lower-Bound Lead | Route B unchanged | PROVED/RESTRICTED, COMPUTATIONAL accepted-byte controls | P versus NP OPEN.**

## Candidate theorem and falsifiers, fixed before the experiment

**Candidate 570.1.** For every *parsed certificate* accepted by the exact historical archived **/386 mathematical checker** `checkProof`, there is an accepted certificate of the identical guarded signed-source formula whose every paid Resolution record is in the terminal contradiction's syntactic ancestor DAG, whose every paid gate owner is needed by a retained record or the transitive paid-gate input dependencies, and whose logical price does not increase. Preserve all mandatory original SOURCE records even when they are not terminal ancestors. The claim does **not** concern the missing unified full `R_mix341` checker.

Precommitted falsifiers: **F1** deleting a nonterminal record changes source completeness or loses a paid shared parent; **F2** a retained auxiliary wire needs an omitted paid gate owner, including a nested owner-input dependency; **F3** chronological RES reindexing or free DEF-facet ownership invalidates the exact original verifier; **F4** full CLI acceptance is wrongly asserted to be preserved despite its synthetic corruption-test behavior. F1–F3 are ruled out for the specified exact mathematical checker by the proof and positive tests. F4 is a real boundary: core-valid W=28 packets fail the complete archived CLI because its destructive gate-deletion self-test does not change a zero-gate packet.

## Source authentication and corpus

Original checker: `experiments/arc/lspv2_386_independent_verify.js`, exact Git blob `338305c0ce101704205e57543756b8127074a986`. Its inference rules are original SOURCE, free truthful DEF facets of globally paid conservative binary AND owners, and strict oriented binary Resolution. It charges a paid RES *record occurrence* once and a gate owner once, even if a node or owner is not terminal-reachable. It requires all `4h+1` distinct signed SOURCE records, and its `checkProof` is separate from the command-line wrapper's eleven synthetic corruption tests.

Read root `proof1.txt` (Git blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (preflight blob `e7cb9e738ea31173766c553b2a5541e71df0c503`), current issue #3, `AGENTS.md` (blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`), `CODEX.md` (blob `754999f50de93cdb693ed37bc8110d31e9e698ef`), the repo-scoped `pnp-research` SKILL (blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`), latest five-role reports/handoffs and relevant LSPV-1/539–569, LSPV-2/539–554, LSPV-3/539–567, LSPV-4/529–540 and LSPV-5/477–484 corpus. In particular, LSPV-1/564 removed a **reachable** but redundant paid gate bridge, LSPV-1/569 established a bounded normal form, and LSPV-4/540 demonstrated that sharing a paid gate owner is not equivalent to sharing a proof-record occurrence. **570 is a different transformation:** it exactly removes **terminal-unreachable** work while keeping mandatory SOURCE authentication and transitive paid owner dependencies. LSPV-2/549 and LSPV-3/567 prevent treating two sibling checker languages or shadowed metadata as mixed-rule acceptance. No authoritative unified `R_mix341` grammar or cross-rule certificate was recovered.

Primary external references consulted: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973; Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), DOI 10.1145/375827.375835; Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV (2000). Their theorems do not authenticate /341-to-/386 transitions and do not transfer Resolution lower bounds to every possible native mixed rule.

## Theorem 570.1: terminal-cone paid-node normal form (PROVED/RESTRICTED)

Fix any packet `P` accepted by the original archived /386 **mathematical** verifier. Let `R` be its chronological record array and `G` its declared paid gate-owner list. Its final record `t` is the empty clause. Define `Anc(t)` by the transitive closure of actual chronological `parents` of `t`, including `t`. Define retained records

$$
K=\operatorname{Anc}(t)\ \cup\ \{r\in R:r.\operatorname{kind}=\mathrm{SOURCE}\}.
$$

Define the required owner set `H` as the *least* set of original paid gate-owner identities containing every owner of any auxiliary wire occurring in any retained clause, every owner explicitly named by a retained DEF facet, and recursively every owner of a signed gate input of an already retained owner. Original edge variables and the fixed guard are not owners. Let `Q` preserve the relative order of `K`, repair every RES parent index by the old-to-new record-index injection, and preserve the original relative declaration order of owners in `H`. Keep every original SOURCE occurrence and the complete unchanged `spec`. Recompute summary counters from these retained objects.

**Claim.** The exact original /386 mathematical checker accepts `Q`. If `r(P)` is the number of RES records and `g(P)` the number of distinct paid gate owners, then

$$
W_{386,\mathrm{core}}(Q)
=r(Q)+g(Q)
\le r(P)+g(P)=W_{386,\mathrm{core}}(P).
$$

Equality holds precisely when the original packet contains no terminal-unreachable paid RES record and no removable paid owner. The transformation is idempotent, and every core-optimal accepted packet is necessarily paid-cone-minimal, a **necessary but not sufficient** condition for global optimum.

**Proof.** (1) The exact checker charges but does not require terminal reachability of all original RES records. Every surviving RES has both parents in `Anc(t)`; preserving relative chronology and remapping their indices gives the same two parent clauses, pivot and strict resolvent, and retains terminal emptiness. (2) Original SOURCE records are all retained, so their original signed clauses, source-vertex provenance, source multiplicity, and `4h+1` completeness remain unchanged. (3) Each retained DEF is an authentic facet of its retained owner; by `H`'s least fixed-point closure, every auxiliary literal in retained records and every signed paid-gate input remains declared. Original owner declaration order is unchanged, so no new future-wire usage arises. (4) Each original accepted record clause is unchanged and thus retains canonical sorting, legal literal coordinates and all type checks. Recomputed exact counts satisfy the checker's full summary checks. The source-only parity/model controls are unchanged because `spec` is unchanged. Hence `checkProof(Q)` accepts. (5) Subset construction removes, never introduces, RES occurrences or paid owners, proving the inequality. Any strict deletion of a paid node strictly decreases unit-paid logical work. A second application sees precisely the same ancestor/owner closure and records, giving idempotence. QED.

**Important:** This is a property of **whole completed certificate normalization**, not an alpha/gamma soundness theorem for *all incremental transitions* of the missing full historical calculus. In particular, do not erase branch assumptions, discharge obligations, LOCAL-CONVERT scopes, exported/private wire semantics, or any genuine mixed-rule shortcut. The complete archived CLI wrapper is not the mathematical inference acceptance predicate.

## Original-code experimental results (COMPUTATIONAL)

The original /386 checker source was executed **unchanged in hosted V8**. For complete-CLI tests, only the host's file input/output, `crypto` output digest and `structuredClone` adapter were supplied; original inference and eleven synthetic corruption-test bodies were not edited. The output-only SHA-256 field in the hosted adapter was **not measured**. The repository also contains a dependency-free Node.js reproducer which invokes the original program in genuine OS subprocesses, but this new script was syntax-checked rather than run as an OS subprocess during the present report.

| Original accepted fixture | Core price before | Core price after cone pruning | Records before/after | Complete original CLI before/after |
| --- | ---: | ---: | ---: | --- |
| LSPV-1/568 K4, unused owner | 29 | **28** | 45 / 45 | ACCEPT / REJECT (synthetic self-test) |
| New exact K4 with 3 owners, 1 dead RES, 3 dead facets | 32 | **28** | 49 / 45 | ACCEPT / REJECT (synthetic self-test) |
| LSPV-3/561 K4 with truly live paid owner | 50 | **50** | 69 / 68 | ACCEPT / ACCEPT |
| LSPV-1/569 nested but unused owners | 30 | **28** | 47 / 45 | ACCEPT / REJECT (synthetic self-test) |

The 32-price packet adds two globally paid but unused owners `[1,9,8,2]`, `[2,10,9,3]` to the original unused owner `[0,8,1,4]`; inserts a valid but terminal-unreachable paid RES of `[2,3,4,5,-7]` from SOURCE records 0 and 4 on pivot `1`; and inserts three valid, unused free facets. This new packet is **exact accepted bytes** in `results/raw/arc/2026-11-11_0400_LSPV1_570_INFLATED_GUARDED_K4_ACCEPTED_PACKET.json`. Its original complete CLI ACCEPT used 3,393 assertion groups across eleven built-in corruption tests. Cone pruning removes four paid objects and three dead facets while preserving all 17 signed SOURCE clauses and the complete shared terminal resolution cone. The result is the 28-paid-node mathematical-core certificate already established in LSPV-1/568; its lower logical price is *not* a new minimum-cost claim.

In the genuinely active owner LSPV-3/561 packet, one dead zero-cost facet disappears but both necessary facets and the paid owner survive, so price stays 50; the original full CLI still ACCEPTS with 4,450 assertions. Five negative controls were rejected by the original checker: deleting an original SOURCE, deleting a genuinely live owner, corrupting final pivot, creating future parent, and underpaying summary. All four positive core outputs passed idempotence and unchanged-source checks. No random seed or heuristic solver was used.

Raw hosted evidence: `results/raw/arc/2026-11-11_0400_LSPV1_570_NATIVE_CONE_NORMAL_FORM_RAW.json`. Native OS reproducibility program: `experiments/arc/lspv1_570_native_cone_normal_form.cjs` (Node standard library, exact Git blob guards, original mathematical core plus actual CLI subprocess controls). The accepted extended packet, exact source checker and existing three seed packets are separately pinned; users need not rely on a manually reconstructed mock checker.

## Proof dependency and next falsifier

**P2-D1 OPEN:** The surviving archive authenticates /386 and /341 as distinct checkers, not the complete historical preselected `R_mix341`. This run obtained no new historical mixed dispatcher, RES-to-AND3 edge, DEF-to-LOCAL-CONVERT port, branch discharge or unknown-opcode rule. No proposed CANON1/2/2R completion was substituted.

**P2-C3 OPEN:** Exact cone normalization is a useful terminal-state abstraction for the restricted /386 language and supplies a rigorous cost-underestimation direction. It does not provide concrete-step inclusion for every genuine mixed transition, nor handle branch contexts, GF(2), joins, deletion, or every paid identity of the missing calculus.

**P2-B1 OPEN:** The 28-paid K4 refutation is an upper bound and a legal shortcut. No published lower bound for Resolution-only systems can simply be extended to a more powerful mixed calculus, and no superpolynomial full-calculus minimum-work theorem is established.

**P2-B2/B3 OPEN:** No same-calculus transfer from a hypothetical polynomial SAT algorithm to polynomial optimal `R_mix341` proof work has been established. Logical paid work, certificate evidence bits, proof discovery, actual time, span and peak space are separate quantities.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `proof1.txt` and `proof2.txt` statuses stay OPEN. Root `main.tex` is an approximately 2 MB shared manuscript; the full-file connector read has previously returned empty content, so I did not overwrite it without a verified full-content SHA/ownership-region reconciliation. LSPV-5 retains whole-manuscript synthesis ownership. No task schedule, role name, weight, owner boundary or TWO Route A / THREE Route B assignment was modified.

**Concrete five-role next target:** LSPV-3 and LSPV-2 must recover an authoritative single mixed-rule historical dispatcher with a source-bound accepted RES-to-AND3 or DEF-to-LOCAL-CONVERT edge; LSPV-5 must independently replay and falsify it; LSPV-4 must separate inferred logical price from evidence/time/space; LSPV-1 must admit every authenticated transition and keep P2-B2/B3 noncircular. A second sibling proof or polyglot acceptance is not enough.

**P versus NP remains OPEN.**
