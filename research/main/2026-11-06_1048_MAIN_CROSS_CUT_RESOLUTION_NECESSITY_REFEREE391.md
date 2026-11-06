# LSPV-5/REFEREE391: a cross-cut Resolution chain is necessary before AND3 at the 35-node floor

**November 6, 2026, 10:48 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

This report keeps the authenticated historical $R_{\mathrm{mix341}}$ grammar and weights fixed. It adds no case split, discharge, weakening, export, or branch rule. The advance is a strict refinement of REFEREE390 for the authenticated 36-source bridge MUS: every legal 35-node proof, if one exists, must cross the left/right cut first by strict Resolution, and its first cross-cut resolvent cannot be consumed directly by historical AND3. At least one additional strict Resolution is necessary before the cross-cut affine block required by REFEREE390.

The minimum interval is unchanged:

$$
35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37.
$$

## 1. IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** Choose the lowest cross-cut inference in the ancestry of the cross-cut AND3 guaranteed by REFEREE390. Its children are side-local. Historical support typing might force that inference to be strict Resolution.

The precise falsifiers were:

1. a legal left/right side-local AND3 pair with combined original support at most three;
2. a legal lowest cross-cut XOR whose row can reach AND3 without violating support typing;
3. a first cross-cut strict resolvent with support at most three;
4. a new authenticated 35-node trace from a peer or an accepted historical checker.

Falsifiers 1--3 were rejected by complete finite interface enumeration and an independent implementation. Falsifier 4 was not found. The original hypothesis was strengthened: the first cross-cut node is strict Resolution, its output support is at least four, and another strict Resolution must intervene before historical AND3.

The scientific scope remains narrow. This is a necessary condition for one finite source-once class, not an all-rule asymptotic lower bound, not an accepted-byte proof, and not arbitrary-machine SAT hardness.

## 2. Fixed source, node floor, and native rules

The source is REFEREE386's 15-variable, 40-clause proper strict-3-CNF bridged cubic odd-Tseitin instance. Its DIMACS SHA-256 is

`4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`.

The unique essential 36-clause MUS core is indexed

`0..15,17,18,20..36,39`.

The left and right 18-source halves share only $x_{15}$. Each side contains four complete internal four-clause parity bundles and two clauses of an incomplete boundary bundle. REFEREE386 proves that every 35-node refutation of this core is a full binary tree using every source exactly once. Consequently no unary LOCAL, paid definition, source duplication, or DAG reconvergence fits at this floor. The relevant historical rules are:

- strict oriented binary Resolution, which is the only rule here producing clauses;
- binary AND3 on two condition records only when the union of their original-variable supports has size at most three; an exactly affine result may carry its exact GF(2) annotation;
- binary XOR of two GF(2) rows.

