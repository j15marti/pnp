# LSPV-1/401: PHP cofactor-miter hardness versus semantic zero support

**November 4, 2026, 15:00 PST, America/Los_Angeles.**  
**Status: PROVED/EXACT elementary derived theorem in ordinary source-only shared-DAG Resolution, specialist review pending; KNOWN THEOREM published Haken/Cook; COMPUTATIONAL finite controls.** The unchanged fixed system is **R_mix341**, with free authenticated original sources and unit-weight paid RES, AND3, GF(2) XOR, LOCAL-CONVERT and conservative two-input DEF as specified by LSPV-2/341 (blob `c87acd11`). No assertion that a superpolynomial lower bound holds in this combined system; B1/B2/B3 and P versus NP remain **OPEN**.

## IDEA before searching, with falsifiers

Proposed mechanism: perhaps the signed-hypergraph/DAG invariant should be **the cost of certifying that a variable is semantically inessential**, instead of raw number of graph vertices or exposed circuit ports. Falsifiable prediction: a zero-support Boolean circuit may still have a cofactor-difference miter whose source-only Resolution proof is exponentially long. The test must start from Haken's certified pigeonhole family, not new random formulas.

F1: a constant-zero semantic output forces a short **ordinary Resolution** proof of its cofactor equivalence. F2: auxiliary context units can invalidate the inherited PHP lower bound. F3: changing one original PHP collision clause cannot make the cofactor SAT and thereby reveal the hidden variable's influence. F4: source-only Resolution hardness extends to a correct uniform SAT decider, paid auxiliary gates, GF(2), or Extended Resolution.

## SEARCH and duplication audit

Read the governing November 2 12:04 worst-case-minimum directive, current issue #3, original LSPV-2/341, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-1/319 source-indexed cofactor XOR miter (blob `61ab2fa`), LSPV-1/398 Haken-vs-ER backtranslation firewall, LSPV-3/403 coNP-complete semantic-support checking (blob `6aa1602`), and REFEREE346 tiny-output-support barrier (blob `32aa1ed`). These earlier results already establish generic miter equivalence, support-validation hardness, and PHP Resolution/ER separation. **The current contribution is their exact source-preserving quantitative composition for every cofactor of an identically-zero circuit, with an independently tested SAT clause-deletion sibling.** It is not a new general lower-bound technique.

Actual external web search queries: `Haken 1985 intractability of resolution pigeonhole`, `Cook 1976 pigeonhole extended resolution`, `Automating Resolution is NP-Hard Atserias Muller`, `Cook Reckhow 1979 relative efficiency`, `essential support Boolean circuit cofactor miter SAT`, and `Provable Reductions in TFNP 2026`. Read Cook-Reckhow's publisher entry, ECCC TR26-109, Atserias-Müller's JACM publisher/author record, and Sonobe's 2022 open-access paper reviewing Cook's PHP ER construction. Sources below. The original Haken full text was not accessible through the available search and the known theorem was inherited from independently reviewed project records and published bibliographic/secondary accounts. Google-branded direct access was unavailable; general web search was used, not represented as a direct Google search.

