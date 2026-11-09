<!-- LSPV-5 REPORT::461::2026-11-09_0702_PST -->
# LSPV-5/461: finite-torsion pooling is annihilated by clause duplication

**2026-11-09 07:02 PST | Route B independent red team | PROVED/RESTRICTED symbolic lemma + COMPUTATIONAL controls | P versus NP OPEN**

**Material evidence node:** `[P2-L5-461]`, refining topology/representation control `[P2-L4-521]` and shortcut/normalization gap `[P2-C3]`. Historical grammar `[P2-D1]`, all-rule mixed lower bound `[P2-B1]`, and noncircular same-calculus B3 `[P2-B2]` remain OPEN. Route-A nodes `[P2-A2]`, `[P2-A4]`, `[P2-A5]` and P-chain `[P1-01]`, `[P1-03]`, `[P1-04]` remain OPEN.

## IDEA -> SEARCH -> ITERATE

### Initial idea and falsifiers

The run began by testing whether a current branching/shared-DAG claim leaked a branch-local lemma or omitted one AND child. The hypothesis was that a split on $x$ without a native source-authenticated discharge is either outside historical $R_{mix341}$ or unsound after reconvergence.

The fixed falsifiers were:

1. the historical grammar supplies a native split/discharge derivation with both children and scope checks;
2. an accepted-byte certificate discharges both $F,x\vdash\bot$ and $F,\neg x\vdash\bot$ without cross-branch leakage;
3. a legal fixed-calculus shortcut avoids the split; or
4. the current corpus already contains the exact scope/AND-join result.

Falsifier 4 fired. `[P2-L5-453]` already proves the restricted context-labelled AND-discharge/source-cover lemma and explicitly records that historical `/341` has no authenticated native split rule. Repeating it would add no evidence. Search then exposed the fresh doubled-clause mod-2 Magnus collision `[P2-L4-521]`. The revised target is the exact general finite-torsion obstruction below.

### Claim card

- **Claim:** every row-erased occurrence-additive fingerprint valued in an abelian group of finite exponent $q$ is annihilated by $q$-fold source-clause duplication.
- **Quantifiers:** for every CNF multiset $F$, every abelian group $A$ with $q a=0$ for all $a\in A$, and every row map $\phi$ from clauses to $A$.
- **Proof model:** ordinary shared-DAG Resolution only for the proof-size preservation clause; size is the number of derived Resolution inference nodes, not input bits or source-leaf occurrences.
- **SAME_REALIZATION:** $F$ and its occurrence-duplicated source $D_q(F)$ use the same variables and clause contents; only multiplicities change.
- **Falsifiers:** non-additive or row-indexed invariants; torsion-free integer coefficients; a proof measure charging repeated source occurrences; a calculus whose rules inspect multiplicity; or a reduction forbidding repeated clauses.

## Theorem 461.1 — torsion-pooling duplication firewall

Let $F$ be a CNF represented as a finite multiset of clause occurrences. For an integer $q\ge2$, let $D_q(F)$ contain exactly $q$ copies of each occurrence of $F$. Let $A$ be an abelian group of exponent dividing $q$, and let $\phi(C)\in A$ be any function of a clause occurrence after its row identity is erased. Define

$$
\Sigma_{A,\phi}(F)=\sum_{C\in\operatorname{occ}(F)}\phi(C).
$$

Then:

$$
\operatorname{SAT}(D_q(F))=\operatorname{SAT}(F),
\qquad
\Sigma_{A,\phi}(D_q(F))=0.
$$

If $\operatorname{ResInf}(F)$ denotes the minimum number of **derived** ordinary Resolution inference nodes in any shared acyclic refutation DAG, then for UNSAT $F$,

$$
\boxed{\operatorname{ResInf}(D_q(F))=\operatorname{ResInf}(F).}
$$

### Proof

Conjunction is idempotent, so repeating every clause preserves every satisfying assignment. For the fingerprint,

$$
\Sigma_{A,\phi}(D_q(F))
=\sum_{C\in\operatorname{occ}(F)}q\phi(C)=0.
$$

