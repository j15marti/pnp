# FROZEN-ANTIPODAL-CUT66: Exact source-coherent handoff

**Date:** October 24, 2026. **Status:** PROVED/EXACT within signed two-witness completion; unrestricted deterministic SAT-time separation OPEN.

## Source and result
Work over a proper 3-uniform support H with degree four at each variable, fixed assignment a, frozen signed occurrence sockets and original quota two positive and two negative per variable. Under a, each unfrozen socket e receives a Boolean desired literal truth x_e. To satisfy both a and its complement, every clause must have exactly one or two true literals. Let p_v count pinned true sockets, t_C count pinned true sockets, and f_v,f_C count free sockets. Residual variable supplies are R_v=2-p_v and clause intervals are L_C=max(0,1-t_C), U_C=min(f_C,2-t_C).

**Exact cut theorem:** Feasibility is equivalent to integral lower-bounded circulation and, after local interval checks, to both cut inequalities for all X subset V and Y subset clauses:

```text
R(X) <= |E_free(X, Clauses \ Y)| + U(Y)
L(Y) <= R(V \ X) + |E_free(X, Y)|
```

These are Hoffman cut conditions, not runtime lower bounds. Flow finds a signing or a violated cut in polynomial time. The same construction with costs yields minimum edit sign repair for both a and complement. Earlier MAIN103 has only *one* prescribed witness; earlier LSPV-4 EULER65 has *two* witnesses but **no pins**.

## Discriminating seven-pin instance
The exact eight clause supports, indexed 0..7, are `012,034,135,245,345,125,024,013`. Fix a=all TRUE. Pin (2,C0) true, (0,C1) true, (0,C6) false, (0,C7) false, (1,C2) true, (1,C5) false, (1,C7) false. In the program's flattened occurrence order these are pin indexes `{2:1,3:1,6:1,15:0,18:0,21:0,22:0}`.

Every variable is individually quota-feasible and every clause individually has L<=U. But variable 0 and variable 1 each require that its only free socket, in C0, be true. The third C0 socket is already pinned true. Hence no double-witness solution. The cut `X={0,1},Y={C0}` reads `R(X)=2`, `free edges X to other clauses=0`, `U(C0)=1`; the upper cut 2<=1 fails.

## Reproducibility
Full standard-library auditor: `frozen_antipodal66_audit.py`, SHA-256 `05a21817a496b8c556060d6c659970ee5414c55d224db8e108eb208450139f8f`, seed 202610240336, provided in the run's downloadable research package. Published minimal reproduction and raw summary under LSPV-4 alongside the LaTeX report. Checks: all 6^6=46656 balanced signings enumerated; 5904 are NAE for a=all TRUE. On 522 pin cases independent brute force and lower-bounded maxflow agreed. On 24 cases all 2^6*2^8 subset pairs were independently checked against flow feasibility. Zero mismatches. Finite tests are COMPUTATIONAL, not asymptotic hardness evidence.

## Explicit transport and cost
n=6,m=k_original=8 for the example; general signed exact-(2,2) has m=4n/3, all clauses genuine ternaries, no SAT-variable auxiliaries, no eliminated variables. The model uses w=ceil(log2(64(n+m+1))) bits per word and N=(4m+2)w. Sign-only edits leave source length constant. Parse, pin discovery, output and witness replay: O(n+m) word work; flow graph linear size, conservative O((n+m)^3) time and O(n+m) peak words; output N bits; cut failure certificate O(n+m) bits, O(n+m) verification. Any optional min-cost variant has polynomial integer-cost bound. The transformation changes signs; it does **not** preserve the SAT label of the original formula.

Baseline: prescribed F_b binary-chain UNSAT iff b=1^q, with q orientation reads only for the declared field-query model. 2CNF plus k ternaries has an exact 2^k polynomial upper bound by choosing one variable per ternary. Padding binary clauses with opposite signs of a fresh variable remains easy. The unrestricted k / signed exact-(2,2) endpoint includes known NP-complete languages, with no lower-bound implication.

## Independent peer tasks
**Role 5:** verify both quantified inequalities and each cut type, audit the frozen socket numbering, test min-cost integrality and the output charges.

**Roles 1-3:** use the seven-pin local/global gap and the polynomial circulation as hostile tests for resource measures based on compulsory compatibility tables, signed entropy, provenance histories, or post-acquisition continuation. Specifically distinguish a sign-changing completion task from an exact SAT decider on unchanged input.

**OPEN:** Establish an all-machine superpolynomial SAT time lower bound that survives direct one-bit decision, SCC/Horn/XOR, matching, flow, caching, source rereads, and signed template recognition. No peer receipt or review is claimed. Do not alter the five-task schedule.
