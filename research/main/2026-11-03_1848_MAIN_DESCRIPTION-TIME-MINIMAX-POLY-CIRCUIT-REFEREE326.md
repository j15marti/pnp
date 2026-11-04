# Description-time minimax equals nonuniform circuit complexity — REFEREE326

**PNP Independent Proof Red Team, November 3, 2026, 18:48 PST.**  
**Status:** a concrete representation-inclusive minimax lemma is **PROVED**; it identifies the surviving invariant with `P/poly`, not with uniform `P`. The candidate is therefore not a new signed-hypergraph intrinsic invariant and does not prove B1, B2, B3, a superpolynomial `Rmix341` lower bound, or P versus NP. No task, schedule, enabled state, calculus rule, weight or ownership boundary was changed.

## 1. Exact obstruction and tested falsifiers

The obstruction is the quantifier order in a minimization over algorithms. Charging the solver/representation description blocks a free exponential truth table only partially: if the minimizer may change with the cutoff `N`, the remaining object is nonuniform advice/circuit complexity.

This run tested four claims without constructing a new hard family:

1. **Pointwise intrinsic claim:** minimizing description plus execution over all globally correct programs gives a hard source invariant. **False:** source-specific hardcoding plus a complete fallback gives linear cost.
2. **Cutoff minimax claim:** moving `min` outside the worst case and charging program length yields a polynomial measure exactly for uniform polynomial-time SAT. **False:** it yields `P/poly`.
3. **Representation-independence claim:** allowing GF(2), circuits, auxiliary variables, shared DAGs, lazy states and arbitrary adaptive solvers can still leave a nontrivial robust invariant. **True only as nonuniform circuit complexity, up to polynomial simulation between reasonable machines.**
4. **B3 repair claim:** polynomial boundedness of this minimax supplies the weakest sufficient `Rmix341` bridge. **False:** it means only SAT is in `P/poly`; no translation into `Rmix341` follows.

## 2. Published lower-bound anchor: exact scope

For `h` holes and `h+1` pigeons, `PHP_(h+1)^h` is the standard unary pigeonhole CNF with variables `x_(i,j)`, one clause `x_(i,1) OR ... OR x_(i,h)` for each pigeon, and collision clauses `NOT x_(i,j) OR NOT x_(k,j)` for distinct pigeons in one hole. It has `h(h+1)` variables and `(h+1)+h*binom(h+1,2)` clauses. Under an explicit signed indexed-literal/DIMACS-style binary encoding its length is `N_h=Theta(h^3 log h)`.

**Haken's theorem used as the anchor:** there are constants `c>0` and `h_0` such that, for every `h>=h_0`, every ordinary unrestricted shared-DAG Resolution refutation of the canonical `PHP_(h+1)^h` CNF has at least `2^(c h)` lines. Arbitrary legal Resolution pivots and DAG reuse are allowed. Extension variables, GF(2), circuits, Horn reasoning, semantic jumps and arbitrary SAT machines are not. Thus this is `2^(Omega((N_h/log N_h)^(1/3)))` restricted proof hardness, not an all-algorithm SAT runtime lower bound.

Haken explicitly contrasts ordinary Resolution with stronger systems; polynomial Extended Resolution proofs of PHP are known. REFEREE325's fixed recognizable-family decider is also mandatory here: even the Resolution-hard PHP family is polynomial-time decidable by one special-case recognizer with a complete fallback. None of this transfers Haken's lower bound to `Rmix341` or to the minimax invariant below.

Primary source: Armin Haken, *The Intractability of Resolution*, Theoretical Computer Science 39 (1985), DOI `10.1016/0304-3975(85)90144-6`.

## 3. Fixed model and total language

Fix:

- one reasonable deterministic universal machine `U` with a self-delimiting binary program encoding;
- one explicit binary encoding of CNF strings;
- the total language `L_SAT`, where valid satisfiable CNFs map to `1`, valid UNSAT CNFs map to `0`, and every malformed string maps to `0`;
- native time `T_U(p,x)` charging program acquisition and reads, source parsing, malformed-input rejection, representation construction, all bit access and updates, conversions, certificate validation, output and halting.

Only programs `p` for which `U(p,.)` is total and correct for `L_SAT` on **every** binary string are admissible. Define

`K_U(N) = min_p ( |p| + max_(|x|<=N) T_U(p,x) ).`

The minimum exists because the objective is a natural number and a fixed exhaustive parser plus brute-force SAT decider is admissible. Intermediate representations may be exponential; their actual construction and access are charged. Compact alternatives are equally admissible.

