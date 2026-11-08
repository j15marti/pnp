# LSPV-2/491: Component-width repairs the satisfiable-Tseitin read-once transfer
**2026-11-08 04:21 PST | Route A | KNOWN THEOREM (Itsykson et al. 2021) + PROVED/RESTRICTED (composition) + COMPUTATIONAL (finite controls). P versus NP OPEN.**

**Exact proof-chain nodes:** [P2-A2], [P2-A4], [P2-A5], and companion [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Stronger restricted evidence is relevant to [P2-A4]; all load-bearing universal Route A/B nodes remain OPEN. Historical `R_mix341` untouched.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** The earlier LSPV-2/490 bound `q(u+O(1)) >= 2^{Omega(H^delta)}` for pointwise OR of syntactic read-once child programs over satisfiable cubic Tseitin functions is quantitatively improvable using an independently published characterization of *component width*.

**Four predeclared falsifiers:** (F1) the stronger 2021 theorem bounds regular Resolution only, not syntactic nondeterministic read-once programs; (F2) it imposes the 2017 spectral `|lambda_2| < d/3` restriction, inapplicable to cubic graphs; (F3) existential child variables or OR sharing violate the read-once projection/composition; (F4) a read-twice or algebraic shortcut invalidates any claimed general-machine interpretation. Search resolved F1 and F2 against ECCC TR19-178 Theorems 13, 41 and 52 (both FALSE); F3 is FALSE only with the explicitly stated **syntactic read-once on all original and private variables** requirement; F4 is TRUE and forces the theorem to remain restricted.

**Literature correction:** LSPV-2/490 relied on Glinskih–Itsykson 2019/2021 and obtained only exponent `H^delta`, `0<delta<1/36`. Itsykson, Riazanov, Sagunov and Smirnov, *Almost Tight Lower Bounds on Regular Resolution Refutations of Tseitin Formulas for All Constant-Degree Graphs*, ECCC TR19-178 (2019), Theorem 41, prove `size(1-NBP for satisfiable T(G,c)) >= 2^{compw(G)}`; Theorem 52 proves `compw(G) >= (tw(G)-1)/2`. The refereed 2021 version is *Near-Optimal Lower Bounds on Regular Resolution Refutations of Tseitin Formulas for All Constant-Degree Graphs*, `Computational Complexity` 30:13, DOI `10.1007/s00037-021-00213-2`. This stronger source supersedes the **quantitative restricted** result /490, not its warnings.

## Authenticated original strict 3-CNF family

Let `G=(V,E)` be a connected simple cubic graph, `H=|V|`, `M=3H/2`; one original Boolean variable `x_e` per edge. For each vertex `v`, order its three edges `a<b<c`, choose charge `b_v`, and insert precisely four clauses

$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus b_v}(x_c),\qquad(p,q)\in\{0,1\}^2,
$$

with `ell_0(x)=x`, `ell_1(x)=not x`. This forbids exactly the odd/even assignments violating `x_a xor x_b xor x_c = b_v`. There are exactly `4H` strictly proper signed ternary source clauses. Dense DIMACS with the natural variable numbering has encoded bits `N=Theta(H log(H+2))`. Connected even-total-charge instances are SAT, and odd-total-charge instances UNSAT, by summing parity equations. **No Tseitin-to-3CNF reduction is needed**, hence no unsupported preservation direction is invoked.

For an established family of constant-degree edge-expanding connected cubic graphs, `tw(G)=Omega(H)`. These are hard in specified Resolution and 1-NBP representation models, **not** hard against arbitrary SAT deciders.

## Revised restricted theorem and derivation

Assume for each such *satisfiable* even-charge original Tseitin **Boolean function** `f_G(x)` there is the pointwise identity

$$
f_G(x)=\bigvee_{i=1}^{q}\exists y_i\;g_i(x,y_i)
$$

and each `g_i` has a **syntactic nondeterministic read-once branching program over all x and y_i variables**, with at most `u` nodes. No universal SAT oracle, proof checker, or algebraic extension is included in this model.

Replace private `y_i` queries by nondeterministic epsilon choices. Because every original/private variable appears at most once on each source-to-sink path, this preserves exactly the existential projection and remains syntactic read-once over `x`. Take the nondeterministic OR of the `q` projected programs with one shared starting choice. With an explicit safe per-child overhead constant of 3 nodes, the result has at most `1+q(u+3)` nodes. The 2021 Theorems 41 and 52 give

$$
1+q(u+3)\ \ge\ 2^{\mathrm{compw}(G)}\ \ge\ 2^{(\mathrm{tw}(G)-1)/2}.
$$

Hence on the cubic-expander sequence,

$$
q(u+3)\ge 2^{\Omega(H)}=2^{\Omega(N/\log N)}.
$$

