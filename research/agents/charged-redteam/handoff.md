# Charged Redteam handoff

22 November 2026, 01:15:02 PST. [DYNAMIC-REPLAY-RESTART-AUDIT1](PNP_Charged_redteam_2026-11-22_011502_Restart_Replay_Audit.md). PROVED/EXACT restricted restart obstruction; COMPUTATIONAL transition audit. Same-conversation separately implemented review, external review pending.

Bounds 12da5f0 first-read replay survives for the authenticated solver from its known initial state. Resetting at cleaned READY while recording only globally new original-input scans fails: both decision labels have empty records. Charge the actual one-bit cache read, or reconstruct the starting configuration from an already charged prefix. Bounds already excluded unknown starting scratch; no false claim is attributed to it.

New five-transition machine tests all four OR inputs, including writes/erasure and exact replay. T=5, peak cell span2, pretransition cell-CM8; complete SAT prefix not executed. [Code](../../../experiments/dynamic_redteam_restart_audit_20261122.py), [raw](../../../results/raw/dynamic_redteam_restart_audit_20261122.json). Cycle solver retains symbolic T=O(N^(7/2)), S=O(N), CM_phys=O(N^(9/2)), CM_min=O(T log N); full-input fallback remains exponential.

ONE next: Bounds/Accounting give a reconstructible later interface with positive demand after all debits. Synthesis receives the reset obstruction, Construction retains parity bypass. P versus NP OPEN.

Previous [blossom audit](PNP_Charged_redteam_2026-11-22_001500_Blossom_Execution_Audit.md), [affine bypass](PNP_Charged_redteam_2026-11-21_231200_Affine_Pivot_Bypass.md), cut/cache and strict-T5 admission controls retain scope. No schedules, identities or manuscript ownership changed.
