# TMR-3/017: physically charged moving-window caches interpolate one-head multihead simulation time and space

**Pacific timestamp:** 2026-11-14 04:40 PST (America/Los_Angeles). **Owner:** TMR-3 Time-Space Tradeoffs, j15marti/pnp main. **Claim status:** CANDIDATE/RESTRICTED pending independent TMR-5 and TMR-1 mathematical audit. **Executed evidence:** COMPUTATIONAL. **General 3-SAT lower bound:** OPEN.

## 1. Exact claim and model

Let A be any ONE fixed finite deterministic total uniform multitape machine with h>=1 independently locally moving read-only heads on the SAME immutable L-bit encoded input, any fixed finite number of ordinary writable work tapes and alphabets, and charged one-cell head moves and writes. Read-only endmarkers occupy positions 0 and L+1. Every tape head moves at most one cell per physical transition. A's control and output distinguish SAT, UNSAT and MALFORMED when A is a total correct 3-SAT classifier. T_A(x) is its actual transition count; S_A(x) is the total number of visited writable work cells on that same run. Machine A can have arbitrary algebraic representations and arbitrary polynomial workspace.

Choose any fixed computable integer cache-window function R(L) satisfying 1<=R(L)<=L+2 and constructible in O(L+2) standard local-tape transitions with O(R(L)+log(L+2)) visited writable cells. Examples include a constant 1, a logarithmic window, R(L)=ceil(sqrt(L+2)), and the entire L+2 cells. Then there is ONE fixed total deterministic machine B_{A,R} using ONE locally moving read-only input head and a fixed number of ordinary work tapes, exactly preserving every simulated A transition and both decision labels, for which, on every x,

$$
T_{B_{A,R}}(x)
\le c_A\left((L+2)+(T_A(x)+1)\left[1+\frac{L+2}{R(L)}\right]\right),
$$

$$
S_{B_{A,R}}(x)
\le S_A(x)+c_A\left(R(L)+\lceil\log_2(L+2)\rceil\right).
$$

The constant depends on the fixed source machine A, window constructor and tape conventions, not on L or x. The two displayed charges refer to the SAME simulator B and the SAME x, not independently optimized programs or inputs. These are simulation **upper bounds**, not time necessities for SAT. Full generic TM microcode was constructed symbolically, not emitted as a finite compiled transition table.

For a fixed rational 0<=alpha<=1 and R(L)=Theta((L+2)^alpha), a fixed computable choice, this provides

$$
T_B=O_A\!\left(L+2+(T_A+1)(L+2)^{1-\alpha}\right),\quad
S_B=S_A+O_A\!\left((L+2)^\alpha+\log(L+2)\right).
$$

In particular, R=Theta(sqrt L) yields O_A(L+sqrt(L) T_A) time and O_A(sqrt L+log L) extra work space; R=L+2 yields O_A(L+T_A) time with O_A(L) extra space. R=1 recovers the O_A(L T_A) bound at O_A(log L) scratch, comparable to the corrected TMR-3/016 fetch method. These are achievable model-transfer choices, not lower bounds or a Pareto-optimality claim.

## 2. All-transition source-port simulation and cost accounting

Maintain h separate actual writable cache tapes, each containing R consecutive source symbols from a physical contiguous source interval [base_i,base_i+R-1], including source endmarkers when inside the interval. The head of cache tape i sits on the cell representing A's virtual input-head position p_i. This is paid work memory: exactly hR cache cells can be simultaneously live, plus O_A(log(L+2)) work for binary bases/indices, counters, source-length discovery and finite-state dispatch. The original A work tapes remain present, unmodified except for precisely simulated transitions.

1. With the ONE actual source head, scan to the right endmarker and back, charge every head movement and binary-length-counter update. Compute R(L), allocate the fixed number h of cache tapes, and load an initial window for every virtual p_i.
2. In ordinary simulated A steps, read source symbols from the actual current cache work-head cells. Apply A's finite transition rule with all original A work tapes, controls, outputs, physical head moves and writes. Move each cache head at most one cell to follow the corresponding virtual read-only head. A's simulated source input is immutable and its entire ordinary writable state is preserved. No source-array lookup or oracle occurs in the mathematical compiler.
3. When virtual head i would leave its cache interval, perform a paid **reload before the next logical A step**. Choose the new length-R interval centered on p_i as far as the real endmarkers permit. Move the original input head from its present physical position to the new interval start by at most L+1 local moves; read and cache R consecutive symbols from the original current input cell, writing each to cache tape i as that cache's physical head advances. Move the cache head to p_i's new offset, and update its O(log L)-bit base and offset representation with paid binary arithmetic. Other cache tapes and A's work tapes are retained, not recomputed.
4. Preserve A's SAT/UNSAT/MALFORMED halt label and halt. For any x, A's totality implies B's totality because every reload and each original logical transition terminate.

