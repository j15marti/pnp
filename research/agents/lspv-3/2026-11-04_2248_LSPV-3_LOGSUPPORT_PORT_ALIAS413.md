# LSPV-3/413 | Source-authenticated two-port aliases for logarithmic original support

**November 4, 2026, 22:48 PST. PROVED/EXACT within an explicitly assumed readable-DEF-facet + strict RES fragment only; independent COMPUTATIONAL replays. Native `R_mix341` grammar, B1/B2/B3, superpolynomial mixed hardness and P versus NP remain OPEN.** No agent identity, task schedule, enabled state, inference rule or weight changed.

## IDEA (before searching), falsifiers

Hypothesis: two distinct outputs `p,q` of a shared acyclic bank of `t` individually paid two-input Boolean DEF gates with only `k` original inputs, whose Boolean functions agree on all `2^k` original valuations, admit **strict Resolution proofs** of both implications in `O(t2^k)` additional paid nodes if each authentic gate CNF facet is independently RES-addressable.

F1 repeated input wires invalidate contextual derivation; F2 reconvergence / shared subcircuits lose a needed literal; F3 a single XOR→XNOR mutation passes equality verification; F4 original native DEF and LOCAL grammar does not authorize the assumed facet selector. F1/F2 passed, F3 failed as predicted, **F4 OPEN** and bars native promotion.

## SEARCH: actual files, queries, restrictions

