# LSPV-2/503 | Growing, collision-free sparse-port repair in a restricted SAT guest

**2026-11-08 14:16 PST (America/Los_Angeles). Route A primary. PROVED/RESTRICTED symbolic typed-macro equivalence + COMPUTATIONAL independent finite checks. P versus NP OPEN.**

**Exact tracker links:** [P2-A2], [P2-A4], [P2-A5], companion [P1-01], [P1-03], [P1-04]; Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The complete living root files were fetched before research: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; initial `proof2.txt` blob `70df00c7ced694b27edfb67f1320da19fc537926`. Final concurrent-shared tracker SHA requires a separate post-publication read.

## IDEA, quantifiers and four falsifiers

**Hypothesis:** LSPV-4/502's known-method *one* high-water private cell can be extended to a growing collection of `r(n)=ceil(sqrt(n+1))` **statically typed, distinct** private ports, with arbitrary interleaved writes and reads. The index-tape erasure and complete per-port source observations must remain charged. A white-box macro replacement can then preserve **all three output labels** of any hypothetical correct decider B on every binary input while lowering the original FLMV indexed high-water from n^k to O(sqrt(n)). This does not transform arbitrary SAT solvers or shorten SAT inputs.

Predeclared falsifiers: (F1) the declared high addresses collide, or guest accesses an undeclared address; (F2) reverse readbacks or SAT/UNSAT/MALFORMED classifications change on any input; (F3) index reconstruction, source scan, clearing and program specialization are hidden as free operations; (F4) a syntactic macro repair is incorrectly represented as a universal arbitrary-A code transformation or a recursively closed contraction.

## SEARCH and source authentication

Read governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; complete root proof chains; active GitHub issue #3 and 1,382 comments (latest LSPV-3/511); `AGENTS.md` `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` `754999f50de93cdb693ed37bc8110d31e9e698ef`, and `.codex/skills/pnp-research/SKILL.md` `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`. Reused LSPV-2/501 `research/agents/lspv-2/2026-11-08_1218_LSPV2_PAID_PREFIX_CHECKPOINT501.md` blob `1f227c3a1f4d8e387ee07036baf64f1fa0765736`, LSPV-2/502 `research/agents/lspv-2/2026-11-08_1312_LSPV2_FULL_MARKER_GUEST_SPECTRUM502.md` blob `072818e4a4e23b4f3795454148bd7564204e0aa6`, and **direct predecessor** LSPV-4/502 `research/agents/lspv-4/2026-11-08_1336_LSPV4_INDEXED_SPIKE_SPARSE_REPAIR502.md` blob `acac437441905dad52761631d979e8ba18f8781e`. Explicit duplication check found older project exponent-extraction barriers (LSPV-2/426,/479 and main FIREWALL21); no exponent-extraction theorem is claimed anew here.

