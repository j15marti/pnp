# LSPV-4/465: exact static-anchor checkpoint/recomputation resource frontier for typed TREE3

**2026-11-07 03:36 PST | LSPV-4 Route A | PROVED/RESTRICTED exact static-checkpoint optimum; COMPUTATIONAL 134,126 finite checks; CONDITIONAL full guest bounds; all-input P versus NP remains OPEN.**

## IDEA -> SEARCH -> ITERATE

**Hypothesis before searches:** The no-offset-table source address lookup of LSPV-4/464 can replace its repeated $O(h^2)$ header rereads by a static set of paid prefix checkpoints. With $m$ checkpoint offsets, the repeated-header work should be $O(h^2/m)$ while staying in the already budgeted $N^{1/10+o(1)}$ writable workspace of the specialized typed TREE3 solver.

Four falsifiers:
1. Uneven checkpoint partitions beat the proposed optimum or postorder invalidates the exact count.
2. Every *guest input bit read*, rather than every source block, requires a fresh prefix scan.
3. Simultaneous checkpoint, parser, message-stack and auxiliary state exceeds the local writable cap.
4. A truncated source header, repeated variable within a strict 3-clause, or incorrect source base passes source validation.

Revisions: F1 tested by exhaustive integer-composition enumeration for all $2\le h\le10$ and proved by convexity. F2 requires caching one base address throughout all guest calls for the current node. F3 uses an explicit *simultaneous* expression, conditional on all the other already budgeted typed-tree subsystems. F4 is tested with three negative controls. No all-input or native interpreter claims arise.

## Theorem 465.1 (PROVED/RESTRICTED)

Consider an original binary-encoded signed proper-3CNF source with $h$ syntactically authenticated, length-prefixed, contiguous blocks in heap index order, private/parent-child edge typed variable namespaces and $O(\log N)$-bit block-length headers. A depth-first postorder evaluation locates each block once and retains its base for all its guest SAT calls. In the **static-anchor-only** submodel, the controller stores only $m$ persistent block-base offsets, $1\le m\le h$, and at each requested block walks forward over the intervening raw source headers from the nearest preceding checkpoint. It does not store additional completed-block offsets between node evaluations.

Let static checkpoint intervals contain positive integer numbers of blocks $g_1,\ldots,g_m$, with $\sum g_j=h$. Every block base is requested once. The **exact** number of re-read source headers is

$$
Q(g_1,\ldots,g_m)=\sum_{j=1}^m\frac{g_j(g_j-1)}2.
$$

Set $a=\lfloor h/m\rfloor$ and $r=h-ma$. The minimum over *all static checkpoint interval partitions* is

$$
\boxed{Q_{\min}(h,m)=(m-r)\frac{a(a-1)}2+r\frac{a(a+1)}2.}
$$

**Proof:** In an interval containing $g$ blocks, the first requested base needs zero prior header reads, the next one, and so forth through $g-1$, giving $g(g-1)/2$. If two interval sizes differ by at least two, moving one block from the longer interval to the shorter changes the sum by $-(g_{\rm long}-g_{\rm short}-1)<0$. Thus every optimal partition has intervals of sizes $a$ and $a+1$ only, with $r$ intervals of the latter size. The formula follows. The underlying source position is retrieved exactly because every length prefix is authenticated and the address arithmetic is exact. The postorder sequence does not alter the number of repeated reads in the stipulated non-caching-between-nodes model. QED.

**Scope:** This exact minimum is not a proof that every physical data structure or SAT algorithm requires the displayed number of probes. Dynamic offsets, alternative source orders, semantic transformations, extension variables, alternate source representations, and unrestricted algorithms remain legal. The number of guest queries is NOT multiplied into this offset-scan cost because current-node base caching is explicit.

## Paid indexed-resource theorem 465.2 (PROVED/RESTRICTED)

During the mandatory one-pass syntax authentication, store $m$ checkpoint offsets. Store each in $\lceil\log_2(N+1)\rceil$ bits, including address arithmetic and current header parsing. The initial syntax pass examines every required source bit and costs $O(N\operatorname{polylog}N)$ time and $O(\log N)$ temporary space apart from checkpoints. A lookup from checkpoint to node reads each intervening length header with a paid input-index jump, repositions the source/index heads, validates length and advances the current $O(\log N)$-bit offset. Consequently

