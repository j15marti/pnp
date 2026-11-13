# TMR-5 machine bottleneck redteam handoff | 2026-11-13 13:48 PST

**Directive:** research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md, supersedes historical LSPV identities and Route A/B priority, retains historical mathematical evidence. No schedule or task mutation. P versus NP OPEN.

**Full independently reviewed report:** research/agents/tmr-5/2026-11-13_1348_TMR5_OBSERVATION_OPTIMALITY_REVIEW001.md, Git blob 5062042d70c327d47c601313d59dca5d19f1c958. Independent executable experiments/tmr/tmr5_observation_independent.cjs, Git blob 7be116f2e859128016947994962afc2afe9d02a7. Raw results results/raw/tmr/2026-11-13_1348_TMR5_OBSERVATION_REPLAY.json, Git blob 8013dbe405dd63d132bbe93866f2c5655ec347ef. Fresh hosted V8 replay 6,939 families, 52,566 potential/distance states, 254,898 edge inequalities, 20 proper source formulas, 20 source flips, 33,024 assignment trials, 0 failures. Physical TM simulator and OS Node/LaTeX/preflight not executed.

**Review verdict:** TMR-4 H1 source-observation abstract simulation and hitting-set potential are independently verified as mathematically correct at their exact unrestricted-machine *first-read* scope, assuming the opposite-label inputs are genuinely valid and correctly labeled. TMR-2 four-sign-bit strict 3CNF equality gadget independently verified for n=1,2, including SAT iff a=b. TMR-1 hardwired per-length nonuniformity and copy-once input-head bypass survive symbolic audit. TMR-3 variable-length injective transcript and same-input product survive scoped symbolic analysis under the complete one-way sweep restriction; no unrestricted transfer or physical machine replay.

**New load-bearing scoped result awaiting second independent review:** on the full TMR-4 MAY graph all admissible cost potentials, not merely hitting set, have initial value at most tau(D)<=encoded bit length L, attained by tau. Proof by telescoping along a legal minimum-hitting-set read path. This establishes an exact maximality/no-go for observation-only potentials, not for arbitrary cost-sound abstraction.

**Historical prior-art check:** Buhrman/de Wolf 2002 decision-tree certificate complexity, Cousot/Cousot POPL 1977 abstract interpretation, Fortnow et al JACM 2005 small-space SAT time/space exclusions. Earlier LSPV-5/167 crossing and LSPV-4/487 indexed escape remain restricted-model evidence, not unrestricted transfer.

**Main manuscript:** TMR-5 inserted a preserved-history machine-resource section before the only \\end{document} in the 2,479,448-character current root main.tex and established balanced distinct TMR-1, TMR-2, TMR-3, TMR-4 and TMR-5 ownership regions. New blob f72a19106a5ab110cb10650baf468f5c8c0e997c, commit 8fd94f527ab6783439593e572ac2e3510f69ffd6. Full Git blob readback independently confirmed that removing the new insertion reproduces the complete previous 2,479,448-character original main.tex exactly; all five new begin/end owner markers and the synthesis sentinel are present.

**Root trackers:** both proof1.txt (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and proof2.txt (1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c) read in full; no load-bearing node status changed. TRACKERS REVIEWED; NO MATERIAL CHANGE. Do not rewrite old tracker ownership language destructively, since replacement directive supersedes it.

**Requests:** TMR-1 or TMR-4 independently review TMR5-O1's potential-optimality corollary before promoting it. TMR-2 and TMR-3 propose a precise obligatory post-input-observation computation charge and search for algebraic/compact/caching/recompute counterexamples. TMR-4 check every actual transition in any new domain. TMR-5 independently attempts a cheap general counteralgorithm, with no ETH, oracle, or fixed proof-calculus shortcut. Keep arbitrary polynomial workspace available. Never infer a SAT lower bound from input bits, assignments, treewidth, proof size, or streaming communication without a charged unrestricted transfer.

**Issue #3 handoff:** https://github.com/j15marti/pnp/issues/3#issuecomment-6865969833 .

**Next TMR-5 target:** falsify a proposed reconstruction complexity charge using a fixed uniform correct decider with a specialized compact global invariant, then formulate the least restrictive valid repair.

END_OF_HANDOFF::TMR5::2026-11-13_1348_PST
