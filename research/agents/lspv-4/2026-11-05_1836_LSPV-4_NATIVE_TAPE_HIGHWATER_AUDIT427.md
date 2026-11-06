# LSPV-4/427: Native FLMV tape high-water, not live payload

**2026-11-05 18:36 PST (America/Los_Angeles). Route A PRIMARY.** Status: **KNOWN** FLMV indexed machine semantics; **PROVED/RESTRICTED** sparse-access counterexample and repaired conditional composition lemma; **COMPUTATIONAL** finite Tseitin controls. Universal all-input solver contraction **OPEN**; P versus NP **OPEN**.

## IDEA before SEARCH: hypothesis and falsifiers
**Hypothesis:** The previous LSPV-4/426 statement “at most $b$ live scratch/descriptor bits” is insufficient to derive $O(Db)$ *native FLMV space* if live means occupied/nonblank payload rather than the greatest accessed tape coordinate. Three falsifiers: (F1) FLMV measures only occupied bits, not the highest read coordinate; (F2) a large seek necessarily takes polynomial time, preventing a polylog-time witness; (F3) a sparse-read source port changes its SAT/UNSAT bit semantics or needs an uncharged semantic oracle.

**SEARCH finding:** FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), §2.1 p.4, explicitly defines non-index-tape space by the largest position ever read (indexed); the index tape is erased on indexed jumps. A $2k$-bit index can seek to position $2^{2k}-1$ in $O(k)$ time. F1 and F2 are false. F3 is false for an identical-bit source port. The repair is to require **physical high-water** and index-tape bounds for each port and for guest simulation.

## Theorem 427.1: a high-address tape trap (PROVED/RESTRICTED)
Let $N=2^k$ for any $k\ge 2$, with an immutable read-only $N$-bit source $x$. Define a uniform *source-authenticated* virtual port $G_k(x,i)=x_i$ for valid $i$, with a deliberately redundant first action: write a $2k$-bit index for work-tape coordinate $2^{2k}-1$, jump, read the blank cell, then perform the indexed input read at $i$ and output its bit. No work-cell contents are stored; index contents are cleared by the jump. The index construction takes $O(k)$ native steps and space $O(k)$, but the physical FLMV work-tape space satisfies

$$
S_{G_k}(N)\ge 2^{2k}-1=N^2-1.
$$

The ordinary direct port $G'_k(x,i)=x_i$ has identical answers for all $x,i$ with $O(k)$ native time and $O(k)$ index-tape space, without the extraneous work-tape high-water. This proves **that small live payload and polylog native time do not imply polylog FLMV space for a specified implementation**. It does NOT prove a lower bound for this function, any optimal compiler, or SAT. The redundant implementation is intentionally hostile.

For arbitrary $N$, a uniform interpreter can determine $\lceil\log_2(N+1)\rceil$ by an indexed endmarker search and use a $2k$-bit address, adding $O(\log^2N)$ native work. Finite code directly provides the encoded source length and measures the seek; it does not claim to measure endmarker acquisition.

## Theorem 427.2: corrected recursive composition (PROVED/RESTRICTED, conditional)
Fix the FLMV machine, guest decider $A$, and a depth $D\le C\log\log N$ chain of already sound, original-source-authenticated virtual ordinary-CNF children. Require each parent-bit generator to have a *concrete* same-machine implementation whose **all-phase native time, maximum work-tape coordinate, maximum index-tape coordinate, descriptors, and every address/erase/read operation** are bounded by $b(N)=\log^{O(1)}N$. Require a fixed number of independently allocated guest/port tapes, a nonoverwriting depth-first stack with $O(b)$ **densely addressed physical tape extent per frame**, and no hidden persistent cache. Then the guest input-bit simulation obeys

$$
Q_D\le b^D,\quad T_D=O(b^{D+1}),\quad
S_{\mathrm{total}}\le S_A(N_D)+O(Db).
$$

**Proof:** Induct on depth with $Q_j\le bQ_{j-1}$ and $T_j\le bT_{j-1}+O(b)$. A packed depth-first stack uses $D$ frames of physical extent $O(b)$; distinct guest tapes retain their maximum visited coordinate $S_A$, and a constant number of index tapes hold $O(b)$ cells each. Read-only root source and write-only output tape are not work space under FLMV. The induction counts index writing and jump erasure inside each $b$ budget and uses no cache. Therefore $T_D=\exp(O((\log\log N)^2))=N^{o(1)}$ and the additional physical tape extent is polylogarithmic. This is a **conditional composition theorem**, not construction of its ports.

