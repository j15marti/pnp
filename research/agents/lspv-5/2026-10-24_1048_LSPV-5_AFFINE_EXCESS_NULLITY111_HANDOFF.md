# LSPV-5 handoff — AFFINE-EXCESS-NULLITY111

**Status:** P versus NP remains OPEN. This run adds a constructive parameterized upper bound and retires a scalar lower-bound inference.

## Exact new theorem

For a mixed instance `E ∧ B`, where `E` is an explicit system of GF(2) equations and `B` is unit/binary CNF:

- let affine component `i` have nullity `d_i`;
- let `e_i = max(d_i - 1, 0)`;
- build the interaction graph on affine components using cross-component clauses of `B`;
- for interaction cluster `C_j`, let `K_j = Σ_{i∈C_j} e_i`.

Charged Gaussian elimination, enumeration of the `K_j` excess basis bits, and SCC on each child decide the instance in

`P_parse+GE(N) + Σ_j 2^{K_j} P_sub+SCC(N_j) + P_replay(N)`

with polynomial peak space under serial depth-first execution. Fixing `d_i-1` basis bits leaves every source variable constant, the sole surviving component bit, or its negation, so every binary clause remains Krom. Interaction clusters factor, hence their costs add rather than multiply.

Consequences:

- `d_i ≤ 1` recovers Role 4's polynomial quotient.
- `max_j K_j = O(log N)` is polynomial even when total `K = Σ_j K_j` is linear.
- For the connected nullity-two graph-colouring endpoint, `K_1 = |V|`, yielding a `2^|V| poly(N)` upper bound only.
- Large total `K` is not a lower bound: `q` independent nullity-two clusters have `K=q` but admit `O(q)` local decisions on matched SAT and UNSAT controls.

## Independent peer audit

- Role 4 AFFINE-NULLITY-BOUNDARY73: nullity-one quotient and odd-XOR3/NAND parsimonious 3-colouring endpoint verified.
- Role 4 LOCAL-AFFINE-JOIN74: exact local relation `∃x,y[...] = p' ∨ (p ⊕ b)` verified; the linked `q=2,b=(1,0)` counterexample correctly invalidates independent local projection; SCC recovery of the shared switch is sound.
- Role 3 PARITY-SHORTCUT-FIREWALL78: used as a guard against mandatory Resolution/DNNF output.
- Fixed-width implication chain: retains exactly `q` orientation-field queries on the all-one input, but only in the declared field/record access model.

## Adaptive state ledger

| Before | Acquisition | Rule | After/correctness | Charged resources |
|---|---|---|---|---|
| Raw source | Full parse and validation | Build affine components | Explicit equation/binary representation | Source reads, storage, failed recognizer |
| Affine representation | Gaussian ranks/bases | Build interaction graph | Profile `(K_1,…,K_s)` | Elimination, policy evaluation, graph storage |
| Cluster, unknown label | Enumerate excess coordinates; SCC | Serial child/cluster solve | SAT witness or all-child failure for a cluster | Every child, switch, reconstruction/replay; polynomial peak space |
| Independent controls | Observe no cross-cluster edges | Local four-state solve | Exact SAT/UNSAT in `O(q)` | At most `4q` local state tests |
| Unsupported CNF | Recognizer failure | Exact DPLL fallback | Total exactness | All failed work and fallback charged |

SAT may stop at one successful child and reconstruct one witness. UNSAT exhausts children of a failing cluster but need not emit a proof system object. This is a restricted policy, not all-decider coverage.

## Reproducible evidence

- Script: `research/agents/lspv-5/2026-10-24_1048_AFFINE_EXCESS_NULLITY111_audit.py`
- Raw: `research/agents/lspv-5/2026-10-24_1048_AFFINE_EXCESS_NULLITY111_raw.json`
- Seed: `202610241048`
- 593 assertion-accounted checks, zero failures, 0.557328 seconds.
- 500 random affine-plus-binary instances checked against complete basis enumeration: 193 SAT, 307 UNSAT.
- All 75 labelled graphs through four vertices checked against direct 3-colour enumeration and the affine/NAND endpoint: 74 SAT, one UNSAT (`K_4`).
- Matched easy SAT/UNSAT controls at `q=8,64,512` have `K=q`, edgeless interaction graphs, and at most `4q` local state tests.
- Code SHA256: `a0f3dc425061308a04a54c2d02159005900e843201a60aaafa2364fb495b5105`
- Raw SHA256: `1d60f7309b15c2e0dd934791c4184e1a4c5713a8c28c4074ba83c8bb21687ef5`

Finite evidence corroborates the implementation and bookkeeping only.

## Transport and coverage

For a source lower bound `L`, reduction/recognition `R`, other overhead `H`, `Q` target calls, and model factor `τ`, the only valid remainder is

`T_new^{≤}(g(n)) ≥ (L(n)-R(n)-H(n))/(Q(n)τ(n))`

when the numerator is positive and models match. The chain source has only an input-order field-query bound, consumed by explicit linear construction; no superlinear remainder results.

Classification:

- **PROVED/EXACT restricted query bound:** chain field acquisition.
- **PROVED/EXACT enumeration upper bound:** clustered excess-nullity theorem.
- **KNOWN NP-completeness + proved reduction:** connected nullity-two affine/NAND endpoint.
- **FALSIFIED/RETIRED:** `K` alone forces `2^{Ω(K)}` work.
- **OPEN:** any unconditional `2^{Ω(max K_j)}` bound for every total uniform exact adaptive decider.
- **OPEN:** unrestricted deterministic superpolynomial SAT lower bound.

## First missing lemma

For one explicit connected NP-complete family, prove a representation-neutral charged work theorem covering every total uniform exact state-adaptive policy after allowing Gaussian/SCC/Horn recognition, local projection, decomposition, branching, clause learning, caching, restarts, recomputation, source rereads and direct decision. It must survive the cluster-profile collapse proved here.

Roles 1–3 should use the independent nullity-two SAT/UNSAT controls against any scalar residual or fixed-strategy potential. Role 4 should next build a connected two-label family that defeats factorization and source-readable shortcuts without presuming enumeration.
