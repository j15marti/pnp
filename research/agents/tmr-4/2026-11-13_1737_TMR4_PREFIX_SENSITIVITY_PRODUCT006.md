# TMR-4/006: cost-sound exact-prefix and residual-sensitivity product

**Run:** November 13, 2026, 17:37 PST. **Role:** new TMR-4 Cost-Sound Abstraction. **Scientific status:** CANDIDATE pending TMR-5 independent mathematical review; finite verification COMPUTATIONAL. Unrestricted superpolynomial deterministic 3-SAT time lower bound OPEN; P versus NP OPEN.

## Theorem TMR4-PS6 and exact machine model

Fix one finite, uniform, total, correct deterministic multitape 3-SAT decider $A$ over ALL binary lengths, one actual encoded source $x$ of $L=|x|$ bits, and one fixed physical source interface which observes at most $q\ge1$ input positions per concrete transition (the fixed number of input heads/ports; source reaccess and random-address construction must be physically charged). Every physical step costs 1. A concrete configuration includes the fixed program and control, source contents and endmarkers, all read-only input heads, complete writable tapes/heads, temporary representations, indices, buffers, encodings, caches and recomputation.

Let $P$ be a certified set of input positions such that for EACH $p\in P$, flipping ONLY bit $p$ produces a valid same-length 3-CNF of the OPPOSITE SAT/UNSAT answer. Correctness on all these neighbors and deterministic unread-bit coupling force the actual run of $A$ on $x$ to observe every $p\in P$. Let $V_t\subseteq P$ be the set of certified positions actually observed in its first $t$ transitions. In particular, $V_{T_A(x)}=P$ and $|V_{t+1}\setminus V_t|\le q$. The sets $V_t$ are external proof-history tags, not free memory accessible to $A$.

For integer $B\ge0$, construct the exact actual concrete prefix of length $h=\min(B,T_A(x))$, recording complete configurations and observation histories. There exists a finite weighted MAY abstraction preserving initial state, EVERY actual concrete transition and the correct terminal label, with an explicit potential satisfying every edge inequality and

$$
\boxed{
\Phi(s)=
\begin{cases}
T_A(x), & T_A(x)\le B,\\
B+\left\lceil |P\setminus V_B|/q\right\rceil, & T_A(x)>B.
\end{cases}
\quad\le T_A(x).
}
$$

In both cases the initial potential equals the abstract minimum path cost to either labeled decision goal. Thus a bounded exact prefix can be combined with source-sensitivity cost **without charging already-observed bits twice**. It is sometimes strictly stronger than either $B$ or $\lceil|P|/q\rceil$ alone, but proves NO superpolynomial initial bound and requires spending up to $B$ concrete simulation steps.

## Exact abstract graph, simulation and potential proof

If the machine halts within $B$ steps, retain cost-one vertices for the complete actual prefix, connect the true terminal label, and leave the opposite terminal label disconnected. Its potential is $T_A(x)-i$ at traced prefix index $i$, zero at goals. No SAT oracle is involved.

Otherwise use a chain of $B$ unit-cost observed-prefix edges ending at suffix vertex $\star_{V_B}$ (for $B=0$ start at $\star_{\varnothing}$). For EVERY $V$ with $V_B\subseteq V\subseteq P$, include a vertex $\star_V$, a cost-zero self-loop, and for EVERY nonempty $D\subseteq P\setminus V$ with $|D|\le q$, include a cost-one edge $\star_V\to\star_{V\cup D}$. At $\star_P$ alone, include cost-zero edges to BOTH SAT and UNSAT labeled goals. Their MAY overapproximation is deliberate; it does not assert either physical answer. Put

$$
\Phi(\star_V)=\left\lceil |P\setminus V|/q\right\rceil,\qquad
\Phi(g_{\rm SAT})=\Phi(g_{\rm UNSAT})=0,
$$

and for traced prefix states $p_i$ put $\Phi(p_i)=B-i+\Phi(\star_{V_B})$.

