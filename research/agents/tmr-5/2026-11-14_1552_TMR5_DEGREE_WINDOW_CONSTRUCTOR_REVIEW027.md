# TMR-5/027: Quantified MCSP indexed-table frontier and constructor-head audit

**Pacific timestamp:** November 14, 2026, 15:52 PST. **Owner:** TMR-5 Machine Bottleneck Redteam. **Status:** DEGREE40 is a proved elementary **RESTRICTED** conditional consequence of a bounded-time Boolean circuit simulation, pending independent TMR-4 and TMR-1 mathematical review. CONHEAD40 is an **OPEN model-transfer premise** in the TMR-3/030 network argument, with a provably sufficient conservative repair. Experiments are COMPUTATIONAL. P versus NP is OPEN.

## 1. What is genuinely new

TMR-4/031 proved that a fixed polynomial-time bit-index evaluator produces an ordinary positive-power MCSP YES truth table when the target arity satisfies $n/\log(L+n)\to\infty$. I derive the **quantitative frontier inside the previously unresolved logarithmic regime**. If the source is length $L$, the output is a full $N=L^{a+o(1)}$ truth table, every indexed target bit is computed by one fixed evaluator within $L^{d+o(1)}$ steps, and $\mu a>2d$, then **every output is ordinary $MCSP[\lfloor N^\mu\rfloor]$ YES**. Thus such a fast-indexable transformation cannot preserve a required MCSP NO label. A complementary inequality lower-bounds the worst-index runtime of any fixed evaluator that actually produces a NO table.

I separately audited TMR-3/030's claimed charged serialization. Its asserted additive $C(N)$ term for a network constructor supplied a binary length header does not follow **unless the constructor's input-head interface is implemented on the same single work tape, or a model conversion is proved and charged**. A generic fully serialized header-input constructor costs at most $O(C(C+\log N))$, which changes the exponent frontier. The original restricted near-linear event bound survives **conditionally** for a constructor whose binary header is already on its work tape. This is a precise missing implication, not a claim that faster simulation is impossible.

I also independently reproduced TMR-2/030's sharp hypergeometric r-witness reference-distance examples and checked TMR-1/029's Shannon counting inequality. Neither is a lower bound for general SAT programs.

## 2. Primary-source theorem and model matrix

| Original theorem and location | Exact relevant model and input | Hypothesis and conclusion |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021 [1], Theorem 1, printed p.23:3 | Ordinary **decision** MCSP, full truth-table length $N=2^n$, threshold $s=2^{\mu_1 n}$ for a sufficiently small fixed $\mu_1>0$; fixed deterministic **one-way read-only input plus one two-way read/write work tape**. | If outside $DTIME_1[N^{1.01}]$, then $P\ne NP$. Premise OPEN. |
| Same [1], Theorem 2, p.23:3 | Ordinary decision MCSP, **different larger** $\mu_2$ close to one, same input/work-head arrangement, bounded-two-sided-error randomized one-work-tape machine (success probability at least $2/3$). | Proven outside $BPTIME_1[N^{1.99}]$. It does NOT imply Theorem 1's small-$\mu_1$ antecedent. |
| Same [1], Theorem 3, p.23:4 | For every $1/2<\mu<1$, even a randomized one-work-tape machine accessing arbitrary oracle queries of length $N^{o(1)}$ has some exponent $1+\mu'>1$ lower bound. | Restricted short-query barrier, not unrestricted SAT separation. |
| McKay, Murray, Williams, STOC 2019 [2], Theorems 1.2-1.3, pp.2-3 | **Search**-$MCSP^A[s(n)]$ with oracle gates, $N=2^n$ complete input, time-constructible $s(n)\ge n$; one-pass $\Sigma_3 SAT^A$-oracle streamer with $\widetilde O(s)$ space and $\widetilde O(s^2)$ update. | If, for suitable $A\in PH$, no deterministic $\mathrm{poly}(s)$ space/update streaming synthesizer exists, then $P\ne NP$. Neither oracle search nor its promises can silently become plain decision MCSP. |
| Pippenger-Fischer, JACM 1979 [3] | Bounded-time Turing-machine computations have nonuniform circuit representations. | Background only. The coarser explicit squared-time simulation below is independently accounted. |

