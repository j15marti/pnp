# TMR-4 / DEFERRED-FINAL-SYMBOL-FALSIFIER003: a uniform all-input counteralgorithm to mandatory post-observation work

**Research date:** 2026-11-13, 14:40 PST (America/Los_Angeles).  
**Owner:** NEW TMR-4 Cost-Sound Abstraction in j15marti/pnp, main.  
**Claim status:** CANDIDATE symbolic constructive theorem pending independent TMR-5 review; finite audit COMPUTATIONAL; unrestricted lower bound OPEN; P versus NP OPEN.

## 1. Single target and falsifiers

**Target:** Attack the team's proposed temporal bottleneck: "after a machine has observed every original input bit, it must perform nonconstant (perhaps superpolynomial) global-consistency work to decide 3-SAT."

**Result:** The temporal order is not necessary. There is ONE fixed correct total deterministic multitape 3-SAT decider which, on EVERY valid encoding in the current length-declared 3-CNF grammar, completes all potentially expensive work BEFORE observing the final original input bit, and then halts after a constant number of physical steps. This does not make the total computation cheap. In fact, the construction may perform two exponential SAT computations before the last physical read.

Falsifiers tested before promoting the claim:
1. An encoded input length cannot be deduced from a strict prefix without reading the last bit.
2. One of the two possible final-bit completions changes the SAT label, invalidating a proposed identical-answer shortcut.
3. Simulating two completions requires uncharged direct access to the real unknown final input bit.
4. A malformed, truncated or overlong input defeats totality or both-label correctness.
5. The construction is mistaken for a polynomial-time SAT algorithm or a lower bound on *total* time.

F1 is ruled out by the declared-length grammar; F2 is realized by a concrete strict-proper-3CNF opposite-label pair, and the algorithm handles it by calculating both labels; F3 is ruled out by paid virtual-tape simulations; F4 is handled by a charged fallback; F5 remains a strict scope firewall.

## 2. Machine, grammar and time phases

Use one fixed deterministic finite-control multitape machine, finite alphabet, one sequential two-way read-only original input head, and a fixed finite number of charged writable tapes. Every head movement, scan, copy, counter update, simulation, lookup, branch and check costs actual transitions. All work cells visited count in peak space. The machine rejects malformed input, accepts exactly encoded satisfiable strict-proper 3-CNF and rejects every valid unsatisfiable one. For its finite experimental emulator only, repeated literals are additionally accepted; the symbolic theorem applies equally with the stricter parser.

The repository's current explicit grammar has a unary header $1^N0\,1^M0$, $M\ge1$ ordered triples of signed literals, and $w=\max(1,\lceil\log_2N\rceil)$ index bits per literal. The exact full encoded length is

$$
K=N+M+2+3M(1+w).
$$

The first two delimiters are encountered strictly before the last encoded bit for every valid input. Hence a physical sequential machine can calculate $K$ using only a proper input prefix and then copy precisely the first $K-1$ bits without observing the last bit. The actual original head can remain parked on the penultimate symbol while other work-tape heads perform arbitrary computation. This is an offline input model, not an uncharged random-access operation.

For a machine $B$ and valid string $x$, let $\tau_B(x)$ denote the physical transition in which the last *previously unobserved original input coordinate* is first read. Define the post-full-observation residue

$$
R_B(x)=T_B(x)-\tau_B(x).
$$

The same-machine total $T_B(x)$ includes all activity preceding $\tau_B(x)$. Endmarker checks count in $R_B$.

## 3. Constructive temporal-deferral theorem (TMR4-TD3)

**Theorem, CANDIDATE pending independent review.** Fix ANY single correct total deterministic multitape binary-input 3-SAT decider $A$ for the stated declared-length encoding (a fixed exhaustive solver is an unconditional example). There exists ONE fixed correct total deterministic multitape decider $B_A$, serving all input lengths, and a machine-dependent absolute constant $c_{B_A}$, such that on EVERY valid encoded 3-CNF input $x$,

$$
R_{B_A}(x)\le c_{B_A}.
$$

All two hypothetical final-bit completions may have different SAT/UNSAT or malformed labels. No assumption that the last bit is irrelevant is needed. If $A$ is polynomial-time on all binary strings, $B_A$ is also polynomial-time, with polynomially charged simulation overhead; this is a conditional closure property, not a constructed polynomial-time SAT solver.

**Construction.**

1. Read and validate the two unary headers and compute the declared $K$ with fully charged counters. If malformed or too short, invoke a fixed exhaustive total parser/decider as fallback.
2. Copy input cells $0,\ldots,K-2$ onto writable tape without ever visiting original cell $K-1$. Let $p$ denote this known $(K-1)$-bit prefix.
3. With the original head still parked, construct the *virtual* strings $p0$ and $p1$ on work tapes and run a paid simulation of $A$ to completion on each. Store their two decision bits $r_0=A(p0)$ and $r_1=A(p1)$ in finite control. Because $A$ is fixed and total, both simulations terminate. They require no observation of the real final input bit. Every simulated step, work tape, scan and copied bit is charged; there is no oracle, advice or supplied proof.
4. Only now move the original input head onto physical cell $K-1$, read its bit $b$, then move once to inspect the right endmarker. If it is the endmarker, output the previously computed $r_b$ and halt. The machine needs only a fixed number of transitions after the final input bit is first observed. If extra trailing symbols are present, invoke the fully charged total fallback, which is allowed to take arbitrarily longer on malformed strings.

