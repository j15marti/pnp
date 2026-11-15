# TMR-5/045: Allender–MajMajSAT tie-bias firewall, conditional compiler budget, and independent fusion controls

**2026-11-15 09:45 PST (America/Los_Angeles) | PNP Machine Bottleneck Redteam | ALLENDER045**

**Status:** The tie normalization and sample-only information bound are PROVED/RESTRICTED by the explicit mathematics below, subject to independent mathematical peer review. The deterministic-oracle/quantum SAT compiler is **CONDITIONAL** on its stated interfaces and model translations. Finite exhaustive checks are **COMPUTATIONAL**. All unrestricted P versus NP implications are **OPEN**.

## 1. Candidate and four predeclared falsifiers

**Candidate:** The known Allender et al. small-space MajMajSAT bound can audit a *fully specified* reduction/simulation from a hypothetical fast SAT subroutine, but cannot by itself serve as a fusion potential or as evidence that a probabilistic majority oracle can be replaced by one cheap randomized test. The exact near-tie bias gives an explicit quantitative obstruction to the latter replacement.

**Falsifiers stated before focused source/corpus review:**

1. A strict unbounded-error machine already classifies the *at-least-half* equality case with constant bias, invalidating the small-bias construction.
2. Polynomially many independent weak-majority samples uniformly amplify a bias of $2^{-\Theta(m)}$ to bounded error with no additional work.
3. Materializing an $\Omega(N)$-bit oracle query requires only $N^\sigma$, $\sigma<1$, writable space in the claimed physical model.
4. The compiler silently switches from MajMajSAT to SAT, from a uniform full language to an explicitly hardwired family, from one whole-machine time/space pair to unrelated executions, or from bounded-error quantum to unrestricted quantum/unbounded-error probabilistic composition.

The first three are falsified by exact counts, a sample-only information inequality, and a physical writable-tape definition. The fourth remains a mandatory audit gate for any proposed compiler.

## 2. Primary-source scope and hierarchy bookkeeping

[Allender, Koucký, Ronneburger, Roy and Vinay (CCC 2001), Theorem 7](https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf), Section 3.2, prove for **each fixed** $0<\sigma<1$ the existence of some $\gamma(\sigma)>0$ for which
\[
\operatorname{MajMajSAT}\notin\operatorname{PrTiSp}(N^{1+\gamma(\sigma)},N^\sigma).
\]
This is **uniform unbounded-error probabilistic language noncontainment** with both bounds on the **same** algorithm, not a pointwise lower bound on a common explicit instance family, not a superpolynomial lower bound, and not a result for arbitrary polynomial workspace. Their majority convention is **at least half** for the inner and outer quantifiers. The reduction direction in their proof is $\mathrm{LCH}_2\longrightarrow\operatorname{MajMajSAT}$ with quasilinear target length and locally computable output bits; it is not a MajMajSAT-to-SAT reduction. The paper does not supply a numerical $\gamma$.

