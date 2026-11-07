# LSPV-4/479 | Cubic-expander packet-frontier obstruction for PATH and binary TREE3 layouts

**2026-11-07 14:40 PST | Route A resource auditor | PROVED/RESTRICTED symbolic structural bounds; COMPUTATIONAL finite exact layout optima | P versus NP OPEN**

**Tracker IDs:** Material restricted gap/evidence at **[P2-A4]**. Load-bearing **[P2-A2]** (uniform all-input contraction), **[P2-A5]** (recursive same-machine applicability) and **[P1-01]**, **[P1-03]**, **[P1-04]** remain OPEN. Separate mixed-calculus **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]** remain OPEN. Historical `R_mix341` grammar, weights, proof DAG optimization and all existing roles are unchanged.

## IDEA -> SEARCH -> ITERATE and falsifiers

**Hypothesis.** An *original-packet-preserving* decomposition of a known odd-charge 3-regular expander Tseitin 3-CNF into small original-source blocks cannot have logarithmic literal interfaces, **even if** blocks are ordered adaptively or arranged in an arbitrary rooted binary tree. The point is a quantitative restriction on the specific original-variable, literal-boundary compiler, **not** hardness of arbitrary algorithms.

**Predictions/falsifiers, declared before construction:** (F1) packet regrouping into blocks of at most $K=o(H)$ might evade the familiar single-packet frontier lower bound; (F2) binary reconvergence might evade all large cuts by choosing a different hierarchy; (F3) an algebraic XOR or legal extension-variable shortcut might disprove an attempted inference from interface width to actual machine hardness; (F4) exact finite minima might disagree between independent subset DP and threshold-reachability programs or fail original SAT/UNSAT and malformed-packet controls.

**SEARCH and continuity.** Read both complete current proof-chain trackers and coordination issue #3; governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, LSPV-2/457 (blob `3a6cd30d73af1bf3b1bb3431a73eeb80f3e25de5`), LSPV-2/476 (blob `94a1ba7fc5dc2073fe87b422ed61f9a80113666c`), LSPV-2/477 (blob `3b4e01f7218f523fd895e4f2178a93175d91989d`), LSPV-4/478 (blob `f11604d838f0ce459fd68872b9e67d3aa708bb69`), current Grok `GROKPROOF/2026-11-07_1920_PROGRESS.md` (blob `231561ce216699f286b705a0056584789ba9ee99`) and actual Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`. LSPV-2/457 **already mentioned** a qualitative $\Omega(H)$ expander frontier. The substantive strengthening here is an **explicit $K$-versus-$w$ tradeoff for arbitrary packet blocks and binary trees**, with separately certified finite optimums; the underlying expansion idea is standard, not claimed novel.

**Primary sources:** Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48(2) (2001), ECCC original https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/ (ordinary shared-DAG Resolution, not the fixed mixed calculus); Fortnow et al., *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), https://doi.org/10.1145/1101821.1101822 (indexed random-access uniform machine model, not a syntactic frontier theorem). Reviewed standard separator/pathwidth discussions and the project's Kinnersley 1992 control through LSPV-2/338. External repository paths actually checked: `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` (finite-machine P subseteq NP only), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (bounded techniques), `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab` (original parity generator), `meelgroup/frat-xor/README.md` blob `38a137bca4d4ab6443703d4c31fba5783021c581` (external proof checker), `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` (raw research stages, not an all-SAT theorem). No separate branded Google interface or native FLMV instruction-level simulator was used.

**ITERATE.** The earlier packet-by-packet cutwidth observation survives arbitrary bounded **block aggregation**. For binary trees a stronger balanced-subtree lemma supplies the obstruction with internal packets permitted. Conversely XOR summation is a legitimate **cheap algorithmic shortcut** on these exact sources, so the result must remain a structural non-applicability firewall rather than a runtime lower bound.

## Exact published-family control: cubic-expander Tseitin strict signed 3-CNF

Let $G_H=(V,E)$ be a connected simple **3-regular edge expander** with even $H=|V|$, $|E|=3H/2$ and uniform edge-expansion $\varepsilon>0$:

$$
|\delta(S)|\ge\varepsilon\min(|S|,H-|S|)
\quad\text{for all }S\subset V.
$$

