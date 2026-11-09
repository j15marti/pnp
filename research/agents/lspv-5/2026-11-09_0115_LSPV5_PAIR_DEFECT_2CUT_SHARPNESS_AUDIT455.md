# LSPV-5/455: the pair-defect $J_9$ block fails exactly at a connected cubic two-cut

**2026-11-09 01:15 PST | Route B independent red team | PROVED/RESTRICTED sharpness lemma + exhaustive finite controls. P versus NP OPEN.**

**Proof-chain scope.** This run directly tests [P2-L1-528] against a compact connected cubic graph outside its stated 3-vertex-connected hypothesis. It also checks the source semantics used by [P2-L3-521], [P2-L3-522] and [P2-L5-452]. It does not change [P2-D1], [P2-C3], [P2-B1] or [P2-B2]. The peer ER2 composition packet [P2-L3-528] is a separately declared proposed grammar and remains outside historical accepted-byte authentication.

TRACKERS REVIEWED; NO MATERIAL CHANGE

## IDEA -> falsifiers -> SEARCH -> ITERATE

**Initial hypothesis.** The connected-residual step in [P2-L1-528] is load-bearing: if the hypothesis is weakened from simple 3-vertex-connected cubic graphs to connected cubic graphs, a nonadjacent two-vertex cut can prevent some of the $9\times9$ local wrong-defect pairs from extending. Prediction: the corresponding block has 27 rather than 81 edges, so the reported regular degree and spectral decomposition fail.

The following falsifiers were fixed before computation:

1. the proposed graph is not simple, connected and cubic, or deleting vertices 0 and 1 does not disconnect it;
2. all 81 local wrong-defect pairs at the nonadjacent cut still extend;
3. reversal/mixing of the arbitrary edge orientation, or movement of the unique nonzero charge, changes the block count;
4. the failure is merely an implementation or local-tuple ordering artifact rather than the residual-component incidence condition.

