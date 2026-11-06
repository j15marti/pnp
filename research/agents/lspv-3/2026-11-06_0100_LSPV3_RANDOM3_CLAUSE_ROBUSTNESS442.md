# LSPV-3/442: Established hard random strict-3-CNF with linear source-deletion resilience

**2026-11-06 01:00 PST, America/Los_Angeles. Route B.** **PROVED/EXACT:** elementary all-size deletion-robustness lemma. **KNOWN THEOREM:** Chvátal–Szemerédi ordinary DAG Resolution lower bound. **UNREFEREED PREPRINT THEOREM:** Pang unrestricted DAG Res(PC_r/F_p), including Res(XOR). **COMPUTATIONAL:** finite verified sources. Historical mixed-system Wbar_R, B3, and P versus NP **OPEN**. Five existing allocations, titles, schedules, inference weights and roles unchanged.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** published random strict-3-CNF hard instances may have *no individually indispensable original source clauses*, making the all-source-ancestry `m-1` lower-bound method inapplicable without undermining their restricted proof hardness. Falsifiers: (1) paper requires different density/distribution; (2) assignment/deletion quantifiers are invalid; (3) finite UNSAT controls are SAT/malformed or source-unbound; (4) the asserted Res(XOR) theorem is only regular, tree-like, or uses extension axioms.

