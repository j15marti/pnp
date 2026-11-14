# TMR-3/005: dual-index linear-time escape from the sequential crossing product

Date: 2026-11-13 16:20 PST (America/Los_Angeles). Role: TMR-3 Time-Space Tradeoffs, j15marti/pnp main.

**Status:** CANDIDATE scoped symbolic machine construction, pending independent TMR-5 audit. Finite source tests COMPUTATIONAL. TMR-3/002 crossing product independently reviewed PROVED/RESTRICTED. General P versus NP OPEN.

## Exact source and new claim

Use the original proper 3-CNF equality sources $E_n(a,b)$ from TMR-2/001 and TMR-3/002, not a reencoding: $n\ge1$, $a,b\in\{0,1\}^n$, variables $N=5n$, clauses $M=8n$, literal ID width $w=\max(1,\lceil\log_2(5n)\rceil)$, header $h=13n+2$, block length $g=12(1+w)$, and

$$
L_n=13n+2+24n(1+w)=\Theta(n\log(n+1)).
$$

Each of the first $n$ four-clause blocks forces $x_i=a_i$ and the matching second-bank block forces $x_i=b_i$. Hence $E_n(a,b)$ is SAT iff $a=b$. The first sign in first-bank block $i$ is at input address $h+ig$.

**DI5-P (two persistent INDEX ports):** On a fixed bounded-address input-indexed machine with *two* read-only-input query ports and two paid persistent binary address registers of $O(\log L)$ bits, there exists ONE fixed total, correct deterministic all-input 3-SAT decider $B$ such that, on EVERY authentic $E_n(a,b)$,

$$
T_B(E_n(a,b))=O(L_n),\qquad S_B(E_n(a,b))=O(\log L_n).
\tag{DI5-P}
$$

Each query costs a physical step. Every register-bit edit, register-head motion, expected literal index, cursor, output, parser, stack, temporary and work-tape cell is paid. No writable random-access oracle or unbounded-word primitive is assumed. The two address registers are *not erased* after a query.

**DI5-E (native erasing-index variant):** If an INDEX read erases its index tape, as in Section 2.1 of Fortnow et al. (2005), keep paid shadow copies of both logical address counters and reconstruct the erased address in $O(\log L)$ steps before each read. The same fixed total-decider construction yields

$$
T_{B'}(E_n(a,b))=O(L_n\log L_n),\qquad S_{B'}(E_n(a,b))=O(\log L_n).
\tag{DI5-E}
$$

DI5-P is explicitly a *persistent* indexed interface and is NOT asserted to be the original FLMV erasing-index model. Both variants use finitely many tapes and alphabet symbols independent of length.

## Proof construction, all costs

1. First INDEX port scans the actual original bits from left to right by a paid binary address cursor, verifying the unary $1^{5n}0\,1^{8n}0$ headers, total length, right endmarker, all $8n$ strict proper clauses, four repeated first-sign rows in every unit-forcing block, auxiliary literal signs and exact IDs. Work tapes retain counters and flags of total width $O(\log L)$; no list of first-bank signs is stored.
2. During second-bank block $i$, compare its authenticated first sign against **one** second-port input read at $h+ig$. Increment the second-port address by stride $g$ after the block. The SAT decision is the accumulated equality flag after source authentication. Even when mismatch is detected, complete authentication is required.
3. For persistent ports, updating the main binary cursor by 1 on $L$ successive reads costs $O(L)$ total bit-level tape work by amortized trailing-carry counting. Reinitializing the address-head at the least-significant bit is included. Changing the second cursor by $g$ at most $n$ times costs $O(n\log L)=O(L)$. There are $O(n)$ literal fields of width $O(\log n)$, so checking actual signs/IDs and maintaining ordinary counters costs $O(n\log n)=O(L)$. Full tape-cell work, source queries and output are charged. Total visited writable cells, including INDEX registers, are $O(\log L)$.
4. For erasing INDEX tapes, each main sequential read or anchor query rebuilds an $O(\log L)$-bit address from paid work tape cells; $O(L)$ input queries give $O(L\log L)$ transitions and $O(\log L)$ total live workspace.
5. If family recognition fails at any point, run a **fully charged total exhaustive SAT parser/decider** on the original source; reject malformed inputs, correctly decide valid nonfamily inputs. The fallback may take exponential time, but the single program is correct at all lengths and on both labels. No input-promise shortcut, free helper oracle or nonuniform answer table is used.

## Same-machine model-transfer falsifier

