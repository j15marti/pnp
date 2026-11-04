# LSPV-3/380 | Aggregate XOR-row mass versus lazy proof-DAG certificate

November 3, 2026, 18:20 PST. Existing task, identity, enabled state, hourly schedule, Rmix341 calculus and ownership unchanged. **P versus NP OPEN.**

## Scope and exact result

Existing starting theorem: Urquhart (1987) and Ben-Sasson--Wigderson (2001) show exponential **ordinary DAG Resolution** lines on appropriate odd cubic expander-Tseitin 3-CNF formulas, with \(h\) vertices, \(3h/2\) edge variables, \(4h\) width-three clauses and indexed bit length \(N_h=\Theta(h\log(h+2))\). This is not a lower bound for arbitrary correct uniform SAT deciders. The unchanged fixed Rmix341 admits the earlier certified \(4h-1\) mixed AND3/GF(2) shortcut on the same family.

**New scoped theorem, independent specialist review pending.** For every odd-charge connected cubic graph \(G\) with \(h\ge12\), expansion \(\beta(G)\), and **every** legal binary XOR refutation stage with exactly \(h-1\) paid XOR additions of authenticated vertex rows, including any adaptive order or shared-DAG syntax,

$$
M(\pi)\ \ge\ \frac{\beta(G)h}{2}\log_2(h/6)-3h.
$$

Here \(M\) sums the fully expanded variable widths of all *derived* rows, excluding source rows. A constant-expansion family forces \(\Omega(h\log h)\) total expanded variable occurrences in every such minimum-node pure-XOR stage. Proof: odd-charge augmented incidence rows are linearly independent; \(h-1\) fan-in-two gates reaching \(h\) necessary source leaves form an unshared tree. A leaf-weighted centroid of a maximum-degree-three proof tree forces at least \(h\log_2(h/6)/2\) total smaller-side cut cardinality; graph expansion converts cuts to row widths; subtract \(3h\) source widths. This strengthens the prior LSPV-3/375 **maximal single-row** lemma but not the full mixed-system lower bound.

## Materialization counterexample

A pointer-DAG representation of the exact same XOR proof needs only \(h-1\) parent pairs, \(O(h\log h)\) bits. One fixed polynomial-time verifier authenticates all original signed parity quartets and verifies each pointer, source usage and the odd global charge without constructing all intermediate masks. By contrast, explicit fixed-width edge ID lists require \(\Omega(h(\log h)^2)\) output bits and dense full-row masks require \(\Theta(h^2)\) bits. These are representation-dependent *certificate* costs, not universal solver runtime. No hidden semantic oracle, no per-instance hardcoded result. Charge source parsing, indexing, construction, checking, output, caches, failed attempts, and simultaneous peak memory; retain all-phase rho in the resource envelope.

## Independent controls

The deterministic, seed-free exhaustive subset-partition DP gave exact aggregate stage minima 7, 15, 23, 31 for K4, K3,3, cube, pentagonal prism (h=4,6,8,10). Authentic parity source SAT controls: odd charge 0 models in each; even charge 8,16,32,64 models. Full local independent JS test passed 299,461 assertions. Separate compact verifier fetched back from GitHub and executed successfully using the authenticated raw ledger passed 149,945 assertions; both rejected six corrupted and four malformed fixtures. These finite results do not establish an all-size theorem by extrapolation and do not optimize longer XOR DAGs or mixed proofs.

Four falsifiers tested: minimum-node XOR gate sharing (disproved by tree edge count), impossibility of aggregate width amplification (disproved by centroid lemma), necessity of expanded row traffic in all representations (disproved by pointer-DAG check), and superpolynomial full-R hardness on Tseitin (false, full mixed linear shortcut).

## Corpus, source critique, and handoff

Read the specified November 2 12:04 refocus, commit 4e29ed7646f484707767acb6e63ec5f38afd98a8 / blob 033b54b87b7cbe94912af5cf67daa52859143a07, issue #3, AGENTS.md, CODEX.md, repo pnp-research skill, LSPV-3/375/378/379, LSPV-1/376, LSPV-2/375, LSPV-4/373 and LSPV-5/325. Prior single-row width and essential-source arguments adopted; no new hard family generated. Search terms: centroid XOR width, aggregate affine width, sum of cuts Tseitin, XOR tree layout, original primary Resolution papers, github.com/openai proof checker. No literature novelty asserted.

**Grok actual folder** GROKPROOF/2026-11-04_0116_PROGRESS.md, blob ca5a835356eb918b8cb4ab94d14de6174edeab03, identifies all-input fully charged ARC/FLMV transfer as OPEN. **Claude actual folder** research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67 (restricted alternation trading); research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a (restricted sequential access). Neither resolves B3. LSPV-5/325's recognizable-island encoding counterexample remains a mandatory semantic-transfer control.

## Published repository outbox

- research/agents/lspv-3/2026-11-03_1820_LSPV-3_CENTROID_XOR_ROW_MASS380.tex
- experiments/arc/lspv3_380_row_mass.py
- experiments/arc/lspv3_380_independent_verify.js
- results/raw/arc/2026-11-03_1820_LSPV3_CENTROID_XOR_ROW_MASS380_raw.json
- research/coordination/2026-11-03_1820_LSPV3_CENTROID_XOR_ROW_MASS380_FIVE_ROLE_HANDOFF.md

Create-only writes, precise current-head checks and full readback required. The local full reproducibility archive also contains separately written scripts, full finite certificates and controls. Complete local checkout unavailable; no claim of repository-wide preflight or report-check pass. Main.tex must only be edited from an authenticated complete blob within the LSPV-3 ownership region and verified byte-for-byte outside it.

**Next task:** test a source-rooted cost-reflecting invariant under lazy XOR, conservative gates, compact root-only circuits and the actual typed full LOCAL-CONVERT rule. Superpolynomial full-R minimum, B1, B2, B3 and P versus NP remain OPEN.
