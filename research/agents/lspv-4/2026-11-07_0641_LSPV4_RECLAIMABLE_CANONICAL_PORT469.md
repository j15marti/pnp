# LSPV-4/469: reclaimable canonical WORK-address roots, slot reuse and FLMV model firewall

**2026-11-07 06:41 PST | LSPV-4 Route A | PROVED/RESTRICTED abstract interner lemma | COMPUTATIONAL finite checks | native indexed-machine and universal SAT transformation OPEN.** Preserve all five agents, TWO Route A / THREE Route B, historical R_mix341/341 native weights and grammar, schedule and enabled states. P versus NP OPEN.

## IDEA -> SEARCH -> ITERATE and adversarial falsifiers

**Initial candidate:** repair LSPV-4/468's append-only canonical WORK-address root interner by reference counts, deterministic unique-table deletion, and **physical record-slot recycling**, keeping canonical equality among all *still-live* keys. Expected to eliminate the previously demonstrated $2^r$ historical-root accumulation for an $r$-bit Gray enumeration. This is a *secondary implementation alternative* to LSPV-2/469's direct native address packing, not a better proof of the global contraction.

Falsifiers stated before the source review: (F1) a reconstructed address reached by a different guest history receives a different key while its WORK value is still live; (F2) dropping an unreachable tree destroys a still-live shared subnode; (F3) recycling IDs makes a stale WORK alias or capacity-expansion mismatch; (F4) deallocating nodes without reusing their physical addresses still causes an unbounded WORK-tape high-water. An additional finite implementation falsifier emerged: the first candidate used JavaScript 32-bit shift-right for digit extraction, which wraps shift counts modulo 32 and caused an alias failure immediately after 64-to-128-bit-position expansion. Replaced it with `Math.floor(n/2**j)%2`; the published checker tests both capacity changes. The original unmodified append-only counterexample remains correct.

## Sources, prior work, and qualifications

