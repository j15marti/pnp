# LSPV-5 REFEREE367: exact Resolution equivalence of context-typed shared branching

**November 5, 2026, 10:48 PST. Route B primary.** **PROVED/EXACT** for the explicitly declared context-typed branch calculus below: its minimum paid inference count is exactly ordinary shared-DAG Resolution's minimum inference count. **KNOWN/RESTRICTED**: Urquhart/Ben-Sasson--Wigderson cubic-expander Tseitin lower bounds therefore transfer to this branch-only calculus. **COMPUTATIONAL**: an exact K4 Tseitin source, a 267-paid-node shared branching trace, and its independently checked 29-inference ordinary-Resolution normalization. **FAMILY FAILURE for full mixed hardness**: the same cubic odd-Tseitin sources have the previously authenticated linear `R_mix341` AND3/GF(2) shortcut. Historical native grammar, a global mixed normalizer, superpolynomial full-mixed $\overline W$, B1/B2/B3, and P versus NP remain **OPEN**. No historical rule or weight is changed.

## IDEA stated before SEARCH

**Hypothesis.** The REFEREE366 EF firewall can be sharpened: exact context-scoped assumptions, Resolution and complementary branch discharge do not buy even a shorter proof than ordinary DAG Resolution. Compile every judgement $\Gamma\vdash C$ to its guarded clause $\neg\Gamma\vee C$, then eliminate every weakening and tautological assumption line by retaining a non-tautological subclause. If the elimination preserves DAG sharing, arbitrary nested and reconvergent branching is exactly Resolution-equivalent under unit paid-inference weights.

**Falsifiers fixed in advance.** (F1) a tautological guarded assumption is used to derive an unavailable non-tautological clause; (F2) a node is reused under an incomparable or weaker context; (F3) a merge omits one AND-obligatory branch or does not discharge exact complementary contexts; (F4) normalization unfolds a shared DAG exponentially. Prediction: each guarded line is mapped once either to no line (tautology) or to an ordinary-Resolution-derived subclause; a non-tautological final empty clause cannot disappear.

## SEARCH: governing record, current peers, external reviews, literature and repositories

Read the governing handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3, original `/341`, REFEREE366, and current peer artifacts. LSPV-3/427, `research/agents/lspv-3/2026-11-05_1030_LSPV3_NATIVE_RES_BRANCH_LIFT427.md`, blob `51be409881b9f2a1a8dd6c667a485b3c4eb91915`, proves the complementary two-restriction source lift and reuses only unconditional clauses. Its K4/K3,3/cube controls use 31/79/135 native RES nodes and reject seven corruptions. This run credits that local result and extends the proof obligation to arbitrary nested context DAGs with reconvergence.

