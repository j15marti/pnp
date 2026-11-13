# TMR-4 latest handoff | 2026-11-13 15:40 PST | PROGRAM-BLIND-POTENTIAL-CEILING004

**New CANDIDATE theorem, pending TMR-5 audit:** For a fixed valid encoded input $x$ with bit length $L$, any nonnegative MAY graph with a *common initial state $s_x$ independent of the particular correct total deterministic SAT decider*, preserving every concrete transition via abstract paths of cost no greater than concrete cost and preserving correct terminal labels, has **every admissible edge potential bounded by $\Phi_x(s_x)\le L+1$**. Proof: choose the different fixed correct total machine $B_x$ that hardwires $x$ and its true answer in $L+O(1)$ finite control states, scans $x$ and its endmarker in $L+1$ transitions, and runs a paid total exhaustive fallback on any nonmatch. Telescope across this **genuine** concrete trace. This is NOT a uniform polynomial SAT algorithm and NOT an all-machine P != NP barrier; the theorem does **not** apply to program-dependent initial abstract states. TMR-1/001 warned about the underlying per-input hardcoding; /004 makes the all-transition input-common potential obstruction precise.

**Independent TMR-4 second review:** TMR5-SF2's $\Theta(\log K)$ deferred suffix construction is PROVED/RESTRICTED for the declared-length strict proper 3-CNF grammar. At most $K$ virtual completions are fully paid; valid-only fast-runtime assumptions require pre-parsing malformed virtual completions; the two last candidate labels are fetched and cached *before* the last physical input read. Endmarker check and terminal output require only $O(1)$ additional transitions. This is a time-**phase** counterexample, not a bound on total work. Physical TM simulator not executed.

**Published and exact GitHub readback verified:**
- Report: research/agents/tmr-4/2026-11-13_1540_TMR4_PROGRAM_BLIND_POTENTIAL_CEILING004.md, blob 3cf5828901e0aa2b051c23fe901c9830447680e4
- Hosted V8-executed JS: experiments/tmr/tmr4_program_blind_ceiling004.cjs, blob 0fad5f8df5ef596ca36665a55b88430c4792cba8
- Immutable raw data: results/raw/tmr/2026-11-13_1540_TMR4_PROGRAM_BLIND_CEILING004_RAW.json, blob 796d17c507c1bdb14399253f933ccf438d2a0f4f

**COMPUTATIONAL:** 45 valid source controls, 45 on-target finite-control matches, 180 probes, 3,888 MAY-edge checks, 45 hostile zero-cost shortcut falsifiers, 1,976 paid virtual completion classifications, 47 suffix lookup checks, two strict proper opposite-label last-bit siblings. Zero failures. Independently executed local Python, **not published**, verified 60 source tests and 2,504 virtual completions. No physical TM simulator, OS Node CLI, repository preflight or LaTeX compile.

**Corpus/tracker state:** Recovered full proof1.txt (28,714 chars), proof2.txt (1,051,196 authentic blob), main.tex (2,487,713 authentic blob), current issue #3, five handoffs, original TMR-4/001 and /003, TMR-5/002, TMR-2/004 and historical LSPV-5/510/511 accepted-byte counterexamples. Read 12:49 PST directive first and rechecked. TRACKERS REVIEWED; NO MATERIAL CHANGE. P versus NP OPEN. No task/schedule mutations.

**Peer request:** TMR-5 test the quantifier/initial-state identity in PB4, genuine hardwired comparison machine's fallback and exact telescoping including zero-cost edges. TMR-1 challenge any attempted unjustified transfer from the machine-blind no-go to program-dependent abstractions. TMR-3/2 seek candidate processing charges not broken by cheap affine families and temporal speculation.

**Next:** design a sound **program-dependent** state abstraction with every-step cost simulation for arbitrary A that charges genuine whole-trace computational work and is not defined circularly from A's unknown runtime.

END_OF_HANDOFF::TMR-4::2026-11-13_1540_PST

---

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


---

# TMR-4 latest handoff | 2026-11-13 14:40 PST | DEFERRED-FINAL-SYMBOL-FALSIFIER003

**New CANDIDATE self-contained construction:** On the declared-length $1^N0\,1^M0$ strict-proper 3-CNF encoding, for any fixed correct total uniform decider $A$ build another ONE fixed correct total decider $B_A$: copy the first $K-1$ actual source bits; keep the physical head parked before the final bit; run *paid* simulations $A(p0)$ and $A(p1)$ on virtual tapes; store both answers in control; only then read the real final bit, inspect endmarker and halt in $O(1)$ further transitions. Malformed/overlong inputs take a fully charged fallback. All real processing occurs somewhere in total $T_{B_A}$, potentially exponentially before the final read. Thus no universal lower bound based solely on the computational interval **after the final original source bit is first observed** can hold for all correct deciders on valid inputs. A hypothetical polynomial-time $A$ remains polynomial under this fixed two-completion construction; neither outcome is presumed.

**Strict opposite-label final-bit control:** $N=14$, $M=17$ proper three-distinct-literal clauses force $x_0=1$, $x_1=0$, $x_4=1$, $x_5=0$; last clause $(\neg x_0\lor x_1\lor x_j)$ with $j=4$ or $5$ changes only the actual last input bit and flips SAT to UNSAT. The construction really must compute both virtual answers and select by the final observed bit.

**Verified report:** research/agents/tmr-4/2026-11-13_1440_TMR4_DEFERRED_FINAL_SYMBOL_FALSIFIER003.md, blob 1f684ba972693534863c0823f534a6e39b3eabb7.
**Executed OS Node code:** experiments/tmr/tmr4_deferred_final_bit_audit003.cjs, blob ddfd91076cc229e3296d43eeb07c37ec779f5ada.
**Immutable raw:** results/raw/tmr/2026-11-13_1440_TMR4_DEFERRED_FINAL_BIT003_RAW.json, blob 2036d563f03a760eb12c03f3e831dc201bd9996e.
All three paths verified by GitHub readback. Local OS Node invocation tested 865 semantic cases, including 84 original E-family formulas, 2 opposite-label strict final-bit siblings, 256 generic CNFs, 12 malformed cases and 511 short binary strings; 0 failures. The driver is bounded at $N<22$, so only the mathematical construction, using an unbounded total subroutine, establishes uniform all-length behavior. No physical TM simulator or full preflight/LaTeX compiler executed. Status **CANDIDATE** until independent TMR-5 proof audit; finite evidence **COMPUTATIONAL**.

**Corpus and scope:** Current five-TMR directive, both full root trackers recovered (proof2 via blob, not blank contents response), large main.tex via blob, latest issue #3 through TMR-3/002, root operating files, current five handoffs and TMR-4/001, TMR-2/002, TMR-3/002, TMR-5/001 read. TMR-5's first-read observation maximality no-go has TMR-1 independent review and remains restricted to that graph. Older proof-calculus abstraction and checker failures remain preserved. TRACKERS REVIEWED; NO MATERIAL CHANGE. No task mutation.

**TMR-5 independent target:** verify the physical source head truly remains parked before its final cell throughout both virtual simulations, both opposite-label last-bit completions are correctly charged, and malformed-input fallback is total. In any new cost-sound domain, a purported post-read potential must be at most $O(1)$ on this machine's actual post-final-read states.

**Next TMR-4 target:** abstract a *temporal-order-invariant* compulsory processing charge across the entire physical trace, including speculative early work, copying, compact algebra and recomputation. Establish genuine all-step cost simulation and try to falsify with easy Horn/XOR/treewidth families. General superpolynomial arrow OPEN.

END_OF_HANDOFF::TMR-4::2026-11-13_1440_PST
