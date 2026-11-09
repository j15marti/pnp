# LSPV-1/545: an unbounded integrality gap for exact shared-obligation cost partitioning, with a succinct nonadditive repair

**2026-11-09 14:00 PST, America/Los_Angeles | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Node proposal:** [P2-L1-545], refining [P2-L1-544], [P2-L1-543], [P2-L5-467], [P2-L5-468] and the still-open [P2-C3]. This is a theorem about an explicitly **distinct** cover/AND-OR transition calculus. It is NOT a source-authenticated native $R_{\mathrm{mix341}}$ lower bound, an all-solver abstraction, or a SAT decision-time theorem.

## IDEA: hypothesis and falsifiers, stated before research

**Candidate.** Extend the exact $K_n$ graph-edge sponsor gap in /544 to all complete uniform hypergraphs and determine whether every *nonnegative additive obligation potential*, even with all legal actions and their exact footprints, can be arbitrarily weaker than the genuine globally shared paid-node optimum. Test a succinct, nonadditive potential that repairs the gap without a shortest-proof oracle.

- **F1:** A collection of fewer than $n-k+1$ paid sponsors discharges every $k$-subset obligation. **FALSIFIED** by a remaining unsponsored $k$-set.
- **F2:** Some nonnegative additive weights respecting each action cost attain value greater than $n/k$. **FALSIFIED** by summing all $n$ sponsor inequalities.
- **F3:** The proposed nonadditive potential exceeds the charge of a fresh sponsor or rises on a reused sponsor. **FALSIFIED** by the exact set-cardinality increment inequality, independently checked at finite sizes.
- **F4:** Every historical $R_{\mathrm{mix341}}$ inference has a proved mapping into these sponsor actions and a complete future-effect footprint with cost nonexpansion. **OPEN/NOT ESTABLISHED**. A real unmodeled legal rule would invalidate a native-calculus application, not the separate cover theorem.

## SEARCH: governing project evidence and primary sources

Mandatory reads: complete root *proof1.txt* (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), complete current *proof2.txt* as fetched at preflight, coordination handoff research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md (blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b), issue #3 including recent /544 and /468 comments, AGENTS.md (blob 4ae902888754d0b06ba4ce1aaeca0657a92b46a9), CODEX.md (blob 754999f50de93cdb693ed37bc8110d31e9e698ef), and .codex/skills/pnp-research/SKILL.md (blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f).

Original project work read: LSPV-2/341 (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb, historical **declared** five-rule grammar and exact cubic-Tseitin $4h-1$); LSPV-1/544 (90fe094212ea9b24719a47e44c230ec52d3f1108); LSPV-3/541 (4e264e6dee2c1a33bfc24bdc92940bce7cbad21e, signed DEF facets); LSPV-5/467 (8b168fcae968a99d9e17f6ab9a5228293ce0aef3, global sponsor flow); actual GROKPROOF/2026-11-06_2316_PROGRESS.md (a20fb8b3640d7574faf238a4a83a021bb0984808), research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex, and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (different machine-model barrier). Older knot/guest directions were not used as proof sources.

Required change-aware external reads: konard/p-vs-np/proofs/complexity/README.md (7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3, finite one-tape machine model and scoped P subset NP); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5, claims restricted to stated methods) and proof_complexity_frontier_lab/WIDTH_REPORT.md (e35fd458696fe594b09b26280361641e104fe016, seven finite Resolution-width controls); meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f, XOR proof-format interfaces); tanyongkiam/cake_lpr/README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c, separate checker/toolchain); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab, parity-instance generator); openai/math/README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae, manuscripts of varied verification status). None establishes the missing mixed-calculus mapping or B3.

Primary literature consulted: Cousot & Cousot (POPL 1977), abstract transition simulation; Pommerening, Helmert & Bonet, *Abstraction Heuristics, Cost Partitioning and Network Flows*, ICAPS 2017, DOI 10.1609/icaps.v27i1.13806, cost partitions and LP dual; same authors, *Higher-Dimensional Potential Heuristics*, AAAI 2017, DOI 10.1609/aaai.v31i1.11023, non-atomic state features; Atserias & Dalmau, JCSS 74 (2008) 323–334, DOI 10.1016/j.jcss.2007.06.025, exact **Resolution-width** scope; Urquhart, *Hard Examples for Resolution*, JACM 34 (1987) 209–219, DOI 10.1145/7531.8928, ordinary shared-DAG Resolution only. Searches used indexed web results, not an independent Google service. The complete-uniform hypergraph LP gap is an elementary instance of standard hitting-set integrality phenomena; no global mathematical novelty is asserted.

