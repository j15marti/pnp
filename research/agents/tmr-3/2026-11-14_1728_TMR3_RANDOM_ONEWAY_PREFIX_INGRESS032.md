# TMR-3/032: A randomized one-way MCSP prefix-ingress theorem and a network-model firewall

**Pacific timestamp:** November 14, 2026, 17:28 PST. **Role:** TMR-3, Time-Space Tradeoffs. **Scientific status:** ONEWAY-PREFIX46 is an elementary **PROVED/RESTRICTED** conditional on the physical one-way-input model, pending TMR-2/TMR-5 independent review. Finite examples are **COMPUTATIONAL** only. Every inference to P versus NP is **OPEN**.

## 1. What is genuinely new

The October 20 QUERY-COVERAGE-FIBER27 already showed that a deterministic exact source-bit algorithm must read $N-O(N^\mu\log N)$ bits on an MCSP YES source. TMR-3/031 improved a randomized *indexed* source-bit model to $\Omega(N^{1-\mu})$ expected distinct queries on each YES source; TMR-5/028 strengthened its coefficient.

The new result is the **near-complete physical source-ingress probability on every YES source for randomized one-way-input machines**, allowing arbitrary writable memory. A source head advancing only one position per physical transition induces a different, stronger lower bound than an indexed-bit oracle. New model synthesis: the prior TMR-3/030 event-frontier contradiction inequalities have no overlap with **sequential source-ingress** networks, although they remain potentially applicable to their originally declared charged *indexed-source* network model.

This proves no post-ingress computation lower bound and no superlinear lower bound.

## 2. Exact model and one-way theorem

Let $N=2^n$ be a complete truth table on $n$ Boolean inputs. Let $s=\lfloor N^\mu\rfloor$, with fixed $0<\mu<1$. Let $\mathcal{Y}_{n,s}$ be the ordinary exact MCSP YES set of tables computable by at most $s$ gates from a finite AND/OR/NOT fan-in-two basis, with named input wires, constants and arbitrary fanout. The generous description count is
$$
|\mathcal Y_{n,s}|\le D(n,s):=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$
No Gap-MCSP promise, MKTP measure, succinct-input assumption, or circuit-minimization oracle is involved.

Let $A$ be a fixed total randomized finite-alphabet machine correct on **all** complete truth tables, with at most $\delta<1/2$ two-sided decision error for every input and every length. The sole source interface is one ordinary locally moving, left-initialized, **one-way read-only input head**: each physical transition advances its head by at most one source position, or pauses. All tape transitions, reads, computation, caches, and output steps count as time. $A$ may have any fixed finite number of writable tapes with arbitrary space, may know $N,n$ initially, and may use an unbounded random tape or equivalent coin flips. Only source-specific free advice, prepositioned input heads, and indexed reads are excluded.

Set
$$
h(n)=\lceil\log_2N\rceil+2,\qquad
m(n)=\lceil\log_2D(n,s)\rceil+h(n),\qquad
b(n)=N-m(n).
$$
For sufficiently large $n$, $1\le b(n)<N$, and
$$
m(n)=O_\mu(N^\mu\log N)=o(N).
$$

**ONEWAY-PREFIX46.** On every YES table $x\in\mathcal Y_{n,s}$, let $R_A(x)$ be the event that, in the run with random coins $\rho$, the source head reaches position $b(n)$, the first position after the first $b(n)$ source bits. Then
$$
\boxed{\Pr_\rho[R_A(x)]\ge1-2\delta-(1-\delta)2^{-h(n)}.}
$$
If $T_A(x,\rho)$ is the actual number of physical transitions, then on **the same randomized execution**
$$
\boxed{\mathbb E_\rho T_A(x,\rho)
\ge b(n)\big(1-2\delta-(1-\delta)2^{-h(n)}\big)
=(1-2\delta-o(1))N.}
$$
In particular, at $\delta=1/3$ the expected physical runtime on every YES input is at least $(1/3-o(1))N$, with no workspace restriction. No fixed finite-N claim is made when $m(n)\ge N$; the asymptotic theorem is explicitly only for sufficiently large $n$.

