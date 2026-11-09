# LSPV-4/514: Clock-oblivious clipped INPUT-head simulation

**November 8, 2026, 23:54 PST | Route A | PROVED/RESTRICTED symbolic lemma + COMPUTATIONAL; native FLMV cost CONDITIONAL. P versus NP OPEN.**

**Exact nodes:** new evidence [P2-L4-514] refines OPEN [P2-A4] and tests peer [P2-L2-515]. Universal [P2-A2], recursive [P2-A5], companion [P1-01]/[P1-03]/[P1-04], and cross-route [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2] all remain OPEN.

## IDEA and predeclared falsifiers

**Hypothesis:** the fixed-horizon clipped INPUT monitor of LSPV-4/505 can be made **independent of advance knowledge of the polynomial guest-time exponent** using clock budgets 1, 2, 4, ... with full guest restart, provided all restart and index-tape costs are separately charged. A low-bit vector plus high-nonzero counter should handle arbitrary guest INDEX-tape overwrites and its native atomic erase, without building astronomical INPUT-head coordinates.

Four falsifiers: (F1) any INPUT symbol disagreement during a horizon; (F2) high-bit overwrite, INDEX-tape erasure or fresh indexed re-entry changes actual guest INDEX observations or INPUT read trace; (F3) geometric restart consumes at least 3T guest steps for a halting T-step guest; (F4) an asserted physical FLMV bound hides guest WORK reset, source/guest index collisions, abandoned output, or all-phase high-water.

This is only an INPUT-port/resource component. It assumes no universal SAT reduction, no semantic oracle, and no free transcript acquisition.

## SEARCH and audited sources

Read complete proof1.txt, starting Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, and proof2.txt, starting blob 1b401cd45f987966d1cc54c91bb36b71dc644bee. Read actual issue #3 comments including LSPV-1/527, LSPV-2/515, LSPV-3/526 and LSPV-5/453; governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e514ddbd747150dcb68607013a3b2d154; AGENTS.md 19656af102604d5f0a721d548cf2e4e72a063561; CODEX.md 754999f50de93cdb693ed37bc8110d31e9e698ef; .codex/skills/pnp-research/SKILL.md b8df83a7b0b1428f349b0e02ce1387d979e8db7f. Peer research/agents/lspv-2/2026-11-08_2312_LSPV2_AFFINE_READ_DECISION_TRIE515.md blob 3c29ef7536316c1aa328f5c3a4e3ee866ca36412 and prior LSPV-4/505,/513 were reviewed. Actual Grok file GROKPROOF/2026-11-06_2316_PROGRESS.md blob a20fb8b3640d7574faf238a4a83a021bb0984808 and Claude research/agents/claude/world-ledger/README.md blob de75a371ce3143a4495e6892df7fb04794a6b708 reviewed.

**Primary model:** Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6), 2005, DOI 10.1145/1101821.1101822; https://lance.fortnow.com/papers/files/tst.pdf, section 2.1, printed page 4 visually inspected. It specifies indexed INPUT (not counted toward WORK), special indexed move erasing the INDEX tape, write-only OUTPUT, and WORK high-water. Polylog sparse simulation is discussed, not a free arbitrary SAT compiler. Urquhart 1987 and Ben-Sasson/Wigderson 2001 certify selected growing expander Tseitin families hard only for ordinary Resolution.

**Change-aware external checks:** konard/p-vs-np/README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2: finite-model scope, no unrestricted NP subset P. blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md blob b30515cced93d8911a6415555ee9ec1444502d93: conditional rank/DP and explicit open acquisition. meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f: separate proof grammar. MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab: source construction. openai/math/CONTENTS.md blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 checked, no all-input FLMV compiler found. Public web searches on indexed machine and decision-tree semantics performed; separate Google-branded service and native FLMV executable unavailable.

## ITERATE: bounded-stage clipped-coordinate theorem

For a deterministic guest with physical binary INPUT length $M$ and stage horizon $H\ge1$, set $B=M+H$ and $\ell=\lceil\log_2(B+2)\rceil$. An indexed INPUT-head coordinate is stored exactly if at most $B$, and otherwise as FAR. In FAR, ordinary unit INPUT-head moves leave FAR unchanged, until the next indexed jump.

The guest INDEX tape has ordinary sequential head motion and permits arbitrary overwrites. Maintain a low-bit vector $L$ at positions $j<\ell$ and a high-nonzero counter $U$ for positions $j\ge\ell$. At a guest INDEX write replace the affected low bit or update $U$ by new_bit minus old_bit, where old_bit is the guest-visible prior INDEX-tape bit. At indexed INPUT jump, set FAR if $U>0$ or $L>B$, else set the precise INPUT coordinate $L$. Clear $L,U$ in accordance with native INDEX-tape atomic erasure. A fresh indexed jump can exit FAR.

**Proof:** At any non-FAR point the coordinate is exact by induction. A FAR coordinate exceeds $M+H$; the guest has at most $H$ remaining unit INPUT-head moves and thus cannot reach any nonblank position $0,\ldots,M-1$ without another indexed jump. After any indexed jump, the low bits and high-nonzero counter recover whether the exact index is within $B$, independently of overwritten bits. Every INPUT read, guest INDEX read, and therefore every deterministic observable action agrees throughout the $H$-step prefix if all other guest state is faithfully simulated. This proves a symbolic trace invariant, **not** complete same-machine implementation.