First read governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` commit `4e29ed7`, verified blob `033b54b8`, then issue #3 and recent peer handoffs; original `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11`; LOCAL addendum `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` blob `bbcdad9a`; AGENTS, CODEX, repository skill, LSPV-2/409, LSPV-3/412, LSPV-4/404, REFEREE354. Grok `GROKPROOF/2026-11-04_2315_PROGRESS.md` blob `f5b8ef62` and actual Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727`) and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6`) were read. None proves native LOCAL or B3.

General-web queries: `Cook Reckhow 1979 relative efficiency propositional proof systems polynomially bounded iff NP coNP`; `Haken 1985 intractability resolution pigeonhole explicit lower bound`; `Raz Tzameret 2008 resolution over linear equations parities extended resolution`; `Davis Putnam 1960 computing procedure quantification theory resolution elimination SAT`; `Seidler Minimal Circuits Boolean Functions Few Variables arbitrary binary gates 2022`. Read Cook's original author publication page https://www.cs.toronto.edu/~sacook/ and Weizmann's publisher metadata https://weizmann.esploro.exlibrisgroup.com/esploro/outputs/journalArticle/Resolution-over-linear-equations-and-multilinear/993262684803596. Journal full text access was restricted. **Direct Google-branded UI unavailable**, so no claim of direct Google search.

Authenticated `github.com/openai` queries: `ExecCNFNodeSearchCosts`, `LRAT`, `Tseitin proof`, `resolution proof checker`, `CookLevin`. Full sources read: `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f4` and `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean` blob `1e23a159`; neither supplies same-R source-authenticated proof translation. Contextual Resolution overlaps project LSPV-3/412; new contribution is the **parameterized pairwise alias proof** for arbitrary k, not an independent novelty claim for the method.

## Theorem 413.1: restricted exact upper bound

Let `k≥1,t≥2`, let `D` comprise `t` globally fresh, conservative, acyclic, paid arbitrary binary Boolean DEF gates whose inputs reference only `k` original variables or prior gates. Let `p,q` be distinct gate outputs and assume

$$
\forall a\in\{0,1\}^k,\quad f_p(a)=f_q(a).
$$

**Additional interface assumption:** every non-tautological defining CNF facet of a paid gate is an individually selectable strict-RES premise, with the facets attributed to the gate's already paid node. This is not ratified by the original /341 byte grammar.

Then strict RES derives a clause contained in each of `¬p∨q` and `p∨¬q`, with at most

$$
\boxed{q_{\rm RES}\le2t2^k+2(2^k-1)}
$$

new distinct RES nodes. Including the existing paid definitions, `q≤t+(2t+2)2^k-2`.

**Proof.** For each complete input assignment `a`, let `B_a` be the clause falsified precisely by `a`, and `L_{v,a}` the actual signed value literal of gate `v`. The correct gate-defining CNF facet for `v=g(u,w)` is `¬L_{u,a}∨¬L_{w,a}∨L_{v,a}`. Resolve away at most two earlier gate-input literals using previously derived contexts, leaving `P_{v,a}⊆B_a∨L_{v,a}` at a cost ≤2 RES per gate per assignment. The true output literal remains, since erasing it would produce an implicate falsified by the unique satisfying extension of `a`. For the target `¬p∨q`, choose `P_{p,a}` if `p(a)=0`, or `P_{q,a}` if `p(a)=1`. These are subclauses of `B_a∨(¬p∨q)`. Pair opposite bit contexts using Resolution when both blocker literals occur, or keep the stronger one; at most `2^k-1` steps yield a subclause of the target. Repeat symmetrically for `p∨¬q`. Thus at most `2t2^k+2(2^k-1)` added nodes. The source formula is unchanged. QED.

**Source provenance firewall:** `F=(x),p=x,q=1` gives equality on source models but not on all original assignments; DEF-only semantic equality is false at `x=0`. Source-conditional equality requires source-clause usage and authentic ancestry. This theorem does not license implicit reuse of unexported LOCAL wires, DEF facets in the original grammar, GF(2) row exports, or AND3 type changes.

## ITERATE: independent verification and exact costs

Deterministic Python producer (seed `317k`) constructed full gate/facet/RES evidence for `k=1,2,3,4,5,6`. Every step has exact signed literals, parent identifiers and real complementary pivot. Separate JavaScript checker reconstructed source facets, evaluated all original inputs, replayed every strict inference and independently checked two output subclauses. **66,167 independent JS assertions passed**, including six corrupted-pivot rejections; the mutated XNOR counterexample was rejected. Same-variable-universe `(x_1)` SAT and `(x_1)∧(¬x_1)` UNSAT controls had 8 and 0 assignments; two malformed gate controls rejected.

|k|paid t|actual extra RES|proved extra RES bound|
|--:|--:|--:|--:|
|1|4|10|18|
|2|4|22|38|
|3|5|54|94|
|4|6|126|222|
|5|7|286|510|
|6|8|638|1150|

Raw full six-fixture signed proof certificate SHA256 `ed09972dfcacb20d8343fa28a03251bf18a95c2ea62461f55913d8e9b24c2353`, generated by accompanying archived Python source. **These are constructed upper bounds, not certified minima.** The proof is symbolic; tests are finite.

For `k≤c log_2(N+E+2)`, with fixed `c` and complete explicit source+old evidence length `N+E`, both logical cost and flat binary proof bits are polynomial in `N+E`. Constructed evidence uses `O((t2^k+N)log(t2^k+N+2))` bits for constant-size gate tables and flat indices (plus required original evidence). Source parsing, truth-table acquisition, failed checks, pivot access, writes, validation and output memory are separately charged; naive buffered bit-time `O(M^3)` and bit-space `O(M^2)` in complete evidence/output size `M=N+E+q+2` are conservative, not FLMV time-space bounds. Arbitrary unpaid giant LOCAL payloads are not covered.

## Hardness and transfer

Haken's ordinary shared-DAG Resolution unary PHP lower bound is `2^{Ω(h)}` for `PHP_(h+1)^h`, with `h(h+1)` variables, `h+1+h*binom(h+1,2)` source clauses and `Θ(h^3 log h)` signed-index bits; it is not a mixed-R or machine bound. Cook's Extended Resolution short PHP construction and affine odd-Tseitin XOR refutation remain countercontrols. The proof system described by Raz–Tzameret is not the fixed `R_mix341`.

**Native full rule translation, noncircular same-fixed-R B3, B1/B2 and superpolynomial mixed minimum remain OPEN.** No polynomial decider correctness is presumed and no source-independent UNSAT axiom is introduced. Prior /412's `113t+r` theorem is unaffected; our theorem specifically addresses two equal named ports over unbounded but parameterized original support.

**Next:** Freeze exact native DEF facet selectors and LOCAL circuit/export/GF(2) grammar from the original version, and test whether every authenticated consumer can be replayed with paid bit normalization. Separately audit whether any all-algorithm same-R B3 argument exists without a correctness reflection assumption. Root `main.tex` must only be reconciled inside LSPV-3 ownership after complete current readback.
