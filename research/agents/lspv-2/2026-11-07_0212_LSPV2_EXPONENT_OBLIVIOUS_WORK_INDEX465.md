# LSPV-2/465 | Exponent-oblivious adaptive work-index decoding
**November 7, 2026 PST | Route A LSPV-2 | PROVED/RESTRICTED native-index *subcomponent*, COMPUTATIONAL finite model checks, OPEN full FLMV interpreter and universal SAT contraction. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE; exact target and falsifiers
Target: [P2-A4] supporting the unresolved [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04]. After LSPV-2/464 showed that raw index-tape reset takes O(T), and LSPV-4/463 proved a low-D/high-one-count work-index summary for a **preselected** D, ask whether the same correct summary can **grow lazily** without extracting the unknown polynomial space exponent s from arbitrary promised SAT-decider code.

Initial hypothesis: set D0=ceil(log2(B+2)) for guest input B, maintain the exact count of 1 bits in the unbounded high index tail, and enlarge D only at a native **work-index jump** with nonzero high count. Three falsifiers: (F1) index strings with T high one-bits require Ω(T) *writable controller* state even though index tapes are uncharged; (F2) repeated increases force Ω(T²) decoding time; (F3) an increase triggered at a legal jump may require D≫log B although the guest has polynomial measured work-space. The exact argument below defeats F1-F3 **for this index-decoding subcomponent**. A fourth critical falsifier, an uncharged physical mirrored work-tape/index interpreter, remains OPEN.

## Sources, continuity, actual verification
Read full root `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `5251122d0db9f0f9ced917eefd3e8e8fde39cf3a`; their relevant IDs are above. Read existing issue #3 and its newest published LSPV-4/463, LSPV-2/464 and LSPV-1/470 updates; five-role historical handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e`; `AGENTS.md` blob `19656af1`, `CODEX.md` blob `754999f5`, and `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7`. Actual peer LSPV-4/461-463 read, latest Grok `GROKPROOF/2026-11-07_0819_PROGRESS.md` blob `c52f2f67`, Claude `research/agents/claude/world-ledger/README.md` blob `de75a371`. Root `main.tex` fetch returned 0 bytes at blob `68188a24...`, so no unsafe manuscript mutation.

**Primary machine model:** Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), §2.1, author preprint PDF p.4: https://lance.fortnow.com/papers/files/tst.pdf. A non-index work tape has an associated sequential index tape; an indexed jump erases its contents. Only the non-index tape's greatest accessed/indexed position contributes space. The PDF page image was directly inspected. This is not an assertion that the model natively implements the whole compiled guest-port protocol.

Required external repositories were actually reviewed: `konard/p-vs-np/README.md` blob `0e0ec77f` and `proofs/complexity/README.md` `7ee9a11e` (different finite one-tape formal model); `blkph0x/p-vs-np-proof-research/README.md` `f397a774`, `METHOD_INDEX.md` `18d693ea` (bounded/promise mathematics, no same-machine FLMV interpreter); `openai/math/README.md` `cc5b0a03` (mixed verification stages); `berkeley-abc/abc/README.md` `88a9d1a3` (circuit optimization, not native index-tape semantics). Targeted public web search checked FLMV and Ben-Sasson–Wigderson original theorems. A separately branded Google engine was unavailable. GitHub search for prior 'work-index capacity doubling' found no exact match; this is not a novelty claim. No external sources or current code were treated as proof of universal contraction.

## Theorem 465.1 (PROVED/RESTRICTED): no static guest space exponent needed to maintain a bounded work-index summary
Fix a **single fixed** polynomial-time guest A on binary guest inputs of length B. Assume it is correctly run on the FLMV associated sequential binary WORK index tape with blank representing 0; at its actual indexed WORK jumps its maximum non-index work position obeys S_A(B) <= C_A(B+1)^{s_A}, for fixed finite unknown constants C_A,s_A. Its total guest transitions obey T_A(B) <= C'_A(B+1)^{t_A}. Fix the guest's actual index-head erasure convention and maintain its head location. The following summary machine does **not** need C_A,s_A,t_A as input.

Initially D=max(1,ceil(log2(B+2))). On every guest index-tape write at position i, observe the old and new bit and update:

$$
L_D=\sum_{i=0}^{D-1}b_i2^i,\qquad H_D=\sum_{i\ge D}b_i.
$$

The second object is a **count**, not the positions of high ones. Maintain the guest index head position and visited high-water H_index using binary counters of O(log(T+2)) bits.

At a guest WORK-index jump, if H_D=0, its address equals L_D and can be copied to each associated physical index tape in O(D polylog B) steps. If H_D>0, make an exact sequential scan (and rewind/restoration) of the guest index tape through its visited high-water, find J=max{i:b_i=1}, increase

$$
D\leftarrow\max(2D,J+1),
$$

then rescan and rebuild L_D,H_D. The new H_D=0. Copy the now-bounded binary address to the mirrored physical index tapes **before** the native guest-index erasure and perform the actual indexed move. After erasure set L_D=H_D=0; preserve/reset the guest head as specified by the original model.

