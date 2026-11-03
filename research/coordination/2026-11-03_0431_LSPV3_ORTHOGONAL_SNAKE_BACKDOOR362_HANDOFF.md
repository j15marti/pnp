# LSPV-3 ORTHOGONAL-SNAKE-BACKDOOR362 | five-role handoff
**November 3, 2026, 04:31 PST. Unchanged Rmix341, schedules and task identities. P versus NP OPEN.**

**PROVED/EXACT internally within fixed Rmix341, independent external academic review pending; COMPUTATIONAL separate Python/Node finite check.** For each integer r>=2, let n=r^2 and H,V be serpentine Hamiltonian paths of an r-by-r square grid. Define Horn-path minimally UNSAT U(P) as first vertex positive unit, n-1 forward implications and last vertex negative unit. With a single fresh selector b, F_r contains b-guarded U(H) and not-b-guarded U(V). Its n+1 variables and m=2n+2 source clauses have deficiency n+1. It is a clause-minimally UNSAT, individually occurrence-sign-sensitive, width<=3 CNF whose primal graph contains the whole grid, tw>=r-1. Assigning b in either direction leaves a minimally UNSAT Horn chain of treewidth 1, hence {b} is a minimal strong Horn and strong tw1 backdoor.

**New exact mixed-system global optimum**:
$$
W_{R_{\mathrm{mix341}}}(F_r)=2r^2+1=m-1.
$$
Every source is indispensable, so the source-ancestry indegree inequality q>=m-1 applies to every permitted mixed proof DAG, despite shared nodes, adaptivity, GF(2), conservative charged definitions and temporary growth. An explicit strict binary-Resolution proof derives b using n path pivots, derives not-b in another n, and resolves them in one final pivot. This yields q=m-1, attaining the global minimum. Encoded input N=Theta(r^2 log(r+1)) bits. This **falsifies high primal tw + high deficiency + individual sign sensitivity + minimal UNSAT as jointly sufficient for superlinear mixed logical cost**. It is a FAMILY FAILURE of an indicator, NOT a worst-case lower bound or a B3 counterexample.

**Overlaps and novelty discipline:** LSPV-1 STRONG-BACKDOOR-DUAL-CORRIDOR354 previously gave a high-tw, high-deficiency, low-backdoor sign-sensitive grid MUS with only a proof-cost interval. LSPV-1 ADAPTIVE-BACKDOOR-TREE-EXACT355 already supplies general branch lifting. LSPV-3 DP-WIDTH-UPPER361 remains a valid *one-way necessary condition*. This new instance gives a simple exact optimum at the universal source floor with **two orthogonal Hamiltonian snakes**. General backdoors and treewidth upper methods are established, not claimed as academic discoveries. Related literature: Gaspers--Szeider 2012; Fomin et al. SODA 2015; Cai--Li arXiv:2610.02047 (October 1 2026).

**Controls:** Eight sizes r=2,3,4,5,6,8,12,16. Separate Python producer and no-import Node checker tested 1,116 authentic signed RES nodes, 1,124 source-deletion SAT witnesses, 3,340 occurrence-flip repairs, 11 malformed or corrupted cases; 392,399 independent assertions. First two sources were exhausted over every complete Boolean assignment. Full local 484,293-byte raw JSON, SHA256 4efb68d61bf6e6af0c65374014911e0b95aa78c35f57133fbb328839612d5a72, is in conversation reproducibility ZIP along with both scripts. Public compact JS and public JSON summary are independently readback-verified and should not be represented as the full local independently checked suite.

**Published paths:** 
- research/agents/lspv-3/2026-11-03_0431_LSPV-3_ORTHOGONAL_SNAKE_BACKDOOR362.tex
- experiments/arc/lspv3_362_orthogonal_snake_compact.js
- results/raw/arc/2026-11-03_0431_LSPV3_ORTHOGONAL_SNAKE_BACKDOOR362_summary.json
- research/coordination/2026-11-03_0431_LSPV3_ORTHOGONAL_SNAKE_BACKDOOR362_HANDOFF.md

**Next work split:** LSPV-1 keep same-preselected-R B3 and correct quantifiers; LSPV-2 search nonaffine candidate families with no small adaptive Horn/treewidth backdoors and test mixed shortcuts; LSPV-3 seek a superlinear excess invariant surviving all representations (this run excludes geometric indicators alone); LSPV-4 distinguish proof DAG node count, evidence bytes and schedule/acquisition costs, all-phase rho; LSPV-5 red-team all-size proof, width and sign-sensitivity claims and coordinate literature overlap. No task identities or scheduling changed, no legacy roles activated. B1/B2/B3 and superpolynomial Wbar_R OPEN, P versus NP OPEN.

**Safe fallback:** Root main.tex connector reads yielded empty content with a valid blob SHA even when ranges were requested, so no potentially destructive owner-region rewrite was attempted. Repository checkout/preflight failed due local DNS, and full local raw archive is not claimed published to GitHub. These are documented incomplete administrative steps, not mathematical proof gaps.