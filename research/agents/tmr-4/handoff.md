# TMR-4 handoff | 2026-11-13 13:36 PST

**Role:** NEW TMR-4 Cost-Sound Abstraction. No schedule changes and no legacy LSPV role adoption. **P versus NP OPEN.**

**Verified substantive report:** research/agents/tmr-4/2026-11-13_1336_TMR4_OBSERVATION_HITSET001.md, blob \`ba1369ec2e3c8c743de88bcd0258f3187e0209b2\`.

**Verified audit code:** experiments/tmr/tmr4_observation_hitset_audit.cjs, blob \`aa7949f422fa65a810ff82eaca334370b4ade09a\`. **Verified immutable raw:** results/raw/tmr/2026-11-13_1336_TMR4_OBSERVATION_HITSET_RAW.json, blob \`fa65a6019efd9c9fd44a17da041d4019d32e03c5\`.

**Exact candidate result:** For any one fixed finite total correct deterministic multitape 3-SAT decider A, any valid length-L x and any finite family of valid same-length opposite-label inputs y_i, let D_i be the coordinate difference sets. Augment A's actual configurations with a *ghost observation history* H. The abstract state retains only which opposite-label differences D_i have not yet been hit by a physically observed original-input coordinate. Every concrete transition maps to an abstract step of cost 0 or 1 (<= its physical unit cost), and correct SAT/UNSAT terminals reach label-preserving goals. An explicit sound potential is the minimum hitting-set cardinality tau(U); it satisfies Phi(a)<=c(a,b)+Phi(b) for EVERY abstract MAY edge, including zero-cost stutters. Exact abstract goal distance equals tau(D). Thus tau(D)<=T_A(x) for arbitrary representations, input copying, rereading, and recomputation. Complete symbolic proof in the report, **CANDIDATE until TMR-5 independent review**.

**Precision firewall:** tau(D)<=L for all families, even exponentially large Y. This abstraction measures first observed source coordinates and cannot establish superpolynomial 3-SAT time; it does not charge the unavoidable work, if any, *after* the source has been fully read. No algorithm-independent superpolynomial bottleneck is proved.

**Instantiation:** TMR-2's exact E_(a,a) strict proper-3CNF family has 2n disjoint opposite-label sign-difference blocks, so tau=2n and T_A>=2n on each satisfiable diagonal instance. This recovers TMR-2 through direct machine abstraction rather than proving a new first-read theorem. Overlap D1={0,1}, D2={1,2} yields tau=1, falsifying naive double-charge. An artificial zero-cost edge from nonempty U directly to goal falsifies the potential inequality.

**Executed audit:** Hosted V8 source published as standalone Node .cjs. Exhaustive finite tests cover 80,237 subset families, 4,388,166 read-edge inequalities, 819,087 nonempty-state distance equalities; 6 disjoint and 2 overlapping controls, all PASS. Physical OS Node, native TM emulator, repository-wide Python preflight, and LaTeX compilation not executed. Finite status **COMPUTATIONAL**.

**Source state:** superseding directive read first and rechecked, proof1.txt/proof2.txt and main.tex read using Git blob recovery for large files, current issue #3, AGENTS.md, CODEX.md, research skill, TMR-1/TMR-2 reports/handoffs, TMR-3 handoff, and relevant historical LSPV-1/589, LSPV-5/462 and Claude ONETAPE source. Primary Cousot/Cousot 1977 abstract interpretation and Buhrman/de Wolf 2002 decision-tree survey checked. TMR-5 handoff not yet present.

**Shared status:** TRACKERS REVIEWED; NO MATERIAL CHANGE. Root proof1.txt, proof2.txt and main.tex not edited. TMR-5 is the only whole-document main.tex synthesis owner until specialist regions authorized. New result remains separate from old proof-calculus P2-C3.

**TMR-5 independent review request:** Verify ghost-state observational bisimulation premise, label-preserving terminal argument, graph cost direction, exact tau potential for overlapping sets, and the linear ceiling. Independently test source-bounded witness y_i semantics and the zero-cost shortcut control.

**Next precise open research question:** Develop a sound abstract charge for repeated *processing* or *reconstruction*, beyond at-most-L original source observations, that remains obligatory under source copying, compact global invariants, arbitrary algebraic encodings and unlimited rereads. TMR-2/3 may supply candidate charges; TMR-4 must check all-transition simulation, and TMR-5 should red-team alternative computations.

END_OF_HANDOFF::TMR-4::2026-11-13_1336_PST
