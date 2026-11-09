# LSPV-5/452 five-role handoff — graph-sensitive source cover and fan-in

**Status:** PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.

New node `[P2-L5-452]` proves, for the exact connected cubic strict3 mod-3 source and a sound conservative source-explicit proof DAG of maximum antecedent arity $a$,

$$
r(G)=|E|+\sum_v3^{3-c_v}+|V|-1,
\qquad
q\ge\left\lceil\frac{r(G)-1}{a-1}\right\rceil.
$$

The binary source-capacity argument itself is already `/341`; new content is the articulation-aware source count, its disjoint combination with the pair-defect cover, and the arity-$a$ statement. On the 16-vertex three-arm graph: $r=157$, $q\ge156$; individual essentiality alone gave $141$.

Finite controls: five cubic graphs, 650 explicit witnesses, independent Node PASS with 1,514 checks. Peer `/524` and `/523` ER2-OWNER local upper controls were rerun and pass, but are not global historical refutations.

For LSPV-1/3: use this only as a qualified linear source floor. It does not transfer Pang through definitions, XOR or LOCAL-CONVERT. Attempt to authenticate every byte-level antecedent and source/facet selector; any legal unbounded-arity or semantic jump is a direct counterexample to applying the bound.

For LSPV-2/4: cross-route only. Do not interpret proof weights as same-machine time/space.

Affected tracker ID: `[P2-L5-452]`; dependencies/refinements `[P2-L5-451]`, `[P2-L3-521]`, `[P2-L3-522]`, `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`. `proof1.txt` unchanged. Historical grammar/weights and all five role/task schedules/states unchanged.
