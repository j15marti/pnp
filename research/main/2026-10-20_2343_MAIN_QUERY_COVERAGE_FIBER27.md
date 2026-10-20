# QUERY-COVERAGE-FIBER27: sparse deterministic source access cannot produce MCSP-label-pure fibers

**Timestamp:** 2026-10-20 23:43 Asia/Seoul  
**Scope:** exactly two active routes: MCSP/MKTP hardness magnification and arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 remains a supporting diagnostic.  
**Global status:** **P versus NP remains OPEN.**

## Executive result

This run proves an exact deterministic source-query barrier and composes it
with `INJECTIVE-THRESHOLD-BARRIER25`.

Let `LOW_beta(N)` be the set of `N=2^n`-bit truth tables having ordinary
fan-in-two circuit size at most `s=N^beta`, for fixed `0<beta<1`. Let `R` be
any deterministic oracle transducer that receives a truth table through
individual source-bit queries and emits an arbitrary output. On the all-zero
source, suppose `R` queries `q` distinct source positions in total. If

```text
N - q > log2 |LOW_beta(N)|,
```

then the output fiber containing zero is mixed-label: it also contains a
source outside `LOW_beta(N)`. Standard circuit counting gives

```text
log2 |LOW_beta(N)| = O(N^beta log N),
```

so an all-input MCSP-label-monochromatic output fiber containing zero requires

```text
q >= N - O(N^beta log N).
```

This is a semantic/query-coverage lower bound, not a one-tape time lower bound.
A complete one-way scan queries all `N` positions and escapes the theorem.
Randomized reductions and non-bit global primitives are also outside its
scope.

Combined with the preceding injective barrier, strict deterministic threshold
descent must be both:

1. **lossy**—an injective near-linear map cannot preserve the YES threshold;
2. **nearly source-global** on the zero path—or else its lossy fiber contains
   both an easy and a hard source.

No current construction satisfies these requirements while also meeting the
CHMY/MMW machine, promise, and resource ledgers.

## Recovered state

The governing portfolio, continuity protocol, COMPACT-HISTORY20 addendum,
`main2.tex` through `main5.tex`, newest GitHub commits, newest complete peer
bodies, code/raw when accessible, and the shared Google Docs fallback log were
read. The maintained root blobs remain:

| file | Git blob |
|---|---|
| `main2.tex` | `56464cb3d6bf9fc0b853287d1917d03bcf329ce3` |
| `main3.tex` | `d82342d236feb2dcaadd03c8ae4c47a02d639137` |
| `main4.tex` | `0281dcfc8833a031f2c5967a05ab7fdd8423640f` |
| `main5.tex` | `05d9adae357b2970437130c3673fa2cc27e155e0` |

The newest substantive peer artifact is
`CHMY-SPECTRAL-PHASE26` at commit
`efec20ce523c602fd46a43e5ae98713abbd8c4da`. It gives an exact family

```text
f_h(x,y) = x·y XOR h(y)
```

with opposite MCSP labels but identical complete Walsh magnitudes, full
autocorrelation, weight, signed-value histogram, and algebraic degree under
the stated constraints. In its restricted feature-query model, recovering
enough spectral phase requires `(1-o(1))*sqrt(N)` distinct phase locations.
The GitHub commit contains the complete theorem body, but no executable or raw
ledger was accessible in the repository during this synthesis; its claimed
78,281 finite assertions were therefore not independently rerun here.

The latest ARC handoff remains `ARC-HEREDITARY-SCOPED10`: fixed-depth
iteration is exact for already-valid scoped streams with `w=o(log N)`, but
the promise class is directly solvable in near-linear time and subpolynomial
space. No newer complete all-input ARC body was visible. Root `main.tex` has
again received independent review annotations and remains outside the
marker-safe synthesis path; it was not modified.

## Falsifiable repairs proposed before literature

1. Replace feature-specific attacks by a generic deterministic decision-tree
   theorem based only on the number of distinct source positions exposed on
   the easy-source path.
2. Compose it with the injective barrier to obtain the **lossy-and-global
   dichotomy** for strict threshold descent.
3. Treat a full one-way source scan as a legitimate escape and charge it
   explicitly, rather than misreporting the semantic theorem as a CHMY tape
   lower bound.
4. Transfer only the indistinguishability lesson to ARC: sparse clause-status
   or child-selection transcripts require a separate semantic gluing proof;
   they do not become an all-input contractor by analogy.

## Primary-source model audit

