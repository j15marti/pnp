# LSPV-1/543: weighted source-component MAY abstraction has an exact knapsack ceiling

**2026-11-09, 13:01 PST | Route B lead | PROVED/RESTRICTED (an explicitly specified abstract domain) + COMPUTATIONAL | P versus NP OPEN.**

**Exact proof-chain IDs:** new [P2-L1-543], refining [P2-L3-536], [P2-L3-538], [P2-L1-538], [P2-L5-467], and still-OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. This does NOT authenticate the full native historical grammar or establish a superpolynomial lower bound. The theorem is a sharp ceiling for a particular family of MAY abstractions and a sound conditional potential under exhaustive dependency/charge rules.

## IDEA, falsifiers, and change from prior work

Candidate: generalize the exact binary-merge ceiling of LSPV-3/538 to **heterogeneous charged hyperedge rules**. Represent each legal paid rule type only by an upper bound on how many indispensable-source components its **complete source-bearing dependency footprint** can combine and by an abstract charge no greater than native work. Predict an exact unbounded-budget abstract minimum given by a finite unbounded-knapsack program. If so, every finite fixed-arity source-partition-only may abstraction has at most linear abstract goal distance, even if the true refutation minimum is much larger. This identifies what additional semantic information a superlinear cost-sound invariant MUST use.

Precommitted falsifiers:

1. An abstract rule able to merge at most $r_j$ source components with charge $c_j$ can connect all $m$ abstract source blocks at cost strictly **less** than the proposed covering knapsack.
2. A minimum covering-knapsack solution cannot be implemented as an abstract partition-reduction path, perhaps because its last step has unused merge capacity.
3. A verified historical rule, split discharge, private DEF facet or LOCAL-CONVERT side read merges more than the claimed number of components for its assigned native charge. This defeats application to historical $R_{\mathrm{mix341}}$, though not the mathematical theorem for the declared abstraction.
4. LSPV-3/538 or another prior report already proves this exact heterogeneous-cost, arbitrary-arity knapsack equality. The prior report proves the $r=2,c=1$ case. Broader source-hyperedge reasoning exists elsewhere in the corpus, and we do not claim novelty for general set-partition dynamic programming.

Falsifiers (1) and (2) are ruled out symbolically, checked independently in finite partition-state exhaustive searches. Falsifier (3) remains **OPEN** for unauthenticated historical rules. Falsifier (4) was not located in targeted project search but absence of a search hit does not establish academic novelty.

## SEARCH, corpus, exact evidence, and external scope

**Governing evidence read:** complete repository-root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), proof2.txt (startup blob 3298a3fcc7fd5383a371a671e21cada58c99e556), current issue #3 and its latest comments through [P2-L5-467], AGENTS.md blob 4ae902888754d0b06ba4ce1aaeca0657a92b46a9, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef, .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f, and research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b. Original declared semantics read from research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. The historical two-rule producer/checker audit at experiments/review/lspv5_413_historical_341_checker_audit.py and LSPV-5/412 confirms the surviving accepted-byte grammar is NOT authenticated for RES/LOCAL-CONVERT/DEF or all typed parent views.

**Relevant peer original reports:** LSPV-3/536 (conditional source partition invariant), /538 (exact binary-only ceiling), /539 (affine-hull CEGAR), /540 (eight-bit exact local factor); LSPV-5/464 (shared occurrence versus label), /466 (provenance-aware alpha joins), /467 (Hall/max-flow whole-DAG sponsor accounting); LSPV-1/538 (source-side reads), /541 (conditional nominal quotient), /542 (different-calculus source-exact macro); LSPV-2/526 (RAT/RUP transfer firewall); REFEREE336 (typed ER fragment), LSPV-3/440 (conditional owner-to-LOCAL facet compiler), and REFEREE379/446 (full polynomial Cook FACET-A/FACET4 shortcuts). Relevant searches included "r-1 component", "weighted source partition", "source merge capacity", "general extended resolution simulator", and "ER-to-mixed compiler". The ER-to-mixed simulation was already proved in REFEREE299/336; it is NOT a new result here.