Relate the entire exact concrete configuration at each traced step $i<B$ to $p_i$, and each later instrumented actual configuration $(c_t,t,V_t)$ to $\star_{V_t}$. Each traced concrete step maps to its unit-cost prefix edge. After horizon, a concrete step observing no NEW certified bit maps to a zero-cost self-loop; one newly observing $D$ maps to its unit-cost edge. If the successor physically halts, append the zero-cost edge from $\star_P$ to its ACTUAL correct labeled goal. The guard $V_T=P$ was proved by coupling with opposite-label neighbors, not by an assumed solver template. Thus EVERY actual concrete transition, including source rereads, compact computation, repeated configurations, temporary encodings, all writable-work operations and recomputation, maps to a finite abstract path of total cost at most the concrete increment 1. Every genuine complete execution and both terminal types are preserved.

For ALL abstract edges, $\Phi(u)\le c(u,v)+\Phi(v)$: prefix edges are tight; zero-cost loops preserve potential; a cost-one edge adds at most $q$ newly observed bits, so its ceiling potential decreases by at most 1; terminal edges begin at zero potential. Goals have potential zero. Telescoping every real trace proves $\Phi(s)\le T_A(x)$. Conversely, every abstract goal path must traverse all $B$ unit prefix edges, then acquire every remaining element of $P$ at most $q$ per cost-one edge. A permitted partition into groups of size at most $q$ attains exactly $B+\lceil|P\setminus V_B|/q\rceil$. Hence this is ALSO the exact abstract shortest decision-path cost. The suffix graph has up to $2^{|P|}$ nodes and can be represented symbolically; no efficient general analyzer is claimed.

## A concrete failure and its repair

The naive **FALSE** candidate $B+\lceil|P|/q\rceil$ double-charges sensitive input reads already made in the exact prefix. On a four-bit toy parity language, all four bits are sensitive, one scanner observes one bit per transition, and the fifth transition outputs its label: $T=5$. Choosing $B=3$ makes the false bound $3+4=7>T$. The repaired cost is $3+\lceil(4-3)/1\rceil=4\le5$. Conversely, a toy machine with three paid idle preprocessing transitions before it reads its four sensitive bits gives at horizon $B=3$ an actual sound potential 7, compared with the weaker $\max(3,4)=4$. Genuine speculative computation and recomputation remain charged in the actual prefix but may be conservatively forgotten after it.

An invented zero-cost edge from $\star_V$ to $\star_P$ when $V\ne P$ is **unsound** as a physical first-read simulation: it violates the potential edge inequality. Valid zero-cost stutters cannot change the observed-bit set. Short MAY post-horizon paths do not justify removing a genuine cheaper execution. Refine only after replay proves spurious behavior, as in standard CEGAR discipline.

## Precise 3-SAT control and transfer gap

For a clause-minimally UNSAT properly encoded 3-CNF, a satisfying assignment of every one-clause-deletion formula falsifies the deleted clause. Flipping ANY literal polarity in that clause produces a valid same-length SAT neighbor. Therefore ALL separately encoded literal-polarity bits are certified sensitive, without demanding that the decider output a proof. The recent TMR-2/005-006 chained-XOR clique Tseitin construction proposes a clause-minimally UNSAT family with $M=4m(m-3)$ original clauses and $P=12m(m-3)$ individually sensitive signs at encoded $L=\Theta(m^2\log m)$. **The explicit family instantiation depends on peer verification of TMR-2/005's claimed minimality**, currently CANDIDATE; the generic product theorem does not depend on that family. For any already validated such family and a fixed $q$-port machine, the conditional time bound is $T_A(F)\ge B+\lceil(12m(m-3)-|V_B|)/q\rceil$ whenever the actual trace has not halted by $B$.

The analysis is source-bound and program-dependent, not a free SAT oracle. Arbitrary all-length correct SAT programs, both labels, all polynomial workspaces, Horn, 2-SAT, affine/Tseitin Gaussian elimination, bounded-treewidth DP, products, sharing, renaming, padding, auxiliary encodings and repeated source reads remain eligible. A genuine polynomial-time solver on these inputs is permitted. A cost necessary **after acquisition** remains OPEN. The universal target remains: for every correct fixed $A$, integer $k\ge1$, $C>0$, $L_0$, some valid $F$ of length at least $L_0$ must have $T_A(F)>C(|F|+1)^k$. PS6 does not prove it.

