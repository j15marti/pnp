# LSPV-2/511: Reordering independent deterministic SAT guest phases

**2026-11-08 19:44 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Exact nodes:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Preserve five agent identities, two Route A / three Route B allocation, schedules, enabled states, historical R_mix341 grammar/weights, and main.tex.

## IDEA, prior-art correction and falsifiers

Initial hypothesis was undecidability of exact all-length static high-index WORK-read reachability in a total polynomial SAT wrapper. The required project search located **LSPV-2/439**, research/agents/lspv-2/2026-11-06_0212_LSPV-2_ROUTE_A_TAGGED_SCAN_REACHABILITY439.md, blob b98d6e841ea2540425c5bf500055449a87843df6, already proving the same bounded-halting-reduction principle for tagged source scans. The high-index variant is only a change of tagged operation. **It is NOT a new theorem or a material proof-chain change; it was discarded.**

Revised hypothesis: the trusted dynamic read/write footprints in LSPV-2/509 and the sequential effect composition of LSPV-2/510 permit sound **phase reordering** under an explicit isolation and noninterference guard, while charging both phase executions. Falsifiers fixed before implementation: F1 P writes a cell read by Q; F2 P and Q both write a cell; F3 dynamically calculated indirect addresses depend on changed values; F4 a forged read set or hidden registers/branch assumptions violates the guard.

## SEARCH: exact project and outside sources

Read BOTH complete root proof1.txt and proof2.txt; current coordination issue #3; historical handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514ddbd747150dcb68607013a3b2d154); AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), and .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f). Exact predecessors LSPV-2/509 blob cd11b940ba5c4ac6a96fe8f0df475b1ba7c37ba6 and LSPV-2/510 blob a62fce9b130ca9d4fbc0f3d7db2218ab68b5211a. Peer LSPV-4/508 at research/agents/lspv-4/2026-11-08_LSPV4_CHARGE_SEMANTIC_QUOTIENT508.md (c484bff630fdb6760b6c3df8741c508f31674f22) explicitly separates semantic parity quotient from answer-cache leaves. Grok: GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f176e996e9542f0386b7aa7fe2ce89e70); Claude: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727d3e2b009cba7afec2a93beb62959dd67).

Required outside repository reads: konard/p-vs-np/README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2), a finite-machine formalization not an FLMV simulation; blkph0x/p-vs-np-proof-research/README.md (f397a7747eaca82df3d754d0a4b4bab1fe10f814), METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93), which keep all-input resource acquisition OPEN; meelgroup/frat-xor/README.md (38a137bca4d4ab6443703d4c31fba5783021c581), distinct external proof grammar; MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab), original parity sources; berkeley-abc/abc/README.md (88a9d1a316dd9751acade746de315fd1e6e6c362), circuit rewrites; openai/math/CONTENTS.md (7e1ed90ac5a666f1bbecb22027387c4ad79e9d03), general mathematics corpus, no FLMV simulator.

Primary sources: Fortnow, Lipton, van Melkebeek, Viglas, JACM 52(6) (2005), DOI 10.1145/1101821.1101822; Acar, Ahmed, Blume, Imperative Self-Adjusting Computation (2007), https://newtraell.cs.uchicago.edu/research/publications/techreports/TR-2007-18; Acar, Blume, Donham, A Consistent Semantics of Self-Adjusting Computation, JFP (2013), DOI 10.1017/S0956796813000099. These establish prior art for dependency tracking, memoization and dynamic side effects; **no novelty is asserted**. Web research used; separate Google-branded research interface not available.

## ITERATE: authenticated isolated-phase commutation lemma (PROVED/RESTRICTED)

Two isolated deterministic phases P and Q operate on common WORK memory M and immutable original source x. Every invocation starts from the same declared control registers, isolated return channels, no shared external effects, and no hidden mutable state except M. The actual P;Q run authenticates **all** WORK read addresses R_P,R_Q and write addresses W_P,W_Q, including indirect addresses and reads after internal writes; also source reads, original branch-assumption context, entry/exit metadata and historical WORK/index high-water.

Assume:
$$
W_P\cap(R_Q\cup W_Q)=\varnothing,\qquad
W_Q\cap(R_P\cup W_P)=\varnothing.
$$
Then executing Q;P from the same M yields the same individual phase observation traces and return values, and the same final WORK memory as P;Q. This is a sufficient, not necessary, guard.

**Proof:** By the first disjointness condition P changes none of the cells whose original values control Q, including dynamically computed addresses. Transition induction makes Q after P equal to Q directly from M. Symmetrically, the second disjointness condition makes P after Q identical to P directly from M. The write domains are disjoint, so the two final write maps commute. Every unwritten caller-private cell remains unchanged. Isolated entry control and immutable source ensure there is no additional order-dependent input. Both executions visit the same high-water addresses, while any inherited ancestral peak remains separately charged. QED.

