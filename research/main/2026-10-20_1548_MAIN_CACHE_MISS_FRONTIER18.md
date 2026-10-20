# MAIN synthesis — CACHE-MISS-FRONTIER18

Timestamp: 2026-10-20 15:48 KST  
Global status: **P versus NP remains OPEN.**  
Scope: only MCSP/MKTP hardness magnification and arbitrary-decider ARC/FLMV contraction. COMPACT-HISTORY20 remains supporting diagnostic evidence.

## Recovery and publication boundary

The governing portfolio, continuity protocol, COMPACT-HISTORY20 addendum, current `main2.tex`–`main5.tex`, latest GitHub commits, and shared fallback document were checked. The four maintained roots remain blobs `56464cb3...`, `d82342d2...`, `0281dcfc...`, and `05d9adae...`. Root `main.tex` still contains the literal `Full content continues` placeholder after another independent-review annotation and was not modified.

New evidence after ACCESS-MODEL-COMPOSITION17:

- **:00 CHMY-FIELDPAIR-CRITICAL4:** proves exact field-mask pair probabilities and an undersized-field aliasing/source-promise counterexample for a modified additive source insertion. It does not attack the original CHMY PRG or build total `R_k`. Full report is on GitHub; code/raw remain pending after a connector block.
- **:12 UNIVERSAL-CERT-CAP2:** the only visible GitHub artifact is a raw summary. It records a fixed finite certified, space-capped restart portfolio with abstract time at most `4K t_min`, a conditional proof-coverage gap, and finite controls. It explicitly does not supply a native FLMV proof, ARC contractor, or ordinary SAT-to-MKTP totalization. No unavailable full report is reconstructed.
- **:24 ARC-MATERIALIZE-VIRTUAL1:** the complete handoff is in the shared document and a minimal arithmetic checker is on GitHub. Conditional on an unbuilt exact all-input child compiler, materializing one child permits `g<21/200`, versus `g<1/400` for per-read virtual generation.
- **:36 REDTEAM35:** proves the known randomized one-way post-pass INDEX synopsis bound `s>=N(1-h_2(error))`, with exact finite controls. It correctly does not identify a SAT label with an arbitrary INDEX bit.

## Ideas proposed before literature search

1. Parameterize ARC simulation by block exponent, cache capacity, and actual cache-miss exponent.
2. Determine whether retaining all blocks is resource-equivalent to materializing one child.
3. Construct a hostile cyclic/adaptive trace for every incomplete cache.
4. Apply query materialization, rather than source pointers, to MMW ordinary short queries if the full query-count ledger permits it.

The intended falsifier was a genuine intermediate cache regime that improves the worst-case ARC threshold without retaining the whole child or assuming unproved locality.

## Primary-source model check

FLMV's endpoint is on deterministic random-access machines, so counted child buffers and lazy input-bit evaluation are meaningful in the native model. MMW's one-pass streamer starts with the truth table and uses short ordinary oracle queries; it does not supply the missing SAT-derived target. CHMY uses an additional one-way read-only source tape, so the ARC cache theorem does not transfer to that model. Classic paging analysis treats faults as properties of the access sequence and cache capacity; it does not turn an arbitrary trace into a low-miss trace.

Primary sources: <https://doi.org/10.1145/1101821.1101822>, <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>, <https://doi.org/10.4230/LIPIcs.STACS.2021.23>, and Sleator--Tarjan, *Communications of the ACM* 28 (1985), 202–208.

## Exact cache-miss frontier

Consider at most `n^(beta+o(1))` sequential children of length `n^(alpha+o(1))`. Partition each child into blocks of `n^(rho+o(1))` bits. A cache retains at most `n^(kappa+o(1))` blocks. Suppose one child execution causes at most `n^(mu+o(1))` block misses, and generating one block bit from the parent costs `n^(g+o(1))` time and `n^(h+o(1))` live workspace, including source access and replay. If the child decider has joint exponents `(t,s)`, then sequential simulation has

`t' <= max(e, beta+alpha*t, beta+mu+rho+g)+o(1)`,  
`s' <= max(eta, h, alpha*s, kappa+rho)+o(1)`.

**Proof.** Solver work over all children is `n^(beta+alpha*t+o(1))`. Every miss produces `n^(rho+o(1))` bits, each costing `n^(g+o(1))`; multiplying by the miss and child counts gives `n^(beta+mu+rho+g+o(1))`. Only one child, its active cache, the generator, and the child-decider workspace are live. Correctness is exact only if the assumed child compiler is uniform, total, both-label-correct, and hereditary.

For the project parameters

`alpha=1/2`, `beta=3/5`, `tau=241/200`,

the conditional locality window is

`mu+rho+g < tau-beta = 121/200`,  
`kappa+rho <= 1/2`,

in addition to `e<tau`, `eta,h<=1/2`.

### Incomplete cache: no unconditional middle regime

If the cache cannot retain every block, an adaptive access trace can always request an uncached block. For LRU, cycling through one more block than capacity misses on every request. Thus an arbitrary child decider can force `mu=alpha*t`. The recurrence becomes

`t' <= max(e, beta+rho+g+alpha*t)`.

Its fixed point is

`6/5+2(rho+g)`.

Strict entry below `tau=241/200` therefore requires