Actual external assessments read: `GROKPROOF/2026-11-05_1428_PROGRESS.md`, blob `a0e35e77f5d35edb41cef00daf72e36d1536ae44`, which remains Route-A-specific and supplies no branch/Rmix/B3 compiler; and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`, whose central warning is that an open lemma implying the desired separation cannot be used as a bridge.

Primary queries actually run included `Ben-Sasson Wigderson Short Proofs are Narrow Resolution Tseitin expander PDF ECCC`, `Urquhart Hard examples for resolution 1987 Tseitin expanders DOI`, `Res XOR proof system Tseitin contradictions resolution over linear equations paper`, and `site:github.com/openai SAT resolution proof checker weakening branch assumptions`. Direct Google-branded search was unavailable; indexed web and authenticated GitHub were used, and no Google access is claimed.

Primary sources read, not only snippets:

- Ben-Sasson--Wigderson, ECCC TR99-022, define Resolution with Resolution plus weakening, explicitly note weakening is inessential, define shared DAG proofs, give restriction-lifting lemmas, and derive exponential ordinary-Resolution size for Tseitin contradictions on suitable 3-regular expanders. Their exact degree-three encoding has at most $h2^{3-1}=4h$ clauses and $3h/2$ edge variables.
- Urquhart, JACM 34(1), DOI `10.1145/7531.8928`, proves exponential length lower bounds for ordinary Resolution refutations of expander/Tseitin clause sets while noting short standard-propositional-calculus proofs.
- Raz--Tzameret, ECCC TR07-078 / APAL 2008, show that stronger linear-equation systems have polynomial Tseitin proofs. The later `Res(\oplus)` literature likewise states that parity splits quickly solve explicit GF(2) systems but proves lower bounds only for stated restricted systems such as tree-like `Res(\oplus)`. These are shortcut and scope controls, not arbitrary-machine lower bounds.

Required repository change-aware review:

| Repository/path | Pinned head/blob | Useful result and exact limit |
|---|---|---|
| `konard/p-vs-np`, `proofs/complexity/README.md` | head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, blob `7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3` | A finite one-tape machine and explicit polynomial-bound model; expressly no equivalence to every conventional machine model and no Rmix/B3 theorem. |
| `blkph0x/p-vs-np-proof-research`, `resolution_width_lab/THEOREM.md` | head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, blob `b9030425c38b36ae6f80306f663f07a0e541f333` | Exact bounded-width closure with weakening and Resolution, carefully scoped to Resolution. Its finite PHP results and cap warnings do not supply a mixed-system transfer. |
| `meelgroup/frat-xor`, `format.md` | head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, blob `986a21aa92b62f844ef1fce852193142c41b2b1f` | Distinct CNF/XOR IDs and explicit premises are useful provenance precedent; it is not historical `/341`, and the current checker scope is explicitly limited. |
| `peitl/short-proof` | head `2c524cfceecf68b56f51d23f6b63255b502856d3` | Minimum/short Resolution tooling only; no mixed-normalization or B3 theorem. |
| `openai/math`, `lean/OAI/Algorithms/SubexponentialSAT/SAT.lean` | head `4eaee87548250b2682affda7d05d947c05554bae`, blob `14dcfd0c910a08b005354da1fa66fbdac3ae7192` | Formal finite CNF semantics, tautology removal and absorption/normalization. It contains no historical Rmix grammar, proof compiler or B3 implication. |

An initially malformed parenthesized GitHub code-search query returned HTTP 422 and was not counted as a search result; corrected single-term searches found the scoped artifacts above. Repository titles, successful builds and formal syntax are evidence, not P-versus-NP theorems.

## Established family/theorem/encoding/method ledger

The primary family is not newly invented. Let $G=(V,E)$ be a connected cubic graph and $\chi:V\to\{0,1\}$ have odd total charge. There is one variable $x_e$ per edge. At vertex $v$, for every local edge assignment $a\in\{0,1\}^3$ with parity different from $\chi(v)$, include the width-three clause that excludes $a$:

$$
C_{v,a}=\bigvee_{e\ni v}\begin{cases}x_e,&a_e=0,\\ \neg x_e,&a_e=1.\end{cases}
$$

Thus $h=|V|$ gives exactly $3h/2$ variables and $4h$ width-three clauses; odd total charge makes the CNF UNSAT. With binary variable names, explicit DIMACS length is $N=\Theta(h\log h)$.

| Item | Exact status |
|---|---|
| Published theorem | For a suitable infinite family of cubic expanders, every ordinary unrestricted shared-DAG Resolution refutation has $2^{\Omega(h)}$ lines. The theorem quantifies over every Resolution proof of each family member; it is not an average solver observation. |
| Permitted rules | Source clauses, ordinary binary Resolution, and harmless weakening in the cited presentation; proofs are DAGs. Weakening is eliminable. No GF(2), extension variables, semantic oracle or branch-discharge primitive is included. |
| Known branch method | DPLL-style restrictions and both-case discharge; LSPV-3/427 gives a native source lift for one split. The theorem below handles arbitrary typed branch DAGs and proves they cannot beat Resolution. |
| Strongest mixed shortcut | Four clauses at each vertex authenticate one parity row using three paid AND3 nodes; adding $h$ rows uses $h-1$ GF(2) nodes. The existing fixed-mixed ledger therefore gives exact $4h-1$ paid nodes for connected simple bridgeless cubic odd Tseitin. |
| Remaining transfer | A lower bound for every legal mixture of historical RES, LOCAL-CONVERT, exported wires, AND3, GF(2) and paid DEF is absent. This family is a full-mixed family failure, not a candidate mixed lower bound. |

Haken's unary PHP theorem remains a mandatory ordinary-DAG-Resolution control, and Cook's polynomial Extended-Resolution PHP proofs remain the extension-variable shortcut. Standard PHP is not exact 3-CNF; this run makes no 3-CNF hardness claim from mere equisatisfiability. The Ben-Sasson--Wigderson row-extended PHP is exact 3-CNF but their displayed exponential statement is tree-like, so it is not substituted for the shared-DAG Tseitin theorem.

## Declared branch calculus and AND/OR semantics

A judgement is $\Gamma\vdash C$, where $\Gamma$ is a consistent finite set of signed literals and $C$ is a canonical non-tautological clause. Original sources are free references; every `ASSUME`, `RES` and `MERGE` is one paid unit.

1. `SRC`: from original source clause $C$, derive $\varnothing\vdash C$.
2. `ASSUME`: if $\ell\in\Gamma$, derive $\Gamma\vdash(\ell)$.
3. `RES`: from $\Gamma_1\vdash A\vee p$ and $\Gamma_2\vdash B\vee\neg p$, at a consumer context $\Delta\supseteq\Gamma_1\cup\Gamma_2$, derive the exact oriented resolvent $\Delta\vdash A\vee B$.
4. `MERGE`: from **both** $\Gamma\cup\{x\}\vdash C$ and $\Gamma\cup\{\neg x\}\vdash C$, derive $\Gamma\vdash C$.

The two `MERGE` premises form an AND obligation. Different legal derivations of the same needed judgement are OR alternatives: the minimum may choose one. A lemma may be cited under a stronger context, but not in an incomparable or weaker context. Distinct inference nodes are charged once regardless of fan-out. The dependency hypergraph is acyclic even if a search implementation revisits states.

This is a declared comparison calculus, not a silent addition to historical `R_mix341`, which has no authenticated `ASSUME` or `MERGE` serialization.

## Exact normalization theorem

Encode $\Gamma\vdash C$ by the guarded clause

$$J(\Gamma,C)=\neg\Gamma\vee C.$$

Compile each branch-DAG node once into Resolution-with-Weakening-and-Tautologies (`RWT`): `SRC` stays a source; `ASSUME` becomes its guarded tautology; each `RES` weakens its two guarded parents to the consumer guard and performs one exact Resolution; each `MERGE` resolves the two complementary guarded children on the split variable. A branch `RES` contributes at most two weakenings and one Resolution, while `MERGE` contributes one Resolution. Parent references preserve sharing.

**Lemma 1 (weakening/tautology elimination, PROVED/EXACT).** For every RWT line $D_i$, process lines in topological order and store either `None` when $D_i$ is tautological, or an ordinary-Resolution-derived non-tautological clause $D_i'\subseteq D_i$.

**Proof.** Sources map to themselves. A tautology maps to `None`. A weakening inherits its parent's subclause. For a Resolution line $R=(A\setminus\{p\})\cup(B\setminus\{\neg p\})$:

- if $R$ is tautological, map it to `None`;
- if both parent images contain the required opposite pivots, resolve them; the result is a subclause of $R$;
- if an image omits its pivot, inherit that image, which is already a subclause of $R$;
- if one parent image is `None` but $R$ is non-tautological, every complementary pair in that tautological parent must use the removed pivot. The other parent's image is therefore a subclause of $R$ and is inherited;
- both parent images cannot be `None` while $R$ is non-tautological: the surviving opposite pivot literals would make $R$ tautological.

The final guarded empty clause is non-tautological, and its only subclause is empty, so it maps to an ordinary Resolution contradiction. Every RWT node is processed once; no fan-out is unfolded. $\square$

**Theorem 2 (exact inference-minimum equality, PROVED/EXACT).** For every tautology-free UNSAT CNF $F$, with free source references and unit cost for each non-source inference,

$$
W_{\mathrm{Bctx}}(F)=W_{\mathrm{Resolution}}(F)
$$

Tautological source clauses can be deleted first without affecting satisfiability or either minimum: in the same strengthening induction they map to `None` and can contribute no non-tautological conclusion unavailable from the other parent. Thus the statement extends to ordinary CNF encodings after this paid-linear syntactic normalization, but the declared fixture/checker deliberately requires tautology-free source bytes.

**Proof.** The compiler plus Lemma 1 produces at most one ordinary Resolution inference for each branch `RES` or `MERGE`; `ASSUME` nodes disappear. Hence every Bctx proof of paid cost $q$ gives an ordinary proof with at most $q$ paid inferences, so $W_{\mathrm{Resolution}}(F)\le W_{\mathrm{Bctx}}(F)$. Conversely, an ordinary Resolution DAG embeds with empty contexts and exactly the same paid RES nodes, so $W_{\mathrm{Bctx}}(F)\le W_{\mathrm{Resolution}}(F)$. $\square$

The same compiler is polynomial in explicit evidence bits: the RWT stage has at most $S+A+3R+M$ lines for $S,A,R,M$ rule counts, guarded clauses have length bounded by the explicitly encoded context plus clause, and the elimination uses only parent/pivot/subset scans. Line equality is stronger than p-equivalence, but it applies only to this declared unit-weight branch system.

**Corollary 3 (restricted asymptotic transfer).** Urquhart/Ben-Sasson--Wigderson's $2^{\Omega(h)}$ ordinary Resolution lower bound applies unchanged, up to the free $4h$ source lines, to every valid shared Bctx branching proof of the cubic-expander Tseitin family. This covers optimal after-the-fact branch selection, arbitrary nested splits, reconvergence and shared unconditional lemmas. It proves no full-`R_mix341` or SAT-machine lower bound.

## Exact finite accepted traces and hostile controls

The producer generated the exact K4 instance (six edge variables, sixteen width-three clauses, one odd charge) rather than a bespoke family. Exhaustive evaluation found zero models; the same graph with even charge has eight models.

The Bctx fixture performs a full six-variable split. Twelve globally shared `ASSUME` nodes are cited under the appropriate full leaf contexts. At each of 64 leaves, one falsified source clause is resolved against three assumptions to obtain empty. Sixty-three exact complementary `MERGE` nodes discharge all branches. The trace has 283 total nodes: 16 free sources and 267 paid nodes (12 ASSUME, 192 RES, 63 MERGE). Its 22,093 canonical bytes / 176,744 evidence bits have SHA-256 `ba466719cc5b54c3ce3c5a913c73c079fdce5378679e41003a8394e1cb599a21`.

The direct guarded compilation has 539 lines: 16 sources, 12 tautologies, 256 weakenings and 255 Resolution lines, with 3,210 stored literal occurrences. Normalization yields an ordinary source-authenticated DAG with 45 total lines, 29 paid Resolution inferences and 142 stored literal occurrences. Its 2,923 bytes have SHA-256 `9967d704c5d23a1951e746fdc05ba52255e5d015c7190df2939bdce1a8ccb501`. This finite 29-step proof is not an asymptotic lower bound or a minimum claim; it is a compiler/reconvergence control.

The Python checker performed 16 source reads, 510 parent-reference reads, 384 context-subset tests and 1,674 typed literal scans. It rejected an omitted AND branch, cross-context leakage, opposite-label source replay, corrupt Resolution pivot and malformed DIMACS count. The independent Node implementation imported no Python checker code, reconstructed the K4 parity source, exhaustively confirmed UNSAT, replayed all typed and ordinary nodes, made 2,003 assertions, and again rejected omitted-branch and corrupt-pivot controls.

Artifacts:

- `experiments/arc/lspv5_367/branch_resolution_equivalence_referee367.py`
- `experiments/arc/lspv5_367/verify_branch_resolution_referee367.mjs`
- `experiments/arc/lspv5_367/k4_tseitin_typed_branch_referee367.json`
- `experiments/arc/lspv5_367/k4_tseitin_resolution_referee367.json`
- `results/raw/arc/2026-11-05_1048_LSPV5_REFEREE367_raw.json`
- `results/raw/arc/2026-11-05_1048_LSPV5_REFEREE367_independent.json`

No authoritative historical native checker was executed. These exact bytes are accepted only by the two declared independent REFEREE367 implementations.

## Work, span, evidence, time and space are different ledgers

| Ledger | Measured value / theorem |
|---|---|
| Distinct logical work | Bctx 267 paid nodes; ordinary normalization 29 paid inferences. Shared nodes count once. |
| Unit-inference critical path | 9 (three leaf resolutions followed by six merges), under an ideal parallel model with free source availability. This is not physical runtime. |
| Explicit evidence | 22,093 typed-trace bytes; 2,923 ordinary-proof bytes; RWT intermediate held 3,210 literal occurrences. |
| Construction/search | Producer enumerated 64 assignments, selected a falsified source at each leaf, built all records and performed all controls. This is charged in an implementation but deliberately absent from the logical minimum. |
| Verification/access | Exact source parsing, hash binding, parent/pivot/context reads, clause scans, parity enumeration and corrupt controls are recorded separately above. |
| Actual producer/check process | 9,821,746 ns and 13,308 KiB `ru_maxrss` in the published recorded Python run. These host measurements include interpreter overhead and prove no machine lower bound. |
| Retention versus recomputation | The measured run materialized all records. A DFS schedule could trade retained branch records for recomputation, but no exact optimum schedule is claimed. Serialized certificate output itself must still be written. |

Reference/application costs are not silently added to the declared logical weights; parent-reference reads are separately recorded. Minimum work, minimum span and minimum space need not be attained by the same proof or schedule.

## Consequences for full Rmix lower bounds and B3

1. **Branching does not evade a Resolution lower bound.** Exact typed assumptions, all-case discharge, reconvergence and sharing collapse back to ordinary Resolution. Any claimed branch-only Tseitin shortcut must contain an omitted branch, scope leak, non-Resolution inference or merely a different cost convention.
2. **The chosen established family fails against the full mixed calculus.** The legal AND3/GF(2) proof has $4h-1$ paid nodes. The exponential Resolution/Bctx theorem therefore cannot lower-bound $W_{R_{\mathrm{mix341}}}$ for these sources. A known shortcut is part of the true minimum and cannot be excluded.
3. **No B3 bridge.** Since Bctx has an unconditional superpolynomial worst-case Resolution lower bound, the statement `SAT in P => Bctx Wbar polynomial` would itself imply SAT is not in P. It is not obtained from branch syntax, trace checking or completeness. For full Rmix, both a superpolynomial mixed $\overline W$ and a noncircular same-system B3 remain absent.
4. **No historical grammar completion.** `ASSUME` and `MERGE` are comparison rules only. The theorem neither authenticates nor revises historical LOCAL-CONVERT, exported/private wires, AND3, GF(2), DEF facets or their weights. Combining a branch wrapper with those rules would require a new rule-by-rule simulation and could be strictly stronger.
5. **No arbitrary-machine hardness.** Exponential explicit backtranslation from a linear GF(2) proof to Resolution measures a weak output format. It is not SAT runtime, discovery cost or an all-representation invariant.

## Revised claim and precise remaining gap

The initial EF-only statement is revised upward: exact context-typed shared branching is **exactly** ordinary Resolution in minimum unit inference count, not merely EF-simulable. The evidence that changed the claim was Ben-Sasson--Wigderson's explicit weakening-inessential formulation plus LSPV-3/427's original-source branch lift; the nodewise strengthening invariant closes arbitrary nested reconvergence without exponential duplication.

The next Route-B obligation is outside this settled fragment: authenticate the exact historical `/341` consumer grammar, then either prove a lower-bound invariant surviving every legal RES/LOCAL-CONVERT/exported-wire/AND3/GF(2)/paid-DEF mixture or exhibit its legal shortcut. Independently, a B3 proof must convert `SAT in P` to polynomial $\overline W_{R_{\mathrm{mix341}}}$ without assuming correctness reflection, polynomial certificates or the desired separation. Nothing here supplies either arrow.

## References

- E. Ben-Sasson, A. Wigderson, *Short Proofs Are Narrow--Resolution Made Simple*, ECCC TR99-022; JACM 48(2), 2001, 149--169.
- A. Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987, 209--219, DOI `10.1145/7531.8928`.
- R. Raz, I. Tzameret, *Resolution over Linear Equations and Multilinear Proofs*, ECCC TR07-078; APAL 155, 2008.
- S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976.
- A. Haken, *The Intractability of Resolution*, TCS 39, 1985.

**Publication guard.** No task identity, title, timezone, schedule, enabled state, historical rule or weight was modified. No other role's manuscript region was edited. P versus NP remains **OPEN**.

