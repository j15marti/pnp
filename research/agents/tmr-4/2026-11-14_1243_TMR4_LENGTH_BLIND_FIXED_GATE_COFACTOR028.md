# TMR-4/028: Length-blind cofactor inheritance for fixed-gate MCSP

**Date:** November 14, 2026, 12:43 PST (America/Los_Angeles). **Role:** TMR-4 Cost-Sound Abstraction.
**Status:** PROVED/RESTRICTED symbolic constructive upper bound, pending TMR-1/TMR-2/TMR-5 peer audit; finite verification COMPUTATIONAL; P versus NP OPEN.

## Preflight, historical ledger, novelty

Read the current Nov-14 MCSP directive FIRST (blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then Nov-13 TMR replacement, AGENTS.md, CODEX.md, pnp research skill, issue #3 through TMR-3/027, all five current TMR handoffs, root proof1.txt (28,714 characters), proof2.txt (1,051,196 characters), and root main.tex (2,545,859 characters). Large-file Git contents responses were blank for proof2 and main.tex; full texts were recovered from original Git blobs 930c5eeddafce656717f28055a7a9a755f44737c and 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. No root changes.

Relevant original files and status:

| Original artifact | Status / distinction |
| --- | --- |
| research/agents/tmr-5/2026-11-14_1155_TMR5_AFFINE_VS_NONLINEAR_STREAMING_REVIEW023.md | PRIOR length-blind single-work-tape MCSP[0] in O(N log^2 N) time |
| research/agents/tmr-2/2026-11-14_1221_TMR2_ODOMETER_CODE_CERTIFICATE027.md | PRIOR O(N log N) improvement for MCSP[0], and Hamming-code query theorem |
| research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md | PRIOR fixed source-independent affine sketch Hamming-far collision; does not cover nonlinear adaptive summaries |
| research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex | PRIOR ordinary MCSP fixed affine-kernel collision |
| research/agents/tmr-1/2026-11-14_1200_TMR1_MCSP_GATE_SPECTRUM_RESOLUTION026.md | PRIOR additive circuit-size spectrum and failed dummy-padding threshold transfer |
| research/agents/tmr-3/handoff.md, current /027 | PRIOR annotated single-work-tape source padding and restricted full-output header bound |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, 2026-10-28_1326_CLAUDE_TPORT-0001.tex, 2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex | PRIOR one-tape/portfolio transfer cautions |
| research/agents/lspv-2/2026-11-01_0515_LSPV-2_STREAMED_WALSH_OVERLAP297.tex, GROKPROOF/2026-11-13_0526_PROGRESS.md | PRIOR compact algebra / restricted-checker controls, not universal SAT hardness |

**New relative to the repository:** An explicit length-blind streaming construction for ordinary exact MCSP at **every fixed gate count s0**, not just zero gates. The key device is cofactor inheritance across growing source-length stages. This is an elementary construction, not claimed an external literature-first result. It falsifies an attempted passage from the fixed affine-sketch/description-count lower bound to an arbitrary one-work-tape decision-time lower bound at fixed thresholds.

## Theorem FIXEDGATE28 and detailed proof

Fix any integer s0>=0 **once in the finite program**, independently of input length. Circuit basis is fan-in-two AND/OR, unary NOT, free constants and input wires, unrestricted fanout; count Boolean gates. The target language is exact ordinary MCSP[s0] on a complete truth table of N=2^n bits, n>=1, in standard binary assignment-index order. Malformed lengths are rejected. There is no promise, header, oracle or advice.

**Theorem (PROVED/RESTRICTED, independent audit pending).** One deterministic finite-control machine with one **one-way read-only input** and exactly one two-way read/write work tape decides both labels for every valid length without knowing N or n beforehand, with

$$
S(N)=(\log N)^{O_{s_0}(1)},\qquad
T(N)=N(\log N)^{O_{s_0}(1)}.
$$

Conservative constructive accounting yields S(N)=O_s0((1+log N)^(2s0+5)) and T(N)=O_s0(N(1+log N)^(6s0+20)). For every epsilon>0 this is O_s0,epsilon(N^(1+epsilon)), including epsilon=0.01. The exponent's hidden constant depends on **fixed s0** and is not uniform over a growing s(N).

**Step 1: All descriptions.** Enumerate every ordered circuit DAG description of at most s0 gates, including any gate or base source as output. A loose bound on their number is

$$
D(n,s_0)=(s_0+1)(n+s_0+2)[3(n+s_0+2)^2]^{s_0}
=O_{s_0}((n+1)^{2s_0+1}).
$$

Store one match flag for each *description*, not only distinct truth tables. The fixed control generates descriptions with counters on its sole work tape; no circuit minimization is performed.

**Step 2: Invariant.** Having read the first i table bits x_0,...,x_(i-1), for every current candidate c maintain a_c=1 exactly when c(j)=x_j for every j<i. Initially use the zero-arity constant-circuit list. At each next input bit i, evaluate all candidate circuits on the standard binary address i and update a_c by conjunction with [c(i)=x_i]. All shared gates, inversions and constants are evaluated according to their actual descriptions.

**Step 3: Length-blind promotion.** When exactly 2^k bits have been read, all candidates in the k-input list have correct flags for the full prefix. If endmarker follows, output the OR of these flags (reject length one if n=0). Otherwise, before consuming the next bit, promote to the k+1-input list. For every new circuit c, substitute its newly appearing most significant input variable z_k with constant zero, obtaining a k-input circuit c0 with at most s0 gates. Crucially c0 is present as a syntactically generated candidate in the previous list, without any gate minimization. Initialize the new flag a_c from the old flag a_c0. All previously observed addresses j<2^k have z_k=0, so this inheritance is exact. Discard old list and process the next source symbol normally. By induction, the invariant holds at **every** prefix for **every** input length. This avoids replaying unreadable earlier input bits.

**Step 4: Terminal labels and physical charges.** At endmarker accept iff input length is a power of two at least 2 and some surviving candidate flag is 1. By the invariant this is equivalent to the complete table having a circuit of <=s0 gates. Both YES and NO are preserved. Input-head movement, indexing, new-candidate generation, substitution, buffers, circuit evaluation, flag updates and terminal output are included. Both old/new lists coexist only during each promotion. All descriptions, counters, flags and temporary gate buffers fit in O_s0(D(n,s0)(n+s0+2)^3) visited work cells. A conservative nested-sweep implementation on **one locally moving work tape** uses O_s0((D+1)^3(n+s0+2)^10) transitions per input symbol and per promotion. Since promotions are O(log N), the displayed loose bounds follow. This uses only fixed finite-state loops and finite-alphabet local moves, not unbounded-word arithmetic or a second work tape.

## Full limitation and magnification matrix

| Exact primary result | Input measure, gate threshold, machine, conclusion | Relationship to FIXEDGATE28 |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, **Theorem 1, p. 23:3** [1] | Ordinary exact MCSP[2^(mu1*n)] on explicit N=2^n truth-table bits, small fixed mu1>0; if NO deterministic one-way-input/one-work-tape O(N^1.01) decider, then P!=NP | Required hypothesis OPEN. Fixed s0 is not N^mu1. |
| Same paper, **Theorem 2, p. 23:3** [1] | Randomized two-sided-error one-way-input/one-work-tape N^1.99 lower bound for MCSP[2^(mu2*n)] at a distinct, larger mu2>mu1 | KNOWN THEOREM; stronger exponent at wrong threshold cannot be transferred. |
| McKay, Murray, Williams, STOC 2019 [2] | Streaming/search-resource magnification for bounded-circuit compression; model and resource parameters must be held fixed | No reduction from this fixed-s0 algorithm is claimed. |
| Oliveira, Pich, Santhanam, CCC 2019 [3] | Hardness magnification in restricted/approximation circuit variants | No promise or nonuniform transfer asserted. |

The source SAT encoding length L is **not** n or N. A succinct 3-CNF satisfaction predicate does not give its full N=2^n truth table for free. The algorithm starts with an **already explicit** MCSP truth table. The threshold-growing regime is the exact missing step: when s(n+1)>s(n), the cofactor of a newly admitted (n+1)-input circuit may require more than s(n) gates, so the previous stage need **not** contain its comparison flag. At s(N)=N^mu the number of candidate descriptions is no longer polylogarithmic. Neither the missing cofactor summary nor a matching one-tape running-time bound is established. No result about Gap-MCSP at altered distance parameters, MKTP, SAT or P!=NP follows.

## Executed computational verification

**Native CPython actually executed** the exact committed program experiments/tmr/tmr4_fixed_gate_stream028.py with seed 20261114. It enumerates complete distinct circuit-function classes for gate budgets s0=0,1,2 at arities n=0,...,4, checks the cofactor inclusion property and compares the staged prefix-flag algorithm against independent offline circuit-class membership. For n<=3 it tests every truth table; for n=4 it tests 512 seeded random tables per s0. Non-power-of-two malformed-length controls are included.

**2,593 assertions/classifications/cofactor checks, zero failures**. Candidate function counts by n=0,...,4: s0=0: [2,3,4,5,6]; s0=1: [2,4,8,14,22]; s0=2: [2,4,14,40,90]. The three runs also recorded 60,984, 180,256, and 607,552 **semantic candidate-flag proxy updates**. These are NOT native tape transitions. This finite experiment does not establish asymptotic complexity.

Source: experiments/tmr/tmr4_fixed_gate_stream028.py, SHA256 dca4dee365d63a3bce111d8f6a4cf13576f019a97ef5cc56bfb586960413e496, Git blob 4dcb1a429d3b9531209ffbdda13cdcf05d72fb9c.
Raw: results/raw/tmr/2026-11-14_1243_TMR4_FIXED_GATE_STREAM028_RAW.json, SHA256 b6eb3e1e804c15201feb696d136d63a00f6b32d522711937dfa7bf52a0a4e653, Git blob bad20bb6e1223a998fa1ef153a177f929ab1fc51.
This is a finite semantic-mask emulator, **not** a native finite-alphabet one-tape transition compiler. The one-tape resource theorem is a symbolic constructive charge, pending independent audit.

## Hostile controls, exact remaining gap, review request

Circuit constants, projections, inversions, AND/OR fan-in-two, shared subexpressions, dummy inputs and bit-index extensions are included. The method never requires enumerating satisfying assignments of SAT, or maintaining a large fixed affine sketch, or producing a full permuted/padded target table. Gaussian elimination on XOR, Horn/2-SAT, bounded-treewidth DP, products, auxiliary variables, sharing, source rewrites and rereads remain legitimate alternative computations; no restricted representation is asserted unavoidable.

**Failed implication:** A rank/description-count obstruction for a fixed source-independent sketch does not entail a superlinear fixed-exponent lower bound on one-way-input one-work-tape MCSP[s0] decision, for ANY fixed s0. The counterexample is this complete uniform algorithm. Its existence is compatible with TMR-4/027's restricted kernel theorem and TMR-2/027's deterministic high-query-complexity result.

**Next target:** For a growing schedule s(n), determine whether a cost-sound *compact inherited prefix state* can represent comparisons against newly admitted circuits after a length doubling. First hostile test: choose s(n+1)>s(n) and find an explicit cofactor circuit requiring >s(n) gates, invalidating naïve flag inheritance. Charge every stage and explore whether a stronger nonlinear summary repairs it. TMR-2 should audit the prefix-flag invariant and output labels, TMR-3 the one-tape sweep bound, TMR-1 the exact CHMY threshold, and TMR-5 the no-header model and potential overlooked circuits. All magnification and arbitrary-SAT arrows remain **OPEN**. Root proof1/proof2/main.tex unchanged; schedules unchanged.

## References

[1] M. Cheraghchi, S. Hirahara, D. Myrisiotis, Y. Yoshida. One-Tape Turing Machine and Branching Program Lower Bounds for MCSP. STACS 2021, Theorems 1–2, p. 23:3. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] D. McKay, C. Murray, R. Williams. Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes. STOC 2019. https://doi.org/10.1145/3313276.3316396

[3] I. C. Oliveira, J. Pich, R. Santhanam. Hardness Magnification near State-of-the-Art Lower Bounds. CCC 2019. https://doi.org/10.4230/LIPIcs.CCC.2019.27
