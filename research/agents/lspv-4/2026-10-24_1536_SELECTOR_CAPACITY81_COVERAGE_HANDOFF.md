# SELECTOR-CAPACITY-BIT-LEDGER81 | LSPV-4 cumulative coverage and gap handoff
Research timestamp: 2026-10-24 15:36 Asia/Seoul. **P versus NP remains OPEN.** No automation/task changes and no messages to third parties.

## Exact new both-label hostile control

For M>=8 use one **fixed** proper 3CNF parent P_M: the eight signed ternaries on a common three-variable triple plus M-8 distinct positive ternaries on disjoint fresh triples. Full parent is UNSAT. For any K-subset S of clause indices, retain exactly those clauses in sorted order, with original variable IDs and same n=3+3(M-8) header. Put r=|S intersect {0,...,7}|. The exact child model count is
`(8-r)*7^(K-r)*8^((M-8)-(K-r))`.
Hence child UNSAT iff all eight core clauses are selected. For K<8, **every** short child is SAT while the parent is UNSAT. For K>=8, exactly binomial(M-8,K-8) children are UNSAT; all others SAT, with identical length for any two K-children. This is PROVED/EXACT for this source family, independently reviewable.

## Exact service-separation lemma, with duplication caution

A fixed deterministic stateless decoder given fixed P_M, charged descriptor d_S and query bit i, with no other S-dependent advice, must assign different descriptor strings to all binomial(M,K) distinct ordinary children. Consequently a fixed-length descriptor needs
`D >= ceil(log2 binomial(M,K)) >= K*log2(M/K)`.
Colex rank attains first information bound (unranking need not be polylog); explicit sorted K-index array costs K*ceil(log2 M) bits and locally fetches any ordinary child bit in polylog time and O(log N) scratch. At K=Theta(N^.5/log N), every full-universe descriptor needs Theta(N^.5) bits.

**Duplication:** This entropy and index-array lemma was already stated in research/main/2026-10-22_1048_MAIN_SELECTOR_VIRTUAL_CHILD62.md (blob c3303e3d3ac57ea484e1018a7d27dc59c0f07d09). Do not promote it as a newly discovered theorem. This run's addition is the same-parent SAT/UNSAT witness control, exact model counts, bit-level service comparison and charged decision-only bypass.

The child SAT label is instead computable from streamed indices with an eight-flag mask, O(K log M) bit work and O(log M) writable bits. No full child or descriptor is needed. This is a **restricted family upper bound**, not an all-input SAT result. A fixed codebook of Q selectors also escapes the all-subsets entropy premise, but its construction/storage and possible nonuniform advice must be charged.

## Bit-resource and conditional ARC ledger

Use w(n,m)=ceil(log2(64(n+m+1))), full source N=(4M+2)w(n,M), ordinary child L=(4K+2)w(n,K). Primitive bit work counts reads, comparisons, addressing, control, all writes including unchanged-value writes. Independently count actual complete-state bit flips, source/workspace reads and writes, peak live writable bits, cumulative bit-time and representation/program size. An eager L-bit serializer writes all L bits, but actual blank-to-output flips equal the output's one-bit count. A lazy virtual evaluator may legally avoid this buffer.

**Conditional only:** if an all-input semantically correct ARC parent procedure generates Q=N^(3/5+o(1)) sequential K-index children of length L=N^(1/2+o(1)), with charged selector acquisition, parent glue, failures and read-only source, then the explicit index-array implementation has
`t' <= max(r, 1.1, 0.6+t/2)`, `s' <= max(eta,kappa,0.5,s/2)`.
r is parent local time exponent, eta scratch, kappa ancestors and caches, and (t,s) are simultaneous exponents for ONE ordinary-child solver in the matched model. The 1.1 term is an upper bound for explicit fresh descriptor writes, not a universal lower bound for correlated/adaptive selectors. No all-input SAT child-generation/gluing theorem was produced.

## Adaptive-state controls

Initial state: source pointer, n,M,K and a selector stream, label unknown. Charge source and selector acquisition. If only a status bit is requested, switch to an eight-bit mask. If ordinary child bits are requested, switch to index-array virtual fetch, combinatorial rank decoding, or eager serialization, with regeneration, cache, address work and bit-time charged. Both SAT and UNSAT controls occur for same n,M,K. Horn, affine/XOR, SCC 2SAT, padded 2SAT, independent components, direct-source decisions and altered representations remain legitimate hostile shortcuts. This finite menu is not a claim about all SAT algorithms.

## Verified computational record

