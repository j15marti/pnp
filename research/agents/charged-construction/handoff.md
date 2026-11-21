# charged-construction handoff
Updated 2026-11-21 08:39 PST, America/Los_Angeles.

Current report: [T5-3COL-PRIVATE1](PNP_Charged_construction_2026-11-21_083900_Three_Color_Private_Leaves.md).
Baseline 10d2ccb2062c3efd4b4f03873eaa88822edf732f; recovery head c4b8923cb7437f2794fa0da3181be3795dd2e35b. First repository handoff for this namespace; latest saved old Construction 07:33 Boolean-module report recovered, not overwritten.

PROVED/EXACT, independent review pending: any simple graph G maps to strict symmetric C using five anchors, two private domain leaves per vertex, and one private leaf per edge. At a valid anchor frame, the exact leaf projection is three-coloring on {a2,a3,a4}. n=5+3v+e, m=5+2v+e; original target bit N is explicitly tracked. Both SAT and UNSAT occur.

Exact count is 10 times a WEIGHTED color sum: vertex weights (2,1,2), edge matrix [[0,2,1],[2,0,2],[1,2,0]]. FALSIFIED/RETIRED only a constant multiplier depending on v,e: path4/star4 each have 24 colorings and N=270 but T5 counts 6400/7680. No parsimonious #3COL reduction asserted.

COMPUTATIONAL: 1100 graphs v<=5, 3241056 exact interface rows; 67 UNSAT images, 1033 SAT images. Seven controls in all ten frames and under renaming/reordering; full brute force only for empty and one-isolate formulas. Code experiments/t5_construction_3color_private1_20261121.py; raw results/raw/t5_construction_3color_private1_20261121.json.

Feature beyond matching/NAND: global three-color compatibility and both labels. Cheap leaf elimination leaves the arbitrary graph core; it is allowed, not charged as exponential work. Graph width, witness counts and NP-completeness do not prove a runtime lower bound. Anchors have high occurrence; do not call this a bounded-occurrence T5 reduction.

ONE next dependency to Accounting, review by Redteam: T5-3COL-DYNAMIC1. Declare a graph distribution/subfamily and actual information-transfer obligations U_j,B_j,Pi_j,b,r that remain compulsory after leaf elimination, sharing and relocation; exceed brKN^a or falsify the candidate. No such lower demand currently exists. Synthesis should retain this as a separate decision branch.

No manuscript ownership or edits. No checkout/preflight/LaTeX build. Same-solver cap ceilings remain unchanged. P versus NP OPEN.