**Search performed.** The complete current `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (blob `b2c5dad9ee0bb0b7293e004fb993ddf932a824aa`) were read at main head `d43c91dce8c62b4baa06f4e2a63fb036ab1798a4`, together with issue #3, the five-role refocus, AGENTS.md, CODEX.md, the repository research instructions, actual `GROKPROOF/2026-11-08_1130_PROGRESS.md`, and actual `research/agents/claude/worlds/README.md`. The current role reports for [P2-L1-528] and [P2-L3-528], their code/raw/handoffs, and the prior LSPV-5/454 independent K4 audit were inspected. Project searches for `3-vertex-connected`, `pair-defect`, and `G-{u,v}` found the [P2-L3-522] exact-core report and [P2-L1-528], but no prior connectivity-sharpness counterexample.

Required repository review was change-aware. `konard/p-vs-np` was pinned at `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `proofs/experiments/issue532/ideas/Idea25.md` proves exact disjoint-component splitting but correctly leaves the all-input reduction open. `blkph0x/p-vs-np-proof-research` was pinned at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md` and `tseitin_expander_lab/README.md` explicitly qualify the finite connected-cubic sweep and do not claim a uniform-expander theorem. `MassimoLauria/cnfgen` was pinned at `24e633e4339d80d76bdd4b2aa830562ab5ef7761`; `cnfgen/families/tseitin.py` implements one edge variable with a parity constraint at every vertex, and `docs/graphs.rst` cites Urquhart only for Resolution-hard expander instances. Targeted checks of current `openai/math` (`4eaee...`) found no Tseitin/connectivity result relevant to the gap. No current-head delta was found in the two mandatory external repositories.

Primary-source search authenticated the restricted literature scope: Urquhart, *JACM* 34(1), 1987, DOI 10.1145/7531.8928, proves exponential ordinary-Resolution lower bounds for Tseitin clauses built from expander graphs; Ben-Sasson--Wigderson's width presentation gives a $d$-CNF with at most $n2^{d-1}$ clauses and an expansion-dependent width bound; Pang arXiv:2610.00837v2 gives constant-$r$ algebraic proof-system lower bounds, not a full mixed-calculus bound. General web search was available. No separate Google-specific implementation was available, so no Google use is claimed.

**Revision after evidence.** The experiment falsifies the weakened theorem, not [P2-L1-528] itself. The exact replacement is a residual-component criterion: after the local tuples at $u,v$ are fixed, an extension exists iff the prescribed residual divergence has zero sum on every connected component of $G-\{u,v\}$. Three-vertex-connectivity makes this automatic for nonadjacent $u,v$ because the residual has one component and zero total. A two-cut creates an additional independent component equation.

## Exact family / encoding / theorem / method / remaining-transfer ledger

Let $G_8$ have vertices $0,\ldots,7$ and edges

$$
\begin{aligned}
E={}&\{02,03,12,13,23,46,47,56,57,67,04,15\}.
\end{aligned}
$$

Equivalently, take two copies of $K_4$, delete edge $01$ in the first and edge $45$ in the second, and add cross edges $04,15$. Every vertex has degree three and the graph is connected. Vertices 0 and 1 are nonadjacent, but

$$
G_8-\{0,1\}=G[\{2,3\}]\;\dot\cup\;G[\{4,5,6,7\}].
$$

Use the exact signed proper strict-3-CNF source of [P2-L1-528]: for every edge $e$, Boolean atoms $x_{e,0},x_{e,1},x_{e,2}$ and the width-three ALO clause; for every cubic vertex, eighteen width-three negative clauses forbidding the incident label triples whose signed sum differs from charge $b_v$. Take $b=(1,0,\ldots,0)\in\mathbb F_3^8$, so $\sigma=\sum b_v=1$. The source has 36 Boolean atoms, 12 edge ALO clauses and $18\cdot8=144$ vertex clauses, hence 156 strict width-three clauses. Summing all vertex equations cancels every oriented edge and yields $0=1$, certifying UNSAT.

This finite graph is a validation control, not a claimed hard family. The cited asymptotic lower bounds require expanders and a specified proof system. Certified UNSAT, finite compatibility structure, empirical solver behavior and proof-size hardness remain distinct.

## Theorem 455.1: residual-component extension criterion (PROVED/RESTRICTED)

Fix distinct vertices $u,v$ and fixed local incident-edge labels at them. Delete $u,v$. For every connected component $C$ of the residual graph, sum the desired vertex divergence equations over $C$. Internal edge contributions cancel. The remaining boundary-edge values are already fixed by the local tuples. Therefore zero residual sum on $C$ is necessary.

Conversely, on each connected component $C$, the signed incidence matrix over $\mathbb F_3$ has image equal to the codimension-one zero-sum subspace. If the component residual sum is zero, its remaining internal edge labels can be chosen to realize the prescribed residual divergence. Components are edge-disjoint, so these choices combine. Thus the component equations are also sufficient.

This is the exact missing qualification behind the [P2-L1-528] nonadjacent $J_9$ block. When $G-\{u,v\}$ is connected, the single component equation is the already-known global zero total and all 81 local pairs extend. If the deletion disconnects the graph, extra component equations may remove local pairs.

## Theorem 455.2: explicit connected-cubic counterexample to the weakened $J_9$ claim

Orient every edge from its smaller endpoint to its larger endpoint. At vertices 0 and 1, a wrong-defect tuple must have signed sum $b_v+\sigma$, hence respectively 2 and 1. For component $C=\{2,3\}$, the criterion becomes

$$
x_{02}+x_{03}+x_{12}+x_{13}=0\pmod 3.
$$

For example, the two local tuples

$$
t_0=(0,0,2),\qquad t_1=(0,0,1)
$$

satisfy their local wrong-defect equations and the component equation, and the raw artifact contains a global extension. Replacing $t_1$ by $(0,1,0)$ preserves its local wrong-defect sum but changes the displayed boundary sum to 1, so no extension exists. Exact enumeration finds precisely 27 compatible pairs out of the possible 81 at block $(0,1)$.

Across all 28 vertex pairs, 12 blocks have 81 edges and 16 have 27 edges. The 16 comprise the 12 adjacent-pair blocks plus four nonadjacent two-cut blocks. The resulting 72-vertex pair-defect compatibility graph has 1,404 edges and degree histogram

$$
33^{(36)},\qquad45^{(36)}.
$$

It is not regular. Therefore the $9h-27=45$ regularity and the [P2-L1-528] direct-sum spectrum do not extend to all connected cubic graphs. This proves the 3-vertex-connectivity assumption is genuinely used; it does not weaken the theorem at its published scope.

## Independent checks and hostile controls

`experiments/review/lspv5_455_pair_defect_2cut_audit.py` enumerates all $3^{12}=531,441$ edge-label assignments per run. It checks simplicity, connectedness, cubicity, every residual component and all 28 compatibility blocks. The base run, full orientation reversal, a mixed orientation and all eight locations of the unique nonzero charge agree. Eleven full enumerations were executed. Deleting one graph edge is rejected as noncubic, a forged local tuple is rejected, and explicit accepted/rejected cut-pair tuples are stored.

`experiments/review/verify_lspv5_455_pair_defect_2cut.mjs` is an independent Node implementation. It does not enumerate the Python assignment table: it computes exact ranks over $\mathbb F_3$ for every one of the $28\cdot81$ local-pair extension systems. It obtains incidence rank 7, the same `27:16, 81:12` block histogram, and rejects a forged $J_9$ cut block and a corrupted raw count.

Raw artifact: `results/raw/arc/2026-11-09_0115_LSPV5_455_PAIR_DEFECT_2CUT_RAW.json`. SHA-256 values at publication staging:

- Python: `8621b8ddac00ae8ec6bc33f088ea313f7d17e1f168d5e9b1f28ec0b6b8830666`;
- Node: `61a9038e680fdfd7d458f58631b70f95020bc4b36e59de272f79df96b9b823b9`;
- raw JSON: `8ed342845df9c1a01d59d629e5d9255bf4cea9c9004bd4c0656630834ded9b96`.

The raw JSON also carries an internal canonical-payload hash `028d9ae23229820f297aa713243477a09f25b596e25076222daccb82f579d0b0` computed before insertion of that field.

## Resource and proof-model ledger

- logical inference nodes constructed: 0;
- finite labels inspected: $11\cdot3^{12}=5,845,851$ Python edge-label assignments;
- independent Node consistency systems: $28\cdot81=2,268$;
- Python wall time for its 11 runs: approximately 17 seconds on this host; Node wall time was below one second;
- explicit evidence: 27 accepted cut-pair witnesses plus all pair/component counts and hostile controls in 30,075 raw bytes;
- peak memory, web/GitHub reads, parsing, source indexing, caches, process startup, report construction, verification, publication and readback are not included in the experiment timer;
- no proof-search cost was hidden inside $W_R$: this run builds no refutation and makes no numerical claim about $W_R$;
- no semantic SAT oracle, case-split/discharge rule, weakening rule, historical weight change, or FLMV machine simulation is introduced.

The ideal minimum remains free to choose any legal shared DAG. Actual algorithms must charge search, construction, failed policies, references, storage, retrieval/recomputation, parsing, verification and output. Work, span and realizable space are not identified here.

## Red-team result and precise remaining gap

**Actual advance.** The connected-residual step in [P2-L1-528] is now independently isolated and shown sharp by an exact connected cubic two-cut control. The correct residual-component lemma is proved, an explicit legal local nonextension is exhibited, and two independent programs agree on every block. This prevents accidental use of the $J_9$ block, regular degree or spectrum on merely connected cubic graphs.

**What remains open.** The result supplies no superpolynomial lower bound across all historical `R_mix341` rules and no noncircular fixed-calculus B3 implication. [P2-D1] exact historical grammar/accepted bytes, [P2-C3] full mixed-rule transfer, [P2-B1] all-rule superpolynomial work lower bound and [P2-B2] B3 remain OPEN. [P2-L3-528] remains a proposed-ER2 composition result with no claim of historical checker execution. Restricted Resolution or constant-$r$ algebraic hardness is not arbitrary-machine SAT hardness.

Root `main.tex` was not modified. Historical roles, IDs, titles, schedules, enabled states, `R_mix341` grammar/weights and the two-Route-A/three-Route-B allocation were preserved. P versus NP remains OPEN.

## References

1. [P2-L1-528], `research/agents/lspv-1/2026-11-09_0010_LSPV1_PAIR_DEFECT_SPECTRAL_SOURCE_COVER528.md`.
2. [P2-L3-522], exact source-core theorem for 3-vertex-connected cubic sources.
3. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Theorem 7.2(b), https://arxiv.org/html/2610.00837v2.
4. Alasdair Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987, 209--219, DOI 10.1145/7531.8928.
5. Eli Ben-Sasson and Avi Wigderson, *Short Proofs Are Narrow---Resolution Made Simple*, JACM 48(2), 2001.
6. CNFgen, `cnfgen/families/tseitin.py` and `docs/graphs.rst`, commit `24e633e4339d80d76bdd4b2aa830562ab5ef7761`.
