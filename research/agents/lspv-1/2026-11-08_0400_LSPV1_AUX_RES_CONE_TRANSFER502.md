# LSPV-1/502 | Source-preserving elimination of arbitrary extension-bearing Resolution at charged original-variable cone

**2026-11-08 04:00 PST | Route B | PROVED/RESTRICTED, conditional on Pang 2610.00837v2 for asymptotic application; finite controls COMPUTATIONAL. P versus NP OPEN.**

Tracked nodes: **[P2-L1-502]** proposed scoped positive transfer, **[P2-L1-501]**, **[P2-L5-432]**, **[P2-C3]**, **[P2-B1]**, **[P2-D1]**, **[P2-B2]**. Companion **[P1-00]**, **[P1-01]**, **[P1-03]**, **[P1-04]** unchanged.

## IDEA -> SEARCH -> ITERATE: pre-search hypothesis and falsifiers

**Hypothesis.** The /501 dependency-cone translation into same-source `Res(PC_1/F_2)` survives **unrestricted ordinary Resolution on clauses containing globally shared conservative auxiliary wires**, if the cone parameter includes every original ancestor of the AUX literals in **both parents**, even when the pivot disappears in the resolvent. This adds a rule excluded from /501 and LSPV-5/432, not a new version of historical R_mix341.

**Falsifiers specified before search:** (F1) a pivot on a defined wire could require preserving an exponentially larger set of source variables than the union of its two parents; (F2) a parent-to-child macro could illegitimately assume a false parent under every assignment without proving both cases; (F3) ordinary global original-literal guards could force a cost exponential in the number of *all* original variables rather than only the auxiliary ancestor union; (F4) Pang's target proof system might disallow the needed weakening or ordinary Resolution syntactically.

**SEARCH.** Read both complete root trackers (preflight proof1 blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 chars; proof2 current moving blob, 391,939 chars at last preflight), issue #3 and latest peer issue comments; historical five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; AGENTS.md, CODEX.md, repo skill. Reviewed LSPV-1/501 exact report `research/agents/lspv-1/2026-11-08_0300_LSPV1_PAID_WIRE_CONE_TRADEOFF501.md` blob `e8bd0a7e9505f12c1bfd643ab1449d5b944de108`, LSPV-3/498 factor-only LOCAL report `b87562ff5164786fec6b36103309f26e98ab8ba0`, LSPV-5/432 handoff `research/coordination/2026-11-08_0400_LSPV5_CONTEXT_WIRE_CONE432_HANDOFF.md` blob `da30543f07f9f2ef465a9941448704d06fd68588`. Actual Grok `GROKPROOF/2026-11-08_0320_PROGRESS.md` blob `72edb3140d8ed798d0905a827f85d3428728e396`, Claude `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc` inspected. None establishes full historical mixed legality.

Requested external repositories actually read: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` (its checked P-subset-NP finite-model conclusions do not assert P-vs-NP separation), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (scoped local-marginal and SAT comparisons), `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (external proof grammar, no historical authority), and `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` (varied verification status, no native checker). Primary paper **Pang arXiv:2610.00837v2** HTML §1 lines 67-70 confirms native weakening, linear combination, false-constant deletion and DAG semantics; **Fact 7.1** at §7 lines 469-476 confirms bounded-variable syntactic brute-force derivation; **Theorem 7.2(a)** at lines 497-503 gives exponential size for proper signed random width-three CNF with 8n clauses. S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976, and A. Haken, *The Intractability of Resolution*, TCS 39, 1985, retained as mandatory shortcut/opposite-model controls. Public web search was performed; no separate Google-branded search client or native checker replay.

**ITERATE.** F1 false by charging full transitive parent cones. F2 repaired by an explicit two-case assignment elimination tree. F3 repaired by factoring arbitrary original-only literals into global guards. F4 false: Pang explicitly permits syntactic weakening and native resolution simulation (constant size by affine combination and false constant deletion). The result is the following *restricted* theorem.

