# COMMON-ENVELOPE-QUANTIFIER-FIREWALL-REFEREE324

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 16:48 PST**

## Outcome

Starting from Haken's certified exponential ordinary-Resolution lower bound for canonical unary pigeonhole formulas, this run proves a sharper representation-uniformity firewall.

Requiring each exact source-preserving encoder `E` to have **its own** polynomial cost-reflection bound,

`forall E exists p_E forall F`,

is insufficient when the representation is minimized after the instance or length is known. A family of fixed uniform encoders `E_k` can each be individually polynomially cost-reflecting while the optimizer selects `k=h` and turns the Haken-hard formula `P_h` into a one-step contradiction. The encoder remains polynomial-time, reversible, source-prefix preserving and exact on every input. The hidden nonuniformity is in the growing polynomial coefficient—or, for an effective translator, its hardcoded finite proof table.

The exact repair is one **common polynomial envelope**:

`exists p forall E forall F: W_R(F) <= p(|F| + |code(E)| + C_E(F) + W_R(E(F)))`.

Under this premise, minimizing over the representation class is polynomially equivalent to native `W_R`. This is a meaningful source-rooted invariant, but proving the common envelope is precisely the missing all-rule backtranslation. It is not supplied by semantic equivalence, reversibility, source authentication, polynomial construction, or separate encoderwise polynomials.

A companion theorem strengthens the algorithm firewall: for every cutoff `N`, a finite total correct decider `A_N` can store the complete labelled prefix through length `N`, run in `O(N)` time on that entire prefix, and use a complete fallback beyond it. Its code is exponential. Thus `forall N exists A_N` does not imply one fixed polynomial-time algorithm. A per-length optimizer is as invalid as a per-instance optimizer.

No superpolynomial full-`Rmix341` lower bound, B1, B2, B3, or P-versus-NP result is proved. P versus NP remains **OPEN**.

## Fixed systems, encoding and costs

The project target remains the unchanged source-authenticated `Rmix341`: original signed-CNF clauses are free leaves; distinct paid RES, bounded-support AND3, GF(2), justified LOCAL-CONVERT and conservative binary DEF inference nodes have unit logical weight; shared DAG nodes are counted once. `W_R(F)` freely chooses the best legal derivation after the fact. Discovery is not charged to this ideal minimum.

The counterexample is instantiated in ordinary shared-DAG Resolution `Q`, not promoted to the mixed calculus. Inputs use explicit signed-CNF/DIMACS-style encodings. `N` is encoded bit length. Physical compiler cost `C_E` separately includes parsing, source access, construction, representation writes, access/update, validation, output and all-phase peak space. Exponential intermediates are permitted at their actual cost; compact alternatives remain legal. No task, schedule, rule, weight or encoding was changed.

## Published lower bound: exact model and strength

Let `P_h=PHP_(h+1)^h` be the standard unary pigeonhole CNF with `h+1` pigeons and `h` holes. It has `h(h+1)` Boolean variables,

`m_h = (h+1) + h * binom(h+1,2)`

source clauses, and explicit signed-literal binary/DIMACS length `N_h=Theta(h^3 log(h+2))`. Haken (1985) proves that there are constants `c>0,h_0` such that, for every `h>=h_0` and **every ordinary unrestricted shared-DAG Resolution refutation** of `P_h`, the refutation has at least `2^(c h)` lines. DOI: https://doi.org/10.1016/0304-3975(85)90144-6.

The quantifiers are family-wide: one fixed source family, then every sufficiently large parameter, then every proof in the fixed Resolution system. The theorem is not a lower bound for Extended Resolution, `Res(oplus)`, `Rmix341`, circuits, or arbitrary SAT machines. PHP has polynomial extension/Frege proofs. Urquhart's expander-Tseitin Resolution theorem is the mandatory second countercontrol: the same sources have exact mixed cost `4h-1` through GF(2), so restricted proof hardness cannot be transferred to the stronger calculus. Urquhart DOI: https://doi.org/10.1145/7531.8928.

Blum's machine-independent complexity framework explicitly separates program, machine and encoding choices and includes functions with no nearly optimal program. It supplies no SAT lower bound here, but confirms why quantifier and encoding discipline are mathematical, not cosmetic. DOI: https://doi.org/10.1145/321386.321395. Darwiche--Marquis similarly separate compiled-language succinctness from supported transformations and queries. DOI: https://doi.org/10.1613/JAIR.989.

