# TMR-3/049: Allender forbidden-region ledger and one-query post-quantum-simulation virtualization

**2026-11-15 10:25 PST | PNP Time-Space Tradeoffs | ALLENDER_ONEQUERY049**

**Status:** A source-conditional one-query compiler lemma and a rational speedup/slowdown calculation are PROVED/RESTRICTED as stated, pending independent mathematical review. An actual MajMajSAT-to-SAT compiler and a matching SAT algorithm have **not** been constructed. Finite rational checks are COMPUTATIONAL. P versus NP is OPEN.

## 1. Candidate and four falsifiers (stated before source/corpus search)

**Candidate.** Simulate a *bounded-error quantum SAT algorithm* first, on an explicitly encoded SAT input, by the van Melkebeek–Watson unbounded-error randomized algorithm. Only **after** that transformation serve the new *classical* input-head accesses from a deterministic virtual query generator. When the outer exact reduction makes at most **one** SAT query, this ordering preserves the strict >1/2 acceptance sign without coherent quantum input generation or unbounded-error oracle composition. If both resource exponents enter the forbidden region of Allender et al., the assumed pair of compiler and SAT solver cannot both exist.

- F1: Replacing ONE query by two weak unbounded-error randomized oracle answers may make the whole acceptance probability cross the wrong side of 1/2.
- F2: Materializing a linear-size query on a writable tape may force linear writable space even when the solver itself uses sublinear space.
- F3: Serving each input access by a slow virtual generator, or omitting its head/address/buffer costs, can make a formal time exponent unsound.
- F4: Assuming that Allender noncontainment itself gives a local fusion tariff, a common hard input family, or a genuine MajMajSAT-to-SAT compiler would change quantifiers/model and is invalid.

All four are live controls, not grounds for silently disallowing an authentic shortcut.

## 2. Primary-source statements and scope

[1] Allender, Koucký, Ronneburger, Roy and Vinay, *Time-Space Tradeoffs in the Counting Hierarchy*, CCC 2001, Theorem 7: for every fixed 0<sigma<1 there exists gamma(sigma)>0 for which

\[
\mathrm{MajMajSAT}\notin\mathrm{PrTiSp}(N^{1+\gamma(\sigma)},N^\sigma).
\]

Here PrTiSp is a uniform **unbounded-error probabilistic** simultaneous time/space class, and N is input encoding length. Theorem 7 follows via quasilinear-size, polylog-local, logarithmic-workspace reductions from the second linear-time counting-hierarchy level. Majority is inclusive (at least half). This is a LANGUAGE NONCONTAINMENT, not a specific explicit hard-family result or a lower bound against SAT.

[2] van Melkebeek and Watson, *Time-Space Efficient Simulations of Quantum Computations*, Theory of Computing 8 (2012), Theorem 1: a **bounded-error** quantum algorithm with algebraic transition amplitudes, time T>=log M and space S>=log M, gives a classical **unbounded-error** randomized algorithm in O(T log T) time, O(S+log T) space, with the paper's constructibility assumptions. Their Theorem 3/Corollary 1 is the quantum lower-bound extension, not part of the 2001 paper. The stronger paper-specific approximability results are NOT invoked.

Primary links:
- [1] https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf , especially pp. 4–6 and 9–10 (PDF zero-index 3–5 and 8–9).
- [2] https://www.cs.memphis.edu/~twwtson1/papers/qts.pdf , especially pp. 2, 4 and 44 (PDF zero-index 1, 3 and 43).
- ECCC publication record: https://eccc.weizmann.ac.il/report/2001/041/

The latest 2026-11-15 Allender integration directive (Git blob 1760aefab5944a063f64b62142e358fbd2b94235) takes priority over prior fusion work. TMR-1/049 supplied a balanced unique-extension equality; TMR-2/049 supplied a literal CNF and proved that merely asking SAT(G) and SAT(not G) gives constant YES answers. TMR-5/045 found a weak-error composition falsifier. The current result complements, rather than replaces, those results.

