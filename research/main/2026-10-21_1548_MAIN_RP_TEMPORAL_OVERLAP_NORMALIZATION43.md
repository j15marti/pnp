# RP-TEMPORAL-OVERLAP-NORMALIZATION43

**Timestamp:** 2026-10-21 15:48 Asia/Seoul  
**Status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. New evidence and bounded source review

The only new specialist artifact accessible after the preceding synthesis was
the two-line :36 `TEMPORAL-REPLAY8` interim status. It reports a restricted
dynamic program for logarithmic certified random-address window overlap and a
coNP-complete all-tapes certificate problem, but explicitly says its complete
report and tests remain unsynchronized. Those unshared details are therefore
not promoted here.

This run also reread the complete repository report `RP-REPLAY-STATE6` and the
verified `RP-BLOCK-SPECTRAL-HEAVY-PATH42` synthesis. The shared Drive fallback
log was checked and still ended with the older
`ARC-HEREDITARY-SCOPED10` handoff. This is a bounded targeted review, not an
exhaustive historical-source claim.

Before the repository follow-up, three repairs were fixed:

1. delete semantically dead random-tape reads before measuring temporal
   overlap;
2. minimize overlap over equivalent verifiers rather than one implementation;
3. combine certified low overlap with the restricted block-spectral theorem.

The first repair encounters a coNP-hard semantic certification problem. The
second is not supplied by either verifier theorem and collapses immediately on
easy languages with a separate deterministic decider. The third remains a
valid restricted combination but gives no arbitrary-RP normal form.

## 2. Exact temporal-padding theorem

Let `V(x;r)` be any uniform verifier using `m(n)` random-tape addresses and
halting within `T(n)` steps on every tape. Construct `V^up` as follows:

1. read every random address `1,...,m` once and discard the values;
2. execute `V(x;r)` unchanged, retaining its output bit;
3. read every random address `1,...,m` once more and discard the values;
4. return the saved output bit.

Define the temporal window of address `j` as the interval from its first to
its last read.

**Theorem 1 (ESTABLISHED).** For every input and every fixed random tape,
`V^up(x;r)=V(x;r)`. Every one of the `m` address windows overlaps the entire
execution of the middle copy of `V`. The construction is uniform, adds
exactly `2m` random-tape reads, `O(m)` time and only counter/output bookkeeping
space, and uses no advice or oracle.

Thus a verifier can be changed from low temporal overlap to overlap `m`
without changing even its pointwise acceptance function. Temporal overlap is
not a language invariant and is not invariant under pointwise-equivalent
verifier padding.

This theorem does **not** refute a correctly promised low-overlap dynamic
program. It refutes promotion of high overlap, or hardness of certifying one
implementation, into a language lower bound.

## 3. Dead-read removal is coNP-hard on one easy language

Let `C(z)` be a Boolean circuit. Define a verifier, independent of its source
input, using random bits `q,a,z` by

`F_C(q,a,z) = q OR (a AND C(z))`.

For every circuit `C`, at least the half of tapes with `q=1` accept. Hence
every `F_C` is a valid RP verifier for the same trivial language `Sigma*`.

**Theorem 2 (ESTABLISHED).** The address `a` is semantically dead—changing it
can never change acceptance—if and only if `C` is unsatisfiable.

**Proof.** If `C` is unsatisfiable, `F_C=q`, so `a` is irrelevant. If `C` has
a satisfying assignment `z*`, then at `q=0,z=z*`, changing `a` from zero to
one changes the output. Therefore circuit-UNSAT many-one reduces to semantic
deadness. QED.

Consequently, a normalization that removes every semantically dead random
read must solve a coNP-hard problem even on selected verifiers all recognizing
`Sigma*`. This is a certification obstacle, not evidence that `Sigma*` or any
RP language lies outside P.

## 4. Reproducible consistency audit

`rp_temporal_overlap_normalization43_audit.py` exhausts:

- 65,812 Boolean acceptance functions on one through four random bits and
  1,050,696 tapes for pointwise temporal-padding equivalence;
- 65,814 circuit truth tables through four input bits;
- 4,202,792 rows of the verifier `F_C`;
- the equivalence `a is dead iff C is UNSAT`; and
- the RP density lower bound for every constructed verifier.

Result: **5,450,928 assertions, zero failures**. These are finite controls for
the displayed identities, not complexity-class evidence.

## 5. Integration with the proof DAGs

### P versus RP

- **ESTABLISHED, restricted:** `REPLAY-STATE6`,
  `BLOCK-SPECTRAL-HEAVY-PATH42`, and the claimed portion of
  `TEMPORAL-REPLAY8` apply when their explicit structural certificates are
  supplied.
- **ESTABLISHED barrier:** temporal overlap can be inflated to `m` by dead
  reads without changing pointwise acceptance; exact semantic dead-read
  detection is coNP-hard even for verifiers of `Sigma*`.
- **OPEN:** a uniform semantic normalization of every RP verifier into any of
  the restricted models.
- **OPEN:** a uniform deterministic simulation of every RP language (`P=RP`).
- **OPEN:** an explicit language in `RP` outside all deterministic polynomial
  machines (`P!=RP`).

The interim `TEMPORAL-REPLAY8` theorem and its computational claims remain
**UNVERIFIED/PENDING SYNCHRONIZATION** beyond the two-line shared status.

### P versus NP

- **OPEN:** deterministic total both-label SAT-to-ordinary-MKTP/MCSP mapping
  with a genuine threshold gap and charged source/index/output/runtime costs.
- **OPEN:** all-input hereditary arbitrary-decider ARC successor with ordinary
  serialized children, correct parent semantics, replay and simultaneous peak
  workspace charged.
- **CONDITIONAL:** the published magnification and FLMV endpoints become
  relevant only after their matched missing arrows are constructed.
- **RETIRED as separation arguments:** selected-verifier replay, timing,
  random hashes, semantic-certificate hardness, or finite experiments.

Temporal padding supplies neither an ordinary MKTP target nor an ARC child.

## 6. Single next discriminating test per role

- **SAT-to-MKTP:** implement one nonlinear total both-label generator and
  compute ordinary KT including decoder, source acquisition, indexing,
  runtime and `p>=log M`; reject on the first matched-label collision.
- **P!=RP:** name one ordinary language rather than one verifier, then test an
  alternative deterministic implementation before any tape-geometry claim.
- **ARC/FLMV:** materialize one high-width nonaffine semantic child and verify
  both SAT and UNSAT parent reconstruction with complete peak-space charging.
- **P=RP:** obtain and independently read the full `TEMPORAL-REPLAY8` body;
  then test whether its certificate survives the preread/postread padding or
  requires solving semantic deadness.
- **Synthesis:** promote only properties invariant under pointwise-equivalent
  verifier rewrites, or state the promise explicitly.

No root manuscript, role, or automation was modified.

