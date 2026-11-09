# LSPV-5/465: finite paid-label budget ceiling for cost-sound proof abstractions

**2026-11-09 10:44 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proof-chain status.** This run proposes material node [P2-L5-465], refining still-OPEN [P2-C3] and [P2-B1], with historical transformer authentication still [P2-D1] OPEN. It gives an exact ceiling for the entire class of finite, history-separated, count-once paid-label abstractions introduced in [P2-L5-464]. It is broader than [P2-L3-538], which proves an $m-1$ ceiling for one source-partition-only domain. [P2-B2] remains a separate noncircular same-calculus B3 obligation. proof1.txt was reviewed; no proof1 node changed.

## IDEA: hypothesis and falsifiers before search

**Initial hypothesis.** If a goal-covering cost-sound may abstraction charges each distinguishable abstract paid label at most once, then its minimum refutation work cannot exceed the total charge of its available label universe. Hence polynomially many polynomial-charge labels cannot certify superpolynomial work, even if the occurrence DAG, branching structure, or abstract fixed-point search is elaborate.

Falsifiers stated before search:

1. a reachable abstract refutation can cost more than the sum of every available first-use label charge;
2. a complete finite-label abstraction with polynomially many polynomial-charge labels has superpolynomial abstract minimum work;
3. the proof silently omits a legal nonlinear, algebraic, extension, branching, reconvergent or shared-DAG derivation;
4. the live tracker already contains this exact general theorem rather than a narrower collision or source-partition result.

The search did not find (1), (2), or (4). Falsifier (3) becomes an explicit premise: **every** legal historical transformer and terminal goal must be covered. If a rule is unknown, its may transformer must be conservatively permissive. The theorem is invalid as a whole-calculus statement if a legal rule is omitted.

## Continuity and exact reads

Startup main head was `eaf4c45431de6b68d52e695e18fe1b5298f044c5`. Complete root files were read: proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2.txt blob `bccac71b425f0dcbe73fb57d2636bf330b159761`. The governing abstract-interpretation handoff was blob `8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b`; AGENTS.md `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`, CODEX.md `754999f50de93cdb693ed37bc8110d31e9e698ef`, and the project research instructions `b8df83a7b0b1428f349b0e02ce1387d979e8db7f` were read completely.

Current issue #3 was read through LSPV-3/538. Exact peer reports read were LSPV-1/540 blob `f0d869d7b7c6d315550c402e94b9fb80093912df`, LSPV-2/523 blob `5cf5c630d4060cda0d39d5e2e50a2b8b544f267f`, LSPV-3/538 blob `e530dcc4e15247b359d52720bfa90941ab4e12ad`, LSPV-4/522 blob `bfc4a48f25be4961f5ec9b423f27430c971e4b00`, and LSPV-5/464 blob `c1349a53398fd0e2b5a7102c2d4dd711894e20f3`. The original /341 semantic declaration was read at blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Actual Grok file `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex` blob `d06a2d56befc775660c34a59067b61f0a8c142a8` and Claude file `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67` were read. The requested guessed knot/link handoff filename was absent on current main; this absence is recorded rather than treated as a review.

## SEARCH: primary literature and repositories

Primary sources inspected:

- Cousot and Cousot's abstract-interpretation materials formalize soundness as coverage of concrete behaviors and distinguish finite abstract domains, MOP semantics, refinement and completion: https://www.di.ens.fr/~cousot/AI/ . This supports the coverage polarity, not the quantitative label-budget theorem by itself.
- D'Silva, Haller and Kroening, *Abstract Conflict Driven Learning*, POPL 2013, considers completely additive reductive functions on finite powerset lattices and combines over- and underapproximations: https://www.kroening.com/papers/popl2013.pdf . Its solver correctness is not an unrestricted proof-work lower bound.
- D'Silva, Haller and Kroening, *Abstract Satisfaction*, POPL 2014, represents logical reasoning by lattices, transformers, deduction, abduction, quantification and fixed points: https://www.kroening.com/papers/popl2014.pdf . It supplies a framework for refinement, not a free count-once cost theorem.
- Grädel, Grohe, Pago and Pakusa, *A Finite-Model-Theoretic View on Propositional Proof Complexity*, characterizes several **restricted** proof systems by fixed-point logics: https://arxiv.org/abs/1802.09377 . Its scope does not authenticate historical R_mix341 or transfer restricted lower bounds to all mixed rules.
- Haken 1985 and Urquhart 1987 remain ordinary-Resolution lower-bound controls; Cook Extended Resolution and the mixed Tseitin GF(2) shortcut remain mandatory counter-controls.

