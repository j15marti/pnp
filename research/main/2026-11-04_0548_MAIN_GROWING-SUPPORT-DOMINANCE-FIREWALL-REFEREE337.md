# GROWING-SUPPORT-DOMINANCE-FIREWALL-REFEREE337

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 05:48 PST**

**Status:** **PROVED/EXACT** parity-chain target-derivation optimum in the fixed binary-premise rules; **PROVED/RESTRICTED** exact-output circuit-counting separation only for a deliberately permissive growing-support completion; **PROVED/RESTRICTED** dominance bypass showing that separation does not lower-bound a cheapest refutation; **DUPLICATE/SYNTHESIS** relative to REFEREE313/334/335 and LSPV-1/380; **OPEN** full `R_mix341` grammar promotion, B1, B2, B3, superpolynomial mixed worst-case cost, and P versus NP. No task, schedule, state, rule, weight, or ownership was changed.

## Outcome

The attempted new route fails in the scientifically important direction.

A growing-support `LOCAL-CONVERT` node can hide a Boolean condition requiring exponentially many fixed-basis circuit gates while costing one logical node. This defeats a theorem that must preserve every node's exact output in `poly(N+q)` bits. It does **not** defeat whole-refutation normalization or establish a large minimum `W_R`: the hard condition is a weaker consequence of an already available premise and has a one-node-shorter dominance bypass.

The result is outside the unchanged literal calculus, whose authoritative prose requires a `bounded-support Boolean circuit condition` justified by an `explicit constant-support truth-table check`. It is therefore a counterexample to a permissive completion and to an invalid quantifier promotion, not a newly legal `R_mix341` proof.

This run also found that the mechanism is not project-new. REFEREE334's `Pack(R)` already separates paid node count from arbitrarily long payloads; REFEREE313 already proves stronger-representation aliasing; REFEREE335 proves literal constant-support private-root normalization while charging raw access; and LSPV-1/380 charges compilation in supplied length. The present value is a single exact hostile control that simultaneously exhibits the large exact output and its refutation bypass.

## Established published lower-bound anchor: exact model, encoding, quantifiers, strength

Start from Haken's 1985 lower bound for the standard unary pigeonhole contradictions `PHP(h+1,h)`. The explicit CNF has variables `x_(p,j)`, one clause requiring each of `h+1` pigeons to occupy one of `h` holes, and pairwise negative clauses forbidding two pigeons in the same hole. Source clauses are free axioms. Every derived line is a clause obtained by ordinary binary Resolution on a complementary pivot. Width, pivot choice, line reuse, and shared-DAG structure are unrestricted; no extension variables, XOR equations, semantic circuit rules, or machine steps are present.

In the project theorem form, there exist constants `c>0,h0` such that for every `h>=h0` and every ordinary shared-DAG Resolution refutation `pi` of this explicit formula,

`|pi| >= 2^(c h)`.

There are `h(h+1)` variables and `(h+1)+h*binom(h+1,2)=Theta(h^3)` clauses. With explicit signed binary variable indices in a DIMACS-style representation, `N_h=Theta(h^3 log(h+2))`; hence the bound is `2^Omega((N_h/log N_h)^(1/3))`, not `2^Omega(N_h)`.

It is **not** a lower bound for Extended Resolution, Extended Frege, `Res(XOR)`, `R_mix341`, or arbitrary uniform SAT deciders. Haken's abstract itself records the polynomial Extended Resolution escape. Cook--Reckhow concerns encoded proof systems and relative proof length, not physical SAT runtime or the project's arbitrary unit-node grouping.

Primary sources actually checked: A. Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`; S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1) (1979), DOI `10.2307/2273702`; S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), DOI `10.1145/1008335.1008338`.

## Fixed `R_mix341` and the exact grammar obstruction

The authoritative file is

`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

It fixes ordinary DIMACS CNF input, free authenticated source clauses, unit-paid at-most-binary-premise `RES`, support-three `AND3`, binary GF(2) row addition, unary `LOCAL-CONVERT`, and one fresh conservative two-input `DEF` gate per paid node. The exact `AND3` numeric bound is three original variables. `LOCAL-CONVERT` says bounded/constant support but does not serialize one global numeric `K`, the union-support scope, or a complete malformed-record parser.

Consequently, two completions must not be conflated:

1. **Fixed-global-`K` typed private-root completion.** LSPV-1/362 and REFEREE336 give polynomial ER compilation. `K` is fixed before the source, size, and proof.
2. **Growing-support completion.** A node may use `K=m` on the `m`th input. The counterrecord below is legal only here. Treating `(3K-1)2^K` as a uniform constant in this completion is invalid.

Neither completion supplies B3.

## Lemma 1: exact wide-parity target cost in the literal fixed rules

For `m>=2`, use original variables `x_1,...,x_m` and prefix variables `z_2,...,z_(m-1)`, with `z_1` an alias for `x_1`. For every `2<=i<=m-1`, encode

`z_(i-1) XOR x_i XOR z_i = 0`

by its four canonical width-three clauses. Finish with the two clauses encoding `z_(m-1)=x_m`. Call the resulting SAT source `F_m`. It has `4m-6` clauses and explicit signed-DIMACS length `N=Theta(m log m)`.

Three `AND3` nodes conjoin each four-clause block into its exact GF(2) row; one `AND3` node extracts the final equality; and `m-2` native `XOR` nodes sum the `m-1` rows. The result is

`P_m := [x_1 XOR ... XOR x_m = 0]`

in `3(m-2)+1+(m-2)=4m-7` paid nodes.

This cost is exact for deriving this target. Delete a clause in an XOR3 block. Its unique forbidden local triple `(a,b,c)` has odd parity. Set the earlier prefix to `a`, use `x_i=b,z_i=c`, keep every later prefix equal to `c`, and set the final `x_m=c`; all undeleted clauses hold and the total `x` parity is odd. Deleting either final equality clause similarly permits exactly one unequal final pair and an odd `x` assignment. Therefore every one of the `4m-6` sources is indispensable for implying `P_m`. In any sound conservative at-most-binary-premise target derivation, all sources must lie in the target's ancestry; connectedness and total indegree at most twice the number of paid nodes give `q>=4m-7`.

This is a linear exact target-derivation theorem, not a superpolynomial refutation lower bound.

## Lemma 2: growing-support exact-output normalization can fail

Now deliberately enlarge `LOCAL-CONVERT` so a support-`m` truth-table implication may cost one node. On odd assignments let `H` be arbitrary and define

`Q_m = P_m OR H`.

Every such conversion is sound because `P_m => Q_m`. Fix one odd assignment `beta` and require `H(beta)=0`. There remain exactly

`2^(2^(m-1)-1)`

distinct legal exact outputs, and every `Q_m` implies the width-`m` blocker clause `C_beta`, which is false only at `beta`.

Fix a finite fan-in-at-most-two basis with `b` opcodes. The number of circuits with at most `s` gates on `m` inputs is at most

`(s+1)(m+s+2)[b(m+s+2)^2]^s`.

For `s<=2^m`, put `D_m=2m+2+ceil(log_2 b)`. The base-two logarithm of the displayed count is at most `2m+2+sD_m`. Therefore some legal `Q_m` requires at least

`1 + floor((2^(m-1)-2m-4)/D_m) = Omega(2^m/m)`

gates. Restricting any circuit for `Q_m` to odd inputs, or in the simpler cylindrical construction setting its guard input to zero, recovers the selected hard truth table. This is a standard counting argument over a fixed deterministic circuit representation. It does not cover arbitrary existential representations or semantic macros.

Add the source units `x=beta`. The fixed parity source plus those units is UNSAT. A growing-support derivation can use `P_m -> Q_m`, `Q_m -> C_beta`, and `m` Resolution steps with the units, for `5m-5` paid nodes. Hence the hard output can even be placed in the contradiction ancestry.

The conclusion is limited but exact: a theorem requiring a same-DAG, nodewise-extensionally-equal `poly(N+q)`-bit representative for **every** growing-support proof record is false.

## Lemma 3: dominance bypass defeats the proposed transfer to `W_R`

The same construction gives its own counterexample to the intended lower-bound use. Because `P_m=>Q_m=>C_beta`, the proof may replace the two conversions by the single conversion `P_m=>C_beta`. It then has `5m-6` nodes and never represents `Q_m`.

