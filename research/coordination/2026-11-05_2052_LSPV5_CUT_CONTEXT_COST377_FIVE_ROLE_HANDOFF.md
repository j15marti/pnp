# LSPV-5/REFEREE377 five-role handoff | 2026-11-05 20:52 PST

**Route B primary. PROVED/EXACT RESTRICTED + COMPUTATIONAL. P versus NP OPEN.** Existing 2A/3B allocation, roles, schedules, task identities, native rules/weights, and `main.tex` are unchanged.

**Idea -> search -> iterate.** The initial rejecting-trace idea duplicated REFEREE363 and was dropped. The revised target audited LSPV-3/438's $2^{k-3}$ cut-context statement against the historical wide-GF(2) rule. Four falsifiers: incorrect original-source cut projection, a smaller subcube cover, forbidden wide XOR, or omitted antecedent work. The first three fail; the fourth fixes the scope.

**Exact restricted theorem:** if all $2^k$ parity-boundary assignments must be covered by leaf subcubes leaving at most three coordinates free, each leaf covers at most eight assignments, so at least $2^{k-3}$ are required. Fixing any $k-3$ coordinates gives a matching disjoint cover. Before $k-3$ pins every projection onto at most three unpinned coordinates is full; at the threshold a nontrivial parity relation remains.

**Native firewall:** this leaf count is not a historical $R_{\mathrm{mix341}}$ work lower bound. Two already-derived opposite $k$-wide rows XOR to $0=1$ in one paid native node and use zero branch contexts. On the authenticated odd-$K_4$ strict-3 control, $S=\{0,1\}$ and its connected complement export opposite four-wire rows. The full mixed proof remains the established exact 15 nodes (12 AND3 + 3 XOR); only the final combination is one node.

**Work/span/space:** a proposed paid full split tree has $L=2^{k-3}$ leaves, $L-1$ internal nodes and span $k-3$ plus leaf closure. Materializing contexts takes $L(k-3)$ fixed-bit records; DFS needs $O(k)$ live context plus leaf proof. None is a historical weight until split/discharge and assumption labels are natively specified. If contexts are free, leaf count alone gives no $W_R$ lower bound.

**Verification:** producer 33,811 checks, independent Node 8,303, and exact replay of LSPV-3/438 compact source 1,356. Odd/even original sources, exact hashes, 64-assignment labels, both cut projections, malformed header, corrupt literal, and same-row XOR control. These are semantic checks, not authoritative accepted trace bytes.

**Artifacts:**

- report `research/main/2026-11-05_2052_MAIN_CUT_CONTEXT_COST_FIREWALL_REFEREE377.md`;
- producer `experiments/review/lspv5_377_cut_context_cost_firewall.py`;
- verifier `experiments/review/lspv5_377_independent_verify.mjs`;
- raw `results/raw/review/2026-11-05_2052_LSPV5_CUT_CONTEXT_COST377.json`.

**Role actions:** LSPV-1 should require a polynomial full-rule context simulation before using branch counts in $\overline W_R$; LSPV-3 should label $2^{k-3}$ strictly as the proposed split-to-localize optimum and retain the zero-context GF(2) control; LSPV-2/4 may use the work/span/space separation only as periodic peer critique, not as Route-A transfer. LSPV-5 next attacks any claim that restricted branch contexts survive DEF/RES/GF(2) reconvergence. B3 and the full mixed lower bound remain OPEN.
