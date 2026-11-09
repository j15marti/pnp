# LSPV-5 independent red-team report: graph-sensitive source cover to bounded-fan-in shared-DAG work

**Run:** 452  
**Role:** LSPV-5, Route B independent red team  
**Time:** 2026-11-08 21:57 PST (America/Los_Angeles)  
**Tracker node:** `[P2-L5-452]`  
**Status:** **PROVED/RESTRICTED** lemma; **COMPUTATIONAL** finite controls; historical accepted-byte grammar, complete mixed transfer, superpolynomial bound and B3 remain **OPEN**.  
**P versus NP:** **OPEN**.

## Claim card before search

**Initial hypothesis.** For the published-family-derived strict-3CNF mod-3 Tseitin source, the articulation correction in `[P2-L5-451]` and the two-vertex defect cover in `[P2-L3-521]` combine into a graph-parameterized lower bound on the number of distinct original sources used by any sound source-explicit refutation. If every charged inference has at most $a$ antecedents, the standard connected-ancestry count then survives arbitrary legal sharing and gives a charged-node bound.

Assumptions were fixed before testing: connected simple cubic $G$; nonzero total charge $sigma\in\mathbb F_3$; the exact original-variable proper strict-3CNF source below; every dependence on the input passes through an authenticated original-source leaf; auxiliary definitions are conservative; all inference rules are sound; the chosen refutation dependency graph is finite, acyclic and has one false root; and every charged internal node has at most $a\ge2$ antecedents. For historical `R_mix341`, the frozen `/341` prose declares $a=2$ and unit cost, but the accepted-byte grammar remains `[P2-D1]` **OPEN**.

**Precise falsifiers.**

1. An indispensable forbidden clause from `[P2-L5-451]` also belongs to the pair-defect class $R_v$, invalidating addition of the two source counts.
2. A legal, sound, conservative source-explicit derivation can refute a satisfiable subset of the sources it actually uses.
3. Reconvergence or a shared lemma yields a finite acyclic dependency graph with $r$ source leaves and $q<\lceil(r-1)/(a-1)\rceil$ internal nodes of indegree at most $a$.
4. Historical `R_mix341` has a native authenticated inference of unbounded antecedent arity, or the prose declaration is insufficient to authenticate the byte-level antecedent relation.

## IDEA -> SEARCH -> ITERATE outcome

Falsifiers 1--3 did not fire under the stated assumptions. Falsifier 4 **partly fired at the authentication layer**: the frozen `/341` declaration is explicitly at-most-binary, but no authoritative accepted-byte grammar/checker was found or executed. Therefore the mathematical lemma is proved for the declared/source-explicit bounded-arity model and is only conditional on a faithful historical byte realization.

The initial idea was revised in two ways.

* The binary connected-ancestry inequality is not new here: it is already proved in the historical `/341` report. The actual advance is the graph-sensitive lower bound on required sources, its articulation-aware combination with the pair-defect cover, and the explicit arity-$a$ form.
* The result is linear. It neither strengthens `[P2-L3-522]` on 3-vertex-connected graphs nor transfers Pang's exponential lower bound through all legal `R_mix341` rules. It is a necessary lower-bound control, not `[P2-B1]`.

## Exact family/encoding/theorem/method/transfer ledger

