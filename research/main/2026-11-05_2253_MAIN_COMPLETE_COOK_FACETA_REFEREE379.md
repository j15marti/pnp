# REFEREE379: complete paid Cook suffix for strict-3 bit-PHP in FACET-A

**November 5, 2026, 22:53 PST. LSPV-5 Independent Proof Red Team, Route B.**

**Status. PROVED/EXACT, RESTRICTED to FACET-A378-v1:** the REFEREE378 strict-3 Braun bit-pigeonhole decoder can be continued through a fully explicit Cook extended-Resolution suffix to the empty clause. For $n=2^\ell$, $m=n+1$, and $M=n\binom{n+1}{2}$, the complete exhibited shared-DAG has paid union work

$$
W_{\mathrm{full}}=
M(4\ell-3)+(n+1)(2n\ell-9)
+\frac{n(n+1)(27n^2+11n-14)}{24}=O(n^4),
$$

and constructed critical-path span

$$
\operatorname{span}_{\mathrm{full}}
=\max\{n-1,4\ell-3\}+\frac{(n-1)(n+4)}2+2.
$$

Every Cook extension is implemented by two paid signed-AND2 definitions and three paid Resolution nodes; no weakening, substitution, split, discharge, semantic oracle, or answer axiom is used. **COMPUTATIONAL:** independent replay accepted complete declared-grammar traces for $\ell=2,3$ with 70,443 checks and rejected seven targeted corruptions. **CONDITIONAL:** under LSPV-3/440's proposed GATE-LOCAL grammar, replacing each owner facet by one paid LOCAL gives another polynomial proof. **OPEN:** neither proposed grammar has been authenticated as the exact historical native $R_{\mathrm{mix341}}$ byte language. No superpolynomial lower bound for the full mixed calculus, no B1/B2/B3 bridge, and no result on P versus NP follows.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

The initial repair hypothesis was: Cook's published extended-Resolution PHP construction can be compiled into the already declared FACET-A signed-AND2/Resolution interface without any extra structural rule. Its falsifiable prediction was a complete empty-clause DAG whose every antecedent is either an authenticated source, an owner-qualified defining facet, or a prior correctly oriented resolvent.

Precise falsifiers were:

1. Cook's stage relation needs a primitive other than fresh extension definitions and Resolution;
2. the reduction of $PHP_{k+1}^{k}$ to $PHP_k^{k-1}$ uses weakening, substitution, case discharge, or a missing AND branch;
3. a reused defining facet or PHP lemma lacks a source/owner dependency or leaks across an incompatible assumption context;
4. current LSPV-1/436 or LSPV-3/440 already provides complete accepted historical bytes or a legal counterexample to this compilation.

The literature search rejected falsifiers 1 and 2: Cook's relation is a Boolean extension equality, and its four clauses plus the stage clauses admit an explicit weakening-free Resolution derivation. Project inspection rejected falsifier 4: /436 supplies a compact-guard lower-bound candidate and /440 supplies a proposed local grammar only through the unary PHP premises. The independent dependency replay rejected falsifier 3 for the emitted FACET-A DAG. The claim was therefore narrowed to an exact upper bound in FACET-A, with historical acceptance left open.

## Continuity, primary sources, and repository search

Read the governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; current issue #3 through the current LSPV-1/436 chain; LSPV-1/436; LSPV-3/440 report/code/raw/handoff; REFEREE378; historical /341; and the actual Grok and Claude research files. The repository-local preflight script was executed. It correctly reported that this scratch runtime lacks the full checkout's root `main.tex`, `AGENTS.md`, `CODEX.md`, and packaged skill files. Those files were therefore read from the current GitHub repository, and the complete 1,744,703-character root manuscript was recovered through the contents endpoint rather than a partial large-file response.

Primary statements inspected:

- Stephen Cook, “A short proof of the pigeon hole principle using extended resolution,” *SIGACT News* 8(4), 1976, DOI 10.1145/1008335.1008338. This is the original polynomial ER shortcut control.
- Samuel Buss, “Quasipolynomial Size Proofs of the Propositional Pigeonhole Principle,” *Theoretical Computer Science* 576 (2015), pp. 72–89. Section 2 explicitly recalls the Cook--Reckhow inductive relation
  $$q^k_{i,j}\leftrightarrow q^{k+1}_{i,j}\vee(q^{k+1}_{i,k}\wedge q^{k+1}_{k+1,j})$$
  and the resulting polynomial extended-Frege proof.
- Kamil Braun, “An exponential lower bound for the bit pigeonhole principle in resolution over parities,” arXiv:2609.23015, Theorem 1.1. For $\ell\ge32$, $n=2^\ell$, DAG-like Res($\oplus$) refutations require more than $\exp(n/(32768\ell^2))$ lines. The system has affine clauses and semantic weakening but no extension axioms.

Direct Google-branded access was unavailable; indexed web search was used. Queries included “Cook extended resolution pigeonhole exact extension clauses,” “Cook Reckhow PHP stage q i j k,” “Buss 2015 quasipolynomial pigeonhole extension formula,” and “Braun bit pigeonhole Res XOR Theorem 1.1.”

Change-aware repository review pinned these heads:

| Repository | Head | Relevant result |
| --- | --- | --- |
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | Idea 28 recognizes Cook ER as a polynomial PHP shortcut and separates proof finding from proof existence; no full mixed lower bound or B3 theorem. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | Targeted ER/B3 search found no authenticated $R_{\mathrm{mix341}}$ interface or same-system B3 bridge. |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | Typed clause/XOR proof format, not an extension-definition or historical-/341 checker. |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | Verified LPR checking, not a Cook-extension producer. |
| `peitl/short-proof` | `2c524cfceecf68b56f51d23f6b63255b502856d3` | Bounded ordinary-Resolution minimization, not all-rule mixed minimization. |
| `MassimoLauria/cnfgen` | `24e6334eae1a3a7488bda1ce58cfa3d6beccaf24` | Reproducible unary PHP generator (`cnfgen php 5 4`), not a lower-bound transfer. |
| `marijnheule/drat-trim` | `2e3b2ba2f0433f41b43affc660f9aa615a0d28f3` | DRAT verification; targeted search found no native extension owner relation matching /341. |
| `berkeley-abc/abc` | `0d3399ae1b5cc05d97608603cbcb1fcf9a09c04d` | Circuit rewriting/equivalence is a shortcut/search control, not checkable source provenance for /341. |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | Formal SAT execution-cost work, not a same-$R$ proof-size bridge. |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | Claimed formal subexponential 3-SAT development; even at its stated scope it supplies neither polynomial SAT nor B3 for /341. |

Repository claims and successful builds are evidence about their declared artifacts, not proof of P versus NP.

## Established-family/theorem/encoding/shortcut ledger

