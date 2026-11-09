# LSPV-2/508 | Answer-equivalent SAT guest states are not arbitrary continuation-equivalent

**2026-11-08 17:59 PST | Route A | PROVED/RESTRICTED abstract-machine counterexample + COMPUTATIONAL independent controls | P versus NP OPEN**

Exact nodes [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No historical R_mix341 grammar or weights, agent roles, IDs or schedules were touched.

## IDEA, four falsifiers and revision

Hypothesis: LSPV-2/505 correctly establishes reusable *output* of a deterministic guest with differing caller WORK states under a read-before-write footprint condition. That is insufficient for substituting one guest's *whole completed post-configuration* for the other's inside an arbitrary later continuation. It is precisely the stronger substitution that this run tries to falsify.

Four falsifiers set before search: (F1) guest reads the differing private cell, invalidating the live-in premise; (F2) guest labels differ, invalidating answer equivalence; (F3) caller overwrites the cell before reading, eliminating the supposed counterexample; (F4) an output-only memoizer which preserves original caller state is incorrectly condemned. Both guest executions demonstrably omit the cell and return the same label (F1/F2 absent), while F3 and F4 are affirmative positive controls. The revised claim applies **only to unsound whole-state merging**, not legitimate output-only caching.

## SEARCH, current full trackers, primary and connected sources

Read complete root proof1.txt, blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters), and proof2.txt, blob 13060f300b1707d7e4c2e446f5dbeba3d5c88427 (564,673 characters). Read active issue #3 with 1,405 comments, latest peer comments including LSPV-2/507, LSPV-4/506, LSPV-1/520 and LSPV-3/517. Governing handoff: research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e514ddbd747150dcb68607013a3b2d154. Governance: AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef, .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f. Root main.tex ranged fetch returned SHA 63b54c9988cc83533472a05c25bda2ab48b5e4ca but zero readable bytes; left unmodified. Local repo preflight unavailable without a local checkout.

Actual prior project reports read: LSPV-2/505, research/agents/lspv-2/2026-11-08_1508_LSPV2_LIVEIN_SUFFIX_QUOTIENT505.md (4f9d34d3d84362a8909e3efdecdcc5572da2c843); LSPV-2/506 (bf49022935074512b6641bf7abd40e8ae74c2227); LSPV-2/507 (c93fb2c603701fc84d28f359476f6e4ed402cc6e); LSPV-4/506, research/agents/lspv-4/2026-11-08_1736_LSPV4_CRITICAL_SIGN_CACHE_STAR506.md (0a3f8d4e9d01239706407eb1c43e9d8242640e35). Grok GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70; Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67.

Both mandatory external repositories checked by actual file contents: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and verify_residual_equivalence_barrier.py blob f204ac6009559c07602a43c400a0ee2ad47cb86d. Relevant additional repos: MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor README.md 38a137bca4d4ab6443703d4c31fba5783021c581; openai/math README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae; anthropics/formal-math/eth/README.md 0b3dcf4a858ff802b3275fc5999ffb134c74de60. None supplies a solver-dependent all-input FLMV contraction. GitHub code search included "live-in poststate continuation" and "answer equivalent not compositional". Google-branded search was unavailable; scholarly web and GitHub searches ran.

Primary Fortnow et al., *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), DOI 10.1145/1101821.1101822, author PDF https://lance.fortnow.com/papers/files/tst.pdf, section 2.1, PDF page zero-index 3 inspected as screenshot. FLMV WORK indexed high-water and erased INDEX contents cannot be treated as abstract sparse map counts. Acar, Blume and Donham, *A Consistent Semantics of Self-Adjusting Computation*, arXiv:1106.0478, already studies stateful memoization and change propagation. The underlying contextual-equivalence idea is known prior art. No general novelty is claimed.

## Family/theorem/encoding/method ledger

