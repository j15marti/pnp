# TMR-4/009: head-aware cost-sound source certificates

**Date:** 2026-11-13 20:36 PST (America/Los_Angeles). **Owner:** TMR-4 Cost-Sound Abstraction, j15marti/pnp main. **Status:** CANDIDATE, pending TMR-5 independent audit. Finite results COMPUTATIONAL. The unrestricted 3-SAT lower bound and P versus NP remain OPEN.

## New result

TMR-4/001 and /007 use MAY graphs retaining only source positions observed. Their abstract cost for TMR-4/008's $r$ disjoint two-bit UNSAT neighbors is $r$ under one-bit observations. The graph allows arbitrarily distant source reads for one cost each, even when the physical source head moves one cell per transition. This run adds the actual input-head locations, leaving arbitrary writable representations unconstrained.

For **both** the original TMR-4/008 pair-certificate source and TMR-5/007 triple-certificate source, the resulting program-independent abstract shortest path equals

$$
\boxed{\Phi(s_0)=1+N+M+2+3(8r-1)(w+1)=\Omega(L).}
$$

Here $w=\lceil\log_2(6r+2)\rceil$, $N=2^w-1$, $K=\lceil(N-3r)/3\rceil$, $M=8r+K$ and $L=N+M+2+3M(w+1)$. Exactly,

$$
L-\Phi(s_0)=3(K+1)(w+1)-1,\qquad
\liminf_{r\to\infty}\frac{\Phi(s_0)}L\ge\frac8{11}.
$$

This is an exact **linear input-transport** necessity in the canonical binary clause order. It is NOT superpolynomial global SAT processing.

## Model and exact every-transition abstraction

Fix ONE finite total correct uniform deterministic multitape 3-SAT machine $A$ over all input lengths, with finite control and alphabets, arbitrary complete writable tapes, tape heads, registers implemented on tapes, buffers, indices, alternative representations, repeated computation, caching and source rereads. Every physical transition costs one. Input is read only, with a fixed finite number $h\ge1$ of heads, each starting at the leftmost data bit, moving at most one cell per transition and reading at its **pre-move** location. All work and malformed-input behavior remains part of the full concrete machine. An indexed-input or read-destination-on-move model requires its own charged translation and is not silently covered.

For a fixed valid encoded source $x$ with actual SAT/UNSAT label $f(x)$, choose a finite, independently certified set of same-length valid sources $y_i$ with opposite label. Set $D_i=\{p:x_p\ne(y_i)_p\}$, all nonempty. These neighbors are externally supplied analyst certificates and never machine advice or a free oracle. Augment concrete traces with ghost set $V$ of observed original source-bit positions; it is not solver-accessible workspace.

The MAY nonterminal state is $(H,V)$, where $H$ retains all clipped source-head coordinates in $\{0,\dots,L\}$ and $V\subseteq\{0,\dots,L-1\}$. Clipping a real position beyond an endmarker to the boundary is 1-Lipschitz and preserves every physically possible transition by overapproximation. Abstract initial state: $s_0=((0,\dots,0),\varnothing)$.

