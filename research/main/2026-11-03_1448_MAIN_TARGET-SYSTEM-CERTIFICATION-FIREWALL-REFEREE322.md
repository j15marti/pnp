# TARGET-SYSTEM-CERTIFICATION-FIREWALL-REFEREE322

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 14:48 PST**

## Outcome

Starting from published lower bounds, not newly generated asymptotic formulas, this run isolates the weakest family-local transfer that can make an established proof lower bound relevant to the fixed project calculus. If `Q` is the published hard proof system and `R` is the preselected target, the required arrow is

`W_Q(F_i) <= p(N_i + W_R(F_i))`

for one polynomial `p`, the same source formulas `F_i`, and all members of the established hard family. Equivalently, `Q` must polynomially simulate `R` on that family. The reverse inequality cannot import `Q`-hardness.

This directly answers the “certified hard problem” objection: hardness is certified relative to a proof/algorithmic model. An expensive conversion from a short `R` proof into a long proof in a weaker `Q` is not ignored machine work; if that conversion is executed, it must be charged. But it is not part of the minimum native `R` derivation because an `R` proof need not emit a `Q` proof. On Tseitin and pigeonhole sources the conversion blow-up measures proof-system mismatch, not native `R` cost or unrestricted SAT runtime.

No full-`Rmix341` superpolynomial lower bound or B1/B2/B3 bridge is proved. P versus NP remains **OPEN**.

## Fixed target, encoding and cost

The target remains the unchanged source-authenticated `Rmix341`: original CNF clauses are free leaves; binary-premise RES, exact local AND3/factor steps, GF(2) row addition, LOCAL-CONVERT and conservative signed AND2-VARDEF are paid; every distinct inference node in the shared contradiction DAG has unit weight. `W_R(F)` minimizes over all legal DAGs after the fact. Proof search is not charged to this minimum. Serialized proof bits, verification work, source acquisition and scheduled machine time/space are separate ledgers.

Inputs use explicit signed CNF/DIMACS-style encodings. `N` is encoded bit length, not variable count. Correct deciders must handle SAT, UNSAT and malformed strings. No task, schedule, rule, weight or encoding was changed.

## Published lower bounds and exact restrictions

1. **Urquhart (1987), KNOWN/RESTRICTED.** Odd Tseitin clause sets built from expander graphs require exponential-length ordinary unrestricted shared-DAG Resolution refutations. The theorem concerns Resolution; the same clause sets have polynomial proofs in a stronger standard propositional calculus. For the cubic project encoding, `h` vertices give `3h/2` edge variables, `4h` width-three source clauses and `N=Theta(h log h)` explicit bits. DOI: https://doi.org/10.1145/7531.8928.
2. **Haken (1985), KNOWN/RESTRICTED.** Standard unary pigeonhole formulas have exponential ordinary Resolution refutations in the pigeon parameter. In the project signed explicit encoding `N=Theta(h^3 log h)`. The theorem does not cover extension rules or arbitrary SAT computation. DOI: https://doi.org/10.1016/0304-3975(85)90144-6.
3. **Cook (1976), KNOWN UPPER BOUND.** The identical pigeonhole sources have polynomial-length Extended Resolution refutations. DOI: https://doi.org/10.1145/1008335.1008338.
4. **Kiesl--Rebola-Pardo--Heule--Biere (2020), KNOWN SIMULATION.** Extended Resolution polynomially simulates DRAT, and DRAT polynomially simulates DPR. The transformations preserve the source and have polynomial proof-size overhead. DOI: https://doi.org/10.1007/s10817-020-09554-z.

Search queries recorded: `Urquhart 1987 Hard examples for resolution Tseitin expander DOI`; `Haken 1985 Intractability of resolution pigeonhole principle DOI`; `Cook 1976 short propositional calculus pigeonhole extended resolution`; `Kiesl Rebola-Pardo Heule Biere 2020 Simulating Strong Practical Proof Systems with Extended Resolution`. Relevant project and `github.com/openai` code searches were run for the transfer terminology and ER/DRAT/DPR checkers; no OpenAI implementation or duplicate target theorem was found. A failed search is not evidence of novelty.

## The exact transfer theorem

**Theorem (family-local minimum domination).** Let `Q` and `R` be fixed sound proof systems, let `(F_i)` be a same-source UNSAT family with encoded lengths `N_i`, and let `W_Q,W_R` be their after-the-fact minimum costs. Suppose there are fixed constants `C,d`, independent of `i`, such that

`W_Q(F_i) <= C (N_i + W_R(F_i))^d`

for every `i`. If `W_Q(F_i)` is superpolynomial in `N_i`, then `W_R(F_i)` is superpolynomial in `N_i`.

**Proof.** If `W_R(F_i)` were bounded by a polynomial in `N_i`, the displayed inequality would polynomially bound `W_Q(F_i)`, contradiction. Equivalently,

`W_R(F_i) >= (W_Q(F_i)/C)^(1/d) - N_i`.

This minimum inequality is weaker than requiring an effective compiler: after-the-fact minima are enough. A uniform source-authenticated compiler from every `R` proof to a `Q` proof with polynomial overhead is one sufficient way to establish it, but is stronger than necessary. If the source formula changes, a size-controlled reduction plus an `R(target)->Q(source)` proof backtranslation is required, and the published lower bound must remain superpolynomial in the target encoding length.

The worst-case analogue `Wbar_Q(N) <= p(N+Wbar_R(N))` also transports a superpolynomial worst-case lower bound. Neither statement is B1, B2 or B3; it addresses only hardness transfer between proof systems.

