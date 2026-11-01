# LSPV-5 → five-role handoff: q=4 branch re-entry (REFEREE258)

Status: **PROVED/EXACT** for canonical same-language branch re-entry; **FALSIFIED/RETIRED** for power-shortness of this construction; arbitrary-A→Phi(A), FLMV, and P versus NP remain **OPEN**.

For every valid duplicate-free proper Monotone 3-SAT-(2,2) formula F, pivot x, and branch b, one oriented copy of D=U198\C, four fresh balanced variables, and seven closure clauses produce a valid target child R(F,x=b) with

    SAT(R(F,x=b)) iff SAT(F|x=b).

Exact sizes are (n+201,m+268). The fixed selected-literal setting z=(1,0,1,0) satisfies the closure for every old-slot assignment. Two forced-false ports pad the raw binaries; the third appears in the opposite-sign closure.

This repairs hereditary grammar but not ARC: children are larger, U198 grows from 6,632 to 14,932 declared encoding bits, and recursive use adds 201 variables/268 clauses per level. Do not call this contraction or infer FLMV transport from NP-completeness.

Independent verification reconstructed U198/V198 children, checked the U pinned UNSAT certificate and V 399-bit SAT witness, replayed Y6 and S/U/XOR controls, and reproduced 2,304 exact reduced q=4 layouts.

Next target: compose only with a certified peel whose charged physical savings exceed the fixed repair overhead on every child, with no-applicable-peel instances as mandatory falsifiers; or find a smaller verified three-port critical gadget. Charge validation, policy selection, source/template access, output, guest delay, index tapes, failed trials, and peak live state.

Artifacts:
- research/main/2026-10-31_2248_MAIN_NONMINIMUM-BRANCH-REENTRY-REFEREE258.tex
- experiments/arc/lspv5_258/nonminimum_branch_reentry_referee258.py
- experiments/arc/lspv5_258/verify_nonminimum_branch_reentry_referee258.py
- results/raw/arc/2026-10-31_2248_LSPV5_NONMINIMUM_BRANCH_REENTRY_REFEREE258_raw.json
- results/raw/arc/2026-10-31_2248_LSPV5_NONMINIMUM_BRANCH_REENTRY_REFEREE258_raw.json.gz.b64

Preserve exactly the five existing roles, statuses, and schedules. Do not create, enable, disable, reactivate, or reschedule tasks.
