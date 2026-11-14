# TMR-3/028: Raw-bit-cache single-head MCSP audit and annotated-stream space frontier

**Pacific timestamp:** 2026-11-14 13:27 PST (America/Los_Angeles). **Role:** TMR-3 Time-Space Tradeoffs. **Status:** RAWSCAN28 PROVED/RESTRICTED symbolic model-specific upper construction, independently auditing TMR-1/027; physical micro-rotations COMPUTATIONAL. ANNO28 PROVED/RESTRICTED conditional on a literal upfront input-arity header. No unrestricted P-vs-NP implication. P versus NP OPEN.

## 1. New result relative to original work and prior-work ledger

TMR-1/027 already reported an ordinary exact MCSP enumerator on one work tape with time $N D(n,s)\operatorname{poly}(n+s)$, using **indexed source records** and $O(N\operatorname{poly}(n+s))$ writable cells. The genuinely new result here is an **independent raw-bit-only tape compiler** reducing its peak visited work cells to $N+O(n+s\log(n+s+2))$, while retaining the same time exponent; and a distinct, fully chargeable **header-known streaming construction** with $D(n,s)\operatorname{poly}(n+s)$ work cells, sublinear for slowly growing thresholds. These are upper bounds, not unconditional lower bounds. No claimed novelty as a general circuit-enumeration discovery.

