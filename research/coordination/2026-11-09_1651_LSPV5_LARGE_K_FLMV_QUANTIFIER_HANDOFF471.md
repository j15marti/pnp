# LSPV-5/471 handoff: fixed-finite exponents versus a uniform iteration count

**2026-11-09 16:51 PST | Independent red team | CONDITIONAL arithmetic theorem + COMPUTATIONAL controls | P versus NP OPEN**

## Exact result

Assume, without asserting, the open same-machine all-input transformation [P2-A2]

$$
t_{r+1}\leq\max\left\{\frac{11}{10},\frac35+\frac{t_r}{2}\right\},
\qquad
s_{r+1}\leq\max\left\{\frac12,\frac{s_r}{2}\right\}.
$$

For every **fixed finite** initial pair $t_0\ge6/5$, $s_0<\infty$, some finite number of recursive applications reaches $s_r\le1/2<\beta(t_r)$. The required number of rounds grows only logarithmically in the initial exponents. However, **no one finite round works uniformly over all finite $t_0,s_0$**. For any fixed $r$, choosing $t_0\ge6/5+2^r(c_\dagger-6/5)$ keeps $t_r\ge c_\dagger$, where $c_\dagger$ is the unique root above $6/5$ of

$$
c^3+c^2-c-2=0,
\qquad c_\dagger=1.2055694304005903\ldots,
$$

and hence $\beta(t_r)\le1/2$. This answers the large-$k$ question: P permits an arbitrarily large **fixed** exponent across algorithms; it does not permit a single exponent $k(N)\to\infty$ while remaining polynomially bounded. The proof may select a finite $r$ after fixing the hypothetical algorithm, but the transformation must itself be uniform, effective, recursively closed and exponent-oblivious.

## Red-team correction

Knowing $T(N)=O(N^k\operatorname{polylog}N)$ does not determine $S$. Conditional on any such decider, a language-preserving wrapper may touch $N^q$ fresh work cells for any $q\le k$ before running the decider; it retains the same time exponent but forces peak space $\Omega(N^q)$ on the exact model. FLMV supplies a necessary simultaneous lower bound, not an exact space function. A nondeterministic NP verifier remains a separate existential-branch model and cannot discharge deterministic UNSAT or inherit the deterministic recurrence.

## Evidence and next target

- Report: `research/agents/lspv-5/2026-11-09_1651_LSPV5_LARGE_K_FLMV_QUANTIFIER_AUDIT471.md`
- Exact Python: `experiments/review/lspv5_471_large_k_flmv_recurrence.py`
- Independent Node: `experiments/review/verify_lspv5_471_large_k_flmv.mjs`
- Raw: `results/raw/arc/2026-11-09_1651_LSPV5_471_LARGE_K_FLMV_RAW.json`

The precise remaining gap is still [P2-A2]: construct the concrete same-machine solver transformation with complete configurations, both-label/malformed correctness, all-phase peak space, source authentication and recursive closure. Arithmetic cannot substitute for it. No task identity, route allocation, schedule, enabled state, R_mix341 grammar or weight changes.
