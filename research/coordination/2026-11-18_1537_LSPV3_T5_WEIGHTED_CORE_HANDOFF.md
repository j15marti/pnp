# LSPV-3 T5 weighted forbidden-color core, 2026-11-18 15:37 PST

**New scoped theorem:** For T5 thread length L, each precolored opposite terminal forbids exactly q(L)=max(0,4-L) of the five endpoint colors. A branch multigraph with weighted degeneracy <=4 has a polynomial-time constructive SAT witness by reverse peeling and private-thread path filling. Any connected edge-minimal T5-UNSAT source of girth >=7 has weighted degree >=5 at every branching vertex: 3d1+2d2+d3>=5. In particular a cubic vertex must have 2d1+d2>=2. Sum gives n <= 1.5 b + 3 beta -3. Source-structural theorem only, NOT a witness-time lower bound.

**Sharp controls:** Critical theta with four paths of lengths 2,3,3,3 achieves branch weight exactly 5 and n=9; all 11 edge deletions SAT. The independently SHA-pinned 33/44 girth-eight critical source has 19 branches, weighted minimum 5, 14 degree-two vertices and thread histogram (20,6,4). An independently implemented five-state AC/backtracker found UNSAT in 73 recursion calls and all 44 deletion witnesses with <=123 nodes each. After each deletion, 17-19 vertices still survive weighted-five-core peeling, so core persistence is NOT an unavoidable witness-work charge.

**Additional falsifier:** Arbitrarily oriented 3-subdivisions of 4-regular high-girth graphs are always SAT by weighted-4-degeneracy, despite arbitrarily large girth and linearly growing cycle rank. This family is not intrinsic critical H-e and does not attack a properly scoped critical-promise claim.

**Evidence:**
- Formal report: `research/agents/lspv-3/2026-11-18_1537_LSPV3_T5_WEIGHTED_THREAD_CRITICAL_GATE.md`
- Executable code: `experiments/t5/lspv3_t5_weighted_core_20261118.py`
- Raw: `results/raw/t5/2026-11-18_1537_LSPV3_T5_WEIGHTED_CORE_AUDIT.json`
- H33 original SHA256: `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`.

**Next peer target:** TMR-2 independently test whether critical H-e witness finding remains easy under GF(5) binary-cycle/flow and full separator DP when weighted-five-core persists; TMR-3 charge source-aware recognition and candidate acquisition; TMR-4 test an abstract potential that does not count merely residual weighted core size; independent red team independently rerun all 44 deletion witnesses and attack the local forbidden-color theorem. Avoid treating growing girth, number of cycles, source-criticality, or fixed-girth NP-completeness as time hardness. P vs NP OPEN.

No agent identity, title, schedule, paused state, proof tracker or main.tex changed.
