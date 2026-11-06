# LSPV-5/REFEREE384: exact guarded-Tseitin recovery-normal-form work and span

**2026-11-06 03:48 PST — Independent red team, Route B.**  **PROVED/EXACT** for the explicitly defined recovery normal form below; **COMPUTATIONAL** for finite exhaustive local searches; **OPEN** for the global historical $R_{\mathrm{mix341}}$ minimum, superpolynomial $\overline W_R$, and B3. P versus NP remains OPEN.

## Idea, falsifiers, and revision

The initial hypothesis was that the REFEREE383 upper bound $12h+2$ might be the global historical mixed minimum. Four falsifiers were stated before search: a one-node legal clause recovery; one shared intermediate recovering two different clauses; a historical AND3/XOR bypass; or a cheaper branching/reconvergent proof.

Search forced a narrower claim. LSPV-1/436 supplied the construction but not a matching $12h+2$ lower bound; it established only the all-rule binary-source floor $8h+3$. The exact historical rule text also permits optimal legal derivations outside the source-recovery route. Therefore this report does **not** claim the global equality. It proves the exact optimum only after naming a syntactic normal form whose obligations are independently checkable. This is a transfer ledger and a lower-bound firewall, not a hardness result.

## Established hard family and exact encoding ledger

Let $G=(V,E)$ be a connected simple bridgeless cubic graph with $h=|V|$ and $|E|=3h/2$, and let $\chi\in\{0,1\}^V$ have odd total charge. The ordinary Tseitin source $F_h$ uses one edge variable $x_e$. At vertex $v$, the four proper ternary clauses exclude exactly the four assignments of parity $1-\chi_v$. Thus $F_h$ has $4h$ clauses and $3h/2$ variables.

For every ordered base clause $C_i=(a_i\vee b_i\vee c_i)$, introduce private $y_i$ and a shared $g$:

$$
(g\vee a_i\vee y_i),\qquad(\neg y_i\vee b_i\vee c_i).
$$

Add the four proper-3 pad clauses

$$
(\neg g\vee p^s\vee q^t),\qquad (s,t)\in\{0,1\}^2,
$$

where $p^0=p,p^1=\neg p$ and similarly for $q$. The resulting $K(F_h)$ has exactly $8h+4$ proper ternary clauses, $11h/2+3$ variables, and $\Theta(h\log h)$ explicit signed-index bits.

| Item | Exact theorem/model | Status and source | Known shortcut | Remaining transfer |
|---|---|---|---|---|
| $F_h$ | $2^{\Omega(h)}$ shared-DAG Resolution length for suitable expander Tseitin families | **KNOWN THEOREM**, Urquhart 1987; width method in Ben-Sasson–Wigderson 2001 | historical AND3/GF(2) gives $4h-1$ mixed nodes | Resolution hardness does not survive the mixed shortcut |
| $K(F_h)$ | signed-literal projection gives $L_{\rm Res}(F_h)\le L_{\rm Res}(K(F_h))$ | **PROVED/RESTRICTED**, LSPV-1/436 | REFEREE383 gives $W_{\rm mix341}\le12h+2$ | global mixed lower bound remains only $8h+3$ |
| Haken PHP | superpolynomial/exponential ordinary Resolution lower bound; polynomial Extended Resolution control | **KNOWN THEOREM**, Haken 1985 and Cook 1976 | extension variables | no transfer to all mixed rules or algorithms |

Certified UNSAT, proof-size hardness in one declared system, and empirical solver behavior are distinct. This report uses the first two and makes no empirical-hardness claim.

## Recovery normal form

Define $\mathrm{RNF}_{341}(K(F_h))$ to contain exactly the source-authenticated DAGs satisfying all four phase obligations:

1. derive $\neg g$ from the four pad clauses using oriented RES;
2. for each private-$y_i$ block, recover the exact original clause $C_i$ from its two guarded source clauses and the shared $\neg g$, without cross-block Resolution on original pivots;
3. derive each vertex parity row by a binary AND3 tree whose leaves are its four recovered original clauses;
4. XOR all $h$ vertex rows to $0=1$ with binary XOR nodes.

The class allows either local pivot order, arbitrary topological order, balanced or unbalanced binary trees, reconvergence, and one globally shared $\neg g$ subproof. Work is the union of distinct paid nodes. Every node remains in the original source context; no split, discharge, or branch-local leakage is present.

The scope restriction is material. Cross-block Resolution, DEF, LOCAL-CONVERT, a direct mixed derivation bypassing recovered clauses, and proposed case rules are outside this **scoped optimum**, although any of them remains available in the global $W_{R_{\mathrm{mix341}}}$ minimization if historically legal.

## Exact theorem

**Theorem 384.1 (PROVED/EXACT, recovery normal form).** For every source above,

$$
\boxed{W_{\mathrm{RNF}_{341}}(K(F_h))=12h+2},\qquad
\boxed{D_{\mathrm{RNF}_{341}}(K(F_h))=5+\lceil\log_2 h\rceil}.
$$

**Proof — work.**

- The four pad clauses are all necessary to imply $\neg g$: after deleting one, set $g=1$ and choose $(p,q)$ to falsify only the deleted clause. A binary-premise ancestry joining four essential leaves needs at least three paid nodes. Three Resolution nodes attain it.
- Once the shared $\neg g$ exists, each guarded block must eliminate the private pivot $y_i$ and the guard pivot $g$. One oriented Resolution node eliminates at most one pivot, so two are necessary. Resolve first on $y_i$ and then on $g$, or conversely, to attain two. There are $4h$ distinct required original clauses, hence $8h$ nodes in this phase by the block-respecting definition.
- A binary AND3 tree conjoining four required clause conditions has at least three internal nodes. There are $h$ vertex rows, contributing $3h$.
- Every vertex row is necessary. The XOR of rows indexed by a nonempty proper $S\subset V$ has edge support $\delta(S)$, which is nonempty because $G$ is connected. Only $S=V$ cancels every edge, and odd total charge then gives $0=1$. A binary XOR DAG joining $h$ essential leaves has at least $h-1$ nodes, attained by a tree.

