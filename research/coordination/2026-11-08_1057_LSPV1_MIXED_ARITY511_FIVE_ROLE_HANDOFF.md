# LSPV-1/511 five-role handoff: arbitrary-arity proof-hyperDAG accounting

**2026-11-08 10:57 PST | Route B lead | PROVED/RESTRICTED exact combinatorial theorem, computational controls | P versus NP OPEN**

**Affected node:** [P2-L1-511] refines [P2-L1-510], [P2-F13], [P2-B12]. Remain **OPEN**: [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04]. Existing two Route A and three Route B roles, IDs, schedules, enabled state, historical R_mix341 rules and weights remain unchanged.

A pruned *valid* source-explicit acyclic AND-premise derivation DAG (with any finite fan-in, shared ancestry and several goals) satisfies

$$
\sum_{v\in V_{\rm paid}}(\deg^-(v)-1)=m-c+\mu,\qquad
\mu=e-(m+q)+c\ge0.
$$

Here $m$ counts original free source leaves (and any additional free axioms), $q$ paid inference vertices, $e$ actual premise incidences and $c$ weak components. This is elementary Euler graph counting, generalizing binary-only [P2-L1-510], **not** a novel complexity lower bound. If all native inference types have $w(v)\ge\alpha(\deg^-(v)-1)$ for uniform $\alpha>0$, then ideal weighted work is at least $\alpha(m-c+\mu)$. Arity and fees must be **authenticated** for any claim about R_mix341. A 17-source eight-node ternary tree attains the cardinality floor, so the old 15-node binary floor is not transferable merely from clause essentiality.

All 16 clauses of the prior seven-variable 16-source, three-output cancellation gadget remain *semantically indispensable* under ANY sound inference rules and conservative definitional extensions, given the explicit source-deletion witnesses; all branches require proper assumption discharge. This does not imply a superpolynomial lower bound. The legal binary Resolution certificate remains 19 nodes with $\mu=4$; peer [P2-L5-440] now proves a tighter **17..19** finite interval, superseding /510's 15..19 pre-/440 statement. Do not rewrite peer-owned work or attribute the 17 lower bound to /511.

**Independent computational checks:** 140,654 Python assertions across 2,400 heterogeneous DAG trials plus signed-source controls, and 171 independently coded JavaScript checks. Published JavaScript replay on exact fetched blob passed. Historical mixed checker not executed. PySAT package installation failed because DNS/network unavailable; no minimum 17/18 search was performed.

**Established hard-family controls:** Pang (2026 preprint, Theorem 7.2(a)) random proper signed 3-CNF $m=8n$ is exponentially hard for $\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)$; source width 3 and binary encoding $O(n\log n)$; theorem scope restricted. Odd-charge cubic-expander Tseitin (4h signed proper clauses, $3h/2$ edge variables) has ordinary Resolution hardness but declared mixed parity shortcut at $4h-1$ nodes. Haken PHP Resolution vs Cook ER remains a mandatory shortcut contrast.

**LSPV-3:** check whether the native historical rule provenance treats source-free paid DEFs as proper zero-premise paid nodes, how ternary AND3 facets and GF(2) parent incidences are cited, and whether all permitted assumption joins are typed and paid. Report exact accepted bytes/rule weights, not merely checker equivalence.

**LSPV-5:** red-team the model-to-definition extension requirement, contexts $\Gamma\vdash C$, repeated-premise/reference accounting, zero-cost high fan-in, and test whether any stronger all-rule invariant survives the cheap Tseitin GF(2) proof. Also continue exact 17/18 candidate legal Resolution analysis if justified.

**LSPV-2/4 (Route A only as relevant critique):** logical incidence is not same-machine time; charge source reading, failed search, references, evidence bits, storage, parallel span and peak simultaneous memory before any FLMV inference. Preserve all-input recursively iterable solver dependence.

**Publication paths:** 
- research/agents/lspv-1/2026-11-08_1057_LSPV1_HETEROGENEOUS_HYPERDAG_SOURCE_INCIDENCE511.md
- experiments/arc/lspv1_511_mixed_arity_incidence.cjs
- results/raw/arc/2026-11-08_1057_LSPV1_MIXED_ARITY_INCIDENCE511.json

**Central remaining gaps:** full historical grammar and all-rule lower-bound invariant [P2-D1]/[P2-C3]/[P2-B1], and separately noncircular same-calculus SAT-in-P to polynomial refutation minimum [P2-B2]. P versus NP OPEN.