$L$ always denotes encoded SAT input bit length, $n$ target Boolean arity, and $N=2^n$ complete output truth-table length. The circuit basis is fan-in-two AND/OR and unary NOT with unrestricted fanout and free input wires/constants. No ETH, SETH, cryptographic hypothesis, free oracle/advice, or assumed NP-completeness of ordinary MCSP appears. Oliveira-Santhanam magnification and Chen et al. locality barriers were considered as scope controls, not imported as uncited implication arrows.

## 3. DEGREE40: quantitative indexed-output theorem

Fix **one** total finite-alphabet deterministic multitape bit evaluator $E$. Given source $F$ of length $L$ and index $i$ of exactly $n$ bits, let it return Boolean bit $Y_F[i]$. The output is a complete $N=2^n$ truth table only if all $N$ bits are eventually materialized. Let $t(L,n)$ bound the runtime on **every index** for the **same** fixed $E$.

For a uniform evaluator bound $t(L,n)\le c(L+n+2)^d$ with constants $c,d\ge1$, hardwire only $F$ and leave $i$ as live circuit inputs. A one-hot encoding of every relevant tape symbol, head position, and finite control state can be unrolled for $t$ transitions. Every input cell and every visited work cell is represented, including all writes, switches, rereads, shared state and head moves. Since the fixed number of tapes occupies at most $O(L+n+t+2)$ relevant cells, a conservative Boolean layer implementation gives

$$
CC_n(Y_F)\le K_E(L+n+t+2)^2
$$

for a model-dependent fixed $K_E>0$. This is the TMR-4/031 simulation bound, with its input-length and nonuniformity assumptions independently checked; this circuit-construction statement is not a one-work-tape runtime claim.

Put $X=L+n+2$, $K'=K_E(1+c)^2$ and fix $\mu,\delta>0$. Since $d\ge1$,

$$
CC_n(Y_F)\le K'X^{2d}.
$$

If $n\ge ((2d+\delta)/\mu)\log_2 X$, then $N^\mu\ge X^{2d+\delta}$, and for sufficiently large $X$ the floor $s(n)=\lfloor N^\mu\rfloor$ exceeds $K'X^{2d}$. Therefore

$$
\boxed{Y_F\in MCSP[\lfloor N^\mu\rfloor]\quad\text{for every source }F.}
$$

**New polynomial-output corollary:** Along families $N=L^{a+o(1)}$ and $t(L,n)=O(L^{d+o(1)})$, all outputs are MCSP YES for sufficiently large $L$ if

$$
\boxed{a\mu>2d.}
$$

Proof: $n=(a+o(1))\log_2L$ and $X=L(1+o(1))$, so the positive gap between $a\mu$ and $2d$ absorbs all constants and subpolynomial factors. A polynomial-output, both-label SAT-to-MCSP reduction meeting this per-bit bound would fail its NO requirement. **Outside that inequality the compiler upper bound is merely inconclusive, not a NO-instance construction.**

**Inverted necessary evaluator cost:** For any output $Y_F$ that really is MCSP NO at threshold $s=\lfloor N^\mu\rfloor$,

$$
s<CC_n(Y_F)\le K_E(L+n+t+2)^2
$$

and hence

$$
\boxed{t>\sqrt{s/K_E}-(L+n+2).}
$$

If $L+n=o(N^{\mu/2})$, the fixed evaluator has worst-index time $\Omega(N^{\mu/2})$ on any such NO sequence. This is a bound on a specified indexed evaluator, not on every uniform SAT decider.

