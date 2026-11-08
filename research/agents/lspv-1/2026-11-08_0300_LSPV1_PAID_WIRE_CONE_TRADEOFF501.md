# LSPV-1/501 | Paid conservative wire definitions: original-support versus proof-size tradeoff

**2026-11-08 03:00 PST | Route B | PROVED/RESTRICTED conditional on Pang arXiv:2610.00837v2; COMPUTATIONAL independent finite controls; P versus NP OPEN.**

Tracked nodes: **[P2-L1-501]** (new restricted evidence), **[P2-L1-500]**, **[P2-C3]**, **[P2-B1]**, **[P2-D1]**, **[P2-B2]**. Companion **[P1-00]**, **[P1-01]**, **[P1-03]**, **[P1-04]** read but unchanged. No historical grammar/weights/agent/schedule changes.

## IDEA (specified before search)

Initial hypothesis: two-input acyclic conservative gate definitions can be admitted into the /500 same-source lower-bound compiler while retaining the small-support simulation overhead. Falsifiers: **F1** nested fan-in-two gates could have linear original-variable support; **F2** a native historical RES, XOR or LOCAL-CONVERT on extension-bearing global lines might evade any bounded support test; **F3** Pang Fact 7.1 or Theorem 7.2(a) might not apply to the exact same proper signed 3-CNF, field and DAG grammar; **F4** a purported inference may require an uncharged semantic oracle or permit branch-local premises outside justified contexts.

**ITERATION:** F1 is CONFIRMED: a depth-logarithmic binary AND tree has output depending on every original input. Thus direct fan-in/depth is invalid as the locality parameter. F2 is an explicit exclusion in the distinct calculus below, **NOT** an assertion about historical R_mix341. F3 was checked directly in arXiv:2610.00837v2 §7 (Fact 7.1, Theorem 7.2(a)); the paper remains a preprint, not independently reproved here. F4 is handled by explicitly witness-checkable original-support tables and no assumptions; the historical native checker remains unauthenticated.

## SEARCH and exact continuity

Both live complete root trackers were fetched: proof1.txt SHA **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** (18,553 characters) and proof2.txt SHA **98a1f9cd17fd62d803ab94ffc4ee5bc8bee9dbc2** (376,201 characters). The full proof2 SHA must be refreshed before any write. Read current coordination issue #3 (1,317 comments), original governing handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), and .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f). Latest relevant own /500 report 2a53755f9f3843d87a2c593c659ec3d20b131e59, LSPV-3/496 tagged grammar a27e0c8cf71defcadcfe8fcf685bc2958b4191c2, peer LSPV-5/430 referee and latest issue comments inspected. Actual Grok GROKPROOF/2026-11-08_0930_PROGRESS.md blob e3e8c9657e0f2b2e0751752135cf2558e28183cf and Claude research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex blob 95c2649b29ae7efac79e9400effffd2c3bdeb2fc were read and do not supply native mixed-rule completeness.

External corpus inspected (actual files): konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f. These are model-specific methods and external proof formats, not historical authority. Primary research searches reviewed Pang arXiv:2610.00837v2 §1 and §7 at https://arxiv.org/html/2610.00837v2; Grosof, Zhang and Heule arXiv:2207.11284 and Cook 1976 polynomial Extended Resolution PHP shortcut (as a required upper-bound/family control). No separate Google-branded query, native Lean replay or official historical checker execution took place. No evidence of a complete mixed-system transfer was found.

## FORMAL MODEL: distinct cone-typed system, not historical R_mix341

Fix source-authenticated proper signed 3-CNF F with n **original** variables and m clauses. The distinct effective, sound, Resolution-complete system **R_wire-cone** allows:

1. Original-only global ordinary RES and original-only affine unit-row GF(2) addition, each paid. Source clauses carry original source IDs. A global rule containing *any* auxiliary Boolean wire is NOT admitted.
2. Paid globally fresh two-input Boolean gate definitions z=g(u,v), g in the fixed 16-function Boolean basis, with acyclic topological definitions and explicit defining facets. These are *conservative*: they impose no constraint on original inputs. For each wire z, its unfolded truth function φ_z has original ancestor set supp(z), computed recursively through definitions.
3. Paid, at-most-two-parent **LOCAL** implications between compact Boolean lines/factors over original variables and named auxiliary wires. An inference must be correct under substitution z:=φ_z for **every** original assignment on the union U of the complete transitive original supports of its premises and output. All parent/output IDs, original-source provenance and an explicit falsifying-output/false-parent witness table are checked. No SAT oracle, free split/discharge, context leak or unproved semantic inference is allowed. This effective rule may cost 2^{|U|} validation time, and its evidence bits are independently charged in physical ledgers. No support upper bound is imposed on the calculus itself.