Read full **proof1.txt** (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and current **proof2.txt**, especially [P1-01], [P1-03], [P1-04], [P1-S3], [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-B1], [P2-B2]. Read issue #3 and its recent LSPV-2/469, LSPV-1/476, LSPV-5/410, LSPV-4/468 comments; the five-role governing handoff, AGENTS.md, CODEX.md, and pnp-research SKILL.md. Read actual LSPV-4/468 (blob `0dcecfeb48393630088aa72b8b2cf0eedc5ee886`), LSPV-2/466 (blob `c2b17af05e1843bf88d25a7875f047f0f56817a1`), LSPV-2/468 (blob `784206b73b0b5a869375b69916d0ddd3cfe662b5`), LSPV-2/469 (blob `32f118a3a6999f414e0371a83bc8c413898d861b`), GROKPROOF/2026-11-07_1220_PROGRESS.md (blob `2c450bb3084c8a2065243305168d269442ace430`) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`). The older Claude result is a sequential access control, not a general random-access transfer.

Targeted source/repository review: FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 2005 §2.1, author PDF https://lance.fortnow.com/papers/files/tst.pdf (page 4 inspected; indexed head moves, erasure, maximum non-index work address accounting); Driscoll-Sarnak-Sleator-Tarjan, *Making Data Structures Persistent*, STOC 1986, DOI 10.1145/12130.12142 (persistence context, **not** a proof of this exact reference-count implementation); Urquhart 1987 and Ben-Sasson-Wigderson 2001 for ordinary Resolution hardness of odd-charge cubic expander Tseitin formulas; konard/p-vs-np README.md SHA `0e0ec77f` and proofs/complexity/README.md SHA `7ee9a11e` (different finite machine model, no SAT separation); blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA `18d693ea` and INDEPENDENT_AUDIT.md SHA `b30515cc` (promise and discovery caveats); meelgroup/frat-xor/format.md SHA `986a21aa` (distinct external proof grammar); MassimoLauria/cnfgen/cnfgen/families/tseitin.py SHA `4bb5fd19` (authentic Tseitin generator); openai/math/README.md SHA `cc5b0a03` (mixed formalization statuses). Public web search and the authenticated GitHub repository connector were used. A separately identifiable Google-branded search service was not available, and no official native FLMV test was executed.

## Restricted Lemma 469.1: finite-live-root reclamation

Fix a finite logical bit-position universe of size $U=2^d$, represented by a *canonical* binary radix DAG. A nonzero node at height $j$ has a unique key $(j,\ell,r)$ in a deterministic lookup table, with canonical zero subtrees. Every root held by the INDEX register, WORK-head register, or nonblank WORK dictionary is an explicit external reference. A node's reference count equals the number of live external-root and live-parent references. A point edit constructs and shares at most $O(d)$ new nodes. When an external root or parent edge disappears, recursively free any node whose reference count becomes zero and remove its unique-table entry. Add each freed **physical slot ID** to a free list and reuse slots before growing the arena.

**PROVED/RESTRICTED.** By induction on edits and reference-count changes, every live node's refcount remains positive, no live child is released prematurely, and for two *live* roots at the same capacity

$$
r(a)=r(b)\ \Longleftrightarrow\ a=b.
$$

All unreachable nodes are reclaimed, including unreachable historical Gray-code roots. Reusing an ID is safe because it had no live parent or external root when freed; the stale ID must not be used again. A WORK cell whose old key remains referenced cannot be spuriously aliased. When capacity doubles, wrap **each live root** with a canonical all-zero high half and rekey every live nonblank WORK entry; hold new roots before releasing old ones. A temporary at most constant-factor doubling in live roots and dictionary metadata is charged.

Let $H$ be the maximum number of sequential INDEX bit positions ever exposed, $S_W$ the maximum numerical WORK address read/indexed, $M$ the maximum number of simultaneously nonblank WORK cells, and $K$ the fixed number of live guest INDEX/WORK-head registers. With all zero subtrees canonical, each INDEX root uses $O(H)$ reachable nonzero nodes, while each bounded WORK address has at most $O(\log(S_W+2))$ nonzero bits and requires $O(\log(S_W+2)\log(H+2))$ radix nodes. Hence **the number of live radix records** is bounded by

$$
V=O\left(K(H+1)+(M+K)\log(S_W+2)\log(H+2)+\log^2(H+2)\right).
$$

Allow one extra logarithmic factor per record for explicit IDs, refcounts, free-list slots and balanced unique-table links. A deterministic balanced unique-table lookup is a *proposed paid implementation*, not a completed native FLMV interpreter. Cumulative reclamation time is charged to nodes previously created: a single release may take $\Theta(V)$ time, but total released nodes do not exceed total allocated nodes. Rebuilding/rekeying at capacity growth and all simultaneous ancestor/child buffers must also be counted. Therefore, **conditional on** $H$ and $M$ fitting the guest's *charged* space resource and on a paid native dictionary, this macro has a plausible $S_{\rm guest}\operatorname{polylog}(B+T+2)$ space envelope. That implication has **not** been established for the exact FLMV machine. In particular, FLMV's wording distinguishes work and index tapes; a conversion may not silently treat $H$ as charged unless proved.

Crucial physical distinction: *releasing a Map node alone is insufficient on an indexed machine.* A monotone physical slot allocator can reach $\Omega(2^r)$ high-water even when only $O(r)$ nodes are live. **The free-list reuse is mathematically necessary for this particular direct-address allocation strategy.** Slot recycling keeps physical record high-water at most the maximum simultaneous allocation requirement, not the total number of historical allocations. A full fixed-alphabet tape encoding and address/index movements remain unimplemented.

## Reproducible computational falsification and repair

Exact submitted V8 source: `experiments/arc/lspv4_469_refcount_recycling.cjs`. Raw output: `results/raw/arc/2026-11-07_0641_LSPV4_469_RECLAIMABLE_ROOTS_RAW.json`.

The complete deterministic checker passed **576,522** internal assertions with **29,038** radix-record creations and the same number of releases. Physical record IDs were reused: overall peak simultaneously allocated nodes and peak numeric slot ID were **378**. Without recycling, the earlier locally tested monotone-ID variant reached 29,038 assigned IDs on the same overall operation shape, despite 378 peak live records. This is a representation-specific high-water falsifier, not a native FLMV measurement.

| Gray index bits $r$ | Distinct historical addresses | Maximum live interned nodes | Maximum physical slot ID |
| ---: | ---: | ---: | ---: |
| 4 | 16 | 3 | 5 |
| 6 | 64 | 6 | 8 |
| 8 | 256 | 6 | 8 |
| 10 | 1024 | 9 | 12 |
| 12 | 4096 | 9 | 12 |

The checker also executed 1100 WORK dictionary alias operations with two capacity expansions, verified both direct and reconstructed address identities against an independent numerical oracle, and ended with zero unreleased roots. On K4, 16 signed proper 3-clauses yield 8 even-charge satisfying assignments and zero odd-charge models. A malformed duplicate-literal control was rejected. All finite observations are **COMPUTATIONAL**, not a proof of asymptotic hard-family size, FLMV timing or universal SAT hardness.

## Explicit resource ledger and scope of implication

* Logical node creation: 29,038 finite intern allocations, peak 378 live, with 576,522 assertions; these are **macro operations**, not weighted R_mix341 proof nodes.
* Physical evidence bits: dictionary records, keys, refcounts, target addresses, freelist, root registers, and the original 5,831-byte checked JS source must be charged when compiled. Raw output is a separately written fixed finite result; no inferred native byte bound.
* Construction and failed policies: root creation, failed lookups and reference-release cascades are counted abstractly; no universal decomposition policy, no guest source acquisition, no all-input compiled machine.
* Indexed reads/movement: `Map` does not implement native indexed tape moves. A future realization must pay bit-serial key comparisons, index construction/erasure, WORK-head restoration, overflow, simultaneous guest/native tape buffers, data retrieval and writes.
* Peak work space: temporary old/new roots during capacity doubling, the source interface, dictionary metadata, cache, output, proof certificates and all other phases must be simultaneous. Host heap measurements and number of live JS objects do not establish native FLMV work space.
* Time/space theorem: no new bound for $t'$ or $s'$ follows. LSPV-2/469's **alternative** native direct-coordinate scheme avoids this canonical interner entirely and may be more efficient. It also leaves the full INPUT-port and all-input contraction open.

The published hard-family control is cubic-expander odd-charge Tseitin strict 3-CNF: one variable per edge, four proper signed 3-clauses per degree-3 vertex, $4|V|$ clauses, $(3/2)|V|$ variables and encoded size $\Theta(|V|\log |V|)$. Urquhart and Ben-Sasson-Wigderson prove exponential **ordinary shared-DAG Resolution** size under bounded-degree expansion. GF(2) elimination is a polynomial shortcut, so neither a mixed R_mix341 nor arbitrary-machine lower bound follows. Haken PHP and Cook ER remain required shortcut controls.

## Tracker decision and exact remaining implication

The representation-specific material repair refines **[P2-A4]** only. The prior LSPV-4/468 append-only counterexample is *preserved* at its true scope, with a new live-reference/free-slot alternative. No change to [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A5], [P2-D1], [P2-B1], [P2-B2]. Root main.tex is not modified without complete authenticated current content, outside ownership-marker preservation and a safe SHA-guarded write. No historical R_mix341 rules or weights changed.

**Actual advance:** exact abstract reclamation invariant plus a high-water allocation falsifier and corrective slot-recycling mechanism. **Verification:** finite executable reference and symbolic restricted induction; native-matching bit costs OPEN. **Next missing implication:** a fully charged fixed-alphabet FLMV INPUT/WORK/INDEX implementation with guest-space-relative *all-phase* peak, followed by the uniform malformed-aware recursively iterable all-input SAT contraction [P2-A2]. **P versus NP remains OPEN.**