[van Melkebeek and Watson (Theory of Computing 2012), Theorem 1](https://www.cs.memphis.edu/~twwtson1/papers/qts.pdf) simulate **bounded-error** quantum time $t$, space $s$ with algebraic transition amplitudes by **unbounded-error probabilistic** time $O(t\log t)$, space $O(s+\log t)$, assuming $t,s\ge\log N$ and the stated constructibility bounds; their more general approximability conditions have separate hypotheses. With fixed polynomial exponents strictly inside Allender's forbidden region, the logarithms can be absorbed in the positive exponent margins. This quantum extension is not part of Allender's original paper. Arbitrary unbounded-error quantum computations and arbitrary real amplitudes are not covered automatically.

The Allender conclusion is $\forall A$ with a forbidden simultaneous resource **uniform bound**; it does not give $\exists (F_N)$ such that the same $F_N$ is worst-case for every $A$. It does not establish $P\ne NP$.

## 3. New exact at-least-half to strict-PP normalizer

For $m\ge2$, let $F:\{0,1\}^m\to\{0,1\}$ and $S(F)=|\{x:F(x)=1\}|$. Choose $(b,x)$ uniformly from $\{0,1\}^2\times\{0,1\}^m$. Define one accepted sampling outcome by this *complete* four-branch rule:

| Two-bit prefix $b$ | Accept exactly when |
|---|---|
| $00$ | $F(x)=1$ |
| $01$ | $F(x)=1$ |
| $10$ | always |
| $11$ | $x=0^m$ |

There are exactly $2S(F)+2^m+1$ accepting outcomes among $2^{m+2}$ equally likely outcomes. Consequently
\[
p_F=\frac{2S(F)+2^m+1}{2^{m+2}},\qquad
p_F>\tfrac12\iff S(F)\ge2^{m-1}.
\]
The construction is *uniform*: evaluating its branch predicate uses one actual evaluation of $F(x)$ on prefixes $00/01$, a paid $m$-bit all-zero test, and otherwise finite control. It faithfully converts the **inclusive** majority threshold into **strictly greater than half**, including ties. The $+1$ is essential. It is **one** majority quantifier, not a free solution to two nested majority quantifiers.

Consider the explicitly easy formula pair
\[
F_m^+(x)=x_1,\qquad
F_m^-(x)=x_1\wedge\neg(x_2\wedge\cdots\wedge x_m).
\]
Their satisfying counts are $2^{m-1}$ and $2^{m-1}-1$. The normalized acceptance probabilities are exactly
\[
p_+=\tfrac12+\epsilon_m,\qquad
p_-=\tfrac12-\epsilon_m,\qquad
\epsilon_m=2^{-(m+2)}.
\]
Both formulas are short and straightforward to recognize; the following bound is strictly **black-box/sample-only**, not a formula-processing or SAT runtime lower bound.

### 3.1 Exponential sample-only amplification barrier

Suppose a decoder is shown only $K$ independent Bernoulli outcomes of the above normalizer, with a hidden choice between $F_m^+$ and $F_m^-$, and must identify which distribution was used with probability at least $2/3$ on each case. For $\epsilon=\epsilon_m\le1/8$,
\[
D_{\rm KL}(\operatorname{Ber}(\tfrac12+\epsilon)\Vert
\operatorname{Ber}(\tfrac12-\epsilon))
=2\epsilon\ln\frac{1+2\epsilon}{1-2\epsilon}
\le 16\epsilon^2.
\]
The relative entropy of $K$ samples is at most $16K\epsilon^2$. Pinsker's inequality gives total variation at most $\sqrt{8K}\epsilon$. Both error probabilities at most $1/3$ require total variation at least $1/3$. Hence
\[
\boxed{K\ge\frac1{72\epsilon_m^2}
=\frac29\,4^m.}
\]
An adaptive rule using at most $K$ samples obeys the same bound by padding unused samples. This proves an **exponential cost in this *specific* sample interface** to amplify the near-tie PP bias. It cannot be exported as a computational lower bound because direct formula inspection, counting techniques, algebra, circuits, sharing, and arbitrary SAT/PP algorithms are legal outside this black box.

A second exact counterexample: two independent yes-majority tests that each output YES with probability $p_+$, followed by an AND of the sampled YES bits, accept with probability $p_+^2\le (9/16)^2<1/2$ for every $m\ge2$. Thus the naive substitution of two weak random decision bits for two correct PP oracle answers does not preserve even the sign of the acceptance bias, before any adaptive or nested issues.

**Fusion implication:** One legal weak-majority sample may simultaneously touch multiple syntactic/semantic obligations. It cannot be treated as an *exact, free* discharge of those obligations or as a constant-error oracle. Conversely, the exponential sample-only lower bound is not a fusion-safe initial potential for arbitrary machines.

## 4. Conditional deterministic-oracle to quantum-SAT compiler lemma

This is a **conditional interface theorem**, not a claim that the required reduction exists.

Let $R$ be **one uniform deterministic total exact SAT-oracle** reduction deciding MajMajSAT length $N$. Assume at most $q(N)\le N^b$ sequential, possibly adaptive SAT queries, each length at most $N^a$, with total nonoracle time $O(N^r)$ and peak retained writable space $O(N^u)$. Include all query construction, parsing, addresses, outputs, scheduler, and retained state in these charges. Let the SAT subroutine $Q$ be one **uniform bounded-error** quantum machine with algebraic (or appropriately approximable) amplitudes, time $O(m^t)$ and space $O(m^s)$ on every query length $m$. Assume the classical-control/quantum-machine interface implements $R$ and measured calls to $Q$ at at most polylogarithmic multiplicative overhead; if it does not, the exact translation overhead must be separately inserted.

For **materialized writable queries**, independent bounded-error repetition $O(\log(q+2))=O(\log N)$ per query, with a measured majority of repetitions, reduces each call's conditional error to at most $1/(6\max(1,q))$. Union bounding over all adaptive calls makes the entire oracle transcript correct with probability at least $5/6$. The SAT query work tape and $Q$'s writable cells exist on the **same** execution. Therefore the compiled quantum computation has
\[
T_{\rm comp}(N)=O\bigl(N^{\max(r,b+at)}\operatorname{polylog}N\bigr),
\quad
S_{\rm comp}(N)=O\bigl(N^{\max(u,a,as)}\operatorname{polylog}N\bigr).
\]
No tiny unbounded-error bias is used in this composition: *bounded* error is a mandatory premise.

For any fixed $0<\sigma<1$ and its unknown Allender exponent $\gamma(\sigma)>0$, if the **same** compiled algorithm satisfies both **strict** inequalities
\[
\boxed{\max(r,b+at)<1+\gamma(\sigma),\qquad
\max(u,a,as)<\sigma,}
\]
then van Melkebeek–Watson followed by Allender yields a contradiction. This is a quantitative **conditional compiler exclusion**, not a lower bound for SAT from $P=NP$.

**Sharp materialization firewall:** If any input family forces $R$ to actually write an $\Omega(N)$-bit query into its writable memory, its peak writable space is $\Omega(N)$ on those inputs; in the exponent template this is $a\ge1$. It cannot meet the $\sigma<1$ space requirement even if the SAT subroutine itself uses logarithmic space. The important exception is *virtual read-only* query access. For an independently justified virtual bit evaluator of cost $N^h$ per target read with its address/state already included in $u$, the corresponding **conditional** bookkeeping becomes
\[
\theta_{\rm virt}=\max(r,b+at+h),\quad
\eta_{\rm virt}=\max(u,as),
\]
plus full quantum/reversible-interface and bookkeeping costs if nontrivial. No such MajMajSAT-to-SAT virtual compiler has been constructed or verified here.

**Fixed exponent versus separation:** Even a successful forbidden-box contradiction would exclude only specified near-linear/sublinear-space MajMajSAT implementations. A fixed positive $\gamma(\sigma)$ remains polynomial time; it does not establish a superpolynomial bound for unrestricted SAT or drop the small-space restriction.

## 5. Independent peer fusion reproductions and hostile transfer

### TMR-1/048: repeatable one-gate/one-batch FUSE

In its **preauthenticated** exact record model, $t$ unpaid distinct gate IDs, pending set $U$ needing $\tau(U)$ actual batches, and one separate mandatory HALT have minimum paid work
\[
W_{\min}=\max(t,\tau(U))+h.
\]
**Independent symbolic check:** every paid CHECK/FUSE pays at most one new gate and every BATCH/FUSE discharges at most one batch, so at least $\max(t,\tau(U))$ transitions are needed; a minimum batch cover can be paired with $\min(t,\tau(U))$ genuine FUSE operations, followed by the remainder individually. A separate HALT adds $h$. This matches the TMR-1/048 restricted theorem. The original model's zero-cost metadata VIEW never touches the paid ledger. **PASS/RESTRICTED**, not an arbitrary SAT or MajMajSAT execution theorem.

### TMR-2/048: huge Cartesian mutation count, linear optimal read tariff

Independently reconstructed the claimed vector at unread counts $u_i\in\{0,\ldots,q\}$:
\[
p_{\mathrm{sep}}=\min_i u_i,\qquad
p_{\mathrm{fus}}={\bf1}[\forall i:u_i>0],\qquad
p_{\mathrm{int}}=\prod_i u_i.
\]
Reading one original sign in copy $i$ decrements $u_i$ and causes nonnegative component drops bounded by $(1,1,q^{r-1})$. This **simultaneously** maximal row exists at $(u_1,\ldots,u_r)=(1,q,\ldots,q)$, reading copy 1's last unread sign. The complete nonnegative cone for these three coordinates is therefore
\[
\lambda_{\mathrm{sep}}+\lambda_{\mathrm{fus}}+
q^{r-1}\lambda_{\mathrm{int}}\le1.
\]
At the all-unread initial vector $(q,1,q^r)$ the exact optimum is $\max(q,1,q)=q$, although the raw Cartesian mutant count is $q^r$. The independent enumerator checked every legal count transition for $q=2,\ldots,5$, $r=2,\ldots,4$ (8,478 priced rows), including the maximizing witness. **PASS/RESTRICTED** for the count-vector calculation. Authentic source witness construction remains dependent on the peer's separate source verification; the Gaussian-elimination shortcut and absence of superpolynomial time inference are preserved.

### TMR-3/048: prepared physical multihead suffix

The claimed exact $1+\max(d_0,d_1,d_2)$ lower and matching sweep are plausible **only in the explicit already-staged-marker physical service**. With one local head per tape, simultaneous source read and two writes must be charged as **one** real transition, not three additive ones; the original-source marker creation remains excluded and is a necessary end-to-end cost. This run **did not independently replay the full physical simulator**. Verdict **RESTRICTED; independent low-level machine compiler OPEN**.

### TMR-4/049: repeatable heterogeneous FUSE and overlapping-cover failure

Under TMR-4's genuine **singleton batch** grammar and catalogue $B=\{2\}$, let $t$ distinct unpaid identities and $u$ distinct unpaid singleton batches remain. The optimal amount of gate work saved is
\[
M_{\{2\}}(t,u)=2\min(\lfloor t/2\rfloor,u).
\]
The independently enumerated Bellman recurrence, with price-one CHECK, BATCH, FUSE$_2$ and distinct HALT, agrees with
\[
W(t,u)=t+u-M_{\{2\}}(t,u)+1
\]
on all 130 states $0\le t\le12$, $0\le u\le9$. **PASS/RESTRICTED**.

However, importing the formula into a new **overlapping** batch menu $E=\{\{a\},\{b\},\{a,b\}\}$ by replacing $u$ with the minimum cover $\tau=1$ is FALSE. At $t=4$ and pending $\{a,b\}$, a real legal sequence is FUSE$_2(\{a\})$, FUSE$_2(\{b\})$, HALT, cost **3**. The naive overlapping-$\tau$ potential is **4** and would violate one genuine unit-cost row. Independent exhaustive shortest-path enumeration gave the same length-three witness. **FAIL** for the cross-grammar imported potential; no original peer theorem is invalidated.

## 6. Ranked dependency/status map

| Rank | Dependency | Status and independent evidence |
|---|---|---|
| 1 | Allender Theorem 7, exact $N$, fixed $\sigma$, unknown $\gamma(\sigma)$ | KNOWN THEOREM, primary source checked |
| 2 | van Melkebeek–Watson Theorem 1, bounded error, constructibility, algebraic amplitudes | KNOWN THEOREM, primary source checked |
| 3 | Strict-PP inclusive-majority normalizer and $\Omega(4^m)$ sample-only near-tie amplification | PROVED/RESTRICTED symbolic; 8,674 actual assertions overall; independent mathematical review OPEN |
| 4 | Materialized deterministic SAT-oracle compiler exponents and conditional quantum contradiction | CONDITIONAL theorem; no MajMajSAT-to-SAT compiler established |
| 5 | TMR-1/048 max/tau Bellman and TMR-2/048 Cartesian tariff | PASS/RESTRICTED; independent symbolic and count-vector replay |
| 6 | TMR-4/049 singleton batch knapsack formula | PASS/RESTRICTED; 130 exact Bellman cases |
| 7 | Imported overlapping-cover knapsack formula | FAIL; authentic three-step path |
| 8 | TMR-3/048 prepared physical suffix to blank-tape SAT machine | RESTRICTED model, end-to-end transfer OPEN |
| 9 | Exact two-level majority-preserving uniform compiler to fast SAT calls | OPEN; no reduction or error-safe oracle composition supplied |
| 10 | Fusion-safe superpolynomial SAT potential plus arbitrary-correct-machine transfer | OPEN; cannot follow from counting-class noncontainment |

**Historical authorities:** /341 stays **FAIL** as full logical UNSAT authority; /386 stays **RESTRICTED**. Neither is repaired, relabeled or used here.

## 7. Reproducibility and preflight

The independent self-contained executable is [experiments/tmr/tmr5_allender_tie_blackbox045.js](../../../experiments/tmr/tmr5_allender_tie_blackbox045.js). Its immutable raw data are [results/raw/tmr/2026-11-15_0945_TMR5_ALLENDER045_V8_RAW.json](../../../results/raw/tmr/2026-11-15_0945_TMR5_ALLENDER045_V8_RAW.json). Tests include complete enumeration of all $2^{m+2}$ branches for both tie-boundary formulas for $m=2,\ldots,11$, 32,736 exhaustive sampled-branch evaluations, independent shortest-cost recurrences, original TMR-2 count-vector discharge rows, and the honest overlapping-fusion paid shortcut. **8,674 actual V8 assertions, zero failures**. The sample-only information inequality and conditional compiler lemma are analytic results and are **not** proved merely by those finite tests.

Source recovery: governing new 2026-11-15 Allender directive read **FIRST** (blob 1760aefab5944a063f64b62142e358fbd2b94235), then older fusion/TMR directives; entire root proof1 and authentic complete Git blobs for root proof2 (930c5eeddafce656717f28055a7a755f44737c) and main.tex (6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34); AGENTS.md, CODEX.md, repository research skill; all five current TMR handoffs, issue #3 through TMR-4/049, and original TMR-1/048, TMR-2/048, TMR-3/048, TMR-4/049 reports and relevant original raw. The preflight.py script, native physical TM compiler and LaTeX compilation were **not** run in this connector-based execution. The exact V8 function, rather than a fixed claimed count, generated and validated the published raw numbers.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No edits to proof1.txt, proof2.txt or canonical root main.tex. No changes to any five existing agent schedules, identities, ownership or enabled states.

## 8. Strongest surviving next lemma and peer repair

**Priority repair:** construct or disprove a *specific, uniform, exact, fully charged* MajMajSAT-to-SAT-oracle compiler with both majority blocks and tie behavior preserved, with actual measured exponents $(a,b,r,u)$ and physical/virtual query access. It must preserve adaptivity, actual quantum bounded error or strict PP sign under every call, and aggregate same-execution workspace. For each proposed compiler test the two strict simultaneous inequalities in Section 4 **before** claiming to reach Allender's forbidden box. The $a\ge1$ materialization firewall means any such sublinear-space candidate using long queries must address virtual access explicitly.

Peer checks: TMR-1 verify the hierarchy/reduction quantifiers and whether any locally computable *reverse* reduction is available; TMR-2 verify exact two-block quantifier and tie preservation through auxiliary variables; TMR-3 charge all virtual input reads, logged queries, retained memory and quantum error reduction; TMR-4 enforce all-step path and sign-sensitive abstract semantics, including free-answer-edge falsifier; TMR-5 independently attack every proposed exponent row and the compulsory materialization assumption. P versus NP remains **OPEN**.