Definitions themselves only substitute tautologies, so they are not additional original axioms. A local fact containing any auxiliary variable cannot become input to a global RES/XOR step except through a separately permitted and paid original-only LOCAL conversion. This is a strict syntactic firewall, not a proposed completion of R_mix341.

For any proof DAG π, define q(π) as distinct paid inference/definition nodes (not source axioms), and

$$
b(\pi)=\max_{\text{LOCAL step }v}\left|\bigcup_{P\in\mathrm{parents}(v)\cup\{v\}}\mathrm{supp}_{\mathrm{orig}}(P)\right|
$$

with b=0 if no LOCAL step is present. Define the vector over original ancestors, **not** a count of gate inputs, words, leaves in one line, DAG depth or named wire occurrences.

**Theorem 501.1 (per-proof, not fixed-threshold, compilation).** For every source F and every valid source-authenticated shared refutation π in this DISTINCT R_wire-cone, there is an explicit syntactic, same-original-source Res(PC_1/F_2) refutation with

$$
S_{\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)}(F)
\le C\bigl(m+n+q(\pi)+1\bigr)(b(\pi)+1)2^{b(\pi)}
$$

for an absolute constant C. The bound holds with nested and shared conservative definitions of arbitrary total number and depth, as long as every extension-bearing use is a LOCAL step measured by complete original support.

**Proof.** Process the definitional and inference DAG in topological order. Substitute each named fresh gate z by its unique acyclic original-input Boolean function φ_z. Source-original clauses remain identical; each paid definition facet becomes a Boolean tautology after substitution and contributes no extra axiom. Represent a LOCAL Boolean line P by its canonical set of original-variable exclusion clauses D_α for all assignments α on supp(P) falsifying P. Each such canonical clause excludes exactly the assignment α to its support. At any LOCAL step, fix U as defined above, |U|=s≤b. For every U-assignment α falsifying the output, soundness plus the recorded table identifies an actually false named parent. Its already-derived canonical exclusion D_(α|supp(parent)) can be syntactically weakened to D_α; when the parent is a native original clause or affine row, the same O(s) syntactic Boolean-axiom/linear-combination macro supplies D_α (Pang Fact 7.1). The at most 2^s full exclusions are projected to output support J⊆U by binary Resolution on U\J, costing fewer than 2^s additional nodes. If the output is an original-only clause or affine row for subsequent global use, Pang Fact 7.1 supplies its native degree-one syntax in O((s+1)2^s) nodes. Original-only global RES and global GF(2) each have constant-cost native syntactic simulations. Every bundle is retained and referenced once as a DAG object; no invalid reuse across assumptions, because this system has none. Hence total target nodes are bounded as claimed. QED.

**Corollary 501.2 (published random-hard-family conditional).** Pang Theorem 7.2(a) states that for F_n drawn as 8n independently sampled proper signed 3-clauses on n variables (repetitions allowed), for some κ>0, with high probability,

$$
S_{\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)}(F_n)\ge e^{\kappa n}.
$$

Therefore every legal π in this distinct system on such a hard F_n satisfies

$$
\ln(m+n+q(\pi)+1)+b(\pi)\ln2+\ln(b(\pi)+1)\ge\kappa n-O(1).
$$

If q(π)≤n^d for any fixed d, **necessarily**

$$
b(\pi)\ge \frac{\kappa}{\ln2}n-O(\log n).
$$

If b(π)=o(n), necessarily q(π)=e^{\Omega(n)}. Unlike /500, this inequality is **per proof** and applies with an arbitrary (not pre-fixed) locality profile and fresh paid conservative wires, subject to the explicit R_wire-cone grammar. Original 8n-clause source length N=Θ(n log n), so the restricted source lower-bound scale is e^{Ω(N/log N)} when b=o(n). This result does **NOT** establish historical R_mix341 hardness or any general SAT time lower bound. The premise is Pang's specified preprint theorem, not a locally independently proven lower bound.

