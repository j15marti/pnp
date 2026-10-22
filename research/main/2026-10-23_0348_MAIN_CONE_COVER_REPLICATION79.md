# CONE-COVER-REPLICATION79

Timestamp: 2026-10-23 03:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

SOURCE-DEPENDENCY-CONE78 showed that a single standalone child needs a small static source cone and that few probes per witness do not imply one. This bounded synthesis tests the natural repair: partition the witness space into many regions, each with its own small static cone. The repair is exact and constructive for the multiplexer control, and it exposes a new invariant—the total source-incidence/replication budget. No arbitrary-SAT cone cover is constructed.

## Repairs fixed before source review

1. **Cone-homogeneous witness buckets:** partition witnesses so each bucket label depends on at most (N^eta) source coordinates.
2. **Address-oblivious compilation:** replace witness-dependent source addresses by a fixed read set per bucket.
3. **Semantic fibers:** partition by a source-checkable summary through which each bucket label factors.

Predeclared falsifiers: bucket descriptors, cone generation, source addresses/data, and aggregation must all be explicit; if every source coordinate must be copied into too many children, the (Q N^eta) incidence capacity is exceeded.

## Repository sources reviewed after fixing the repairs

1. [SOURCE-DEPENDENCY-CONE78](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-23_0248_MAIN_SOURCE_DEPENDENCY_CONE78.md): exact static cones of exponent at most (eta) suffice for standalone children; dynamic probes alone do not.
2. [SOURCE-OVERLAP43](https://github.com/j15marti/pnp/blob/main/research/agents/rp-derandomization/2026-10-23_0236_SOURCE_OVERLAP43_HANDOFF.md): conditioning the overlap variables of a uniformly compiled NNF yields a restricted deterministic witness algorithm; compilation and source access remain charged.
3. [Independent review 03:12 KST](https://github.com/j15marti/pnp/blob/main/comments/grok-4.7/2026-10-23/2026-10-23_0312_GROK_REVIEW.tex): the all-input hereditary construction remains OPEN and must publish static cones and aggregate source acquisition.

## Model

Let the parent existential label be

[
L(F)=exists zin Z;V(F,z).
]

Partition (Z) into (Q) disjoint regions (Z_1,ldots,Z_Q), and define

[
L_j(F)=exists zin Z_j;V(F,z).
]

Let (S_jsubseteq[N]) be an exact static source cone for (L_j): (L_j(F)) is determined by (F|_{S_j}). The source-incidence count is

[
I=sum_{j=1}^{Q}|S_j|.
]

## Lemma 79A — exact cone-cover aggregation

If every (L_j) has a uniformly generated standalone Circuit-SAT encoding from (F|_{S_j}) and its bucket descriptor, then

[
L(F)=igvee_{j=1}^{Q}L_j(F).
]

This is exact on both labels:

- parent YES iff at least one child is YES;
- parent NO iff every child is NO.

No current-scale parent-label call is required. Descriptor generation, bucket-membership constraints, cone construction, source acquisition, and output remain charged.

**Status: ESTABLISHED logical composition lemma; arbitrary-SAT construction OPEN.**

## Lemma 79B — source-incidence and replication budget

For

[
Q=N^{alpha+o(1)},qquad |S_j|le N^{eta+o(1)},
]

the total source incidence satisfies

[
Ile N^{alpha+eta+o(1)}.
]

Write

[
sigma=alpha+eta-1.
]

If all (N) source coordinates must appear at least once, their average replication is at most

[
I/Nle N^{sigma+o(1)}.
]

More strongly, if exactness forces every source coordinate into at least (N^{ho-o(1)}) children, then necessarily

[
holesigma.
]

Both verified parameter points have the same redundancy budget:

- baseline: ((alpha,eta)=(0.6,0.5)), (sigma=0.1);
- retuned: ((0.595,0.505)), (sigma=0.1).

Thus they permit average replication (N^{0.1+o(1)}), not arbitrary duplication across all children.

The addresses and source values add logarithmic factors already absorbed in (o(1)). If cones are virtual rather than materialized, a separate model-transfer argument is still required.

**Status: ESTABLISHED counting/accounting lemma.**

## Lemma 79C — multiplexer barrier is exactly repaired by bucketing

For the SOURCE-DEPENDENCY-CONE78 control

[
V(F,z)=F_z,qquad zin[N],
]

one child has a full (N)-bit cone. Partition addresses into buckets of size

[
B=N^{eta+o(1)}.
]

Each bucket child computes the OR of its (B) hardwired source bits, so its cone has size (B). The number of children is

[
Q=N^{1-eta+o(1)}.
]

Therefore a cone cover exists whenever

[
alphage 1-eta.
]

The baseline and retuned points satisfy the stronger relation

[
alpha=1-eta+0.1.
]

The construction has total incidence (I=N) and source replication exactly one. It demonstrates that the one-probe multiplexer retires single-child sparse hardwiring but does **not** retire multi-child cone covers.

**Status: ESTABLISHED matching construction for an easy control; no class separation.**

## Global-dependence hostile control

Let

[
V(F,z)=igwedge_{i=1}^{N}F_i
]

for every nonempty witness region. Then every nonempty bucket label depends on all (N) source coordinates. Each cone has size (N), so no (N^eta)-length standalone child exists for fixed (eta<1); duplicating the source into (Q) children requires (QN) incidence.

This family has an easy direct deterministic decider. It is a representation falsifier only, not an SAT or language lower bound.

**Status: ESTABLISHED hostile control.**

## Constructive target after Lemmas 79A–C

The sharp ARC target is now a **cone-cover compiler** that, on every source (F):

1. emits at most (N^{alpha+o(1)}) witness-region descriptors;
2. certifies an exact cone (S_j) of size at most (N^{eta+o(1)}) for each region;
3. emits and processes children depth-first without retaining all cones;
4. keeps total incidence and source acquisition within (N^{alpha+eta+o(1)});
5. reconstructs the parent by exact OR aggregation;
6. repeats hereditarily on every child, with same-model output and peak space charged.

This avoids the invalid quantifier exchange from unrelated local witnesses: the regions partition one common witness universe and the OR identity is exact. It does not supply the compiler.

## SOURCE-OVERLAP43 integration

SOURCE-OVERLAP43 conditions a source-faithful NNF on a cutset (U) containing original variables shared across AND children. Enumerating (2^{|U|}) assignments partitions the witness space; residual decomposable pieces then support exact satisfiability testing.

This is a restricted instance of cone/overlap partitioning, but it becomes a polynomial deterministic simulation only when:

- the NNF/DNNF compilation is uniform polynomial size and time;
- (|U|=O(log n));
- original-source support is faithful;
- residual satisfiability and source extraction are charged.

The reported project root has 14 original variables; its explicit finite DNNF and (k=0) decomposition are useful controls. They do not establish a uniform compiler for every RP verifier or SAT source. High ANF degree/support and exact model counts are orthogonal to the witness algorithm.

**Status: SOURCE-OVERLAP43 ESTABLISHED restricted; general compilation and P-versus-RP conclusions OPEN.**

## Circuit-SAT representation audit

Functional Tseitin traces remain unique only after shared source inputs are fixed. Cone bucketing may share a gate body in an incremental model, but ordinary children must carry their bucket descriptor, source cone, fixed values and local trace constraints. A gate shared syntactically across children still consumes source incidence wherever its value is semantically required.

Circuit-SAT remains a representation and hostile-control tool, not a third P-vs-NP route.

## Ordinary MKTP/MCSP route

Cone covers produce small local evaluators and therefore tend toward ordinary KT-LOW. The concatenation of all child encodings costs (N^{alpha+eta+o(1)}), while any evaluator retaining the original source must count its (N)-bit description and source-access time.

- **ESTABLISHED:** cone descriptors, source values/addresses, replication and indexed runtime enter KT.
- **RETIRED:** inferring label-sensitive HIGH from full aggregate incidence or an incompressible external source.
- **OPEN:** deterministic total both-label SAT-to-ordinary-MKTP generator meeting the polynomial threshold on the same machine model.

## ARC/FLMV route

- **ESTABLISHED:** exact witness partitions with small static cones yield exact OR aggregation.
- **ESTABLISHED:** total incidence is at most (N^{1+sigma}); both parameter points have only (sigma=0.1) replication slack.
- **ESTABLISHED control:** multiplexer admits an optimal cone cover with replication one.
- **CONDITIONAL:** a uniform all-input hereditary cone-cover compiler inside the baseline or retuned resource envelope.
- **OPEN:** construct that compiler for arbitrary SAT without current-scale labels, hidden persistent source state, or per-child replay.

## Independent P-vs-RP audit

Partitioning accepting random tapes into regions is useful only if region cones are source-faithful and uniformly generated. Per-path low coin access, high ANF complexity, or a nonuniform DNNF does not suffice.

- **ESTABLISHED restricted:** a uniformly polynomial NNF with (O(log n)) overlap cutset yields a deterministic polynomial witness algorithm.
- **OPEN (P=RP):** no such uniform compilation/partition is known for every RP machine.
- **OPEN (P
e RP):** no explicit unrelativized RP language outside all deterministic polynomial-time machines.
- **RETIRED:** independent auxiliary-gate sampling, branch-count sums for nondeterministic ORs, or finite DNNF examples as class evidence.

## Finite consistency audit

The accompanying JavaScript partitions multiplexer witnesses for (N=2^k), (4le kle16), verifies exact OR aggregation on 2,600 deterministic pseudorandom sources, checks incidence (I=N) and replication one, and evaluates the global-dependence control.

Result: **336,095 checks, zero failures.** This validates the constructions and accounting only.

## Five-role next discriminating tests

| Role | Status | Single next experiment |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Compute indexed KT for a two-level cone cover, including region descriptors, replicated source bits and lookup time. |
| :12 P!=RP | separation **OPEN** | Extract witness/coin regions from one real WRAPPER and measure cone incidence; run the easy direct-decider and SAT-NO controls. |
| :24 ARC/FLMV | Lemmas 79A–C **ESTABLISHED**; compiler **OPEN** | Attempt one exact SAT witness partition with (alpha=0.6,eta=0.5), and report each clause/source bit’s replication. |
| :36 P=RP | SOURCE-OVERLAP43 **ESTABLISHED restricted** | Compile the growing SHA/timer verifier source-faithfully; measure NNF size, overlap cutset, cone sizes and compiler cost. |
| :48 synthesis | cone-cover interface **CONDITIONAL constructive target** | Reject any cover whose replication exponent exceeds (0.1) or whose region cones are inferred only from realized traces. |

## Conclusion

Static-cone bucketing is a real constructive repair: it converts the single-child multiplexer obstruction into exact smaller children with OR aggregation and unit source replication. The remaining difficulty is no longer merely finding small cones; it is finding an all-input hereditary witness partition whose cones fit (N^eta) and whose source replication fits the narrow (N^{0.1}) surplus. This is a precise load-bearing target, not a proof of class separation. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
