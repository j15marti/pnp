# TMR-1/011: exact spatial MAY distance for an arbitrary one-head origin

**Date:** 2026-11-13 20:58 PST (America/Los_Angeles). **Owner:** TMR-1, Machine Model Lead. **Status:** CANDIDATE pending TMR-4/TMR-5 independent review. **Independent review:** TMR-5/008's left-aligned identity, PROVED/RESTRICTED. Finite experiments COMPUTATIONAL. P versus NP OPEN.

## Exact model and dependencies

Fix a valid encoded 3-CNF string $x\in\{0,1\}^L$, with $L$ the complete number of encoded bits, not the number of variables or clauses. Let $\mathcal D=\{D_i\}_{i=1}^m$ be a nonempty finite collection of nonempty support sets. Every $D_i$ is certified by a valid, same-length opposite-label source $y_i$ with $D_i=\{j:x_j\ne(y_i)_j\}$. These neighbors are analyst evidence, never algorithmic advice.

Consider one fixed finite total deterministic multitape 3-SAT decider $A$ across all lengths. It has finite control, fixed finite alphabets, one adjacent-moving read-only input head, arbitrary charged writable tapes, work-head coordinates, buffers, caching, representations, rereads and recomputation, and both-label correctness plus malformed handling. Each transition costs one, reads the **pre-move** input cell and moves the input head at most one position. For the generalized theorem allow any mathematical initial data-cell position $p_0\in\{0,\dots,L-1\}$; this does not grant arbitrary initialization to the ordinary machine. Random indexed input, post-move free reads or free RAM words are different models.

A concrete correct run on $x$ must read at least one coordinate from each $D_i$. Otherwise a run on $y_i$ has the same entire read transcript and, by deterministic induction, identical machine configuration sequence, including every writable cell, hence the same output on opposite-label inputs. This is valid with arbitrary memory and repeated input reading.

The TMR-4/009 sound MAY abstraction records source-head position $p$ and a ghost observed set $V$, but drops concrete work-tape contents. A paid edge reads an arbitrary subset of the pre-move coordinate and moves by at most one. Zero-cost stutters are allowed. A zero-cost SAT or UNSAT goal edge becomes possible only once $V$ hits all $D_i$. Every real transition has an abstract one-step simulation with no greater cost, and every real correct terminal has the appropriate label preserved by the coupling lemma. Thus $d_{\rm MAY}((p_0,\emptyset),goal)\le T_A(x)$, without a free SAT oracle in the physical algorithm.

## NEW theorem TMR1-AO11: exact one-head transport distance

Call an interval $[a,b]$ hitting if $[a,b]\cap D_i\ne\emptyset$ for every $i$. Then

$$
\boxed{
d_{\rm MAY}((p_0,\emptyset),goal)=
\min_{\substack{0\le a\le p_0\le b<L\\
[a,b]\cap D_i\ne\emptyset\ \forall i}}
\left[(b-a)+\min\{p_0-a,b-p_0\}+1\right].
}
$$

**Lower bound proof.** Along any successful path, the interval spanning $p_0$ and every pre-move input coordinate actually read is a hitting interval $[a,b]$. A local single-head walk starting at $p_0$ needs at least $(b-a)+\min(p_0-a,b-p_0)$ movements to reach both extremes. It also needs the final paid step to read the endpoint reached last, since reading occurs before movement. Skipping reads, unnecessary wandering and rereading do not reduce this cost. Hence every successful path costs at least the minimum displayed.

**Upper bound proof.** Choose a minimizing hitting interval. First move to the nearer endpoint, then traverse the entire interval to the other endpoint, reading along the way, and finally pay the pre-move read at that last endpoint. Every coordinate of the interval is observed, so all supports are hit and the zero-cost MAY goal edge is enabled. This is an abstract path construction, not a physical 3-SAT solver.

**Sharp noncircular cost potential.** At a general abstract state $(p,V)$, discard supports already intersecting $V$, then apply the same interval formula to the remaining supports. Define $\Psi(p,V)=0$ when none remain. This is the *exact abstract remaining goal distance*, computed solely from explicit supports, not from unknown $T_A$. Every paid abstract edge $u\to v$ satisfies $\Psi(u)\le 1+\Psi(v)$, since prefixing the step to an optimal suffix yields a path from $u$. Zero-cost stutters preserve it, and zero-cost goal edges occur only when $\Psi=0$. Thus this potential satisfies the all-edge condition and $\Psi(goal)=0$. Telescoping yields the concrete lower bound.

**Independent review of TMR-5/008.** When $p_0=0$, the hitting interval must be $[0,b]$ and its minimum rightmost endpoint is $b_*=\max_i\min D_i$. The exact formula therefore reduces to

$$
d_{\rm MAY}((0,\emptyset),goal)=1+\max_i\min D_i\le L.
$$

This independently confirms the new TMR-5/008 left-aligned hypergraph identity within the stated physical MAY model. It does not prove anything about arbitrary SAT processing time.

## NEW all-origin expressivity ceiling and hostile controls

Sweeping all source positions from the nearer endpoint gives, for *any* support family,

$$
d_{\rm MAY}((p_0,\emptyset),goal)
\le L+\min(p_0,L-1-p_0)
\le L+\lfloor(L-1)/2\rfloor <3L/2
\quad(L\ge2).
$$

