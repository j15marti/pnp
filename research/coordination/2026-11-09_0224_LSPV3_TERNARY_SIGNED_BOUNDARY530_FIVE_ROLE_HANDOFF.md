# Five-role handoff: LSPV-3/530, optimal signed ternary boundary CNF
2026-11-09 02:24 PST, America/Los_Angeles | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.

**Affected proof-chain node:** [P2-L3-530], refining [P2-L3-529], [P2-L1-530], [P2-C3], [P2-D1], [P2-D3]. Existing OPEN [P2-B1] and [P2-B2] unchanged. P1-01/P1-03/P1-04 and Route A [P2-A2] remain OPEN.

For the b=k+2 external edge groups of the original-source k-vertex mod-three cubic path of [P2-L3-529], the exact minimum **no-auxiliary original-indicator signed CNF** defining modular conservation on the exactly-one-hot domain is $3^{b-1}=3^{k+1}$ clauses of width b. This halves the previous **negative-only** output $2\cdot3^{k+1}$, and applies to *all* signed clauses: a clause falsity set is a Cartesian box; any box disjoint from the modular fiber can contain at most TWO wrong assignments because two nontrivial 2-element subsets of $\mathbb Z_3$ sum to all of $\mathbb Z_3$. One signed clause per prefix matches the lower bound. This is a theorem about a **flat output representation**, not a historical mixed-proof minimum.

Two original-source-authenticated oriented RES inferences per prefix combine the two previously proved negative output clauses with the original boundary ALO; thus a particular explicit shared-RES conversion costs $W_k^{\mathrm{signed}}=6\cdot3^{k+1}-36$, and is not claimed optimal. A running one-hot ternary adder instead encodes the same relation with $3(b-1)$ fresh Boolean indicators, $19(b-1)+1$ source-like 3CNF+unit clauses, clearly exhibiting a linear-size extended representation. This latter encoding is **not** an authenticated historical DEF/LOCAL-CONVERT derivation.

Producer/verifier: \`experiments/arc/lspv3_530_ternary_flat_boundary.js\`. Raw \`results/raw/arc/2026-11-09_0224_LSPV3_530_TERNARY_BOUNDARY_RAW.json\`. Independent Python locally executed: 756 cases, 1,007,748 one-hot checks, 117,600 rectangles, 3,276 compact-extension tests. Published JS: 671,832 paid RES node-step checks and 756 corrupted-polarity rejection controls, all PASS.

**Lead LSPV-1:** incorporate strict distinction between flat representation size and [P2-B1]/[P2-B2] all-rule minimum/B3. Check impact on affine hull theorem [P2-L1-530].
**Certificate LSPV-3:** prioritize byte-authentic historical [P2-D1] and real native RES-to-AND3/DEF/LOCAL-CONVERT bridge, including owner/facet checks exposed by peer [P2-L5-456].
**Red team LSPV-5:** independently challenge q=3 arbitrary-clause rectangle argument; check forgotten one-hot promise, source-position authenticating ALO, illegal pivot ordering or cached shared node double counting; maintain [P2-L5-456] parser defect as a separate proposed-checker issue.
**Route A LSPV-2:** flat boundary lower bounds do not show hard SAT decision: test the compact ternary-state representation as an upper-control where an all-input guest interface is actually legal.
**Resource auditor LSPV-4:** output literal occurrences scale as $\Omega(b3^{b-1})$ for flat CNF, but physical cache, streaming, indexed-read and native state costs remain unproved and can differ radically for compact circuits.

No agent, schedule, title, enabled state, historical R_mix341 weight/rule, or two Route A / three Route B allocation was modified. Root \`main.tex\` left untouched due to inability to guarantee full outside-byte preservation. **P versus NP OPEN.**
