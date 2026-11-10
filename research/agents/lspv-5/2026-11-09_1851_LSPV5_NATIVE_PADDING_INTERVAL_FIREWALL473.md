# LSPV-5 independent red team: native-space padding and the nonempty FLMV interval [P2-L5-473]

**Time:** 2026-11-09 18:51 PST (America/Los_Angeles)  
**Role:** LSPV-5 Independent Proof Red Team; historical Route B label preserved  
**Status:** **PROVED-RESTRICTED + COMPUTATIONAL; unrestricted SAT-space identification OPEN; P versus NP OPEN**

## Outcome first

Knowing only that a uniform total deterministic SAT solver $A_P$ runs in

$$
T_P(N)=O(N^c\operatorname{polylog}N)
$$

does not determine its space, even on the exact Fortnow--Lipton--van Melkebeek--Viglas (FLMV) random-access Turing-machine model.

There are two different statements that must not be conflated:

1. **The original machine's native space.** In FLMV, a non-index work tape contributes the largest position ever read or indexed. A fixed wrapper can build the binary address $2^{\lfloor r\lfloor\log_2N\rfloor\rfloor}$, jump once, touch one dummy cell, and then run $A_P$. For every fixed rational $r>0$, this preserves the language and the $N^c\operatorname{polylog}N$ time class for $c\ge1$, but forces native high-water $\Theta(N^r)$. Thus a time upper does not even upper-bound the native space exponent of the original machine.
2. **An equivalent sparse-normalized machine.** FLMV Section 2.1 states that accessed cells can be stored in an appropriate data structure, preventing space from exceeding time with at most polylogarithmic time overhead. This gives an equivalent representative with normalized exponent $\sigma\le c$, not a fact that the original machine used that space and not an exact value of $S$.

Combining this normalized upper with published lower bounds yields a nonempty interval, not a contradiction. In the common exponent notation $T=N^{c+o(1)}$, $S=N^{\sigma+o(1)}$, the displayed FLMV branch and the later alternation-trading product constraint give, within their stated models and strict theorem ranges,

$$
\max\left\{0,\beta(c),2\cos(\pi/7)-c\right\}\ \le\ \sigma\ \le\ c,
\qquad
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right).
$$

At $c=6/5$, the older displayed branch gives $23/45=0.5111\ldots$, while the later product bound gives the stronger lower exponent

$$
2\cos(\pi/7)-\frac65=0.6019377358\ldots.
$$

The normalized feasible interval is therefore approximately $[0.60194,1.2]$, still wide and nonempty. As $c\to\infty$, both known positive lower terms vanish and the coarse interval tends to $[0,c]$.

## IDEA -> SEARCH -> ITERATE

### Initial idea and falsifiers stated before search

**Hypothesis.** Bounded-write random-access transitions might turn the assumed time bound into an upper space exponent and, when combined with FLMV, determine $S$ or cause a contradiction.

**Falsifiable prediction.** The exact machine should admit a source-preserving $S\le O(T)$ conclusion for the original solver, and that upper should cross the published lower envelope for some $c$.

**Falsifiers.** (F1) one legal indexed jump can create large native high-water while touching one cell; (F2) sparse normalization changes the representation/machine rather than measuring the original; (F3) machine conversion or polylog overhead changes exponent bookkeeping; (F4) the resulting lower and upper exponent intervals overlap for every applicable $c$.

### Search and continuity

The run began from the current verified 16:24 five-role handoff, current issue #3, complete root `proof1.txt` and `proof2.txt`, AGENTS.md, CODEX.md, the research instructions, the November 2 governing handoff, and actual current peer/Grok/Claude files.

Fresh peer evidence materially changed the initial idea:

- [P2-L2-533] independently confirmed an exact eight-command sparse indexed-tape simulation and pointed to FLMV Section 2.1's stronger generic normalization. It correctly distinguished native indexed high-water from serialized sparse layout.
- [P2-L1-550] derived the sharp collapse of the optimized 2005 FLMV $d_k(c)$ envelope near $\phi$; this makes clear that the lower exponent can be positive yet extremely small.
- [P2-L3-546] showed that a separately supplied locally checkable proof DAG may be replayed with low live verifier space, while proof acquisition remains unpaid and cannot be converted into a SAT decider.
- [P2-L5-472] already blocked source/branch/proof-cardinality-to-memory inference. The present run adds the distinct native-high-address padding obstruction and a numerical lower/upper interval.

