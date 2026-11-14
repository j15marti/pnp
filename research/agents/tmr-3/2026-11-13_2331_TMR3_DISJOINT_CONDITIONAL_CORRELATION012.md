# TMR-3/012: disjoint conditional coding does not amplify the aggregate Kraft tail

**Date:** November 13, 2026, 23:31 PST (America/Los_Angeles). **Role:** TMR-3 Time-Space Tradeoffs, j15marti/pnp main. **Mathematical status:** CANDIDATE, complete finite-codebook construction and proof below, pending TMR-5 or TMR-2 independent review. **Finite evidence:** COMPUTATIONAL. **Arbitrary-machine SAT processing lower bound:** OPEN.

## 1. Exact new claim and relationship to the previously proved lemma

TMR-3/010 proved the exact aggregate prefix-free inequality for code lengths z_i depending on a common random input, assuming conditional prefix-free injectivity on q free bits separately at every cut. TMR-5/009 constructed an almost sharp example by repeating ONE codebook on ONE q-bit variable across K cuts. The tempting strengthening is to infer a K-dependent concentration gain when the q free coordinates supporting different cuts are **disjoint and independent**. That inference is false if each conditional codebook is still permitted to depend on all the outside coordinates, as TMR-3/010 explicitly allows.

**Theorem TMR3-DC12 (disjoint-fiber perfect correlation, CANDIDATE pending peer review).** Fix any integers q>t>=1 and K>=2 and put ell=q-t. Let X_1,...,X_K be independent uniform q-bit strings. For every i, there is a deterministic binary code function c_i(X_i;X_{-i}) with the following properties:

1. For EVERY fixed value of X_{-i}, the 2^q codewords as X_i varies are injective and prefix-free.
2. Every length z_i=|c_i| is either ell or ell+q, and on EVERY global vector X all K lengths are exactly equal, although their independently uniform free q-bit blocks X_i are pairwise disjoint.
3. With delta=2^{-t}(1+2^{-q}) and p=2^{-t}-2^{-q}, the aggregate lower-tail event satisfies

$$
\Pr\left[\frac1K\sum_{i=1}^K z_i(X)
<q-\log_2(1/\delta)\right]=p,
\qquad
\frac p\delta=\frac{1-2^{t-q}}{1+2^{-q}}\longrightarrow1
$$

as q grows at fixed t, irrespective of K. In particular, no error bound tending to zero with K follows from **disjoint independence of the free q-bit blocks plus per-block conditional prefix-freeness alone**. This is a theorem about conditional code lengths, not a construction of crossing sequences for a 3-SAT Turing machine.

## 2. Explicit construction and complete proof

Split each q-bit block as X_i=(U_i,V_i) with U_i in {0,1}^t and V_i in {0,1}^ell. Let

$$
U=\bigoplus_{j=1}^K U_j,\quad
V=\bigoplus_{j=1}^K V_j,\quad
E=\{U=0^t,\ V\ne0^\ell\}.
$$

For each i and fixed outside W_i=X_{-i}, define the required high part h_i= XOR_{j ne i} U_j and excluded low value e_i=XOR_{j ne i} V_j. Exactly 2^ell-1 possible X_i satisfy U_i=h_i and V_i ne e_i. Denote this short fiber M_i(W_i).

Define c_i as follows. For X_i in M_i, give the ell-bit binary representation of its zero-based lexicographic rank in M_i, which takes the values 0,...,2^ell-2. This uses every ell-bit word EXCEPT 1^ell. For all other X_i, give the length-(ell+q) word

$$
1^\ell\ \Vert\ X_i.
$$

For any fixed W_i, each short word is unique, none equals 1^ell, and every long word starts with 1^ell and has a distinct q-bit suffix. The code is injective and prefix-free, including cross-length pairs. Its Kraft sum is

$$
\kappa=\frac{2^\ell-1}{2^\ell}
+\frac{2^q-(2^\ell-1)}{2^{\ell+q}}
=1-\frac{2^\ell-1}{2^{\ell+q}}<1.
$$

The condition X_i in M_i(W_i) is EXACTLY U=0^t and V ne0^ell, which does not depend on i. Therefore ALL z_i(X) are ell exactly on E, and ALL equal ell+q outside E. Since XOR of independent uniform q-bit blocks is itself uniform, Pr(E)=(2^ell-1)/2^q=2^{-t}-2^{-q}.

For the stated delta, the aggregate threshold is q+log_2(delta)=ell+log_2(1+2^{-q}), strictly between ell and ell+1; thus precisely E is the strict lower-tail event. Taking q to infinity at fixed t gives p/delta ->1. The construction and proof apply for ANY K>=2, even if K grows with q. QED, subject to independent review for project promotion.

**Nonfree computability audit:** This example does not assume an oracle to choose a codebook. The total XOR of all blocks can be computed by a single fixed finite multitape program with O(q+log K) writable cells and a conservative polynomial O(K q^2+K log(K+2)) transition bound on an explicitly delimited source. Given the stored XOR and one Xi, one can derive the outside XOR, select short versus long, compute the rank with finite-width binary subtraction, and emit its code in paid polynomial time. This does NOT make these strings crossing transcripts of a correct SAT decider; actual physical input layout and crossing continuity would require a separate simulation theorem.

## 3. Reproducible exhaustive experiment and hostile control

Published source: experiments/tmr/tmr3_disjoint_conditional012.cjs. Immutable raw: results/raw/tmr/2026-11-13_2329_TMR3_DISJOINT_CONDITIONAL012_RAW.json. The exact source function was evaluated in the hosted V8 execution environment and serialized into the Node-compatible published executable (same function body, no wrapper invocation). It was NOT run natively under OS Node.

