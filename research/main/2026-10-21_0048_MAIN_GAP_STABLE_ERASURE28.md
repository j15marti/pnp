# GAP-STABLE-ERASURE28: a lossy global GapMCSP fiber that preserves, but does not descend, the threshold exponent

**Timestamp:** 2026-10-21 00:48 Asia/Seoul  
**Scope:** exactly two active directions: MCSP/MKTP hardness magnification and arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 is retained only as a supporting diagnostic.  
**Global status:** **P versus NP remains OPEN.**

## Executive result

The preceding two synthesis results imposed complementary constraints on a
deterministic MCSP threshold transform:

1. `INJECTIVE-THRESHOLD-BARRIER25` ruled out strict exponent descent by a
   near-linear injective encoding.
2. `QUERY-COVERAGE-FIBER27` showed that a deterministic source-bit transform
   whose zero execution leaves substantially more than
   `O(N^beta log N)` bits unseen has a mixed MCSP-label fiber.

This run supplies a positive control satisfying both necessary design
features—lossy and source-global—after changing the target to an explicit
additive promise gap. The construction is fixed-coordinate erasure.

Let `N=2^n`, let `U` be a fixed set of `u` truth-table coordinates, and define

```text
E_U(f)(x) = 0     if x is in U,
             f(x) otherwise.
```

Over a fixed finite fan-in-two Boolean basis, there is an explicit constant

```text
K = 2un + 1 = O(u log N)
```

such that

```text
|CC(f) - CC(E_U(f))| <= K.
```

Every output fiber has cardinality exactly `2^u` and circuit-complexity
diameter at most `2K`. Therefore

```text
CC(f) <= s       => CC(E_U(f)) <= s+K,
CC(f) > s+2K    => CC(E_U(f)) > s+K.
```

This is an exact reduction from an additive GapMCSP promise to ordinary MCSP
at the shifted threshold. It is not a cofinal threshold descent: if
`u=o(s/log N)`, then `s+K=(1+o(1))s`, so the exponent remains unchanged.
The result constructs the first explicit project example of a lossy,
full-scan, promise-label-monochromatic fiber, while also showing precisely why
that alone does not reach CHMY, MMW, OPS magnification, ARC, or FLMV.

## Recovered live state

The governing proof-portfolio and continuity files, COMPACT-HISTORY20
addendum, maintained `main2.tex` through `main5.tex`, newest GitHub commits,
latest complete peer reports/code/raw available through the repository, and
the shared Google Docs fallback log were checked. Since
`QUERY-COVERAGE-FIBER27`, no newer complete specialist scientific artifact was
visible in GitHub. The backup log still ends with:

- `CHMY-QUERYFRONTIER24`: an adjacent-pair nonlinear transform and exact
  distinguisher, but all-input YES preservation fails; the reported audit has
  3,284,449 checks and zero failures.
- `ARC-HEREDITARY-SCOPED10`: exact fixed-depth recursion on an already valid
  scoped promise with `w=o(log N)`, but the promise is itself directly easy;
  no arbitrary-input successor or universal contractor is supplied.

The latest repository change was a review annotation rather than a new
load-bearing proof body. Root `main.tex` remains outside the marker-safe path
and was not overwritten.

## Falsifiable repairs proposed before the source search

1. **Fixed-coordinate erasure:** deliberately accept lossiness, but read every
   source bit and quantify the exact complexity distortion of every collision.
2. **Additive-promise repair:** replace impossible exact-threshold fiber purity
   by a source promise gap wider than the fiber's complexity diameter.
3. **Stream-friendly coordinate family:** choose `U` as a suffix interval so
   the erasure can be implemented during one forward scan without a stored
   membership table.
4. **Exponent falsifier:** test whether the additive margin can ever reduce
   `N^beta` to `N^(beta-epsilon)`; the predicted answer is no because the map
   preserves the original circuit as a subcircuit up to an additive gadget.

The fourth prediction is confirmed exactly by the theorem below.

## Primary-source model check

- Cheraghchi--Hirahara--Myrisiotis--Yoshida, STACS 2021, proves randomized
  two-sided-error lower bounds for MCSP on a one-tape Turing machine with an
  additional one-way read-only input tape. A complete forward source scan is
  legal in that model; the present construction does not yield their required
  threshold descent. <https://doi.org/10.4230/LIPIcs.STACS.2021.23>
