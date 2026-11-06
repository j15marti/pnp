# LSPV-5/REFEREE396: the first branched post-cross sibling also fails source authentication

**November 6, 2026, 15:48 PST | Route B independent red team | COMPUTATIONAL exact finite result | P versus NP OPEN.**

This run preserves the historical $R_{\mathrm{mix341}}$ rules and weights. It adds no split, discharge, weakening, export, semantic equality oracle, or discovery charge to the ideal minimum. It tests the first branched sibling topology left after REFEREE394--395:

$$
\operatorname{Res}\bigl(C_0,\operatorname{Res}(P_1,P_2)\bigr),
\qquad
P_i=\operatorname{Res}(C_i,D_i),
$$

where each $C_i$ is a first cross-cut strict resolvent and each $D_i$ is a side-local source-once subtree chosen independently on either side. Of 20,689,215 exact inner-resolvent templates, 1,051,016 have both semantic parents in the legal one-post-cross catalog. **None** admits disjoint original-source ancestry. The branch catalog is therefore empty before the final join.

The finite global interval remains

$$
35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37.
$$

This does not prove an unbounded-family lower bound or B3.

## 1. IDEA -> SEARCH -> ITERATE claim card

**Initial hypothesis.** Backward support accounting reduces the branched topology to all support-$\le5$ one-post-cross premises. Rather than pair 59,440 clauses quadratically, enumerate every possible support-$\le4$ inner resolvent $Q$, its pivot, and the three choices for each output literal: left parent only, right parent only, or both. Exact provenance will then either produce a legal counterexample or exclude the topology.

**Falsifiers fixed before search.**

1. A fully source-disjoint final support-$\le3$ realization.
2. A legal parent of support above five omitted by the backward bound.
3. A peer or historical accepted trace realizing the topology.
4. A native non-Resolution bypass invalidating the existing 35-node topology reduction.

**Evidence-driven revision.** LSPV-3/460 proves only a source-local AND3 scarcity theorem for the published random proper 3-CNF family and explicitly records unrestricted Resolution/DEF escapes. It does not justify a shallow-width cutoff. REFEREE396 therefore retains every support-four-to-six first-cross state, every legal support-$\le5$ one-post-cross state, and every exact support-$\le4$ inner resolvent template. The resulting obstruction is provenance, not semantic width: over one million semantic branch pairs exist, but zero source-disjoint pairs survive.

**Revised claim.** Under the already verified 35-node source-once tree reduction for the authenticated bridge MUS, the displayed branched topology is impossible. This is finite, computational, and topology-specific.

## 2. Source, model, AND/OR obligations, and known upper bound

The source is the authenticated proper strict-3-CNF obtained from two subdivided $K_4$ graphs connected by one bridge edge. Edge variables are $x_1,\ldots,x_{15}$. Every cubic vertex emits the four clauses excluding assignments of the wrong local parity. The charge vector $(1,0,\ldots,0)$ gives 40 clauses, and the unique essential 36-clause MUS uses source IDs

$$
0,\ldots,15,17,18,20,\ldots,36,39.
$$

The two 18-source halves share only $x_{15}$. The DIMACS SHA-256 is `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`.

REFEREE386 forces every 35-node candidate to be a full binary source-once tree. REFEREE390 requires a cross-cut AND3-produced factor/equation. REFEREE391 makes the lowest cross-cut clause ancestor a strict Resolution node of support at least four. REFEREE392--395 exclude side-local, first-cross, one-post-cross, and linear two-post-cross immediate siblings. At this floor no unary LOCAL, paid DEF, duplicated source, or reconvergence fits.

All choices of pivots, source subsets, local tree shapes, and sides for $D_1,D_2$ are OR alternatives minimized over after the fact. Every strict Resolution node is an AND obligation requiring both premises. The source-mask check requires $P_1$ and $P_2$ to be disjoint separately on both halves, and then requires their union to be disjoint from $C_0$. No premise is omitted and no branch-local conclusion leaks across assumptions. Sharing is not double-counted because the 35-node dependency graph is forced to be a tree; 36-node reconvergence remains open.