**Proof.** Fix any MCSP YES table $x$. Let random $Y$ agree with $x$ on the first $b=N-m$ source positions and have a uniformly sampled final $m$ bits. There are $2^m$ possible completions, of which at most $D$ are MCSP YES. Therefore
$$
\epsilon_x:=\Pr[Y\in\mathcal Y_{n,s}]\le D/2^m\le 2^{-h}.
$$
Couple the executions $A(x;\rho)$ and $A(Y;\rho)$ with **identical randomness**, control, and initial writable configurations. Until a source head first reaches position $b$, all source symbols observed and all resulting adaptive state transitions are identical. If the run on $x$ halts before this event, the run on $Y$ halts identically. Thus
$$
\Pr[A(x)=YES]-\Pr[A(Y)=YES]\le\Pr_\rho[R_A(x)].
$$
Correctness yields $\Pr[A(x)=YES]\ge1-\delta$. Averaging correctness on all $Y$ gives
$$
\Pr[A(Y)=YES]\le\delta(1-\epsilon_x)+\epsilon_x
\le\delta+(1-\delta)2^{-h}.
$$
Subtract to prove the first inequality. On the event $R_A(x)$, the standard one-way source head has taken at least $b$ charged moves, and hence at least $b$ physical transitions. Taking the expectation on that same run proves the second inequality. Finally, $\log D=O(s\log(n+s))=O(N^\mu\log N)$, giving $m=o(N)$. No same-machine resource borrowing or state-capacity inference is used. QED.

**Near-sharp ingress coefficient.** At $\delta=1/4$, a uniform random pair of bits chooses: immediately YES with probability $1/4$, immediately NO with probability $1/4$, otherwise perform a full sequential scan followed by any correct exact (possibly slow) MCSP computation with probability $1/2$. Its worst-case error is $1/4$ on each label, and its input-head reach probability is exactly $1/2=1-2\delta$. This demonstrates asymptotic tightness of the *ingress probability coefficient* under these correctness assumptions, but says nothing about tightness of the total decision-time cost.

## 3. Network transfer and precise failed implication

Suppose a uniformly specified network of any number of locally computing processors obtains its source exclusively through **one common sequential physical input stream** initially at position zero, or through separately initialized local streams whose heads each advance at most one cell per elapsed time unit. A source-dependent constructor must use the same charged stream or previously charged messages. All source reads, copies, messages, preprocessing, temporary buffers, caching, and switching must be paid. Until the stream frontier passes $b$, a coupling of the same random choices across two shared-prefix sources makes the complete network computation identical. For any correct $\delta$-error network on ordinary MCSP, on every YES source and with probability at least $1-2\delta-o(1)$, physical source access must advance to the final $o(N)$-bit suffix. Hence at least $b$ source-ingress events and at least $b$ elapsed steps occur on those runs if one source frontier advances at most one cell per elapsed step.

The conclusion fails for networks with charged-but-arbitrary **indexed** reads from a globally stored input, multiple pre-positioned heads, or free source-dependent constructor output. These are different source access models, not ways to evade the proof on its stated model.

TMR-3/030, NETFRONT39, derives, using Cheraghchi et al. Theorem 2 at the **high** MCSP circuit threshold $\mu_2$, a sufficient contradiction whenever (using $a,b,c,e$ now as **resource-growth exponents**, not the prefix length)
$$
c<1.99,\qquad e+\max(1,a,b,e)<1.99.
$$
Here $E_{\max}=O(N^e)$ is the all-input worst-case number of paid events, $p=O(N^a)$ processors, description length $B=O(N^b)$, and constructor cost $C=O(N^c)$. For an actual **sequential-ingress** network, the new theorem forces $E_{\max}=\Omega(N)$ even for randomized correct networks because an MCSP YES input exists and the reach event has constant probability. Thus any valid polynomial upper exponent $e\ge1$, and the sufficient NETFRONT39 inequality has left-hand side at least $2$. Its contradiction corridor $e<0.99$ is **vacuous for this sequential variant**.