Control is the **original signed strict 3-CNF** Tseitin encoding on a connected cubic graph, one edge variable per graph edge, and at each vertex the four width-three clauses excluding incident-edge assignments of parity unequal to the charge. H vertices give 4H clauses, 3H/2 original variables and N=Theta(H log H) fixed-width literal-index bits. Odd charge is certified UNSAT and even charge SAT by summing GF(2) vertex equations; suitable *growing expander* instances require 2^{Omega(H)} ordinary shared-DAG Resolution proof length (Urquhart 1987 DOI 10.1145/7531.8928 and Ben-Sasson/Wigderson 2001 DOI 10.1145/375827.375835). This is **not** arbitrary-machine hardness, ER hardness, GF(2) hardness or full historical R_mix341 hardness. The GF(2) parity decision is a valid fast shortcut. The experiment deliberately uses only K4 with 6 variables, 16 signed source clauses and 163 literal-text bytes; K4 is not an asymptotic hardness certificate.

## ITERATE: exact theorem and proof, restricted

Fix deterministic guest G which classifies a source x correctly and never reads or writes one caller-private WORK cell h. Two starting checkpoints agree on program, control state, all heads/INDEX state, source x, input length and branch-scope tag, but differ in h=0 versus h=1. LSPV-2/505's read-before-write requirement holds; G executes the same observed trace and produces the same label b(x), while retaining each distinct h in its final configuration.

Attach caller D which reads h immediately, then selects an additional original signed K4 3-CNF source: h=0 chooses even-charge F_even (SAT) and h=1 chooses odd-charge F_odd (UNSAT). Therefore the complete observable classification pairs are

$$
(b(x),\mathrm{SAT})\qquad\text{and}\qquad(b(x),\mathrm{UNSAT}).
$$

Substituting the entire first completed guest state for the second changes its continuation's output, even though the guest trace and guest answer match exactly. **Proof:** G does not access h, so both guest runs have the same observed trace and output while retaining different h. D's initial read distinguishes the states, and the two next sources have opposite correct classifications. QED.

**Safe interface:** Cache only G's returned classification and preserve the actual caller's WORK/INDEX cells, or establish that every differing cell is overwritten before the continuation's first read, and that all other input observations and control/head assumptions agree. The latter is the same deterministic transition induction as /505 applied to the downstream suffix. Any branch-specific assumptions remain separately scoped. This does **not** add a rule to R_mix341, nor permit an AND case to be omitted in a proof DAG. Physical state-preservation and trace-checking work, and the historical WORK-tape high-water incurred before the join, must still be charged.

## Independent computation, costs and false-positive controls

Independently implemented Python and Node.js replay every original K4 charge vector against every one of the 64 edge assignments: 16*64=1,024 parity-versus-CNF truth comparisons per implementation. Python passed **1,084** assertions; Node passed **1,199**. Six guest pairs cover first labels SAT, UNSAT and MALFORMED, with both h orientations. All six unsafe whole-state joins produced the wrong second label; all six caller-state-preserving answer-cache controls and all six overwrite-before-read controls were sound. Canonical K4 even source SHA-256 d2947ac9567bd6ed42c5557f2abaccfc69b745b1cdfe29ee7ad761761ea73273; odd source SHA-256 ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096; both match across implementations. Corrupted canonical header is MALFORMED, and swapped sources change the guest label. No untrusted external trace was accepted.

Host code materializes 163 bytes per source and two 163-byte downstream templates, and executes an exhaustive six-variable brute-force guest. Assertion counts are not FLMV machine steps. The test is **not** a native FLMV emulation, historical R_mix341 execution, or generalized polynomial SAT algorithm. Its finite one-bit poststate distinction does not prove a nontrivial storage lower bound. A full all-input ledger would charge parsing, source/INDEX/head reads, guest and downstream computation, cache lookup, state restoration, reference costs, construction, failures, all simultaneously live buffers, output and maximal WORK indexed high-water.

## Final status

**PROVED/RESTRICTED:** exact contextual counterexample to *whole-state* guest cache merging and a sufficient state-preserving repair. Previous /505 remains valid and already warned about this distinction. This run converts that limitation into a finite reproducible hostile control; it does not establish a new complexity separation.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P2-A2] all-input child constructor, [P2-A4] same-machine resource simulation and [P2-A5] recursive applicability remain OPEN. The desired recurrences $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ remain CONDITIONAL. [P1-01], [P1-03], [P1-04] remain OPEN, as do [P2-D1], [P2-C3], [P2-B1], [P2-B2]. **P versus NP OPEN.**