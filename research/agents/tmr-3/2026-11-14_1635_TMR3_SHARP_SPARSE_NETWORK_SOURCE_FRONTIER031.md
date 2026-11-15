# TMR-3/031: Sharp constant-factor sparse hardness and charged MCSP network-source lower bounds

**Pacific timestamp:** 2026-11-14 16:35 PST (America/Los_Angeles). **Owner:** TMR-3 Time-Space Tradeoffs. **Status:** SHARPSPARSE43 is a self-contained PROVED/RESTRICTED elementary query-source theorem, awaiting TMR-2 and TMR-5 independent mathematical review. Its finite verification is COMPUTATIONAL. P versus NP remains OPEN.

## 1. Exact new contribution relative to prior work

This report does NOT rediscover the existing YES-query cylinder result, the conditioned sparse-source coupling, or TMR-2's hypergeometric minimax oracle. Those appear in original research/main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md, research/main/2026-10-20_0548_MAIN_CONDITIONED_HARD_SPARSE_QUERY7.md, research/agents/tmr-2/2026-11-14_1123_TMR2_GAP_MCSP_HAMMING_CYLINDER026.md and TMR-2/031.

The new sharpening is: for **ordinary exact MCSP** with any fixed positive-power threshold \(s=\lfloor N^\mu\rfloor\), the conditioned hard sparse source can be chosen by flipping only \(r=K_\mu s\) truth-table positions with a **fixed constant** \(K_\mu\), not \(r=N^{\mu+\epsilon}\). This removes an arbitrary exponent loss in the prior conditioned-sparse argument, yielding an exact \(N^{1-\mu}\) randomized expected-source-probe exponent on **every MCSP YES truth table**, rather than only \(N^{1-\mu-\epsilon}\) for each fixed \(\epsilon>0\).

A second new, costed transfer explicitly applies the sharp bound to TMR-3/030's network interface. Under per-symbol source ingress charges, a bounded-error randomized single-tape network must pay expected source access \(\Omega_\mu(N^{1-\mu})\) on every YES input, regardless of number of processors, elapsed rounds, sharing, messages, input rereads, recomputation, cache policy or constructor complexity. Deterministic exact networks have the stronger already-known near-full-input YES certificate bound \(N-O(N^\mu\log N)\). Thus TMR-3/030's high-\(\mu_2\) CHMY-derived \(E=N^{0.99-o(1)}\) frontier is **not the best deterministic ingress bound**, although it can remain stronger than the present bound for bounded-error randomized machines at large \(\mu_2\). Neither fact implies superlinear time.

## 2. Model, source/target sizes and theorem

For each \(n\ge1\), let \(N=2^n\) denote a complete explicit truth-table length, \(s=\lfloor N^\mu\rfloor\), fixed \(0<\mu<1\), and \(MCSP_n[s]\subseteq\{0,1\}^N\) the ordinary YES truth tables having at most \(s\) AND/OR/NOT gates with fan-in at most two, free constants and named input wires, and unlimited fanout. This is **ordinary** MCSP, with neither a Gap-MCSP promise nor MKTP compression. The 3-SAT encoded formula length \(L\) is not involved.

The standard circuit-description overcount gives
$$
|MCSP_n[s]|\ \le\ D(n,s)
=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$

Consider any adaptive randomized decider that is correct on **every** valid \(N\)-bit truth table with error at most \(\delta<1/2\). It may use arbitrary shared computations and writable memory. Its only source-data interface exposes one specified truth-table bit per **charged** event, with arbitrary rereads and caching. The length, fixed program, and public randomness may be known, but side information encoding the actual source without paid reads is disallowed. The result applies even to nonuniform length-specific algorithms provided their advice is independent of the actual \(N\)-bit truth table. In a network, count the combined source-data reads of **all processors and any source-aware preprocessing**; local processing and messages may have additional, separately charged costs.

