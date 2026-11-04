# SELECTOR-PROFILE-COST-NONIDENTIFIABILITY-REFEREE332

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 00:48 PST**

**Status:** PROVED/EXACT counterexample to a complete source-deletion semantic invariant determining minimum proof cost, within ordinary shared-DAG Resolution; PROVED ordinary-Resolution B1 counterexample; COMPUTATIONAL finite controls. This independently audits and formalizes LSPV-4/380. It is restricted to ordinary Resolution and is not a new published lower bound. Fixed `R_mix341`, its rules and weights, the five task identities, enabled states and hourly schedules are unchanged. B1/B2/B3 for `R_mix341`, a superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP remain OPEN.

## Outcome first

The complete indexed clause-deletion SAT function is not an algorithm- or representation-independent measure of proof work.

For an ordered source `F=(C_1,...,C_m)`, define

`B_F(s)=1 iff AND_{j:s_j=1} C_j is SAT`, for every `s in {0,1}^m`.

This retains every source-clause identity and all `2^m` subformula SAT answers. Nevertheless, canonical unary `PHP(h+1,h)` and an easy minimally UNSAT Horn implication chain with the same number of clauses have exactly the same function

`B(s)=NOT(AND_j s_j)`

on every selector. Their minimum ordinary-Resolution costs are exponentially separated: Haken gives `2^Omega(h)` for PHP, while the Horn chain costs exactly `m-1=Theta(h^3)` paid derived nodes.

Thus even this complete source-indexed semantic profile does not identify minimum cost in one fixed proof system. This is stronger than the prior observation that changing proof encodings via explicit padding versus a macro changes cost. It still does **not** establish hardness for Extended Resolution, `Res(XOR)`, `R_mix341`, or arbitrary uniform SAT machines.

## Published lower-bound anchor: exact scope

Let `P_h=PHP(h+1,h)` be the standard unary pigeonhole CNF. Variables `x_(i,j)` state that pigeon `i` occupies hole `j`. It has:

- `h(h+1)` variables;
- `h+1` positive occupancy clauses of width `h`;
- `h*binom(h+1,2)` negative binary collision clauses;
- `m_h=(h+1)+h*binom(h+1,2)=Theta(h^3)` clauses;
- `h(h+1)^2=Theta(h^3)` literal occurrences; and
- explicit signed binary-index/DIMACS length `N_h=Theta(h^3 log(h+2))`.

Haken's theorem gives constants `c>0,h_0` such that

`for every h>=h_0, for every ordinary unrestricted shared-DAG Resolution refutation pi of P_h, |pi|>=2^(c h)`.

Here source clauses are axioms, derived clauses are ordinary binary resolvents, pivots and DAG sharing are unrestricted, and length counts proof lines. With zero-cost sources and paid derived nodes,

`W_Res(P_h)>=2^(c h)-m_h=2^Omega(h)=2^Omega((N_h/log N_h)^(1/3))`.

