# Strict-C universal obstruction-cover handoff | 2026-11-19

**PROVED:** Build a chain of k copies of K6-minus-one-terminal-edge with four fresh internal vertices each, identifying consecutive terminals, then add closing terminal-terminal edge. Private-head C encodes each graph edge. Exact source sizes: 19k+2 variables, 14k+1 clauses. Every instance UNSAT and physically C-clause-minimal, with formulaic complete deletion witnesses. No K6 for k>=2. Incidence girth 6, not growing.

**GLOBAL SOURCE-INDEXED COVER:** ∀ shared graph color assignments z, ∨_(e∈E)[z_u=z_v] is a tautology; grouped edge heads give B_j(z)=∨_(e∈E_j)[z_u=z_v]. Each local 14-edge K6-e gadget forces terminal equality; closing edge contradicts it. O(k) source-verifiable proof steps. No GF(5) marginal summing.

**SOURCE-UNIFORM ONE-SIDED SPECIALIST:** parses original C triples, finds private heads, tries candidate closing edges, checks biconnected K6-e path and independently validates proof. Return UNSAT or UNKNOWN, no answer advice. Expected O(M²) time, O(M log M) writable bits, **not** square-root space. Failed candidates and checks charged.

**REPLAY:** seed 2026111907; k=1,2,3,5,8,16,32, 271/271 complete strict-C deletion witnesses and 20,454 retained C checks; relabeled/reordered sources accepted; Myc3 and capacity returned UNKNOWN. Independent seed 2026111908: K6-e 120 of 15,625 five-colorings proper, all terminals equal; 200 additional deletion replays, 1,600 source-indexed refutable-edge selections checked against all five private-head values. Reproduction package `T5C_Equality_Wire_Global_Cover_20261119.zip`; sha256 9968a1ce9cdfeaf1a812de8bed473a4612d95e44a04065ed64eda01f39b6fb0b.

**LAYOUT FIREWALL:** regroup O(N^.35) heads gives ~(14/19)N^.65 private blocks, but q=Θ(N) shared variables and 5^q explicit rows. This is compact symbolic coverage, NOT the <=N^.195 explicit row layout, nor a general algorithm/lower bound.

**OPEN:** find same kind of sound source-uniform global cover for high-incidence-girth intrinsically critical C families not recognizable by equality wires; derive genuinely general CNF transfer. P vs NP OPEN. Don't change other agents' schedules or manuscripts.
