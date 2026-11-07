# LSPV-4/466: two-arena sparse INDEX snapshot with paid virtual INPUT-head semantics

**2026-11-07 04:36 PST | LSPV-4, Route A.** PROVED/RESTRICTED in an explicitly specified indexed-dictionary/transducer submodel; COMPUTATIONAL exact-original-source finite checks; CONDITIONAL machine embedding; OPEN complete FLMV interpreter, all-input recursively iterable SAT contraction, and P versus NP. No change to the existing two Route A / three Route B allocation or historical R_mix341 rules/weights.

## IDEA -> SEARCH -> ITERATE

**Hypothesis before searching:** The missing guest virtual INPUT port can freeze a possibly enormous indexed-input address without copying all its binary digits by swapping two *paid* sparse bit-index arenas: live guest INDEX and frozen INPUT-base. Keep a signed incremental displacement from the last indexed jump; compare the frozen indexed address with a polynomial-size threshold before ever materializing it. Clear the retired base using a live set of nonzero bits, charging each actual clear to a prior distinct 0-to-1 guest INDEX write. This component should avoid both repeated full INDEX scans and an unknown guest-exponent cutoff.

**Precise falsifiers:** (F1) q repeated indexed jumps to an exponentially distant address cause Omega(qS) host clearing time for only O(q) guest steps. (F2) a base address 2^S forces S binary digits to be copied or a free oracle to decide an INPUT read. (F3) a large indexed jump followed by ordinary left/right INPUT-head motions yields a false blank or mishandles zero clamping. (F4) AVL/sparse dictionary accesses, index-head realignment, retired-base clearing or simultaneous peak high-water cannot be implemented with the stated indexed-work resources.

**Search and result:** F1-F3 are defeated in the specified abstract model, with adversarial tests. F4 remains an explicit **native FLMV machine-compiler** obligation, not silently asserted. The result is a resource sublemma, NOT the missing universal SAT reduction.

## Theorem 466.1: dual-arena bit-snapshot lemma (PROVED/RESTRICTED)

Fix a guest with a sequential binary INPUT-INDEX tape and a one-way-infinite, read-only INPUT tape. A guest indexed INPUT jump sets the INPUT head to the nonnegative integer represented by the INDEX bits and erases those bits; the INDEX-head coordinate is preserved (or any alternative native convention must be separately simulated). Ordinary INPUT-head moves change that coordinate by plus/minus one, with attempted moves left from zero remaining at zero. Let B be the finite number of virtual INPUT bits. Accesses beyond B return blank.

For a T-step guest trace, let S be the maximum guest INPUT-INDEX-head position *ever visited* (also charged as writable INDEX-tape space). There is an abstract uniform transducer, independent of any guessed polynomial running-time or workspace exponent, that implements this INPUT/INDEX interface with:

$$
T_{\mathrm{port}}=O\!\left((T+1)\operatorname{polylog}(B+T+S+2)\right)+T_{\mathrm{underlying\ source}},
$$

$$
S_{\mathrm{port}}=O\!\left((S+1)\operatorname{polylog}(B+T+S+2)\right)
$$

bit-workspace and indexed-work high-water in the stipulated dictionary model, plus whatever separately charged original-source/guest-memory state is simultaneously live. $T_{\mathrm{underlying\ source}}$ charges actual indexed source-byte retrieval and virtual-header/suffix decoding, with at most O(polylog N) work per original-source bit in the authenticated, bit-compatible TREE3/PATH3 layouts. Source storage is read-only and NOT clandestinely cloned.

**Representation.** Maintain two mutable deterministic balanced ordered sets I and J of positions whose current INDEX bits equal one. The first represents the live guest INDEX; the second is the frozen nonnegative integer $a=\sum_{j\in J}2^j$ established at the last jump. Both physical bit tapes are work-tape-backed, not free read-only extra input. The guest INPUT head is represented as $a+\delta$, where the signed displacement $\delta$ has magnitude at most T since the last jump. Maintain the guest INDEX-head coordinate $j$ separately, using $O(\log(T+2))$ controller bits. Any guest INDEX write inserts/deletes the current position in I; sequential INDEX-head moves update j.

**Indexed jump.** Erase all nonzero bits of *retired* J by enumerating J on its physically writable tape; each deletion has a paid indexed-work access. Then exchange the identities I,J (no copying of I), reset $\delta=0$, and use a paid indexed-work move to place the physical new-live-INDEX head at guest j. The newly live I is now empty. The old live INDEX bit structure becomes the frozen base. This remains valid if j is very large, because the host stores only a $O(\log(j+2))$-bit address and visits a physical WORK cell at coordinate $O(j\operatorname{polylog}T)$; guest INDEX high-water already includes j. No huge work-coordinate is free.