This does **not** refute NETFRONT39 for its original charged *indexed-read* network, and does **not** prove that an alternative, more efficient physical simulator is impossible. Its generic serialization upper-bound expression $O((E+1)M)$, with $M=\Omega(N)$, being at least quadratic as an expression is not a lower bound on the actual runtime of any optimal simulator.

The known near-linear source-ingress charge is below Cheraghchi et al. Theorem 1's **$N^{1.01}$** one-way-input, one-work-tape lower-bound premise at its distinct *small* threshold $\mu_1$. No result here transfers to unrestricted uniform multitape 3-SAT on source descriptions of bit length $L$.

## 4. Primary-source theorem and parameter ledger

| Primary paper and exact theorem | Input measure, problem, model and threshold | Hypotheses and exact conclusion | Use here |
| --- | --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS **2021**, Theorem 1, printed p.23:3 [1] | Full $N=2^n$-bit ordinary MCSP table, $s=2^{\mu_1n}$ for a sufficiently small fixed $\mu_1>0$, deterministic one-way read-only input plus **one** two-way work tape | **Conditional:** its absence from deterministic $O(N^{1.01})$ one-work-tape time implies $P\ne NP$ | The small-threshold antecedent is **OPEN**. ONEWAY-PREFIX46 gives only linear cost. |
| Same STACS 2021, Theorem 2, printed p.23:3 [1] | Full ordinary MCSP, a **different larger** constant $\mu_2$ close to 1, randomized bounded-error one-way input plus one work tape | **KNOWN THEOREM:** exclusion from two-sided-error time $O(N^{1.99})$ at that different threshold | Used only in NETFRONT39 audit. Do not transfer $\mu_2$ to $\mu_1$. |
| McKay, Murray, Williams, STOC **2019**, Theorems 1.2 and 1.3 [2] | Streaming **search** $MCSP^A[s(n)]$, $s(n)\ge n$, $N=2^n$ table, poly-hierarchy oracle and $\Sigma_3SAT^A$ queries | Oracle-assisted streaming search construction in Theorem 1.2; a specifically quantified simultaneous poly($s$) update-time and memory failure for some $A\in PH$ would imply $P\ne NP$ in Theorem 1.3 | Not ordinary decision MCSP; no claimed input/source or threshold transfer. |

No unconditional hardness assumption is smuggled in. The arbitrary source 3-SAT encoding size $L$ is separate from $N$ and $n$, and a succinct $L$-bit circuit is never equated to its $N$-bit truth table without paying construction.

## 5. Historical original work and falsification controls

| Path, earlier result | Relation to this run |
| --- | --- |
| research/main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md | **PRIOR** near-full deterministic YES-path query-coverage theorem, does not provide randomized physical one-way reach probability. |
| research/main/2026-10-20_0548_MAIN_CONDITIONED_HARD_SPARSE_QUERY7.md | **PRIOR** randomized hard sparse source lower bound in paid **indexed** bit-query model. |
| research/agents/tmr-3/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK_SOURCE_FRONTIER031.md, experiments/tmr/tmr3_sharp_sparse_network043.js, original corresponding raw JSON | **PRIOR** $\Omega(N^{1-\mu})$ randomized indexed-source expected reads on every YES source. New theorem adds the physically sequential-head restriction. |
| research/agents/tmr-3/2026-11-14_1533_TMR3_HIGHMU_NETWORK_EVENT_FRONTIER030.md, experiments/tmr/tmr3_network_event_frontier039.py, original corresponding raw JSON | **PRIOR** high-$\mu_2$ indexed network event contradiction frontier. New sequential-scope audit identifies its vacuous corridor only in that altered access model. |
| research/agents/tmr-1/2026-11-14_1605_TMR1_SHORT_HEADER_CONSTRUCTOR_SIMULATION030.md and research/agents/tmr-1/2026-11-14_1704_TMR1_LOCAL_PREFIX_PF_COMPOSITION031.md | **PRIOR** restricted physical simulation/circuit compilation upper bounds; not MCSP solver time lower bounds. |
| research/agents/tmr-2/2026-11-14_1618_TMR2_RANDOM_SHARED_SPARSE_MINIMAX031.md; research/agents/tmr-5/2026-11-14_1650_TMR5_LOCALHEAD_AND_SPARSE_TAIL_AUDIT028.md | **PRIOR** source-oracle and hypergeometric randomized results; source access model differs. |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; 2026-10-28_1326_CLAUDE_TPORT-0001.tex; 2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex | **PRIOR** crossing-sequence, portfolio and direct-product limitations, not an unrestricted SAT transfer. |
| research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex | **PRIOR** compact affine/hash summary label collisions; source representations are not compulsory. |

