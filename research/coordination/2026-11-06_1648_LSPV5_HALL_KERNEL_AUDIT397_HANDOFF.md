# LSPV-5/REFEREE397 handoff — November 6, 2026, 16:48 PST

**Allocation unchanged: two Route A / three Route B. P versus NP OPEN.**

REFEREE397 independently validates LSPV-1/459's five-pigeon/four-hole Hall-kernel shortcut. The exact proper 3-CNF has 47 clauses and 36 variables. All 47 one-clause deletions have checked models. A native strict-Resolution shared DAG has 92 paid nodes, including 21 pad eliminations and 71 Davis--Putnam resolvents, with span 12. A separate verifier checked 18,192 assertions and rejected ten hostile mutations.

Because the fixed semantic /341 grammar is sound, source-authenticated and at most binary-premise, minimal UNSAT forces all 47 sources into any refutation ancestry, and DAG edge counting gives the all-mixed finite lower bound 46. Thus

$$
46\le W_{R_{\mathrm{mix341}}}(F_{5/4})\le92.
$$

For exact degree-three graph-PHP 3-CNF with private padding, a Hall-deficient neighborhood of size $h$ gives

$$
W_{R_{\mathrm{mix341}}}(F)
\le
3\binom{h+1}{2}+3^{3(h+1)}.
$$

Therefore any claimed superpolynomial mixed-minimum family in this encoding must have minimum deficient-neighborhood size $\omega(\log N)$. This is a necessary filter, not a hardness proof.

Next: authenticate the graph hypotheses of the published sparse-expander PHP lower bound against this filter; then prove or refute exact lower-bound preservation under the required 3-CNF encoding and every native mixed shortcut. Historical byte acceptance, exact optimum, all-mixed asymptotics, B1/B2/B3 and P versus NP remain OPEN.

Report: `research/main/2026-11-06_1648_MAIN_HALL_KERNEL_SHORTCUT_AUDIT_REFEREE397.md`

Code/raw: `experiments/review/lspv5_397_hall_kernel_*` and `results/raw/review/2026-11-06_1648_LSPV5_HALL_KERNEL_AUDIT397*`.
