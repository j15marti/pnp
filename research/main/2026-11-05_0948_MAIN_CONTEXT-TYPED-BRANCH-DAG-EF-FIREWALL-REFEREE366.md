# LSPV-5 REFEREE366: context-typed branch DAGs, shared reasoning, and the EF firewall

**November 5, 2026, 09:48 PST. Route B primary.**  **PROVED/EXACT** for the explicitly declared context-typed branch-DAG extension below; **FALSIFIED/RETIRED** for context-erasing cross-branch sharing; **COMPUTATIONAL** for the accepted 2,124-byte fixture and independent replay. Historical native `R_mix341` grammar, a full native normalizer, a superpolynomial full-mixed minimum, B1/B2/B3, and P versus NP remain **OPEN**. No historical rule or weight is changed.

## IDEA stated before SEARCH

**Hypothesis.** Branching and shared reasoning can be added soundly only if each derived clause is typed by its live assumption context. A node derived under context $\Gamma$ may be consumed under a stronger context $\Delta\supseteq\Gamma$, and opposite branches may be merged only by explicitly discharging one complementary split literal. Under those conditions the whole DAG has a polynomial Extended-Frege translation. If contexts are erased, the checker accepts a false refutation of a satisfiable source.

**Falsifiers fixed in advance.** (F1) reuse an assumption-dependent node in a weaker or incomparable context; (F2) merge two noncomplementary branches; (F3) obtain a stronger system than EF because DAG sharing causes exponential duplication; (F4) smuggle branch assumptions or cubes at zero cost. Prediction: F1/F2 are rejected, sharing is retained nodewise with polynomial evidence, and every `ASSUME` and `MERGE` is paid.

## SEARCH: governing record, peers, external reviews, literature, and code

Read the governing handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3 through LSPV-1/422, LSPV-3/426 and LSPV-4/417, original `/341`, REFEREE365, AGENTS/CODEX and the repository research protocol. Root `main.tex` again returned blob `1b8a7d9a1514b06c96501849a7902b7aa3dae2a1` with **zero readable content**, so no root edit was attempted.

Current peers materially changed the initial formulation. LSPV-3/426 proves that a noninjective variable quotient need not commute with exact oriented Resolution and that unrestricted weakening is absent from historical `/341`. LSPV-1/422 proves a one-export-bit global projection barrier but explicitly concedes that it is not a legal historical LOCAL-CONVERT. LSPV-2/398 already gave a guarded branch-discharge lemma for a declared RES+AND2 fragment. This run therefore does **not** claim branch discharge as novel; its increment is the explicit context type system, minimal context-erasure exploit, shared reconvergent accepted trace, and exact EF simulation boundary.

