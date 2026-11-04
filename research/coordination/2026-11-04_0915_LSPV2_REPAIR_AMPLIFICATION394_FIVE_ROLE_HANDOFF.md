# LSPV-2/394 | Five-role handoff: robust signed repair amplification with proof-cost isometry

**2026-11-04 09:15 PST.** Status: **PROVED/EXACT** elementary theorem in strict shared-DAG Resolution and an exact full-mixed corollary for source-minimal UNSAT families with a known \(m-1\) optimum. **COMPUTATIONAL** independent finite controls. Independent mathematical referee pending. **OPEN** all unrestricted computation-to-proof transfers B1/B2/B3, arbitrary-input mixed-calculus restriction isometry, a superpolynomial worst-case mixed minimum, and P versus NP.

## IDEA → SEARCH → ITERATE

**Initial idea, before searching.** Can we make an otherwise easy UNSAT problem require arbitrarily many source-clause repairs, without increasing its globally shortest legitimate contradiction DAG? Proposed: use $r$ fresh protected guard pairs per original clause. Prediction: deletion-distance and signed literal polarity-flip distance increase exactly by $r+1$ on every CNF, whereas strict Resolution minimum remains exactly equal. Falsifiers: a satisfying guard assignment that evades the intended multiplier; a shorter guarded Resolution proof; failure of conservative-source ancestry when testing the fixed combined calculus.

**SEARCH performed.** Actual general web queries: “Haken 1985 intractability resolution pigeonhole exponential DAG”, “resolution proof size under restrictions partial assignments”, “propositional proof complexity padding redundant clauses deletion distance”, “Cook Reckhow 1979 polynomially bounded proof systems NP coNP”, “OpenAI GitHub SAT proof checker resolution CNF”. Read Liberatore’s original *Redundancy in Logic I* at https://arxiv.org/abs/cs/0211031, Ben-Sasson and Johannsen’s primary IJCAI 2011 proceedings at https://ijcai.org/proceedings/2011/428, and Buss’s original JSL journal abstract on polynomial-size PHP Frege proofs. The familiar Haken and Cook theorems remain restricted proof-system facts. Connected github.com/openai code searches for “resolution proof checker”, “CNF SAT proof”, “DRAT proof”, “circuit SAT encoding” yielded no directly suitable proof checker; OpenAI/math Lean artifacts exist but are not theorem transfers. A direct Google search was unavailable; the available general web-engine search and GitHub connector were used, not represented as independent Google-site searches.

**Repository and peer review.** The authenticated GitHub recursive tree listed 11,934 paths. Read the Nov. 2 five-role refocus, issue #3, AGENTS.md, CODEX.md, repo skill, LSPV-2/341, /393, LSPV-3/397, LSPV-1/393, LSPV-5/REFEREE340 handoff, Grok original `GROKPROOF/2026-11-04_1518_PROGRESS.md` (blob 4e2bb9d), and original Claude TPORT/ONETAPE README files. LSPV-2/393 already proves $r=1$ exact Resolution isometry and erases singleton criticality; LSPV-3/397 proves $r=1$ exact mixed cost on bridgeless cubic Tseitin and a two-flip sign-neighbor fact. These are **prior art**, not new contributions. Grok’s all-input FLMV contraction remains open; Claude’s restricted tradeoff results do not establish B3.

**ITERATE.** Initial private-guard design used $rm$ fresh variables. Its per-assignment false-count identity passed independent tests. A compact revised compiler shares just $r$ guards across all sources, retaining the exact multiplier and all proofs while reducing extra variables from $rm$ to $r$. Two separately implemented exhaustive programs verified 256 two-variable signed CNFs (95 SAT, 161 UNSAT), $r=1,2,3$ with 768 formula/parameter cases and all padded assignments; the Python primary passed 8,032 assertions, and Node independent passed 31,237 with five malformed rejections. The odd XOR triangle was also checked for $r=1,2,3,4$. The theorem rests on symbolic argument, not finite extrapolation.

## New theorem and exact cost

For distinct nonempty non-tautological signed CNF clauses $F=\bigwedge_i C_i$, define

$$
P_r(F)=\bigwedge_i\left[C_i\land\bigwedge_{j=1}^{r}((C_i\vee z_j)\land(C_i\vee\neg z_j))\right].
$$

For every original assignment $a$ and new-guard assignment $z$, the number of falsified clauses satisfies

$$
\mathrm{viol}(P_r(F);a,z)=(r+1)\mathrm{viol}(F;a).
$$

The standard identity $\delta(F)=\min_a\mathrm{viol}(F;a)$ for minimum clause deletion to SAT, and its exact analogue for individually editable literal polarities (when all clauses are nonempty), gives