For R>=2, a freshly centered window has distance at least floor((R-1)/2) to every exit-able end; at a clamped left or right edge, the corresponding physical endmarker prevents exit. Hence a further reload of that SAME virtual head requires at least floor((R-1)/2)+1>=R/2 locally moving virtual-head steps. For R=1 the trivial separation is one step. Since each head moves at most once per A transition,

$$
N_{\rm reload}(x)\le h\left(1+\frac{2T_A(x)}{R}\right)
$$

up to harmless integer rounding. Each reload costs O_A(L+2): original source travel O(L), cache writing and head positioning O(R), base/index update O(log L). Each simulated A transition without reloading costs O_A(1) because h and the tape count are fixed. Initial discovery and h initial fills cost O_A(L+2). Summing the partition of actual costs yields exactly the claimed upper time envelope and visited-workspace footprint. This counts every source reread, cache write, head restoration, preprocessing and output. Repeated or shared cached symbols are not charged as fresh input reads, but every cache-tape read is an actual work-tape operation.

The choice of cache R is NOT advice: the entire machine B_{A,R} is fixed before x, and the specified R(L) is calculated uniformly from the physical input length. A source symbol enters a cache only through a charged current-cell original-input read. For all R, no virtual head jumps, no unbounded-word access, and no external truth table occurs.

## 3. Fresh computational audit and hostile controls

New exact standalone hosted-V8 JS was **actually executed** and saved at experiments/tmr/tmr3_window_cache_onehead017.cjs; its output is immutable raw data results/raw/tmr/2026-11-14_0441_TMR3_WINDOW_CACHE017_RAW.json. The emulator has THREE virtual source heads, three physically tracked writable cache heads, one original physical source head. Every cache fill reads only from that physical head's **current** source position. Numeric access to the source in the direct verifier computes expected symbols, not simulator input. Address updates are represented by conservatively charged O(log L) micro-operation ledgers; they are **not** compiled into binary-counter instruction tables. The full arbitrary-A generic finite transition compiler remains unexecuted.

**Executed finite controls:** all binary x at lengths 0 through 8; longer deterministic source fixtures at L=15,31,32,63,64,127,255,511,1023; window regimes R=1,2,3,sqrt(L),quarter-source,half-source,whole-source; four distinct direction/state policies including reversals and data-dependent moves. Actual observations:

| Counter | Executed result |
|---|---:|
| Complete checked traces | 11,636 |
| Simulated multihead logical steps | 872,256 |
| Independently compared cached symbols | 2,616,768 |
| Current-cell original source reads | 2,062,686 |
| Physically charged original source-head moves | 81,279,763 |
| Window reloads | 911,339 |
| Charged cache work-head moves | 3,688,034 |
| Total conservatively instrumented operations | 173,875,577 |
| Failed assertions | 0 |

A mechanical upper-envelope check gave measured maximum ratio 35.137 against the advertised expression before a conservative fixed multiplier 600; this is evidence for the instrumented code only, not a proof of the universal model compiler. The original source-position bug from TMR-3/016 identified by TMR-5/015 is NOT repeated: every fresh actual source read occurs at the tracked input-head position before repositioning.

**Hostile algorithms and transfer checks:** Horn, 2-SAT, XOR/Gaussian, bounded-treewidth, disjoint products, auxiliary variables, compact circuits, shared subcomputations and arbitrary preprocessing are allowed in A, since no A-internal representation is inspected. They are symbolic controls, **not** executed SAT benchmarks in this run. Adversarial virtual-head motion near cache boundaries is included in the finite movement policies. Input-length exponential padding is explicitly NOT used. This simulator can retain up to Theta(L) source information; there is no claim that such retention is compulsory for a SAT solver.

## 4. Primary prior art at its real scope and original project evidence

