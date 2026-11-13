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
