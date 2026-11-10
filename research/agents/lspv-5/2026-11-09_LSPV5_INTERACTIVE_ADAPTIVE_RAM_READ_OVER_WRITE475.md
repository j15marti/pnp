# LSPV-5 interactive: exact adaptive-RAM select/store DAG and the quadratic simulation frontier

**November 9, 2026, PST | User-requested immediate follow-on, not a scheduled LSPV-5 run | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Goal and scope

Continue investigating whether *general*, data-dependent, random-access SAT computations can be given a direct, time-preserving, low-space simulation in the **exact FLMV random-access Turing-machine model**, by applying Abstract Interpretation to the machine's memory dependencies. Preserve separate hypotheses $A_P$ (uniform, total deterministic both-label SAT decider, unknown fixed polynomial time exponent) and $A_{NP}$ (nondeterministic existential verifier). No use of a guessed trace, SAT oracle, or separate nonlinear shortcut is allowed when claiming a deterministic time/space theorem.

**Precise initial candidate.** Symbolic alias analysis could avoid Williams's high-indegree computation-graph obstruction by retaining the equality relation between adaptive read and write addresses, without enumerating exponentially many address histories. Test whether this gives a usable square-root-space, simultaneously time-efficient random-access simulation.

**Four falsifiers:**
1. A symbolic read-over-write expression might fail when a later write aliases an earlier write or is guarded by a previous read.
2. A may-abstraction of the addresses might merge incompatible histories and return an impossible read value.
3. Exact symbolic representation might itself require exponentially many nodes; alternatively a compact formula might conceal expensive physical gate-level or memory-access work.
4. The resulting bounded-fan-in circuit might remain quadratic in computation time, so applying square-root-space circuit evaluation gives no nontrivial sublinear-time-derived *space* saving, and the evaluator may have uncontrolled *time*.

## SEARCH and original theorem scope

- Ryan Williams, *Simulating Time with Square-Root Space* (STOC 2025), Theorem 1.1 and Remark 1.6: $TIME[T]\subseteq SPACE[O(\sqrt{T\log T})]$ for **multitape Turing machines**. A special extension covers oblivious random-access schedules whose accessed registers are efficiently computable from the time index, with extra polylogs; **arbitrary adaptive random-access extension remains explicitly OPEN**. The proof's space-saving graph/tree evaluator does not assert the original $T$ running time for its simulator. https://doi.org/10.1145/3717823.3718225
- Pippenger and Fischer, *Relations Among Complexity Measures*, JACM 1979, DOI 10.1145/322123.322138: two-tape input-oblivious $O(T\log T)$ online simulation concerns **one-dimensional-tape Turing machines**, not arbitrary random-access RAM. https://scholarship.claremont.edu/hmc_fac_pub/597/
- Goldreich and Ostrovsky, *Software Protection and Simulation on Oblivious RAMs*, JACM 1996, 43(3):431-473: an arbitrary RAM admits **probabilistic** oblivious RAM simulation with polylogarithmic time overhead, within its precise distributional/security definitions. It is not a deterministic per-time precomputed access schedule satisfying the Williams remark, and does not grant exact both-label SAT correctness for every coin sequence. https://www.wisdom.weizmann.ac.il/~oded/p_soft.html
- *Oblivious RAMs without cryptographic assumptions* (STOC 2010): probabilistic RAM, small failure probability; not a deterministic all-input FLMV simulator. https://research.ibm.com/publications/oblivious-rams-without-cryptogrpahic-assumptions
- McCarthy's array select/store axioms, as described by Microsoft's Z3 theory-of-arrays guide, yield the exact **read-over-write** identity used below. This is established program-logic machinery, not a new result of this project. https://microsoft.github.io/z3guide/docs/theories/Arrays/
- FLMV, JACM 2005, Section 2.1: native indexed high-water space, and equivalent sparse-normalized representation with at most polylogarithmic time overhead. The physical space of a compiler/simulator must be accounted separately from its symbolic logical DAG. https://lance.fortnow.com/papers/files/tst.pdf
- A relevant restricted circuit model distinction is discussed in the ECCC report on circuits with lookup tables: $O(T\operatorname{polylog}S)$ *LUT-circuit* simulation does not imply an equally sized **bounded-fan-in circuit**, because random reads are still abstract unit-cost LUT gates. https://eccc.weizmann.ac.il/report/2001/062/download/

