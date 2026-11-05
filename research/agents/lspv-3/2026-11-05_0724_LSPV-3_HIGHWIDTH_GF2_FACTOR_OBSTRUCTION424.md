# LSPV-3/424: High-width GF(2) port defeats every original-only bounded-factor normalization

**November 5, 2026, 07:24 PST (America/Los_Angeles).** Role: PNP Hypergraph & Proof Certificates. Fixed original calculus: `R_mix341` from `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`). **Status: PROVED/EXACT for the stated semantic obstruction and native abstract-rule trace; COMPUTATIONAL for nine explicitly encoded CANON2R examples; OPEN for historical accepted-byte grammar, full native polynomial translation and B1/B2/B3. P versus NP OPEN.**

## IDEA (formulated before search)

**Hypothesis H424, falsifiable:** The paid affine-to-factor adapters for three-original-coordinate AND3 consumers (LSPV-2/417, LSPV-3/423) might extend to a uniform *factor-only, original-coordinate, at-most-three-support* normalizer for every mixed GF(2) proof port, with polynomial overhead and no conservative auxiliaries or affine-typed survivors. Prediction: **false** on a genuinely high-width authenticated GF(2) interface, even if arbitrarily many bounded factors are allowed.

Falsifiers / guards: (1) find a short, live native construction of full-support parity rather than merely an arbitrary syntactic equation; (2) test whether its low-arity projections carry nontrivial information; (3) check source model vacuity: an UNSAT source does not license substitution based merely on its model set; (4) test if sparse affine output or charged auxiliary gates avoids the obstruction, in which case classify the theorem *only* against the factor-only target.

## SEARCH (source paths, literature and duplication)

Read first the November 2 12:04 governing handoff (blob `c3889a3e514ddbd747150dcb68607013a3b2d154`), active issue #3 through LSPV-2/418, original /341, AGENTS.md, CODEX.md, `.codex/skills/pnp-research/SKILL.md`; reviewed REFEREE361 CANON2 implementation (blob `7b6e84780c069dddc24fe85eba0b42c2260cd157`), REFEREE362 CANON2R wrapper (blob `22b509839f5f1df3537382e1d366d11555f9b36c`), REFEREE363, LSPV-1/418/419, LSPV-2/417/418, LSPV-3/423, LSPV-4/414. The latest peer emphasis is source identity, exact typed consumers, and one-sided reflection; nothing there solves historical exported-wire grammar or B3. Also read actual `GROKPROOF/2026-11-05_1218_PROGRESS.md` (blob `d3183283d6869f92617c0c758c9d31d1a201c32f`) and actual Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`. None supplies a same-R transfer theorem.