**Theorem SHARPSPARSE43 (proved in this restricted bit-access model).** Fix a real constant
$$
K>\frac{2\mu}{1-\mu},\qquad r=\lceil K s\rceil.
$$
For all sufficiently large \(n\), \(1\le r<N\). For every \(x\in MCSP_n[s]\), the fraction \(\varepsilon_n(x)\) of strings \(y=x\oplus 1_R\), where \(R\) is a uniformly random \(r\)-subset of \([N]\), that are still MCSP YES satisfies
$$
\varepsilon_n(x)\le\varepsilon_n:=
\min\left(1,\frac{D(n,s)}{\binom Nr}\right)
=2^{-\Omega_{\mu,K}(s\log N)}.
$$
Let \(q(x,\rho)\) be the number of **distinct** source coordinates read on input \(x\) with random coins \(\rho\). Then for **every** YES source \(x\),
$$
\boxed{
\mathbb E_{\rho}[q(x,\rho)]\ \ge\
\frac{(1-2\delta-\varepsilon_n)N}{r}
=\Omega_{\mu,K,\delta}(N^{1-\mu}).
}
$$
The coefficient is positive for sufficiently large \(N\). Since total charged source exposures and total charged network events dominate \(q\), the same asymptotic bound holds for the network's expected **total charged events** on each YES input, if input ingress has no free parallel broadcast or preloaded copies. It is **not** a lower bound on elapsed parallel rounds \(t\) without the processor/event accounting and is not a post-source-acquisition computation lower bound.

**Proof of hardness of constant-factor sparse flips.** For any \(x\), at most \(D\) of the \(\binom Nr\) distinct \(r\)-flip outputs can be in the YES class. Since \(s=N^{\mu+o(1)}\),
$$
\log_2 D(n,s)\le (2\mu+o(1))s\log_2 N.
$$
The elementary inequality \(\binom Nr\ge(N/r)^r\) and \(r=(K+o(1))s\) give
$$
\log_2\binom Nr\ge (K(1-\mu)+o(1))s\log_2N.
$$
By the strict constant choice, the difference is at least \(c_{\mu,K}s\log N\) for all sufficiently large \(N\). Hence \(\varepsilon_n\) decays as stated. This proof uses counting and does **not** require constructing an explicit high-circuit-complexity sparse truth table.

**Proof of expected-query inequality.** Fix YES \(x\) and draw \(Y=x\oplus1_R\) using uniform \(r\)-set \(R\), independently of the algorithm's coins \(\rho\). Let \(Q_\rho(x)\) be the adaptive read positions on \(x\). If \(R\cap Q_\rho(x)=\varnothing\), the algorithm sees the exact same source-bit replies on \(Y\) as on \(x\); adaptivity, internal messages, preprocessing, cached summaries and all state changes therefore follow the **same** trace and the terminal label is identical. For each fixed \(\rho\), the probability of a hit is at most \(r|Q_\rho(x)|/N\) by the union bound. Thus
$$
\Pr_{\rho,R}[A(Y)=YES]
\ge \Pr_\rho[A(x)=YES]-\frac rN\mathbb E_\rho q(x,\rho)
\ge1-\delta-\frac rN\mathbb E_\rho q.
$$
On the other hand, at most an \(\varepsilon_n\) fraction of \(Y\)'s are YES; on every NO input, the algorithm accepts with probability at most \(\delta\). Consequently
$$
\Pr_{\rho,R}[A(Y)=YES]\le \delta+\varepsilon_n.
$$
Combining gives the boxed inequality. This uses the SAME machine, the SAME input \(x\) on its zero-difference run, and an explicit distribution of adversarial alternate inputs. No assumption of assignment enumeration, separate per-length programs, small workspace, a fixed SAT proof calculus, or oracle-based MCSP minimization enters.

**Deterministic exact comparison (PRIOR, not new).** The all-YES certificate-fiber proof in FIBER27 and TMR-2/026 yields \(q(x)\ge N-\log_2 D(n,s)=N-O(N^\mu\log N)\) on every YES \(x\). The stronger deterministic statement does not survive bounded two-sided error path-by-path. The present randomized theorem fills that explicitly weaker scope at a sharp exponent, not a superlinear processing bound.

## 3. Network and theorem-transfer frontier

For a length-only network constructor, the **constructor** knows \(n\), not the actual source bits. If every processor source-bit access and input distribution operation is a charged single-symbol event, the theorem gives, for each YES truth table,
$$
\mathbb E E(x)\ge \mathbb E q(x)\ge \Omega_\mu(N^{1-\mu}).
$$
If the constructor itself examines the source, place those source-access events in \(E_{\rm total}=E_{\rm constructor\,source}+E_{\rm network}\); the same lower bound applies to the sum. No bound on just the post-construction \(E_{\rm network}\) follows without the length-only restriction. Broadcasting a source bit after one paid read can be arbitrarily shared, but cannot reveal any **other** unread bit. A network whose input is all preloaded as source-dependent advice does not satisfy this model.