| Item | Exact statement and qualification |
|---|---|
| Family | Connected simple cubic $G=(V,E)$, $h=|V|$, $m=3h/2$, an orientation, charges $b:V\to\mathbb F_3$ with $\sigma=\sum_v b_v\ne0$. Variables $x_{e,t}$ for $e\in E,t\in\mathbb F_3$. |
| Exact strict-3CNF source | For every edge, $A_e=(x_{e,0}\lor x_{e,1}\lor x_{e,2})$. For every vertex $v$ and every incident triple $t=(t_1,t_2,t_3)$ whose signed sum is not $b_v$, include $D_{v,t}=(\neg x_{e_1,t_1}\lor\neg x_{e_2,t_2}\lor\neg x_{e_3,t_3})$. There are $m+18h$ clauses, all width 3. The local clauses and ALOs force singleton edge labels in any model. |
| Size parameter | $h$ vertices, $m=3h/2$ edges, $3m$ Boolean variables, $m+18h=39h/2$ clauses; ordinary binary-ID encoding length is $O(h\log h)$. |
| Certified UNSAT | Summing all signed vertex equations cancels every edge and contradicts $\sigma\ne0$. This is semantic UNSAT, not a proof-size lower bound by itself. |
| Published restricted hardness control | Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837, Theorem 7.2(b): for fixed primes $q\ne p$, fixed $r$, and fixed-degree regular edge expanders, the one-hot $\mathrm{Tseitin}_q(G,b)$ encoding needs $\exp(\Omega(N))$ size in $\operatorname{Res}(\mathrm{PC}_r/\mathbb F_p)$. The theorem states its encoding and the opposite-characteristic PC-degree transfer. This is **PROVED/RESTRICTED**, not all algorithms and not automatically this exact strict3 source or `R_mix341`. |
| Haken/Cook controls | Haken (TCS 39, 1985, DOI 10.1016/0304-3975(85)90144-6) proves superpolynomial ordinary Resolution lower bounds for PHP; Cook's 1976 ER construction gives polynomial proofs. Thus an ordinary-Resolution lower bound cannot be imported across definitions/extensions without a simulation theorem. |
| Known shortcuts actively retained | Shared-DAG Resolution, case analysis where native, extension-variable/ER packets, GF(2)/affine Tseitin reasoning, learned lemmas and reconvergence. `[P2-L1-524]` and `[P2-L3-523]` are explicit ER2-OWNER local upper controls. None is excluded to protect the lower bound. |
| Remaining transfer | Authenticate historical source/facet/antecedent bytes `[P2-D1]`; prove the strict3-to-published-family lower-bound-preservation direction, not mere equisatisfiability; simulate or lower-bound every mixed rule `[P2-C3]`; obtain superpolynomial $\overline W_R$ `[P2-B1]`; prove noncircular same-$R$ B3 `[P2-B2]`. |

The primary Pang statement explicitly requires fixed $r$, opposite characteristic $p\ne q$, and regular expanders. Its weakening rule can add many disjuncts in one step, so it is not silently identified with the historical bounded-antecedent calculus. Haken and Cook are mandatory opposing controls: definitions can collapse a restricted-system lower bound.

## New restricted theorem

For $v\in V$, let $c_v$ be the number of connected components of $G-v$. By `[P2-L5-451]`, exactly

$$
e_v=3^{3-c_v}
$$

forbidden clauses at $v$ are individually indispensable. Their incident triples have signed sum $b_v-\sigma$. Every $A_e$ is individually indispensable.

Let $R_v$ be the nine forbidden clauses whose incident triples have signed sum $b_v+\sigma$. Since $\sigma\ne0$ in $\mathbb F_3$, $b_v-\sigma\ne b_v+\sigma$, so the indispensable class and $R_v$ are disjoint. By `[P2-L3-521]`, deleting all of $R_u\cup R_v$ for any distinct $u,v$ makes the source satisfiable: the prescribed divergence $b+\sigma(e_u+e_v)$ has total zero and hence lies in the incidence image of a connected graph. Deleting only one complete $R_v$ does not change the nonzero total.

Let $S$ be the set of distinct original source clauses in the ancestry of a sound refutation.

* Every individually indispensable clause is in $S$. If one were absent, $S$ would be a subset of the satisfiable formula obtained by deleting that clause.
* $S$ contains at least one member of $R_v$ for at least $h-1$ vertices. Otherwise two complete groups $R_u,R_v$ are absent and $S$ is a subset of the satisfiable two-group deletion.
* These obligations are disjoint.

Therefore every such ancestry uses at least

$$
r(G)=m+\sum_{v\in V}3^{3-c_v}+(h-1)
$$

distinct original sources.

Now retain only ancestors of the false root. With $r$ source leaves and $q$ charged internal nodes, the underlying undirected dependency graph is connected, hence has at least $r+q-1$ distinct dependency edges. Each internal node has at most $a$ incoming dependency edges, so it has at most $aq$ edges in total. Thus

$$
q\ge \left\lceil\frac{r(G)-1}{a-1}\right\rceil.
$$

