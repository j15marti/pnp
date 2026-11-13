# TMR-2 latest handoff | 2026-11-13 15:12 PST | AFFINE-CLIQUE-TSEITIN-004

**CANDIDATE symbolic construction pending independent TMR-5 review; COMPUTATIONAL exact tests; P versus NP OPEN.** New TMR-2 identity under superseding replacement directive. No schedules, tasks, retired LSPV roles or old Route A/B allocations changed.

**Substantive hostile falsifier:** For every even m >= 6 and charge b in GF(2)^m, an explicit strictly proper 3-CNF of three-variable XOR rows on K_m has N=3m(m-3)/2 source variables and M=4m(m-3) original clauses. SAT iff XOR of all charges is zero. Each SAT formula has exactly 2^[(m-1)(m-2)/2] complete satisfying assignments, and its ORIGINAL CNF primal graph contains a K_m minor, hence treewidth >=m-1. Nevertheless one fixed total correct all-input SAT decider recognizes the affine four-clause XOR3 blocks, decides the recognized class by paid GF(2) Gaussian elimination in polynomial time, and uses an exhaustive paid fallback elsewhere. On canonical K_m templates it needs only an authenticated charge XOR flag and O(log L) counters. No mandatory exponential memory, assignment traversal or time follows from width/semantic multiplicity. This extends known Tseitin/affine fast-path ideas with an explicit primal minor; it is NOT a new general polynomial SAT algorithm.

**Verified main artifacts:**
- Report: research/agents/tmr-2/2026-11-13_1512_TMR2_CLIQUE_TSEITIN_COMPRESSION004.md, blob 689809f905e18d704200e7b40064dc30acd745df
- Executable: experiments/tmr/tmr2_clique_affine_audit004.cjs, blob 2bab7fa2261df323a4352fce73d3b54d8e68801e
- Raw: results/raw/tmr/2026-11-13_1512_TMR2_CLIQUE_AFFINE004_RAW.json, blob c7a1df10710305e45fdad94fb37f5fbf77576cfd

**COMPUTATIONAL:** V8 executed the exact readback-published audit on 30 cases (15 SAT/15 UNSAT), 30 signed source roundtrips, 30 independent GF(2) classifications, 8 K_m branch-set certificates, 163,840 exhaustive m=6 edge-bit assignments, 5 solution-count identities, 15 renaming/reordering, 15 sign flips and 15 missing-clause rejections, zero failures. Largest L=379,527. Independent local-only Python test also passed, not published. Physical TM emulator, OS Node CLI, repository preflight, report validator and LaTeX compile not executed.

**Priority review:** TMR-5 independently test auxiliary elimination, minor branch-set disjointness/connectivity, arbitrary renamed odd charges, affine block recognizer soundness and fallback; TMR-4 keep cheap physical trace as genuine may path; TMR-3 check on-the-same-input time/space account; TMR-1 quantifier discipline. Historical four-clause XOR3 compiler is LSPV-1/452; Tseitin 1968 and de Colnet/Mengel 2023 restrict classical proof-system claims.

**Read state:** 12:49 PST directive first and rechecked. Root proof1.txt (28,714 chars), recovered full proof2.txt Git blob (1,051,196 chars), root main.tex (2,487,713 chars), root protocols, newest five TMR handoffs, issue #3, and relevant original reports examined. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No changes to proof1/proof2 or main.tex. All universal superpolynomial arrows remain OPEN.

**ONE next target:** develop a representation-independent, temporal-order-independent lower-bound charge for non-affine global consistency, allowing every correct total deterministic solver to use genuine fast recognizable affine/other subroutine paths.

END_OF_HANDOFF::TMR-2::2026-11-13_1512_PST

---

# TMR-2 handoff, 2026-11-13 13:15 PST

**Owner:** TMR-2 Information Necessity, replacing old LSPV-2 identity, no old Route A obligation. **Proof status:** CANDIDATE elementary symbolic lemmas pending TMR-5 independent review; COMPUTATIONAL finite regression; P versus NP OPEN. No agent/schedule changes.

**Verified report:** research/agents/tmr-2/2026-11-13_1315_TMR2_INPUT_BLOCK_SENSITIVITY001.md (blob ccd5734076e214fa68f696eaa21a0448bc6bd21e).  
**Verified executable:** experiments/tmr/tmr2_strict3_input_block_audit.cjs (blob cfae39fb39ce7042e927822cbb25ddd9c33fee03).  
**Verified raw:** results/raw/tmr/2026-11-13_1315_TMR2_STRICT3_INPUT_BLOCK_RAW.json (blob bbe6ec0004284c911fadf2e3d449e6303003f522).

**Necessary event valid for arbitrary correct deterministic multitape deciders:** On x, every disjoint coordinate block B whose full flip yields a same-length opposite-label valid input must contribute at least one actually read input coordinate. Determinism otherwise makes the execution identical on x and the changed input. Hence r disjoint sensitive blocks impose r physical reads, where r<=encoded bit length L. This is not a memory or superpolynomial runtime lower bound.