This upper ceiling on a **lower-bound abstraction** is sharp with support sets $\{0\}$ and $\{L-1\}$ and a central head. For any fixed number $h\ge1$ of arbitrarily dispersed, adjacent-moving input heads, choose one head to sweep the whole source while the others idle. The same $<3L/2$ ceiling holds for the MAY domain, although the displayed *exact* one-head formula is not valid for $h>1$. Neither statement bounds actual SAT solver time.

At $L=11$ and $p_0=5$ with supports $\{0\},\{10\}$, the earlier pointwise spatial potential from TMR-4/009 is only 6, but the true one-head MAY shortest path is 16. Starting at 0 yields 11 and recovers TMR-5/008. With **two initially dispersed heads at 0 and 10**, both supports can be read in one transition; using the one-head formula there would be invalid. With a free INDEX jump from 0 to 10, the local travel floor similarly fails. A difference-certificate collection, however exponentially large, cannot make this source/head-only MAY abstraction prove $L^{1+\epsilon}$.

This conclusion is compatible with arbitrary compact algebra, Gaussian elimination on XOR/Tseitin, Horn/2-SAT, bounded-treewidth algorithms, disjoint products, sharing, padding, renaming, auxiliary variables, cached bits, rereads and recomputation. The authenticated two-label mask classifier TMR-2/010 is an explicit polynomial specialized solver for the recent high-radius source examples. No transfer to arbitrary-polynomial-exponent SAT time hardness follows, and the same-machine fact $S_A\le O(T_A)$ cannot turn an $O(L)$ abstract transport ceiling into such a lower bound.

## Quantifier and dependency audit

The unrestricted separation target remains

$$
\forall A\ \text{fixed total correct},\ \forall k\ge1,\ \forall C>0,\ \forall L_0,\
\exists x\text{ valid},\ |x|\ge L_0:\ T_A(x)>C(|x|+1)^k.
$$

This requires excluding **every** polynomial-time exponent while permitting arbitrary polynomial workspace, with the same machine and same input throughout. Hard instances may depend on $A,k,C,L_0$. Minimizing over independent size-specific hardcoded programs is not a valid alternative. This run proves only an exact restricted abstraction cost and its linear ceiling, not a separation.

Dependencies: exact encoded binary sources and opposite-label certificates (TMR-4/008, TMR-5/007 and TMR-1/010) -> first-read deterministic coupling (TMR-2) -> all-transition head-aware MAY simulation (TMR-4/009) -> independent review of TMR-5/008 left-origin identity -> **new arbitrary-origin interval theorem and sharp potential** -> **OPEN** program-aware processing-work necessity or a correct general polynomial SAT algorithm.

Requested peer targets: TMR-4 audit the sharp potential at arbitrary observed sets $V$ and the pre-move step convention; TMR-5 independently replay the new exact minimization and challenge any terminal rule claiming compulsory post-acquisition processing. TMR-3 examine same-machine $T,S$ only after a stronger processing invariant is established.

## Executed finite evidence

Independent native OS Node.js v22.16.0, fixed seed 0x1A2B3C4D, compared the exact interval formula against BFS shortest paths in **453** finite source-head/certificate configurations, covering **8,581** BFS states and **18,505** BFS edges. It checked **3,047,920** paid edges for the TMR-4 pointwise potential, **346,390** terminal guards, **111** left-origin reductions and **65,664** paid edges for the new sharp remaining-distance potential. Zero failed assertions. Largest finite input 11 source bits and largest exact MAY path 16. The three explicit negative controls above passed. These are finite COMPUTATIONAL evidence only. No physical all-length multitape transition table or actual SAT solver execution was tested.

Reproducer: experiments/tmr/tmr1_arbitrary_origin_spatial011.cjs.
Raw results: results/raw/tmr/2026-11-13_2058_TMR1_ARBITRARY_ORIGIN_SPATIAL011_RAW.json.

## Original evidence, primary literature and limits

[1] P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977, 238-252, https://doi.org/10.1145/512950.512973. Only the general may-simulation framework, not the new geometry, is attributed to this paper.

[2] H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, TCS 288 (2002), 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X. Query and certificate complexity do not entail physical post-acquisition processing cost.

[3] L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (2005), https://doi.org/10.1145/1101821.1101822. Its published simultaneous small-space hypotheses do not exclude all polynomial time with arbitrary polynomial space.

**Reads:** Directive first and rechecked, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; full proof1.txt 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; authentic full proof2.txt Git blob 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c; complete main.tex Git blob 2,504,241 characters SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064. AGENTS.md, CODEX.md, pnp skill, latest issue #3, all five current TMR handoffs, original TMR-4/009, TMR-5/008, TMR-2/010 and TMR-1/010, plus original historical LSPV-5/511 real-checker counterexample were consulted. Actual repository checkout/preflight, LaTeX compilation and physical TM instruction-level simulation were not performed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Do not edit canonical main.tex outside TMR-5's synthesis authority. Historical failed checker paths retained; old role priorities superseded. No tasks or schedules created, revived or modified.

**Next target:** a noncircular *processing-state* potential remaining positive after all input bits have been read, sound against arbitrary compact algebra, real cached computation and a fully correct fixed deterministic machine. The unrestricted all-exponent arrow stays OPEN.