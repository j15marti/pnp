# LSPV-5/REFEREE394: one-post-cross siblings still cannot legally recontract to AND3 at the 35-node floor

**November 6, 2026, 13:48 PST | Route B independent red team | COMPUTATIONAL exact finite result | P versus NP OPEN.**

This run preserves the historical $R_{\mathrm{mix341}}$ rules and weights. It adds no split, discharge, weakening, clause export, semantic equality oracle, or free discovery step. It closes exactly the next sibling shape left open by REFEREE393:

$$
\operatorname{Res}\bigl(C_1,\operatorname{Res}(C_2,D)\bigr),
$$

where $C_1,C_2$ are first cross-cut strict resolvents and $D$ is side-local. Every semantically attractive support-at-most-three realization reuses an authenticated original source and is therefore illegal in the 35-node source-once tree. The global interval remains

$$
35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37.
$$

## 1. IDEA -> SEARCH -> ITERATE claim card

**Exact claim.** For every source-once realization of $C_1=\operatorname{Res}(L_1,R_1)$ and $C_2=\operatorname{Res}(L_2,R_2)$, and every side-local source-once clause $D$ disjoint from $C_2$, if both displayed Resolution steps are strict and the final result has support at most three, then the ancestry of $C_1$ intersects the ancestry of $\operatorname{Res}(C_2,D)$. Thus these two children cannot be siblings in a legal 35-node source-once proof tree.

**Model and quantifiers.** The authenticated 36-source bridge MUS; a full binary 35-paid-node source-once tree; historical strict Resolution; support-at-most-three input to AND3. All legal pivots, source partitions, local Resolution shapes, and minimal provenance masks are OR alternatives minimized over after the fact. Each binary inference is an AND obligation requiring both premise subtrees.

**SAME_REALIZATION.** The same original source IDs, left/right cut, clause polarities, pivots, and source masks are used in the semantic clause computation and the legality test.

**Initial falsifiers.** (1) A source-disjoint realization of the displayed shape; (2) an output whose final support is at most three; (3) an accepted peer or historical trace of the shape; (4) a native non-Resolution rule bypassing the interface at the 35-node floor.

Falsifier (2) is abundant: 25,920 strict patterns yield 2,296 distinct support-at-most-three clauses. Falsifier (1) does not occur. No instance of (3) or (4) was found.

**Iteration after an internal red-team failure.** The first implementation incorrectly restricted $D$ to variables already in $C_2$. That is complete for support-five $C_2$, but a support-four $C_2$ permits $D$ to introduce one new side variable while its post-cross resolvent still has support four. That preliminary zero was withdrawn. Both final implementations enumerate the exact outside-support allowance $5-|\operatorname{supp}(C_2)|$ and independently reproduce the enlarged counts and the zero.

## 2. Fixed source and native-scope dependencies

The control is the exact proper strict-3-CNF generated as follows. Take two copies of $K_4$ on vertices $0,1,2,3$ and $5,6,7,8$; subdivide edge $(0,1)$ in the first by vertex 4 and edge $(5,6)$ in the second by vertex 9; add bridge edge $(4,9)$. Edge variables are numbered in deterministic list order, with the bridge $x_{15}$. At every cubic vertex emit the four width-three clauses falsified by assignments of the wrong local parity, with charge vector $(1,0,\ldots,0)$. This gives 15 variables and 40 clauses; the exact generator is `experiments/review/lspv5_387_annotation_firewall.py`, and the DIMACS SHA-256 is `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`.

Its unique essential 36-clause MUS uses source IDs

$$
0,\ldots,15,17,18,20,\ldots,36,39.
$$

The two 18-source halves share only $x_{15}$. Earlier verified dependencies are used only at their stated scope:

- REFEREE386: every 35-node derivation is a full binary tree with all 36 sources used exactly once;
- REFEREE389: the pure-Resolution 35-node class is impossible;
- REFEREE390: a remaining 35-node proof needs a cross-cut AND3-produced factor/equation;
- REFEREE391: the lowest cross-cut clause ancestor is strict Resolution and every first cross resolvent has support at least four;
- REFEREE392: a first cross resolvent followed by Resolution with a side-local sibling cannot reach support at most three;
- REFEREE393: two first cross resolvents cannot be legal siblings that resolve to support at most three.

