# LSPV-2/413: Nonlinear paid-DEF elimination cannot be represented by affine rows alone

**November 5, 2026, 02:12 PST. Role:** PNP SAT-Circuit Reduction Builder (LSPV-2). **Original fixed calculus:** `R_mix341`, defined in `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`), unchanged. **Status:** PROVED/EXACT for the stated small algebraic and finite CNF claims, and an 11-node original-source RES/AND3/GF(2) derivation; COMPUTATIONAL independent tests; CONDITIONAL 12-node LOCAL variant; OPEN native DEF exports, LOCAL byte grammar, full normalizer, B1/B2/B3, superpolynomial mixed proof cost, P versus NP. Specialist mathematical review pending.

## IDEA (before SEARCH): a falsifiable compiler failure

Attempt to eliminate every *paid* two-input conservative DEF output by replacing it with GF(2) equations only on original inputs, then replay later affine proofs. Predict failure on a nonlinear two-gate network, but compact non-affine CNF/circuit recovery. Falsifiers: (F1) projected relation may secretly be affine; (F2) alleged native proof may rely on unauthenticated DEF-to-GF2 exports; (F3) eliminating a gate may need many clauses even in this constant-size case; (F4) a polynomial SAT decider may secretly supply a native proof without proving machine-correctness reflection. F1 is refuted by triple-XOR witness; F2 avoided in a separate legal native source-only replay; F3 defeated by an exact six-clause CNF; F4 remains an unsupported B3 step.

## SEARCH: source log and duplication/access audit

Read governing five-role refocus `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, issue #3 and current peers, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, literal original /341, /384 native grammar addendum, LSPV-2/371 and /412, LSPV-3/414 and /417, LSPV-4/408, LSPV-1/413, and REFEREE358. Actual Grok `GROKPROOF/2026-11-05_1218_PROGRESS.md` blob `d3183283` and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6` reviewed: neither establishes B3 or a native grammar compiler. LSPV-2/371 already proves a scoped nonlinear-gate branching lemma; /412 already refutes independent shared-variable projection; LSPV-3/414 already falsifies source-model-only GF(2) retyping. These precedents are NOT claimed new.

Actual general-web queries: `Haken 1985 intractability of resolution theorem pigeonhole principle 2^cn size paper PDF`; `Cook 1976 feasibly constructive proofs pigeonhole principle extended resolution`; `Raz Tzameret resolution over linear equations Res(lin F2) Tseitin`; `Cook Reckhow 1979 relative efficiency propositional proof systems NP coNP polynomially bounded`; `Pich Santhanam 2023 199 self provability EF SAT polynomial time uniform`; `Armin Haken The Intractability of Resolution 1985 Theoretical Computer Science 39 297 308 publisher`. Read Haken publisher abstract, author-hosted full Cook–Reckhow paper (including PDF page image), Raz–Tzameret institutional record, Pich–Santhanam ECCC record. Direct Google-branded search is unavailable; indexed general web search was used. Authenticated `github.com/openai` searches: `ExecCNFNodeSearchCosts`, `CookLevin`, `LRAT checker`; read **complete** `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f4`, and `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean` blob `1e23a159`. They do not prove the required same-calculus compiler. Repository code searches `affine elimination paid DEF`, `nonlinear gate GF2 projection` located the duplicate predecessors. Local git network access failed DNS; authenticated GitHub connector used.

## ITERATE: exact nonlinear quotient counterexample

Let `x,y,z` be original variables. Add TWO separately charged fresh conservative two-input gates
$$c=x\land y,\qquad d=c\oplus z.$$
Each original assignment uniquely extends. Eliminate internal `c`, yielding the exact graph on original/exposed variables
$$Q(x,y,z,d)\ \iff\ d=(x\land y)\oplus z.$$

**Theorem 413.1 (PROVED/EXACT; model-scoped).** No conjunction of any number of GF(2) linear equations *over x,y,z,d alone* defines `Q`.

**Proof.** Every nonempty solution set of a linear system over GF(2) is an affine coset and is closed under triple XOR. The three satisfying tuples `0000,0100,1000` have triple XOR `1100`, which violates `d=xy XOR z`. Contradiction. This does NOT exclude disjunctions of linear equations (Res(XOR)), CNF, non-affine circuits or separately paid auxiliaries.

A compact **auxiliary-free repair** is the six-clause exact CNF:
$$
\begin{aligned}
&(\neg x\vee\neg y\vee\neg z\vee\neg d),\quad
(\neg x\vee\neg y\vee z\vee d),\\
&(y\vee\neg z\vee d),\quad(y\vee z\vee\neg d),\\
&(x\vee\neg z\vee d),\quad(x\vee z\vee\neg d).
\end{aligned}
$$

**Theorem 413.2 (PROVED/EXACT finite).** Every equivalent auxiliary-free CNF over these four named variables requires at least SIX non-tautological clauses. An exact six-clause CNF requires at least TWENTY literal occurrences. The displayed CNF achieves both bounds. **Proof:** Of the `3^4 - 1 = 80` proper nonempty signed clauses, exact evaluation on `Q`'s eight satisfying valuations finds precisely 12 nontrivial implicates. Six nonmodels with lexicographic indices `2,3,4,5,6,7` are pairwise incompatible under implicates: each implicate can exclude at most one of the six. This proves the six-clause floor. The twelve implicates' `2^12=4096` subsets can be exhaustively covered independently of the producer's 256-state minimum-cost DP, certifying the optimal `(clause count,literal count)=(6,20)`. The companion standalone checker recomputes this independent exhaustive certificate. This is a *finite representation minimum*, not an asymptotic mixed-proof cost lower bound.

