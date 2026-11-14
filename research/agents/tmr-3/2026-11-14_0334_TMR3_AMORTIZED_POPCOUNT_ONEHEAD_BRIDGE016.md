# TMR-3/016: remove logarithmic per-source-position overhead from the charged one-head multihead simulator

**Pacific timestamp:** 2026-11-14 03:34 PST (America/Los_Angeles). **Role:** TMR-3 Time-Space Tradeoffs. **New TMR3-AP16 claim:** CANDIDATE/RESTRICTED until independent TMR-5/TMR-1 review. **Executed check:** COMPUTATIONAL. **Unrestricted SAT lower bound:** OPEN.

## 1. Specific improvement over the original peer result

TMR-5/014 constructed a fully charged compiler from one fixed $h$-input-head deterministic multitape decider $A$ to one standard locally moving original-source-head decider $B_A$. Its verified *upper bound* is

$$
T_{B_A}(x)\le c_A(L+2)(w+1)(T_A(x)+1),\quad
S_{B_A}(x)\le S_A(x)+c_A(w+1),\quad
w=\lceil\log_2(L+2)\rceil.
$$

Original peer report, source and raw data inspected: `research/agents/tmr-5/2026-11-14_0251_TMR5_ONEHEAD_MULTIHEAD_SIMULATION_AUDIT014.md`, `experiments/tmr/tmr5_onehead_multihead_bridge014.cjs`, `results/raw/tmr/2026-11-14_0251_TMR5_ONEHEAD_MULTIHEAD_BRIDGE014_RAW.json`. This TMR-3 run produces a **distinct charged implementation of the physical source lookup** with amortized constant binary-counter cost for each input-cell advance, without retaining an entire source copy.

**Candidate theorem TMR3-AP16 (fixed-machine model translation).** For every one **fixed finite total uniform** deterministic multitape machine $A$ with $h\ge1$ independently locally moving read-only source heads, fixed $b$ ordinary writable work tapes and finite alphabets, there is one **fixed finite total uniform** deterministic multitape machine $B_A$ with one locally moving read-only source head, preserving all terminal labels and every simulated original work-tape transition, and finite $c_A$ such that for every length-$L$ source $x$,

$$
\boxed{T_{B_A}(x)\le c_A(L+2)(T_A(x)+1),\qquad
S_{B_A}(x)\le S_A(x)+c_A\lceil\log_2(L+2)\rceil.}
\tag{AP16}
$$

This improves the previously established $O_A(L\log L)$ per-logical-transition bound to **$O_A(L)$**, with the same logarithmic extra writable space. It is a simulation *upper bound*. It is not a SAT lower bound, does not assert $T_{B_A}=T_A$, and does not replace the same-machine resource model for $A$.

## 2. Exact amortized source-fetch argument

Set $q=L+1$, $w=\max(1,\lceil\log_2(L+2)\rceil)$. Maintain all $h$ virtual source-head positions $p_i\in\{0,\ldots,q\}$ on ordinary little-endian binary work-tape registers of length $w$. Original $A$ work tapes, symbols and head positions remain physically present and are not discarded. A single source fetch at virtual position $p$ proceeds as follows:

1. The physical source head begins on the left endmarker. Copy the requested $w$-bit virtual position to a scratch $w$-bit countdown register, charging $O(w)$ current-cell reads, writes, head travel and restoration. Initialize a *unary popcount head*: one ordinary writable work-tape head is positioned at integer $K=\operatorname{popcount}(p)$, reached by at most $w$ local head moves; it uses at most $w+2$ visited cells.
2. As long as $K>0$, decrement the scratch number and move the physical source head exactly one cell right. If the current positive binary count is $j$ with $t=\nu_2(j)$ trailing zero bits, the little-endian decrement flips those $t$ zeros to ones, flips the first one to zero and restores the counter head to the least significant digit. To maintain exact unary popcount, move its head $t$ cells right and one left, thus $K\gets K+t-1$. This is legal since the count remains nonnegative and requires $O(t+1)$ charged local moves, reads and writes.
3. Zero is detected in **constant time** from the unary head being at its left-endmarker, rather than scanning all $w$ bits on every iteration. After precisely $p$ decrements the scratch register is zero, so the physical source head is exactly at cell $p$. Read the **current** data/endmarker symbol, cache this one of finitely many symbols in finite control, then move the physical source head $p$ cells left to the left endmarker, charging every step. The virtual position register $p_i$ was never changed.

For each $p\ge0$,

$$
\sum_{j=1}^{p}\nu_2(j)
=\sum_{r\ge1}\lfloor p/2^r\rfloor
\le p.
$$

Thus the cost of all $p$ binary decrements **including the popcount-head zero test** is $O(p)$, and the complete symbol fetch costs $O(p+w)\subseteq O(L+2)$ transitions with $O(w)$ visited scratch cells. An explicit serialized micro-operation ledger used in the executed verifier charges

$$
C_{\rm fetch}(p,w)
=5w+5\sum_{j=1}^{p}\nu_2(j)+6p+1
\le 11p+5w+1.
\tag{AP16-fetch}
$$

The ledger treats the $5w$ initialization as a conservative bounded-cost subroutine, not a separately executed hardware TM compiler. A standard multitape implementation can realize this subroutine in $O(w)$ local steps because fixed several heads can traverse corresponding $w$-cell tapes synchronously and move the unary head one step per set bit. The extra microcharges are upper bounds on required physical operations rather than free random access. The same counting argument holds for the left and right source endmarkers, including $p=0$.

