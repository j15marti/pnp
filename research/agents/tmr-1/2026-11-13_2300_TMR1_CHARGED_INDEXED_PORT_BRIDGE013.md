# TMR-1/013: charged binary-address input-port simulation and quantifier bridge

**Date:** November 13, 2026, 23:00 PST (America/Los_Angeles). **Role:** TMR-1 Machine Model Lead. **Repository:** j15marti/pnp, main.

**Status:** New model-transfer theorem **CANDIDATE pending independent TMR-5/TMR-4 review**. The finite index-trace audit is **COMPUTATIONAL**. This is a polynomial-simulation arrow, not a lower bound. P versus NP and the general superpolynomial processing bottleneck remain **OPEN**.

## 1. Exact distinct models and source binding

Fix binary source word x of exactly L encoded bits between endmarkers at positions 0 and L+1. The classification is 3-SAT on a fixed explicit valid-input encoding and a fixed total behavior on malformed binary strings. A is one *fixed*, finite, total, uniform deterministic program across every L, with finite-state control, a fixed finite alphabet and a fixed number of locally moving writable work tapes. Count every transition and every visited writable cell on the same input execution, including address construction, input access, indices, scratch, representation conversion, source caching and recomputation.

**Local model M_local:** one read-only original-input head moves at most one adjacent source position per transition, and reads the current pre-move symbol. A fixed number of ordinary mutable work tapes and heads is allowed.

**Indexed source-port model M_idx(w):** A has the same ordinary local work tapes plus one idealized read-only source port. The query address is a delimited binary field on one **ordinary charged writable address tape**, with at most w=ceil(log2(L+2)) data bits and a one-bit invalid/overflow tag, with the address-tape head at the field's left delimiter when a query is issued. Any register updates, length determination and ordinary work are charged as local work-tape transitions. On a source-query transition the port returns x_j for 0<=j<L and the distinguished right/end-of-range symbol R otherwise. The port can read the finite bounded-length address field *in one transition*. That last operation is a deliberately stronger, explicitly declared primitive. It is not a free oracle for SAT, not unbounded-word arithmetic, and not random access to arbitrary growing work memory. Ordinary simultaneous work-tape read/write/head movement still uses a fixed finite transition table.

The invalid tag is needed for an out-of-range test address such as j=L+3 that may require more than w data bits. It returns R without magically extending a w-bit register. Endmarkers and malformed 3-CNF inputs are preserved and both SAT/UNSAT terminal labels are mapped exactly.

## 2. New constructive theorem TMR1-IP13

**Claim (CANDIDATE pending peer review).** For every one fixed total M_idx(w) program A there is one fixed finite total local-input multitape program B_A, depending on A but NOT on L, such that for every binary source x of length L,

$$
\operatorname{out}_{B_A}(x)=\operatorname{out}_A(x),
$$

$$
T_{B_A}(x)\le d_A(L+2)(w+1)(T_A(x)+1),
\qquad
S_{B_A}(x)\le S_A(x)+(L+2)+d_A(w+1).
$$

Here d_A>0 is a constant depending only on A's finite machine description. Any fixed multiplicative slack in the number of local simulator work tapes is absorbed in d_A. The bounds hold on the *same source and same simulated A execution*, not for a length-by-length family of programs.

**Construction and every-transition proof.** B_A first performs a paid left-to-right sweep copying L data bits and both source endmarkers to one ordinary writable tape. It then rewinds that tape's head. The literal copy/rewind implementation of TMR-1/012 takes 2L+3 transitions; preparing a binary counter and the width w requires at most O(L+1) additional local steps and O(w+1) writable cells. B stores A's fixed finite control and preserves all original A work-tape content/head positions. Each nonquery A transition is simulated by a bounded number of B transitions. For a query, B temporarily inspects the delimited address field on the charged A address tape, restores its original head and content, computes the desired position j or invalid tag in an auxiliary w+O(1)-bit binary counter, and walks the source-copy head locally to the data cell j+1. Comparison, increment/decrement and orientation of the counter take O(w+1) local steps per walked copy cell; at most L+1 source-copy moves are needed because the head always remains within the copied endpoints. Invalid/out-of-range queries return R. The fetched finite-alphabet bit is held in finite control while B executes precisely the queried A transition (original work symbols, writes, head directions and next control); B's private copy/counter workspace is outside the simulated A state. Restore the A address-head position before the logical transition; then apply A's original action. Therefore one simulated query needs at most d_A(L+2)(w+1) transitions, including width decoding, walking, local-work update, and restoration. Induction on A's entire actual transition trace shows exact simulated state preservation and both outputs. Totality follows because every finite scan and every A execution terminate.