For a deterministic exact network, the prior \(\Omega(N)\) YES-ingress lower bound **dominates** the near-\(N^{0.99}\) NETFRONT39 estimate in the \(C,B,p=O(N)\) regime. For a bounded-error randomized network, CHMY STACS2021 Theorem 2 can still prohibit \(E=O(N^{0.99-\epsilon})\) under TMR-3/030 and TMR-1/030's **restricted** fully charged single-work-tape serialization and \(C,B,p=O(N)\); the present independent ingress theorem only forces \(E=\Omega(N^{1-\mu_2})\) at its large \(\mu_2\), often weaker. For the small \(\mu_1\) magnification threshold, the new randomized ingress exponent \(1-\mu_1\) is near one but never exceeds one, much less \(1.01\).

No current statement turns either input-acquisition bound into an \(N^{1.01}\) lower bound for the precise one-way-input, one-work-tape low-threshold MCSP machine. All such computational arrows remain **OPEN**.

## 4. Original prior-work ledger and independently inspected primary sources

| Original source | Statement and scope | Status or role in this run |
| --- | --- | --- |
| research/main/2026-10-20_0548_MAIN_CONDITIONED_HARD_SPARSE_QUERY7.md | Conditioned sparse random source vs zero, arbitrary adaptive source probes; earlier exponent required \(r=N^{\mu+\epsilon}\) or \(\kappa<1-\mu\). | PRIOR, generalized here to arbitrary YES \(x\) and sharp \(r=K_\mu s\), then transferred to charged machine networks. |
| research/main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md | Deterministic nearly-global source read bound on a YES fiber. | PRIOR, stronger deterministic control, not newly claimed. |
| research/agents/tmr-2/2026-11-14_1123_TMR2_GAP_MCSP_HAMMING_CYLINDER026.md | Exact deterministic YES Hamming-cylinder and randomized gap-promise query bounds. | PRIOR; its Gap-MCSP promise is not imported into ordinary MCSP. |
| research/agents/tmr-2/2026-11-14_1618_TMR2_RANDOM_SHARED_SPARSE_MINIMAX031.md | Exact minimax for source-evaluation oracle with zero-vs-r ones, unrestricted sharing. | PRIOR, not itself a physical MCSP source-hardness theorem. |
| research/agents/tmr-3/2026-11-14_1533_TMR3_HIGHMU_NETWORK_EVENT_FRONTIER030.md | High-\(\mu_2\) \(N^{1.99}\) CHMY-bound transfer through bounded-symbol uniform networks; constructor peak-space correction. | PRIOR restricted network baseline, not superseded in randomized large-\(\mu\) regime. |
| research/agents/tmr-1/2026-11-14_1605_TMR1_SHORT_HEADER_CONSTRUCTOR_SIMULATION030.md | One-work-head, short-header constructor simulation \(O(C(\log\log N)^2)\); finite V8 tests. | PRIOR claimed repair pending **independent low-level simulation peer audit**; not assumed in proof of SHARPSPARSE43. |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; 2026-10-28_1326_CLAUDE_TPORT-0001.tex; 2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex | Crossing sequence transport, portfolio barrier, failed uniform direct-product hitting-set hypothesis. | ORIGINAL controls. No SAT transfer borrowed. |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, p.23:3 [1] | Ordinary full-table \(MCSP[N^{\mu_1}]\), one-way read-only input + one two-way writable work tape, deterministic; **conditional** lower bound \(N^{1.01}\) implies \(P\ne NP\). | Magnification premise still OPEN. |
| Same, Theorem 2, p.23:3 [1] | Ordinary full-table \(MCSP[N^{\mu_2}]\), \(\mu_2\) different and close to 1, randomized two-sided error; excludes \(\mathrm{BPTIME}_1[N^{1.99}]\). | KNOWN THEOREM at larger threshold. |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2–1.3 [2] | Search-MCSP with oracle gates, \(s(n)\ge n\), one-pass streaming small-workspace/update magnification conditions; check exact oracle and variant before any transfer. | Background only, not invoked in proof. |
| Buhrman, de Wolf, TCS 2002, pp. 21–43 [3] | Standard deterministic/randomized decision-tree and certificate complexity framework. | Context only; our counting/coupling argument is self-contained. |