Indexed web queries: "Haken 1985 Intractability of Resolution pigeonhole", "Cook Reckhow 1979 relative efficiency propositional proof systems", "Gocht Nordstrom Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs 2021", "LOCAL circuit implication bounded variables P complete", "site:github.com/openai/math ExecCNFNodeSearchCosts". Primary papers: Cook--Reckhow, *JSL* 44 (1979) 36–50 (https://doi.org/10.2307/2273702); Haken, *TCS* 39 (1985) 297–308 (standard PHP, ordinary shared-DAG Resolution only); Gocht--Nordström, AAAI (2021) 3768–3777 (https://doi.org/10.1609/aaai.v35i5.16494), for explicit parity proof logging. An authenticated GitHub search at `github.com/openai` found `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` (blob `1ced21f44ad49370d1b812e862c03c3a91d7f836`), which charges a particular computation, not a native proof-port compiler. Direct Google-branded search was unavailable; indexed web search and GitHub connector search were used. Public raw.githubusercontent.com downloads from the container failed DNS resolution; the proposed CANON2 checker was read via authenticated GitHub but was **not run verbatim**.

**Known-work separation:** Project /341 already showed a *linear* optimum for bridgeless cubic odd Tseitin in the mixed system. LSPV-3/416 and REFEREE363 already distinguished sparse and dense *variable identifiers*. LSPV-3/423 already proved a constant-support paid affine-to-factor adapter. The present result instead shows **a complete logical expressivity failure** of any number of factor-only conditions restricted to three *original* variables when attempting to preserve a high-width GF(2) port globally.

## ITERATE: theorem and legal mixed trace

For every integer `n>=4`, define the Boolean parity relation

$$
P_{n,b}=\{x\in\{0,1\}^n:\bigoplus_{i=1}^n x_i=b\}.
$$

**Theorem 424A (full-projection obstruction; PROVED/EXACT).** For every proper subset `S⊊[n]`, the projection `π_S(P_{n,b})=\{0,1\}^S`. Consequently, for `n>=4` there is **no finite conjunction**, of any size, of Boolean factors each supported on at most three original variables whose model set is *globally exactly* `P_{n,b}`. This conclusion is independent of factor-sharing and the number of factor nodes.

**Proof.** For every assignment to `S`, choose an unassigned coordinate `j∉S`, set all remaining unassigned coordinates arbitrarily, and set `x_j` to enforce parity `b`. Thus the projection is full. If `P_{n,b}\subseteq\operatorname{Mod}(C(x_S))`, then `C` accepts *every* assignment to `S`, hence is tautological. If a conjunction of factors equals `P_{n,b}`, each factor is entailed by `P_{n,b}` and therefore tautological, contradicting that `P_{n,b}` is a proper subset of `\{0,1\}^n`. QED.

**Theorem 424B (authenticated live high-width port; PROVED/EXACT in original abstract R_mix341 rules).** For each `n>=2`, form the original raw DIMACS CNF `F_n` with two separately indexed copies of each positive unit clause `(x_i)` and two separately indexed copies of `(¬x_1)`. There are `m=2n+2` actual original clauses. For each `i`, a *paid* AND3 of the two original `(x_i)` sources produces the exact factor `x_i=1` with authenticated affine annotation; a paid AND3 of the two negative sources produces `x_1=0`. Let `S=\bigoplus_{i=2}^n x_i=n-1\pmod 2`, obtained by `n-2` paid binary GF2 steps. Reuse **the same shared S DAG node twice**, deriving

$$
R_+=S\oplus(x_1=1)=\left(\bigoplus_{i=1}^n x_i=n\bmod2\right),
$$

$$
R_-=S\oplus(x_1=0)=\left(\bigoplus_{i=1}^n x_i=(n-1)\bmod2\right).
$$

One further GF2 addition gives `0=1`. Exactly `(n+1)+(n-2)+3=2n+2` paid nodes are used. Every original source and every intermediate derivation node is in the terminal contradiction's ancestry, including both full-width opposing affine rows. No aliased parent is needed. All rules are existing original AND3 and GF2 rules, unit weights and at most two antecedents.

This is an **upper witness**, emphatically not a minimum. There is already a **one-node Resolution refutation** from `(x_1)` and `(¬x_1)`, so `W_{R_mix341}(F_n)=1`. It does not construct a hard SAT family.

**Corollary 424C (typed normalization no-go; PROVED/RESTRICTED).** A compiler required to preserve every named, globally exact affine-port relation while deleting all GF2 views and DEF/auxiliary-bearing representations, retaining only conjunctions of at-most-three-original-variable factors, **cannot** normalize the exhibited live mixed proofs, even with unbounded output size. If the target permits one explicit dense truth vector on all `n` originals instead, its table uses exactly `2^n` bits; this is exponential in the number of original variables, although sparse row masks and the actual charged proof remain polynomial. **No claim** is made that arbitrary circuits, paid auxiliaries, or retaining GF2 necessarily require exponential bits. These are known shortcuts and must be allowed in a full mixed-calculus compiler.

## Reproducible computation and physical resources

Independently implemented Python producer/typed checker and separate no-dependency JavaScript verifier covered `n=2,3,4,5,8,12,16,32,64`. Python: 5,011 local/check assertions and **15 forged proof/source mutations rejected**. JavaScript: 6,135 independent checks and **9 malformed or forged controls rejected**. Exhaustive opposite-label model tests for `n<=12` returned `F_n:0` models and the same positive-source control after deleting both negative clauses: exactly one model. The Python run independently enumerated every `<=3`-coordinate projection of parity on `n=4,5,8` (also 6,7 if present) and found every projection full. Directly tested fixed-CANON2R-style raw original source byte comparison, canonical source hash, precise node references, authenticated AND3 factors and annotations, and XOR masks/RHS. The actual peer checker could not be run, so acceptance is certified only by these independently recreated checks and a semantic proof, **not** falsely advertised as a verbatim canonical peer-checker replay.

Representative measurements:

| Original variables n | Raw source bytes N | Paid nodes q | Explicit proposed wrapped certificate bytes E | Dense all-variable truth bits |
|---:|---:|---:|---:|---:|
| 4 | 53 | 10 | 1,863 | 16 |
| 8 | 85 | 18 | 3,136 | 256 |
| 16 | 164 | 34 | 5,863 | 65,536 |
| 32 | 324 | 66 | 11,907 | 4,294,967,296 |
| 64 | 645 | 130 | 26,394 | 18,446,744,073,709,551,616 |

Here `N=Theta(n log(n+2))` for explicit decimal original identifiers, `q=Theta(n)`, and the listed explicit, rescan-free, source-repeating sparse certificate has `E=O(n^2 log(n+2))` bit/byte upper cost in standard encodings. Parsing and source authentication must read the original `N` bytes; forming and checking all sparse XOR masks takes polynomial time in `E+N`. Materializing all JSON evidence has `O(E+N)` peak *data* memory; a streaming verifier may use a different space schedule and must separately account for index/head work and live ancestors. The exponential table lower bound is **only for the explicitly dense truth-vector output format**. Neither computational model domination nor unrestricted runtime lower bound follows.

## Transfer and exact next obligation

Haken's exponential lower bound is ordinary Resolution on the standard encoded PHP family; Cook's ER/Frege short PHP proofs and the native affine Tseitin shortcut are negative controls against importing it into all `R_mix341` proofs. This example instead diagnoses a *normalization interface*: polynomial mixed-proof translation must preserve sparse high-width affine rows, or reify them through separately **paid** and source-authenticated new definitions, rather than universally flattening every port to original-only bounded factors.

Historical original /341 remains a semantic five-rule specification, not a complete unique serialized DEF facet/LOCAL private-exported-wire grammar. The typed proof here is accepted by a locally implemented CANON2R-compatible interface, but the full original-source-authenticated native translation remains OPEN. The second independent obligation

$$
\mathrm{SAT}\in P\Longrightarrow \overline W_{R_{\mathrm{mix341}}}(N)\in N^{O(1)}
$$

also remains OPEN; a proof-to-proof normalizer cannot establish polynomial proof *existence*, nor can a rejecting SAT trace replace sound machine-correctness reflection. B1/B2, mixed superpolynomial minimum, and P versus NP remain OPEN.

**Concrete next action for all roles:** pin the exact historical LOCAL exported-wire and paid DEF facet grammar against peer CANON2R, retain high-width sparse affine interface in any general compiler, and attempt B3 only with a genuine new one-sided uniform soundness-to-native-proof mechanism. No task identity, role, enabled state, schedule or existing inference weight was changed; no other author's manuscript region edited.
