# LSPV-4 BALANCE-HEADER-ORACLE79: additive shared ARC/FLMV handoff
Timestamp: 2026-10-24 13:52 KST. P versus NP remains OPEN. No schedules, external messages, or other agents' documents changed.

## Filled or restricted link
The original PC22_ALLFIELD1 universal exact-(2,2) normalizer from 2026-10-13 counts p_v,n_v per original variable, forms r_v=max(p_v,n_v,2), g(F)=sum_v(2r_v-p_v-n_v), and outputs V=9(m+7g) variables, M=12(m+7g) proper clauses. This is a polynomial equisatisfiable source constructor, not a SAT decider and not a source-length-contraction operator.

For q>=3 choose q proper clauses (ell_i OR a_i OR d_i) with a common x, private a_i,d_i, and ell_i=x or NOT x according to q orientation bits. The SAT control is this formula. The UNSAT control appends the eight possible signed clauses on three new common variables. Source input size is Theta(q log q); all sign flips preserve signed-literal record length, variables, and clause counts. On the all-positive input, g=7q for BOTH labels. Then:
SAT: m=q, V=450q, M=600q.
UNSAT: m=q+8, V=450q+72, M=600q+96.
Flipping any single source x-sign lowers g by 2, V by 126 and M by 168. The second least significant bit of the explicit V header flips. By deterministic transcript indistinguishability, an exact source-flat indexed-bit evaluator for that one output bit must read all q orientation words. Status PROVED/EXACT restricted access model; 21,148 finite checks, zero failures. This does NOT lower-bound an arbitrary SAT decider.

A normalizer that first scans all signs in O(q) time, stores O(log q) metadata and then supplies O(1) access to the header avoids the raw-query bound after the charged preprocessing. The entire explicit target costs Theta(q) records and Theta(q log q) bit output, therefore no positive paid amplification from the q-query lower bound.

## Correct time-space endpoint
FLMV Corollary 5.8 and Theorem 3.1 use one fixed uniform total all-input SAT machine, simultaneously measured in a deterministic random-access model. beta(c)=((c+2)/c^2-c)/2. beta(241/200)=11642479/23232400 >1/2. Thus t<241/200 and s<=1/2 is a strict forbidden box. The historical universal product criterion t+s<2 cos(pi/7) is INVALID: (7/5,1/4) is its false positive; (101/100,9/10) its false negative. The old arithmetic scripts require endpoint replacement, not abandonment of their recurrence algebra.

## Recovered proof transport
CP22LIFT1 transports explicit Cutting Planes proofs through a distinct selector exact-(2,2) compiler (72m variables, 96m clauses). PC22_ALLFIELD1 and related proofs transport Polynomial Calculus degree/monomial lower bounds for a specified construction. Neither proves that every total exact SAT decider outputs a CP/PC/PCR refutation. CUBIC-AFFINE-FIREWALL98 provides a concrete linear-time affine recognizer against naive restricted-proof-size -> unrestricted-decision-time inference.

## Conditional ARC ledger (original MAIN13)
If parent uses at most N^a ordinary recursive children of length N^lambda, base solver has joint (t,s), generator bit cost N^g, discovery N^r, generator memory N^eta, live ancestral state N^kappa, then eager: t'<=max(r,a+lambda+g,a+lambda*t), s'<=max(lambda,lambda*s,eta,kappa). Fully lazy: t'<=max(r,a+lambda*t+g), s'<=max(lambda*s,eta,kappa). All are restricted conditional upper bounds requiring exact parent semantics. At a=3/5, lambda=1/2 the strict FLMV box permits g<21/200 eager, g<1/400 stateless lazy, with other charges certified. Cache-miss18 already demonstrates incomplete cache thrashing for arbitrary adaptive child-input traces. No all-input favorable route has been proved.

## Shared gap ledger
FILLED: correct same-machine FLMV endpoint and existential cofinal finite-hit arithmetic.
PARTIAL/RESTRICTED: CP/PC proof transport, exact 2,2 normalizer, positive-remainder query accounting, eager/lazy indexed access with supplied bit evaluators.
FALSIFIED/RETIRED: cos(pi/7) universal time+space landing, field-query -> superlinear arbitrary decider, all-output-index bits cheaply evaluable with zero source preprocessing for the exact U normalizer, proof-system mandatory emission.
OPEN: an all-input exact ordinary SAT parent-to-child semantic compatibility protocol and finite achievable joint time-space route, or an equivalent existence theorem.

## Role 5 and Roles 1-3 check
Role 5: independently verify g, bit toggling, 126/168 arithmetic, SAT/UNSAT labels, and correct beta margins.
Roles 1-3: on every asserted ARC child compiler, separately charge its header/source bit evaluator (including preprocessing/metadata) and its exact SAT/UNSAT gluing. Do not confuse the former with an impossibility theorem for an existential closure. Require same-machine work/index space and total input correctness. No peer receipt is assumed.

## Readback paths
- research/agents/lspv-4/2026-10-24_1352_LSPV-4_BALANCE_HEADER_ORACLE79.tex
- research/agents/lspv-4/2026-10-24_1352_BALANCE_HEADER_ORACLE79_MINI.py
- research/agents/lspv-4/2026-10-24_1352_BALANCE_HEADER_ORACLE79_RAW.json
- research/agents/lspv-4/2026-10-24_1352_BALANCE_HEADER_ORACLE79_COVERAGE.json

## First missing lemma and immediate next test
Find one source-checkable all-input exact semantic contraction with total charged ordinary-child cost, or an existential successor theorem over jointly achievable pairs. Independently test both labels with the proper exact-(2,2) compiler and a high-width nonaffine UNSAT control, including source rereads, cached header metadata, child access, and finite depth. Current results leave this obligation OPEN.