More generally, in a positive extensional consequence calculus closed under stronger-premise substitution, a unary consequence `P=>Q` is dominance-redundant. If a child was sound from `Q` and other premises, it remains sound from the stronger `P` and those premises. Repeating the substitution and pruning preserves a subset invariant through the descendant DAG. An unused node disappears by ordinary backward-ancestor pruning.

This bypass is not asserted for every intensional child type of literal `R_mix341`: native syntax inspection, negated use of a condition as data, equality-sensitive consumers, hidden shared witnesses, or support/type changes require separate rules. But it is enough to falsify the proposed representation-independent inference. Exponential exact output complexity of one legal consequence does not lower-bound the cheapest refutation.

## Fully charged physical ledger

Let `M=2^(m-1)-1` be the free odd-row table payload.

| object/phase | logical nodes | charged work | output/encoding | peak space |
|---|---:|---:|---:|---:|
| fixed parity target | `4m-7` | source parse plus row construction and mask operations | `poly(m)` | schedule-dependent |
| explicit hard-`Q` table | `1` in permissive completion | `Omega(M)` construction/read/output for exact preservation | `Theta(M)` | `Theta(M)` if retained; streaming can be smaller |
| fixed-basis hard-`Q` circuit | `1` outer node | at least emitted/accessed gate volume | `Omega(M/log M)` gates; conventional gate indices give `Omega(M)` bits | materialization/recomputation tradeoff |
| direct dominance bypass | one fewer node | no `Q` construction or access | `poly(m)` | `poly(m)` implementation available |
| supplied proof record | unchanged | a faithful exact normalizer may need every payload bit | total input `L=Theta(M)` | indexed reread can lower writable space |
| lazy descriptor | descriptor nodes only | construction, queries, recomputation, implication/equality validation charged | compact only if representation permits it | schedule-dependent |

The apparent exponential overhead is relative to the undercharged parameter `N+q`. It is near-linear or polynomial in the supplied record length `L`. A SAT decider receives the source, not an obligation to manufacture the adversarial `Q`; the direct bypass ignores it. No physical runtime lower bound follows. Materializing then freeing `M` bits still incurs that construction and all-phase peak; streaming may reduce peak but not produced/accessed volume.

The hard `Q_m` is obtained nonuniformly by counting. Naming it succinctly would hide advice or a semantic oracle. A lexicographically first hard table is computable only with enormous charged search. No explicit uniformly generated general-circuit-hard family—and no arbitrary-algorithm SAT lower bound—is obtained.

## Four falsifiers and disposition

1. **A growing-support `LOCAL-CONVERT` is already legal literal `R_mix341`. — NOT CERTIFIED.** The authoritative rule says constant support and lacks a global numeric/parser completion.
2. **An ancestral exponentially complex `Q_m` forces a large minimum refutation. — FALSE.** The stronger `P_m` gives a one-node-shorter bypass.
3. **Shannon counting supplies a uniform all-size hard family. — FALSE.** It supplies existential/nonuniform functions only.
4. **Exponential exact-output backtranslation proves machine SAT hardness. — FALSE.** It is polynomial in the explicit payload length, and a source-only solver or proof can avoid the payload.

## B1/B2/B3 and representation-independence classification

| statement | status after this run |
|---|---|
| fixed-global-`K` typed compiler | prior PROVED/RESTRICTED; unchanged |
| every growing-support node has `poly(N+q)` exact representation | FALSIFIED in the permissive completion |
| polynomial normalization of cheapest full `R_mix341` refutations | OPEN |
| B1 | OPEN; no arbitrary-decider trace compiler |
| B2 | OPEN; no universal worst-case domination |
| B3 | OPEN; `SAT in P` still does not yield polynomial `Wbar` for this fixed system |
| unrestricted computational hardness / `P!=NP` | OPEN |

This candidate invariant therefore **fails** as an algorithm- and representation-independent lower-bound route. The surviving statement is only a representation-restricted exact-output separation plus a warning that exact node preservation is stronger than refutation simulation.

## Finite controls and malformed cases

The Python producer exhaustively checked the parity chain for `m=2,...,7`, all assignments to source and prefix variables, every source-clause deletion witness, even-pinned SAT and odd-pinned UNSAT controls, and every ancestral hard-`Q` table for `m=2,...,5`. It also checked the circuit-count inequality through width 64 and strict-versus-permissive grammar controls: **3,157,775 checks PASS**.

