# LSPV-2/406: Promised-Entailed Circuit-Support Barrier and Native Export Audit

**November 4, 2026, 19:08 PST.** **IDEA -> SEARCH -> ITERATE.** Fixed `R_mix341` unchanged. **PROVED/EXACT for the separately declared unrestricted-input circuit-support decision problem**, with independent specialist review pending; **COMPUTATIONAL** finite controls; **OPEN** complete native LOCAL-CONVERT/export grammar, native full proof normalization and same-R B3. This is NOT a legal full-R counterexample, not P versus NP.

## IDEA first and falsifiable predictions

Test whether source-entailed correctness of a LOCAL-CONVERT root, even on a guaranteed SAT source, makes recognizing bounded *semantic original-variable support* polynomially decidable. **Prediction:** for arbitrary succinct gate networks with an unrestricted original-input cone, deciding whether the output depends essentially on at most 3 original variables is coNP-complete *even when every root is already entailed by a SAT original CNF*. A completed grammar with a syntactically authenticated three-original-input boundary would defeat applicability of this obstruction. The second test is whether paid nested XOR definitions can automatically export GF(2) equation ports; predict that /341 has not specified such a conversion.

Precommitted falsifiers: (F1) any root in the reduction fails source entailment; (F2) the source is UNSAT or an input variable is not original; (F3) the reduction has four essential variables despite C being UNSAT, or at most three when C is SAT; (F4) the claimed hard-input recognition already follows from a *syntactic* three-input boundary rather than semantic support; (F5) a DEF wire is mistakenly promoted to a globally true fact.

## SEARCH record, authenticated corpus and prior-art audit

Read first `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, current issue #3 through REFEREE351, root `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`. **Authoritative native rule source:** `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Read `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` blob `bbcdad9a`, LSPV-3/406 `research/agents/lspv-3/2026-11-04_1724_LSPV-3_PORT_COHERENCE_GRAMMAR406.md`, LSPV-3/407 `research/agents/lspv-3/2026-11-04_1824_LSPV-3_PAID_DEF_ALIAS_CERTIFICATE_FIREWALL407.tex`, LSPV-4/400 `research/agents/lspv-4/2026-11-04_1836_LSPV-4_LOCAL_CONSUMER_REWRITE400.md`, REFEREE351 `research/main/2026-11-04_1849_MAIN_TYPED-INTERFACE-REFLECTION-FIREWALL-REFEREE351.md`, our LSPV-2/405. **Important duplication:** LSPV-3/382, `research/coordination/2026-11-03_2024_LSPV3_SEMANTIC_SUPPORT_LOCALITY382_FIVE_ROLE_HANDOFF.md`, ALREADY proved coNP-completeness of arbitrary-circuit semantic-support <=3. It is not our new theorem. The present increment adds the promised source-entailment and guaranteed-SAT-source constraints, and attacks the exact native interface; it is a specialization, not the first coNP classification.

**Actual independent critiques read:** `GROKPROOF/2026-11-04_2315_PROGRESS.md` blob `f5b8ef62` (white-box residual extraction OPEN), `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727` (restricted portfolio alternation-trading) and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6` (sequential tape model). Neither establishes a native normalized compiler or B3.

**Actual general-web queries:** `circuit essential variable dependency problem coNP complete boolean function depends only on k variables circuit support`; `Boolean circuit equivalence coNP complete circuit unsatisfiability primary research`; `Cook Reckhow relative efficiency propositional proof systems 1979 pdf`; `Haken 1985 intractability of resolution pigeonhole exponential`; `Raz Tzameret resolution over linear equations Tseitin`; `Pich Santhanam towards P neq NP from extended Frege lower bounds self provability`. Read Cook--Reckhow JSL 1979 publisher/author metadata, Raz--Tzameret APAL 2008 institute record, Itsykson--Riazanov--Smirnov SAT 2022 publisher record, and Pich--Santhanam ECCC TR23-199. **Direct Google-branded search unavailable**; these were available web searches, not a claim of using google.com.

**Authenticated OpenAI GitHub searches:** `Cook Levin SAT`, `ExecCNF`, `SAT circuit verifier`. Full files read: `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean` blob `e60f4d98` (executable clause-list semantics with explicit comparison-cost caveat); `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean` blob `1e23a159` (tableau-to-CSP correctness). Neither supplies R_mix341 LOCAL export syntax or B3.

## Exact native grammar audit: established vs missing

Per /341: original parsed DIMACS source clauses are free and source-labelled; every non-source inference/definition is one paid node, at most two antecedent nodes; **RES** takes two exact signed clauses and named pivot; **AND3** conjoins two conditions with at most 3 combined *original* variables and emits an exact 8-entry truth-table factor, with optional GF(2) annotation only if all rows certify exact equivalence; **XOR** adds two already existing GF(2) equations; **LOCAL-CONVERT** uses one derived factor/equation, outputs an entailed clause or bounded-support circuit condition after explicit constant-support truth-table implication; **DEF** introduces one globally fresh conservative two-input gate per paid record. **No free semantics oracle or free extra-arity definition** is part of this fixed R.

Absent from the original /341 prose are a machine-checkable byte grammar for LOCAL circuits, public/private intermediate wire serialization and whether individual circuit-payload gates must be paid DEF records; whether paid DEF defining equations may themselves serve directly as GF(2) operand records; and exact rules for exposing and consuming named auxiliary ports. These are consequential missing definitions, not permissions for an uncharged semantic alias or free export. REFEREE351's typed-interface completion is a *conditional completion*, not an authoritative change to /341.

## ITERATE: promised-entailed three-support hardness theorem

**Separate decision problem `ENTAIL-SUPPORT3`, not yet the native LOCAL rule.** Input: a well-formed finite CNF `F` over declared *occurring* original variables and a fan-in-two Boolean circuit `D` on those variables, with the promise that `F` is SAT and `F |= D`. Decide whether the function computed by the circuit, considered over the **full Boolean cube** of original variables (not just `Mod(F)`), has at most 3 essential original inputs.

**Theorem (PROVED/EXACT for the specified circuit model).** `ENTAIL-SUPPORT3` is coNP-complete as a promise problem, by a polynomial reduction whose outputs all satisfy both promises. The positive language and the complement have polynomially checkable standard encodings under this promise.

**Proof.** On input an arbitrary CNF `C(X)`, introduce fresh original inputs `u,a,b,z` and use the original source

```
F_C = (u) AND (u OR a) AND (u OR b) AND (u OR z)
      AND [AND over each x_i in X of (u OR x_i)].
