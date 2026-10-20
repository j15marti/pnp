# FIXED-PARAMETER-HARDWIRING22

**Status:** exact quantifier-order theorem and counterexample proved; arithmetic
audited; both P-versus-NP routes remain open.

## Recovered current state

This synthesis remains limited to the two active directions: MCSP/MKTP hardness
magnification and arbitrary-decider ARC contraction into the matched FLMV
endpoint.  COMPACT-HISTORY20 remains a supporting diagnostic.

Newest accessible peer artifacts were read directly:

* **MCSP :00 — SPARSE-TEMPLATE-NOGO5.**  Polylogarithmically sparse target
  strings have low ordinary KT by listing their exceptional positions.  The
  restricted lemma reports 4,751 checks, zero failures.  Dense, total,
  both-promise ordinary targets remain open.
* **Universal Solver :12 — UNIFORMITY BRIEF.**  For an already-present target,
  a growing parameter can make the MMW exponent approach one, but a hidden
  `2^(2^k)` constant invalidates the substitution
  `k=k(N)=ceil(sqrt(log_2 N))`.  The brief reports 608 checks, zero failures.
* **ARC :24 — ARC-BOUNDARY-ONEWAY-GLUE6.**  Two proper-3CNF pin blocks over a
  `b`-bit shared boundary are separately satisfiable and jointly satisfiable
  exactly when their boundary strings agree.  Every deterministic irrevocable
  left-first exact summary needs at least `b` bits.  The theorem is restricted
  to a one-way interface and does not apply to FLMV random-access rereads.
  Published controls report 134,188 checks, zero failures.
* **Red team :36.**  The newest accessible artifact remains the REDTEAM39 raw
  tableau/parity ledger; no newer exact theorem body was available at read time.

The shared fallback document was read; its last modification remained
2026-10-20 18:22 KST.  Root `main.tex` was fetched at blob
`47614403327a871005bc40f6bb704ad9e67069d3` and was not edited.

## Ideas proposed before literature search

1. **Fixed-parameter absorption.**  Choose a sufficiently large `k` only after
   fixing the hypothetical solver exponents, then keep `k` constant as input
   length tends to infinity.  Test whether arbitrary finite `k`-dependent
   constants disappear asymptotically.
2. **Variable-parameter counterexample.**  Test the same family after silently
   substituting `k(N)`; look for a constant family that becomes superpolynomial.
3. **Finite-depth ARC hardwiring.**  After fixing the hypothetical decider, use
   one finite recursion depth rather than a depth varying with input length.
4. **Boundary-information repair.**  Replace child SAT-status summaries by an
   explicit separator relation, but preserve the distinction between one-way
   memory and FLMV random access.

## Primary-source model check

* McKay--Murray--Williams (STOC 2019,
  DOI `10.1145/3313276.3316396`) supplies the short ordinary-query streaming
  consequence after the target is present.  It does not supply the SAT-derived
  target and does not license an uncontrolled variable auxiliary parameter.
* FLMV (JACM 2005, DOI `10.1145/1101821.1101822`) gives the eventual joint
  deterministic random-access time-space endpoint.  One-way separator-memory
  lower bounds do not automatically transfer to this model.
* CHMY (STACS 2021, DOI `10.4230/LIPIcs.STACS.2021.23`) remains a randomized
  one-work-tape theorem with an additional one-way read-only input tape.
* OPS (Theory of Computing 2021, DOI `10.4086/toc.2021.v017a011`) is nonuniform
  GapMCSP/MKtP magnification, not a standard-model SAT-to-MKTP reduction.
* Ilango (SIAM J. Comput. 2026, DOI `10.1137/24M1652568`) proves a reduction in
  a random-oracle setting; it does not furnish the required deterministic `R_k`.
* Hutter's fastest-program result ranges over programs with proofs of
  correctness and time bounds.  It neither extracts exponents for every correct
  polynomial decider nor resolves the present target-construction interface.
* Levin/Blum speedup and complexity-measure results do not alter the fixed-
  parameter asymptotic quantifier order proved below.  Easy-witness theorems do
  not create the missing compact witness for the special diagonal family.

## Theorem 22A: fixed-parameter constants are absorbable

Let `tau>a` and `sigma>0`.  Fix finite constants `C,D` and suppose that, for an
unbounded set `K` of **fixed integers** `k`, a correct composition has

```
T_k(N) <= A_k N^(a(1+(C+1)/k)+o_k(1)),
S_k(N) <= B_k N^(a max(1,D)/k+o_k(1)),
```

where `A_k,B_k` are arbitrary finite constants and each `o_k(1)` tends to zero
as `N` tends to infinity with `k` held fixed.

If some fixed `k in K` satisfies

```
a(1+(C+1)/k) < tau,
a max(1,D)/k < sigma,
```

then the same fixed composition satisfies

```
T_k(N) < N^tau,   S_k(N) < N^sigma
```

for all sufficiently large `N`.

### Proof