**Concrete exact strict proper-3CNF family:** E_(a,b) has a signed four-clause unit-forcing gadget for each x_i=a_i in the prefix, and similarly for x_i=b_i in the suffix; all auxiliaries are fresh. N=5n variables; M=8n clauses, every clause has 3 distinct variables; L=13n+2+24n(1+ceil(log2(5n))). E_(a,b) is SAT iff a=b. Every single E_(a,a) has 2n pairwise disjoint four-sign-bit source blocks, each whose flip makes an UNSAT valid input. Thus T_A(E_(a,a))>=2n for **every correct total uniform A**. First-input-bit acquisition alone has linear upper ceiling and cannot settle P versus NP.

**Model-transfer falsifier:** One-pass streaming after the prefix requires 2^n different configurations (Omega(n) cells under fixed alphabet/tapes). A two-way read-only-input algorithm recognizes the rigid family using O(log L) workspace and compares pairs with repeated input scans in O(L^2 log L) time. Add any total exhaustive SAT fallback for other inputs to obtain one *all-input correct* deterministic algorithm that is cheap on E. The full read-only input differs even where work states coincide at the cut. Earlier Claude one-tape equality/crossing papers already established the broader family concept; we claim no priority for equality.

**Executed V8 finite test:** exhaustive 1,364 a,b instances n<=5, 516 four-sign-bit opposite-label flips, 20 complete brute-force formulas n<=2, 101,952 local gadget truth assignments, all PASS. Full Node OS CLI runner, full preflight, formal TM simulator and independent proof review not executed. Separate Python local test matched 1,364/516/20 but was not published; GitHub V8 runner and raw are the reproducible shared evidence.

**Review and synchronization:** Directive read first and rechecked before shared writes. Both root proof1 and proof2 and canonical root main.tex read; large file fetch blanks recovered through Git blob API; issue #3 read; TMR-1/001/handoff, Claude ONETAPE original notes, AGENTS.md, CODEX.md and repo research skill read. Historical work preserved. No other TMR handoffs were available when checked. No TMR-2 ownership section is yet authorized in root main.tex. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

**TMR-5 request:** check valid four-bit sign coordinates, same-input disjoint perturbation proof, and one-way state-count assumptions before promotion. TMR-3 should account for repeat source crossings; TMR-4 should model each necessary read in a universal cost-underestimating abstraction.

**Next target:** an independent charged repeated-discrimination/recomputation necessity beyond first source reads, resistant to O(log L)-workspace rereads, full-input copying, algebraic/Gaussian elimination, and source/representation change.

END_OF_HANDOFF::TMR-2::2026-11-13_1315_PST

---

# TMR-2 latest handoff, 2026-11-13 14:20 PST, ONE-SWEEP-MATCHING-UPPER-002

**New verified publication:** research/agents/tmr-2/2026-11-13_1420_TMR2_ONE_SWEEP_MATCHING_UPPER002.md, readback blob d662afe2f197cb2b8943e3846d828821461bbd5e. Executable experiments/tmr/tmr2_sweep_tightness002.cjs, blob 6c29ed9ed53d14210a805737f92884ae8cced6ff. Immutable raw results/raw/tmr/2026-11-13_1420_TMR2_SWEEP_TIGHTNESS002_RAW.json, blob 0f7f5bf6e5e9c717b21c918bfcfa9ec16e535318.

**New candidate theorem:** ONE fixed total correct deterministic multitape 3-SAT machine performs a single left-to-right complete source sweep on every exact TMR-2 proper-3CNF equality input E_n(a,b), decides correctly in T=Theta(L), uses S=Theta(n) work cells for stored prefix signs and paid indices, and has p=1. It recognizes the exact rigid family; on nonfamily sources it performs a paid subsequent sweep and fixed exhaustive SAT fallback. Its same-input p(S+1)=Theta(n) and T(S+1)=Theta(L n) match TMR-3's restricted lower bounds. All-input correct, not all-input polynomial-time. A distinct post-observation computation phase is NOT necessary on E; process signs while acquiring them and output after endmarker. No representation-independent superpolynomial bottleneck established.

**COMPUTATIONAL evidence:** published code read back and executed in fresh hosted V8 via exported audit() with lightweight Node shims; independent Python check also executed. 5,460 exact sources n=1..6, 126 SAT, 5,334 UNSAT, 1,284 valid whole-block flips, 126 invalid individual flips rejected and 36 malformed controls rejected, all pass. No OS Node CLI, physical TM simulator or LaTeX/preflight. Symbolic claim remains CANDIDATE pending TMR-5 review.

**Peer actions:** TMR-3 should verify one-sweep eligibility and same-input product tightness; TMR-4 must include processing concurrent with observation in any abstraction; TMR-5 should check exact family recognition and the charged all-input fallback; TMR-1 should preserve the fixed-machine all-polynomial quantifiers. The earlier TMR-2/001 input-sensitivity lower bound is unchanged and independently scoped in TMR-5/001.

**Read scope:** five-TMR replacement directive, proof1 full, proof2 full via Git blob, main.tex full via Git blob, AGENTS.md, CODEX.md, repo skill/modes/protocol, latest issue #3, all TMR handoffs, TMR-2/001, TMR-3/001 and original Claude ONETAPE notes. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left for TMR-5 synthesis following independent review. No task/schedule mutations.

**Next single objective:** falsify or construct a source-aware necessity metric charging computational work *irrespective of its temporal interleaving with input reads*, surviving the one-sweep equality decoder, algebraic/Gaussian elimination, arbitrary copying, caching and recomputation. P versus NP remains OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_1420_PST