**Scope falsifier:** When $L=N=2^n$, the uniform program $E(F,i)=F[i]$ can scan source $F$ and return its indexed bit in $O(L)$ time. Circuit counting shows that for each fixed $0<\mu<1$ some arbitrary source strings still have $CC_n(F)>N^\mu$. They are not claimed to be 3-CNF strings. Here $a=1,d=1$ does not meet $a\mu>2d$, so the new sufficient theorem correctly stays silent. Horn, 2-SAT, XOR/Tseitin, bounded treewidth, products, padding, renaming, compact algebra and recomputation remain legitimate inexpensive controls.

## 4. CONHEAD40: audit of the TMR-3/030 network simulator

TMR-3/030 considers a length-only, uniformly constructed network with a binary-$n$ constructor of time $C(N)$, description size $B(N)$, processors $p(N)$ and full-run charged events $E(N)$. The virtual tape-record region has length

$$
M=O(N+B+(E+p+1)\log(N+B+E+p+2)).
$$

The claimed additive-constructor simulation is $T_{\mathrm{sim}}=O(C+N+(E+1)M)$. That is valid **if** $C$ refers to physically executing a constructor with binary $n$ already placed on its **one writable work tape**, with no independent constructor input head. But the source MCSP machine has only a one-way input stream, already at EOF after copying its full table. A constructor described as taking binary $n$ on a separate input head cannot simply be run with its own source tape for free. TMR-3's 7,200 original native-Python checks exercise parity-network semantic proxies and rational exponents, not this physical input translation.

A conservative fully charged generic repair for a fixed constructor with an additional read-only header head is straightforward: place its binary header, one-hot input-head marker, work tape, and virtual-control record on the single available work tape. At most $O(C+\log N)$ cells are represented; one entire scan and update per simulated constructor step costs $O(C+\log N)$, yielding

$$
T_{\mathrm{sim}}=O(N+C(C+\log N)+(E+1)M).
$$

For power laws $C=O(N^c)$, $B=O(N^b)$, $p=O(N^a)$, $E=O(N^e)$, this generic simulator can invoke [1, Theorem 2] when both $2c<1.99$ and $e+\max(1,a,b,e)<1.99$. TMR-3's stronger $c<1.99$ is **not justified by this generic model conversion**. For the illustrative regime $C=\Theta(N)$, $E=N^{0.8}$ and $B,p=O(N)$, the original formula gives an $N^{1.8+o(1)}$ one-work-tape bound, whereas the generic header interpreter's available upper bound is $N^{2+o(1)}$, insufficient against Theorem 2. This does **not** prove a faster simulation is impossible.

**Preserving repair:** Restrict the theorem to a true single-work-tape constructor that receives its binary-$n$ header prewritten on the same tape, with its native physical runtime $C$ and header-writing time charged; then additive $C$ is available and the previously stated restricted high-$\mu_2$ network frontier survives. Alternatively TMR-3 can prove a stronger exact header-interface conversion. Current general-input-constructor wording should remain OPEN pending that proof. The earlier corrected peak-space ledger $S_{\mathrm{sim}}=O(S_C+M)$ remains valid.

## 5. Independent actual execution

Original native CPython source: experiments/tmr/tmr5_degree_constructor_audit040.py, SHA256 fd0ebf458ac0b277b2a670b062ff9bbb29d724478ff9f4e58af241b7718363a7. Immutable native JSON stdout: results/raw/tmr/2026-11-14_1552_TMR5_DEGREE_CONHEAD040_RAW.json, SHA256 b45cc02e3ebbd7633335c72870178150bec72744e42fbf39b67218d718b21fe3.

**3,302 assertions, zero failures.** Exhaustively evaluated 208 exact r-sparse hypergeometric reference-distance configurations and 3,864 witness supports, checked circuit counting inequalities for 192 arities $n=8,\ldots,199$, ran 2,268 exact rational $\mu$ polynomial-degree threshold comparisons and 384 independent network exponent-frontier comparisons. The degree comparisons use integers $L=2^h$, $n=ah$, $t=L^d$, and constant test $K=128$, not floating arithmetic, not materialized exponential tables. All finite work is COMPUTATIONAL. No physical finite-state TM was compiled or executed, no actual SAT reduction was produced, and no asymptotic lower bound follows from tests alone.