The mandatory upper-bound control is the known 37-node mixed proof: 28 AND3, 6 XOR, 2 LOCAL, and 1 Resolution node. Known algebraic or extension shortcuts are evidence about the true minimum and are not excluded.

## 3. Complete backward support lemma

Write $Q=\operatorname{Res}(P_1,P_2)$. A strict non-tautological Resolution step removes exactly its pivot and preserves every non-pivot parent variable. Since every first cross resolvent has support at least four:

1. final support at most three forces $|\operatorname{supp}(C_0)|=4$ and $|\operatorname{supp}(Q)|\le4$;
2. each branch parent satisfies $|\operatorname{supp}(P_i)|\le5$;
3. each first-cross ancestor satisfies $|\operatorname{supp}(C_i)|\le6$;
4. the corresponding side-local $D_i$ may introduce at most $6-|\operatorname{supp}(C_i)|$ variables outside $C_i$.

Thus the support ceilings 4, 5, and 6 are necessary consequences, not optimizer cutoffs.

For every exact signed clause $Q$ of support at most four, every pivot outside $Q$, and every assignment of each literal of $Q$ to left-only, right-only, or both parents, the code constructs the unique oriented parent pair with positive pivot on the first parent and negative pivot on the second. This enumerates every strict non-tautological parent pair resolving to $Q$ exactly once. Both parents are looked up in the complete one-post-cross catalog. Componentwise inclusion-minimal provenance antichains are lossless for later disjointness.

## 4. Exact result

Both implementations reproduce:

| Quantity | Exact value |
|---|---:|
| Unique side-local clauses | 3,234 per side |
| All first-cross strict-resolvent patterns | 4,056,196 |
| Support-four first-cross patterns | 6,724 |
| Support-four-to-six first-cross patterns | 211,716 |
| Minimal masks on support-four-to-six cross clauses | 1,133,732 |
| One-post-cross candidate queries | 19,258,192 |
| One-post-cross strict patterns | 5,288,672 |
| One-post-cross legal mask unions | 947,264 |
| One-post-cross unique clauses / minimal pairs | 59,440 / 70,592 |
| Exact support-$\le4$ target clauses | 25,931 |
| Exact branch resolvent templates | 20,689,215 |
| Templates with both parents present | 1,051,016 |
| Semantically valid branch pairs | 1,051,016 |
| Source-disjoint branch mask unions | **0** |
| Final branch catalog entries | **0** |
| Fully source-disjoint final realizations | **0** |

### Theorem 396.1 (COMPUTATIONAL exact finite)

For the authenticated bridge MUS and the historical strict-Resolution rule, no source-once realization of

$$
\operatorname{Res}\bigl(C_0,\operatorname{Res}(P_1,P_2)\bigr),
\qquad
P_i=\operatorname{Res}(C_i,D_i),
$$

has final support at most three when $C_0,C_1,C_2$ are first cross-cut resolvents and $D_1,D_2$ are side-local.

### Verification

The producer represents clauses by positive/negative bit pairs and performs exact subset closure on each 18-source side. The independent verifier reconstructs the graph and all source clauses from incidence, uses base-three local clauses and a separately generated 43,046,721-entry Resolution table, and recomputes every cross clause, post-cross provenance antichain, branch template, and disjointness test. It reproduces all counts and rejects 18 hostile count/result mutations.

Producer: 34.979185 s and 830,364 KiB peak RSS. Independent verifier: 49.2906 s and 491,116 KiB peak RSS. This is not execution of the unavailable authoritative historical accepted-byte checker.

## 5. Established-family / theorem / encoding / shortcut ledger

