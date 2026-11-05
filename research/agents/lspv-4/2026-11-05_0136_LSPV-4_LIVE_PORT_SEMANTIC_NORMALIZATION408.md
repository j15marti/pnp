# LSPV-4/408: bounded-live-export semantic compiler and resource audit

**November 5, 2026, 01:36 PST. STATUS: PROVED only for the declared typed semantic-port fragment, COMPUTATIONAL exact finite tests. Full native R_mix341 grammar and B3 OPEN. P versus NP OPEN.** Fixed rules/weights and all five tasks untouched.

## IDEA before search

Prediction: If a circuit-valued LOCAL node has syntactic transitive support in at most three ORIGINAL variables, and downstream q paid records make at most bq explicitly addressable bounded-arity private-wire selections, every LIVE selected port has a globally exact five-gate representation. An injective rename of the r<=bq external port names, with *all* signed consumers rewritten, preserves meaning and name identity. The old circuit may contain unbounded unused private gates. Falsifiers: an untracked fourth original input, aliasing two distinct named ports, conflating source-model truth with global truth, unpaid enormous input evidence, and illegal native exports.

## SEARCH and independent review

Read first `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; then current issue #3 and peers. Original fixed `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob c87acd11; `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` blob bbcdad9a; LSPV-3/414 native GF(2) counterexample, /415 root-only five-gate theorem, /416 sparse-index audit; LSPV-4/404 public-port semantics, /407 flat-DNF counterexample; LSPV-2/412 joint DEF projection and LSPV-5 REFEREE357 B3-p-optimality. Also read AGENTS.md, CODEX.md, actual `GROKPROOF/2026-11-05_1218_PROGRESS.md` and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`; neither resolves native exports or B3.

General-web queries: `Cook Reckhow 1979 relative efficiency propositional proof systems`; `Haken 1985 intractability resolution PHP`; `Cook 1976 Extended Resolution pigeonhole`; `Raz Tzameret 2008 resolution over linear equations`; `Bryant 1986 Boolean function DAG`; `Pich Santhanam 2023 EF lower bounds`. Read original institutional/publisher records of Cook-Reckhow, Raz-Tzameret and Bryant; full publisher content not always accessible. Direct Google-branded search unavailable, so general indexed web search used. Authenticated github.com/openai queries: `ExecCNFNodeSearchCosts`, `CookLevin`, `LRAT proof checker`, `LOCAL CONVERT exported wire`. Read complete `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` (135 lines); it is not a same-R proof compiler.

## ITERATE, exact restricted theorem

**Declared fragment `R_live3^sem`, NOT ratified as native.** LOCAL circuit payloads have at most three original-variable syntactic leaves. Consumers are explicitly typed semantic wire readers with bounded port selectors, sensitive only to exact Boolean values under ALL original valuations, stable named identity, signs, ordered duplicates and preserved downstream result records. *No separate paid DEF identities are merged*. If q consumer records have at most b references each, r<=bq distinct private ports are observable.

For each live port f(x1,x2,x3), evaluate the complete 8-row truth vector. Obtain two binary cofactors f0(x2,x3),f1(x2,x3). The identity

$$
f=f_0\oplus[x_1\land(f_0\oplus f_1)]
$$

uses five arbitrary two-input representation gates, preserving f on ALL 8 assignments. Retain distinct output IDs for syntactically distinct old ports even if functions coincide; globally rename all references injectively. This preserves every declared consumer by induction, but only if actual rules really permit such ports and depend only on the stipulated type/value/identity semantics. Five gates are *representation syntax within this declared semantic LOCAL*, not automatically five free native DEF operations. For native DEF they must each be paid and their legal exports established.

With q paid records, b constant and original N-bit input, and otherwise polynomially balanced typed fields, the compiled explicit evidence is polynomial(N+q), with at most 5bq internal representation gates. **This does not bound q by polynomial(N).** If the supplied original evidence has E bits, all E bits must be acquired and checked, including huge unused gate payload. A conservative buffered indexed bit-machine upper ledger is T=O((N+E+q+2)^4), all-phase S_peak=O((N+E+q+2)^2), including scanning, parsing, gate evaluation, global remapping, output, verification, index and source references. No sublinear-ρ or FLMV result; if E≥N and buffered, ρ≥1.

**Hostile native control:** LSPV-3/414 proves a legal six-paid-node AND3/LOCAL/XOR prefix where source-model-equal LOCAL replacements change the globally exact GF(2) annotation. Our premise demands global eight-row equality. REFEREE357 demonstrates two source-sound DEF-facet selector completions disagree on a two-node trace. Original /341 does NOT fix private LOCAL port export, DEF facet selection, GF(2) row selectors or payload charging, so **this restricted theorem is NOT a full native normalization theorem**. The requested native settlement is still OPEN.

## Verification and physical distinctions

Reproducibility archive contains `producer.py`, independent `independent.js`, original and normalized full 511-gate JSON fixtures, `summary.json`, expanded report, console outputs and SHA-256 manifest. Python produced five acyclic 16-function gate networks with L=15,31,127,511,1023, r=5,10,24,32,40 live ports, q=3,5,12,16,20 two-port consumers. Checked all eight assignments and signs/duplicate consumer refs; **1,784 recorded primitive comparisons**; both SAT and UNSAT sources and four malformed gates passed. Input/output bytes at L=1023: **16,977 / 4,387**; old port names up to 782 characters. Naive whole-network repeated evaluation cost 485,640 gate operations, **not** a universal lower bound. Independent Node referee on 511-gate case: **665 assertion groups PASS** over 8 rows, 32 ports, 16 consumer records, plus malformed names/gates. These are host semantic tests, NOT native proof checking or indexed-FLMV TM traces.

Haken (1985): every ordinary shared-DAG Resolution refutation of explicitly encoded unary PHP with h+1 pigeons and h holes, ~h³ clauses and N=Θ(h³log h) bits, requires 2^Ω(h) nodes. Cook (1976) ER and Raz-Tzameret (2008) Res(lin) compact proofs block transfer to stronger systems. Fixed mixed R has short odd-Tseitin GF(2) proofs. No inference is made to all-algorithm SAT hardness.

## Status / exact next obligation

1. **OPEN native grammar:** ratify actual serialized LOCAL public/private wire selector, separate paid DEF facet slots, AND3 support/GF(2) equation RHS and consumer permissions. Prove same-original-source consumer-preserving whole-proof polynomial translation, or give an accepted genuine native counterexample.
2. **OPEN noncircular B3:** SAT in P => worst-case minimum paid-node Wbar_Rmix341(N) is polynomial. REFEREE357 p-optimality equivalence for encoded proof bytes requires a separate polynomial byte-versus-q normalization and does not prove same-R p-optimality.

B1/B2/B3, mixed superpolynomial minimum and P versus NP remain OPEN. No role, task, schedule, weights or rules changed.

### References
[1] Cook & Reckhow (1979), JSL 44:36-50. [2] Haken (1985), TCS 39:297-308. [3] Cook (1976), SIGACT News 8(4):28-32. [4] Raz & Tzameret (2008), APAL 155:194-224. [5] Bryant (1986), IEEE TC 35:677-691. [6] Pich & Santhanam (2023), ECCC TR23-199.
