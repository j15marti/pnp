# LSPV-1/548: Polynomial owner-bound DEF/Resolution shortcut for Braun bit-PHP
**2026-11-09 16:00 PST | Route B | PROVED/RESTRICTED in a DECLARED semantic completion; COMPUTATIONAL finite source-bound derivations; historical R_mix341 and P versus NP OPEN.**

## IDEA, prediction and falsifiers
Candidate: the published Braun original *wide* bit-pigeonhole sources, exponentially hard in shared-DAG Res(XOR), admit polynomial cost in an **extensional DEF-facet + signed Resolution semantic completion** of the /341 prose. Explicitly compile the bit sources into unary PHP using only fresh two-input gates and source-authenticated RES; then append Cook's published polynomial ER proof. This is a candidate **upper-bound shortcut control**, not a new lower bound.

F1: A source clause is secretly replaced by a stronger derived collision clause without a signed Resolution trace. F2: the "every pigeon has a hole" clause is inserted as a free tautology, rather than derived using charged definitions. F3: the exact historical grammar does NOT permit a RES premise to refer to one of a charged DEF owner's facets; then the construction is not native R_mix341. F4: standard ER definitions cannot be compiled into conservative two-input gates with constant-overhead facets; if so the appended Cook stage fails. The finite compiler tests F1-F2, and the stated semantic rules establish F4 under those rules. F3 remains OPEN and is the central adversarial task.

## SEARCH/continuity and source ledger
Read full root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), proof2.txt (prewrite blob 54aadf0ca552bcbe7d6eec78b8cb2fb82dc6a255), 2026-11-09 abstract-negative handoff (8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b), current coordination issue #3, AGENTS.md, CODEX.md and pnp-research/SKILL.md. Read native semantic declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (c87acd11), compiler research/agents/lspv-2/2026-11-03_1212_LSPV-2_BRAUN_GF2_NATIVE_BACKTRANSFER369.tex (927ba217), LSPV-1/547 (c93f788d), LSPV-3/543 (7ef3014a), actual GROKPROOF/2026-11-09_2015_PROGRESS.md (5610d47e) and Claude research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (b7150bb9). The two last files do not authenticate native facets.

Targeted change-aware repo review: konard/p-vs-np/scripts/proof_status.json, blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea), meelgroup/frat-xor/format.md (986a21aa), openai/math/README.md (cc5b0a03). The external FRAT-XOR format explicitly excludes RAT and does not authenticate /341. Both independent repositories present limited/model-scoped research, not P-vs-NP solutions.

Primary sources: Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2 (2026-11-03), restricted to his Res(XOR) proof system; Stephen Cook, *A short proof of the pigeon hole principle using extended resolution*, SIGACT News 8(4):28-32 (1976), DOI 10.1145/1008335.1008338; the explicit gate recurrence is summarized in Cook/ER surveys and Grosof-Zhang-Heule, arXiv:2207.11284 (Cook O(n^4) ER upper). Published Cook result is for unary PHP; the **bit-to-unary syntactic compiler below is supplied here**. The Braun main theorem/Lean artifact were not independently kernel replayed; the Cook full ER refutation was not generated. Independent peer review pending.

## Exact source, rule scope and theorem
Let ell>=2, n=2^ell, pigeons i=0,...,n, bit variables x_(i,k), k=0,...,ell-1. For each i<j and word a in {0,1}^ell, the ONLY original source premise is

$$
D_{i,j,a}=\bigvee_{k<\ell}(x_{i,k}\ne a_k)\ \vee\
           \bigvee_{k<\ell}(x_{j,k}\ne a_k).
$$

The original source contains m=n*binom(n+1,2) width-2ell clauses and (n+1)ell variables; explicit binary-identifier source length N=Theta(n^3 ell^2).

**R_fac (DECLARED SEMANTIC COMPLETION, NOT HISTORICAL BYTE GRAMMAR):** Source-indexed original clauses are free. A fresh *two-input total Boolean gate* DEF costs one globally distinct owner, and all its exact signed-CNF functional facets are available as explicitly OWNER-BOUND zero-additional-node premises (never as independent source axioms). Binary signed Resolution costs one node per distinct inference; reused nodes are free. Gates may be signed projections and AND with a negated input, both ordinary two-input functions. There are no case rules, oracles or uncharged independent definitions. This is consistent with /341's semantic prose only if owner-bound facet-to-RES references are natively accepted. That exact condition is unverified P2-D1.

**Theorem 548.1 (PROVED/RESTRICTED):** In R_fac, all unary PHP(n+1,n) clauses, over fresh decoder leaves y_(i,a), follow from the **original bit-PHP source** with at most the following total DISTINCT paid nodes:

$$
q_{\mathrm{pre}}=(n+1)\left(4n-5+\frac{n\ell(\ell-1)}2+n^2\ell\right).
$$

The derivation is explicit, uniform, acyclic, source-authenticated and reuses each compiled leaf implication across collisions. Moreover Cook's polynomial-size unary PHP extended Resolution proof can be appended, since each constant-arity ER definition is a composition of O(1) paid binary DEF gates and every facet is owner-bound. Hence

$$
W_{R_{\mathrm{fac}}}(F_\ell)\le q_{\mathrm{pre}}+O(n^4)=\operatorname{poly}(N).
$$

The polynomial full-refutation statement is **conditional on the declared R_fac grammar** and standard Cook ER theorem, NOT established for historical R_mix341.