- Fortnow, Lipton, van Melkebeek and Viglas, **Time-space lower bounds for satisfiability**, JACM 52(6):835-865 (2005), https://doi.org/10.1145/1101821.1101822 . Their stated random-access SAT nonmembership is for simultaneous T=n^c and S=n^d with c<the golden ratio and a suitable d>0, NOT every polynomial workspace, NOT the new cache theorem.
- Hong and Kung, **I/O complexity: The red-blue pebble game**, STOC 1981, pp. 326-333, https://doi.org/10.1145/800076.802486 . Their game models I/O for specified computational dependencies such as FFT and conventional matrix multiplication, NOT an unrestricted 3-SAT processing DAG; no game lower bound is imported here.
- Borodin and Cook, **A time-space tradeoff for sorting on a general sequential model of computation**, SIAM J. Computing 11(2):287-297 (1982), https://doi.org/10.1137/0211022 . Their TS=Omega(N^2/log N) lower bound concerns sorting, not SAT; no implication is borrowed.
- Previous ORIGINAL team construction: TMR-3/016 source-fetch model transfer at research/agents/tmr-3/2026-11-14_0334_TMR3_AMORTIZED_POPCOUNT_ONEHEAD_BRIDGE016.md. TMR-5/015, research/agents/tmr-5/2026-11-14_0353_TMR5_PHYSICAL_FETCH_REDTEAM015.md, independently caught its off-current-cell executable read and supplied the correct read-before-return physical repair. This run adds the **variable-sized retention vs reload interpolation**, not a recycled binary countdown.
- TMR-3/002, research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md, and TMR-3/008, research/agents/tmr-3/2026-11-13_1935_TMR3_BATCH_LOCALITY_TRADEOFF008.md, already study SAME-INPUT crossing TS tradeoffs on recognized equality-3CNF sources. Their polynomial-strength restricted lower bounds and specialized batch caches must not be labeled general SAT hardness. This run's cache simulator is a generic **multihead model translation**, separate from the equality-source-specific cache.

## 5. Exact all-polynomial-exponent gap and next peer obligations

The new upper frontier does not exclude any pair (T_A,S_A) for a correct A, because it constructs an alternative machine B. For a hypothetical polynomial T_A=O(L^k), S_A=O(L^s), each fixed rational alpha yields a polynomial B with T_B=O(L^{max(1,k+1-alpha)}) and S_B=O(L^{max(s,alpha)}+log L). Neither this nor FLMV's small-space exclusions yields the required all-machine, all-k contradiction. Even an unconditional TS>=Omega(L^2/log L) restricted crossing inequality is compatible with T=O(L), S=O(L). The same-machine inequality S<=O(T) does not turn this upper simulation into an obligatory superpolynomial processing cost. Every unrestricted separation arrow remains **OPEN**.

**Independent peer target:** TMR-5 should formally inspect the clamped-window reload spacing, literal current-source-cell reads, physical contiguous cache-tape layout and any extra hidden head-index operations; TMR-1 should verify fixed-program R(L) uniformity. TMR-4 can encode reloads as actual all-transition abstract paths, not free oracle edges. TMR-2 should test whether any compulsory distinction cost survives the R=L whole-source retention option.

**Repository preflight:** governing 2026-11-13 12:49 PST directive first and rechecked (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4); root proof1.txt fully read (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), root proof2.txt fully recovered via authentic Git blob (1,051,196 chars, SHA 930c5eeddafce656717f28055a7a755f44737c), root main.tex fully recovered via authentic Git blob (2,530,965 chars, SHA 91b4e582c16cb7f60c9aa1ea2aebf09cd4caa2c6), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, all newest five handoffs, latest issue #3, ORIGINAL TMR-3/002,/008,/016 and TMR-5/015. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Do not rewrite unreadable contents or edit canonical TMR-5-owned main.tex. No tasks or schedules modified. Exact tool-executed code/raw evidence and report publications are independently read back on main; no native Node execution, generic TM compiler, or LaTeX compilation was run.

**Next target:** a physical source/cache tradeoff lower bound with an adversarial all-machine SAT obligation rather than a chosen multihead simulation interface. Preserve the actual R=L cached-copy algorithm and all alternative source encodings as falsifiers.

END_OF_REPORT::TMR-3/017::2026-11-14_0440_PST
