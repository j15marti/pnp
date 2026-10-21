# RP-TWO-AXIS-VERIFIER-FIREWALL41

**Timestamp:** 2026-10-21 13:48 Asia/Seoul  
**Scope:** P-vs-NP two-route synthesis plus a separate P-vs-RP proof DAG.  
**Status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Recovered specialist state

This run read both newly shared RP specialist packages and their coverage
ledgers:

- RP-REPLAY-STATE6 (:12): 149 identified records, 140 inherited and nine
  new. Its exact restricted theorem derandomizes a verifier whose ordinary
  configuration graph is polynomial and whose explicitly identified
  recurrent random-address set has size O(log N). Its CNF control correctly
  shows that replacing persistent assignment bits by fresh bits destroys
  one-sided soundness.
- RP-TRACE-FOURIER4 (:36): 140 identified records, 121 inherited and 19
  directly indexed or reviewed in that run. Its exact restricted theorem
  derandomizes acceptance functions having a known polynomial Fourier L1
  bound by an explicit trace small-bias set. Its quadratic-phase family
  proves that polynomial-time, constant-width verifiers can have exponential
  Fourier L1 mass.

Both ledgers explicitly describe their corpus coverage as partial. This
synthesis therefore makes no comprehensive-history claim.

No newer substantive :00 MKTP or :24 ARC body was shared after the previous
synthesis. The shared fallback Doc remains unchanged at the older
ARC-HEREDITARY-SCOPED10 entry. Root main.tex received an external review
annotation at commit a4d323b; this run did not edit it.

## 2. Mechanisms proposed before fresh literature search

1. Construct four verifiers for one fixed easy language realizing every
   low/high combination of recurrent-address support and Fourier L1 mass.
2. Inflate replay support using semantically discarded repeated reads and
   test exact acceptance-function invariance.
3. Inflate Fourier mass with a quadratic phase while retaining RP density and
   an obvious deterministic language bypass.
4. Require any claimed universal combination to supply a uniform normal-form
   transformation, not merely a disjunction of verifier-specific sufficient
   conditions.

Mechanisms 1--3 are proved and exhaustively tested below.

## 3. Primary-source boundary

