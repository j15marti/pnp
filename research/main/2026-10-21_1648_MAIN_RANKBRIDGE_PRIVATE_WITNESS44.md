# RANKBRIDGE-PRIVATE-WITNESS44

**Timestamp:** 2026-10-21 16:48 Asia/Seoul  
**Status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Bounded evidence review and proposed repairs

This run read the newly synchronized `DIAG-SWITCH20` (:00) and
`ARC-RANKBRIDGE9` (:24) reports, and compared them with the verified
`SOURCE-REFERENCE-FLOOR15` synthesis. No newer complete :12 or :36 RP report
was accessible; their last fully synchronized conclusions therefore remain
unchanged. The shared Drive fallback still ended at the older
`ARC-HEREDITARY-SCOPED10` handoff. This was a targeted review of three relevant
artifacts, not a claim that every project file was re-examined.

Three repairs were fixed before this comparison:

1. use Rankbridge's short shared seed as the ordinary-KT program;
2. augment that seed by a uniform circuit selecting all private block
   witnesses;
3. keep Rankbridge solely as a restricted ARC construction unless such a
   selector is proved small and fully charged.

The first repair is falsified below. The second is exactly the open compact-
witness quantifier upgrade, not a consequence of the short seed. The third is
the sound current allocation.

## 2. Private-witness quantifier firewall

For a Boolean bit `b`, let `G_b(y,u,v)` be the four proper 3-clauses

`(l OR u OR v) AND (l OR u OR -v) AND (l OR -u OR v) AND (l OR -u OR -v)`,

where `l=y` if `b=1` and `l=-y` if `b=0`. The gadget is satisfiable exactly
when `y=b`; the auxiliaries `u,v` are otherwise irrelevant.

For every vector `b=(b_1,...,b_q)`, construct a tagged Rankbridge instance
`F_b` with the same fixed shared seed `sigma=0` and `q` disjoint private
blocks `G_{b_j}(y_j,u_j,v_j)`. The shared XOR recurrence is identical for all
members of the family.

**Theorem (ESTABLISHED, restricted counterfamily).** Every `F_b` is
satisfiable with the same shared seed. Its projected private witness vector is
uniquely `b`. If a fixed total decoder `D(sigma,a,j)` must output the projected
private witness for every member of this family, then some selecting advice
`a` has length at least `q`.

**Proof.** There are `2^q` source instances and `2^q` distinct forced
projections. With `sigma` fixed, advice strings of length at most `s` induce
fewer than `2^(s+1)` decoder outputs. In the fixed-length formulation there
are only `2^s` outputs. Covering all projections therefore requires
`s >= q` (or `q-O(1)` under a self-delimiting convention). QED.

The same counting applies to ordinary KT programs: runtime does not increase
the number of distinct outputs named by a fixed program. Thus, for any
injective target representation retaining the complete private projection,
some member requires KT at least `q-O(1)`.

Under the report's intended `k=241` scale, canonical source length is
`N=Theta(q log q)`, target length is `M=N^(6/5+o(1))`, and

`p_241=max(log M, M^(1/241+o(1)))=N^(6/1205+o(1))=o(q)`.

So an injective private-witness target cannot be LOW for every `F_b` merely
from the shared `O(log N)` seed. This does **not** prove an unrestricted KT
lower bound: a valid SAT-to-MKTP mapping may erase or semantically compress
the private witnesses. It precisely falsifies the proposed direct reuse of
the Rankbridge seed, and any injective witness-retaining variant, as the
ordinary-KT generator.

The quantifier distinction is the load-bearing point:

`exists sigma, for all j, exists y_j B_j(sigma,y_j)`

does not imply

`exists one small W, for all j, W(j)=y_j and B_j(sigma,y_j)`.

This is the same `forall j exists y_j` versus single compact `W` interface
isolated by `COMPACT-HISTORY20`.

## 3. Reproducible consistency audit

