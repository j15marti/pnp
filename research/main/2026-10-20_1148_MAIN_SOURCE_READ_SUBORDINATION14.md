# MAIN synthesis — SOURCE-READ-SUBORDINATION14

Timestamp: 2026-10-20 11:48 KST  
Global status: **P versus NP remains OPEN.**  
Scope: only MCSP/MKTP magnification and arbitrary-decider ARC/FLMV contraction. COMPACT-HISTORY20 remains diagnostic support.

## Recovered evidence

Governance, continuity, COMPACT-HISTORY20, `main2.tex`–`main5.tex`, current GitHub artifacts, and the shared fallback document were read. The newest complete scientific material is REDTEAM31/32:

- REDTEAM31 proves a restricted source-dependent-advice bound with a factor `Bq` only when one of `B` advice values is revealed without charging its acquisition.
- REDTEAM32 correctly requires every preprocessing and later named-source read to be charged. Its finite summary reports 350 policies, 1,050 seed cases, 29,400 sparse runs, 350 exact TV identities, and zero failures.
- REDTEAM32 also gives an explicit fast-forwardable trajectory whose endpoint has zero gates while the full indexed trajectory has exactly `n` gates. This reinforces that endpoint simplicity, full-history complexity, and runtime are distinct.
- No newer complete :00/:12/:24 body was visible. The fallback document ends at REDTEAM29, so GitHub is the current source of REDTEAM31/32.
- Root `main.tex` is still unsafe: current blob `7022882d7a8df0cd8672ea7b603780b6a932f14f` contains a literal truncation marker. It was not modified.

## Ideas proposed before literature search

1. **Endogenous-advice collapse.** If advice is computed only from charged source reads, couple the complete pipeline until its first differing read; the free-advice alphabet factor `B` should disappear.
2. **Output-dominates-read-tax.** Translate the sparse-source access lower bound into the target-length exponent ledger. A one-pass or sublinear-probe lower bound may be entirely hidden beneath the unavoidable `M` output writes.
3. **Retention, not reading, as the sharp separator.** Full source or target retention has space exponent at least one and immediately misses the FLMV space target, even though a full scan has only time exponent one.
4. **Replay threshold.** Require red-team attacks to prove sufficiently many reads or passes to cross the strict time boundary, not merely `Omega(N/k)` source probes.

## Primary-source check

MMW's actual streamer reads successive truth-table blocks, issues short `Sigma_3 SAT` queries, and accounts total time and workspace; it does not forbid a charged source scan. <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>. CHMY concerns randomized one-way input with one work tape, so the named-random-access coupling here is not a transfer into CHMY. <https://doi.org/10.4230/LIPIcs.STACS.2021.23>. OPS remains a separate nonuniform GapMCSP/GapMKTP magnification theorem. <https://doi.org/10.4086/toc.2021.v017a011>. FLMV's endpoint is deterministic random-access SAT and explicitly depends on simultaneous time and space. <https://doi.org/10.1145/1101821.1101822>.

## Lemma A — charged endogenous advice has no alphabet multiplier

Let a randomized adaptive pipeline interact with an `N`-bit source only by named-coordinate reads. Its preprocessing may compute arbitrary advice, and later stages may branch on that advice, but all advice is a deterministic function of the independent coins and previously read answers. Couple a run on `0^N` with a run on a uniformly random `k`-sparse source using the same coins. Let `Q(R)` be the set of coordinates read during the **entire zero-source execution**, across preprocessing, advice construction, target generation, replay, and decoding, and put `u(R)=|Q(R)|`. Then

`TV(Transcript_0, Transcript_sparse) <= E_R[1-C(N-u(R),k)/C(N,k)] <= k E_R[u(R)]/N`.

Proof: until the sparse support intersects a queried coordinate, both executions have identical state, hence identical endogenous advice and identical next query. Therefore divergence implies that the support intersects the single realized zero path `Q(R)`. Condition on `R`, take the exact hypergeometric hit probability, then average. The union over all possible advice values is unnecessary because unrealized advice branches cannot be reached before a differing source answer. The final inequality is the union bound. QED.

The `Bq` bound remains correct for **free source-conditioned advice**. Lemma A says that once advice acquisition is implemented inside the machine, its reads join one execution-wide budget and `B` disappears.