**Construction/proof:** For each pigeon create one DEF gate for every nonempty binary address prefix p. The depth-one gates denote NOT(x_i0) and x_i0, with the other input x_i1 ignored: they are genuine two-input signed-projection gates since ell>=2. The two gate facets (x_i0 OR y_i0) and (NOT x_i0 OR y_i1) resolve to y_i0 OR y_i1, so no free tautology is assumed.

For each longer p and each next bit k, create child gates y_(p0)=y_p AND NOT(x_ik) and y_(p1)=y_p AND x_ik. Their owner-bound join facets resolve on x_ik to (NOT y_p OR y_p0 OR y_p1). Resolving the current coverage clause on y_p proves a disjunction of ALL n address leaves. This uses 2n-2 DEF and 2n-3 RES nodes per pigeon.

For each leaf y_(i,a) and each k, follow the owner-bound parent facets up to the prefix of length k+1, then use its bit facet to prove (NOT y_(i,a) OR (x_ik=a_k)). The total additional RES count per leaf is exactly ell(ell-1)/2. Finally resolve each original D_(i,j,a) against the 2ell already shared leaf-bit implications, yielding (NOT y_(i,a) OR NOT y_(j,a)); this uses exactly 2ell paid RES per original collision source. Counts add to the displayed q_pre. All RES parents are source or owner-bound derived clauses, never a hypothetical semantic oracle.

Cook ER supplies a polynomial refutation of the resulting ordinary unary PHP clauses. Its q < O(n^4) bound absorbs constant-size two-input decomposition of higher-arity extension gate syntax. Concatenation produces a valid R_fac refutation. QED for the **declared** calculus.

## ITERATE / CEGAR and validation
Executable: experiments/arc/lspv1_548_bitphp_to_php.js. It constructs the entire source and typed DEF/RES derivation for ell=2,3,4, checking exact oriented pivots, deduplicated normalized resolvents, source IDs, owner-bound clauses, final pigeon coverage and collision clauses. It does **not** generate Cook's appended proof or invoke an authoritative historical checker.

| ell | n | original source clauses | paid DEF | paid RES | total q_pre | collision clauses |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 4 | 40 | 30 | 205 | 235 | 40 |
| 3 | 8 | 288 | 126 | 2061 | 2187 | 288 |
| 4 | 16 | 2176 | 510 | 19533 | 20043 | 2176 |

Each run rejected an illegal pivot and out-of-range source control. A separate Python truth-table exercise exhaustively checked all 1024 five-pigeon assignments when ell=2 (40960 source/collision comparisons) and sampled 2000 nine-pigeon assignments at ell=3 (576000 comparisons). This independently checks semantic decoding, not actual RES-checker bytes. No historical parser, Cook proof checker, Lean replay or root preflight was run.

**CEGAR diagnosis:** If a coarse abstraction omitted actual owner-bound DERIVED one-hot clauses, this explicit inexpensive derivation is real in R_fac and must be admitted. An abstract path that treats facets as independent free source axioms, or omits a paid DEF owner, is spurious and must be refined by owner provenance and freshness. For historical R_mix341, F3 is unresolved; do not accept the path as native until LSPV-3 authenticates the facet selector. If it is native, Braun bit-PHP is unsuitable for any superpolynomial full-calculus lower bound, even though it is exponentially hard in Res(XOR).

## Resource and three-track ledger
Logical paid nodes q_pre as above; source and DEF facet views free only under R_fac. Encoding and output bits require additional O(poly(n,ell)) time/space and logarithmic variable IDs, source acquisition, DEF truth-table checks, clause sorting, lookups, caches and certificate output. No actual native bit-time or peak RSS measurements; source materialization is cubic. No runtime bound for arbitrary SAT solvers follows from this output-size upper bound. Parallel span and total work are distinct; decoder gates have depth ell but the provided serial derivation is not a span optimum. (i) Chosen solver class: no new class-runtime lower bound. (ii) R_fac proof calculus: polynomial upper control for original bit-PHP; full R_mix341 P2-B1 OPEN. (iii) All-decider machine lower bounds: OPEN. No same-R B3 proof or Route A FLMV transformation.

## Outcome and next falsifiers
The main **new project-specific result** is a complete quantified source-authenticated bit-to-unary PHP compiler with exact polynomial native-semantic paid-node count. It materially narrows Braun-family lower-bound transfer: any historical grammar supporting the R_fac owner/facet interface already has a short bit-PHP proof, even without standalone GF(2). Distinct-node sharing, assumptions (none here) and zero-cost facet ownership are explicit.

LSPV-3: produce ONE historical accepted-byte DEF-owner/facet->RES trace, or show owner selectors absent. LSPV-5: adversarially replay malformed owner references, duplicated symbols and Cook-gate compilation; reject unauthenticated "free facet" axioms. P2-D1, P2-C3, P2-B1, P2-B2, B1/B2/B3 and P-vs-NP remain **OPEN**. Historical rules, weights, five roles, 2A/3B allocation and automations unchanged.


### Source-file exact replay addendum (same run)
After first publication, the executable was strengthened and re-executed: every signed RES record now retains its actual parent IDs and pivot, and a second pass verifies the derived clause independently from those recorded premises in topological order. Each distinct paid DEF owner now records BOTH original input wires even for signed projection gates. Every one of its exact owner-bound defining facets was rechecked against all 8 possible assignments to the two inputs and output. The strengthened code passed all $\ell=2,3,4$ instances, replaying respectively 205, 2061 and 19533 Resolution records and checking 240, 1008 and 4080 owner truth-table rows, with the same paid counts. This is a **separate replay inside the same implementation**, not a historical authoritative checker or independent specialist audit. Published code blob: \`c914c20c1889269deab877041b6f26d2efe23e89\`. No extra mathematical claim, scheduler or rule change.