Primary sources reviewed:

- FLMV, JACM 2005, Section 2.1 and Theorems 1.1, 3.1 and 5.7. The model has arbitrary work/index tapes; indexed jumps erase the index; input/output tapes are uncharged; non-index tapes contribute the largest position ever read/indexed. The paper explicitly notes native space can be exponential in time and gives sparse normalization with polylogarithmic time overhead.
- Buss--Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds* (2012): $\operatorname{DTISP}(n^c,n^\epsilon)$ means time $n^{c+o(1)}$ and space $n^{\epsilon+o(1)}$; the cited Williams line gives $c+\epsilon\ge2\cos(\pi/7)$ for SAT, and the paper characterizes the limits of that proof paradigm rather than unrestricted SAT hardness.
- Williams, *Alternation-Trading Proofs, Linear Programming, and Lower Bounds*: resource-trading assumes simultaneous time and space, then applies explicit speedup/slowdown lemmas; it does not derive low space from time alone.
- Cousot--Cousot abstract interpretation and D'Silva--Haller--Kroening ACDCL/Abstract Satisfaction: sound may abstraction, fixed-point refinement and bottom reasoning do not identify a concrete resource value unless the resource counter and its polarity are explicitly related to every concrete transition.
- Savitch-style recomputation remains a control: semantic reachability size or proof-DAG work need not be materialized simultaneously.

Change-aware repository review found no head change from the preceding run:

| Repository | Head | Result |
|---|---:|---|
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | scoped finite-machine material; no SAT live-space theorem |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | representation/recomputation cautions; no universal bridge |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | proof checking remains distinct from solver peak space |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | verified checker does not infer SAT-decider space |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | no changed relevant bridge |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | ETH formalization does not supply this transfer |
| `uds-psl/coq-library-complexity` | `14b5f413d2fb7adecde79c5451b483f9a1af59a8` | no current random-access live-space bridge |
| `leanprover/leansat` | `b83b5d8631ee54bc913b0e6aaf44711c34a50e0d` | repository remains deprecated; not treated as current authority |

Latest Grok file `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex` (blob `d06a2d56...`) concerns finite circuit rewiring, not random-access space. Latest Claude file `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6...`) is sequential one-tape/crossing-sequence scoped and does not transfer to FLMV random access.

### Revised claim

The search falsified the original-machine upper but retained a normalized-equivalent upper. The correct result is the following two-level firewall.

## Lemma 473-A: native high-address padding (PROVED-RESTRICTED)

Let $A$ be a uniform total deterministic FLMV-model machine deciding any language on binary inputs, with $T_A(N)=O(N^c\operatorname{polylog}N)$ for $c\ge1$. For every fixed rational $r>0$, there is a uniform total deterministic machine $A^{\langle r\rangle}$ deciding the same language with the same time exponent and native work-space high-water at least $\Theta(N^r)$.

**Construction.** Scan the input once if its length is not already available, storing $N$ in binary. Let $m=\lfloor\log_2N\rfloor$ and $e=\lfloor rm\rfloor$. Write the binary index $10^e$ on an index tape, perform one legal indexed jump to work-tape position $2^e$, write one dummy mark, then run $A$ unchanged. Malformed sources still reach $A$'s original total parse/reject behavior.

**Costs.** Length acquisition costs $O(N)$ time and $O(\log N)$ index/counter bits; index construction costs $O(r\log N)$ bit steps and bits; one jump/write is constant native steps. Since

$$
2^{\lfloor r\lfloor\log_2N\rfloor\rfloor}=\Theta(N^r),
$$

the FLMV native largest-position measure is $\Theta(N^r)$ although only one dummy data cell is nonzero. For $c\ge1$, $O(N)+T_A(N)$ retains the assumed time class. Correctness and source identity are unchanged. Because $r$ is arbitrary, $T_A$ does not upper-bound the original machine's native space exponent.

This does **not** claim physical allocation of $N^r$ bytes. It exploits the exact native metric specified by FLMV and is precisely why their paper separately introduces sparse normalization.

## Lemma 473-B: normalized exponent interval is nonempty (PROVED-RESTRICTED)

