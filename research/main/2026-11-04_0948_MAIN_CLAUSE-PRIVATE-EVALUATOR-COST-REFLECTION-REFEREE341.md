# CLAUSE-PRIVATE-EVALUATOR-COST-REFLECTION-REFEREE341

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 09:48 PST**

**Status:** **PROVED/RESTRICTED exact macro-splice theorem.** For the unchanged fixed `R_mix341`, a normalized CNF `F` with `L` literal occurrences admits an authenticated clause-private evaluator replay using the displayed `3(L-1)` paid nodes, and

\[
W_{R_{\mathrm{mix341}}}(F)
\le W_{R_{\mathrm{mix341}}}(T(F))+3(L-1).
\]

Here `T(F)` is one declared private binary OR/AND evaluator encoding, not an arbitrary semantically equivalent representation. The displayed macro has exactly `3(L-1)` nodes; no minimum claim is made. **PROVED/FINITE:** Python checked 262 signed polarity/AND-chain records and one complete 34-node source-to-contradiction splice; an independently written JavaScript verifier passed 94 record checks; five malformed controls were rejected. **OPEN:** specialization of a uniform indexed evaluator to `T(F)`, short reflection proofs from `SAT in P`, full B1/B2/B3, a superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP. No task, schedule, enabled state, rule, weight, or ownership changed.

## Outcome

REFEREE340 showed that extensional evaluator correctness alone does not imply source retraction. This run gives a positive repair for one natural, transparent representation. It proves the correct-direction polynomial cost reflection from an already specialized clause-private evaluator back to authentic source clauses. It does **not** prove representation-independent hardness: a universal bit-level evaluator can specialize to parser, multiplexer, alias and constant circuitry rather than this private evaluator, and `SAT in P` does not supply short `R_mix341` reflection proofs.

The initial broad idea was partly duplicate. REFEREE284 already proved the private evaluator gate count `L-1`; LSPV-4/376 already used `L-1` definitions plus `2(L-1)` Resolution nodes to force the root before a hypothetical semantic-zero rule; LSPV-1/354, /356 and /361 already supplied conditional source-replay machinery. The surviving increment is the explicit full-calculus cost-reflection inequality: once `T(F)` itself is the source of any typed `R_mix341` refutation, its free definition-clause leaves can be replaced by charged DEF-slot views, its output unit by the authentic replay, and every downstream mixed node copied unchanged.

## IDEA -> SEARCH -> ITERATE

### IDEA, stated before search

Build a clause-private evaluator: a binary OR tree for every source clause and a binary AND tree over the clause outputs.

**Proposed lemma.** Authentic source clauses plus paid two-input DEF gates and ordinary Resolution derive the evaluator's positive output in `O(L)` paid nodes. Any refutation whose source leaves are exactly those gate clauses plus the output unit can then be spliced onto the authentic source.

**Assumptions.** Valid normalized CNF; fresh gate outputs; signed two-input OR/AND DEF nodes; every used defining clause cites its charged DEF node; ordinary binary Resolution; no free semantic equivalence, SAT oracle or answer-dependent definition; proof-owned auxiliary variables alpha-renamed; malformed inputs rejected before the lemma.

**Falsifiable prediction.** The exact displayed macro uses at most `3(L-1)` nodes independent of clause width. A surviving source leaf not equal to a DEF facet or the derived root unit falsifies the splice.

### SEARCH and evidence that changed the idea

Primary literature actually read:

- Jan Krajíček, *A Note on SAT Algorithms and Proof Complexity*, Information Processing Letters 112 (2012), 490–493, DOI `10.1016/j.ipl.2012.03.009`, full author PDF `https://www2.karlin.mff.cuni.cz/~krajicek/sat.pdf`. The paper warns that the SAT encoding must be selected carefully and states D1–D4; D4 is efficient recovery of a source proof from the evaluator statement. Its theorem uses D1–D4, not extensional evaluator correctness alone.
- Stephen Cook and Robert Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50. Polynomial simulation is an explicit proof translator property.
- Samuel Buss and Jakob Nordström, *Proof Complexity and SAT Solving*, in *Handbook of Satisfiability*, 2021, DOI `10.3233/FAIA200990`, for the separation between proof-system strength and SAT algorithms.
- Benjamin Kiesl, Adrián Rebola-Pardo, Marijn Heule et al., *Simulating Strong Practical Proof Systems with Extended Resolution*, Journal of Automated Reasoning 64 (2020), DOI `10.1007/s10817-020-09554-z`. A polynomial simulation requires a concrete encoded proof transformation.

