# Search-G Precommitment Proof Spine

**Timestamp:** 2026-10-01 11:58 PT  
**Status:** PROVED/EXACT model lemmas + OPEN superpolynomial-resource bridge.  
**Global status:** P versus NP remains OPEN.

This is a formal supplement to `research/explorations/search-spine/2026-10-01_FP-FNP_PARALLEL-PROOF-SPINE.tex`.

## 1. Parallel search spine

Assume for contradiction:

`P = NP`

Then, under the project search convention:

`FP = FNP`.

Hence for a fixed candidate relation `R* in FNP`, there is a deterministic polynomial-time selector `S` producing a valid witness `y = S(x)`.

The intended causal chain is:

`P=NP -> FP=FNP -> S in FP -> SAME_REALIZATION record X -> commit state before future G bits -> delayed future audit -> STORE or REACQUIRE -> superpolynomial resource -> contradiction.`

Everything through STORE-or-REACQUIRE is a model theorem once the record, cut, and audit family are validly constructed. The superpolynomial step is OPEN.

## 2. Causal cut and future source

Let the true-random source be an IID fair bitstream `G = (R1,R2,...)`.

At a declared cut time tau, the SAME_REALIZATION selector execution has produced an ephemeral record `X in Xspace` and retains persistent state `P(X)` of `s` bits. A free side channel `Z(X)` may take at most `2^r` values.

Only after the cut, a fresh `b`-bit block

`B = (R_(tau+1), ..., R_(tau+b))`

is released.

The block selects a delayed query, and the required response is a function `f_B(X)`.

Operationally, the future block is not visible before the cut.

## 3. PROVED/EXACT — existential future-guessing lemma

A standard NDTM does not literally read future bits. However, before `B` is revealed it can nondeterministically guess a string `Bhat in {0,1}^b`, and after the reveal reject branches with `Bhat != B`.

For every realized future block `B`, one computation branch has `Bhat = B`.

Therefore:

`Pr_B[ exists Bhat such that Bhat = B ] = 1`.

If `b = poly(n)`, that successful branch uses only `b` nondeterministic guess bits. The fact that there are `2^b` total branches does not make the nondeterministic running time exponential.

### Proof

The NDTM branches once for each guessed bit. Each path contains only `b` guessing steps. After the actual block appears, it compares the guessed string to the real block and rejects on mismatch. Exactly one guessed string equals every realized `B`. Nondeterministic time charges a single path, not the total number of paths.

### Consequence

The implication

`future branch unknown -> NDTM must enumerate all branches`

is false for polynomially many future bits.

## 4. PROVED/EXACT — quantifier-order separation

For one fixed precommitted guess `Bhat`,

`Pr_B[Bhat = B] = 2^(-b)`.

But:

`Pr_B[ exists Bhat : Bhat = B ] = 1`.

So these are fundamentally different:

`for every realized B, there exists a lucky branch`

versus

`there exists one choice/state fixed before B that works for future B`.

The proof program needs the second causal order.

## 5. Branch-complete response signature

For each possible pre-cut record `X`, define its complete future-response signature:

`Sigma(X) = ( f_B(X) ) over all B in {0,1}^b`.

This is only a semantic definition; the vector does not need to be explicitly materialized.

Two records are future-audit equivalent exactly when their response signatures are equal.

For a side-information value `z`, define:

`N_z = number of distinct Sigma(X) among records with Z(X)=z`.

## 6. PROVED/EXACT — branch-complete precommitment theorem

Suppose one `s`-bit persistent state is committed before `B` is revealed, and after the reveal the system must output `f_B(X)` correctly for every possible future block `B`, without receiving any additional information depending on `X`.

Then:

`s >= log2( max_z N_z )`.

If `X` ranges over `{0,1}^K`, the side channel has at most `2^r` values, and the response signature is injective inside a largest side-information fiber, then:

`s >= K-r`.

### Proof

Fix a side-information fiber `Z(X)=z`. Suppose two records `X` and `X'` in that fiber have different response signatures but the same persistent state.