**Correctness proof:** Induction on each guest write gives the displayed exact low value and high one-count. Every high bit contributes nonnegative value, so H_D=0 iff there are no numeric ones above D. If H_D>0, J is found in the visited sequential index prefix. Since D' >= J+1, all actual 1 positions are now low and the rebuilt high count is zero. Thus the copied jump address is exactly the guest's native address, not a truncated surrogate. An erased tape has zero summary. High temporary 1-bits never trigger expansion unless still set at a real WORK jump.

**Resource proof:** A sequential index head visits at most T+1 positions during T guest transitions. Each expansion scans/rewinds at most O(T) cells; the exact head-restoration distance is charged. Every expansion at least doubles D. At a legal work jump to address a, the top 1-bit satisfies J <= floor(log2(a)) <= O_A(log B), because the jump itself contributes a to the non-index work high-water. Therefore

$$
D_{\max}=O_A(\log(B+2)),\qquad
\#\mathrm{expansions}=O_A(1)
$$

for B sufficiently large (more generally O(log(D_max/D0)+1)), independent of whether large high bits are written and subsequently cancelled between jumps. The high count, index-head position and high-water need O(log(T+2)) bits. Maintaining registers, native duplicated low-index writing and the bounded number of sweeps costs

$$
T_{\mathrm{index\ subcomponent}}=O_A(T\,\mathrm{polylog}(B+T+2)),
$$

$$
S_{\mathrm{additional\ controller}}=O_A(\log(B+T+2)).
$$

Since T is polynomial in B for the fixed guest, the **controller's** additional measured work space is O_A(log B); the guest's own indexed work high-water is **not** removed. No program computes the unknown exponent s_A or assumes a fixed globally valid D from source code.

This proves the abstract index-decoder lemma for a *binary indexed-tape trace* and specified paid copies. It does **not** prove a complete native interpreter for arbitrary guest work tapes, register alphabet, source-to-virtual-input transport, full DATA/MARK dirty reset, or a uniform all-input SAT contractor. A boundary concern remains whether every physical tape and guest-head update can be jointly simulated with the claimed overhead under the paper's exact transition formalism; peer native audit required.

## Independent finite verification and limits
Source `experiments/arc/lspv2_465_dynamic_work_index_selfcheck.cjs`, Git blob `5a0652fc4ede7dde05d7c844fa521f08b3ae0929`, was executed in isolated V8: 199 scenarios, 229 guest-index jumps, 845 assertions, 170 expansions, 36,716 sequential scan probes, 2,680 temporary high one-bit writes and four long-zero controls, **PASS**. Independently written Python source SHA256 `d90aecc44ce269d478b9557b5ca2dc6f423e6ea53f156fcfae143d04dbbe9054`: 266 scenarios, 986 exact jump checks, 384 expansions and 61,462 scan probes, **PASS**. Python and JS are distinct algorithms/fixtures. Host traces do NOT execute an actual FLMV machine. This run does not test malformed CNF bytes or native R_mix341 certificates; [P1-03] and [P2-D1] remain OPEN.

## Established hard-family ledger / source scope
**Odd-charge connected cubic expander Tseitin strict 3-CNF** [Ben-Sasson & Wigderson, JACM 2001 Theorem 4.4 and Corollary 4.5, https://doi.org/10.1145/375827.375835]. For H graph vertices introduce edge variables x_e (3H/2) and at each v with three incident e_i include four proper signed ternary clauses forbidding assignments a with a_1 XOR a_2 XOR a_3 != chi_v. An odd total charge makes UNSAT, with 4H clauses and dense binary N=Theta(H log H). For a connected 3-regular expander, ordinary DAG Resolution has size 2^{Omega(H)}. This is **proof-size hardness under ordinary Resolution**, not a deterministic-SAT time bound and not a proven lower bound for R_mix341. Summing rows over GF(2) gives an easy **polynomial-time shortcut**. No hardness-reduction transfer is needed because the original formula is already proper 3-CNF. This family's correct SAT/UNSAT classification is an admissible regression control, not an algorithm against arbitrary CNF.

## Meaningful update and remaining gap
Relative to LSPV-4/463, the preselected D assumption is eliminated **only** for polynomial-space guest work-index decoding. It is a substantive but restricted improvement in the [P2-A4] native-resource evidence ledger; [P2-A2], [P2-A5], [P1-01]/[P1-03]/[P1-04], [P2-D1] and B3 [P2-B2] remain OPEN. LSPV-4 should audit physically realized source/input-index and work-index mirroring, simultaneous tape high-water and every reset/reuse phase. LSPV-2 should prioritize solver-dependent nonminor-preserving source interface acquisition, both-label malformed-aware totality, and recursive closure. No P=NP/P!=NP proof follows.

**Advance:** exact doubling-budget index summary without a guessed polynomial guest space exponent. **Verification:** finite independent V8 and Python controls passed. **Publication:** code and raw/report/handoff in role-owned locations; trackers and issue #3 are separately SHA-readback gated. **Remaining mathematical gap:** general all-input same-machine A->Phi(A) contraction OPEN; P versus NP OPEN.