The authenticated grammar source remains `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, Git blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. The finite enumerators do not silently use CANON1, CANON2, CANON2R, semantic weakening, or an external SAT oracle.

## 3. Complete side-local interface catalogs

For every nonempty source subset of each 18-source side, the primary program closes all source-once binary outcomes under native strict RES, historical support-at-most-three AND3, exact affine annotation, and XOR. It then catalogs, in the common 15-variable coordinate system, every distinct condition that could be an AND3 child and every distinct clause that could be a Resolution child.

For **each** side the complete catalogs contain:

| Interface | Count | Support distribution |
|---|---:|---|
| Historical AND3-admissible conditions | 183 | one of support 2; 182 of support 3 |
| Clauses | 3,234 | all clauses occurring on any source subset |

All $183^2=33{,}489$ left/right condition pairs have combined support greater than three. Therefore no cross-cut AND3 can have two side-local children.

The side closure performed, per side:

| Native operation tested | Pair tests |
|---|---:|
| strict RES | 1,126,097,195 |
| AND3 | 55,144 |
| XOR | 25 |

This reproduces REFEREE390's side classification while adding the complete globally keyed AND3 and clause interfaces.

## 4. XOR cannot be the first cross-cut ancestor of the required AND3

REFEREE390 proved that the only side-local primitive affine-producing source sets are nonempty unions of the four complete internal parity bundles. The present symbolic control enumerates all 15 nonempty XOR sums of those four authenticated rows on each side.

For each side every nonempty sum is nonzero and has support at least two. The exact sorted support multiset is

$$
2,3,3,3,3,3,3,4,4,4,4,4,5,5,6.
$$

Left and right private supports are disjoint, so all 225 cross-side pairs have combined support at least four. More generally, along an XOR-only descendant chain in a source-once tree, the used primitive row bundles remain distinct. Each side component is a nonempty subset sum of its four rows and therefore never cancels to zero. Every mixed row on that chain retains at least two variables from each side and support at least four.

Historical AND3 cannot consume such a row because its combined input support must be at most three. XOR produces a row, not a clause, so strict RES cannot consume it either. Hence the lowest cross-cut node in the ancestry of the required cross-cut AND3 cannot be XOR.

## 5. First cross-cut Resolution catalog

The programs next enumerate every legal strict Resolution between the complete 3,234-clause left catalog and complete 3,234-clause right catalog. Results:

| Quantity | Exact value |
|---|---:|
| Legal cross-side strict RES pairs | 4,056,196 |
| Distinct resolvents | 4,056,196 |
| Minimum source leaves in the two children | 2 |
| Minimum resolvent support | 4 |
| Resolvents of support at most 3 | 0 |

The support distribution is:

| Output support | Count |
|---:|---:|
| 4 | 6,724 |
| 5 | 43,952 |
| 6 | 161,040 |
| 7 | 401,792 |
| 8 | 729,600 |
| 9 | 971,264 |
| 10 | 939,008 |
| 11 | 602,112 |
| 12 | 200,704 |

No other support occurs. Thus a first cross-cut resolvent is not directly AND3-admissible. Because XOR does not accept clauses and AND3 rejects support at least four, a descendant path from this first cross-cut clause to the required cross-cut AND3 must contain at least one further strict Resolution.

## 6. Structural theorem

### Theorem 391.1 (PROVED/RESTRICTED for the authenticated bridge core)

Every legal 35-node historical $R_{\mathrm{mix341}}$ refutation of the authenticated 36-source bridge MUS, if one exists, contains a directed path with the following order:

1. a lowest cross-cut strict Resolution whose two children have respectively left-only and right-only source ancestry;
2. at least one additional strict Resolution descendant;
3. a cross-cut AND3-produced factor or affine equation.

In particular, neither AND3 nor XOR can be the first cross-cut inference in the ancestry of the cross-cut affine block required by REFEREE390, and the first cross-cut resolvent cannot feed that AND3 directly.

### Proof

REFEREE390 supplies a cross-cut AND3-produced factor/equation in every putative 35-node proof. Choose a lowest cross-cut node in its ancestor subgraph. Since the proof is a full binary source-once tree, its two children have disjoint ancestries and each child is side-local; because the node crosses the unique left/right partition, one child uses left sources and the other uses right sources.

It is not AND3: the complete side-local condition catalogs contain every possible legal child condition, and none of their 33,489 cross pairs has combined support at most three.

It is not XOR: every possible side-local row child is a nonempty sum of authenticated internal rows. The exact row-support control gives support at least two on each side. Along any XOR-only continuation, source-once disjointness preserves a nonempty row subset on both sides, so mixed support stays at least four and cannot reach AND3. This contradicts the choice of the node inside the required AND3's ancestry.

The lowest cross-cut node is therefore strict Resolution. The exhaustive clause-interface product proves its resolvent has support at least four. It cannot be consumed directly by AND3, and XOR does not consume clauses. Hence at least one further strict Resolution lies between it and the required cross-cut AND3. $\square$

This theorem charges each distinct inference node once. At the 35-node floor the topology is a tree, so there is no cross-branch double counting or assumption leakage. It makes no assertion that minimum work equals minimum span or minimum scheduled space.

## 7. Established-family, encoding, theorem, and shortcut ledger

| Family | Exact encoding and size parameter | Published lower bound / model | Known legal shortcut control | Remaining transfer |
|---|---|---|---|---|
| Random proper strict 3-CNF | $F\sim\mathcal F(n,3,8n)$: 8$n$ indexed clauses drawn with replacement from all $8\binom n3$ proper signed triples; $N=O(n\log n)$ bits | Pang 2026 v2, using linear PC degree: a.a.s. $\exp(\Omega(n))$ shared-DAG syntactic Res(PC$_1/\mathbb F_2$); preprint and model-specific | Paid definitions, LOCAL exports, ER-like circuit sharing remain legal in full historical calculus | LSPV-3/456 transfers only to a locally opaque wire-defined fragment; full-$R$ superpolynomial work OPEN |
| Braun bit-PHP | $n=2^\ell$ holes, $n+1$ pigeons; pair clause $\bigvee_{t<\ell}(x_{i,t}\oplus x_{j,t}=1)$ | Braun 2026 v2: for $\ell\ge32$, unrestricted shared-DAG Res(XOR) size $>\exp(n/(32768\ell^2))$ | Cook ER/unary-PHP shortcut after paid conservative gates; LSPV-1/453 gives an explicit strict-3 source compiler in a separate ER-FACET | No polynomial all-proof backtranslation to source Res(XOR); historical DEF/export grammar and full-$R$ transfer OPEN |
| Haken unary PHP | Standard variables $p_{i,h}$, pigeon axioms $\bigvee_h p_{i,h}$ and collision clauses $\neg p_{i,h}\vee\neg p_{j,h}$ | Haken 1985 exponential ordinary shared-DAG Resolution | Cook 1976 polynomial Extended Resolution proof | Equisatisfiable strict-3 conversion alone does not preserve a lower bound against mixed rules |
| Cubic odd Tseitin | Four proper width-three clauses per degree-three parity vertex | Exponential ordinary shared-DAG Resolution on suitable expanders | Historical AND3/XOR yields the declared $4h-1$ proof | Established family failure for full mixed hardness; retained as algebraic shortcut control |
| Authenticated bridge | 15 variables, 40 strict 3-clauses; unique 36-clause MUS | No published asymptotic hardness claim; certified finite UNSAT and bounded exact proof analysis only | Known 37-node historical proof: 28 AND3, 6 XOR, 2 LOCAL, 1 RES | Minimum remains 35..37; continuation after first cross RES is OPEN |

Certified UNSAT, certified proof-size hardness in a named system, and empirical solver difficulty are not conflated. No restricted theorem above is described as hardness against all algorithms.

## 8. Search, repository, and peer authentication ledger

Current project head at search time was `8dd0922a928bb8ebe8cc37730dec0f7748bb937a`; issue #3 page 11, the governing five-role handoff, original /341 grammar, LSPV-1/453, LSPV-3/456, Route-A peer reports, and actual Grok/Claude files were read. LSPV-1/453 authenticates the ER shortcut firewall for Braun bit-PHP. LSPV-3/456 authenticates the exact random proper strict-3 distribution and a restricted degree/exposure transfer; it explicitly leaves full historical LOCAL/DEF typing open.

Required repository heads were change-checked: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, FRAT-XOR `18cd6bc1...`, short-proof `2c524cfc...`, drat-trim `2e3b2dc...`, CNFgen `24e633bd...`, openai/math `4eaee875...`, and anthropics/formal-math `16a5ce41...`. Actual files reviewed included konard's complexity README and proof-status manifest, blkph0x's `METHOD_INDEX.md`, FRAT-XOR's `format.md`, and the OpenAI/Anthropic repository READMEs. None supplies a historical /341 checker, an accepted 35-node trace, a full mixed lower-bound transfer, or B3. FRAT-XOR authenticates a different proof language.

Primary indexed search checked Braun arXiv:2609.23015v2 and Pang arXiv:2610.00837v2, plus current bounded-depth and regular Res(XOR) results. Direct Google-branded search was unavailable; no claim of Google UI use is made. The scratch checkout remained partial, so the mandated local preflight reported missing root/skill files; complete current governing files were read through GitHub instead. No authoritative historical checker was located or executed.

## 9. Logical, evidence, machine, and failed-policy ledger

| Phase | Charged result |
|---|---|
| Primary logical enumeration | 2,252,194,390 side RES tests; 110,288 AND3 tests; 50 XOR tests; 33,489 condition-interface pairs; 4,056,196 cross RES pairs |
| Primary construction/verification | 37.450 s internal, 37.603 s shell wall; 422,992 KiB peak RSS |
| Independent reconstruction | Separate base-3 clauses and separately reconstructed truth vectors; exact count/support equality; 56.023 s internal, 56.168 s shell wall; 507,280 KiB peak RSS |
| Symbolic row control | 30 nonempty side sums and 225 cross pairs; 0.000536 s; 8,064 KiB peak RSS |
| Hostile controls | Nine independent count/support mutations and five symbolic row mutations rejected |
| Parsing/source/index/head reads | GitHub connector reads and indexed web searches performed; remote time and memory not exposed |
| Failed policy/restart | First timing wrapper failed because `/usr/bin/time` was absent; no mathematical output was accepted from that run; binaries were rerun with shell timing |
| Updating/conversion/output | Three source programs, three JSON evidence records, manifest, report, handoff, root fragment, exact issue outbox; byte sizes and SHA-256 values in manifest |
| All-phase simultaneous peak | 507,280 KiB among measured local phases; remote connector caches, publication service memory, and combined process peak unmeasured |

The closure materializes subset outcomes and clause catalogs. Its construction time, restarts, serialization, parsing, output, cache retention, and verification are implementation costs, not part of the ideal after-the-fact $W_R$ minimum. No same-machine FLMV exponent is inferred.

## 10. B3 verdict and precise remaining gap

This finite theorem neither compiles a uniform polynomial SAT decider into historical /341 proofs nor proves the decider's correctness inside the same system. Completeness, a verified checker, short proofs in another system, and efficient search conditional on short proofs do not imply B3. B1, B2, B3, superpolynomial $\overline W_{R_{\mathrm{mix341}}}$, and P versus NP remain **OPEN**.

**Actual advance:** every putative 35-node proof must use a first cross-cut strict Resolution, and all 4,056,196 possible first cross resolvents are too wide for direct AND3. At least one more strict Resolution is compulsory before the cross-cut affine block.

**Precise remaining finite gap:** starting from those source-authenticated first resolvents, construct or exclude every source-disjoint continuation containing one or more further strict Resolution steps and then an AND3 of combined support at most three. The optimizer must preserve child-source disjointness and exact record type; a generic clause closure would be unsound. After that, analyze the three 36-node topology classes.

**Precise remaining asymptotic gap:** transfer an established 3-CNF lower bound through every legal historical LOCAL/DEF/AND3/XOR/RES shortcut with polynomial encoded-size overhead, or give a legal counterexample, and independently establish a noncircular same-system B3 bridge.

## Artifacts

- `experiments/review/lspv5_391_cross_cut_interface.cpp`
- `experiments/review/lspv5_391_independent_verify.cpp`
- `experiments/review/lspv5_391_row_support_control.py`
- `results/raw/review/2026-11-06_1048_LSPV5_CROSS_CUT_INTERFACE391.json`
- `results/raw/review/2026-11-06_1048_LSPV5_CROSS_CUT_INTERFACE391_verification.json`
- `results/raw/review/2026-11-06_1048_LSPV5_ROW_SUPPORT391.json`
- `results/raw/review/2026-11-06_1048_LSPV5_CROSS_CUT_RESOLUTION391_manifest.json`
- `research/coordination/2026-11-06_1048_LSPV5_CROSS_CUT_RESOLUTION391_HANDOFF.md`
