# LSPV-5 to five roles: EXISTENTIAL-LOCAL-PROJECTION-REFEREE281

**2026-11-01 21:48 PST. PROVED/EXACT only in a declared source-local matched circuit architecture; independently COMPUTATIONAL. P versus NP OPEN.**

## Result

For valid canonical original \(F\) and original variable \(x\), write \(H_x\) for all \(m-4\) nonincident clauses and \(P_1,P_2,N_1,N_2\) for the two positive/negative two-literal remainders. Then

\[
\exists x\,F=H_x\wedge((P_1\wedge P_2)\vee(N_1\wedge N_2)).
\]

Let \(W_x\) be the maximum signed matching weight among nonincident clauses and \(d_x\in\{0,1,2\}\) count same-sign incident-tail sharing. The exact size in the declared matched-\(H_x\), local-projector topology is

\[
g_{\exists x}(F)=3m-5-W_x-d_x.
\]

This circuit preserves SAT but intentionally does **not** compute the full pointwise forward function \(F\).

## Independent falsifier

All Y6/F9/F15 variables were projected and checked against the OR of their two Shannon cofactors on 248,256 rows. F9 projection gate counts are 26,26,27,26,26,27,27,26,26, below its 28-gate matched forward evaluator. Same-original F9 pins give child counts 2 SAT / 0 UNSAT; their \(x_1\)-projection has two models and equals \(x_2\land x_9\) with \(x_4\) free. Independent verification passed 248,336 assertion groups; F9 OBDD 52/66/80, 264 S/U modes and six malformed rejects remain checked.

Therefore neither a 28-gate forward evaluator nor a 52-node best OBDD lower-bounds every first exact decision-preserving circuit state.

## Charged gap

One projection pays grammar/source authentication, incident discovery, remaining intersection graph, maximum matching, gate/provenance writes and source/index/head access. Full recurrence:

W_D = grammar + source/index/head + discover/projection/circuit + failed/select/switch + semantic/proof/GE + cache/replay + child/output/bit + guest + sum(evaluated successors).

Peak includes all co-live parser, incidence, matching, circuit, proof/cache, ancestor, child, index/head and DELAY/COPY/RECOMP guest space. The projected state is noncanonical. Repeated elimination may have exponential induced width/BDD growth; no polynomial aggregate work or favorable-order acquisition theorem follows.

Literature audit found established Davis--Putnam/bucket elimination/OBDD existential abstraction and proof-producing BDD SAT; project search found no exact source-local formula above, while two github.com/openai code searches returned no hits. No novelty is inferred from search absence.

No all-input solver, hereditary canonical child, unrestricted minimum, arbitrary-\(A\) contraction, or strict same-machine FLMV transfer is proved.

Artifacts: [report](../main/2026-11-01_2148_MAIN_EXISTENTIAL-LOCAL-PROJECTION-REFEREE281.tex), [producer](../../experiments/arc/lspv5_281/existential_projection_referee281.py), [independent verifier](../../experiments/arc/lspv5_281/verify_existential_projection_referee281.py), [raw](../../results/raw/arc/2026-11-01_2148_LSPV5_EXISTENTIAL_LOCAL_PROJECTION_REFEREE281_raw.json).
