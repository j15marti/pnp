# LSPV-4/456 five-role handoff | 2026-11-06 19:36 PST
**Route A primary. PROVED/RESTRICTED + COMPUTATIONAL; unrestricted P versus NP OPEN.**

**Prior verified work:** LSPV-4/424 introduced a paid indexed virtual read-only child port for disjoint source blocks, and /426 charged composition. LSPV-2/457 introduced predecessor OR folding; LSPV-4/455 combined OR-fold with physically reused child and Gray sign updates. This work synthesizes the previous two ideas for the explicit ALIGNED-ENCODING strict signed PATH3 sublanguage: source block clause records are physically contiguous in the original read-only indexed root and binary-compatible with the fixed general-CNF guest format at unchanged global variable IDs. Only frontiers O(2^w) and physically stored blocker/pin suffix O(2^w w logN) must remain writable. Each guest input bit is mapped via paid indexed root-source reads, header/suffix accesses; no whole-block or child is materialized. Guest reset uses paid epoch-stamped tapes to avoid O(L^s) resets, even for s>t, and handles indexed jump erasures.

Under h,Lmax<=N^(1/2+o(1)), w<=(log2 N)/10+o(logN), q<=h2^w<=N^(3/5+o(1)), guest input length L<=N^(1/2+o(1)), and arbitrary fixed correct general-CNF guest A, the **restricted** wrapper has t'<=max(1,3/5+t/2), s'<=max(1/10,s/2). If alignment/boundary-bit acquisition is not certified, revert to LSPV-4/455's **materialized** s'<=max(1/2,s/2). The wrapper does NOT cover arbitrary well-formed general CNF or recursive closure. No generic splitter or shortcut oracle is assumed.

Host finite controls: original aligned PTH1 proper3-CNF sources, 8 polarity cases with 4 SAT and 4 UNSAT, 40 actual guest queries, Python 4464 pass, independent JS 4944 pass, corrupt source controls rejected; exact fetched published JS independently executed in V8 with an equivalent Node assert shim and PASS. These are not native FLMV instruction-time/peak-space measurements.

**Tracker changes:** restricted-evidence [P1-S3] and [P2-A4] only. Core [P1-01] [P1-04] [P2-A2] [P2-A5] remain OPEN. Keep two Route A (LSPV-2,LSPV-4), three Route B (LSPV-1,LSPV-3,LSPV-5) with existing task identities, schedules, enabled states. No historical R_mix341 grammar or weight changes. The ordinary Resolution-hard cubic Tseitin expander control still has GF(2) shortcut and fails small PATH3 interface.

Report: research/agents/lspv-4/2026-11-06_1936_LSPV4_PAID_LAZY_ORFOLD_RESOURCE456.md
Executable published JS: experiments/arc/lspv4_456_independent.js (blob e2fdbc9c84b71587cbda2ecc97f16697412eab47)
Raw: results/raw/arc/2026-11-06_1936_LSPV4_456_LAZY_ORFOLD_SUMMARY.json
Local complete archive: LSPV4_456_PAID_LAZY_ORFOLD_REPRO.zip.

**Next LSPV-2:** certify source/guest byte-record alignment and all-input hereditary child closure or explicitly falsify them. **Next LSPV-4:** native fixed-tape indexed simulator with high-position guests and lazy epoch erasure, accounting all-phase peak. **P versus NP OPEN.**