`rankbridge_private_witness44_audit.py` checked:

- all 16 rows of the forcing gadget;
- 30 complete formulas through `q=4`, covering 69,904 assignments;
- 324 exact counting-capacity cases through `q=24`; and
- the charged `k=241` threshold comparison for `q=2^4,...,2^24` under a
  canonical literal serialization.

Result: **391 assertions, zero failures**. At `q=16`, the conservative source
serialization already gives `p_241=13<16`; the ratio `q/p_241` then grows.
These computations audit the displayed identities only. They are not
complexity-class evidence.

## 4. Integration with the two PNP routes

### SAT to ordinary MKTP/MCSP

- **ESTABLISHED barrier:** `DIAG-SWITCH20` shows that a source-independent
  logarithmic diagonal string has only `poly(log M)` KT and eventually lies
  below every positive-power threshold.
- **ESTABLISHED barrier:** the theorem above shows that a short shared
  Rankbridge seed does not uniformly select the private witnesses; retaining
  their projection incurs `Omega(q)` information on some source.
- **OPEN:** a deterministic, total, both-label mapping that semantically
  compresses the source while giving the exact ordinary-KT gap, with source
  reads, indexing, runtime, output and same-machine costs charged.
- **RETIRED:** source-independent diagonalization, raw source hardwiring, and
  shared-seed-as-program as standalone repairs.

The combined constraint is useful: a candidate must be source-sensitive
enough to preserve the SAT label, but cannot merely carry either the `N`-bit
source or the `q`-bit private witness vector.

### Arbitrary-decider ARC/FLMV

- **ESTABLISHED, restricted:** `ARC-RANKBRIDGE9` gives the claimed exponent
  ledger only on its tagged XOR/private-namespace family.
- **OPEN:** extend it to every input, every recursive child and every
  arbitrary SAT decider while retaining parent semantics and charging child
  acquisition, replay and simultaneous peak space.
- **CONDITIONAL:** the recurrence and FLMV endpoint apply only after that
  all-input hereditary contractor exists.

The private-witness theorem does not invalidate restricted Rankbridge ARC. It
only prevents transferring its short compatibility seed into the MKTP route
without a proved global selector.

## 5. Separate RP proof DAG

No new complete :12/:36 artifact was synchronized, so no RP claim is promoted.

- **ESTABLISHED:** verifier-specific replay, block-spectral and temporal-
  overlap theorems retain only their explicit promises. Temporal overlap is
  not invariant under pointwise-equivalent dead-read padding.
- **OPEN (`P=RP`):** a uniform deterministic simulation of every RP machine.
- **OPEN (`P!=RP`):** an explicit RP language outside all deterministic
  polynomial-time machines.
- **RETIRED as class conclusions:** selected-verifier geometry, random hashes,
  oracle bounds, proof-system bounds and finite tests.

SAT in RP would yield `NP=RP`, not by itself `P=RP`; `P!=RP` would imply
`P!=NP`, but neither premise has been proved.

## 6. Single next discriminating test per active role

- **:00 SAT-to-MKTP:** require the next generator to state whether its LOW
  program outputs an injective encoding of private witnesses. If yes, apply
  the `Omega(q)` family immediately; if no, prove the exact semantic label
  preserved by the erasure.
- **:12 P!=RP:** name one ordinary language and test the proposed obstruction
  against a pointwise-equivalent deterministic verifier before any promotion.
- **:24 ARC/FLMV:** add one well-formed high-width non-XOR shared constraint
  and test whether seed enumeration still produces all children within the
  simultaneous peak-space ledger.
- **:36 P=RP:** on the next synchronized replay normal form, test whether its
  certificate survives preread/postread padding without semantic dead-read
  analysis.
- **:48 synthesis:** treat `exists seed` as a compatibility certificate, not
  a compact global witness, until a single source-independent selector and
  its full KT/time-space cost are proved.

No root manuscript, role or automation was modified.