**Crucial amortization.** Let U count guest live-INDEX transitions from bit zero to one. Each bit cleared from a retired frozen arena originated in a *unique* earlier zero-to-one transition of the epoch that created that base, and is cleared only once before that arena is reused. Therefore

$$
\boxed{\sum_{\mathrm{jumps}}|\mathrm{retired\ base\ one\ positions}|\le U\le T.}
$$

A guest that keeps its INDEX head at position S and performs q one-bit indexed jumps costs O(q polylog(T+S)) for retired-bit clearing after the initial paid journey to S, NOT qS. No dense INDEX sweep, full copy or uncharged generation tag is required. In particular, this avoids the unknown-exponent epoch-width concern for repeated *within-guest INPUT jumps*. The earlier LSPV-2/466 native WORK-index epoch lemma is a different component.

**Correct virtual read and head motion.** Let $C=B+|\delta|+2$ and $\ell=\lfloor\log_2C\rfloor+1$. Query the largest position $m$ in the frozen set J. If $m\ge\ell$, then $a\ge2^m>C$, so $a+\delta>B$ and every virtual read is blank, and a single left move cannot encounter zero. Otherwise $a<2^\ell$ and its entire numerical value can be assembled from at most $\ell$ low set-bit positions using O(polylog(B+T+S)) indexed dictionary steps and $O(\log(B+T))$ register bits; the exact position $a+\delta$ is then used for the virtual read or left-boundary test. This handles huge frozen address values without constructing a huge numeric head register. On an INPUT-head LEFT at zero, leave $\delta$ unchanged. On RIGHT, increment it. A new INDEX jump replaces a and resets $\delta$.

**Proof.** The INDEX representation is maintained by direct AVL insert/delete; the frozen one-set is immutable until retirement. The jump exchange establishes $a$ exactly while restoring a blank live INDEX. The amortization inequality above bounds all physical retirement clears. Every subsequent sequential INPUT-head motion changes $\delta$ exactly, except correctly clamped LEFT. The threshold test is sound because a high set bit makes $a>B+|\delta|$; otherwise full low evaluation is exact. An AVL dictionary has O(log(S+2)) search/update and O(S+1) stored keys. With O(log(B+T+S)) bits per stored key/pointer/node and per indexed work-coordinate, the stated time/space bounds follow for the explicitly assumed paid indexed dictionary operations. The number of physical data/index tapes is constant. QED *in this transducer submodel*.

**Native qualification:** A complete instruction-level compilation of balanced-tree lookup, dense contiguous node allocation/free lists, cross-tape head repositioning, guest simultaneous transitions, initial input-head conventions, guest source-port conversion, output, work-tape reset and full host high-water has NOT been carried out. Therefore the display is **not** a fully proved native FLMV same-machine lemma and cannot be substituted into [P2-A2] without these simulations. In a native representation the bit sets and balanced-tree pointers must occupy *charged WORK*, with all indexed probes and release costs paid. The ability to read a remote source bit is not a free SAT oracle.

## Resource ledger and predecessor comparison

| Component | Charge / condition |
| --- | --- |
| Guest INDEX sequential moves/writes | Each guest action plus O(polylog(T+S)) balanced-set, head counter and tape-location work |
| Frozen INPUT base | Original binary set of one-bit positions, physically on paid WORK; no cloned $2^S$ address |
| Within-guest indexed INPUT jump | Paid new INDEX work-head relocation, O(polylog(T+S)) metadata, plus retired base enumeration |
| Retirement clears | Total <= U <= T, O(T polylog(T+S)) work, including references and dictionary updates |
| Ordinary virtual INPUT left/right | Delta update and zero-clamp test, O(polylog(B+T+S)) |
| Virtual INPUT read | Threshold/highest-set-bit test; source/header/suffix bit retrieval only when within B |
| All-phase peak space | Two simultaneous one-bit sets, balanced-tree cells/pointers, tape heads and delta: O((S+1)polylog(B+T+S)); other guest/frontier state additive |
| Physical machine and conversions | Explicit native encoding/check and fixed-alphabet transition simulation still OPEN |
| Output/guest WORK/program control | NOT paid by this isolated theorem; full transformer remains OPEN |
| Failed source policies, preprocessing, guest calls | Must be separately charged for any Route A contraction |
| Distinct logical proof nodes/work/span | Not applicable to this INPUT-port subroutine; fixed R_mix341 untouched |

Relative to LSPV-4/463 and LSPV-2/465, this approach needs no preselected high-digit cutoff and no periodic reclassification of high one-bit positions: it relies on a frozen ordered set and the displacement comparison. Relative to LSPV-2/467, it does **not** misclassify the writable guest INDEX tape as free space. That report correctly retired such a purported separation. It complements, rather than subsumes, the restricted native WORK-index packing of LSPV-2/466 and the static block-source address checkpoints of LSPV-4/465.

## Finite independent controls (COMPUTATIONAL)

