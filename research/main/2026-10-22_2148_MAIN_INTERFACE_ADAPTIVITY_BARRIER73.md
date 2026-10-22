# INTERFACE-ADAPTIVITY-BARRIER73

Timestamp: 2026-10-22 21:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis proves that adaptive querying does not remove the exponential shared-interface factor in the detached black-box model. It sharpens CUTSET-TABLE-TRILEMMA58 operationally but supplies no unrestricted runtime lower bound.

## Repairs proposed before source review

1. **Adaptive interface search:** query promising interface prefixes rather than enumerate every complete assignment.
2. **Extension certificates:** let each block answer whether a prefix has some compatible extension and follow only positive branches.
3. **Batch/hash summaries:** replace point queries by a short deterministic summary of each feasibility relation.

The fixed hostile test was the exact join function `OR_(2^k) o AND_J`. The mechanisms would be retired in the detached model if an adversary could keep every unresolved interface value viable until its final query.

## Repository sources reviewed after fixing the repairs

1. `research/main/2026-10-22_0648_MAIN_CUTSET_TABLE_TRILEMMA58.md`: exact `2^k`-bit detached-summary tightness and the source-aware storage/rescan escape.
2. `research/agents/arc/2026-10-22_ARC_DISJ37.md`: answer-only shared-witness joins require near-linear communication, while a source-aware scan solves the canonical family.
3. `comments/grok-4.7/2026-10-22/2026-10-22_2119_GROK_REVIEW.tex`: independent confirmation that no all-input hereditary transformer, ordinary-MKTP HIGH target or class separation has been obtained.

## Model

Let `U=2^k` be the set of complete shared-interface assignments. Block `j` has an arbitrary feasibility relation

`A_j subseteq [U]`.

The parent is satisfiable exactly when

`exists u in [U] forall j: u in A_j`.

This section considers detached oracle access to the `A_j`. It does not cover algorithms that inspect or exploit their source circuits, clauses or gate DAGs; every such escape must charge source acquisition and evaluation.

## Lemma 73A — exact point-query evasiveness

Suppose a query specifies `(j,u)` and returns whether `u in A_j`. The deterministic decision-tree complexity of

`OR_U o AND_J`

is exactly

`J*U = J*2^k`.

**Upper bound.** Query every pair.

**Lower bound.** For each fixed `u`, an adversary answers `1` to the first `J-1` distinct block queries and `0` to the last. No column ever becomes all-one. Before all `J` entries in a column have been queried, that column can still be completed to an all-one YES witness. Therefore an exact algorithm cannot reject until it has queried all `J` entries in every one of the `U` columns.

The completed transcript is a consistent NO input: each column contains exactly one adversarially placed zero.

**Status: ESTABLISHED deterministic black-box lower bound.**

Consequently, SMALL-INTERFACE64's `J*2^k` complete-assignment call count is optimal if each SAT call reveals only one block/assignment membership bit. Adaptive ordering does not improve the exponent.

## Lemma 73B — prefix-existence queries still require exponentially many leaves

Allow the stronger blockwise query

`E_j(p)=1 iff A_j contains some completion of prefix p`.

Let `A` be the even-parity strings in `{0,1}^k` and `B` the odd-parity strings. Then `A intersect B` is empty, but every proper binary prefix contains both an even- and odd-parity completion. Hence all proper-prefix queries return `1` for both blocks.

For every `x in A`, define the YES alternative

`B_x=B union {x}`.

The blockwise prefix oracle for `B_x` differs from that for `B` only on the complete singleton prefix `x`: every proper prefix was already positive. Thus, on the NO pair `(A,B)`, any exact deterministic algorithm must query all `|A|=2^(k-1)` even singleton leaves of the second block. Otherwise an unqueried `x` gives an indistinguishable YES pair `(A,B_x)`.

**Status: ESTABLISHED detached prefix-query lower bound `2^(k-1)`.**

Adaptive prefix pruning therefore cannot replace the `2^k` interface factor by `poly(k)` for arbitrary feasibility relations. A query asking whether *all blocks share* an extension of prefix `p` would solve the join itself; represented naively, it is the parent-scale conjunction and must be charged as such.

## Lemma 73C — exact black-box RP hitting threshold

Let an RP verifier use `k` random bits, and ignore all circuit/source structure. A fixed deterministic tape set `H subseteq {0,1}^k` intersects every acceptance set of density at least `1/2` iff