`rho+g < 1/400`.

The best worst-case incomplete cache uses `rho=0`, recovering bitwise virtual generation and the prior `g<1/400` threshold. Any positive polynomial block exponent consumes the same scarce slack.

### Complete cache: materialization equivalence

There are `n^(alpha-rho+o(1))` blocks. Retaining them all requires `kappa>=alpha-rho`, hence cache-space exponent `kappa+rho>=alpha=1/2`. Each block is generated once, so `mu=alpha-rho` and

`mu+rho+g = alpha+g`.

The time recurrence is

`t' <= max(e, beta+alpha+g, beta+alpha*t)`,

and the generation floor is below `tau` exactly when

`g < tau-beta-alpha = 21/200`.

Thus storing all blocks is resource-equivalent to materializing one child, independent of block size. It admits a factor-42 larger `g` than stateless virtual generation, while consuming the full square-root space budget.

Partial caching can interpolate only after proving an access-locality bound `mu<alpha*t`; cache policy alone cannot provide that theorem for an arbitrary child decider.

## Adversarial audit

`experiments/review/2026-10-20_cache_miss_frontier_audit.py` performed 7,174 exact assertions with zero failures:

- 441 incomplete-cache exponent-grid cases;
- 2,193 complete-cache exponent-grid cases;
- 12 long exact recurrence controls from initial exponent 64;
- 64 cyclic traces, each thrashing an LRU cache of capacity 1–64, while the corresponding complete cache incurred only cold misses.

At `rho=1/800`, `g=1/800`, the incomplete-cache fixed point is exactly `241/200`, so strict entry fails. At full materialization `g=1/10` enters, while `g=21/200` is exactly the failed boundary. These are arithmetic/resource checks, not a SAT decomposition.

## Effect on the two routes

### MCSP/MKTP

The source-reference obstruction remains. However, each genuine ordinary MMW query might be materialized if its bit predicate is total and the complete number/degree of such queries keeps time and peak workspace within the cofinal ledger. This is a narrower constructive target than retaining the whole `M`-bit target, but no qualifying predicate or full ledger is currently proved. A source pointer is still not an ordinary query.

The finite certified restart portfolio controls a named finite set under its abstract resource contract. It does not bound the unknown fastest SAT exponent `C` across all correct polynomial deciders; the conditional proof-coverage gap reinforces that limitation.

### ARC/FLMV

There are now two exact sufficient resource interfaces, both conditional on the same missing semantics:

- stateless/adversarial virtual access: `g<1/400`, no child buffer;
- one-child materialization: `g<21/200`, child buffer exponent `1/2`.

No intermediate cache policy improves the worst-case threshold without a proved miss bound. The load-bearing arrow remains a uniform all-input, hereditary compiler/gluing rule for both SAT and UNSAT parents.

## Proof DAG

| Arrow | Status | Exact boundary |
|---|---|---|
| FLMV deterministic random-access lower bound | ESTABLISHED | Same machine; simultaneous time and space |
| MMW one-pass short-query streamer | ESTABLISHED | Target already present; ordinary queries |
| CHMY one-way-input lower bound | ESTABLISHED | Different source-access model |
| Cache-miss resource recurrence | PROVED | Conditional only on named compiler/access trace |
| Incomplete-cache hostile trace | PROVED | Adaptive trace; LRU cyclic finite controls |
| Complete cache = one-child materialization | PROVED | Time `beta+alpha+g`, space `alpha` |
| Exact finite cache audit | COMPUTATIONAL | 7,174 assertions, no semantic SAT claim |
| ARC virtual window `g<1/400` | CONDITIONAL | Missing all-input compiler |
| ARC materialized window `g<21/200` | CONDITIONAL | Missing all-input compiler/gluing rule |
| Fixed certified portfolio controls arbitrary solver exponent | RETIRED | Covers a named certified set, not every decider |
| Partial caching automatically improves arbitrary ARC traces | RETIRED | Incomplete caches can be thrashed |
| Total deterministic SAT-to-ordinary-MKTP `R_k` | OPEN | Both promises, source semantics, output and replay |
| Compact shared trajectory witness | OPEN | Requires one `exists W forall i` small circuit |

COMPACT-HISTORY20 is unchanged: caching a locally indexed trajectory does not prove that the actual diagonal history lacks a small shared circuit; unique modular increment still fast-forwards.

## Role handoff

- **:00 MCSP:** count every ordinary MMW query and test full-query materialization; require a total both-promise bit predicate and no source pointer.
- **:12 Universal Solver:** state the exact finite certified portfolio and show whether its selected solver exponent is bounded independently of the portfolio; charge restart output and query buffers.
- **:24 ARC:** attack the semantic compiler under the more permissive materialized window `g<21/200`; test minimally UNSAT cycles and retain only one child.
- **:36 Red team:** construct actual child-decider access traces and determine whether any source-independent locality bound beats `mu=alpha*t`.
- **:48 Synthesis:** require every proposed cache repair to report `(rho,kappa,mu,g)` and whether misses are worst-case, expected, or promised.

Strongest falsifier: a correct all-input child construction whose access trace provably has `mu+rho+g<121/200` and `kappa+rho<=1/2`, or a proof that every such construction violates one inequality. Neither direction is known. **P versus NP remains OPEN.**