Apply the FLMV sparse representation to obtain an equivalent solver $\widehat A$ with polylogarithmic time overhead and $\sigma\le c$ in exponent notation. For $c>1$,

$$
\beta(c)<c.
$$

Indeed, $\beta(c)<c$ is equivalent to $c+2<3c^3$, with equality at $c=1$ and strict inequality thereafter. Also, with $L=2\cos(\pi/7)<2$,

$$
L-c<c
$$

for every $c\ge1$. Hence every interval

$$
\left[\max\{0,\beta(c),L-c\},c\right]
$$

is nonempty wherever the cited lower bounds apply. The sparse-normalization upper cannot by itself contradict either lower bound. A contradiction requires an additional same-machine transformation that forces $\sigma$ **strictly below** the applicable lower envelope.

The optimized FLMV $d_k(c)$ family also cannot conflict with the coarse upper: by definition $d_k(c)\le c^{-k}\le1<c$ for $c>1$. This independently verifies the direction of [P2-L1-550].

## Complete concrete/abstract configuration and transformers

For fixed authenticated machine/source $(M,x)$, use complete concrete states

$$
\sigma=(M,\operatorname{auth}M,x,\operatorname{auth}x,q,I,W,h_I,h_W,\mathit{idx},\mathit{out},\mathit{parse},\tau,H,U,B,L,L_{\max}),
$$

where $I$ is read-only input; $W$ is the exact finite work/index-tape map; `idx` is the current binary index content; $H$ is the largest non-index position ever read/indexed; $U$ is the set of touched cells; $B$ the nonblank cells; $L$ current explicit live representation bits; and $L_{\max}$ their high-water. Nondeterministic states additionally carry the current choice port and semantic history tag, without summing mutually exclusive branches.

Concrete domain $C=\mathcal P(\Sigma)$ is ordered by inclusion. The abstract product is

$$
A=\mathsf{Auth}\times\mathsf{MayPC}\times\mathsf{Parse}\times
\mathsf{Int}(\tau)\times\mathsf{Int}(|\mathit{idx}|)\times\mathsf{Int}(H)
\times\mathsf{Int}(|U|)\times\mathsf{Int}(|B|)\times\mathsf{Int}(L)\times\mathsf{Int}(L_{\max}).
$$

$\alpha$ preserves exact authentication sets and takes may-unions/interval hulls; $\gamma$ contains all complete states satisfying every component. Thus $X\subseteq\gamma(\alpha(X))$. Relevant transformers are:

- input scan: $\tau':=\tau+1$, input head advances, $L$ changes only for explicit counter bits;
- append index bit: $\tau':=\tau+1$, $|\mathit{idx}|':=|\mathit{idx}|+1$;
- indexed jump: $\tau':=\tau+1$, $H':=\max(H,\operatorname{value}(\mathit{idx}))$, target enters $U$, and the index is erased;
- write/clear: update exact $W,B,L,L_{\max}$ and one step of time;
- deterministic step: functional post; nondeterministic step: relational union with per-branch maxima, never cross-branch storage;
- sparse-normalization step: **not** an abstract transformer on the same state space; it is a machine/representation conversion that stores $(\text{address},\text{symbol})$ records and must charge dictionary operations, address bits and peak storage.

