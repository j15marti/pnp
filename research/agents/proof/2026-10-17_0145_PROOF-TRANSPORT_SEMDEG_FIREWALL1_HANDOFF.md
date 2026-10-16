# PROOF-TRANSPORT SEMDEG-FIREWALL1
2026-10-17 01:45 Asia/Seoul.

Prior proposals: fixed-degree semantic verification hardness; promised Mobius reconstruction; formal quotient witness; arbitrary-decider escape audit.

Search: latest project chats and local files, GitHub history and all-field compiler reports, Google Drive's Semantic Schaefer and BIG_PICTURE reports, Grochow-Pitassi IPS and Boolean-degree literature.

Result: For each fixed prime p and fixed r>=0, checking whether the Boolean multilinearization of a division-free arithmetic circuit has degree<=r is coNP-complete. For a CNF F, form its small SAT-indicator circuit A_F and multiply by r+1 fresh selector variables. The output is the zero Boolean function iff F is UNSAT; if F is SAT its multilinear degree exceeds r. Membership has a polynomial witness: a nonzero mixed Boolean finite difference of r+1 variables.

Separately, Boolean-black-box exact degree testing needs 2^N deterministic queries, and Omega(2^N) randomized bounded-error queries, using point delta functions with O(N)-gate circuits. Under a *given* low-degree promise, coefficient recovery from weight<=r assignments is polynomial for fixed r. Without that promise the construction fails on product_i x_i.

Audit PASS: 2,907 field/formula/bound tests, 18,552 source Boolean checks, 480 promised cases, 117 false-promise checks, and 12,000 sampled query trials.

Limit: syntactic certified low-degree proof lines are still replayable, but arbitrary compact lines with semantically low degree cannot be credited without verification costs. This is a restricted interface result; arbitrary-decider proof transport remains open.

Next: charged, deterministic Boolean-ideal quotient witnesses with exact field, expansion cost and same-realization accounting.

Full local report: 2026-10-17_0140_PROOF-TRANSPORT_SEMDEG_FIREWALL1.md.
