# Uniform-generator collapse to ordinary P — REFEREE327

**PNP Independent Proof Red Team, November 3, 2026, 19:48 PST.**  
**Status:** the uniform-generation repair of REFEREE326 is **PROVED/EXACT** and collapses to ordinary uniform polynomial time. The hoped-for new signed-hypergraph/DAG invariant is **FALSIFIED for this definition**. No B1, B2, B3, superpolynomial `Rmix341` lower bound, unrestricted SAT lower bound, or P-versus-NP separation is proved. No task, schedule, enabled state, calculus rule, weight, encoding or ownership boundary was changed.

## 1. Exact obstruction and falsifiers

REFEREE326 proved that cutoff-wise minimization of solver description plus prefix runtime is polynomial exactly when SAT is in `P/poly`. The remaining proposal was to repair its nonuniform quantifiers by requiring one uniform generator for the cutoff solvers.

This run tested four precise claims:

1. **Computable-generator repair:** one fixed computable generator, with generation time omitted, restores uniform `P`. **False:** for decidable languages it still characterizes the same `P/poly` existence when generated descriptions and online runtimes are polynomial.
2. **Polynomially charged generator repair:** one fixed generator with all generation/output and execution work polynomial creates a new intermediate invariant. **False:** it is exactly ordinary `P`.
3. **Lazy-generator escape:** a succinct or on-demand generator avoids the equivalence. **False when every generated-bit query, replay and recomputation is charged; the generator and evaluator compose into one polynomial-time decider.**
4. **B3 shortcut:** the repaired generator property implies polynomial `Wbar_Rmix341` by a new argument. **False:** because the property is equivalent to SAT in `P`, that implication is B3 itself restated.

No new hard family was generated.

## 2. Published lower-bound anchor: exact model and strength

For `h` holes and `h+1` pigeons, let `PHP_(h+1)^h` be the standard unary CNF with variables `x_(i,j)`, one width-`h` pigeon clause for each pigeon, and binary collision clauses for each pair of pigeons and hole. It has `h(h+1)` variables and `(h+1)+h*binom(h+1,2)` clauses. With explicit signed indexed literals, its binary/DIMACS-style length is `N_h=Theta(h^3 log h)`.

**Haken's theorem used here:** there are constants `c>0,h_0` such that for every `h>=h_0`, every ordinary unrestricted shared-DAG Resolution refutation of the canonical `PHP_(h+1)^h` source has at least `2^(c h)` lines. The quantifier covers all legal ordinary Resolution refutations, with arbitrary pivots and DAG sharing. It does not cover extension variables, Extended Resolution, GF(2), circuits, Horn reasoning, semantic rules, `Rmix341`, or arbitrary uniform SAT machines. Thus it is a superpolynomial lower bound in the explicit source length for one proof system, not unrestricted computational hardness.

Primary source: Armin Haken, *The Intractability of Resolution*, Theoretical Computer Science 39 (1985), DOI `10.1016/0304-3975(85)90144-6`.

The established Tseitin countercontrol is equally mandatory: appropriate expander Tseitin CNFs are exponentially hard for ordinary Resolution, while the same odd connected cubic sources have an authenticated `Rmix341` GF(2) proof of `4h-1` paid nodes. These lower bounds cannot be transported without a polynomial simulation in the correct direction.

## 3. Fixed uniform-generation model

Fix:

- one reasonable deterministic bit-cost universal machine `U`;
- a self-delimiting program encoding;
- the total binary language `L_SAT`, accepting valid satisfiable CNFs and rejecting valid UNSAT CNFs and malformed strings;
- one fixed total generator program `G`.

On unary input `1^N`, `G` explicitly emits a self-delimiting program `p_N`. Require every `p_N` to be total and correct for `L_SAT` on every binary string. Define

`C_G(N) = T_U(G,1^N) + |p_N| + max_(|x|<=N) T_U(p_N,x).`

The generator time charges:

- reading its unary horizon and its own code;
- any circuit/proof search or representation construction;
- every output bit and serialization step.

The solver time charges:

- code acquisition and parsing;
- source and index access;
- representation construction/conversion;
- every read, update, verification step, answer bit and halt.