Give every original edge $e$ its own Boolean variable $x_e$. For each vertex $v$ with distinct incident original edges $e_1,e_2,e_3$ and charge $b_v$, place **exactly four proper signed ternary clauses**, one forbidding each three-bit tuple with parity different from $b_v$. Thus the packet is precisely $x_{e_1}\oplus x_{e_2}\oplus x_{e_3}=b_v$. Choose $\bigoplus_v b_v=1$. XOR of the equations gives $0=1$, certifying UNSAT.

The original encoding has $4H$ strict 3-clauses, $3H/2$ original variables, and $12H$ signed literal occurrences. With $W=\lceil\log_2(3H/2+1)\rceil$ identifier bits, a canonical explicit packet stream needs $N=12H(W+1)+O(\log H)=\Theta(H\log H)$ bits. For suitable growing cubic expanders, the published Ben-Sasson–Wigderson/Urquhart analysis gives refutation size $2^{\Omega(H)}$ in **ordinary shared-DAG Resolution**. Neither the expander promise nor the ordinary Resolution theorem establishes hardness against all SAT algorithms, stronger GF(2) rules, extensions, or full historical `R_mix341`.

## Theorem 479.1 (PROVED/RESTRICTED): blocked PATH frontier

A *packet-preserving original-variable block layout* assigns each of the $H$ complete four-clause vertex packets to exactly one ordered block $B_i$, with at most $K<H/2$ packets per block. There is **no cloning, renaming, semantic elimination, extra-variable factoring or compression**. For each cut after a block, every original edge variable occurring on both sides must be explicitly carried in the literal interface $Z_i$. Let $w=\max_i|Z_i|$.

Then for **every block order and partition**,

$$
\boxed{w\ge \varepsilon(H/2-K).}
$$

**Proof.** Select the last block-boundary prefix $S$ of vertices having $|S|\le H/2$. The next block has at most $K$ vertices, so $|S|>H/2-K$ (the bound also holds if a prefix is empty). Each $e\in\delta(S)$ occurs in a packet before and a packet after this cut, hence its original variable must cross the interface. The $|\delta(S)|$ variables are distinct. Expansion gives $w\ge|\delta(S)|\ge\varepsilon|S|>\varepsilon(H/2-K)$. QED.

## Theorem 479.2 (PROVED/RESTRICTED): arbitrary binary TREE3 frontier

Assign the $H$ complete original packets to nodes of an arbitrary rooted tree with at most **two children per node**, at most $K<H/3$ packets at each node, and a complete binary OR/AND decomposition permitted **only as a source-layout tree**. Every original variable whose packet occurrences lie inside and outside a descendant subtree must be carried through that subtree's parent interface. Then

$$
\boxed{w_{\mathrm{tree}}\ge \varepsilon(H/3-K).}
$$

**Proof.** Descend the rooted tree to a lowest subtree $T$ containing at least $H/3$ original vertex packets. Both child subtrees contain fewer than $H/3$ packets and the root node of $T$ owns at most $K$, so $H/3\le|T|<2H/3+K$. Since $K<H/3$, its complement has more than $H/3-K$ packets. Therefore $\min(|T|,H-|T|)>H/3-K$. Every original edge crossing $T$ versus its complement has one source-packet occurrence on each side, so its source variable must cross the single parent interface. Expansion gives $w_{\mathrm{tree}}\ge|\delta(T)|\ge\varepsilon(H/3-K)$. QED.

**Application and limitation.** In both compiler layouts a child/source node of at most $N^{1/2+o(1)}$ **actual source bits** contains at most $K=O(N^{1/2+o(1)}/\log H)=o(H)$ original complete packets. Thus both proofs require $w=\Omega(H)=\Omega(N/\log N)$, incompatible with LSPV-2/457's $w\le(\log_2 N)/10+o(\log N)$ restricted promise. This is a *quantified syntactic source-preservation obstruction* to extending that literal-interface compiler by a different grouping/order/tree alone. It does **not** forbid polynomially charged semantic GF(2) reduction, auxiliaries, learned lemmas, a different source representation or an all-input transformation.

## Finite exact optima and independent controls (COMPUTATIONAL)

