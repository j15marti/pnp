# LSPV-2/466: Shifted native WORK index for epoch-stamped SAT guest calls

**November 7 2026, 03:08 PST | Route A LSPV-2.** Status: **PROVED/RESTRICTED** for an indexed-WORK-tape coordinate lemma under stated index-bit/head conventions; **COMPUTATIONAL** for finite independent host checks; **OPEN** for the complete native FLMV interpreter, universal all-input recursive contraction, and P versus NP.

## IDEA -> SEARCH -> ITERATE

**Idea:** Prior epoch-stamped virtual WORK-tape constructions (LSPV-4/458) assume charged numerical work-index conversion, while DATA/MARK/dirty-log alternatives (LSPV-4/461) require cloned work indices. Instead embed an entire guest WORK tape in one physical WORK tape, mapping guest cell i to the base of an R-cell record at Ri, and shift each corresponding index bit by a fixed number of sequential index-tape positions. This uses the native indexed head move, not a costly arbitrary-address decoder.

**Falsifiers stated before source review:** (F1) native index-bit orientation or erasure-head semantics invalidate shifted positions; (F2) generation tags wrap or expose stale work data; (F3) a sparse high-address indexed jump forces high-address-proportional reset *time*; (F4) ordinary guest WORK/index head moves fail to preserve the invariant.

**Primary model reviewed:** Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), Section 2.1, author PDF page 4 (physically inspected): https://lance.fortnow.com/papers/files/tst.pdf . Work tapes have associated sequential index tapes; indexed jumps erase the index contents; largest work address accessed contributes space, though index-tape length does not. The paragraph does NOT completely fix bit order or index-head semantics, so both are explicit simulation hypotheses below. The FLMV lower bound remains unconditional only in its published machine model.

**Project continuity and exact proof-chain IDs:** Read both /proof1.txt and /proof2.txt, particularly [P1-S3], [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-B2]. Inspected issue #3, governing 2026-11-02 five-role handoff, AGENTS.md, CODEX.md, research skill, peer LSPV-4/458,/461,/462,/463,/464, LSPV-2/465, actual Grok 2026-11-07_1030 progress and Claude world-ledger README. Previous epoch tags and work-index accounting are acknowledged prior art; the particular direct native bit-shift implementation is the **restricted** refinement being tested.

**External source checks (actual GitHub files):** konard/p-vs-np README.md and proofs/complexity/README.md (different finite one-tape P subset NP model); blkph0x/p-vs-np-proof-research README.md and METHOD_INDEX.md (bounded/promise results); openai/math README.md (mixed formalization status); berkeley-abc/abc README.md (AIG optimization, not tape semantics); meelgroup/frat-xor format.md (distinct external mixed-proof grammar). Targeted web searches of FLMV indexed tapes and Ben-Sasson/Wigderson Resolution hardness; no separate Google-branded search was verified. None supplies all-input SAT contraction.

## Lemma 466.1: exact native WORK-index coordinate lift (PROVED/RESTRICTED)

Fix a binary indexed WORK tape W and sequential binary INDEX tape I in which index bit b_j contributes b_j 2^j, and assume native index jumps erase I while head positioning is preserved or recoverable with explicitly charged O(d) steps.

For a known bound q >= 1 on guest calls, set

$$
r=\max(1,\lceil\log_2(q+1)\rceil),\qquad d=\lceil\log_2(r+1)\rceil,\qquad R=2^d.
$$

Represent guest WORK cell i by a physical block [Ri,Ri+R), with an r-bit *nonzero* current-generation tag and one data bit. Store guest index bit b_j at host INDEX position j+d; positions 0,...,d-1 remain zero; host index head position is guest index head position plus d. Then

$$
a_{\rm host}=\sum_{j\ge0}b_j2^{j+d}=R\sum_{j\ge0}b_j2^j=Ra_{\rm guest}.
$$

Therefore the ORIGINAL native indexed WORK-head move lands at the correct guest-cell block base without ever constructing or copying the guest's arbitrary-precision address into an auxiliary controller. The native INDEX erasure corresponds exactly to the guest INDEX erasure. Ordinary guest WORK moves cost R physical steps, and each read/write costs O(r) local tag/data steps. On invocation j, write the tag j (1 <= j <= q); an absent or differently tagged cell reads as blank, so previously used work cells do not leak across invocations. This is the standard generation-tag invariant combined with the explicit native index-place shift.

**Proof:** Induction over guest operations. The index-bit shift and index-head displacement are invariant under one-cell INDEX writes/moves. At a jump, the displayed arithmetic equality makes the host WORK head land at R times the guest address; both index tapes are erased. Work moves map one guest cell to exactly R physical moves; scanning tag+data and restoring the base position makes read/write semantics exact. At each new invocation, all tags differing from its nonzero new tag are interpreted as blanks. The generation field has at least q nonzero values, so no wrap occurs. This is an exact restricted simulation of the one WORK/INDEX pair, not a whole-machine compiler.