For the time bound, let `delta` be the positive exponent gap.  Because `k` is
fixed, eventually the `N^o_k(1)` term is at most `N^(delta/3)`.  The finite
constant `A_k` is at most `N^(delta/3)` for all sufficiently large `N`.
Multiplying leaves exponent at most `tau-delta/3<tau`.  The space proof is
identical.  No computable bound on the threshold input length is required for
the existential asymptotic contradiction.  QED.

At `a=6/5`, `tau=241/200`, and `sigma=1/2`, it suffices to choose a fixed

```
k > max(240(C+1), (12/5) max(1,D)).
```

This is exactly the quantifier order

```
fix solver -> obtain fixed C,D -> choose one fixed k -> let N tend to infinity.
```

It is not an algorithm that computes `k` from solver code, and it does not
conflict with EXPONENT-EXTRACTOR-FIREWALL21.

## Counterexample 22B: variable parameter substitution is invalid

For each fixed `k`, define

```
T_k(N) = 2^(2^k) N^r.
```

Then `T_k(N)=O_k(N^r)` for every fixed `k`.  However, on inputs with
`log_2 N=q^2`, set `k(N)=q`.  The hidden factor contributes exponent

```
log_N 2^(2^k) = 2^q/q^2,
```

which tends to infinity.  Therefore `T_{k(N)}(N)` is not bounded by any fixed
polynomial in `N`.

Consequently,

```
for every fixed k: O_k(N^r)
```

does **not** imply a uniform bound after replacing `k` by a growing `k(N)`.
Any variable-parameter construction must provide a single uniform machine and
explicit control of parameter-dependent constants, initialization, query
languages, and source access.

## Corollary 22C: finite ARC depth uses the same repair

Assume the still-open contractor is uniform, correct on every input,
hereditary, and preserves its jointly charged hypotheses under iteration.  For
one fixed hypothetical SAT decider with finite exponents `(t_0,s_0)`, iterate

```
t_(j+1) <= max(11/10, 3/5+t_j/2),
s_(j+1) <= max(1/2, s_j/2).
```

There exists a finite depth `r` with `t_r<241/200` and `s_r<=1/2`.  Fix that
`r` in the final machine.  Any finite product of level-dependent constants is
again one constant and is asymptotically absorbed.  No exponent extractor and
no input-dependent recursion depth are required.

This corollary remains conditional because the all-input semantic contractor
does not exist.  ARC-BOUNDARY-ONEWAY-GLUE6 supplies a useful separator warning,
not that contractor: its `b`-bit summary lower bound assumes irreversible
left-first processing, whereas FLMV permits random access.

## Exact audit

`experiments/review/2026-10-20_fixed_parameter_hardwiring_audit.py` uses exact
rational arithmetic and checks:

| Category | Assertions | Result |
|---|---:|---|
| Fixed-`k` exponent gaps for all `C,D=0..128` | 33,282 | zero failures |
| Absorption of `A_k=B_k=2^(2^k)` | 33,282 | zero failures |
| Variable-`k` counterexample controls | 129 | zero failures |
| Finite ARC entry for integer `t,s=1..64` | 4,096 | zero failures |
| **Total** | **70,789** | **zero failures** |

The largest ARC depth observed was 14.  The largest absorption threshold had a
30,985-bit binary logarithm—astronomical but finite.  This underscores the
difference between an asymptotic existence proof and a practical algorithm.

## Proof DAG and allocation

| Arrow | Status | Scope |
|---|---|---|
| Fixed-parameter constant absorption | **ESTABLISHED** | exact quantifier theorem |
| Variable `k(N)` from fixed-`k` big-O alone | **FALSIFIED/RETIRED** | explicit `2^(2^k)` counterexample |
| Fixed finite ARC depth absorbs constants | **CONDITIONAL** | requires missing hereditary contractor |
| MMW short-query downstream step | **ESTABLISHED source theorem** | target already present |
| Sparse/short-period MKTP targets | **RETIRED** | ordinary-KT upper bounds |
| One-way separator synopsis below `b` bits | **ESTABLISHED restricted** | not FLMV random access |
| Deterministic total ordinary `R_k` | **OPEN** | first MCSP/MKTP arrow |
| All-input hereditary ARC contractor | **OPEN** | first ARC/FLMV arrow |
| Special diagonal compact witness | **OPEN diagnostic** | not a third route |
| `P` versus `NP` | **OPEN** | no separation |

### Narrow next tests

* **:00 MCSP:** build one correct fixed-`k` dense target-bit predicate.  Report
  all `k`-dependent constants, but do not require a variable `k(N)` machine.
* **:12 Universal Solver:** formalize the single fixed solver/query language
  composition.  Retire variable-parameter and global-exponent-extractor work.
* **:24 ARC:** use explicit separator relations rather than child SAT labels;
  charge random-access rereads so the one-way lower bound is not misapplied.
* **:36 Red team:** attempt to break cofinal hardwiring by finding a
  `k`-dependent change in promise, language, correctness, or machine model—not
  merely a large finite constant.
* **:48 Synthesis:** accept only quantifiers in the order fixed above.

No task was added or reactivated.  `P` versus `NP` remains **OPEN**.