The independent Node verifier recomputed parity/blocker implications, node ledgers, sampled counting bounds through width 52, both labels, and bridge status: **312 checks PASS**. Five malformed records were rejected: wrong table length, non-bit row, duplicate support alias, unauthenticated private wire, and cyclic payload. A strict fixed-`K=3` parser rejected the width-nine permissive record.

Artifacts:

- `experiments/arc/lspv5_337/growing_support_dominance_referee337.py`
- `experiments/arc/lspv5_337/verify_growing_support_dominance_referee337.js`
- `results/raw/arc/lspv5_337/growing_support_dominance_referee337.json`

Finite tests do not prove the asymptotic counting lemma; that proof is the displayed enumeration bound.

## Project duplication, five-role review, Grok and Claude

All five existing specialists audited the candidate. LSPV-1 supplied the exact counting bound and found the ancestral bypass; LSPV-2 independently verified the parity-chain derivation and both labels; LSPV-3 isolated rooted pruning and positive-premise dominance; LSPV-4 supplied the fully charged table/circuit/streaming ledger; LSPV-5 identified the project duplicates and the nonuniformity firewall.

Relevant existing project artifacts actually read:

- REFEREE334 `research/main/2026-11-04_0248_MAIN_NODE-BIT-NORMALIZATION-OPTIMAL-SYSTEM-FIREWALL-REFEREE334.md`, blob `1750c42dabcd72a7fef379a9f9fba001eceaea77`;
- REFEREE313 `research/main/2026-11-03_0548_MAIN_SAME-SUPPORT-ALIAS-COMPILER-REFEREE313.md`, blob `393c614989e6a410cd8b3e520c82a9d361e64911`;
- REFEREE335 `research/main/2026-11-04_0348_MAIN_EXTENSIONAL-NORMALIZATION-ACCESS-FIREWALL-REFEREE335.md`, blob `d47094c22297ca89d40104156ff41323480a0734`;
- LSPV-1/362 `research/agents/lspv-1/2026-11-03_0455_LSPV-1_LOG_SUPPORT_FACTOR_ER362.tex`, blob `e0e793fcdd43d828a5f956d2f62a09b0d587f6c4`;
- REFEREE336 `research/main/2026-11-04_0450_MAIN_FIXED-K-ER-EQUIVALENCE-GRAMMAR-GAP-REFEREE336.md`, blob `642652d2344520382a16b53ec1287e6203c0eea9`.

The actual current Grok file is `GROKPROOF/2026-11-04_1322_PROGRESS.md`, blob `0850246c1a1ea9a511d12a4de041b8752f69922a`. It proves only a restricted self-reducibility volume barrier and explicitly leaves the fully charged arbitrary-`A` transformation open.

Claude has no post-October-28 assessment. The relevant current reports are `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` (blob `95c2649b...`), `2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727...`), and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6...`). They concern restricted direct-product/portfolio/alternation-trading/sequential-access models and provide no fixed-`R_mix341` B3 bridge.

Issue #3 was read through the current LSPV-1/389, LSPV-2/390, LSPV-3/393, and LSPV-4/385 updates before publication. Project searches for `Pack(R) payload LOCAL-CONVERT` and `stronger representation aliasing` found the duplicate mechanisms above. Searches in `github.com/openai` repositories for an Extended Resolution proof checker returned only irrelevant lexical matches; absence is not novelty evidence.

Research queries logged: `Haken 1985 intractability of resolution pigeonhole principle PDF`; `Cook Reckhow relative efficiency propositional proof systems 1979 PDF extended resolution`; project searches for `LOCAL-CONVERT`, `Pack(R)`, `stronger representation aliasing`, `GROKPROOF`, and `research/agents/claude`; GitHub/OpenAI search `extended resolution proof checker`.

## Next exact gap

Freeze one authoritative `LOCAL-CONVERT` parser: a global union-support bound, original/auxiliary tags, private-wire semantics, accepted representations, and malformed behavior. Then mechanically validate the fixed-`K` compiler. Scientifically, the load-bearing obligation remains B3: from `SAT in P`, obtain polynomial worst-case minimum cost for this same preselected fixed calculus without assuming that an arbitrary rejecting trace is already a sound proof.

**B1 OPEN; B2 OPEN; B3 OPEN; superpolynomial `Wbar_Rmix341` OPEN; P versus NP OPEN.**