**Hostile controls.** Tested constants, input projections, and one-gate Boolean functions in finite exact tables. A zero-table YES and its last-bit singleton perturbation can be distinguished with **one** prepositioned or random-access source-bit query, showing the new linear movement is false under free random access. Preloaded source-dependent work tape or source-specific advice likewise breaks the exact stated assumptions. Horn, 2-SAT, XOR/Gaussian elimination, bounded-treewidth DP, independent products, shared computations, variable renaming, auxiliary variables and padding may be easy source SAT controls; the theorem does not claim they incur exponential work. This matters because $N$ is an *explicit MCSP truth table* rather than a compact SAT encoding of length $L$.

## 6. Executions, evidence, provenance and status

**Actually executed V8:** The exact published source experiments/tmr/tmr3_oneway_prefix046.js was executed using a V8 dynamic function with its Node hashbang omitted solely for invocation; its body and checks were unchanged. Original immutable raw JSON is results/raw/tmr/2026-11-14_1728_TMR3_ONEWAY_PREFIX046_RAW.json. It passed **273 checks, zero failures, 8,384 exhaustive suffix-completion comparisons** for $n\in\{3,4,5\}$, $s\in\{0,1\}$, plus 12 rational parameter-grid budget comparisons for $n\in\{16,32,64,128\}$ and $\mu\in\{1/4,1/2,3/4\}$. The generous circuit-count overestimate is vacuous at $n=16,\mu=3/4$ and becomes nonvacuous at $n=32$; this finite exception was not hidden. Runtime and semantics are finite experimental checks, not native finite-alphabet TM proof. The original general proof is above.

**Local-only independent native CPython:** Additional separate exact-integer/Fraction script executed with 359 checks, zero failures, but its source/raw were not uploaded and are not treated as published evidence. No general physical network compiler or superlinear computation benchmark was executed.

**Preflight:** The Nov14 MCSP directive was read FIRST and rechecked, then the Nov13 TMR replacement; AGENTS.md, CODEX.md, the repo pnp-research skill; newest five TMR handoffs; latest issue #3 through TMR-1/031; original TMR, Claude, indexed-query, affine/circuit and raw/code files. Entire original proof1.txt (28,714 chars), full authentic proof2.txt Git blob (1,051,196 chars) and canonical root main.tex Git blob (2,545,859 chars) were reviewed. An empty GitHub contents response for main.tex was not treated as an empty document.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and TMR-5-owned main.tex remain unchanged; schedules untouched. New result restricted, not promoted to an unrestricted separation or main proof chain.

## 7. Peer request and next target

TMR-2 independently audit the identical-coin randomized prefix coupling and its leading coefficient, especially early termination. TMR-5 verify the **indexed versus sequential** source-access distinction in NETFRONT39 and ensure a faster alternative serializer is not falsely excluded. TMR-1 and TMR-4 verify that a charged source-specific constructor or additional initial heads require a new model bridge.

**Concrete next target:** a genuine **post-ingress** $\omega(N)$ work lower bound at the specific small $\mu_1$ ordinary MCSP parameter on one-way-input plus one-work-tape machines, or a cheap fully charged counterexample to an intermediate proposed invariant. Do not repeat the simple input-scan argument.

## References

[1] Cheraghchi, Hirahara, Myrisiotis, Yoshida (2021), *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021, Theorems 1-2, printed p.23:3. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] McKay, Murray, Williams (2019), *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019, Theorems 1.2-1.3. https://doi.org/10.1145/3313276.3316396

END_OF_REPORT::TMR3::032::2026-11-14_1728_PST
