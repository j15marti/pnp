# LSPV-4/461: Sparse dirty-address reset for indexed guest work tapes
2026-11-06 23:37 PST. Route A. PROVED/RESTRICTED trace lemma; COMPUTATIONAL finite checks; native full interpreter OPEN. P versus NP OPEN.

## IDEA -> SEARCH -> ITERATE
Hypothesis: use a mirrored MARK tape plus a deduplicated dirty-address log to reset each guest invocation without erasing all addresses through the indexed high-water mark.

Falsifiers: (F1) one jump to 2^j forces 2^j reset operations; (F2) repeated accesses duplicate dirty entries; (F3) arbitrary long guest work-index strings cannot be decoded/mirrored with the charged time and workspace; (F4) stale work data persists between invocations.

Project reads: BOTH root trackers, especially [P1-S3],[P1-01],[P1-03],[P1-04],[P2-A2],[P2-A4],[P2-A5], issue #3, AGENTS.md, CODEX.md, research skill, five-role handoff, LSPV-2/461 and LSPV-4/458,/460. Actual Grok progress: GROKPROOF/2026-11-06_2316_PROGRESS.md (blob a20fb8b3640d7574faf238a4a83a021bb0984808); Claude world ledger README (blob de75a371ce3143a4495e6892df7fb04794a6b708). Primary FLMV (Fortnow et al., JACM 2005, Sec 2.1 and author preprint PDF p. 4) explicitly counts maximum indexed work-tape position, permits exponential space in time, and mentions sparse touched-cell representations with polylog time overhead. This is an independently checked reset construction, not an asserted new all-computation theorem.

External repository review: konard/p-vs-np README blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and proofs/complexity/README blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3 use a different finite one-tape model. blkph0x/p-vs-np-proof-research README blob f397a7747eaca82df3d754d0a4b4bab1fe10f814 and METHOD_INDEX blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 document bounded/promise results. meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f checks a different proof format. cslib-community/complexitylib README blob 365a60d105411e5223d158a69d1532f967241d61 and openai/math README blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae did not supply a native FLMV compiler. Targeted web searches on indexed work address, index tapes and sparse machine simulation completed; no direct Google service or native FLMV execution.

## Theorem 461.A, explicit assumptions (PROVED/RESTRICTED)
A deterministic guest trace has T steps, fixed d work tapes, M distinct actually touched (tape,address) pairs, and greatest work address S. Assume guest work-index addresses and mirrored indexed jumps can be implemented with paid polylog N time/scratch per operation, including arbitrary binary address normalization; S is polynomial in N. This last work-index mirroring assumption is NOT yet established for arbitrary FLMV guest programs.

For each guest work tape use DATA and MARK physical work tapes with separate mirrored native index tapes. On first touch of address i, set MARK(i)=1 and append (tapeID,i) to a contiguous dirty log. A revisit sees MARK(i)=1 and does not append. At return, visit the M logged addresses by native index, blank DATA and clear MARK, and discard the log. Fresh guest blank semantics follows by induction across all calls.

$$
M\le d(T+1), \quad M\le d(S+1).
$$

Exactly M DATA and M MARK clearing writes are needed, instead of Theta(S) dense erase. The log contains O(M log(S+2)) explicit bits; simultaneous DATA+MARK+LOG peak high-water is

$$
O(S+M\log(S+2)+\operatorname{polylog}N)
=O((S+1)\operatorname{polylog}N).
$$

Under the stated work-address/mirroring premise, total guest work plus reset is O((T+M) polylog N) = O(T polylog N). The fixed number of physical tapes is 2d+O(1), independent of N. A jump to 2^40 adds one dirty address, not 2^40 clear operations. All address serialization, work-index read, index-head movement, output and simultaneous buffers remain charged.

**Crucial limitation:** the prior LSPV-4/460 virtual INPUT-index high/low summary does not automatically implement an arbitrary guest WORK-index tape decoder, including very long zero-padded indices. A complete instruction-level same-FLMV-machine transcript, mirror and address extraction with these bounds is OPEN. This trace-level lemma offers an alternative to LSPV-4/458 epoch tags, not a finished guest interpreter.

## Restricted Route A and known hard controls
For the preselected authenticated bit-aligned POSTORDER TREE3 grammar of LSPV-2/461 and LSPV-4/460, with h,Lmax<=N^(1/2+o(1)), 2^w<=N^(1/10+o(1)), q<=N^(3/5+o(1)), B<=N^(1/2+o(1)), **conditional on** fully charged source validation, virtual ports and guest interpreter, the restricted resource profile remains

$$
t'\le\max\{1,3/5+t/2\}, \qquad
s'\le\max\{1/10,s/2\}.
$$

Original source/index/head reads, preprocessing, failed calls, child virtual header/blocker construction, guest simulation, MARK/DATA/log space, reset, output and caches are charged. No native R_mix341 inference certificate was generated; fixed historical grammar/weights remain unchanged. Calling A directly on off-promise input length N adds N^t and defeats contraction for t>6/5. Source-independent fallbacks and recursive closure remain OPEN.

Known family: odd-charge Tseitin on a cubic edge expander with H vertices, 3H/2 edge variables, and 4H original strict 3-CNF clauses excluding wrong local parity tuples. Encoded length Theta(H log H) under dense binary IDs. Odd charge sum certifies UNSAT over GF(2). Suitable growing expanders require 2^Omega(H) ordinary shared-DAG Resolution proof size (Urquhart 1987; Ben-Sasson and Wigderson 2001). A polynomial GF(2) sum is a legal shortcut in other systems; neither unrestricted algorithm hardness nor a full R_mix341 lower bound follows.

## Finite experiment
Python producer in reproducibility archive: 300 independent calls of 140 abstract indexed work operations each; 18,773 assertions, 16,763 cross-checked reads, 3,255 deduplicated cleared entries, max work address 1,099,511,627,779, at most 17 entries per call, and 100 explicit stale-data negative controls. Published independent pure JavaScript checker: 300 sessions, 11,660 assertions, 10,544 read checks, 6,993 deduplicated clears, max 33 entries per call. Original signed K4 and cube Tseitin controls: 4 cases (2 SAT, 2 UNSAT) plus malformed zero-literal cases. Small graphs are semantic controls, NOT certified asymptotically hard instances. Host Map/dictionary operation counts are NOT native FLMV running time, writable space or proof-size lower bounds.

## Disposition and sources
Actual advance: a distinct-address charged, rigorous trace-level indexed reset alternative and a precise residual work-index conversion obligation. Verified: symbolic lemma and independently executed host checks. Published: this report and standalone checker. Proof1 [P1-S3] reviewed with no change; proof2 [P2-A4] restricted evidence only; [P2-A2],[P2-A5],[P1-01],[P1-03],[P1-04],[P2-D1],[P2-B1],[P2-B2] OPEN. P versus NP OPEN.

References: [R1] Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, J ACM 52(6) (2005), https://lance.fortnow.com/papers/files/tst.pdf, doi 10.1145/1101821.1101822. [R2] Urquhart, Hard Examples for Resolution, J ACM 34(1) (1987). [R3] Ben-Sasson and Wigderson, Short Proofs Are Narrow, J ACM 48(2) (2001).