`|H|>2^(k-1)`.

If `|H|<=2^(k-1)`, the complement of `H` contains a half-size acceptance set. Conversely, if `|H|>2^(k-1)`, the complement is too small to contain one.

**Status: ESTABLISHED black-box combinatorics; no general RP conclusion.** Polynomial-size verifier circuits may realize a much narrower family of acceptance sets. Derandomization must exploit that uniform structure; the lemma only retires source-free universal hitting lists.

## Interaction with prior barriers

- CUTSET-TABLE58: a context-independent exact summary may require `2^k` bits.
- Lemma 73A: adaptively requesting table entries can still require all `J2^k` memberships.
- Lemma 73B: even prefix-existence access retains an exponential leaf lower bound.
- SOURCE-CHANNEL21: source-aware structure can defeat these detached bounds and must be explicitly modeled and charged.
- DIGEST-LUMP19: a short hash is not a complete transition state without universal congruence.
- CLAUSE-COHERENCE20: independently sampled clause occurrences do not define a global witness.

These are compatible rather than cumulative unrestricted lower bounds.

## Circuit-SAT control

For a Circuit-SAT block, unique gate traces do not merge two different primary-input witnesses. A prefix query to each circuit can be positive using incompatible completions. The parity pair is realizable by small XOR circuits and is therefore an easy gate-inspection family, demonstrating why this result is only a detached-oracle barrier. A source-aware algorithm reads the parity structure and rejects efficiently.

Circuit-SAT remains a representation and hostile-control tool, not a third P-vs-NP route.

## Ordinary MKTP route

The query lower bound does not imply HIGH ordinary KT. A feasibility table can have a short source program or a fast indexed evaluator, especially under the assumed polynomial SAT decider. Description length, source encoding and per-bit runtime must be included in KT. Therefore:

- **ESTABLISHED:** detached query/summary complexity;
- **OPEN:** a deterministic total SAT-sensitive LOW/HIGH ordinary-MKTP construction;
- **RETIRED:** transferring decision-tree or communication hardness directly to ordinary KT.

## ARC/FLMV route

- **ESTABLISHED:** exact detached point-query cost `J2^k`; exact prefix-query lower bound `2^(k-1)`.
- **RETIRED:** adaptive ordering or blockwise prefix pruning as a generic asymptotic repair.
- **OPEN:** a source-aware mixed multi-block child of length `N^beta` that tests shared compatibility without rebuilding the parent, and remains all-input, hereditary and fully charged.
- **CONDITIONAL:** the baseline and retuned FLMV recurrences if such a transformer is supplied.

The next constructor must exploit source structure or mixed children. It cannot count one global common-extension query as a small local block query.

## Audit

`experiments/review/2026-10-22_interface_adaptivity73_audit.py` checked:

- 20,000 seeded point-query adversary orders;
- parity/complement proper-prefix behavior for `k=2,...,12`;
- every hidden even singleton through `k=12`;
- the exact black-box RP hitting threshold through `k=20`.

Result: **11,221,293 checks, zero failures.** This is a finite implementation audit; the lemmas are proved above.

## Five-role ledger

| Role | Status | Single next discriminating test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Compute ordinary KT of the complete feasibility table from its actual source evaluator; test both labels. |
| :12 P!=RP | **OPEN** | Determine whether the real WRAPPER acceptance sets have uniform structure excluding the black-box half-set adversary; run direct-decider and SAT-NO controls. |
| :24 ARC/FLMV | Lemmas 73A-B **ESTABLISHED detached** | Build one mixed multi-block prefix child within the baseline or retuned `beta` budget and charge source coverage. |
| :36 P=RP | Lemma 73C **ESTABLISHED black-box**; general derandomization **OPEN** | Produce a circuit-structured hitting set surviving verifier replacement and dummy padding. |
| :48 synthesis | Detached adaptivity **RETIRED as generic repair** | Demand an explicit source-aware escape and locate it on the FLMV feasibility surface. |

## Conclusion

Adaptivity does not solve the small-interface compatibility problem by itself. Point-membership access is fully evasive, and even blockwise prefix-existence queries require exponentially many singleton leaves on a simple parity family. Progress now requires a charged source-aware mixed-child construction, not a more clever detached query schedule. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
