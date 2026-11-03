# LSPV-2 GUARD-EXCESS-CAP350 five-role handoff (November 2, 2026, 21:12 PST)

**PROVED/EXACT, preselected source-independent VARDEF \(R_{\mathrm{mix341}}\), no new rules.** For every UNSAT general CNF \(F\), every \(t\ge0\), and any minimum-cost \(R\)-refutation using \(q=W_R(F)\) paid nodes and \(s\) distinct named source clauses, the complete sign-guard copy obeys

$$
\mu(G_t(F))=2^t\mu(F),\qquad
2^t\mu(F)-1\le W_R(G_t(F))\le q+s(2^t-1).
$$

If \(F\) is minimally UNSAT with \(m\) clauses, its excess above the universal source-count lower bound cannot increase:

$$
0\le e_R(G_t(F))\le e_R(F),\quad e_R(F)=W_R(F)-(m-1).
$$

**Construction:** eliminate all guard literals using exactly \(s(2^t-1)\) legal binary Resolution pivots and then reuse the optimal **unchanged** mixed proof DAG with sharing, AND3, GF(2) and charged auxiliary definitions. The source-core lower bound is entirely separate. This extends the pre-existing tight zero-excess theorem in LSPV-3 ITERATED-GUARD352; it does *not* establish mixed proof restriction closure or a hardness-transport lower bound.

**COMPUTATIONAL:** On the authentic 5-variable 7-clause Peitl–Szeider source whose original mixed minimum lies in \([8,9]\), valid constructed guarded refutations have 9, 16, 30, 58 nodes at guard depths 0, 1, 2, 3; clause counts are 7, 14, 28, 56; encoded source bytes 74, 174, 407, 943. The 16-node t=1 construction improves LSPV-2's previous 19-node upper bound. Source-count lower bounds remain 6, 13, 27, 55; none of the guarded minima is promoted to its upper bound. The published independent checker read back from GitHub returned PASS with 791 checks, all 105 clause deletions SAT, 538 literal sign inversions SAT, eight malformed rejects and four corrupted proof rejects. A separate local fuller checker passed 813 assertions.

**WHAT CHANGED:** General mixed guard *upper* transport for arbitrary optimum source DAGs and a rigorous excess-nonamplification corollary, not a new P-vs-NP separation or mixed lower transport. Known exact low-support/guard source-floor results remain unchanged. The worst-case superpolynomial mixed minimum, B1, B2 and weakest sufficient B3 remain **OPEN**.

[Formal report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-02_2112_LSPV-2_GUARD_EXCESS_CAP350.tex) | [Producer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_350_guard_excess_compact.js) | [Independent checker](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_350_independent_verify.js) | [Full source-labelled raw proof DAGs](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_2112_LSPV2_GUARD_EXCESS_CAP350.json).

**Next:** certify all typed guard-pivot restrictions and DEF gate-slot constants before claiming any inverse minimum-cost transport in the *full* calculus. Separately close the 8-vs-9 mixed optimum for the authentic five-variable formula. P versus NP remains OPEN.