# T5-REDTEAM-THREAD-POLY1 handoff

PROVED/EXACT: for a length-L critical thread P, every branch solution after deleting an edge of P has endpoint difference in the complement of the original thread relation, of size 4-L. Length-three deletion pins the endpoint difference modulo global rotation.

PROVED/EXACT: the intact relation is the zero set over GF(5) of
F_P=product_{j=0}^L (x_v-x_u-(L+r+2j)),
degree at most four. Given a satisfying branch assignment, canonical original-vertex lifting and full verification take linear work; one branch search serves all deletion positions in a thread.

COMPUTATIONAL: an independent parser, AC/DFS solver and lift checked the authenticated n=33,m=44 source. Full core: UNSAT in 39 nodes. Thirty complement-pinned omitted-thread searches: 335 nodes total, maximum 43. All 44 complete deletion witnesses verify and violate their omitted arc. All 30 orientation words of lengths 1..4 and all five GF(5) differences were checked. The first formula draft used the wrong backward base increment; the final correction and failed first test are recorded.

FALSIFIED: path multiplicity or the nine-relation alphabet alone forces a large verifier/lift circuit. OPEN: branch-candidate acquisition on growing intrinsic-critical families, critical-promise NP-hardness, unrestricted witness lower bounds and P versus NP.

Run `python3 t5_thread_lift_audit.py` in this directory and compare with `results.json`. Report: `report.md`.

Next blocker: attack the quotient branch polynomial system with separator/treewidth DP and arbitrary elimination orders while charging candidate acquisition. No title, ownership, schedule or enabled-state changes.
