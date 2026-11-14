# TMR-3/029: General one-tape network serialization and MCSP exponent firewall

**Pacific timestamp:** 2026-11-14 14:31 PST, America/Los_Angeles. **Role:** TMR-3 Time-Space Tradeoffs. **Status:** NETSIM33 **PROVED/RESTRICTED** symbolic general-network upper simulation; independent physical-model review **OPEN**. Finite Python checks **COMPUTATIONAL**. P versus NP **OPEN**.

## 1. Genuine new result relative to prior work

TMR-3/024 established a fixed-processor simulator, and TMR-3/025 treated a polynomial-size **ring** with a fixed processor catalogue, one shared input stream, and two neighbor message ports. This run does **not** rediscover the standard quadratic one-tape simulation or claim that polynomial parallel-resource collapse is new. The new scoped result generalizes its explicit interface accounting to **an arbitrary directed graph**, with separately generated finite processor programs and initial input copies, high-fanout one-bit messages, FIFO queues, and source-dependent but fully charged **uniform initialization**. The resulting $O(M^2)$ single-work-tape serialization gives a precise failed lower-bound transfer for the existing MCSP exponent regime.

Original evidence ledger and statuses:

| Path | Evidence and actual scope |
| --- | --- |
| research/agents/tmr-3/2026-11-14_1028_TMR3_MCSP_POLY_RING_SERIALIZATION025.md; experiments/tmr/tmr3_ring_network025.cjs | Prior restricted ring simulation $O(U+B(N+pB))$, explicitly NOT arbitrary graph |
| research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md; experiments/tmr/tmr3_rawscan031.py | Prior restricted bare-truth-table MCSP enumeration; $N D(n,s)$ time and $N+O(s\log(n+s)+n)$ work cells |
| research/agents/tmr-3/2026-11-14_1228_TMR3_MCSP_MOBILE_HEADER_FUSION027.md | Prior full-output ordered-header obstruction and mobile-counter fusion, not a network decision lower bound |
| research/agents/tmr-2/2026-11-14_1417_TMR2_SHARED_ORACLE_PREPROCESS032.md | Exact source-independent oracle-query preprocessing bound; cannot impose it on arbitrary syntax-aware SAT |
| research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md | Earlier adaptive locality theorem, evaluation-oracle only |
| research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md | Syntax-aware counterexample and conditional circuit-certificate direction |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex | Previous crossing-sequence SAT lower bound also affects nondeterministic one-tape computation |
| research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex | Prior portfolio collapse and restricted alternation-trading barrier |
| GROKPROOF/2026-11-13_0526_PROGRESS.md; historical affine/Walsh and nonlinear TMR controls | Open unrestricted transfers, and examples where large representations do not imply large computation |

## 2. Explicit uniform network model

Let $F$ be a binary string of encoded input length $L$. A **fixed finite deterministic uniform initializer** $G$ sees the actual source string, takes $B(F)\ge1$ multitape transitions, and emits a fully explicit network descriptor: $K(F)\ge1$ distinct finite processor transition tables, a graph with $E(F)$ explicitly encoded directed edges, initial processor states, private input tape contents/head positions, work tape contents/head positions, empty or explicit initially queued messages, and a distinguished output processor. The entire descriptor length is at most $B(F)$ up to fixed encoding constants. Thus no length-dependent advice or free source duplication is hidden. Programs and initial tapes may depend on $F$, but producing them is fully charged to $G$.

Every processor has one finite-alphabet, two-way read/write **local work tape**, optionally a one-way read-only **private input tape** explicitly initialized by $G$, and fixed finite control as specified by its generated description. Each synchronous round allows at most **one ordinary local transition** per processor, consuming at most one queued message bit and emitting at most one bit per outgoing edge. Each edge broadcast is separately charged; outgoing messages are only visible at the **next** round. A waiting/halting processor is inert. The network always halts with one correct output label after $R(F)$ actual rounds, including rejection and malformed-input behavior. No unbounded machine words, free random access, oracle answers, uncharged code generation, or instantaneous arithmetic are present.

Define the fully charged aggregate envelope

$$
M(F)=1+L+B(F)+(K(F)+E(F))(R(F)+1).
$$

The $L$ term is a physical cache of all source bits, $B$ includes actual uniform generation and all initial data/program output, $KR$ pays local transitions and newly visited tape cells, and $ER$ pays every link bit and maximum FIFO backlog. $M$ is **not** the elapsed parallel clock and is **not** a semantic-information or entropy measure.

## 3. NEW NETSIM33 theorem (model-restricted, elementary symbolic proof)

**Theorem.** Every total correct uniform family in the stated model has one **fixed finite deterministic** simulator $U$ with exactly one locally moving two-way **writable work tape** and one locally moving **one-way read-only input tape**, preserving all terminal labels and satisfying

$$
T_U(F)=O_G(M(F)^2), \qquad S_U(F)=O_G(M(F)).
$$

