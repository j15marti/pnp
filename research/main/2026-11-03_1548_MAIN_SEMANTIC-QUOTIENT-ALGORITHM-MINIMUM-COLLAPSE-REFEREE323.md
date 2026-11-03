# SEMANTIC-QUOTIENT-ALGORITHM-MINIMUM-COLLAPSE-REFEREE323

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 15:48 PST**

## Outcome

This run starts with Urquhart's certified exponential ordinary-Resolution lower bound for expander Tseitin contradictions and asks for a representation- and algorithm-independent signed-hypergraph/DAG invariant. The strongest natural version fails for an exact reason.

For a presentation `F(B,Y)`, let

`Rel_B(F) = { b in {0,1}^B : exists y F(b,y)=1 }`.

Any fully extensional invariant preserved under **every** exact CNF, circuit, GF(2), auxiliary-variable, Extended-Resolution, lazy or shared-DAG representation factors through this projected relation. There are at most `2^(2^|B|)` such relations. For closed SAT decision, `B=empty`, so there are exactly two: `TOP={()}` and `BOTTOM=empty`. Every closed UNSAT source is therefore extensionally identical. If the invariant is also required to lower-bound native `Rmix341` derivation cost on every exact presentation, the opposite-unit presentation `(z) AND (not z)`, of cost one, forces the invariant to be at most one on every closed UNSAT source—including the Resolution-hard Tseitin family.

A second proved no-go concerns algorithm quantifiers. For each fixed valid input string `x`, there is a total correct finite program `A_x` that compares its input with hardcoded `x`, returns the stored correct label on equality, and otherwise invokes complete brute force. On `x`, code acquisition plus execution is `O(|x|)`. Thus pointwise minimization over correct algorithms chosen after seeing the input collapses to linear acquisition. This does **not** refute B1 or worst-case hardness, because those fix one algorithm before quantifying over an unbounded family.

The resulting trilemma is exact:

1. Free after-the-fact exact representation choice collapses to `TOP/BOTTOM`.
2. Per-input or per-size representation/algorithm choice is forbidden nonuniform hardcoding.
3. One fixed all-input exact canonicalizer, with construction charged, is itself a SAT decider.

Therefore a meaningful survivor must retain authenticated source/provenance and charge each representation transformation. It is then source- and model-relative, not purely semantic. The weakest credible cross-representation transfer remains correct-direction, polynomial, source-authenticated proof backtranslation. B1, B2, B3, full-`Rmix341` hardness and P versus NP remain **OPEN**.

## Fixed model and what was not changed

The target remains the preselected `Rmix341`: original signed-CNF clauses are authenticated free leaves; binary-premise RES, exact local AND3/factor steps, GF(2) row addition, LOCAL-CONVERT and conservative signed AND2-VARDEF are paid; each distinct inference node in the shared contradiction DAG has unit weight. `W_R(F)` is the after-the-fact minimum over legal contradiction DAGs. Search for the best DAG is not charged to this minimum.

Input length `N` is explicit binary/DIMACS-style encoded length. Encoded node payload lengths, construction, bit access, update, checking, output and peak live space are separate physical ledgers. Exponential intermediate representations are legal, but must be paid if materialized; compact alternatives remain legal. No task, schedule, rule, weight, encoding or previously verified result was changed.

## Established lower bound: exact theorem and restriction

**Urquhart (1987), KNOWN/RESTRICTED.** There are constant-degree expander graphs with odd Tseitin charges such that every ordinary Resolution refutation of the associated clause set has exponential length in the number `h` of graph vertices. The proof system has clauses as lines and the ordinary Resolution rule (with standard harmless syntactic variants); proofs may be shared DAGs. The quantifiers are: there is one infinite explicitly constructible family and a constant `c>0` such that every Resolution refutation of each sufficiently large family member has at least `2^(c h)` lines. For a cubic graph the project encoding has `3h/2` edge variables and `4h` width-three clauses; explicit binary variable names give `N=Theta(h log h)` bits. DOI: https://doi.org/10.1145/7531.8928.