Complete local standard-library auditor `selector_capacity81_audit.py`: 273719 assertion-accounted checks, 129030 exact ordinary child-bit comparisons, 0 failures, five exhaustive selector families M=10/16 and K=7/8/9, independent brute-counts for all M=10 selections. Script SHA256 0881bc1602224a102c91b2af06cca02cd4eaef81004d6a058b13ca82dbdaa6a6; raw JSON SHA256 f00daa10ef294fe744e7dc59920d5b9b12d753c21f867645827a28b7c78fba8a. GitHub mini reproducer and results summary are separate published artifacts; full code/raw are in this run's user-accessible package, not implicitly shared across agent runtimes.

GitHub report: research/agents/lspv-4/2026-10-24_1536_LSPV-4_SELECTOR_CAPACITY_BIT_LEDGER81.tex
GitHub mini: research/agents/lspv-4/2026-10-24_1536_SELECTOR_CAPACITY81_MINI.py
GitHub summary: research/agents/lspv-4/2026-10-24_1536_SELECTOR_CAPACITY81_RESULTS_SUMMARY.json

## Cumulative coverage and source fidelity

Inherited baseline, **not rerun**: commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640, 3532 prose/source/config files SHA-verified and keyword searched, selective proof-body review.

Full textual source bodies retrieved in this run: main13.tex, AGENTS.md, CODEX.md, repository pnp research skill, SELECTOR-VIRTUAL-CHILD62, VIRTUAL-CHILD-COMPOSITION61 handoff, CACHE-MISS-FRONTIER18 handoff, current Role 1 ARC-CHANNEL-CURVE119 handoff, Role 3 FORBIDDEN-COMPUTATION84 handoff, Role 5 WRITE-SHADOW-ENDPOINT118 handoff. Source report mathematical sections inspected: Role 2 FLMV-CURVE-FRONTIER115, Role 4 SENSITIVITY-SATURATION80, Role 5 WRITE-SHADOW-ENDPOINT118, CP22LIFT1 (prior retrieval). Root main.tex blob fd8858769196417295e34b7761fef4772f5e86d2 was read by targeted head and owned sections, not line-by-line all ~293k characters. Drive ARC proof ancestor (id 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0, revision retrieved) supplied 221 paragraphs, with introductory mathematical sections inspected, not line-by-line entire document. Primary FLMV author PDF Corollary 5.8 on visual page 18 inspected and model checked. No paginated full Drive folder search was attempted in this run.

GitHub queries: CACHE-MISS-FRONTIER18, VIRTUAL-CHILD-COMPOSITION61, EAGER-LAZY-FRONTIER34, selector descriptor, PC22_ALLFIELD1, TRANSFER1, BIT-TIME, WRITE-SHADOW-ENDPOINT118, role1/2/3 latest. These are **bounded targeted matches**, not evidence of archive exhaustion. The earlier 3532-file crawl and metadata inventory are inherited; no new completeness claim.

Unread queue: exact full HEREDITARY-SCOPED10 generator/code, historical main2-main12 theorem-by-theorem, remaining Drive LOG/PROVED_EXACT/BOOL/SIL pages with nonnull continuation tokens, code/data of several older cited proof bodies, full primary CP22/PC22 independent script reruns, and peer-local full audit outputs. Do not infer absence from failed/bounded search.

## Gap-to-evidence table

| Gap | Exact status | Reason |
| --- | --- | --- |
| FLMV matched forbidden region | FILLED, KNOWN THEOREM | JACM 2005 Corollary 5.8 and strict transfer |
| Cofinal finite-hit conditional logic | FILLED, conditional meta-implication | Does not construct route |
| Arbitrary K-subset descriptor lower/upper | PROVED/EXACT restricted, PREVIOUSLY KNOWN | SELECTOR-VIRTUAL-CHILD62 |
| Same-parent both-label short-child model count | PROVED/EXACT restricted, this report | Core eight signed clauses, disjoint fillers |
| Descriptor entropy forces child decision work | FALSIFIED/RETIRED | Eight-mask stream recognizes label cheaply |
| Satisfiability of every short deletion child reconstructs parent SAT | FALSIFIED/RETIRED | K<8 all SAT children, UNSAT parent |
| Eager/lazy child-bit resource interface | PARTIAL/RESTRICTED | Exact virtual service but no semantic gluing |
| All-input favorable charged ARC achievable-pair edge | OPEN | No source supplies matched parent-label join plus resource contraction |

## Next artifact and peer obligations

Role 5: independently check the model-count identity, descriptor injectivity quantifier, SAME_REALIZATION bit/space clauses, and ensure root synthesis does not elevate restriction. Roles 1-3: use this source as a same-parent, both-label test for any recovered contraction or potential. Next inspect original HEREDITARY-SCOPED10 executable body and construct an all-input high-width test measuring selector discovery, number of children, exact ordinary child-bit service, combined labels, peak ancestor/cache space, and BIT-RESOURCE1 event vector. The all-decider favorable ARC edge remains OPEN.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::SELECTOR-CAPACITY-BIT-LEDGER81 -->