The sound abstract post is $\operatorname{Post}^{\#}=\alpha\circ\operatorname{Post}\circ\gamma$. An upper endpoint for $H$ bounds native high-water only if all concrete states are covered. An upper endpoint for sparse $L_{\max}$ bounds the converted representation, not $H$ of the original machine. A lower resource result needs a universal per-run invariant or an underapproximate witness with proved polarity; may-state cardinality, $|U|$, $|B|$ and proof-node count do not supply it.

Abstract Satisfaction can intersect the exponent constraints and ACDCL can learn conflicts among incompatible bounds. Here the intersection is nonempty, so failure to derive bottom is correctly **inconclusive**—not evidence that a polynomial SAT solver exists.

## Numerical controls

The executable used exact rational arithmetic for $\beta(6/5)=23/45$ and $1/90$, checked $\beta(c)<c$ on 3,239 rational cases, checked 40 finite high-address wrappers with three assertions each, and evaluated twelve exponent intervals. Total Python assertions: **3,373**. An independent JavaScript implementation passed **3,293** checks.

For $c=6/5$, illustrative growth laws are:

| $N$ | $N^{23/45}$ | $N^{2\cos(\pi/7)-6/5}$ | normalized coarse upper $N^{6/5}$ |
|---:|---:|---:|---:|
| $10^6$ | $1.166\times10^3$ | $4.089\times10^3$ | $1.585\times10^7$ |
| $10^{12}$ | $1.359\times10^6$ | $1.672\times10^7$ | $2.512\times10^{14}$ |
| $10^{24}$ | $1.848\times10^{12}$ | $2.796\times10^{14}$ | $6.310\times10^{28}$ |
| $10^{60}$ | $4.642\times10^{30}$ | $1.307\times10^{36}$ | $10^{72}$ |

These are exponent-law illustrations, **not bytes**, and suppress constants, $o(1)$ terms, word/address representation and conversion overhead.

## Independent challenges and controls

- **Does the wrapper silently assume $N$?** No. A complete source scan costs $O(N)$ time and $O(\log N)$ counter bits, already within the assumed $c\ge1$ time class.
- **Does one jump allocate physical $N^r$ memory?** No; the theorem concerns FLMV's declared largest-position native space. The sparse simulator exposes exactly this distinction.
- **Can sparse normalization prove the original $A$ was low-space?** No. It constructs an equivalent machine and must charge conversion/dictionary operations. This is sufficient for existence statements, not for measuring $A$.
- **Can an NP branch or proof certificate fill the gap?** No. $A_{NP}$ is not a deterministic both-label SAT/UNSAT decider, and [P2-L3-546] explicitly leaves certificate acquisition unpaid.
- **Can finite $N$ values certify exponents or bytes?** No. They only verify formulas and transition accounting.
- **Known shortcut/family ledger:** Haken PHP Resolution hardness, Cook ER, Tseitin GF(2), compact mod-3 adders and shared-DAG shortcuts are unchanged mandatory controls. This run proves no new hard-family lower bound and changes no $R_{\mathrm{mix341}}$ rule or weight.

## Resource ledger

| Phase | Charged result |
|---|---|
| Source/project reads | governing handoffs, both full trackers, issue #3, three latest peer reports, actual Grok/Claude files, primary papers, eight pinned repositories |
| Parsing/source authentication | explicit in state and wrapper; malformed inputs retain original total label |
| Logical work | two restricted lemmas; no ideal-proof discovery charge altered |
| Executable evidence | Python 3,373 assertions; independent Node 3,293 checks |
| Explicit evidence before publication | Python 4,068 bytes; Node 1,521 bytes; raw JSON 13,806 bytes |
| Wrapper time | $O(N+r\log N)+T_A(N)$ including length scan |
| Wrapper native high-water | $\Theta(N^r)$ largest indexed position; not physical bytes |
| Wrapper explicit live bits | $O(r\log N)$ plus $A$'s live representation |
| Sparse conversion | separate machine; dictionary, address, read/write and peak costs required |
| Failed source/policy reads | full issue-comment connector transport closed once; exact GitHub comment endpoints succeeded; no source was claimed read when unavailable |

## Tracker review and disposition

- `proof1.txt`: [P1-01], [P1-03], [P1-04] reviewed; no material change.
- `proof2.txt`: new [P2-L5-473] materially refines [P2-A1], [P2-A2], [P2-A3] and the resource polarity in [P2-C3]. It independently checks [P2-L1-550], [P2-L2-533], [P2-L3-546] and preserves [P2-L5-472]. [P2-D1], [P2-D3], [P2-C3], [P2-B1], [P2-B2] and B3 remain OPEN.

## Actual advance, verification, publication, precise gap

**Advance:** the exact FLMV model now has a proved two-level distinction: arbitrary native-space padding is compatible with fixed polynomial time, whereas sparse normalization supplies only an equivalent-machine upper. Combining that upper with both the displayed FLMV branch and the later $2\cos(\pi/7)$ product bound leaves an explicit nonempty interval.  
**Verification:** 3,373 Python assertions and 3,293 independent JavaScript checks passed.  
**Publication:** report, code, raw data, handoff, tracker delta and issue #3 receipt are published with full readback.  
**Precise remaining gap:** construct a source-preserving, both-label, malformed-aware, recursively applicable transformation on the exact machine that forces the normalized space exponent strictly below the applicable lower envelope while retaining the required time exponent and charging all phases. No such contraction is known. P versus NP remains OPEN.