- McKay--Murray--Williams, STOC 2019, gives efficient compression/search-MCSP
  algorithms using small ordinary `Sigma_3-SAT` queries once the compression
  target is fixed. Fixed-coordinate erasure neither constructs the missing
  total SAT-to-MKTP map nor bounds the unknown polynomial exponent under
  `P=NP`. <https://doi.org/10.1145/3313276.3316396>
- Oliveira--Pich--Santhanam studies promise GapMCSP/GapMKtP and obtains
  magnification from model-matched lower bounds. The existence of a reduction
  into an MCSP threshold is not itself such a lower bound, and the present
  additive gap is not substituted for any of their stated parameter regimes.
  <https://doi.org/10.4086/toc.2021.v017a011>
- Fortnow--Lipton--van Melkebeek--Viglas concerns simultaneous deterministic
  random-access SAT time and space. A truth-table erasure with linear source
  and output traffic is not an all-input ARC successor.
  <https://doi.org/10.1145/1101821.1101822>

These source checks leave the theorem as a construction lemma only.

## Formal theorem

### Theorem 28A — circuit-complexity Lipschitz bound

Fix a finite fan-in-two Boolean basis containing Boolean negation,
conjunction, and disjunction; changing between standard fixed complete bases
affects only constants. Let `U` be a set of `u` inputs from `{0,1}^n`.
Then, for every Boolean function `f`,

```text
|CC(f) - CC(E_U(f))| <= 2un + 1.
```

**Proof.** For each `a` in `U`, equality with `a` is a conjunction of `n`
literals. It uses at most `n` negations and `n-1` conjunction gates. OR-ing
the `u` equality tests uses `u-1` further gates, so a membership indicator
`D_U` has size at most `2un-1`. The circuit
`f AND NOT D_U` computes `E_U(f)` with at most `2un+1` new gates.

Conversely, hardwire the set `U_f={a in U : f(a)=1}`. Its indicator has size
at most `2un-1`, and `E_U(f) OR D_{U_f}` reconstructs `f` with at most `2un`
new gates. Taking the larger bound proves the claim. QED.

### Corollary 28B — fiber diameter and additive promise transfer

If `E_U(f)=E_U(g)`, then `f` and `g` differ only on `U`, and Theorem 28A
applied through the common erased function gives

```text
|CC(f)-CC(g)| <= 2K,     K=2un+1.
```

Moreover, for every integer `s`,

```text
CC(f) <= s       => CC(E_U(f)) <= s+K,
CC(f) > s+2K    => CC(E_U(f)) > s+K.
```

The second implication is the contrapositive of
`CC(f)<=CC(E_U(f))+K`. Hence no fiber contains both a source-YES instance of
complexity at most `s` and a source-NO instance of complexity greater than
`s+2K`. The map is a promise-preserving many-one reduction from this additive
GapMCSP instance to ordinary MCSP at threshold `s+K`.

### Corollary 28C — stream and exponent ledger

Choose `U` as the final `u` coordinates in truth-table order. A deterministic
transducer reads all `N` source bits once, maintains an `O(log N)` position
counter, writes either the current bit or zero, and emits exactly `N` bits.
Its ledger is:

| item | charged value |
|---|---:|
| source accesses | `N` sequential reads |
| output | `N` sequential writes |
| time | `Theta(N)` |
| live workspace | `O(log N)` bits plus finite control |
| advice/source side table | none for suffix `U` |
| fiber size | exactly `2^u` |
| circuit distortion | at most `K=2un+1` each direction |

For `s=N^beta` and `u=N^alpha` with fixed `alpha<beta`,
`K=N^(alpha+o(1))=o(s)`. Thus the target threshold is
`s+K=N^(beta+o(1))`. The exponent is still `beta`; strict descent is absent.

## Reproducible audit

`experiments/review/2026-10-21_gap_stable_erasure28.py` performed **450,916**
assertions with **zero failures**:

- exact minimum circuit sizes for every Boolean function on one, two, and
  three variables over `{NOT,AND,OR,XOR}`;
- every coordinate set of size at most three in those universes;
- reconstruction identities, safe complexity distortion, additive YES/NO
  transfer, and exact `2^u` fiber cardinality;
- five suffix erasures over all `2^16` four-variable truth tables;
- 171 exact rational exponent comparisons.

The executable audit validates finite controls; the general theorem is the
symbolic construction and proof above.

## Adversarial challenge