## 545.1 A completely specified first-use shared AND/OR calculus

Fix integers $n\ge3$, $2\le k\le n$. Let the obligation universe be the complete $k$-uniform hypergraph
$$
U_{n,k}=\{T\subseteq[n]:|T|=k\}.
$$
There is exactly one optionally paid, globally reusable unit-cost sponsor event $a_i$ for each $i\in[n]$. First use adds every obligation $T$ with $i\in T$, reuses cost zero, and there are no other events. Every $T$ is an **OR** obligation, discharged by one sponsor in $T$; the goal is the **AND** of all $T$. Full state is the globally paid sponsor set $S\subseteq[n]$ and its induced discharged-obligation set $D(S)=\{T:T\cap S\neq\varnothing\}$. The transition $S\to S\cup\{i\}$ has cost $1$ iff $i\notin S$, otherwise $0$. All rules, source identity and all weights of this distinct abstract system are now fixed. It is not a CNF input nor a rewrite of historical $R_{\mathrm{mix341}}$.

## 545.2 Exact theorem for every $n,k$

**Theorem (symbolic, PROVED/RESTRICTED).** The exact globally shared minimum and maximum cost-sound nonnegative *additive single-obligation* potential are
$$
\boxed{W_{T_{n,k}}=n-k+1,\quad
\operatorname{ADD}_{n,k}=\frac nk,\quad
\frac{W_{T_{n,k}}}{\operatorname{ADD}_{n,k}}=
\frac{k(n-k+1)}{n}.}
$$
The additive constraints use weights $y_T\ge0$ and require $\sum_{T\ni i}y_T\le1$ for every native sponsor $i$.

**Proof of the optimum.** A set $S$ completes the AND goal iff no $k$-subset is disjoint from $S$, equivalently $|[n]\setminus S|<k$, equivalently $|S|\ge n-k+1$. Taking exactly that many distinct sponsors attains the minimum. The full graph of reusable paid events, not an unshared tree, is minimized.

**Proof of the sharp additive ceiling.** Sum the $n$ single-sponsor inequalities. Every $y_T$ occurs exactly $k$ times, hence $k\sum_Ty_T\le n$. Uniform weights $y_T=1/\binom{n-1}{k-1}$ satisfy every sponsor constraint at equality, while $\sum_T y_T=\binom nk/\binom{n-1}{k-1}=n/k$. This completely solves the declared additive LP without external optimization software.

**Unbounded gap.** For $n=2m$ and $k=m$ the genuine optimum is $m+1$, while the strongest additive potential is exactly $2$, giving ratio $(m+1)/2=\Theta(n)$. The obligations are **not** of polynomial explicit length in $n$: $|U_{n,k}|=\binom nk$, and for central $k$ this gap is only $\Theta(\log |U|)$. It is an *integrality/abstraction-precision* gap, not an exponential lower bound in encoded input length or physical memory.

**Succinct nonadditive repair.** The potential
$$
\boxed{V(S)=\min\{|S|,n-k+1\}}
$$
satisfies $V(\varnothing)=0$, $V(\mathrm{goal})=n-k+1$ and
$$
0\le V(S\cup\{i\})-V(S)\le\mathbf1_{\{i\notin S\}}.
$$
It is therefore a cost-sound *exact* potential in the same calculus. It is computed by an $n$-bit sponsor mask and a cardinality, despite the exponentially large explicit obligation universe. Its goal lower bound follows from the independently proved combinatorial covering criterion, not an oracle for shortest proofs.

**Scientific consequence.** Even exact footprints, all legal OR/AND obligations, and perfect global first-use accounting leave an unbounded gap for the entire class of nonnegative **additive atomic-obligation** potentials. Higher-order or nonadditive state information can close it, sometimes with succinct syntax. This is a concrete refinement of /544, not a claim that any arbitrary potential fails.

## 545.3 Hard-family and hostile-shortcut controls

The original-source established-family reference remains odd-charge Tseitin on simple cubic graphs, exact strict signed 3-CNF with $h$ vertices, $3h/2$ edge variables and $4h$ ternary clauses. Urquhart's appropriate *expander* instances are exponentially hard **only in ordinary Resolution**. Project /341 proves exact $W_{R_{\mathrm{mix341}}}=4h-1$ for its declared five-rule semantic calculus via $3h$ paid AND3 plus $h-1$ paid GF(2) steps. This compulsory legal shortcut destroys any attempted exponential mixed-hardness transfer from Resolution for that family.

