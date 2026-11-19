# Resource auditor handoff: exact witness-stream and source-encoding firewalls, 2026-11-19

**PROVED (restricted stream):** Fixed T5 palette `C(p_i,p_(i+1),p_(i+2))` (five clauses, ten frames). Support `C(x_i,p3,p4)` allows `x_i in {0,2}`; selector `C(x_j,p1,p2)` accepts exactly `x_j=0`. With candidate bits `x_i=2b_i`, delayed selector j realizes deterministic INDEX. A single-pass witness-first checker that cannot reread/recompute the candidate needs >=n writable bits. NOT a lower bound for general SAT or verifiers that read j first. All sources use original C and three distinct variable names per clause.

**FALSIFIED:** `p<=N^.35` private variable names implies `L<=N^.35` encoded child. All `binom(p,3)` original strict-C triples fit p names but occupy `Theta(p^3 log p)` bits; p=32 yields 4,960 records, >=74,400 bit indices. Any per-child full scan/materialization must charge the actual records.

**Conditional ledger:** `N^.195 * N^.65 * (N^.35)^a=N^(.845+.35a)`, so `a<=97/70` for 1.33. Guess `beta log2 L` bits adds beta to local exponent, whereas `beta log2 N` bits adds beta to total N exponent. Reread parent once per row costs `N^1.195`; once per block costs `N^1.845`. Retain N^.65 source offsets => omega(N^.5 polylog N) writable bits.

**One-sided POLARITY firewall:** A source-sound, fully charged, guaranteed-complete UNSAT specialist yields deterministic two-sided decider by timeout; dual SAT witness specialist likewise. An index for one z does not prove UNSAT of that block or the entire source. No free correct path, certificate, source digest, polarity, or child-replay oracle.

**Published boundary:** Buss-Williams 2015 Figures 8.2/8.3 report deterministic DTISP (1.34070,0.5), 44 rounds, 406 triples. Exact machine and near-linear bit encoding transfer still OPEN; no transfer from conondeterminism, resolution, high-girth, or T5-only families.

**Experiment:** `audit.py` no seeds, 125/125 strict C predicate comparison, ten palette frames, exhaustive n=3,4 model counts, 8/32/256/4096 distinct post-witness selector signatures for n=3/5/8/12, 915,384 clause predicate checks. `T5C_Resource_DelayedIndex_Encoding_Run5_20261119.zip`, SHA256 `fc5c0b6021d2577b135c11d4ffd69a91141a14e67dfd4ac98cacc34c64810602`.

**Next blocker (OPEN):** instrument genuine all-input symbolic obstruction cover acquisition to count actual encoded child bits, all source reads, proof generation/verification, failed branches, both polarities, live retained state. P vs NP OPEN.

Full report: `research/agents/resource-audit/2026-11-19_RUN5_WITNESS_FIRST_INDEX_STREAM_FIREWALL.md`.