Exact published JavaScript source at experiments/arc/lspv4_466_dual_arena_input_port.cjs (blob 856e807f2a9085fe85db7f3a4ec631f686ef4dc1) was retrieved through the GitHub connector and independently executed in V8. Its AVL-key-set simulator is cross-checked after each operation against a *separate* unbounded BigInt reference that directly reconstructs the address, with original virtual source bits. The two implementations do not share the representation of the INPUT head.

Results: **144,970 assertions PASS**; 140 generated traces, 30,800 counted decisions (plus explicitly simulated guest INDEX-head walks within those decisions), 4,126 indexed INPUT jumps, 3,637 guest INDEX zero-to-one insertions, **2,787 paid retired-bit clears**, maximum visited guest INDEX position 512, and 11,587 out-of-source blank-read cases. Repeated 800 high-bit jumps after a paid 512-step initial INDEX-head walk yield **799** retired-bit clears rather than 800*512.

Original strict signed K4 Tseitin parity 3-CNF controls use six edge variables and 16 proper ternary clauses, four forbidden parity-assignment clauses at each vertex; all 64 assignments were exhaustively checked for even charge (8 SAT assignments) and odd charge (0 SAT assignments). Source corruption tests reject a truncated original bitstream and a literal with variable ID zero. These labels are finite source controls, not proof-size hardness certificates. The finite test runs in a host language, not on an actual FLMV machine.

Raw results: results/raw/arc/2026-11-07_0436_LSPV4_466_DUAL_ARENA_RESULTS.json (Git blob 5a8fd9913761efadba5c17b0317c618eb709dcc8).

## IDEA -> SEARCH -> ITERATE source ledger and controls

- **Primary theorem/model:** Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, Section 2.1. Author PDF https://lance.fortnow.com/papers/files/tst.pdf page 4 was visually checked. Its read-only INPUT has an associated sequential writable INDEX tape; indexed moves erase the INDEX contents; physical WORK high-water can be exponentially large. The paper does not separately fix all head-convention details required by this submodel. Do not infer all-machine contraction.
- **Established hard-family control:** Odd-charge cubic-expander Tseitin **original strict 3-CNF**, one edge variable per edge, exactly four ternary clauses per degree-3 vertex, $H$ vertices, $3H/2$ variables, $4H$ clauses and $N=\Theta(H\log H)$ in binary literal-ID encoding. Ordinary shared-DAG Resolution has exponential proof-size on suitable expanders by known width/expansion theorems (Urquhart 1987; Ben-Sasson/Wigderson 2001). GF(2) elimination sums the parity charges efficiently; no full mixed-R lower bound or unrestricted SAT-time bound transfers.
- **Project:** Actual complete proof1.txt and proof2.txt fetched during this run, [P1-01], [P1-03], [P1-04], [P1-S3], [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-B1], [P2-B2]; current issue #3 including LSPV-2/467, LSPV-3/472 and LSPV-1/473. Governing November 2 five-role handoff, AGENTS.md, CODEX.md, pnp-research skill, LSPV-4/465, LSPV-2/465-467 read. GROKPROOF/2026-11-07_1220_PROGRESS.md actually read (scope barrier); actual Claude file research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex read (sequential-access crossing sequences do not transfer to indexed FLMV). No authority inferred from these documents.
- **New required external repositories:** konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3 specifies a different finite one-tape formal model, no FLMV port; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 gives restricted method ledger, no unrestricted time-space transducer.
- **Rotating external corpus:** meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1 is a distinct FRAT-XOR/XLRUP proof grammar; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae catalogs heterogeneous proof-status manuscripts. Neither establishes a native FLMV compiler. General web/ACM/author PDF search and GitHub source connector used. No separate Google-branded search service was verified.
- **General data structure precedent:** deterministic AVL search/insertion/deletion and two live ordered sets are standard. This is not presented as novel data-structure literature, nor as an unrestricted algorithm theorem.

## Tracker and manuscript status

Relevant material support is the restricted input-port resource sublemma under **[P2-A4]**, dependent on still OPEN **[P2-A2]** (all inputs) and **[P2-A5]** (recursive closure). Other open nodes remain unchanged, including [P1-01], [P1-03], [P1-04], historical [P2-D1] and noncircular B3 [P2-B2]. Record tracker blob/readback separately in the five-role handoff. Root main.tex must not be changed absent complete readable contents and LSPV-4 marker-safe verification.

**Actual advance:** Correct abstract virtual INPUT-head and INPUT-INDEX semantics with q-jump sparse reclamation amortized by real guest writes, without a guessed exponent or huge numeric input-head register. **Verification:** mathematical invariant and independently executed finite V8/BigInt controls; NOT native FLMV implementation. **Remaining gap:** native end-to-end port interpreter, together with uniform ALL-INPUT recursively iterable source decomposition and full time/space accounting. **P versus NP OPEN.**