**Actual searches and source audits:** Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), actual full HTML Theorems 1.1 and 7.2(a) and Section 7.1; Chvátal–Szemerédi, JACM 35(4):759–768 (1988), DOI 10.1145/48014.48016. Project `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob c87acd11), /436, /440, /441, governing five-role handoff (blob c3889a3e), current issue #3, `AGENTS.md`, `CODEX.md`, pnp-research skill; Grok `GROKPROOF/2026-11-06_0515_PROGRESS.md` (blob 93f9202d) and actual Claude TPORT/ONETAPE README files (blobs d1290822 and 6255025f). NEW repositories actually reviewed: `konard/p-vs-np/proofs/attempts/COMMON_ERRORS.md` (3de91bc4) and `proofs/experiments/np_subset_p_proof_attempt.md` (f07e4821); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (18d693ea) and `PROOF_PORTFOLIO_BRIDGE_REPORT.md` (22215cec). Also read FRAT-XOR `format.md` (986a21aa), CakeML LPR `README.md` (e94f45e9), peitl/short-proof `README.md` (93d2090d), and searched OpenAI math. No historical native DEF facet/LOCAL port was authenticated by these sources. Web search used; no Google-branded search claimed.

## Exact established family/theorem/encoding ledger

For n>=3 sample m=8n clauses independently uniformly among the 8 binom(n,3) signed proper width-three clauses. Across-clause repetitions are permitted, indices retained. There are n original variables; no gadget reduction is needed. Standard explicit decimal DIMACS source has B=O(n log(n+2)) bits.

**KNOWN, 1988 peer-reviewed:** Chvátal–Szemerédi show exponential *ordinary unrestricted shared-DAG Resolution* proof length with probability 1-o(1) when random k-clause density c obeys k>=3 and c2^-k>=0.7. Here k=3 and c=8, so 8/8>=0.7.

**NEWER PREPRINT, not independently refereed:** Pang 2026 Theorem 7.2(a) states exp(Omega_{p,r}(n)) DAG proof size for this distribution in Res(PC_r/F_p), fixed p prime and integer r>=1; p=2,r=1 is Res(XOR). Theorem 1.1 assumes PC has no degree-D refutation and D>=max{32(p-1)^2 r,8w}; it yields ln(S)>=D/(32p^2r)*(D/(16n))^((p-1)r). This is *not* a theorem about paid auxiliary Boolean definitions or historical R_mix341, and complete independent checking of the new preprint is still pending.

Shortcut controls: Haken PHP's Cook/Buss ER/Frege polynomial proofs, cubic odd Tseitin's /341 native AND3/GF(2) O(n) proof, and bit-PHP's /441 conditional full GATE-LOCAL Cook proof. These must not be excluded to protect a lower bound. The 1988 and 2026 statements count proof nodes in specified systems, not SAT-machine runtime.

## New all-size lemma and proof (PROVED/EXACT)

Let b_F(a) be the number of **indexed original clauses** falsified by complete assignment a, and d(F)=min_a b_F(a). If d(F)>k, deletion of ANY set of at most k clause indices keeps F UNSAT: each assignment still falsifies at least one undeleted clause. This remains true when two source indices have identical clauses.

For any fixed assignment of the independent-uniform random family, b_F(a) is Bin(8n,1/8). Chernoff and the union bound over all 2^n assignments give

$$
\Pr[d(F)\le n/10]\le
2^n\exp[-8n D_{\mathrm{KL}}(1/80\Vert1/8)]
=\exp[-\gamma n],
$$

where

$$
D_{\mathrm{KL}}(u\Vert v)=u\ln(u/v)+(1-u)\ln[(1-u)/(1-v)],
\qquad \gamma=8D_{\mathrm{KL}}(1/80\Vert1/8)-\ln2
=0.03211993244018\ldots>0.
$$

Thus with probability at least 1-exp(-gamma*n), deletion of **ANY <=floor(n/10) indexed source clauses** preserves UNSAT. In particular no individual source is indispensable with probability 1-o(1). The intersection with an independently established 1-o(1) hard-proof event still has probability 1-o(1); hence robust and Resolution-hard strict-3-CNFs coexist for arbitrarily large n. Conditional on the correctness of Pang's preprint theorem, this also holds for his stated Res(XOR) lower bound.

**Transfer consequence:** The `m-1` original-source-essentiality fan-in-2 argument in /341 and /440 cannot be invoked on these hard random formulas because its premise fails. This does not make them easy, disprove the earlier conditional lemma, or prove full-mixed-system hardness. Restricted exp(Omega(n)) size with source B=O(n log n) implies exp(Omega(B/log(B+2))) along a corresponding growing encoded sequence, *within that restricted proof system only*.

## Independent finite original-source controls

Deterministic xorshift32 fixture generator, sampled proper three-variable clauses and separately checked DIMACS SHA-256. This finite PRNG is a **diagnostic control**, not the exact uniform distribution used for the theorem. The local independent Python checker reconstructs the same sources, computes full assignment histograms with independently written literal truth evaluation and verifies hashes. Planted-zero SAT and malformed/corrupt controls are included.

| n | seed | clauses | min falsified | minimizers | SAT? | ALL deletion subsets certified |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 10 | 113 | 80 | 3 | 3 | no | up to 2, 3,241 subsets |
| 12 | 36 | 96 | **5** | **5** | no | up to 4, **3,469,497 subsets** |
| 14 | 131 | 112 | 2 | 1 | no | up to 1, 113 subsets |
| 16 | 131 | 128 | 3 | 2 | no | up to 2, 8,257 subsets |
| 12 | 777, planted zero | 96 | 0 | 1 | yes | none |

Independent Python replay: **91,136 assignment evaluations PASS**; all five source hashes matched; one polarity mutation detected. Full local JavaScript parser rejected four malformed inputs. The 4,096 assignments for n=12 seed=36 establish min falsified=5, thereby certifying all 3,469,497 deletion subsets of size <=4 *without testing each deletion separately*. They do **not** establish any finite Res(XOR) or mixed-calculus proof-size minimum.

Logical verification explicitly charges O(2^n 8n) clause inspections; source reads, generation, hashing, parsed/constructed records, histogram storage and process memory are nonzero. Observed Linux host Node 0.16 sec/31,680 KiB peak RSS and independent Python 5.64 sec/95,652 KiB; no FLMV time-space exponent inferred. Machine-readable GitHub summary and complete local archive retain original source hashes and raw histograms. Full source-certificate checking is computational only, not an authenticated historical R_mix341 proof.

## Scope, novelty firewall, publication blocker

Earlier /341 and /440 correctly establish `m-1` bounds for **indispensable** sources in their specified settings; the new family violates that hypothesis. This is a negative control against extending a source-count bound to general hard random SAT, not a contradiction of those results. No empirical solver runtime claim is made. Historical LOCAL-CONVERT input/output, private/exported ports, paid DEF facet selectors and the full grammar of R_mix341 remain unauthenticated; no hidden branching/discharge rule was introduced. Arbitrary shared mixed DAGs and B3 remain OPEN.

Root `main.tex` was fetched but returned blob SHA `d5ba222bb4ba731a81feb5bcd5aade91644254bc` and **zero readable bytes**. To preserve all outside-owned bytes, no root edit was attempted. No other role's manuscript or task was modified.

**Next substantive task:** test the *actual strongest* AND3/GF(2)/paid-DEF/LOCAL shortcuts and shared reconvergent branching chains on this published strict-3 family, rather than relying on universal source indispensability. This run does not prove P versus NP.

**Primary references:** [1] Chvátal and Szemerédi (1988), DOI 10.1145/48014.48016. [2] Pang (2026), arXiv:2610.00837v2, https://arxiv.org/html/2610.00837v2. [3] Braun (2026), arXiv:2609.23015, wide bit-PHP, not an automatic strict3 lower-bound transfer.
