# TMR-4/096: bounded-error source-bit barrier and representation firewall

**Classification:** PROVED in the explicitly named adaptive **bit-probe** model, with COMPUTATIONAL finite audit. This result is **not** a superpolynomial machine-time lower bound. Primary object: the original T5-CSP, $R(a,b)\iff(b-a)\bmod5\in\{1,3\}$. No change to TMR-4 identity, ownership or hourly schedule.

## Precise candidate and proof

On an explicit ordered-arc matrix, let $E_n$ be the empty graph with $M=n(n-1)$ adjacency bits. For each unordered pair $p=\{i,j\}$, let $B_p$ be the graph with both directed arcs $i\to j$ and $j\to i$, all others absent. There is no satisfying assignment to $B_p$, since $T_5$ has no reciprocal edge. Exactly $Z(E_n)=5^n$ assignments satisfy the empty graph.

**Theorem.** Any arbitrary adaptive, even nonuniform and randomized algorithm that correctly decides **all** $n$-vertex T5 input matrices with pointwise error at most $\varepsilon<1/2$ must make at least
$$
\boxed{\mathbb E Q_A(E_n)\ge(1-2\varepsilon)\binom n2}
$$
source-bit probes on the empty graph. All computation between individual probes may be free; reading each bit is explicitly charged.

**Proof.** Couple runs on $E_n$ and $B_p$ using the same random tape $r$. They have identical transcripts and answers until one of the two bits of pair $p$ is probed in the empty-input run. Let $S_r$ be the unordered pairs touched by this run, and let $a_G(r)$ be its acceptance bit. Pointwise, $a_{E_n}(r)-a_{B_p}(r)\le[p\in S_r]$. Error at most $\varepsilon$ implies $\Pr[p\in S_r]\ge1-2\varepsilon$. Sum this inequality over $\binom n2$ pairs and use $Q_A(E_n)\ge|S_r|$. No fixed variable order is assumed. At $\varepsilon=1/3$, $\mathbb E Q_A(E_n)\ge n(n-1)/6$.

**One-sided stronger corollary from /094.** If accepting UNSAT inputs has probability exactly zero, and accepting SAT inputs has probability at least $1-\varepsilon$, then
$$
\mathbb E Q_A(E_n)\ge(1-\varepsilon)\left(n(n-1)-\left\lfloor\frac{2n^2}{5}\right\rfloor\right).
$$
For almost every random tape accepting the empty source, its probed-zero positions must form a sound deterministic empty-input SAT certificate, or an UNSAT unseen completion would follow the same accepting transcript. The exact certificate size is the proven /094 result. This invokes /094; it is not an independent proof of the extremal certificate formula.

**Hard upper barrier:** Full matrix reading uses $M$ probes before any deterministic exponential enumeration, so these are $\Theta(M)$ input-access bounds, never superpolynomial in input length $L=\Theta(M)$ for the chosen encoding. The randomized algorithm that accepts blindly with probability $1/3$ and otherwise fully reads and correctly decides the graph has all-input error at most $1/3$ and expected zero-input reads $2M/3$; its computation need not be polynomial.

## Four falsifiers

1. **Encoding switch:** sparse edge lists reveal the empty graph versus any two-cycle from their edge record count. A source-aware algorithm can detect these cases in linear input time and use a generic fallback. The $\Omega(n^2)$ result is not encoding-independent. Whole-source authentication hashes must read the source.
2. **Exact-assignment representation mismatch:** $E_n$ has a constant-TRUE complete assignment predicate, and every $B_p$ has constant-FALSE. Both have complete-query five-way OBDDs with exactly $n$ nonterminal nodes and width one. Rejected and accepted path multiplicities are $5^n$ when parallel five-way edges are counted with multiplicity.
3. **Randomization/adaptivity and cache:** coupling handles adaptive probes and arbitrary computation, but a free packed whole-word read, advice indexed by the source itself, or a magic source hash is outside the model. Repeated probes, cache lookup/eviction and parsing are not free in a physical realization.
4. **Source query vs computational work:** reading all $M$ bits gives an $M$-probe upper bound. No adaptive FBDD, complete-assignment OBDD or tensor lower bound is thereby transferred to the runtime of a uniform source decider.

## SAME_REALIZATION ledger and comparisons

Audit starts with canonical and SHA-256 authenticated original directed graph sources, not provided truth labels. Charge source bytes and hash reads; parser, vertex and arc discovery; source address arithmetic; exact five-way transitions; 32-mask domain propagation; fan-out/sharing; cache reads/copies/eviction; rejected paths; integer precision; source output and SAT witness checks; and every Boolean/CNF conversion. No Fourier transform or tensor contraction is executed, hence neither is credited as free. Invalid 3-bit codes 5,6,7 are disallowed by three clauses per vertex. Each original $R$ arc forbids 15 ordered color pairs, giving **$3n+15m$ CNF clauses and $9n+90m$ signed literals**. A grouped Boolean decoder costs at most six nodes per native node; interleaved Boolean FBDD reverse transfer remains OPEN. All 32 unary masks and two directions remain valid.

## Four executed finite gates

* **G1 / authenticated source:** 40 canonical original matrices ($n=2,\ldots,6$), matching Python and independent JavaScript SHA-256 hashes; six malformed controls rejected. Total 1,492 canonical source bytes and 812 matrix positions read in physical full-source audit.
* **G2 / native exact decisions:** 289,300 pointwise original-assignment checks in each language, 5 empty SAT matrices with $Z=5^n$ and 35 two-cycle UNSAT matrices with $Z=0$. Exact complete-query width-one diagrams total 195 internal nodes and preserve all accept/reject multiplicities.
* **G3 / Boolean and domain:** 289,300 actual signed-literal CNF evaluations per language, 25,923 invalid-code evaluations per language and 2,048 oriented 32-domain-mask cases per language; 1,635 generated clauses and 8,055 literal occurrences.
* **G4 / adversarial schedule and replication:** at $n=10$, 45 cyclic random seeds and 45 planted pairs; probing 30 pairs per seed detects every planting on exactly 30 seeds and misses on 15. Both independent programs agree on all source hashes, counts, masks and schedules. Repeated executions byte-identical; zero unexpected assertion failures. The schedule is only a promise test, **not** a globally correct T5 decider.

**Foundational checks:** DISJ as cheap-source control only; relativizing transcript coupling, no nonrelativizing conclusion; DTISP only a charged upper ledger, no forbidden region; configuration counting not invoked as a time LB. Independent formal review and physical Turing-machine microstep verification OPEN.

**Next:** D4-T5-SOURCE-ACCESS-TO-UNIFORM-RESOURCE-GAP-097. A valid P-versus-NP route must establish extra computational work after input access, for all uniform all-input T5 decision algorithms, and justify any machine/representation reverse simulation. **P versus NP OPEN.**

**Evidence:** A complete two-implementation reproducibility package is generated separately as \`TMR4_096_T5_randomized_source_probe.zip\` with code, complete signed literal evaluations, canonical source hashes, raw JSON, repeat logs, a standalone TeX section and SHA-256 manifest. This archive is a conversation artifact, not claimed to be committed into the GitHub tree.
