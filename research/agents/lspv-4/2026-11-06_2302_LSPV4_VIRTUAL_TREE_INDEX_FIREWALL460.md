# LSPV-4/460: Paid virtual guest input and long-index firewall for postorder TREE3
**2026-11-06 23:02 PST | Route A | PROVED/RESTRICTED bit-access lemma; CONDITIONAL native guest simulation; COMPUTATIONAL independent checks. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE: exact target and falsifiers
**Hypothesis.** For the authenticated POSTORDER TREE3 family of LSPV-2/461, the remaining rank/select and guest-input reconstruction assumptions can be replaced by a simpler concrete bit transducer: build only a small auxiliary clause suffix per guest call, alias the current source block directly, and answer every virtual guest-input bit query with paid indexed access. A second firewall must account for very long guest input-index tapes instead of rereading all index bits at each jump.

**F1:** An original signed strict-three clause's record bits fail to match the guest record bits (e.g. minimal-width encoding differs). **F2:** Regenerating the auxiliary suffix per guest costs more than N^(1+o(1)) local work or N^(1/10+o(1)) peak memory. **F3:** An out-of-range indexed read on a long guest index tape requires a scan of its whole contents per access. **F4:** Source/guest index-head restoration, epoch clearing, work-tape stores, malformed input, or general SAT fallback is treated as free or extends a restricted theorem to all inputs.

**Search and revision.** Read both root trackers and project LSPV-2/459, /461, LSPV-4/458, /459, governing handoffs, issue #3, AGENTS.md, CODEX.md, repo skill, GROKPROOF 2026-11-06_2316, and Claude onetape/tport/world-ledger notes. The /461 report already establishes a postorder message scheduler and suggests rank/select for forbidden assignments. The revision here avoids rank/select entirely by materializing ONLY the small auxiliary suffix. The long-index test explicitly distinguishes an incremental index summary from a hidden scan. Primary FLMV [R1] Sec. 2.1 confirms native indexed moves erase the index tape and that work-space counts the greatest accessed work-tape position. This is a narrower bit-provider lemma, not a new universal contraction.

## Exact promised source/guest encoding
Fix ONE general-CNF guest encoding E accepting binary strings consisting of a self-delimiting field-width r, a self-delimiting clause count m+1, followed by m clause records. Each record contains an r-bit arity followed by that many (sign bit, r-bit nonzero variable ID) literal fields. The parser accepts any sufficient declared r, not ONLY the minimal width determined by input length. Source TREE3 blocks consist of the SAME strict-three clause records, preceded by source-only block boundaries. The source contains a perfect binary tree in left/right/parent postorder with the owner/interface grammar of LSPV-2/461. Each original clause remains a byte-for-byte alias of a source record. All source descriptors, numeric IDs, end markers, and bounded-interface promises are validated before final answer. For large sources choose r=O(log N), large enough for all original IDs and pins; arity of generated blocker clauses is <=w and thus representable.

This is an **explicitly promised aligned encoding**, not a theorem that all standard DIMACS encodings are bit-compatible, nor that an arbitrary guest program speaks another encoding. If E demands a different minimal-width encoding, this direct-alias proof does NOT apply. No unsafe source authentication or semantic test is supplied by the accessor itself.

At postorder node v store only its current source record-bit endpoints (a_v,b_v), its two completed child message bitmaps, and the active stack of older subtree messages. For parent interface assignment b, the guest CNF is the existing LSPV-2/461 equation

$$
G_{v,b}=F_v\wedge\operatorname{pin}(E(v),b)\wedge
\bigwedge_{c\in\operatorname{children}(v)}
\bigwedge_{\alpha:M_c(\alpha)=0}D_{c,\alpha}.
$$

D_(c,alpha) is the actual clause falsified precisely by alpha, including a genuine empty clause for a false zero-width interface. For each guest call, physically create ONLY the generated header and all blocker/pin clause records, in an auxiliary suffix buffer. No full source block or guest input is copied. The virtual bit reader first tests whether the requested position lies in the header, then (a_v,b_v), then the auxiliary suffix; otherwise it returns the guest input blank symbol. A source-range read translates guest position j to a_v+j-offset. All transitions of the native source index register, index-tape erasure, head positions and returning to the forward source parser cursor are paid.

## Theorem 460.A: explicit bit-provider resources (PROVED/RESTRICTED)
Assume h,L_max<=N^(1/2+o(1)), interface width w<=log_2(N)/10+o(log N), owner-tagged postorder source, canonical r=O(log N) fields as above, and a constant finite number of clause regions in each guest.

