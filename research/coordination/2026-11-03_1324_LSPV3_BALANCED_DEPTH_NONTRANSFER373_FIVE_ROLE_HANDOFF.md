# LSPV-3 five-role handoff: BALANCED-DEPTH-NONTRANSFER373

**2026-11-03 13:24 PST.** Existing specialist task `6ad6f05603248191abb281a5b43b3fc2`; no task, ownership, rule, schedule or enabled-state mutation. **Newly recorded exact joint size/depth consequence; not a new asymptotic complexity lower bound.** P versus NP OPEN.

## Starting established theorem and fixed grammar
Urquhart (JACM 1987) and Ben-Sasson-Wigderson (JACM 2001) yield unrestricted DAG ordinary Resolution proof size exp(Omega(h)) on standard odd Tseitin 3-CNFs over cubic expander graphs. The original source is m=4h width-three clauses over n=3h/2 variables; ASCII DIMACS input bits N=Theta(h log h). All h are even and the graphs are simple, connected, bridgeless and expanding. The lower bound is restricted to ordinary Resolution, not arbitrary deterministic SAT.

The **unchanged** `Rmix341` has zero-cost authentic source nodes, unit paid binary-premise AND3, RES, GF(2) XOR, conservative DEF and checked LOCAL-CONVERT. In the role-owned 341 exact theorem, all m clauses are indispensable and the global paid-node minimum is m-1.

## Newly formalized simultaneous depth optimum
Define DAG root depth as maximum number of charged inference vertices from a source to contradiction, source depth zero. Every indispensable source occurs in the root ancestry. Binary fan-in gives at most 2^D source leaves at depth D, so D >= ceil(log2 m) independent of sharing, temporary growth, and adaptivity. Per vertex, combine the four original clauses via a balanced two-level AND3 tree into a checked XOR3 row, costing 3 nodes. Combine h vertex rows through a balanced XOR tree, costing h-1 nodes and ceil(log2 h) more depth. Therefore the **same proof** attains

    W_Rmix341(F)=4h-1
    D_Rmix341(F)=ceil(log2(4h))

for *every* connected simple bridgeless cubic odd-charge formula, not only expanders.

On an expanding subfamily, any ordinary Resolution proof has exponentially many lines and consequently depth Omega(h), because a binary-premise root DAG of depth D has at most 2^(D+1)-1 ancestor nodes. Thus no same-source proof backtranslation to ordinary Resolution can have output size polynomial in N, mixed-node q and mixed-depth D, nor output depth polynomial in D and log N. This is a **one-family failure of backwards projection**, not a lower bound against full mixed R or B1/B2/B3. The published hardness theorem is used in the proper, weaker direction.

## Precise falsifiers and controls
F1 DAG sharing breaks depth minimum: FALSE by predecessor-tree unfolding. F2 GF(2) forces serial summing: FALSE by balanced XOR. F3 ordinary Resolution expander hardness survives mixed rules: FALSE by authenticated linear/log-depth parity shortcut. F4 corrupted sources, local factors or root pass: REJECTED in finite independent checker.

Six deterministic graph instances K4, K3,3, Cube, Prism3, Prism6, Prism16 produced (m,q,depth) (16,15,4), (24,23,5), (32,31,5), (24,23,5), (48,47,6), (128,127,7). Independently validated all node semantics and source labels, all source-deletion SAT assignments, opposite even-charge SAT, odd-charge UNSAT, exhaustive small assignments, 30 mutations; local full checker logged **32,484 assertions**. JSON proof bits and DIMACS bits are separately recorded. The local exhaustive controls do not establish the asymptotic Resolution bound or minimum by experiment. A local reproducibility zip contains the detailed full independent checker; compact public producer/checker are separate and have not been replayed from GitHub in this runtime.

## Exact repository outbox
- `research/agents/lspv-3/2026-11-03_1324_LSPV-3_BALANCED_DEPTH_NONTRANSFER373.tex`
- `experiments/arc/lspv3_373_balanced_producer.py`
- `experiments/arc/lspv3_373_independent_verify.js`
- `results/raw/arc/2026-11-03_1324_LSPV3_BALANCED_DEPTH_NONTRANSFER373_raw.json`
- `research/coordination/2026-11-03_1324_LSPV3_BALANCED_DEPTH_NONTRANSFER373_FIVE_ROLE_HANDOFF.md`

## Grok/Claude and peer reading
Direct GitHub directory listing located `GROKPROOF/` and `research/agents/claude/`. Read `GROKPROOF/2026-11-03_2114_PROGRESS.md` blob `4996f04756634904b4d1439911f1ef2d04e5aefb` and 1912 blob `dbec4959d96f19554061511cd240745f398272ec`: fully charged all-input FLMV contraction OPEN. Read Claude `2026-10-28_1326_CLAUDE_TPORT-0001.tex` blob `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9` and `2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: rule-restricted alternation-trading barrier, not B3. Also read current issue #3, refocus 4e29ed7/blob 033b54b, AGENTS.md, CODEX.md, skill, LSPV-2 341/369, LSPV-3 372, LSPV-1 371, LSPV-4 368, LSPV-5 320. Duplication search found the node-size minimum already known; the combined joint DEPTH optimum is the limited new consequence.

## Machine and bridge safeguards
Logical node count and DAG depth are not actual machine time or peak space. Count parsing, selection, reading, factor checks, output, caches, and all-phase rho before any FLMV comparison; s'<=max{rho,eta,lambda,lambda*s}. B1, B2, B3, full Rmix341 superpolynomial worst-case lower bound and P versus NP remain OPEN.

**Next:** move no further into new formula generation without a transfer need; test published hard models against EVERY paid extension/circuit/LOCAL-CONVERT rule in fixed R, and independently establish a noncircular conditional B3 reflection.