The source copy consumes L+2 cells. The binary width/counter/restoration bookkeeping consumes O(w+1) additional cells. Every cell visited by A is preserved and counted, giving the stated same-machine space inequality. No random access survives inside B.

**Scope audit:** This is a standard polynomial slowdown, NOT a one-for-one simulation. The TMR-1/012 additive 2L+3 bound applies to bounded local source heads, not to the present indexed source-query port. The exact constants above are not claimed to apply to arbitrary unbounded-word RAM or arbitrary indexed work memory. No statement about a restricted small-space solver survives the extra Omega(L) copy space.

## 3. Exact separation-quantifier transfer

Let Q_local be the required all-exponent SAT target for every correct local-input B:

$$
\forall B\;\forall k\ge1\;\forall C>0\;\forall L_0\;
\exists F\text{ valid},\quad |F|\ge L_0,\quad
T_B(F)>C(|F|+1)^k.
$$

The constructive simulation yields

$$
\boxed{Q_{\mathrm{local}}\Longrightarrow Q_{\mathrm{idx}(w)}.}
$$

**Proof.** Fix any one correct total indexed-port A, target integer k>=1, C>0 and L0. Let d_A be the constant in the theorem. For every L>=0 we have

$$
(L+2)(w+1)\le4(L+1)^2.
$$

Apply Q_local to the fixed simulator B_A at exponent K=k+2, threshold L0 and constant C_B=4d_A(C+1). This yields a valid F with L>=L0 and

$$
T_{B_A}(F)>4d_A(C+1)(L+1)^{k+2}.
$$

The proved simulation inequality then forces

$$
T_A(F)+1>(C+1)(L+1)^k,
$$

and hence

$$
T_A(F)>C(L+1)^k.
$$

No cross-machine resource pairing, input-dependent program, universal all-UNSAT hard family, or single input that defeats all A is required. The simulator B_A is one fixed program, and the hard formula is permitted to depend on A,k,C,L0. The *same* exponent k is recovered for A even though B's target exponent is k+2. This is a strict consequence of the all-k quantifier, not evidence that Q_local itself is true. The reverse implication is not asserted here.

**Resulting dependency DAG:** exact indexed port contract -> all-concrete-transition charged simulator -> fixed-program polynomial time bound -> Q_local to Q_idx(w). The missing upstream statement Q_local remains OPEN. TMR-4's after-copy source-observation potential is zero because all source bits have been seen. TMR-3's sequential-cut crossing product can become true for B solely because it physically copied its source; this does NOT transfer to an indexed A as a comparable same-machine product. The only valid transfer here is the unrestricted all-exponent **time** target via the charged polynomial slowdown.

## 4. Hostile controls, reproducibility and actual evidence

Published exact executable: experiments/tmr/tmr1_indexed_port_bridge013.cjs. Raw results: results/raw/tmr/2026-11-13_2300_TMR1_INDEXED_PORT_BRIDGE013_RAW.json.

A deterministic JavaScript/V8 test driver was actually executed on all binary sources of lengths 0..9, six synthetic indexed-address access patterns and eleven accesses per pattern. It compared the direct indexed-source symbols and deterministic finite controller against a separately charged walk along an exact copied source with a binary-counter-width ledger. 6,138 paired cases; 67,518 queries; 2,453 accepting and 3,685 rejecting synthetic outcomes; 19,550 invalid/right-marker requests and 31,494 repeated addresses; zero symbol/controller mismatches, zero resource-bound violations and zero auxiliary-space violations. Source code and immutable raw were each published and read back byte-for-byte.