The two virtual inputs have exactly the same length and differ solely in their final bits. On a valid actual input $x=pb$, the stored bit $r_b=A(x)$ is the true decision by correctness of $A$; the other simulated result may differ. The input-head scan is physically sequential, and the heavy virtual-input computations are ordinary machine computations performed *before* the final original observation. One fixed finite program implements the entire construction across ALL lengths.

For a standard fixed-tape direct simulation (with extra fixed work tapes), the total time can be bounded schematically by

$$
T_{B_A}(x)\le \operatorname{poly}_A\!\left(K+T_A(p0)+T_A(p1)\right)
$$

and the peak writable space by a fixed polynomial in $K+\max(S_A(p0),S_A(p1))$. An explicit direct fixed-program simulation gives tighter bounds, but no such refinement is used as a lower-bound step. Theorem requires neither polynomial total time nor small space; it preserves polynomial total time **if it already existed**.

**Important edge cases.** The declared-length preamble is part of the chosen encoding, not provided as external length advice. A malformed header, premature endmarker, forbidden identifier, truncation or overlong suffix is handled by the global fallback, preserving all-input total correctness. The constant residue assertion is restricted to VALID full encodings, not malformed strings that trigger late fallback. The checker of a right endmarker and halt still costs transitions, and those are included.

## 4. Strict proper-3CNF opposite-label control, not an irrelevant bit

A stronger falsifier ensures that the final unobserved bit may genuinely affect the label. Construct a proper 3-CNF with $N=14$ variables and $M=17$ clauses. Use four-clause, three-distinct-variable forcing gadgets to enforce $x_0=1$, $x_1=0$, $x_4=1$, $x_5=0$, each with two independent auxiliaries (IDs 6 through 13). Its final clause is

$$
(\neg x_0\lor x_1\lor x_j),\qquad j\in\{4,5\}.
$$

The last literal index is encoded in $w=4$ bits. Its values $0100$ and $0101$ differ ONLY at the final physical input bit; every earlier encoded bit and the header are identical. For $j=4$ the instance is SAT; for $j=5$ it is UNSAT. Every clause is proper, with three distinct variables and within-range indices. The new algorithm precomputes both results and chooses by the final observed bit. Hence it is NOT secretly assuming that the last source bit is logically immaterial.

## 5. Consequence for cost-sound abstraction

The previous TMR-4/001 and TMR-5/001 abstraction charges first source-bit observations and is independently reviewed at its exact scope. TMR-5 proved its maximum initial observation-only potential is at most $L$. TMR-2/002 already falsified a separate expensive post-read phase on an easy equality family.

TD3 is a different, stronger **temporal no-go**: even for an arbitrary hard formula, all potentially costly computation can be scheduled before observing its final original bit. Fix the actual execution of $B_A$ and let $c^*$ be its full concrete state just after its final previously unobserved original bit is read. Only $O(1)$ charged concrete transitions remain before the correct SAT/UNSAT halt. Therefore any cost-sound abstract simulation of the suffix, with the appropriate terminal goal, admits a path of abstract cost $O(1)$ from a state representing $c^*$. Any admissible potential there satisfies

$$
\Phi(a^*)\le O(1).
$$

It is UNSOUND to infer a compulsory superconstant **post-complete-observation** computational charge for EVERY correct 3-SAT decider. This does NOT cap the potential at the initial state, exclude expensive computational steps interleaved with source reads, or bound the *total* time of any algorithm. Indeed, $B_A$ may do two very expensive speculative computations before its final physical read.

**Repair of the research target:** Define unavoidable global-consistency work as a temporal-order-invariant resource charged throughout the entire actual execution, including speculation, processing during acquisition, source copying, recomputation and late checking. Then prove all-step cost soundness for every correct machine and only afterward seek a superpolynomial initial lower-bound potential. Counting compulsory work *after* the first full original observation is not a viable universal approach.

## 6. Falsification controls, execution and exact scope

The independent audit script tests the real binary encoding and a semantic emulator of the two-completion schedule. It is NOT a physical TM simulator, and no measured instruction counts are used to assert the constant residual bound; that part is symbolic. The experimental bounded brute-force implementation throws for $N\ge22$, so it is NOT an all-input total solver. The symbolic $A$ and the fallback are unbounded, total algorithms, not the bounded test driver.

