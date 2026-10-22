# SOURCE-DEPENDENCY-CONE78

Timestamp: 2026-10-23 02:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis tests whether a single shared source can be compiled once and then reused by many strictly smaller ARC children. Three proposed repairs were fixed before source review: incremental SAT with assumptions, sparse hardwiring of only queried source bits, and a reusable functional-Tseitin source gadget. The sparse repair yields a genuine sufficient condition—a small **static source-dependency cone**—but a one-probe multiplexer falsifies the common inference from few probes per execution to a small standalone child.

## Repairs fixed before source review

1. **Incremental shared source:** keep the parent formula in persistent solver state and issue only small assumption/descriptor queries.
2. **Sparse hardwiring:** for child descriptor (d), embed only source coordinates that its verifier can query.
3. **Reusable Tseitin source gadget:** build the source circuit once and reuse its functional trace across children.

Predeclared falsifier: after conversion to ordinary standalone SAT/Circuit-SAT, either every semantically relevant source bit is fixed inside the child, or leaving it free changes the language; a shared pointer is a different parameterized model.

## Repository sources reviewed after fixing the repairs

1. [PADDING-SELF-REDUCTION-FIREWALL77](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-23_0148_MAIN_PADDING_SELF_REDUCTION_FIREWALL77.md): ordinary self-reduction makes current-scale source-bearing queries; a small exact source evaluator remains OPEN.
2. [SOURCE-SCAN-SCHEDULING69](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-22_1748_MAIN_SOURCE_SCAN_SCHEDULING69.md): one complete source scan per parent is arithmetically affordable only if children can be streamed with one live descriptor and no hidden unfinished state.
3. [Independent review 02:11 KST](https://github.com/j15marti/pnp/blob/main/comments/grok-4.7/2026-10-23/2026-10-23_0211_GROK_REVIEW.tex): no load-bearing implication is closed; a source-aware exact hereditary construction remains the highest-value target.

## Model and dependency notion

Let an explicit source (Fin{0,1}^N), descriptor (d), and witness (z) define a child relation (V(F,d,z)). The intended standalone child label is

[
Psi_F(d)=exists z,V(F,d,z).
]

A set (S_dsubseteq[N]) is an **exact static source cone** if (Psi_F(d)) is determined by (d) and (F|_{S_d}) for every source (F). This is stronger than saying that one realized computation reads few positions.

## Lemma 78A — sparse-cone standardization

Suppose:

1. (|d|,|V_d|le N^{eta+o(1)});
2. an exact static cone (S_d) is uniformly generated with (|S_d|le N^{eta+o(1)});
3. the selected source bits and addresses are acquired and output explicitly.

Then a standalone Circuit-SAT child can hardwire (F|_{S_d}) with encoded length

[
N^{max(eta,eta)+o(1)}.
]

For (Q=N^{alpha+o(1)}) children, explicit output/source work is

[
N^{alpha+max(eta,eta)+o(1)}.
]

Therefore retaining the declared child bound (N^eta) requires (etaleeta). At the baseline ((alpha,eta)=(0.6,0.5)), static sparse hardwiring with (etale0.5) fits the (1.1) output envelope. At the retuned point ((0.595,0.505)), it requires (etale0.505).

This is stricter than the aggregate virtual-probe allowances near (0.605) or (0.6071): those larger allowances cannot be materialized inside (N^eta)-length standalone children. They require a separately justified shared-source/virtual-access model.

**Status: ESTABLISHED sufficient compilation/accounting lemma; construction of such cones for arbitrary SAT remains OPEN.**

## Lemma 78B — per-witness probe count does not bound the static cone

Let (zin{0,1}^{log N}) address a source coordinate and define

[
V(F,z)=F_z.
]

Each fixed witness evaluation makes exactly one source probe. Nevertheless,

[
exists z,V(F,z)=igvee_{j=1}^N F_j,
]

which depends on every source coordinate. Omitting any coordinate (j) confuses the all-zero source with the source having only (F_j=1), although the child label changes.

Hence the valid quantifier is

[
left|igcup_{	ext{all witnesses/branches}}mathrm{probes}(d,z)ight|le N^eta,
]

or a stronger semantic compression theorem—not merely “each witness uses (N^eta) probes.”

**Status: ESTABLISHED exact counterexample. Dynamic-probe-only sparse hardwiring RETIRED.**

## Lemma 78C — arbitrary source tables do not all have small evaluators

For address length (k), (N=2^k), consider fan-in-two Boolean circuits of (s) gates with any of 16 binary gate functions. A coarse upper bound on the number of circuits, including output choice, is

[
(16(k+s)^2)^s(k+s),
]

whose binary logarithm is

[
s(4+2log_2(k+s))+log_2(k+s).
]

There are (2^N) Boolean source tables. Therefore representing every table requires

[
slog s=Omega(N),
]

so some tables need (s=Omega(N/log N)). In particular no fixed (N^eta), (eta<1), evaluator family represents every arbitrary table.

This is a hostile source-table control, not a lower bound for SAT decision: SAT encodings have syntax, and a specialized semantic compiler might exploit it. Such a compiler must be constructed rather than inferred from low dynamic probe count.

**Status: ESTABLISHED counting control; unrestricted SAT compression remains OPEN.**

## Incremental SAT and functional Tseitin audit

### Incremental assumptions

Keeping (F) resident and sending only (d) is a legitimate algorithmic engineering model, but not an ordinary standalone SAT query. To use an arbitrary polynomial SAT decider obtained from (P=NP), one must prove that it supports this persistent interface with charged preprocessing, peak storage, and hereditary reuse. Selecting an incremental solver or treating its state as free advice is not justified.

- Storing an (Theta(N)) compiled source state violates the target (N^{0.5+o(1)}) workspace unless the read-only input model and serialization are matched exactly.
- Rebuilding the state per child restores the (N^{alpha+1}) replay cost.
- A sublinear reusable state is precisely a source-compression construction.

### Functional Tseitin source gadget

A gate trace is unique after primary source values are fixed. Leaving source variables free changes (Psi_F(d)) into an existential statement over alternative sources. Fixing them through equality/unit constraints incurs one canonical constraint per exposed source coordinate. Gate sharing across children helps only in a persistent/common-input model; flattening each child restores the source cone.

**Status: incremental/shared-gadget repair CONDITIONAL in a parameterized model; not an ordinary ARC construction.**

## Circuit-SAT representation control

Circuit sharing can reduce repeated gate bodies, but it does not erase fixed-source information. Any claimed child must publish separately:

- descriptor bits;
- static source cone and how it is generated;
- source bits/addresses embedded in the standalone child;
- auxiliary functional trace variables;
- maximum child length, aggregate acquisition/output work, and peak retained state.

Easy gate inspection and direct source decoding remain mandatory controls.

## Ordinary MKTP/MCSP route

A small static cone yields a short indexed evaluator and therefore naturally supports KT-LOW. The multiplexer family can encode high-complexity tables, but a reduction receiving (F) must count the (N)-bit source description; incompressibility of an externally supplied table does not create the missing deterministic label-sensitive HIGH target.

- **ESTABLISHED:** source-cone bits, addresses, descriptor and runtime belong in ordinary KT.
- **RETIRED:** claiming HIGH from an arbitrary hidden source table or shared solver state.
- **OPEN:** deterministic total both-label SAT-to-ordinary-MKTP generator with correct threshold and same-machine costs.

## ARC/FLMV route

- **ESTABLISHED:** a uniformly generated static cone of exponent (etaleeta) suffices to form standalone children without current-scale source embedding.
- **ESTABLISHED:** few dynamic probes per witness do not suffice; the multiplexer has one probe but full semantic dependence.
- **CONDITIONAL:** shared-source incremental children may exploit the larger aggregate-probe envelope only after a standard-model transfer theorem.
- **OPEN:** construct exact all-input hereditary cones/children for arbitrary SAT without a parent-label call, hidden state, or per-child replay.

This narrows the most constructive surviving arrow: search for a semantic decomposition whose **union dependency cone**, not merely execution trace, is (N^{eta+o(1)}).

## Independent P-vs-RP audit

An RP verifier may read few random bits on each accepting branch while the union over branches covers the entire random tape. Per-path coin sparsity therefore does not yield a uniform hitting set or exact count propagation. A complete small state/cone must cover every original-coin, source, timer, solver and history influence.

- **OPEN (P
e RP):** no explicit unrelativized RP language outside all deterministic polynomial-time machines.
- **OPEN (P=RP):** no uniform deterministic simulator for every RP machine.
- **RETIRED:** per-path low coin access, short digests, high algebraic degree, oracle bounds or finite tests as class evidence.

## Finite consistency audit

The accompanying JavaScript checks the multiplexer union and omitted-coordinate flip controls for (N=2^k), (3le kle16), and evaluates the circuit-count upper bound at (s=lfloorsqrt Nfloor).

Result: **139,478 checks, zero failures.** For this coarse bound, counting already certifies a missing (sqrt N)-gate table from (k=8) onward. This validates the explicit counterexample and arithmetic only.

## Five-role next discriminating tests

| Role | Status | Single next experiment |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | For one candidate target bit, list the full union source cone across all evaluator branches and charge its address/data bits into ordinary KT. |
| :12 P!=RP | SOURCE-CHANNEL21 **ESTABLISHED restricted**; separation **OPEN** | Compute the union of original-source and random-tape coordinates across every accepting WRAPPER branch; run the direct-decider control. |
| :24 ARC/FLMV | Lemmas 78A–C **ESTABLISHED**; transformer **OPEN** | Build one child family with certified static cones of size (N^eta), not merely (N^eta) probes per realized witness. |
| :36 P=RP | per-path sparsity repair **RETIRED**; derandomization **OPEN** | Test whether a proposed quotient is congruent after unioning all original-coin dependency cones. |
| :48 synthesis | sparse-cone interface **CONDITIONAL constructive target** | Reject incremental/shared-source claims until flattened child length or same-model persistent-state transfer is published. |

## Conclusion

Shared-source reuse is not categorically impossible, but ordinary standalone ARC children require more than low per-execution source access. A uniformly generated static dependency cone of size (N^eta) is sufficient and is now the sharp constructive target. The one-probe multiplexer proves that dynamic probe counts alone can hide full (N)-bit dependence; incremental SAT and shared Tseitin gadgets remain different computational models unless their persistent state is fully transferred and charged. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
