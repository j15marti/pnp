# LSPV-5/436 five-role handoff | 2026-11-08 07:48 PST

**Route B independent red team | PROVED/RESTRICTED ordinary shared-DAG Resolution + COMPUTATIONAL controls | Historical full $R_{\rm mix341}$ and P versus NP OPEN.**

**Affected IDs:** new `[P2-L5-436]`; independently validates and generalizes the ordinary-Resolution transfer in `[P2-L3-503]` and the concurrently published all-$k$ extension `[P2-L3-504]`, refining `[P2-D3]`, `[P2-C3]`, and `[P2-F13]`. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]` remain OPEN. `proof1.txt` has no material change.

**Restricted theorem.** Let $H$ and $F$ be CNFs and let a literal substitution $\sigma$ map every source clause $D$ of $H$ either to a tautology or to a clause containing some source clause $C$ of $F$, i.e. $C\subseteq\sigma(D)$. Then every ordinary shared-DAG Resolution refutation of $H$ topologically backtranslates to one of $F$ with at most the same number of inference nodes. The construction keeps a derived subclause representative, uses at most one Resolution inference per input inference, and preserves sharing. It uses no weakening, semantic oracle, or proof search.

For the LSPV-3/503 gadget, and simultaneously for any disjoint collection of such gadgets as in concurrent `[P2-L3-504]`,

$$
A=(\ell_1\lor\ell_2\lor u),\quad B=(\neg u\lor\ell_3\lor v),\quad D=(\neg u\lor\ell_3\lor\neg v),
$$

the substitution $\sigma(u)=\ell_3$, $\sigma(v)=0$ maps $A$ to the original $C=(\ell_1\lor\ell_2\lor\ell_3)$ and maps $B,D$ to tautologies. Hence $S_{\rm Res}(T)\le S_{\rm Res}(H)$. This transfers only the established ordinary-Resolution lower bound, not hardness against the historical mixed calculus.

**Load-bearing direction.** The reversed containment fails: $F=(x\lor y)\land\neg x\land\neg y$ needs two Resolution inferences, while $H=x\land\neg x\land\neg y$ needs one, although the smaller substituted source is contained in the original clause.

**Independent checks.** Exact LSPV-3/503 executable blob `85801666e30b67132f02af2236904c20188e842d` replayed 1,278 assertions, 40 cases, and 80 negative checks. Independent Python exhausted 1,976 one-step cases, checked all eight signed gadgets, translated and reverified 16 complete expanded-K4 proofs, and rejected two hostile controls. Independent JavaScript reproduced the one-step cases and the 2-versus-1 counterexample.

**LSPV-1/3:** use the theorem only for ordinary Resolution; retain algebraic, extension, branching, and recovered mixed shortcuts as upper-bound controls. The next decisive evidence is original accepted historical bytes for RES, RES-to-factor conversion, LOCAL-CONVERT, DEF facets, and assumption discharge. **LSPV-2/4:** Route A unchanged; this is only a restricted family/reduction control.

Report: `research/main/2026-11-08_0748_MAIN_RESOLUTION_RETRACTION_REFEREE436.md`

Code: `experiments/review/lspv5_436_resolution_retraction_audit.py`; `experiments/review/verify_lspv5_436_resolution_retraction.mjs`

Raw: `results/raw/review/2026-11-08_0748_LSPV5_436_RESOLUTION_RETRACTION_RAW.json`

No historical rule/weight, agent, identity, title, schedule, enabled state, or 2A/3B allocation changed. Root `main.tex` is untouched unless its complete bytes and outside-region preservation can be established.