A one-time locally moving sweep can measure $L$ and initialize $q$ with amortized binary increments in $O(L+2)$ steps, since encountering the physical right endmarker terminates the sweep. Every simulated $A$ step makes at most the **fixed** $h$ source fetches, reads the unchanged $b$ original work-head symbols, makes the corresponding original writes/head moves, and updates the $h$ virtual addresses by at most one each in $O_A(w)$ ordinary steps. Hence the total cost is $O_A((L+2)(T_A(x)+1))$, with $O_A(w)$ extra writable cells and one finite program independent of $L$. All original transitions, repeated queries, output labels, and malformed inputs are faithfully simulated. No oracle, advice, source-copy table or unbounded word operation is assumed.

### Cost and model sanity controls

* Source positions $p=0$ and $p=L+1$ are genuine endmarkers and are read at their actual physical positions.
* Binary counts $2^r$ have long single carries, but the summation over a **complete** countdown is linear. Charging each step $O(w)$ independently misses this amortization.
* The unary popcount head does NOT encode a large free integer: its position visits at most $w+2$ ordinary writable cells and every move is charged.
* Inputs of length $L$ can have arbitrary valid/invalid content. The compiler merely simulates $A$; it does not classify SAT from parity, Horn form, XOR rank or gadget structure.
* A solver may optimize away the multihead clock. This compiler does not force the simulated trace on every equivalent solver. In particular, no $T_A(x)$ lower bound for arbitrary SAT is obtained.

**Quantifier bridge only, CONDITIONAL:** If the full all-exponent time lower-bound target were established for every correct ordinary one-input-head $B$, this compiler would extend that target to every fixed-$h$ source-head model. An assumed bound $T_A(x)\le C(L+1)^k$ yields $T_{B_A}(x)=O_A((L+1)^{k+1})$ on the **same** sources. Thus using exponent $k+1$ (with a sufficiently large chosen coefficient) for the one-head target would contradict the assumed all-input time bound for $A$. This is an improvement over TMR-5/014's earlier $k+2$ charged transfer, not a proof of the antecedent.

## 3. Actual execution and limitations

**Executed in hosted V8**, with the exact source published separately: all binary inputs of lengths $0$ through $11$ and every possible physical source position on each; five deterministic binary patterns for each of lengths $15,24,25,31,32,63,64,127,128,255,256,511,512,1023,1024$ with boundary, interior and late positions; genuine three-variable 3-CNF sign-stream SAT/UNSAT controls; independent exhaustive checks of the $\sum\nu_2$ identity for all integers $0\le p\le2048$. Results: **49,833** source-position tests, **4,244,205** charged micro-operations, **245,203** binary trailing-zero movements, maximum physical queried position 1025, auxiliary visited-cell upper bound 35, **2,049** independent arithmetic checks, **zero failed assertions**. All 49,833 current-cell reads returned the expected source data/left/right endmarker. The script constructs and charges the countdown and popcount movements, while the $O(w)$ initial-copy microprogram and full arbitrary-$A$ transition compiler are **symbolic**, not a generated Turing instruction table. These experiments are **COMPUTATIONAL**, not asymptotic proof.

Published standalone source: `experiments/tmr/tmr3_amortized_countdown_bridge016.cjs`.
Published immutable raw output: `results/raw/tmr/2026-11-14_0333_TMR3_AMORTIZED_COUNTDOWN016_RAW.json`.

**Independent primary literature:** Fortnow, Lipton, van Melkebeek and Viglas, *Time-space lower bounds for satisfiability*, JACM 52(6), 835–865 (2005), DOI [10.1145/1101821.1101822](https://doi.org/10.1145/1101821.1101822), explicitly excludes certain simultaneous random-access $n^c$ time and $n^d$ space bounds for $c$ below the golden ratio. Its small-space premise is not a claim for arbitrary polynomial-workspace algorithms. The present elementary amortized simulation is proved here and does not use an unstated FLMV theorem or transfer a random-access SAT bound without a compiled interface.

**Historical evidence:** TMR-3/015 complete-configuration upper bound and restricted high-degree positional clock, TMR-1/015 no-copy indexed-source compiler, TMR-1/016 paid one-head parity amplifier, TMR-2/017 source query-certificate gadget (also recovered and reviewed). Its many disjoint sign alternatives impose at most an $O(L)$ source-acquisition cost and do not contradict this simulator. Horn, 2-SAT, Gaussian-elimination XOR, bounded-treewidth, products, padding, variable renaming and auxiliary variables are not algorithmic restrictions on $A$. Their individual implementations were not executed in this run. Existing original peer experiments were read but not replayed natively. Earlier FLMV/ARC small-space lower bounds remain restricted. No new unrestricted time lower bound was derived.

## 4. Status, dependencies, next action

**New AP16:** CANDIDATE/RESTRICTED awaiting TMR-5 independent proof and concrete single-head microcode audit. **Exact binary carry identity:** PROVED/EXACT elementary arithmetic at the stated model. **Finite ledger:** COMPUTATIONAL. **SAT time necessity / P versus NP:** OPEN.

The full-root `proof1.txt` (28,714 characters) and authenticated `proof2.txt` (1,051,196 characters recovered from Git blob SHA `930c5eeddafce656717f28055a7a9a755f44737c`) and `main.tex` (2,528,412 characters recovered from blob) were reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE**, because this tightens a model-translation *upper bound* without proving either all-input SAT proof-chain endpoint. Canonical `main.tex` remains reserved for TMR-5 synthesis. Directive SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4` rechecked before publication. No task/schedule changes.

**Single next target:** Ask TMR-5 to independently audit the charged unary-popcount zero-test, including the at-most-$w+1$ unary-head excursion and exact physical $O(w)$ initialization, then determine whether an alternative one-head source-fetch can be made worst-case $O(p)$ rather than amortized across each full countdown. No unconditional all-exponent SAT bound currently follows.
