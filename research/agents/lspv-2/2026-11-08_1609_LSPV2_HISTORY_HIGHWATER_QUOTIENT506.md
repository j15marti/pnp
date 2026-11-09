# LSPV-2/506 | Output-trace equivalence does not preserve prior FLMV high-water

**2026-11-08 16:09 PST | Route A | PROVED/RESTRICTED abstract-machine counterexample and COMPUTATIONAL independent controls | P versus NP OPEN**

**Exact nodes:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN; cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** This is a resource-accounting qualification to LSPV-2/505's sound *answer* sharing, not a claim that /505 is logically incorrect.

## IDEA, assumptions and four falsifiers (fixed before search)

Hypothesis: a deterministic SAT guest's exact, trusted suffix may be reusable across two parent contexts with identical guest-entry configurations and identical source, while the parents' already-incurred FLMV WORK high-water costs differ polynomially. Therefore an output-equivalence/live-in-quotient key is not sufficient for transferring a whole-run physical resource estimate.

F1: the far jump uses a read-only INPUT head, which is space-exempt (repair: jump **non-index WORK**). F2: construction of an indexed address of $H$ already writes $H$ INDEX cells (false: it uses $O(\log H)$ cells). F3: after the private jump, WORK cells, index contents/head, or guest entry states differ (explicitly restore and compare). F4: an output-only shortcut is incorrectly generalized to a native FLMV simulation or a SAT lower bound (scope limited below).

## SEARCH: prior work and source authentication

Complete root trackers proof1.txt (Git blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 chars) and proof2.txt (preflight blob `9f9e3c77fdbb753e4d5ac4fd8a9ce0cf4b0cfd7e`, 543,170 chars) were read; issue #3, including last six role comments out of 1,396; governing coordination handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob `c3889a3e514ddbd747150dcb68607013a3b2d154`); AGENTS.md (`19656af102604d5f0a721d548cf2e4e72a063561`), CODEX.md (`754999f50de93cdb693ed37bc8110d31e9e698ef`), and .codex/skills/pnp-research/SKILL.md (`b8df83a7b0b1428f349b0e02ce1387d979e8db7f`). Relevant existing project analyses: LSPV-2/505 (`4f9d34d3d84362a8909e3efdecdcc5572da2c843`), LSPV-2/467 (`a02e7895620d286786688860e025f23c1886622d`), LSPV-4/502 (`acac437441905dad52761631d979e8ba18f8781e`), LSPV-4/504 (`4ec56c20b9b7024ec44b531435d0ddf8f6f076df`); Grok GROKPROOF/2026-11-08_1130_PROGRESS.md (`6942a99f176e996e9542f0386b7aa7fe2ce89e70`); Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (`1f9fc727d3e2b009cba7afec2a93beb62959dd67`). These reports already establish high-address spikes and their possible sparse implementation repairs; novelty of spikes, checkpointing or high-water accounting is **not** claimed.

Primary original FLMV §2.1, author PDF https://lance.fortnow.com/papers/files/tst.pdf, page 4 (zero-index PDF page 3), actually screenshot inspected. It says the non-index tape charges the largest position ever READ (indexed), whereas the INDEX tape is erased after jumping and can be only $O(\log H)$ long. The INPUT tape is excluded from work-space charge but this example does **not** use an INPUT spike. Source DOI 10.1145/1101821.1101822, JACM 52(6), 835-865 (2005). Established prior source controls: Urquhart, *Hard Examples for Resolution*, JACM 34(1) (1987), DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, *Short proofs are narrow*, JACM 48(2) (2001), DOI 10.1145/375827.375835. Prior work on dynamic-dependence computation: Acar et al., TOPLAS 32(1) (2009), DOI 10.1145/1596527.1596530.

External actual files read: konard/p-vs-np/README.md `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and DETAILED_SOLUTION_PLAN.md `19450e384269f1ccf890b924ae0b10ce8da212cd` (educational/finite-machine P-subset-NP, not FLMV); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md `18d693ea71dfa433370eb7afbebc3106e32f03e5` and test_symbolic_suffix_template.py `a2061b7b3f1122b8688a4f9b8bfa5d7d026a5aa1` (certificate macros, not guest memory cost); MassimoLauria/cnfgen/cnfgen/families/tseitin.py `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; meelgroup/frat-xor/README.md `38a137bca4d4ab6443703d4c31fba5783021c581` (external proof format); openai/math/CONTENTS.md `7e1ed90ac5a666f1bbecb22027387c4ad79e9d03` (unrelated general math collection). Targeted repository searches for work-history high-water and source-aware checkpoint sharing located /502 and /504 rather than a universal contraction. Google-branded search was unavailable; public web and GitHub search were actually used.

## ITERATE: theorem 506.1 (PROVED/RESTRICTED, exact charged-history counterexample)

Fix any deterministic total program $B$ for a three-label source interpretation; if a uniform polynomial-time SAT decider exists, instantiate $B$ with that correct all-binary SAT/UNSAT/MALFORMED decider. For fixed integer $k\ge1$, and input length $n$, let

$$
L(n)=k\lceil\log_2(n+2)\rceil,\qquad H(n)=2^{L(n)}=\Theta(n^k).
$$

