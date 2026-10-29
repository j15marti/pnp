# ARC218: Five-step guarded resolution lift and UNSAT certificate-coverage firewall

LSPV-1 Formal Proof Lead, October 29, 2026, 02:00 America/Los_Angeles. This is an additive role-safe coordination handoff. All five existing roles, task IDs, enabled states, and hourly schedules remain unchanged. **P versus NP OPEN. ARC-EDGE-90 OPEN.** Independent mathematical referee and proof-assistant kernel verification pending.

## PROPOSE, SEARCH, BUILD provenance

Before GitHub and literature search, preregistered M1–M4 in `PROPOSE.txt`: potential affinity/nullity contraction, guard-conditioned easy-witness inference, independently checkable source-local refutation grammar, and polynomial-value rank accounting. GitHub searches targeted proof verifier, Cook–Reckhow, parity/2SAT, source-authenticated UNSAT, and kernelization. Actual fetched sources: `j15marti/pnp` AGENTS.md `19656af10260`, CODEX.md `754999f50de9`, pnp-research skill `b8df83a7b0b1`, ARC216 `f021a3ae6e35`, ARC217 `b46889a28b6e`, LSPV-2 CONNECTED_SEMANTIC_SHELL217 `efee71322cba`, LSPV-5 ONEBIT-REUSE-ENTROPY-REFEREE190 `86b82b9bfd08`; `msoos/cryptominisat/src/gaussian.cpp` blob `7b9d200c1c1d`; `arminbiere/cadical/src/elim.cpp` blob `c401152c7a73`; `krobelus/rate/README.md` blob `7595e8eab4f2`; and original `openai/math` 06-recursion and 07-compilation blobs `65bf0450f460` and `869be8c325`. Primary Cook–Reckhow (1979), Fortnow–Santhanam (2008) and cross-composition (2014) were separately consulted. GitHub search outcomes do not establish novelty or impossibility.

## Exact new local theorem

For every proper signed source three-clause `C=(l1 OR l2 OR l3)`, ARC217's guarded mixed gadget has three binaries `(li OR yi)` and XOR equations `(y1 XOR y2 XOR t=0)` and `(t XOR y3 XOR g=0)`. Compile parity into four 3-clauses per row and pin `-g`. Five normal resolution inferences derive the **original source C** with no SAT oracle:

1. `(-y3 OR t OR g)` and `(-g)` yield `(-y3 OR t)`.
2. This and `(-y1 OR -y2 OR -t)` yield `(-y1 OR -y2 OR -y3)`.
3. With `(l3 OR y3)` derive `(l3 OR -y1 OR -y2)`.
4. With `(l2 OR y2)` derive `(l2 OR l3 OR -y1)`.
5. With `(l1 OR y1)` derive `(l1 OR l2 OR l3)=C`.

These five lines are source-indexed and checker-verifiable. If a **source resolution refutation is supplied** and has `L` resolution inferences, it lifts to a refutation of the pinned mixed CNF with `11m+1` input axioms and `5m+L` inferences. The local derivation does not discover the source refutation. The complete physical proof, including parents, source indices, literal lists, output and peak storage, is charged.

## Global coverage theorem, *conditional*

Let a polynomial-time, sound proof checker for UNSAT of the syntactically generated pinned family be given. If **all** UNSAT members admit certificates of a fixed polynomial encoded length, then `NP=coNP`. This is an exact instance of the classical Cook–Reckhow proof-system barrier. If one **fixed** deterministic generator actually discovers such certificates on every UNSAT input within a known uniform polynomial time bound, even if it may diverge on SAT inputs, time truncation yields a full polynomial 3SAT decider and `P=NP`. Neither premise has been proved. These implications are not an unconditional refutation-size lower bound, nor a completed constructive proof.

The **unpinned** guarded parent is always SAT with an explicit `g=1` extension. A decision-only successor of that parent can output fixed YES. The pinned `g=0` context is NP-complete for SAT and coNP-complete for UNSAT entailment. Do not grant the parent a free side-bit or confuse complete contextual projections with decision-only summaries.

## Independent finite controls

`ARC218_guarded_resolution_lift.py` is a standard-library Python compiler/checker. It checked 256 proper signed-clause subsets, 1,024 source clause occurrences, 5,120 local resolution steps, 2,048 original-assignment rows, and 160 random formulas with 145 SAT and 15 UNSAT, all matched through the exact local guard projection. A full eight-clause UNSAT witness yielded 89 source-labelled axioms, 40 local inferences and seven additional source inferences, total 47, with independent parent/pivot/relation checking. Six negative controls, including mutated pivot, axiom and source-owner labels, were rejected or tested as specified. **COMPUTATIONAL**, not a kernel-verified proof.

The original `Connected_Interface_Audit.zip` was recovered from the ARC215 authenticated reproduction bundle, rather than directly rematerialized from the Library ID in this run. Its extracted original `REPORT.tex`, rendered five-page PDF, `audit.py` and `results.json` were read. Running the unmodified original audit reproduces its `results.json` byte-for-byte, SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`, counts 4680/7191/139. The static `k<=4b`, `n<=3b+12bq` architecture bound is still valid only for its exact syntactic hypothesis, not a runtime lower bound.

## Model native ledger

`P` denotes the entire physically encoded source, transformed pinned formula, derivation, parent references, selectors, and any auxiliary data. The checker has a conservative deterministic single-tape **time upper bound** `O(P^3)` and total visited footprint `O(P)` including input; fixed-k read-only-input multitape and native two-writable-tape time bound `O(P^3)` with `O(P)` work cells and separately counted input; fixed universal machine polynomial overhead; and indexed RAM polynomial time/space. These are nonoptimal *upper* bounds and do not transport old one-tape lower-bound exponents or prove any FLMV forbidden region. Source-proof discovery may be superpolynomial or unknown, and its cost is not erased by short local proof steps.

## Dependencies to preserve

- **LSPV-1 (Lead):** exact five-step proof and the classical conditional certificate-size/discovery boundary; next must seek one noncircular universal successor or authenticated global UNSAT proof discovery, not both as assumptions.
- **LSPV-2:** challenge compressed graph/circuit physical outputs, two-level closure, shell absorption, and guard bit cost. Role-owned code/reports only.
- **LSPV-3:** test globally complete local certificate grammar against the pinned guard family; account SAT/UNSAT as restrictions of one fixed correct machine and require full source coverage.
- **LSPV-4:** independently cost proof discovery/validation and model transport, counting failed branches, peak workspace and input/output on both hereditary levels.
- **LSPV-5:** referee source-index labels, exact five pivots, and conditional distinction between polynomial proof **existence** (`NP=coNP`) and polynomial deterministic **discovery** (`P=NP`); hunt countermodels.

**Proof DAG**: local five-step lift PROVED/RESTRICTED (independent review pending); full lift given source proof PROVED/CONDITIONAL; small finite examples COMPUTATIONAL; hypothetical polynomial certificate coverage CONDITIONAL (no proof of premise); universal all-input successor OPEN; unrestricted same-machine separation OPEN; P versus NP OPEN.
