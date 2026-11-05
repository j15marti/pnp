<!-- LSPV-5 REPORT::REFEREE369::2026-11-05T12:48:00-08:00 -->
# LSPV-5 REFEREE369: owner-qualified branch-local DEF names alpha-normalize without unfolding

**November 5, 2026, 12:48 PST. Route B primary.** **PROVED/EXACT for the declared comparison grammar:** global uniqueness of the *printed* DEF alias is unnecessary. If every semantic definition output is the pair “paid owner node, output port,” all uses are owner-qualified, and a local output is visible only in contexts extending its owner's assumptions, then sibling branches may reuse the same cosmetic alias. An injective alpha-renaming of owners to globally fresh variables preserves the dependency DAG, distinct paid-node work, and critical-path span exactly and increases explicit evidence only polynomially. **KNOWN historical limit:** native `R_mix341` requires a fresh DEF variable and says later uses reference its paid node, but has no authenticated `ASSUME/MERGE` byte grammar. The tested trace is therefore not an authoritative native certificate and changes no historical rule or weight. Full LOCAL-CONVERT/exported-wire/AND3/GF(2)/DEF normalization, a superpolynomial full mixed minimum, B1/B2/B3, and P versus NP remain **OPEN**.

## IDEA fixed before SEARCH

**Initial hypothesis.** REFEREE368's rule “incompatible branches may not reuse an output identifier” is stronger than soundness requires. A lexical-scope repair should permit the same branch-local spelling when the semantic identifier carries an owner and cannot escape its assumption scope.

**Falsifiers fixed in advance.** (F1) two sibling owners with the same alias become ambiguous at a consumer; (F2) a branch-local output escapes through `MERGE`, Resolution, a factor, or an affine row; (F3) capture-avoiding alpha-renaming duplicates a shared/reconvergent DAG exponentially; (F4) owner qualification or renaming requires a semantic-equivalence oracle. Prediction: owner-qualified names compile once to globally fresh names with unchanged nodes and span; plain aliases or scope escape must reject.

## SEARCH and evidence that revised the claim

The governing five-role handoff, current issue #3 through LSPV-3/429, native `/341`, REFEREE368, LSPV-1/424, LSPV-3/429, current Grok and Claude files, and the required external repositories were read. The authoritative native description is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. It requires DEF to introduce one fresh variable and says later uses reference its charged node. This supports owner provenance, but does not specify serialized owner/port tokens, positional facet selection, exported/private wires, or branching discharge.

Actual literature queries were:

- `extended Frege extension variables local scope branch alpha renaming proof`
- `propositional proof systems extension variables eigenvariable condition sequent calculus branch`
- `Beyersdorff EF extra premises extension variables deduction theorem scoped`
- `Urquhart hard examples resolution Tseitin expander 3-CNF lower bound primary paper`
- `Ben-Sasson Wigderson Short Proofs Are Narrow Tseitin expander resolution 3-CNF primary`
- `site:github.com/openai extension variables proof complexity SAT certificate`

Direct Google-branded interactive access was unavailable, so Google is not claimed. Indexed primary-web search and authenticated GitHub search were used. Beyersdorff's ECCC TR06-142 and monograph formulation require an EF extension variable to be new relative to earlier formulas, the formula being abbreviated, and the final theorem. This is semantic freshness, not a prohibition on reusing an unbound printer label after alpha-conversion. The search therefore changed the hypothesis: *semantic owners* must be unique and conservative; cosmetic strings need not be. Beyersdorff also shows that broad weak deduction for EF is substantive and tied to optimality/complete disjoint NP-pair questions, so it cannot be inserted as a free B3 bridge.

Primary pages read:

