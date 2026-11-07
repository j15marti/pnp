% LSPV-4 REPORT::458::2026-11-06T21:36:00-08:00
# LSPV-4/458: Indexed high-water padding, paid epoch reset, and TREE offset firewall

**2026-11-06 21:36 PST | Route A | PROVED/RESTRICTED machine-resource falsifier; COMPUTATIONAL finite controls | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE

Initial hypothesis H0: dense erasure of all guest work-tape positions through the high-water mark can be charged to the guest's own runtime, rendering epoch-tagged resets optional. Falsifiers: (F1) a legal indexed guest accesses a very high position in logarithmic time; (F2) a reused cell leaks across calls; (F3) the epoch scheme creates unaccounted time/space or head/index-tape costs; (F4) the newest TT3-460 balanced-tree offset table blocks inheritance of PATH3-456's smaller local-space bound.

**SEARCH/REVISION:** FLMV (2005), §2.1, PDF page index 3, explicitly defines work space through the largest indexed position ever read and permits space much larger than time; the paper discusses a separate sparse-data-structure simulation to normalize this. Its Corollary 5.8, PDF page index 17, proves an `o(n^beta(c))` exclusion on the specified machine, not any contraction. Thus H0 is false without a separate simulation lemma.

## Theorem 458.A: a conditional correct guest defeating dense clearing

Assume a uniform total correct polynomial-time SAT decider `A0` on the FLMV machine, with guest runtime `O(B^t)`; this is the **conditional SAT-in-P premise**, not a proved general algorithm. Fix integer `b>t` and greater than any given polynomial-space exponent of `A0`. Define `A_b`: recover input length `B` by paid indexed end-of-input probes (or an `O(B)` scan absorbed by `t>=1`), then write the binary index for `B^b` in `polylog B` additional time (fixed `b`), jump to that work-tape cell, READ then write a marker, then run `A0` and return precisely its result, including malformed inputs. This machine is still uniform, total, correct, and polynomial time, but has indexed work-tape high-water `Omega(B^b)`.

A wrapper that fully clears cells 0 through the high-water mark after every guest call spends `Omega(B^b)` erasure steps, not `O(B^t)`. With `q=N^(3/5+o(1))` calls and `B=N^(1/2+o(1))`, its dense-erase work can be `Omega(N^(3/5+b/2-o(1)))`, exceeding the proposed exponent `max(1,3/5+t/2)`. **PROVED/RESTRICTED:** this refutes **dense-eager-reset accounting only**, not all guest simulations or all-input SAT contraction.

## Lemma 458.B: fully paid epoch reset at polynomial high-water

With `q=poly(N)` calls, choose `r=ceil(log2(q+1))` bits. For every guest work/index-tape cell `i` encode its data and an `r`-bit call epoch at physical positions around `(r+1)i` on fixed-alphabet tapes. Every call advances the epoch; an old-tagged cell reads as a blank. Every read, write, sequential head move, indexed jump and index-tape erasure is emulated, charging physical address arithmetic and tag access. A new call resets the guest finite control, virtual input-index state, and output disposition. Input-bit fetches must use the *current* auxiliary/pin region and never a stale cache.

An induction over all simulated steps proves the guest sees a fresh blank work configuration. If the guest high-water is polynomial and the virtual-input provider answers in `polylog N` paid time, tag lookup and address conversion cost `polylog N` per guest step. Physical high-water is `O((S_A(B)+1)log N)` plus metadata. Hence under these explicit restrictions:

$$
T_{guest}=O(q T_A(B)\operatorname{polylog}N),\qquad S_{guest}=O((S_A(B)+1)\log N+\operatorname{polylog}N).
$$

This is a symbolic **PROVED/RESTRICTED reset representation**, not an executed instruction-level FLMV wrapper or a free source-bit converter. The fixed physical alphabet is preserved; the extra epoch bits are stored in ordinary tape cells.

## New TREE-vs-PATH composition firewall

Under aligned PATH3-456, generated boundary metadata is `N^(1/10+o(1))` bits; with `B<=N^(1/2+o(1))` and `q<=N^(3/5+o(1))`, the existing *restricted conditional* lazy-guest resource profile is