This theorem is not about `Res(oplus)`, Extended Resolution, arbitrary circuits, `Rmix341`, or unrestricted SAT machines. The mandatory XOR countercontrol is decisive: the same connected simple bridgeless cubic odd sources have exact `Rmix341` cost `4h-1`, and the balanced emitted/checking work is polynomial. The Resolution lower bound therefore certifies a restricted proof-system separation, not computational hardness.

**Cook--Reckhow (1979), KNOWN FRAMEWORK.** A propositional proof system is a fixed polynomial-time computable surjection onto tautologies. Polynomial boundedness of some such system is equivalent to `NP=coNP`; this does not assert that an arbitrary SAT decider emits proofs in the selected system. DOI: https://doi.org/10.2307/2273702.

**Darwiche--Marquis (2002), KNOWN KNOWLEDGE-COMPILATION FRAMEWORK.** NNF-DAG representation languages are assessed separately for succinctness and for supported polynomial-time queries and transformations. Semantic equivalence alone does not provide a compiler or cheap query access. DOI: https://doi.org/10.1613/JAIR.989.

Recorded literature queries: `Urquhart 1987 Hard examples for resolution Tseitin expander exact theorem`; `Cook Reckhow relative efficiency propositional proof systems quantifiers`; `knowledge compilation map succinctness transformations queries representation`; `instance complexity pointwise hardcoded decider uniform program`. Project GitHub was searched for semantic quotients, projected relations, knowledge compilation and representation invariants; `github.com/openai` was searched separately for matching proof/invariant implementations. No relevant OpenAI implementation was found. Failed search is not novelty evidence.

## Theorem 1: projected-semantic quotient collapse

Let `F(B,Y)` be any finite Boolean presentation with declared boundary `B`, and define its exact projected relation as above.

**Theorem.** If `I(F)` is invariant under replacement by every exact presentation with the same boundary relation, then `I` has at most `2^(2^|B|)` values at boundary size `|B|`. At `B=empty`, `I` has at most two values and is constant on all closed UNSAT presentations.

**Proof.** A relation on `B` is a subset of the `2^|B|` boundary assignments, so at most `2^(2^|B|)` relations exist. Exact representation invariance makes `I` a function of that relation. With no boundary variables, there is one empty assignment; the projected relation is `{()}` precisely when `F` is satisfiable and is empty otherwise. Hence every closed UNSAT presentation has the same invariant value. QED.

**Cheapest-representative corollary.** Every boundary relation has a blocking-CNF representation with at most `2^|B|` clauses, obtained by forbidding each nonmember assignment. Its explicit size is `O(|B| 2^|B| log |B|)` under binary indices. At `B=empty`, the two relations have constant representatives `TOP` and `BOTTOM`. Therefore an extensional invariant that lower-bounds native cost on **every** exact representation is bounded by the cheapest representative. In `Rmix341`, the opposite-unit contradiction gives an UNSAT bound of one.

The construction need not be efficiently discoverable from the source. Discovering the relation is exactly the missing charged computational work; allowing the best representative after the fact erases it.

This generalizes the concurrent same-variable result in `research/agents/lspv-2/2026-11-03_1512_LSPV-2_EXTENSIONAL_COST_NOGO372.md`, blob `d23f6fcf9f9525b279e2cad30c97ab721be7cb93`, which gives equal-length odd Tseitin/opposite-unit controls with costs `4h-1` and `1`. It also strengthens the earlier project observation in `research/review/coordination/model_bridge.md` that semantic-state counting can collapse to a small decision quotient. No independent novelty is claimed.

## Theorem 2: pointwise algorithm-minimum collapse

Let `L` be any decidable language and let `x` be a fixed input. Choose a complete decider `D` for `L`. Define the finite program `A_x`:

1. compare input `y` with the stored string `x`;
2. if equal, return the stored correct bit `1[x in L]`;
3. otherwise run `D(y)`.

**Theorem.** `A_x` is a total correct uniform program, has description length `O(|x|+|D|)`, and takes `O(|x|)` time on `x`. Thus

`min_A (|A| + T_A(x)) = O(|x|)`

when the minimum ranges over total correct deciders selected after `x`.

