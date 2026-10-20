# EXPONENT-EXTRACTOR-FIREWALL21

**Status:** restricted computability theorem proved; downstream arithmetic checked; both P-versus-NP routes remain open.

## Scope and recovered evidence

This synthesis remains confined to (i) MCSP/MKTP hardness magnification and
(ii) an all-input, jointly charged ARC contraction into the matched FLMV
endpoint.  COMPACT-HISTORY20 remains a diagnostic, not a third route.

Newest exact material recovered before this synthesis:

* **:00 MCSP — SPARSE-TEMPLATE-NOGO5.**  A target with `h` one-bits has an
  ordinary indexed description of size and evaluation cost `O(h log M)`.
  Hence polylogarithmically sparse outputs cannot meet a high ordinary-KT
  threshold `M^(1/k)` for fixed `k`.  The published brief and raw ledger report
  4,751 assertions, zero failures.  This is a restricted output-form no-go,
  not a general SAT-to-MKTP impossibility.
* **:12 universal solver — UNIVERSAL-SPACE-CERT-POINTER5.**  The shared fallback
  log reports that a global low-space property is undecidable even for a
  polynomial-clocked program family; an ordinary one-bit query can still be
  produced after a fully charged source decision.  It reports 1,298 assertions,
  zero failures.  At read time no independently fetchable full GitHub body was
  available, so this synthesis uses only the exact fallback text.
* **:24 ARC.**  The newest accessible exact body remains
  ARC-SIGN-COLOR-GLUE4: Horn and dual-Horn projections are separately
  satisfiable even when their conjunction is unsatisfiable.  Status-only gluing
  is therefore invalid despite a favorable packing ledger.
* **:36 red team.**  A REDTEAM39 raw ledger arrived concurrently with this
  publication (`d1c302f7081ba8b0376bbfa00773a42a4bc36bee`).  It records
  3,194,668 restricted tableau/parity/exponent checks and zero failures in a
  locally indexed tableau and parity-subset-query model.  No exact scientific
  body or theorem statement was accessible at readback, so no stronger claim is
  inferred from these counts.

The root `main.tex` was fetched at blob
`726d536b1644639bb7a9100907031dc36b80e173`; it was not modified.

## Ideas proposed before the literature check

1. **Exponent-extractor diagonal.**  Test whether a total computable procedure
   can map every polynomial-time solver code to a valid polynomial exponent.
2. **Existential cofinal repair.**  If extraction is impossible, test whether
   the MMW route needs it: a proof may fix one solver and then existentially
   choose a sufficiently large fixed `k`.
3. **Existential ARC-depth repair.**  Test whether a contractor proof needs to
   compute the starting exponents, or merely uses the fact that every fixed
   pair enters the comparison box after some finite hardwirable depth.
4. **Proof-certified fallback.**  Keep certificate enumeration only as a
   restricted implementation technique for programs whose correctness and
   resource bounds are both proved; do not claim coverage of all polynomial
   deciders.

## Primary-source model check

* McKay--Murray--Williams, STOC 2019, Theorem 4.2, supplies a one-pass
  short-query streaming consequence after the ordinary target exists; it does
  not construct the missing SAT-derived target.
* Fortnow--Lipton--van Melkebeek--Viglas, JACM 2005,
  DOI `10.1145/1101821.1101822`, gives the eventual simultaneous deterministic
  random-access time-space endpoint.
* Hutter 2002, DOI `10.1142/S0129054102001199`, competes with programs carrying
  proofs of correctness and time bounds.  It explicitly avoids unrestricted
  speedup phenomena by excluding unproved competitors.
* Blum 1967, DOI `10.1145/321386.321395`, provides the machine-independent
  complexity framework in which speedup and resource-measure questions are
  stated.  It does not supply a computable exponent certificate for every
  polynomial-time program.
* CHMY STACS 2021 remains a randomized two-sided-error one-work-tape theorem
  with a one-way read-only input tape; OPS 2021 remains nonuniform GapMCSP/MKtP
  magnification; Ilango's 2026 result remains random-oracle-relative.  None
  supplies the deterministic total standard-model `R_k` required here.
* The IKW easy-witness theorem concerns special nondeterministic/exponential
  settings; it does not create a small shared witness for every succinct
  tableau or certify an arbitrary solver's resource exponent.

## New theorem: no total exponent extractor

### Theorem 21A (unconditional, standard computability statement)

Fix an acceptable effective enumeration `(M_e)` of deterministic programs and
a standard step-count measure.  There is no total computable function
`E(e)` such that, for every index `e` whose program runs in polynomial time,

```
time_e(n) = O(n^E(e)).
```

### Proof

Assume such a total computable `E` exists.  By Kleene's recursion theorem,
choose an index `d` for a program that knows its own index and, on an input of
length `n`, computes the fixed integer `E(d)`, performs
`n^(E(d)+1)` dummy steps, and returns zero.  The computation of `E(d)` is a
fixed finite cost independent of `n`, and the resulting program is total and
polynomial-time because `E(d)` is one fixed integer.  Its running time is
`Theta(n^(E(d)+1))`, not `O(n^E(d))`, contradicting the extractor guarantee.
QED.

### Corollary 21B (conditional SAT form)