**Proof.** First $U$ reads its source input once, copying $L$ raw bits onto its single physical work tape; it never moves its source head backward. It then interprets the fixed initializer $G$ on an explicitly marked multi-track serialization of virtual tapes and their head positions. Simulating its $B$ multitape steps with a single finite-alphabet work head costs at most $O((L+B)^2)$ real transitions: each virtual step uses a bounded number of scans and, if a new cell is needed, one tape-block shift. Both code and generated data are physically written.

Next $U$ serializes the generated network's complete configuration in one finite-alphabet sequence: local tapes, marked heads, finite control, processor program tables, private input copies, edge table, FIFO contents, staged outgoing messages, current round counter and final output label. Initial description length is $O(B)$. Each of the $K$ local heads visits at most one new cell per round, and each of the $E$ edges creates at most one new bit per round. Hence the entire state, including buffers and indices, is always representable in $O(L+B+KR+ER)=O(M)$ physically visited cells.

For each round, $U$ executes a **processor event** for each vertex, using the old FIFO message and that processor's exact local tape/input symbol and transition-table lookup. It records outgoing bits in a staging region. Only after all local transitions does it execute up to $E$ **delivery events**, appending staged bits to the destination queues for the **following** round. A single event can be performed by $O(1)$ scans of the full $O(M)$ serialized state plus one possible $O(M)$-cost insertion/shift, so each event costs $O(M)$ ordinary single-head transitions. This counts arbitrary generated program lookups, head markers, queue movements, broadcasts and message routing. At most $(K+E)(R+1)$ events occur, giving $O(M^2)$ steps. Initial construction and terminal read/write are absorbed.

Inductively after each completed round, all virtual local states and queues exactly match the simultaneous network semantics, because next-round messages cannot influence the current round. Therefore both output labels, totality and the exact machine/algorithm realization are preserved. QED.

**Scope:** This is an upper simulation, **not** a lower bound. It does not cover one round performing unbounded local computation, arbitrary uncharged multicast payload length, nonuniform hardware, absent setup costs or oracle-like operations. The conservative quadratic exponent may be sharpened for specific graph layouts, such as the previous ring compiler, but no improvement is asserted here.

## 4. A concrete counterexample and the exponent gap

If initializer runtime $B(L)$, processor number $K(L)$, edge count $E(L)$ and elapsed rounds $R(L)$ are all polynomial, so is $M(L)$; the theorem puts the network language in **uniform deterministic P**. Conversely a usual deterministic polynomial-time machine can be simulated by a polynomial-time one-work-tape processor with $K=1$, $E=0$ and polynomial setup. Therefore the *precisely charged polynomial-network model* has the computational power of P, not a new route around uniformity. For 3-SAT, claiming that one of $B,K,E,R$ must be superpolynomial is at least as hard as proving $P\ne NP$; it is not a proved resource dichotomy.

**Falsifier of omitting setup:** Have a uniform initializer brute-force all SAT assignments in exponential time, then place the correct decision into one processor's initial control and halt that processor in one round. The construction has $K=1$ and $R=1$ on **every** SAT and UNSAT instance, but $B$ is exponential. Thus “superpolynomial processor count OR superpolynomial elapsed time” is simply false without charging initialization or forbidding input-dependent preprocessing. This is a uniform, both-label counterexample, not a nonuniform answer table.

Keep **$N=2^n$ explicit MCSP truth-table bits**, arity $n$, and unrelated SAT encoding length $L$ distinct. Suppose for one fixed MCSP threshold $\mu$ a network has $B=O(N^u)$, $K=O(N^a)$, $E=O(N^e)$ and $R=O(N^b)$. The new generic simulator yields

$$
T_U(N)=O(N^{2m}),\quad m=\max\{1,u,a+b,e+b,a,e,b\}\ge1.
$$

CHMY STACS 2021 Theorem 2 (p. 23:3) proves a randomized one-work-tape exclusion $N^{1.99}$ at its **large** parameter $\mu_2$. Any contradiction derived only from this compiler would require $2m<1.99$, hence $m<0.995$, impossible because $m\ge1$. At the distinct **small** $\mu_1$ of CHMY Theorem 1, even assuming an $N^{1.01}$ lower bound, a compiler-based contradiction needs $m<0.505$, likewise impossible. The general conditional fact that a one-work lower bound $N^\alpha$ and a quadratic compiler can only force $M=\Omega(N^{\alpha/2-o(1)})$ has no content beyond built-in $M\ge N$ for $\alpha\le2$.

This **falsifies a proposed proof transfer**, not the existence of a special faster simulation, a direct arbitrary-network lower bound, or a new threshold-preserving reduction. TMR-1/TMR-3 slow-threshold MCSP upper algorithms do not reach CHMY's $s=N^\mu$ for any constant positive $\mu$.

## 5. Primary literature and exact theorem interfaces

