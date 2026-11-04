# REPRESENTATION-EQUIVALENCE-PADDING-FIREWALL-REFEREE331

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 23:48 PST**

**Status:** PROVED/EXACT impossibility of polynomial cost equivalence across unrestricted sound proof encodings; PROVED/EXACT directed polynomial-domination transfer for B3; PROVED/EXACT fully charged explicit-padding countercontrol; COMPUTATIONAL finite grammar controls. This is a synthesis and sharpening of project CLOCK-SUBCORE-B2-FIREWALL339 and COOK-RECKHOW-B3-TRANSFER-REFEREE317, not a novelty claim. `R_mix341`, its rules and weights are unchanged. B1/B2/B3 for that fixed calculus, superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness and P versus NP remain OPEN.

## Outcome first

The proposed algorithm- and representation-independent cost invariant cannot be polynomially equivalent to native proof cost across **all** sound representations.

Take any fixed sound complete proof calculus `R` and add a mandatory chain of exactly `2^|F|` locally checked administrative nodes before its contradiction is accepted. The resulting fixed system `Pad(R)` is still sound, complete and polynomial-time verifiable in the **explicit proof length**, but every refutation costs at least `2^|F|`. Conversely, a sound macro system can replace the chain by one binary `RUN(2^|F|)` record and retain essentially the base cost. The two systems carry the same underlying contradiction evidence, yet translation from the compact grammar to the explicit grammar has exponential output.

Therefore an intrinsic quantity can be robust in only one of two honest senses:

1. restrict admissible representations to a mutually polynomial-cost-equivalent class; or
2. minimize over all admitted sound representations, in which case artificial padding disappears and every compact circuit/GF(2)/extension/lazy macro remains a mandatory escape to defeat.

This is a concrete representation-independence counterexample. It is not a lower bound for the unchanged `R_mix341` or for arbitrary SAT algorithms.

## Established hard theorem: exact scope

Haken's 1985 theorem starts from the standard unary pigeonhole CNF `PHP(h+1,h)`: variables `x_(i,j)` say pigeon `i` uses hole `j`; every pigeon has one positive width-`h` clause, and every pair of pigeons has a negative binary collision clause for each hole. There are `h(h+1)` variables and `(h+1)+h*binom(h+1,2)` clauses. Under ordinary signed binary-index/DIMACS serialization the input length is `N_h=Theta(h^3 log h)`.

There are constants `c>0,h_0` such that for every `h>=h_0` and **every ordinary unrestricted shared-DAG Resolution refutation** `pi` of this explicit source, `|pi|>=2^(c h)`. Pivots and DAG sharing are unrestricted inside Resolution. The theorem does not quantify over Extended Resolution, Res(XOR), circuit or Horn rules, `R_mix341`, or arbitrary uniform SAT machines. Haken's abstract explicitly notes polynomial Extended-Resolution proofs for the same formulas. This is a proof-system lower bound, not all-algorithm SAT hardness. [Haken 1985](https://doi.org/10.1016/0304-3975(85)90144-6); [Cook--Reckhow 1979](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf).

The authoritative unchanged target grammar is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. It accepts explicit DIMACS CNF, rejects malformed encodings, gives source clauses zero cost, and charges each binary-premise RES, bounded-support AND3, GF(2) XOR, authenticated LOCAL-CONVERT or conservative two-input DEF node one unit; shared DAG nodes count once. Cook-style paid DEF+RES is a mandatory PHP escape, and its native GF(2) rule gives linear proofs for odd cubic Tseitin sources that are hard for ordinary Resolution. Haken and Tseitin lower bounds therefore do not transfer to full `R_mix341`.

## Lemma 1: fixed explicit padding

Fix any sound complete CNF refutation system `R` with verifier `V_R`. For a valid source `F`, let `n=|enc(F)|`. A `Pad(R)` proof contains:

- a valid `R` refutation `rho` ending in an `R` contradiction;
- a typed seed with the `(n+1)`-bit counter zero;
- exactly `2^n` unit-weight `TICK` nodes, each with the preceding tick as its sole parent and the next fixed-width binary counter value;
- one unit-weight `JOIN` whose parents are the `R` contradiction and counter value `2^n`, and whose conclusion is the only accepted terminal contradiction.

There is no skip, repetition, virtual-chain or macro rule. Types are disjoint. Consequently, for every valid UNSAT `F`,

`W_Pad(R)(F) = W_R(F) + 2^n + 1`.

Soundness holds because `JOIN` requires a valid `R` contradiction. Completeness holds by appending the unique chain to any `R` refutation. Local verification is uniform and effective. If `V_R` is polynomial-time in explicit source-plus-proof length, then so is the padded verifier: checking all explicit indexed nodes costs `O(n*2^n)` bit operations, which is linear up to an `n` factor in the supplied proof length. This is a Cook--Reckhow proof system despite its exponential shortest proofs.

