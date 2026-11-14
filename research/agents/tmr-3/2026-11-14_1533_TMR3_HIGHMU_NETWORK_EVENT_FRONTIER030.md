# TMR-3/030: A charged high-threshold MCSP network-event frontier and constructor-space repair

**Pacific timestamp:** 2026-11-14 15:33 PST (America/Los_Angeles). **Role:** TMR-3 Time-Space Tradeoffs. **Scientific status:** NETFRONT39 PROVED/RESTRICTED symbolic conditional on the explicit network model and CHMY Theorem 2, independently reviewed **OPEN**; CONSPACE39 direct-simulator ledger correction PROVED/RESTRICTED symbolic, independent audit **OPEN**. Executed finite controls are COMPUTATIONAL. **No unconditional P versus NP separation.**

## 1. What is genuinely new

TMR-3/029 already proved a polynomial-resource network serialization theorem, but extracted only the equivalence with P = NP and noted that generic quadratic serialization cannot establish *superlinear* network event lower bounds from the one-tape $N^{1.99}$ theorem. This run extracts the **exact surviving sublinear-event exponent frontier** for the *published high-threshold ordinary MCSP problem*, retaining all description, construction, input, scheduling and storage charges. It also repairs a concrete incompleteness in /029's **peak writable-space ledger**: the one-work-tape constructor's own visited cells cannot be omitted from peak space even when its output description is short.

The new frontier is useful as a restricted MCSP resource transfer, **not** an all-polynomial-time exclusion or a new route that closes hardness magnification. The assertion that a quadratic simulator yields no useful *superlinear* network bound is retained. Our bound is below linear in total events.

## 2. Exact sources and prior-work ledger

