# TMR-4/077: logarithmic vertex-cover source counterexample

**Scope:** Exact source-authenticated five-symbol BEAT-CSP. This is a restricted upper-bound construction, not an all-machine lower bound. P versus NP remains OPEN.

**New theorem.** For an encoded graph with $n$ vertices, $m$ arcs and a source-derived, verified undirected vertex cover $C$ of size $k$, enumerate $5^k$ cover colorings. For each one, the uncovered vertices are independent, so exact counting is
\[
Z(G)=\sum_{a\in\mathbb Z_5^C}[a\text{ satisfies all }C\to C\text{ arcs}]\prod_{v\notin C}|D_v(a)|.
\]
A complete, pointwise correct five-way OBDD then uses at most $n5^k$ nonterminal nodes and width at most $5^k+1$. Binary three-bit block conversion costs seven nodes per original five-way node; direct CNF emits exactly $3n+15m$ clauses. A greedy degree cover and a matching-endpoint cover are computed from the entire source, and the smaller valid cover is used. The matching fallback gives $k\le2\mathrm{OPT}$, so $\mathrm{OPT}=O(\log L)$ suffices for a polynomial-time compiler without advised layout.

**Counterexample.** For $k$ hubs, add one vertex $v_S$ for each subset $S$ of at least two hubs, with arcs $u\to v_S$ for $u\in S$. This has $n=2^k-1$, is $2$-vertex-connected, false-twin-free, and has connected nonadjacency graph; its feedback-cycle rank is $(k-2)(2^{k-1}-1)=\Theta(n\log n)$. Nevertheless $k=\log_2(n+1)$ is a certified small cover. The instance is SAT by hubs $0$, leaves $1$. Adding a six-hub tournament makes it UNSAT (six mutually adjacent source vertices cannot inject into $T_5$), increases the feedback rank by only 15, and preserves those structural features. The SAT count has the exact formula
\[
5\,2^{2^k-k-1}+5\sum_{a=1}^{k-1}\binom ka2^{2^a+2^{k-a}-k-2}.
\]
These families defeat neither the cover compiler nor simple source-aware decision methods. This is a falsifier of naive structural necessity, not evidence for P≠NP.

**Four gates.** Source: 7 canonical family cases, 110 arbitrary directed graphs, 18 malformed rejections. Pointwise: 430,750 assignment comparisons, 113 exact diagram cases, 4,100 valid CNF checks, 4,100 invalid-code rejections. Scope: quantified $n5^k$ exact diagram upper bound, $f=\Theta(n\log n)$ counterexample, unrestricted necessity OPEN. Reproducibility: two byte-identical Python runs, two byte-identical Node.js BigInt runs, all 7 family counts matched; zero assertion failures.

**SAME_REALIZATION.** Charge authentication, graph discovery, actual cover search, edge checking, 5-bit mask intersections, DAG state sharing and cache keys, exact $O(n)$-bit integers, early rejecting completion weights, 7-node Boolean conversion, CNF conversion, and output. Conservative paired bit bounds are $T=O(L^6(1+5^k))$, $S=O(L^4(1+5^k))$. No Z5/Fourier transform is invoked.

**Reproducer.** This branch includes an independently executed Node.js BigInt counter. Full executed Python diagram/compiler audit and raw JSON are retained in the /077 evidence package. Python SHA256: a2717d1c1675f701d545e1f20ebd558a7c1bc4b5f44c7d328c1fd2cd8b845d02.

**Next dependency:** D4-T5-SMALL-BACKDOOR-REMAINDER. Seek mixed sources that survive log-cover, false-twin and semijoin discovery, local domain propagation and affine/triad extraction, and then compare actual source-aware algorithms. Do not elevate a constructed OBDD lower bound to an arbitrary-machine statement.