No unary LOCAL, paid DEF, reconvergence, or source duplication fits this 35-node floor. At this floor clause outputs are produced only by strict Resolution. This does not authenticate an unavailable historical byte checker and does not analyze 36-node DAGs.

## 3. Complete finite reduction

Write $P=\operatorname{Res}(C_2,D)$. Since every first cross resolvent has support at least four and strict Resolution removes only its pivot while preserving every other parent variable:

1. the final support-at-most-three step forces $|\operatorname{supp}(C_1)|=4$ and $|\operatorname{supp}(P)|\le4$;
2. $|\operatorname{supp}(C_2)|\le5$;
3. every variable of $D$ outside $\operatorname{supp}(C_2)$ survives in $P$, so $D$ may contain at most $5-|\operatorname{supp}(C_2)|$ such variables.

These conditions are necessary, and the final code enumerates every side-catalog clause satisfying them. It then applies strict Resolution, exact source-mask disjointness between $C_2$ and $D$, and componentwise inclusion-minimal left/right mask retention. Minimal-pair retention is lossless for later disjointness: any disjoint nonminimal pair contains a disjoint retained minimal pair.

Both implementations reproduce:

| Quantity | Exact value |
|---|---:|
| Unique side-local clauses | 3,234 per side |
| Side subset-clause occurrences | 11,705,410 per side |
| Side strict-Resolution pair tests | 1,126,097,195 per side |
| All first cross resolvents | 4,056,196 |
| Support-four first cross resolvents $C_1$ | 6,724 |
| Support-four-or-five first cross resolvents $C_2$ | 50,676 |
| Eligible side-catalog queries for $D$ | 183,024 |
| Strict post-cross patterns | 89,872 |
| Source-disjoint post-cross mask unions before minimization | 34,112 |
| Unique post-cross clauses / minimal mask pairs | 6,624 / 6,624 |
| Final clause queries / post-catalog hits | 537,920 / 103,680 |
| Final strict support-at-most-three patterns | 25,920 |
| Distinct final support-at-most-three clauses | 2,296 |
| Fully source-disjoint final realizations | **0** |

### Theorem 394.1 (COMPUTATIONAL exact finite)

For the authenticated bridge MUS and the historical strict-Resolution rule, no source-once realization of

$$
\operatorname{Res}\bigl(C_1,\operatorname{Res}(C_2,D)\bigr)
$$

has final support at most three when $C_1,C_2$ are first cross-cut resolvents and $D$ is side-local.

### Verification

The producer closes each 18-source side under strict Resolution using bit-pair clauses and exact subset masks. The independent verifier reconstructs the graph and 40 source clauses from incidence, encodes every local clause in base three, builds a separately generated 43,046,721-entry Resolution table, and recomputes the entire side closure, cross catalogs, post-cross catalog, and final join. It reproduces every count above and rejects 18 hostile count/result mutations.

The theorem is finite and computational. It is not a symbolic theorem for an unbounded family and not a lower bound against any algorithm.

### Corollary 394.2 (next surviving shape)

Combining REFEREE392--394, the immediate sibling of the next strict Resolution above the lowest cross-cut resolvent is neither side-local, nor a first cross resolvent, nor a first cross resolvent with exactly one additional side-local strict Resolution. A surviving sibling must contain at least two post-cross strict Resolution nodes, or the main path itself must be longer before the AND3 interface.

## 4. Branching, reconvergence, and sharing audit

At the 35-node floor the dependency graph is forced to be a tree. The present result therefore charges each distinct binary inference once and enforces source-disjoint sibling premises. It does not double-count shared subproofs because none fit this floor. It also does not infer anything about a 36-node shared DAG, where one unary node, duplicate source, or reconvergent dependency may fit.

No case-split rule was added. If a future proposed calculus uses assumptions $\Gamma\vdash C$, it must separately authenticate native split/discharge and prevent branch-local conclusions from crossing incompatible contexts. The ideal $W_R$ still excludes discovery cost and grants free optimal legal derivation choice. Measured construction and verification costs below are upper-bound implementation costs, not terms in $W_R$.

