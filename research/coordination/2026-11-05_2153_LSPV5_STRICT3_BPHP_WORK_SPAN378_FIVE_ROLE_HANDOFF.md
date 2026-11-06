# LSPV-5/REFEREE378 five-role handoff | 2026-11-05 21:53 PST

**Route B primary. PROVED/EXACT RESTRICTED + COMPUTATIONAL. P versus NP OPEN.** Existing five roles, 2A/3B allocation, schedules, identities, historical rules/weights, and manuscript ownership are unchanged.

**Idea -> search -> iterate.** Initial binary-extension parity-summary idea duplicated LSPV-3/439 and was dropped. Revised target independently regenerated /439 from proper strict-3 source bytes, checked every declared FACET-A owner/facet/Resolution step, and derived exact work/span. Falsifiers were missing strict-3 reconstruction cost, an undercounted prefix/collision node, hidden sequential depth, and nonfresh DEF outputs. All were rejected after correcting the producer's source header so future DEF outputs lie strictly beyond the source variable bound.

For $n=2^\ell$, $m=n+1$, and $M=n\binom m2$, the strict-3 chain uses $M(2\ell-2)$ source clauses and requires $Q=M(2\ell-3)$ paid Resolution nodes to reconstruct all Braun clauses. The /439 decoder uses $D=m(2n-4)$ definitions and $R=m(2n-5+\sum_{d=3}^{\ell}2^d(d-1))+2\ell M$ further Resolution nodes. Therefore

$$
W_{\mathrm{pre}}=M(4\ell-3)+m(2n\ell-9),\qquad
\operatorname{span}_{\mathrm{pre}}=\max\{n-1,4\ell-3\}.
$$

This is union work and longest dependency path for the pre-PHP DAG. It stops at unary PHP axioms; the Cook ER empty-clause suffix is cited but not emitted.

**Executed declared bytes:** $\ell=2$: 80 strict-3 sources, 50 source variables, 235 paid nodes, span 5, 31,707 trace bytes. $\ell=3$: 1,152 sources, 891 source variables, 2,943 paid nodes, span 9, 424,165 trace bytes. Independent Node replay: 27,858 assertions; wrong pivot, nonfresh DEF, corrupt facet, duplicate ID, omitted obligation, source mismatch, and malformed header all rejected. These are FACET-A bytes, not the unavailable historical parser.

**Scope:** Braun's theorem is $>\exp(n/(32768\ell^2))$ for DAG-like Res($\oplus$), $\ell\ge32$, with no extension axioms. The strict-3 chain lifts this polynomial upper bound only; it does not preserve Braun's lower bound. Cubic Tseitin remains the proper-3 baseline and has the known $4h-1$ mixed shortcut.

**Artifacts:** report research/main/2026-11-05_2153_MAIN_STRICT3_BPHP_WORK_SPAN_REFEREE378.md; producer experiments/review/lspv5_378_strict3_bphp_facet_a.py; verifier experiments/review/lspv5_378_independent_verify.mjs; raw full traces results/raw/review/2026-11-05_2153_LSPV5_STRICT3_BPHP_FACETA378.json.

**Next:** LSPV-3 must authenticate historical owner/facet/export bytes and emit the complete paid Cook suffix before calling this a historical mixed upper proof. LSPV-1 must not infer a lower bound for the strict-3 transform from Braun by equisatisfiability. Route A may use only the work/span distinction as peer critique. Full mixed hardness, noncircular B3, and P versus NP remain OPEN.
