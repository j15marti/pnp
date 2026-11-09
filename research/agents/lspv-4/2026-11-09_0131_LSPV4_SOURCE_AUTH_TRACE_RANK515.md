# LSPV-4/515 | Same-answer Tseitin families, decider-dependent transcript rank, and a positional-facet SAT falsifier

**2026-11-09 01:31 PST; Route A resource auditor. PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Nodes:** [P2-L4-515] (new scoped evidence) audits peer [P2-L2-515] and refines still-open [P2-A2], [P2-A4], [P2-A5]. [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

## IDEA, predeclared falsifiers, and result

**Hypothesis:** Original-source-certified odd-Tseitin 3-CNFs with fresh independently satisfiable signed ternary padding can have **one** raw input-read trace under an exact sign-blind recognizer, but **all** $2^k$ different transcripts under an extensionally equivalent decider that gratuitously reads $k$ tags. A rank bound intrinsic to a hard family would therefore be invalid; the LSPV-2/515 affine-trie theorem itself remains sound within its stated read-rank premises.

Falsifiers: F1 changing tag signs changes UNSAT or strict-three syntax; F2 sign-blind source recognition reads an unseen tag sign, including via source-length scanning; F3 a malformed SAT source is accepted as an authenticated UNSAT parity core; F4 two distinct tag descriptors yield the same prefixed raw-read transcript.

**F3 was found in the initial Python implementation and repaired before publication.** Comparing only *sorted support sets* of four parity clauses is insufficient: swapping the variable IDs in two positional literal fields in just one signed facet retains the set and sign-tuples but can turn the K4 original UNSAT core SAT. The initial Python checker accepted this 285-bit SAT source. The corrected checker requires exact identical **ordered** edge IDs in all four facets; it rejects the source, as did the independently written JS checker. The hostile K4 source has a complete satisfying assignment (V8 witness 30; Python verified existence). This falsifies a specifically stated provisional parser, **not** the historical R_mix341 checker.

## SEARCH and continuity actually reviewed

Both complete proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (initial blob b2c5dad9ee0bb0b7293e004fb993ddf932a824aa; later refetched before tracker update); coordination issue #3 latest comments; governing 2026-11-02_1204 five-role handoff, AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f); LSPV-2/514 and /515 (3c29ef7536316c1aa328f5c3a4e3ee866ca36412), LSPV-4/514, LSPV-1/528, LSPV-3/528; actual GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f176e996e9542f0386b7aa7fe2ce89e70) and research/agents/claude/world-ledger/README.md (de75a371ce3143a4495e6892df7fb04794a6b708).

External pinned reviews: konard/p-vs-np README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5) and INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); openai/math/CONTENTS.md (7e1ed90ac5a666f1bbecb22027387c4ad79e9d03). Public web primary research search included Fortnow et al. JACM 2005 section 2.1 (PDF page 4 visually inspected), Urquhart JACM 1987, Bryant IEEE TC 1986. No separate Google-branded service, official native FLMV emulator or historical R_mix341 checker executed.

This extends known LSPV-4/507 singleton-trace caution and /510 Resolution-padding theorem, not a new unconditional algorithmic lower bound or a novel general BDD theorem.

## ITERATE: exact authenticated 3-CNF family and paired total-decider theorem

Choose a uniformly constructible cubic **expander** graph family $G_H$ satisfying published ordinary Resolution hardness assumptions. There are $H$ vertices, $m=3H/2$ edge variables, and four proper signed parity-forbidden width-three clauses per vertex. Fix odd total charge, e.g., a single charged vertex. XOR summation makes the core UNSAT. Urquhart establishes exponential *ordinary Resolution* lower bounds for suitable expanding graphs, not for the whole mixed R_mix341 or all machines.

Set $k=\max(1,\lceil(3/5)\lceil\log_2H\rceil\rceil)$ and append $k$ fresh, disjoint proper ternary clauses. Toggle only their first literal signs according to $d\in\{0,1\}^k$. Every variant is an **original** signed proper strict 3-CNF UNSAT source: assign each fresh second literal TRUE. The number of distinct children is $q=2^k=H^{3/5+o(1)}$.

Exact packet: 8-bit marker 10110110, unary $1^H0$, $4H+k$ ordered ternary clauses, each literal encoded as $w$ unsigned positive-ID bits plus one sign bit ($w=\lceil\log_2(m+3k+1)\rceil$), final 01. Thus

$$
M(H)=8+(H+1)+3(4H+k)(w+1)+2=\Theta(H\log H).
$$