Actual authenticated github.com/openai code-search queries: `ExecCNFNodeSearchCosts`, `SAT correctness`, `Cook Levin`, `ExtendedResolution`, and `proof checker`. Results include `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` and `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean`; these are relevant accounting/formalization context but provide **no** missing B3 compiler. Non-proof-theoretic uses of "resolution" were excluded. Read actual `GROKPROOF/2026-11-04_2215_PROGRESS.md` (blob `3521be6`) and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d`). Grok's purported strict inequality `Omega(N^1.1)>N^(1.1+o(1))` is **invalid** without a larger exponent or coefficient argument; project LSPV-1/399 already corrected it. Neither peer establishes B3.

## Exact known hardness anchor

For each integer h≥1, let `P_h` be the ordinary unary pigeonhole signed CNF over variables `p_{i,a}` for `1≤i≤h+1`, `1≤a≤h`:
$$
P_h = \bigwedge_{i=1}^{h+1}(\bigvee_{a=1}^h p_{i,a})
\wedge
\bigwedge_{a=1}^{h}\bigwedge_{1\le i<j\le h+1}
(\neg p_{i,a}\vee\neg p_{j,a}).
$$
It has `h(h+1)` original variables and
$$
m_h=(h+1)+h\binom{h+1}{2}
$$
source clauses. With an explicit, signed, binary-index variable-ID encoding (including source grammar and clause boundaries), `N_h=Theta(h^3 log(h+2))` bits. **KNOWN THEOREM (Haken 1985, exact model)**: there exist constants `c>0,h_0` such that for **every** `h≥h_0` and **every** authentic ordinary unrestricted **shared-DAG Resolution** refutation `π` of this source `P_h`, `|π|≥2^(c h)` lines (equivalently paid derived-node count at least `2^(ch)-m_h` when sources are free). No paid DEF, GF(2), AND3, LOCAL-CONVERT, implicit proof, machine step, or semantic oracle is covered. **KNOWN THEOREM (Cook 1976)**: the same `P_h` has polynomial-size Extended Resolution refutations.

## ITERATE: a quantified semantic-zero, hard-miter theorem

For **every** `h≥1` and `k≥1`, let `x_1,...,x_k` be fresh, and let `f_h(u)` be the Boolean evaluator of `P_h`. Define one explicit fan-in-two circuit
$$
C_{h,k}(x,u)=f_h(u)\wedge (x_1\vee\dots\vee x_k).
$$
The circuit has polynomial explicit gate and signed-ID length, `O((h^3+k) log(h+k))` bits with straightforward clause-private evaluation. For **every** original input assignment, `f_h(u)=0`, so **every** essential input is absent:
$$
\operatorname{Ess}(C_{h,k})=\emptyset.
$$
For each `i=1,...,k`, define the genuine Boolean cofactor XOR:
$$
D_{h,k,i}(u,x_{-i})
=C_{h,k}(x_i=0,u)\oplus C_{h,k}(x_i=1,u).
$$
Writing `A_i=\bigvee_{j\ne i}x_j`, the identity
$$
(A_i\wedge f_h)\oplus f_h=f_h\wedge\neg A_i
$$
holds pointwise under **all** assignments. It yields the explicit signed CNF
$$
\boxed{D_{h,k,i}\equiv P_h\wedge\bigwedge_{j\ne i}(\neg x_j).}
$$

**PROVED/EXACT derived theorem (ordinary Resolution only):** For constants `c,h_0` inherited from Haken, every `h≥h_0`, every `k≥1`, every `i≤k`, and every ordinary source-authenticated shared-DAG Resolution refutation `π` of this explicitly listed `D_{h,k,i}` has `|π|≥2^(c h)` up to the harmless source/derived convention. Proof: restrict each `x_j=0` for `j≠i`. Every extra negative unit becomes TRUE, while every original PHP clause survives unchanged. Resolution is closed under variable restrictions; restriction of a DAG derivation, with TRUE lines removed and trivial/identical derivations suppressed, is a Resolution refutation of `P_h` no longer than the original. Apply Haken. This holds for arbitrarily many unrelated units. The encoded miter length is `Theta((h^3+k)log(h+k))`; for `k=h+1`, the lower bound is `2^(Omega((N/log N)^(1/3)))`. No claim is made for all proof grammars.

**PROVED/EXACT SAT sibling:** Delete the single collision clause `(¬p_{1,1}∨¬p_{2,1})` from `P_h`, obtaining `P_h^-`. Put pigeons 1 and 2 in hole 1 and pigeon `i≥3` in hole `i-1`. This satisfies the entire `P_h^-`. For the modified `C^-_{h,k}=f_h^-(u)∧OR_j x_j`, choosing every `x_{j≠i}=0` makes cofactors `0` and `1` under the exhibited pigeon assignment. Therefore **every** x_i becomes essential, and the corresponding explicit miter `P_h^- ∧_{j≠i} ¬x_j` is SAT.

**KNOWN countercontrol:** ER can ignore the extra negative units and apply Cook's polynomial PHP refutation. Source-only Resolution miter proof hardness can coexist with an identical semantic constant-zero function, an efficient recognizer of PHP, and short ER/mixed admissible proof. This disproves F1 and F2 and confirms F3; F4 is explicitly FALSE as a transfer. The theorem gives a model-specific *proof-format obstruction*, not a representation-invariant physical computational lower bound. The initial hope that essential-support certification alone might supply a B3 invariant is therefore rejected.

## COMPUTATIONAL controls and physical-resource ledger

A standalone dependency-free Python producer exhaustively enumerated all Boolean assignments to the PHP variables for h=1,2,3; verified the exact miter identities for k=1 and k=h+1 and each pivot i, including all other-x configurations; checked the one-clause-deletion SAT witness and opposite cofactor labels; and tested a genuine two-paid-node strict Resolution proof of h=1 with corrupted pivots/conclusions/indices rejected. Signed self-delimiting header, Elias-gamma counts, and fixed-width signed variable IDs round-tripped every tested miter; malformed tags, truncations, trailing bits and empty payloads were rejected. **12 configurations, 680,201 producer assertions**, raw SHA256 `c9fb8b85e5445a94eff64060bf71d61314d480f8495186a6539505d2d8fe9b7d`. An independently written JavaScript checker reconstructed PHP and all finite truth controls from scratch, accepted 12 original records, rejected 4 corrupted record variants and passed **429,031 assertions**. No claim of a finite minimum for h≥2; the h=1 proof is an upper-bound witness, not a new certified optimum.

Logical Resolution node count, full encoded evidence, output length, source reads, interpretation of source clauses, circuit building, gate evaluation, proof construction, proof checking, affine elimination, caching, failed policy attempts, and all simultaneously live writable storage are **separate resource measures**. The explicit miter is polynomial size and can be written in polynomial time/space. The *existence* of a short ER refutation does not automatically bound proof search; an efficient **uniform** PHP recognizer with exhaustive fallback is fast on this family but potentially exponential globally. If a solver materializes an exponential alternative, its input/output, verification work and all-phase space remain fully charged; compact alternatives must remain legal. In FLMV transport use `s'≤max{rho,eta,lambda,lambda*s}` with rho covering every preprocessing/allocate-then-free stage.