| Family | Exact encoding and size parameter | Lower-bound theorem/model/status | Known methods and mandatory controls | Remaining transfer |
|---|---|---|---|---|
| Chvátal--Szemerédi random proper 3-CNF | $F(n,3,8n)$ consists of $8n$ independent clauses, each uniform over the $8\binom n3$ ordinary signed clauses on three distinct variables; explicit indexed length $N=\Theta(n\log n)$ | JACM 35(4), 1988: for $c2^{-k}\ge0.7$, the random $cn$ width-$k$ source is UNSAT and needs $(1+\epsilon)^n$ ordinary shared-DAG Resolution lines w.h.p.; applies at $c=8,k=3$. **KNOWN/PROVED-RESTRICTED** | Wide Resolution, branching, learned lemmas, sharing, paid extensions, algebra, and all mixed rules remain legal | No rule-by-rule lower-bound-preserving retraction from full historical $R_{\rm mix341}$ |
| Pang random proper 3-CNF | Same $F(n,3,8n)$ | arXiv:2610.00837v2: exponential DAG lower bounds for fixed-$p$, fixed-$r$ $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ under the stated PC-degree hypotheses. **PROVED-RESTRICTED/preprint** | Its weakening/contraction/polynomial rules do not silently cover historical DEF/LOCAL/AND3 | Full mixed transfer OPEN |
| Haken unary PHP | Pigeon clauses $\bigvee_jx_{ij}$ and collision clauses $\neg x_{ij}\vee\neg x_{i'j}$ | Haken 1985 exponential ordinary shared-DAG Resolution. **KNOWN** | Cook Extended Resolution has polynomial PHP proofs | Wide-to-strict-3 preservation and mixed-rule retraction OPEN; equisatisfiability is insufficient |
| Braun bit-PHP | $n=2^\ell$ holes, $n+1$ pigeons; for each pigeon pair and label, one width-$2\ell$ collision clause on the bit variables | arXiv:2609.23015v2: every DAG-like $\operatorname{Res}(\oplus)$ refutation has more than $\exp(n/(32768\ell^2))$ nodes for $\ell\ge32$. **PROVED-RESTRICTED/preprint** | Arbitrary conservative paid DEF and the historical mixed rules are not covered | Source is not 3-CNF; no proved lower-bound-preserving strict-3 encoding |
| Cubic odd Tseitin | Four proper width-three parity-facet clauses per cubic vertex; $4|V|$ clauses | Exponential ordinary Resolution on suitable expanders. **KNOWN/PROVED-RESTRICTED** | Gaussian elimination, native GF(2), and the historical exact $4h-1$ mixed refutation | Family failure for full mixed hardness unless all algebraic shortcuts are lower-bounded |
| Bridge validation control | Exact 15-variable, 40-clause strict-3 source; unique 36-clause MUS | Certified UNSAT and topology-specific finite computation only. **COMPUTATIONAL** | Known 37-node mixed proof | Other branches, longer paths, and all 36-node DAGs OPEN |

LSPV-3/460 adds a useful but restricted lemma: with high probability the random $F(n,3,8n)$ source has no repeated variable triple, so source-local AND3 cannot directly combine two distinct original clauses. It explicitly does not cover derived Resolution clauses, DEF, or later local factors. Certified UNSAT, certified proof hardness in a named system, and empirical solver difficulty remain separate.

## 6. Search, authentication, and source ledger

The run reviewed the governing five-role handoff, current issue #3, AGENTS, CODEX, the research protocol, the historical /341 grammar, REFEREE386--395, LSPV-1/456--457, LSPV-3/459--460, and Route-A LSPV-4/451--452. It read current Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md` blob `a20fb8b...`, which identifies FRAT-XOR's exact clause/XOR hint checking as a useful different-system authentication model but supplies no mixed lower bound or B3. It reread actual Claude TPORT and ONETAPE READMEs, blobs `d1290822...` and `6255025f...`; their restricted time-space results do not imply this Route B transfer.

Primary indexed search reauthenticated Chvátal--Szemerédi's exact distribution and DAG proof definition, Haken's ordinary-Resolution scope, Cook's polynomial ER shortcut, and Braun's unrestricted DAG-like scope within $\operatorname{Res}(\oplus)$. Search also found newer random-3CNF lower bounds for $k$-DNF Resolution, again restricted proof systems rather than general mixed rules. A direct Google-branded interface was unavailable, so no Google-specific execution is claimed.

Required repository heads were change-aware checked and unchanged: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, FRAT-XOR `18cd6bc1...`, short-proof `2c524cfc...`, openai/math `4eaee875...`, and anthropics/formal-math `16a5ce41...`. These are hypothesis, implementation, or audit sources—not authority for the historical calculus. FRAT-XOR is not the authoritative $R_{\rm mix341}$ checker.

The local preflight again reported a partial checkout with missing root `main.tex`, AGENTS, CODEX, and local protocol file. Complete current GitHub bytes are used for governance and publication. No authoritative historical accepted-byte checker was located or executed.

## 7. Fully charged resource ledger

| Phase | Charged result |
|---|---|
| Logical work | 2,252,194,390 side pair tests; 4,056,196 cross pairs; 19,258,192 post-cross queries; 20,689,215 exact branch templates; 537,920 nominal final queries |
| Producer | 34.979185 s; 830,364 KiB peak RSS |
| Independent verifier | 49.2906 s; 491,116 KiB peak RSS |
| Explicit evidence bits | Two C++ sources, two result JSONs, preflight log, manifest, report, handoff, root fragment, issue outbox |
| Construction/search | Source closures, candidate caches, provenance antichains, template generator, peer and primary-source review |
| Parsing/source/index/head reads | Current project head and peer files, six external heads, primary literature; remote service CPU/RSS unavailable |
| Verification | Separate source construction and clause encoding, 43,046,721 table entries, 18 hostile mutations |
| Output/update/readback | Serialization, SHA-256, Git object creation, lease update, issue write, and full readback charged if successful |
| Caches/retrieval/recomputation | Producer retains side/post catalogs; verifier recomputes all logical state independently |
| Failed/limited policies | Local preflight incomplete; Google-branded interface and authoritative historical checker unavailable |
| All-phase simultaneous measured peak | 830,364 KiB; browser/publication-service peak space unavailable |

Logical work, weighted critical-path span, and realizable time/space schedules remain distinct. The sequential implementation proves no proof-space theorem and no FLMV same-machine bound.

## 8. B3 verdict and precise remaining gaps

No noncircular same-calculus B3 bridge was proved. A polynomial SAT decider, completeness, a checked proof in another system, or free minimum selection does not construct polynomial native $R_{\mathrm{mix341}}$ proofs. B1, B2, B3, superpolynomial $\overline W_{R_{\mathrm{mix341}}}$, and P versus NP remain **OPEN**.

**Actual advance.** The first branched post-cross sibling topology is exhaustively excluded at the authenticated 35-node floor. The obstruction occurs at the branch join itself: 1,051,016 semantic pairs exist, but all reuse an original source.

**Finite next gap.** Classify other branched Resolution shapes and longer main paths, then test all three 36-node topology classes with legal reconvergence and exact context/provenance accounting.

**Asymptotic next gap.** Starting from the established Chvátal--Szemerédi/Pang proper 3-CNF family, prove a polynomial lower-bound-preserving simulation/retraction through every historical mixed rule and every legal shortcut, or exhibit a legal counterexample. Separately prove a noncircular same-system B3 implication.

## Artifacts

- `experiments/review/lspv5_396_branched_post_cross.cpp`
- `experiments/review/lspv5_396_independent_verify.cpp`
- `results/raw/review/2026-11-06_1548_LSPV5_BRANCHED_POST_CROSS396.json`
- `results/raw/review/2026-11-06_1548_LSPV5_BRANCHED_POST_CROSS396_VERIFY.json`
- `results/raw/review/2026-11-06_1548_LSPV5_PREFLIGHT396.log`
- `results/raw/review/2026-11-06_1548_LSPV5_BRANCHED_POST_CROSS396_manifest.json`
- `research/coordination/2026-11-06_1548_LSPV5_BRANCHED_POST_CROSS396_HANDOFF.md`
