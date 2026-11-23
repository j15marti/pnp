# Charged Accounting handoff

23 November 2026, 04:44:38 PST. [Gain normalization ledger](PNP_Charged_accounting_2026-11-23_044438_Gain_Normalization_Ledger.md). GAIN-NORMALIZATION-LEDGER1, PROVED/EXACT for a fixed uniform deterministic program, independent review pending. P versus NP OPEN.

For a rooted spanning forest on q vertices, k edges, c components, paid F3 switching leaves r=k-q+c cotree gains R. The map g↦(nonroot potentials,R) is bijective. Uniform source gains give H(R)=r log2 3 and H(g|R)=(q-c)log2 3. A canonical checkpoint can discard the potentials and raw source while retaining all decision semantics. Its entire suffix cannot decode the original g.

An explicit validation scan has E=2r actual bit reads, fixed-length Pi, b=1,h=0,rho=1, hence E[T]≥r log2 3. Repeated obligations increase rho. The scan is optional and no all-solver decoding necessity is established. Full normalization fits inherited symbolic O(N^7) time,O(N²) span,O(N^9) physical CM,O(N^8) descriptive CM. General exact fallback remains exponential. Zero normalized gains still leave arbitrary quotient three-coloring.

[Code](../../../experiments/dynamic_accounting_gain_normalization_20261123.py) and [raw](../../../results/raw/dynamic_accounting_gain_normalization_20261123.json) check 729 gain vectors, 27 fibers of size 27, 59,049 assignment comparisons, both labels. Native parser/tape/kernel/preflight unexecuted.

Bounds/Synthesis receive the open necessary normalized-state decoder. Redteam receives impossible recovery of discarded g. Discovery receives the normalization audit. Preserve the [scrub](PNP_Charged_accounting_2026-11-23_034000_Cache_Scrub_Ledger.md), [random replay](PNP_Charged_accounting_2026-11-23_024800_Random_Replay_Ledger.md) and [forest](PNP_Charged_accounting_2026-11-23_004800_Forest_Prediction_Audit.md) scopes.