Primary papers: [1] https://doi.org/10.4230/LIPIcs.STACS.2021.23 (published 2021-03-10, Theorems 1–2 visually checked on printed p.23:3); [2] https://doi.org/10.1145/3313276.3316396 (STOC 2019, accepted version https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf); [3] https://doi.org/10.1016/S0304-3975(01)00144-X (2002). Threshold constants \(\mu_1,\mu_2\) are **distinct and unspecified** in the quoted statements. No gap, approximation, partial/succinct, MKTP or SAT reduction is assumed.

## 5. Actually executed evidence and hostile controls

The EXACT standalone V8 function now published at experiments/tmr/tmr3_sharp_sparse_network043.js was executed in the research tool before publication, yielding immutable raw JSON at results/raw/tmr/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK043_RAW.json. It performed **739 assertions, zero failures**, 1,146,600 hypergeometric source-hit comparisons and 163,800 exhaustive sparse-neighbor membership comparisons.

The small exact circuit model used \(n=4\), \(N=16\), at most two gates, and independently enumerated **90** YES truth tables. All \(\binom{16}{4}=1820\) four-flip neighbors of each of the 90 YES tables were checked; the maximum number that remained YES was 24, a fraction 0.013187. Each of 630 random-permutation read-position checks matched exactly \(\binom{16-q}{4}\) no-hit supports for \(q=0,\ldots,6\).

Independent numerical asymptotic controls computed \(\log_2D\), \(\log_2\binom Nr\), and the expected-query lower bound for \((n,\mu,K)=(10,0.25,8),(12,0.5,8),(14,0.6,8),(16,0.5,8)\). The respective combinatorial minus circuit-description log margins were 184.256, 1302.433, 4306.785, and 8573.135 bits. At tiny \(N=16\), the general circuit-description bound \(D\) is too coarse to certify the observed true 0.013187 fraction; the 90-table exact enumeration supplies that **finite** fact. The tests are not a physical multitape or network emulator, not an MCSP solver on large source tables, and not an asymptotic proof. The mathematical proof above supplies the latter.

Hostile controls include compact two-gate XOR-like/AND/OR/NOT truth tables, all YES sources rather than only zero, exhaustive sparse completion, adaptive zero-trace reuse, sharing and rereads. No fixed SAT solver or Horn/GF(2)/bounded-treewidth algorithm is excluded by the theorem, because the source is an explicit full truth table.

## 6. Exact gap, review requests and next target

The new lower bound charges **data ingress**, not intrinsic arithmetic, abstraction potentials, proof generation, or general SAT consistency. The exponent \(1-\mu<1\) is below the \(N^{1.01}\) low-\(\mu_1\) one-work-tape hardness-magnification premise. The deterministic YES bound is \(N-o(N)\), also only linear. It is compatible with arbitrary polynomial work and with a correct hypothetical P-time 3-SAT solver. It cannot settle \(P\) versus \(NP\).

**Peer review requested:** TMR-2 independently check the \(\binom Nr\ge(N/r)^r\) constant-factor regime, all-YES extension, and expected-query coupling with randomized adaptive source-aware preprocessing. TMR-5 independently audit the exact charged network source-ingress model, whether any constructor or initial distribution is accidentally free, and the comparison to NETFRONT39. TMR-1 verify the distinction between \(\mu_1\) and \(\mu_2\). TMR-4 test whether a fully syntax-aware succinct SAT-to-MCSP reduction can bypass the full-table data-ingress premise without free exponential expansion.

**Next concrete target:** Try a post-ingress lower-bound invariant that provably charges computations **after** all \(N\) source bits are read, remains valid under compact circuit/algebraic summaries and cache/recompute strategies, and applies to the exact small-\(\mu_1\) one-way-input single-work-tape model. Seek a falsifying uniform algorithm first.

**Publication and root status:** Two root proof trackers and the full canonical main.tex were recovered, with proof2 and main.tex via authentic Git blob SHA (not empty content endpoint); current statuses remain OPEN. TRACKERS REVIEWED; NO MATERIAL CHANGE. No root manuscript, tracker, role ownership, or schedules altered.

END_OF_REPORT::TMR3::031::2026-11-14_1635_PST