$$
t'\le\max(1,3/5+t/2),\qquad s'\le\max(1/10,s/2).
$$

However, LSPV-2/460's distinct **tagged TREE** source parser retains one complete source-bit offset for each of `h` tree blocks: `Theta(h log N)` writable bits. In a legal limiting regime `h=Theta(sqrt(N/log N))`, this is `Theta(sqrt(N log N))=N^(1/2+o(1))`. Thus merely borrowing the PATH lazy guest-input port into the **specific full-offset-table TREE implementation** cannot justify local space `N^(1/10)`. Its proved/conditional claim remains `s'<=max(1/2,s/2)` until an alternative paid offset-acquisition scheme is proved. This is **not** an all-tree algorithm lower bound.

The result is a material *scope and resource-composition gap* for [P2-A4], not closure of [P2-A2] or [P2-A5]. [P1-S3] already distinguishes the two restricted source languages and remains unchanged.

## Independent finite controls and limitations

Original signed **strict 3-CNF** K4 and cube Tseitin instances, each with even/odd vertex charges: 4 sources, 16/32 clauses, 6/12 variables. Odd charge algebraically certifies UNSAT; even-charge connected graph is SAT. The test guest exhaustively checked both labels and pinned-edge cofactors. Each of eight sequential guest calls touched indexed high work position `B^6`. Naive persistent storage returned a nonblank instead of an initially blank cell in **28/28 subsequent calls**; the epoch emulator returned blank on every one of 32 starts. Independently executed Python **201 assertions PASS**, independent JavaScript **140 checks PASS**. Host dictionary simulations are **COMPUTATIONAL controls only**, not FLMV machine-time measurements, nor asymptotic hardness certificates. Exact source hashes, high-water values, and tests are in the reproducibility archive and raw JSON.

## Sources / actual inspected files

Primary: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), 835-865, DOI 10.1145/1101821.1101822; original https://lance.fortnow.com/papers/files/tst.pdf §2.1 and Cor. 5.8, **page screenshots inspected**. Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209-219, DOI 10.1145/7531.8928, only ordinary Resolution expander-Tseitin hardness; GF(2) polynomial shortcut remains mandatory.

Project: live `proof1.txt` blob `006eeeb51fa0440abcdd55ddf86e8059933f8c70` ([P1-S3], [P1-04]) and `proof2.txt` blob `6e2796ac48b2f9ff04ef8a87dc47f0430be7d3c9` ([P2-A2], [P2-A4], [P2-A5]), current issue #3, governing Nov.2 handoff, `AGENTS.md`, `CODEX.md`, project skill, LSPV-4/456 blob `6bb951c015b601159972a9d498c2df195f6e5f2e`, /457 blob `e01aeebcdac46d4e8892545bd99662b81d219648`, LSPV-2/460 blob `5a5d43dd8716f53c6ef2843138b3421fd61fb025`, Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md` blob `a20fb8b3640d7574faf238a4a83a021bb0984808`, Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`. A newer Claude file discussed on issue #3 is on a separate branch; its contents were not claimed to have been reviewed.

External actual files: `konard/p-vs-np/proofs/complexity/README.md` blob `7ee9a11e` (different one-tape model); `blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md` blob `4aba9d94` (fixed-width problem); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd19`; `meelgroup/frat-xor/format.md` blob `986a21aa`; `openai/math/README.md` blob `cc5b0a03`. Their claims do not supply the unrestricted transfer. Native FLMV profiler and Google-branded search unavailable; standard web literature search and exact project source reads were performed.

**Accounting:** logic nodes, inference bits and ideal shared-DAG work are distinct from executable guest time. All source/index/head reads, parsing, malformed-input rejects, guest restarts, failed branches, output, cache invalidation, virtual child provider, reference and all-phase peak workspace must be charged. No alteration to historical R_mix341 rules/weights or agent tasks. Exact OR/AND and assumption-scope obligations remain with Route B.

**Advance:** a conditional high-water guest falsifier for dense reset; a restricted, charged epoch repair; and a new implementation-specific TREE/PATH offset-composition firewall. **Remaining gap:** source-agnostic all-input, recursively iterable same-machine contraction [P2-A2], [P2-A5] is OPEN; B3 is OPEN. **P versus NP OPEN.**
