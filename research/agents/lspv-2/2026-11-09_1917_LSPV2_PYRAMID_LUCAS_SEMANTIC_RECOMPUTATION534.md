# LSPV-2/534 | XOR pyramid: functional semantics defeats black-pebble memory inference

**2026-11-09 19:17 PST | SAT-Circuit Reduction Builder | Route A | KNOWN THEOREM + PROVED/RESTRICTED corollary + COMPUTATIONAL | P versus NP OPEN**

## Candidate, literature, falsifiers

**Question:** Can a black-pebbling space bound for a succinctly generated circuit be charged to *every* deterministic machine computing that circuit's Boolean function? **No.** This is a restricted **transfer counterexample**, not new SAT hardness.

The example strengthens, for *every height*, Grok H0117's prior finite XOR pyramid/nonmergeability counterexample (`research/agents/grok/2026-10-05_0117_GROK_41774ea2.tex`). It is **not a new black-pebbling or Lucas theorem**. Primary source for the former: Cook 1974 as presented/proved in Nordström, *Short Proofs May Be Spacious*, 2008, Theorem 6.10, https://people.csail.mit.edu/jakobn/research/PhDthesis.pdf ; Nordström 2011, Theorem 3.15, https://www.csc.kth.se/~jakobn/research/RelativeStrength.pdf . FLMV original machine model and sparse normalization: Fortnow, Lipton, van Melkebeek and Viglas, JACM 2005, https://lance.fortnow.com/papers/files/tst.pdf . Later tradeoffs are separate, model dependent: Buss and Williams, 2015, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/ .

Falsifiers: (F1) XOR sharing invalidates the binomial identity (symbolic proof and independent exhaustive replay); (F2) a claimed two-read machine hides binary-length, address/index and output costs (counted below); (F3) algebraic rewrite also works for an arbitrary gate (falsified by an AND-gate control); (F4) a syntactic black-pebble bound automatically applies to native FLMV work tape (falsified by different uniform extensional implementation).

## Exact construction and result

The height-$h$ pyramid has vertices $(r,i)$ with $0\le r\le h$ and $0\le i\le h-r$, and for $r>0$ parents $(r-1,i)$ and $(r-1,i+1)$. There are $(h+1)(h+2)/2$ vertices. In the strict **black pebble** class, loading a source costs a placement; loading an internal vertex requires simultaneous parent pebbles; removal is legal. Every full evaluation requires $h+2$ simultaneous pebbles for $h\ge1$, and a linear-in-vertices placement schedule attains this bound. Source values are charged as pebbles. Black-white pebbling, algebraic identities and alternative algorithms are outside this class.

Assign a source bit $x_i$ to $(0,i)$ and **XOR** at every internal gate. Write $y_{0,i}=x_i$ and $y_{r,i}=y_{r-1,i}\oplus y_{r-1,i+1}$. Induct on $r$ using Pascal's identity to obtain

$$
y_{h,0}=\bigoplus_{i=0}^{h}(\binom{h}{i}\bmod2)x_i.
$$

Over $\mathbb F_2$, $(1+z)^h=\prod_{j:\text{bit}_j(h)=1}(1+z^{2^j})$. Hence the coefficient at index $i$ is one exactly when all set bits of $i$ occur in $h$, i.e. $(i\mathbin{\&}h)=i$:

$$
\boxed{y_{h,0}=\bigoplus_{i:(i\mathbin{\&}h)=i}x_i.}
$$

For $h=2^k$ only $i=0,h$ contribute, so **for all** $2^{h+1}$ source assignments,

$$
\boxed{y_{2^k,0}=x_0\oplus x_{2^k}.}
$$

A distinct uniform algorithm reads only these two bits after constructing their binary addresses. This does not compute the internal DAG vertices, so **no** abstract path-cost map from arbitrary extensional algorithms to the strict pebbling system is proven. A DAG pebble lower bound therefore is **not** a universal machine-memory lower bound.

For every binary source $x$ of length $N\ge2$, define $h_N=2^{\lfloor(3/5)\lfloor\log_2N\rfloor\rfloor}$. We have $h_N=\Theta(N^{3/5})<N$. The fixed succinct circuit generator describes $\Theta(N^{6/5})$ XOR vertices and has black-pebbling price $\Theta(N^{3/5})$ pebbles, yet a fixed uniform deterministic native indexed-tape program scans $N$ bits to obtain length, prepares two input indices, reads $x_0,x_{h_N}$, XORs and outputs using $O(N)$ time and $O(\log N)$ writable native high-water (contiguous counters and index). All source access, index construction, output and peak are charged. There is **no explicit $\Theta(N^{6/5})$ circuit file on the input**; if there were, reading that encoding would incur additional acquisition cost. This is an *all-binary-input circuit function*, **not SAT**, and does not yield the desired all-SAT-input normalization.

## Abstraction polarity, exact models

A complete strict pebble concrete state is $(x,h,G_h,\text{XOR labels},P,\mathrm{pc},t,p)$ with source identity, exact pebble set $P$, cumulative paid events $t$, and peak $p$. Its exact collecting-domain abstraction retains $(P,t,p)$ and all fixed source/gate tags, with $\alpha(X)$ the set of projected states and $\gamma$ the compatible complete states; its legal-placement/removal transformer is exact. Every concrete bounded goal has an abstract path of no greater event cost. The proved pebbling nonreachability for peak $<h+2$ applies to **this declared class only**.