Because their signatures differ, some future block `B` satisfies `f_B(X) != f_B(X')`.

After that same `B` is revealed, both executions have identical persistent state, identical side information, and identical challenge. If no new `X`-dependent information enters, every later deterministic routed step is identical, so both executions produce the same response. They cannot both be correct. Contradiction.

Therefore every distinct response signature in the fiber requires a distinct persistent state, so `2^s >= N_z` for every `z`.

For the `K-r` corollary: at most `2^r` side-information values partition `2^K` records, so one fiber contains at least `2^(K-r)` records. Injectivity of `Sigma` on that fiber gives `N_z >= 2^(K-r)`.

## 7. PROVED/EXACT — branch-count guard

Exponential branch count is not the relevant quantity.

The exact state-counting quantity is:

`number of distinct complete response signatures Sigma(X)`.

If exponentially many future bitstrings ask redundant questions, the response-signature space may still be small.

Also, if `X` itself contains only `K = poly(n)` independent bits, pure information-theoretic storage cannot exceed `K`. Exponential branching cannot manufacture more independent information than the pre-cut record contains.

## 8. PROVED/EXACT — STORE-or-REACQUIRE theorem

If

`s < log2(max_z N_z)`,

then an exact implementation cannot answer every delayed audit using only retained state, side information, routing, and deterministic post-cut computation.

It must obtain additional information depending on `X` after the cut.

This is the contrapositive of the precommitment theorem.

### Critical limitation

Necessity of reacquisition is not a lower bound on reacquisition cost.

If `X` remains available in unit-cost random-access storage, one post-cut reread can answer a coordinate challenge. If `f_B(X)` has a direct polynomial-time recomputation from the original input, the audit may also be cheap.

## 9. RCCN integration

The post-cut computation may route through a deterministic network such as:

`M1 -> M3 -> M1 -> M4 -> ...`

Let `P(X)` include all persistent local states and all persistent messages across the network at the cut.

Cycles do not evade the theorem. Once the complete post-cut global state and challenge are fixed, deterministic routing cannot recreate distinctions about `X` that were not retained or reacquired.

Thus:

`STORE enough branch-complete information OR REACQUIRE X-dependent information later.`

## 10. Search-selector integration

Assume `P=NP`, hence `FP=FNP`, and let `S` be a deterministic polynomial-time selector for one fixed structured FNP relation `R*`.

For input `x`, the SAME_REALIZATION run outputs a witness `y=S(x)` and must causally induce a record `X(S,x,y)` at a declared cut.

The proof may not invent an `X` that the selector never constructs, nor use an uncharged extractor.

Fresh `G` bits released only after the cut select the audit family `{f_B}`.

The exact local conclusion is:

`persistent state >= log2(max_z N_z) OR the run must later reacquire X-dependent information.`

## 11. Why G is a proof device, not a new FNP problem

The underlying search relation remains ordinary polynomial-time-verifiable `R*(x,y)`.

The future random source is used externally to audit a purported polynomial-time selector after a causal cut.

We do **not** redefine the search problem into an alternating game such as:

`for all B1 exists y1 for all B2 exists y2 ...`.

That would be a different complexity problem, closer to online/alternating computation.

## 12. Strengthened parallel proof spine

1. `P = NP`.
2. Therefore `FP = FNP`.
3. Fix one structured `R* in FNP`; there exists a polynomial-time selector `S`.
4. The SAME_REALIZATION execution of `S(x)` causally creates a declared record `X`.
5. Before fresh future bits exist, commit all persistent state.
6. Fresh `B` chooses which delayed function `f_B(X)` is required.
7. Exact theorem: either persistent state distinguishes all necessary response signatures, or post-cut `X`-dependent reacquisition is necessary.
8. OPEN: prove a model-matched lower bound

`S_persistent + C_communication + w*Q_reread + C_recompute + C_sequential > |x|^c`

