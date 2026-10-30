# LSPV-1 SIGNED-NAE-DUAL-MATCH242 | 2026-10-29 23:57 PDT

Active issue: https://github.com/j15marti/pnp/issues/3. Issue #2 equity is paused. Preserve five existing enabled schedules :00/:12/:24/:36/:48 and role-owned files. P versus NP OPEN.

## PROVED/EXACT, restricted, independent referee pending
For a proper original 3CNF consisting of exact complement pairs (D_p, not-D_p), each original variable in two distinct pairs, if the signed cubic dual is balanced, a complete satisfying witness is constructible uniformly in O(N log N + r^2) indexed word-RAM operations and O(N+r log r) bits including source access, matching and verification. BFS on pair-sign parity yields a common variable renaming to monotone NAE; a perfect matching of the cubic dual's bipartite double cover selects one or two incident variable-edges at each pair. Matched edges are TRUE, the other edges FALSE. Reverse renaming and verify all ORIGINAL source clauses. This is a direct constructive restricted reproof of an already-known broader NAE tractability phenomenon, not a new general 3-SAT algorithm. Failed syntactic or balance checks output UNKNOWN, not UNSAT.

For every complement-paired source and every globally consistent assignment a, N0(a)=N3(a), F(a)=F(~a), and F(a)=true precisely when every original clause is middle t=1 or2. Clause-indexed local S_j demands that all literals are true, U_j that all are false; invert local demands explicitly. A pair (D,not-D) has original SS=UU infeasible, SU=US feasible. This is NOT by itself an UNSAT deduction.

## Source-authenticated partial-cube proof
Original C0=(x1 OR x2 OR x3), C3=(not x1 OR not x4 OR not x5), pivot x1, produce non-taut resolvent (x2 OR x3 OR not x4 OR not x5). Forbid entire cube x2=x3=0,x4=x5=1; under it original parents reduce to x1 and not x1, a direct checkable contradiction.

## Hostile controls and actual work
An UNBALANCED signed paired K4 remains SAT (20 complete witnesses), hence balance is NOT necessary. 54/64 sampled K4 signings were unbalanced and SAT. All 20 positive/negative original triple clauses on five variables (K5^(3)) constitute an UNSAT pigeonhole control OUTSIDE strict22; Fano UNSAT also outside strict22. The actual coherent 0^n, 1^n, single/multi-flip and complement N0..N3 trails, per-source occurrence S/U/inversions and four-mode matrices, source-parent resolvent proofs and full source IDs are in the local raw JSON. Exhaustive checks passed: 4,068 pair modes, 10,496 triple modes, 67,960 globally coherent complete-SAT checks, 240 direct non-taut source-parent resolutions, 18 independently replayed DPLL UNSAT leaves.

Same-source fixed-order UP-DPLL selected-operation counts baseline -> recognition+K5+fallback controller (all failed recognition and scans charged): K4 balanced SAT 234->115; Petersen SAT 881->323; K5 UNSAT 955->243; K4 unbalanced SAT 171->392; Fano UNSAT 1741->2315. Finite selected-operation results, not native TM lower bounds or industrial CDCL timings.

## Provenance and limitation
Public proof https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-29_2357_LSPV-1_SIGNED_NAE_DUAL_MATCH242_PUBLIC.tex
Independent compact checker https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-29_2357_LSPV-1_SIGNED_NAE_DUAL_MATCH242_compact.py
Full PDF, 26KB runner and 722KB detailed JSON are locally downloadable ONLY; attempted persistent Library upload failed container_session_unavailable. Raw SHA256 f84c6f2d625665cb9cc9b09f24872f3acd9efa2be45376704c80d0e1465b7d16.
Prior art: Porschen/Randerath/Speckenmeyer SAT2003 10.1007/978-3-540-24605-3_14; Doecker 2019 arXiv:1912.08032; Darmann/Doecker/Dorn 2024 arXiv:2412.03395; Kullmann conflict/hitting clauses. Adopt prior LSPV-1 signed-cycle and LSPV-4 proof-ledger, never claim novelty or P vs NP resolution.

## Role-specific next targets
LSPV-2: investigate strict22 signed-unbalanced paired NAE families without interpreting nonbalance as UNSAT.
LSPV-3: compare exact full 0^n/1^n and inverted flip trials, charge all failed trails.
LSPV-4: audit source-pair discovery, matching, full costs and peaks across RAM/tape, and failed recognition.
LSPV-5: independently attack Hall/edge selection/signs/degree assumptions, reconcile canonical main only with verified balanced ownership markers.
LSPV-1: find an efficiently source-certified partial-cube cut or adaptive constructor for failed-balance signed-dual exact22 residuals, and test net total cost on SAT and UNSAT.

Statuses: PROVED/EXACT restricted elementary constructibility; KNOWN THEOREM broader degree-bounded NAE tractability; COMPUTATIONAL observations; OPEN unrestricted SAT coverage and separation.