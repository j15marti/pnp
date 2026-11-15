# TMR-4/050: Count-preserving configuration-path quotient, exact sampler tariff, and reverse-compiler firewall

2026-11-15 10:39 PST (America/Los_Angeles). TMR-4 / PNP Cost-Sound Abstraction. **Status: PROVED/RESTRICTED mathematical lemma; independent mathematical review OPEN; finite audit COMPUTATIONAL.** P versus NP **OPEN**.

## Priority, candidate, falsifiers (stated before source analysis)

Governing first priority: [Allender MajMajSAT five-agent integration](../../coordination/2026-11-15_ALLENDER_MAJMAJSAT_FIVE_AGENT_INTEGRATION.md), SHA \`1760aefab5944a063f64b62142e358fbd2b94235\`. Earlier fusion-Lipschitz and TMR replacement directives remain subordinate. No task/schedule mutation.

**Candidate:** An *exact counting-semiring*, branch-respecting zero-cost quotient of a time-layered randomized configuration graph preserves every fixed-outer-word acceptance numerator, hence both nested inclusive majority predicates, without double-counting shared DAG nodes. In a fully specified two-coin finite machine, the seven-coordinate clock potential has an exact rational LP tariff.

Four independent falsifiers:
1. Free metadata SCC quotient *duplicates or removes randomized branch multiplicities*.
2. A quotient that forgets the random prefix may have *different outgoing accept counts* from purportedly equivalent states.
3. Boolean support, a shortest accepting path, or unrestricted sharing may erase the distinction between 3/4 and 1/4 acceptance and between outer majority labels.
4. A free precounted answer edge or a purported zero-price generation of exponentially many arithmetic checkpoint terms is a genuine **reverse-compiler shortcut**, not evidence for local machine lower bounds.

## Primary sources and exact scope

[1] Allender, Koucký, Ronneburger, Roy, Vinay, *Time-Space Tradeoffs in the Counting Hierarchy* (CCC 2001), original PDF https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf, Section 3.1, Lemma 5, and Section 3.2, Theorem 7. Lemma 5 expands a probabilistic computation's integer path count via checkpoint **sum of products**. For time \(N^\alpha\), space \(N^{1-\beta}\), checkpoint count \(N^\beta\), it constructs a locally described depth \(O(\alpha/\beta)\), size \(2^{O(N)}\) arithmetic circuit. Theorem 7: for each fixed \(0<\sigma<1\), some \(\gamma(\sigma)>0\) excludes MajMajSAT from uniform unbounded-error \(\mathrm{PrTiSp}(N^{1+\gamma},N^\sigma)\). The theorem is *simultaneous resource class noncontainment*, not a pointwise hard family or an algorithm-independent tariff. The paper defines majority inclusively (at least half).

[2] van Melkebeek and Watson, *Time-Space Efficient Simulations of Quantum Computations*, Theory of Computing 8 (2012), Theorem 1, https://theoryofcomputing.org/articles/v008a001/ . A **bounded-error** quantum computation with qualifying constructible resources and admissible amplitudes (algebraic suffices) admits an unbounded-error randomized simulation with time \(O(t\log t)\), space \(O(s+\log t)\). This does not permit treating arbitrary unbounded-error quantum algorithms, constructive amplitudes, or precision as free.

[3] Project: TMR-1/049's exact unique-extension balancing; TMR-2/049's guarded-CNF and existential SAT firewall; TMR-3/049's one-query virtual-interface exponent ledger; TMR-5/045's tie and black-box stochastic-AND falsifier; TMR-4/049's exact repeatable FUSE tariff, all under their original **restricted** scopes. See the five handoffs on main, and root proof trackers/issue #3. No inherited proof authority is promoted.

## Scoped theorem: stochastic zero-cost SCC quotient

Fix a source \(F\), a classical random-branch machine with \(T\) synchronous fair-bit steps, and a fixed external outer word \(y\). A complete concrete state stores \((F,A,\text{control},t,\text{branch history},\text{work state},\text{coin position},\text{metadata},\text{resource ledger})\). Every charged random transition receives one actual coin bit \(b\in\{0,1\}\), costs its declared physical work, and advances the time layer. Zero-cost administrative transitions may exist **only as branch-free, deterministic representational equivalences**, and their SCCs may not advance time, toss a coin, change terminal output, alter source, or affect charged ledger. These zero-cost paths are canonicalized, **not** counted as new stochastic histories.

Let \(Q_t\) be equivalence classes after zero-cost SCC collapse. Require:
- all \(c,c'\in A\in Q_t\) have identical terminal-output labels when \(t=T\);
- for each next class \(B\in Q_{t+1}\), \(\#\{b:\operatorname{cl}_0(\delta(c,b))\in B\}\) is independent of representative \(c\in A\);
- each real coin branch is retained with its multiplicity, even if branches merge in a shared DAG;
- any charged simulation path cost is **no greater than** the corresponding concrete increment, and completion/terminal label is preserved.

Define the integer transition matrix
\[
M_t(A,B)=\#\{b\in\{0,1\}:\operatorname{cl}_0(\delta(c,b))\in B\}.
\]
Its row sum is exactly \(2\). Let \(e_{A_0}\) be the initial one-hot row and \(f_y\) the terminal 0/1 accept-label column.

**Lemma 050A (branch-preserving count transport).** Under the requirements above,
\[
K_y=e_{A_0}M_0M_1\cdots M_{T-1}f_y
\]
is **exactly** the number of accepting length-\(T\) fair-coin strings of the original concrete execution at fixed \(y\). Consequently \(P_y=K_y/2^T\) is preserved, including ties. If \(y\) ranges over \(2^b\) equally represented outer assignments and the inner random execution realizes the intended inner assignment distribution, then the nested MajMajSAT output is exactly
\[
{\bf 1}\left\{
\sum_{y\in\{0,1\}^b}
{\bf1}[\,2K_y\ge2^T\,]\ge2^{b-1}
\right\}.
\]

**Proof.** By induction on layer \(t\), the component \((e_{A_0}M_0\cdots M_{t-1})_A\) is the number of distinct length-\(t\) random-bit strings leading to quotient class \(A\). For each distinct word in \(A\), extension by the two coin labels contributes *integer multiplicity* \(M_t(A,B)\) to every \(B\). Representative-independence makes the multiplication exact. Free administrative SCCs contribute no coin strings; quotienting them changes no multiplicity. At terminal time each class has a unique accepted/rejected label; dotting with \(f_y\) yields the exact accepted count. Applying inclusive threshold once per fixed \(y\), then inclusively across all \(y\), proves the final formula. This proves neither an efficient construction of matrices nor a lower bound on the complexity of deciding those thresholds. QED.

This is precisely the \((\mathbb N,+,\times)\) path algebra, not the Boolean \((\{\bot,\top\},\lor,\land)\) reachability algebra. A shared node may be evaluated once in an arithmetic DAG, but **its incoming path multiplicities still add**. Checkpoint regrouping preserves the identity
\[
(M_0\cdots M_{T-1})_{u,v}
=\sum_{c_1,\ldots,c_{k-1}}
\prod_{j=0}^{k-1}(M_{I_j})_{c_j,c_{j+1}},
\]
where \(M_{I_j}\) is the exact product over a consecutive time block. Circuit depth and a compact gate label are not physical computation work; [1] may use \(2^{O(N)}\) arithmetic gates. No free construction of their values is inferred.

## Fully specified finite transition system and exact tariff

**Machine:** immutable 16-bit Boolean table \(F(y,x)\), fixed \(y\in\{0,1\}^2\); two uniform fair coin bits \(x_1,x_2\); deterministic control step \(t\in\{0,1,2\}\); exact prefix \(p\in[0,2^t)\); free metadata view \(v\in\{0,1\}\); paid-history/coin ledger \(t\). Full abstract state \((F,y,t,p,v)\). The physical Turing-machine bit-level realization of table address computation is **not** claimed.

- Authentic zero-cost **VIEW** toggles \(v\) and changes nothing else. VIEW is administrative, not an extra probabilistic branch.
- Authentic price-one **COIN_b** for \(b\in\{0,1\}\) takes \((t,p,v)\to(t+1,2p+b,v)\) for \(t<2\).
- At \(t=2\), terminal output is exactly the immutable table bit \(F(y,p)\). For this *sampling service*, completed goal means a terminal 0/1 outcome was reached. Threshold computation over all outcomes is **not** in this service.
- The zero-cost SCCs consist of the two views of each \((t,p)\). There are 14 concrete states, 7 SCCs, 14 zero-cost edges, 12 paid branch edges.

The quotient has two integer matrices
\[
M_0=\begin{bmatrix}1&1\end{bmatrix},
\qquad
M_1=\begin{bmatrix}1&1&0&0\\0&0&1&1\end{bmatrix},
\quad
M_0M_1=\begin{bmatrix}1&1&1&1\end{bmatrix}.
\]
Thus each of the four inner words is counted **once** despite two free metadata representatives.

Use the seven ordered columns (CNF, affine, separator, fusion, assumptions, interface, machine) and
\[
\mathbf p(\widehat C)=(0,0,0,0,0,0,2-t),\qquad
\lambda=(0,0,0,0,0,0,1).
\]
Each VIEW row has \(\Delta=0,w=0\); every paid coin edge has \(\Delta=(0,0,0,0,0,0,1),w=1\). No legal transition is omitted. Terminal potential is zero. The exact rational LP's sole active constraint is \(0\le\lambda_{\rm machine}\le1\); other zero coordinates have inactive nonnegative weights. The initial optimum is \(2/1\), attained by \(1/1\), matched by **every actual two-step fair-coin trajectory**. The concrete-to-abstract step simulation uses zero paths for VIEW, and a single authentic corresponding edge of equal cost for each COIN_b; terminal goals and branch labels are retained.

**Restriction:** This is a two-step sampling-work tariff. It is *not* an all-program MajMajSAT decision-time lower bound. It is intentionally only linear in its declared coin depth, and says nothing about the cost of obtaining each terminal table bit from an encoded SAT instance.

## Three genuine falsifiers and a reverse-compiler no-go

**F1: forgetting counts defeats majority.** For \(a=b=2\), let \(F_+(y,x)={\bf1}[y\ne11]\cdot{\bf1}[x_1=0]\) and \(F_-(y,x)={\bf1}[y=00]\cdot{\bf1}[x_1=0]\). Their ordered inner counts are
\[
(K_y(F_+))_{y=00,01,10,11}=(2,2,2,0),\quad
(K_y(F_-))=(2,0,0,0).
\]
Both sets of distinct inner count values are \(\{0,2\}\); both have accepting and rejecting complete branches, and both are trivial Horn/2-CNF controls. But inclusive outer majority evaluates **YES** for \(F_+\) (three true inner majorities) and **NO** for \(F_-\) (one). Support-only quotient is insufficient even on easy inputs.

**F2: false SCC lumping.** At layer one, merge the states with first-coin prefixes 0 and 1. For \(f(x)={\bf1}[x_1=0]\), the number of second-coin edges to accept is respectively **2 and 0**. The required representative-independent weighted outgoing row fails. This quotient is not a valid semiring abstraction. It cannot be repaired by simply deleting genuine coin edges through CEGAR.

**F3: arithmetic DAG sharing does not license Boolean de-duplication.** Two different fair-bit edges to one successor contribute weight **2**, whereas the support adjacency has value **1**. Replacing \(\mathbb N\) by Boolean reachability changes accepted path counts. A shortest accepting branch is also blind to 3/4 versus 1/4 acceptance.

**F4: reverse reconstruction is indispensable for importing class hardness.** Given any \(T\)-coin program and input, an omniscient abstraction may prelabel a single weighted edge to ACCEPT with weight \(K_F\) and one to REJECT with \(2^T-K_F\). It preserves *exact* acceptance probability and allows a zero-price abstract decision after preprocessing, but **constructing \(K_F\)** from the original input has been hidden, not bounded. Indeed the forward simulation inequality is \(W_{\rm abs}\le W_{\rm concrete}\). Allender's *concrete* lower bound does **not** imply a lower bound on \(W_{\rm abs}\) by that inequality. A reverse compiler from uniformly generated abstract strategies to concrete machines with charged construction, random/error semantics, time and space would be necessary for that direction. Nothing here supplies one.

For the same reason, a \(\mathsf{PrTiSp}\) theorem does not supply a nonnegative local tariff, an explicit common hard family, or a superpolynomial SAT decision lower bound. Padding, compact affine circuits, recomputation, sharing, precomputed counts and source access remain genuine MAY operations outside this two-step calculus.

## Exact numerical resource and verification ledger

The reproducible standalone JavaScript on this branch exhaustively evaluates **65,536** Boolean tables \(F:\{0,1\}^4\to\{0,1\}\) and four fixed outer assignments each. It independently compares matrix multiplication to direct popcounts, checks every inclusive inner/outer majority, both tie conditions, all VIEW SCCs, every legal signed tariff row, and the explicit false quotients. **393,294 V8 assertions, zero failures**. It finds 14 states, seven two-state SCCs, 26 total legal transition rows, 98,304 inner ties, and 18,150 outer ties across all tables. All such finite data are **COMPUTATIONAL**, not asymptotic evidence.

- Executed audit: \`experiments/tmr/tmr4_allender_path_semiring050.js\`.
- Exact raw results: \`results/raw/tmr/2026-11-15_1039_TMR4_ALLENDER_PATH_SEMIRING050_V8_RAW.json\`.
- Machine-readable full 7-column matrix: \`results/raw/tmr/2026-11-15_1039_TMR4_ALLENDER_PATH_SEMIRING050_TARIFF_MATRIX.json\`.

Resource accounting: each sample path uses two real fair coin increments and at most two retained prefix bits, plus view and control; the 16-bit source truth table is immutable in this **finite service**, not a source-local formula-to-table transducer. Exhaustive tester runtime/host memory are **not** measured physical per-input complexity resources. No imaginary physical table access, zero-cost computation of \(K_F\), native source compiler, general quantum input interface, or SAT algorithm is asserted.

For comparison, [1] requires \(2^{O(N)}\) arithmetic circuit size when its quasilinear uniform description is expanded, even though depth is \(O(\alpha/(1-\sigma))\) for space \(N^\sigma\). Turning a locally addressable arithmetic circuit into a sub-\(N^{1+\gamma}\)-time, sub-\(N^\sigma\)-space *evaluation machine* is a separate theorem, not automatic from the small local gate labels or the fusion tariff. The bounded-error quantum simulation [2] remains applicable only with its explicit resource/amplitude hypotheses.

## Status, corpus, ownership

Existing TMR-1/049 and TMR-2/049 balanced majority gadgets preserve threshold only in their precisely declared representation; TMR-3/049 gives a conditional one-virtual-query classical simulation with exponents \(\max(r,at+h)\) and \(\max(u,as)\) after its quantum-to-classical conversion; these are not a constructed MajMajSAT-to-SAT reduction. TMR-4/049's repeatable FUSE calculus is a different preauthenticated record system; its gate prices cannot be imported into this fair-coin machine.

Research preflight could not run because this runtime has no direct GitHub network checkout; authenticated connector read the latest directive, the predecessor directives, role protocols, current five handoffs, and issue #3. Root proof1 content was recovered with SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`; root proof2 and main.tex exposed SHAs \`930c5eeddafce656717f28055a7a9a755f44737c\` and \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\` but the connector returned empty content for these oversized blobs, including ranged reads. Their full bodies were **not** independently recovered this run. No root write was attempted. **TRACKERS REVIEWED AT AVAILABLE METADATA/PREVIOUS VERIFIED CLAIMS; NO MATERIAL CHANGE.** Other agents' ownership and all existing schedules preserved.

Historical \`/341\`: **FAIL** as a full logical UNSAT authority; \`/386\`: **RESTRICTED**. Superpolynomial fusion-safe initial gap, fully charged MajMajSAT-to-SAT reduction, complete abstract-to-concrete reconstruction and unrestricted SAT-machine transfer remain **OPEN**. **P versus NP remains OPEN.**

**Next precise bridge:** characterize the weakest *streaming, weighted-lumpable, locally generated quotient* whose successor counts and terminal labels can be computed in \(N^{r+o(1)}\) time and \(N^{u+o(1)}\) space from the original MajMajSAT input; then audit the reversed resource compiler against Allender's strict simultaneous exponent box. Such a compiler cannot be inferred from this restricted clock tariff.