- O. Beyersdorff, [ECCC TR06-142](https://eccc.weizmann.ac.il/eccc-reports/2006/TR06-142/index.html), weak deduction for EF.
- A. Urquhart, [Hard Examples for Resolution](https://doi.org/10.1145/7531.8928), JACM 34 (1987), 209--219.
- E. Ben-Sasson and A. Wigderson, [ECCC TR99-022](https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/), JACM 48 (2001), 149--169.

Change-aware repository review found unchanged heads: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`; `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; and `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`. Targeted searches for owner-scoped extension variables, branch discharge, and alpha-normalization returned no same-`R_mix341` theorem in either required new repository, OpenAI Math, FRAT-XOR, or short-proof. FRAT-XOR remains a useful typed-reference/checker precedent, not a proof of this theorem or B3. `GROKPROOF/2026-11-05_1913_PROGRESS.md` identifies certificate tooling but supplies no native normalization or bridge. `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` reinforces that an open lemma implying the target separation is a reformulation, not a completed bridge.

## Established family / theorem / encoding / known-method ledger

No new hard family was invented. The family used for the transfer ledger is the established cubic-expander odd-Tseitin 3-CNF. For a connected cubic graph $G=(V,E)$, $h=|V|$, and odd charge vector $\chi$, use one variable $x_e$ per edge. Each degree-three parity equation is encoded by the four width-three clauses excluding its four wrong-parity assignments. Thus there are $3h/2$ original variables, exactly $4h$ proper 3-clauses, and explicit binary/DIMACS length $N=\Theta(h\log h)$.

| Family / theorem | Exact model, rules, bound | Strongest known method admitted to the minimum | Remaining transfer |
|---|---|---|---|
| Urquhart; Ben-Sasson--Wigderson odd Tseitin expanders | Ordinary unrestricted shared-DAG Resolution on the stated clauses; $2^{\Omega(h)}$ lines for suitable expanders. No extension variables, AND3, or GF(2). | Resolution branching/learning and shared lemmas are already included. | Does not transfer to full mixed `R_mix341`. |
| Native `/341` bridgeless cubic odd Tseitin | Source clauses free; unit-cost at-most-binary RES, AND3, GF(2), LOCAL-CONVERT, paid fresh two-input DEF. Source-arity lower bound and affine construction give exact $W_R=4h-1$. | Three AND3 nodes per vertex extract each parity row; $h-1$ shared GF(2) sums derive $0=1$. | This is a linear upper-bound control, not a hard full-mixed family. Historical bytes/exports remain underspecified. |
| LSPV-1/424 restricted $X(K)$ compiler | Under fixed local extensional interfaces, globally fresh signed-AND2 DEF, and GF(2) row width $b$, $6d+3b+\log_2(4h+q+2)\ge\alpha h-O_K(1)$. | Known proof escapes through $b=\Omega(h)$; an ER compiler may escape through many paid definitions. | Restricted escape budget, not superpolynomial $q$ or all-native normalization. |
| LSPV-3/429 unique essential core | For connected cubic odd Tseitin, the individually indispensable clauses form the unique inclusion-minimal UNSAT original-clause core; $M(G)-1\le W_R\le4h-1$. | Same AND3/GF(2) proof. | Source ancestry remains only linear. |
| Haken unary PHP control | Exponential ordinary Resolution size in the standard PHP CNF; not exact 3-CNF. | Cook's Extended Resolution proof is polynomial. | Equisatisfiable 3-CNF conversion does not preserve the lower bound without a proved simulation direction and encoded-size overhead. |

The algebraic and extension shortcuts are evidence about the true minimum and are not excluded. None of these restricted lower bounds is an arbitrary-SAT-machine lower bound.

## Declared scoped-owner grammar

The exact comparison format uses strict DIMACS sources and judgements $\Gamma\vdash C$. Source literals have semantic names `x<i>`. Every paid DEF at record $u$ owns semantic output `d<u>`; its printed `alias` is cosmetic. A reference to a definition facet is the pair `(owner node, positional facet)`. The checker enforces:

1. `d<u>` is self-referenced only in node $u$'s exact defining facets; every later use names owner $u$ explicitly.
2. If DEF owner $u$ has context $\Gamma_u$, a consumer at $\Gamma$ may use `d<u>` only when $\Gamma_u\subseteq\Gamma$.
3. `MERGE` consumes both exact complementary contexts, the two conclusions are semantically identical clauses, and its conclusion contains only variables visible in the discharged context.
4. Resolution is oriented and parent contexts are subsets of the consumer context.
5. Aliases cannot occupy the `x<i>` or `d<u>` semantic namespaces.

This format is intentionally separate from historical `R_mix341`: `ASSUME/MERGE` are comparison rules, and no claim of authoritative byte acceptance is made.

## Scoped alpha-normalization theorem

**Theorem (PROVED/EXACT for the declared grammar).** Let $\pi$ be any finite accepted owner-qualified proof DAG with $q$ paid nodes, explicit evidence length $L$, and DEF-owner set $D$. There is a capture-avoiding translation to globally fresh DEF names with:

$$
q'=q,\qquad \operatorname{span}(\pi')=\operatorname{span}(\pi),\qquad
|\pi'|_{bits}=O\bigl(L+|D|\log(n+|D|)\bigr).
$$

The compiler runs in time polynomial in $L+q$ and uses no semantic-equivalence oracle.

**Proof.** Topologically enumerate the DEF owners and choose an injection $\alpha:D\to\{n+1,\ldots,n+|D|\}$. Replace every semantic literal `d<u>` by original-style variable $x_{\alpha(u)}$, including pivots and every positional facet. Replace each cosmetic alias by a unique printed name. The map is injective, so literal equality, complementation, exact clause identity, oriented Resolution, and truth-table satisfaction are preserved. Owner visibility was already checked before translation; no branch-local output appears after discharge. Parent identifiers, hyperedges, contexts, and node order are unchanged, so no branch or shared subproof is copied and both distinct-node work and weighted critical path are identical. Writing the map and renamed identifiers has the stated bit cost. This is syntactic alpha-conversion after scope checking, not global semantic normalization. $\square$

**Consequence for REFEREE368.** The unsafe seven-node trace remains rejected because it reuses a *source/split semantic variable* as a new output. REFEREE369 relaxes only cosmetic spelling. Conversely, if the trace format stores only the string `z` and omits its owner, sibling reuse is ambiguous and is rejected.

## Exact trace and independent replay

The validation source is the focused UNSAT control

$$
(p\lor q)\land(\neg p\lor q)\land\neg q.
$$

It is not proposed as a hard family. Under the $p$ and $\neg p$ branches, two distinct paid DEF owners both print alias `z`, each defines its own output as $q$, and each output is actually used through both defining facets before recovering $q$. `MERGE` discharges both branches; resolving with $\neg q$ yields contradiction. The owner identities are nodes 5 and 10. Alpha-compilation maps them to globally fresh variables 3 and 4.

Python production/checking and a separately written no-import JavaScript verifier agree:

| Quantity | Scoped trace | Globally alpha-renamed trace |
|---|---:|---:|
| Source models | 0 | 0 (same source) |
| Paid inference nodes | 12 | 12 |
| Ideal unit-weight span | 6 | 6 |
| Canonical bytes | 1,218 | 1,287 |
| SHA-256 | `bc8a62c1b53c0724ac49e704bf0544b1383ab0c2279d3f125a876685a8dd236b` | `d6bc98c2240033fd5228e182acf686d8a230c90b9bc81b1e08d707d43c2cb02d` |

Independent replay passed 3,165 assertions. Both implementations reject: sibling-owner capture; unqualified alias use; local-output escape through `MERGE`; omission of one required AND branch; a corrupt defining facet; use of a semantic namespace as an alias; and malformed DIMACS clause count.

Artifacts:

- `experiments/arc/lspv5_369/scoped_alpha_referee369.py`
- `experiments/arc/lspv5_369/verify_scoped_alpha_referee369.mjs`
- `experiments/arc/lspv5_369/scoped_alias_trace_referee369.json`
- `experiments/arc/lspv5_369/global_alpha_trace_referee369.json`
- `results/raw/arc/2026-11-05_1248_LSPV5_REFEREE369_raw.json`
- `results/raw/arc/2026-11-05_1248_LSPV5_REFEREE369_independent.json`

## Work, span, evidence, physical time, and space

The logical minimum intentionally does not charge discovery. For the actual validation run, the checker performed 3 source reads, 16 parent/facet reads, 14 context tests, 8 definition truth rows, and 36 recorded literal scans. The recorded Python host run took 3,546,519 ns and 11,008 KiB `ru_maxrss`; interpreter/runtime overhead is included. The independent JavaScript run is separately charged but not converted to a Turing-machine bound. The implementation materializes all records and both serialized traces. A production algorithm must additionally charge parsing, map construction, identifier lookup, certificate output, cache/storage, retrieval or recomputation, failed strategies, and all-phase peak space. Logical work 12, span 6, certificate bits, host runtime, and physical peak space are distinct measures.

No claim is made that alpha-renaming is free. It is polynomial and output-linear in the explicit evidence. No exponential intermediate representation is forbidden; none is needed for this translation.

## Implications and exact remaining gaps

1. **REFEREE368 repair narrowed.** Global semantic owner freshness remains mandatory; global uniqueness of cosmetic aliases is not. Owner-qualified sibling reuse is safe and alpha-normalizes without DAG unfolding.
2. **No native counterexample.** The positive trace is legal only in the declared branch comparison grammar. Historical `/341` lacks authenticated branch bytes, so this run neither accepts nor rejects a native certificate.
3. **No full mixed normalization.** The theorem handles name hygiene only. It does not authenticate LOCAL-CONVERT payloads, exported/private wire ownership, AND3 factor serialization, GF(2) row ports, DEF facet multiplicity, or their rule-by-rule source retraction.
4. **LSPV-1/424 unaffected.** Its $d$ counts semantic paid owners, not printed strings. Sibling alias reuse does not reduce $d$ or $b$ and offers no escape from its restricted inequality. Its strengthened-subclause and prior DEF-elimination steps still need independent all-size review before promotion beyond $X(K)$.
5. **B3 remains OPEN.** `SAT in P` supplies a uniform decider but not automatically short refutations in this same fixed calculus. Treating the decider's correctness as a trusted axiom is reflection; assuming polynomial proof certificates is the desired conclusion. Owner alpha-conversion is downstream syntax and supplies none of this missing implication.

## Corpus reconciliation and publication guard

**CORPUS REVIEWED:** governing handoff; issue #3; native `/341`; REFEREE368; LSPV-1/424; LSPV-3/429; current Grok and Claude files; relevant Urquhart, Ben-Sasson--Wigderson, and Beyersdorff sources; required repository heads listed above. **DUPLICATION / CONTRADICTION AUDIT:** generic alpha-conversion and extension freshness are known proof-theoretic principles; no novelty is claimed for them. The project-specific contribution is the exact owner-qualified branch trace, checker, and narrowed REF368 repair. **WHAT CHANGED RELATIVE TO ROOT MAIN:** only the comparison-grammar freshness condition is narrowed; all load-bearing mixed-normalization and B3 arrows remain OPEN. **ADOPTED:** native owner provenance, exact both-branch discharge, shared-DAG accounting. **REJECTED:** plain-alias semantic references, local-output escape, and any inference from this syntax lemma to mixed hardness or B3. **STALE/OVERSTATED CLAIM FOUND:** REFEREE368 condition 3 (“incompatible branches may not reuse an output identifier”) is correct only if “identifier” means semantic owner, not cosmetic alias.

No task identity, title, timezone, schedule, enabled state, historical rule, or weight was changed. No other role's manuscript region was edited. Root `main.tex` requires full byte-preserving retrieval before any write; if the connector does not provide the complete body it will remain untouched and this standalone report is the durable fallback.

**Next exact target:** authenticate the native paid DEF selector/facet/export bytes and test whether every accepted definition reference already carries an unambiguous paid owner/port. Then red-team LSPV-1/424's strengthened-subclause and signed-AND2 elimination compilers on all-size symbolic cases. Separately, a noncircular same-system B3 implication remains entirely missing. P versus NP remains **OPEN**.

<!-- END_OF_VERIFIED_REPORT::LSPV-5::REFEREE369 -->