- **CHMY, STACS 2021, Theorem 16/Corollary 23:** randomized two-sided-error
  MCSP lower bounds for a one-tape Turing machine with an additional one-way
  read-only input tape, plus a stated oracle-query extension. This permits a
  complete forward scan and does not turn the new coverage theorem into a
  one-tape lower bound. DOI: <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
- **MMW, STOC 2019:** the one-pass search-MCSP consequence begins with an
  already specified compression target and uses ordinary short
  `Sigma_3 SAT` queries. It does not construct the missing total
  SAT-to-MKTP transducer. DOI: <https://doi.org/10.1145/3313276.3316396>.
- **OPS, ToC 2021:** hardness magnification concerns promise Gap-MCSP/Gap-MKtP
  and nonuniform circuit conclusions across sufficiently small parameters;
  it is not an ordinary SAT reduction or FLMV endpoint.
  DOI: <https://doi.org/10.4086/toc.2021.v017a011>.
- **Ilango, SICOMP 2026:** SAT hardness is obtained relative to a uniformly
  random oracle; it is not the deterministic standard-model `R_k` needed here.
  DOI: <https://doi.org/10.1137/24M1652568>.
- **FLMV, JACM 2005:** the endpoint is simultaneous time-space for
  deterministic random-access SAT machines. A semantic source quotient must
  first be implemented and charged in that same model.
  DOI: <https://doi.org/10.1145/1101821.1101822>.
- **Hutter/Levin/Blum:** proof-certified or witness-verifiable universal search
  does not uniformly extract the unknown exponent of every correct polynomial
  SAT decider. The prior fixed-parameter hardwiring repair remains the proper
  conditional treatment.
- **Easy witness:** the IKW theorem derives easy witnesses under circuit
  upper-bound hypotheses; it does not prove COMPACT-HISTORY20's source-specific
  `exists W forall i` compactness premise.

No theorem from these sources supplies a label-monochromatic lossy fiber.

## Formal claim card

**Claim ID:** `QUERY-COVERAGE-FIBER27`  
**Status:** ESTABLISHED deterministic source-bit query theorem; project
consequence is a no-go for sparse deterministic semantic fibers.  
**Input:** an `N=2^n`-bit Boolean truth table.  
**Low label:** ordinary circuit complexity at most `s=N^beta` over a fixed
finite fan-in-two basis.  
**Machine:** deterministic adaptive oracle transducer whose only source access
is an individual truth-table-bit query; output length and computation time are
unrestricted.  
**Resource:** number of distinct source coordinates queried on the zero-source
execution path.  
**Falsifier:** such a transducer with a label-monochromatic zero fiber and
`N-q` strictly larger than the logarithm of the number of low-complexity
functions.  
**Excluded:** randomized per-input correctness, non-bit global queries, advice
containing source information, and a full source scan.

## Theorem and proof

### Theorem 27A — exact fiber-capacity bound

Let `L` be any subset of `{0,1}^N` containing the zero string. Let `R` be a
deterministic adaptive source-bit oracle transducer. On source `0^N`, let `Q`
be the set of distinct queried coordinates and `q=|Q|`. If

```text
2^(N-q) > |L|,
```

then there exists `x notin L` with `R(x)=R(0^N)`.

**Proof.** Every source `x` that is zero on all coordinates in `Q` gives the
same answer at each adaptive query as `0^N`. Induction on the query number
shows that the transducer follows the identical path and emits the identical
output. There are exactly `2^(N-q)` such sources. If this exceeds `|L|`, one
lies outside `L`. QED.

### Corollary 27B — MCSP coverage floor

For circuits of size at most `s` on `n=log2 N` inputs over a fixed basis, a
generous description count is

```text
|LOW_s| <= (s+1)(n+s)[B(n+s)^2]^s,
```

where `B` is the constant number of gate types. Hence

```text
log2 |LOW_s| = O(s log(n+s)).
```

With `s=N^beta`, every deterministic output fiber containing `0^N` that is
monochromatic for MCSP at threshold `N^beta` must query

```text
q >= N - O(N^beta log N)
```

distinct positions on the zero path.

### Composite dichotomy with Barrier25

For near-linear target length and a strict target-threshold descent:

- an **injective** map fails source-YES preservation by
  `INJECTIVE-THRESHOLD-BARRIER25`;
- a **lossy deterministic source-bit** map whose zero path leaves more than
  `O(N^beta log N)` positions unseen has a mixed-label zero fiber by this run.

Thus reversible mixing and sparse lossy signatures are both retired. The
remaining deterministic design space is a lossy construction that covers
nearly the entire source and proves that every relevant collision is
label-monochromatic. This is necessary, not sufficient.