**Limitations of the finite audit:** It is an executed **hosted V8** driver of indexed query transcripts, not native Node replay, not a full finite-state multitape-Turing-machine emulator and not a 3-SAT decider. The address sequences are a test driver, not a proof that those scripted sequences form a finite-controller A without any preprocessing. The counter-charging bound is deliberately conservative and only checked for those finite traces. The *all-length* mathematical conclusion rests on the constructive argument above and awaits independent review.

**Adversarial requirements preserved:** A may use Horn and 2-SAT fast paths, exact XOR/Tseitin Gaussian elimination, bounded-treewidth dynamic programming, direct products and shared computation, auxiliary variables, renaming, padding, reencoding, caching, input rereading and arbitrary polynomial workspace. These choices are not excluded by the proof and no computationally necessary representation is assumed. The synthetic test checks repeated/last-cell/invalid indexed reads and both labels; it does NOT separately run those specialized satisfiability families.

## 5. Primary literature and prior corpus

1. Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (2005), DOI https://doi.org/10.1145/1101821.1101822. The original publisher abstract states a *joint time and small-space exclusion* for random-access Turing machines with c below the golden ratio and a positive space exponent d. It does not establish any all-polynomial-time lower bound, and its precise indexed-machine model is not substituted for our deliberately specified binary-address port without further proof.
2. Hartmanis and Stearns, *On the Computational Complexity of Algorithms*, Transactions AMS 117 (1965), 285-306, DOI https://doi.org/10.1090/S0002-9947-1965-0170805-7. Classical time-resource foundations; not cited as proving the present concrete port emulator.
3. Katajainen, van Leeuwen and Penttonen, *Fast Simulation of Turing Machines by Random Access Machines*, SIAM J. Comput. 17(1), 77-88 (1988), DOI https://doi.org/10.1137/0217005. This is the reverse TM-to-RAM simulation under a logarithmic cost criterion; it is not used to prove the port-to-TM direction.
4. Project original TMR-1/012: research/agents/tmr-1/2026-11-13_2204_TMR1_MULTI_INPUT_HEAD_COPY_BRIDGE012.md and its literal source executable/raw. TMR-4/013: research/agents/tmr-4/2026-11-13_2245_TMR4_COPY_READY_POTENTIAL_TRANSFER013.md. TMR-3/011: research/agents/tmr-3/2026-11-13_2233_TMR3_CROSSING_SPLICE_AUDIT011.md. TMR-2/012 and TMR-5/009 countermodels/peer audits likewise reviewed.

**Corpus/status:** Read first the controlling 2026-11-13_1249 replacement directive; both trackers, proof1 (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and authentic proof2 via Git blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c); main.tex via Git blob (2,511,782 characters, SHA c04a02a97492f88938791f363ff91d99b67cd78b); AGENTS.md, CODEX.md, skill, latest issue #3, all five current TMR handoffs and materially relevant original reports/code/raw. Older LSPV governance is superseded. The primary literature source abstracts were inspected directly. No new proof-status change in a root proof chain is warranted. **TRACKERS REVIEWED; NO MATERIAL CHANGE**. Root main.tex left unchanged for TMR-5 synthesis. No scheduled tasks created, revived or modified.

## 6. One next target

TMR-5/TMR-4 should independently inspect the single-step indexed source-query micro-simulation, especially the binary address tape head restoration, overflow/invalid tag, counter travel overhead and preservation of all original writes. Then ask whether the TMR-3 restricted crossing product survives this explicit indexed-port-to-local conversion with enough magnitude to imply anything about A after dividing out the paid polynomial slowdown and the extra source-copy space. An all-exponent post-acquisition processing necessity remains **OPEN**.

END_OF_REPORT::TMR1::2026-11-13_2300_PST