Actual web queries included:

- `propositional proof systems evaluator source formula recovery D4 decent proof system Krajicek SAT algorithms proof complexity`;
- `extended resolution extension axioms derive circuit output from CNF clauses OR tree source replay`;
- `Tseitin encoding clause OR gate output unit derivation resolution source clause`;
- `resolution restriction substitution extended resolution proof source formula evaluator reflection`;
- `Cook Reckhow Extended Resolution circuit evaluation clauses source replay proof`.

The available web-search service was used. A separately branded direct Google UI was unavailable, so this report does not claim a direct Google session.

Project/GitHub queries included `source replay OR tree evaluator DEF Resolution`, `clause transparent evaluator`, `source retraction D4`, `3L-3 evaluator`, `3(L-1) source replay`, `GF2 restriction closure Rmix`, and `LOCAL-CONVERT restriction`. Relevant files actually read:

- `research/main/2026-11-02_0048_MAIN_SOURCE-LIVE-RECOMPILE-REFEREE284.tex`;
- `research/agents/lspv-1/2026-11-03_0004_LSPV-1_MASKED_OR_REFLECTION_REPLAY356.tex`, blob `63dc7545ad7aad2f4b4cd53154f711bb85773c39`;
- `research/agents/lspv-4/2026-11-03_2036_LSPV-4_SEMZERO_OPAQUE_COLLAPSE376.tex`, blob `ee2228adbe5c1a0c9d3024df9d5788dc1430bc14`;
- `research/agents/lspv-2/2026-11-02_2216_LSPV-2_LOCAL_RESTRICTION_PIVOT_FIREWALL351.md`;
- `research/main/2026-11-04_0848_MAIN_SEMANTIC-EVALUATOR-SOURCE-RETRACTION-FIREWALL-REFEREE340.md`;
- authoritative fixed calculus `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

OpenAI GitHub queries `proof verifier SAT resolution extension`, `Tseitin OR gate proof`, `LRAT DRAT resolution`, and `CookLevin CNF evaluator` found no applicable `R_mix341`/ER source-retraction compiler. This absence is not novelty evidence and code would not be a theorem.

### ITERATE

Search showed that the general replay idea and the `L-1`/`2(L-1)` components were already in the project. The revised target became the exact cost-reflection inequality for one fixed transparent representation and arbitrary downstream mixed proofs. A finite proof object was then generated and independently replayed. A second prediction failed: linear logical-node count does **not** imply linear explicit proof bytes; wide intermediate clauses can make serialization quadratic.

## Exact theorem and proof

Let

\[
F=\bigwedge_{i=1}^{m}C_i,
\qquad k_i=|C_i|\ge1,
\qquad L=\sum_i k_i,
\]

be a normalized CNF with distinct non-tautological clauses and no empty clause. Tautologies and duplicates can be ignored after paid parsing; an empty source clause is already contradiction. Build `T(F)` as follows:

1. for every `C_i`, a private left-associated binary OR tree with output `o_i`;
2. a private left-associated binary AND tree over `o_1,...,o_m`, with root `r`;
3. the complete defining CNF facets for all gates and the positive unit `(r)`.

The gate count is

\[
G=\sum_i(k_i-1)+(m-1)=L-1.
\]

For an OR gate `g <-> (a OR b)`, the charged DEF node exposes

\[
(\neg a\vee g),\qquad(\neg b\vee g),\qquad(a\vee b\vee\neg g).
\]

If the current source-derived clause is `(a OR b OR D)`, resolve first with `(not a OR g)` and then `(not b OR g)`. The result is `(g OR D)`. Repeating along clause `i` costs `2(k_i-1)` Resolution nodes and derives unit `(o_i)`.

For an AND gate `g <-> (a AND b)`, its facet `(g OR not a OR not b)` resolved with the already derived units `(a)` and `(b)` yields `(g)` in two Resolution nodes. The AND tree costs `2(m-1)` Resolution nodes. Therefore the displayed source-to-root macro costs

\[
G\text{ DEF}+2G\text{ RES}=3(L-1).
\]

This is an exact ledger for the displayed construction, not a lower bound on all derivations.

Now take any valid `R_mix341` refutation `pi` of `T(F)` of cost `q`. Introduce the same `G` fresh gates from `F`; map every free gate-clause source used by `pi` to the corresponding authenticated slot of its charged DEF node; map the source unit `(r)` to the replay-derived root; alpha-rename every proof-owned fresh variable away from the evaluator gates; copy every remaining node of `pi` in topological order. Its RES, AND3, GF(2), LOCAL-CONVERT and DEF nodes retain the identical typed formulas and antecedents, so no rule is specialized or retyped. Sharing is preserved. Thus

\[
W_{R_{\mathrm{mix341}}}(F)
\le q+3(L-1).
\]

Minimizing over `pi` proves the boxed inequality. The direction is essential: this is a source-proof **upper** bound obtained from an evaluator proof, not a lower bound on the evaluator or a runtime claim.

### Edge cases and scope

- Unit clauses require no OR gate. After duplicate clauses are removed, complementary unit sources yield an immediate direct Resolution contradiction; otherwise distinct unit literals can feed the AND tree.
- An empty clause is already contradiction at zero inference cost. The zero-clause CNF is SAT and has no honest refutation.
- Literal signs do not change the derivation.
- Private gates are deliberate. Arbitrary sharing is not silently treated as source-transparent.
- Every definition bank costs one DEF node; its clause facets are not free axioms in the source proof.
- The compiler is one fixed uniform source parser/build algorithm. It uses no per-input SAT label and no nonuniform per-length optimizer.
- The theorem applies to the explicitly declared `T(F)`. It does not say every equivalent circuit, implicit state, affine descriptor or poisoned evaluator retracts to `F`.

## Published lower-bound anchor: exact scope

For `h` holes and `h+1` pigeons, unary `PHP(h+1,h)` has `h(h+1)` variables, `h+1` positive pigeon clauses, and `h*binom(h+1,2)` binary collision clauses. With ordered signed binary variable indices, its explicit CNF encoding has `N_h=Theta(h^3 log(h+2))` bits.

Haken's theorem states that there exist constants `c>0,h0` such that for every `h>=h0`, **every** ordinary unrestricted shared-DAG Resolution refutation of this explicit CNF has at least `2^(c h)` lines. The system has authentic source clauses and binary Resolution only—no extension variables, GF(2), circuit axioms, semantic rule, SAT oracle or arbitrary algorithm. Therefore its encoded-length strength is `2^Omega((N_h/log N_h)^(1/3))` for this explicit family in ordinary Resolution.

It is not an ER, `Res(oplus)`, `R_mix341`, or machine lower bound. Cook's polynomial Extended-Resolution PHP proofs are the mandatory representation escape. Likewise, odd expander Tseitin formulas are hard for ordinary Resolution but have compact authenticated GF(2) refutations in `R_mix341`. No published restricted proof lower bound is transferred here to unrestricted SAT computation.

## Finite verification

The Python producer/checker generated all signed single-clause replay records of widths 1 through 7 (`254` polarity cases) plus AND chains of one through eight unit outputs (`8` cases), totaling `262`. It also built the two-variable UNSAT blocker

\[
(x\vee y)\wedge(x\vee\neg y)\wedge(\neg x\vee y)\wedge(\neg x\vee\neg y).
\]

Its private evaluator has `L=8`, seven DEF gates and fourteen replay Resolution nodes, hence 21 source-to-root nodes. From the forced evaluator root, a separate 13-step Resolution proof recovers the four clauses and refutes them, giving a complete 34-node splice. A SAT sibling was checked, and five malformed records were rejected.

The independent JavaScript verifier reconstructed every DEF facet, pivot and resolvent in that complete record and passed 94 checks. Raw SHA-256: `d72bd34cbfec0bb347ad3b100b4b34564bf5ead9a19f79a30fec8d1b16f6e730`.

Artifacts:

- `experiments/arc/lspv5_341/evaluator_cost_reflection_referee341.py`;
- `experiments/arc/lspv5_341/verify_evaluator_cost_reflection_referee341.js`;
- `results/raw/arc/lspv5_341/evaluator_cost_reflection_referee341.json`.

These checks validate the finite records and formulas. They do not certify global minima or reprove Haken.

## Fully charged physical ledger

The `3(L-1)` count is ideal logical DAG cost, not physical runtime.

| phase | explicit representation | compact/lazy alternative |
|---|---:|---:|
| source validation | `Omega(N)` adversarial reads; malformed/count/index checks | streaming counters use low space but still read the source |
| gate construction | `Theta(L log(n+L))` encoded bits | generate slots on demand; each query/recomputation is charged |
| replay conclusions | one width-`k` clause emits exactly `k^2-1` intermediate literal occurrences | parent/pivot instructions are near-linear, but the checker reconstructs clauses |
| total explicit replay payload | `sum_(k_i>=2)(k_i^2-1)+3(m-1)` conclusion literals, plus definitions | compact instruction stream shifts work to access/checking |
| splice | reads/writes the original proof bytes plus macro bytes and IDs | streaming saves space but pays recomputation or an ID map |
| verification | at least all source/proof bits plus rule validation | no free virtual clause, semantic equality or random access |
| peak space | source, active clauses, gates, proof and old/new ID map if materialized | smaller cache is allowed; rereads and lost DAG sharing are charged |

Thus explicit serialized replay can require `O((sum_i k_i^2+L) log(n+L))` bits—quadratic in `L` for one wide clause—even though the logical macro has only linear nodes. An exponential truth table or intermediate representation is allowed, but its construction, output, access and peak space are exponential and is dominated here by the compact circuit. The theorem is a proof-cost comparison, not a scheduled machine-time inequality.

## B1/B2/B3 classification

| obligation | result |
|---|---|
| source retraction for the declared `T(F)` | **PROVED/RESTRICTED**, overhead `3(L-1)` |
| arbitrary full-`R_mix341` proof downstream of exact `T(F)` | **PROVED/RESTRICTED** by unchanged typed replay |
| uniform indexed evaluator specialized to exact `T(F)` | **OPEN** |
| SAT in P -> short fixed-`R_mix341` reflection proofs | **OPEN** |
| B1 | **OPEN** |
| B2 | **OPEN** |
| B3 | **OPEN** |
| superpolynomial `Wbar_Rmix341`, unrestricted SAT lower bound, P versus NP | **OPEN** |

The precise next gap is a uniform polynomial normalization from a single all-length indexed evaluator, after `X=F`, to the declared private `T(F)`—including parser/multiplexer constants and aliases—or an alternative source-authenticated evaluator whose specialization is syntactically exact. Separately, one still needs polynomially short reflection proofs from `SAT in P`. The present cost-reflection theorem supplies neither premise.

## Five-role, Grok and Claude review

All five current specialists independently followed IDEA -> SEARCH -> ITERATE. LSPV-1 checked uniform quantifiers and limited the claim to the exact specialized evaluator. LSPV-2 checked arbitrary-width signs, definitions and affine/compact countercontrols. LSPV-3 audited DEF-slot certificate semantics and the full downstream mixed replay. LSPV-4 found the quadratic explicit-serialization counterexample and supplied the all-phase ledger. LSPV-5 attacked malformed inputs, poisoned branches, aliases, nonuniformity and reverse inequalities.

The latest Grok file actually reviewed was `GROKPROOF/2026-11-04_1518_PROGRESS.md`, blob `4e2bb9d941295f620a64e078117d29244caf4fba`; it leaves the arbitrary-decider fully charged transform open and supplies no source-retraction/B3 theorem.

Claude files actually checked were:

- `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`;
- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

They concern restricted direct-product, transport/alternation and one-tape ledgers. None proves universal evaluator normalization, reflection shortness, B3 or unrestricted SAT hardness.
