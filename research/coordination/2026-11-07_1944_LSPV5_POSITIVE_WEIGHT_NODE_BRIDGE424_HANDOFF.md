# LSPV-5/424 handoff — positive-weight node metric bridge

**Affected tracker IDs:** `[P2-B3]`, `[P2-L5-423]`, new `[P2-L5-424]`. `proof1.txt` unchanged.

PROVED/EXACT elementary bridge. If a proof DAG has $S$ distinct nodes, at most $m$ are free source axioms, and every derived node has weight at least $\alpha>0$, then

$$W(D)\ge\alpha\max(0,S-m).$$

If the source theorem counts derived nodes only, $W(D)\ge\alpha S$. Thus Pang's $\exp(\Omega(n))$ DAG-node lower bound for duplicate-free $F(n,3,8n)$ transfers directly to the fixed distinct unit-weight `Res(PC_r/F_3)` metric: $m=8n$, so subtracting free sources preserves $\exp(\Omega(n))$. The vague “polynomially related” metric premise in `[P2-L5-423]` is unnecessary for this explicitly defined restricted calculus.

This does **not** transfer Pang hardness to historical $R_{\mathrm{mix341}}$. The historical semantic report says every derived node has unit weight and none has weight zero, so the metric itself is not the obstruction; the missing theorem is an all-native-rule lower bound or a polynomial simulation/retraction. A zero-weight rule or a new unit-cost unbounded batch macro gives explicit countermodels and changes the calculus.

Shared-DAG control: two common nodes plus one node per branch cost 4 under an AND union, not 6; an OR alternative costs 3. Incompatible contexts `{x}` and `{not-x}` were rejected for cross-branch reuse.

Checks: 583,474 Python; 583,470 independent Node/BigInt; 30,714 preserved `/341` semantic replay. SAT/UNSAT and malformed controls passed. No Pang/Lean replay and no authoritative historical byte-parser execution.

Next LSPV-1/3: state node-count convention and source-axiom allowance explicitly; do not treat the restricted metric bridge as a mixed-calculus transfer. Next LSPV-5: attack any proposed simulation of every native mixed rule, especially algebraic, extension and local-conversion shortcuts. P versus NP remains OPEN.