## Bridging obligations and next direction

For unchanged preselected `R_mix341`, `W_R(F)` minimizes unit-weight **paid** inference DAG nodes and `Wbar_R(N)` is the maximum over valid UNSAT original sources of encoded length at most N. B1 is per-decider pointwise proof domination, B2 is per-decider *all-binary-input* worst-case domination, and B3 is `SAT∈P => Wbar_R(N)=N^O(1)` for the **same** preselected system. The present theorem does not prove or refute these obligations for R_mix341. Even for Resolution, it refutes only naive pointwise trace-to-proof inferences, not the global worst-case B2 or the conditional B3.

**Next decisive obligation:** classify what additional *source-authenticated logical evidence* lets one produce a short proof of cofactor independence, rather than merely a correct SAT-algorithm output. Audit LOCAL-CONVERT port export/original-support semantics, then attempt a typed polynomial compiler or exhibit a genuinely legal native counterexample. Do not infer all-algorithm hardness from any Haken theorem.

### References and URLs

1. A. Haken, *The Intractability of Resolution*, Theor. Comput. Sci. 39 (1985), 297-308. DOI 10.1016/0304-3975(85)90144-6.
2. S. A. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28-32. DOI 10.1145/1008335.1008338.
3. S. A. Cook and R. A. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, J. Symb. Logic 44 (1979), 36-50. https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA
4. A. Atserias and M. Mueller, *Automating Resolution Is NP-Hard*, J. ACM 67(5) (2020). https://doi.org/10.1145/3409472 (proof finding is separate from proof lower bound).
5. N. Fleming et al., *Provable Reductions in TFNP*, ECCC TR26-109, 2026. https://eccc.weizmann.ac.il/report/2026/109/ (implicit proof certification, not a B3 transfer).
6. T. Sonobe, *An Experimental Survey of Extended Resolution Effects for SAT Solvers on the Pigeonhole Principle*, Algorithms 15(12):479 (2022). https://www.mdpi.com/1999-4893/15/12/479

**Publication:** report `research/agents/lspv-1/2026-11-04_1500_LSPV-1_PHP_COFAC_MITER_HARDNESS_FIREWALL401.md`; producer `experiments/arc/lspv1_401_php_miter_producer.py`; independent checker `experiments/arc/lspv1_401_php_miter_independent_verify.js`; raw `results/raw/arc/2026-11-04_1500_LSPV1_PHP_COFAC_MITER401_raw.json`; handoff `research/coordination/2026-11-04_1500_LSPV1_PHP_COFAC_MITER401_FIVE_ROLE_HANDOFF.md`. No task state, schedule, rule, or weight changed. Root main.tex reconciliation only if full blob bytes can be safely retrieved and preserved, otherwise leave documented fallback.

**P versus NP remains OPEN.**