Two **parent-side**, typed contexts run on the same immutable input $x$, with the same guest $B$ and clean private tapes. Both determine $n$ in charged $O(n)$ time. Context $C_0$ calls $B$ directly. Context $C_1$ writes the $L(n)+1$ bits of $H(n)$ on its private associated WORK INDEX tape, jumps the private non-index WORK head to address $H(n)$, READS the blank cell, loads zero on INDEX, jumps back to WORK position zero, and restores every guest-visible register/head/tape before invoking $B$. These are *two legal outer contexts*, not two different input encodings or two alleged native executions on a single fixed source-only SAT decider.

The resulting **guest-entry** configurations and all subsequent $B$ transitions and labels are identical. Yet $C_1$ has already incurred private non-index WORK high-water at least $H(n)$, whereas $C_0$ incurs no corresponding spike. The added prefix has only $O(n+k\log(n+2))$ time and $O(k\log(n+2))$ INDEX high-water, with non-index WORK spike $H(n)$; the overall charged peak obeys

$$
S_{C_1(B)}(x)\ge H(n),\quad
S_{C_0(B)}(x)=O(S_B(x)+\log(n+2)),\quad
T_{C_1(B)}(x)=T_B(x)+O(n+k\log(n+2)).
$$

The last two expressions assume the simple context/length counter and no additional guest copying; the contexts may take a larger constant overhead in an exact instruction table. In particular, **same trusted guest suffix** does not imply same *already-consumed* resource profile. A cache key adequate for correctness cannot be used as a certificate of equal full-run FLMV space unless it separately carries and joins the ancestral high-water ledger. With sequential branches, the physical peak is the maximum over all actually visited host states, not the space cost of only the reused suffix. This observation does not prohibit a different compiled program that erases or sparsely simulates the spike: FLMV §2.1 and LSPV-4/502 explicitly allow paid representation repairs.

Proof: indexed WORK read at $H(n)$ makes the maximum position ever read at least $H(n)$; the INDEX contents are erased by the indexed moves. A private read of an untouched zero cell causes no permanent work-content difference. Returning the WORK head, clearing INDEX, and restoring guest control/tapes makes the $B$ start states identical. Determinism gives identical entire suffix and output. The space measure is historical, so the already incurred maximum remains different. QED.

## Established 3-CNF family/theorem/shortcut ledger

For connected cubic $G_H$ with $H$ vertices and edge variables $x_e$, use the original four signed width-three clauses at each vertex that exclude the four assignments violating its GF(2) charge $\chi_v$. This yields $3H/2$ variables, $4H$ original proper ternary clauses and $\Theta(H\log H)$ ordinary binary literal-ID size. Odd $\bigoplus_v\chi_v$ certifies UNSAT. Suitable cubic expander families have exponential **ordinary DAG Resolution** refutation-size lower bounds per Urquhart and Ben-Sasson/Wigderson, not against arbitrary algorithms or mixed R_mix341. GF(2) elimination is the required polynomial-time upper control. This run uses only the $H=4$ K4 finite fixture, **not** an asymptotically proof-hard instance.

## FINITE controls and measured ledgers (COMPUTATIONAL, not native machine execution)

Two independent implementations, Python and Node.js, independently reconstruct all 16 original signed K4 sources, with source-zero SHA-256 `9fa4c20d987e11a768d3a3c28960c154f451399975f491fdb36a997c2ae2e1a4`, and separately brute-force all 64 assignments for source labels. Eight are SAT and eight UNSAT; six malformed byte controls are rejected by the restricted exact-source grammar. For $k\in\{1,2,3,4\}$ there are **88 paired control runs**. Python **1,012 assertions** and independently written JavaScript **925 assertions** passed, with 67 high-water cases exceeding $n^2$, an observed largest symbolic WORK address $2^{32}=4,294,967,296$ and maximal INDEX representation 33 bits. At every paired guest entry, registers, tape contents and head positions matched, and so did SAT/UNSAT/MALFORMED classifications. The tests simulate index operations symbolically and **do not allocate 2^{32} cells**: that large number is the native high-water tariff *if the specified indexed WORK read were executed on FLMV*, not a measured host-language RSS usage or executed native FLMV machine. Guest brute-force classification is a finite fixture, not a polynomial all-input SAT decider.

Separate charges: original source parsing/brute-force validation and local loop testing are fully executed as host-language experiments but no asymptotic native parser theorem follows; symbolic INDEX construction/write and erasure are modeled, physical FLMV instruction-level timing is not measured; one source SHA/digest is a cross-implementation byte-equality control, not an UNSAT proof; preamble peak, guest peak, construction, output and publication reads count in their respective accounting channels. All complete source artifacts and raw results are under experiments/arc and results/raw/arc. No historical R_mix341 grammar or weight is touched.

## Status and next unresolved implication

**Actual advance:** explicit *historical high-water non-congruence* of the exact live-in/trace equivalence used for answer reuse, with falsifiers F1–F4 passed in a restricted abstract indexed-WORK experiment. The finding strengthens the resource-audit qualification of LSPV-2/505 but does not materially change [P2-A2], [P2-A4] or [P2-A5]; their requirements already separately charge all-phase high-water. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** A peer may advance proof2 concurrently, so the stated preflight SHA is not a permanent head assertion.

**Remaining gap:** effective, solver-dependent, exponent-oblivious, recursively iterable, **all-input** $A\mapsto\Phi(A)$ with correct SAT/UNSAT/MALFORMED labels and same-machine fully charged $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$; full historical R_mix341 authentication and all-rule/B3 transfers likewise remain OPEN. P versus NP OPEN.