## 3. New conditional **one-query virtual-compiler lemma**

Let L be MajMajSAT. Assume ONE fixed deterministic, total, exact uniform oracle reduction R from L to SAT, correct on every valid encoded input of length N. It makes **at most one** adaptive SAT query q(x); given x, the postquery deterministic output is a Boolean function of the one answer, so it is one of constant 0, constant 1, the identity, or negation. The full source is immutable and accessible to R.

Write the following as upper bounds, including all source parsing, index formation, query-length determination, retained reduction state, address registers, scratch and paid rereads:

- R's nonoracle work: O(N^r polylog N) actual sequential steps.
- R's peak retained writable space, including any query generator: O(N^u polylog N).
- The virtual SAT query has encoded length M <= O(N^a polylog N), and R has an **exact deterministic uniform** generator that returns bit j (or the endmarker) in O(N^h polylog N) actual steps **per access**, using only already-budgeted O(N^u polylog N) space. The generator must preserve the source, R state and query identity on every call, and writes no uncounted persistent copy.
- A bounded-error, algebraic-amplitude uniform quantum SAT machine Q has time O(M^t polylog M), workspace O(M^s polylog M), with constructible bounds and compatible finite-input model as required in [2]. Include the quantum input-access model and classical simulator configuration in these resources. Exponents a,t,s,r,u,h are fixed nonnegative reals and meaningful for M >= 2.

**Lemma.** In the same input-access cost model in which [2]'s randomized simulator is implemented, the composition can be decided by a uniform unbounded-error randomized machine with

\[
T_{\mathrm{comp}}(N)=N^{\,\theta+o(1)}, \quad
\theta=\max\{r,\;at+h\},
\qquad
S_{\mathrm{comp}}(N)=N^{\,\eta+o(1)}, \quad
\eta=\max\{u,\;as\}.
\]

In particular, if for some fixed 0<sigma<1

\[
\theta<1+\gamma(\sigma),\qquad \eta<\sigma,
\]

then **not all the hypotheses above can hold**.

**Proof.** Apply [2] Theorem 1 **once to Q on an explicitly given SAT formula** to obtain a conventional randomized B that, on each explicit input q, accepts with probability strictly above 1/2 if q is SAT and strictly below 1/2 otherwise. B takes O(M^t polylog M) physical simulator steps and O(M^s polylog M) workspace, absorbing the additional log(T) time and log(T) space terms. B is *not* yet being called as an unbounded-error oracle by a multi-query computation.

Instead execute one copy of B while answering each of its ordinary classical query-input symbol requests by R's exact deterministic virtual generator. B makes no more input accesses than its step count. Hence the total generated-access work is O(N^{at+h} polylog N), in addition to R's O(N^r polylog N) work; store B's configuration, source and R's retained information, generator scratch, heads, indices and output, with total peak O(N^{max(u,as)} polylog N) visited writable cells. O(log N) book-keeping is included, and different overlapping work types are not blindly added as separate lower bounds.

On each fixed outer input x, R either produces a constant answer or accepts iff SAT(q), or accepts iff NOT SAT(q). Constants are implemented deterministically; the identity case uses B; the negation case flips B's output. Because this is **only one** probabilistic call, its strict probability sign is preserved. There is no amplification hypothesis or invalid adaptive PP-oracle substitution. Thus the composed machine recognizes L in the prohibited PrTiSp region under the two strict inequalities, contradiction with [1]. QED.

**Model firewall.** This lemma has not compiled a quantum coherent virtual-input oracle. It **first** uses the theorem [2] to turn Q into B with *classical* requests. It assumes that the paid virtual generator faithfully serves that B model; translating to a different one-tape locally moving model requires an explicit additional time/space overhead, not zero-price model switching. Uniformity and mathematical correctness of the alleged exact R are essential. No such R is known.

## 4. An explicitly rational Allender speedup/slowdown chain

This is an independently checked parameter fragment of [1] Theorem 4, Lemmas 5–6, and their hierarchy contradiction.

