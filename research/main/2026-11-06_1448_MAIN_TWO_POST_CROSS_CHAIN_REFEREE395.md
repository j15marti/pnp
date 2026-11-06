# LSPV-5/REFEREE395: two post-cross side-local steps still do not recontract legally at the 35-node floor

**November 6, 2026, 14:48 PST | Route B independent red team | COMPUTATIONAL exact finite result | P versus NP OPEN.**

This run preserves the historical $R_{\mathrm{mix341}}$ grammar and weights. It adds no split, discharge, weakening, export, semantic oracle, or free discovery step. It tests exactly the next surviving sibling shape from REFEREE394,

$$
\operatorname{Res}\bigl(C_1,\operatorname{Res}(\operatorname{Res}(C_2,D_1),D_2)\bigr),
$$

where $C_1,C_2$ are first cross-cut strict resolvents and each $D_i$ is a side-local source-once subtree. Both local steps independently choose either side. Exact original-source masks are carried through both steps. The result is zero fully source-disjoint support-at-most-three realizations. Therefore this displayed shape cannot supply the cross-cut AND3 input in a legal 35-node source-once proof tree. The global finite interval remains

$$
35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37.
$$

This is not an asymptotic lower bound and does not prove B3.

## 1. IDEA -> SEARCH -> ITERATE claim card

**Initial hypothesis.** Backward support accounting makes the two-step shape finite without a width shortcut: the final support-$\le3$ join forces $C_1$ to support four, its sibling $P_2$ to support at most four, $P_1$ to support at most five, and $C_2$ to support at most six. Exhausting precisely those states with source authentication will either produce a legal counterexample or exclude this one topology.

**Falsifiers stated before search.**

1. A fully source-disjoint support-$\le3$ realization of the displayed shape.
2. A required support-six intermediate omitted by the cutoff.
3. A peer or historical accepted trace realizing the topology.
4. A native non-Resolution rule reaching the 35-node floor and bypassing the topology reduction.

Falsifier 2 materially changed the search relative to REFEREE394: current LSPV-3/459 proves that support-four first steps and support-five next steps occur linearly often in random proper 3-CNF, so no shallow width plateau may be generalized. The final code retains every support-four, five, and six first-cross state forced by the exact backward bound. No instance of falsifiers 1, 3, or 4 was found.

**Revised claim.** For the authenticated bridge MUS, under the already established 35-node source-once tree reduction, no legal realization of the displayed two-post-cross chain produces support at most three. This claim is finite, computational, and topology-specific.

## 2. Fixed source, assumptions, and AND/OR semantics

The source is the exact proper strict-3-CNF from two subdivided $K_4$ graphs joined by one bridge edge. Edge variables are $x_1,\ldots,x_{15}$. At each degree-three vertex, the four clauses falsified by assignments of the wrong local parity are emitted. The charge vector is $(1,0,\ldots,0)$, giving 40 clauses. The unique essential 36-clause MUS uses source IDs

$$
0,\ldots,15,17,18,20,\ldots,36,39.
$$

The two 18-source halves share only $x_{15}$. The DIMACS SHA-256 remains `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`.

The run depends on earlier verified finite statements only at their published scope: REFEREE386 forces any 35-node derivation to be a full binary source-once tree; REFEREE390 forces a cross-cut AND3-produced factor/equation; REFEREE391 makes the lowest cross-cut clause ancestor a strict Resolution node of support at least four; REFEREE392--394 exclude side-local, first-cross, and one-post-cross immediate siblings. No unary LOCAL, paid DEF, reconvergence, or duplicated source fits the 35-node floor.

Every choice of pivot, source subset, left/right side for $D_1,D_2$, and local tree is an OR alternative minimized over after the fact. Every strict Resolution node is an AND obligation requiring both premise subtrees. The final sibling join enforces source disjointness on the left and right source-ID masks separately. No branch-local lemma is exported across assumptions; no case-split or discharge rule is used. Sharing is not double-counted: at this floor the dependency graph is forced to be a tree. This says nothing about 36-node shared DAGs.

## 3. Complete finite reduction

Let

$$
P_1=\operatorname{Res}(C_2,D_1),\qquad P_2=\operatorname{Res}(P_1,D_2).
$$

