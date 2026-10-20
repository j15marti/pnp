# Hourly check — 2026-10-20 08:43 UTC (17:43 KST)

**Global status: P versus NP remains OPEN.** (Nothing here changes any proof status.)

## New since last check
- Only one new commit on `main`: `5f1a23b9` "ARC GLUE4 exact raw counts" — adds
  `results/raw/separation/2026-10-20_1724_ARC_SIGN_COLOR_GLUE4_summary.json`
  (1545 tests, 0 failures; 255/256 subsets SAT, 1 UNSAT; Horn and dual-Horn colour
  projections SAT on every proper 3CNF; shared-witness conjunction equals the source).
  Status as recorded: restricted theorem; all-input ARC contractor OPEN.
- Preceding hour: MMW-QUERY-ABSORPTION19 (conditional cofinal-`k` absorption theorem),
  REDTEAM37 (conditional EXP-witness compactness firewall), independent Grok 4.7 review annotation in `main.tex`.
- No open PRs were inspected as load-bearing; research branches `research-magred-*` exist on origin.

## Own angle (documented, not a proof claim)
Weakest arrows per the v19 DAG: (a) SAT -> one-way ordinary MKTP transducer `R_k` with common
`rho<1`; (b) arbitrary SAT decider -> hereditary charged ARC successor. Observation on the
absorption arithmetic: composite peak space is `n^{max(rho, aC/k)+o(1)}`, so any cofinal family
needs `rho<1` *uniformly in k* — a `rho_k -> 1` family (typical of naive replay buffers) gives no
contradiction. Suggested hostile control: tabulate the best known SAT->MKTP streaming
constructions' `rho_k` and check whether `sup_k rho_k < 1`; if buffering the source costs
`rho=1`, the route collapses to the ARC arrow. CANDIDATE control only; not run today.

Literature note: relevant primary sources are already audited in MMW-QUERY-ABSORPTION19
(McKay–Murray–Williams STOC'19 Thm 4.2; Oliveira–Pich–Santhanam; Ilango 2023). No new search performed this hour.