This full-source construction is deliberately simpler than the prior source-subcore clock in `research/agents/lspv-1/2026-11-02_1530_LSPV-1_CLOCK_SUBCORE_B2_FIREWALL339.tex`, blob `afbb11451a178437e56a7a3220c50c7e7ebc9d8b`. That report already proves the stronger source-hereditary exact minimum and B2 failure. The present contribution is the representation-equivalence and B3 synthesis below.

## Lemma 2: no all-sound-representation polynomial cost invariant

Let `H_k` be the minimally UNSAT Horn chain

`x_1`, `(not x_1 or x_2)`, ..., `(not x_(k-1) or x_k)`, `(not x_k)`.

Its explicit binary-index source length is `N_k=Theta(k log k)`, and ordinary unit Resolution, hence `R_mix341`, refutes it in `O(k)` nodes.

Suppose an intrinsic source quantity `I(F)` were polynomially cost-equivalent to minimum proof cost in every sound representation. In particular, allow separate fixed polynomials for the base system and for `Pad(R)`:

`I(F) <= p(N+W_R(F))`, and `W_Pad(R)(F) <= q(N+I(F))`.

On `H_k`, the first inequality gives `I(H_k)<=poly(N_k)`. The second would then give `W_Pad(R)(H_k)<=poly(N_k)`. But Lemma 1 gives `W_Pad(R)(H_k)>=2^N_k`, a contradiction.

Thus no quantity is polynomially equivalent to native paid cost across an unrestricted class containing both a calculus and its sound explicit-padding encoding. This remains true even though the proof semantics and base contradiction evidence are identical.

A compact `RUN(2^n)` or doubling-DAG rule avoids the chain with `O(n)` encoded bits and `O(poly(n))` checking. That is a different sound grammar. `Pad(R) -> Macro(R)` is cheap in the length of the supplied padded proof: delete the ticks and emit the endpoint. `Macro(R) -> Pad(R)` must output `2^n` records and is exponential in the compact source proof length. An exponential backtranslation is not evidence of machine hardness or polynomial equivalence.

## Lemma 3: exact directed B3 transfer

For fixed proof systems `P,Q`, define polynomial **length domination** in the needed direction by

`D(P -> Q): exists polynomial p, for every UNSAT F, W_Q(F) <= p(|F|+W_P(F))`.

Then:

- `D(P -> Q)` implies `B3(P) -> B3(Q)`;
- a superpolynomial `Wbar_Q` plus `D(P -> Q)` implies superpolynomial `Wbar_P`;
- mutual domination makes B3 invariant between `P` and `Q`;
- a uniform polynomial-time proof translator is sufficient for domination but is strictly stronger than B3, which requires only after-the-fact proof existence.

The inequality direction is load-bearing. For padding, projection proves `W_R(F)<=W_Pad(R)(F)`, but B3 transfer into the padded system would require the opposite upper bound `W_Pad(R)(F)<=poly(N+W_R(F))`, which is false. A compact-to-explicit exponential expansion cannot replace it.

Under a hypothetical fixed uniform polynomial-time SAT decider `A`, the decider-induced Cook--Reckhow system `D_A` has linear statement-copy proofs: its verifier runs `A` and accepts exactly valid UNSAT sources, with soundness supplied by the all-input correctness premise. B3 for fixed `R_mix341` is exactly conditional polynomial length domination `D(D_A -> R_mix341)`. It does not require a proof producer. This equivalence was established in `research/main/2026-11-03_0948_MAIN_COOK-RECKHOW-B3-TRANSFER-REFEREE317.md`; no such domination has been proved.

## B1/B2/B3 classification of the countercontrol

Use one fixed total uniform exhaustive CNF decider `A_exh`: strictly parse or reject malformed strings, compact the `v` actually occurring variable identifiers, enumerate all assignments, and check the explicit clauses. In the declared binary-index encoding, `N=Omega(v log(v+1))`, so

`T_Aexh^wc(N) = 2^O(N/log N) * poly(N)`.

On the Horn chains, `W_Pad(R)(H_k)>=2^N_k`, while `T_Aexh(H_k)=2^O(k)*poly(N_k)=2^O(N_k/log N_k)`. Hence:

| obligation | padded system | unchanged `R_mix341` |
|---|---|---|
| B1 | **FALSE** for fixed `A_exh` | **OPEN** |
| B2 | **FALSE** for the same fixed `A_exh` | **OPEN** |
| B3 | `SAT in P -> false`, hence logically equivalent to `SAT notin P` | **OPEN** |

Because `Wbar_Pad` is unconditionally superpolynomial, B3 for the padded system must **not** be reported unconditionally false: the implication is vacuously true if SAT is not in P. Proving generic B3 for every sound complete effective proof system would already prove `SAT notin P`, equivalently P != NP. The safe exact conclusion is that soundness, completeness and polynomial-time verification do not yield polynomial boundedness, and cannot by themselves discharge fixed-system B3.

## Fully charged representation ledger

