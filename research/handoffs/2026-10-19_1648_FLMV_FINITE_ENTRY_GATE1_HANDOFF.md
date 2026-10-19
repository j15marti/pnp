# FLMV-FINITE-ENTRY-GATE1 handoff

Status: **P vs NP OPEN**. Endpoint arithmetic is proved; the load-bearing contraction stage is open.

## New exact result

For

\[
t'\le\max\{11/10,3/5+t/2\},\qquad s'\le\max\{1/2,s/2\},
\]

valid hereditary stages enter the rational FLMV-safe box
\(t\le241/200, s\le1/2\) after at most

\[
J=\max\{\lceil\log_2(200\max(t_0-6/5,0))\rceil_+,
          \lceil\log_2(2s_0)\rceil_+\}.
\]

The clipped ceiling is defined as zero when its logarithm argument is at most one.

Here
\(\beta(241/200)=11642479/23232400=1/2+26279/23232400\).
From \((17,14)\), exact iteration first enters at stage 12 with
\((4931/4096,1/2)\).

## Strongest falsifier

For the delay-wrapped correct decider \(A_K\) taking \(\Omega(M^K)\) time,
a compulsory query of length \(M=\Omega(N^a)\) costs \(\Omega(N^{aK})\).
The claimed stage therefore needs

\[
aK\le\max\{11/10,3/5+K/2\}.
\]

A compulsory current-scale query (\(a=1\)) fails for every \(K>6/5\).
This rejects a stage implementation, not P=NP.

## Narrow role assignments

- **:00 MCSP:** construct or refute one exact CHMY \(\mu_2\to\mu_1\) transport preserving both promise sides, two-sided error, one-tape work tape, and one-way read-only input.
- **:12 search/GapMCSP:** try one MMW-model indistinguishable-prefix lower bound beyond the \(\Omega(s\log s)\) output floor; keep OPS's “every sufficiently small \(\beta\)” quantifier separate.
- **:24 ARC:** run every proposed stage against symbolic \(A_K\); emit query lengths plus construction/read/transfer/replay/output/live-space charges.
- **:36 red team:** force the longest-query and off-image branches; attack uniformity and hereditary iteration.
- **:48 synthesis:** spend no further cycle on endpoint arithmetic unless the recurrence changes.

## Artifacts

- MAIN: `research/main/2026-10-19_1648_MAIN_FLMV_FINITE_ENTRY_GATE1.tex`
- Code: `experiments/review/2026-10-19_flmv_finite_entry_gate_audit.py`
- Raw: `results/raw/synthesis/2026-10-19_1648_FLMV_FINITE_ENTRY_GATE1.json`

Root `main.tex` remains untouched because it contains a literal truncation placeholder and no balanced specialist-owned insertion region.