Every refutation of $F$ is a refutation of $D_q(F)$ because every original source clause is present, so $\operatorname{ResInf}(D_q(F))\le\operatorname{ResInf}(F)$. Conversely, take any refutation DAG of $D_q(F)$ and redirect each source-copy leaf to the corresponding clause of $F$. Every oriented Resolution inference has the same two clause contents, pivot and resolvent. The dependency graph remains acyclic, reconvergent subproofs remain shared, and no derived node is added. Hence $\operatorname{ResInf}(F)\le\operatorname{ResInf}(D_q(F))$. Equality follows.

This proof respects shared-DAG accounting: the union of distinct derived nodes is counted once. It does not double-count a shared subproof and does not introduce a case-split, weakening, discharge or semantic rule.

## Corollary 461.2 — established 3-CNF hard-family control

For a connected cubic graph $G$ with $H$ vertices, the canonical edge-variable Tseitin encoding has $3H/2$ variables and four proper width-three clauses per vertex. An even total charge is SAT; an odd total charge is UNSAT. On the published bounded-degree expander families, odd-charge formulas require $\exp(\Omega(H))$ ordinary shared-DAG Resolution size (Urquhart 1987; equivalently obtainable through the later width method at the proper scope).

Apply $D_q$ to both an even-charge and odd-charge source on the same graph. Both sources retain the same variables, occurrence count and fixed-width encoding length; both have zero row-erased $A$-pool; their SAT labels differ; and the odd formula retains exactly its original minimum number of derived ordinary Resolution inference nodes.

Therefore no classifier or universal lower-bound potential whose only semantic input is the dimensions and such a finite-torsion row-erased additive pool can distinguish the pair. This includes the mod-2 pool in `[P2-L4-521]` as $q=2$, and extends it to every fixed finite abelian target by choosing a multiple of its exponent.

### Scope firewall

The theorem does **not** attack:

- row-indexed fingerprints, which retain clause provenance;
- torsion-free integer Magnus coefficients;
- non-additive link invariants or invariants of the complete link diagram;
- source grammars that forbid duplicate clauses;
- proof measures charging source parsing/evidence bits rather than derived Resolution inferences;
- GF(2), extension, algebraic or LOCAL-CONVERT shortcuts in the full mixed calculus.

It is not a link-isotopy theorem and not a lower bound on arbitrary SAT algorithms. It is a representation countercontrol against a specific universalization pattern.

## Independent checks

The independently authored Python verifier generated canonical original edge-variable Tseitin 3-CNFs for K4, triangular prism, cube and Petersen graphs. It used even and one-odd charge vectors and $q\in\{2,3,5\}$.

- 12 graph/exponent configurations;
- 124 explicit assertions;
- even model counts $8,16,32,64$ and odd model count zero;
- both finite-torsion pools empty in every configuration;
- equal paired packet lengths;
- one-copy deletion and one-literal corruption controls nonzero;
- 2.716053 seconds host wall time and 9,344 KiB peak RSS.

These graphs are correctness controls, not asymptotic expander certificates. No Resolution optimizer, historical $R_{mix341}$ checker, link-isotopy checker, Lean build or SAT-universal machine was executed.

Peer replay was also performed from exact published blobs:

- LSPV-3/534 JavaScript blob `7115fe51d0b0cc7c26f10e32426d91c00da80de5`: 33 configurations, 24,564 truth inputs, 24,564 coefficient checks and 33 corruptions passed. Its unrestricted-size ANF depth theorem survives this audit but remains outside historical $R_{mix341}$.
- LSPV-1/535 Python blob `277f51b1aa07d0c44d7e851b982d1e0bbc8bebd9`: 560 checks, 64 parameter samples and 120 occurrence-budget controls passed. Its result remains a conditional guest-algorithm upper construction and analytic-envelope theorem, not a mixed-system lower bound.

## Family/theorem/encoding/method ledger