This count already minimizes over the chosen legal proof DAG. OR-alternatives not selected are free; every selected AND/multi-premise obligation contributes its actual dependency edges. Reconvergence and shared lemmas are counted once and do not invalidate connectedness. Branch-local assumptions cannot leak: the theorem assumes a sound complete discharge to the unique root, and any additional assumption leaves only strengthen the graph count. It does not add a case-split, weakening or discharge rule to `R_mix341`.

For the declared unit-cost binary `/341` model,

$$
W\ge q\ge m+\sum_v3^{3-c_v}+h-2.
$$

For 2-connected cubic graphs this gives $23h/2-2$, reproducing the prior weak source-cover bound. It is weaker than the exact $39h/2-10$ source-core result `[P2-L3-522]` under 3-vertex-connectivity. For the 16-vertex three-arm articulation graph of `[P2-L5-451]`, $m=24$ and $\sum_v3^{3-c_v}=118$, so $r=157$ and $q\ge156$. Individual essentiality alone gave only $q\ge141$; the pair-defect cover adds 15 valid source obligations. The unsafe 2-connected substitution would instead claim $q\ge182$.

## Independent finite construction and hostile checks

The Python producer and independently authored Node verifier cover $K_4$, $K_{3,3}$, the cube, Petersen and the 16-vertex articulation graph. They reconstruct incidence equations over $\mathbb F_3$ and check:

* every indispensable forbidden-clause deletion witness;
* every edge-ALO deletion witness;
* every two-vertex $R_u,R_v$ deletion witness;
* infeasibility of every single wrong-defect target;
* all $c_v$, $r(G)$ and arity-$a$ bounds for $a=2,3,4$;
* tight abstract acyclic dependency DAGs attaining the combinatorial ceiling; and
* rejection/classification of sigma-zero overlap, omitted-two-group, unbounded-arity and cyclic-dependency hostile controls.

| Graph | $h$ | $m$ | $\sum_v3^{3-c_v}$ | $r(G)$ | binary $q$ lower bound | fan-in 3 | fan-in 4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| $K_4$ | 4 | 6 | 36 | 45 | 44 | 22 | 15 |
| $K_{3,3}$ | 6 | 9 | 54 | 68 | 67 | 34 | 23 |
| cube | 8 | 12 | 72 | 91 | 90 | 45 | 30 |
| Petersen | 10 | 15 | 90 | 114 | 113 | 57 | 38 |
| three-arm articulation | 16 | 24 | 118 | 157 | 156 | 78 | 52 |

Producer: 650 explicit finite witnesses, 0.096 s, 11,136 KiB reported maximum RSS. Independent Node replay: **PASS**, five graphs, 1,514 checks. SHA-256: producer `7cc4ddd53dec2e9583b10ed42464c0dc3fadaf3f3c6d5eda31e93fc2269f3a2f`; verifier `085365fec2c4fdefb546f30195c0dbc36e2ce0d60264f1a986e3d971ea5aef2d`; raw `97a7f83a1477ea6c6d6f0e77f9a4979b7aa77edf56c715ce51a7859b3d4499dc`. This is an independent source-semantics implementation, not an execution of an authoritative historical checker.

## Peer upper controls replayed

The exact published LSPV-1/524 producer and independent verifier were fetched and rerun: 7 original sources, 19 DEF owners, 54 RES, 73 paid nodes, 118 records, 160 verifier checks, five corruptions and three malformed inputs rejected, maximum RES depth 11. The LSPV-3/523 composition was also rerun: 21 genuine sources, 87 RES + 19 DEF = 106 paid nodes, 165 records, 512 source valuations with 9 models, maximum RES depth 16. Both pass at their stated **proposed ER2-OWNER local-component** scope. Neither is a global UNSAT refutation or historical checker execution, so neither contradicts the source lower bound. They remain important evidence that extensions and local algebraic ports can create short legal upper paths if the historical calculus authenticates them.

## B3 red-team result

No noncircular same-calculus B3 bridge was found. Cook--Reckhow proves that NP closure under complement is equivalent to the existence of a polynomially bounded propositional proof system; it does not make this fixed `R_mix341` polynomially bounded. A verified trace checker proves only acceptance/soundness of supplied traces. The present bounded-fan-in lower bound likewise says nothing about constructing traces from a hypothetical SAT decider. `[P2-B2]` remains **OPEN**.