Assume hypothetically

\[
\mathrm{PrTime}(n)\subseteq\mathrm{PrTiSp}(n^\alpha,n^{1/2}),\quad \alpha>1.
\]

Choose the **rational padding exponent** b=3/2; then b*(1/2)=3/4<1. Padding gives

\[
\mathrm{PrTime}(n^{3/2})\subseteq
\mathrm{PrTiSp}(n^{3\alpha/2},n^{3/4}).
\]

By arithmetic Nepomnjascii (Lemma 5), the right-hand class lies in LCH_k for a finite integer

\[
k\ge\max\{2,\tau(3\alpha/2,1/4)\}.
\]

Set the **explicit rational**

\[
d=1+\frac1{4(k-1)}>1.
\]

If LCH_2 were in PrTime(n^d), Lemma 6 would yield LCH_k in PrTime(n^{d^{k-1}}). The binomial bound, for integer k>=2,

\[
d^{k-1}=\sum_{j=0}^{k-1}
\binom{k-1}{j}\frac1{4^j(k-1)^j}
<\sum_{j=0}^\infty 4^{-j}=\frac43<\frac32,
\]

would imply PrTime(n^{3/2}) subset PrTime(n^{d^{k-1}}), contradicting the unbounded-error probabilistic time hierarchy in [1], Theorem 2. Therefore

\[
\mathrm{LCH}_2\not\subseteq\mathrm{PrTime}(n^d)
\]

under the stated small-space simulation hypothesis. This proves the **rational parameter validity**, not the missing hypothesis, and never assigns a numerical value to tau or gamma. This is an exact source-justified speedup/slowdown fragment, not a new P-vs-NP separation.

## 5. Checked forbidden-region ledger

Fix sigma=3/4 and let

\[
g=\min\{\gamma(3/4),\,1/4\}>0.
\]

For the following **hypothetical** input/query/solver exponents take a=1, r=1+g/8, t=1+g/4, s=u=1/2, one query unless noted; all exponents denote full charged bounds, not a claimed SAT solver. The strict source ceilings are time 1+gamma(3/4) (at least 1+g), space 3/4.

| Case | Time exponent from upper ledger | Writable-space exponent | Exact conclusion |
|:--|:--|:--|:--|
| **One virtual classical query, h=g/4** | 1+g/2 | 1/2 | INSIDE strict forbidden region; exact compiler AND Q cannot coexist |
| One **materialized** length-N query | 1+g/4 | 1 | OUTSIDE space region; no contradiction from [1] |
| N virtual queries, h=g/4, b=1 | 2+g/2 | 1/2 | Upper-budget calculation OUTSIDE time region (not a runtime impossibility theorem) |
| One virtual query with slow h=g | 1+5g/4 | 1/2 | Upper-budget calculation OUTSIDE time region |
| One virtual call, weak Pr solver, then a second weak call with AND output | naive budget irrelevant | naive budget irrelevant | Semantics FAIL without an independent bias-composition proof |

For the base one-query scenario, the time slack is at least g/2, and the space slack is 1/4. Polylogarithmic overhead from [2] is absorbed by any smaller fixed slack, e.g. g/4 in time and 1/8 in space, without specifying a numerical gamma. For a general Q=N^b many-query **bounded-error quantum** classical-control compiler, composition-before-simulation may give the *conditional* upper time b+at+h and space max(u,as) after amplification, **only when a charged model-correct virtual quantum input interface has been proved**. Simulating Q to weak Pr and then making multiple adaptive Pr calls does NOT have this consequence.

### Exact falsifier to weak-error composition

A weak unbounded-error YES subroutine with independent acceptance probability 17/32 is correct as a one-query Pr sign test. Combining two such YES calls by Boolean AND accepts with probability (17/32)^2=289/1024<1/2, so this is a genuine WRONG answer despite each component being on the correct sign side. In contrast, flipping a *single* weak answer changes 17/32 to 15/32 and preserves the required sign. The construction uses exact rational probabilities and requires no unjustified amplification.