| representation/phase | encoded work and space |
|---|---|
| constant-size explicit tick token | `Theta(2^N)` output bytes and token reads |
| explicit `O(N)`-bit tick index | `Theta(N*2^N)` output/construction/verification bit work |
| streaming producer/verifier | exponential time/output; `O(N)` counter bits plus base-system workspace |
| materialized proof | exponential retained storage and peak live space |
| random access | cannot validate an accepted explicit chain without authenticating every required record |
| compact `RUN(2^N)` macro | `O(N)` description and polynomial arithmetic check, but a different rule/encoding |

Premature `END`, skipped or duplicated counters, wrong parent/source IDs, invalid base refutations, extra records and trailing bytes are rejected. Malformed sources are rejected before refutation semantics. A valid SAT source remains unrefutable even with a perfect tick chain. Exponential intermediate representations are included with their real costs; the compact alternative is also included and is exactly why the lower bound is representation-relative.

No arbitrary SAT decider is required to construct or verify `Pad(R)` proofs. Ideal node cost is therefore not physical machine runtime. Only an algorithm actually emitting or checking this explicit format pays the exponential output/access work.

## Four falsifiers

1. **Sound, complete, effective means polynomially bounded. — FALSE.** `Pad(R)` has all three properties and mandatory exponential minimum.
2. **Semantic equivalence makes proof cost representation-independent. — FALSE.** Explicit ticks and a compact endpoint macro have exponentially separated costs.
3. **A cheap padded-to-base projection transfers base boundedness into the padded system. — FALSE DIRECTION.** B3 needs base-to-padded polynomial length domination.
4. **B3 needs a uniform proof compiler. — FALSE.** Polynomial length domination suffices; p-simulation and proof construction are stronger. For `R_mix341`, even the weaker domination remains open.

## Grok, Claude, peers and search record

Issue #3 was read through 743 comments initially and current peer updates were checked. Relevant exact files include LSPV-1/382 `research/coordination/2026-11-03_2308_LSPV1_382_PEER_HANDOFF_AUDIT_ADDENDUM.md`, LSPV-2/381 `research/coordination/2026-11-03_2312_LSPV2_GUARD_DEPENDENT_AND2_RESTRICTION381_FIVE_ROLE_HANDOFF.md`, LSPV-3/386 `research/coordination/2026-11-03_2324_LSPV3_LOCAL_IMPLICATE_GUARD386_FIVE_ROLE_HANDOFF.md`, and LSPV-4/379 `research/agents/lspv-4/2026-11-03_2336_LSPV-4_SIGNED_GUARD_CVP379.md` (blob `597910a06696fe071752c80b2bfb3d3346b0ef22`). Their guard/circuit compilers are restricted, explicit-length results and do not supply full B3.

Current Grok `GROKPROOF/2026-11-04_0720_PROGRESS.md`, blob `06304e87e03b707fd7930f3b2c5a43d0c9c0cf9`, explicitly leaves the universal fully charged all-input transformation open and rejects transfer from restricted proof/circuit bounds. Current Claude files actually read were `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727d3e2b009cba7afec2a93beb62959dd67`), `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`) and the spectral-padding critique `2026-09-30_CLAUDE-0266_review.tex` (`694c1c8169d9a193397b94e6ee572c476e639a94`). They concern restricted alternation-trading/sequential models or counterexamples to unstable formula scores, not a proof-system-to-`R_mix341` bridge.

Primary searches covered Cook--Reckhow relative proof-system efficiency, polynomial boundedness and p-simulation, Haken's exact Resolution scope, and representation padding. Cook--Reckhow establishes that **some** polynomially bounded proof system exists iff `NP=coNP`; it does not bound every fixed system. A scoped `github.com/openai` search for a Cook--Reckhow/p-simulation/padding checker returned no applicable result; absence is not novelty evidence.

## Finite controls

The Python producer instantiated the declared explicit-unary and compact-macro grammars for source lengths 4 through 14, accepted exact padded UNSAT unit contradictions, rejected one-short and one-long chains, rejected compact macros in the unary grammar, and accepted them only in the separate macro grammar. It also rejected padded proofs for four SAT sources and eight malformed sources. It passed **86 assertions**. A separately written Node verifier independently checked **88 assertions** after the final B1/B2/B3 classification fields were added. Peak producer host RSS and exact artifact hashes are recorded in the raw ledger. These are grammar/cost controls, not a replay of Haken or a claim that the toy source grammar is `R_mix341`.

Artifacts:

- `experiments/arc/lspv5_331/proof_padding_firewall_referee331.py`
- `experiments/arc/lspv5_331/verify_proof_padding_firewall_referee331.js`
- `results/raw/arc/lspv5_331/proof_padding_firewall_referee331.json`

## Exact next gap

The phrase “independent of representation and algorithm” must now be made quantitative. The weakest viable next target is a source-authenticated invariant for the **fixed** `R_mix341`, or for a declared class of systems mutually polynomially cost-equivalent to it, that survives paid DEF, GF(2), shared circuits, lazy access and adaptive rule choice. If instead the invariant minimizes over every sound representation, its lower bound must also cover compact macros and decider-induced proof systems. Neither theorem is currently known.

P versus NP remains **OPEN**.
