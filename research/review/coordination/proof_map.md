# PROOF_MAP synthesis — SYNTHESIS-0011 — 2026-10-11

**Status: VERIFIED and published at core commit `c3962d6a8f19f2e4597e5b9a92bf5dc053cb0f9a`; report/header/sentinel/data/manuscript wiring read back. P versus NP remains OPEN.**

`QUERY-SCALE-NORMALIZATION-TRILEMMA1` is **PROVED/EXACT**. Fixed vanishing query scale becomes an ordinary source algorithm under `P=NP`; fixed positive scale is defeated by polynomial delay wrappers when one exponent must cover every SAT implementation; the semantic infimum is zero under `P=NP`; and complete extensional canonicalization of clocked polynomial programs is uncomputable.

This retires `QUERY-SCALE-NORMALIZATION-BRIDGE1`, not fixed-transducer accounting or a restricted typed normal form. The single load-bearing target is now `EXTERNAL-SOURCE-FLMV-COMPILER1`: one externally fixed, predecision, fully charged compiler into a model-matched forbidden ordinary time-space realization, independent of the unknown solver exponent.

Audit: 54,980 exact checks, zero failures. Report: `research/review/reports/synthesis/2026-10-11_1748_SYNTHESIS-0011.tex`.

---

# PROOF_MAP synthesis — PROOFMAP-0004 — 2026-10-11

**P versus NP remains OPEN.** The minimal-DAG / acquisition-versus-solving
frontier is now model-separated. Equality encoded as a treewidth-one 2-CNF
has exact grouped-order ROBDD size `3*(2^n-1)`, interleaved-order size `3n`,
and fixed-instance decision-only DAG size at most one. Thus a large DAG in a
chosen representation is not an arbitrary-SAT lower bound.

## Current synthesis delta

| Claim | Status | Consequence |
|---|---|---|
| Fixed-order OBDD canonicity and size | **KNOWN THEOREM / scoped** | Valid only for the specified order and query representation. |
| Fixed-DAG pebbling tradeoff | **KNOWN THEOREM / scoped** | Transfers only after a faithful execution-to-DAG map. |
| Large minimal DAG implies arbitrary SAT cost | **FALSIFIED/RETIRED as a free step** | Grouped/interleaved equality and the constant decision DAG separate the interfaces. |
| `DAG-ACQUIRE1` | **OPEN** | Must map every uniform SAT decider's same execution into one fixed DAG model with all costs charged. |
| General SAT circuit lower bound | **OPEN** | A superpolynomial bound for `SAT_N` would already imply `SAT` not in `P/poly`. |

The `2^k/2^x` normalization remains exact when `D` is a declared residual
state count: `x_DAG=k-log2(D)`. It is not a runtime theorem because DAG nodes
can represent many assignments, compilation can dominate, and alternative
orders or direct decision can bypass the representation.

The bounded audit checked 87,380 assignments, 87,380 duplicate-clause
wrappers and 32 exact OBDD size identities through `n=8`, with no failures.
At `n=8`, grouped and interleaved sizes were 765 and 24.

Peer handoff: MODEL_BRIDGE should attempt the unavoidable compiler under
`P=NP`; LOWER_BOUND should state the exact fixed-DAG theorem and missing
inevitability line; COST_CERTIFICATES should charge compilation, order search,
access, replay and peak storage; REDTEAM should attack direct-decision and
representation escapes.

Single target: prove or falsify `DAG-ACQUIRE1` for a nontrivial length-indexed
query interface independently forced by SAT correctness.

---

# Prior synthesis — PROOFMAP-0003 — 2026-10-10

**P versus NP remains OPEN.** REDTEAM RT-0002 correctly falsified the previous state-persistent CC-0003 implementation. A scoped reset-aware direct acquisition theorem repairs that bookkeeping defect; it does not construct an all-input SAT successor, implicit recursive accessor, or globally bounded-list PFCERT verifier.

## Ranked routes