Change-aware repository review found no relevant head changes since the preceding run: `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c` (README blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, proof status `93b77ed3d8fe456f81c690035f45f07910a247f2`); `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, METHOD_INDEX blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, format blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3`; Cake LPR README blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; CNFgen Tseitin generator blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`; `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. These supply formats, generators, formalization techniques and scoped claim audits, not authority for the fixed historical grammar or a P-versus-NP result. Indexed public web search was available; no separately authenticated Google-branded interface or external proof-assistant replay was available.

## ITERATE: concrete and abstract domains

Fix one UNSAT source $F$ and the preselected sound, complete, effective weighted calculus $R$.

**Concrete domain.** A concrete partial proof state records the complete finite acyclic occurrence hypergraph, every native rule tag and premise hyperedge, conclusions, contexts, source IDs and hashes, exported/private wire ownership, paid definitions/facets, fresh identifiers, side evidence and the global set of paid native nodes. A completed concrete state is a source-authenticated refutation of $F$.

**Abstract domain.** An abstract state is

$$
(D^\#,H^\#),
$$

where $D^\#$ retains distinct occurrence vertices and dependency hyperedges and $H^\#\subseteq L_F$ is the set of already-paid labels from an abstract label universe $L_F$. A label may encode source identity, rule, conclusion, context, provenance, wire ownership and canonical auxiliary identity. Coarser choices are legal relaxations but may lose lower-bound strength.

The abstraction $\alpha$ maps every concrete occurrence to an abstract occurrence, retains every AND premise and legal reconvergence, and maps the concrete paid set to its abstract labels. The concretization $\gamma(D^\#,H^\#)$ is the set of concrete partial proofs represented by that state. The may direction is

$$
s\in\gamma(a)\quad\Longrightarrow\quad
t_R(s)\in\gamma(t_R^\#(a))
$$

for every relevant native rule $R$. SOURCE, oriented Resolution, AND3, GF(2), LOCAL-CONVERT, DEF/facets, reuse/reference, and any authenticated split/discharge rule each need their own transformer. Unknown historical semantics must be mapped to a permissive transformer, never omitted or invented.

Each first use of label $\ell$ has nonnegative abstract charge $\widehat w_F(\ell)$. Reuse is zero unless the historical calculus specifies a reference/application charge. Cost soundness requires the /464 fiber condition

$$
\widehat w_F(\ell)
\leq
\inf\{w_R(v):v\text{ is a legal fresh native node mapped to }\ell\}.
$$

## Finite paid-label budget theorem

**Theorem [P2-L5-465].** Assume:

1. $L_F$ is finite;
2. every legal concrete refutation $P$ has a goal-preserving abstract image $P^\#$;
3. abstract work is the sum of nonnegative first-use charges of distinct labels in $P^\#$;
4. the abstract charge is no greater than concrete native work.

Define

$$
B_F^\#=\sum_{\ell\in L_F}\widehat w_F(\ell).
$$

Then the abstract minimum satisfies

$$
W_R^\#(F)\leq B_F^\#.
$$

**Proof.** Completeness of $R$ gives at least one finite concrete refutation. Coverage gives a completed abstract image $P^\#$. Let $U(P^\#)\subseteq L_F$ be its used paid-label set. Count-once charging gives

$$
\operatorname{cost}(P^\#)
=\sum_{\ell\in U(P^\#)}\widehat w_F(\ell)
\leq\sum_{\ell\in L_F}\widehat w_F(\ell)
=B_F^\#.
$$

Minimizing over completed abstract proofs cannot increase this value. The proof treats $P^\#$ as one complete branching/reconvergent hypergraph: every AND premise is present, OR alternatives select one completed derivation, and a shared label is charged once. No path unfolding or discovery cost is used. QED.

**Corollary.** If for all sources of encoded length at most $N$,

$$
|L_F|\leq p(N)
\quad\text{and}\quad
\max_{\ell\in L_F}\widehat w_F(\ell)\leq q(N),
$$

then

$$
W_R^\#(F)\leq p(N)q(N).
$$

Consequently, a superpolynomial lower bound on the abstract minimum requires a superpolynomial total paid-label budget on infinitely many sizes. With fixed constant historical node weights, it requires superpolynomially many distinguishable paid labels. This is a necessary condition for this abstraction class, not a concrete R_mix341 lower bound.

**Sharpness.** An abstract AND goal that requires all $M$ distinct labels, with no alternate goal proof, has minimum exactly their total charge. Thus the ceiling cannot be improved using label cardinality and charges alone.

## Red-team boundaries

- An infinite or nonsummable label universe is outside the finite theorem. Arbitrarily fresh auxiliary IDs may create such a universe unless a sound canonical-renaming quotient is proved.
- Per-occurrence charging is a different model and can exceed the label budget, but it risks the shared-DAG overcharge shown in [P2-L5-464]. It needs an independent cost-nonincreasing simulation.
- A compact symbolic description of exponentially many labels does not imply exponential machine space or time. No representation lower bound follows without a separate access/computation theorem.
- Spurious abstract shortcuts lower $W_R^\#$ and are safe for the transfer direction but weaken the result. Removing one by CEGAR requires exact rule-specific nonapplicability while retaining every other legal rule.
- Abstract UNSAT, abstract goal nonreachability and failure of an analyzer to decide remain distinct claims. This theorem concerns the ceiling of a goal-reachable abstract proof-cost relaxation.
- Solver correctness in Abstract Satisfaction/ACDL does not prove [P2-B2]. B3 still needs a noncircular same-R simulation from every hypothetical polynomial SAT decider.

## Mandatory family and shortcut controls

| Family | Exact encoding and restricted theorem | Known shortcut/control | Consequence for /465 |
|---|---|---|---|
| Odd-charge cubic Tseitin on a qualifying connected expander | One edge variable; four proper signed 3-clauses per degree-three vertex; $n=3h/2$, $m=4h$, $N=\Theta(h\log h)$. Urquhart gives exponential ordinary shared-DAG Resolution length. | GF(2) elimination and the declared mixed $3h$ AND3 plus $h-1$ GF(2) certificate cost $4h-1$. | A source/row label universe of size $O(h)$ with fixed weights has only an $O(h)$ ceiling; it cannot transfer the Resolution exponential bound to the full mixed calculus. |
| Unary $PHP^{n+1}_n$ | Standard pigeon at-least-one and pairwise collision clauses; starts outside strict 3-CNF. Haken gives exponential ordinary Resolution size. | Cook Extended Resolution has polynomial proofs. | A polynomial original-source label budget cannot certify the Resolution exponential bound; derived-clause labels must grow or the abstraction stays coarse. ER must remain covered, and any 3-CNF conversion needs lower-bound preservation, not equisatisfiability. |
| Horn implication chain $H_n$ | Width-one/two CNF; exact $n$-node binary-Resolution proof in LSPV-2/523. | One RUP macro record derives empty after source unit propagation in a different calculus. | A rule tag/label budget that omits the genuine macro is not cost-sound; a macro label can sharply reduce the abstract ceiling. |

Compact mod-3 adders, nonlinear definitions, extension variables, affine rows, preprocessing, source-side tables and shared learned lemmas remain legal controls whenever native. The label universe must represent them or conservatively admit their effects.

## Independent computation

- `experiments/review/lspv5_465_finite_label_budget.py`, SHA-256 `12f49b0275267724d985dbe133cb969f1a00bc211dca4b6637196933190548f1`
- `experiments/review/verify_lspv5_465_finite_label_budget.mjs`, SHA-256 `6e6d93b922d223d307899f421d77164b45c39cab50ee358fecf7e1a1c631f967`
- `results/raw/arc/2026-11-09_1044_LSPV5_465_FINITE_LABEL_BUDGET_RAW.json`, SHA-256 `2472b7bb2a89f976258019fcceed6ebaf2dbacb4684bf5f0948a3c3eff54ed6c`

Both implementations independently checked 2,396,745 charge/subset cases, 346,944 occurrence-DAG/history cases with arbitrary multi-parent nodes, and 55,986 fiber-minimum quotient cases: 2,799,678 checks each, zero violations. A shared-diamond control cost 8 with paid history but 11 under tree unfolding, while its total label budget was 8. These finite checks validate the combinatorial implementation only; they do not execute the authoritative checker or optimize historical proofs.

## Logical and physical resources

The theorem bounds ideal distinct-label logical work. The finite experiments separately incurred enumeration, parsing, hashing, serialization and output. A realized analyzer must additionally charge source/index/head reads, transformer construction, abstraction/refinement, failed policies, caches, evidence storage, references, retrieval/recomputation, verification and simultaneous peak space. Exponentially many implicit labels may have compact representation, expensive enumeration, or both; /465 proves none of those physical alternatives. Discovery remains intentionally excluded from ideal $W_R$.

## Actual advance and precise remaining gap

**Actual advance.** [P2-L5-465] proves a general exact ceiling for finite history-separated count-once abstractions: their minimum cannot exceed total distinguishable paid-label budget. Thus a polynomial label budget cannot support the desired superpolynomial abstract minimum, regardless of branching, reconvergence, shared lemmas or fixed-point search.

**Precise remaining gap.** Historical rule authentication [P2-D1] remains OPEN. A complete all-rule occurrence/history abstraction with exact transformer coverage [P2-C3] remains OPEN. One must exhibit a family whose sound abstract label budget and legal-goal constraints force superpolynomial minimum work despite GF(2), ER, RUP-like macros, definitions and all other native shortcuts [P2-B1] OPEN. Noncircular same-R B3 [P2-B2] remains OPEN. P versus NP remains OPEN.