The word “uniform” here means that each `A_x` is one ordinary finite program correct on all inputs. The family `(A_x)` is nonuniform in `x`; there is no single fast program for all `x`. The theorem falsifies `sup_x inf_A T_A(x)` as an intrinsic hardness measure. It does not falsify the meaningful order `inf_A sup_{|x|<=N} T_A(x)`, nor the statement that for every fixed `A` there are infinitely many hard inputs.

## Theorem 3: uniform-transformation trilemma

Suppose a transformer `C` is required to output `TOP` for SAT sources and `BOTTOM` for UNSAT sources.

- If `C` is chosen after the input, its output is a hardcoded answer.
- If `C` is fixed and correct on every input, running `C` decides SAT.
- More generally, if fixed `C` outputs an exact representation and fixed `E` decides emptiness of that representation, `E(C(F))` is a SAT decider.

All costs of `C` and `E`—parsing, source/index/head reads, descriptor construction, conversions, accesses, updates, certificate checks, output and simultaneous live memory—must be charged. Proving that every such composition needs superpolynomial work is the unrestricted SAT lower-bound problem, not a consequence of semantic invariance.

## Four falsifiers and verdicts

1. **“A growing exact semantic invariant lower-bounds every representation.” FALSIFIED.** Closed UNSAT has one extensional class and a constant representative.
2. **“A large boundary table is intrinsic.” FALSIFIED AS AN UNRESTRICTED CLAIM.** Equality, parity and other relations can have compact circuits/XOR systems; implicit descriptors charge only actual construction and access.
3. **“Minimize over every correct algorithm to get pointwise intrinsic work.” FALSIFIED.** `A_x` is linear on its chosen target and complete elsewhere.
4. **“A uniform canonicalizer is harmless preprocessing.” FALSIFIED AS A FREE STEP.** A correct all-input `TOP/BOTTOM` canonicalizer decides SAT; its entire physical cost is part of the algorithm.

## What survives

The strongest current invariant robust to internal representation changes is **source-query sensitivity**: if flipping each of `L` independently encoded source bits can change the SAT label, then an exact deterministic decision-tree algorithm must read all `L` bits on an adversarial input. This survives circuits, XOR, auxiliaries and lazy internal states because it concerns authenticated source access. It is nevertheless source-encoding- and machine-model-relative and only linear: `Omega(L)` bit probes or `Omega(L/w)` ordinary `w`-bit word probes. It supplies no superpolynomial lower bound and none of B1/B2/B3.

For proof hardness, the weakest credible representation condition remains correct-direction cost reflection:

`W_R(F) <= p(|F| + W_R(E(F)))`

for one fixed polynomial, one uniform source-authenticated encoder `E`, and all inputs in the promised family. Two-way representation equivalence requires the analogous inequality in both directions. A merely reversible or equisatisfiable encoding is insufficient; an exponential-overhead backtranslation proves no machine lower bound.

The concurrent peer `research/agents/lspv-1/2026-11-03_1500_LSPV-1_REVERSIBLE_REPRESENTATION_TRAP373.tex`, blob `1cf73470332a8d3de56dd5f4d918f5343e96ff97`, makes this concrete: a fixed polynomial-time invertible source-prefix-preserving encoder can recognize Haken PHP and append a one-step Resolution contradiction. Reversibility and source preservation still do not imply polynomial proof backtranslation.

## Physical cost ledger

- An explicitly materialized `B`-bit intermediate costs at least `ceil(B/w)` word writes; retaining it requires `B` live bits.
- Streaming preserves output time but may reduce peak space.
- An implicit/lazy object charges its descriptor and every actual evaluation/access, not an unmaterialized `2^k`-entry virtual table.
- Shared logical DAG nodes are counted once in `W_R`; scheduling, storage, retrieval and recomputation remain separate machine costs.
- A proof node of unit weight does not imply unit serialized length or unit verification work.

The concurrent peer `research/agents/lspv-3/2026-11-03_1524_LSPV-3_BALANCED_ROW_BUDGET376.tex`, blob `2e0841e126f670e587d2571153fd4746735259eb`, shows why this separation matters: odd cubic Tseitin can force an `Omega(h)`-wide XOR row yet has a `4h-1`-node proof, `O(h log^2 h)` emission/checking bit work and `O(h log h)` peak live bits. Linear width is not exponential physical work.