Parameters: 15 deterministic (q,t,K) cases, q=3,...,8, 2<=K<=4, no random seed. For each conditioned outside assignment and each i the tester explicitly generated all 2^q codewords, sorted them, checked adjacent prefix violations, checked exact count of short words and Kraft. It then exhausted all global vectors and asserted identical K lengths, equivalence to E and the exact strict tail probability.

| Executed test | Count |
|---|---:|
| Parameter cases | 15 |
| Complete global X vectors | 474,176 |
| Conditional fibers | 34,192 |
| Conditional codewords constructed | 1,378,944 |
| Sorted adjacent prefix comparisons | 1,344,752 |
| Cases falsifying the artificial independent-cut delta^K bound | 15 |
| Failed assertions | 0 |

A small hostile example is q=4, t=2, K=4: the error event has exact probability 3/16=0.1875 while delta=0.265625 and delta^4=0.0049782395362854. Every cut uses a DIFFERENT free block, but all four lengths are short together. The tested finite case is COMPUTATIONAL evidence, not the asymptotic proof.

**Controls and scope:** The construction explicitly preserves conditional prefix-freeness and independence of X_i, so merely adding these conditions cannot repair an invalid K-concentration claim. It does not force any real SAT solver to build, store, or traverse the codes. Real programs may use GF(2) elimination, Horn/2-SAT solvers, bounded-treewidth DP, products, shared computations, padding, reencoding, rereading, caching or recomputation; no hypothetical universal lower bound is applied to these algorithms, and they were not independently executed here. The XOR correlation here is an easy algebraic operation, not an assumed exponential computational obstruction.

## 4. Consequence for the actual same-machine T/S proof program

The exact published TMR-3/010 statement survives. The new example does NOT refute its probability bound or TMR-3/011's still-CANDIDATE crossing/injective-splice premises. It strengthens TMR-5/009's negative conclusion: even **disjoint independent local information supports** cannot improve the aggregate tail solely from the per-cut conditioned Kraft inequalities when codebooks may depend on outside source bits. Any stronger probability theorem must prove additional physical/causal restrictions on the crossing transcripts, not infer independence from disjoint q-subvectors.

For one fixed total uniform deterministic multitape SAT decider A, encoded input bits L, actual transitions T_A(F), and SAME-run visited writable work cells S_A(F), the existing conditional crossing product has only

$$
T_A(F)(S_A(F)+1)=\Omega_A(Lm)
$$

on the original easy batched equality sources. For m=Theta(n^alpha), 0<alpha<=1 and L=Theta(n log n), this excludes only simultaneous exponents k+s<1+alpha, up to logs. It excludes NO candidate with k>=2. From S_A(F)<=O_A(T_A(F)+1) on a standard LOCAL multitape machine, the product gives at best a fixed polynomial time exponent, not all exponents. It does not transfer as a small-space statement through the input-copy bridge: that bridge adds Theta(L) writable space. Actual local-source transport, crossing transcripts, and post-acquisition processing cost are distinct quantities. In particular, this conditional-code result is not a SAT T/S lower bound of its own.

**Unresolved OPEN arrows:** (a) independently audit whether TMR-3/011's physical splice coding truly covers every locally moving transition; (b) prove any additional *same-physical-machine* causality structure that forbids the conditional-code adversary, or accept that marginal Kraft is optimal; (c) prove a noncircular superpolynomial post-copy processing invariant valid for arbitrary polynomial workspace and all uniform SAT deciders. No hard-input witnesses may be combined from different A runs. Neither P=NP nor P!=NP is proved.

## 5. Corpus, prior art and publication discipline

First read the superseding TMR replacement directive, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Read root proof1.txt (28,714 chars, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and proof2.txt (full authentic Git blob 1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c, ordinary file fetch returned blank), root main.tex (authentic Git blob 2,511,782 chars, SHA c04a02a97492f88938791f363ff91d99b67cd78b), current issue #3 through TMR-2/013, AGENTS.md, CODEX.md, repo research skill, current five peer handoffs and original TMR-3/010-/011, TMR-5/009, TMR-4/013, TMR-1/013 and TMR-2/013 reports.

Primary literature inspected for exact scope: Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), https://doi.org/10.1145/1101821.1101822 and https://lance.fortnow.com/papers/files/tst.pdf, especially Theorem 1.1 and section 2.1. Their random-access model has index tapes, and establishes for each c<golden ratio some d>0 excluding simultaneous time n^c and space n^d, NOT arbitrary polynomial workspace or a purely time lower bound. Hennie (1965), original one-tape/offline crossing-sequence ancestry, https://ntrs.nasa.gov/citations/19660035639, supplies context, not this new conditional code theorem. Our theorem is self-contained Kraft/prefix-code combinatorics and does not claim any published SAT lower bound from those papers.

**Tracker action:** TRACKERS REVIEWED; NO MATERIAL CHANGE. New TMR-3 report and handoff only. Canonical root main.tex is not modified, leaving synthesis to TMR-5. No tasks or schedules changed. Actual code/raw/report publication requires direct GitHub readback. Local clone, native Node execution, OS Python tests and LaTeX compilation were not performed.

**One next target:** TMR-5 or TMR-2 independently verify the disjoint-fiber prefix-free construction, then test whether actual complete crossing sequences impose enough joint causal restrictions to permit probability amplification beyond the marginal Kraft bound. Keep post-copy processing and all-exponent SAT resource lower bounds OPEN.

END_OF_REPORT::TMR3::DISJOINT_CONDITIONAL_CORRELATION012::2026-11-13_2331_PST