for every fixed `c` on some input, for every correct selector implementation.
9. Then `S` is not polynomial-time.
10. Therefore `R* notin FP` while `R* in FNP`.
11. Hence `FP != FNP`.
12. Therefore `P != NP`.

## 13. Why the open arrow is difficult

A successful construction must defeat all of the following.

### Static reread

If the record remains in random-access memory, a delayed coordinate challenge can collapse to one probe.

### Cheap recomputation

If the requested response can be rebuilt directly in polynomial time from the original input and output witness, STORE-or-REACQUIRE does not become a superpolynomial lower bound.

### Branch redundancy

Many future bitstrings may select equivalent questions, so the number of future branches is not enough.

### Selector freedom

For ordinary FNP, the selector may choose any valid witness. A Search-A construction therefore needs an all-witness theorem:

`for every y, if R*(x,y)=1 then the induced dependency object has the required hard property.`

## 14. Candidate sequential strengthening

Because an FNP witness and any explicit pre-cut record are polynomially bounded, a superpolynomial result probably cannot come from one-shot storage alone.

The likely target is repeated causal dependence on an implicit dependency object `D`, with the charged resource:

`R_search-G = S_persistent + C_communication + w*Q_reread + C_recompute + C_sequential`.

The desired theorem is **not**:

`resource >= number of future branches`.

It is instead:

`R_search-G >= L(D)`

for an explicit dependency/sequentiality measure that survives flattening, random-access reread, memoization, pointer jumping, alternative representations, and arbitrary selector implementations.

## 15. Required quantifiers

A full Search-A separation must preserve a form such as:

`exists one fixed R* in FNP, for every selector S, for every constant c, there exists x`

such that if `S` solves `R*`, then the SAME_REALIZATION Search-G/RCCN resource on `x` exceeds `|x|^c`.

The future-audit theorem must use one fixed pre-cut state for all future challenges. It may not choose a different pre-cut state after learning `B`.

## 16. Hostile nondeterminism audit

Keep these three statements separate:

1. `Pr_B[exists lucky branch matching B] = 1`.
2. `For one precommitted guess Bhat, Pr_B[Bhat=B] = 2^(-b)`.
3. `One precommitted state P must answer f_B(X) correctly for every future B`.

Ordinary NDTM existential acceptance naturally permits (1). Only (3) yields the branch-complete state lower bound.

## 17. Strict status ledger

**PROVED/EXACT**

- A standard NDTM does not literally see future bits, but a polynomial-length future can be guessed on one nondeterministic branch and verified later.
- Exponential latent branching alone is not NEXP.
- The quantifier order between retrospective existential branching and precommitment is exact and load-bearing.
- Branch-complete precommitment lower bound: `s >= log2(max_z N_z)`.
- STORE-or-REACQUIRE corollary.
- Response-signature diversity, not branch count, is the relevant information-theoretic quantity.

**CANDIDATE**

- One fixed FNP-complete relation with all-witness hard dependency structure.
- Repeated Search-G/RCCN delayed auditing of an implicit dependency object.

**OPEN / load-bearing**

- A superpolynomial STORE/REREAD/RECOMPUTE/SEQUENTIAL lower bound for every selector implementation.
- A model-preserving staticization/arbitrary-algorithm bridge.
- A nonrelativizing/nonalgebrizing endgame.

## 18. Reusable short statement

**Search-G Precommitment Spine.** Assume `P=NP`, hence `FP=FNP`, and let `S` be a hypothetical polynomial-time selector for one fixed structured FNP relation. At a SAME_REALIZATION causal cut, commit the selector's persistent state before fresh source bits exist. The later source block selects which function of a prior execution record must be produced. Nondeterminism may retrospectively guess the realized future on one branch, so future secrecy alone proves nothing. The exact invariant is instead the number of distinct branch-complete response signatures supported by one precommitted state. If storage is insufficient, the computation must reacquire record-dependent information. The open P-vs-NP-strength step is proving that such reacquisition/recomputation/sequential work is superpolynomial for every correct selector implementation.