**Actually executed:** OS Node.js 22 on 2026-11-13, one deterministic invocation (no randomness) under 25 seconds. Result: 865 assertion-group input cases, zero failures. Cases: all 84 proper E-family pairs for $n=1,2,3$ (14 SAT/70 UNSAT), 2 strict-proper opposite-label final-bit siblings, 256 generic CNF cases with $N\le4$, 12 malformed controls and 511 binary strings of length at most eight. Across valid audited inputs, 76 test cases had opposite outcomes for the two virtual final-bit completions, demonstrating that the algorithm does not rely on an irrelevant suffix. The finite tests checked semantic equivalence of the deferred choice and ordinary exact brute-force decision, not physical running time or asymptotic limits.

**Exact code:** experiments/tmr/tmr4_deferred_final_bit_audit003.cjs, verified Git blob ddfd91076cc229e3296d43eeb07c37ec779f5ada.  
**Raw:** results/raw/tmr/2026-11-13_1440_TMR4_DEFERRED_FINAL_BIT003_RAW.json, verified Git blob 2036d563f03a760eb12c03f3e831dc201bd9996e.  
The source and JSON byte counts (4981 and 254) match the local files that were executed/generated. No full repository preflight, LaTeX compilation, or physical TM state execution was performed. This is a model-exact symbolic construction supported by bounded semantic tests, awaiting independent review.

## 7. Corpus, duplication and proof-chain ledger

Read FIRST the superseding 2026-11-13 12:49 PST directive; read full root proof1.txt (28,714 characters) and recovered nonempty proof2.txt Git blob (1,051,196 characters), current root main.tex Git blob (2,484,173 characters; TMR-1..5 ownership regions), AGENTS.md, CODEX.md, repository research skill, current issue #3 (through TMR-3/002), current TMR-1..5 handoffs, TMR-4/001, TMR-2/002, TMR-3/002, TMR-5/001, and the historical LSPV-1/589 and LSPV-5/462 distinctions cited in TMR-4/001. Scoped literature: Cousot/Cousot 1977 abstract simulation; Buhrman/de Wolf 2002 decision-tree complexity; Fortnow/Lipton/van Melkebeek/Viglas 2005 SAT time-space lower bounds. None proves TD3 by itself; its construction is self-contained. The precise last-bit postponement formulation has not been established as new relative to all complexity literature, and no priority is claimed.

**Novel relative to current TMR main:** TD3 generalizes the E-only incremental-processing falsifier to a paid two-completion construction for EVERY valid length-declared encoded 3-CNF, and supplies a genuine opposite-label final-symbol pair. It does not negate the prior valid first-observation potential, the TMR-3 two-way crossing theorem within its physical-access model, or any published restricted SAT time-space theorem.

**Status and dependency:** TMR4-TD3 CANDIDATE pending TMR-5 hostile independent proof review; 865 finite cases COMPUTATIONAL. No unrestricted post-acquisition computation lower bound; no P!=NP theorem; total time lower-bound arrow OPEN. Proof1.txt and proof2.txt fully recovered and reviewed; no material P1/P2 node closure, **TRACKERS REVIEWED; NO MATERIAL CHANGE**. Root main.tex TMR-4 region is authorized and should state only the candidate, not a theorem promotion. Preserve all non-TMR-4 bytes.

## 8. Primary literature and project originals

[1] P. Cousot and R. Cousot, "Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints," POPL 1977, 238-252. Author-hosted bibliography and summary: https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml . Provides abstract execution methodology; not a SAT lower bound.

[2] H. Buhrman and R. de Wolf, "Complexity Measures and Decision Tree Complexity: A Survey," Theoretical Computer Science 288(1), 2002, 21-43. Author-hosted preprint: https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf . Covers input-query/decision-tree complexity; not unrestricted machine runtime.

[3] L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, "Time-Space Lower Bounds for Satisfiability," JACM 52(6), 2005, 835-865. https://doi.org/10.1145/1101821.1101822 . Exact random-access small-space exclusions, not all polynomial-time all-space separation.

[4] Project TMR-2/002, research/agents/tmr-2/2026-11-13_1420_TMR2_ONE_SWEEP_MATCHING_UPPER002.md; TMR-3/002, research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md; TMR-4/001, research/agents/tmr-4/2026-11-13_1336_TMR4_OBSERVATION_HITSET001.md; TMR-5/001, research/agents/tmr-5/2026-11-13_1348_TMR5_OBSERVATION_OPTIMALITY_REVIEW001.md.

**ONE next objective for TMR-2/3/4/5:** devise a temporal-order-invariant compulsory computational charge beyond at-most-$L$ first-read observations, prove cost underestimation for EVERY real machine transition and test against speculative two-completion simulations, Gaussian elimination, and low-treewidth dynamic programming. TMR-5 should independently construct/replay $B_A$ and audit exactly how the real input head avoids its final cell until both virtual simulations finish.

END_OF_REPORT::TMR4_DEFERRED_FINAL_SYMBOL_FALSIFIER003::2026-11-13_1440_PST
