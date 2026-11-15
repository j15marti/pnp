# TMR-4/045: Exact shortest physical program for the same extensional gate-record goal

**2026-11-15 05:40 PST (America/Los_Angeles).** Governing fusion-Lipschitz directive SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. **PROVED/RESTRICTED** mathematical theorem for one precisely specified unary record/marker service; independent mathematical review OPEN. Executed finite evidence **COMPUTATIONAL**. P versus NP **OPEN**.

## 1. Candidate and four advance falsifiers

**Candidate:** The extra return-to-header charge in TMR-1/044 is real for its fixed execution program but not forced by the unchanged final output/EOF goal. A *different single fixed uniform deterministic physical program* can place the final header and all marker bits on its FIRST step, write the same n-1 distinct paid gate cells during its forward scan, then read the genuine EOF and HALT on one microstep. The exact minimum across all physically locally moving programs for this separately qualified final-state service is n+1, rather than the slow program's 2n+2.

F1: A supposed fast operation moves a tape head more than one cell, writes multiple cells on one tape, or uses an input-length-dependent opcode. F2: The final-state service secretly requires the **procedural order** "all records first, activation second" rather than just the same completed records, markers, EOF, and HALT. F3: An actual free source read bypasses the paid EOF bound, or a multiread original input interface changes the model. F4: A common tariff is falsely exported to arbitrary SAT deciders, which need not produce these records or inspect EOF on both labels. F1 is excluded by a complete transition table and replay; F2 is an explicit **different-system** boundary, not a claim that TMR-1's original fixed machine has a faster edge; F3 is outside the declared physical model; F4 is OPEN and no transfer is claimed.

## 2. Corpus and literature reconciliation

Read FIRST the approved 2026-11-14 fusion tariff directive, followed by the 2026-11-13 TMR replacement directive, complete proof1.txt SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, authentic complete Git blobs proof2.txt SHA 930c5eeddafce656717f28055a7a9a755f44737c and root main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (the normal oversized-file contents API returns blank, not empty stored content), issue #3 and recent comments, AGENTS.md, CODEX.md, repository pnp-research skill, all five latest TMR handoffs, original TMR-1/044, TMR-3/043, TMR-5/040, TMR-4/044 reports and the TMR-1/TMR-5 original executed scripts and tariff JSON, TMR-2/044 Feistel compact-circuit countercontrol, and historical LEAD-0029 Lipschitz audit. Historical /341 remains **FAIL** as full logical UNSAT authority; /386 remains **RESTRICTED** in its tested guarded fragment.

Primary methodological literature verified: P. Cousot and R. Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints," POPL 1977, DOI https://doi.org/10.1145/512950.512973, covers abstract-execution soundness; R. E. Tarjan, "Amortized Computational Complexity," SIAM Journal on Algebraic Discrete Methods 6(2), 1985, DOI https://doi.org/10.1137/0606031, supplies potential-method context; F. C. Hennie and R. E. Stearns, "Two-Tape Simulation of Multitape Turing Machines," JACM 13(4), 1966, DOI https://doi.org/10.1145/321356.321362, emphasizes the quantitative importance of the actual tape model. None proves this elementary new record-service theorem.

**Novelty relative to these project reports:** TMR-5/040 established a partial n+1 tariff for the *slow* program; TMR-1/044 exactly matched that slow program's 2n+2 runtime using a phase-sensitive backward-head coordinate. This report constructs an **alternate fixed physical program meeting the same extensional terminal service**, proves a universal service lower bound n+1 for all such programs, and provides a new complete common seven-column tariff/dual for both physical traces. It neither falsifies nor relabels the exact prior TMR-1/044 *program-specific* theorem.

## 3. Concrete extensional service, two honest programs and cost ledger

Fix m>=1 ONCE as a constant number of designated separate marker tapes. A successful promised source is original read-only 1^n# with n>=2, physically occupying N=n+1 consecutive cells with its sole input head initially at cell 0. One initially blank stage tape W with one locally moving head, m initially blank independent output tapes O_i, fixed finite control, finite alphabets {blank,0,1,g} for W and {blank,@} for each O_i. Each physical transition reads one scanned symbol from each tape, writes at most ONE cell **per tape**, moves each head by at most one position, and costs exactly 1. Program identity, full control/head/tape contents, the immutable input, paid gate-cell identities, source read history, output/interface status and all obligation flags are retained in the complete concrete configuration. There are no physical zero-price transitions. The physical zero-cost SCC quotient and cl0 are identity.

The **extensional GOAL**, deliberately distinct from a mandatory stage-then-activate procedural order, is: source # actually inspected; W[0]=1; all W[j]=g for 1<=j<n, each with a distinct actual paid write; O_i[0]=@ on each of the m separate tapes; and actual HALT after those output markers were placed. This service does not demand output proof interpretation, a prescribed computation tree, or a SAT decision.

**New single fixed deterministic program M_DIRECT (same fixed transition table for all n):**