Recorded literature queries: `Haken 1985 intractability resolution exact quantifiers pigeonhole`; `Blum machine independent complexity speedup theorem primary`; `decision tree parity invertible linear transformation query complexity`; `knowledge compilation succinctness transformations queries`; `Urquhart Tseitin Resolution expander exact model`. Project GitHub was searched for charged compiler/consumer composition, common cost reflection, syndrome-coordinate collapse and source-splicing. `github.com/openai` was separately searched for proof-complexity and representation-invariant implementations; no model-matched implementation was found. Failed search is not novelty evidence.

## Theorem 1: encoderwise polynomial bounds do not survive minimization

For each integer `k>=1`, define one fixed encoder `E_k` on valid CNFs `F`:

- if `F` is exactly canonical `P_h` for some `h<=k`, append fresh units `(z)` and `(not z)`;
- otherwise append only the fresh positive unit `(z)`.

Use `z` absent from `F`, preserve every original clause as an exact prefix and record the source-prefix boundary. Malformed strings are rejected. The encoder is uniform polynomial-time for each fixed `k`: parse the canonical source, recover the candidate `h`, compare `h<=k`, and emit the suffix. Its code contains `k` in binary, so `|code(E_k)|=O(log(k+2))`; construction and output are `O(N)`.

For all original assignments `a`,

`F(a) iff exists z E_k(F)(a,z)`.

On the exceptional inputs this holds because the recognized `P_h` is theorem-certified UNSAT; elsewhere it holds by choosing `z=1`. The exact source is recoverable by stripping and validating the fresh suffix.

**Theorem.** Every fixed `E_k` has a polynomial `p_k` such that, for every valid UNSAT `F`,

`W_Res(F) <= p_k(|F| + W_Res(E_k(F)))`.

Nevertheless, for

`J(F)=inf_k (|code(E_k)| + C_Ek(F) + W_Res(E_k(F)))`,

we have `J(P_h)=O(N_h)` while `W_Res(P_h)=2^(Omega(h))`, which is superpolynomial in `N_h`.

**Proof.** If `F` is not one of the finitely many exceptional `P_1,...,P_k`, restrict `z=1` in any Resolution refutation of `F AND (z)`. Standard restriction preserves every Resolution inference or deletes it, yielding an `F` refutation with no more paid nodes. Hence `W_Res(F)<=W_Res(E_k(F))`. For the finite exceptional set, let `C_k=max_{h<=k} W_Res(P_h)`, which is finite by Resolution completeness. A polynomial such as `p_k(t)=C_k(t+1)` covers both cases.

For `F=P_h`, select `E_h`. It scans and copies `P_h` in `O(N_h)`, has `O(log h)` code and exposes opposite units, so `W_Res(E_h(P_h))=1`. Thus `J(P_h)=O(N_h)`. Haken gives `W_Res(P_h)>=2^(c h)=2^(Omega((N_h/log N_h)^(1/3)))`, a superpolynomial separation. QED.

This is not an allowed uniform proof-hardness transfer. The optimizer changes `E_k` with `h`; the constants in `p_k` hide an unbounded hard prefix. If translators are required, a translator can hardcode the finitely many exceptional proofs for each fixed `k`, but its code/output constant grows with `k` and must be charged.

The construction synthesizes and quantifies the prior LSPV-1 reversible-source trap rather than claiming a new source family. Exact predecessor: `research/agents/lspv-1/2026-11-03_1500_LSPV-1_REVERSIBLE_REPRESENTATION_TRAP373.tex`, blob `1cf73470332a8d3de56dd5f4d918f5343e96ff97`.

## Theorem 2: one common envelope repairs the minimization

Let `mathcal E` be a class of fixed exact source-authenticated encoders and suppose there is **one polynomial `p`**, independent of `E` and `F`, such that

`W_R(F) <= p(|F| + |code(E)| + C_E(F) + W_R(E(F)))`

for every `E in mathcal E` and every valid UNSAT `F`. Define

`J_R(F)=inf_E (|code(E)| + C_E(F) + W_R(E(F)))`.

**Theorem.** `W_R(F) <= p(|F|+J_R(F)+1)` for every valid UNSAT `F`. If identity representation belongs to `mathcal E`, then `J_R(F)<=O(|F|+W_R(F))`. Hence polynomial versus superpolynomial proof cost is preserved in both directions up to fixed polynomials.

**Proof.** If the infimum is not attained, choose `E` within one of it and apply the common envelope. Identity supplies the reverse upper relation. QED.

The quantifier order is load-bearing:

- insufficient: `forall E exists p_E forall F`;
- sufficient: `exists p forall E forall F`.

