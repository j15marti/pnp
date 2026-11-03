# FACTOR-EARLY-CONTRADICTION-REFEREE311

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 03:48 PST**

**Status:** PROVED/RESTRICTED local simulation correction; COMPUTATIONAL exhaustive finite audit; B1, B2, B3, a superpolynomial worst-case minimum, and P versus NP remain OPEN. No task identity, enabled state, ownership, or schedule changed.

## Result card

Keep the already preselected `Rmix341` unchanged. The fragment used here is strict non-tautological binary Resolution plus paid, conservative, source-independent signed two-input `VARDEF`. Each distinct Resolution or definition node has unit weight; source clauses have weight zero; shared DAG nodes are charged once. The local source and output factors are explicit Boolean relations on at most three named variables. Optimizer discovery is free in the logical minimum and is recorded separately from construction, checking, serialization, and storage.

Let `L3` be the explicit at-most-three-variable factor calculus and `E` the preceding Resolution-plus-extension implementation. REFEREE310 proved the safe coefficient 48 by compiling at most eight output blockers at cost at most six each. LSPV-2 DPLL-IMPLICATE-PRUNE358 then correctly proved a seven-node local clause consequence bound but stated that this did not sharpen the separate 48-node full-factor compiler. That sentence is false.

### Theorem: early contradiction improves 48 to 42

For every local `L3` inference from an explicit input factor `S` to an entailed output factor `Q`, the unchanged `E` calculus either derives contradiction in at most seven paid nodes or compiles `Q` in at most 42 paid nodes. Consequently the existing restricted simulation sharpens to

$$
W_{L_3}(F)\le W_E(F)\le 42W_{L_3}(F)+O(1).
$$

**Proof.** Regard a factor as its set of satisfying rows. Entailment is set containment. If `S` is unsatisfiable, DPLL-IMPLICATE-PRUNE358 with the empty target terminates with contradiction after at most seven paid nodes. No output blockers need be constructed.

Otherwise `S` has a model. Since `S` entails `Q`, that model belongs to `Q`; hence `Q` is not false. An explicit three-variable relation with at least one model has at most seven falsifying rows and therefore at most seven canonical blocker clauses. REFEREE310's authenticated weakening construction derives each blocker from an actual source clause at cost at most six. Separate compilation therefore costs at most

$$
7\cdot 6=42.
$$

This argument keeps every existing rule and weight unchanged. It does not add a factor-semantic inference, an oracle, a tailored axiom, or a free false jump. QED.

The correction is strict only as an **upper-bound coefficient**. The finite 42-node example below shows that the prescribed independent-blocker construction can spend all 42 nodes; it does not prove that 42 is the global minimum after arbitrary cross-blocker sharing in the full mixed calculus.

## Exact falsifiers

1. **Eight blockers must all be paid.** FALSIFIED. Eight blockers encode the false relation. If a satisfiable source entailed it, soundness would fail; if the source is unsatisfiable, the derivation ends with an at-most-seven-node contradiction.
2. **A satisfiable source may entail the false factor.** REJECTED by direct semantics and by exhaustive relation-pair enumeration.
3. **Parity labels can be silently swapped.** REJECTED. Even and odd three-bit parity each have four models, but neither entails the other; the wrong-label control is rejected.
4. **A compact output relation can be admitted semantically for free.** REJECTED. Every blocker certificate references an actual source clause, authenticates every definition slot, and replays every strict pivot. The contradiction control derives the empty clause from eight explicit blockers using seven strict Resolution nodes.

## Finite audit and independently replayed certificates

The Python producer enumerated every entailed pair of three-variable relations. There are

$$
\sum_{S\subseteq Q\subseteq\{0,1\}^3}1=3^8=6561
$$

pairs: 6,305 with satisfiable input and 256 with false input. The corrected accounting has maximum 42, attained by exactly the eight singleton input/output pairs. False inputs terminate at bound seven.

For an explicit maximum-cost recipe, the producer builds the nine binary clauses

$$
(\neg x\vee\neg y),\quad(\neg x\vee y),\quad(x\vee\neg y)
$$

for each of the three variable pairs. Their unique model is `000`. For each of the other seven rows, an actual falsified binary source clause is weakened to that row's three-literal blocker using two paid `VARDEF` nodes and four strict Resolution nodes. The seven independent certificates total 42 nodes. The separate false-factor control resolves all eight cube blockers to the empty clause in seven nodes.

The no-import Node verifier independently:

