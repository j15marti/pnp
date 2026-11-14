# TMR-1/015: no-copy, logarithmic-extra-space simulation of a bounded indexed source port

**Date:** November 14, 2026, 01:05 PST (America/Los_Angeles). **Role:** NEW TMR-1 Machine Model Lead. **Repository:** j15marti/pnp, main. **Exact claim ID:** TMR1-NC15.

**Statuses:** The new uniform model-translation theorem is **CANDIDATE pending independent TMR-5/TMR-4 review**. Finite machine-microstep ledger and independent native Python replication are **COMPUTATIONAL**. The unrestricted all-exponent 3-SAT lower bound and P versus NP are **OPEN**. This is an upper bound on SIMULATION cost, not a lower bound on solving SAT.

## 1. Model and theorem

Let $x$ be any binary source of exactly $L$ encoded bits, with immutable left and right endmarkers at physical positions $0$ and $L+1$. This includes valid fixed-encoding 3-CNF formulae and malformed encodings. A is ONE fixed finite total uniform deterministic multitape program for EVERY source length and ALL outputs, with a fixed finite work alphabet/control and a fixed number of ordinary, locally moving writable work tapes. Time counts all physical transitions. $S_A(x)$ counts the total number of visited writable work cells, including addresses, indices, stacks, buffers, partial copies, caches, conversions and recomputation. The correct SAT, UNSAT and declared malformed-input responses are all preserved.

**Declared bounded indexed-port model.** On a query, A's address tape contains a delimited binary representation of an index $j$ of at most $w=\lceil\log_2(L+2)\rceil$ bits, with its head at a fixed query delimiter. The canonical validity/overflow tag is explicitly readable and paid; invalid/overflow queries return a distinguished right/end-of-range symbol R. A valid-address query returns $x_j$ for $0\le j<L$, or R otherwise, in ONE special transition. Its ordinary work-tape actions remain locally charged. The query field must satisfy this bounded-length interface contract on every query, even for malformed source inputs. The port may read the entire field in the one special step; this is explicitly more powerful than an ordinary local TM, and is not a unit-cost growing-word RAM.

**Local model.** B has one ordinary read-only original-input head, initially at the left endmarker, moving at most one cell per counted transition. All writable heads move locally. B may use the finite ordinary A work tapes plus a fixed number of new ordinary scratch tapes. It neither receives advice nor has a second physical copy of the source.

**New theorem TMR1-NC15 (CANDIDATE).** For every one fixed total A in the bounded-port model, there exists ONE fixed total deterministic local-input-head machine $B_A$, independent of $L$ and $x$, and a finite constant $d_A>0$ such that on ALL binary strings:

$$
\operatorname{out}_{B_A}(x)=\operatorname{out}_A(x),
$$

$$
T_{B_A}(x)\le d_A(L+2)(w+1)(T_A(x)+1),
$$

$$
\boxed{S_{B_A}(x)\le S_A(x)+d_A(w+1).}
$$

Unlike the previous TMR-1/013 source-copy simulator, this construction adds **NO $L$-cell source copy**. The new substantive arrow is logarithmic-extra-space preservation under the explicitly bounded source-index interface.

### Constructive proof, with all micro-operations charged

B carries A's fixed program, finite control and original writable work tapes unchanged. To simulate a nonquery A step, B executes the same local work-tape actions in a fixed number of transitions. A's indexed query transition is decomposed as follows:

1. Without changing other A tape heads, traverse the bounded delimited address field on its original A address tape, copying the $j$ bits onto an auxiliary binary counter tape. Record or read the valid/overflow tag. Restore A's original address head to its original delimiter. The other A work heads and writable symbols are unchanged. At most $O(w+1)$ new scratch cells and $O(w+1)$ local transitions are needed. If the flag is invalid, return R without any original-source traversal.
2. From wherever B's ONE genuine original-source head currently rests, move it left to physical position 0. At most $L+1$ local steps are needed. Move right to the first source-data cell, physical position 1, charging this step.
3. Use the binary scratch counter (initial value $j$) to walk forward. Before every source advance, scan at most $w$ counter cells to test whether the counter is zero. If it is zero, read the currently exposed source symbol; if that symbol is the right endmarker, return R. Otherwise advance the genuine source head one position and decrement the binary scratch counter using a locally moving head, at most $O(w)$ transitions. Stop and return R immediately upon meeting the right endmarker, even if the counter is still nonzero. There are at most $L+1$ rightward source moves, irrespective of how large $j$ is within its bounded width. No random access or uncharged arithmetic is performed.
4. Keep the fetched data bit or R in the finite control (constant alphabet). Restore any scratch/original address head needed by the declared query convention. Only then perform the ONE original A transition, including the original simultaneous reads/writes/head movements on all A work tapes and the next A control state, using the fetched bit to choose that finite transition.

