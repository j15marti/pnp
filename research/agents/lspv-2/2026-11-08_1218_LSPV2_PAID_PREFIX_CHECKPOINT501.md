# LSPV-2/501: Paid checkpoint continuations across distinct child SAT inputs

**2026-11-08 12:18 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL, resource transfer CONDITIONAL | P versus NP OPEN.**

**Exact tracker IDs:** [P2-A2], [P2-A4], [P2-A5]; companion [P1-01], [P1-03], [P1-04]; Route B controls [P2-D1], [P2-C3], [P2-B1], [P2-B2]. All load-bearing obligations remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both complete root files were authenticated and read. The earlier proof1 blob was 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2's latest independent current-head read was 7d320b1158697c2a54a5fe1ac5d84280bfc95590. Neither root was edited.

## IDEA, falsifiers and prior work

Hypothesis: Rather than recycling only a *final* classification as in LSPV-2/500, retain an internally trusted **intermediate machine state** after an authenticated input-read prefix. It can be resumed on a different child even when the complete execution scans all bits and thus defeats the exact-answer cache (LSPV-4/500).

Precise falsifiers: (F1) same input length and agreement on every earlier observed input bit but different machine state at the checkpoint; (F2) a cached prefix incorrectly reuses a final UNSAT answer for a SAT suffix or an unencoded branch context; (F3) the state-copy/read-match overhead exceeds fully charged FLMV time and space, particularly with indexed high-water exceeding runtime; (F4) K4 odd-charge original signed 3-CNF fails source UNSAT, individual-clause necessity or malformed controls.

## SEARCH, exact sources and prior art

Read both full trackers, current GitHub issue #3 and recent comments, AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f), the governing 2026-11-02 five-role handoff (c3889a3e514ddbd747150dcb68607013a3b2d154), LSPV-2/500 (a8238aa7e3629f85f6155de01d0bfc6662ded27b) and peer LSPV-4/500 at research/agents/lspv-4/2026-11-08_LSPV4_FULLSCAN_TRACE_ANTICHAIN500.md (98397dc8dc3277b8440be9467b511c6082ec53e8). Actual GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f176e996e9542f0386b7aa7fe2ce89e70) and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727d3e2b009cba7afec2a93beb62959dd67) were inspected.

Required repository source reads, exact paths/blob IDs: konard/p-vs-np README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); MassimoLauria/cnfgen cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); berkeley-abc/abc README.md (88a9d1a316dd9751acade746de315fd1e6e6c362); pysathq/pysat README.rst (fefde10b1426a92a21425029892f3f49466bf03c); lsils/mockturtle README.md (c1d2b0c4728d923dc7f4ac2b6759994dbaba4c1b); openai/math CONTENTS.md (7e1ed90ac5a666f1bbecb22027387c4ad79e9d03). None proves the unrestricted transfer.

Primary published sources: Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822, **machine model §2.1, page 4** (actual PDF and page screenshot inspected); Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987, DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48(2), 2001, DOI 10.1145/375827.375835. State-migration prior art: Biere et al., *Migrating Solver State*, SAT 2022, https://www.amazon.science/publications/migrating-solver-state; STP incremental solving https://stp.github.io/stp/incremental-solving.html. A web search was performed; an independent Google-branded interface was not used. No assertion of novelty or an official checker run is made.

**Hard-family ledger.** Source: connected cubic expanding odd-charge Tseitin formulas. Four original proper signed 3-clauses per vertex, 3H/2 edge variables, 4H clauses and Θ(H log H) binary bits in a fixed-width ID encoding. Odd parity gives certified UNSAT. Exponential *ordinary DAG Resolution* proof size on expanding families is established by the cited literature, not in full R_mix341 or for arbitrary algorithms. Known legal shortcuts include GF(2) elimination, shared learned lemmas, extension variables and incremental proof-state reuse. Any lower-bound transfer must prove its direction for the exact 3-CNF and calculus; mere equisatisfiability is not enough. The test here uses the original signed K4 16-clause finite instance, not a claim of expanding-family hardness.

## ITERATE: theorem 501.1, authenticated intermediate-state sharing (PROVED/RESTRICTED)

Fix a total deterministic three-label binary-input machine A. After an actually executed and authenticated prefix of τ transitions on x, retain its full machine configuration Cτ (including work tapes, index heads, program counter, and state) and all (address,bit) observations Rτ of the original input up to that point. If another complete child y has the same length and agrees with every observed input bit, then the genuine run A(y) reaches **exactly the same configuration** Cτ after τ transitions. It may therefore resume from this state and continue using y to obtain its own SAT, UNSAT or MALFORMED answer.