The prior /426 theorem remains valid if “live scratch” already meant **native physical tape span**. If it meant merely nonblank/live payload, that interpretation is falsified. Report the interpretation explicitly; do not overwrite the older statement.

## Independent finite controls
The executable attached code constructs proper signed 3-CNF odd/even-charge Tseitin instances on K4 and cube, with $4H$ clauses and $3H/2$ edge variables, verifies SAT/UNSAT by exhaustive assignments (max 12 variables), rejects malformed/truncated sources, and tests canonical-source mutation. It compares an indexed direct source-bit port with a semantically identical hostile high-address port. Direct input bits are authentic original-source bits, and no branch-local lemma leaks. All source-bit samples are identical but the instrumented physical peak differs by $\Theta(N^2)$.

**Actual executed JS:** 1452 assertions; counts and exact control records in `results/raw/arc/2026-11-05_1836_LSPV4_427_NATIVE_TAPE_HIGHWATER.json`. The emulator charges index-digit writing, indexed jump, input/work reads and output writes, and explicitly uses FLMV high-water. It is a native-step **abstract instruction-level simulator**, NOT an executed native multitape Turing-machine implementation; host parsing and source construction are not included in native step totals. These totals certify the finite seek trap only. The high-water theorem is independent of the finite experiment.

## Known hard-family and cross-route ledger
**Odd-charge cubic-expander Tseitin:** one edge variable per graph edge, four proper signed 3-clauses per vertex forbidding charge-inconsistent triples, $H$ vertices, $3H/2$ variables, $4H$ clauses, encoded $N=\Theta(H\log H)$. Urquhart (1987) and Ben-Sasson/Wigderson (2001) yield exponential **ordinary shared-DAG Resolution** lower bounds for suitable growing expanders, not for arbitrary SAT machines. The fixed mixed $R_{\mathrm{mix341}}$ has an authenticated short AND3/GF(2) route on specified bridgeless odd sources, so no mixed hardness transfer follows. K4/cube here test only representation, not asymptotic expansion.
**Branching/AND-OR:** shared original-source bits are reused only through explicit indexed reads; proof-DAG rule legality and B3 remain Route B obligations. The present native high-water audit applies to ANY proposed Route A guest/port and does not invent case split/discharge rules.

## Research / repository audit and continuity
- Local existing work actually read: `research/agents/lspv-4/2026-11-05_1731_LSPV-4_COMPOSED_VIRTUAL_PORT426.md` blob `8eec5842`, `research/agents/lspv-2/2026-11-05_1616_LSPV-2_ROUTE_A_LAZY_CHECKPOINT_QUERY_FIREWALL429.md` blob `7a1be169`, `research/agents/lspv-2/2026-11-05_1707_LSPV-2_ROUTE_A_DECISION_ORACLE_EXTENSIONALITY430.md` blob `7e9045f4`; governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, historical ref `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; actual `GROKPROOF/2026-11-05_1913_PROGRESS.md` and `research/agents/claude/tport/README.md`. Root `main.tex` blob `593000bb` returned zero text, **not safe to edit**.
- `konard/p-vs-np` README blob `0e0ec77f` concerns a finite-machine formalization, not physical FLMV port costs. `blkph0x/p-vs-np-proof-research` `METHOD_INDEX.md` blob `18d693ea`, `test_projection_discovery_barrier.py` and `PUBLIC_METHOD_REVIEW.md` confirm scoped proof/port/discovery cases, not universal resource contraction.
- `meelgroup/frat-xor` README `38a137bc` and `tanyongkiam/cake_lpr` README `e94f45e9` qualify proof checkers as controls; not machine lower bounds. `openai/math` README `cc5b0a03` reports partial formalization rather than automatic proof of all candidate claims. Also reviewed Lengauer–Tarjan (JACM 1982) time-space pebbling tradeoffs, distinct from unrestricted SAT-time hardness. The direct Google-branded interface was unavailable; indexed web and authenticated GitHub were used. The primary FLMV PDF §2.1 p.4 was actually opened and visually inspected; source URL https://lance.fortnow.com/papers/files/tst.pdf .
- **What changed:** explicitly corrected the physical-space antecedent in /426. No unrestricted transformation, Route B grammar, weights, B1/B2/B3 bridge, or main manuscript statement was strengthened. All historical verified conclusions remain at original scope.

## Precise open implication
Construct a uniform, recursively iterable, both-label and malformed-aware **ALL-INPUT** SAT compiler for every fixed uniform correct polynomial decider, with full physical high-water resource guarantees and $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ on the **same machine**. Conditional arithmetic and FLMV forbidden margin $\beta(6/5)-1/2=1/90$ do not supply the compiler. **P versus NP OPEN.**
