# LSPV-4/462 | Direct FLMV index-tape reset firewall
**2026-11-07 00:36 PST | Route A LSPV-4 | PROVED/RESTRICTED native-direct-reset lemma; COMPUTATIONAL finite checks; P vs NP OPEN.**

## IDEA -> SEARCH -> ITERATE
**Hypothesis:** The prior LSPV-4/461 touched-work-cell reset ledger omitted clearing *guest index-tape contents*, which can be large even if just one non-index work cell is touched. **Falsifiers:** F1 the original FLMV machine can clear a nonblank index tape with a native operation that does not jump the associated work head; F2 work index-tape contents are themselves charged as high-water workspace; F3 an L-bit all-ones index can be safely erased by one bounded-space jump after o(L) single-cell edits; F4 the prior text had already paid separately for every index bit and head position. The primary original-model specification rules out F1/F2, the proof below rules out F3 for *direct physical tape restoration*, and F4 requires restricting the earlier M-cell-only claim to DATA/MARK, not a complete guest reset.

## Authenticated source and review ledger
Read both complete root proof chains: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt blob d03cf5888745b70b8aa2a9b7b9ce4a429c6f0c7a. Relevant node IDs: [P1-01], [P1-03], [P1-04], [P1-S3], [P2-A1], [P2-A2], [P2-A3], [P2-A4], [P2-A5], [P2-D1]. Also read issue #3 (latest review), AGENTS.md 19656af1, CODEX.md 754999f5, research skill b8df83a7, historical five-role refocus c3889a3e, LSPV-4/461 0f6f4f6a, LSPV-2/462 97db73d4 and /463 44410f13, coordination handoff 59633cf2, actual Grok GROKPROOF/2026-11-07_0819_PROGRESS.md c52f2f67 and Claude world-ledger README de75a371.

**Primary model:** Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, Sec. 2.1, author PDF https://lance.fortnow.com/papers/files/tst.pdf page 4, actual page image inspected. A non-index work tape W has an associated index tape I. An indexed W-head move to the binary address encoded in I takes a step and **erases I**. Work space charges the largest accessed/indexed non-index work position, not the number of touched work cells or the length of uncharged index-tape contents. The authors' general sparse-storage observation does not implement this project's specific guest reset.

**External checks:** konard/p-vs-np README 0e0ec77f and proofs/complexity/README 7ee9a11e concern a different finite one-tape model; blkph0x/p-vs-np-proof-research README f397a774 and METHOD_INDEX 18d693ea distinguish bounded/promise methods; meelgroup/frat-xor format.md 986a21aa is a foreign mixed proof format; cslib-community/complexitylib README b563d562 and openai/math README cc5b0a03 do not provide a native FLMV interpreter. Targeted public web searches addressed FLMV work/index access and Tseitin proof complexity; a separate Google-branded service was not available. These sources were actually retrieved, but no native FLMV interpreter or historical R_mix341 checker was run.

## Theorem 462.A (PROVED/RESTRICTED): direct raw index reset dichotomy
Consider one FLMV work tape W with its original physical index tape I. A legal guest trace writes 1 to each of L consecutive index cells 0,...,L-1 without an indexed W-head move; it touches at most one W cell. Time is O(L), guest touched-work count M=1 and guest measured work high-water S=O(1). The binary value of I is 2^L-1.

A reset of **that same raw index tape** to the all-blank initial configuration must either (i) overwrite L nonblank index cells using at least L one-cell writes if no erasing indexed move occurs, or (ii) perform an erasing indexed W-head move. For the latter let the allowable physical high-water budget be L^k, with fixed k. Before the *first* such jump, every still-set index bit j exceeding floor(k log2 L) must already be cleared, otherwise the indexed work-head jump exceeds L^k. Thus the number of distinct separately edited index cells before an allowable erasing jump is at least

$$
R_{\mathrm{index}}\ge\max(0,L-\lfloor k\log_2L\rfloor-1)=\Omega(L).
$$