## Lemma 466.2: charged reset and resources (PROVED/RESTRICTED)

Let T_j be guest transitions, S_j the maximum guest WORK position read/indexed, and L_j the greatest sequential INDEX-head position reached during guest j. L_j <= T_j+O(1). At guest return, erase the physical INDEX tape by a sequential sweep over visited cells and reposition its head, O(T_j+d); leave physical WORK data intact, increment epoch, and perform a blank-index native jump returning the WORK head to the base at address zero. Crucially, do NOT jump to the huge old index value merely to clear the index.

$$
S_{\rm physical}\le R(\max_j S_j+1)+O(r),\quad
T_{\rm work+reset}=O\left((r+R)\sum_{j=1}^q(T_j+1)+qd\right).
$$

With q <= N^{3/5+o(1)}, r,R=O(log N), d=O(log log N), this isolated WORK/INDEX simulation adds polylogarithmic overhead and preserves the guest component's exponent 3/5+t/2 in time and s/2 in work-space under B<=N^{1/2+o(1)}. A jump to 2^40 is a high-space event with physical work high-water of order R 2^40, NOT free space. This does **not** prove source-port input indexing, complete machine simulation, full construction/search costs, malformed-input handling, arbitrary A source extraction or recursion.

## Independent finite verification (COMPUTATIONAL)

The executed Python sparse host/reference guest simulator used seed 46620261107: 350 guest invocations, 2,796 guest operations, and 15,185 assertion groups across q=1,2,3,7,16,64,257, with stale-cell checks, index-head displacement and work-head movements. A high-bit index jump to 2^40 verified large sparse address and constant-time logical reset (while correctly charging huge space). A separately written JavaScript verifier exhaustively executed 10,000 two-call four-operation traces, 40,000 actions, 213,400 assertions (PASS). This is host-language semantic testing, not a native FLMV machine.

For original source SAT/UNSAT controls, K4 signed ternary Tseitin uses 4 degree-3 parity clauses per vertex, 16 proper 3-CNF clauses total, 6 edge variables; even total charge is SAT, odd total charge UNSAT by exhaustive truth table. These **finite** labels are not asymptotic proof-size lower bounds.

## Established hard-family / known-shortcut ledger

| Family | Encoding and size | Certified theorem and proof system | Shortcut and transfer limitation |
| --- | --- | --- | --- |
| Odd-charge connected cubic-expander Tseitin F_H | One edge variable each, each degree-3 vertex parity constraint encoded as its 4 forbidden signed proper 3-clauses; 4H clauses, 3H/2 variables, N=Theta(H log H) under binary integer-ID encoding | Ben-Sasson/Wigderson (2001) expansion + width implies 2^{Omega(H)} **ordinary DAG Resolution** refutation size | Gaussian elimination GF(2) polynomial SAT/UNSAT decision; no all-machine lower bound and no bound for unrestricted R_mix341 without transfer |
| K4 even/odd charges | 16 proper 3-clauses, 6 variables | Finite truth-table SAT/UNSAT check only | No growing-instance hardness inference |

No equivalence-preserving 3-CNF reduction is claimed to preserve a proof-system lower bound. Haken Resolution and Cook Extended Resolution remain distinct mandatory controls, not evidence of full mixed-calculus hardness.

## Accounting, publication, and gaps

Explicitly paid in this isolated primitive: shifted INDEX writes/moves, native index jumps and erasure, WORK tag scans and ordinary head movements, source-independent fresh epoch, sequential INDEX cleanup and work-head reset, controller generation bits and physical WORK high-water. Unproved in the *complete wrapper*: multiple-tape native composition, guest virtual-input random access and source index maintenance, external-source authentication and malformed-input rejection, output handling, failed search, source exploration, retained messages and caches, materialized vs lazy child bit representations, explicit certificate output and verification, and all-phase peak work space. No historical R_mix341 grammar, inference weight or proof rule changed.

Relevant [P2-A4] receives only restricted supporting evidence. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-B2], B3 and P vs NP remain **OPEN**. Preserve existing 2 Route A / 3 Route B roles and schedules. The full native source/compiler and all-input recursive solver-dependent A -> Phi(A) contraction are NOT established.

**Actual advance:** native index-coordinate shift avoids a separate arbitrary-precision WORK address decoder for one directly packed WORK/INDEX tape. **Verification:** mathematical restricted proof plus independent finite checks. **Remaining gap:** full same-machine and universal all-input recursive contraction.