| Control | Scanned input and actual microstep | Successor | Cost |
|---|---|---|---|
| FIRST | On first 1: write W[0]=1 and all m O_i[0]=@; move original input and W heads right one | GATE | 1 |
| GATE | On each subsequent 1: write ONE unique W[j]=g at current work head, move original input and W right one; retain GATE | GATE | 1 each |
| EOF_HALT | On authentic # after at least one GATE record: read the # and enter HALT simultaneously; no new write | HALT | 1 |

The repeated 1 transition uses a fixed finite control loop; the number n is NOT encoded in the program, nor does it use a giant one-price AND macro. A constant-sized state refinement distinguishes whether the first GATE record has occurred, rejecting too-short/malformed input if a total recognizer outside the successful promise is required. The real successful path has n distinct W-cell writes, each charged in its own microstep, n-1 individually paid gate records, m physical output writes to m **distinct** tapes on FIRST, and one final EOF read/HALT microstep. **Exact length n+1**. The output markers precede the actual HALT, satisfying the temporal requirement.

**Peer slow program M_STAGE_OUTPUT_m:** Original TMR-5/040 rules INIT 1, GATE n-1, EOF_BACK 1, BACK_G n-1, ACTIVATE_AND_MARK 1, HALT 1 cost a total **2n+2** and reach exactly the same extensional terminal tape obligations. Its additional demand to postpone activation/marking and return its work head is a property of its fixed control path, not an extensional requirement of these final outputs. Never call a fast transition legal in the original slow program.

## 4. Universal physical lower bound for this extensional goal

**Theorem TMR4-045(A), PROVED/RESTRICTED:** For every m>=1 fixed and every n>=2, any deterministic physical finite-tape program A with the specified single original locally moving input head starting at position zero, whose successful terminal state satisfies the above GOAL, must execute at least n+1 paid transitions; a *single fixed program M_DIRECT* simultaneously attains n+1 for all n. Therefore the minimum across ALL such programs is exactly