**Proof:** Induction over the τ deterministic machine transitions. Given identical initial configuration and every input observation actually required before τ, each successor configuration matches. After τ the future inputs may differ, so the guest must still execute its suffix. The checkpoint is not an UNSAT lemma or a completed answer; unencoded branch assumptions cannot be reused. Forged external checkpoint packets are not trusted without paid validation.

This extends LSPV-2/500 completed-label reuse and is compatible with LSPV-4/500's distinct-input full-scan antichain: sharing *prefix computation* does not imply any completed-label cache hit or worst-case reduction in the number of guest suffix executions.

## Theorem 501.2, explicit conditional resource ledger (CONDITIONAL)

Assume an already-proved all-input source transformer emits q ≤ N^(3/5+o(1)) sequential children of length L ≤ N^(1/2+o(1)), paying N^(11/10+o(1)) local time and N^(1/2+o(1)) simultaneous space including source authentication, virtual child bits, join, failed policies and output. Assume fixed guest A has worst-case time L^(t+o(1)), space L^(s+o(1)), and an *effective native* FLMV same-model sparse accessed-cell simulation whose state can be serialized/restored in O(T_A(L) polylog L) time and O(min(S_A(L),T_A(L)) polylog L) bits. Keep h=polylog N authenticated checkpoints including ≤L input observations each. Then the actual charged stage is bounded by

$$
T_{\mathrm{stage}}(N) \le N^{\max\{11/10,\;3/5+t/2\}+o(1)},\qquad
S_{\mathrm{stage}}(N) \le N^{\max\{1/2,\;s/2\}+o(1)}.
$$

Indeed comparison and lookup are O(qhL polylog N), snapshot copies and actual continued/completed guest work at most O(qT_A(L) polylog N), and retained evidence plus machine states use O(h(L log L + min(S_A,T_A) polylog L)) bits. The full guest may still execute q times. The *assumed* source transformer, exact native simulator and recursive closure are NOT constructed. FLMV §2.1 explicitly warns indexed tape high-water may be **exponentially larger** than running time: naive copying of all high-water cells is invalid, and s≤t cannot be assumed. Sparse accessed-cell normalization is necessary and must itself be paid and tested on the target native machine.

## Exact computational controls and resource measurements (COMPUTATIONAL)

Generate 128 pairwise-distinct strict original signed K4 3-CNF sources, alternating odd-charge core C0/C1, followed by 24 legal fresh-variable ternary clauses. Header 26 bits, 40 clauses ×15 bits, child length L=626. A 266-bit header/core prefix is checked and then a deliberately nonoptimal *pairwise original-clause audit* performs 3,600 additional input probes before a checkpoint. The guest then reads the remaining 360 source bits. Each full guest reads **every** address, making completed-label footprint cache hits zero among distinct children.

| Portfolio | Fresh prefixes | Resumed prefixes | Guest bit probes | Paid comparisons | Charged state-copy bits | Total charged units | Peak cache bits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| No checkpoint | 128 | 0 | 540,928 | 0 | 0 | 540,928 | 0 |
| One checkpoint | 128 | 0 | 540,928 | 4,699 | 0 | 545,627 | 346 |
| Two checkpoints | 2 | **126** | 53,812 | 35,884 | 8,064 | **97,760** | 692 |

Python reference passed 589 assertion groups, independently written Node.js passed 483, and their exact ledgers and first/last source SHA-256 hashes agree. Each odd-charge K4 was exhaustively certified UNSAT on all 64 edge assignments, and *every one* of its 16 clauses was checked essential by deletion; even-charge SAT, opposite SAT/UNSAT suffixes with same prefix, one deleted original clause restoring SAT, and five malformed encodings were tested. The two-checkpoint wrapper reuses computation but never reuses a final answer and still finishes all 128 guests. The deliberately costly source audit makes this an illustration of paid savings, not a proof of optimal SAT computation or any asymptotic lower bound. The full Python and independent JS reference implementations and raw files are in the conversation reproducibility archive; the published compact JS is a *separate* finite replay of the main 128-child charged ledger.

**Publication:** role-owned mathematical report, compact independent JS verifier, cross-language raw ledger and five-role handoff. Root main.tex unchanged. Historical R_mix341 native rules and weights, all five agent schedules, titles, enabled states and two-Route-A/three-Route-B allocation untouched.

**Precisely OPEN:** [P2-A2], [P2-A4], [P2-A5] solver-dependent exponent-oblivious, all-input, malformed-aware, recursively iterable same-machine A→Φ(A) with fully charged resources; [P2-D1], [P2-C3], [P2-B1], [P2-B2] historical mixed-calculus authentication, universal bound and noncircular B3. **P versus NP remains OPEN.**
