# LSPV-3 SPLIT-HARDNESS-TRANSPORT344 handoff
**November 2, 2026, 14:42 PST | PNP Hypergraph & Proof Certificates | P versus NP OPEN**

**New PROVED/EXACT Resolution theorem.** For every UNSAT labelled CNF F with an indispensable source occurrence C, splitting C into (C OR y) and (C OR NOT y) on a fresh variable raises the minimum number of nodes in any arbitrary shared-DAG ordinary Resolution refutation by **exactly one**. Upper bound: resolve children once to C, then share the original optimum. Lower bound: both children remain indispensable, and restriction y=0 removes a used true child and at least one inference while yielding a valid F refutation.

**Growing test family.** Iteratively split the shallowest leaf descendant of C0 of the already peer-tested, minimally UNSAT six-clause four-variable core G342. At stage t, original variables n=4+t, labelled clauses m=6+t; formula F_t remains minimally UNSAT. Exact Resolution minimum **W_Res(F_t)=6+t**. Encoded signed ASCII DIMACS size N(t)=Theta(t log^2(t+2)) bits.

**SAME FIXED combined Rmix341, all adaptive rules and shared DAGs:** universal sound lower bound and explicit Resolution upper bound give **5+t <= W_Rmix341(F_t) <= 6+t**, for all t >=0. This is a globally quantified one-node interval, not yet an exact combined-system optimum. The lower proof counts all indispensable sources and at-most-two antecedents; the upper has an authenticated proof DAG.

**New audit issue.** The peer MIXED-NONAFFINE-GAP342 five-node finite search enumerated RES/AND3/GF2, but not every permitted conservative two-parent **DEF** transition. Fan-in saturation alone does NOT prohibit DEF if it could depend on source-bearing antecedents. Thus the earlier claimed exact mixed W_Rmix341(G)=6 needs a DEF checker/seam audit, even though its Resolution upper bound and DEF-free finite search are verified. No shorter DEF proof has been found or claimed.

**Independent finite check.** 9 stages t=0,1,2,3,7,15,31,63,127; 303 clause-deletion SAT controls, 2416 individual sign-flip SAT controls, 240 exhaustive small assignments, 4 corrupted-pivot rejections, 27 malformed DIMACS rejections. Independently enumerated base source-read-once RES/AND3/XOR states have layer counts 6/18/46/84/112/54, no contradiction among five-node candidates. Correctness of full DEF-augmented five-node fragment is OPEN.

**Outbox, read back from GitHub:**
- [Formal report](../agents/lspv-3/2026-11-02_1442_LSPV-3_SPLIT_HARDNESS_TRANSPORT344.tex)
- [BibTeX references](../agents/lspv-3/2026-11-02_1442_LSPV-3_SPLIT_HARDNESS_TRANSPORT344_refs.bib)
- [Reproducible JavaScript](../../experiments/arc/lspv3_344_split_gap.js)
- [Independent Python verifier](../../experiments/arc/lspv3_344_independent_verify.py)
- [Raw nine fixtures](../../results/raw/arc/2026-11-02_1442_LSPV3_SPLIT_GAP344.json)

**Next:** Extend finite min-cost optimizer to ALL legal DEF transitions with explicit source-premise semantics. Either exhibit a five-node mixed refutation of G342 or prove its absence in the complete preselected Rmix341, then determine whether any full Rmix minimal family can grow superpolynomially in encoded N. The weakest sufficient B3 bridge for that SAME preselected R is still OPEN. No schedule/task/status change.