The alternative semantic machine has complete state $(x,N,\text{program},\text{read-only head},\text{index},\text{work cells/heads},\text{pc},t,S_{\max},a)$; a valid upper resource invariant retains the scan phase, counter/index bounds and XOR accumulator. Its own transitions establish $O(N)$ worst-case actual time and $O(\log N)$ actual writable high-water on *every binary input*. There is no lawful lower-bound transfer from $\mathcal M_{peb}$ to this different machine without a simulation-preservation theorem. Number of configurations or circuit vertices is not live writable space.

The user's hypothetical $A_P$ remains a **fixed uniform total deterministic** SAT decider with *assumed* $T_P(N)=O(N^c\operatorname{polylog}N)$ for unknown $c$, all SAT/UNSAT/malformed outcomes, complete guest/ancestor/caches/source phases; a true NP verifier $A_{NP}$ has existential branches and does not decide UNSAT deterministically. Nothing in the XOR computation supplies $A_P$'s required peak-work-space upper bound.

## Exact FLMV exponent firewall

The historical formula is $\beta(c)=\frac12((c+2)/c^2-c)$, positive for $1\le c\lesssim1.52138$. For $c=6/5$,

$$
\beta(6/5)=23/45=1/2+1/90.
$$

A same-machine SAT decider with both time $O(N^{6/5}\operatorname{polylog}N)$ and native space $O(N^{1/2}\operatorname{polylog}N)$ would contradict FLMV; neither is constructed here. SAT in P does not grant $c=6/5$. Later stronger alternation-trading statements require separately matched resource and model hypotheses, and cannot be replaced by an undocumented simple linear-product bound.

**Illustrative exponents, not bytes or finite-$N$ machine bounds:**

| Binary $N$ | Chosen $h_N$ | Strict pebbles | DAG vertices | $N^{23/45}$ | $N^{1/90}$ |
|--:|--:|--:|--:|--:|--:|
| $10^6$ | $2,048$ | $2,050$ | $2,100,225$ | $10^{3.0667}$ | $1.1659$ |
| $10^{12}$ | $8,388,608$ | $8,388,610$ | $3.5184\cdot10^{13}$ | $10^{6.1333}$ | $1.3594$ |
| $10^{24}$ | $1.4074\cdot10^{14}$ | about $1.4074\cdot10^{14}$ | $9.9035\cdot10^{27}$ | $10^{12.2667}$ | $1.8478$ |
| $10^{60}$ | $6.6461\cdot10^{35}$ | about $6.6461\cdot10^{35}$ | $2.2086\cdot10^{71}$ | $10^{30.6667}$ | $4.6416$ |

For large $c$, the particular $\beta$ branch is not positive; no value of $S(N)$ follows from assumed polynomial $T(N)$.

## Independent controls and corpus authentication

Python and independently written Node.js each passed **2,562 checks** and agreed on all height-by-height results. Exact finite BFS covered pebbling heights 1–4, including spurious impossible low-peak goals; XOR exhaustively covered all input strings for heights 0–9 and checked 80 deterministic patterns per height for 10–15. Both checked Lucas support cardinality and two-input powers-of-two. An AND pyramid at all-ones inputs rejects any operator-agnostic XOR shortcut. Both independently reconstructed signed original K4 strict 3-CNF sources in binary S3C format, 6 variables and 16 clauses: odd-charge UNSAT (0 models; SHA-256 `55ca7c9e2034c0055f24ce06e2915c7f21f3f34e5bf169535060e43cb452ffdd`) and even-charge SAT (8 models; SHA-256 `233470a40d069d061d83572d24e0c2776a9f18729111c7c589d2e2992f0ca1cb`), plus six malformed-source rejections each. Small K4 classification is exhaustive and has no asymptotic hardness force. No native FLMV machine or historical R_mix341 checker executed.

Report source cross-checks: governing 16:24 handoff, abstract-negative handoff, AGENTS.md, CODEX.md, repo skill, current issue #3, both root trackers, recent LSPV-2/533, LSPV-5/473, LSPV-1/551, the original Grok H0117, MODELBRIDGE-0010. Change-aware code searches in konard/p-vs-np, blkph0x/p-vs-np-proof-research and relevant formalization repositories found no universal SAT model bridge. Older Grok already captured the *finite* pebbling/functional divergence; the new parameterized result is an explicit all-heights algebraic countercontrol, not proof-system novelty. Exact published code and raw JSON below.

Paths: `experiments/arc/lspv2_534_pyramid_xor.py`, `experiments/arc/lspv2_534_pyramid_xor_independent.mjs`, `results/raw/arc/2026-11-09_1917_LSPV2_534_PYRAMID_LUCAS_RAW.json`.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Relevant IDs: [P1-01], [P1-03], [P1-04]; [P2-A1], [P2-A2], [P2-A3], [P2-C3], [P2-D1], [P2-B1], [P2-B2], [P2-L2-533], [P2-L5-473], [P2-L1-551]. Preserve OPEN statuses, historical R_mix341 rules/weights, all five roles and schedules, 2 Route A/3 Route B and enabled states. No automations modified.

**Next arrow OPEN:** show a uniform, recursively iterable solver-intensional all-SAT-input transformation preserving SAT/UNSAT/malformed with fully charged same-machine $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$; XOR gate cancellation and strict pebbling do **not** establish it. P versus NP OPEN.