1. **Exact-threshold failure:** without the additive promise gap, a fiber may
   contain functions on opposite sides of a threshold. That is expected and
   prevents use as an exact-MCSP descent.
2. **No exponent shrinkage:** `s+K` has the same exponent as `s` whenever the
   overhead is useful. Increasing `u` until `K` changes the exponent only
   worsens the target threshold.
3. **Hardwired-set cost:** an arbitrary `U` may require a stored membership
   description or expensive lookup. The stream implementation claim is made
   only for an explicitly simple suffix family.
4. **Full traffic is charged:** the construction reads and writes `N` bits.
   It evades the sparse-query barrier but gives no sublinear materialization
   or simultaneous SAT time-space improvement.
5. **No standard-model proof-of-work replacement:** the map supplies neither
   Ilango's missing deterministic standard-model soundness nor a total
   SAT-monochromatic semantic fiber.

The strongest falsifier for route value is already proved: the target
threshold exponent is invariant. Therefore this construction is retained as
a positive-control lemma and is not promoted to a load-bearing arrow.

## Two-route proof DAG

### Route 1 — MCSP/MKTP magnification

- **ESTABLISHED:** fixed-coordinate erasure is lossy, full-scan, has fibers of
  size `2^u`, and transfers an additive GapMCSP promise with distortion
  `O(u log N)`.
- **ESTABLISHED barrier:** injective near-linear strict descent fails; sparse
  deterministic zero-path fibers mix labels.
- **CONDITIONAL:** under `P=NP`, the MMW machinery may replace its small SAT
  queries by a polynomial algorithm, but the fixed exponent `C` remains
  uncontrolled for the proposed parameter schedule.
- **OPEN:** deterministic standard-model charged totalization `R_k`; ordinary
  KT/MKTP both-promise preservation without an `M`-bit side table; cofinal
  vanishing parameters with `p_k` at least logarithmic in target length;
  exact simultaneous streaming/materialization costs; a route from those
  resources to a matched lower-bound endpoint.
- **RETIRED:** use of fixed-coordinate erasure itself as strict threshold
  descent.

### Route 2 — ARC into FLMV

- **ESTABLISHED algebra:** if a jointly charged all-input hereditary successor
  existed with the recorded recurrences, iteration would approach the
  conditional fixed point near `(6/5,1/2)`.
- **COMPUTATIONAL:** scoped fixed-depth recursions pass finite tests on their
  promise class.
- **OPEN weakest arrow:** from an arbitrary polynomial-time SAT decider to a
  total all-input successor, charging source acquisition, construction,
  selection, replay, output, and maximum simultaneously live bits in the
  FLMV random-access model.
- **RETIRED:** treating a directly easy scoped promise as that universal
  successor; importing truth-table erasure as an ARC contractor.

### COMPACT-HISTORY20 supporting diagnostic

- **CONDITIONAL:** the earlier diagonal implication works if the specified
  self-padded YES instances have one satisfying-assignment circuit `W` of
  size `tau(n)^o(1)` with quantifiers `exists W forall i`.
- **OPEN:** that single-circuit premise.
- **ESTABLISHED non-implications:** `forall i exists W_i`, exact `t` oracle
  queries for arbitrary iteration, and `Omega(t)` gates for histories of some
  truth-table-described functions do not imply the premise for explicit
  succinct transitions; modular increment remains a fast-forward control.

## Allocation

- **:00 MCSP:** try to compose a lossy full-scan promise-pure map with a
  source-matched strict threshold descent; report both promise directions and
  reject any composition that silently becomes injective or sparse-query.
- **:12 Universal Solver:** state the fastest-correct portfolio quantifiers and
  prove or refute a uniform, input-length-independent bound on the MMW
  exponent `C`; machine-specific constants do not suffice.
- **:24 ARC:** construct one arbitrary-input successor with a complete
  acquisition/replay/output/live-space ledger in the deterministic
  random-access model, or give a minimal counterexample to heredity.
- **:36 Red team:** search for an exact-MCSP boundary fiber, basis-conversion
  omission, or off-by-one error; separately challenge the suffix-stream
  implementation and its output charge.
- **:48 Synthesis:** retain GAP-STABLE-ERASURE28 only as a benchmark for
  collision accounting and promise width. Continue allocating primary effort
  to the deterministic totalization interface and the all-input ARC
  successor.

No unrestricted separation follows. **P versus NP remains OPEN.**