**Lemma 501.3 (fan-in falsifier).** For n=2^h original inputs, a balanced n−1-gate binary AND tree has gate fan-in two and depth h, but its single output z satisfies supp(z)=[n]. Induction on tree levels proves this exactly. Thus replacing b(π) with maximal gate fan-in or even gate depth in Theorem 501.1 is false. Actual finite controls n=4,8,16,32 check every original ancestor.

**Dangerous alternate calculus.** If one permits a single unchecked or merely exponentially truth-table-verified all-variable semantic "source F ⇒ false" shortcut at unit logical weight, any UNSAT F acquires tiny node count regardless of solver time. Such a rule is NOT a legal inference in the historical project. The theorem above explicitly pays all witness evidence and source-anchored transitive support, and the per-proof inequality accordingly becomes vacuous when b=n. This is a resource firewall, not a discovery-cost objection.

## ITERATE: independent checked controls and resource ledger

A standalone JS prototype with explicit original-support propagation, nested/reconvergent OR/AND/XOR gates, exclusion witnesses and actual binary Resolution projection executed in the local container with **48 checks and 12 hostile rejects**; code SHA256 a5c9d4d72c2cda52d3c8d25c622b7443f1a9760d7773714974036b5b097e15e2. Independently authored Python exercised six predicate/macro cases and four gate-tree sizes, **433 independent checks PASS**, with a deliberate false entailment rejected (SHA256 56c844cc51150d98d1e20d2455e77d2e914b58f26ed9660ca2717e107f0f923c). The published independent standalone JS performs 41 checks, four hostile rejects, five two-parent local macro witness controls and four tree scopes, and its raw results were run in V8 and read back exactly. The container Node process was measured at ~0.17 s wall, 30,580 KB peak RSS; independent Python ~1.04 s wall, 95,884 KB peak RSS, specific to these finite experiments. No theoretical complexity is inferred from timing.

The full source-side evidence check can require Θ(q 2^b × line-expression-work) operations and Θ(2^b) simultaneously resident witness entries if fully materialized. Binary exclusion projection and original-source normalization produce O((q+m+n)(b+1)2^b) target nodes and O((q+m+n)b2^b polylog(q+n)) explicit output bits. A source-encoded certificate additionally charges all definition IDs, facet bytes, parent indices, source-index authentication, reads/writes, parsing, verification, output, storage, retrieval/recomputation and construction/search (not part of ideal W). Separate weighted critical-path span may be O(qb) along a sequential dependency, whereas total distinct-node work and real schedules vary. Any quadratic or exponential intermediate materialization incurs its actual peak, even when released before the final stage. No FLMV same-machine claim is made.

Published artifacts:
- Code: experiments/arc/lspv1_501_wire_cone_tradeoff.cjs (blob ed9be97440823f11eda2101a368c2383f4dd8088)
- Raw: results/raw/arc/2026-11-08_0300_LSPV1_501_WIRE_CONE_RAW.json (blob 13c6ec1ebb63aca412737e8952902c07c650e562)
- Handoff: research/coordination/2026-11-08_0300_LSPV1_WIRE_CONE501_FIVE_ROLE_HANDOFF.md

**BOUNDARY:** Original historical checker/byte grammar and all legal historical aux-bearing RES, AND3, LOCAL-CONVERT, GF(2), branching/discharge, weights and provenance semantics are still OPEN at [P2-D1]/[P2-C3]. Native mixed hardness [P2-B1] and noncircular same-calculus B3 [P2-B2] are OPEN. Historical R_mix341 is unchanged. Root main.tex was not modified because complete outside-region bytes were not safely available. P versus NP remains OPEN.

## Primary sources

[1] Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, 24 October 2026, §1 and §7, Fact 7.1 and Theorem 7.2(a): https://arxiv.org/html/2610.00837v2

[2] I. Grosof, N. Zhang, M. Heule, *Towards the Shortest DRAT Proof of the Pigeonhole Principle*, arXiv:2207.11284, and S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution* (1976), as extension-variable shortcut controls; neither is a lower bound for historical R_mix341.

[3] V. Chvátal and E. Szemerédi, *Many Hard Examples for Resolution*, JACM 35 (1988), 759–768, a distinct ordinary Resolution lower-bound control.
