# TWO-LABEL-CERTIFICATE-ENVELOPE76

Timestamp: 2026-10-23 00:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis tests whether the missing ARC transformer can be supplied by a two-label certificate under `P=NP`: a SAT witness on one label, an UNSAT certificate on the other, split across smaller children. The explicit-history and sampled-digest versions fail the verified ARC resource envelope. A succinct certificate-bit circuit remains a precise CONDITIONAL interface, but its existence and uniform acquisition are exactly the unresolved COMPACT-HISTORY20 burden.

## Repairs fixed before source review

1. **Streamed two-label certificate:** distribute a complete SAT/UNSAT certificate across `Q=N^alpha` children of length `D=N^beta`.
2. **Digest plus sampled openings:** commit to a longer certificate using a short hash/Merkle root and inspect only selected local constraints.
3. **Succinct bit-circuit:** represent the certificate by a circuit `W(i)` and create a smaller Circuit-SAT child asking whether any local consistency condition is violated.

Falsifiers fixed in advance: explicit output capacity `QD`, the exact black-box validity predicate `AND_L`, and a computation history whose length inherits the unknown polynomial decider exponent.

## Repository sources reviewed after fixing the repairs

1. `research/main/2026-10-22_2348_MAIN_MINIMAL_CORE_SOURCE_COVERAGE75.md`: explicit proof/certificate materialization may be nearly linear even when the proof has a short indexed generator.
2. `research/agents/rp-separation/2026-10-22_2312_RP_DENSE_COVER_ORACLE38_HANDOFF.md`: black-box zero-versus-half-density separates `P^A` from `RP^A` relative to a recursive oracle, while explicit hostile circuits admit gate-readable bypasses.
3. `comments/grok-4.7/2026-10-23/2026-10-23_0016_GROK_REVIEW.tex`: independent review retains exact all-input hereditary semantic compression as the load-bearing OPEN arrow.

The RP handoff's correction is incorporated: for each fixed circuit gate budget, a small hitting list exists nonuniformly by counting/union bound; this is not a uniform cross-size derandomizer.

## Model

Suppose a one-level ARC transformation emits

- `Q=N^(alpha+o(1))` explicit children,
- each of maximum encoded length `D=N^(beta+o(1))`,
- within construction/output time `N^(gamma+o(1))`.

Let a proposed label certificate have explicit length `L=N^(omega+o(1))`.

The baseline point is `(alpha,beta,gamma)=(0.6,0.5,1.1)`; the retuned point has `(alpha,beta)=(0.595,0.505)`. Both satisfy `alpha+beta=1.1`.

## Lemma 76A — explicit certificate-capacity envelope

If every certificate bit is explicitly placed in at least one emitted child, then

`omega <= alpha+beta`

is necessary. Independently, explicit emission takes `Omega(L)` time, so

`omega <= gamma`

is necessary.

**Proof.** The total number of emitted child bits is at most

`QD=N^(alpha+beta+o(1))`.

Covering `L` distinct required certificate positions needs `L<=QD`. Writing them takes at least `L` output steps in the ordinary explicit-output model. QED.

At both verified ARC points, an explicit certificate with exponent `omega>1.1` cannot be distributed within one level. Equality at `1.1` leaves no polynomial slack for source acquisition, addressing, redundancy, local constraints or aggregation.

**Status: ESTABLISHED output/accounting lemma.**

### Consequence for computation histories

Fix an assumed SAT decider `A` with time `T(N)=N^(C+o(1))`. A materialized step-by-step computation history contains at least `Omega(T)` time positions and therefore has `omega>=C` in the direct history model; standard Cook-Levin-style encodings inherit exponent `C` up to lower-order factors or worse model-specific overhead.

Because `P=NP` does not provide an a priori bound `C<=1.1`, the direct history strategy cannot supply the fixed ARC transformer needed to improve an arbitrary polynomial decider. Running `A(F)` merely to choose the correct label also restores SEMANTIC-PARENT-CALL-CIRCULARITY66.

- **RETIRED:** explicit full-history certificates as a generic constructor.
- **OPEN:** a proof that the required certificate has a much smaller indexed representation.

## Lemma 76B — exact sampled-checking firewall

Consider certificate validity

`VALID(y)=AND_(i=1)^L y_i`.

Any deterministic exact query algorithm makes all `L` queries on input `1^L`.

**Proof.** If position `j` is unqueried, change only `y_j` to zero. The transcript is unchanged, but validity flips. QED.

This simple verifier is an adversarial control for sampled local checking. It does not assert that every proof system has this form; it proves that sampling alone cannot guarantee exactness for all local-validity relations.

### Digest/Merkle implications

- A digest computed exactly from the certificate may encode the validity bit, but acquisition can itself require all `L` reads; that cost cannot be omitted.
- Treating a supplied digest as trusted moves the burden outside the standard deterministic model.
- Merkle openings certify only opened leaves unless collision resistance and commitment correctness are assumed; cryptographic assumptions do not yield an unconditional exact SAT equivalence.
- Random PCP-style tests have bounded soundness error. Enumerating enough tests to restore deterministic exactness must be charged and can recover the full validation cost.

**Status: ESTABLISHED black-box exact-query barrier; sampled digest repair RETIRED generically.**

## Candidate 76C — succinct certificate-bit circuit

Let `W(i)` generate certificate bit `i`, and suppose local invalidity can be expressed as a circuit

`Bad(F,b,W,i)`.

Then certificate validity is

`forall i: not Bad(F,b,W,i)`,