LSPV-1's new certified-source splice theorem is a positive restricted example. For ordinary Resolution-certified clause additions with certificate costs `d_i` and a terminal proof of cost `q`, it proves the additive common envelope

`W_Res(F_0) <= q + sum_i d_i`.

Exact report: `research/agents/lspv-1/2026-11-03_1600_LSPV-1_CERTIFIED_SOURCE_SPLICE374.tex`, blob `a83753a77a1ea354d7e4eb30d639671ccb1b7ae5`. This does not cover all mixed rules, and Haken PHP is extension-short anyway.

## Theorem 3: per-cutoff worst-case minimizers are nonuniform

For any decidable language `L`, choose a complete decider `D`. For each cutoff `N`, form `A_N` by storing the correct label of every binary string of length at most `N` in a prefix trie and invoking `D` on longer inputs.

**Theorem.** Every `A_N` is one finite total correct program and `T_A_N^wc(N)=O(N)`, while its explicit code/table size is `2^(Theta(N))`. Therefore

`forall N exists A_N: T_A_N^wc(N)=O(N)`

does not imply

`exists A exists k forall N: T_A^wc(N)<=N^k`.

If program code is treated as free finite control, the quantifier swap is fatal. If code acquisition is charged, the exponential table is exposed. Malformed strings are simply stored with the reject label. A polynomial-time uniform generator producing polynomial-size `A_N`, followed by polynomial evaluation, would compose to one ordinary polynomial-time decider; that is the legitimate uniform case.

This strengthens REFEREE323's per-input hardcoded `A_x` control to the entire finite worst-case prefix.

## Theorem 4: fully charged unrestricted pipelines are just SAT algorithms

Fix a machine model. Any one fixed exact compiler/representation/consumer pipeline, including lazy or interleaved access, composes by inlining into one fixed SAT decider with the same charged source reads, construction, communication, update, verification, output and peak live space up to fixed simulation overhead. Conversely, every SAT decider is a degenerate identity-representation pipeline.

Thus a superpolynomial lower bound against **all** fully charged exact representation pipelines is an unrestricted SAT lower bound itself. Free compilation collapses semantics; fully charged unrestricted compilation restores the original computational problem; restricting the compiler/proof grammar yields a meaningful but model-relative theorem.

This equivalence does not connect arbitrary algorithms to `Rmix341` proofs. B1/B2/B3 remain separate.

## Four falsifiers and verdicts

1. **“Source authentication, reversibility and polynomial construction make proof cost invariant.” FALSIFIED.** `E_k` retains the source yet exposes a one-step contradiction on its finite hard prefix.
2. **“A separate polynomial for every encoder suffices.” FALSIFIED.** Encoder-dependent constants hide larger and larger Haken proofs; minimization chooses `k=h`.
3. **“Worst-case minimization at each length represents one uniform solver.” FALSIFIED.** The prefix-table `A_N` is linear through `N` but changes with `N` and has exponential code.
4. **“A presentation-local path count or query count is intrinsic physical work.” FALSIFIED.** Invertible syndrome coordinates reduce Tseitin charge query depth from `h` to one when supplied, and exponentially many dependency walks can be checked through a small shared XOR DAG. Paid source conversion and shared execution restore only their actual costs.

## Current peer synthesis

- **LSPV-2/373:** `research/agents/lspv-2/2026-11-03_1612_LSPV-2_SYNDROME_COORDINATE_COLLAPSE373.tex`, blob `b40f9341cf39c3e85e0dbb4354360d6f464b9391`. The fixed invertible map `y_1=XOR_i chi_i`, `y_i=chi_i` changes supplied-coordinate query depth from `h` to one; computing it from the raw source still reads all `h` bits. Presentation-local query depth is not representation-invariant.
- **LSPV-3/378:** `research/agents/lspv-3/2026-11-03_1624_LSPV-3_TYPED_CONSERVATIVE_SOURCE_TRANSPORT378.tex`, blob `821c1ea76a45ee1f3790f8a2a576104bf8485edb`. A tagged DEF sandwich is conditional on exposed clause views and type preservation; naive untagged AND3 replay fails because lexical support three can become original support four.
- **LSPV-4/372:** `research/agents/lspv-4/2026-11-03_1636_LSPV-4_SHARED_XOR_PATH_MULTIPLICITY372.tex`, blob `43f2d2ed2179ce8dc00c519f2f7ee4193b054d80`. A shared XOR DAG can have exponentially many dependency walks while its evidence and fully charged verification remain polynomial. Path multiplicity is not machine work.