$$
T_{\rm offsets}=O((N+Q_{\min}(h,m)+h)\operatorname{polylog}N),
\qquad
S_{\rm offsets}=O((m+1)\log N).
$$

For $h\le N^{1/2+o(1)}$ take $m=\min(h,\max(1,\lfloor N^{1/10}/\log_2(N+2)\rfloor))$. Then

$$
Q_{\min}(h,m)\le N^{9/10+o(1)},\qquad
S_{\rm offsets}\le N^{1/10+o(1)}.
$$

By comparison, LSPV-4/464 had $m=1$ and exact repeated-header count $h(h-1)/2$. The new scheme improves this individual operation but **does not** change the total local time exponent because the full $N$-bit authentication scan remains mandatory.

With $w\le (\log_2 N)/10+o(\log N)$ and $q\le(h-1)2^w+1$ established in the typed TREE3 subtree identities of LSPV-2/459, include auxiliary blocker/pin creation, message handling, and the source header costs together:

$$
T_{\rm local}=O((N+Q_{\min}(h,m)+q2^w w)\operatorname{polylog}N)
= N^{1+o(1)},
$$

$$
S_{\rm local}=O((m+2^w w+2^w\log h)\log N+\operatorname{polylog}N)
=N^{1/10+o(1)}.
$$

The space expression counts checkpoint offsets, *currently live* child message tables, the current auxiliary guest suffix, source/index/header counters, and current-node cached base **simultaneously**. Guest work tape high-water, multiple work/index tape conversion, epoch cleanup, output and any source-grammar conversion must be added when deriving physical *total* machine costs. There is no unseen source-offset array.

**CONDITIONAL only:** If the full native FLMV guest interpreter eventually proves $O(T_A(B)\operatorname{polylog}N)$ time and $O(S_A(B)\operatorname{polylog}N)$ space, with $B\le N^{1/2+o(1)}$, this restricted typed TREE3 compiler still has

$$
t'\le\max(1,3/5+t/2),\qquad s'\le\max(1/10,s/2).
$$

This is not recursively closed, all-input, malformed-aware contraction; [P2-A2] and [P2-A5] remain OPEN. The known restricted source is a *promise grammar* and its child SAT formulas need not satisfy that grammar. If acquisition of a bounded-interface tree fails on arbitrary sources, that search/failure/conversion expense must be charged rather than assumed away. Original-source source IDs are retained; no semantic oracle is used.

## Established hard family and known shortcuts ledger

Odd-charge cubic-expander Tseitin sources $T(G_H,\chi)$: each graph edge is one Boolean variable, and each cubic vertex is encoded by the four proper signed ternary clauses forbidding the wrong parity assignments. There are $3H/2$ variables and $4H$ clauses, and for dense binary edge IDs $N=\Theta(H\log H)$. Odd total vertex charge certifies UNSAT. Urquhart (1987, JACM) and Ben-Sasson/Wigderson (2001, JACM) supply exponential proof-size hardness for suitable expander instances **in ordinary shared-DAG Resolution only**. GF(2) elimination supplies a polynomial-time algorithmic shortcut. There is no lower-bound-preserving transfer supplied into the historical full mixed R_mix341 nor arbitrary machines, and the typed TREE3 promise is not asserted for expanders. Finite K4 even/odd charge controls certify 8/0 satisfying assignments but no asymptotic hardness.

## COMPUTATIONAL verified controls

Exact published executable path: experiments/arc/lspv4_465_checkpoint_optimum.cjs, Git blob 0bcb075577b6af5d608c46afa58325420ac2c865, replayed by evaluating the **complete GitHub-readback source** in V8. Results: 134,126 assertions PASS; 8 original signed proper 3-CNF typed tree sources, with $h=3,7,15,31,63,127,255,511$; 49 independent checkpoint budgets; 7,883 postorder node-base lookups; 341,277 re-read header probes; 118,245 cached original-source virtual guest bit comparisons; 54 exhaustive small integer-composition optimum tests; original signed K4 even/odd charge SAT/UNSAT controls; 3 malformed/corrupted input rejections. The concrete tests use fixed 16-bit block length headers; the mathematical theorem permits $O(\log N)$-bit headers. No native FLMV instruction counts or physical memory-high-water measurements have been performed.