| Family | Exact encoding | Published theorem/model | Known shortcut | Remaining transfer |
|---|---|---|---|---|
| Odd Tseitin on bounded-degree expanders | one edge variable; four width-three parity clauses per cubic vertex; $D_q$ repeats each occurrence $q$ times | exponential ordinary DAG Resolution lower bound; derived-inference minimum preserved exactly by $D_q$ | Gaussian elimination/GF(2), stronger Frege/extension-style reasoning | no lower bound over every legal historical mixed rule |
| Even Tseitin on the same graph | identical grammar and size, even total charge | certified SAT with $2^{|E|-|V|+1}$ models | Gaussian elimination | easy paired label control only |
| KT clause-link reduction | published commutator clause components | polynomial decision reduction, not proof-size preservation | pairwise/mod-2 encodings and full diagram algorithms | no native rule-by-rule $R_{mix341}$ simulation |

Certified UNSAT/SAT labels, ordinary Resolution proof-size hardness, and empirical computation are kept separate.

## Search and corpus reconciliation

Read complete `proof1.txt` at starting blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and complete `proof2.txt` at starting blob `8999215be7e9828d88d02028433ebd75ab65523e`; current issue #3 through LSPV-4/521; governing 2026-11-02 handoff; current knot/link handoff; AGENTS.md, CODEX.md, skill and red-team mode/protocol; LSPV-1/535, LSPV-3/534, LSPV-4/521 and prior `[P2-L5-453]`; Grok `GROKPROOF/2026-11-09_1230_PROGRESS.md` blob `0ee19c6b2fdf92b64427ab737fe563346779c828`; Claude world-ledger README blob `de75a371ce3143a4495e6892df7fb04794a6b708`.

Primary sources inspected through full text or theorem-bearing primary pages: Koenig--Tsvietkova (2021) clause commutator reduction; Urquhart (1987) expander-Tseitin ordinary Resolution lower bound; Ben-Sasson--Wigderson width-size framework. The KT construction accepts a 3-SAT clause list and does not itself provide a lower-bound-preserving proof translation.

Change-aware repository review: `konard/p-vs-np` head `ecedd2d863245641c4ea6e87b0401b82761fa082`, `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3`; and CNFgen `tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`. Neither required P-vs-NP repository changed from the previous pinned review. A Google-branded interface was unavailable; general indexed web search was used and this limitation is explicit.

**Duplication/contradiction audit:** `[P2-L4-521]` proved only the $q=2$ Magnus-row instance. The finite-group exponent theorem and exact ordinary-Resolution inference-minimum preservation are the material additions. No contradiction was found in LSPV-1/535 or LSPV-3/534. Root `main.tex` blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` again returned zero content bytes, so no unsafe whole-document edit was attempted.

## Resource ledger and publication

Logical proof: symbolic, with no search cost hidden. Finite verifier costs separately include graph construction, source serialization, exhaustive model evaluation, pooling, corruption controls, hashing, JSON output and Python runtime. Code SHA256 `b13dd953c452bf13a6de4bffcbb0762bdc5fa83cad43dff9ec86a0a8c5199fd7`; raw SHA256 `57d104a8680b6f0dba8eb613b5b04108380ad0f8abff35dae5491fc12d686fc3`.

Artifacts:

- `experiments/review/lspv5_461_torsion_pooling_duplication.py`
- `results/raw/arc/2026-11-09_0702_LSPV5_461_TORSION_POOLING_RAW.json`
- this report
- `research/coordination/2026-11-09_0702_LSPV5_TORSION_POOLING_FIVE_ROLE_HANDOFF461.md`

Tracker update: `[P2-L5-461]` appended conflict-safely. Final `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; final `proof2.txt` blob `e12b483853cd8fa536bf9c899a2d2a64c6a95863`; complete 747,596-character readback, exactly one `[P2-L5-461]`, and complete prior-prefix preservation PASS.

## Status and next gap

**Actual advance:** exact finite-exponent generalization of the doubled-clause collision, plus an exact shared-DAG ordinary-Resolution inference-minimum preservation proof and independent finite controls.

**Precise remaining gap:** prove an original-source-authenticated invariant that survives every legal historical $R_{mix341}$ rule, sharing, extensions and algebraic shortcuts, or provide a full polynomial normalization into a restricted hard system; independently establish noncircular B3 for the same fixed calculus. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. P versus NP remains OPEN.

<!-- END_OF_VERIFIED_REPORT::LSPV-5::461 -->
