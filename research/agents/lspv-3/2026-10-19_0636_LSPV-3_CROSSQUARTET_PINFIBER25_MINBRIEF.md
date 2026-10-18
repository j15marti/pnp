# CROSSQUARTET-PINFIBER25 (2026-10-19 06:36 KST)
Independent combinatorial audit, no unrestricted complexity claim.

Four blocks with two clauses each are linked by K4 interblock variables
plus k extra edges on block pairs (0,3),(1,2), for k=1 or 2.
Two crossing 2+2 block partitions each have exactly 4+2k
shared source variables (width 6 or 8). All four intersections
of these splits are nonempty. No unrooted tree can display both.
Exhaustive check: 10,395 binary labelled eight-leaf trees;
225 display first split, 225 second, zero display both.

Repair of known laminar gauge gadget: four canonical NAE clauses per leaf
and one extra NAE clause on each pendant tree edge. For m>=4
the resulting target has n+5m-5 variables, 9m-6 proper
signed NAE clauses, max auxiliary occurrence 8,
and exactly 2^(m-2) satisfying extensions per source model.
The parent gauge equality network is locally eliminable.
Exhaustive 18-variable signed target check: 262,144 assignments,
16 models over four source models, no failures.

Limit: structural displayed-tree obstruction only. It does not bound
minimal semantic separators, show expensive hierarchy discovery,
give an unrestricted SAT runtime lower bound or resolve P versus NP.
Full report, Python checker and JSON are retained in a local ZIP.