$$
\boxed{\min_A T_A(1^n\#)=n+1.}
$$

**Proof:** The first source position visible before transition 1 is cell 0. Because the head moves by at most one cell per transition, the authentic right endmarker at source cell n cannot be inspected earlier than transition n+1. Inspection is a conjunct of GOAL. Hence every goal-reaching execution pays at least n+1 unit-cost transitions, regardless of encoding of work, caching, precomputation, branching, compact circuits, affine/Gaussian operations or output sharing. M_DIRECT's three finite-control rule classes above inspect cells 0 through n in n+1 successive steps, write every mandatory cell in a distinct legal on-tape operation, and halt successfully. The SAME uniform fixed program works for every n and for its fixed m. QED.

A constant-size record grammar and explicit EOF requirement are essential. This is at most **linear** in encoded input length. It does not prove an input-length lower bound on SAT machines allowed to decide without that explicit output service.

## 5. All-step reduced product, zero closure, signed matrix and rational LP

Define common seven-column reduced product, with identical coordinate semantics for **both** program traces:

$$
p(C)=(0,0,0,a(C),q(C),u(C),o(C)+h(C)).
$$

Here a=1 iff W[0] is not yet 1, q is the number of missing W[1..n-1] paid g symbols, u=n+1 minus the number of authenticated source-prefix cells already scanned (max-rightmost frontier, including #), o is the count of missing @ markers across all m designated output tapes, and h=1 until HALT. The initial state of either machine has

$$
p(C_0)=(0,0,0,1,n-1,n+1,m+1),
$$

and p(GOAL)=0. Every real source access, head movement, gate write, output marker and halt is charged; combining them on distinct tapes happens in ONE paid microstep, with each paid gate identity counted once. All genuine goal obligations remain conjunctive.

**Full rule-by-component matrix:** order CNF,XOR,SEP,FUS,Gamma,Interface,Machine; all first three deltas zero. All prices 1.

| Real rule | Delta FUS | Delta Gamma | Delta Interface | Delta Machine |
|---|---:|---:|---:|---:|
| M_DIRECT FIRST | 1 | 0 | 1 | m |
| M_DIRECT GATE | 0 | 1 | 1 | 0 |
| M_DIRECT EOF_HALT | 0 | 0 | 1 | 1 |
| M_STAGE INIT | 0 | 0 | 1 | 0 |
| M_STAGE GATE | 0 | 1 | 1 | 0 |
| M_STAGE EOF_BACK | 0 | 0 | 1 | 0 |
| M_STAGE BACK_G | 0 | 0 | 0 | 0 |
| M_STAGE ACTIVATE_AND_MARK | 1 | 0 | 0 | m |
| M_STAGE HALT | 0 | 0 | 0 | 1 |

The exact nonnegative cone for a **single common vector of weights valid independently for both qualified fixed programs** is

$$
\boxed{f+i+mt\le1,\qquad g+i\le1,\qquad i+t\le1,\qquad f,g,i,t\ge0.}
$$

All slow-program constraints are implied by the three fast-program constraints for nonnegative weights. Necessity is witnessed by each genuine fast rule. Sufficiency follows by checking the COMPLETE nine authentic successful-source rule classes; no zero-cost edge decreases the vector. In particular the real FIRST step jointly discharges header activation, source progress and m output markers, while final EOF_HALT jointly discharges EOF and termination.

**Exact rational primal and dual:** Maximize the common initial scalar potential

$$
\max \{ f+(n-1)g+(n+1)i+(m+1)t \}
= \boxed{n+1}.
$$

Primal certificate is (f,g,i,t)=(0,0,1,0); in canonical seven columns lambda=(0,0,0,0,0,1,0). Exact dual assigns row multiplicities (1,n-1,1) to FAST_FIRST, FAST_GATE, FAST_EOF_HALT, with total price n+1. Their weighted discharge covers the initial vector *exactly* componentwise: (FUS,Gamma,Interface,Machine)=(1,n-1,n+1,m+1). Primal and dual costs coincide, so exact rational LP optimality is proved independently of finite testing. This is a **shared calibration of two different programs**, not an assertion of free switching between their machine states.

**All-program cost-underestimating simulation lemma:** For any eligible locally moving physical program, let r(C) be the number of original input positions in its authenticated scanned prefix, capped at n+1; abstract to u(C)=n+1-r(C). For every real paid unit transition C->C', r(C')-r(C) is 0 or 1 (the head can reread, move left, cache, recompute, learn, use Gaussian operations, or write on many separate tapes, but cannot newly scan two original source cells in one move). The abstract transition u->u' of price at most 1 simulates it; all completed GOAL states require u=0. The source-only potential u has Delta<=1 on every physical step. No arbitrary machine control is incorrectly discarded from the concrete relation: retain the full C and all paid histories in the concrete/abstract pair. Unknown future source interfaces with more original read heads are MAY and require requalification.

A proposed **2n+2 program-sensitive** phase/return potential is sound for M_STAGE_OUTPUT_m, but CANNOT be transported to the **all-program** version of the same extensional GOAL, since the authentic M_DIRECT length n+1 trace would contradict its initial bound. This is a genuine cheaper alternate-program control, not a violation of an original M_STAGE transition. CEGAR must retain the fast program when the larger program class is the target.

## 6. Reproducible evidence, hostile controls and status

**Exactly executed original native V8 audit function** is serialized into experiments/tmr/tmr4_direct_program_gap099.js and read back byte-for-byte from the publication branch. It replays each real state transition with full W/output cells, input/work head positions, source frontier, individual distinct gate records, output symbols and terminal checks. For n=2..96 and m=1..5: **475 fast and 475 slow complete traces**, 71,250 paid physical transitions, 935,220 assertions, 6,594 finite rational-grid feasible-certificate checks, **zero failures**. The 47,025 naive per-component unweighted overcharge detections are warnings, not rejected legal paths. No randomness. The typed seven-column raw matrix, exact summary and source are separately published. The symbolic theorem holds for all n; finite evidence status remains COMPUTATIONAL. Native OS Node executable was not independently launched and no full checkout-based repository preflight/LaTeX run was possible in this connector-only environment.

Hostile controls: FIRST simultaneously writes one stage header and one marker on each **different** output tape, never m cells on one tape; EOF_HALT fuses source inspection and halt without an extra fictitious step; all gate identities have separate paid W writes; stage return steps remain priced in M_STAGE; compact circuits, Boolean algebra, Horn/Krom, affine/Tseitin, autarkies, bounded treewidth, equality, learning, renaming, padding, rereading and recomputation are permitted for richer SAT machines rather than excluded by this trivial unary-output service; free EOF access, absent records, different original interface or a mandated activation-order change would be a **different** service/model. Zero-cost closure is identity in each physical program, not just SCC-only. Historical /341 FAIL full language; /386 RESTRICTED.

**Relative dependency statuses:** M_STAGE original 2n+2 program-specific tariff remains **PROVED/RESTRICTED** and unchallenged; M_DIRECT fixed-program n+1 upper bound plus universal goal-EOF n+1 lower bound **PROVED/RESTRICTED, peer review OPEN**; two-program joint signed matrix/LP certificate **PROVED/RESTRICTED, peer review OPEN**; finite V8 replay COMPUTATIONAL; superpolynomial SAT-machine initial potential and unrestricted same-system transfer **OPEN**. No contradiction with TMR-2/044's separate nonlinear Feistel rank countercontrol. P versus NP **OPEN**.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt, proof2.txt, root main.tex and all five schedules left unchanged. Ownership preserved.

**Next:** TMR-3/5 should independently verify M_DIRECT's first/last physically simultaneous writes and enforce the honest extensional-versus-procedural goal boundary. TMR-1 should incorporate this new program-quantifier guard. TMR-2 should seek a SAT-specific dynamic obstruction that survives early header staging, compact nonlinear circuits and this same-goal alternate-program shortcut. TMR-4 next should replace the unary service with TMR-2/044's physically charged signed-Feistel family recognizer and explicit fallback, preserving the genuine polynomial fast path.