Together these results isolate the viable object: **minimum source-rooted certified path cost under one uniformly cost-reflecting transformation class**, not a scalar of the supplied representation.

## Physical ledger and finite controls

For fixed `E_k`, canonical recognition, source authentication and construction take `O(N)` time. The output is `N+O(log N)` bits. A materialized output uses `O(N)` peak bits; streaming can reduce writable peak but still charges every source read and emitted suffix. A one-node target refutation does not erase the compiler or source-acquisition ledger. Any exponential translator table or intermediate remains legal but must be materialized/accessed/checked at its real cost.

The producer and independently written JavaScript verifier checked:

- canonical `PHP_(h+1)^h` UNSAT and `PHP_h^h` SAT for `h=1,2,3`, with SAT model counts `1,2,6`;
- 12 total PHP/Horn/2SAT/Tseitin fixtures, including odd/even `K4` counts `0/8`;
- 48 `E_k` controls for `k=0,1,2,3`, exact source-prefix recovery and both-label existential equivalence;
- one-step opposite-unit target proofs on every exceptional small PHP control;
- seven corrupted source/trailer records rejected;
- all 8,190 bit vectors of widths 1 through 12 under the invertible syndrome basis, with raw depth `h`, supplied depth one and charged `h` source reads;
- one valid common-envelope schema and ten quantifier/direction/accounting failures;
- eight malformed DIMACS strings rejected before encoding.

The independent verifier passed 16,516 assertions. Host runtime/RSS are experimental metadata, not FLMV resources. No asymptotic hard family was regenerated and no shortest proof was experimentally searched.

## Grok and Claude folder audit

All active reviewers located and read the actual `GROKPROOF/`, `research/agents/grok/` and `research/agents/claude/` folders.

- `GROKPROOF/2026-11-03_1514_PROGRESS.md`, blob `a96183b1acb61274ab72557789bd7b8ad13d249d`: the current note leaves the one fixed all-input fully charged transformation open. Its contextual projections require charged implication/UNSAT certificates; absent a uniform polynomial certificate theorem, that proposal restates the missing transfer. Pippenger--Fischer simulation is an upper bound and cannot be reversed.
- `GROKPROOF/2026-11-03_2214_PROGRESS.md`, blob `59fe73c20473bd6bc20500cf58d75e42519aee88`: semantic-core extraction and arbitrary-decider contraction remain open.
- `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex`, blob `d06a2d56befc775660c34a59067b61f0a8c142a8`: finite circuit rewriting/accounting, explicitly no lower bound.
- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`: correctly objects to hidden deterministic selection; averaging does not produce a uniform selector.
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`, and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: restricted alternation-trading and sequential-access results only.

Independent review agrees with those restrictions. None supplies a common envelope for full `Rmix341`, B1, B2 or B3.

## Classification and next exact gap

- **PROVED:** encoderwise-polynomial quantifier counterexample; common-envelope repair theorem; per-cutoff algorithm firewall; fully charged pipeline composition equivalence; finite controls.
- **PROVED/RESTRICTED:** pure-Resolution certified source splicing; raw-source sensitivity; syndrome-coordinate collapse; tagged conservative transport under explicit syntax hypotheses.
- **CONDITIONAL:** a representation class preserves hardness if one fixed common cost-reflection polynomial covers all its encoders and all sources.
- **OPEN:** authenticate such an envelope for every `Rmix341` rule, especially AND3 support typing and LOCAL-CONVERT payloads; full mixed hardness; B1, B2 and B3.
- **NOT ESTABLISHED:** an unrestricted superpolynomial SAT lower bound or `P!=NP`.

The next valid theorem target is a full-rule source-splicing/common-envelope result with one fixed polynomial, source tags, conservative alpha-renaming, explicit payload lengths and polynomial validation. Separate `p_E` bounds, per-length encoders and exponential backtranslations are insufficient.

## Artifacts

- `experiments/arc/lspv5_324/common_envelope_firewall_referee324.py`
- `experiments/arc/lspv5_324/verify_common_envelope_firewall_referee324.js`
- `results/raw/arc/lspv5_324/common_envelope_firewall_referee324.json`

SHA-256: producer `24ba27ca88d98d3c2d462c92b7ca65e2d621a0344ffcea370df581633b237d6a`; verifier `adb54c79d79ae0e40af129dd95435c979837d72b11b16f8fcd083fe1e9c51e18`; raw `987bb0524613f35166104e64e5eb77d86dd24fdff830c1cbf537f50753a9ace9`.