**Actual cross-model evidence:** GROKPROOF/2026-11-09_2015_PROGRESS.md blob 5610d47e2a78ded4e4e57bc24fca3266e03f42ac; research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4e7e0e3edff3aba8610852c45534bdde128. Neither supplies full native grammar or B3.

**Required external repository reads:** konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (scoped finite-machine theorem status); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped methods, no PNP resolution); meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (separate XOR typed format); MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (graph/charge input generator); openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (mixed formal-verification stages). No repository file is permission to change the historical rule system. These are change-aware checks rather than a full reread of every repository.

**Primary literature:** Cousot & Cousot POPL 1977 https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml (may overapproximation, not quantitative proof-work bound); Pommerening, Helmert & Bonet, ICAPS 2017, DOI 10.1609/icaps.v27i1.13806 (cost partitioning in abstract planning, MODEL TRANSFER REQUIRES this paper's explicit full-proof-state simulation); Urquhart, JACM 1987 DOI 10.1145/7531.8928 (ordinary Resolution on expander Tseitin); Cook, SIGACT News 1976 DOI 10.1145/1008335.1008338 (Extended Resolution PHP shortcut); Pich & Santhanam, JACM 2026 DOI 10.1145/3801091 (lower-bound-to-circuit implication barriers). No separately branded Google search interface was used; general indexed web queries and authenticated GitHub reads were used.

## Exact abstract transition system and theorem

Fix a **minimally UNSAT** source $F=(C_1,\ldots,C_m)$ whose source clauses have immutable, separately authenticated IDs. Consider any full concrete partial proof state with original-source bytes; a shared acyclic inference hypergraph with **distinct paid occurrence IDs**; all active assumption contexts and discharge evidence; definition owners, names and global freshness; source provenance including side reads and facets; cumulative native logical work. A completed legal refutation has all assumptions discharged, and any legal source-authenticated sound proof depends on every individually indispensable $C_i$.

Our coarse **MAY projection** retains only the partition $\pi$ of the $m$ source identities into connected source-bearing dependency components, and optionally the exact paid-ID ledger (which does not restrict merges in this projection). For each declared abstract rule type $j\in J$, fix an integer capacity $r_j\ge2$ and a nonnegative abstract charge $c_j$. The MAY transition permits an arbitrary merger of **any** $2,\ldots,\min(r_j,|\pi|)$ distinct blocks and charges $c_j$; source-free, reuse, or nonmerging steps stutter at their native stated charge or less. The goal is the one-block partition; it may include spurious goals and is therefore a conservative relaxation. There is no source-clause semantic or typed GF(2)/DEF constraint on these MAY joins.

**Conditional sound projection lemma:** For EACH actual source-authenticated paid transition of type $j$, assume (a) its complete source-bearing hyperedge (including side reads and owner facets) reduces the number of source components by at most $r_j-1$, (b) its abstract first-use charge $c_j$ is no greater than the native charge for that **distinct occurrence**, (c) reuse/reference is accounted for with the historical fee, and (d) every legal goal is represented by one source-bearing component. Then every full concrete refutation path projects into the MAY state machine at no higher charged work, including arbitrary sharing/reconvergence and all AND obligations, so $D_J(m)\le W_R(F)$. Incompatible branch contexts are NOT legalized by the projection: they are simply forgotten as an overapproximation. Missing native rules must be conservatively represented, not omitted. Conditions (a)-(d) are **NOT authenticated for all historical R_mix341 bytes**.

**Theorem 543.1 (PROVED/RESTRICTED, exact MAY minimum).** For every $m\ge1$ and finite nonempty $J$ with each $r_j\ge2$, $c_j\ge0$, the minimum abstract goal cost is exactly

$$
\boxed{
D_J(m)=\min_{\substack{t_j\in\mathbb N_0\\
\sum_j (r_j-1)t_j\ge m-1}}\sum_j c_jt_j .
}
$$

**Proof, lower direction:** Every charged step of type $j$ lowers the component count by at most $r_j-1$. Along any path from $m$ blocks to one, the total component decrease is $m-1$, so its type-use counts form a feasible vector in the displayed program and the path cost is at least the minimum.

**Proof, upper direction:** Take a minimizing integer vector $t$. Starting with the discrete partition, apply the listed types in any order, each time joining the maximum available number of blocks (up to $r_j$), and stop once one block remains. Since the listed total merge capacity is at least $m-1$, the goal is reached within those steps. It is irrelevant if the last step has unused capacity; stopping early can only reduce cost because $c_j\ge0$. Thus a legal MAY path has cost no more than the integer-program optimum. Equality follows. These abstract moves may be **spurious as native RES/AND3/GF(2)/DEF/LOCAL derivations**; that is exactly why this is a MAY ceiling, not a concrete upper bound.

Put $\rho=\min_j c_j/(r_j-1)$ and choose any minimizer $j_*$. The state potential

$$
V(\pi)=\rho\,[m-|\pi|]
$$

has $V(\pi_0)=0$, $V(\text{goal})=\rho(m-1)$, and across EVERY declared MAY rule $\Delta V\le\rho(r_j-1)\le c_j$. Conversely, repeating type $j_*$ gives

$$
\boxed{
\rho(m-1)\le D_J(m)\le
c_{j_*}\left\lceil\frac{m-1}{r_{j_*}-1}\right\rceil
<\rho(m-1)+c_{j_*}
}
$$

for $m>1$ and $c_{j_*}>0$; if $c_{j_*}=0$, then $D_J(m)=0$. For $m=1$, $D_J(1)=0$. In particular, when all caps and charges are fixed independently of source size, **no superlinear or superpolynomial bound can be certified solely by this entire partition/type/price MAY domain**. Even if its semantic native projection is sound, it has artificial low-cost abstract joins.

**Unknown-rule CEGAR firewall:** If a potentially historical source-sensitive rule has *unverified* exhaustive source-dependency arity and might in one paid step join all $m$ components, a sound conservative MAY extension must permit type $(r,c)=(m,c)$ with $c$ at most the native logical fee; when $c=1$ it forces $D_J(m)\le1$. If a zero-cost multi-source discharge is possible, the conservative bound is zero. This is a **diagnostic about missing information**, NOT evidence that R_mix341 actually contains such a macro. To recover a nontrivial invariant authenticate a stricter rule footprint and introduce exact typed semantic restrictions on which joins are legal.

## Established hard-family, encoding and shortcut ledger

**Tseitin:** Qualifying connected, bridgeless cubic *expander* $G_h$ has $h$ vertices, $n=3h/2$ edge variables, four strict 3-clauses at each vertex and $m=4h$ source clauses; the local four signed facets prohibit wrong parity, and odd vertex charge makes UNSAT. Input index length $N=\Theta(h\log(h+2))$ for standard indexing. Urquhart's theorem gives exponential *ordinary shared-DAG Resolution* lower bounds for appropriate expanding families, not full $R_{\mathrm{mix341}}$. LSPV-2/341 already gives the explicit DECLARED mixed system proof with exactly $4h-1$ unit paid AND3+XOR nodes. The single type $(r,c)=(2,1)$ gives $D_J(4h)=4h-1$, agreeing only with that declared result. Adding a hypothetical unit-priced global $(4h,1)$ rule gives $D_J=1$, but the LSPV-1/542 TSEITIN-CLOSE macro is from a DIFFERENT calculus.

**Bit-PHP and encoding:** Braun's original n=$2^\ell$-hole bit PHP with n+1 pigeons has $\ell(n+1)$ address bits and $M=n\binom{n+1}{2}$ source clauses of width $2\ell$. Its **private-chain strict 3CNF** uses $S=M(2\ell-2)$ clauses and $V=(n+1)\ell+M(2\ell-3)$ variables, $N=\Theta(n^3\ell^2)$ encoded bits. Braun arXiv:2609.23015v2 and Pang arXiv:2610.00837v2 prove specified original-formula Res(XOR)/Res(PC1/F2) DAG lower bounds, not this strict-3 encoding, not ER, and not native mixed. The source partition with unit binary merges gives only $S-1$. Cook ER and the project REFEREE379 FACET-A short shared-DAG proofs are mandatory controls; the latter grammar is not authenticated as native.

## Independent verification and resource ledger

**Published JavaScript:** experiments/arc/lspv1_543_weighted_source_merges.js, blob 0b30ac574647b9adcbca30747443aa223ce8c001. It exhaustively explores **entire set partitions** using Dijkstra, independently compares to a capacity-knapsack DP and checks the potential bound. It ran 35 cases (seven type sets, $2\le m\le6$), 108 deterministic assertion groups, max 203 distinct reachable partitions. Extra controls show $D_{(2,1)}(16)=15$, $D_{(2,1),(16,1)}(16)=1$, and free global merge gives zero. **Independent Python:** experiments/arc/lspv1_543_weighted_source_merges_independent.py, blob 208bc3d46b6ba07b2ea9cbf7f6f61947169a1152, executed separately on the same 35 parameter cases with 105 independent grouped assertions and max 203 partition states. There are no random seeds and no SAT formula parser in this experiment: both-label/malformed-input proof checks are NOT claimed, and this is not execution of any original historical proof checker. Full machine output: results/raw/arc/2026-11-09_1301_LSPV1_543_WEIGHTED_MERGES_RAW.json.

The resulting claim is **symbolic** in all $m$ and finite rule types; the finite computations only check its implementation. The logical abstract cost is not encoded evidence bits, actual search/construction/runtime, parallel span or peak space. The Dijkstra state graph includes at most Bell($m$) partitions and was exhaustively searched only at $m\le6$, not asserted to be a uniform efficient SAT solver. Explicit source parsing, optional proof concretization, branch/certificate replay, source head reads, output, and failed CEGAR refinements must be fully charged in any actual algorithm. A sound global paid-ID sponsor-flow check per LSPV-5/467 is still required for more detailed abstractions: a local abstract-cost comparison alone does not justify double spending a shared native node.

## Duplication / contradiction / root-MAIN / exact next implication

**Adopt:** LSPV-3/536's scoped source-component invariant, /538's special binary optimum, LSPV-5/467's count-once sponsor condition, LSPV-1/541's conditional global-name orbit, and LSPV-3/540's exact local factor representation. **Reject:** the mistaken inference that the partition MAY lower estimate automatically grows superlinearly when the concrete family is Resolution-hard. **Do not promote:** any cost ceiling to a concrete shortcut, any abstract-domain state count to solver time, any restricted proof minimum to all-algorithm hardness, or any conditional ER simulation to historical grammar authentication. The current root main.tex already documents source-arity and paid-history caveats; this result adds a heterogeneous type-and-weight ceiling, not a replacement for its proof spine. There is no contradiction with verified historical results.

For a next-stage genuine mixed-rule lower bound, LSPV-3 should replace arbitrary type-j block merges with **source-authenticated legal-conclusion transformers**, exposing exact 8-bit local AND3 semantics and conservative definition-owner facets. LSPV-5 should independently attack any superlinear proposed semantic potential using compact ER/FACET-A, GF(2), shared paid occurrence IDs and cross-branch discharge. LSPV-1 retains the separate noncircular B3 quantifier obligation. All [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain **OPEN**, and the Route A all-input same-machine transfer remains OPEN. Historical grammar/weights and five roles with 2 Route A/3 Route B remain unchanged. **P versus NP remains OPEN.**