Peak writable space is separately recorded as `S_U(p,x)`. On the usual step-counted machines reachable writable space is at most polynomial in `|x|+|p|+T`; adding `max S` to the scalar does not change the polynomial-boundedness theorem below. It does not preserve fine FLMV exponents.

The decisive quantifiers are

`for every N, there exists p_N, for every x with |x|<=N`.

Every `p_N` is globally correct, but the program may vary with `N`.

## 4. Main theorem

### Theorem (description-time minimax / circuit equivalence)

For every fixed reasonable universal machine `U`,

`K_U(N) = N^O(1) for all N  iff  L_SAT is in P/poly.`

Quantitatively, if `C_L(n)` is the minimum Boolean-circuit size for length-`n` inputs, then under standard encodings

`C_L(n) <= poly(n + K_U(n))`,

and

`K_U(N) <= poly(N + sum_(n<=N) C_L(n)).`

### Proof: program to circuits

Assume `K_U(n)<=n^c`. Choose one globally correct witness `p_n` of description `s_n` and prefix time `t_n`, with `s_n+t_n<=n^c`. Hardwire `p_n` into a circuit that simulates `U(p_n,x)` on length-`n` inputs.

The standard Turing-machine-to-circuit construction gives size polynomial in `n+s_n+t_n`. For a fixed standard one-dimensional multitape model, Pippenger and Fischer obtain combinational-network cost `O(t_n log t_n)` after the appropriate oblivious simulation; the coarser polynomial bound is sufficient and robust here. The circuit explicitly contains the program bits and all local configuration transitions, so the inequality direction is

`machine description/time upper bound  =>  circuit-size upper bound`.

It must not be reversed to infer machine hardness from a restricted proof lower bound. Because `p_n` is correct on all strings, the hardwired circuit is correct on all `n`-bit strings, including malformed encodings. Hence `L_SAT` is in `P/poly`.

### Proof: circuits to globally correct programs

Assume `L_SAT` has circuits `C_n` of size `n^d`. For each cutoff `N`, form one program `p_N` containing encodings of `C_0,...,C_N`, a generic circuit evaluator and a fixed complete parser plus exhaustive SAT fallback.

On input `x`:

- if `|x|<=N`, select and evaluate `C_|x|`;
- otherwise run the fixed complete fallback.

The fallback makes `p_N` total and correct on every string rather than a finite-prefix promise solver. With an ordinary gate-list encoding,

`|p_N| = sum_(n<=N) O(|C_n| log |C_n|) = N^O(1).`

Parsing, selecting, loading and evaluating the active circuit, writing the answer and retaining the needed state take polynomial time and peak space on the prefix. Hence `K_U(N)=N^O(1)`.

This proves the equivalence. It also shows why global correctness does not restore uniformity: the expensive fallback is never used inside the optimized prefix, and a different globally correct `p_N` may be selected at every cutoff.

### Reasonable-machine robustness

If universal machines `U` and `V` admit polynomial program translation and simulation overhead, their `K` measures polynomially dominate one another. Polynomial boundedness is robust; exact values and exponents are not.

## 5. The invariant trilemma

The attempted all-representation signed-hypergraph/DAG invariant now has three precise outcomes.

### 5.1 Per-source minimization collapses

Define `J_U(F)=min_p(|p|+T_U(p,F))` over globally correct programs. Hardcode `F` and its correct label in `p_F`; compare the input with `F`, answer on equality, and invoke the fixed exhaustive fallback otherwise. Then `p_F` is globally correct and `J_U(F)=O(|F|)` under standard encodings. Therefore `max_(|F|<=N) J_U(F)` is polynomial. This is per-input hardcoding and is inadmissible as a lower-bound invariant even though each program is globally correct.

### 5.2 Cutoff minimax becomes `P/poly`

Moving `min` outside the prefix maximum blocks per-input selection, but still has `for every N there exists p_N`. Charging `|p_N|` prevents a free exponentially long table only when that table is actually long. Polynomial boundedness is exactly polynomial advice/circuits, not uniform `P`.

A superpolynomial lower bound for `K_U` would prove `SAT notin P/poly`, equivalently `NP not subseteq P/poly`. That is stronger than P versus NP and is open. It is a legitimate algorithm/representation-inclusive target, but not a weaker route to B3 and not an intrinsic hypergraph invariant.

### 5.3 Source-rooting returns to fixed-calculus cost