The clipped coordinate, guest INDEX-head-position counter, $L$, and $U$ require $O(\log(M+H))$ supplemental logical bits. Accessing and maintaining these on actual indexed WORK tapes, mirroring guest INDEX state and erasing it, and source-read port service must be separately paid; a fully compiled FLMV upper bound is **not yet proved**.

## Clock-oblivious geometric-restart lemma

Restart the guest from its original initial state with horizons 1,2,4,..., suppressing output from aborted stages. For a guest halting after $T\ge1$ steps, if $2^{r-1}<T\le2^r$, total guest steps charged across stages are

$$
C(T)=\sum_{j=0}^{r-1}2^j+T=2^r-1+T<3T.
$$

The same bound holds at $T=1$. Thus no prior knowledge of guest time exponent is needed for the **bounded INPUT-coordinate monitor**. If each simulated step, guest tape reset, and virtual-bit operation cost at most polylogarithmic overhead on the **same FLMV machine**, time is conditionally $O(T\operatorname{polylog}(M+T))$. For every fixed polynomial-time guest, $\log(M+T)=O(\log M)$ even though the finite exponent was not supplied in advance. This conditional cost does not establish contraction or full recursive applicability.

**Critical open native obligations:** full guest WORK/INDEX tape replay and reset without temporary high-water blowup; parent-source INPUT indexing while simulating guest indexed INPUT moves; sparse versus dense guest WORK storage; header/length/malformed bytes; cache retention; output suppression without allocating output-length WORK buffers. Only a final constant-size SAT/UNSAT/malformed label is addressed. Longer output streams need a separate bound. No free source decomposition or after-the-fact optimizer is presumed.

## Family/theorem/encoding/shortcut ledger

Established family: odd-charge connected cubic-expander Tseitin 3-CNF with $H$ vertices, $3H/2$ edge variables, and four proper width-three clauses at each vertex ($4H$ clauses), original source length $\Theta(H\log H)$ under an unbounded binary literal encoding. Published exponential hardness applies to **ordinary shared-DAG Resolution** on suitable expanding graphs, not R_mix341 or any SAT algorithm. GF(2) charge-parity elimination is a polynomial-time shortcut and remains a legal upper-bound control. The new port theorem does not transfer Resolution hardness.

Finite authenticated control: signed K4 3-CNF, 6 edge variables, 16 signed original clauses, 8 SAT/8 UNSAT charge sources. Packet comprises magic 0xA5, 8-bit clause count, 48 literal fields each 3-bit ID plus sign, terminal 01, total **210 bits**. The SHA-256 of concatenated 16 ordered physical packets matched in independent Python and Node: 4c8443d4c7ed81f0811ae635bb546368ccba8c421f7e1f38312513848df7c084. K4 is finite, not an asymptotically hard expander.

## Independent verification and all-phase resource charges

Python symbolic reference: 496 guest traces, 5,088 prefix/full assertions, 9,794 guest read observations, 67,712 guest steps, 157,840 total clocked steps (ratio 2.331049), maximum guest INDEX-head position tested 62. Independently authored Node: 464 cases, 9,762 assertions, 8,890 read observations, 71,694 guest steps, 171,582 clocked steps (ratio 2.393255). Third separately published V8 checker: 368 cases, 3,091 assertions, 6,278 read observations, 47,344 guest steps, 114,624 clocked steps (ratio 2.421088). All PASS, including high-bit overwrite, jump erasure, random indexed jumps and partial horizons. The V8 verifier at experiments/arc/lspv4_514_clocked_clipped_input_v8.js (blob d0105b11e951529ed6d2979724d2487a503d6eb6) was **actually executed** and read back. All three raw summaries at results/raw/arc/2026-11-08_2354_LSPV4_514_CLOCKED_PORT_RESULTS.json (blob e9f9852e51e0b665650f102e7f5b91c3f1e4cfe5). The Python and Node originals and exact raw files are in the independent local ZIP archive, not falsely claimed as committed. No native FLMV instruction interpreter, general malformed-input parser/classifier, or historical R_mix341 checker was executed. Abstract port accepts opaque bytes, but actual malformed binary classifications were not tested.

| Phase | Exact or conditional charge | Open implementation issue |
| --- | --- | --- |
| Guest logical steps and geometric restart | fewer than $3T$ | native transition/interpreter overhead |
| Clipped INPUT coordinate, INDEX low/high counters | $O(\log(M+T))$ logical bits | physical layout, random access, erasure |
| Child virtual bit | one exact addressed symbol | parent indexed source access, affine descriptor computation |
| Guest WORK/INDEX | full faithful guest state required | peak physical workspace, clearing, isolation, sparse layout |
| Cache/trie and missed policies | zero in this component | any actual $q$-child solver, fallback, failed policies |
| Output | final classification only | suppress aborted writes; final emission |
| Simultaneous all-phase peak | **not established** | source/ancestor, guest, cache, child and retained history |

This theorem removes a fixed-runtime **parameter** from one low-level monitoring primitive. It does not create the missing sound all-input child reduction, favorable rank bound, or recursive self-composition; [P2-A2], [P2-A4] and [P2-A5] remain OPEN. The ideal free-choice logical refutation DAG of Route B is unaffected. **P versus NP OPEN.**