## Executed finite verification (COMPUTATIONAL)

The independently authored hosted-V8 executable constructs four different deterministic TOY parity-language transition-event programs (FAST single scan, IDLE preprocessing/finish, RECOMPUTE read/rewind/read, PAIR two source observations per step). For every binary source of lengths 0 through 7 it checks SAT/UNSAT *toy terminal labels*, source accesses, initial/terminal and all-step path preservation for several horizons, exact shortest MAY cost using an independent BFS, and EVERY enumerated suffix-edge potential inequality, including zero-cost loops. It tests both logical labels and hostile invalid zero-cost reveals.

**Actually executed:** 1,020 source/program runs, 7,573 horizon cases, 745,894 paid abstract edges, 960,346 potential-edge checks, 84,128 concrete-step-path checks, 203,392 zero-cost stutters, 1,014 cases of strict improvement over the separate bound maximum, 1,972 detected double-counting falsifiers, 4,238 invalid free-revelation attempts, zero assertion failures. Maximum input 7 bits, maximum toy trace 22 steps. **These are toy source-event simulations, NOT native Node physical TM simulations or actual 3-SAT Turing-machine executions.** The asymptotic theorem is argued symbolically and awaits independent peer review. No native Node, full preflight or LaTeX compilation was run.

Executable and raw, created on main and verified byte-for-byte by GitHub readback:
- experiments/tmr/tmr4_sensitive_prefix_product006.cjs (Git blob 0def776623f4f3c99e0c924fd15df56d02e8f6ac).
- results/raw/tmr/2026-11-13_1737_TMR4_SENSITIVE_PREFIX_PRODUCT006_RAW.json (Git blob 4fed3f363bd87dfc5686d6ebfd143acfd5dabd0a).

## Primary literature, provenance and status

[1] P. Cousot and R. Cousot, *Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints*, POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973 . Original work abstract and bibliography inspected; it supplies methodological context, not a SAT lower bound.

[2] E. Clarke, O. Grumberg, S. Jha, Y. Lu and H. Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15 . Original authors' hosted abstract at https://kilthub.cmu.edu/articles/journal_contribution/Counterexample-guided_Abstraction_Refinement/6604547 inspected. True cheap physical paths must not be deleted.

[3] H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288 (2002), 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X . Original author abstract and journal metadata inspected; query complexity is NOT an unrestricted SAT computation lower bound.

Prior original mathematical evidence directly read: TMR-4/004 common-start ceiling, TMR-4/005 exact-trace horizon and its executable, TMR-2/005 minimally UNSAT report, TMR-2/006 sign-bit argument and executable. Historical accepted-checker counterexamples directly read: LSPV-5/510 infinity/null parse-reserialization failure and LSPV-5/511 string-valued support accepted-byte failure, plus original LSPV-5/510 reproducer; no historical accepted path is erased or reclassified.

Read FIRST the new 12:49 PST directive, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, and rechecked before shared writes. Read complete proof1.txt (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343). The contents API returned blank proof2.txt and main.tex with their SHAs, but their ORIGINAL Git blobs were recovered in full: proof2.txt 1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex 2,494,937 characters, SHA 873daeec6e11d4a7448f3b0547c9ed1ccfebd805. Inspected AGENTS.md, CODEX.md, pnp-research skill, all five newest TMR handoffs, and issue #3 through its latest TMR-3/006 comment (1,958 comments).

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither proof tracker nor the canonical main.tex was edited; TMR-5 owns manuscript synthesis pending peer audit. No schedules, agents or tasks were altered.

**Next target:** TMR-5 independently replay the abstract mask graph and the four-bit double-count falsifier. TMR-2 supply new explicit opposite-label neighbors, TMR-3 audit input-port cost translation, and TMR-1 audit uniform model. Seek a genuinely unavoidable whole-execution processing potential beyond this linear source-observation cost. Every unrestricted load-bearing arrow stays OPEN.

END_OF_REPORT::TMR4::PREFIX-SENSITIVITY-PRODUCT006::2026-11-13_1737_PST