## Search and repository audit log

Indexed web search was available; no separate Google-branded portal was available, so no Google-specific use is claimed. Actual queries included `Haken 1985 intractability resolution pigeonhole primary`, `Cook extended resolution pigeonhole polynomial`, `bounded fan-in proof DAG leaves internal nodes`, `minimal unsatisfiable clause lower bound`, and `Pang Res(PC_r) Tseitin Theorem 7.2`.

Primary statements inspected: Pang arXiv:2610.00837 lines containing the exact Tseitin encoding and Theorem 7.2(b); Haken DOI abstract; Cook--Reckhow 1979 Definitions 1.3 and Propositions 1.4; Goldreich's proof-complexity DAG discussion, which explicitly separates finite bounded-fan-in DAG proof size from uniform discovery cost.

Required change-aware repositories:

* `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, unchanged from the pinned review. Full `proofs/experiments/issue532/ideas/Idea15.md` was read. Its circuit/formula fan-in remarks do not authenticate `R_mix341`; its own verdict keeps the P-versus-NP implication conditional.
* `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, unchanged. Full `ROADMAP.md` was read. It explicitly preserves restricted-proof and finite-certificate limits; no same-calculus B3 or source-cover theorem was found.

Rotating corpus actually inspected:

* `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, full `format.md`: XLRUP is a distinct format/checker, with XOR steps passed to `cake_xlrup`; it is not historical `R_mix341` authentication.
* `tanyongkiam/cake_lpr` head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`.
* `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3`, full `README.md`: finite shortest Resolution/Q-resolution search only, not all mixed rules.
* `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`; no relevant fixed-calculus bridge found.
* `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; repository text/build claims were not treated as proof of this target.

The governing handoff, issue #3, `AGENTS.md`, `CODEX.md`, the complete PNP research skill and its mode/protocol references, actual Grok and Claude directories, relevant historical reports, and both trackers were read. Exact tracker blobs before publication: `proof1.txt` `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` was refetched again before the write because peers appended `[P2-L4-511]` during this run.

## Full resource ledger

Logical lower-bound work is the qualified $q$ above; it excludes discovery cost by definition. Actual audit costs were separately charged: governing/tracker/issue/repository reads; seven external head reads; full relevant-file reads; primary-literature retrieval; Python construction; 398,926 raw JSON bytes; independent Node parsing/reconstruction; peer producer/checker replay; report/handoff/delta/outbox construction; Git blob/tree/commit/ref operations; issue comment; and full post-write readback. No cache or precomputed witness was silently counted as a historical proof. Failed work included unavailable `/usr/bin/time`, after which internal producer timing and `resource.getrusage` were used; the failed call produced no scientific result. Peak producer RSS was 11,136 KiB. The 398,926-byte raw artifact dominates simultaneous local output storage; all publication blobs are explicitly stored and read back.

The root `main.tex` blob still returned zero readable bytes. It was not edited. A durable LSPV-5 insertion fallback was published instead. No task, title, identity, schedule, timezone, enabled state, allocation, historical grammar or historical weight was changed.

## Tracker determination and precise remaining gap

`proof1.txt`: no material status, dependency, evidence or gap change.  
`proof2.txt`: material new restricted evidence, recorded as `[P2-L5-452]`, depending on/refining `[P2-L5-451]`, `[P2-L3-521]`, `[P2-L3-522]`, `[P2-D1]`, `[P2-C3]`, `[P2-B1]` and `[P2-B2]`.

**Actual advance:** an articulation-aware required-source theorem and arity-$a$ shared-DAG node bound, with independent finite controls and explicit scope.  
**Verification:** all new controls and the two current peer upper controls passed at their stated scopes.  
**Publication:** report, producer, independent verifier, raw JSON, fallback insertion, handoff, tracker update and issue #3 notice were prepared for conflict-safe publication and full readback.  
**Precise remaining gap:** authenticate the historical byte grammar and every native mixed rule, then prove a lower-bound-preserving transfer from an established restricted hard family across all those rules to superpolynomial $\overline W_R$, while separately proving a noncircular B3 for the same fixed calculus. None is supplied here. P versus NP remains **OPEN**.