## Lemma B — output/read/retention exponent ledger

Assume the conditional ordinary-MKTP target has length `M=N^(a+o(1))`, threshold `p=M^(1/kappa+o(1))`, and is emitted online. Let:

- total named-source reads have cost `N^(r+o(1))`;
- retained source-dependent storage be `N^(z+o(1))` bits;
- other generation overhead be time `M p^(B+o(1))`, space `p^(E+o(1))`;
- under `P=NP`, the one fixed MMW short-query solver use time `L^C`, space `L^D`.

Then the same-machine composition has

`t = max(r, a(1+max(B,C+1)/kappa))`,

`s = max(z, a max(E,1,D)/kappa)`.

This includes the unavoidable `Omega(M)` output time. Consequently, any unit-cost sparse-source access bound `Omega(N/(wk))` has exponent at most one in `N` and is subordinate to output whenever `a>=1`. It cannot by itself force `g_k>1` in the output-normalized ledger or falsify the target box.

At `a=6/5`, `tau=241/200`, `sigma=1/2`:

- one full source scan (`r=1`) is harmless;
- even total read exponent `r=6/5` remains strictly below `tau`;
- `r>=241/200` fails the strict time bound;
- retaining `N^(1/2)` bits fails the strict space bound;
- full source or full target retention fails immediately.

Thus the current source-query results are useful accounting firewalls but not the load-bearing obstruction. A viable falsifier must establish either `r>=241/200`, `z>=1/2`, an `M`-scale rewind/side table, loss of total ordinary-MKTP semantics, or excessive output-normalized overhead `B/kappa>=1/240`.

## Reproducible adversarial test

`experiments/review/2026-10-20_source_read_subordination_audit.py` exhausts every two-stage one-bit endogenous-advice policy at `N=7,k=2`, directly computes transcript TV, and checks it against the single charged zero-path set. It also checks the combined exponent identities over a broad exact-rational grid, boundary retention/read profiles, and all rational sparse/word exponents with denominator at most 64. The raw JSON preserves all failures.

## Proof DAG

| Arrow | Status | Current meaning |
|---|---|---|
| MMW short-query one-pass streamer | ESTABLISHED, model-specific | Downstream component only |
| CHMY one-tape threshold magnification | ESTABLISHED, restricted model | No deterministic ordinary-MKTP transport |
| OPS GapMCSP/GapMKTP magnification | ESTABLISHED, nonuniform models | Separate route/model |
| Ilango SAT hardness | ESTABLISHED with random oracle | Standard deterministic replacement OPEN |
| Endogenous-advice coupling, Lemma A | PROVED in named-coordinate model | No `B` multiplier after acquisition is charged |
| Output/read/retention ledger, Lemma B | PROVED conditional interface | Shows existing read taxes are subordinate |
| Charged deterministic totalization `R_k` | OPEN | Weakest MCSP arrow |
| Total ordinary MKTP semantics without `M`-bit table/replay | OPEN | Weakest implementation interface |
| All-input hereditary ARC successor | OPEN | Weakest ARC arrow |
| Matched FLMV contradiction | CONDITIONAL | Requires one preceding route to close |
| Compact shared `W` for the actual diagonal family | OPEN | Must be one `W` for all indices; fast-forward escapes survive |
| Named-read lower bound alone as P-vs-NP separator | RETIRED | Subordinate to target output at `a>=1` |

## Narrow handoff

- **:00 MCSP:** stop optimizing named-source probe lower bounds unless they force retention/replay; produce one explicit total target generator and its `(r,z,B,E)` ledger.
- **:12 Universal Solver:** test whether MMW can consume the generator with `z<1/2` and no rewind; keep one fixed query-solver exponent pair `(C,D)`.
- **:24 ARC:** state acquisition and retained state separately for every child; a scan is not fatal, `N^(1/2)` retained state is.
- **:36 Red team:** try to force `r>=241/200`, `z>=1/2`, or `B/kappa>=1/240`; do not report `Omega(N/k)` alone as a route obstruction.
- **:48 Synthesis:** preserve two-route and model boundaries; Compact History remains diagnostic.

Strongest falsifier: exhibit an unavoidable full table/replay or prove that every total ordinary-MKTP generator crosses one of the three strict thresholds above. None is presently proved. **P versus NP remains OPEN.**
