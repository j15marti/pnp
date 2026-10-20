# CERTIFIED-PADDING-QUOTIENT30

**Timestamp:** 2026-10-21 02:48 Asia/Seoul  
**Scope:** exactly two active directions: MCSP/MKTP hardness magnification and arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 is diagnostic only.  
**Global status:** **P versus NP remains OPEN.**

## 1. Recovered state and publication safety

The governing proof-portfolio file, continuity protocol, the user-specified
COMPACT-HISTORY20 addendum at commit `c4e1f72f10976405fa2479c88499894d3d58633f`,
current `main2.tex` through `main5.tex`, recent commits, and the shared fallback
Google Doc were read.  The maintained root blobs remain:

- `main2.tex`: `56464cb3d6bf9fc0b853287d1917d03bcf329ce3`
- `main3.tex`: `d82342d236feb2dcaadd03c8ae4c47a02d639137`
- `main4.tex`: `0281dcfc8833a031f2c5967a05ab7fdd8423640f`
- `main5.tex`: `05d9adae357b2970437130c3673fa2cc27e155e0`

Root `main.tex` is blob `24825a0154a2a67ae5b575e10440863cbbf414e2`
after more independent-review annotations.  It was not modified.  No newer
complete two-route specialist publication was visible after
`LOW-SIDE-ORBIT-COLLAPSE29`; the shared Doc still ends with the blocked
`ARC-HEREDITARY-SCOPED10` handoff.  Commit
`c00f6467a358db814f3b9d67c34a42956e2b4fb7` proves a bounded-universal-bit QBF
unrolling result.  It is retained only as compact-witness comparison, not as a
third active route.

The named 13-page and four-page compact-witness PDFs were not discoverable as
repository files.  This run therefore used the verified governance addendum
and the repository formal audit, and did not reconstruct absent PDF text.

## 2. Falsifiable proposals made before literature search

1. **Certified-padding canonicalizer.** Normalize every payload sign in one
   forward scan.  Falsifier: two members of one promised same-label orbit have
   different canonical outputs, or the SAT and UNSAT canonical cores collide.
2. **High-side survival test.** Bound ordinary indexed KT of both canonical
   targets.  Falsifier: both become MKTP-YES at the desired polynomial
   threshold.
3. **Checksum-retaining quotient.** Retain one semantic checksum while erasing
   payload.  Falsifier: construct opposite-label cores with the same checksum.
4. **ARC local-normalization analogue.** Normalize only locally certified
   replay segments.  Falsifier: the transformation has no strict size shrink,
   is not all-input, or its acquisition/transcript cost breaks the recurrence.

This run builds and falsifies the first proposal as a route-level bridge via
the second test.

## 3. Primary-source model check

- MMW STOC 2019 distinguishes `MKtP` (`c+log t`) from ordinary indexed
  `MKTP` (`c+t`).  Its Theorem 4.2 requires `p(N)>=log N` and gives an ordinary
  MKTP streamer in `O(Np)` time and `O(p)` space with `Sigma_3 SAT` queries of
  length `O(p)`: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- CHMY STACS 2021 works with a one-way read-only input tape and one two-way
  read/write work tape; its Corollary 23 charges oracle query length in the PRG
  seed: <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
- OPS 2021 concerns promise Gap-MKtP/Gap-MCSP in nonuniform circuit models, not
  a transfer theorem for this streaming canonicalizer:
  <https://doi.org/10.4086/toc.2021.v017a011>.
- FLMV JACM 2005 uses deterministic random-access Turing machines with read-only
  input and one-way write-only output excluded from work space.  Theorem 3.1
  supplies the local SAT transfer; Corollary 5.8 has forbidden exponent
  `d=( (c+2)/c^2 - c )/2`, equal to `23/45` at `c=6/5`:
  <https://lance.fortnow.com/papers/files/tst.pdf>.
- The easy-witness theorem assumes an NP circuit upper bound and produces a
  polynomial-size witness circuit; it does not establish the
  `tau(n)^o(1)` premise required by COMPACT-HISTORY20:
  <https://people.csail.mit.edu/rrw/easy-witness-nqp.pdf>.
- Ilango's SAT/MCSP evidence is explicitly a random-oracle result, not the
  missing deterministic standard-model bridge:
  <https://doi.org/10.1137/24M1652568>.

## 4. Exact theorem: a canonical quotient exists but destroys the high side

### Theorem 30 (certified-padding quotient and polynomial-threshold failure)

For every integer `r>=0` there are equal-length proper-3CNF families
`O_SAT(r)={F_SAT(r,z):z in {0,1}^r}` and
`O_UNSAT(r)={F_UNSAT(r,z):z in {0,1}^r}` and a deterministic promised-domain
transducer `Q_r` with all of the following properties.

1. Every member of `O_SAT(r)` is satisfiable and every member of
   `O_UNSAT(r)` is unsatisfiable.
2. `Q_r` maps each of the `2^r` members of a fixed-label orbit to one canonical
   representative, while the two label representatives remain distinct.
3. In the fixed-width clause-record encoding used by the audit, `Q_r` reads and
   writes every record exactly once, uses no source rereads, uses `O(log r)`
   working bits plus one literal record, and has linear record/bit time.
4. Each of the two canonical-output families has ordinary indexed KT
   `polylog(M)`, where `M` is target length.  Consequently, for every fixed
   `k`, a threshold `p=M^(1/k+o(1))` eventually accepts **both** canonical
   outputs.  Thus `Q_r` is not a SAT-to-MKTP reduction despite satisfying the
   selected orbit-collapse and opposite-label-separation tests.