If every representation leaf and inference must carry a paid source-derived `Rmix341` macro, topological splicing yields an `Rmix341` refutation. Taking the infimum over all rooted packages then gives the native `W_Rmix341` (or a declared polynomially related variant). This restores source meaning only by returning to model-relative proof complexity. Arbitrary-decider transport remains B1/B2/B3.

No reviewed candidate is simultaneously:

- source-intrinsic;
- independent of every representation and algorithm;
- nontrivial against source-specific recognition;
- and weaker than nonuniform circuit lower bounds.

That is a proved diagnosis of these three definitions, not an impossibility theorem covering every conceivable invariant.

## 6. Relation to B1, B2 and B3

For fixed `Rmix341`, recall:

- **B1:** for every fixed total correct decider `A`, each UNSAT `F` has `W_R(F)<=p_A(|F|+T_A(F))`;
- **B2:** `Wbar_R(N)<=p_A(N+T_A^wc(N))` for every fixed `A`;
- **B3:** SAT in `P` implies `Wbar_R` polynomial.

The theorem proves none of them.

- `SAT in P` implies polynomial `K_U`, but the converse is only `SAT in P/poly`.
- B1 and B2 allow a polynomial depending on one fixed `A`; they do not allow substituting the varying sequence `p_N` and silently choosing one uniform polynomial.
- To minimize over programs before applying a bridge one would need the much stronger uniform-in-code statement

  `exists fixed polynomial q, for every p,N: Wbar_R(N) <= q(N+|p|+T_p^wc(N)).`

  This is not B2 as stated and is not proved for `Rmix341`. Combined with a superpolynomial `Wbar_R`, it would yield the stronger `SAT notin P/poly` conclusion.

The correct simulation direction remains `short computation => short R proof`. Restricted proof hardness has computational consequences only after that polynomial-overhead direction is established. An exponential backtranslation or the reverse inequality is insufficient.

## 7. Compact countercontrols and physical costs

- **PHP:** ordinary Resolution is exponentially hard, but a fixed canonical-family recognizer is polynomial on the whole family; Extended Resolution also has polynomial proofs.
- **Tseitin:** expander instances are hard for ordinary Resolution, while authenticated GF(2) addition gives the fixed mixed calculus a linear `4h-1` shortcut. LSPV-3/380's `Omega(h log h)` expanded-row mass is encoded by a pointer DAG in `O(h log h)` bits.
- **Lazy/implicit state:** large logical residual changes need not be physical writes. Reads, unchanged writes, motion and failed attempts may consume time with zero data-bit XOR change.
- **Exponential objects:** allowed, but their serialization, construction, access, checking, output and live storage are charged. Their existence does not force use when a compact representation exists.
- **Logical DAG nodes:** node count alone is not runtime. Payload length and a schedule are necessary.

The finite control records a one-bit offline XOR between correct and corrupted advice tables. No `d_phys` is claimed because the Python/JavaScript execution is not a declared fixed-tape native machine. This preserves the XOR adjunct as a diagnostic, not a free oracle or universal lower bound.

## 8. Independent five-role, Grok and Claude review

All five roles—the root red team plus LSPV-1 through LSPV-4—independently located and checked current Grok/Claude materials rather than relying on folder names.

