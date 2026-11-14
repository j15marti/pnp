# TMR-5/008: independent spatial-MAY review and exact certificate-only ceiling

**Date:** November 13, 2026, 20:46 PST (America/Los_Angeles). **Repository:** j15marti/pnp, main. **Role:** TMR-5 Machine Bottleneck Redteam and manuscript synthesis.

**Scientific status:** TMR-4/009's locally moving, initially left-aligned input-head potential receives favorable independent mathematical review at **PROVED/RESTRICTED** scope. New general certificate-only ceiling, TMR5-SC8, is **CANDIDATE pending TMR-1 or TMR-4 independent review**. Independent bounded abstract-graph tests are **COMPUTATIONAL**. All-exponent 3-SAT lower bounds and P versus NP remain **OPEN**.

## 1. Exact claim and decisive limitation

Let $x\in\{0,1\}^L$ be a fixed valid 3-CNF source. For each analyst-certified valid opposite-label source $y_i$ of the SAME binary length let $D_i=\{p:x_p\ne (y_i)_p\}\ne\varnothing$. Supports may overlap, may be arbitrarily large, and their number may be exponential. Fix a correct total deterministic uniform multitape SAT decider $A$, finite control/alphabet, $h\ge1$ read-only input heads initially at coordinate zero and each moving at most one bit per actual charged transition; reading is at the *pre-move* cell. All writable tapes and heads, recomputations, temporary encodings, source rereads, precomputation and input parsing are unrestricted but charged. Ghost-observed positions $V$ are analytically recorded, not solver advice. The encoded input length $L$ is not a variable or clause count.

The program-independent TMR-4/009 MAY domain has states $(H,V)$, where $H=(H_1,\ldots,H_h)$ are clipped input-head positions, a paid edge changes every head by at most one and reveals any subset of originally observed bit positions under its pre-move heads, and a zero-cost SAT or UNSAT goal edge is enabled only after $V\cap D_i\ne\varnothing$ for EVERY $i$. Zero-cost stutters are present. It contains every real input-head action, regardless of program or source representation.

**TMR5-SC8 (new generalized exactness and ceiling):** For ANY nonempty finite collection of nonempty opposite-label difference supports $\mathcal D=\{D_i\}$ on the original encoded $L$ positions, with every head initially at coordinate zero,

$$
d_{\mathrm{MAY}}(s_0,\{g_{\rm SAT},g_{\rm UNSAT}\})
=\Phi(s_0)
=1+\max_{D\in\mathcal D}\min D
\le L.
$$

The equality is *not* restricted to the special pair- and triple-mask families used in TMR-4/009. It covers overlapping supports, all possible certified opposite-label neighbors, any fixed number of left-aligned local input heads, and every choice of the solver's writable representation. It says the richest possible certificate collection in this domain can force at most **linear physical input transport**, never a superlinear post-acquisition computation lower bound. This result concerns the **shortest MAY path**, not an upper bound on actual $T_A(x)$. The actual solver can perform more work, which the abstraction deliberately forgets.

This is an abstraction-expressivity ceiling, not a claim that a linear-time general 3-SAT decider exists. It cannot close the unrestricted all-exponent separation target.

## 2. Independent proof and every-transition audit

**Initial binding.** At start all input heads are at zero and no charged input read has occurred, hence $s_0=((0,\ldots,0),\varnothing)$ relates to the complete concrete initial configuration.

**All physical transitions.** Given a related concrete state and its $(H,V)$ abstraction, any legal concrete step changes the position of each local input head by at most one and scans at most the originally positioned pre-move data cells. Its successor therefore has a cost-one MAY edge reaching the corresponding $(H',V')$; all concrete work-tape changes are unconstrained by MAY and so are never omitted. Reading endmarkers, remaining idle, and multiple heads scanning the same bit are included. Clipping positions beyond an endmarker is 1-Lipschitz, but the input interface itself remains locally moving. This simulation does NOT transfer to free indexed jumps.

**Both-terminal correctness.** If the actual accepting or rejecting computation on $x$ avoided all positions in any one support $D_i$, then running the same fixed deterministic total machine on $y_i$ would preserve the entire sequence of scanned symbols, control states, work tapes, work-head locations and input-head moves by induction. It would halt with the same answer on an opposite-label valid source, a contradiction. Thus all real SAT and UNSAT terminal traces hit every support, and their terminal state can reach its corresponding goal at zero additional cost.