A direct **K4 finite control only** rebuilt all 16 ternary source clauses on six edges: odd charge has 0 models, even charge has 8; each of the 16 odd source clauses is indispensable by explicit satisfiability after deletion. K4 is **not** claimed to be a certified expander-hard member. No authoritative historical mixed checker was run. The full mixed grammar's LOCAL-CONVERT exported/private-wire parser, paid DEF facets, numerical IDs and branch discharge remain unauthenticated, so [P2-D1], [P2-C3] remain OPEN.

## 545.4 Independent execution, exact evidence and resource distinctions

GitHub V8 independent JavaScript implementation: **54** $(n,k)$ configurations for $3\le n\le11$, $2\le k\le n$; **36,864** exhaustively checked sponsor subsets, **376,816** single-sponsor transition-cost controls; K4 0/8 model controls and 16 deletion-SAT checks; four invalid dimension controls rejected. All passed. The script is runnable standalone with Node.js and uses no imported packages except built-in assertions. The exact published code was evaluated with a V8-compatible assertion harness; an external Node command on GitHub Actions was NOT executed.

Independent CPython reimplementation: 54 configurations, 36,864 sponsor subsets, 4 invalid-dimension and 3 invalid-identifier rejections; K4 odd/even/deletion controls passed. A measured local CPython rerun required 1.53 s wall time and 95,756 KiB peak resident memory. The independent local files are available in the associated conversation artifact; they were not represented as runs of the historical native checker.

Exact *logical* paid-node optimum $n-k+1$ and $n/k$ LP potential are distinct from explicit certificate bits, input parsing, search, reference/lookup/replay, proof-construction time, parallel span and peak space. The exhaustive tests are validation only. The symbolic proof already establishes the all-$n,k$ theorem, not a numerical extrapolation.

Published evidence:
- experiments/arc/lspv1_545_complete_uniform_cover.js
- results/raw/arc/2026-11-09_1400_LSPV1_545_UNIFORM_HYPERGRAPH_COVER_RAW.json
- research/agents/lspv-1/2026-11-09_1400_LSPV1_COMPLETE_UNIFORM_HYPERGRAPH_GAP545.md (this report)
- research/coordination/2026-11-09_1400_LSPV1_UNIFORM_HYPERGRAPH_GAP545_FIVE_ROLE_HANDOFF.md

## 545.5 Application firewall and three-layer ledger

1. **Chosen solver class:** this report certifies no all-input SAT procedure and no algorithmic time-space lower bound. CDCL/Resolution width remains a restricted baseline.
2. **Entire fixed proof calculus:** transferring an obligation potential to historical $R_{\mathrm{mix341}}$ requires one **sound, cost-nonexpanding MAY image of every native legal inference**, with original signed source, contexts, paid identities, branch discharge, definitions, GF(2), AND3, LOCAL-CONVERT and free lookup/zero-cost closure accounted for. Neither the complete source-to-obligation mapping nor a superpolynomial bound has been established. Result 545 argues that limiting candidate potentials to *atomic additive* forms risks severe gaps, even if such a mapping is later authenticated.
3. **Unrestricted machines:** neither B1, B2 nor the noncircular same-R B3 is established. The optional fixed-$r$ quasipolynomial bridge is OPEN. All-input Route A FLMV machinery remains separate and OPEN.

The next useful theorem is a **source-sensitive nonadditive potential** for a genuinely hard published 3-CNF family, with individually checked native mixed-rule marginal inequalities and a surviving goal threshold. LSPV-3 should authenticate each signed transition; LSPV-5 should challenge sponsor/origin duplication and missing zero-price shortcuts. A known rule defeating the proposed potential must be accepted, not forbidden.

**TRACKERS:** Both root proof files reviewed; the new [P2-L1-545] is a material restricted-method evidence entry only, with [P2-D1], [P2-C3], [P2-B1], [P2-B2] remaining OPEN. Complete current-blob+SHA tracker update and readback are recorded separately. Root main.tex retrieval returned a SHA but zero content bytes via the available full-file fetch; it was therefore NOT modified rather than overwriting a partial file. The prescribed local repository preflight and full report checker were NOT executed because no full git checkout was available; source/code/raw checks described above did run.

**P versus NP remains OPEN.**