The generated suffix contains at most two child blocker tables and one outgoing pin table. Its explicit size is

$$
O(2^w\,w\,\log N+\operatorname{polylog}N)=N^{1/10+o(1)}
$$

bits. Constructing it from child message bitmaps takes the same order of time per guest. The guest-input bit transducer uses O(log N) temporary address/index registers and O(log N) native steps per requested bit, including a fresh parent source-index tape fill and erasure. It never needs a global table of h source offsets: the postorder scheduler retains the current (a_v,b_v) and restores the parser at b_v.

The number of guest queries q<=(h-1)2^w+1<=N^(3/5+o(1)). Hence ALL repeated physical suffix builds cost at most

$$
O(q\,2^w\,w\log N)=N^{7/10+o(1)},
$$

within the O(N polylog N) source-validation envelope. This eliminates the proposed rank/select prerequisite in /461 for the stated aligned encoding. It does NOT establish a program that solves arbitrary 3-SAT or an unrestricted native interpreter for all guest instructions.

**Proof.** Three contiguous regions partition the guest binary string. A source record is an exact bit alias by the fixed r-record grammar; each other bit belongs to a physically computed finite header or suffix. Therefore the accessor equals the fully materialized legal guest string at every position, including beyond the logical end. All source offsets, region lengths, and index registers are O(log N) bits. A native FLMV indexed move to the parent input requires a constructed O(log N)-bit address and clears its index tape [R1]. Enumerating the <=2^(w+1) forbidden child assignments and <=w pins once per guest yields the suffix bound. Multiply by q for the total. QED.

## Lemma 460.B: long guest input-index summary (PROVED/RESTRICTED abstract tape representation)
A naive virtual-index dispatcher that scans the entire simulated guest input-index tape on EVERY guest input move can incur superlinear work relative to the guest, even when the indexed move itself is one native step. Explicitly maintain its low ell=ceil(log_2(B+1)) binary digits and a count H of nonzero higher digits. Every guest index-tape head edit updates either a low digit or H, using its simulated head position (index tapes themselves are sequential). An indexed guest input read is in range iff H=0 and the low value is <B. The read then uses Theorem 460.A. Clearing the guest index tape is an epoch reset, not a scan. For guest input-index tape length polynomial in B, each edit, move, counter update and address test costs polylog N time and bits (plus any live simulated tape-cell storage already charged to guest workspace). No uncharged long-index-to-integer conversion is necessary.

This is a *representation lemma*, not a full native interpreter proof. Exact tape-alphabet/binary orientation, index-tape edit conventions, epoch-tag physical store, sparse high-water guest WORK-tape simulation, and matching native tape count still require complete machine instruction verification. The high/low summary needs a correct write/update path for ALL guest index-tape mutations. It is not justified to read the whole index tape on every jump.

## Conditional matched-machine composition and complete resource ledger
If a fixed total correct general-CNF A on this SAME specified FLMV indexed machine admits a fully verified paid interpreter with O(polylog N) overhead per A transition (including work/index tapes, sparse high-water, output, restart and caches), then the postorder tree wrapper has

$$
T_{\Phi(A)}(N)=O\bigl(N\operatorname{polylog}N+qT_A(B)\operatorname{polylog}N\bigr),
\quad B=N^{1/2+o(1)},
$$

$$
S_{\Phi(A)}(N)=O\bigl(2^w w\operatorname{polylog}N+S_A(B)\operatorname{polylog}N\bigr),
$$

thus **only on the promised aligned TREE3 class and under the interpreter premise**

$$
t'\le\max\{1,3/5+t/2\},\qquad s'\le\max\{1/10,s/2\}.
$$

**Ledger:** validation/source-index and head reads O(N polylog N) time; failed guest policies <=q and explicitly charged; per-guest header/suffix allocation/build/clear O(2^w w log N); parent read-only source alias O(log N) per guest bit; guest input-index high-bit summary polylog per modification/move; work/index-tape and epoch store O(S_A(B) polylog N) simultaneous peak conditionally; retained AND/OR message stack O(2^w log h) bits; active source offsets O(log N); output one final SAT/UNSAT bit after complete source validation; off-promise CNF and malformed inputs still require separate total behavior. No physical complete B-bit child is allocated in this construction. All source/aux buffers coexist when their peaks are counted. A production implementation must log actual inference/certificate bytes separately from decision bits; this is not an R_mix341 proof.