## 6. Integrated dependency map and explicit retirements

| Priority | Evidence that survives | Exact remaining arrow |
| --- | --- | --- |
| 1, highest | CHMY [1] Theorem 1 is a published conditional hardness magnification implication. | Prove ordinary low-$\mu_1$ MCSP outside deterministic one-way-input one-work-tape $N^{1.01}$, **OPEN**. CHMY high-$\mu_2$ Theorem 2 cannot substitute. |
| 2 | TMR-1 capped minimization has bounded/slow-growing threshold decision and exact symbolic enumeration. | Actual one-work-tape physical implementation and $s=N^{\mu_1}$ transition remain **OPEN**. |
| 3 | TMR-2/030 exact r-sparse black-box reference-distance bound, independently checked here. | Syntax-dependent, globally shared algorithm and charged source-query-to-one-tape conversion **OPEN**. |
| 4 | TMR-4/031 indexed compiler, with this new $a\mu>2d$ boundary. | **RETIRED within scope:** fast-indexed large-output reductions cannot produce positive-threshold MCSP NO tables. General polynomial-output syntax-aware reductions **OPEN**. |
| 5 | TMR-3/030 high-$\mu_2$ exponent inequality correct **conditional on an exact charged serialization**. | Constructor header-interface conversion **OPEN** as generally worded; survives for native single-work-tape header constructors. |
| Retired | TMR-5/026 dummy-variable table repetition, TMR-4/030 masked-CNF compiler, unrestricted promotion of query-only locality. | **RETIRED as automatic SAT hardness amplifiers only**, not as a theorem ruling out all nontrivial reductions. |

The unrestricted goal still quantifies over every fixed correct total finite-alphabet uniform deterministic multitape 3-SAT decider $A$, every integer $k\ge1$, every constant $C>0$ and every $L_0$, requiring some valid formula $F$ with $|F|\ge L_0$ and $T_A(F)>C(|F|+1)^k$. No artifact closes that arrow. No free semantic oracle, proof-calculus obligation, fixed-space assumption, input reread ban, nonuniform hardcoded table, or cross-machine time/space borrowing has been inserted.

## 7. Corpus governance and next review

Read first the governing November 14 MCSP handoff (Git blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then the November 13 role replacement; AGENTS, CODEX, PNP skill and modes; both root proof trackers and the authentic complete proof2 Git blob (1,051,196 chars), canonical root main.tex Git blob (2,545,859 chars), all five TMR handoffs and issue #3 through TMR-4/031. Inspected original TMR-1/029, TMR-2/030, TMR-3/029/030, TMR-4/030/031, TMR-5/025/026 reports plus relevant original source and raw evidence. Also surveyed prior Claude ONETAPE/DIRECTPRODUCT/TPORT, compact GF(2)/Walsh/moment and Grok/legacy accepted-counterexample records through canonical provenance; no historical restricted result was promoted. Checked primary CHMY STACS 2021 publisher PDF page images 23:3-4 and MMW 2019 author PDF.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex and both proof trackers were not edited while a load-bearing arrow is OPEN. No tasks, schedules or agents were changed.

**Peer requests:** TMR-3 should define the exact binary-header constructor input interface and reproduce the one-work-tape model conversion, or accept the narrower native-work-tape constructor theorem. TMR-4 should independently audit DEGREE40's exponents and floors. TMR-1 should verify exact $\mu_1/\mu_2$ theorem dependency and TMR-2 the r-sparse restricted promise. Next TMR-5 run should synthesize only peer-verified results.

## Numbered primary references

[1] Cheraghchi, Hirahara, Myrisiotis and Yoshida, STACS 2021, Theorems 1-3, https://doi.org/10.4230/LIPIcs.STACS.2021.23.

[2] McKay, Murray and Williams, STOC 2019, Theorems 1.2-1.3, https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf, https://doi.org/10.1145/3313276.3316396.

[3] Pippenger and Fischer, JACM 1979, https://doi.org/10.1145/322123.322138.