Actual external assessments read: `GROKPROOF/2026-11-05_1428_PROGRESS.md` at repository head `1de75a413d579be544dfdbe7d0901fd16778a5fe` (Route A remains open and supplies no B3 translator), and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` (a conditional world ledger, not a native proof compiler).

Required repository delta review:

| Repository/path | Pinned head/path | Finding |
|---|---|---|
| `konard/p-vs-np` | head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `proofs/complexity/README.md` | Explicit finite-machine P/NP model; expressly no theorem equating it with every machine model and no Rmix/B3 bridge. Unchanged from REFEREE365. |
| `blkph0x/p-vs-np-proof-research` | head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md`, `proof_producing_cdcl_lab/cdcl.py` | The method ledger scopes every result; the readable CDCL engine records Resolution derivations and treats decision assignments as search state, not free global proof premises. Unchanged head. |
| `meelgroup/frat-xor` | head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `format.md` | Separate typed clause/XOR identifiers and explicit premise IDs support the provenance discipline; the format is not historical Rmix. |
| `marijnheule/drat-trim` | head `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; `README.md` | Additions are checked against the current formula; DRAT is stronger than Resolution and is described as a generalization of ER. It does not license branch-context erasure. |
| `openai/math` | head `4eaee87548250b2682affda7d05d947c05554bae` | Targeted SAT/proof-trace/assumption search found no Rmix grammar or B3 result. Code is not a mathematical transfer theorem. |

Primary searches actually run: `Beame Kautz Sabharwal clause learning resolution simulation`; `Pipatsrisawat Darwiche clause learning resolution engines`; `Cook Reckhow relative efficiency propositional proof systems`; `Haken intractability of resolution pigeonhole`. The papers say, respectively, that specified clause-learning/restart models simulate Resolution, that practical CDCL variants p-simulate general Resolution, that propositional proof-system p-simulation is the relevant proof-length notion, and that PHP is exponentially hard for ordinary Resolution while ER is a shortcut control. None states a same-fixed-`Rmix341` B3 implication. Direct Google-branded search was unavailable; indexed web and authenticated GitHub were used, and no Google access is claimed.

## ITERATE I: declared grammar and exact soundness theorem

A judgement is $\Gamma\vdash C$, where $\Gamma$ is a consistent finite set of signed assumption literals and $C$ is a canonical clause. Every distinct inference node is paid; source references are free only after exact source-byte authentication.

1. `SRC`: for an original source clause $C$, $\varnothing\vdash C$.
2. `ASSUME`: if $\ell\in\Gamma$, infer $\Gamma\vdash(\ell)$. This node is paid.
3. `RES`: from $\Gamma_1\vdash A\vee p$ and $\Gamma_2\vdash B\vee\neg p$, under a node context $\Delta\supseteq\Gamma_1\cup\Gamma_2$, infer the **exact oriented resolvent** $\Delta\vdash A\vee B$. This node is paid; tautological stored resolvents are rejected.
4. `MERGE`: from $\Gamma\cup\{x\}\vdash C$ and $\Gamma\cup\{\neg x\}\vdash C$, infer $\Gamma\vdash C$. Both child contexts must be exact complementary extensions and the child clauses identical. This node is paid.

**Theorem 1 (soundness, PROVED/EXACT).** Every accepted judgement satisfies $F\land\Gamma\models C$.

**Proof.** `SRC` and `ASSUME` are immediate. `RES` is ordinary sound Resolution, and strengthening the assumptions from either parent context to $\Delta$ preserves entailment. For `MERGE`, every valuation satisfying $F\land\Gamma$ sets $x$ either true or false and therefore satisfies one child premise, hence $C$. Induction in dense node order proves the theorem. Exact source bytes and parent IDs prevent external-premise substitution. $\square$

## ITERATE II: polynomial translation that preserves sharing

Encode a judgement by the propositional formula

$$
J(\Gamma,C)=\left(\bigwedge_{\ell\in\Gamma}\ell\right)\to\left(\bigvee C\right),
$$

equivalently the guarded clause $\neg\Gamma\vee C$. For `SRC`, EF derives the weakening of the source clause. For `ASSUME`, $J$ is a tautology. For `RES`, a fixed Frege tautology schema combines the two parent implications after adding the missing guards. For `MERGE`, the fixed case-split schema

$$
((\Gamma\land x)\to C)\land((\Gamma\land\neg x)\to C)\to(\Gamma\to C)
$$

discharges the split. Substitution into these fixed schemas has proof size polynomial in the displayed formulas. Each proof-DAG node is translated once and may be cited by all consumers, so sharing is not unfolded into a tree.

**Theorem 2 (EF simulation, PROVED/EXACT).** Let $L$ be the explicit source bytes plus the sum, over all nodes and edges, of encoded identifiers, contexts, clauses, rule tags and pivots. There is one uniform source-authenticated compiler producing an EF refutation of size $\operatorname{poly}(L)$. The direct macro ledger is $O(\sum_v(1+|\Gamma_v|+|C_v|)+|E|\log |V|)$; identifiers, parsing and output bits are included.

This target is deliberately EF, not bare historical Resolution. Pretending that guarded-clause weakening is a free native RES step would contradict the exact-rule warning in LSPV-3/426. Under the separately proposed CANON2R completion, REFEREE365 already supplies EF/CANON2R p-equivalence, so adding this typed branch layer does not cross the EF boundary. It says nothing about historical `/341` until its missing facet/export selectors are authenticated.

## Minimal counterexample to context erasure

Take the satisfiable empty CNF over one variable $x$. A context-erasing checker accepts these three paid nodes:

1. under context $\{x\}$, `ASSUME` derives $(x)$;
2. under context $\{\neg x\}$, `ASSUME` derives $(\neg x)$;
3. at empty context, naively resolve them to the empty clause.

The typed checker rejects node 3 because neither parent context is a subset of the empty consumer context. Within this declared grammar the witness is arity-minimal: no assumption produces the empty clause, and a binary consumer needs two earlier opposite assumption leaves. This is a checker/normalizer counterexample, **not** a legal historical Rmix refutation because `/341` has no `ASSUME` or `MERGE` rule.

## Accepted shared-DAG fixture and hostile controls

The 63-byte source is

```text
p cnf 5 6
1 2 0
-1 2 0
-2 3 4 0
-2 3 -4 0
-2 -3 5 0
-2 -3 -5 0
```

The first two clauses yield the shared clause `(2)`, used in both $x_3$ branches. Under $\neg x_3$, the next pair yields both $(4)$ and $(-4)$; under $x_3$, the last pair yields both $(5)$ and $(-5)$. Each branch derives empty, and one paid `MERGE` discharges $x_3$. The exact trace has 20 nodes: 6 authenticated source references and 14 paid nodes (11 RES, 2 ASSUME, 1 MERGE). It is 2,124 bytes / 16,992 evidence bits, SHA-256 `b434b3088185a92bfd8d9ae8d458dfeb2304a0b02f4cea050ce79047568eb318`.

The Python checker performed 6 source reads, 24 parent-reference reads, 22 context-subset tests, 43 stored literal scans and 640 exhaustive node/valuation semantic checks. Its conditional-clause representation has 39 literal occurrences and the deliberately conservative EF macro ledger is 218 units. The measured producer/check run was 3.26 ms with 10,624 KiB process peak RSS; these are implementation measurements, not SAT runtime and not proof-search cost. The separately structured Node replay imported no checker code and passed 229 assertions, rechecking all 640 valuations, 24 parent references, byte hash and paid count.

Rejected controls: wrong split, weaker-context reuse, inconsistent context, corrupt resolvent, malformed DIMACS clause count, duplicate JSON key, and a source-bound trace replayed on an opposite-label SAT mutation. The SAT mutation has witness mask 22, variables 2,3,5 true. The unsafe checker accepted the three-node empty-source exploit; the proper checker rejected it.

Artifacts:

- `experiments/arc/lspv5_366/branch_context_dag_referee366.py`
- `experiments/arc/lspv5_366/verify_branch_context_referee366.js`
- `experiments/arc/lspv5_366/branch_shared_trace_referee366.json`
- `results/raw/arc/2026-11-05_0948_LSPV5_REFEREE366_raw.json`
- `results/raw/arc/2026-11-05_0948_LSPV5_REFEREE366_independent.json`

No authoritative native checker was executed. The exact bytes are accepted only by the two declared independent REFEREE366 implementations.

## Consequences for lower bounds and B3

1. **No new mixed lower bound.** Haken's theorem still quantifies over ordinary shared-DAG Resolution, not this branch system, EF, ER, GF(2), CANON2R, historical full Rmix or SAT machines. Cook's short ER PHP proofs and Gaussian-elimination Tseitin proofs remain mandatory shortcuts.
2. **No noncircular B3.** The compiler proves `typed branch proof -> EF proof`. It does not prove that SAT in P gives short EF proofs or short typed branch proofs. Combining it with REFEREE365 leaves exactly the open implication $P=NP\Rightarrow$ EF is polynomially bounded. Treating a decider's branches as proof nodes without the typed assumptions and discharge rules recreates the three-node unsoundness witness.
3. **Historical grammar still blocks transfer.** The accepted fixture contains no LOCAL-CONVERT, exported/private wire, AND3, GF(2), or paid DEF bytes. It neither repairs nor counterexamples their historical serialization. It only settles how any proposed branching wrapper must type and pay its additional rules.
4. **Physical work remains separate.** Logical node count does not charge branch discovery, source parsing, policy search, construction, bit access, verifier time, output or peak space. Conversely, those costs do not invalidate a lower bound on the best legal DAG. They are separate ledgers.

## Precise remaining gap

Authenticate actual historical `/341` selector bytes for DEF facets, exported wires, LOCAL-CONVERT and GF(2), then replay an LSPV-1/3 proposed certificate with its exact source and cost. For B3, one still needs a noncircular theorem that a polynomial SAT decider implies polynomial EF/CANON2R (and then historical Rmix) refutations, without assuming correctness reflection or polynomial certificates. This run proves that generic branch-and-share syntax does not supply that missing arrow.

## References

- P. Beame, H. Kautz, A. Sabharwal, *Towards Understanding and Harnessing the Potential of Clause Learning*, JAIR 22 (2004), 319–351, DOI 10.1613/jair.1410.
- K. Pipatsrisawat, A. Darwiche, *On the Power of Clause-Learning SAT Solvers as Resolution Engines*, Artificial Intelligence 175 (2011), 512–525.
- S. Cook, R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50.
- A. Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308.
- S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28–32.

**Publication guard.** No task identity, title, timezone, schedule, enabled state, rule or weight was modified. No other role's manuscript region was edited. P versus NP remains **OPEN**.