- `GROKPROOF/2026-11-04_0116_PROGRESS.md`, blob `ca5a835356eb918b8cb4ab94d14de6174edeab03`: explicitly leaves the fully charged all-input ARC/FLMV transfer open and does not turn proof hardness into machine hardness.
- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`: useful hidden-selector/portfolio objection; the needed unconditional derandomization is not established.
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: restricted random-access/subpolynomial-space alternation-trading theorem, not B3.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: restricted sequential/crossing-sequence theorem, not B3.

Relevant current peer artifacts were also checked:

- `research/coordination/2026-11-03_1800_LSPV1_ROOT_EXTENSIONAL_SEMANTIC_QUOTIENT376_FIVE_ROLE_HANDOFF.md`, blob `05f10deae5d456c3975c679cb46f953a405e6956`: root-private truth-table quotient is proof existence; payload checking and full mixed grammar remain open.
- `research/coordination/2026-11-03_1807_LSPV2_NATIVE_SIGNED_XOR376_FIVE_ROLE_HANDOFF.md`, blob `4e87561da303906c0608ef1e9ce27e0269abac26`: exact three-AND XOR gadget is a strict-fragment result and compact shortcut, not a global lower bound.
- `research/coordination/2026-11-03_1820_LSPV3_CENTROID_XOR_ROW_MASS380_FIVE_ROLE_HANDOFF.md`, blob `8d7db5c01e7b8b3acc163aebd4edf2c6575d3eb7`: aggregate expanded row mass is representation-dependent; pointer encoding is polynomial.
- `research/agents/lspv-4/2026-11-03_1636_LSPV-4_SHARED_XOR_PATH_MULTIPLICITY372.tex`, blob `43f2d2ed2179ce8dc00c519f2f7ee4193b054d80`: exponential path multiplicity coexists with a polynomial shared-DAG validation.
- `research/main/2026-11-03_1748_MAIN_RECOGNIZABLE-ISLAND-CERTIFICATE-ROOTING-REFEREE325.md`, blob `96fef8265f70e440bcc6ce87aeed9640791cdfad`: recognizable-island shortcuts falsify broad source-unrooted envelopes.

These assessments are corroborating evidence, not authority. None supplies B3.

## 9. Literature and repository searches

Web/primary-source queries:

- `Pippenger Fischer Relations among complexity measures 1979 PDF circuit simulation Turing machine`;
- `Karp Lipton some connections between nonuniform and uniform complexity classes PDF 1980`.

Findings:

- Nicholas Pippenger and Michael J. Fischer, *Relations Among Complexity Measures*, JACM 26(2):361-381 (1979), gives the relevant machine-to-combinational-network simulation, including `O(t log t)` cost in its stated model: <https://scholarship.claremont.edu/hmc_fac_pub/597/> and <https://research.ibm.com/publications/relations-among-complexity-measures>.
- Richard Karp and Richard Lipton, *Some Connections Between Nonuniform and Uniform Complexity Classes*, STOC 1980, DOI `10.1145/800141.804678`, is the primary nonuniform-complexity reference: <https://dblp.org/rec/conf/stoc/KarpL80.html>.

Separate GitHub searches:

- `P/poly description time minimax SAT` in `j15marti/pnp`: no direct match; the peer artifacts above were found through issue #3/current handoffs.
- `Turing machine circuit simulation P/poly` under `github.com/openai`: no match returned.

A failed search is not a novelty claim. Current issue #3 was read through the latest LSPV-1/376, LSPV-2/376, LSPV-3/380 and LSPV-4/373 updates before this proof was finalized.

## 10. Finite controls and reproducibility

The producer and an independently written JavaScript verifier use the complete tiny universe formed by nonempty subsets of the eight complete 3-variable blocking clauses. Exactly 254 of 255 records are SAT; the all-eight record is UNSAT. They check:

- a hardwired cutoff table plus fixed fallback is globally correct on the tiny total language;
- ten malformed controls are rejected;
- one corrupted UNSAT advice bit is detected;
- description bits remain charged even when abstract lookup is short;
- K4 Tseitin has zero models for odd total charge and eight for even zero charge;
- B1/B2/B3 and P versus NP are recorded OPEN.

Producer: 281 assertions. Independent verifier: 277 assertions.

SHA-256:

- producer `cb584c5dc419df86bea2e8c88a68e590fe8904999307249e7f310a1011adaae1`;
- verifier `76bde9877ef1f29079d960cb39e739e6a30583bc9b94b8e5a4cd4c83ec5866c7`;
- raw JSON `c10ab38944b0f8958cdf422ff71b5119c5803c222dc40919e737f4db3531ed51`.

These controls test the theorem's quantifier and malformed-input obligations. They do not regenerate or empirically support a published asymptotic lower bound.

## 11. Classification and next obligation

**PROVED:** per-source program minimization collapses; description-plus-prefix-time minimax is polynomial exactly for `P/poly`; the statement is robust up to polynomial simulation between reasonable machines; physical costs are included in time and peak space remains separate.

**RESTRICTED:** Haken concerns ordinary Resolution; the XOR and semantic-quotient peer results concern declared fragments; Grok/Claude results concern their stated machine models.

**FALSIFIED:** polynomial cutoff minimax does not characterize uniform `P` and does not supply B3; charged description alone does not create a source-hypergraph intrinsic invariant.

**OPEN:** `SAT notin P/poly`; a superpolynomial `Wbar_Rmix341`; polynomial source-rooted transport for every full mixed rule; B1/B2/B3; any unrestricted SAT time/space lower bound; P versus NP.

The weakest honest next transfer target remains model-relative: prove a polynomial source-rooted compiler for one additional precisely specified `Rmix341` rule class, with payload length and checker time charged. An all-algorithm invariant should not be advertised as easier unless it avoids the three outcomes above without silently assuming a nonuniform circuit lower bound.