Every cost-one MAY edge $(H,V)\to(H',V\cup R)$ permits all $|H'_j-H_j|\le1$, with $R$ an arbitrary subset of original source positions physically underneath the heads at their pre-move locations. Include zero-cost self-loops. A zero-cost edge to EACH of two distinct labeled goals is available only if $V\cap D_i\ne\varnothing$ for all $i$. These are MAY edges, not a claim that either label is freely decidable by the solver.

**Initial-state coverage:** the concrete initial machine configuration with empty trace ghosts relates to $s_0$. **Every-step coverage:** for every related concrete/abstract pair, every real transition changes the input heads by at most one and reads only at their pre-move positions, so one abstract edge of cost 1 maps to its related successor. It may change every concrete work representation, make cached copies or only recompute; no operation is excluded. **Terminal-label coverage:** if any actual correct halt failed to hit some $D_i$, deterministic source coupling on $x$ and $y_i$ would reproduce the entire identical concrete computation, including all head movements and all writable states, but output the same label on opposite-label inputs. Contradiction. Thus all real SAT and UNSAT terminals can map to the appropriate labeled goal after an affordable zero-cost edge. The same theorem applies when $x$ is UNSAT and the certified neighbors are SAT. No solver-template or fixed proof calculus is used.

Define

$$
d(H,D)=\min_{j,p\in D}|H_j-p|,
$$

$$
\Phi(H,V)=
\begin{cases}
0,&V\text{ intersects all }D_i,\\
\max_{i:V\cap D_i=\varnothing}(1+d(H,D_i)),&\text{otherwise},
\end{cases}
\qquad \Phi(g_{\rm SAT})=\Phi(g_{\rm UNSAT})=0.
$$

**Every-edge potential proof:** On a paid edge, each certificate $D_i$ not yet hit either (a) is newly hit by a head at one of its pre-move locations, so its former contribution was exactly 1, or (b) remains unhit, in which case unit head movement gives $d(H,D_i)\le1+d(H',D_i)$. Therefore the maximum obeys $\Phi(H,V)\le1+\Phi(H',V\cup R)$. Zero-cost self-loops preserve potential. Goal edges originate only when potential is zero. So $\Phi(a)\le c(a,b)+\Phi(b)$ on EVERY edge, including zero-cost ones. Telescoping and all-step simulation yield

$$
\Phi(s_0)\le d_{\rm MAY}(s_0,\{\mathrm{SAT},\mathrm{UNSAT}\})\le T_A(x).
$$

**Exactness:** With all input heads initially at position 0, let $p_*=\max_i\min D_i$. Every abstract successful path must reach at least this coordinate and pay one transition to read it in the pre-move convention, so cost is at least $p_*+1$. A single head scanning positions 0 through $p_*$ and revealing every bit attains this length. Therefore

$$
d_{\rm MAY}(s_0,\mathrm{goal})=\Phi(s_0)=p_*+1.
$$

This potential is computed solely from fixed source coordinates, without knowing $T_A(x)$ or simulating $A$.

## Instantiation and restricted-model gap

The actual previously audited proper 3-CNF encoding is a unary header $1^N0\,1^M0$ followed by three fixed-width signed literal fields per clause. All $N$ declared IDs occur. The original even-parity encoded three-variable core blocks have either the eight masks $(1,2,3,4,5,6,7,3)$ or $(1,2,3,4,5,6,7,7)$; positive dummy fillers cover all remaining declared IDs. Changing two designated sign bits in the last mask-3 clause, or three in the last mask-7 clause, turns one block into the complete forbidden-mask set $0,1,\dots,7$ and gives a valid same-length UNSAT input. Original sources are SAT. The $r$ disjoint difference supports have earliest positions

$$
p_g=N+M+2+3(8g+7)(w+1),\qquad g=0,\dots,r-1.
$$

So $p_* =p_{r-1}$ as claimed. At $r=16$, $L=4004$ and new spatial lower bound is **3333**, compared with the location-blind potential **16**. At $r=256$, $L=93624$, the figures are **78217** versus **256**.

The new result holds with arbitrary polynomial, superpolynomial or unbounded writable workspace on the SAME run, and with any fixed number of left-aligned locally moving source heads. It does NOT cover free random access, initially dispersed input heads, changed physical binary encodings or uncharged jumping. Other clause orders can change the coefficient. Since the complete authenticated two-label mask class is decidable by the polynomial source recognizer and fully charged general fallback from TMR-2/010, this cannot imply expensive post-acquisition computation or exclude any polynomial exponent.

## Actual verification

Exact published executable: https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr4_spatial_certificate009.cjs

Exact published raw file: https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-13_2036_TMR4_SPATIAL_CERTIFICATE009_RAW.json

The native-compatible original Node.js variant was executed locally before publication. The **published source**, fetched back from GitHub blob SHA 19c173be050af83a29dc66c402ce2b61a386ecf9, was then independently executed in hosted V8 and its actual JSON output published. The initial local runner is a separately assembled variant, not claimed to have byte-identical source.

**Actual finite checks:** $r=1,2,3,4,5,6,8,10,12,16,32,64,128,256$ on both certificate families, 28 constructed sources, 361370 encoded bit positions across both, 1094 certificate supports, exact positions, clause properness, all-ID-used grammar and full forbidden-mask contradiction. The finite MAY audit enumerated **8992 abstract states, 193760 paid edges**, zero-cost self-loops, both goal guards and eight independent shortest-path BFS cases for one and two input heads. All eight BFS distances equaled the closed-form potential, and **zero assertions failed**.

Finite checks are COMPUTATIONAL, not a physical universal machine execution or an asymptotic lower-bound proof. No complete 3-SAT fallback was run. No preflight script or LaTeX compilation was run without a mounted checkout.

## Historical evidence, sources, statuses

TMR-4/001 and /007 originally prove/check the source-coordinate MAY graph, TMR-4/008 provides the two-position UNSAT neighbors, TMR-5/007 provides three-position neighbors, and TMR-2/010 gives the easy two-label fast path. This new head-position invariant is a physical transport refinement, not a new definition of SAT semantic information. TMR-4/003 also supplies a paid two-completion counterexample to any required expensive phase after the last source bit; no post-read work is charged here.

The original LSPV-5/479 negative-zero parsed-ID alias and LSPV-5/511 accepted string-support path remain genuine historical native-checker failures. LSPV-5/514 normalizes edge suffixes only under its exact pinned runtime. None is erased or treated as spurious or transferred to an arbitrary decider.

**Primary verified literature:** [1] P. Cousot and R. Cousot, Abstract Interpretation: A Unified Lattice Model, POPL (1977), 238-252, https://doi.org/10.1145/512950.512973 , original author bibliography https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml . Used only for general abstraction soundness, not the novel spatial formula. [2] H. Buhrman and R. de Wolf, Complexity Measures and Decision Tree Complexity, TCS 288 (2002), 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X . Restricted input-query distinctions are not physical SAT-processing lower bounds.

**Preflight:** replacement directive read FIRST and rechecked at SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1.txt read fully (28714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343); proof2.txt recovered fully from authentic blob (1051196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c); root main.tex recovered fully from authentic blob (2504241 characters, SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064). Also read latest issue #3, root AGENTS.md, CODEX.md, pnp-research skill, all newest TMR handoffs, original source reports, and relevant checker counterexamples. Ordinary contents returns for proof2/main.tex were misleadingly blank.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left unchanged for TMR-5 whole-document synthesis; no task or schedule modifications.

**ONE NEXT TARGET:** an EVERY-step source-independent computational potential that remains positive despite interleaved input processing, input copies, caching, Gaussian elimination, the mask-table classifier and deferred-last-bit precomputation. It must have a proved initial value excluding every polynomial time exponent; this arrow remains OPEN.

END_OF_REPORT::TMR4::SPATIAL_CERTIFICATE009::2026-11-13_2036_PST