## Adversarial challenge and limits

The theorem does **not** forbid a forward scan of all `N` input bits. CHMY's
machine has exactly such a one-way read-only source, so a legal transform can
escape the coverage bound while still failing for other reasons. It also does
not rule out a randomized transform: `forall x Pr_seed[success]>=2/3` does not
provide one seed correct on all inputs. Nor does it handle a primitive that
returns a global function of the source at unit cost; such a primitive must be
specified and charged separately.

`CHMY-SPECTRAL-PHASE26` fits the theorem's broader lesson but is not subsumed
as a bit-query result: a signed Walsh coefficient is a global feature. Its
explicit matched-label construction shows that even rich global summaries can
lose the decisive phase information. Together the two results eliminate both
sparse local signatures and the current absolute-spectrum candidate, but they
do not prove that every lossy quotient fails.

For ARC, the analogous `MINIMAL-UNSAT-PROJECTION20` family already shows that
strict-subformula SAT-status transcripts can be identical on opposite-label
parents. A correct contractor must carry coupling/boundary information or pay
separately charged semantic work. No all-input successor is constructed here.

## Reproducible audit

`experiments/review/2026-10-20_query_coverage_fiber27.py` performs:

- exact rational exponent-gap checks for 19 threshold exponents;
- explicit fan-in-two circuit-description counts through `n=160` for five
  representative thresholds;
- exhaustive pigeonhole verification across 3,154 small abstract low-label
  families;
- 3,298 deterministic adaptive policies with exhaustive compatible sources.

Result: **339,759 assertions, zero failures**. The first implementation was
killed because it attempted to materialize the doubly enormous integer
`2^u`; the corrected audit compares the exact exponents, which is the actual
mathematical test. A second finite-control revision replaced an invalid
first-success monotonicity assumption with a last-failure record to accommodate
floor effects. Neither implementation issue changes the symbolic theorem.

## Two-route proof DAG

| Status | Arrow/result |
|---|---|
| **ESTABLISHED** | CHMY, MMW, OPS, Ilango-random-oracle, IKW, and FLMV only in their stated models; injective threshold barrier; deterministic query-coverage fiber theorem; spectral-phase mixed-fiber family; restricted scoped ARC semantics. |
| **COMPUTATIONAL** | This audit: 339,759 checks, zero failures. Spectral peer reports 78,281 assertions but its executable/raw files were not accessible for independent rerun. |
| **CONDITIONAL** | `SAT -> charged deterministic totalization R_k -> ordinary MKTP/KT at p_k=M^(1/k+o(1)) -> MMW under P=NP with fixed unknown C -> simultaneous SAT DTISP -> FLMV`; scoped ARC recurrence on promised streams. |
| **OPEN** | Deterministic standard-model replacement for Ilango; a lossy nearly-global label-monochromatic fiber; vanishing parameter with `p_k>=log M`; no-table totalization; deterministic replay; all-input ARC acquisition/high-width successor; exact same-machine output ledger; COMPACT-HISTORY20's `exists W forall i` size premise. |
| **RETIRED** | Injective/reversible strict descent; sparse deterministic source signatures; absolute Walsh spectrum/autocorrelation quotient; fixed-threshold CHMY as cofinal descent; universal exponent extraction; status-only strict-subformula ARC; compact history or finite tests as unrestricted runtime lower bounds. |

## Role-targeted next tests

- **:00 MCSP:** Construct one deterministic lossy map whose zero-source path
  reads all but `O(N^beta log N)` bits. State the exact collision invariant
  and try to produce a mixed-label completion before invoking CHMY.
- **:12 Universal Solver:** Given that candidate, audit whether canonical
  fiber-representative selection or certification hides an `N`-bit table,
  random rereads, advice, or a solver-dependent exponent. Do not attempt
  universal exponent extraction.
- **:24 ARC:** Test one all-input child generator on the minimal-UNSAT family,
  charging source reads, coupling constraints, emitted bits, replay, live
  width, and output in the random-access model.
- **:36 Red team:** Extend the matched-transcript attack to randomized seeds
  without swapping quantifiers, or exhibit a concrete nearly-global lossy map
  that escapes both Barrier25 and this theorem.
- **:48 Synthesis:** Promote an MCSP step only with an explicit
  label-monochromatic-fiber proof, and promote ARC only with an all-input
  jointly charged successor. Otherwise retain both arrows as OPEN.

No schedule, duplicate task, or third route was created. Root `main.tex` was
not modified. **P versus NP remains OPEN.**

<!-- END_VERIFIED_QUERY_COVERAGE_FIBER27 -->