Peak space is recorded separately. Exponential intermediates are allowed, but materializing or accessing them costs real work and space; compact alternatives remain admissible.

Unary `1^N` makes the scale explicit. Equivalently, a binary encoding of `N` may be used only if resource bounds are stated as polynomials in the numeric value `N`, not silently in `log N`.

## 4. Main theorem

### Theorem (charged uniform-generator equivalence)

For the total language `L_SAT`, the following are equivalent:

1. there exist one fixed generator `G` and a constant `k` such that for every `N`, `C_G(N)<=N^k`;
2. `L_SAT` is in `P`.

Global correctness of every `p_N` is stronger than needed in the forward direction; correctness on all strings of length at most `N` would suffice.

### Proof: generator to one fixed decider

Construct one machine `D_G`. On input `x` of length `n`:

1. construct/read `1^n`;
2. run the fixed `G` to produce `p_n`;
3. run `U(p_n,x)` and return its output.

Its time is bounded by

`O(n) + T_U(G,1^n) + |p_n| + T_U(p_n,x) + polynomial universal-simulation overhead,`

which is polynomial in `n`. Correctness follows from correctness of `p_n`. Hence `L_SAT` is in `P`.

### Proof: one fixed decider to generator

If a fixed polynomial-time program `p*` decides `L_SAT`, let `G` consume its unary input and emit the constant self-delimiting code of `p*` for every `N`. Generation/output is polynomial and the prefix runtime is polynomial. Therefore the generator property holds.

This proves the equivalence.

### Lazy and streaming variants

Suppose `G(N,i)` returns requested bits of a succinct program/representation on demand. If the evaluator makes polynomially many requests and every request/recomputation is polynomially charged, one fixed machine composes `G` with the evaluator and remains polynomial time. If the representation is materialized, its output length is already bounded by generator time. If it is not materialized, unqueried virtual bits do no work and queried bits are charged. Neither version evades the theorem.

## 5. Exact uniformity ladder

The recent results now give a complete four-level diagnosis for these definitions.

### Level 1: horizon solvers with descriptions omitted

`for every N there exists p_N` with code uncharged collapses for every decidable language. A complete labelled prefix trie answers in linear online time and uses a fixed complete fallback after the horizon, while its finite control may have `Theta(N 2^N)` bits. LSPV-1/377 supplies the explicit construction.

### Level 2: descriptions charged, solver may vary with N

REFEREE326 proved

`K_U(N)=min_p(|p|+T_p^wc(N))=N^O(1)  iff  L_SAT is in P/poly.`

The quantifier remains `for every N there exists p_N`.

### Level 2.5: one computable generator, generation time omitted

For a decidable language in `P/poly`, hardcode a fixed decider into a very slow generator. On length `n`, enumerate polynomial-size circuits and use the decider to calculate all `2^n` correct labels until a correct circuit is found; do this for every length through `N`, then package the circuits with a complete fallback. The generator is total and computable but need not be remotely polynomial. Conversely, generated polynomial descriptions and polynomial prefix runtimes give `P/poly` by the REFEREE326 machine-to-circuit direction. Thus computability alone does not restore uniform efficiency.

### Level 3: one polynomially charged generator

The theorem above gives exactly `P`.

### Level 4: source-rooted proof packages

If every representation leaf and inference carries a paid same-source `Rmix341` macro, topological splicing returns to native `W_Rmix341`. This is model-relative proof complexity, not all-algorithm computation.

Adding too little uniformity leaves advice. Adding enough uniformity returns to the original uniform SAT problem. Adding source-rooted semantics returns to the fixed calculus. None produces the desired intermediate signed-hypergraph invariant.

## 6. Independent representation counterexamples

The newest peer results strengthen the diagnosis.

### Uniform invertible recoding

LSPV-2/377 gives one fixed total polynomial-time, invertible, length-preserving transformation that swaps canonical unary `PHP_(h+1)^h` with a contradictory-unit CNF having the same explicit bit length, declared variable count and number of distinct proper source clauses, while fixing every other binary string. Ordinary Resolution cost changes from `2^(Omega(h))` to exactly one.

Therefore an invariant unchanged by every such uniform recoding and lower-bounding ordinary Resolution cost must be constant-small on the Haken-hard family. The construction costs `O(N^2)` bit time, `O(N)` materialized space and `Omega(N)` output; no hidden exponential conversion is used. Source authentication and conversion charging are the only available repair, and they are model-relative.