equivalently the Circuit-SAT instance `exists i: Bad(F,b,W,i)` is UNSAT. This is a real derived semantic child rather than a subset of source clauses.

It fits a child-length exponent `beta` only if all of the following are available:

1. `W` has size at most `N^(beta+o(1))`;
2. source-bit access to `F` inside `Bad` has an equally small, model-valid representation rather than a free oracle;
3. the correct label `b` and circuit `W` are generated uniformly without first deciding the current-scale parent;
4. exact violation search, encoding conversion, output and peak space satisfy the same ARC/FLMV machine ledger;
5. these properties remain hereditary at every recursive child.

Under `P=NP`, polynomial-hierarchy validity search collapses to polynomial time, but that alone neither bounds the exponent nor gives a small `W`; invoking the parent-scale decider repeats circularity. COMPACT-HISTORY20's `tau(n)^o(1)` satisfying-assignment-circuit premise would address item 1 on its specified padded inputs, but that premise remains OPEN and is not implied by oracle-query or explicit-history lower bounds.

**Status: CONDITIONAL interface, not a construction.**

## Circuit-SAT representation control

A functional Tseitin encoding gives a unique gate trace after primary inputs and `W` are fixed. It does not prove that a small correct `W` exists, nor that source access factors through a short digest. Easy gate inspection may expose a deterministic bypass, as in DENSE-COVER-ORACLE38. Therefore every candidate must publish primary inputs, original random coins, auxiliary trace variables, source evaluators and peak resources separately.

Circuit-SAT remains a representation tool, not a third P-vs-NP route.

## Ordinary MKTP/MCSP route

- An explicit long certificate can still have a short indexed generator, so materialized length does not imply HIGH ordinary KT.
- A genuinely small `W` is naturally a short description and therefore tends toward KT-LOW, not the missing label-sensitive HIGH target.
- **OPEN:** deterministic total both-label SAT-to-ordinary-MKTP construction with correct polynomial threshold, indexed runtime and same-machine source costs.
- **RETIRED:** using explicit certificate/history length alone as the HIGH-side argument.

## ARC/FLMV route

- **ESTABLISHED:** explicit certificate capacity requires `omega<=min(gamma,alpha+beta)`.
- **ESTABLISHED restricted:** deterministic exact black-box validity may require every certificate position.
- **RETIRED:** arbitrary-exponent computation histories and sampled hashes as generic one-level repairs.
- **CONDITIONAL:** a small, uniformly acquired `W` plus a small source evaluator yields a violation-search child.
- **OPEN:** prove those premises on every input and recursive descendant inside either verified FLMV envelope.

## Independent P-vs-RP cross-audit

DENSE-COVER-ORACLE38 correctly supplies a **relative** separation `P^A != RP^A` for one recursive oracle; Baker-Gill-Solovay-type opposite oracle worlds prevent unrelativized transfer. Its explicit Circuit-SAT control is easy by source/gate inspection.

For a fixed family of at most `M=2^ell` half-dense acceptance sets, `h=ell+t` independent tapes miss some set with union-bound probability at most `2^(-t)`. Counting bounded-fan-in circuits of fixed gate budget therefore gives a polynomial-size **nonuniform** hitting list, consistent with `RP subseteq P/poly`. What remains OPEN is uniform construction across machine descriptions and all polynomial size exponents.

- **OPEN (`P!=RP`):** an explicit unrelativized RP language outside every deterministic polynomial-time machine.
- **OPEN (`P=RP`):** a uniform deterministic simulator for every promised RP machine.
- **RETIRED:** transferring oracle query separation, proof length, sampled commitments or fixed-budget advice to either conclusion.

## Finite audit

`experiments/review/2026-10-23_two_label_certificate_envelope76_audit.py` checked:

- every proper query subset for `AND_L`, `L<=16`;
- 20,000 larger proper query schedules through `L=4096`;
- 18,002 baseline/retuned capacity cases;
- 6,000 fixed-family hitting-set union-bound cases.

Result: **312,112 checks, zero failures.** This validates implementations of the proved identities only.

## Five-role status and next discriminating tests

| Role | Status | Single next experiment |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Compute ordinary KT for a local-history `W(i)` including random-access time; reject materialized-length arguments if the indexed generator is short. |
| :12 P!=RP | Relative oracle separation **ESTABLISHED**; unrelativized **OPEN** | Run DENSE-COVER38 against three real WRAPPER acceptance circuits and record gate-readable deterministic bypasses. |
| :24 ARC/FLMV | Certificate capacity **ESTABLISHED**; transformer **OPEN** | Construct one `Bad(F,b,W,i)` child and measure `|W|`, embedded source evaluator size, acquisition calls and maximum encoded length. |
| :36 P=RP | Fixed-budget nonuniform hitting **ESTABLISHED**; uniformity **OPEN** | Attempt to generate—not merely count—a hitting list from the verifier description, surviving dummy coins and replacement. |
| :48 synthesis | Explicit history/sample repairs **RETIRED** | Require every succinct-certificate claim to expose `W` acquisition and exact source access before placing it on the FLMV surface. |

## Conclusion

Two-label certificates do not by themselves construct the ARC transformer. Explicit histories inherit the unknown solver exponent and exceed the `1.1` output envelope; sampled digests do not give deterministic exactness. The remaining constructive possibility is sharply isolated: a uniformly acquired, small certificate-bit circuit together with a small exact source evaluator and hereditary violation-search encoding. That is a reformulation of the compact-witness gap, not its solution. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