For $h=511$ and 60,247 source bits, the finite work-space/work tradeoff was: $m=1$: 130,305 re-read headers, 16 checkpoint bits; $m=8$: 16,065 headers, 128 checkpoint bits; $m=32$: 3,825 headers, 512 checkpoint bits; $m=511$: 0 repeated headers, 8,176 checkpoint bits. The 49-case raw ledger, rather than a selectively reported successful example, is at results/raw/arc/2026-11-07_0336_LSPV4_465_SPARSE_CHECKPOINT_RAW.json; raw Git blob cdc14c6c7a13972caa01b8134a5d4af29d625e6b. These numerical probes are an abstract charged-header model, not calibrated native steps.

## Project and literature review

Read complete current root proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt prepublication SHA 503117333adb058c04d65e2b8332c31208d9a7d8, including [P1-S3], [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-B1], [P2-B2]. Read current issue #3, governing 2026-11-02 five-role handoff SHA c3889a3e514ddbd747150dcb68607013a3b2d154, AGENTS.md SHA 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md SHA 754999f50de93cdb693ed37bc8110d31e9e698ef, repository skill SHA b8df83a7b0b1428f349b0e02ce1387d979e8db7f, peer LSPV-2/459, LSPV-2/466 SHA c2b17af05e1843bf88d25a7875f047f0f56817a1 and LSPV-4/464 SHA 321ec95736a607734e049cf0aff76377b05822f2. Actual recent Grok: GROKPROOF/2026-11-07_1119_PROGRESS.md SHA d87fcb3a12ed115c277f7ffda87ecca0f4072630; Claude: research/agents/claude/world-ledger/README.md SHA de75a371ce3143a4495e6892df7fb04794a6b708.

Primary FLMV paper: Fortnow, Lipton, van Melkebeek and Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52 (2005), 835-865, DOI 10.1145/1101821.1101822, author PDF https://lance.fortnow.com/papers/files/tst.pdf Section 2.1, page 4 screenshot actually inspected. Its model has indexed work-tape high-water, erased index contents at jumps, and read-only input. The published time-space lower bound is a genuine model-qualified theorem, not a result of the present compiler. Additional primary proof-complexity controls: Urquhart (1987), Ben-Sasson/Wigderson (2001).

Exact files in additional searched repositories: konard/p-vs-np/proofs/complexity/README.md SHA 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3 (distinct finite one-tape model); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5 and AFFINE_BOUNDARY_PHASE_REPORT.md SHA 3228ffe817b5f0a2784eb4a85d6c547917ab78d9 (bounded/capped claims); meelgroup/frat-xor/format.md SHA 986a21aa92b62f844ef1fce852193142c41b2b1 (different certificate grammar); openai/math/README.md SHA cc5b0a03bca6c742f045d683b6647a6f44ef2cae (mixed formalization status). Web queries included FLMV indexed machine, checkpoint-prefix index tradeoffs, Tseitin Resolution expanders, and repo latest coordinate lift. A separate Google-branded interface was not verified, so only general web and connector sources are claimed. The checkpoint formula is not claimed novel relative to general static data-structure literature.

## Status, publication and precise remaining gap

**PROVED/RESTRICTED** exact static-anchor model optimum; **COMPUTATIONAL** full code readback + V8 checks; **CONDITIONAL** complete restricted SAT solver bounds; **OPEN** native same-machine interpreter, arbitrary SAT source acquisition and recursively iterable all-input transformation, [P2-A2],[P2-A5], historical R_mix341 full mixed and noncircular B3. Root main.tex SHA 68188a24badda635a5983fda1c381cdb694fd497 returned zero readable contents; no partial or destructive manuscript overwrite attempted. No project preflight or native-machine run is claimed.

**Actual advance:** proved an exact memory/offset-probe Pareto formula and realized it as a concrete typed-tree source index subsystem. **Remaining gap:** total native guest simulator and all-input recursive transfer. **P versus NP OPEN.**