### Construction and proof

The SAT core consists of two copies of the four clauses
`(x1, +/-x2, +/-x3)`, so `x1=1` satisfies it.  The UNSAT core contains all
eight sign patterns on `x1,x2,x3`; every assignment falsifies exactly one of
them.  For each payload bit `z_i`, add a clause

`(a_i, b_i, (-1)^(z_i) c_i)`

on three fresh variables.  Setting every `a_i=1` satisfies all payload
clauses, so the payload cannot change the core label.  The promised
canonicalizer replaces the third literal by positive `c_i`.  This proves the
first three items directly.

For the fourth item, hardwire the one-bit core selector and `r` in a program.
Given an index, arithmetic on the fixed-width header and clause number outputs
the indexed canonical bit in `polylog(M)` time using a `polylog(M)`-bit
description.  Under ordinary KT the description length and index-output time
are added.  A fixed positive power `M^(1/k+o(1))` dominates this polylogarithm,
so both label templates are low-KT.  Distinct output strings are therefore not
enough; the target labels, not target identities, must separate.

## 5. Reproducible audit and adversarial challenge

`experiments/review/2026-10-21_certified_padding_quotient30.py` checked
`r=0..12`:

- 16,382 generated formulas;
- 16,382 proper-3CNF checks;
- 16,408 orbit-collapse assertions;
- 13 SAT/UNSAT canonical-target separation checks;
- 39 fixed-length checks;
- 62 independent brute-force truth checks for all orbit members at `r<=4`;
- zero failures.

Strongest falsifier: this exact positive canonicalizer defeats any claim that
same-label orbit collapse plus distinct opposite-label targets is sufficient.
Both outputs are explicit, locally indexable templates and hence land on the
same low-KT side at every fixed-power threshold.  A surviving construction
must prove a target **complexity gap**, not merely a quotient or a collision
avoidance property.

The transducer is deliberately promised-domain.  It validates no arbitrary
CNF, provides no standard-model replacement for Ilango, and does not solve
conditional-to-total conversion.  Its output length is unchanged (`lambda=1`),
so it provides no ARC contraction.  Extending it to arbitrary inputs without
semantic SAT work is OPEN.

## 6. COMPACT-HISTORY20 diagnostic

The canonical targets are another explicit-syntax fast-forward control.  An
exponentially large padding orbit can have a single `polylog(M)`-KT canonical
template.  This agrees with the modular-increment firewall: black-box orbit or
history cardinality does not force high KT or a large time-indexed witness for
an explicit transition.  The load-bearing compact-history premise remains one
circuit with quantifiers `exists W forall i` and size `tau(n)^o(1)` on the
specified diagonal sources.  This theorem supplies no such circuit and no
lower bound against one.

## 7. Versioned two-route proof DAG

### Route I: MCSP/MKTP

- **ESTABLISHED:** MMW Theorem 4.2 ordinary-MKTP streaming parameters and CHMY
  one-tape lower bounds in their published models.
- **ESTABLISHED:** cofinal fixed-`k` hardwiring can absorb a single solver
  exponent after that solver is fixed.
- **PROVED, restricted control:** a certified syntactic quotient can collapse
  an entire padding orbit in one pass.
- **FALSIFIED:** orbit collapse plus opposite-label output inequality suffices
  for a SAT-to-MKTP reduction.
- **OPEN, weakest arrow:** a deterministic all-input, both-label SAT-to-ordinary-
  MKTP totalization with threshold `p=M^(1/k+o(1))`, no `M`-bit side table,
  same-machine access, and a proved low/high KT gap.

### Route II: ARC/FLMV

- **ESTABLISHED:** the conditional exponent recurrence converges to `(6/5,1/2)`
  and FLMV Corollary 5.8 excludes space `n^(23/45-o(1))` at time `n^(6/5)`
  after matched-model transfer.
- **PROVED, restricted controls:** scoped/sublog-width and locally certified
  replay domains can be normalized or solved, but they are not all-input.
- **FALSIFIED for this construction:** the certified-padding quotient has
  `lambda=1` and therefore cannot instantiate the ARC shrink step.
- **OPEN, weakest arrow:** an all-input hereditary successor for every SAT
  input with charged acquisition, at most `N^(3/5+o(1))` children of ordinary
  length at most `N^(1/2+o(1))`, and peak space `N^(1/2+o(1))`.

## 8. Narrow role handoff

- **:00 MCSP:** construct one source-checkable quotient whose two canonical
  label families have a proved KT gap at `p=M^(1/k)`; first test all explicit
  template and affine-conjugacy escapes.
- **:12 Universal Solver:** determine whether any certified fastest-correct
  portfolio supplies a single `exists W forall i` witness with an explicit
  size/access bound, rather than per-index witnesses or an unknown exponent.
- **:24 ARC:** test a connected high-width nonaffine family for an actual
  `lambda<=1/2` serialized successor; charge validation, source rereads,
  ancestor state, output, and rejected attempts.
- **:36 Red team:** attack the indexed-KT upper bound under the exact universal
  machine and try to totalize the canonicalizer; any totalization must exhibit
  either a mixed-label fiber, a semantic SAT call, or a high-side proof.
- **:48 Synthesis:** next attempt a two-layer construction: certified low-side
  quotient followed by a source-monochromatic high-side code.  Reject it on
  the first explicit low-KT opposite-label control or model mismatch.

No schedule was changed and no additional task was created.  P versus NP
remains OPEN.