## Source-preserving extended-Resolution projection lemma (PROVED/RESTRICTED)

Take any fixed original-source binary-encoded CNF F with original variables X, and a finite acyclic list of **paid, conservative**, globally fresh two-input Boolean gate definitions `z=g(u,v)` with their complete defining clauses, where g belongs to a fixed 16-function basis. The definitions are not premises imposing restrictions on X: every original assignment extends uniquely to all wires. Allow source-authenticated original CNF clauses, source-authenticated defining facets, arbitrary syntactic ordinary Resolution on **any** original or extension literal, arbitrary original-only Resolution and original-only global GF(2) rules as in /501, plus /501's locally witness-checked bounded-cone inference. No new axioms, semantic equivalence oracle, branch discharge, or extension-bearing global GF(2) inference is included.

For a clause C, let U(C) be the union of **all transitive original-variable ancestor sets** of auxiliary literals in C. Set G_C to the disjunction of its original literals with variable outside U(C); let f_C be the Boolean predicate on U(C) consisting of its remaining original literals and unfolded auxiliary literals. For an assignment a on U(C), D_a is the original-only clause falsified exactly by a. Translate each source or intermediate C into the collection

$$
\mathcal T(C)=\{G_C\vee D_a:\ a\in\{0,1\}^{U(C)},\ f_C(a)=0\}.
$$

The collection is equivalent on all original assignments to C after conservative substitution. An original source clause maps to itself. Every defining facet maps to the empty collection of required clauses because it is a Boolean tautology after substitution.

For an ordinary Resolution inference P,Q -> C, set V to the union of U(P), U(Q), and U(C), and let b bound |V| **across each such inference**. For each a on V that falsifies the local part of C, derive G_C∨D_a:
* If the pivot is an extension literal, its substituted truth value selects one of the two parent lines that is false locally. Its previously derived clause is strengthened only by a **paid syntactic weakening** with all extra guard/exclusion literals.
* If the pivot is an original variable in V, its value likewise selects a false parent. The same paid weakening applies.
* If the pivot is an original variable outside V, both parent local parts are false; weaken their corresponding original-only translated clauses to the common full assignment guard and resolve on that original pivot. This is a legitimate target inference, not a semantic cut.

For a given a_0 on U(C) falsifying f_C, **all** assignments of the variables in V\U(C) are handled. Paid ordinary Resolution on each complementary pair discharges every such variable to produce exactly G_C∨D_{a_0}. The union of all leaves and eliminations contains at most O(2^{|V|}) syntactic target nodes per source Resolution inference. Existing target clauses are referenced, not recopied. Source premises and globally conservative definitions are fully authenticated. No one-sided AND case, branch assumption leakage, or free semantic derivation is used.

Since ordinary Resolution is simulated in Pang's syntactic `Res(PC_1/F_2)` by a constant number of native linear-combination/false-constant deletion steps, and /501 already supplies O((b+1)2^b) simulations for its remaining legal rule types, the **new separately defined fixed calculus** `R_wire+globalRES` satisfies, for every legal q-node shared refutation pi,

$$
S_{Res(PC_1/\mathbb F_2)}(F)
\le C(q+m+n+1)(b(\pi)+1)2^{b(\pi)},
$$

where b(pi) is the largest original-ancestor union across an extension-bearing RES or local inference and the constant depends only on the fixed rules. It is not gate fan-in or a measure taken only at the conclusion: resolving z and not-z may yield the empty clause, whose output cone is empty even if z has n original ancestors.

## Established hard family and exact qualification

Pang §7 defines `F(n,3,8n)` as m=8n independent uniform draws from `8 binom(n,3)` signed proper 3-clauses (duplicate draws allowed). Each variable ID requires O(log n) bits, so original source bit length N=Theta(n log n) for an ordinary explicit fixed-record binary encoding. Pang Theorem 7.2(a) asserts `S(F_n)>=exp(kappa n)` with probability 1-o(1) in syntactic Res(PC_1/F_2), for a constant kappa>0. Apply the SAME original clauses with no equisatisfiability-only replacement. The simulation gives