In a strict non-tautological Resolution inference, every non-pivot variable of either parent survives. Since every first cross resolvent has support at least four:

1. final support $\le3$ forces $|\operatorname{supp}(C_1)|=4$ and $|\operatorname{supp}(P_2)|\le4$;
2. the second local step forces $|\operatorname{supp}(P_1)|\le5$;
3. the first local step forces $|\operatorname{supp}(C_2)|\le6$;
4. a local $D_1$ may introduce at most $6-|\operatorname{supp}(C_2)|$ variables outside $C_2$;
5. a local $D_2$ may introduce at most $5-|\operatorname{supp}(P_1)|$ variables outside $P_1$.

These are necessary bounds, not heuristic cutoffs. The producer enumerates all first-cross states of support 4--6, applies every eligible side-local catalog clause on either side at each step, and retains componentwise inclusion-minimal $(M_L,M_R)$ provenance pairs. This antichain reduction is lossless for later disjointness: if a nonminimal pair is disjoint from another ancestry, a retained componentwise subpair is also disjoint.

Both independently written implementations reproduce:

| Quantity | Exact value |
|---|---:|
| Unique side-local clauses | 3,234 per side |
| All first cross strict-resolvent patterns | 4,056,196 |
| Support-four first-cross patterns | 6,724 |
| Support-four-to-six first-cross patterns | 211,716 |
| Unique support-four-to-six cross clauses | 211,716 |
| Minimal source-mask pairs on those clauses | 1,133,732 |
| First extension candidate queries | 19,258,192 |
| First extension strict patterns | 5,288,672 |
| First extension legal mask unions | 947,264 |
| First extension unique clauses / minimal pairs | 59,440 / 70,592 |
| Second extension candidate queries | 303,040 |
| Second extension strict patterns | 128,288 |
| Second extension legal mask unions | 32,832 |
| Second extension unique clauses / minimal pairs | 6,464 / 6,944 |
| Final clause queries / catalog hits | 537,920 / 101,376 |
| Final strict support-$\le3$ patterns | 25,344 |
| Distinct final support-$\le3$ clauses | 2,296 |
| Fully source-disjoint final realizations | **0** |

### Theorem 395.1 (COMPUTATIONAL exact finite)

For the authenticated bridge MUS and historical strict Resolution, no source-once realization of

$$
\operatorname{Res}\bigl(C_1,\operatorname{Res}(\operatorname{Res}(C_2,D_1),D_2)\bigr)
$$

has final support at most three when $C_1,C_2$ are first cross-cut resolvents and $D_1,D_2$ are side-local.

### Independent verification

The producer represents clauses as positive/negative bit pairs and closes each 18-source side by exact subset dynamic programming. The verifier independently reconstructs the graph and source clauses from incidence, encodes local clauses in base three, builds a separately generated 43,046,721-entry Resolution table, and recomputes every closure, cross state, extension, antichain, and final join. It reproduced every producer field and rejected 27 hostile one-count/result mutations. Producer time was 33.361029 s with 830,244 KiB peak RSS; verifier time was 43.0988 s with 490,992 KiB peak RSS.

This was not execution of the unavailable authoritative historical accepted-byte checker.

## 4. What the zero proves—and what it does not

Combining REFEREE392--395, the immediate sibling above the relevant first cross-cut path cannot be side-local, a first cross resolvent, a first cross resolvent with one side-local continuation, or the exact linear two-side-local continuation tested here. The zero does not exclude:

- branched post-cross sibling subtrees rather than a linear continuation;
- longer main paths before the AND3 interface;
- a 36-node proof with one unary node, one duplicated source, or reconvergence;
- any legal mixed-rule shortcut outside the already established 35-node reduction;
- a short proof for an unbounded hard family.

The known 37-node bridge derivation remains a mandatory upper-bound control: 28 AND3, 6 XOR, 2 LOCAL, and 1 Resolution node. The ideal $W_R$ grants free after-the-fact optimal legal choice; the search cost below is charged only to this implemented upper-bound/finite-exclusion computation.

## 5. Established-family / theorem / encoding / shortcut ledger