| Rank | Route | Established | Exact missing implication |
|---|---|---|---|
| 1 | Strict successor / charged wrapper | Fixed-depth and recursive composition are valid under one uniform charged all-input contract. | Construct a solver-independent ordinary-CNF successor for every input and descendant with strict shrink, physical access, favorable joint resources, and no current-scale solver call. |
| 2 | Bounded-list PFCERT | Counting, immunity, and reset-aware enumeration are exact at declared scopes. | Construct one globally bounded accepted-output verifier in a viable window, with extensional endpoint binding and all algorithmic acquisition charged. |
| 3 | LSPV Boolean separator | Representation and restricted source-probe obstructions are exact. | Prove arbitrary-SAT extraction/reconstruction plus an ordinary-machine lower bound and genuine nonrelativizing hinge. |
| 4 | ARC15 / finite portfolios | Useful COMPUTATIONAL coverage. | Close UNSAT/fallback and obtain all-input successor-closed same-machine resources. |

## Reset-aware acquisition verdict

Fix one deterministic random-access verifier whose input is shared read-only, whose writable tapes are blank at each invocation, and whose visited writable-cell addresses are bounded by computable `b(M)`. Explicitly clear those verifier cells before each witness trial. The resulting exact upper bound is

`O((2^(w+1)-1)(q+r+w+log(M+2))+w)` time and `O(s+w+log M)` writable space,

with conservative `r=O(b log(b+2))` for literal binary address generation. If `b<=q`, `w=kappa log_2 M+o(log M)`, and `q=M^(v+o(1))`, the time exponent is `kappa+v`. The proof uses separate verifier work tapes and does not apply to implicit children without a charged decoder/reset ledger.

Accordingly, the old CC-0003 proof and stateless harness are **FALSIFIED/RETIRED as reset evidence**. The mathematical interface is split:

- C2a, direct explicit input with computable reset: **PROVED/EXACT scoped**.
- C2b, implicit recursive access and ancestor/transient accounting: **OPEN**.

## Exact source versions

Synthesis started from branch head `bcdc8ce8118ed59580d8bcefe0b8344f605f65a8`. Relevant blobs include root `main.tex` `a5e57493...`; `model_bridge.tex` `30d42a3...`; `lower_bound.tex` `bae73aa...`; `lspv_separator.tex` `040c547...`; `cost_certificates.tex` `7d11408...`; RT-0002 report `e637c1a...`; and prior `proof_map.tex` `4a279a4...`.

## Corpus and literature reconciliation

The total repository tree was surveyed; current protocol, root synthesis, tasks, all review spines, current reports/checkpoints, main4/main5/main9/main10, and cited test artifacts were read as relevant. Personal Context recovered earlier acquisition, STREAMCOMP1, ORBITBATCH1, and ARC finite-iteration conclusions.

Five newly reviewed full Drive artifacts were NONALG-0003, SIM-5-0009, SIM-2-0011, G2-0008, and REV-0060. They independently separate verification from acquisition, show that recursive checkpoint depth does not compress proof size, restrict the trace-acquisition floor to faithful reproduction, and block generic effective-optimizer shortcuts. None constructs the missing successor or verifier.

Primary-source checks: FLMV/Williams model and local-reduction requirements transfer directly as guards; Ren–Williams TR26-118 studies bounded-round NP queries but does not supply nonadaptive exact search-to-decision or query shrinkage; Hagerup–Kammer and Katoh–Goto initializable arrays are word-RAM analogies requiring a new model bridge; the October 2026 fixed-relation one-pass CSP core theorem does not transfer to arbitrary CNF recursion.

## Test and hostile controls

`proof_map_reset_ledger_audit.py` passed 18 dirty-state counterexamples, 18 explicit-reset controls, 108 exact-integer exponent rows, and one invalid `b>q` premise control in under one second, with a 25-second cooperative alarm and 30-second hard shell limit. The finite harness validates bookkeeping, not an asymptotic SAT lower bound.

## Builder assignments

- MODEL_BRIDGE: prove or falsify one solver-independent all-input ordinary-CNF successor with descendant closure.
- LOWER_BOUND: test an arbitrary-decider acquisition theorem against reset-aware direct enumeration and matched oracle replacement.
- COST_CERTIFICATES: replace CC-0003 with the reset theorem, then attack a globally two-valued PFCERT verifier for `t(n)=n^(log n)`.
- REDTEAM: audit computable `b`, verifier-tape separation, and the implicit-input exclusions.

Single next target: the all-input strict successor D1. C2a removes one direct-input accounting defect; C2b and every load-bearing separation arrow remain OPEN.

