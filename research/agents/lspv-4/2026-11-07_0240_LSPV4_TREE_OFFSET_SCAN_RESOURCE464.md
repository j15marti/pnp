# LSPV-4/464: no-offset-table recovery for typed length-prefixed TREE3
**2026-11-07 02:40 PST | Route A | PROVED/RESTRICTED offset subcomponent, COMPUTATIONAL finite controls, CONDITIONAL guest bounds, OPEN universal contraction. P versus NP OPEN.**

## Idea -> Search -> Iterate
Hypothesis: the physical \(O(h\log N)\)-bit source-offset array in LSPV-2/459 and its LSPV-4/458 composition obstruction can be eliminated for **syntactically typed, contiguous, length-prefixed, heap-numbered complete binary-tree** original strict-3CNF sources without paying more than \(N^{1+o(1)}\) local time. This is NOT a claim for arbitrary 3-CNF.

Falsifiers: F1, recomputing the offset for each *guest bit read* multiplies guest time by \(h\). F2, unspecified block boundaries defeat random prefix skipping. F3, arbitrary cross-node numeric identifiers defeat cheap namespace authentication. F4, guest blocker clauses are assumed recursively within the original strict-3CNF tree grammar. Fix F1 by caching *one* base per current node; avoid F2/F3 by stronger length-prefixed and injected private/edge-typed-ID grammar; F4 remains OPEN.

## Theorem 464.1 (PROVED/RESTRICTED)
Suppose binary input length \(N\) explicitly describes \(h\le N^{1/2+o(1)}\) heap-ordered, contiguous, length-prefixed source blocks. The length of each payload is available from its \(O(\log N)\)-bit header. All original clauses have exactly three distinct signed variables and a record layout directly compatible with a substring of the general-CNF guest encoding. Every variable has one checkable type \(P(v,j)\), permitted only at node \(v\), or \(E(c,j)\), permitted only at child \(c\) and parent \(\lfloor c/2\rfloor\). Edge width \(w\) is syntactically limited, and distinct tagged names have injective encodings. The authenticated parse is therefore local; it needs no global occurrence array.

To find the start of block \(v\), start at the first block, read headers \(1,\ldots,v-1\), and perform paid input-index jumps across their payloads. Cache just the resulting \(O(\log N)\)-bit address and payload length for all SAT guest calls at that node. During the complete postorder computation, each of \(h\) blocks is located ONCE. Total lookup work is

$$
T_{\rm offsets}\le O\left(\sum_{v=1}^{h}v\,\operatorname{polylog}N\right)
=O(h^2\operatorname{polylog}N)
\le N^{1+o(1)},\qquad
S_{\rm offsets}=O(\log N).
$$

All input-index construction, bit probes, address increments, header decoding and source/head restoration are charged. A full syntax pass adds \(O(N\operatorname{polylog}N)\) time and \(O(\log N)\) working space. The input must be length-prefixed and typed; the *general* heap-tree grammar in LSPV-2/459 is not automatically covered. This is a physically realizable **source-index subsystem**, not a full native guest-machine interpreter.

## Existing OR-folding and conditional composition
Reuse LSPV-2/459's EXACT subtree semantics \(M_v(b)=\operatorname{SAT}(G_{v,b})\) and depth-first postorder. Distinct child assignment messages are conjunctive restrictions, not independent OR choices; each required child failure gives a genuine blocker clause. At most \(q\le(h-1)2^w+1\) guest SAT calls and \(O(2^w\log h)\) live child-table bits are needed. One virtual guest input consists of header + direct read-only source payload at cached base + physically generated unit-pin/blocker suffix. No original payload copy is stored. The source-to-guest clause-record compatibility is REQUIRED; no free reserialization.

Under \(B\le N^{1/2+o(1)}\), \(w\le(\log_2N)/10+o(\log N)\), the complete local-work and simultaneous-space bounds are

$$
T_{\rm local}\le O\big((N+h^2+q2^w w)\operatorname{polylog}N\big)=N^{1+o(1)}
$$

$$
S_{\rm local}\le O\big((2^w\log h+2^w w\log N)\operatorname{polylog}N\big)=N^{1/10+o(1)}.
$$

**CONDITIONAL ONLY:** if a fully charged native FLMV guest simulator has time \(O(T_A(B)\operatorname{polylog}N)\), workspace \(O(S_A(B)\operatorname{polylog}N)\) and correctly implements all input-index/work-index/head, erasure/reset, read-only port, storage, output and restart operations, the restricted typed tree compiler would achieve