In contrast, an immediate erasing indexed jump without these edits uses work-space at least 2^L-1. This precisely defeats a proposed **complete direct tape reset** bound O(M polylog L), since M=1; it does NOT defeat all virtual-tag schemes, tape remapping or alternative representations. No new SAT or arbitrary-machine lower bound is asserted.

## Corrected full-phase resource ledger
With T_j guest steps, M_j distinct touched work cells, S_j maximum work high-water, and L_j index-tape writes in guest invocation j, the raw DATA/MARK dirty-address log still needs exactly M_j clears of each of DATA and MARK, conditional on a paid address-recovery mechanism. But index tapes, index heads, other guest tapes, parsing, source reads, child headers, failed policy searches, output, caches, retained ancestors and all simultaneous buffers **also require accounting**. On the direct physical-index implementation an explicit conservative guest-plus-reset estimate is

$$
T_{\mathrm{guest+reset},j}=O(T_j\operatorname{polylog}N+M_j\operatorname{polylog}N+L_j).
$$

Because L_j<=O(T_j), this may still be O(T_j polylog N), under the other **unproved** native work-address and same-machine assumptions. It is false that the **entire reset phase** always costs O(M_j polylog N). The space ledger charges any temporary indexed jump to the actually reached work position, even if the index contents are subsequently erased. One cannot use a jump to 2^L-1 as a free reset. q calls must sum every such cost. This is a correction to the scope of /461, not a contradiction of its DATA/MARK-only clearing count or of the conditional final exponents.

## Established hard-family control
Odd-charge cubic edge-expander Tseitin proper 3-CNF: choose a fixed connected cubic edge-expander G_H with H vertices, edge variables x_e (3H/2 edges), and charges chi_v with XOR_v chi_v=1. At vertex v with e_1,e_2,e_3, include the four ternary clauses

$$
C_{v,a}=\bigvee_{i=1}^{3} \begin{cases}x_{e_i}&a_i=0\\ \neg x_{e_i}&a_i=1\end{cases},\quad a_1\oplus a_2\oplus a_3\ne\chi_v.
$$

There are 4H original proper clauses, Theta(H log H) encoded bits with dense IDs. Charge-sum GF(2) proves UNSAT efficiently. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) give 2^Omega(H) ordinary shared-DAG Resolution lower bounds for suitable expanding families, NOT arbitrary deterministic machines or full historical R_mix341. No 3-CNF lower-bound-preserving reduction is needed for this already ternary family. Small K4 signed even/odd charges are **finite semantic controls**, not a certified asymptotic hardness sequence.

## Finite independent verification and status
Published experiments/arc/lspv4_462_index_reset_falsifier.cjs at Git blob 890b14b7715810033e4aec5a6cd878c1cc9abd63 and results/raw/arc/2026-11-07_0036_LSPV4_462_INDEX_RESET.json at 74b7ccba06c7cfc7112f34fd8c29bf9ca70a0ca6. The EXACT retrieved published checker was reexecuted and its result compared field for field with published JSON: **72 assertions PASS**, 8 budgets L=12,...,64, 4 original signed strict-3CNF K4 SAT/UNSAT controls and 4 malformed controls. For L=64, instant index erasure jumps to 2^64-1 work position; with cubic budget L^3=262144 at least 45 high-bit edits are mandatory before an erasing jump. A separately implemented Python producer checked the related formula and K4 controls. Host execution is not native FLMV machine measurement.

Tracker status: [P2-A4] gains a restricted direct-index reset falsifier; [P1-04] reviewed without closing it. [P2-A2],[P2-A5],[P2-D1],[P2-B1],[P2-B2] OPEN. No change in R_mix341 weights, grammar, tasks, titles, roles or schedules. P versus NP OPEN.

**Advance:** explicit previously unpaid index-tape reset cost for a direct native dirty-address implementation. **Verification:** symbolic direct-tape argument and finite exact published checker; native instruction-level interpreter still OPEN. **Remaining gap:** a uniformly effective fully charged work-address, all-index-tape, fresh guest interpreter and an all-input recursively iterable SAT contraction for every polynomial SAT decider.