| Source/version | Exact theorem, model, input measure and hypotheses | Conclusion and restriction |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, printed p. 23:3 [1] | Ordinary exact **decision** MCSP with **full $N=2^n$ truth table**, threshold $2^{\mu_1 n}$ for some sufficiently small $\mu_1>0$, deterministic **one-way read-only input** and **ONE two-way read/write work tape**; hypothetical exclusion from $\mathrm{DTIME}_1[N^{1.01}]$ | **Conditional** $P\ne NP$; the premise is OPEN |
| Same paper, Theorem 2, p. 23:3 [1] | Same explicit-input/work-tape interface, **randomized two-sided-error** ($\ge2/3$ accuracy); threshold $2^{\mu_2 n}$ for some distinct **large** $\mu_2<1$ | **KNOWN THEOREM** $\mathrm{MCSP}[2^{\mu_2n}]\notin\mathrm{BPTIME}_1[N^{1.99}]$; does not satisfy Theorem 1's parameter |
| Same paper, Theorem 3, p. 23:4 [1] | Oracle queries each of length $N^{o(1)}$, any oracle, threshold $2^{\mu n}$ for $\mu>1/2$; randomized one-work-tape oracle model | **KNOWN THEOREM** excludes some $N^{1+\mu'}$ oracle time; not a no-go for all network algorithms |
| McKay, Murray, Williams, STOC 2019, Theorem 1.2 [2] | **Search** $\mathrm{MCSP}^{A}[s(n)]$ on **full $N=2^n$ table**, $s(n)\ge n$, one-pass streaming with $\Sigma_3\mathrm{SAT}^{A}$ short oracle queries, $\widetilde O(s)$ space and $\widetilde O(s^2)$ update | **KNOWN THEOREM** oracle construction; no free ordinary MCSP decider |
| Same paper, Theorem 1.3 [2] | For some time-constructible $s(n)\ge n$ and $A\in PH$, assume search $\mathrm{MCSP}^A[s(n)]$ has **no** poly$(s)$-space and poly$(s)$-update streaming algorithm | **CONDITIONAL** $P\ne NP$; search/oracle/streaming interface distinct from this network |
| Hennie and Stearns, JACM 1966 [3] | General multitape simulation on **two** work tapes, $O(T\log T)$ | Background only, **not** incorrectly imported as a one-work-tape theorem |

[1] https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; publisher PDF pages 23:3-23:4 visually checked.

[2] https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf ; author PDF visually checked, published DOI https://doi.org/10.1145/3313276.3316396 .

[3] https://doi.org/10.1145/321356.321362 .

## 6. Executed experiment, hostile controls, status and handoff

**Actually executed native CPython 3.13 in one under-25-second invocation:** experiments/tmr/tmr3_network_sim033.py. This independently cross-checks a simultaneous frozen-round reference interpreter against a differently structured serial processor/message interpreter. It uses directed empty, line, ring, star and complete graphs; all $K=1,\ldots,6$; all 16 length-four source strings; six round budgets, plus 300 reproducibly seeded random graphs with $K\le10$, source length 0..15 and up to 18 rounds. Complete states, work-tape content, heads, source-head positions, FIFO queues and all-round transcripts agree. **2,880 exhaustive + 300 random cases, 12,720 checks, zero failed assertions, 41,040 total exhaustive message transmissions.** Raw native output: results/raw/tmr/2026-11-14_1431_TMR3_NETWORK_SIM033_RAW.json. The script uses Python dictionaries, **not** a compiled physical one-work-tape universal interpreter; its empirical findings are only **COMPUTATIONAL**.

Hostile controls include input reread via paid cache, high-degree fanout, arbitrary graph cyclic queues, shared/padded data, source-aware initializer, distinct machine programs, and an initializer that solves the whole problem. Cheap Horn, 2-SAT, Gaussian elimination, bounded-treewidth, products, variable renaming, compact representations and recomputation are all allowed by the simulator: none is charged as compelled SAT difficulty. No ETH, SETH, crypto or oracle hardness assumption enters the unconditional simulation.

**Preflight/reconciliation:** Read the Nov 14 MCSP directive FIRST, then Nov 13 TMR replacement, AGENTS.md, CODEX.md, pnp-research skill, both authentic proof trackers (proof2.txt recovered from complete original Git blob; 1,051,196 chars), canonical main.tex (complete original blob; 2,545,859 chars), latest issue #3 and all five TMR handoffs; original TMR-3/025 and /028 code/raw, peer and Claude/Grok historical controls. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No unauthorized main.tex edit; no schedules changed.

**Next target and peer-review request:** TMR-5 independently audit the $O(M)$ per-event physical single-head implementation for arbitrary FIFO routing and high fanout, and TMR-1 audit uniform input-dependent setup and the exact exponent premises. TMR-2/TMR-4 should seek a genuine post-input-acquisition lower bound for the **entire** small-positive-$\mu$ ordinary MCSP language or an exact model-preserving threshold transfer. One load-bearing lower-bound arrow remains OPEN, so **P versus NP remains OPEN**.