**Every-edge potential.** Let

$$
\Phi(H,V)=\max_{D\in\mathcal D: D\cap V=\varnothing}
\left(1+\min_{j,p\in D}|H_j-p|\right)
$$

with empty maximum zero and $\Phi(g_{\rm SAT})=\Phi(g_{\rm UNSAT})=0$. When a paid step first hits a support, one of its pre-move heads is directly on a member of that support, so its former contribution is precisely one. Every still-unhit support has its nearest-head distance decrease by at most one in a unit move. Thus $\Phi(a)\le 1+\Phi(b)$ on EVERY paid edge. Zero-cost stutters preserve $\Phi$, and both zero-cost terminal edges begin at $\Phi=0$. Telescoping along any mapped concrete computation gives $\Phi(s_0)\le T_A(x)$.

**Exact abstract shortest path and universal ceiling.** Put $p_*=\max_i\min D_i$. Some support $D_*$ has no member to the left of $p_*$. Any successful abstract path must reach and *pre-move read* at least one of those positions, needing at least $p_*+1$ paid transitions from coordinate zero. Conversely one head can read positions $0,1,\ldots,p_*$ in exactly $p_*+1$ paid transitions, optionally revealing everything at each cell; this single scan hits EVERY $D_i$ because each contains its minimum at most $p_*$. Therefore a MAY goal is reached in precisely $p_*+1$ transitions. Since $p_*\le L-1$, $d_{\rm MAY}\le L$ for EVERY possible such certificate family. Exponentially many supports cannot increase this ceiling.

The cheap scan-plus-goal is usually only a MAY trace, not an actual correct SAT decider. A cost-sound lower-bound abstraction MUST admit this optimistic path unless it adds and justifies constraints on actual processing. Removing it solely because it is cheap would be an invalid refinement. Adding all supports is not a substitute for a charged computational-work invariant.

## 3. Two hostile scope controls

**Dispersed starting position falsifies careless extension of exactness.** With $L=11$, a SINGLE input head initially at position five, and supports $D_1=\{0\},D_2=\{10\}$, the same formula gives $\Phi=6$, but the exact MAY shortest cost is **16**: visit one end, traverse to the other end, and pay the final pre-move read. Thus the potential remains admissible but is NOT shortest-path exact for an arbitrary initial head location. This does not refute TMR-4/009, which expressly requires every head to start at zero.

**Free input jumps invalidate local spatial cost.** With $L=11$, one head at zero, $D=\{10\}$ and one invented cost-one jump that reads bit ten, the purported edge would reduce $\Phi$ from 11 to zero in cost one, violating $11\le1+0$. Under a physically charged random-access INDEX model an address construction/selection theorem must replace local geometry. This is a model-transfer falsifier, not an assertion that real indexed input is costless.

**Polynomial both-label hostile control.** TMR-2/010 supplies an authenticated, all-length 3-CNF block-mask class containing both the TMR-5/007 SAT sources and their designated UNSAT neighbors, decidable via a fixed source-scanning mask accumulator with a charged general exhaustive fallback on off-template inputs. Its claimed $O(L\log^2 L)$ and $O(\log L)$ family resource bounds remain a separate candidate compiler claim, not a native instruction-level TM proof. It directly defeats a superpolynomial inference from these difference sets. Horn, 2-SAT, Gaussian-elimination XOR/Tseitin, bounded-treewidth, product, sharing, renaming, padding and recomputation shortcuts remain allowed.

## 4. Actual executions and reproducibility

A new standalone published JavaScript implementation was **directly executed in hosted V8** and its exact emitted JSON published; no project source code was imported. It independently reimplements arbitrary support hypergraphs, the potential, every abstract paid edge, both goal guards and shortest-path BFS. For $L=2,3,4,5$, one and two left-aligned input heads, and singleton, pair and seeded multiset support collections:

| Executed check | Count |
|---|---:|
| Hypergraph/head cases with independent BFS equality | 304 |
| Exhaustively enumerated abstract states | 16,864 |
| Exhaustively checked paid abstract edges | 286,496 |
| Guarded terminal abstract states | 8,428 |
| Failed checks | 0 |

The two hostile controls above were also executed, yielding $6$ versus $16$ for dispersed starts, and a failed spatial edge inequality for a free jump.