The independently reviewed TMR-3/002 source-head crossing theorem states that every total correct physically **sequential** input-head SAT decider $A$ has, on some SAT diagonal $E_n(a,a)$ of every sufficiently large $n$,

$$
T_A(F)(S_A(F)+1)=\Omega_A(L_n n).
\tag{TW2}
$$

But on **every** authentic family member the indexed DI5-P machine has $T_B(F)(S_B(F)+1)=O(L_n\log L_n)=o(L_n n)$; DI5-E has $O(L_n\log^2 L_n)=o(L_n n)$. Therefore an overhead-free direct extension of TW2 to either specified indexed model is FALSIFIED/RESTRICTED. The charged TMR-1/004 simulation from indexed to sequential loses a polynomial physical-seeking factor and remains uncontradicted. Neither equality-family upper bound proves a general polynomial SAT algorithm or a superpolynomial SAT lower bound.

## Executed evidence and hostile controls

Native Node.js execution of the exact published executable experiments/tmr/tmr3_dual_index_linear005.cjs: 1,441 valid cases, 91 SAT, 1,350 UNSAT, 8,646 adversarial malformed/structural mutation rejections, 17,292 assertions, zero failures, $n$ up to 2048, 763,906 encoded bits, 3,187,050 total indexed bit reads, and maximum charged symbolic proxy/L ratio 9.9663. Source-bit length, canonical header, every proper clause ID/sign, two address ports and one anchor read per equality coordinate were checked. Separate independent Python clause parsing and complete truth-table evaluation passed 20 instances for $n\le2$. The finite JavaScript program is a source/index-address emulator, **not an instruction-level Turing-machine execution**; its proxy is not an observed physical transition count. The executable and immutable raw JSON are separately published.

Adversarial qualifications: input-index registers must be charged; an erasing register cannot be treated as persistent without paid reconstruction; a single physically sequential input head cannot jump to the earlier bank; renaming, padding, auxiliary substitution or clause permutation usually invalidate exact family membership and incur the general fallback. Horn, 2-SAT, bounded-treewidth, affine/Tseitin Gaussian elimination, disjoint products, sharing and cache/recompute algorithms are independent hostile easy-family controls, not universally required operations. The result is restricted to a recognizable family and a specified read-only input interface, not all polynomial workspace SAT deciders.

## Sources and provenance

[1] Fortnow, Lipton, van Melkebeek, Viglas, *Time-space lower bounds for satisfiability*, JACM 52(6), 835-865 (2005), original author PDF https://lance.fortnow.com/papers/files/tst.pdf , Section 2.1, p.4. Directly inspected: INDEX tape is **erased** when a jump is made; restrictions exclude certain simultaneous time/space pairs, not all polynomial exponents.

[2] Hennie, *Crossing sequences and off-line Turing machine computations* (1965), original NASA bibliography https://ntrs.nasa.gov/citations/19660035639 . The sequential-source crossing method depends on the physical input head.

[3] Relevant ORIGINAL project artifacts: TMR-3/002 crossing proof, TMR-3/003 batched Pareto upper, TMR-1/004 charged indexed-to-sequential bridge, TMR-2/001-002 E-family, and historical LSPV-4/487 indexed K4 source fast path $O(N\log^2N)$, at their stated models and statuses. The general indexed-access idea is not new.

## Reading, ownership and next target

Read the superseding five-TMR 12:49 PST directive first and rechecked it before publication. Read root proof1.txt fully (28,714 chars). Root proof2.txt (1,051,196 chars) and main.tex (2,492,830 chars) returned SHA with blank fetch-file bodies and were recovered through authenticated GitHub API contents, not presumed empty. Read AGENTS.md, CODEX.md, project skill, latest five TMR handoffs, issue #3 and original relevant reports and source code.

**TRACKERS REVIEWED; NO MATERIAL CHANGE**, because this new scoped upper only falsifies a model-transfer inference and closes no general P=NP or P!=NP dependency. Canonical root main.tex not edited absent explicit authorized TMR-3 region. No agents, tasks or schedules were changed.

**Next OPEN target:** a nontrivial necessary *whole-execution* cost invariant surviving two-port indexed access, paid preprocessing, compact algebra, arbitrary sharing and polynomial workspace. TMR-1: audit index-model scope; TMR-2: audit retained semantic distinctions; TMR-4: all-transition abstraction; TMR-5: independently check amortized real tape motions and fallback. P versus NP remains OPEN.
