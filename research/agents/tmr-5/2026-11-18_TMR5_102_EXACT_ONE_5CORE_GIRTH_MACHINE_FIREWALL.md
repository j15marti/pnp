# TMR-5/102: exact-one T5 private-head machine and girth firewall

**Scope.** TMR-5 independent red team, 2026-11-18 Pacific Time. The fixed tournament has \(R(a,b)\iff (b-a)\bmod5\in\{1,3\}\), no loops, and \(Q(h,u,v)=R(h,u)\oplus R(h,v)\). In the **private-head** subfamily \(F(H)=\bigwedge_{\{u,v\}\in E(H)}Q(h_{uv},u,v)\), each head is fresh, appears in no follower position, and has its own clause. We take the source vertex set to consist exactly of the **active followers**, with no isolated vertices added to the formula count. This is not the general shared-head problem.

## New proved statements

**Exact projection and paid witness extension.** \(F(H)\) is SAT exactly when source graph \(H\) is 5-colorable. Given a proper coloring, choose each private head's value equal to the endpoint color that beats the other. Computing and checking all \(n+m\) output letters costs \(O(n+m)\) time, but the source coloring must first be found, supplied and charged. A read-only, random-access supplied coloring permits \(O(\log(n+m))\) *additional* bit workspace for streamed output; this is NOT a deterministic low-space coloring algorithm. Source graph extraction with ordinary adjacency lists costs linear workspace.

**Critical degree/density.** If \(F(H)\) is clause-minimal UNSAT, the active-follower graph \(H\) is connected, edge-critical 6-chromatic, and has minimum degree at least 5. Deleting a clause is exactly deleting one follower graph edge. All \(H-e\) are 5-colorable, while \(H\) is not; one fresh sixth color restores \(H\), so \(\chi(H)=6\). A degree-at-most-four vertex could be greedily recolored after deleting that vertex, a contradiction. Therefore \(m\ge5n/2\); with \(N=n+m\) variables, \(n\le2N/7\) and at least \(5N/7\) variables are private heads.

**Moore girth barrier.** For a simple minimum-degree-five graph of girth \(g\),
\[
n\ge\begin{cases}
1+\frac53(4^r-1),&g=2r+1;\\
\frac23(4^r-1),&g=2r .
\end{cases}
\]
For \(F(H)\), the incidence girth is *exactly* \(2g\), since clause nodes subdivide follower edges and private heads are leaves. Thus any clause-critical private-head family has \(g_{\rm incidence}\le2\log_2N+O(1)\). **Superlogarithmic girth is impossible in this critical subfamily.** The bound does not extend to general shared-head Q without a new proof.

## Sound, uniform, incomplete specialist

Parse and verify private heads. Compute the 5-core by deleting graph vertices of current degree at most four. If empty, reconstruct a 5-coloring backwards, lift the heads and verify every Q clause; output SAT+witness. Otherwise, if the source graph is bipartite, return SAT+verified two-color witness. Otherwise search for a \(K_6\), verify its 15 distinct source edges, and return UNSAT+certificate if found. All other cases return **UNKNOWN**. This is sound and needs no advice. The first two stages are linear time using linear adjacency workspace, but naive \(K_6\) search can cost \(O(n^6)\); NO \(n^{1.33}\) theorem is claimed.

## Exact independent controls

- \(K_6\): \(n=6,m=15,N=21\); 5-core size 6; UNSAT with a checked \(K_6\) certificate. Every one of 15 edge deletions empties the 5-core and yields a completely verified SAT witness.
- Triple-Mycielski \(C_5\): imported fixture \(n=47,m=236,N=283\); full graph 5-core size 47. Across all 236 edge deletions, **211** have 5-core 47 and **25** have 5-core 46. **Zero** are solved by the degree-at-most-four peeling method. The fixture's independent structural UNSAT proof and all its SAT deletion witnesses were supplied in the evidence archive. Our incomplete generic specialist returns UNKNOWN on the intact graph, correctly not an unverified UNSAT.
- \(K_{5,6}\): \(n=11,m=30,N=41\), nonempty 5-core 11, yet SAT by bipartite coloring. This falsifies the inference "nonempty 5-core means UNSAT."
- Four independently seeded 130-follower, 4-degenerate planted graphs with respectively \(329,330,302,314\) edges had empty 5-cores and fully verified SAT assignments.
- An irrelevant 4-degenerate padding component attached disjointly to \(K_6\) gave \(n=136,m=331\), with six-node residual core and a short K6 refutation.

The full stdlib audit counts head checks, Q witness verification, adjacency scans, degree operations, queue use, candidate clique tests, witness symbols and elapsed time. Peak Python allocations and RSS were recorded separately and are NOT theoretical RAM bounds. Local Q=60/125, old P=20/125, overlap 0, independently rechecked. No prior 2,320-run grid or exhaustive 4-variable classification was repeated.

## Literature transfer and exact limitation

Emden-Weinert, Hougardy and Kreuter (1998), *Uniquely Colourable Graphs and the Hardness of Colouring Graphs of Large Girth*, [DOI](https://doi.org/10.1017/S0963548398003678), state that fixed-k coloring on source graphs of girth at least \(\log n/(13\log k)\) and maximum degree \(\le6k^{13}\) admits no polynomial algorithm unless NP=RP. With k=5 and constant maximum degree, the private-head transformation has \(N=n+m=\Theta(n)\), twice source girth in the incidence graph and a source-preserving polynomial reduction. Therefore restricted Q on such high-incidence-girth instances inherits the cited **conditional** polynomial barrier. It does NOT prove deterministic NP-hardness of the **critical promise**, a numerical \(n^{1.33}\) bound, or hardness of individual graphs. The finite core findings are compatible with this theorem.

## Shared-z, path advice, and proof chain

The proposed scan of \(n^{.195}\) rows and \(n^{.65}\) size-\(n^{.35}\) blocks costs \(n^{.845+.35t}\) per fixed z with a child decision time exponent t; standard per-variable black-box decision-to-witness reconstruction yields \(n^{1.195+.35t}\) (at t=1: 1.545) for that implementation, before universal z coverage. These are *upper bounds of described implementations*, not unrestricted lower bounds. Any complete k-bit correct-path model with sound decisive outputs may be deterministically enumerated at \(2^kT\) time plus replay workspace; a free unverified polarity oracle does not qualify. SAT positive certificates verify quickly; UNSAT claims require a sound negative mechanism. Buss and Williams (2015), [DOI](https://doi.org/10.1007/s00037-015-0104-9), concern precise SAT random-access models; their numeric exponent cannot simply be transported through an unspecified polynomial reduction to Q.

**PROVED:** Projection, charged witness extension conditional on a source coloring, critical degree/density, Moore barrier, sound partial algorithm, finite certificates and core counts.
**FALSIFIED:** Nonempty 5-core implies UNSAT; all SAT critical deletions are 4-degenerate; superlogarithmic incidence girth of fresh-head critical formulas.
**CONDITIONAL:** High-logarithmic-girth noncritical class polynomial hardness unless NP=RP.
**OPEN:** All-input Q decision, critical-deletion witness hardness, deterministic one-sided arbitrary CNF contraction, \(n^{1.33+o(1)}\)/square-root-space, unrestricted superpolynomial lower bounds.

The independent full script, compact separately rerun verifier, exact raw JSON, mathematical report and LaTeX appendix are preserved in the run's reproducibility archive. No other agent or automation settings were modified. P versus NP remains OPEN.