Explicit failing controls: P writes memory cell 1 before Q reads that cell; P and Q both write cell 1 with different values; P changes cell 1 before Q indirectly writes memory[1] mod 16; a forged Q read footprint omitting cell 1 falsely certifies independence. The last control confirms that **authentic read evidence** is not optional. The result is only a deterministic machine-phase fact, not an added historical R_mix341 case-split, discharge or weakening rule.

**Conditional reuse implication:** A branching SAT computation may reorder or reuse such already executed, context-compatible phases if every authentic live-in, source read, write effect, caller frame and branch scope is checked as in LSPV-2/509-510, and retrieval/replay and history costs are paid. Neither mandatory phase may simply be omitted. A guest can have arbitrary conflicting footprints, making the guard false. Hence no all-input contraction follows.

## Published hard-family and shortcut controls

Use the established original signed strict proper 3-CNF **cubic Tseitin** source family: connected cubic graph G on H vertices, 3H/2 edge variables; each local charge parity yields four original signed width-three clauses, total 4H clauses and N=Theta(H log H) for a growing explicit identifier encoding. SAT iff total charge XOR is 0. Urquhart, Hard Examples for Resolution, JACM 34(1):209-219 (1987), DOI 10.1145/7531.8928 and Ben-Sasson/Wigderson, Short Proofs Are Narrow, JACM 48(2):149-169 (2001), DOI 10.1145/375827.375835 certify exponential **ordinary shared-DAG Resolution** size for suitable expanding odd-charge families under their model assumptions. K4 instances are finite fixtures, not a growing hardness proof. Algebraic GF(2) parity elimination is polynomial and must remain a valid algorithmic upper control; Cook ER, extensions, mixed native R_mix341 rules and other shortcuts cannot be silently excluded. No lower bound against all algorithms or full mixed R_mix341 is inferred.

## Independent computational checks and full-cost limits

Python local independent verifier: 4,096 seeded random phase pairs, 2,214 passed the guard and **all 2,214 commuted**; 1,882 did not pass and 1,507 full orderings differed; 2,245 assertions PASS. Separately authored Node.js verifier: 4,096 distinct random phase pairs, 2,218 passed the guard and **all 2,218 commuted**; 1,878 failed the guard and 1,507 orderings differed; 2,249 assertions PASS. Both enumerated 16 original signed K4 Tseitin CNFs (8 SAT/8 UNSAT), seven mutated-source rejection fixtures, four hostile overlap fixtures and a forged footprint control. First K4 original source SHA-256 in both: d2947ac9567bd6ed42c5557f2abaccfc69b745b1cdfe29ee7ad761761ea73273.

Repository executable: experiments/arc/lspv2_511_effect_commutation.cjs. Independently executed full Python and Node scripts and raw JSON reside in separate local reproducibility archive. The published standalone source and source SHA must be read back independently; container outbound DNS did not permit fetching raw.githubusercontent.com. These are finite symbolic tests of a **restricted phase ISA**, not native FLMV, R_mix341, or all-input polynomial SAT execution. Malformed fixtures are exclusions by exact finite-source-set recognition, not a general original-source parser.

**Charged ledger:** For E actual operations with address-bit width b and value width w, an explicit read/write footprint/effect transcript requires O(E(b+w)) evidence bits plus context, source, program/register and high-water metadata. Acquiring it requires executing the phases. Sorting/intersecting sets costs at least the actual paid comparisons (e.g. O(E log E) word comparisons, with bit overhead); every lookup/replay, failed match, cache, source/index/head access, conversion, output and historic WORK peak must be charged. Reordering alone executes both phases and does not reduce worst-case work or show E<=N^(1/2+o(1)). No effective, exponent-oblivious all-input transformation with q<=N^(3/5+o(1)), child size <=N^(1/2+o(1)), and local work <=N^(11/10+o(1)) is constructed.

## Publication and proof-chain decisions

Both trackers were read completely. This **restricted sufficiency guard** does not change status/dependencies or material generalized evidence/gaps, so **TRACKERS REVIEWED; NO MATERIAL CHANGE** rather than padding proof2.txt. Root main.tex fetch supplied zero readable bytes at blob 87081775f78ee61032a55abc8ffce806bedff245; it remains untouched. Issue #3 is the coordination channel. Route A [P2-A2]/[P2-A4]/[P2-A5] and [P1-01]/[P1-03]/[P1-04] OPEN; Route B [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2] OPEN. **P versus NP remains OPEN.**
