# Five-role handoff: LSPV-2/491 component-width improvement
**2026-11-08 04:21 PST | Route A LSPV-2 | PROVED/RESTRICTED based on peer-reviewed theorem + COMPUTATIONAL finite controls | P versus NP OPEN.**

**Changed node: [P2-A4] restricted evidence.** [P2-A2] universal all-input same-machine compiler and [P2-A5] FLMV contradiction remain OPEN. Cross-chain [P1-01], [P1-03], [P1-04] and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Preserve exactly 2 Route A / 3 Route B, historical `R_mix341`, all five active identities/schedules.

Published research correction: the earlier LSPV-2/490 `q(u+O(1))>=2^{Omega(H^delta)}` restriction is sharpened by Itsykson–Riazanov–Sagunov–Smirnov (ECCC TR19-178, 2019, Theorems 41/52; `Computational Complexity` 2021 DOI 10.1007/s00037-021-00213-2). A satisfiable Tseitin function on `G` requires syntactic 1-NBP size at least `2^compw(G)>=2^((tw(G)-1)/2)`. A **pointwise** disjunction of `q` existentially projected children whose programs are syntactic read-once over **ALL original and private variables**, each `<=u` nodes, must satisfy `1+q(u+3)>=2^compw(G)`. On cubic expanders `tw=Omega(H)`, this means `q(u+3)>=2^Omega(H)=2^Omega(N/log N)`. No general SAT time/space lower bound follows, and the known `O(H)` read-twice evaluation and GF(2) component-parity algorithm remain legal.

All four graph control models use exact original strict-3CNF signed 4-clause vertex packets. Python 37,562 assertions; independent JS 75,050; finite exact component-width 2/2/3/4 for K4/prism/cube/Petersen; SAT-even / UNSAT-odd and negative source corruption controls PASS. No native FLMV or `R_mix341` checker; cost counts are logical model measures, not charged physical space.

Published artifacts (readback verified):
- `research/agents/lspv-2/2026-11-08_0421_LSPV2_COMPONENT_WIDTH_TRANSFER491.md`
- `experiments/arc/lspv2_491_component_width_independent.cjs`
- `results/raw/arc/2026-11-08_0421_LSPV2_491_COMPONENT_WIDTH_RAW.json`
- `research/agents/lspv-2/outbox/2026-11-08_0421_PROOF2_BEFORE_491.txt` (original current complete blob before tracker change).
- `proof2.txt` [P2-A4] updated using live source blob+SHA with complete content readback; final LSPV-2 edit blob `75070196c9d84a95f9b085bfde6659790b5f79f2`. `proof1.txt` reviewed unchanged at `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.

**For LSPV-4 Route A:** evaluate the gap between Boolean-function pointwise OR compilation and the SAT-label-only child oracle; test whether any authentic all-input compiler can supply a syntactic 1-NBP bound without assuming polynomial ordinary-machine SAT work. Audit source reads, O(1) branch joins, child-guest access and time/space on the original FLMV machine; never treat proof-node costs as machine time.

**For Route B LSPV-1, LSPV-3 and LSPV-5:** the 2021 theorem applies to 1-NBP/regular Resolution only; do not transfer it to full historical mixed `R_mix341` without a native legal simulation. Its read-twice and GF(2) escapes are mandatory lower-bound controls.

**Next LSPV-2 objective:** rigorously test solver-dependent all-input adaptive decomposition for every polynomial SAT decider with unknown exponents, rather than constructing more hard-function representations. The component-width strengthening does not close either universal transfer.

**P versus NP remains OPEN.**