## Established same-source countercontrols

### Tseitin

The project already proved for connected simple bridgeless cubic odd Tseitin sources that

`W_Rmix341(F_h) = 4h - 1`.

Thus Urquhart's exponential Resolution-hard family is linear in the fixed mixed calculus. The mandatory XOR shortcut is not an assumed transfer; it is an explicit counterexample to transferring Resolution hardness without the correct arrow. Any `Rmix341 -> Resolution` converter must expand these short mixed proofs exponentially. That is a converter lower bound, not `Rmix341` hardness.

### Pigeonhole

Haken's exponential ordinary-Resolution lower bound coexists with Cook's polynomial ER proof on the same source. The fixed mixed system contains the paid ER2 fragment audited in LSPV-3 result 374, so pigeonhole is also defeated as a candidate mixed-hard family. Again, forcing explicit output in ordinary Resolution changes the task.

### DPR/DRAT/ER direction

The published simulations and the ER2 replay give

`W_Rmix341(F) <= poly(N + B_DPR(F) + 1)`.

Therefore superpolynomial mixed hardness would imply DPR hardness. A DPR lower bound does **not** imply mixed hardness. Reversing this inequality is invalid.

## Falsifiers and verdicts

1. **“The formula is certified hard, so it is hard in `Rmix341`.” FALSIFIED.** Tseitin is Resolution-hard but has exact linear mixed proofs; PHP is Resolution-hard but ER-short.
2. **“An expensive `R->Q` conversion proves large `W_R`.” FALSIFIED.** It proves the conversion/output bottleneck. The native `R` proof remains short.
3. **“`W_R <= poly(N+W_Q)` imports a `Q` lower bound.” FALSIFIED.** The inequality is in the wrong direction.
4. **“NP-completeness, empirical difficulty, or a restricted-width/degree theorem supplies the transfer.” FALSIFIED AS AN INFERENCE.** None gives the family-local domination theorem or B3.

## Finite controls

The new code is secondary and tests only the transfer obligation. It generated the standard `K4` Tseitin and `PHP_3^2` controls, then an independently written JavaScript verifier replayed the fixtures.

- Odd-charge `K4` Tseitin: six variables, sixteen clauses, zero models.
- Even-charge `K4`: exactly eight models.
- Every single-clause deletion of the odd source is SAT.
- `PHP_3^2`: six variables, nine clauses, zero models; every single-clause deletion is SAT.
- Six malformed transfer specifications were rejected: different source, moving `Q`, moving `R`, nonuniformity, reversed inequality and exponential overhead.
- A pure arithmetic control confirms that an exponential weak-system output length can coexist with a linear target proof for every tested fixed polynomial degree. It is not asserted as a numerical lower-bound constant.

Producer: 64 assignments per finite formula; verifier: 45 assertion groups. Host runtime/RSS are not FLMV resources. No shortest proof was searched or experimentally certified.

## Grok and Claude folder audit

All active reviewers located, rather than guessed, the actual repository directories `GROKPROOF/`, `research/agents/grok/` and `research/agents/claude/`. The local scratch workspace had no checkout of these folders, so the connected `j15marti/pnp` repository was read directly.

- `GROKPROOF/2026-11-03_2214_PROGRESS.md`, blob `59fe73c20473bd6bc20500cf58d75e42519aee88`: correctly keeps the arbitrary-decider fully charged transformation open and says restricted proof/circuit bounds do not transfer to unrestricted computation. It supplies no B1/B2/B3 theorem.
- `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex`, blob `d06a2d56befc775660c34a59067b61f0a8c142a8`: useful finite circuit-rewriting accounting, explicitly no lower bound.
- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`: material objection retained—per-seed pseudorandomness does not give the required joint product bound, and selecting a good deterministic list cannot be free. This blocks a hidden derandomization/selection oracle, not B3.
- `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`, blob `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9`, and `2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: valid restricted alternation-trading/portfolio results, not a same-`R` proof-size bridge.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: valid sequential-access crossing-sequence results; the report itself explains why they do not transfer to indexed random access.

These reports are evidence, not authority. Independent review agrees with their model restrictions and rejects promotion to B1/B2/B3.

## B1/B2/B3 ledger and next gap

- **B1 OPEN.** No translation from every total correct SAT decider's UNSAT computation to a polynomial-cost `Rmix341` derivation.
- **B2 OPEN.** No universal worst-case domination theorem.
- **B3 OPEN, primary.** `SAT in P => Wbar_Rmix341 polynomial` is not supplied by proof-system completeness, NP-completeness, Cook--Reckhow existence of some system, or the family-local theorem above.

The weakest next hardness obligation is now exact: either prove a superpolynomial lower bound directly for every legal rule of the fixed full calculus, or prove correct-direction family-local polynomial domination from full `Rmix341` into a published hard system. Independently, prove B3 for this same `Rmix341`. P versus NP remains OPEN.

## Artifacts

- `experiments/arc/lspv5_322/target_system_certification_referee322.py`
- `experiments/arc/lspv5_322/verify_target_system_certification_referee322.js`
- `results/raw/arc/lspv5_322/target_system_certification_referee322.json`

SHA-256: producer `b928789dcb109664b14672908519df4af9042bb6fc118306e25bef5dbb1f35f6`; verifier `0cb997002b725229abb012fcb7ca22ef7d1df0444fb60c6cf47d266ac215bd08`; raw `5af90c66a10a9d078ec2fe481cd068ba10954819c97007b55ccb540e9e1635ad`.
