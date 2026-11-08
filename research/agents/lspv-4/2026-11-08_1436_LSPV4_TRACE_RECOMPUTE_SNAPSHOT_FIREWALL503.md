# LSPV-4/503 | Trace recomputation versus sealed-source snapshots

**2026-11-08 14:36 PST | Route A | PROVED/RESTRICTED symbolic lemma + COMPUTATIONAL independent hosted tests | P versus NP OPEN**

**Proof-chain IDs:** new [P2-L4-503] under [P2-A4], refining [P2-L4-502] and LSPV-2/503; universal [P2-A2] and recursive [P2-A5] OPEN; companion [P1-01], [P1-03], [P1-04] OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. No changes to historical R_mix341 grammar or weights.

## IDEA and predeclared falsifiers

Hypothesis: The growing port array in LSPV-2/503 consists of write-once bits computable from immutable INPUT and can be **recomputed on readback** with $O(\log n)$ physical WORK, rather than materialized at $O(\sqrt n)$ WORK. Maintain the identical readback sequence, audit digest and final SAT/UNSAT/MALFORMED label, charging each indexed source reread and all phases.

F1: Find a SAT, UNSAT or malformed source (including $n=0,1$) where streamed readback or digest differs. F2: Prove that input indexing, recovering $n$ or $r$, INDEX erasure, or workspace clearing needs an uncharged polynomial-size buffer or super-$O(n+r\log n)$ time. F3: Assert the same low-space result for $r$ arbitrary independent values when the source is sealed and an adversary chooses the later read index. F4: Mistakenly promote wrapper optimization to smaller SAT children, universal $\Phi(B)$ or a native machine simulation.

## SEARCH: actual sources and authentication

Read complete original proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt initial blob d009a1aa5b2a6685a0e5d972e648d09c5349a286; current coordination issue #3 including peer LSPV-2/503, governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e514ddbd747150dcb68607013a3b2d154, AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef, and repo skill .codex/skills/pnp-research/SKILL.md. Direct peer: research/agents/lspv-2/2026-11-08_1416_LSPV2_GROWING_SPARSE_PORT_COMPILER503.md blob 944337e9e8b334d7bdf11dd96299fe5ea834c4a9 and actual executable experiments/arc/lspv2_503_multiport_sparse_compiler.cjs blob 28997e160442d005f10d28fd5967404450a15976. Predecessor research/agents/lspv-4/2026-11-08_1336_LSPV4_INDEXED_SPIKE_SPARSE_REPAIR502.md blob acac437441905dad52761631d979e8ba18f8781e. Actual Grok GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70 and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a were retrieved.

Primary: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822, https://lance.fortnow.com/papers/files/tst.pdf, section 2.1 **PDF page 4 screenshot inspected**. FLMV charges highest indexed WORK address and erases INDEX after indexed moves; their text already notes sparse normalization with polylog overhead, so no novelty asserted for general sparse storage. Literature on Resolution-hard expanders: Urquhart, *Hard Examples for Resolution* (1987); Ben-Sasson/Wigderson, *Short Proofs Are Narrow* (2001).

Required external repository checks on real files: konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3 formalizes a **different one-tape** machine model, no NP subset P theorem; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 restricts claims to named models. Source generator MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab, certificate format meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f, and actual costed program openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f44ad49370d1b812e862c03c3a91d7f836 were inspected. None supplies the missing arbitrary-decider FLMV transfer. Web search checked primary FLMV scope; no separate Google-branded interface was used. No external repository build or theorem checker was executed.

## ITERATE: three sharply different interfaces

**Theorem 503.1, typed input-reconstruction (PROVED/RESTRICTED).** Fix any deterministic total three-label SAT decider $B$ on all binary strings. In the exact typed private wrapper of LSPV-2/503, let $n=|x|$, $r=\lceil\sqrt{n+1}\rceil$, fixed integer $k\ge2$, $A=2^{k\lceil\log_2(n+1)\rceil}$. On a dedicated private WORK tape write once to $A+i$, for $0\le i<r$, the value

$$
v_i(x)=\begin{cases}
x_{i\bmod n}\oplus(i\bmod 2),&n>0,\\
i\bmod 2,&n=0.
\end{cases}
$$

The typed wrapper rereads ports in reverse, calculates an eight-bit digest, then invokes $B(x)$ on fresh disjoint tapes and returns exactly its SAT/UNSAT/MALFORMED output. Private tape and digest cannot influence $B$.

**Streaming repair:** Scan immutable read-only input and count $n$ with $O(\log(n+2))$ WORK; compute $r$ by an $O(r\log n)$ increment-and-square counter; iterate the reverse port order and use the REAL indexed INPUT head (with freshly constructed and erased INDEX) to recompute each $v_i(x)$, update the identical digest, then clear registers and invoke $B$ unchanged. Induction over each port read proves equality of all readback bits and digest. $n=0$ is a defined special case. Native finite-tape program construction is fixed and syntactically typed, not a semantic oracle. Source reads, INDEX erasure, counters, input scan, output, cleanup and $B$ are charged:

$$
T_{\mathrm{stream}}(n)=O(T_B(n)+n+r\log(n+2)),
\qquad
S_{\mathrm{stream}}(n)=O(\max\{S_B(n),\log(n+2)\}).
$$