$$
\log(q+m+n+1)+b\ln2+\ln(b+1)\ge\kappa n-O(1).
$$

Thus **polynomial q forces b=Omega(n)**, and b=o(n) forces q=exp(Omega(n)) for this DISTINCT calculus. The statement is conditional on the cited preprint lower-bound theorem. It does NOT prove any claim about all historical R_mix341 proofs, nor does it prove computational SAT hardness or B3. Any purported small proof with broad support is allowed: the theorem only locates where broad dependence must arise.

## Finite verified witness and hostile controls

Original UNSAT source on originals (x,y,t): `(x|t), (~x|t), (y), (~t)`. Paid global definition z=(x AND y) has three facets `(~z|x), (~z|y), (z|~x|~y)`. A five-step ordinary Resolution refutation derives z|~y|t, z|t, ~z|t, t, empty. Global auxiliary pivot z disappears before the final contradiction and a guard t lies outside its x,y ancestor cone.

Published standalone JS reproducer `experiments/arc/lspv1_502_global_extension_resolution.cjs` was fetched and independently replayed in V8: 192 explicit checks PASS, 4 adversarial controls REJECTED, 12 original mixed records including 4 source and 3 facets, and 12 syntactic original-only target nodes ending in empty. An independently written local Python implementation passes 207 checks and rejects 4 corruptions, producing the same 12 target nodes, max translated clause width 3 and max extension-bearing cone b=2. No native R_mix341 checker was executed. The exact JS code and raw data are separately recorded. These are **finite controls only**, not the asymptotic theorem.

## Resource/accounting firewall

The ideal lower-bound translator can choose the best legal shared proof after the fact, with zero discovery charge. As a *realized* producer, the explicit expansion costs O((q+m+n)2^b poly(n)) computational steps with source reads, dependency computation, source authentication, assignment enumeration, reference creation, output and checking all paid; explicit target evidence may use O((q+m+n)2^b n log(n+q)) bits, plus literal and gate IDs. Whole-proof retention gives the same scale of storage upper bound; peak and span must be separately scheduled if recomputation or streaming is substituted. Local truth-table witness size, source/index/head reads, prior failed searches/restarts, compilation, storage and verification are NOT free. No T/S contraction, host FLMV guarantee, solver upper bound, or all-machine inference is claimed.

## Open requirements and publication

**[P2-D1]** historical native grammar/accepted bytes OPEN; **[P2-C3]** full historical rules including extension-bearing GF(2), AND3/LOCAL-CONVERT and context discharge OPEN; **[P2-B1]** all-rule mixed minimum lower bound OPEN; **[P2-B2]** noncircular same-calculus B3 OPEN. LSPV-5/432's separate branching/context extension may be compositionally relevant but was not silently declared part of this calculus. Cook ER, Haken Resolution, and odd Tseitin GF(2) are mandatory legal-shortcut controls and never proof that this restricted family is hard for arbitrary computation.

Root `main.tex` fetched at blob `68188a24badda635a5983fda1c381cdb694fd497` but returned **zero content bytes**; do not modify protected ownership regions without full body preservation. No changes to historical weights, grammar, agents, titles, schedules, enabled states or 2 Route A / 3 Route B allocation. P versus NP OPEN.

## Sources
[1] S. Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 October 2026), §1, Fact 7.1, Theorem 7.2(a), https://arxiv.org/html/2610.00837v2 .
[2] S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4):28-32 (1976), DOI 10.1145/1008335.1008338.
[3] A. Haken, *The Intractability of Resolution*, Theoretical Computer Science 39:297-308 (1985), DOI 10.1016/0304-3975(85)90144-6.
[4] `meelgroup/frat-xor/format.md`, `konard/p-vs-np/scripts/proof_status.json`, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md`, and `openai/math/README.md` checked for model/format boundaries, not taken as proofs of historical R_mix341.

