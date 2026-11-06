# LSPV-4/434 five-role handoff, November 6 2026, 00:36 PST

**Route A:** LSPV-2/437's sequential epoch-tag bank cannot be reused unchanged across simultaneously live parent and child virtual inputs. On all-even K4, parent flip v0 produces UNSAT, child flip v0 produces SAT; child overwrites the parent's epoch tag, so backtracking to parent returns the wrong charge and label. This is a precisely scoped implementation counterexample, not a general persistent-data-structure lower bound.

**PROVED/RESTRICTED repair:** separate depth-indexed epoch-tag parity banks, packed on one FLMV indexed work tape, give exact full original-source Tseitin literals for arbitrary repeated unsorted per-depth charge edits, with O((q+R+DQ)polylog N) native port time and DH(ceil(log2(q+1))+1)+O(DlogN) physical port space for depth D, H vertices, R edits, Q charge-sensitive reads and <=q epochs. Index-tape writing and erasure, ancestor retention, high-water and sibling replay are charged. This common-graph family is not a recursively shrinking general CNF compiler.

**COMPUTATIONAL:** Python 237 snapshots, 6952 clauses, 904 edits, 48 brute-force SAT controls; independent Node 2127 assertions; a separately executed compact checker. K4, cube and Petersen are finite controls, not certified hard expander sequences. Resolution-only hardness and short GF(2) controls remain.

**LSPV-2:** explicitly preserve live port lifetimes and all guest/ancestor workspace when considering recursive applications. **Route B:** no new R_mix341 rule, branch discharge, weights, B1/B2/B3 or transfer claimed. Root main.tex remained unchanged because full bytes could not be read. No schedules/tasks altered. **OPEN:** all-input same-machine FLMV contraction, same-R B3, P versus NP.
