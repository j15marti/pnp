# 2026-11-19 critical-graphs handoff: native equality bridge
PROVED: extract G(7,20) by removing C(7,20,22), clause index 10, from certified 25-clause native strict-C critical UNSAT source. The unused head 22 has degree one. G has 24 physical clauses, 24 variables, girth 8, terminal incidence distance 6; G is SAT, forces its two terminals equal, and deleting any G clause admits unequal terminals. The prior static 1,046-node UNSAT proof was independently replayed; all 25 physical seed deletion witnesses checked.

PROVED: for every k>=1, chain k disjoint-internal copies G_i(t[i-1],t[i]) and close with C(t0,tk,h). Exact N=23k+2, M=24k+1, incidence girth=8, physically clause-critical UNSAT. All deletion witnesses can be synthesized in O(N) each from seed witness table, verified under ORIGINAL C. Test k=1,2,4,16,64: total 2,093 deletions and 2,523,029 C evaluations passed. Independent verifier reran k=1,4,64 (1,659 witnesses).

Symbolic global cover: first mismatched consecutive terminals selects refutable G_i; if all equal, closing C is refutable. This is not an explicit row bound, the stipulated resource endpoint or a general SAT lower bound. Recognition specialist checks exact canonical source records, replays base proof, emits CERTIFIED_UNSAT or UNKNOWN. It has no free polarity/advice.

CRITICAL GAP: girth stays **8**, so k does not supply growing incidence girth. Search for a *new primitive* high-girth minimally equality-enforcing native-C bridge. Native 150/176 girth-10 source remains without certified clause-critical core. Classical 6-edge-critical high-girth graph route gives existence, not difficult explicit examples.

All code and evidence archived as T5C_Critical_EqualityBridge_20261119.zip. P vs NP OPEN.