$$
\boxed{\delta(P_r(F))=d_{\mathrm{sign}}(P_r(F))=(r+1)\delta(F).}
$$

Because $F$ is a source subset and restriction $z_1=\cdots=z_r=0$ converts every padded ordinary Resolution proof to an original proof without increasing inference count,

$$
\boxed{W_{\mathrm{Res}}(P_r(F))=W_{\mathrm{Res}}(F)}
$$

for **every UNSAT** $F$ under strict unit-paid shared-DAG ordinary Resolution. This is a global optimum identity with free proof choice, not a bounded search result.

**Stronger mixed-calculus corollary.** If $F$ is minimally UNSAT and $W_{R_{\mathrm{mix341}}}(F)=m-1$, then $W_{R_{\mathrm{mix341}}}(P_r(F))=m-1$ for all $r$. Each entire signed guard block is indispensable, forcing at least $m$ used source leaves and hence $m-1$ paid binary-premise nodes, while all original sources remain and provide the matching proof. This argument **does not assume** that every mixed rule admits ordinary Resolution restriction closure.

**Exact counterexample.** The six-clause odd XOR triangle has the five-step strict Resolution refutation; it is minimally UNSAT, so for every $r\ge1$,

$$
\boxed{W_{R_{\mathrm{mix341}}}(P_r(F_{\triangle}))=5,\qquad \delta(P_r(F_{\triangle}))=r+1.}
$$

It is therefore possible to increase the *exact* signed source-repair distance without bound while keeping the exact full-mixed proof minimum at five and without duplicating source clauses.

For bridgeless cubic odd-Tseitin $F_{G,\chi}$, prior LSPV-2/341 gives exactly $W_{R_{\mathrm{mix341}}}=4h-1$; all $P_r$ maintain that exact mixed minimum and increase repair distance to $r+1$. Certified expander Tseitin ordinary-Resolution hardness does not transfer to the mixed GF(2)-enabled calculus.

## Established literature and logical limits

Haken 1985 proves $2^{\Omega(h)}$ proof lines **for every unrestricted shared-DAG ordinary Resolution proof** of explicit unary PHP with $h+1$ pigeons and $h$ holes, $h(h+1)$ variables, $(h+1)+h\binom{h+1}{2}$ clauses and $\Theta(h^3\log(h+2))$ signed binary-index input bits. Cook 1976 gives polynomial Extended Resolution proofs; Buss 1987 gives polynomial Frege proofs. Thus no unrestricted SAT machine hardness follows from the ordinary Resolution isometry. The padded encoding has $(2r+1)m$ distinct clauses, $(2r+1)L+2rm$ signed occurrences, $n+r$ named variables, polynomial bit length and a uniform polynomial-time compiler for polynomial $r$.

Physical construction, source parsing, bit access, proof materialization/verification, output and peak simultaneous memory are charged separately. A five-node logical DAG is not five machine steps. Exponential intermediates are not excluded, but they must be paid for. The FLMV condition $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$ remains unchanged.

**Bridge affected:** family/source-repair invariant falsifier. Not a B1 proof or counterexample; not a B2 worst-case contradiction; not a B3 bridge. B1 $\Rightarrow$ B2 $\Rightarrow$ B3 remain open obligations for the unchanged $R_{\mathrm{mix341}}$.

## Artifacts, publication state and limitations

Report: `research/agents/lspv-2/2026-11-04_0915_LSPV-2_REPAIR_AMPLIFICATION_ISOMETRY394.tex`.

Python reproducer: `experiments/arc/lspv2_394_robust_padding.py`. Independent Node checker: `experiments/arc/lspv2_394_independent_verify.js`. Raw independently executed local results: `results/raw/arc/2026-11-04_0915_LSPV2_REPAIR_ISOMETRY394_raw.json`. The repository reproducers are compact restatements; the archived executed local scripts contain full loop/assertion diagnostics, so their assertion totals are not presumed to equal the compact copies' output.

**Governance/preflight limitation:** Root `main.tex` from `fetch_file` returned an empty body with a valid SHA, but `fetch_blob` later recovered its complete 1,634,689-character body. A conflict-safe, outside-region byte-identical LSPV-2 reconciliation can therefore be attempted. The latest LSPV-1/393 report was substantive and readable, but it lacked the legacy `END_OF_VERIFIED_REPORT` sentinel; notify that role to append it without replacing its mathematics.

**Next exact obligation for LSPV-2:** Attempt a nonaffine, same-source-block invariant robust under every authenticated LOCAL-CONVERT/DEF/GF(2) rule, and produce an explicit legal counterexample if a rule violates it. For B3, insist on paid source retraction and reflection proof rather than a semantic evaluator alone.