**Resource falsifier retained:** If an indexed guest simulation cannot answer all input and work-tape events with the stated per-transition bound, the conditional exponent claim is WITHDRAWN, and /459's charged materialized-child envelope is the fallback. In particular, a source encoding forcing full block conversion breaks Theorem 460.A's bit-alias premise. An off-promise valid CNF must not be declared malformed merely because the special parser refuses it.

## Existing hard-family and shortcut ledger
**Published family:** Urquhart (1987), and Ben-Sasson/Wigderson (2001), odd-charge cubic-expander Tseitin. Each vertex v, incident edges e1,e2,e3, charge chi_v, gives four original clauses excluding wrong-parity assignments:

$$
C_{v,a}=\bigvee_{i=1}^{3}(a_i=0?x_{e_i}:\neg x_{e_i}),
\qquad a_1\oplus a_2\oplus a_3\ne\chi_v.
$$

There are 4H original strict-three clauses on 3H/2 edge variables and N=Theta(H log H) source bits for dense binary IDs. Odd total charge certifies semantic UNSAT. Suitable cubic expanders have 2^Omega(H) lower bounds for **ordinary shared-DAG Resolution** [R2,R3]. The legally available GF(2) charge sum is a polynomial shortcut and must be counted as an upper-bound control. The original-clause source-tree interface obstruction of LSPV-4/459 prevents simply assuming this family is inside the postorder small-interface class. No all-machine time lower bound, mixed-rule size lower bound or lower-bound-preserving translation follows.

**Other controls:** Horn, 2-SAT, independent blocks, tiny UNSAT core, arbitrary renaming and large-ID cases; extension-variable proofs, branching shared DAGs and parity elimination remain available and cannot be excluded to protect a hardness assertion. [P2-A2], [P2-A5], [P2-B2] remain OPEN.

## Reproducibility and literature/repository audit
Local Python bit-exact producer: 24 original signed 3-clause-tree cases, 384 separate guest formulas, 90,528 total guest virtual-bit/beyond-end probes, 384 SAT classifications by independent direct assignment predicate, 72 truncation/trailing/alias-mutation controls. PASS, fixed seed 460. Independent Node.js implementation: 384 guest formulas, 90,528 bit probes, 384 SAT comparisons, 72 mutation controls, PASS. Additional independent Python index-tape tracker: 10,000 random tape actions, 1,005 range checks, 91 out-of-range events, 999 epoch resets, 5,004 writes, plus a distant high-bit control, PASS. These are host-language finite tests, **NOT native FLMV instruction-level measurements**. Full Python/JS source and raw are in the supplied reproducibility archive.

Actual read refs: j15marti/pnp proof1.txt [P1-S3],[P1-01],[P1-04]; proof2.txt [P2-A2],[P2-A4],[P2-A5],[P2-D1],[P2-B2], governing handoff and issue #3; LSPV-2/461 blob e44d45e052f8ed6f0a1f7873b1b1db3f3c4e934f; LSPV-4/459 blob 9795607976944dd924dd76ecae5867f8ed2e69a5; GROKPROOF progress blob a20fb8b3640d7574faf238a4a83a021bb0984808; Claude world-ledger README de75a371ce3143a4495e6892df7fb04794a6b708. NEW repo konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (finite-machine P subset NP only); blkph0x/p-vs-np-proof-research REVIEW_ADDENDUM.md blob 6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70 (qualified all-dual parity-polytope failure). FRAT-XOR format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f is DISTINCT external mixed-proof grammar, not a license to change historical R_mix341. OpenAI/math and ABC reviewed through already cited peer /461 (not independently fetched this run). Web/primary search included [R1]-[R3]. No independent branded Google service was used, no native-machine compiler was run, and no authoritative historical R_mix341 checker was invoked.

## Status and exact remaining gap
**Actual advance:** Proven explicit restricted virtual bit transducer that eliminates /461's rank/select premise, plus a provable incremental long-index range-check lemma and negative naive-index-scan audit. **Verification:** independent finite Python/JS checkers PASS; no native FLMV instruction execution. **Transfer:** All-input, source-agnostic, both-label/malformed-aware recursively iterable same-machine contraction remains OPEN [P2-A2], as do [P1-01], [P1-03], [P1-04]. The full R_mix341 lower bound and noncircular B3 remain OPEN. **P versus NP OPEN.**

**Sources:** [R1] Fortnow, Lipton, van Melkebeek, Viglas, JACM 52 (2005), Sec. 2.1, https://lance.fortnow.com/papers/files/tst.pdf ; [R2] Urquhart, JACM 34 (1987), DOI 10.1145/7531.8928; [R3] Ben-Sasson and Wigderson, JACM 48 (2001), DOI 10.1145/375827.375835.