A **separately written native Python 3.13** implementation, independently developed without the published JavaScript, checked **304** analogous seeded and exhaustive cases, **16,864** abstract states, **286,496** paid edges, **10,268** goal states (different pseudorandom sample), all **304** BFS equalities, and the same two hostile countercontrols with zero failures. Its source and raw JSON were run and saved locally at `/mnt/data/tmr5_20261113_2046/`; they are **local-only**, not falsely represented as GitHub publications. No actual general SAT TM instruction trace was replayed; the peer's own JS was inspected mathematically, not natively executed. Both executions are COMPUTATIONAL evidence rather than asymptotic proof.

**Readback-verified GitHub artifacts:**
- `experiments/tmr/tmr5_spatial_ceiling008.cjs`, blob `ebdca60aa32de8cb6c0665cbdae7ae3eb9980557`.
- `results/raw/tmr/2026-11-13_2046_TMR5_SPATIAL_CEILING008_RAW.json`, blob `720fb16fc86066dded100d748c80f9592b0f08f7`.

## 5. Dependencies, source records, and final status

**Original materials audited:** TMR-4/009 full report, exact JS and raw finite output; TMR-4/008 original pair-source report; TMR-5/007 original triple-source report; TMR-1/010 all-field robustness; TMR-2/010 source-mask classifier; TMR-3/008 and /009 original crossing reports; previous LSPV/ARC checker reports were retained as historical scope controls, not substituted for this physical abstraction audit.

**Primary literature independently checked:** [1] Cousot and Cousot, *Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints*, POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973 (sound overapproximation methodology; NOT the novel spatial theorem). [2] Buhrman and de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288 (2002), pp. 21-43, https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf (decision-tree and certificate distinctions, NOT physical 3-SAT processing hardness). [3] Hennie, *One-Tape, Off-Line Turing Machine Computations*, Information and Control 8 (1965), pp. 553-578, https://doi.org/10.1016/S0019-9958(65)90399-2 (crossing-sequence antecedent; does not give the new all-head bound).

**Machine quantifiers:** the team target is $\forall$ correct fixed finite total uniform $A$, $\forall k\ge1$, $\forall C>0$, $\forall L_0$, $\exists$ a valid input $F$ of length at least $L_0$ with $T_A(F)>C(|F|+1)^k$. TMR5-SC8 proves a ceiling on ONE overly permissive abstraction for each given source, not the target, even though the lower-bound coupling itself works for any eligible $A$. No SAT/UNSAT family universally hard for every $A$ was assumed. Polynomial workspace is not restricted.

**Corpus read and governance:** replacement directive read first and rechecked at SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4`; full proof1.txt 28,714 characters SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; proof2.txt recovered by authentic Git blob (1,051,196 characters, SHA `930c5eeddafce656717f28055a7a9a755f44737c`), not from the misleading blank file body; full root main.tex recovered via authentic blob (2,504,241 characters, SHA `103435a5c6ff2b02e2b975e7c00d37476d66b064`). AGENTS.md, CODEX.md, pnp-research skill, newest five role handoffs and issue #3 through TMR-4/009 also reviewed. The repository Python preflight and LaTeX compiler were unavailable without a mounted checkout; no claim they ran. Both trackers unchanged because no P=NP or P!=NP proof arrow changed.

**Synthesis dependency:** TMR-4/009 spatial source transport **PROVED/RESTRICTED after TMR-5 review** -> TMR5-SC8 arbitrary-certificate exact MAY ceiling **CANDIDATE pending second independent role** -> any post-acquisition computational obstruction **OPEN** -> all-exponent deterministic 3-SAT lower bound **OPEN** -> P versus NP **OPEN**.

**Next target:** TMR-4 should propose a full-configuration processing-sensitive, every-transition potential whose optimistic path cannot simply scan and halt; TMR-2 must test it against the authenticated mask classifier and compact GF(2) summaries; TMR-3 must establish any same-machine time/space tradeoff for all polynomial workspace; TMR-1 must audit fixed-program quantifiers and any INDEX model translation. TMR-5 will independently replay the resulting cheapest real versus spurious paths. TMR5-SC8 requires TMR-1 or TMR-4 peer review before promotion.

END_OF_REPORT::TMR5::SPATIAL_CEILING008::2026-11-13_2046_PST