**This is strictly stronger than /490's `2^{Omega(H^delta)}` bound, but ONLY for pointwise Boolean-function representation by OR of syntactic 1-NBP child programs.** It does not imply lower bounds on the size of child CNFs, on a general machine executing SAT queries, on arbitrary shared proof DAGs, or on decision-only algorithms.

The published paper explicitly permits the known **read-twice** small-program escape. A deterministic program can test each cubic parity packet in sequence with at most five query nodes per vertex plus two sinks, querying each edge at most twice because it meets two endpoints, so size `<=5H+2`. Moreover, componentwise XOR of vertex charges decides satisfiability; source parsing, component discovery, and actual machine resources remain charged when implemented. These are legal upper-bound controls, not exclusions.

## Independent finite reproducibility controls (not asymptotic verification)

The Python reference exhaustively evaluates even/odd original clauses on K4, triangular prism, cube and Petersen, independently computes every edge-subset connectivity count and the exact minimax component width by subset dynamic programming, and checks cofactor truth-set signatures on the chosen minimax prefix. A separate JavaScript implementation uses graph BFS rather than Python's union-find and reimplements the minimax computation. Both use expensive host-language memory; neither is an implementation of Reingold's logspace connectivity nor an FLMV-machine resource bound.

| Original graph | H | M | strict clauses | even-charge satisfying assignments | exact component width | 1-NBP lower, nodes |
|---|---:|---:|---:|---:|---:|---:|
| K4 | 4 | 6 | 16 | 8 | 2 | 4 |
| Triangular prism | 6 | 9 | 24 | 16 | 2 | 4 |
| Cube | 8 | 12 | 32 | 32 | 3 | 8 |
| Petersen | 10 | 15 | 40 | 64 | 4 | 16 |

Odd-charge sources are UNSAT for each. Python **37,562** asserted controls, including rejected flipped-sign, missing-clause, duplicated-clause and zero-literal packets. Independently written JavaScript **75,050** assertions, including flipped-sign, missing, duplicate controls. The exact minimax computation covers `2^6+2^9+2^12+2^15=37,440` edge subsets; it is a finite component-width optimum, **not** a minimum over all SAT algorithms or all (R_{mix341}) proofs.

**Resource ledger:** the physical Python/Node verifiers materialize up to `2^15=32768` subset width/DP states; SAT enumeration visits up to `2^15` full assignments. This consumes `Theta(2^M)` host writable memory and `O((H+M)2^M+M2^M)` arithmetic steps for connectivity/DP, plus exhaustive SAT evaluation. The 1-NBP bound concerns *logical representation nodes*, not proof-search cost, work-span, certificate bits or FLMV peak space. No native FLMV instruction-level trace; no authoritative historic `R_mix341` checker. All-encoded-input parsing, same-machine translation, restart/cache/read costs, and recursive applicability remain unproved.

## Continuity and source review

Project: complete root `proof1.txt` and `proof2.txt`, governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, current issue #3 (latest LSPV-1/501, LSPV-3/498, LSPV-4/492, LSPV-5/432), LSPV-2/490, actual `GROKPROOF/2026-11-06_2316_PROGRESS.md` and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`. Code search for exact `compw` in project returned no hits, but absence is not a novelty proof. This review did not rewrite another role's report.

External inspected paths/blobs: `konard/p-vs-np:scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research:METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `INDEPENDENT_AUDIT.md` `b30515cced93d8911a6415555ee9ec1444502d93`; `MassimoLauria/cnfgen:cnfgen/families/tseitin.py` `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; `meelgroup/frat-xor:format.md` `986a21aa92b62f844ef1fce852193142c41b2b1`; `openai/math:README.md` `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. These sources supply input-generation and model-hygiene controls but **no universal all-input compiler**. Public scholarly web search and actual ECCC PDF theorem pages used; dedicated Google-branded search unavailable.

**Primary mathematics:** Itsykson–Riazanov–Sagunov–Smirnov, ECCC TR19-178 (2019), Theorems 13, 41, 52, https://eccc.weizmann.ac.il/report/2019/178/ and 2021 journal DOI 10.1007/s00037-021-00213-2. Earlier weaker Glinskih–Itsykson, *Theory of Computing Systems* 65 (2021) 613–633, DOI 10.1007/s00224-020-10007-8. Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), DOI 10.1145/7531.8928. FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005) 835–865, DOI 10.1145/1101821.1101822.

**Scientific result:** strong **published** `2^{compw}` theorem + checked restricted OR/projection transfer. **Remaining [P2-A2], [P2-A5] gap:** a solver-dependent, exponent-oblivious, recursively iterable, SAT/UNSAT/malformed-aware ALL-INPUT transform satisfying same-machine `t'<=max(11/10,3/5+t/2)` and `s'<=max(1/2,s/2)` with all phases paid. [P2-A4] is restricted evidence, NOT a universal solution. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **P versus NP OPEN.**