The counter is a physically writable $O(w)$-cell binary tape, not a free integer register. Its zero tests, borrow propagation, head restoration and all original-input head moves are counted. The original A address-field cells visited during decoding add at most $w+O(1)$ work-cell visits even if A itself never visited them; no uncharged original A work storage is assumed. No retained copy of the source is made. The original input is still immutable and is never used as free random-access memory.

A simulated query takes $O((L+2)(w+1))$ actual local steps; a nonquery step takes $O(1)$. This holds even for repeated, backward and adaptively chosen indexed requests, because every request is rescanned and charged independently. At all instants B retains A's full writable configuration plus $O(w+1)$ scratch cells. Induction on A's complete transition sequence proves that A's exact next state, work contents and output label are reproduced. A halts on every source, so B also halts: the address traversal and each bounded original-source scan are finite. All bounds refer to **the same input and same simulated A computation**.

**Potential failure modes explicitly excluded by the model:** an unbounded-length address field without an overflow marker; arbitrary unit-cost indexed WORK tape access; unbounded-unit-cost arithmetic; an oracle that supplies SAT/UNSAT rather than the next source bit. None is included in NC15. A stronger theorem for any such model requires a separately paid compiler.

## 2. Quantifier bridge and precise resource consequences

The team's target is

$$
Q_{\rm local}:\quad
\forall A\text{ correct fixed total local},\
\forall k\in\mathbb{Z}_{\ge1},\
\forall C>0,\ \forall L_0,\
\exists F\text{ valid},\
|F|\ge L_0,\
T_A(F)>C(|F|+1)^k.
$$

Since $(L+2)(w+1)\le4(L+1)^2$ for $L\ge0$, the charged compiler gives the old but now **space-improved** conditional implication:

$$
\boxed{Q_{\rm local}\Longrightarrow Q_{\rm indexed\ bounded\ port}.}
$$

Fix A, k, C and $L_0$. Apply $Q_{\rm local}$ to its ONE fixed B at exponent $k+2$ and constant $4d_A(C+1)$. Divide by the simulation inequality to force an A-input violating $C(L+1)^k$. The hard formula may depend on the machine, k, C, and $L_0$. This is not per-length algorithm minimization; no hard-coded advice or single all-UNSAT family is involved.

**New resource consequence.** If a fixed indexed A uses at most $s(L)$ visited writable cells on each length-L input and $s(L)=\Omega(\log(L+2))$, then the ONE compiled local B uses $O(s(L))$ writable space, while taking at most an $O(L\log L)$ multiplicative time overhead. In particular a logarithmic-space indexed input algorithm translates to a logarithmic-space local input algorithm, not a linear-space algorithm. This repairs the **space blowup** of TMR-1/013; it does not remove the time overhead.

The converse language-class observation is immediate when local source queries are also supported by the indexed model (one can pay ordinary local reads rather than make indexed requests); it must NOT be read as identifying this interface with FLMV's stronger random-access WORK-tape model. The theorem also does not transfer a fixed SAT time exponent or an existing small-space time-space exclusion without rechecking the shifted exponent and every model hypothesis.

For a fixed physical $r$-work-tape machine, $S_A(x)\le r(T_A(x)+1)$ (up to the chosen initial-cell convention). This SAME-machine upper bound on visited writable space does not convert any fixed-small-space exclusion into an all-exponent lower bound. All-transition TMR-4 potentials still require separate initial/terminal bindings and all-edge cost soundness; this upper-bound compiler alone is not a SAT processing lower bound.

## 3. Hostile controls and actual execution evidence

**Published and readback-verified V8 audit:** experiments/tmr/tmr1_nocopy_indexed_bridge015.cjs (Git blob e20b44143f5a33dd01956dae958a5ff9badd0e22); immutable raw results/raw/tmr/2026-11-14_0104_TMR1_NOCOPY_INDEXED015_RAW.json (Git blob 458eef955b781f74c8a23e9f745bd3041bf3a48a). Exact self-contained function was executed directly in hosted V8 before its source was published. Across all 1,023 binary inputs of lengths 0 through 9, it performed 64,380 indexed-port query comparisons and 5,374,254 charged microsteps, including 9,207 tagged-invalid cases, 25,113 out-of-range addresses, 9,207 dynamic adaptive source queries and all three fixed original-head starting positions. Address/counter/source head moves and visited scratch cells were explicitly ledgered. Zero query/output mismatches, zero conservative time bound violations and zero scratch-width violations. Its synthetic finite-controller outputs included 565 accept and 458 reject outcomes.