## Native authenticated control and conditional LOCAL test

Original CNF `F` has five **original** variables `x,y,z,a,b` and fourteen authenticated signed source clauses: three CNF gate clauses for `a=x AND y`; four parity clauses for `a XOR z XOR b=0`; units `x,y,NOT z,NOT b`; padding clauses `(a OR x),(NOT z OR x),(NOT b OR x)`. The exact 111 ASCII-byte DIMACS source and full replay certificate are in the downloadable reproducibility archive. The source is UNSAT under all 32 valuations; deleting `NOT b` or `y` gives SAT controls.

A strictly native **11-paid-node** proof (NO DEF facets or LOCAL private exports) has: 2 RES nodes deriving `a` from clauses `NOT x OR NOT y OR a, x, y`; 3 AND3 nodes identifying the globally exact rows `a=1, z=0, b=0` using independent implied padding source clauses; 3 AND3 nodes conjoining four authenticated parity clauses into the globally exact row `a XOR z XOR b=0`; 3 binary GF(2) additions deriving `0=1`. Every factor's combined support is at most three ORIGINAL variables, every added node is charged, and all signed rows are checked under all input assignments. Thus `W_R(F)<=11`. No global shortest-proof claim is made: redundant padding sources invalidate a source-arity minimum proof.

A second **12-paid-node** certificate inserts a unary LOCAL circuit root (8 explicit binary representation gates) into the parity-factor chain. The root implication is globally correct, but native serialization and whether internal payload gates require separate DEF charges remain unspecified. **Hence the 12-node count is CONDITIONAL, not a certified legal-native byte-level claim.** The separate conservative paid `c,d` gates in Theorem 413.1 are NOT ancestors of the above contradiction; no GF(2) operands are illicitly exported from them.

## Verification and physical resource firewall

Standalone Python producer and independently authored JS verifier are in the complete attached reproducibility archive. The independent JS run verified 11-node and conditional 12-node typed derivations, all 32 source models, all 16 four-variable truth rows, exact 12 implicates, exhaustive 4096 subset covers, four malformed DIMACS cases and five corrupted proof controls: **657 assertion groups PASS**. The native source has 111 ASCII bytes (888 bits). Full machine-readable proof/test record has **10,939 bytes**. Distinguish 11 paid logical nodes, 12 conditional LOCAL nodes, two separate paid gate definitions, length of circuit payload, input acquisition, proof parsing, index lookup, checking and output, and peak physical memory. Neither host program establishes FLMV native time/space bounds.

## Transfer audit, exact role of established lower bounds, outstanding obligations

Haken's exponential lower bound is for **ordinary DAG Resolution** on standard PHP of polynomially encoded length, **not** all SAT decision algorithms nor the full mixed calculus. Cook/Extended Resolution and affine Tseitin shortcuts are mandatory family controls. A purported universal normalized translation that erases GF(2) into source-only Resolution is already disproved by REFEREE358 using restricted hard families. Our new theorem only invalidates replacement of nonlinear DEFS by conjunctive affine rows in original variables. It is repaired with 2 paid gates or 6 clauses, so no failure of B1, B2, B3 or a new mixed lower bound follows.

For the SAME preselected `R_mix341`, the B3 target
$$SAT\in P\ \Longrightarrow\ \exists C,k\;\forall N:\ \overline W_{R_{mix341}}(N)\le C(N+1)^k$$
remains **OPEN**. Cook–Reckhow ensures a polynomially bounded proof system exists if NP=coNP, but does **not** identify this fixed R. A polynomial-time decider's rejecting trace is not a certified source-authenticated native refutation unless its correctness/reflection has independently proved polynomial simulation. Assuming that certificate already exists is circular. This run neither proves nor refutes B3.

**Root MAIN safety:** authenticated `main.tex` retrieval returned existing SHA `4d40c3eab611ad5e0df785bde88a4ff468c1f6d7` with **ZERO content bytes**. It was not overwritten. No other role's region or task identity, schedule, enabled state, rule or weight was modified. Full checkout preflight and manuscript compilation unavailable; document this rather than claim they passed.

**Next decisive obligation:** obtain authoritative byte-level selectors for paid DEF facets, DEF-to-GF2 row operands, LOCAL public/private wire exports, LOCAL internal-gate charging and AND3 source typing. Then attempt an actual source-authenticated and consumer-preserving **nonlinear** DEF->LOCAL/AND3->GF(2) full proof compilation, or produce a genuinely legal native obstruction. Separately establish noncircular same-R B3; do not use a shortest-proof optimizer as nonuniform advice.

## Primary references

[1] A. Haken, "The Intractability of Resolution", TCS 39 (1985), 297-308. DOI 10.1016/0304-3975(85)90144-6.

[2] S. Cook and R. Reckhow, "The Relative Efficiency of Propositional Proof Systems", JSL 44 (1979), 36-50. https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf

[3] R. Raz and I. Tzameret, "Resolution over Linear Equations and Multilinear Proofs", APAL 155 (2008), 194-224. DOI 10.1016/j.apal.2008.04.001.

[4] J. Pich and R. Santhanam, "Towards P != NP from Extended Frege Lower Bounds", ECCC TR23-199 (2023), https://eccc.weizmann.ac.il/report/2023/199/.