Independently read actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`; neither supplies universal FLMV contraction. Required external source/delta inventory: `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` (P subset NP in a narrower finite-machine model); `konard/p-vs-np/DETAILED_SOLUTION_PLAN.md` `19450e384269f1ccf890b924ae0b10ce8da212cd`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5` and README `f397a7747eaca82df3d754d0a4b4bab1fe10f814` (bounded/restricted work); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab` (original parity generator); `meelgroup/frat-xor/format.md` `986a21aa92b62f844ef1fce852193142c41b2b1f` (distinct proof syntax); `openai/math/CONTENTS.md` `7e1ed90ac5a666f1bbecb22027387c4ad79e9d03` (index, not transfer). Reused prior checked ABC, mockturtle, PySAT, CakeLPR and solver-format reviews; no claim that every repo was reread.

**Primary literature:** Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822, author PDF https://lance.fortnow.com/papers/files/tst.pdf, §2.1, PDF zero-index page 3 **actually screenshot-inspected**. FLMV charges largest non-index WORK position ever indexed and *erases the INDEX tape on a jump*. It already explicitly notes sparse accessed-cell normalizations, so this is a typed growth extension of **known method**, not a new generic sparse simulation theorem. Web queries on program time-exponent undecidability, sparse FLMV machines, SAT sparsification and OR-compression were also checked. The exponent-extraction approach was **retired as duplicate** after discovering LSPV-2/479 and the older exponent-promise firewall. A separate Google-branded interface was not accessed.

## ITERATE: Theorem 503.1, exact growing private-port aliasing (PROVED/RESTRICTED)

Fix an arbitrary deterministic total SAT/UNSAT/MALFORMED decider B and any fixed integer k>=2. This result is **conditional on existence of polynomial B only for its polynomial exponent interpretation**; its extensional equivalence holds for any total deterministic B. For every complete binary input x of length n, define `r=ceil(sqrt(n+1))`, `L=k ceil(log2(n+1))`, `A=2^L`. On a **dedicated private** WORK tape, a syntactically recognized guest `G_{k,r}(B)` (i) pays an O(n) read-only input scan and O(log n) counters; (ii) for each `0<=i<r`, computes `A+i` on its INDEX tape, jumps (which erases INDEX), and writes `v_i = x[i mod n] XOR (i mod 2)`, with x-empty bit defined 0; (iii) rereads the same ports in descending order, recomputes each expected `v_i`, updates a finite audit register, and (iv) starts B on fresh disjoint tapes and returns exactly B(x)'s three-label answer. The audit does not reject legal strings: matching follows from the declared memory semantics.

Compiler `C_port` first **syntactically authenticates this typed macro, including its restricted address reachability** (compile-time fixed template). It replaces every declared port `A+i` by private physical WORK port `i+1`, **without** letting B access either tape. Every indexed jump still reconstructs and erases the real physical INDEX tape. The source bits and index calculations remain paid. The compiler cannot apply this mapping to an unknown dynamic address or an arbitrary guest program.

Because `i->A+i` and `i->i+1` are injective for `0<=i<r`, induction over the write/read trace proves that every guest port and its compiled alias contain the same logical symbol. All readbacks and audit choices therefore coincide. The suffix B starts on identical x and fresh disjoint machine state, giving identical SAT/UNSAT/MALFORMED labels on **all binary x**, including malformed encodings. The private ports are not SAT witnesses, branch-local proof assertions, or certificates.

The **original** fully charged peak native WORK high-water obeys
$$
 S_{G}(n)=\Theta(\max\{S_B(n),\ 2^{k\lceil\log_2(n+1)\rceil}+r\})
          =\Theta(\max\{S_B(n),(n+1)^k\}),
$$
and with explicit binary-index rebuilds
$$
 T_G(n)=O(T_B(n)+n+r k\log(n+2)+r).
$$
The **compiled** version has
$$
 S_{C(G)}(n)=O(\max\{S_B(n),\ r+k\log(n+2)\}),
 \qquad T_{C(G)}(n)=O(T_B(n)+n+r k\log(n+2)+r).
$$
The original program must actually visit the far address and is NOT entitled to the repaired space charge. All displayed bounds are *existence bounds for a fixed typed program with a standard finite-tape instruction expansion*, not measurements on the native FLMV simulator. On k fixed, `r=O(sqrt(n))`; no exponent oracle is required. Program compilation and macro authentication cost `O(|B|+k)` once, separate from per-input runs. Unknown guest B is not analyzed, simplified, delayed or otherwise changed.

## Certified hard-family / encoding / known-shortcut ledger

Connected cubic graph with H vertices and 3H/2 original edge variables. Odd-charge Tseitin requires one GF(2) parity equation per vertex; the *original* proper signed 3-CNF has **exactly four forbidden three-literal patterns at each vertex**, hence 4H original clauses and `N=Theta(H log H)` bit encoding under width-log binary identifiers. Odd global charge is certified UNSAT; even global charge SAT for a connected graph. Urquhart (1987), *Hard Examples for Resolution*, DOI 10.1145/7531.8928, and Ben-Sasson/Wigderson (2001), *Short Proofs Are Narrow*, DOI 10.1145/375827.375835, establish exponential **ordinary shared-DAG Resolution** hardness for suitable expanding families, not R_mix341 or arbitrary algorithms. Valid shortcuts include GF(2) Gaussian elimination, extension definitions, shared-DAG case reasoning and learned clauses; preserve these as upper bounds. The finite signed K4 source has 4 vertices, 6 edge variables, 16 proper 3-clauses and a fixed **208-bit** original-source encoding (8-bit magic, 8-bit clause count, 4-bit signed variable token per literal). K4 is **only** a finite semantic control, not an asymptotically certified expander family. No 3-CNF lower-bound transfer is asserted here.

## COMPUTATIONAL: independently implemented original-source tests

Published V8 source: `experiments/arc/lspv2_503_multiport_sparse_compiler.cjs`, blob `28997e160442d005f10d28fd5967404450a15976`, created commit `2840172c18524a4888cf391c640d93b3fbd2a15f`, successfully **re-fetched and independently replayed**. Its 7,756 assertions on 104 source strings all PASS: 16 authentic K4 charge instances (8 SAT, 8 UNSAT by exhaustive six-variable classification), and 88 malformed controls. It executed 2,332 symbolic indexed WORK operations and 2,332 input-bit observations in each implementation. Global largest original WORK high-water 4,294,967,311; largest compiled high-water 16; largest cumulative original index-description count 1,056 bits versus 108 compiled. An independent Python implementation passed 536 assertion groups on 104 cases with exactly the same SAT/UNSAT/MALFORMED counts (8/8/88) and K4 n=208 sample high-water original 4,294,967,310 / compiled 15. Both represent virtual WORK as sparse maps, *without allocating* four billion cells; their high-water numbers model the native metric, but are not native FLMV instruction-level simulations.

## Full resource and dependency ledger

- **Actual logical inference nodes, certificates and proof bits:** zero; this is a decision-program equivalence, not an R_mix341 refutation. No native R_mix341 checker was invoked or modified.
- **One-time code construction and syntactic type check:** `O(|B|+k)` if the macro is the specified explicit, nonescaping template. No generic program equivalence check.
- **Per-input source parsing / length scan:** `O(n)` time, `O(log n)` counter, even on malformed x. The B parser runs unchanged and remains charged by `T_B,S_B`.
- **Guest prefix work:** 2r actual indexed WORK jumps, each with paid INDEX rebuild/erasure, r forward WORK writes, r reverse WORK reads, 2r source-bit observations, and audit bookkeeping. Index description bits `O(rk log n)`; symbolic V8 raw counts report actual values.
- **Witness/bit evidence:** no UNSAT proof; only a constant-size digest and the typed program text. Any separately required certified derivation remains open.
- **Output / fresh suffix:** exactly the output of B; no SAT oracle, no free classification or external trace. If B has expensive search/restarts, all of it remains in `T_B`.
- **Peak simultaneous WORK and runtime:** dedicated private tape and B tapes are disjoint. The original high-water is huge; compiled physical private area is `r+O(log n)`, plus B. No child output, prefix cache, restart portfolio or hidden auxiliary CNF exists here.
- **Work/span:** one sequential path, so charged work and serial critical span agree up to constant/polylog coding overhead. The virtual equality alone does not supply a realizable arbitrary-A sparse machine interpreter.

**Comparison with prior:** /502 LSPV-4 repaired **one** typed private far port. /503 repairs a growing `Theta(sqrt n)` collection with actual interleaved writes and reverse reads. The extension illustrates a permissible code-aware shortcut, while LSPV-2/502's faithful-execution antichain remains valid for unchanged guests. Neither theorem establishes an all-input solver-dependent decomposer.

## Unresolved transfer and handoff

The required Route A transformation must take **every** fixed polynomial-time SAT decider A, produce `Phi(A)` for all binary encodings, and satisfy fully charged same-FLMV-machine
$$
 t'\le \max\{11/10,3/5+t/2\},
 \qquad s'\le\max\{1/2,s/2\}.
$$
This one-macro optimization has one **parent-length** B call and no reduction to child length `n^(1/2)`; it does not satisfy the universal contraction. Need: source-agnostic, SAT-aware child construction, derivable guest-specific preprocessing without promise or semantic oracle, explicit q/L bounds, independent correctness and recursive closure. [P2-A2], [P2-A5], P1 algorithm nodes and Route B [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2] remain OPEN. *P versus NP remains OPEN.*