Naor--Naor small-bias spaces guarantee approximate parity balance, not
fooling of every polynomial-time predicate
([DOI 10.1137/0222053](https://doi.org/10.1137/0222053)). Nisan's
space-bounded generator is a model-specific simulation theorem
([paper](https://resources.mpi-inf.mpg.de/departments/d1/teaching/ws10/EG/Nisan_PRG.pdf));
it does not convert arbitrary trace syntax into a language lower bound.

MMW begins with an existing explicit MCSP/MKTP target
([paper](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf)).
FLMV supplies a deterministic random-access simultaneous SAT time-space
endpoint
([paper](https://lance.fortnow.com/papers/files/tst.pdf)).
Neither RP structural theorem constructs the missing PNP totalizer or ARC
successor.

## 4. Four-quadrant verifier theorem

Let L be the odd-parity language, decided deterministically in linear time.
Fix an even random-tape length m=2h and define

Q_m(r) = XOR over j of r_(2j) AND r_(2j+1),

and f_m(r)=1 exactly when Q_m(r)=0. Standard tensor-product calculation gives

Pr[f_m=1] = 1/2 + 2^(-h-1)

and

Fourier-L1(f_m) = 1/2 + 2^(h-1).

Construct four uniform verifiers:

1. LL: ignore the random tape and return parity(x).
2. HL: read every random address twice, discard all values, and return
   parity(x).
3. LH: read each random address once, compute f_m, and return
   parity(x) AND f_m(r).
4. HH: read each random address twice, use one copy to compute f_m, discard
   the duplicate, and return parity(x) AND f_m(r).

The first letter records recurrent-address support: L means zero and H means
m. The second records Fourier mass: L means one and H means
1/2+2^(m/2-1).

### Theorem

All four verifiers recognize exactly the same language L with valid
one-sided RP error. They realize all four low/high combinations:

| Verifier | recurrent support | YES Fourier L1 |
|---|---:|---:|
| LL | 0 | 1 |
| HL | m | 1 |
| LH | 0 | 1/2 + 2^(m/2-1) |
| HH | m | 1/2 + 2^(m/2-1) |

### Proof

On an even-parity input every verifier returns zero on every tape. On an
odd-parity input LL and HL accept every tape; LH and HH accept with probability
1/2+2^(-m/2-1), which is at least 1/2.

LL and HL have a tape-independent Boolean acceptance function on YES inputs,
so their only nonzero Fourier coefficient is the constant coefficient one.
For LH and HH, each two-bit phase (-1)^(uv) has four Walsh coefficients of
magnitude 1/2. Tensoring h independent pairs yields the stated exponential
norm after converting the sign function to its zero-phase indicator.

In LL and LH no address is read twice, so the minimal recurrent set is empty.
In HL and HH every address is read twice on every execution, so every address
belongs to the minimal recurrent set. The second read is semantically
discarded, hence HL equals LL and HH equals LH pointwise. Each machine runs in
O(n+m) time and logarithmic index space.

### Consequence

The REPLAY-STATE6 and TRACE-FOURIER4 theorems remain correct sufficient
conditions:

- LH is covered by bounded replay even though it has exponential Fourier
  mass.
- HL is covered by bounded Fourier mass even though its selected
  implementation has linear recurrent support.

But HH fails both hypotheses while recognizing the same easy language.
Therefore simultaneous failure of the two restrictions is not evidence for
P!=RP. Recurrent support can be syntactically inflated without changing the
acceptance function, and Fourier mass can be changed by choosing a different
RP verifier for the same language.

Any universal conclusion now needs a uniform semantic normal-form theorem:
given an arbitrary RP machine, construct a polynomial-time equivalent
deterministic decider or a verifier satisfying a proved derandomizable
property. No such theorem is supplied here.

## 5. Reproducible audit

The standard-library checker exhausts every random tape for even
m=2,4,...,16 and all four source bits:

- 11,534,160 verifier executions;
- 2,796,160 pointwise semantic-equivalence checks;
- 32 exact density checks;
- 32 exact Walsh/Fourier checks;
- 32 recurrent-support checks;
- 3,146,288 instrumented assertions;
- zero failures.

Raw SHA-256:
afaeba849d410cdf00ffc429ed30e2dc5ffc7bbdf81a157533d175c66aebea8a.
The finite audit validates the implementations. The tensor-product and
pointwise-equivalence arguments prove the all-m theorem.

## 6. Separate proof DAGs

### P versus NP

**ESTABLISHED:** MMW, CHMY, OPS and FLMV only in their published models;
conditional ARC exponent accounting; restricted low-width joins.

**CONDITIONAL:** SAT -> charged deterministic total both-label ordinary-MKTP
target -> MMW streamer -> same-machine SAT bounds -> FLMV contradiction.

**OPEN:** a genuine all-input ordinary-KT gap with p at least log M; an
all-input hereditary fully charged ARC successor; COMPACT-HISTORY20's single
exists-W-forall-i subpolynomial witness circuit.

**RETIRED:** short tags/transcripts, affine mixers, verifier replay or Fourier
structure, output materialization and finite tests as unrestricted SAT lower
bounds.

### P versus RP

**ESTABLISHED:** REPLAY-STATE6 and TRACE-FOURIER4 as restricted sufficient
conditions; the four-quadrant theorem above; P subseteq RP subseteq NP.

**CONDITIONAL/CANDIDATE:** a uniform class-covering normal form placing every
RP language into one of the two restricted families would imply P=RP, but no
such transformation is known.

**OPEN:** an explicit language in RP outside every deterministic polynomial
machine, or a uniform deterministic simulation of every RP machine.

**FALSIFIED/RETIRED:** large recurrent support, large Fourier mass, or their
joint occurrence as language hardness; public seed sets as universal hitting
sets; SAT in RP as P=RP; relativizing/hash/finite evidence as a separation.

## 7. Single highest-value next experiment per active route

- **:00 MKTP:** test the first genuinely nonlinear total target on matched
  labels and compute ordinary indexed KT including source acquisition,
  decoder, index and runtime; reject any short-tag or replayable transcript.
- **:24 ARC:** eagerly serialize one high-width nonaffine semantic child
  family and measure rejected children, rereads, ancestors and peak space on
  matched SAT/UNSAT parents.
- **:12 RP separation:** state the candidate language independently of its
  verifier and attack every claimed obstruction by replacing the verifier
  with a semantically equivalent easy implementation.
- **:36 RP derandomization:** attempt a uniform normalization of arbitrary RP
  verifiers into bounded replay or bounded Fourier mass; the HH verifier is
  the first required syntax-invariance test.
- **:48 synthesis:** promote only language-invariant arrows; retain both new
  RP theorems as restricted deliverables.

No automation, role, or schedule was changed.