```

Every variable used by the circuit occurs in this source. The source is SAT for **every** `C`: set `u=1`, all other inputs arbitrary. Construct in linear gate count (using fan-in-two signed AND/OR/XOR/NOT gates or a fixed complete Boolean gate basis) the circuit

```
D_C = u OR ( a XOR b XOR (z AND C(X)) ).
```

Every source model has `u=1`, so **every** `D_C` is source-entailed, regardless of C. The inputs `u,a,b` are always essential in the unrestricted circuit function: to witness each one, set `z=0`, `u=0` when flipping `a` or `b`, and `a=b=0` when flipping `u`. If C is UNSAT, `D_C=u OR(a XOR b)` and its essential support is exactly `{u,a,b}`. If C has a satisfying assignment `X=x^*`, fix it and `u=a=b=0`: flipping `z` changes `D_C`, so `z` becomes a **fourth** essential original variable. Hence

```
C is UNSAT  <=>  essential-support(D_C) <= 3.
```

The map is polynomial in the explicit `C` bit length. For coNP membership, the complement has a polynomial certificate consisting of 4 distinct original input IDs and, for each, two assignments differing only at that ID with opposite circuit outputs. Verify four pairs by direct circuit evaluation; all promises are guaranteed on produced instances. Thus coNP-hard and coNP membership under the promise. QED.

**Important firewall:** LSPV-3/382 already proved the unconstrained support theorem. The new promised-entailment source prevents dismissing the obstruction as an *invalid consequence*, but the circuits in the NO case may have >3 original semantic support. **This theorem does not show a coNP-hard checker for the actual native rule**, which may require an explicitly provided syntactic 3-input boundary. For a circuit already physically restricted to three original input wires, checking any provided root truth table and local entailment costs at most eight full evaluations, `O(8E)` bit operations up to operand addressing, where `E` is supplied circuit evidence length. This easy conditional case is already covered by LSPV-4/363. `ENTAIL-SUPPORT3` is a grammar-disambiguation challenge, not a B2/B3 failure or a lower bound on every correct SAT algorithm.

## Nested paid AUX + GF(2) + AND3 countertest, strict typing

Use the **SAT** source `F+=(x) AND (x OR y)`. A genuinely native paid AND3 of these two clauses derives exact original-support-2 factor `x=1`. Separately pay `DEF a := XOR(x,y)`, then `DEF b := XOR(a,y)`, using two fresh globally distinct outputs and exact binary gate tables. Topological semantic evaluation gives `a XOR x XOR y=0`, `b XOR a XOR y=0`, and `b=x` for **every** original valuation. It is **not** legal to use `a` or `b` as asserted TRUE simply because it is a named DEF output. A desired GF(2) derivation would take the two defining equations as exported row objects, XOR them to obtain `b XOR x=0`, then XOR with `x=1` to obtain `b=1`, and optionally LOCAL-convert to the clause `(b)`. The original native rule text does **not** specify the DEF-to-AFFINE export or the consumption of the auxiliary `b` as a LOCAL output. **Therefore the displayed nested construction is a semantically correct, separately paid countertest with an UNRESOLVED legal edge, NOT a certified legal full native proof.** It pinpoints which missing grammar rule must be checked rather than inventing it.

The structurally legal native prefix has 3 paid nodes (AND3 + DEF + DEF). A conditional completion with two authenticated defining-row ports would add 2 GF(2) row sums and, if authorized, 1 LOCAL-to-clause: 6 paid nodes in total, not 3; if port exports need extra paid nodes, charge them. The source is SAT, so any alleged contradiction in this chain would be an unsound export counterexample. A compact alternative is to represent the term `b=x` by sharing the already paid two DEF gates and a structural identity, not asserting `b` without provenance.

## Independent finite controls and fully charged costs

Python producer `experiments/arc/lspv2_406_entailed_support.py`: all 256 subsets of eight non-tautological unit/binary clauses on two variables. 95 `C` SAT, 161 `C` UNSAT. For all cases, source-entailment tests passed on 8,192 source-model input valuations. Essential-support histogram (3,4,5,6) = (161,1,20,74). 34,250 actual single-variable comparison probes, six malformed gate-record controls rejected, total 42,456 registered finite checks, no discrepancy. No random seed. Independent JavaScript bit-mask verifier `experiments/arc/lspv2_406_independent_verify.js` made 8,986 assertions, obtained the same 256 labels and histogram and checked the nested XOR identities. These finite checks corroborate the reduction, not its all-CNF quantifiers.

Let `N` denote **source encoded bits**, `E` supplied gate/proof evidence bits, `g` paid definitions, and `q` total logical nodes. The explicit family above has `N=O(n log(n+2))`, `g=O(|C|)` if all circuit gates are separately charged, and `E=O(|C| log(n+|C|+2))` under binary signed IDs. `q` need not dominate `E` unless the exact native serialization/charging rules guarantee it. The uniform reduction and circuit evaluation operate in polynomial bit time including parsing, token/access/index processing, writing, and validation. Exhaustive semantic support computation could cost `O(2^{n+4}E)`; **no superpolynomial lower bound on the time of all algorithms follows unconditionally** from coNP-hardness. A physical checker and normalizer must charge all provided bytes, intermediate circuit objects, source/proof indexing, annotation validation, consumers, output and simultaneous peak space, not just q. No FLMV resource bound is claimed.

## Established hard-family and B3 firewall

Haken's 1985 lower bound concerns **all ordinary shared-DAG Resolution refutations** of the **explicit unary PHP(h+1,h)** CNF with `h(h+1)` propositional variables, `m_h=(h+1)+h*binom(h+1,2)` clauses and `N_h=Theta(h^3 log(h+2))` signed-index bits: for some `c>0`, all sufficiently large h require `2^(c h)` ordinary Resolution lines. **No** GF(2), EXTENDED RES, DEF, AND3, LOCAL, mixed-rule or unrestricted machine lower bound is supplied. Cook's polynomial Extended Resolution PHP proofs and our exact affine Tseitin mixed optimum `4h-1` are mandatory countercontrols. Raz--Tzameret 2008 concerns a separately defined resolution-over-linear-equations proof system. No lower-bound transfer into our complete combined R is established.

B3 remains the **same-preselected-R** conditional:
```
SAT in P => exists C,k  forall N: Wbar_Rmix341(N) <= C (N+1)^k.
```
A polynomial-time decider alone yields an *algorithm*, not a short verified original-source R_mix341 refutation of every rejected input. A rejecting trace is compatible with an incorrect machine; making the trace into a sound UNSAT certificate requires a separately justified same-system correctness/reflection argument. Pich--Santhanam 2023 explicitly studies self-provability as additional structure. Neither B1 nor B2 nor B3 is proved or refuted here. **P versus NP OPEN.**

## Publication and next load-bearing test

New theorem is a strengthened **conditional grammar firewall**, not new hardness for the native calculus. Source-authenticated polynomial **structural** certificates may still be possible after a complete public-port contract; consumer-aware exact typed normalization is required (REFEREE351). Next: obtain authority for an exact serialized native LOCAL payload plus DEF-to-AFFINE exported-row policy, and either (i) build a consumer-aware compiler polynomial in `N+E`, then separately establish any `N+q` domination, or (ii) exhibit an accepted **native** counterexample. Independently, attack the noncircular same-R correctness/reflection step required for B3, not a mere restatement.

**Repository root main.tex:** authenticated `fetch_file` returned SHA `c4dfd0f6822668277bd18c64b69f56d71dff831f` but content length zero despite large expected size. Deliberately **not edited**; cannot safely preserve outside bytes or ownership markers from empty partial retrieval. No other role's region, prior artifact, task, schedule, enabled state or fixed R changed.

## References (primary)

[1] A. Haken, *The Intractability of Resolution*, Theoretical Computer Science 39 (1985), 297–308.

[2] S. A. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28–32.

[3] S. A. Cook and R. A. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf.

[4] R. Raz and I. Tzameret, *Resolution over Linear Equations and Multilinear Proofs*, Annals of Pure and Applied Logic 155(3) (2008), 194–224, https://doi.org/10.1016/j.apal.2008.04.001.

[5] D. Itsykson, A. Riazanov and P. Smirnov, *Tight Bounds for Tseitin Formulas*, SAT 2022, https://doi.org/10.4230/LIPIcs.SAT.2022.6 (regular Resolution / restricted OBDD).

[6] J. Pich and R. Santhanam, *Towards P != NP from Extended Frege Lower Bounds*, ECCC TR23-199 (2023), https://eccc.weizmann.ac.il/report/2023/199/.