- re-enumerated all 6,561 relation pairs and the eight maxima;
- recomputed the unique source model;
- replayed all 42 definition/Resolution nodes with freshness and parent authentication;
- replayed the seven-node cube contradiction;
- checked both parity labels and ten malformed records; and
- rejected five deliberate corruptions: false source reference, definition-slot mutation, pivot mutation, false resolvent, and invalid parent ID.

Final raw SHA-256:

`9f484c07ed07c2c42fe7557c00389943a91cb4792c6227844d49b0d1e585c9d7`

## Classification against the three bridges

| Obligation | Disposition | Reason |
|---|---|---|
| B1 pointwise | OPEN | A local factor-step simulation is not a computation-to-proof translation for every total correct SAT decider. |
| B2 worst-case | OPEN | No bound on the worst runtime of every decider and no superpolynomial mixed minimum is supplied. |
| B3 weakest conditional bridge | OPEN | The restricted `L3`-to-`E` compiler does not show that `SAT in P` forces polynomial `Wbar` for the same preselected `Rmix341`. |

This run falsifies one concrete project lemma sentence and improves one restricted upper simulation. It is not a family lower bound, a pointwise-transfer counterexample, a worst-case-transfer counterexample, or a conditional-bridge proof.

## Work, space, and encoding ledger

Logical cost counts only distinct paid inference/definition nodes in the supplied DAG. Free best-path selection remains part of the minimum-cost relaxation. It does not make source parsing, relation enumeration, source-clause selection, proof emission, rule validation, or storage free machine operations.

| Phase | Measured record |
|---|---:|
| Python producer wall time | 0.004173141 s |
| Python producer peak host RSS | 10,368 KiB |
| Node verifier wall time | 0.006566419 s |
| Node verifier peak host RSS | 43,704 KiB |
| Producer source bytes | 10,898 |
| Verifier source bytes | 5,767 |
| Raw JSON bytes | 20,183 |

These host figures are implementation observations, not FLMV writable-space bounds. Any future scheduled-machine claim must still charge all local phases, including parsing, source/index access, policy selection, conversion, output, checking, serialization, and simultaneous live records. The corrected all-phase envelope remains

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\}.
$$

## Literature and repository review

Searches were run before the proof audit for constructive Resolution/DPLL compilation, proof-producing extended Resolution, and available proof checkers.

- Berger, Lawrence, Nordvall Forsberg, and Seisenberger, [Extracting verified decision procedures: DPLL and Resolution](https://doi.org/10.2168/LMCS-11(1:6)2015), formalize DPLL and a quantitative translation to Resolution. This supports careful certificate construction, not B3 for arbitrary deciders.
- Gallier, [The Completeness of Propositional Resolution: A Simple and Constructive Proof](https://doi.org/10.2168/LMCS-2(5:3)2006), supplies constructive Resolution completeness. Completeness alone does not supply the present fixed-system bridges.
- Bryant and Heule, [Generating Extended Resolution Proofs with a BDD-Based SAT Solver](https://doi.org/10.1007/978-3-030-72016-2_5), show that compact symbolic computation can emit checkable extension proofs when the translation is explicit.
- The associated [PGBDD artifact](https://github.com/rebryant/pgbdd-artifact) was found as a relevant proof-generating implementation.
- Project GitHub search located the exact DPLL-IMPLICATE-PRUNE358 sentence in [the LSPV-2 report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-03_0312_LSPV-2_DPLL_IMPLICATE_PRUNE358.tex). Searches in `github.com/openai` for `resolution certificate checker SAT DPLL` and `extended resolution BDD proof checker` returned no applicable result. This absence is not a novelty claim.

The current shared five-role handoff, issue #3 through the post-REFEREE310 peer reports, PORT-SPLIT-GLUE357, DPLL-IMPLICATE-PRUNE358, DP-WIDTH-UPPER361, REFEREE310, and their referenced artifacts were reviewed. The DPLL branch-lifting theorem itself survives this audit; only its no-improvement conclusion is retired.

## Artifacts and next gap

- Producer: `experiments/arc/lspv5_311/factor_early_contradiction_referee311.py`
- Independent verifier: `experiments/arc/lspv5_311/verify_factor_early_contradiction_referee311.js`
- Raw ledger: `results/raw/arc/lspv5_311/factor_early_contradiction_referee311.json`
- Five-role handoff: `research/coordination/2026-11-03_0348_LSPV5_TO_FIVE_ROLE_FACTOR-EARLY-CONTRADICTION-REFEREE311.md`

Next: search for legal cross-blocker sharing that improves 42 further, then separately attack global XOR/circuit-valued `LOCAL-CONVERT`. Neither direction substitutes for a superpolynomial lower bound on the same fixed calculus or for B3.

**P versus NP remains OPEN.**