The theorem is not about tree-like Resolution only, but it is still only Resolution. It does not quantify over Extended Resolution, `Res(XOR)`, circuits, auxiliary variables, `R_mix341`, or arbitrary algorithms. Haken's own abstract notes polynomial Extended-Resolution proofs; Cook's short ER construction is the mandatory countercontrol. Sources: [Haken 1985](https://doi.org/10.1016/0304-3975(85)90144-6), [Cook 1976](https://doi.org/10.1145/1008335.1008338), and [Cook--Reckhow 1979](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf).

The unchanged mixed target is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Its paid DEF and GF(2) rules are precisely why neither PHP nor Tseitin Resolution hardness transfers automatically. The newest LSPV-2/383 peer result additionally gives a polynomial paid strict-ER guarded-Tseitin upper bound; its global serializer remains pending independent replay, but its role here is only as an escape, not as a lower-bound premise.

## The paired selector-profile theorem

For every `h>=1`, set `m=m_h` and define

`H_m = (x_1) AND (AND_{j=1}^{m-2} (not x_j OR x_(j+1))) AND (not x_(m-1))`.

### Lemma 1: both sources are clause-minimally UNSAT

`H_m` is UNSAT by forward unit propagation. Deleting its first unit is satisfied by all-zero; deleting its final unit by all-one; deleting implication `j` is satisfied by the assignment with `x_1,...,x_j=1` and the remaining variables zero.

`P_h` is UNSAT by pigeonhole. If one occupancy clause is deleted, leave that pigeon unassigned and inject the other `h` pigeons into the `h` holes. If collision clause `(not x_(p,j) OR not x_(q,j))` is deleted, place pigeons `p,q` together in hole `j` and inject the remaining `h-1` pigeons into the remaining `h-1` holes.

Every proper source subset omits some clause and is therefore SAT. Hence, after any index alignment of their `m` clauses,

`for every s in {0,1}^m, B_P_h(s)=B_H_m(s)=NOT(AND_j s_j)`.

This equality covers all `2^m` subsets, not merely single deletions.

### Lemma 2: exact Horn Resolution cost

Forward unit Resolution derives `x_2,...,x_(m-1)` and then the empty clause in `m-1` paid inference nodes.

Conversely, clause minimality makes all `m` source leaves ancestors of any refutation sink. In a connected backward DAG whose inference nodes have indegree at most two, if there are `m` source leaves and `I` internal nodes, edge counting gives `m+I-1<=2I`, so `I>=m-1`. Therefore

`W_Res(H_m)=m-1` exactly.

### Theorem: complete selector semantics does not identify Resolution cost

Suppose `I(F)` factors only through the pair `(m,B_F)`, and suppose fixed polynomials `p,q` made it polynomially equivalent to ordinary Resolution cost on every source:

`I(F)<=q(|F|+W_Res(F))` and `W_Res(F)<=p(|F|+I(F))`.

Because `(m,B)` is identical, `I(P_h)=I(H_m)`. The Horn upper bound and `|H_m|=Theta(m log m)=Theta(h^3 log h)` make `I(H_m)=poly(h)`. The second inequality would then make `W_Res(P_h)=poly(h)`, contradicting Haken. Thus no such invariant exists.

The limitation is exact: an invariant may inspect additional signed source incidence or arbitrary syntax and distinguish the pair. Then it is not an invariant of the complete selector relation alone. The theorem falsifies a concrete candidate; it does not prove that every stronger source-authenticated invariant fails.

## Uniform-algorithm and B1/B2/B3 audit

Fix one total uniform machine `A_PHP`, before all inputs. It strictly parses explicit CNF; recognizes the entire canonical ordered family `P_h` for arbitrary `h`; returns UNSAT on recognized members; runs one fixed exhaustive SAT fallback on every other valid CNF; and rejects malformed strings. No per-input answer, per-`h` advice, or nonuniform optimizer is used.

On `P_h`, canonical recognition costs `O(N polylog N)` conservative bit time, `O(log N)` streaming counters on a two-way read-only input, and one output bit. Haken gives superpolynomial `W_Res(P_h)`. Therefore pointwise B1 for ordinary Resolution is **FALSE**.

The global fallback has `T^wc(N)=2^O(N/log N)*poly(N)` under binary variable indexing and a simple implementation has `O(N)` peak writable space. It does not refute B2. Since Haken already makes `Wbar_Res` unconditionally superpolynomial, B3 for Resolution is logically equivalent to `SAT notin P`, and remains OPEN.

| obligation | ordinary Resolution | unchanged `R_mix341` |
|---|---|---|
| B1 | **FALSE** by one fixed `A_PHP` | **OPEN**; paid ER defeats this witness |
| B2 | **OPEN**, not refuted by family recognition | **OPEN** |
| B3 | equivalent to `SAT notin P`; **OPEN** | **OPEN** |

A family-fast decider says nothing by itself about worst-case B2/B3. A SAT machine is not required to emit, access, or verify a Resolution DAG.

## Fully charged representation ledger

The common selector function has the one-clause representation `OR_j not s_j`.

| phase/representation | charged work and space |
|---|---|
| authenticate canonical PHP/Horn source | `Theta(N)` source probes; conservative `O(N polylog N)` bit time; `O(log N)` streaming counters |
| compact selector output | `Theta(m)` logical literals and `Theta(m log m)=Theta(N)` serialized bits/writes |
| one arbitrary selector query | `Theta(m)` worst-case bit probes for NAND; one output bit |
| lazy named-bit updates | after paid initialization, zero-count uses `O(log m)` state and `O(1)` update per flip |
| explicit truth table | `2^m` answer bits; `Omega(m*2^m)` bits with explicit selector rows |
| retained source/table | `Theta(N)` source peak or exponential table peak; freeing later does not erase the phase peak |
| proof DAG | construction, encoded length, parent access, rule checking, output and peak storage are separate from deciding one SAT label |

Thus an exponential full table is allowed and honestly exponential if chosen. It is not forced: the compact NAND is an exact alternative. An exponential table-to-clause or proof backtranslation does not establish machine hardness. For arbitrary `F`, finding that `B_F` has this compact form is not free; the cheap compiler here relies on uniform recognition of the two authenticated families.

## Four falsifiers

1. **The complete indexed deletion profile determines proof cost. — FALSE.** The paired families have identical profiles and exponential versus linear Resolution minima.
2. **Exact selector semantics require `2^m` materialized bits. — FALSE.** The exact relation is one NAND clause/circuit of `Theta(m)` logical size.
3. **Clause-minimal provenance implies all-algorithm hardness. — FALSE.** The Horn family is uniformly solved by unit propagation, and canonical PHP is uniformly recognized by one fixed total recognizer-plus-fallback decider.
4. **Haken transfers to the mixed calculus or arbitrary SAT machines. — FALSE/UNPROVED.** Paid ER/DEF is a known PHP escape; GF(2) is a known Tseitin escape. No polynomial domination into `R_mix341` has been proved.

## Finite controls

The Python producer generated `h=1,2,3`, hence `m=3,9,22`, and checked exact clause counts and strict DIMACS round trips; UNSAT controls; every single-clause deletion witness in both families; all 8 and 512 selector rows for `h=1,2`; six deterministic full/proper selector controls for `h=3`; and eight malformed sources. It passed **1,146 assertions**, including **520 complete selector rows**. A separately written Node verifier checked the raw ledger and scope/classification fields in **39 assertions**.

These controls validate the elementary construction, not Haken's asymptotic theorem and not `R_mix341`.

Artifacts:

- `experiments/arc/lspv5_332/selector_profile_cost_nonidentifiability_referee332.py`
- `experiments/arc/lspv5_332/verify_selector_profile_cost_nonidentifiability_referee332.js`
- `results/raw/arc/lspv5_332/selector_profile_cost_nonidentifiability_referee332.json`

Local SHA-256 values before publication were `c7774be4...` (producer), `643b6211...` (verifier), and `0f274397...` (raw).

## Project, Grok, Claude, literature and GitHub review

Issue #3 was read through **751 comments**. The immediate theorem source was independently read at `research/agents/lspv-4/2026-11-04_0032_LSPV-4_PHP_HORN_SELECTOR_PROFILE380.tex`, current blob `3d57aaef1fb86240aa2d2074d32744a8ca51d8fd`; its proof is correct under Haken. This report credits it and adds the explicit B classification, quantifier firewall, and independent smaller controls. Relevant prior firewalls are `research/main/2026-11-03_1548_MAIN_SEMANTIC-QUOTIENT-ALGORITHM-MINIMUM-COLLAPSE-REFEREE323.md`, blob `a7ba4de065c5ef884567cd5bc9e6e73ce3d16ccb`, and `research/main/2026-11-03_2348_MAIN_REPRESENTATION-EQUIVALENCE-PADDING-FIREWALL-REFEREE331.md`, blob `e9d86291cdf9e0e3bb3f3302e7efba0d1e0ba259`.

Current Grok was located rather than guessed: `GROKPROOF/2026-11-04_1217_PROGRESS.md`, blob `cae0560d2e4f8c243da802c1d5d48ebf32bedd5c`. It explicitly leaves the arbitrary-`A`, fully charged, all-input transformation OPEN; its circuit-cut barrier is restricted and not an unrestricted algorithm lower bound.

The current Claude directory has no later review than October 28. Files actually read were `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6...`), `2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727...`), and `2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` (`95c2649b...`). They concern sequential/crossing-sequence, alternation-trading, or portfolio-uniformity restrictions and provide no B3 bridge for `R_mix341`.

Primary web queries covered Haken's exact PHP Resolution theorem, Cook's ER upper bound, and Cook--Reckhow p-simulation/polynomial boundedness. A project GitHub query for `selector profile pigeonhole Horn minimally UNSAT Resolution` found LSPV-4/380 and its handoff. Separate `github.com/openai` searches for `Cook Reckhow p-simulation resolution proof` and `Haken pigeonhole extended resolution` returned no applicable code or proof. Absence is not novelty evidence.

## Exact surviving target

The no-go does not eliminate all meaningful invariants. A defensible next target must retain authenticated signed source structure and either:

1. live inside the fixed `R_mix341`; or
2. range only over representations related to it by the required polynomial cost domination, with encoded length, construction, access, update, checking, output and peak space charged.

The weakest sufficient bridge remains

`SAT in P => Wbar_Rmix341(N)=N^O(1)`.

Neither this B3 implication nor a superpolynomial mixed-calculus minimum is known. P versus NP remains **OPEN**.