**Separately implemented native CPython audit:** experiments/tmr/tmr1_independent_nocopy015.py (Git blob 79323052188f9c98c54ca306b22e1452d2856a39, identical to the locally executed file's git hash-object). Immutable results/raw/tmr/2026-11-14_0104_TMR1_INDEPENDENT_NOCOPY015_RAW.json (Git blob 4c87700b05fcf6f068d88b6ca07da41f000c1069). Independent source tests lengths 0 through 10: **95,118** queried source/head pairs, **4,094** explicit repeated-address pairs and separately verified parity-controller outputs (1,024 even/1,023 odd). Maximum observed ledgered query cost 152 microsteps and scratch width 4; zero assertions failed. Neither implementation imports the other.

**Scope limitations:** These are explicit local-head and counter **microstep ledgers**, not an instruction-level finite transition-table construction for a general SAT decider, nor native OS Node replay of the published JavaScript. They are finite **COMPUTATIONAL** evidence supporting the separate symbolic compilation proof. The bounded width, tag, delimiters and empty-input case were tested. The theorem itself handles Horn, 2-SAT, XOR/Tseitin Gaussian-elimination programs, bounded treewidth, disjoint products, sharing, padding, renaming, auxiliary variables, compact algebra, repeated rereads, caching and recomputation simply by faithfully emulating their actual ordinary A work transitions; the two finite drivers do **not** independently solve those SAT families.

## 4. Original sources, reconciliation and dependency audit

1. Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (2005), DOI https://doi.org/10.1145/1101821.1101822, primary original author manuscript https://lance.fortnow.com/papers/files/tst.pdf, Section 2.1 directly checked. Their chosen random-access TM has **INDEX tapes on non-input work tapes**; indexed moves erase the index tape, and work-space measures include the largest position indexed. It is NOT the same model as this bounded original-source-bit port; the well-known $c<\varphi$ exclusions are simultaneous time **and restricted space**, not all-polynomial-time exclusions.
2. TMR-1/013, original report research/agents/tmr-1/2026-11-13_2300_TMR1_CHARGED_INDEXED_PORT_BRIDGE013.md and original code/raw, previously obtained $S_B\le S_A+L+O(\log L)$ via a complete writable source copy. NC15 improves THIS model bridge's extra writable-space guarantee but does not call the old theorem incorrect.
3. TMR-1/012, original research/agents/tmr-1/2026-11-13_2204_TMR1_MULTI_INPUT_HEAD_COPY_BRIDGE012.md; a distinct bounded LOCAL h-source-head copy construction, with its own space overhead.
4. TMR-3/011, original research/agents/tmr-3/2026-11-13_2233_TMR3_CROSSING_SPLICE_AUDIT011.md; fixed-cut local physical crossing statements. NC15 does not claim to transport a particular crossing product back to indexed A.
5. TMR-4/013 and /015; original reports research/agents/tmr-4/2026-11-13_2245_TMR4_COPY_READY_POTENTIAL_TRANSFER013.md and research/agents/tmr-4/2026-11-14_0031_TMR4_UNIFORM_LATE_COPY_BELLMAN_NO_GO015.md. Their copy checkpoint and source-observation limitations remain distinct from this no-copy micro-simulation.
6. Superseding 2026-11-13 12:49 PST TMR-five directive at research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, rechecked before shared writes. The legacy Route A/B assignments and LSPV ownership text are superseded, but historical valid mathematics/counterexamples remain evidence.

**Read contract:** Full root proof1.txt (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), full authentic proof2.txt via Git blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c, ordinary file fetch erroneously blank), and full canonical main.tex via Git blob (2,522,180 characters, SHA 903092cd483c0b17694c9f500fa03b5a703508cc, ordinary file fetch blank) were recovered. AGENTS.md, CODEX.md, repo skill, latest issue #3 through TMR-5/012, all five peer handoffs, and materially relevant original reports/code/data were consulted. The role-specific authorized main.tex region exists but the TMR-5 synthesis owner should integrate this new **CANDIDATE** without changing its status; main.tex is not modified here. The existing proof targets have no new closed load-bearing lower-bound arrow: **TRACKERS REVIEWED; NO MATERIAL CHANGE**. No scheduled task was created, revived or modified.

## 5. One next target

**TMR-5/TMR-4 independent review request:** Check every local-head/counter micro-operation of NC15, especially the address-field head restoration, all-length overflow contract, empty source, and exact $S_A+O(\log L)$ visited-cell accounting. Then determine whether any known *same-machine* local-input lower bound with a sufficiently strong exponent and unrestricted space could survive the $O(L\log L)$ time slowdown. Do not extrapolate restricted crossing cuts or FLMV small-space results beyond their quantitative scope.

**General 3-SAT superpolynomial processing necessity: OPEN. P versus NP: OPEN.**

END_OF_REPORT::TMR1::2026-11-14_0105_PST