## 5. Established-family/theorem/encoding/shortcut ledger

| Family | Exact encoding and size parameter | Theorem/model/status | Legal shortcut control | Missing transfer |
|---|---|---|---|---|
| Pang random proper strict 3-CNF | $F(n,3,8n)$: independently sample $m=8n$ clauses, with replacement, uniformly from the $8\binom n3$ signed width-three clauses on three distinct variables | Pang, arXiv:2610.00837v2, Thm. 7.2(a): $\exp(\Omega(n))$ shared-DAG lower bounds in the stated fixed-$p,r$ $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ model, under its degree-size hypotheses. **PROVED-RESTRICTED/preprint** | Native wide excursions, DEF/LOCAL, AND3, affine rules, sharing, and branching remain legal in $R_{\rm mix341}$ | No simulation/retraction covering every historical mixed rule; LSPV-3/458 only bounds a shallow strict-Resolution fragment with high probability |
| Braun bit-PHP | $n=2^\ell$ holes, $n+1$ pigeons, variables $b_{it}$; for every pigeon pair $i<i'$ and label $z\in\{0,1\}^\ell$, one width-$2\ell$ collision clause. Formula length $\Theta(n^3\log n)$ | Braun, arXiv:2609.23015v2, Thm. 1.1: every unrestricted shared-DAG $\operatorname{Res}(\oplus)$ refutation has $>\exp(n/(32768\ell^2))$ lines for $\ell\ge32$. **KNOWN/PROVED-RESTRICTED preprint** | Cook-style paid extensions and arbitrary historical mixed gates must be allowed | The source is not 3-CNF. Equisatisfiable strict-3 conversion is insufficient; a lower-bound-preserving direction with encoded-size overhead remains OPEN |
| Haken unary PHP | Variables $x_{ij}$; pigeon clauses $\bigvee_jx_{ij}$ and binary collision clauses $\neg x_{ij}\vee\neg x_{i'j}$ | Haken 1985: $2^{\Omega(n)}$ ordinary shared-DAG Resolution lower bound. **KNOWN** | Cook 1976 gives polynomial Extended Resolution proofs | Wide-to-3-CNF transfer and full mixed-rule retraction remain OPEN |
| Cubic odd Tseitin strict 3-CNF | For each degree-three vertex, emit the four clauses excluding the wrong parity on its incident edge variables; odd total charge is UNSAT; size $4|V|$ clauses | Exponential ordinary Resolution on suitable growing expanders. **KNOWN/PROVED-RESTRICTED** | Gaussian elimination, native GF(2), and the historical $4h-1$ mixed proof are mandatory shortcuts | Family failure for full mixed hardness unless every algebraic shortcut is charged and lower-bounded |
| Authenticated bridge control | The exact 15-variable, 40-clause graph encoding above; unique 36-clause MUS | Certified finite UNSAT plus scoped exact proof analysis; no asymptotic proof-size hardness claim | Known 37-node derivation: 28 AND3, 6 XOR, 2 LOCAL, 1 RES | Two-or-more post-cross steps and all 36-node topologies remain OPEN |

Certified UNSAT, certified restricted proof-size hardness, and empirical solver difficulty are distinct. No row establishes hardness for all algorithms. Cook ER and Tseitin GF(2) are evidence about the true minimum and are never excluded to preserve a claim.

## 6. Search and authentication ledger

The current governing handoff, issue #3 through LSPV-3/458, root instructions, research protocol, original /341 grammar, REFEREE386--393, LSPV-1/455, Route-A peer LSPV-2/452, actual Grok and Claude files, and the latest current project head were reviewed. LSPV-3/458's random-3CNF theorem is a useful shallow native-Resolution scarcity result, but it explicitly leaves wide and mixed steps open.

Primary indexed search rechecked Braun arXiv:2609.23015v2, Pang arXiv:2610.00837v2, Haken 1985, and Cook 1976. Braun's exact shared-DAG definition counts proof nodes and permits reuse; it excludes extension axioms. A direct Google-branded interface was unavailable, so no Google-specific execution is claimed.

Required repository heads were change-aware checked: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, FRAT-XOR `18cd6bc1...`, short-proof `2c524cfc...`, openai/math `4eaee875...`, and anthropics/formal-math `16a5ce41...`; all were unchanged from REFEREE393. Actual READMEs and FRAT-XOR's format were reread. FRAT-XOR provides an XOR-aware checker pipeline but is not the authoritative historical $R_{\rm mix341}$ checker. External research repositories were treated as hypothesis/evidence sources, not authorities.

The local partial checkout preflight reported missing root `main.tex`, local skill text, AGENTS, and CODEX. Current complete versions were read remotely. Root reconciliation, if published, uses only complete remote blob bytes. No authoritative historical accepted-byte checker was located or executed.

## 7. Fully charged resource ledger

| Phase | Charged result |
|---|---|
| Primary logical work | 2,252,194,390 side pair tests; 4,056,196 cross pairs; 183,024 eligible $D$ queries; 537,920 final clause queries |
| Primary final run | 34.226072 s internal; 791,464 KiB peak RSS |
| Independent final run | 43.6591 s internal; 491,116 KiB peak RSS |
| Explicit evidence bits | Two C++ sources; primary JSON; independent JSON; manifest; report; handoff; root fragment; issue outbox |
| Hostile controls | 18 independently coded count/result mutations rejected; support-four outside-variable omission found and repaired before publication |
| Failed/preliminary policies | `/usr/bin/time` was absent (exit 127 before execution); incomplete-support producer/verifier runs of 31.495851 s and 45.1283 s were charged and withdrawn |
| Parsing/source/index/head reads | Current project head, issue, peer reports, primary literature, six external repository heads and actual files; remote service CPU/RSS not exposed |
| Construction/search | Source closure, 43,046,721-entry verifier table, cross/post catalogs, exact provenance antichains; discovery cost excluded only from ideal $W_R$ |
| Verification/output/publication | JSON comparison, hostile mutations, SHA-256 manifest, remote writes and complete readback charged as performed |
| Cache/retrieval/recomputation | Materialized subset closures and candidate caches retained during each run; independent run recomputed rather than trusted producer state |
| All-phase simultaneous measured peak | 791,464 KiB; publication-service and browser peak space unavailable |

Logical work, critical-path span, and realizable schedules remain distinct. This run measures sequential implementations only and proves no proof-space or FLMV same-machine bound.

## 8. B3 verdict and exact remaining gaps

This finite exclusion neither proves superpolynomial $\overline W_{R_{\mathrm{mix341}}}$ nor compiles an arbitrary polynomial-time SAT decider into a polynomial refutation in this same calculus. It supplies no reflection theorem for arbitrary decider correctness. B1, B2, B3, and P versus NP remain **OPEN**.

**Actual advance:** the exact next cross-cut sibling shape with one internal side-local post-cross Resolution has been exhaustively excluded under source authentication, including the previously omitted one-new-variable candidates.

**Finite next gap:** enumerate or structurally exclude siblings containing at least two post-cross strict Resolution nodes and longer main paths, then analyze all three 36-node topology classes with legal sharing/reconvergence.

**Asymptotic next gap:** starting from Pang's exact proper 3-CNF family or another established family, prove a polynomial lower-bound-preserving transfer through every historical mixed rule and known shortcut, or produce a legal counterexample; separately prove a noncircular same-system B3 implication.

## Artifacts

- `experiments/review/lspv5_394_one_post_cross_sibling.cpp`
- `experiments/review/lspv5_394_independent_verify.cpp`
- `results/raw/review/2026-11-06_1348_LSPV5_ONE_POST_CROSS394.json`
- `results/raw/review/2026-11-06_1348_LSPV5_ONE_POST_CROSS394_VERIFY.json`
- `results/raw/review/2026-11-06_1348_LSPV5_ONE_POST_CROSS394_manifest.json`
- `research/coordination/2026-11-06_1348_LSPV5_ONE_POST_CROSS394_HANDOFF.md`