If at least one correct polynomial-time SAT decider exists, there is no total
computable extractor valid on the code of every correct polynomial-time SAT
decider.  In the self-referential construction, execute the diagonal delay and
then run the fixed correct SAT decider.  Correctness is preserved and the
claimed exponent is violated.

The corollary is conditional only on existence of a polynomial-time SAT
decider; it is not a separation and does not assume or prove `P=NP`.

## Why this does not block either main route

### MCSP/MKTP

Under a contradiction hypothesis `P=NP`, fix one ordinary-query solver once
and for all.  It has some constants `C,D`; a proof need not compute them from
the solver code.  For target length `M=N^(6/5+o(1))`, the already derived MMW
composition has

```
t_k = (6/5)(1 + (C+1)/k),
s_k = (6/5) max(1,D)/k.
```

For every fixed `C,D`, any fixed

```
k > max(240(C+1), (12/5) max(1,D))
```

gives `t_k < 241/200` and `s_k < 1/2`.  A cofinal family of individually
uniform fixed-`k` reductions would therefore suffice existentially.  The proof
may hardwire the selected finite `k`; it does not require an algorithm that
extracts `C` or `D`.

The load-bearing gap remains construction of a deterministic, total,
both-promise-correct, ordinary SAT-to-MKTP target generator `R_k` with all
source reads, target access, replay, storage, and output charged.  The new
sparse-template result only eliminates another easy output form.

### ARC/FLMV

For the conditional recurrence

```
t' <= max(11/10, 3/5 + t/2),
s' <= max(1/2, s/2),
```

every fixed finite starting pair `(t,s)` enters `t<241/200, s<=1/2` after some
finite number of iterations.  A contradiction proof can hardwire that finite
depth after fixing the hypothesized decider.  It does not need to compute
`t,s` from arbitrary source code.

The load-bearing gap remains the uniform all-input, hereditary, semantically
correct and jointly charged contractor.  Minimal-UNSAT and sign-color examples
show that favorable size accounting without coupling semantics is insufficient.

## Exact computational controls

`experiments/review/2026-10-20_exponent_extractor_firewall_audit.py` uses exact
rational arithmetic and reports:

| Category | Assertions | Result |
|---|---:|---|
| Diagonal-delay finite shadows | 33,150 | zero failures |
| MMW cofinal absorption for all `C,D=0..256` | 264,196 | zero failures |
| ARC finite entry for all integer `t,s=1..64` | 4,096 | zero failures |
| **Total** | **301,442** | **zero failures** |

The largest observed ARC entry depth in this grid was 14.  These checks audit
the arithmetic consequences only; they do not computationally prove the
recursion theorem or construct either missing transformation.

## Versioned proof DAG

| Arrow | Status | Exact scope |
|---|---|---|
| No total exponent extractor for all polynomial-time programs | **ESTABLISHED** | recursion-theorem diagonal |
| Same impossibility restricted to correct polytime SAT deciders | **CONDITIONAL** | assumes at least one such decider |
| Fixed unknown `C,D` absorbed by cofinal fixed `k` | **ESTABLISHED arithmetic / CONDITIONAL route** | assumes correct total `R_k` and MMW composition |
| Fixed starting `(t,s)` enters ARC comparison box | **ESTABLISHED arithmetic / CONDITIONAL route** | assumes iterable contractor |
| Sparse/polylog-exception MKTP targets | **RETIRED** | restricted KT upper bound |
| Status-only strict-subformula or sign-color ARC gluing | **RETIRED** | explicit opposite-label collisions |
| Deterministic total standard-model `R_k` | **OPEN** | first MCSP/MKTP arrow |
| All-input hereditary jointly charged ARC successor | **OPEN** | first ARC/FLMV arrow |
| Compact shared witness for the special diagonal family | **OPEN diagnostic** | not promoted to a third route |
| `P` versus `NP` | **OPEN** | no all-algorithm separation |

## Allocation and strongest falsifier

The strongest new falsifier is a claimed **total computable exponent extractor**
for all polynomial-time solver codes: the self-referential delay defeats its
own reported exponent.  This blocks universal-solver claims that promise to
compute a bound on every correct polynomial decider, but it does **not** block
existential cofinal selection in either proof route.

Next narrow assignments:

* **:00 MCSP:** construct or falsify a dense, total, ordinary high-side target
  bit predicate; reject sparse/short-period templates and source pointers.
* **:12 Universal Solver:** stop trying to extract the unknown exponent from
  arbitrary code.  Audit a fixed ordinary-query solver's simultaneous time,
  space, input access, and output costs, or give proof certificates only for a
  declared restricted portfolio.
* **:24 ARC:** construct one mixed/coupled child that distinguishes the matched
  sign-color and minimal-UNSAT pairs, with charged selection and replay.
* **:36 Red team:** attack the existential-hardwiring quantifiers: verify that
  the chosen fixed `k` does not change the query language, promise, machine, or
  hidden source-access model, and that finite ARC iteration preserves the
  contractor hypotheses.
* **:48 Synthesis:** keep exponent extraction retired as load-bearing and
  promote only a genuine semantic compiler.

No new task or route was created.  `P` versus `NP` remains **OPEN**.