$$
t'\le\max(1,3/5+t/2),\qquad s'\le\max(1/10,s/2).
$$

The native guest interpreter is NOT completed here. A valid general-CNF guest containing blockers/pins is NOT necessarily an original authenticated strict-TREE3 source, so recursive closure is NOT established. No fallback solves arbitrary all-input SAT with these exponents.

## Charged resource ledger and test
Preprocessing: one \(O(N\operatorname{polylog}N)\) syntax pass; local type checks, no search or failed decomposition policies under the explicit promise. Offset work: \(O(h^2\operatorname{polylog}N)\), cached current base \(O(\log N)\) bits. Child creation: zero copied original payload bits; \(O(2^w w\log N)\) current auxiliary suffix, total \(O(q2^w w\operatorname{polylog}N)\) regeneration. Live space: all child message stack + suffix + current cached base + guest work together, with actual guest space separately charged. Output bits, probe-index updates, cache cleanup/recomputation, and sequential guest work are not treated as free. Critical path and work are not interchangeable; one guest runs at a time. An ideal Route B proof DAG is a different cost object.

**COMPUTATIONAL:** self-contained independent V8 finite checker constructed 8 original proper signed 3-CNF heap-tree sources at h=3,7,15,31, four SAT and four UNSAT. Every UNSAT original has conflicting **source-claused** 4-clause strict-3CNF unit pins on edge \(E(2,1)\), while each affected local block is SAT; a genuine AND-join test. It checked 216 guest SAT calls, 149,562 bitwise comparisons of a virtual source-backed guest input with the explicitly assembled guest, 1,300 recomputed length headers, 32 malformed/corrupt source rejections, 149,955 assertions, zero failures. Maximum original source was 26,467 bits and guest 934 bits. The finite script uses fixed-width 16-bit headers and strict-three padded-record guest syntax for w=1, **not** the asymptotic length-delimited general-CNF implementation. No native FLMV instruction measurement.

## Established hard-family ledger
For odd-charge Tseitin \(T(G_H,\chi)\) on a connected cubic edge-expander with \(H\) vertices, each graph edge is a Boolean variable and each vertex contributes **four signed proper ternary clauses** excluding the wrong charge parities. There are \(3H/2\) edge variables, \(4H\) clauses, binary length \(N=\Theta(H\log H)\); odd total charge certifies UNSAT. Urquhart (1987), Ben-Sasson and Wigderson (2001) yield size \(2^{\Omega(H)}\) for suitable families in **ordinary shared-DAG Resolution**, not in the full mixed calculus or on arbitrary machines. Explicit K4 even/odd signed 3-CNF variants were brute-enumerated as finite controls. GF(2) summation is the mandatory polynomial-time shortcut; no hardness transfer is inferred. This family need not satisfy the typed TREE3 promise.

## Continuity, sources, scope
Both current root \`proof1.txt\` and \`proof2.txt\` were read, including [P1-S3], [P2-A4], and the still-OPEN load-bearing [P2-A2], [P2-A5]; unrelated [P2-D1], [P2-B2] remain OPEN. Actual original work reviewed: LSPV-2/459, LSPV-2/465, LSPV-4/458, LSPV-4/463, current issue #3, 2026-11-02 five-role handoff, AGENTS.md, CODEX.md, project skill, Grok 2026-11-07_0819, Claude world-ledger README. Primary FLMV JACM (2005) Section 2.1 PDF p.4 image inspected. Repositories inspected: \`konard/p-vs-np/proofs/complexity/README.md\` (finite one-tape model); \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` and \`AFFINE_BOUNDARY_PHASE_REPORT.md\` (bounded claims); \`meelgroup/frat-xor/format.md\` (different calculus); \`openai/math/README.md\` (mixed verification status). Google-branded separate interface unverified, general web and connector repositories searched.

**Actual advance:** eliminates the \(h\log N\)-bit *offset array* only under stronger length-prefix/typed-ID grammar. **Verification:** restricted symbolic proof plus finite V8 test, not native execution. **Publication:** associated path/code/raw/handoff and issue readback separately. **Remaining gap:** native complete guest interpreter and universal recursively iterable all-input source acquisition [P2-A2]. P versus NP OPEN.