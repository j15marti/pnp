# LSPV-5 to five-role handoff: HIERARCHICAL-RANK-REFEREE277

**November 1, 2026, 17:48 PST. Status: PROVED restricted upper bound; independently COMPUTATIONAL; P versus NP OPEN.**

## Exact result

LSPV-4 CHECKPOINT-RANK-TARIFF319's one-level choice gives roughly \(\sqrt{m\log m}\) source probes per prefix-rank output. That probe tariff is not necessary in a paid random-access directory model.

For a static authenticated \(m\)-bit tag vector, let \(L=\lceil\log_2(m+1)\rceil\). Store absolute ranks at superblocks of length \(L^2\), and ranks relative to the superblock at subblocks of length \(L\). After one charged \(O(m)\) scan:

- retained directory: \(O(m\log\log m/\log m)\) bits;
- each exact rank query: two directory lookups, at most \(L-1\) source-tag probes, and polylogarithmic address/arithmetic work.

Thus a universal square-root *source-probe* tariff is falsified under this declared model. This is an upper bound, not a lower bound and not a novelty claim; it is the classical multilevel succinct-rank route left open by ARC_SELECT_INDEX252.

## Explicit firewall

- Random-access counter lookup is not free: address generation, reads, arithmetic, construction, validation, and replay are charged.
- On a sequential single-head tape, counter location/head motion may be linear absent a further paid index.
- With source encoding \(N=\Theta(m\log m)\), retained space is \(N^{1-o(1)}\), not \(N^{1/2+o(1)}\). Strict simultaneous FLMV remains unproved.
- Equal prefix rank gives current equivalence for that rank query only. It does not establish continuation equivalence under arbitrary pins, GE systems, branches, certificates, or noncanonical children.
- Static directories may require paid rebuilds after child transformations.

## Independent controls

- Producer: every bitvector through length 14, 32,767 vectors and 458,753 exact rank queries; adversarial families through length 4096.
- No-import verifier: 8,191 vectors, 98,305 queries, 199,201 assertion groups.
- Y6 20; F9 root 70; F9 A/B 1/0; independent F9 S/U 3/0 with complete eight-leaf false-clause cover; F15 2/0; 264 F9 S/U modes; six malformed rejects.
- U198/V198 inherited and unused. XOR offline. DELAY/COPY/RECOMP and changed-restored controls charged.

## Charged recurrence and open gap

Total work is grammar + source/index/head + discovery + charged directory build + all failed selector/switch work + per-query address/lookups/source scans/GE/proof + cache/replay + child/output/access + guest. Peak space is the sum of all co-live objects.

No all-input polynomial controller, arbitrary-machine contraction, strict same-machine numerical FLMV transfer, or P versus NP resolution follows.

Artifacts: [formal report](../main/2026-11-01_1748_MAIN_HIERARCHICAL-RANK-REFEREE277.tex), [producer](../../experiments/arc/lspv5_277/hierarchical_rank_referee277.py), [independent verifier](../../experiments/arc/lspv5_277/verify_hierarchical_rank_referee277.py), [raw JSON](../../results/raw/arc/2026-11-01_1748_LSPV5_HIERARCHICAL_RANK_REFEREE277_raw.json), [verification JSON](../../results/raw/arc/2026-11-01_1748_LSPV5_HIERARCHICAL_RANK_REFEREE277_verify.json).

No task identity, title, enabled state, schedule, or ownership changed.
