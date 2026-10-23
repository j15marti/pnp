# KROM-PROJECTION-CEILING99 handoff

**Global status:** P versus NP OPEN. PROVED/EXACT representation theorem; COMPUTATIONAL audit; no unrestricted SAT time lower bound.

## Exact result

For every 2-CNF F(X,Y) with s retained variables, existential projection onto X has an equivalent auxiliary-free 2-CNF with at most 2s^2 distinct non-tautological unit/binary clauses. Therefore recursive Krom/2-CNF mediator composition cannot force superquadratic final CNF size in s.

Role 4's mediator family

M_p = AND_i(not a_i or u) AND_j(not u or not b_j)

projects to

P_p = AND_(i,j)(not a_i or not b_j).

Every equivalent auxiliary-free CNF, even with arbitrary clause widths, needs at least p^2 clauses. Since s=2p, the quadratic ceiling is asymptotically tight.

## Firewall

The same P_p has:

- a two-term DNF, (all A false) OR (all B false), with 2p literals;
- the original 2p-clause CNF with one retained mediator;
- an O(p) direct scan.

Thus the Omega(p^2) explicit output is caused by the conjunction of CNF form and no auxiliary variables. It is not one-bit decision hardness. Role 3 SELECTOR-PROJECTION-FIREWALL65 raises auxiliary-free CNF output to exponential, but still has compact DNF, existential CNF, and linear contextual decisions.

## Independent Role 4 audit

For the matched H_(p,lambda) sources, positive lambda is UNSAT and negative lambda has exactly

64 * 7^(p-1) * 3^p

models. The pair differs in one sign word, so it forces one source read, not p reads. A source recognizer decides it in O(p).

## Transport

Only the compatible-model inequality

L_old <= R + H + Q*tau*T_new^{<=}(g)

is used. Materializing the projection costs Omega(p^2) clause writes, but retaining u or using the DNF bypasses it. The output cost cannot be charged to every target solver. Direct inclusion preserves only the actual input-observation bound.

## Ladder

- Fixed-width 2-CNF chain: exact q-field lower bound, linear SCC/scan.
- Projected 2-CNF: exact Theta(s^2) worst-case auxiliary-free CNF size.
- Nonlinear selector projection: exponential restricted output size, compact alternate representations.
- Affine matching plus positive ternaries: explicit parsimonious NP-complete endpoint.
- Arbitrary deterministic superpolynomial time: OPEN.

## Reproducible audit

- Code: experiments/review/krom_projection_ceiling99_audit.py
- Raw: results/raw/review/KROM_PROJECTION_CEILING99_raw.json
- 3,526 assertion-accounted checks
- 340 exhaustive core boundary assignments
- all clauses enumerated through p=4; exact minima 1,4,9,16
- 320 random 2-CNF projections and 2,840 projected assignments
- Role 4 weighted counts through p=8
- 1,048,576 full p=1 source assignments
- zero failures

## Inputs reconciled

- research/agents/lspv-4/2026-10-23_1234_LSPV-4_PROJECTION_BLOWUP59.tex
- research/agents/lspv-4/2026-10-23_2045_LSPV-4_AFFINE_MATCHING59.tex
- research/agents/lspv-3/2026-10-23_2024_LSPV-3_SELECTOR_PROJECTION_FIREWALL65.tex
- research/main/2026-10-23_1148_MAIN_TERNARY_PROJECTION_KERNEL88.tex
- Davis--Putnam 1960; Tarasov 2001; Liberatore 2024; Schaefer 1978

## Single next lemma

Prove a representation-portfolio extraction-or-continuation theorem covering every total uniform exact decider of one fixed NP-complete encoding. It must survive source retention, extension variables, CNF, DNF, circuits, branching programs, SCC, affine elimination, bipolar kernels, caching, learning, and decide-first normalization.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::KROM-PROJECTION-CEILING99 -->
