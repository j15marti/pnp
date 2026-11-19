# Agent handoff: source-verifiable spectral global obstruction covers

2026-11-19. **PROVED restricted all-z theorem; VERIFIED physical source; OPEN criticality/resource endpoint/P-vs-NP.**

**New exact theorem:** Let a projectable strict-C original source have simple d-regular projected graph on n shared vertices with adjacency A. For integer t with `A+t I >= 0` and `d>4t`, **every** shared assignment z violates at least
`ceil(((d+t)*S5(n)-t*n*n)/(2*n))`
projected edges, where `S5(n)=(5-r)*floor(n/5)^2+r*ceil(n/5)^2, r=n mod 5`. Each equal-endpoint original C clause fails for all five private-head colors. Group heads into disjoint blocks of at most s: **every z has >=ceil(Mmin/s) different refutable blocks**. Proof uses indicator-vector quadratic form and C projection, not sampled rows.

**Physical Paley109 evidence:** A deterministic shuffled original-C source with 2,943 physical clauses, 3,052 variable names (109 shared), d=54, lambda=26, mu=27. The integer source-checked identity `A^2+A=27I+27J` and t=6 yield **at least 328 bad original C clauses for EVERY z**. Block size s=16, block count B=184<=N^.65, and at least 21 refutable blocks per z. **One symbolic proof root is not one literal shared-assignment row.** This source has incidence girth six and is *not clause-critical*: deleting as many as 327 clauses preserves UNSAT. Independent audits: 11,881 matrix identity entries, 109 exact positive Bareiss minors, 735,750 original-C head evaluations in 50 deterministic samples. SAT K5/K6-e complete original-C witness controls passed; nonprojectable intrinsic UNSAT appropriately returns UNKNOWN. Seed 2026111904. The complete reproducibility ZIP is `T5C_Spectral_ManyBlock_Global_Cover_20261119.zip` in this conversation.

**Uniform independent solver:** `general_spectral.py` reads arbitrary original source, discovers private heads, checks projected d-regular graph and all t attempts, verifies exact integer positive-definiteness by fraction-free Bareiss, emits UNSAT certificate or UNKNOWN. No family labels, oracle, polarity advice or successful path. Whole-process measured general path for Paley109: 1.48 s and 97,548 KiB peak RSS (machine-specific). The fast strongly-regular branch accepts a tiny source-checkable d/lambda/mu/t certificate; low-writable-space via repeated rescans is feasible but high-polynomial-time and not benchmarked. **No N^1.33-time/N^.5-space result**.

**Growing incidence girth without hard cover acquisition:** Classical *nonbipartite* LPS Ramanujan graphs at p=101, degree102, have min nontrivial eigenvalue >-21 and graph girth Omega(log n). After private-head original-C encoding, incidence girth is Omega(log N), yet the exact general spectral specialist acquires a polynomial-time global proof with >=1.8n monochromatic source edges for each z, and <=N^.65 blocks asymptotically. This uses published graph theorems (not a finite LPS implementation); LPS instances are also heavily noncritical. These are counterexample controls against transferring growing girth alone into a hard-cover claim.

**Next proof obligation:** Reconcile the symbolic all-z proof with the exact semantics of the <=N^.195 *row* condition, then seek a comparable source-checkable selector on *clause-critical, growing-incidence-girth* strict-C sources under complete source/index/certificate acquisition, replay and peak live writable-space accounting. No inference from proof-system hardness or restricted graph family to unrestricted SAT is justified.

Full report: [spectral global cover](https://github.com/j15marti/pnp/blob/main/research/agents/strict-c-cover/2026-11-19_SPECTRAL_MANY_BLOCK_SOURCE_GLOBAL_COVER.md).
References: Lubotzky-Phillips-Sarnak, *Ramanujan Graphs* (1988), https://doi.org/10.1007/BF02126799; nonbipartite exposition https://math.berkeley.edu/~zstier/LPSRamanujanGraphs.pdf.

P versus NP remains OPEN.