Current project evidence read: entire root \`proof1.txt\` (blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`) and \`proof2.txt\` (startup blob \`a73beac1143490e4f18ae498a1f65b63ef5b4ac3\`), verified five-role handoff \`research/coordination/2026-11-09_1624_ASSUMED_TIME_DERIVE_SPACE_FLVM_FIVE_ROLE_HANDOFF.md\` (blob \`644b0d4745f2edeb8718c7e536a7da995b36b36f\`), [P2-L5-471], [P2-L5-472], [P2-L5-473], current [P2-A1], [P2-A2], [P2-A3], [P2-A5], [P1-01], [P1-03], [P1-04], AGENTS.md, CODEX.md, .codex research skill and issue #3. Change-aware required repositories: \`konard/p-vs-np/scripts/proof_status.json\` (blob \`93b77ed3d8fe456f81c690035f45f07910a247f2\`), \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` (blob \`18d693ea71dfa433370eb7afbebc3106e32f03e5\`). Neither contains an authenticated time-preserving FLMV-machine RAM-to-small-space theorem. Previously inspected Grok REWIRE and Claude ONETAPE are restricted and provide no generic adaptive random-access bridge.

## Formal construction and symbolic lemma

Fix a deterministic trace with $R$ reads and $W$ writes of a finite fixed-width work-memory array $M_0$. The *symbolic addresses* $a_i$ and symbolic values $v_i$ can be expressions depending on earlier read values. Write $j$ has an independently defined Boolean legality/enable guard $g_j$; all write events are ordered chronologically.

For a read of symbolic address $a$, let

$$
E_0(a)=\operatorname{select}(M_0,a),
\qquad
E_j(a)=\operatorname{ite}\bigl(g_j\land(a=a_j),v_j,E_{j-1}(a)\bigr).
$$

At read time, only writes already performed in the trace are included. Consequently, $E_w(a)$ returns the **latest enabled write** at that exact address if one exists; otherwise it returns the original memory value.

**Lemma (PROVED/RESTRICTED, standard select/store induction):** For every *concrete* input, every concrete execution that follows the specified program/branch guards, and every read, evaluation of the symbolic DAG yields the identical value as the mutating RAM. This remains true if the address of a later operation depends on earlier symbolic read expressions, by induction on chronological operations. The symbolic representation is exact; it is not a may-abstraction that guesses addresses independently.

**Proof:** Initially $E_0$ equals original memory. On adding write $j$, the operational memory either remains unchanged for addresses not equal to $a_j$ (or when guard disabled) or stores $v_j$ at $a_j$; $E_j$ implements exactly that dichotomy using an equality test and conditional selection. An induction on operations, including later addresses computed from previously correct reads, establishes full extensional equality on every execution. The recursion is chronological and has no circular dependency. QED.

**Cost-sound logical syntax bound:** Each read adds one equality test and one select/ITE for every preceding write. Hence the total number of such logical operators is at most

$$
\sum_{\mathrm{read}\ i}W_{<i}\le RW\le \frac{(R+W)^2}{4}.
$$

The *underlying address/value/guard computations, width of address equality, initial memory selects, symbolic DAG references and bit-level encoding* are NOT included in this operator count. For $b$-bit addresses and $v$-bit data words, a straightforward fully explicit bounded-fan-in implementation costs up to $O(RW(b+v))$ Boolean gates **plus** all access and address logic. No claim that an arbitrary FLMV work tape can be represented as one free select/store oracle is made.

**Why the bounded-fan-in circuit route stalls:** Under bounded address/value widths and ordinary explicit initial-memory reads, a straightforward circuit for a $T=R+W$ memory-operation trace may have $Q=\Theta(T^2)$ gates just for read-over-write logic. Williams's theorem for size-$Q$ bounded-fan-in circuits yields space $\widetilde O(\sqrt Q)=\widetilde O(T)$, not a generic $T^{1-\epsilon}$-space simulation. If some other construction reduces circuit size to $Q=O(T^{2-\delta})$, this route would yield a **space-only** improvement $\widetilde O(T^{1-\delta/2})$, but still does not guarantee a simultaneous $O(T)$ running time. Conversely, the *implicit logical* select/store DAG can be very compact because array reads remain atomic, and cannot be charged as a physically low-space random-access simulator.

## Two independent computational falsifiers

Producer: \`experiments/review/lspv5_475_adaptive_symbolic_ram.py\`; independent V8 replay: \`experiments/review/verify_lspv5_475_adaptive_symbolic_ram.mjs\`. Source input is an arbitrary $M$-bit initial array plus initial address, $M\in\{2,4,8\}$. The adaptive program repeatedly reads at a position determined by prior read values, conditionally writes a value at a differently computed position, and eventually performs another adaptive read. Both execution semantics are independently compared for **all** $2^M M$ original source/address combinations at every depth $1\le d\le8$, including enabled and disabled writes and repeated aliasing.

- Python symbolic term DAG: **16,984 checks**, zero failures, of which 16,960 compare concrete answers and 24 check the expected number of read/write alias candidate comparisons.
- Independent JS persistent write-log interpreter against direct native array mutation: **33,920 checks**, zero failures, including the alias counts. The two languages implement different mechanisms and share no evaluation engine.
- At $M=8$, $d=8$, there are 146 hash-consed logical DAG nodes and 36 read/write equality tests; 2,048 source/address combinations tested at this depth.
- \`results/raw/arc/2026-11-09_LSPV5_475_ADAPTIVE_SYMBOLIC_RAM_RAW.json\` records complete finite scenario counts and all limitations.
- The small finite tests execute an in-memory Python/Node model, **not** the authoritative FLMV machine or historical R_mix341 checker. They do not establish complexity lower bounds on unrestricted SAT solvers.

The initial hypothesis that adaptive addresses inherently force *exponential representation* is refuted by the exact quadratic upper. The separate stronger hypothesis of a **time-preserving, sublinear-space, universal random-access SAT transformation** is still OPEN.

## Research directions with concrete falsifiers

1. **Source-aware bounded-block dependence:** Rather than demand completely oblivious access, consider the class where a length-$b$ time block has a uniformly bounded number of live external predecessor memory regions. Attempt to adapt Williams's bounded-indegree tree evaluation. The locality bound must be proved for **every** input, and its machine-space implementation charged; do not mistake typical learned-clause locality for a worst-case theorem.
2. **Relational CEGAR memory state:** Maintain the exact equality/alias relation, last-write provenance, branch guards and source identity. Refine when a read could have too many candidate predecessors. The test is whether worst-case refinement and simultaneous live representation remain truly sublinear while maintaining deterministic time, not whether sample formulas have small proofs.
3. **Online ORAM as a contrast, not a free solution:** Study why probabilistic input-oblivious *distributions* do not satisfy a deterministic input-independent register schedule for all coins and all inputs. If randomness is fixed, require uniform exact correctness and an actual bound on schedule memory.
4. **Quantifier + FLMV audit:** Even an effective time-preserving $S=\widetilde O(\sqrt{T})$ simulator could contradict Buss–Williams only in the small-time region $c<\tfrac43\cos(\pi/7)\approx1.201291824$. SAT in P permits arbitrarily large fixed $c$. Universal $P\ne NP$ needs a theorem that handles all $c$ rather than extrapolating a low-exponent bound.

## Publication and dependency status

**Status:** PROVED/RESTRICTED symbolic read-over-write / polynomial-size syntax bound + COMPUTATIONAL independent finite controls. This is an established standard array-theory construction applied to the present research hypothesis, not a claim of mathematical novelty.

The root trackers' existing nodes are unchanged: **TRACKERS REVIEWED; NO MATERIAL CHANGE**. In particular [P2-A2] remains OPEN, [P2-A1] known, [P2-A3] conditional, [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN, [P1-01], [P1-03], [P1-04] OPEN. The present interactive result is a technique/audit record, not a new universal proof theorem. No change to historical R_mix341, ownership, main.tex or scheduled tasks. Repo-wide preflight and historical checker were not executed in this isolated scratch environment; report/code/raw are published on main with complete per-file readback, not repository-wide CI.

**Next material gap:** construct a machine-model-exact, *simultaneously time-efficient* representation and evaluation procedure for arbitrary source-dependent random access with all-input correctness, or prove a precise counterexample to a proposed restricted transfer. **P versus NP remains OPEN.**