| Family | Exact 3-CNF encoding and size parameter | Published hardness theorem/model | Known legal shortcut control | Remaining transfer |
| --- | --- | --- | --- | --- |
| Braun bit-PHP | Start with $m=n+1$, $n=2^\ell$, $m\ell$ bit variables and $M=n\binom m2$ width-$2\ell$ collision clauses. Replace each by the standard private chain of $2\ell-2$ proper 3-clauses and $2\ell-3$ fresh variables. | $>\exp(n/(32768\ell^2))$ lines for DAG-like Res($\oplus$), $\ell\ge32$; extension axioms excluded. | REFEREE378 decodes unary PHP premises; this report completes Cook's ER suffix in FACET-A. | Equisatisfiability does not preserve the Res($\oplus$) lower bound. Need a simulation/back-translation theorem surviving new chain and extension variables. |
| Unary $PHP_{n+1}^{n}$ | At-least-one clauses $\bigvee_{j<n}p_{i,j}$ and binary collision clauses $\neg p_{i,j}\vee\neg p_{i',j}$. Not 3-CNF when $n>3$. | Haken: exponential ordinary shared-DAG Resolution. | Cook: polynomial extended Resolution; compiled here without weakening. | Ordinary Resolution hardness does not imply mixed-calculus hardness. |
| Cubic odd Tseitin | One edge variable and four proper signed width-3 parity blockers per cubic vertex; $3h/2$ variables, $4h$ clauses. | Exponential ordinary Resolution on suitable expanders. | Historical semantic AND3/GF(2) derivation has $4h-1$ paid nodes. | Family is a mandatory negative control, not a full-mixed witness. |

“Certified UNSAT,” “certified lower bound in a named proof system,” and “empirical solver difficulty” are not interchangeable.

## Exact FACET-A source and precompiler

REFEREE378 defines the strict-3 Braun source. Every width-$2\ell$ collision clause is replaced by a private chain

$$
(l_1\vee l_2\vee z_1),
(\neg z_1\vee l_3\vee z_2),\ldots,
(\neg z_{2\ell-3}\vee l_{2\ell-1}\vee l_{2\ell}),
$$

and reconstructed in $2\ell-3$ paid Resolution nodes. FACET-A378-v1 permits free authenticated strict-3 sources, unit-paid globally fresh signed-AND2 owners with addressable defining facets, and unit-paid correctly oriented binary Resolution. The exact pre-PHP work is

$$
W_{\mathrm{pre}}=M(4\ell-3)+(n+1)(2n\ell-9),
\qquad
\operatorname{span}_{\mathrm{pre}}=\max\{n-1,4\ell-3\}.
$$

It produces all unary $PHP_{n+1}^{n}$ axioms with authenticated ancestry.

## Native signed-AND2 realization of one Cook extension

For the Cook relation

$$q=a\vee(b\wedge c),$$

introduce two globally fresh signed-AND2 owners

$$w=b\wedge c,\qquad r=\neg a\wedge\neg w,$$

and represent $q$ by the literal $\neg r$. The standard four extension clauses are derived as follows:

1. $q\vee\neg a$ is the direct $r$-owner facet $\neg r\vee\neg a$;
2. $q\vee\neg b\vee\neg c$ resolves $\neg r\vee\neg w$ with $w\vee\neg b\vee\neg c$;
3. $\neg q\vee a\vee b$ resolves $r\vee a\vee w$ with $\neg w\vee b$;
4. $\neg q\vee a\vee c$ resolves $r\vee a\vee w$ with $\neg w\vee c$.

Thus one Cook variable costs exactly two DEF nodes and three RES nodes beyond its owner facets. The three logical inputs are distinct underlying variables throughout Cook's construction, satisfying /440's nondegenerate distinct-input qualification. This realization is a candidate native derivation only after the historical owner/facet selectors are authenticated.

## Weakening-free stage derivation

At stage $k$ there are $k(k+1)$ Cook variables $q^k_{i,j}$ obtained from the $k+1$ stage. Each new at-least-one clause is derived by resolving the two relevant $(k+1)$-stage totality clauses through the extension clauses; the exact totality cost is $2(k+1)^2$ Resolution nodes.

For a fixed target hole and pair of target pigeons, the required collision clause is derived by a nine-Resolution template. The template expands both target literals through their four extension clauses, applies the available old collision clauses for all resulting old-pigeon/old-hole combinations, and eliminates the private conjunction literals. It uses every antecedent as an AND obligation and derives exactly the binary target collision clause; no superset clause or weakening step is accepted. There are

$$k\binom{k+1}{2}$$

such collision clauses at stage $k$, hence $9k\binom{k+1}{2}$ collision Resolution nodes. At the final $PHP_2^1$ stage, the two units and the collision clause yield the empty clause in two more Resolution nodes.

Summing stages $k=1,\ldots,n-1$ gives

$$
D_{\mathrm{Cook}}=2\sum_{k=1}^{n-1}k(k+1)=\frac{2(n-1)n(n+1)}3,
$$

and

$$
R_{\mathrm{Cook}}
=3\sum_{k=1}^{n-1}k(k+1)
+2\sum_{k=1}^{n-1}(k+1)^2
+9\sum_{k=1}^{n-1}k\binom{k+1}{2}+2.
$$

Therefore the exact suffix union work is

$$
\boxed{
C_{\mathrm{Cook}}(n)=D_{\mathrm{Cook}}+R_{\mathrm{Cook}}
=\frac{n(n+1)(27n^2+11n-14)}{24}.
}
$$

This is the cost of the exhibited DAG and proves $W_R(F)\le W_{\mathrm{full}}$ in FACET-A. It is not a claim that the displayed DAG is minimum.

## Shared-DAG semantics, work, and span

The dependency object is an acyclic directed hypergraph. Every multi-premise Resolution node is an AND obligation; alternative legal proofs are OR choices outside this particular exhibited proof. The proof uses no branch assumptions, so there is no case-discharge rule and no branch-local conclusion to leak. Each distinct inference node is charged once even when referenced by several later clauses. Owner facets retain their definition ancestry, and the verifier requires every paid node and source used by the final empty clause to lie in its backward slice.

Let $Q_k$ be maximum owner depth of stage-$k$ Cook variables, $C_k$ maximum collision depth, and $A_k$ maximum totality depth. With the REFEREE378 inputs,

$$
Q_k=\ell-1+2(n-k),\qquad
C_k=4\ell-3+4(n-k),
$$

and the stage totality recurrence is

$$A_k=\max\{A_{k+1},C_{k+1}\}+k+2.$$

After the first stage, $A$ dominates. Including the final two Resolution nodes yields

$$
\boxed{
\operatorname{span}_{\mathrm{full}}
=\max\{n-1,4\ell-3\}+\frac{(n-1)(n+4)}2+2.
}
$$

This span assumes unlimited parallel processors, unit latency per paid node, free already-authenticated source reads, and retained antecedents. It is not a realizable time or space schedule. A concrete checker must separately pay parsing, indexing, references, retrieval, retention/recomputation, output, and peak live state.

## GATE-LOCAL conditional and historical firewall

LSPV-3/440 proposes a GATE-LOCAL grammar in which each owner-qualified defining facet is reconstructed by one paid LOCAL node. The complete proof has

$$
D_{\mathrm{total}}=(n+1)(2n-4)+\frac{2(n-1)n(n+1)}3
$$

definitions. Replacing each of its three owner facets by one LOCAL node adds at most $3D_{\mathrm{total}}$, still polynomial. This is a conditional upper bound in a proposed calculus.

It does **not** show that historical $R_{\mathrm{mix341}}$ accepts these bytes. The remaining authentication obligations include the exact LOCAL-CONVERT record, export/private-wire selectors, definition ownership, global freshness, repeated-input/tautological facets, source/index/head binding, and exact historical weights. Semantic equivalence of a circuit relation is insufficient provenance.

## Reproducibility, controls, and resources

The Python producer imports the published REFEREE378 strict-3 source compiler and emits compact complete proof metadata. The independent Node verifier reconstructs every omitted clause/facet from typed records and checks:

- exact source DIMACS and source hash;
- strict-3 properness and header bounds;
- unique IDs, global freshness, and acyclic ownership;
- exact signed-AND2 facets and all four Cook clauses;
- correctly oriented pivots and exact non-tautological resolvents;
- every unary PHP stage, the final empty clause, exact node counts, and span;
- backward reachability of every paid node and every source from the final empty clause;
- SAT controls and seven hostile mutations.

| $\ell$ | strict-3 sources | source/final variables | base work | suffix DEF/RES | total work | span | final node |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | 80 | 50 / 110 | 235 | 40 / 345 | 620 | 19 | `E_R345` |
| 3 | 1,152 | 891 / 1,335 | 2,943 | 336 / 5,070 | 8,349 | 53 | `E_R5070` |

Independent replay executed 70,443 checks and rejected wrong pivot, nonfresh definition, wrong owner provenance, duplicate ID, source-hash corruption, an omitted collision obligation, and a false final clause. Two consecutive post-fix generations were byte-identical.

Resource ledger for the executed finite controls:

| Component | Charged observation |
| --- | --- |
| Logical nodes | 620 and 8,349 paid nodes; sources excluded exactly as FACET-A declares. |
| Explicit evidence | 741,690 bytes = 5,933,520 bits; result clauses/facets are compactly omitted only when deterministically reconstructed. |
| Producer | 12,381-byte source; 0.2605 host seconds; observed max RSS 20,168 KiB. |
| Independent verifier | 7,150-byte source; 0.1602 host seconds; cumulative child max RSS 78,164 KiB. |
| Parsing/index/head reads | Included in observed host execution; separately represented by the verifier's source table, owner table, node table, and dependency-depth map. |
| Construction/search | Deterministic construction only; no optimizer search, restarts, or failed policies. The ideal minimum still grants free after-the-fact proof choice. |
| Updating/conversion/output | JSON serialization and file output included in producer time; SHA-256 and full readback charged separately in publication checks. |
| Retrieval/recomputation | Checker reconstructs omitted facets/resolvents and retains indexed proof metadata; no claim of streaming space. |
| Peak simultaneous space | Host RSS values above include runtime overhead and are not FLMV same-machine exponents. |
| Exponential intermediate | None materialized. A truth-table expansion was neither assumed nor forbidden; the compact Cook circuit was used. |

Artifact SHA-256 values:

- producer: `3f0ac4fc9661738f9f91e67d23fc55b55522fed3a5e1896b4ecea8a89c2735a1`;
- independent verifier: `d6faaa373dbedeab50be74f73f28b991de8556242a4217498a1761affe9d5afd`;
- raw trace: `0a6b0b4bb3e1bb9e674513424ffd8e57e9478bf676eab9bec4624d98ba3cfcbc` (741,690 bytes).

These are independent declared-grammar checks, not execution of the authoritative historical checker.

## B3 audit

The new proof is a family-specific unconditional upper bound in FACET-A. It neither supplies nor refutes the noncircular implication

$$\mathrm{SAT}\in\mathrm P\Longrightarrow \overline W_{R_{\mathrm{mix341}}}(N)\le\operatorname{poly}(N).$$

Completeness, a verified checker, efficient verification, and Cook's short proof for one family do not compile an arbitrary polynomial SAT decider into this same fixed calculus. The missing rule-specific correctness/reflection theorem is unchanged. B1, B2, and B3 remain open and must not be conflated.

## Actual advance, verification status, and precise remaining gap

- **PROVED/EXACT, RESTRICTED FACET-A:** complete strict-3 bit-PHP refutation, exact work $W_{\mathrm{full}}$, and exact constructed span.
- **PROVED:** Cook's Boolean extension relation compiles to two signed-AND2 definitions plus three Resolution nodes; the stage proof is weakening-free.
- **COMPUTATIONAL:** complete $\ell=2,3$ empty-clause traces, 70,443 checks, seven hostile rejections, all-node backward-slice closure, and deterministic hashes.
- **CONDITIONAL:** polynomial GATE-LOCAL proof after paying three LOCAL facet nodes per definition.
- **FAMILY FAILURE FOR FULL-MIXED HARDNESS:** Braun's family has a polynomial shortcut whenever the proposed extension interface is legal; the published Res($\oplus$) lower bound does not cover it.
- **OPEN:** authenticate the exact historical /341 grammar and execute accepted native bytes; otherwise produce a legal historical rejection. For a lower bound, find an established 3-CNF family and invariant surviving every historical extension, GF(2), LOCAL, Resolution, sharing, temporary growth, and optimal proof choice. For B3, prove a same-system noncircular compiler/reflection theorem. P versus NP remains **OPEN**.
