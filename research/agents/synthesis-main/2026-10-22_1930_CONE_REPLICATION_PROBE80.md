% NOT an LSPV report; informal hourly-check note (branch ccr-8d8a5ce7-9u4w7i). Root main.tex NOT modified.
# Cone-replication probe 80 (COMPUTATIONAL, restricted)

**Global status: P versus NP remains OPEN.**

Context: MAIN79 (CONE_COVER_REPLICATION79) leaves the all-input hereditary cone-cover compiler OPEN and asks for a replication measurement (alpha=0.6).

Probe: random 3-CNF, m=4.26n, variables split into contiguous blocks of size s=n^alpha (alpha in {0.4,0.6}), n up to 1e5, 2 seeds.
Script/data: `2026-10-22_1930_cone_replication_probe80.{py,json}` (each run < 1 s).

Observed (COMPUTATIONAL): per-clause replication <= 3 (= k, exact for any variable-block partition), mean -> 3 as n grows, so incidence ~ 3m, i.e. replication exponent sigma = 0. Cone size per region ~ 12.8*s (linear in region size).

Interpretation (CANDIDATE, no new theorem):
- This only re-confirms the trivial static variable-block cover; it is NOT a witness-region cover. The MAIN79 requirement is that cones be hereditary for witness regions on every input, which a syntactic variable partition does not provide.
- The sigma<=0.1 budget is therefore not the bottleneck for syntactic covers; the bottleneck remains showing the cover captures witness structure (a non-syntactic, input-adaptive partition) without per-child replay.
- Suggested next test: replace blocks by regions induced by a real WRAPPER witness/coin trace and measure incidence plus direct-decider and SAT-NO controls (MAIN79 :12 role).

No status upgraded; no load-bearing arrow closed.