| Primary source / project original | Verified theorem, status and restriction |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, [publisher paper](https://doi.org/10.4230/LIPIcs.STACS.2021.23), Theorem 2, printed p.23:3 [1] | Ordinary **decision** $MCSP[2^{\mu_2 n}]$ for some fixed $0<\mu_2<1$ on complete $N=2^n$ tables is **not** in randomized two-sided-error $\mathrm{BPTIME}_1[N^{1.99}]$. Model: one-way read-only source plus one two-way writable work tape, bounded error. No promise beyond valid complete truth tables. This is the *larger threshold* theorem, not the magnification hypothesis. The PDF page image was inspected in this run. |
| Same, Theorem 1, printed p.23:3 [1] | For some *different sufficiently small* $\mu_1>0$, $MCSP[2^{\mu_1 n}]\notin\mathrm{DTIME}_1[N^{1.01}]$ would imply $P\ne NP$. This antecedent remains OPEN. One-way read-only source plus one work tape, deterministic. |
| McKay, Murray, Williams, STOC 2019, [author/MIT manuscript](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf), Theorems 1.2-1.3 [2] | The streaming magnification starting point uses **search**-MCSP with oracle circuits and small updates. Do not identify it with ordinary positive-threshold decision MCSP or a polynomial SAT reduction. No part of NETFRONT39 imports a search-streamer implication. |
| `research/agents/tmr-3/2026-11-14_1455_TMR3_TWOWAY_HEADER_NETWORK_BRIDGE029.md`; `experiments/tmr/tmr3_twoway_header032.js`; original raw `results/raw/tmr/2026-11-14_1455_TMR3_TWOWAY_BRIDGE032_RAW.json` | PRIOR NETWORK32 serial simulator with $T=O(C+N+(E+1)M)$ and $M=O(N+B+(E+p)\log(N+B+E+p))$. Our result sharpens its exponents and corrects its constructor peak-space accounting. Original symbolic report/code/raw were inspected. |
| `research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md` and original source/raw | PRIOR header-dependent and raw-cache one-work-tape MCSP *upper bounds*. Their slow $s(n)=\Theta(n/\log n)$ thresholds do not match $N^{\mu_2}$ or $N^{\mu_1}$. |
| `research/agents/tmr-1/2026-11-14_1504_TMR1_PADDING_WINDOW_NEAR_TIGHT029.md` and original source/raw | PRIOR near-tight universal dummy-input YES-collapse at $r=(1/\mu-1)n+O_\mu(\log n)$. Restricted padding statement, not a time lower bound. |
| `research/agents/tmr-2/2026-11-14_1521_TMR2_RSPARSE_HYPERGEOMETRIC_QUERY030.md`, `research/agents/tmr-4/2026-11-14_1439_TMR4_POSITIVE_POWER_COMPILER_FIREWALL030.md`, `research/agents/tmr-5/2026-11-14_1452_TMR5_DUMMY_PADDING_UNIVERSAL_COLLAPSE026.md` | Current peer oracle/syntax/padding controls, all restricted to their own source-access/circuit constructions. |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`, `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, `research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex` | Original prior crossing-sequence/portfolio/direct-product and lossy-hash controls; none authorizes transferring a selected access model to arbitrary uniform SAT algorithms. |

The November 14 MCSP priority directive was read FIRST, then the November 13 TMR replacement, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, all five newest handoffs, and the latest issue #3. Root `proof1.txt` (28,714 characters) was read; `proof2.txt` (1,051,196 characters) and canonical `main.tex` (2,545,859 characters) were recovered and reviewed through their authentic Git blobs after the content endpoint returned blank bodies. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Their OPEN obligations persist, and no root file is edited.

## 3. Declared physical source and network model

Let $N=2^n$ be the actual **explicit MCSP input length**, and $s(N)=\lfloor N^{\mu_2}\rfloor$ be CHMY Theorem 2's large-threshold regime. This $n$ is truth-table arity. The encoded 3-CNF input length $L$ is a **different parameter** and does not enter this theorem.

A fixed finite deterministic one-work-tape, binary-$n$-input **length-only constructor** emits a $B(N)$-bit fully specified network description in $C(N)$ physical transitions, using peak visited writable cells $S_C(N)\le C(N)+O(n)$. This construction is uniform across all $n$, and its cost is **not free**. The network has at most $p(N)$ processors with single finite-alphabet local tapes and uniformly declared local programs. It may access the explicit source by indexed reads and send/receive a constant-size symbol per *charged* event. Every receiving interface, output cell update, source read, queue action and local machine transition is individually represented. Arbitrary copying, broadcasts, preprocessing, input rereads, caching, switching and recomputation must be counted. Every processor uses at most one local charged event per synchronous round; $E(x)$ denotes **the full run's** event count, including final output. Define $E_{\max}(N)=\max_{|x|=N}E(x)$, covering both YES and NO tables. Malformed lengths are handled by a fixed total parser.

The length-only assumption matters: a more general source-dependent constructor reading a separate one-way input would require an additional explicit simulation, possibly invalidating an additive $C$ bound. This report does **not** silently inherit that uncharged variant. The network may be deterministic or bounded-two-sided-error randomized; in the randomized version, all event/time bounds are worst-case over coins and simulation preserves the distribution.

## 4. NETFRONT39, a quantitative restricted transfer

**Lemma (literal serial emulator).** For the declared length-only constructor, a fixed uniform deterministic one-way-input plus ONE two-way writable-tape machine can, on each $N$-bit source, read the source once into a contiguous raw cache, run the binary-$n$ constructor in a separate tape block, and represent processor programs/heads, all virtual tapes, work buffers, queues, source indices and outstanding messages in one serialized area. There is a universal model-dependent constant such that

$$
M(N)=O\left(N+B(N)+(E_{\max}(N)+p(N)+1)\log(N+B(N)+E_{\max}(N)+p(N)+2)\right)
$$

and its physical time and space satisfy

$$
T_{\rm sim}(N)=O\left(C(N)+N+(E_{\max}(N)+1)M(N)\right),
$$

$$
S_{\rm sim}(N)=O\left(S_C(N)+M(N)\right).
$$

A randomized network yields a bounded-error **randomized** one-work-tape simulator with the same worst-case bounds.

**Proof.** The one-way physical source is copied while its head advances and the single writable head appends cache bits; a binary counter supplies $n$. Running the length-only one-head constructor on a disjoint block takes its declared $C$ transitions, with no virtual second input head. Reserve/compact the resulting description and allocate records for processors, heads, binary indices, local tape cells, shared source cache, and one record per queued symbol/message. At most $O(E+p)$ new records are created, each with fixed symbol/identifier fields of $O(\log(N+B+E+p))$ bits. A single real work head can sweep these records to find the active virtual cell, perform its finite local transition, update a queue, read a source coordinate, or move a virtual head in at most $O(M)$ steps per charged event. Records are not assumed to be random-access or unit-cost words. The sequential source copy costs $O(N)$; uniform construction costs $O(C)$; full event replay costs $O((E+1)M)$. The constructor's visited cells remain in the peak-space charge even if erased. Correct terminal labels and, where applicable, random-coin output distributions are preserved. The fixed finite interpreter handles every input length, so there is no per-length advice. QED, modulo an independent low-level finite-alphabet implementation audit.

**Corollary (exact exponent frontier).** Suppose for some fixed real exponents $a,b,c,e\ge0$ with $C(N)=O(N^c)$, $B(N)=O(N^b)$, $p(N)=O(N^a)$, and $E_{\max}(N)=O(N^e)$ for all sufficiently large valid $N$. Put $d=\max\{1,a,b\}$. Then

$$
T_{\rm sim}(N)=O\left(N^c+N+N^{e+\max(d,e)}\log(N+2)\right).
$$

By [1, Theorem 2], **no** network deciding ordinary $MCSP[N^{\mu_2}]$ with both labels correctly and the declared uniform source/model can satisfy simultaneously

$$
\boxed{c<1.99\quad\text{and}\quad e+\max(d,e)<1.99.}
$$

Otherwise its deterministic or bounded-error randomized single-tape emulator would lie in $\mathrm{BPTIME}_1[N^{1.99}]$, contradicting [1]. This is a *theorem-transfer contradiction*, not a finite experimental time lower bound. At the equality exponent, the unspecified logarithm prevents an inference.

**Concrete low-overhead regime.** If $C,B,p=O(N)$, then $d=1$. For **every fixed** $\varepsilon>0$, a correct uniform high-threshold MCSP network with all those bounds cannot have $E_{\max}(N)=O(N^{0.99-\varepsilon})$. Since $E_{\max}\le O(p(N)t(N))$ under the event schedule, the simultaneous bounds $p=O(N^a)$ and $t=O(N^b)$ are excluded whenever $a+b<0.99$ (and the other low-overhead premises hold). This proves only a *near-linear total-event restriction* at the high $\mu_2$ threshold. It is compatible with networks having polynomially many processors and polynomial elapsed time.

**Resource sensitivity.** If $B=N^{1.5}$ while $C<N^{1.99}$, then $d=1.5$ and the serial argument only excludes $e<0.49$. If $C\ge N^{1.99}$ or $B\ge N^{1.99}$, this transfer gives no positive event exponent. Larger machine counts or input-replication descriptions can consume the entire one-tape lower-bound budget. Never read the $N^{1.99}$ input/table lower bound as a bound on *elapsed parallel rounds* with no $p,B,C$ accounting.

## 5. CONSPACE39: direct-simulator peak-space correction

TMR-3/029 claimed $S_{\rm serial}(N)=O(M(N))$ for the generic simulator while also executing an arbitrary specified constructor charged $C(N)$ transitions. That bound omits the constructor's peak visited writable cells. A concrete obstruction is a valid fixed constructor that, on a binary description of $N$, writes through $N^2$ work cells, erases them, and then emits a constant-size description for a one-processor network deciding the constant-zero language. Its $B,p,E$ are $O(1)$ and $M=O(N)$, but the **literal simulator that executes that specified constructor** visits $\Omega(N^2)$ cells. Its peak space is not $O(M)$. This does **not** assert that an alternative optimized constructor for the same trivial network must visit those cells.

Thus the cost-sound general direct-emulator ledger is $S_{\rm sim}=O(S_C+M)$, not $O(M)$ without a separately proved assumption $S_C=O(M)$ or a compiler that demonstrably bypasses the original constructor. The **time** corollary and the polynomial-uniformity implication survive because $S_C\le O(C)$ for that same constructor.

## 6. Actual execution, hostile controls, limitations

Native CPython 3 executed exact source `experiments/tmr/tmr3_network_event_frontier039.py`; its immutable stdout is `results/raw/tmr/2026-11-14_1533_TMR3_HIGHMU_NETWORK039_RAW.json`. The exact local source SHA256 is `ded70d2897ce3ef8808d0a57bbbd2fa460aeacbca6b4a785fb35e4a0c0e38ff2`; raw SHA256 is `908750ee69be15a416cd29921d50648983d98c3248276dd601363bf67e8b367f`. The Git blobs are respectively `961688c511d6e92b24f956d6a045a0d48d07a8b2` and `65bc84593b95c26cc0c44dfbe70a76c997b03ec1`.

The program executed **7,200 assertions with zero failures**, including 1,016 exhaustive small parity-network replays ($N=1..7$, $p=1..4$), 13,772 separately charged local/interface events, 148,136 record-visit proxies, 300,736 constructor-description bits accounted, and 3,315 exact rational exponent cases. Countercontrols include cheap parity summaries, source re-read access, explicit messages, larger description $d=1.5$, constructor-cost saturation $c\ge1.99$, and the critical $e=0.99$ boundary.

The execution checks **semantic correctness and accounting** of a simple finite network and exact rational exponent arithmetic. It neither executes MCSP at the theorem's asymptotic threshold nor compiles the entire simulator to a finite-control physical one-work-tape machine. The asymptotic restricted result follows from CHMY plus the independent symbolic serialization proof; it remains available for hostile peer review.

## 7. Proof dependency and precise OPEN gap

The chain is

$$
\text{high-}\mu_2\ \mathrm{MCSP}\text{ lower bound [1]}
\; +\; \text{charged length-only network simulation}
\;\Longrightarrow\; \text{restricted near-linear event frontier}.
$$

It does **not** imply the different low-$\mu_1$ lower bound in [1, Theorem 1], nor a lower bound for any fixed correct uniform multitape **3-SAT** decider. To prove $P\ne NP$, a stronger bridge must preserve the **exact small threshold, one-way-input one-work-tape model, and the $N^{1.01}$ nonmembership premise**, or directly establish an unrestricted all-polynomial $L$-time SAT lower bound for every fixed total machine.

With $L=|F|$, the missing unrestricted target is $\forall A\,\forall k\ge1\,\forall C>0\,\forall L_0\,\exists F$ valid, $|F|\ge L_0$ and $T_A(F)>C(|F|+1)^k$. The present exponent $0.99$ in $N$ is not a substitute. No model-selective crossing-sequence, communication, certificate, GF(2), Horn, 2-SAT, bounded-treewidth, product, padding or Walsh/moment result supplies the missing arbitrary-machine bridge.

**One concrete next target and review request:** TMR-5 should audit the length-only constructor premise, peak-space correction, and strict exponent threshold. TMR-1 should check that [1, Theorem 2] truly applies to the randomized serialized model with the exact high $\mu_2$. TMR-2 should test whether an input-query lower bound can strengthen $E_{\max}$ without imposing an online prefix restriction. TMR-4 should seek a charged same-model high-to-low threshold reduction. All load-bearing unverified transfers remain OPEN.

**Publication:** This is a role-owned report. Recheck the MCSP directive before branch merge and verify report, executed source, raw evidence and compact handoff on `main`; post paths to issue #3. Canonical `main.tex` is TMR-5-owned. No proof tracker edits and no schedule changes are authorized by this result.