| Original path | Prior contribution and preserved scope |
| --- | --- |
| `research/agents/tmr-1/2026-11-14_1307_TMR1_MCSP_GROWING_THRESHOLD_ENUMERATION027.md` plus `experiments/tmr/tmr1_slowthreshold030.py` and raw output | PRIOR indexed-record one-tape upper bound, symbolic, finite semantic proxy; this report independently tightens space |
| `research/agents/tmr-3/2026-11-14_1228_TMR3_MCSP_MOBILE_HEADER_FUSION027.md`, original runner and raw evidence | PRIOR annotated-input repetition simulator; full-output early-header retention bound; neither provides this candidate-parallel streaming compiler |
| `research/agents/tmr-3/2026-11-14_1028_TMR3_MCSP_POLY_RING_SERIALIZATION025.md` | PRIOR growing-ring serial upper simulation; quadratic full-input barrier is about that compiler, not all programs |
| `research/agents/tmr-4/2026-11-14_1243_TMR4_LENGTH_BLIND_FIXED_GATE_COFACTOR028.md` and TMR-5/024 original report | PRIOR compact length-blind fixed-cap or bounded-schedule algorithms; no unbounded $N^\mu$ threshold claim |
| `research/agents/tmr-2/2026-11-14_1221_TMR2_ODOMETER_CODE_CERTIFICATE027.md` | PRIOR threshold-zero logarithmic-space one-tape algorithm; high YES query depth is not decision time |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`, TMR-4/023 Walsh and TMR-5/020 moment counterexamples | Historical restricted crossing-sequence, portfolio, failed shortcut and algebraic-summary controls, not a multitape SAT bridge |
| `GROKPROOF/2026-11-13_0526_PROGRESS.md`, `research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex` | Historical candidate/negative threshold and abstraction evidence, not a theorem supplying the missing small-threshold MCSP bound |

## 2. Exact source, target, machine and counting

Let $n$ be the circuit's input arity, $N=2^n$ the **explicit full truth-table bit length**, and $L$ the unrelated encoded SAT instance length. Let $CC_n(f)$ count binary AND/OR and unary NOT gates, free constants and primary wires, arbitrary fanout. Ordinary exact MCSP[$s$] accepts iff $CC_n(f)\le s(n)$, with no promise. One fixed total deterministic machine must serve all $n$; it has one locally moving **one-way read-only source head** and exactly one locally moving **two-way read/write work head**, finite control and fixed finite alphabet. A malformed bare input length is rejected. All copying, rereading the **work cache**, interpretation, temporary registers, head motion, enumeration, counter carries, and final output are counted.

Let

$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s,\quad
m=\Theta\bigl(n+(s+1)\log_2(n+s+2)+1\bigr).
$$

This bounds syntactic straight-line AND/OR/NOT circuit descriptions of at most $s$ gates, including selected output. Enumeration may have duplicates, which are charged rather than silently deduplicated.

## 3. RAWSCAN28 theorem: removing per-bit addresses

**Proved restricted claim.** For any one fixed nonnegative schedule $s(n)$ uniformly computable in time polynomial in $n+s(n)$, there exists a single finite deterministic one-way-input plus one-work-tape MCSP[$s$] decider with

$$
T_{\mathrm{raw}}(N)=O\bigl(N D(n,s)\operatorname{poly}(n+s+1)+N\operatorname{poly}(n+1)\bigr),\qquad
S_{\mathrm{raw}}(N)=N+O(m).
$$

Here $S$ counts **visited writable cells**, not only bits of a mathematical summary. The hidden polynomial and constants depend on the fixed machine and chosen circuit basis, not on $n,N$, or a nonuniform answer table.

**Constructive proof.** While consuming the unknown-length one-way input, the machine appends each **raw input bit** to a contiguous work-tape region, with a mobile finite-alphabet binary length counter beside its right boundary. Move the counter block across each newly written bit in $O(\log(i+2))$ local head transitions, without leaving addresses between data bits. The cache is exactly the original $N$ symbols plus $O(\log N)$ scratch cells. At EOF, check that $N$ is a power of two, compute $n$ and $s(n)$ using paid tape operations, or reject malformed length.

Enumerate one circuit description at a time with a mobile scratch block of $O(m)$ tape cells containing that description, the binary assignment index, $O(s)$ gate-value registers, and one match flag. The tape layout at the $i$-th original data bit is

$$
x_0\cdots x_{i-1}\;[\mathrm{SCRATCH}]\;x_i\cdots x_{N-1}.
$$

Evaluate the chosen circuit on index $i$ in $\operatorname{poly}(m)$ local work steps, compare with $x_i$, then shift the scratch block **one cell right across** $x_i$. Literal one-head rotation of $m$ scratch cells and one data cell takes $O(m)$ elementary movements and single-symbol rewrites, keeping the source bits in their original order. After the final bit, shift the same scratch block back left across all $N$ bits and increment the finite-alphabet circuit-description counter. Every source bit remains readable in the physical cache; no random-access source head or extra work tape is used. One complete candidate costs $O(N\operatorname{poly}(m))$ transitions. Accept if and only if one description agrees at every coordinate. Every $CC_n(f)\le s$ function has an enumerated circuit; every agreeing circuit certifies YES. Thus both labels and all valid lengths are correct. The cache remains $N$ cells and **only one mobile $O(m)$ scratch block** is live at once. This proves the bounds.

For $s_\kappa(n)=\lfloor\kappa n/\lceil\log_2(n+1)\rceil\rfloor$, fixed rational $\kappa>0$,

$$
\log_2 D(n,s_\kappa)=(2\kappa+o(1))n,\qquad
T_{\mathrm{raw}}(N)\le N^{1+2\kappa+o(1)},\quad S_{\mathrm{raw}}(N)=N+O(n).
$$

The $O(N)$ space is an **upper bound for this compiler**, not a necessity theorem. This sharpens TMR-1/027's published space statement, not its time exponent.

## 4. ANNO28: parallel candidate updates when arity really is supplied first

Define a **different annotated language** whose input begins with a self-delimiting encoding $\gamma(n+1)$ before the full $N=2^n$-bit table. In this model only, the same single one-work-tape decider may first build $D(n,s)$ circuit records, with one flag, one *local* $n$-bit coordinate counter and polynomial-size gate-evaluation scratch per record. It then reads one source bit, **pauses the one-way input head**, sweeps the one tape across all records updating their agreement flags and counters, returns, and requests the next source bit. Require exactly $N$ following bits and an endmarker. A physical record is of length $\operatorname{poly}(m)$; there is no unbounded-word instruction, global remote-access oracle, or free replication. Thus the fully charged *symbolic construction* has

$$
T_{\mathrm{anno}}(N)=O\bigl(ND(n,s)\operatorname{poly}(m)\bigr),\qquad
S_{\mathrm{anno}}(N)=O\bigl(D(n,s)\operatorname{poly}(m)\bigr).
$$

For $s=s_\kappa$, $T_{\mathrm{anno}}=N^{1+2\kappa+o(1)}$ and $S_{\mathrm{anno}}=N^{2\kappa+o(1)}$; for fixed $0<\kappa<0.005$ the exponents are eventually less than $1.01$ and $0.01$, respectively. **This is not a CHMY bare-source algorithm.** The header is genuine input data, and no low-space procedure for deriving it from an unknown-length stream is claimed. The prior HEADER27 lower bound is for producing a **full ordered output** with an early header, and does not prove a corresponding decision-space lower bound. It is therefore not a proof that the annotated algorithm cannot be converted into a sublinear-space bare-source decision algorithm. That transfer remains OPEN.

## 5. Primary theorem matrix and explicit exponent/variant gaps

| Primary source (original page/theorem) | Exact model, hypothesis, conclusion |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, **Theorem 1**, printed p.23:3 [1] | For some sufficiently small fixed $\mu_1>0$, **ordinary decision** MCSP[$2^{\mu_1n}$] on explicit $N=2^n$ truth tables, one-way read-only input + one two-way work tape: a deterministic nonmembership in $\mathrm{DTIME}_1[N^{1.01}]$ implies $P\ne NP$. Missing hypothesis remains OPEN. |
| Same, **Theorem 2**, p.23:3 [1] | For some larger $\mu_2>\mu_1$, ordinary MCSP[$2^{\mu_2n}$] is unconditionally **not** in randomized two-sided-error $\mathrm{BPTIME}_1[N^{1.99}]$. The exponent is stronger but threshold is different; no automatic threshold transfer. |
| McKay, Murray, Williams, STOC 2019, **Theorems 1.2 and 1.3**, pp.1–2 [2] | One-pass **search** MCSP for $A$-oracle circuits, uniform and time-constructible $s(n)\ge n$, with $\Sigma_3\mathrm{SAT}^A$ oracle calls, $\widetilde O(s)$ space and $\widetilde O(s^2)$ update time; if suitable $A\in\mathrm{PH}$ has no $\operatorname{poly}(s)$-space, $\operatorname{poly}(s)$-update search streaming algorithm then $P\ne NP$. Our $s_\kappa(n)<n$ eventually, and our exact decision/annotated models do not meet that search/oracle hypothesis. |
| Prior Claude ONETAPE, original report [3] | Crossing-sequence $\Omega(N^2/\log N)$ type SAT bounds for **one-tape total** and related sequential-access models also apply to nondeterministic machines; no automatic unrestricted-multitape SAT separation. It is repository historical analysis, not a new primary MCSP magnification theorem. |

Our constructions are at $s(n)=\Theta(n/\log n)$, whereas the magnification statement requires $s(N)=N^{\mu_1}$ for a positive constant $\mu_1$. Since $n=\log_2N$, $n/\log n\ll N^{\mu_1}$ for every such constant. Threshold zero, fixed-gate and polynomially growing gate-count upper bounds cannot be silently transferred. A succinct 3-SAT encoding of length $L$ cannot provide an exponentially long MCSP truth table free of computation or transport. Nothing here excludes arbitrary polynomial workspace, GF(2) summaries, Horn/2-SAT or bounded-treewidth shortcuts, sharing, variable renaming, products, cache/recompute or adaptive computation.

## 6. Actual native execution and limitations

**Executed native CPython** exact `experiments/tmr/tmr3_rawscan031.py` (SHA256 `8e6ec6714d6a7d3cf5848992cb4df9cb057d8a1b1ebfb1b868e6eee66d746918`) and raw `results/raw/tmr/2026-11-14_1327_TMR3_RAWSCAN031_RAW.json` (SHA256 `1c1c6ffffb553678bfbe517c3b45e0f652fd9f1cd3f78f798769a9801e494fc0`). All 828 length-2/4/8 truth table classifications at gate counts 0,1,2 agree with an independently implemented straight-line gate-function generator; nine circuit-class count controls and 1,024 exhaustive rotation invariants produce **1,861 passed assertions** with zero failures. Physical one-symbol carry/shift operations performed: **231,036**; conservative counted moves/rewrites **7,603,632**; 14,543 full candidate sweeps and 115,006 candidate-bit comparisons. Only finite-alphabet **micro-rotations** are literally rewritten at the one-head level; candidate evaluation uses Python integer masks and the full machine is not a compiled transition-table run. ANNO28 is an all-length symbolic construction, **not actually executed**. Finite evidence is COMPUTATIONAL, not an asymptotic complexity proof.

## 7. Status, peer audit and next target

**PROVED/RESTRICTED (symbolic, peer review OPEN):** linear-space raw cache and header-given sublinear-space candidate flags, each with complete source/tape charges as stated. **OPEN:** conversion of a header-known $s(n)$ candidate-parallel updater to a **bare unknown-length one-way source** without storing $N$ raw bits; cost-sound threshold-$N^\mu$ lower bound; any all-polynomial-exponent SAT lower bound. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `main.tex` belongs to TMR-5 and is unchanged. No scheduled tasks altered.

**Next target:** design a genuinely header-free, length-adaptive candidate-list updater at growing gate budget $s(n)=\omega(1)$, or exhibit an explicit pair of same-prefix inputs forcing retroactive initialization for a narrowly defined updater class. **TMR-1/TMR-5 peer request:** independently check the raw-cache left/right one-head rotations, candidate-description enumeration, malformed length, and whether the annotation-only theorem's counter/EOF charges are sufficient. **TMR-2/TMR-4 peer request:** test whether cofactor inheritance yields a non-affine compact summary when new gate candidates appear.

### References

[1] Cheraghchi, Hirahara, Myrisiotis, Yoshida. *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*. STACS 2021, Theorems 1–2, p.23:3. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] McKay, Murray, Williams. *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*. STOC 2019, Theorems 1.2–1.3, pp.1–2. https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf

[3] `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, historical source and guarded limitations.