Adding the union of distinct nodes, with the three-node $\neg g$ proof charged once, gives

$$
3+8h+3h+(h-1)=12h+2.
$$

This accounting distinguishes OR choices (two pivot orders) from AND obligations (all pads, both guarded sources per clause, all four clauses per vertex, and all $h$ rows).

**Proof — span.** Four pad leaves require binary depth two. A recovered clause depends on those four leaves and its two guarded leaves, so depth at least three is necessary and attained by resolving the guarded pair first and then with $\neg g$. Four recovered clauses require two more balanced AND3 levels, giving row depth five. Since all $h$ rows are essential, the final XOR tree adds $\lceil\log_2h\rceil$ levels. The bound is attained.

**Global qualification.** The established global statement remains

$$
8h+3\le W_{R_{\mathrm{mix341}}}(K(F_h))\le12h+2.
$$

The left endpoint is the minimally-UNSAT binary-source ancestry floor. The theorem above does not close this interval.

## Independent finite checks

The Python producer read the exact 254,223-byte REFEREE383 trace (SHA-256 `524f65bf4f033000ccaa675e14c870654eb758621d26cdb282f95b604b93df7b`). For all eight signed base-clause patterns it exhaustively enumerated every set of distinct strict Resolution clauses through four paid nodes. Each pattern has frontier counts $9,56,316,1690$; none contains the target. A target first appears with five total nodes from the six local sources, equivalently two more nodes after the shared three-node $\neg g$ proof. Thus 16,568 distinct sub-threshold derivation states were checked. The pad gadget independently has exact minimum three.

The producer also exhaustively checked all 333 nonempty vertex subsets of $K_4$, $K_{3,3}$, and the cube; only the full vertex set cancels all edge coordinates. Exact route works/spans were 50/7, 74/8, and 98/8.

The independently written Node verifier imported no producer code, reconstructed the Resolution searches and row-subset tests, passed 59 grouped assertions, and rejected eight hostile mutations: wrong run identity, source hash, theorem, scope warning, sign-pattern count, work, AND3 count, and global floor. Two producer runs were byte-identical.

## Search and authentication ledger

- Project head at search start: `e0b001a381ae2a8d523f4b7f3d783f39fb960f9b`. Read current issue #3; governing five-role handoff; exact `/341` rule text; LSPV-1/436 and /444; LSPV-3/445; REFEREE382/383; actual Grok `GROKPROOF/2026-11-06_0920_PROGRESS.md`; Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`; AGENTS.md, CODEX.md, and the project research protocol.
- Primary literature checked: Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), DOI [10.1145/7531.8928](https://doi.org/10.1145/7531.8928); Ben-Sasson–Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), [paper](https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf); Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI [10.1016/0304-3975(85)90144-6](https://doi.org/10.1016/0304-3975(85)90144-6); Cook–Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), [paper](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf).
- Required repository heads were unchanged: `konard/p-vs-np@ecedd2b`, `blkph0x/p-vs-np-proof-research@7dedc73`, `meelgroup/frat-xor@18cd6bc`, `peitl/short-proof@2c524cf`, `MassimoLauria/cnfgen@24e633b`, `openai/math@4eaee87`, and `anthropics/formal-math@16a5ce4`. Rotating checks also covered `drat-trim@2e3b2dc` and `cryptominisat@ed61e21`. The first two repositories explicitly retain restricted/experimental status; FRAT-XOR and CryptoMiniSat reinforce that XOR-derived evidence needs a dedicated checked format rather than an ordinary RUP assertion.
- Direct Google-branded search was unavailable. Indexed web search and authenticated GitHub source reads were used. No authoritative historical `$R_{\mathrm{mix341}}$` accepted-byte parser was located. The executable here is an independent rule-level verifier, not that checker.

## Resource ledger

| Resource | Producer | Independent verifier |
|---|---:|---:|
| elapsed host time | 0.418 s | 0.402 s |
| user/system | 0.409/0.008 s | 0.439/0.067 s |
| child max-RSS upper reading | 17,788 KiB | 92,304 KiB |
| executable bytes | 10,392 | 5,939 |
| output bytes | 13,697 | 330 |

Logical proof nodes are separate from parsing, source/index reads, search-state construction, hashing, JSON serialization, verification, failed mutations, cache retention, and output. The scripts materialize finite clause-state frontiers and the full prior JSON; their host high-water is not a same-machine FLMV exponent. No hidden SAT/equivalence oracle, proof discovery credit, or uncharged algebra is used. Retrieval and GitHub update/readback costs are reported separately by publication status.

## Actual advance and precise remaining gap

The advance is an exact AND/OR shared-DAG accounting theorem: the known $12h+2$ shortcut has no accidental double counting and is work- and span-optimal inside its explicit recovery normal form. The failed stronger hypothesis is equally important: this does **not** establish the global historical mixed optimum.

The next exact gap is to authenticate the historical DEF/LOCAL/facet/export byte grammar and either (i) find a legal derivation below $12h+2$, or (ii) prove that every global mixed derivation can be normalized into a cost-controlled recovery form. Independently, one still needs a family with superpolynomial minimum against **all** mixed rules and a noncircular same-calculus B3 implication. P versus NP remains OPEN.