The self-contained JavaScript optimizer computes exact minimum maximum boundary size for (i) a sequential partition into blocks of at most $K$ whole packets and (ii) a rooted binary tree whose leaves contain at most $K$ whole packets. It uses explicit subsets, edge-cut counts and exact min-max recurrences. The tree finite optimizer is **leaf-block only**; Theorem 479.2 additionally allows packets at internal nodes. Independent Python uses thresholded reachability/recursive feasibility, not the JavaScript numerical DP.

| Original cubic graph | H | K | Exact PATH width | Exact binary-tree width |
|---|---:|---:|---:|---:|
| K4 | 4 | 1 | 4 | 4 |
| K3,3 | 6 | 1 / 2 | 5 / 4 | 4 / 4 |
| cube Q3 | 8 | 1 / 2 / 3 | 5 / 4 / 4 | 4 / 4 / 4 |
| Petersen | 10 | 1 / 2 / 3 | 6 / 5 / 5 | 5 / 5 / 5 |
| prism C6 x K2 | 12 | 1 / 2 / 3 | 5 / 4 / 4 | 4 / 4 / 4 |

The JavaScript reports 65,367 enumerated/checked finite configurations, including exhaustive permutation checks for $H\le8$, and stored explicit optimal PATH partitions. Independent Python confirmed **24** exact PATH/TREE minima by a distinct threshold-feasibility method. Separately, **original signed strict 3-CNF clauses** were constructed and exhaustively evaluated over 9,344 assignments on K4, K3,3 and Q3, with even/odd model counts 8/0, 16/0 and 32/0; twelve altered-sign/duplicate-literal packet controls were rejected as **out of this authenticated parity-packet family** (not as malformed general CNF).

### Full computation-cost distinction

The **finite offline exact optimizer** uses subset DP with up to $2^H$ resident subset entries, $O(3^H\operatorname{poly}(H))$ enumeration work and explicit parent pointers; it is NOT a universal polynomial SAT solver. Source/edge parsing, subset masks, edge cuts, all failed candidate partitions, min-max comparisons, allocation, proof-witness reconstruction, output and simultaneous peak are paid in that exponential finite optimizer. The **structural theorem** charges no discovered-layout cost because it is a universal statement about *all layouts*, not a proposed executable SAT solver. A real solver using the source layout must additionally charge grammar acquisition, input/INDEX/head reads, child construction, guest time/work, caches, recomputation, branch joins, output and all simultaneous ancestor/child buffers. No valid FLMV-native $(t',s')$ exponents are inferred from these finite computations.

**Mandatory shortcut control.** Given the authenticated parity-packet structure, XOR of all vertex charges decides the Tseitin **SAT/UNSAT** label for connected $G_H$: odd total charge UNSAT, even total charge SAT (the latter is solvable by a spanning-tree incidence assignment). For fixed known graph source layout, this is a low-cost algebraic algorithm even though the original source has exponential **ordinary Resolution** refutations and linear literal frontiers. This directly falsifies any attempt to equate the present large syntactic interface with general algorithmic time or space hardness. The native GF(2)/conversion permission for historical `R_mix341` is unchanged and must be checked, not assumed.

**Next precise transfer gap:** For [P2-A2] an effective transformation must break one of the packet/layout hypotheses through a *paid* authentic semantic compression, source decomposition, extension or alternative solver representation, and show all-input correctness and recursive same-FLMV applicability [P2-A5]. Neither a forbidden algebraic shortcut nor exponential offline layout enumeration is a legal free operation. For Route B, ordinary Resolution's published lower bound still requires all-rule transfer plus noncircular B3; none is supplied here. **P versus NP OPEN.**

**Published reproducer:** `experiments/arc/lspv4_479_packet_frontier.js` (blob `ee250db0595e6b67cfd460517f9cf981fa7b1403`); independent `experiments/arc/lspv4_479_independent.py` (blob `8aa05da826548818a49923a0f166e8b51f845288`); original-source `experiments/arc/lspv4_479_source_controls.py` (blob `5934e4e6b70236b2743fedbbfad0f70bdafa68c2`); raw `results/raw/arc/2026-11-07_1440_LSPV4_479_PACKET_FRONTIER_RAW.json` (blob `1bb20a790d596e9fa9a32dcc21aad5729fba2ac6`). Root `main.tex` must only be edited inside LSPV-4 ownership markers after complete authenticated readback; do not replace a truncated source.