An authenticating recognizer checks all four positional clause facets per vertex against the same **ordered** edge-ID triple and the exact four parity-forbidden polarity patterns, each edge ID occurring exactly twice, the fresh tag variables and required non-tag signs, and exact packet length via indexed terminal and immediate blank probes. It deliberately does **not** read the variable first-sign positions of the tags. A whole-source sequential read on the recognized path would invalidate the claim. This is a typed source-recognition algorithm, not a source magic oracle. On success, the odd XOR certificate establishes UNSAT; other inputs are handled by any supplied correct total general-CNF decider $A$ after cleanup. This wrapper $B_{skip}^A$ is all-input correct (SAT, UNSAT, malformed). $B_{scan}^A$ first reads all $k$ computed tag signs, discards them, then runs $B_{skip}^A$ from fresh machine state. It is extensionally equivalent to $B_{skip}^A$.

On the authenticated family $B_{skip}^A$ has one raw input-read transcript and coefficient rank **zero**; $B_{scan}^A$ has $k$ standard-basis read rows, rank **$k$**, and $2^k$ distinct raw transcripts, although every output is UNSAT. If SAT were in P, both wrappers around an arbitrary hypothetical polynomial SAT decider would be total polynomial-time SAT deciders. This is a **conditional** same-language presentation result, not an unconditional SAT-in-P claim or a no-go theorem for code-aware compilers. The ideal minimum may simply omit the gratuitous scan.

Fresh-variable restriction proves the minimum **ordinary Resolution** inference count of the padded source equals that of its hard core: restrict each tag clause to TRUE to reduce any padded refutation to a core refutation, while a core refutation also refutes the padded source. This prior /510 fact is not a transfer to GF(2), ER, arbitrary computation or historical R_mix341.

## Independent finite controls

Hosted Python verifier: 20 different actual signed strict-three sources across K4, triangular prism, cube and Petersen, exact encoded lengths 285/407/631/795 bits, 4/4/4/8 descriptors; 127 checks, 11 malformed/hostile rejection controls, four SAT charge-switch controls, and sixteen legal tag changes, PASS. Node independently parses all 20 packets, checks 93 assertions and four corruption/allowance controls, PASS. Both agree on K4 baseline SHA-256 91c193d63d00665d1d541ac0b146fe7ac82431a1410b7d3d7ff16e2cb232cd9c. A separately executed standalone V8/Node K4 reproducer verifies 4 physical UNSAT sources, one sign-blind versus four scanned transcripts, SAT witness 30 for the order-swapped malformed core, and charge-switch SAT control. Finite Petersen is not an asymptotic expander certificate.

## Fully charged resource and limitations ledger

Typed recognized-source phase: unary header $O(H)$ reads; exact source, clause and positional authentication via indexed probes; $O(Hm)$ source rereads for edge-incidence count, each costing $O(\log M)$ index construction/erasure; terminal/blank probes; $O(\log M)$ local counters, head positions and index width. Worst-case modeled upper bound $O(M^2\operatorname{polylog}M)$ time, $O(\log M)$ supplemental workspace. The scan wrapper adds $k=O(\log M)$ reads, $O(\log^2M)$ indexing time after header and $O(\log M)$ additional bits. All nonrecognized and malformed sources invoke a fully charged general decider $A$ after cleaning local tapes. Simultaneous peak is bounded symbolically by $O(S_A(M)+\log M)$, including local high-water, assuming correct finite-tape composition; **no native FLMV instruction-level proof or execution** was completed. Materializing all q children costs $\Omega(qM)$ output operations. Caching, lookups, rank acquisition, failed policies, replay, reference storage, output, recomputation, all-phase peak and guest verification are not free. Distinct traces are not minimum logical proof-DAG work, nor general computational hardness.

**Actual advance:** A sound restricted paired-decider transcript-rank non-invariance result and an explicit SAT counterexample to unordered-facet source certification, corrected and verified independently. **OPEN:** [P2-A2] universal contracted SAT decider; [P2-A4] complete native resource accounting; [P2-A5] recursive same-machine applicability; Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2]. P versus NP OPEN.

## Primary references

[1] Fortnow, Lipton, van Melkebeek, Viglas (2005), JACM 52(6), 835-865, DOI 10.1145/1101821.1101822, section 2.1: https://lance.fortnow.com/papers/files/tst.pdf.
[2] Urquhart (1987), *Hard Examples for Resolution*, JACM 34(1), 209-219, DOI 10.1145/7531.8928.
[3] Bryant (1986), *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Transactions on Computers, 35(8), 677-691, DOI 10.1109/TC.1986.1676819.
[4] Published prior project findings LSPV-4/507, /510R, /513, and LSPV-2/515.