This removes LSPV-2/503's $r$ physical private ports **under its precise write-once and immutable-source assumptions**. An arbitrary dynamic-address or source-changing program is outside the theorem. The original unchanged guest still incurs WORK high-water $\Theta((n+1)^k)$; only the *different compiled program* has small WORK.

**Theorem 503.2, output-only program equivalence.** If only the final three-label classification is observed, even the trace-streaming work is unnecessary: the entire private wrapper is dead and can be erased, leaving exactly $B(x)$ up to entry overhead. Hence synthetic expensive guest operations provide no implementation-independent computational lower bound. This does not improve the time or space exponent of $B$.

**Theorem 503.3, sealed-source snapshot lower bound (PROVED/RESTRICTED).** Consider a DIFFERENT interface: $r$ independently arbitrary written bits, no source access after writing, then an adversary selects any index $j$ and requires the saved $v_j$. The encoder must have $2^r$ distinguishable persistent configurations: distinct vectors differing at $j$ cannot share a configuration. Thus at least $r$ bits of configuration information are necessary. This is **not** automatically an FLMV WORK-space bound without accounting for finite control and head-position information, and does not apply to LSPV-2/503 because immutable INPUT remains readable and no adversarial read index is exposed. On a fixed-tape machine with input-head positions limited to a length-$n$ source, those positions can encode only $O(\log n)$ bits, so for $r=\Theta(\sqrt n)$ the information demand still cannot be hidden solely in such head positions.

## Established family and transfer ledger

The original graph Tseitin family on connected **cubic expanders** has $3H/2$ edge variables, four proper original signed 3-clauses per vertex and $4H$ clauses, with $\Theta(H\log H)$ dense binary source bits. Odd total charge certifies UNSAT by summing GF(2) equations. Urquhart 1987 and Ben-Sasson/Wigderson 2001 give exponential **ordinary shared-DAG Resolution** size lower bounds for appropriate expanding families, not R_mix341 or unrestricted computation. Existing shortcuts include linear algebra on the parity rows, shared reasoning and legal extension/learning. The finite control here is only K4, with $H=4$, six variables, 16 strict clauses, and exactly **208 source bits** (8-bit magic, 8-bit clause count and twelve 4-bit tokens per vertex). No reduction changes the 3-CNF; the wrapper only changes machine behavior. Required missing transfer: all-input source-agnostic children, correct $q=N^{3/5+o(1)}$ and $M=N^{1/2+o(1)}$ constraints, recursively iterable same-machine $\Phi(B)$, and full search/space charging.

## Full resource ledger

Original typed guest: $O(n)$ parser/length scan; $2r$ original far-WORK jumps with rebuilt/erased INDEX, one source-derived write per port and reverse readback; $r$ stored values and large physical WORK high-water $\Theta((n+1)^k)$; optional digest/audit; clean suffix $B$ with all construction/search/output phases retained. Trace-streaming compiler: *no* far-WORK jump, $O(n+r\log n)$ local time, $O(\log n)$ local peak WORK and INDEX, actual indexed input bit rereads, constant digest and charged cleanup; then same complete $B$ on fresh tapes. Output-only compiler: simply execute $B$ with zero wrapper overhead. The independent sealed-source query-interface must retain $\Omega(r)$ bits of distinguishable persistent information in its total configuration and cannot borrow the streaming bound. All three are sequential single paths, so work equals serial span up to fixed/polylog overhead; there are no inference DAG nodes, no proof evidence bits, no guest children, no cache sharing, no failed search policies or R_mix341 certificate. Any real recursive child system must charge ancestor/child simultaneous buffers and time/space schedules separately.

**Independent verification:** GitHub-published executable experiments/arc/lspv4_503_streaming_snapshot_control.cjs blob 35976b1801533932dbb8a9363577c77b04b2e29e was independently read back and evaluated in V8: 17,755 PASS assertions across 141 binary input controls, 16 original K4 charges (8 SAT, 8 UNSAT), 125 malformed/short, 5,133 port observations, 2,046 vectors and 16,398 restricted snapshot collision witnesses, 63 source-mutability negatives. A separately implemented Python checker passed 42,823 assertions on a different 143-input suite (8 SAT, 8 UNSAT, 127 malformed) and snapshot bit-flip witnesses through $r=11$. Its initial independent K4 clause-order mismatch was caught by unequal source SHA-256 and corrected before final run; final first/last hashes match existing peer original source: 29b451e68dfad057135bf8b41e8797d00517d10ccc66f51ed8e8486cea3c8dbc and ff26e171983f627405cb4207d312904f685ee99e7c1d639cc68450a3c60b6176. Raw results results/raw/arc/2026-11-08_1436_LSPV4_503_PORT_RECOMPUTE_SCOPE_RAW.json. **No native FLMV instruction-level interpreter or authoritative historical R_mix341 checker executed.** Hosted tests are semantic controls, not lower bounds.

**Actual advance:** tight scoped separation of output-only dead-code elimination, trace-preserving source recomputation, and genuinely information-carrying sealed-source snapshots. **Unresolved:** [P2-A2], [P2-A5], same-realization fully paid [P2-A4], and Route B [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2]. P versus NP OPEN.