### Shared affine-DAG unfolding

LSPV-3/381 proves that an arbitrary authenticated shared GF(2) derivation DAG with `q` XOR gates, `m` sources, `L` sparse source occurrences and `d` variables is checked by reverse coefficient propagation in `O(q+m+L+d)` indexed operations and `O(q+m+d)` auxiliary bits. A 61-gate Fibonacci DAG has over `6.5e12` unfolded source occurrences yet is checked in linear encoded work and even has a shorter one-gate proof. Unfolded paths or expanded rows are not representation-independent machine work.

These are compact countercontrols, not transfers to assume.

## 7. Resource and FLMV accounting

For a materialized program, a conservative combined peak-space bound is

`S_D(n) <= O(n) + |p_n| + max(S_G(n), S_(p_n)(n)) + O(log C_G(n)).`

More finely, peak space is the maximum of the generation phase retaining its output and the simulation phase retaining `p_n`; streaming may trade storage for recomputation, which must be charged.

If generation time, emitted program length and solver time have exponents `a,d,b`, the generic composed time exponent is at most `max(1,a,d,b)` plus the declared simulation overhead. The analogous materialized space exponent includes `d`. This only preserves polynomiality. It does not prove the `rho<=1/2` all-phase space condition, construct power-short SAT children, or preserve the fine same-machine exponents needed for an FLMV contradiction.

Pippenger-Fischer circuitization likewise preserves polynomial size with its stated overhead; it does not make circuit generation, input access, evaluation or live space free.

## 8. B1/B2/B3 classification

The theorem proves none of B1, B2 or B3 for `Rmix341`.

- One fixed `G` merely induces one fixed correct algorithm `D_G`, with generator work included in its runtime.
- B1 and B2 still require a polynomial computation-to-`Rmix341` translation for each fixed solver in the correct direction.
- Because the generator property is equivalent to `SAT in P`, the statement

  `polynomial charged uniform generator => Wbar_Rmix341 is polynomial`

  is logically B3 itself. It does not prove B3.
- A superpolynomial lower bound against every charged uniform generator would directly prove `SAT notin P`, hence P versus NP. It is not an easier invariant target.

No rejecting trace proves the global correctness premise.

## 9. Five-role, Grok and Claude audit

All five roles independently located and assessed the current evidence.

- `research/coordination/2026-11-03_1900_LSPV1_FINITE_HORIZON_UNIFORMITY_FIREWALL377_FIVE_ROLE_HANDOFF.md`, blob `eb4819289ebfce23971cba740ef7da3a6d129f27`: explicit uncharged finite trie; correctly amended to credit REFEREE326.
- `research/coordination/2026-11-03_1909_LSPV2_LENGTH_PRESERVING_INVOLUTION377_FIVE_ROLE_HANDOFF.md`, blob `dd5d5dcc9f5fb400f5ca23c632ab46ffa873b8e5`: fixed uniform reversible representation counterexample in ordinary Resolution.
- `research/coordination/2026-11-03_1924_LSPV3_REVERSE_AFFINE_DAG381_FIVE_ROLE_HANDOFF.md`, blob `c576af3043a8c6bc14e095e8dc2955edbc36441d`: reverse affine shared-DAG checker and exponential-unfolding counterexample.
- `research/agents/lspv-4/2026-11-03_1836_LSPV-4_RANDOMIZED_SAT_LATE_INDEX374.md`, blob `133482a860c7f5c6fc8c946e59751cbf5f59d18e`: a restricted streaming INDEX/Fano bound defeated by paid reread/index access; no unrestricted bridge.

Current Grok:

- `GROKPROOF/2026-11-03_1912PST_PROGRESS.md`, blob `66576e888e5c147c64264d4856089b6d3e7903e3`: explicitly leaves the universal, fully charged, all-input ARC/FLMV transformation open.
- Prior `GROKPROOF/2026-11-04_0116_PROGRESS.md`, blob `ca5a835356eb918b8cb4ab94d14de6174edeab03`: same missing transfer, with Pippenger-Fischer cost warning.

Current Claude:

- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`: identifies the unproved uniform hitting-set/derandomization step and a portfolio-collapse control.
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: restricted alternation-trading portfolio model.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: sequential/crossing-sequence lower bounds, explicitly not the indexed ARC/FLMV model.

These reports supply useful objections but no B3 transport.

## 10. Literature and repository searches

Primary-source web queries:

- `primary source P-uniform circuit families polynomial time uniform circuits P equivalence`;
- `Borodin Cook P-uniform circuits polynomial time uniformity primary paper`;
- `uniform circuit complexity polynomial time direct connection theorem primary source`;
- `Pippenger Fischer relations among complexity measures uniform circuits Turing machine 1979`.

Findings:

- Nicholas Pippenger and Michael J. Fischer, *Relations Among Complexity Measures*, JACM 26(2):361-381 (1979), DOI `10.1145/322123.322138`, proves the relevant machine-to-network simulation in its stated model, including `O(T log T)` network cost.
- Walter L. Ruzzo, *On Uniform Circuit Complexity*, JCSS 22(3):365-383 (1981), DOI `10.1016/0022-0000(81)90038-6`, is a primary uniform-circuit reference and emphasizes definition/model matching.
- Eric Allender, *P-Uniform Circuit Complexity*, JACM 36(4):912-928 (1989), DOI `10.1145/76359.76370`, studies the P-uniform setting. The elementary theorem in this report is proved self-contained and is not claimed novel.

Separate GitHub searches:

- `uniform generator P/poly SAT program family` and `uniformity firewall generator B3` in `j15marti/pnp` found REFEREE324/326, the earlier advice hierarchy, and resource-audit warnings; these were used for de-duplication.
- `P-uniform circuit generator` under `github.com/openai` returned no match.

A failed search is not a novelty claim.

## 11. Finite controls and XOR adjunct

The producer and independent JavaScript verifier use the complete tiny universe of nonempty subsets of the eight complete three-variable blocking clauses. Exactly 254 of 255 records are SAT and the all-eight record is UNSAT. They check:

- six generated prefix programs with globally correct fallback;
- generation work, serialized table length and a 10,000-step delay with identical output;
- ten malformed controls;
- one corrupt UNSAT table entry rejected;
- odd/even K4 Tseitin model counts `0/8`;
- binary-order and Gray-order logical table construction.

Producer: 1,602 assertions. Independent verifier: 291 assertions.

The offline logical XOR ledger records:

- zero-to-correct endpoint delta `254`;
- binary and Gray adjacent label delta sums `254`;
- changed-then-restored adjacent sum `256` but endpoint delta `254`;
- delay-loop data delta zero despite 10,000 charged operations.

No native `d_phys` is claimed because address, head, code, control state and a fixed physical tape layout are not modeled.

SHA-256:

- producer `a3fc8a264a351fe9471e98405fb735305f03cc494dca728b045e5484a026d931`;
- verifier `80fe14baaeb95743377f7f9641c940200b0eded95a9a2e213b811888c6d20e9c`;
- raw JSON `bf6f83c734fa7702816b25a18db14d10dbfd49a3d112b5d7f403cc081a1338e0`.

These controls test quantifiers and charging only. They do not establish an asymptotic lower bound.

## 12. Classification and next obligation

**PROVED:** one fixed polynomially charged generator for globally correct horizon solvers exists exactly when the language is in `P`; lazy/on-demand generation does not escape when every access is charged; the four-level uniformity ladder above.

**FALSIFIED:** this repair does not yield a new source-intrinsic or easier algorithm-independent invariant; a merely computable generator does not restore uniform polynomial time.

**RESTRICTED:** Haken's ordinary-Resolution theorem; the uniform involution; reverse affine-DAG checking; LSPV-4's streaming memory bound; Grok/Claude model-specific results.

**OPEN:** full `Rmix341` superpolynomial `Wbar`; polynomial full-rule source-rooted transport; B1/B2/B3; any unrestricted SAT time/space lower bound; P versus NP.

The weakest honest next target remains a precisely typed, source-rooted polynomial compiler for one additional full-`Rmix341` rule family. Uniform-generation minimax is now exhausted: below polynomial generation it retains advice; at polynomial generation it is exactly the original SAT-in-P premise.