## Finite controls

New formula generation was secondary and only tested the transfer/no-go obligations. Python production and an independently written JavaScript verifier checked:

- standard odd/even `K4` Tseitin: zero/eight models;
- `PHP_3^2`, Horn and 2-SAT UNSAT controls: all map to the same empty 0-ary relation;
- SAT siblings: all map to `{()}`;
- equality and an auxiliary-variable equality chain: identical boundary relation `{00,11}`;
- one-boundary guarded UNSAT/SAT controls: `{0}` versus `{0,1}`;
- exact quotient counts for boundary sizes 0,1,2,3: 2,4,16,256;
- seven target-specific total correct deciders across 49 target/candidate pairs;
- eight malformed DIMACS strings rejected before semantic classification.

The producer enumerated at most 64 assignments per fixture. The independent verifier passed 43 assertion groups. Host runtime/RSS are experimental metadata, not FLMV time/space. No asymptotic hard family was regenerated and no shortest proof was searched.

## Grok and Claude folder audit

All active reviewers located the repository paths `GROKPROOF/`, `research/agents/grok/` and `research/agents/claude/` rather than guessing them. The folders were absent from the local scratch projection, so their current contents were read from the connected `j15marti/pnp` repository.

- `GROKPROOF/2026-11-03_2214_PROGRESS.md`, blob `59fe73c20473bd6bc20500cf58d75e42519aee88`: correctly leaves the fully charged all-input transformation and semantic-core extraction open and denies transfer from restricted proof/circuit bounds to unrestricted computation.
- `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex`, blob `d06a2d56befc775660c34a59067b61f0a8c142a8`: useful finite circuit-rewrite accounting, explicitly no lower bound.
- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`: materially relevant objection—per-seed existence does not give a uniform deterministic selector; free selection hides nonuniform advice.
- `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`, blob `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9`, and `2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: restricted alternation-trading results only.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: sequential-access crossing-sequence theorem, explicitly nontransferable to indexed random access.

These are research evidence, not authority. Independent checking agrees with the stated restrictions. None supplies B1, B2, B3, full mixed hardness or an unrestricted invariant.

## Classification and next gap

- **PROVED:** projected-semantic quotient collapse; pointwise algorithm-minimum collapse; uniform canonicalization trilemma; exact finite controls.
- **KNOWN/RESTRICTED:** Urquhart ordinary-Resolution lower bound; source-query sensitivity; `Rmix341` Tseitin XOR upper bound; proof-system simulation results.
- **CONDITIONAL:** if one fixed charged all-input compiler and emptiness checker are polynomial, their composition is a polynomial SAT decider; if a correct-direction polynomial proof backtranslation exists, target proof hardness can transfer in the direction stated.
- **OPEN:** a source-sensitive invariant preserved by every cost-reflecting representation; polynomial backtranslation for full `Rmix341`; full mixed lower bound; B1, B2 and B3.
- **NOT ESTABLISHED:** an unrestricted superpolynomial SAT lower bound or `P!=NP`.

The next substantive obligation is not another hard formula. It is either (i) define a nontrivial source-authenticated invariant and prove it monotone under **every legal `Rmix341` rule and every cost-reflecting representation conversion**, or (ii) prove one fixed polynomial-overhead computation-to-proof/cost-reflecting transformation. Pure semantic representation independence is now ruled out as too strong.

## Artifacts

- `experiments/arc/lspv5_323/semantic_quotient_collapse_referee323.py`
- `experiments/arc/lspv5_323/verify_semantic_quotient_collapse_referee323.js`
- `results/raw/arc/lspv5_323/semantic_quotient_collapse_referee323.json`

SHA-256: producer `48e17371008d05865cb01b3aba0a285638a13dde1022079ff8f9e06f81d8e48a`; verifier `aefe02948099688d497d8c6c0fac2a34757f363f695a7554a6099361749b9bd1`; raw `356f215afa5e42707db9dc895855bb1502033f949686cbf233ed21785c13d078`.