| Family | Exact 3-CNF encoding and size | Published lower bound and model | Known legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Chvátal--Szemerédi random proper 3-CNF | $F(n,3,8n)$: $8n$ independent clauses, each uniform over the $8\binom n3$ ordinary signed clauses on three distinct variables; source length $N=\Theta(n\log n)$ in explicit binary indexing | JACM 35(4), 1988, theorem at pp. 759--768: for $c2^{-k}\ge0.7$, random $cn$ width-$k$ CNF is UNSAT and ordinary shared-DAG Resolution complexity is at least $(1+\epsilon)^n$ w.h.p. For $k=3,c=8$ this applies. **KNOWN/PROVED-RESTRICTED** | Arbitrary width, sharing, branching, preprocessing, extensions, algebra, and mixed rules must remain legal | No lower-bound-preserving simulation/retraction through every historical $R_{\rm mix341}$ rule |
| Pang random proper 3-CNF | Same $F(n,3,8n)$ family | arXiv:2610.00837v2, degree--size theorem plus applications: exponential DAG size in fixed-$p$, fixed-$r$ $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ under the stated linear PC-degree premise. **PROVED-RESTRICTED/preprint** | Syntactic weakening, contraction, polynomial combination/multiplication are native there; historical DEF/LOCAL/AND3/GF(2) are not thereby covered | Exact rule-by-rule transfer to the fixed mixed calculus remains OPEN |
| Haken unary PHP | Variables $x_{ij}$; pigeon clauses $\bigvee_jx_{ij}$ plus binary collision clauses $\neg x_{ij}\vee\neg x_{i'j}$ | Haken, TCS 39 (1985), ordinary shared-DAG Resolution exponential lower bound. **KNOWN** | Cook Extended Resolution has polynomial proofs | Wide-to-strict-3 lower-bound preservation and full mixed-rule retraction remain OPEN; equisatisfiability is insufficient |
| Braun bit-PHP | $n=2^\ell$ holes, $n+1$ pigeons, bit variables $b_{it}$; for each pigeon pair and label $z\in\{0,1\}^\ell$, one width-$2\ell$ collision clause | arXiv:2609.23015v2: every DAG-like $\operatorname{Res}(\oplus)$ refutation has more than $\exp(n/(32768\ell^2))$ nodes for $\ell\ge32$. **PROVED-RESTRICTED/preprint** | Paid extensions and all historical mixed gates remain legal controls | Source is not 3-CNF; no precise lower-bound-preserving strict-3 encoding is established |
| Cubic odd Tseitin | At each cubic vertex emit four proper width-three clauses excluding the wrong parity; $4|V|$ clauses | Exponential ordinary Resolution on suitable expanders. **KNOWN/PROVED-RESTRICTED** | Gaussian elimination, native GF(2), and the historical $4h-1$ proof are mandatory shortcuts | This family is a failure for full mixed hardness unless those shortcuts are lower-bounded |
| Authenticated bridge control | Exact 15-variable, 40-clause strict-3 encoding; unique 36-clause MUS | Certified finite UNSAT plus topology-specific exact computation; **COMPUTATIONAL**, not asymptotic hardness | Known 37-node mixed derivation | Branched post-cross and all 36-node topologies remain OPEN |

Certified UNSAT, certified proof-size hardness in a named system, and empirical solver difficulty are different claims. None of these rows establishes hardness against all algorithms.

## 6. Search and source-authentication ledger

The run read the governing five-role handoff, issue #3, current Route B peer reports, Route A correction, root instructions, research protocol, original /341 grammar, REFEREE386--394, and the actual Grok and Claude TPORT assessments. LSPV-1/456 contributes a random-3CNF source-core lower bound of only $\Omega(n)$ for a broad binary-premise unit-paid ancestry model; it is not superpolynomial and does not prove B3. LSPV-3/459 supplies the width-four/width-five escape falsifier noted above. LSPV-4/451 corrects a Route A streaming claim and supplies no Route B transfer.

Primary search authenticated the exact Chvátal--Szemerédi distribution and DAG-sequence definition from the paper, Haken's ordinary Resolution scope, Braun's DAG-like $\operatorname{Res}(\oplus)$ scope, and Pang's explicit node-counting $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ rules. The Haken publisher page returned HTTP 403, but its bibliographic record and theorem scope were available; this limitation is recorded. A Google-branded search interface was unavailable, so no Google-specific execution is claimed.

Required repository heads were change-aware checked and unchanged from the immediately preceding run: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, FRAT-XOR `18cd6bc1...`, short-proof `2c524cfc...`, openai/math `4eaee875...`, and anthropics/formal-math `16a5ce41...`. These repositories remain evidence and hypothesis sources, not authorities. FRAT-XOR is an XOR-aware proof/checking format; it is not the authoritative historical $R_{\rm mix341}$ checker.

The local preflight reported missing root `main.tex`, AGENTS, CODEX, and local research skill text because this workspace is a partial checkout. Complete current remote files were used for governance and any root update must use the complete remote blob. `/usr/bin/time` was also absent; that launch failed before program execution and was charged. Both executables report their own wall time and `getrusage` peak RSS.

## 7. Fully charged resource ledger

| Phase | Charged result |
|---|---|
| Logical nodes/queries | 2,252,194,390 side pair tests; 4,056,196 cross pairs; 19,258,192 first-extension queries; 303,040 second-extension queries; 537,920 final queries |
| Producer | 33.361029 s; 830,244 KiB peak RSS |
| Independent verifier | 43.0988 s; 490,992 KiB peak RSS |
| Evidence bits | Two C++ sources, producer JSON, verifier JSON, preflight log, manifest, report, handoff, root fragment, issue outbox |
| Construction/search | Exact subset closures, provenance antichains, candidate caches, source reads, primary-literature search, peer review |
| Parsing/index/head reads | Current project head/issue, six external repository heads, governing and peer files; service CPU/RSS unavailable |
| Failed policies | Missing `/usr/bin/time` launch (exit 127 before execution); incomplete local preflight |
| Verification | Independent graph reconstruction, base-3 encoding, 43,046,721 table entries, 27 hostile mutations |
| Caches/retrieval/recomputation | Producer retained subset closures and caches; verifier recomputed all logical state rather than trusting producer memory |
| Output/publication | SHA-256 manifest, GitHub tree/commit/ref update, issue comment, and complete readback charged if successful |
| All-phase simultaneous measured peak | 830,244 KiB; browser and publication-service peak unavailable |

Logical work, weighted critical-path span, and realizable time/space schedules remain distinct. This sequential finite computation establishes no proof-space theorem and no FLMV same-machine bound.

## 8. B3 verdict and precise remaining gaps

No noncircular same-system B3 bridge was proved. Completeness, a polynomial SAT decider, a verified checker, or polynomial proofs in some other system does not by itself yield polynomial $R_{\mathrm{mix341}}$ refutations. B1, B2, B3, superpolynomial $\overline W_{R_{\mathrm{mix341}}}$, and P versus NP remain **OPEN**.

**Actual advance.** The exact linear two-post-cross side-local sibling shape is exhaustively excluded at the authenticated 35-node floor, including all forced support-six first-cross intermediates, both side choices at each extension, and exact source provenance.

**Finite next gap.** Test branched post-cross sibling subtrees and longer main paths; then analyze all three 36-node topology classes with assumption-safe sharing/reconvergence.

**Asymptotic next gap.** Starting from the established Chvátal--Szemerédi/Pang proper 3-CNF family, prove a polynomial lower-bound-preserving transfer through every historical mixed rule and every known shortcut, or produce a legal counterexample. Separately prove a noncircular rule-specific B3 implication for this same calculus.

## Artifacts

- `experiments/review/lspv5_395_two_post_cross_chain.cpp`
- `experiments/review/lspv5_395_independent_verify.cpp`
- `results/raw/review/2026-11-06_1448_LSPV5_TWO_POST_CROSS395.json`
- `results/raw/review/2026-11-06_1448_LSPV5_TWO_POST_CROSS395_VERIFY.json`
- `results/raw/review/2026-11-06_1448_LSPV5_PREFLIGHT395.json`
- `results/raw/review/2026-11-06_1448_LSPV5_TWO_POST_CROSS395_manifest.json`
- `research/coordination/2026-11-06_1448_LSPV5_TWO_POST_CROSS395_HANDOFF.md`