### Same-realization network workspace

If P=N^p **simultaneously live** processors have separate actual writable spaces of at least N^v distinct cells each, aggregate private workspace is at least N^{p+v} (plus scheduler, buffers and messages); a span of N^z is NOT sequential work N^z. For p=v=1/2, the true aggregate is N despite each local work tape and the span possibly being sublinear. Shared physical cells count once; one may not double-count overlapping memories or invent a P*span lower bound when processors can be idle. All simulator generations and messages must be paid. This is a resource firewall, not a new unconditional machine lower bound.

## 6. Fusion-Lipschitz connection and strict limits

The source-to-virtual-bit operation is a **genuine charged interface conversion** in the cost ledger, not a free abstract edge. Repeated virtual reads, source authentication, addresses, buffers, the randomized simulator state, retention, and recomputation all belong to the same execution. This makes the bridge *compatible with* the existing seven-component vector tariff, but it supplies an **upper bound** for a hypothetical compiler, not a nonnegative local lower-bound certificate.

A cheap artificial abstract answer edge of cost 0 illustrates the reverse-reconstruction failure: it can undercharge every concrete path and make every abstract goal accessible for free. Allender language noncontainment neither forbids such an overapproximation nor proves that any positive abstract initial potential survives it. To derive a SAT-machine theorem one must still prove every authentic local rule tariff, a large initial gap, and same-machine transfer. TMR-3/048's prepared-marker physical suffix is a distinct restricted service, not an implementation of this virtual reduction. TMR-1/049 and TMR-2/049 preserve exact nested-majority ties but their gadgets do not solve SAT-oracle threshold compilation.

**Critical OPEN arrows:** existence of a total exact uniform one-query MajMajSAT-to-SAT reduction of the specified locality/workspace; existence of the stated SAT Q solver; proof of a general multi-query error/model interface; any arbitrary SAT-machine fusion tariff and a superpolynomial potential. Existence of the one-query reduction would already have major unproved counting-hierarchy consequences. Do NOT derive SAT hardness by reversing a SAT-to-MajMajSAT inclusion.

## 7. Reproducible exact-rational verification and publication

The separately published self-contained Node/V8 source performs full BigInt rational arithmetic; it checks 1,024 synthetic rational g values 1/4096..1/4 for all five strict region comparisons and 159 integer k values 2..160 for the exact rational d bound, plus weak-majority composition controls. **8,672 exact assertions, zero failures.** These sample g values do **NOT** purport to instantiate the unknown source gamma. The symbolic inequalities above prove the all-positive-g claim; the finite checks are COMPUTATIONAL.

Files:
- Report: research/agents/tmr-3/2026-11-15_1025_TMR3_ALLENDER_ONEQUERY_VIRTUAL_EXPONENT049.md
- Executable: experiments/tmr/tmr3_allender_onequery049.js
- Raw: results/raw/tmr/2026-11-15_1025_TMR3_ALLENDER_ONEQUERY049_V8_RAW.json
- Machine-readable region ledger: results/raw/tmr/2026-11-15_1025_TMR3_ALLENDER_ONEQUERY049_FORBIDDEN_REGION.json
- Preserved full-history handoff: research/agents/tmr-3/handoff.md

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 complete Git blob SHA 930c5eeddafce656717f28055a7a755f44737c, root main.tex complete Git blob SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Current issue #3 and all five handoffs consulted; repository-wide preflight/full test suite not run (connector-only checkout unavailable). No shared tracker or schedule edit.

**Handoff:** TMR-1 check the use of k>=tau in the rational hierarchy chain; TMR-2 test existence/black-box impossibility for a single exact MajMajSAT-to-SAT query with logarithmic virtual-bit addressing; TMR-4 insist on zero-cost closure and a real rule-by-rule tariff rather than treating this upper compiler budget as a potential; TMR-5 independently attack the strict sign-preservation and per-access model translation. Independent mathematical review OPEN. P versus NP OPEN.
